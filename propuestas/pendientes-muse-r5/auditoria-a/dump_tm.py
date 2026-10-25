import json
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
for lote in ['tic', 'matriculas']:
    d = json.load(open(f'propuestas/pendientes-muse-r5/{lote}/entrega.json', encoding='utf-8'))
    print('=' * 30, lote, 'reglas:', len(d['reglas']))
    for r in d['reglas']:
        dd = r['definiciones'][0]
        dec = unquote(dd)
        dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
        idx = int(dec.rsplit('/', 1)[1])
        row = insp[dic]['definiciones'][idx - 1]
        print('-', r['id'], '| conc:', r.get('concepto'), '| rep:', r.get('representacion'))
        print('  NOMB:', r.get('nombres'), '| DESC:', str(r.get('descripciones'))[:160])
        print('  ROW:', {k: str(v)[:100] for k, v in row.items() if 'variable' in k.lower() or 'descrip' in k.lower() or 'tipo' in k.lower() or 'ejemplo' in k.lower() or 'formato' in k.lower() or 'unidad' in k.lower() or 'catalogo' in k.lower()})
        print('  LIM:', str(r.get('limites', r.get('limite')))[:400])
