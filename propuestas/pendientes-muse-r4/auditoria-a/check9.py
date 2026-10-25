import json
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx-1]
def fld(row, key):
    for k in row:
        if k.strip().lower() == key:
            return row[k]
    return ''
import unicodedata
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).lower()) if unicodedata.category(c) != 'Mn')
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        dd = r['definiciones'][0]
        dic, idx, row = get_row(dd)
        tipo = fld(row, 'tipo de dato')
        if 'booleano' in norm(tipo):
            print(f"{r['id']} rep={r.get('representacion')} conc={r.get('concepto')}")
            print(f"   desc={str(fld(row,'descripción') or fld(row,'descripcion'))[:110]!r} ej={str(fld(row,'ejemplo de dato'))[:40]!r}")
