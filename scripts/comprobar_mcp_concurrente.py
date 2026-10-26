"""Comprueba consultas concurrentes por CLI y MCP stdio sin abrir otro store."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from mcp_compartido import conectar, verificar_consulta

ROOT = Path(__file__).resolve().parents[1]
QUERY = 'SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o } LIMIT 1'


def cli(_):
    p = subprocess.run([sys.executable, str(ROOT / 'scripts/consultar_ontologia.py'),
                        'sparql', QUERY], capture_output=True, text=True, encoding='utf-8', check=True)
    return int(json.loads(p.stdout)['resultados'][0]['n'])


def mcp(_):
    client = conectar()
    try:
        return client.call('onto_query', {'query': QUERY})
    finally:
        client.cerrar()


def stdio(_):
    messages = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
            'protocolVersion': '2025-03-26', 'capabilities': {},
            'clientInfo': {'name': 'prueba-concurrente', 'version': '1'}}},
        {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
         'params': {'name': 'onto_query', 'arguments': {'query': QUERY}}},
        {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'onto_query',
         'arguments': {'query': 'SELECT ("Educación y atención" AS ?texto) WHERE {} LIMIT 1'}}},
    ]
    proc = subprocess.run([sys.executable, str(ROOT / 'scripts/servir_ontologia_mcp.py')],
        input='\n'.join(json.dumps(m, ensure_ascii=False) for m in messages) + '\n',
        capture_output=True, text=True, encoding='utf-8', check=True, timeout=120)
    responses = [json.loads(line) for line in proc.stdout.splitlines()]
    assert not any('error' in r or r.get('result', {}).get('isError') for r in responses), responses
    assert any('Educación y atención' in json.dumps(r, ensure_ascii=False) for r in responses)
    return True


def main():
    client = conectar()
    tools = client.rpc('tools/list', {})
    names = sorted(t['name'] for t in tools['tools'])
    assert names == sorted(['onto_query','onto_stats','onto_status','onto_validate','onto_shacl']), names
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(cli, range(6)))
    assert len(set(results)) == 1 and results[0] > 0
    with ThreadPoolExecutor(max_workers=6) as pool:
        direct = list(pool.map(mcp, range(6)))
    with ThreadPoolExecutor(max_workers=6) as pool:
        proxies = list(pool.map(stdio, range(6)))
    for q in ('DELETE WHERE {?s ?p ?o} LIMIT 1', 'SELECT * WHERE {?s ?p ?o}',
              'SELECT * WHERE {?s ?p ?o} LIMIT 2001'):
        try:
            verificar_consulta(q)
        except ValueError:
            continue
        raise AssertionError('Consulta inválida aceptada')
    report = {'verificado_en_utc': datetime.now(timezone.utc).isoformat(),
              'clientes_cli_concurrentes': len(results), 'clientes_mcp_concurrentes': len(direct),
              'clientes_stdio_concurrentes': len(proxies), 'utf8': True,
              'triples': results[0], 'herramientas': names, 'ok': True}
    (ROOT / 'reports/mcp-concurrencia.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    client.cerrar()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
