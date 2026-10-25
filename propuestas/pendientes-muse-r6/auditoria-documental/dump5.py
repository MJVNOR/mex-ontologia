import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
c = json.load(open(STAGE / 'catalogos' / 'entrega.json', encoding='utf-8'))
print('DECISIONES catalogos:')
for s in c['decisiones_significados']:
    print('-', str(s.get('definicion_iri', ''))[-20:], s.get('decision'), '|', str(s.get('motivo'))[:220].replace('\n', ' '))
print()
print('SOLICITUDES catalogos:', json.load(open(STAGE / 'catalogos' / 'solicitudes-web.json', encoding='utf-8')) if (STAGE / 'catalogos' / 'solicitudes-web.json').exists() else 'AUSENTE')
print()
sw = json.load(open(STAGE / 'tic' / 'solicitudes-web.json', encoding='utf-8'))
print('TIC solicitudes:', len(sw) if isinstance(sw, list) else type(sw), json.dumps(sw, ensure_ascii=False)[:800])
msw = json.load(open(STAGE / 'matriculas' / 'solicitudes-web.json', encoding='utf-8'))
print('MAT solicitudes:', len(msw) if isinstance(msw, list) else type(msw))
esw = json.load(open(STAGE / 'epidemiologia' / 'solicitudes-web.json', encoding='utf-8'))
print('EPI solicitudes:', len(esw) if isinstance(esw, list) else type(esw), json.dumps(esw, ensure_ascii=False)[:600])
