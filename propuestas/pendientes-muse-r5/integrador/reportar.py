from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import copy,hashlib,json,shutil
R=Path(__file__).resolve().parents[3];S=R/'propuestas/pendientes-muse-r5'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 c=read(R/'data/semantica/cobertura.json');accepted=read(R/'data/integracion-ronda-5/aceptadas.json')
 pending=[v for v in c['variables'] if v['estado']!='respaldada_por_definicion'];assert len(pending)==171
 ids={v['definicion_iri'] for v in pending};approved={d for r in accepted['reglas'] for d in r['definiciones']}
 assert len(approved)==8 and not ids.intersection(approved)
 decisions={}
 for role in ['nacimientos','defunciones','matriculas','epidemiologia','tic','diversos']:
  for d in read(S/role/'entrega.json')['decisiones_significados']:decisions[d['definicion_iri']]=d
 for v in pending:v['dictamen_documental']=decisions[v['definicion_iri']]
 write(R/'reports/pendientes-ronda-5.json',{'significados':pending,'conteo':171,'columna_ambigua':read(S/'presas/entrega.json'),'catalogos':read(S/'catalogos-web/entrega.json'),'limite':'Una investigación documental no acredita valores, comparabilidad ni vigencia sin vínculo a fuente y periodo.'})
 draft=read(S/'diversos/solicitudes-publicador.json');groups=[]
 for group in draft['grupos']:
  g=copy.deepcopy(group);g['iris']=[v for v in g['iris'] if v['definicion_iri'] in ids];g['n']=len(g['iris'])
  if g['n']:groups.append(g)
 assert {v['definicion_iri'] for g in groups for v in g['iris']}==ids
 draft.update(grupos=groups,alcance='171 significados aún pendientes tras integrar 8; columna presas y 17 referencias de catálogo aparte. Borrador local, sin envío.',resueltos_excluidos=sorted(approved))
 write(R/'reports/solicitudes-publicador-ronda-5.json',draft)
 lines=['# Aclaraciones documentales para publicadores','', 'Borrador local: no se ha enviado ni contactado a nadie. Contiene únicamente los 171 significados todavía pendientes; los ocho resueltos están excluidos. Por cada fila se necesita una definición completa y su vínculo a recurso, edición y periodo. Las preguntas de contexto del JSON deben ajustarse a la lista final de filas.', '']
 for g in groups:
  lines += ['## '+g['titulo_conjunto'],'',f"Diccionario: `{g['diccionario']}`. Filas pendientes: {g['n']}.",'']
  for v in g['iris']:
   d=decisions[v['definicion_iri']];lines += ['- `'+v['variable']+'` — '+v['definicion_iri']+' — '+str(d.get('motivo','Falta definición documental suficiente.'))]
  lines+=['']
 lines+=['## Presas y catálogos','','Para `cat_estatal/Clave` se requiere acreditar a qué hoja del diccionario corresponde y su dominio. Para las 16 referencias con recurso de catálogo identificado se requiere edición y vínculo de adopción al recurso y periodo. `des_mpo_res` necesita además identificar el catálogo aplicable. Las fechas de publicación y la semejanza de valores no bastan.','']
 (R/'reports/solicitudes-publicador-ronda-5.md').write_text('\n'.join(lines),encoding='utf-8')
 native=read(R/'reports/portal-carga.json');live=read(R/'reports/ronda-5-studio.json');sync=read(R/'reports/studio-portal-sync.json')
 assert native['shacl']['conforms'] and sync['shacl']['conforms'] and live['verificado']
 log=(S/'integrador/pruebas-finales-2.log').read_text(encoding='utf-8-sig');assert 'Ran 130 tests' in log and log.rstrip().endswith('OK')
 repairs=R/'data/integracion-ronda-5-compatibilidad'
 if not repairs.exists():
  audit=read(S/'auditoria-b/revision-tests-sync.json')
  for item in audit['revisiones']:
   if sha(R/item['archivo'])!=item['sha_actual']:raise ValueError('Reparación distinta de la auditada')
   dest=repairs/item['archivo'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/item['archivo'],dest)
  shutil.copy2(S/'auditoria-b/revision-tests-sync.json',repairs/'auditoria.json')
  write(repairs/'manifiesto.json',{'archivos':{p.relative_to(repairs).as_posix():sha(p) for p in repairs.rglob('*') if p.is_file()},'ronda5_manifiesto_sha256':read(R/'ontologia/revision-ronda-5.json')['manifiesto_sha256']})
 out={'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'investigación completada e integración validada; brechas documentales externas conservadas','agentes':10,'modelo_agentes':'opencode-go/muse-spark-1.3-contributor','significados_investigados':179,'significados_resueltos':8,'significados_pendientes':171,'por_rol':{'nacimientos':{'iniciales':54,'resueltos':1,'pendientes':53},'defunciones':{'iniciales':32,'resueltos':0,'pendientes':32},'matriculas':{'iniciales':30,'resueltos':0,'pendientes':30},'epidemiologia':{'iniciales':25,'resueltos':0,'pendientes':25},'tic':{'iniciales':31,'resueltos':7,'pendientes':24},'diversos':{'iniciales':7,'resueltos':0,'pendientes':7}},'resumen':c['resumen'],'columna_ambigua':1,'vinculos_ambiguos':2,'catalogos_con_recurso_sin_vigencia':16,'referencia_catalogo_sin_resolver':1,'pruebas':{'total':130,'resultado':'OK','log':'propuestas/pendientes-muse-r5/integrador/pruebas-finales-2.log'},'shacl_generado':native['shacl'],'shacl_studio':sync['shacl'],'studio':live,'triples_studio':sync['triples_totales_studio'],'investigacion_web':{'herramienta':'MCP Obscura','solicitudes_unicas':33,'respuestas':34,'respuesta_duplicada_preservada':1,'pdf_oficiales':5,'manifiesto_sha256':sha(R/'data/integracion-ronda-5-web/manifiesto.json')},'manifiesto_nucleo_sha256':read(R/'ontologia/revision-ronda-5.json')['manifiesto_sha256'],'manifiesto_compatibilidad_sha256':sha(repairs/'manifiesto.json'),'rechazos':{'propuestas_matriculas_retiradas':15,'motivo':'Descripción ausente, truncada o tautológica; nombre/ejemplo no aportan respaldo suficiente.'},'chat':{'modelo_solicitado':'gemma-4-31b-it','configurado_e_instalado':True,'activacion_en_interfaz':'no confirmada: Computer Use emitió señal de parada; se detuvieron acciones de interfaz','pruebas_reales':'F2 respondió con contexto corregido; otras consultas HTTP500 del proveedor; no se certifica todo el chat.','presupuesto_entrada_estimado':6500,'pruebas_sidecar':'49 pasan, 1 omitida'},'contactos_externos_enviados':0}
 write(R/'reports/ronda-5.json',out)
 text='''# Ronda 5: investigación e integración verificadas

Se investigaron los 179 significados con **10 agentes OpenCode/Muse 1.3**, búsquedas con MCP Obscura y dos revisiones independientes. Se integraron **8 significados, 3 conceptos y 8 correspondencias**. El núcleo queda en **1392 significados respaldados, 1075 conceptos y 4474 correspondencias revisadas**. Toda la base anterior se conservó.

Las **130 pruebas pasan**. SHACL nativo del grafo completo y del estado previsto de Studio termina sin violaciones; las consultas SELECT del Studio vivo confirman el resultado. Studio conserva 321209 triples, incluidas sus ediciones ajenas a la ampliación. Las tres fichas de cruce, 72 comparaciones de 2020 y 144 evidencias se mantienen.

## Resultado documental

| Grupo | Investigados | Resueltos | Pendientes |
|---|---:|---:|---:|
| Nacimientos | 54 | 1 | 53 |
| Defunciones | 32 | 0 | 32 |
| Matrículas | 30 | 0 | 30 |
| Vigilancia epidemiológica | 25 | 0 | 25 |
| TIC | 31 | 7 | 24 |
| Diversos | 7 | 0 | 7 |
| Total | 179 | 8 | 171 |

Se respaldó el indicador textual de residencia extranjera de la madre y siete campos de encuestas TIC: cinco declaraciones de sector, una lista de condiciones para innovación y la consignación textual de recursos anuales para innovación. Las reglas conservan los límites documentales: no acreditan moneda, cantidades, catálogos, identidad de medidas ni comparabilidad entre encuestas.

Se retiraron 15 propuestas iniciales de matrículas al comprobar que no tenían respaldo más allá de nombres, ejemplos o descripciones incompletas. Los reglamentos UES de 2019/2022 y la guía de titulación de 2023 aportan contexto, pero no resuelven las definiciones y códigos del recurso local de 2022. La adenda documenta además que el reglamento previo sí contiene equivalentes numéricos; eso no define los promedios ni su método.

La búsqueda ampliada atendió **33 solicitudes únicas** (34 respuestas, una repetida de presas) y preservó cinco PDF oficiales. No se localizó evidencia suficiente para acreditar la hoja de destino de `cat_estatal/Clave`, la vigencia histórica de los 16 catálogos identificados ni el catálogo aplicable a `des_mpo_res`. No se afirma ausencia universal de documentación; se registra lo revisado y la brecha exacta.

## Evidencia y siguiente dependencia

- `pendientes-ronda-5.json`: 171 definiciones con dictamen y evidencia faltante, más presas y catálogos.
- `solicitudes-publicador-ronda-5.md` y `.json`: borradores locales con los ocho casos resueltos excluidos; no se contactó a nadie.
- `data/integracion-ronda-5/`: adiciones, base y auditorías fijadas por manifiesto.
- `data/integracion-ronda-5-web/`: investigación ampliada, documentos y adenda.
- `data/integracion-ronda-5-compatibilidad/`: ajustes de pruebas históricas y manejo del archivo abierto en Windows, auditados por separado. Los manifiestos anteriores no se reescribieron.

Para resolver los 171 casos restantes se requieren definiciones completas, correcciones del publicador o vínculos documentales al recurso y periodo. Más agentes no sustituyen esa evidencia.

Gemma 4 31B permanece configurado y su ajuste está instalado. Una prueba real de F2 respondió; otras consultas recibieron HTTP500 del proveedor. El control de Studio emitió una señal de parada y se detuvieron las acciones de interfaz: **no se confirmó la activación del nuevo sidecar ni se certifica todo el chat**.
'''
 (R/'reports/ronda-5.md').write_text(text,encoding='utf-8')
 write(S/'estado.json',{'estado':'investigacion_completada_integracion_validada','agentes':10,'investigados':179,'resueltos':8,'pendientes':171,'columna_ambigua':1,'referencias_catalogo_pendientes':17,'pruebas':130,'shacl':True,'studio_verificado':True,'chat_activacion':'no confirmada por interrupción de Computer Use','informe':'reports/ronda-5.md'})
 print('Informes y borradores finales escritos: 171 pendientes, 8 resueltos, 130 pruebas OK.')
if __name__=='__main__':main()
