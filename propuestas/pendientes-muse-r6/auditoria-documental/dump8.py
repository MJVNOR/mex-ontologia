import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
w = json.load(open(STAGE / 'web' / 'entrega.json', encoding='utf-8'))
for d in w['decisiones']:
    print('-', d['id'], '|', d['decision'], '|', str(d.get('motivo', ''))[:260].replace('\n', ' '))
print()
vn = json.load(open(STAGE / 'web' / 'verificacion_nuevas.json', encoding='utf-8'))
print('N verificaciones:', len(vn['verificaciones']), [v['id'] for v in vn['verificaciones']])
for v in vn['verificaciones']:
    if v['id'] not in ('VW-24', 'VW-25', 'VW-26') and not str(v['id']).startswith('VW-27'):
        print('==', v['id'], '|', str(v.get('url_solicitada', ''))[:110])
        print('   concl:', str(v.get('conclusion', ''))[:220])
        print('   aplic:', str(v.get('aplicabilidad', ''))[:220])
