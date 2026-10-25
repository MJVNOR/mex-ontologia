import json, unicodedata
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).lower()) if unicodedata.category(c) != 'Mn')

def show(iri):
    dec = unquote(iri)
    try:
        dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
        idx = int(dec.rsplit('/', 1)[1])
        row = insp[dic]['definiciones'][idx - 1]
    except Exception as e:
        print('  SIN FILA:', iri[-60:], e)
        return
    t = next((str(row[k]) for k in row if 'tipo de dato' in norm(k)), '?')
    f = next((str(row[k]) for k in row if k.strip().lower() == 'formato'), '')
    e = next((str(row[k]) for k in row if 'ejemplo' in norm(k)), '')
    d = next((str(row[k]) for k in row if 'descrip' in norm(k)), '')
    n = next((str(row[k]) for k in row if norm(k) in ('nombre variable', 'nombre de variable', 'variable', 'nombre campo')), '?')
    print(f'  [{t} | fmt={f!r} | ej={e[:60]!r}] {n!r} :: {d[:120]!r}')

for g in ['tic', 'nacimientos', 'matriculas']:
    a = json.load(open(f'propuestas/pendientes-muse-r5/{g}/asignacion.json', encoding='utf-8'))
    sigs = a['significados']
    print('=' * 20, g, len(sigs))
    n_bool = n_empty = 0
    for s in sigs:
        iri = s.get('definicion_iri', '')
        dec = unquote(iri)
        try:
            dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
            idx = int(dec.rsplit('/', 1)[1])
            row = insp[dic]['definiciones'][idx - 1]
            t = next((str(row[k]) for k in row if 'tipo de dato' in norm(k)), '?')
            d = next((str(row[k]) for k in row if 'descrip' in norm(k)), '')
            if 'booleano' in norm(t):
                n_bool += 1
            if (d or '').strip().lower() in ('', 'pendiente de especificar'):
                n_empty += 1
        except Exception:
            pass
    print(f'  booleanos={n_bool} descripciones_vacias={n_empty}')
    for s in sigs[:40]:
        show(s.get('definicion_iri', ''))
