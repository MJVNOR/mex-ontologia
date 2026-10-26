"""Un backend persistente, múltiples sesiones MCP HTTP/stdio. Solo lectura."""
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time
from urllib.request import Request, urlopen
from rdflib.plugins.sparql.parser import parseQuery

ROOT = Path(__file__).resolve().parents[1]
ALLOW = 'onto_query,onto_stats,onto_status,onto_validate,onto_shacl'


def verificar_consulta(q):
    if re.search(r'\b(INSERT|DELETE|LOAD|CLEAR|DROP|CREATE|WITH|COPY|MOVE|ADD|SERVICE)\b', q, re.I):
        raise ValueError('Solo lectura local; escritura y SERVICE rechazados')
    try:
        parsed = parseQuery(q)[1]
    except Exception as exc:
        raise ValueError('SPARQL SELECT inválido') from exc
    if parsed.name != 'SelectQuery':
        raise ValueError('Consulta libre: solo SELECT acotado')
    limit = parsed['limitoffset']['limit'] if 'limitoffset' in parsed and 'limit' in parsed['limitoffset'] else None
    if limit is None or not 0 < int(limit) <= 2000:
        raise ValueError('Se requiere LIMIT entre 1 y 2000')


class Cliente:
    def __init__(self, url, token):
        self.url = url
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream',
                        'Authorization': 'Bearer ' + token, 'MCP-Protocol-Version': '2025-03-26'}
        self.id = 0

    def enviar(self, message):
        req = Request(self.url, data=json.dumps(message).encode(), headers=self.headers)
        with urlopen(req, timeout=120) as response:
            if response.headers.get('Mcp-Session-Id'):
                self.headers['Mcp-Session-Id'] = response.headers['Mcp-Session-Id']
            raw = response.read().decode()
        if not raw.strip():
            return None
        if raw.lstrip().startswith(('data:', 'event:')):
            for line in raw.splitlines():
                if line.startswith('data:') and line[5:].strip():
                    payload = json.loads(line[5:])
                    if payload.get('id') == message.get('id'):
                        return payload
            raise RuntimeError('Respuesta SSE sin resultado de la solicitud')
        return json.loads(raw)

    def rpc(self, method, params):
        self.id += 1
        response = self.enviar({'jsonrpc': '2.0', 'id': self.id, 'method': method, 'params': params})
        if not response or 'error' in response:
            raise RuntimeError(response)
        return response['result']

    def iniciar(self):
        self.rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                               'clientInfo': {'name': 'mex-ontologia', 'version': '0.2.0'}})
        self.enviar({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return self

    def cerrar(self):
        if 'Mcp-Session-Id' in self.headers:
            try:
                with urlopen(Request(self.url, method='DELETE', headers=self.headers), timeout=5):
                    pass
            except OSError:
                pass
            self.headers.pop('Mcp-Session-Id', None)

    def call(self, name, arguments=None):
        if name not in ALLOW.split(','):
            raise ValueError('Herramienta fuera del contrato de solo lectura')
        if name == 'onto_query':
            verificar_consulta(arguments['query'])
        result = self.rpc('tools/call', {'name': name, 'arguments': arguments or {}})
        if result.get('isError'):
            raise RuntimeError(result)
        value = result.get('structuredContent')
        if value is None:
            value = json.loads('\n'.join(c['text'] for c in result['content'] if c['type'] == 'text'))
        if isinstance(value, dict) and value.get('error'):
            raise RuntimeError(value)
        return value


@contextlib.contextmanager
def bloqueo(path):
    with path.open('a+b') as f:
        f.seek(0)
        f.write(b'0')
        f.flush()
        deadline = time.monotonic() + 35
        while True:
            try:
                f.seek(0)
                if os.name == 'nt':
                    import msvcrt
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() > deadline:
                    raise RuntimeError('Tiempo agotado esperando el arranque del MCP compartido')
                time.sleep(.1)
        try:
            yield
        finally:
            f.seek(0)
            if os.name == 'nt':
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(f, fcntl.LOCK_UN)


def conectar():
    manifest = json.loads((ROOT / 'reports/portal-carga.json').read_text(encoding='utf-8'))
    store = (ROOT / manifest['store_dir']).resolve()
    state = ROOT / 'store' / ('mcp-' + hashlib.sha256(str(store).encode()).hexdigest()[:16] + '.json')
    state.parent.mkdir(exist_ok=True)
    with bloqueo(state.with_suffix('.lock')):
        if state.exists():
            data = json.loads(state.read_text())
            try:
                return Cliente(data['url'], data['token']).iniciar()
            except (OSError, RuntimeError):
                pass
        import secrets
        token = secrets.token_urlsafe(32)
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        log_path = state.with_suffix('.log')
        url = f'http://127.0.0.1:{port}/mcp'
        # Publicar la identidad antes de arrancar: un fallo de negociación no
        # debe dejar un backend huérfano cuyo token ya no pueda recuperarse.
        temp = state.with_suffix('.tmp')
        temp.write_text(json.dumps({'url': url, 'token': token, 'pid': None, 'store': str(store)}))
        temp.replace(state)
        with log_path.open('ab') as log:
            flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            proc = subprocess.Popen([str(ROOT / 'tools/open-ontologies.exe'), 'serve-http',
                '--host', '127.0.0.1', '--port', str(port), '--storage-mode', 'persistent',
                '--data-dir', str(store), '--tools-allow', ALLOW],
                env={**os.environ, 'OPEN_ONTOLOGIES_TOKEN': token},
                stdin=subprocess.DEVNULL, stdout=log, stderr=log, creationflags=flags)
        for _ in range(100):
            if proc.poll() is not None:
                raise RuntimeError('No se pudo abrir el almacén persistente. Una sesión antigua puede '
                    'retenerlo; debe reconectarse una vez al nuevo lanzador. Diagnóstico: ' + str(log_path))
            try:
                client = Cliente(url, token).iniciar()
                temp = state.with_suffix('.tmp')
                temp.write_text(json.dumps({'url': url, 'token': token, 'pid': proc.pid, 'store': str(store)}))
                temp.replace(state)
                return client
            except OSError:
                time.sleep(.1)
        proc.terminate()
        raise RuntimeError('El backend MCP no respondió al iniciar')
