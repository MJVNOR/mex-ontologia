"""Extensión R6 de catálogos: sin reglas ni conceptos nuevos; como máximo la correspondencia única de presas."""
import copy
import hashlib
import json
from pathlib import Path
from rdflib import Graph,Literal,Namespace,RDF,URIRef
from construir_catalogo import ROOT,PROV

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dentro(root,relative):
 p=(root/relative).resolve()
 if not p.is_relative_to(root.resolve()):raise ValueError('Evidencia de ronda 6 fuera de carpeta')
 return p
def cargar(root=ROOT):
 cp=root/'ontologia/revision-ronda-6.json'
 config=json.loads(cp.read_text(encoding='utf-8'))
 folder=dentro(root,config['evidencia']);mp=folder/'manifiesto.json'
 if sha(mp)!=config['manifiesto_sha256']:raise ValueError('Manifiesto de ronda 6 modificado')
 manifest=json.loads(mp.read_text(encoding='utf-8'));sources={'revision_ronda_6':cp,'manifiesto_ronda_6':mp}
 required={'base-semantica.json','aceptadas.json','auditorias/auditoria-a.json','auditorias/auditoria-b.json'}
 if not isinstance(manifest.get('archivos'),dict) or not isinstance(manifest.get('insumos'),dict) or not required.issubset(manifest['archivos']):raise ValueError('Manifiesto de ronda 6 incompleto')
 for category,base in [('archivos',folder),('insumos',root)]:
  for rel,h in manifest[category].items():
   p=dentro(base,rel)
   if sha(p)!=h:raise ValueError('Evidencia de ronda 6 modificada: '+rel)
   sources['ronda_6_'+category+'_'+rel]=p
 read=lambda rel:json.loads((folder/rel).read_text(encoding='utf-8'))
 accepted=read('aceptadas.json')
 if accepted.get('reglas'):raise ValueError('Ronda 6 no admite reglas nuevas')
 if accepted.get('conceptos'):raise ValueError('Ronda 6 no admite conceptos nuevos')
 cols=[r['columna'] for r in accepted.get('vinculos',[])]
 if len(cols)!=len(set(cols)):raise ValueError('Columnas duplicadas en ronda 6')
 if len(cols)>1:raise ValueError('Ronda 6 admite como máximo la correspondencia única de presas')
 for category,key in [('vinculos','columna')]:
  for row in accepted[category]:
   origins=accepted.get('origenes',{}).get(row[key],[])
   if not origins or any(rel not in manifest['archivos'] for rel in origins):raise ValueError('Origen no fijado por manifiesto de ronda 6: '+row[key])
 return config,folder,read('base-semantica.json'),accepted,sources
def validar_sobre_base(rules,base_r5,root=ROOT):
 config,folder,baseline,accepted,sources=cargar(root)
 if baseline!=base_r5:raise ValueError('Base de ronda 6 no coincide con ronda 5 validada')
 expected=copy.deepcopy(baseline)
 expected['reglas_descripcion_exacta'].extend(accepted['reglas'])
 expected['vinculos_documentales_revisados'].extend(accepted['vinculos'])
 for k,v in accepted['conceptos'].items():
  if k in expected['conceptos'] and expected['conceptos'][k]!=v:raise ValueError('Ronda 6 sustituyó concepto previo: '+k)
  expected['conceptos'][k]=v
 if rules!=expected:raise ValueError('Ronda 6 permite solo la base y la adenda-diversos auditada exacta')
 for field,key in [('reglas_descripcion_exacta','id'),('vinculos_documentales_revisados','columna')]:
  ids=[r[key] for r in rules[field]]
  if len(ids)!=len(set(ids)):raise ValueError('Reglas o columnas duplicadas en ronda 6')
 for audit_name,category,key in [('auditoria-a','reglas','id'),('auditoria-b','vinculos','columna')]:
  audit=json.loads((folder/'auditorias'/f'{audit_name}.json').read_text(encoding='utf-8'))
  approvals={x['id'] for x in audit['dictamenes'] if x['tipo']==category and x['dictamen']=='aceptar'}
  for row in accepted[category]:
   if row[key] not in approvals:raise ValueError('Ronda 6 sin aprobación independiente: '+row[key])
 return config,folder,baseline,accepted,sources
def construir(report,rules,base):
 # Valida además toda la cadena histórica R4→R5→R6. R4 invoca validar_sobre_base
 # (R5 delega a R6 solo si existe config de ronda 6); no se reemplazan manifiestos anteriores.
 from integrar_ronda_4 import validar
 validar(rules)
 config,folder,baseline,accepted,sources=cargar()
 g=Graph();mex=Namespace(base+'vocab/')
 variables={v['definicion_iri']:v for v in report['variables']}
 mappings={v['columna']:v for v in report['correspondencias'] if v['estado']=='documental_revisada'}
 for category,key in [('reglas','id'),('vinculos','columna')]:
  for row in accepted[category]:
   if category=='reglas':
    observed=variables[row['definiciones'][0]]
    if observed.get('regla')!=row['id'] or observed.get('concepto')!=row['concepto'] or observed.get('huella_fila_diccionario')!=row['huella_fila_diccionario']:raise ValueError('Regla R6 no materializada fielmente')
   else:
    observed=mappings[row['columna']]
    if observed['revision']!=row:raise ValueError('Vínculo R6 no materializado fielmente')
   for rel in accepted['origenes'][row[key]]:
    p=dentro(folder,rel);entity=URIRef(p.as_uri())
    g.add((entity,RDF.type,PROV.Entity));g.add((entity,mex.sha256Evidencia,Literal(sha(p))))
    g.add((URIRef(observed['iri']),PROV.wasDerivedFrom,entity))
 return g,dict(accepted['resumen'],manifiesto_sha256=config['manifiesto_sha256']),sources
