from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];S=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pending=read(R/'reports/pendientes-ronda-5.json')['significados']
roles={'nacimientos':'salud','defunciones':'salud','epidemiologia':'epidemiologia','matriculas':'matriculas','tic':'tic','diversos':'diversos-presas'}
for role in set(roles.values()):
 vs=[]
 for old,new in roles.items():
  if new==role:
   ids={v['definicion_iri'] for v in read(R/f'propuestas/pendientes-muse-r5/{old}/asignacion.json')['significados']}
   vs += [v for v in pending if v['definicion_iri'] in ids]
 write(S/role/'asignacion.json',{'rol':role,'significados':vs,'conteo':len(vs)})
write(S/'catalogos'/'asignacion.json',read(R/'propuestas/pendientes-muse-r5/catalogos-web/entrega.json'))
write(S/'diversos-presas'/'presas.json',read(R/'propuestas/pendientes-muse-r5/presas/entrega.json'))
write(S/'base.json',{'pendientes':171,'respaldados':1392,'correspondencias':4474,'conceptos':1075,'sha':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['ontologia/semantica.json','data/semantica/cobertura.json','ontologia/revision-ronda-5.json']}})
print('Asignaciones R6 preparadas')
