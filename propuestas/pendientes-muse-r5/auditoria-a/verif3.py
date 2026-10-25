import json, hashlib
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
# SHAs exactos vs listo
for f in ['defunciones', 'epidemiologia', 'diversos']:
    p = f'propuestas/pendientes-muse-r5/{f}/entrega.json'
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    lj = json.load(open(f'propuestas/pendientes-muse-r5/{f}/listo.json', encoding='utf-8'))
    lh = lj.get('sha256_entrega', lj.get('sha256_entrega_json', ''))
    print(f, 'entrega=', h[:16], 'listo=', str(lh)[:16], 'COINCIDE' if h == lh else 'DIFIERE!!!')
# filas diversos: 177/178 corruptas, TRIMESTRE, CLASIF, CVOTRAS, Total_Egresos
for iri in ['https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177',
            'https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2',
            'https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5',
            'https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7',
            'https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15']:
    dec = unquote(iri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    print('==', dic[:8], idx, json.dumps(insp[dic]['definiciones'][idx - 1], ensure_ascii=False)[:400])
