import json, hashlib, collections
from pathlib import Path
R=Path(__file__).resolve().parents[2]
S=Path(__file__).resolve().parent
def read(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=read(Path('data/semantica/cobertura.json'))
p=[v for v in c['variables'] if v['estado']!='respaldada_por_definicion']
assert len(p)==179
groups=collections.defaultdict(list)
for v in p:
 t=v['titulo_conjunto']
 role=('nacimientos' if t=='Información Sobre Nacimientos' else 'defunciones' if t=='Sistema Epidemiológico y Estadístico de Defunciones' else 'matriculas' if t=='Matrículas de Estudiantes' else 'epidemiologia' if t=='Vigilancia Epidemiológica' else 'tic' if ('Administración Pública Estatal' in t) else 'diversos')
 groups[role].append(v)
for role,vs in groups.items():
 defs={v['definicion_iri'] for v in vs}; iris={v.get('iri',v['definicion_iri'].replace('/definition/','/documented-variable/')) for v in vs}
 maps=[m for m in c['correspondencias'] if m.get('variable') in iris]
 save(S/role/'asignacion.json',{'rol':role,'significados':vs,'correspondencias_actuales':maps,'conteo':len(vs)})
save(S/'catalogos-web'/'asignacion.json',read(Path('propuestas/pendientes-muse-r4/catalogos/entrega.json')))
save(S/'presas'/'asignacion.json',read(Path('propuestas/pendientes-muse-r4/ambiguedades/pendientes.json')))
files=['ontologia/semantica.json','data/semantica/cobertura.json','ontologia/revision-ronda-4.json']
save(S/'base.json',{'significados_pendientes':179,'respaldados':1384,'correspondencias_revisadas':4466,'huellas':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},'grupos':{k:len(v) for k,v in groups.items()}})
print(json.dumps({k:len(v) for k,v in groups.items()},ensure_ascii=False))
