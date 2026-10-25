import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
for f in ['tic', 'matriculas', 'epidemiologia', 'catalogos']:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    print('=' * 30, f)
    for k in ['rol', 'ronda', 'alcance', 'conteos']:
        if k in d:
            print(' ', k, '=', json.dumps(d[k], ensure_ascii=False)[:500])
    for k in ['decisiones_significados', 'reglas', 'decisiones_columnas', 'vinculos', 'fuentes', 'pendientes', 'novedades_r6', 'novedades_respecto_r5']:
        if k in d:
            v = d[k]
            print(f'  {k}: n={len(v) if isinstance(v, list) else len(v)}')
    if 'decisiones_significados' in d:
        from collections import Counter
        print('  decisions:', Counter(s.get('decision') for s in d['decisiones_significados']))
    if d.get('reglas'):
        for r in d['reglas']:
            print('  REGLA:', r.get('id'), r.get('concepto'))
    print()
