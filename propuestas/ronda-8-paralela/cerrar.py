"""Cierra R8 sólo con delta exacto, fuentes preservadas, suite verde y Studio verificado."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
from collections import Counter
import json,hashlib,copy,re,zipfile
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def require(ok,msg):
    if not ok: raise ValueError(msg)
before=read(E/'comprobacion-preintegracion.json')
require(not before['faltantes'] and not before['discrepancias'],'Preintegración no limpia')
backup=read(E/'respaldo-previo.json')
require(sha(ROOT/backup['zip'])==backup['zip_sha256'],'Respaldo modificado')
with zipfile.ZipFile(ROOT/backup['zip']) as z:
    for rel,m in backup['archivos'].items():
        require(hashlib.sha256(z.read(rel)).hexdigest()==m['sha256'],'Copia previa alterada '+rel)
for item in before['seleccion']:
    require(sha(ROOT/item['entrega'])==item['sha256_entrega'],'Entrega cambió')
    require(sha(ROOT/item['marcador'])==item['sha256_marcador'],'Marcador cambió')
mutable={'ontologia/semantica.json','data/semantica/cobertura.json','data/portal/portal-completo.ttl','data/catalogo/studio-live.ttl'}
mutable.update({'reports/studio-portal-sync.json','reports/portal-carga.json','data/semantica/interpretaciones.ttl','data/semantica/nucleo.ttl','data/territorio/verificacion.json','data/territorio/territorio.ttl','data/integracion/integracion.ttl','data/integracion-ronda-2/ronda-2.ttl'})
mutable.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'data/portal').glob('*.ttl'))
for r in read(E/'aplicacion.json')['cambios']: mutable.add(r['ruta'])
for r in read(E/'io-atomico-aplicado.json')['cambios']: mutable.add(r['ruta'])
for rel,h in read(E/'base.json')['sha256'].items():
    require(rel in mutable or sha(ROOT/rel)==h,'Histórico alterado '+rel)
for rel,h in before['fuentes_cotejadas'].items():
    if sha(ROOT/rel)!=h:
        require(rel in mutable and backup['archivos'].get(rel,{}).get('sha256')==h,'Fuente primaria alterada '+rel)
M=E/'materializacion/v003'
accepted=read(M/'aceptadas.json');baseline=read(M/'base-semantica.json')
expected=copy.deepcopy(baseline);expected['vinculos_documentales_revisados'].extend(accepted['vinculos'])
require(read(ROOT/'ontologia/semantica.json')==expected,'Delta distinto de 28 vínculos')
for role in ('A-documental','B-tecnica'):
    a=read(E/role/'auditoria-material-v003.json')
    require(a['dictamen']=='aceptar' and a['aceptadas_sha256']==sha(M/'aceptadas.json'),'Auditoría exacta ausente')
cfg=read(ROOT/'ontologia/revision-ronda-8.json');folder=ROOT/cfg['evidencia']
require(sha(folder/'manifiesto.json')==cfg['manifiesto_sha256'],'Manifiesto R8 modificado')
for rel,h in read(folder/'manifiesto.json')['archivos'].items():
    require(sha(folder/rel)==h,'Evidencia R8 cambió '+rel)
cov=read(ROOT/'data/semantica/cobertura.json');summary=cov['resumen']
require(summary['estados_variables']=={'respaldada_por_definicion':1423,'fuera_del_nucleo_actual':124,'candidata_sin_definicion_suficiente':16},'Estados significados')
require(summary['conceptos_compartidos']==1106 and summary['estados_correspondencias']=={'documental_revisada':4506,'candidata_por_nombre':17},'Estados vínculos')
load=read(ROOT/'reports/portal-carga.json');sync=read(ROOT/'reports/studio-portal-sync.json')
require(load['shacl']['conforms'] and sync['verificado'] and sync['shacl']['conforms'],'RDF/SHACL/Studio sin validar')
require(load['semantica']['huellas_entrada']['reglas']==sha(ROOT/'ontologia/semantica.json'),'Carga desactualizada')
def suite(name,count):
    p=E/'validacion'/name;text=p.read_text(encoding='utf-8-sig')
    matches=re.findall(r'Ran (\d+) tests? in ([\d.]+)s',text)
    require(matches and int(matches[-1][0])==count and re.search(r'^OK\s*$',text,re.M) and not re.search(r'^FAILED',text,re.M),'Suite no verde '+name)
    return dict(ref(p),pruebas=count,segundos=float(matches[-1][1]),resultado='OK')
tests={'R7':suite('suite-r7-corregida.log',154),'R8':suite('suite-r8-v004.log',181),'regresiones_evidencia_real':suite('regresion-r8.log',9),'antecedentes':[ref(E/'validacion/suite-r8-v001.log'),ref(E/'validacion/suite-r8-v002.log'),ref(E/'validacion/suite-r8-v003.log'),ref(ROOT/'propuestas/suite-r7-inicial.log')]}
rows=copy.deepcopy(before['decisiones']);approved={v['columna'] for v in accepted['vinculos']}
require(len(rows)==202,'Casos no son 202')
for row in rows: row['estado_final']='integrado_r8' if row['id'] in approved else row['estado']
require(sum(r['estado_final']=='integrado_r8' for r in rows)==28,'Integraciones no son 28')
require(sum(r['rol'].startswith('S') for r in rows)==138,'Significados pendientes no son 138')
changes=[]
for rel,m in backup['archivos'].items():
    actual=sha(ROOT/rel)
    if actual!=m['sha256']:
        require(not rel.startswith(('reports/ronda-4','reports/ronda-5','reports/ronda-6','reports/ronda-7','reports/pendientes-depurados','reports/investigacion-post-r6','reports/cierre-brechas-post-r6')),'Informe histórico modificado '+rel)
        changes.append({'ruta':rel,'sha256_antes':m['sha256'],'sha256_despues':actual})
now=datetime.now(timezone.utc)
report={'fecha_utc':now.isoformat(),'fecha_hermosillo':now.astimezone(timezone(timedelta(hours=-7))).isoformat(),'estado':'cerrado_integrado_validado_y_sincronizado','expediente':E.relative_to(ROOT).as_posix(),'mcp':'OpenCode nativo; Muse 1.3 Contributor; Obscura disponible sin nuevas peticiones concretas','delta':{'significados':0,'conceptos':0,'correspondencias_revisadas':28},'resumen_actual':summary,'pendientes':{'significados_reales':138,'vigencias':16,'referencia_catalogo':'des_mpo_res','encabezados_corruptos':2,'candidatas_semanticas':17,'vigencias_acceso_no_resuelto':['V13','V14']},'casos':rows,'conteos_casos':dict(Counter(r['estado_final'] for r in rows)),'seleccion':before['seleccion'],'auditorias':[ref(E/role/name) for role,name in [('A-documental','auditoria-material-v003.json'),('B-tecnica','auditoria-material-v003.json'),('B-tecnica','auditoria-codigo-v003.json'),('C-codigo','auditoria-pruebas.json'),('C-codigo','auditoria-pruebas-r8.json'),('C-codigo','auditoria-ajuste-tests.json')]],'aplicacion':read(E/'aplicacion.json'),'pruebas_aplicadas':read(E/'pruebas-aplicadas.json'),'ajuste_tests':read(E/'ajuste-tests-aplicado.json'),'pruebas':tests,'portal':{'triples_combinados':load['triples_combinados'],'sintaxis':load['sintaxis'],'shacl':load['shacl']},'studio':sync,'integridad':{'preintegracion':ref(E/'comprobacion-preintegracion.json'),'base':ref(E/'base.json'),'respaldo':ref(E/'respaldo-previo.json'),'manifiesto_r8':ref(folder/'manifiesto.json'),'fuentes_cotejadas':len(before['fuentes_cotejadas']),'cambios_respaldados':changes},'limites':['Las 28 asociaciones físicas se apoyan en significados ya aprobados en R7; no son significados nuevos.','No se inventan definiciones, vigencias, equivalencias de catálogos, códigos ni joins.','Los 138 significados y 16 vigencias conservan evidencia faltante y condición de reapertura por caso; sin nueva pista primaria concreta no se repiten búsquedas agotadas.','Los dos encabezados corruptos se conservan como artefactos del original y se excluyen del conteo de significados reales.','Los errores de propuestas previas de M2 (IRI y descripción) fueron corregidos y auditados antes de instalar; sólo se aplicó material v003.','La suite inicial R7 falló por expectativas antiguas; la primera R8 tuvo dos llamadas históricas a una foto R7. Se corrigieron las pruebas conservando sus aserciones.'],'gemma':'excluido_sin_cambios','contactos_externos':0}
md=['# Ronda 8 — ejecución paralela sin Gemma','','## Resultado','','- 28 correspondencias SINAC incorporadas con doble auditoría y evidencia SHA-256.','- **4506 correspondencias revisadas, 17 candidatas y cero ambiguas.**','- **1423 significados respaldados y 1106 conceptos**, sin adiciones de significados en esta ronda.',f"- Studio: **{sync['triples_totales_studio']} triples**, sincronizado y verificado; RDF y SHACL conformes.",'','## Pruebas','','- R7 corregida: **154 pruebas OK**.','- R8 final: **176 pruebas OK**, incluidas regresiones de IRI, descripciones originales, huellas, universo de columnas y doble aprobación exacta.','- Los resultados iniciales y correcciones se preservan en el expediente.','','## Pendientes externos','','| Frente | Significados pendientes |','| --- | ---: |','| Defunciones | 32 |','| Nacimientos | 22 |','| Matrículas | 30 |','| Epidemiología | 25 |','| TIC | 24 |','| Diversos | 5 |','','Quedan **138 significados, 16 vigencias y 17 correspondencias candidatas** dependientes del respaldo faltante. V13/V14 conservan acceso no resuelto. `des_mpo_res` sigue sin catálogo aplicable identificado; los dos encabezados corruptos permanecen como evidencia del original, fuera del conteo de significados reales.','','Los agentes revisaron los 202 casos asignados. La documentación ya examinada no aporta una resolución adicional de las brechas externas; cada caso del JSON conserva fuentes, evidencia faltante y condición para reabrir. Obscura quedó disponible; no hubo peticiones web con pista primaria nueva concreta.','','## Integridad y alcance','','Se preservaron los manifiestos anteriores, los significados de R7 y los respaldos. Las 28 asociaciones físicas no autorizan joins, identidades entre catálogos, vigencias ni códigos no documentados. Gemma quedó excluido y no se contactó a publicadores.','','[Casos, versiones, auditorías, pruebas, respaldos y recibo de Studio](ronda-8.json).','']
report['io_atomico']=read(E/'io-atomico-aplicado.json')
report['auditorias'].append(ref(E/'C-codigo/auditoria-io-atomico.json'))
report['io_reintentos']=read(E/'io-retry-aplicado.json')
report['auditorias'].append(ref(E/'C-codigo/auditoria-io-retry.json'))
report['incidencias_io']=[ref(E/'validacion/portal-r8.log'),ref(E/'validacion/portal-r8-v002.log'),ref(E/'validacion/portal-r8-v003.log')]
md=[line.replace('**176 pruebas OK**',f"**{tests['R8']['pruebas']} pruebas OK**") for line in md]
for name in ('ronda-8.json','ronda-8.md'): require(not (ROOT/'reports'/name).exists(),'Informe ya existe')
(ROOT/'reports/ronda-8.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'reports/ronda-8.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'estado':report['estado'],'resumen':summary,'tests':tests['R8']['pruebas'],'studio':sync['triples_totales_studio']}))
