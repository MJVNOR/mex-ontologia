import json, hashlib
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
p = STAGE / 'web' / 'evidencia' / 'cat_estatal_1.xlsx'
print('web xlsx existe:', p.exists())
if p.exists():
    b = open(p, 'rb').read()
    print('tam:', len(b), 'magic:', b[:8])
    print('sha:', hashlib.sha256(b).hexdigest())
vn = json.load(open(STAGE / 'web' / 'verificacion_nuevas.json', encoding='utf-8'))
for v in vn['verificaciones']:
    if v['id'] == 'VW-33':
        print('VW-33:', json.dumps(v, ensure_ascii=False)[:1200])
s = json.load(open(STAGE / 'salud' / 'entrega.json', encoding='utf-8'))
n = 0
for x in s['decisiones_significados']:
    m = str(x.get('motivo', ''))
    if 'Manual' in m or 'P17' in m or 'P34' in m or 'semanas' in m or 'parentesco' in m.lower():
        n += 1
        if n <= 3:
            print('SALUD c/manual:', str(x.get('definicion_iri', ''))[-16:], '|', m[:300])
print('salud motivos que mencionan manual:', n, '/', len(s['decisiones_significados']))
print('muestra motivo SEED:', str(s['decisiones_significados'][0].get('motivo', ''))[:400])
