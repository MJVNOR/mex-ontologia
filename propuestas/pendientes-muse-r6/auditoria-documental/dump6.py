import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
s = json.load(open(STAGE / 'salud' / 'entrega.json', encoding='utf-8'))
print('SALUD keys:', list(s.keys()))
print('fuentes:', len(s.get('fuentes', [])))
from collections import Counter
print('decisiones:', Counter(x.get('decision') for x in s['decisiones_significados']))
for x in s['decisiones_significados'][:5]:
    print('-', str(x.get('definicion_iri', ''))[-16:], x.get('decision'), '|', str(x.get('motivo'))[:180])
print('novedades:', str(s.get('novedades_r6', ''))[:1500])
print()
dp = json.load(open(STAGE / 'diversos-presas' / 'entrega.json', encoding='utf-8'))
print('DIVPRES keys:', list(dp.keys()))
print('decisiones:', Counter(x.get('decision') for x in dp['decisiones_significados']))
for x in dp['decisiones_significados']:
    print('-', str(x.get('definicion_iri', ''))[-16:], x.get('decision'), '|', str(x.get('motivo'))[:220])
print('columnas:', json.load(open(STAGE / 'diversos-presas' / 'entrega.json', encoding='utf-8')).get('decisiones_columnas'))
print()
w = json.load(open(STAGE / 'web' / 'entrega.json', encoding='utf-8'))
print('WEB keys:', list(w.keys()), 'listo:', json.load(open(STAGE / 'web' / 'listo.json', encoding='utf-8')))
