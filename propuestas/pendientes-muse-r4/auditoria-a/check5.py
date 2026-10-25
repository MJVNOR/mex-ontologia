import json, unicodedata
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def get_row(defiri):
    from urllib.parse import unquote
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx-1]
d = json.load(open('propuestas/pendientes-muse-r4/lote-1/entrega.json', encoding='utf-8'))
for r in d['reglas']:
    print('==', r['id'], r['concepto'], r.get('representacion'))
    print('  nombres:', r.get('nombres'), 'descs:', [str(x)[:100] for x in r.get('descripciones',[])])
    print('  limites:', r.get('limites'))
    dd = r['definiciones'][0]
    dic, idx, row = get_row(dd)
    for k,v in row.items():
        if any(s in k.lower() for s in ['variable','tipo','formato','unidad','descrip','ejemplo','catalog','identific']):
            print(f'    {k}: {str(v)[:150]!r}')
    print()
