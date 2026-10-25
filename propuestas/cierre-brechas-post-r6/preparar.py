"""Fija la base y distribuye casos documentales sin cambiar fuentes anteriores."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))
def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

coverage = read('data/semantica/cobertura.json')
mappings = sorted((r for r in coverage['correspondencias'] if r['estado']=='candidata_por_nombre'), key=lambda r:r['columna'])
gaps = read('propuestas/depuracion-post-r6/catalogos/brechas.json')['brechas']
meanings = read('reports/investigacion-post-r6.json')['decisiones']
excluded = read('propuestas/depuracion-post-r6/encabezados/exclusiones.json')['exclusiones']
tasks = []
def assign(name, kind, rows, key):
    assert len(rows) == len({r[key] for r in rows})
    write(HERE/name/'asignacion.json', {'tarea':name,'tipo':kind,'clave_id':key,'conteo':len(rows),'casos':rows})
    tasks.append({'tarea':name,'tipo':kind,'conteo':len(rows),'clave_id':key})

assert len(mappings)==20 and len(meanings)==169 and len(gaps)==17
assign('correspondencias-a','correspondencias',mappings[:10],'columna')
assign('correspondencias-b','correspondencias',mappings[10:],'columna')
for name, ids in [('vigencias-uth-presas',{'V01','V02','V03','V04','V05'}),('vigencias-salud',{'V06','V07','V08'}),('vigencias-coespo',{'V09','V10','V11','V12','V15','V16'}),('vigencias-seguridad',{'V13','V14'})]:
    assign(name,'vigencias',[r for r in gaps if r['id'] in ids],'id')
assign('anomalias','anomalias',[dict(r,id=r['definicion_iri']) for r in excluded]+[r for r in gaps if r['id']=='des_mpo_res'],'id')
for name, groups in [('significados-salud',{'salud-defunciones','salud-nacimientos'}),('significados-educacion-epidemiologia',{'matriculas','epidemiologia'}),('significados-tic-diversos',{'tic','diversos'})]:
    assign(name,'significados',[r for r in meanings if r['grupo_fuente'] in groups],'definicion_iri')
write(HERE/'tareas.json',tasks)
paths = set(read('propuestas/investigacion-post-r6/base.json')['fuentes_base'])
paths.update(['reports/investigacion-post-r6.json','reports/investigacion-post-r6.md','propuestas/investigacion-post-r6/cierre.json','ontologia/revision-ronda-6.json','ontologia/revision-ronda-5.json','data/portal/portal-completo.ttl','data/catalogo/studio-live.ttl'])
paths.update(str(p.relative_to(ROOT)).replace('\\','/') for p in (ROOT/'propuestas/investigacion-post-r6').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
write(HERE/'base.json',{'fecha_utc':datetime.now(timezone.utc).isoformat(),'fuentes_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)}})
print(json.dumps(tasks))
