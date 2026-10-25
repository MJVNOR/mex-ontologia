"""Captura HTTP primaria TIC post-R6 (solo escribe en propuestas/investigacion-post-r6/tic/).
Descarga metadatos CKAN package_show de los 8 conjuntos TIC + paginas oficiales
relacionadas, guarda bytes exactos y registra log con URL/fecha/status/SHA256.
"""
import urllib.request
import json
import hashlib
import datetime
import pathlib

REPO = pathlib.Path(r'C:\Users\marti\Documents\MEX-Ontologi')
OUT = REPO / 'propuestas' / 'investigacion-post-r6' / 'tic'
EV = OUT / 'evidencia'
EV.mkdir(parents=True, exist_ok=True)

UTC = datetime.datetime.now(datetime.timezone.utc).isoformat()
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}

CONJUNTOS = [
    'aa353273-7ef0-4279-987a-40fc49b3d712',
    '0ec245ba-6941-4995-a564-52e0a4f3999f',
    '9208a313-553c-4308-8d58-506e037060b1',
    'c9a63b8b-4d70-47db-bfc7-cf86a10b0514',
    'd175b134-77f4-4201-9409-08b05c1d5ffa',
    '37ab8134-d376-4ebd-94cc-f48bcc7eacd6',
    'a3ea3c02-2e31-40b6-a90b-c12be719f9da',
    '7c6183e5-5903-47c6-9fce-34f018bbdb6a',
]

Targets = [('ckan-package-' + c[:8],
            f'https://datos.sonora.gob.mx/api/3/action/package_show?id={c}') for c in CONJUNTOS]
Targets += [
    ('programa-especial-gobierno-digital',
     'https://oficialiamayor.sonora.gob.mx/programa-especial-de-gobierno-digital/'),
    ('diagnostico-entorno-digital',
     'https://www.sonora.gob.mx/datos/diagnostico-entorno-digital'),
]


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={**UA, 'Accept': '*/*'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read(), None
    except Exception as e:
        return None, {}, b'', repr(e)


log = []
for nombre, url in Targets:
    status, headers, body, error = fetch(url)
    fn = f'{nombre}.bin'
    (EV / fn).write_bytes(body)
    sha = hashlib.sha256(body).hexdigest()
    entry = {
        'nombre': nombre,
        'url': url,
        'fecha_consulta_utc': UTC,
        'http_status': status,
        'error': error,
        'bytes': len(body),
        'content_type': headers.get('Content-Type') or headers.get('content-type'),
        'archivo': f'propuestas/investigacion-post-r6/tic/evidencia/{fn}',
        'sha256': sha,
    }
    log.append(entry)
    print(nombre, status, len(body), sha[:16], error or '')

(EV / 'http_log.json').write_bytes(json.dumps({
    'fecha_utc': UTC,
    'herramienta': 'urllib con UA de navegador (equivalente a navegacion directa)',
    'entradas': log,
}, ensure_ascii=False, indent=1).encode('utf-8'))
print('OK entradas=%d' % len(log))
