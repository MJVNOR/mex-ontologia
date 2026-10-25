import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
t = json.load(open(STAGE / 'tic' / 'entrega.json', encoding='utf-8'))
print('decisiones:', len(t['decisiones_significados']), 'pendientes:', len(t['pendientes']))
for s in t['decisiones_significados']:
    iri = s.get('definicion_iri', '')
    print('-', iri[-16:], '|', str(s.get('motivo'))[:150].replace('\n', ' '))
print()
print('FUENTES:')
for f in t.get('fuentes', []):
    print(' ', json.dumps(f, ensure_ascii=False)[:600])
