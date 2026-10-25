"""Recibo final basado en evidencia congelada, cobertura regenerada y Studio verificado."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,copy
from comprobar_ejecucion import inspect
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def require(ok,msg):
    if not ok: raise ValueError(msg)
selection=read(E/'seleccion-v002.json')
checked=inspect(E,selection['versiones'])
allowed={'ontologia/semantica.json','data/semantica/cobertura.json','data/portal/portal-completo.ttl','data/catalogo/studio-live.ttl'}
historical_cov=E/'integracion/respaldo-previo/data/semantica/cobertura.json'
def cambio_esperado(x):
    if x['tipo']=='fuente_base_alterada' and x['ruta'] in allowed:
        return True
    # S5 citó la cobertura vigente R6: su copia de respaldo conserva ese
    # mismo SHA; la cobertura actual se regenera legítimamente en R7.
    return x['tipo']=='sha_no_coincide' and x['ruta']=='data/semantica/cobertura.json' and x['declarado']==sha(historical_cov)
unexpected=[x for x in checked['discrepancias'] if not cambio_esperado(x)]
require(not checked['faltantes'] and not unexpected,'Fuentes alteradas: '+str(unexpected[:5]))
before_check=read(E/'comprobacion-v002.json')
require(not before_check['faltantes'] and not before_check['discrepancias'],'El cotejo anterior a integrar no fue limpio')
material=E/'integracion/materializacion/v002'
accepted=read(material/'aceptadas.json')
accepted_sha=sha(material/'aceptadas.json')
for role in ('A-documental','B-tecnica'):
    a=read(E/role/'dictamen.json')
    require(a['dictamen']=='aceptar' and a['seleccion_sha256']==sha(E/'seleccion-v002.json'),'Auditoría global incorrecta')
    a=read(E/role/'auditoria-reglas-vinculos.json')
    require(a['dictamen']=='aceptar' and a['aceptadas_sha256']==accepted_sha,'Auditoría material incorrecta')
    for kind,ids in [('reglas',{r['id'] for r in accepted['reglas']}),('vinculos',{r['columna'] for r in accepted['vinculos']})]:
        approved={r['id'] for r in a['dictamenes'] if r['tipo']==kind and r['dictamen']=='aceptar'}
        require(ids<=approved,'Aprobación incompleta '+role)
base=read(material/'base-semantica.json')
expected=copy.deepcopy(base)
expected['reglas_descripcion_exacta']+=accepted['reglas']
expected['vinculos_documentales_revisados']+=accepted['vinculos']
expected['conceptos'].update(accepted['conceptos'])
require(read(ROOT/'ontologia/semantica.json')==expected,'Delta semántico distinto al aprobado')
config=read(ROOT/'ontologia/revision-ronda-7.json')
folder=ROOT/config['evidencia']
require(sha(folder/'manifiesto.json')==config['manifiesto_sha256'],'Manifiesto R7 modificado')
for rel,h in read(folder/'manifiesto.json')['archivos'].items():
    require(sha(folder/rel)==h,'Evidencia R7 alterada: '+rel)
cov=read(ROOT/'data/semantica/cobertura.json')
s=cov['resumen']
require(s['conceptos_compartidos']==1106,'Conceptos')
require(s['estados_variables']=={'respaldada_por_definicion':1423,'fuera_del_nucleo_actual':124,'candidata_sin_definicion_suficiente':16},'Estados significados')
require(s['estados_correspondencias']=={'documental_revisada':4478,'candidata_por_nombre':45},'Estados correspondencias')
load=read(ROOT/'reports/portal-carga.json')
sync=read(ROOT/'reports/studio-portal-sync.json')
require(load['shacl']['conforms'] and sync['verificado'] and sync['shacl']['conforms'],'SHACL/Studio')
require(load['semantica']['huellas_entrada']['reglas']==sha(ROOT/'ontologia/semantica.json'),'Carga del portal obsoleta')
oldcov=read(E/'integracion/respaldo-previo/data/semantica/cobertura.json')
oldcand={r['columna'] for r in oldcov['correspondencias'] if r['estado']=='candidata_por_nombre'}
candidates={r['columna'] for r in cov['correspondencias'] if r['estado']=='candidata_por_nombre'}
newcand=candidates-oldcand
require(len(newcand)==28 and len(candidates&oldcand)==17,'Partición candidatas')
approved_defs={r['definiciones'][0] for r in accepted['reglas']}
cases=[]
for row in checked['decisiones']:
    r=copy.deepcopy(row)
    r['estado_final']='integrado_r7' if r['id'] in approved_defs and r['tipo']=='significados' else r['estado']
    cases.append(r)
require(len(cases)==188 and sum(r['estado_final']=='integrado_r7' for r in cases)==31,'Overlay casos')
dependencies=read(E/'dependencias-correspondencias.json')
approved_cols={r['columna'] for r in accepted['vinculos']}
for row in dependencies:
    row['estado_semantico_final']='documental_revisada' if row['columna'] in approved_cols else 'candidata_por_nombre'
changes=[]
backup=read(E/'integracion/respaldo-previo/manifiesto-respaldo.json')
closed_prefix=('reports/ronda-4','reports/ronda-5','reports/ronda-6','reports/pendientes-depurados','reports/investigacion-post-r6','reports/cierre-brechas-post-r6')
for entry in backup['copias']:
    rel=entry['original']
    require(sha(ROOT/entry['respaldo'])==entry['sha256'],'Respaldo alterado '+rel)
    actual=sha(ROOT/rel)
    if actual!=entry['sha256']:
        require(not rel.startswith(closed_prefix),'Informe histórico modificado '+rel)
        changes.append({'ruta':rel,'sha256_antes':entry['sha256'],'sha256_despues':actual})
web=list(selection['paquetes_web'])
adenda=E/'W-web/paquete-v004/congelada-v004.json'
for marker in [ROOT/w['ruta'] for w in web]+[adenda]:
    for r in read(marker)['archivos']:
        if r.get('sha256') is None:
            require((ROOT/r['ruta']).resolve()==marker.resolve(),'Referencia web sin SHA')
        else:
            require(sha(ROOT/r['ruta'])==r['sha256'],'Paquete web alterado')
web.append(ref(adenda))
report={'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'integrado_regenerado_validado_y_sincronizado','expediente':E.relative_to(ROOT).as_posix(),'modelo_agentes':'opencode-go/muse-spark-1.3-contributor','mcp':'nativo OpenCode; investigación web por MCP Obscura','delta':{'significados':31,'conceptos':31,'correspondencias_revisadas':3},'resumen_actual':s,'pendientes':{'significados_reales':138,'filas_corruptas_encabezado':2,'vigencias':16,'vigencias_acceso_no_resuelto':['V13','V14'],'anomalia_referencia':'des_mpo_res','correspondencias_candidatas_anteriores':17,'correspondencias_candidatas_nuevas':28},'candidatas_nuevas':sorted(newcand),'decisiones':cases,'dependencias_20_pares_previos':dependencies,'auditorias':[ref(E/role/name) for role in ('A-documental','B-tecnica') for name in ('dictamen.json','auditoria-reglas-vinculos.json')],'seleccion':ref(E/'seleccion-v002.json'),'evidencia_r7':ref(folder/'manifiesto.json'),'materializacion':ref(material/'congelada.json'),'aplicacion':read(E/'integracion/aplicacion.json'),'compatibilidad':[read(E/'integracion'/f'compatibilidad-aplicada{suffix}.json') for suffix in ('','-v003','-v004')],'web':web,'integridad':{'base_previa':ref(E/'base.json'),'comprobacion_previa':ref(E/'comprobacion-v002.json'),'fuentes_base':len(read(E/'base.json')['fuentes_sha256']),'cambios_base_aprobados':[x for x in checked['discrepancias']],'respaldo':ref(E/'integracion/respaldo-previo/manifiesto-respaldo.json'),'cambios_derivados_y_codigo':changes},'portal':{'triples_combinados':load['triples_combinados'],'shacl':load['shacl']},'studio':sync,'chat_gemma':'excluido_sin_cambios','contactos_externos':0,'pruebas_python':'no ejecutadas en esta ronda; se ejecutó regeneración y validación de datos/RDF/SHACL','limites':['Sin definiciones ni vigencias inventadas.','No joins, identidad global entre catálogos ni adopción de catálogos completos.','La predicción de 17 candidatas del staging era incompleta: aparecieron 28 nuevas coincidencias automáticas; el total real es 45.','Los 20 pares estructurales anteriores no se cuentan como pares nuevos; tres tienen ahora significado respaldado.']}
lines=['# Ronda 7 — ejecución paralela sin Gemma','','## Resultado','','- 31 significados SINAC incorporados con dos auditorías y evidencia fijada por SHA-256.','- 1423 significados respaldados, 1106 conceptos y 4478 correspondencias revisadas.','- 45 correspondencias candidatas: 17 anteriores y 28 nuevas coincidencias automáticas. Cero ambiguas.',f"- Studio sincronizado y verificado: {sync['triples_totales_studio']} triples. RDF y SHACL conformes.",'','## Brechas conservadas','','| Frente | Significados sin respaldo |','| --- | ---: |','| Defunciones | 32 |','| Nacimientos | 22 |','| Matrículas | 30 |','| Epidemiología | 25 |','| TIC | 24 |','| Diversos | 5 |','','Quedan 138 significados reales, 16 vigencias y la anomalía `des_mpo_res` con dos encabezados corruptos. V13/V14 permanecen como acceso no resuelto. El JSON conserva por caso las fuentes examinadas, evidencia faltante y condición para reabrir. Las consultas web específicas quedaron atendidas por las vías examinadas.','','## Alcance','','Los textos aprobados mantienen sus límites de recurso y edición. No acreditan vigencias, joins, identidades de catálogos ni códigos que la evidencia no documenta. Los 20 pares estructurales de R6 se conservan como antecedente; tres se promovieron.','','La predicción inicial de 17 candidatas no contemplaba las 28 coincidencias que aparecen al materializar los nuevos significados. Se corrigieron los adaptadores de conteos de R1/R2 sin modificar manifiestos anteriores.','','Gemma quedó excluido y no se contactó a publicadores. Se validaron datos, RDF y SHACL; no se ejecutó la suite Python en esta ronda.','','[Casos, auditorías, evidencia, respaldos y recibo de Studio](ronda-7.json).','']
for name in ('ronda-7','ejecucion-plan-sin-gemma'):
    for suffix in ('.json','.md'):
        require(not (ROOT/'reports'/(name+suffix)).exists(),'Informe ya existe')
for name in ('ronda-7','ejecucion-plan-sin-gemma'):
    (ROOT/'reports'/(name+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'reports'/(name+'.md')).write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'estado':report['estado'],'resumen':s,'studio_triples':sync['triples_totales_studio']},ensure_ascii=False))
