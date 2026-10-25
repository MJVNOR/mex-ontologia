"""Fija el estado anterior de esta actualización documental, sin abrir ronda."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/cobertura-operativa-post-r9/ejecucion-20261024'
dest=E/'base.json';assert not dest.exists()
paths=set((ROOT/'ontologia').glob('*.json'))
paths.update((ROOT/'data').rglob('manifiesto*.json'))
paths.update((ROOT/'reports').glob('ronda-*.json'))
paths.update((ROOT/'reports').glob('ronda-*.md'))
paths.update(ROOT/p for p in ['data/semantica/cobertura.json','data/portal/portal-completo.ttl',
    'data/portal/ampliacion.ttl','data/portal/shapes.ttl','data/catalogo/studio-live.ttl',
    'data/portal/studio-managed.ttl','reports/portal-carga.json','reports/studio-portal-sync.json',
    'docs/plan-actualizado-tras-r9.md','docs/plan-actualizado-tras-r9.json',
    'propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json'])
data={'fecha_utc':datetime.now(timezone.utc).isoformat(),'release_base':'R9',
      'sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos_fijados':len(paths)}))
