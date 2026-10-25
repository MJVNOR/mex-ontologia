import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
for f in ['matriculas', 'epidemiologia', 'catalogos']:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    print('=' * 25, f)
    print(' FUENTES:')
    for fu in d.get('fuentes', []):
        print('  -', json.dumps(fu, ensure_ascii=False)[:550])
    print(' NOVEDADES:', str(d.get('novedades_r6', d.get('novedades_respecto_r5', '')))[:900])
    print(' DECISIONES:')
    for s in d.get('decisiones_significados', [])[:4]:
        print('  -', str(s.get('definicion_iri', ''))[-16:], s.get('decision'), '|', str(s.get('motivo'))[:180])
    print('  ... total', len(d['decisiones_significados']))
