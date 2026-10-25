"""Instala dos adaptadores de conteos auditados sin alterar manifiestos anteriores."""
from pathlib import Path
import json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
version=sys.argv[1] if len(sys.argv)>1 else 'v002'
folder=E/f'integracion/compatibilidad-{version}'
audit_path=E/'B-tecnica'/('auditoria-compatibilidad-r7.json' if version=='v002' else f'auditoria-compatibilidad-r7-{version}.json')
audit=read(audit_path)
assert audit['dictamen']=='aceptar'
assert audit['staging']['version']==version and audit['staging']['veredicto']=='aceptar'
refs=audit.get('referencias',[])
assert any(r['ruta'].endswith(f'compatibilidad-{version}/congelada.json') and sha(ROOT/r['ruta'])==r['sha256'] for r in refs)
for r in refs:
    assert sha(ROOT/r['ruta'])==r['sha256'],r['ruta']
for r in read(folder/'congelada.json')['archivos']:
    assert sha(ROOT/r['ruta'])==r['sha256'],r['ruta']
backup_folder=E/('integracion/respaldo-compatibilidad' if version=='v002' else f'integracion/respaldo-compatibilidad-{version}')
assert not backup_folder.exists()
backup_folder.mkdir()
changes=[]
for name in ('integrar_entregas.py','integrar_ronda_2.py'):
    dest=ROOT/'scripts'/name
    rel=dest.relative_to(ROOT).as_posix()
    shutil.copy2(dest,backup_folder/name)
    assert sha(dest)==sha(backup_folder/name)
    changes.append({'ruta':rel,'sha256_antes':sha(dest),'sha256_despues':sha(folder/name)})
for name in ('integrar_entregas.py','integrar_ronda_2.py'):
    shutil.copy2(folder/name,ROOT/'scripts'/name)
out=E/('integracion/compatibilidad-aplicada.json' if version=='v002' else f'integracion/compatibilidad-aplicada-{version}.json')
assert not out.exists()
out.write_text(json.dumps({'version':version,'cambios':changes,'auditoria_sha256':sha(audit_path),'chat_gemma':'sin cambios'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out.relative_to(ROOT))
