from pathlib import Path
import json,copy,sys
R=Path(__file__).resolve().parents[3];S=R/'propuestas/pendientes-muse-r5'
sys.path.insert(0,str(R/'scripts'))
from consolidar_semantica import construir
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rules=read(R/'ontologia/semantica.json');merged=copy.deepcopy(rules)
owners={};definitions={}
for role in ['nacimientos','defunciones','matriculas','epidemiologia','tic','diversos']:
 d=read(S/role/'entrega.json');merged['reglas_descripcion_exacta']+=d['reglas'];merged['vinculos_documentales_revisados']+=d.get('vinculos',[])
 for k,v in d.get('conceptos_nuevos',{}).items():
  if k in merged['conceptos'] and merged['conceptos'][k]!=v:raise ValueError('Concepto sustituido '+k)
  merged['conceptos'][k]=v
 for rule in d['reglas']:
  owners[rule['id']]=role
  for iri in rule['definiciones']:definitions[iri.replace('/definition/','/documented-variable/')]=role
g,m,report=construir(read(R/'data/portal/inventario.json'),read(R/'data/portal/contenido-inspeccion.json'),merged,read(R/'data/portal/lote-cruces/catalogo-municipal-portal.json'),'https://example.org/mex-ontologi/')
base=read(R/'data/semantica/cobertura.json');vs={v['definicion_iri']:v for v in report['variables']};maps={v['columna']:v for v in report['correspondencias'] if v['estado']=='documental_revisada'}
for v in base['variables']:
 if v['estado']=='respaldada_por_definicion' and vs[v['definicion_iri']]!=v:raise ValueError('Cambio de significado previo')
for v in base['correspondencias']:
 if v['estado']=='documental_revisada' and maps[v['columna']]!=v:raise ValueError('Cambio de vínculo previo')
for role in set(owners.values()):
 rows=[v for v in report['correspondencias'] if definitions.get(v.get('variable'))==role and v['estado']!='documental_revisada']
 (S/role/'columnas-adicionales.json').write_text(json.dumps({'rol':role,'propuestas_condicionadas':True,'columnas':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(S/'integrador/semantica-propuesta.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(S/'integrador/simulacion.json').write_text(json.dumps({'base_preservada':True,'resumen':report['resumen'],'reglas_nuevas':len(owners),'reglas':list(owners)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report['resumen'],ensure_ascii=False))
