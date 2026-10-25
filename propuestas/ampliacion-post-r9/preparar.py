"""Congela la base de ampliación conservando la IRI y los cierres anteriores."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ampliacion-post-r9/ejecucion-20261024'
assert not (E/'base.json').exists()
paths=set((ROOT/'ontologia').glob('*'))
paths={p for p in paths if p.is_file()}
paths.update((ROOT/'data').rglob('manifiesto*.json'))
paths.update((ROOT/'reports').glob('ronda-*'))
paths.update((ROOT/'scripts').glob('*.py'))
paths.update((ROOT/'tests').glob('*.py'))
paths.update((ROOT/'shapes').glob('*.ttl'))
paths.update(ROOT/p for p in ['README.md','PLAN.md','data/semantica/cobertura.json',
    'data/portal/portal-completo.ttl','data/portal/shapes.ttl','data/portal/ampliacion.ttl',
    'data/portal/studio-managed.ttl','data/catalogo/studio-live.ttl',
    'reports/portal-carga.json','reports/studio-portal-sync.json',
    'reports/seguimiento-operativo-post-r9.json','reports/seguimiento-operativo-post-r9.md',
    'reports/cobertura-operativa-r9.json','reports/cobertura-operativa-r9.md',
    'docs/plan-actualizado-tras-r9.md','docs/plan-actualizado-tras-r9.json'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base={'fecha_utc':datetime.now(timezone.utc).isoformat(),'release_base':'R9',
      'base_iri':'https://example.org/mex-ontologi/','decision_iri':'fuera_de_alcance_no_modificar',
      'sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}}
(E/'base.json').write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
archive=E/'respaldo-previo.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(paths):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    for rel,h in base['sha256'].items():assert hashlib.sha256(z.read(rel)).hexdigest()==h
(E/'respaldo-previo.json').write_text(json.dumps({'zip':archive.relative_to(ROOT).as_posix(),
    'sha256':sha(archive),'archivos':len(paths),'verificado':True},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos':len(paths),'respaldo_sha256':sha(archive)}))
