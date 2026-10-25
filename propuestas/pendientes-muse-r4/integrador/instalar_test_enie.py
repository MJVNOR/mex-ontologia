from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[3]
S=R/'propuestas/pendientes-muse-r4/auditoria-b/reparacion-test-enie'
p=S/'tests/test_ronda_2.py'
d=json.loads((S/'dictamen.json').read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(p)==d['sha_archivo']
dst=R/'tests/test_ronda_2.py'
backup=S/'test_ronda_2-antes.py'
if backup.exists():
 if sha(backup)!=sha(dst):raise ValueError('Respaldo y archivo central distintos: no repetir')
else:shutil.copy2(dst,backup)
text=p.read_text(encoding='utf-8').replace('ROOT = Path(__file__).resolve().parents[5]  # copia en auditoria-b: mismo repo real, sin tocar central','ROOT = Path(__file__).resolve().parents[1]')
tmp=dst.with_suffix('.py.r4-temporal')
tmp.write_text(text,encoding='utf-8')
tmp.replace(dst)
(S/'instalacion.json').write_text(json.dumps({'antes_sha256':sha(backup),'despues_sha256':sha(dst),'ajuste_ruta':'ROOT parents5 copia -> parents1 central'},indent=2)+'\n',encoding='utf-8')
