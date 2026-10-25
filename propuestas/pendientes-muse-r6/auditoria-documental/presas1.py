import json, hashlib
from pathlib import Path
# 1. xlsx autentico vs inspeccion original
xb = Path('propuestas/pendientes-muse-r6/web/evidencia/cat_estatal_1.xlsx').read_bytes()
print('xlsx sha:', hashlib.sha256(xb).hexdigest(), 'tam:', len(xb), 'magic:', xb[:4])
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
r = insp['4219d141-5084-4308-bda3-d44ca28a4f53']
print('recurso ok:', r['ok'], 'sha_fragmento:', r.get('sha256_fragmento_o_archivo'))
print('tablas:', [(t.get('hoja'), len(t.get('campos', []))) for t in r.get('tablas', [])])
for t in r.get('tablas', []):
    print(' HOJA', t.get('hoja'), 'metodo:', t.get('metodo_encabezado'))
    for c in t.get('campos', [])[:20]:
        print('   pos', c.get('posicion_original'), '=', repr(c.get('id'))[:60])
# 2. diccionario presas: 2 hojas
d = insp['bfb8788b-8ce3-475e-8bbd-dd1c5154c877']
print('dicc ok:', d.get('ok'), 'tablas:', [(t.get('hoja')) for t in d.get('tablas', [])])
print('definiciones:', len(d.get('definiciones', [])))
for row in d.get('definiciones', []):
    print(' -', json.dumps(row, ensure_ascii=False)[:300])
