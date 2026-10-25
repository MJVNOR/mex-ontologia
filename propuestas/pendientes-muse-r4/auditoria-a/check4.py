import json, unicodedata
from urllib.parse import unquote
def norm(s):
    import unicodedata
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[0].rsplit('/', 1)[-1]) if False else int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx-1]
for lote, rid in [('lote-2','r4-lote-2-021'),('lote-2','r4-lote-2-020'),('lote-5','r4-lote-5-023'),('lote-3','r4-lote-3-numero-entrada-registro-24'),('lote-3','r4-lote-3-numero-entrada-registro-35')]:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    r = [x for x in d['reglas'] if x['id']==rid][0]
    dd = r['definiciones'][0]
    dic, idx, row = get_row(dd)
    print('==', rid, r['concepto'], r['descripciones'], r['nombres'])
    for k,v in row.items():
        print(f'  {k}: {str(v)[:200]!r}')
    print('  limites:', r.get('limites', r.get('limite')))
    print()
