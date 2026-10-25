"""Respalda los archivos que pueden regenerarse durante la aplicación aprobada."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,sys

ROOT=Path(__file__).resolve().parents[2]
folder=(ROOT/sys.argv[1]).resolve()
dest=folder/'integracion/respaldo-previo'
if dest.exists():
    raise ValueError('El respaldo ya existe; no se sobrescribe')
dest.mkdir(parents=True)
targets=['ontologia/semantica.json','scripts/consolidar_semantica.py','scripts/integrar_ronda_6.py','data/semantica','data/portal','data/territorio','data/catalogo/studio-live.ttl','data/integracion/integracion.ttl','data/integracion-ronda-2/ronda-2.ttl','reports','docs','PLAN.md','README.md']
copies=[]
seen=set()
for rel in targets:
    entry=ROOT/rel
    paths=entry.rglob('*') if entry.is_dir() else [entry]
    for path in paths:
        if not path.is_file() or path in seen or '__pycache__' in path.parts:
            continue
        seen.add(path)
        relative=path.relative_to(ROOT)
        out=dest/relative
        out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,out)
        fingerprint=hashlib.sha256(path.read_bytes()).hexdigest()
        if hashlib.sha256(out.read_bytes()).hexdigest()!=fingerprint:
            raise ValueError('Copia no coincide: '+str(relative))
        copies.append({'original':relative.as_posix(),'respaldo':out.relative_to(ROOT).as_posix(),'sha256':fingerprint,'bytes':path.stat().st_size})
data={'fecha_utc':datetime.now(timezone.utc).isoformat(),'copias':copies,'archivos_nuevos_previstos':['scripts/integrar_ronda_7.py','ontologia/revision-ronda-7.json'],'gemma':'sin cambios; no se respaldan ni editan claves/configuración de chat'}
(dest/'manifiesto-respaldo.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos_respaldados':len(copies),'bytes':sum(r['bytes'] for r in copies),'manifiesto':(dest/'manifiesto-respaldo.json').relative_to(ROOT).as_posix()}))
