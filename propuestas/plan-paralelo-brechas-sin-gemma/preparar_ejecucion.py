"""Fija una ejecución nueva del plan; conserva todos los expedientes anteriores."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import hashlib,json

ROOT=Path(__file__).resolve().parents[2]
def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc)
folder=ROOT/'propuestas/plan-paralelo-brechas-sin-gemma'/('ejecucion-'+now.strftime('%Y%m%d-%H%M%SZ'))
folder.mkdir()
prior=read('reports/cierre-brechas-post-r6.json')
cases={r['id']:r for r in prior['decisiones'] if r['tipo']!='correspondencias'}
roles=[]
def assign(name,ids):
    rows=[{'id':ident,'tipo':cases[ident]['tipo'],'original':cases[ident]['original'],'antecedente':cases[ident]} for ident in ids]
    assert len(rows)==len({r['id'] for r in rows})
    path=folder/name/'asignacion.json'
    write(path,{'rol':name,'conteo':len(rows),'casos':rows})
    roles.append({'rol':name,'conteo':len(rows),'asignacion':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
groups=[('S1-defunciones','salud-defunciones'),('S2-nacimientos','salud-nacimientos'),('S3-matriculas','matriculas'),('S4-epidemiologia','epidemiologia'),('S5-tic','tic'),('S6-diversos','diversos')]
for name,group in groups:
    assign(name,[ident for ident,row in cases.items() if row['tipo']=='significados' and row['original']['grupo_fuente']==group])
assign('V1-uth-presas',[f'V{i:02}' for i in range(1,6)])
assign('V2-salud-anomalias',[f'V{i:02}' for i in range(6,9)]+[ident for ident,row in cases.items() if row['tipo']=='anomalias'])
assign('V3-coespo',[f'V{i:02}' for i in (9,10,11,12,15,16)])
assign('V4-seguridad',['V13','V14'])
assert sum(r['conteo'] for r in roles)==188
owner={r['id']:role['rol'] for role in roles for r in read(role['asignacion'])['casos']}
ledger=read('data/revision-estructural-post-r6/revisiones.json')
deps=[{'columna':r['columna'],'definicion_iri':r['definicion_iri'],'rol_responsable':owner[r['definicion_iri']],'estado_semantico_actual':r['estado_semantico_actual'],'original_estructural':r} for r in ledger['pares']]
assert len(deps)==20
write(folder/'dependencias-correspondencias.json',deps)
write(folder/'roles.json',roles)
paths=set(read('propuestas/cierre-brechas-post-r6/base.json')['fuentes_sha256'])
for tree in ('propuestas/cierre-brechas-post-r6','propuestas/investigacion-post-r6'):
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/tree).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths.update(['data/revision-estructural-post-r6/revisiones.json','reports/cierre-brechas-post-r6.json','reports/cierre-brechas-post-r6.md','reports/investigacion-post-r6.json','reports/investigacion-post-r6.md'])
base={'inicio_utc':now.isoformat(),'inicio_hermosillo':now.astimezone(timezone(timedelta(hours=-7))).isoformat(),'fuentes_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(paths)},'conteos_semanticos':{'significados_respaldados':1392,'conceptos':1075,'correspondencias_revisadas':4475,'candidatas':20,'ambiguas':0},'chat_gemma':'excluido'}
write(folder/'base.json',base)
print(json.dumps({'carpeta':folder.relative_to(ROOT).as_posix(),'roles':roles,'base_archivos':len(paths),'casos_primarios':188,'dependencias_correspondencias':20}))
