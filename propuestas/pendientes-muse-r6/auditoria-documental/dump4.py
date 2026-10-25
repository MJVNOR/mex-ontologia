import json, hashlib
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
# 1. asignaciones pendientes: salud + diversos-presas deben sumar 75
for f in ['salud', 'diversos-presas']:
    a = json.load(open(STAGE / f / 'asignacion.json', encoding='utf-8'))
    print(f, 'keys:', list(a.keys()))
    for k, v in a.items():
        if isinstance(v, list):
            print('  ', k, 'n=', len(v))
        else:
            print('  ', k, '=', str(v)[:300])
# 2. base SHA vs live
base = json.load(open(STAGE / 'base.json', encoding='utf-8'))
for k, h in base['sha'].items():
    live = hashlib.sha256(open(k, 'rb').read()).hexdigest()
    print(k, 'IGUAL' if h == live else 'CAMBIO!!!')
# 3. matriculas PDF existe + magic
p = STAGE / 'matriculas' / 'evidencia' / 'UES_Reglamentoescolar_ues-mx.pdf'
print('PDF existe:', p.exists(), 'tam:', p.stat().st_size if p.exists() else 0)
if p.exists():
    print('magic:', open(p, 'rb').read(8))
# 4. epi manual sha longitud
print('manual sha len:', len('f35746a0353c902b03d8ae01f703d1dfafdf3ad4bbf01777b648353d1b833757'))
