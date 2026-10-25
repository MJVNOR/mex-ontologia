import json
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx-1]
for lote in ['lote-6','lote-5','lote-2','lote-3']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    print('====', lote)
    for r in d['reglas']:
        dd = r['definiciones'][0]
        dic, idx, row = get_row(dd)
        tipo = next((row[k] for k in row if 'tipo' in k.lower()), '')
        fmt = next((row[k] for k in row if k.strip().lower()=='formato'), '')
        ej = next((row[k] for k in row if 'ejemplo' in k.lower()), '')
        desc = next((row[k] for k in row if 'descrip' in k.lower()), '')
        print(f" {r['id']} conc={r.get('concepto')} rep={r.get('representacion')} tipo={str(tipo)[:28]!r} fmt={str(fmt)[:20]!r} ej={str(ej)[:45]!r}")
        print(f"    desc={str(desc)[:95]!r} lim={str(r.get('limites', r.get('limite')))[:160]!r}")
