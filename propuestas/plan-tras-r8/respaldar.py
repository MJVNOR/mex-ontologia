"""Respaldo verificado previo a aplicar correcciones o nuevas revisiones R8."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
out=E/'respaldo-previo.zip'
assert not out.exists()
files=set()
for name in ('ontologia','scripts','tests','reports','docs','data/semantica','data/territorio'):
    files.update(p for p in (ROOT/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for name in ('README.md','PLAN.md','data/catalogo/studio-live.ttl','data/integracion/integracion.ttl','data/integracion-ronda-2/ronda-2.ttl'):
    files.add(ROOT/name)
files.update((ROOT/'data/portal').glob('*.ttl'))
meta={}
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):
        rel=p.relative_to(ROOT).as_posix()
        data=p.read_bytes()
        meta[rel]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        z.writestr(rel,data)
with zipfile.ZipFile(out) as z:
    for name,m in meta.items():
        assert hashlib.sha256(z.read(name)).hexdigest()==m['sha256'],name
record={'fecha_utc':datetime.now(timezone.utc).isoformat(),'zip':out.relative_to(ROOT).as_posix(),'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'archivos':meta,'chat_gemma':'sin cambios'}
(E/'respaldo-previo.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos':len(meta),'bytes_zip':out.stat().st_size,'sha256':record['zip_sha256']}))
