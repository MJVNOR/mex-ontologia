import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
w = json.load(open(STAGE / 'web' / 'entrega.json', encoding='utf-8'))
from collections import Counter
print('WEB decisiones:', Counter(d['decision'] for d in w['decisiones']))
for d in w['decisiones']:
    if d['decision'] != 'pendiente':
        print('NO-PENDIENTE:', json.dumps(d, ensure_ascii=False)[:500])
print('WEB conteos:', w['conteos'])
s = json.load(open(STAGE / 'salud' / 'entrega.json', encoding='utf-8'))
print('SALUD fuentes:')
for f in s.get('fuentes', []):
    print(' -', json.dumps(f, ensure_ascii=False)[:400])
print('SALUD novedades keys:', [k for k in s.keys() if 'noved' in k.lower()], '| solicitudes:', s.get('solicitudes_web_archivo'))
print('SALUD verificacion:', json.dumps(s.get('verificacion', {}), ensure_ascii=False)[:600])
