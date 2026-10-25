import json
from pathlib import Path
STAGE = Path('propuestas/pendientes-muse-r6')
w = json.load(open(STAGE / 'web' / 'entrega.json', encoding='utf-8'))
print('WEB entrega:', json.dumps(w, ensure_ascii=False)[:3000])
print()
vn = json.load(open(STAGE / 'web' / 'verificacion_nuevas.json', encoding='utf-8'))
print('VERIF_NUEVAS keys:', list(vn.keys()) if isinstance(vn, dict) else type(vn))
print(json.dumps(vn, ensure_ascii=False)[:4000])
