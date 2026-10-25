"""Fija la base R8 y prepara las auditorías locales y pilotos del plan devuelto."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
assert not E.exists();E.mkdir(parents=True)
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r8=read(ROOT/'reports/ronda-8.json');cov=read(ROOT/'data/semantica/cobertura.json');rules=read(ROOT/'ontologia/semantica.json')
require=r8['estado']=='cerrado_integrado_validado_y_sincronizado';assert require
vs={v['iri']:v for v in cov['variables'] if v.get('iri')}
candidates=[dict(m,definicion=vs[m['variable']]) for m in cov['correspondencias'] if m['estado']=='candidata_por_nombre']
clinical=[{'id':k,'concepto':v,'variables':[x for x in cov['variables'] if x.get('concepto')==k]} for k,v in rules['conceptos'].items() if k.startswith('caso-con-')]
assert len(candidates)==17 and len(clinical)==101
refs=[r for r in r8['casos'] if r['rol'].startswith('V') or r['rol']=='X-anomalias']
specs=[('C1-candidatas','Priorizar y trazar las 17 candidatas, sin repetir investigación agotada.',candidates),('C2-oportunidades','Vista nueva de prioridad de cruces con cobertura R8; oportunidades no equivalen a joins validados.',[]),('C3-cobertura','Reconciliar 5523 columnas, cinco estados y cinco observaciones; distinguir columnas de significados.',[]),('C4-referencias','Cotejar 16 vigencias y tres anomalías; preparar dependencias y preguntas documentales sin enviarlas.',refs),('P1-qudt','Inventario de unidades explícitas y propuesta mínima QUDT local y cualificada; no inventar valores ni conversiones.',[]),('P2-owl-time','Inventario de periodos escolares/agrícolas y piloto temporal sólo con límites documentados.',[]),('P3-jerarquia-clinica','Revisión documental de 101 conceptos caso-con-*; agrupaciones SKOS sólo justificadas por fuentes.',clinical),('P4-shacl-versionado','Exclusión documentado/candidato permitiendo ninguno; versionado de formato separado de release; fixtures del motor.',[]),('W-estandares','Único navegador Obscura. Fuentes primarias normativas de estándares nuevos y peticiones concretas de pilotos.',[])]
roles=[]
for name,scope,items in specs:
    folder=E/name;folder.mkdir()
    p=folder/'asignacion.json'
    write(p,{'rol':name,'alcance':scope,'casos':items,'base':'reports/ronda-8.json','plan':'docs/plan-actualizado-tras-r8.md','salida':'v001/entrega.json/md + archivos propuestos y congelada.json; no editar tras congelar','limites':['Gemma excluido','Sin contactos externos','Sin promoción por nombre','Sin cambios centrales ni Studio','No repetir búsquedas agotadas sin pista primaria concreta']})
    roles.append({'rol':name,'casos':len(items),'asignacion':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
write(E/'roles.json',roles)
paths=['reports/ronda-8.json','reports/ronda-8.md','ontologia/revision-ronda-8.json','ontologia/semantica.json','data/semantica/cobertura.json','reports/pendientes-semanticos.json','data/portal/oportunidades-cruce.json','reports/portal-carga.json','reports/studio-portal-sync.json','shapes/semantica.ttl','docs/plan-actualizado-tras-r8.md','docs/plan-actualizado-tras-r8.json']
pins={p:sha(ROOT/p) for p in paths}
for p in (ROOT/'data').glob('integracion*/manifiesto.json'): pins[p.relative_to(ROOT).as_posix()]=sha(p)
write(E/'base.json',{'fecha_utc':datetime.now(timezone.utc).isoformat(),'resumen':cov['resumen'],'sha256':pins,'gemma':'excluido','plan_recibido_del_chat':'01a16c87-06d0-7541-83bb-6023e23bb0c9'})
write(E/'base-semantica.json',rules)
# Reutilizar el procedimiento de respaldo verificado con un destino nuevo.
source=(ROOT/'propuestas/ronda-8-paralela/respaldar.py').read_text(encoding='utf-8')
source=source.replace("E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'","E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'")
(E.parent/'respaldar.py').write_text(source,encoding='utf-8')
print(json.dumps({'expediente':E.relative_to(ROOT).as_posix(),'roles':roles}))
