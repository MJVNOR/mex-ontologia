from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3]
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
c=read('data/semantica/cobertura.json');load=read('reports/portal-carga.json');live=read('reports/ronda-4-studio.json');sync=read('reports/studio-portal-sync.json')
out={'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'núcleo integrado y verificado; chat en fase de instalación y prueba','resumen':c['resumen'],'significados_respaldados':1384,'significados_pendientes':179,'conceptos':1072,'correspondencias_revisadas':4466,'adiciones':{'significados':172,'conceptos':132,'correspondencias':3601},'columnas_ambiguas':1,'vinculos_ambiguos':2,'referencias_catalogo_sin_vigencia':16,'referencias_catalogo_no_resueltas':1,'pruebas_centrales':{'total':121,'resultado':'OK','log':'propuestas/pendientes-muse-r4/integrador/pruebas-finales-corregidas-2.log'},'shacl':load['shacl'],'grafo_generado':load['stats'],'studio':live,'sincronizacion':sync,'manifiesto_ronda4_sha256':'c9edd8a180b0c79cc4c3eacce3c9e52009ddb63e68951db7181c6a377da046f2','reparacion_historia_manifiesto_sha256':'c4d7b52a18fa437fb810611d2be50998965ec8d04b160d4c8cf4eb0bd52c8528','modelo_chat_solicitado':'gemma-4-31b-it','chat_real_final':'pendiente de activar sidecar compilado y pruebas espaciadas','ronda5':'Investigación de 179 significados + presas + catálogos en curso; no confundir propuestas con integraciones.'}
(R/'reports/ronda-4.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='''# Ronda 4: núcleo integrado

Se integraron 172 significados, 132 conceptos y 3601 correspondencias revisadas. El resultado contiene **1384 significados respaldados, 1072 conceptos y 4466 correspondencias revisadas**. Las 121 pruebas centrales pasan y la validación SHACL nativa del grafo completo no registra violaciones.

Los 1212 significados y 865 vínculos de la base se conservaron exactamente. Continúan las tres fichas de cruce, las 72 comparaciones de 2020 y sus 144 evidencias. No se confunde igualdad de código con identidad ni se extiende F2 a otros años.

Las consultas SELECT del Studio vivo confirman los conteos. La sincronización preservó las ediciones ajenas; se verificaron 320869 triples vivos. Windows impidió guardar el archivo canónico abierto (error 1224) después de aplicar y comprobar los cambios. El estado vivo y la propiedad gestionada quedaron recuperados, con copia íntegra y huella en `studio-portal-sync.json`; queda sustituir la copia canónica al cerrar ese archivo.

Se conservan el manifiesto original y los dictámenes históricos. La compatibilidad de cuatro promociones posteriores se fijó por separado en `data/integracion-ronda-4-historia/`; la revisión explícita de Año/ano está probada sin aprobar la normalización automática de eñe.

Quedan 179 significados sin respaldo suficiente para incorporarlos, una columna física ambigua (dos vínculos candidatos), 16 vigencias de catálogos sin acreditar y una referencia a catálogo sin resolver. La ronda 5 investiga estos casos con especialistas, búsquedas primarias y revisión independiente. Los pendientes de documentación no se cierran por semejanza de nombres o fechas de descarga.

El modelo solicitado para el chat es **Gemma 4 31B**. La instalación del contexto corregido y las pruebas reales espaciadas siguen en curso; este informe no certifica todavía el chat final ni la interfaz.

Detalle verificable: `ronda-4.json`, `ronda-4-studio.json`, `portal-carga.json`, `studio-portal-sync.json` y las entregas fijadas en `data/integracion-ronda-4/`.
'''
(R/'reports/ronda-4.md').write_text(text,encoding='utf-8')
print('Informes ronda-4.md/json actualizados')
