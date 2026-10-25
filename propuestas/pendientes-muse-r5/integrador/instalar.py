"""Fija entregas auditadas y añade R5 sin cambiar los manifiestos anteriores."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,shutil,sys,zipfile
R=Path(__file__).resolve().parents[3];S=R/'propuestas/pendientes-muse-r5';D=R/'data/integracion-ronda-5'
sys.path.insert(0,str(R/'scripts'))
from consolidar_semantica import construir
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.r5-temporal');tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(p)
def main():
 if D.exists() or (R/'ontologia/revision-ronda-5.json').exists():raise ValueError('Ronda 5 ya fijada o instalada: no repetir')
 for rel,h in read(S/'base.json')['huellas'].items():
  if sha(R/rel)!=h:raise ValueError('Base cambió: '+rel)
 A=read(S/'auditoria-a/entrega.json');B=read(S/'auditoria-b/entrega-final.json');C=read(S/'auditoria-b/dictamen-codigo-final.json')
 roles=['nacimientos','defunciones','matriculas','epidemiologia','tic','diversos','presas','catalogos-web']
 for role in roles:
  p=S/role/'entrega.json';m=read(S/role/'listo.json');h=m.get('sha256_entrega',m.get('sha256',m.get('sha256_entrega_json')))
  if sha(p)!=h:raise ValueError('Entrega sin cierre SHA: '+role)
  if role in roles[:6] and A['sha_entregas'].get(role)!=h:raise ValueError('Auditoría A sobre versión distinta: '+role)
  if B['sha_entregas'].get(role)!=h:raise ValueError('Auditoría B sobre versión distinta: '+role)
 if set(C['archivos'])!={'scripts/integrar_ronda_5.py','scripts/integrar_ronda_4.py','scripts/consolidar_semantica.py','tests/test_ronda_5.py'}:raise ValueError('Revisión de código incompleta')
 for rel,item in C['archivos'].items():
  if item['dictamen']!='aceptar' or sha(S/'integrador/codigo'/rel)!=item['sha256']:raise ValueError('Código no aprobado o cambiado: '+rel)
 ar={x['id'] for x in A['dictamenes'] if x['tipo']=='reglas' and x['dictamen']=='aceptar'}
 bl={x['id'] for x in B['dictamenes'] if x['tipo']=='vinculos' and x['dictamen']=='aceptar'}
 additions={'reglas':[],'vinculos':[],'conceptos':{},'origenes':{},'resumen':{}}
 concept_pool={};base=read(R/'ontologia/semantica.json');merged=copy.deepcopy(base)
 for role in roles[:6]:
  delivery=read(S/role/'entrega.json');concept_pool.update(delivery.get('conceptos_nuevos',{}))
  for row in delivery['reglas']:
   if row['id'] not in ar:raise ValueError('Regla propuesta sin aceptación: '+row['id'])
   additions['reglas'].append(row);additions['origenes'][row['id']]=['entregas/'+role+'/entrega.json']
  for row in delivery.get('vinculos',[]):
   if row['columna'] not in bl:raise ValueError('Vínculo sin aceptación: '+row['columna'])
   additions['vinculos'].append(row);additions['origenes'][row['columna']]=['entregas/'+role+'/entrega.json']
 extra=read(S/'tic/adicionales.json')
 if B.get('sha_adicionales',{}).get('tic')!=sha(S/'tic/adicionales.json'):raise ValueError('Auditoría B sobre adicionales distintos')
 for row in extra.get('vinculos',[]):
  if row['columna'] not in bl:raise ValueError('Vínculo adicional sin aceptación')
  additions['vinculos'].append(row);additions['origenes'][row['columna']]=['entregas/tic/adicionales.json','entregas/tic/entrega.json']
 def concept(k):
  if k in base['conceptos']:return
  if k in additions['conceptos']:return
  value=concept_pool[k];additions['conceptos'][k]=value
  if value[2]:concept(value[2])
 for row in additions['reglas']:concept(row['concepto'])
 merged['reglas_descripcion_exacta']+=additions['reglas'];merged['vinculos_documentales_revisados']+=additions['vinculos'];merged['conceptos'].update(additions['conceptos'])
 g,m,report=construir(read(R/'data/portal/inventario.json'),read(R/'data/portal/contenido-inspeccion.json'),merged,read(R/'data/portal/lote-cruces/catalogo-municipal-portal.json'),'https://example.org/mex-ontologi/')
 coverage=read(R/'data/semantica/cobertura.json');vs={v['definicion_iri']:v for v in report['variables']};links={v['columna']:v for v in report['correspondencias'] if v['estado']=='documental_revisada'}
 for v in coverage['variables']:
  if v['estado']=='respaldada_por_definicion' and vs[v['definicion_iri']]!=v:raise ValueError('Significado previo alterado')
 for v in coverage['correspondencias']:
  if v['estado']=='documental_revisada' and links[v['columna']]!=v:raise ValueError('Correspondencia previa alterada')
 if len(additions['reglas'])!=8 or len(additions['vinculos'])!=8:raise ValueError('Cambio de alcance: revisar aceptación y resumen antes de instalar')
 additions['resumen']={'significados_nuevos':len(additions['reglas']),'vinculos_nuevos':len(additions['vinculos']),'conceptos_nuevos':len(additions['conceptos']),'significados_iniciales_pendientes':179,'significados_restantes':171,'base_preservada':True}
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');backup=R/'data/backups'/('antes-r5-'+stamp+'.zip')
 targets=['ontologia/semantica.json','ontologia/revision-agentes.json','ontologia/revision-ronda-2.json']
 codefiles=list((S/'integrador/codigo').rglob('*.py'))
 with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
  for rel in targets:z.write(R/rel,rel)
  for p in codefiles:
   rel=p.relative_to(S/'integrador/codigo')
   if (R/rel).exists():z.write(R/rel,rel.as_posix())
 D.mkdir()
 shutil.copy2(R/'ontologia/semantica.json',D/'base-semantica.json');shutil.copy2(R/'data/semantica/cobertura.json',D/'base-cobertura.json')
 for role in roles:
  for p in (S/role).rglob('*'):
   # La investigación web ampliada sigue en curso y se fijará aparte.
   # El núcleo usa únicamente las entregas cerradas, no borradores web.
   if role=='catalogos-web' and p.relative_to(S/role).as_posix() not in {'entrega.json','asignacion.json','evidencia_web.json'}:continue
   if p.is_file() and p.suffix.lower() in {'.json','.md','.txt','.pdf','.xlsx','.csv','.html'}:
    dest=D/'entregas'/role/p.relative_to(S/role);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 for name,src in [('auditoria-a',S/'auditoria-a/entrega.json'),('auditoria-b',S/'auditoria-b/entrega-final.json'),('codigo',S/'auditoria-b/dictamen-codigo-final.json')]:write(D/'auditorias'/f'{name}.json',read(src))
 for p in codefiles:
  dest=D/'codigo'/p.relative_to(S/'integrador/codigo');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 write(D/'aceptadas.json',additions)
 sources=[R/'data/portal/inventario.json',R/'data/portal/contenido-inspeccion.json',R/'data/portal/lote-cruces/catalogo-municipal-portal.json',*sorted((R/'data/portal/inspecciones').glob('*.json'))]
 manifest={'archivos':{p.relative_to(D).as_posix():sha(p) for p in D.rglob('*') if p.is_file()},'insumos':{p.relative_to(R).as_posix():sha(p) for p in sources}}
 write(D/'manifiesto.json',manifest)
 config={'evidencia':'data/integracion-ronda-5','manifiesto_sha256':sha(D/'manifiesto.json'),'respaldo':backup.relative_to(R).as_posix(),'respaldo_sha256':sha(backup),'resumen':additions['resumen'],'estados_variables_esperados':report['resumen']['estados_variables'],'estados_correspondencias_esperados':report['resumen']['estados_correspondencias']}
 agents=read(R/'ontologia/revision-agentes.json');agents['esperado_actual'].update({'conceptos':len(merged['conceptos']),'variables_respaldadas':1392,'variables_pendientes':19,'correspondencias_revisadas':len(links)})
 r2=read(R/'ontologia/revision-ronda-2.json');r2['esperado_actual'].update({'revisadas':len(links),'candidatas':report['resumen']['estados_correspondencias'].get('candidata_por_nombre',0)})
 for p in codefiles:
  dest=R/p.relative_to(S/'integrador/codigo');dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_suffix('.py.r5-temporal');shutil.copy2(p,tmp);tmp.replace(dest)
 write(R/'ontologia/revision-ronda-5.json',config);write(R/'ontologia/semantica.json',merged);write(R/'ontologia/revision-agentes.json',agents);write(R/'ontologia/revision-ronda-2.json',r2)
 # Nuevo proceso de generación valida la cadena desde los módulos instalados.
 write(S/'integrador/instalacion.json',{'instalado':True,'config':config,'resumen_simulado':report['resumen'],'semantica_sha256':sha(R/'ontologia/semantica.json')})
 print(json.dumps(report['resumen'],ensure_ascii=False))
if __name__=='__main__':main()
