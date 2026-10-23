# Estructuras, diccionarios y primer cruce

## Qué está incorporado

La ejecución inspeccionó los 486 recursos del inventario existente. De ellos, 484 tienen evidencia accesible. Se añadieron 464 esquemas de hojas/archivos y 5,675 columnas a los 78 esquemas y 910 columnas DataStore previos. Total: 542 esquemas y 6,585 columnas observadas.

Los 88 diccionarios se leyeron completos dentro de los límites de la herramienta. Contienen 1,570 filas recuperadas, de las que 1,563 tienen nombre de variable. Las otras 7 permanecen en la evidencia JSON y no se convierten en definiciones sin nombre. Se conservan las descripciones, unidades declaradas y los demás campos originales, sin validar automáticamente su exactitud.

Los dos recursos sin acceso son Ganadería Sonora año 2013 y Datos hídricos 1960–1969. La API `resource_show` confirma URL vacía y `datastore_search` devuelve 404 para ambos. Sus intentos y consultas están registrados en `data/portal/inspecciones/`.

## Relaciones nuevas

- Recurso → `mex:inspeccionContenido` → resultado, método, fecha y procedencia.
- Recurso → `mex:esquemaArchivo` → esquema por hoja → `mex:columna` → columna observada.
- Diccionario → `mex:definicionVariable` → definición declarada y fila original.
- Columna → `mex:definicionCandidata` → definición con nombre normalizado único dentro del mismo conjunto.
- Columna → `mex:rolCandidato` → dimensión sugerida por la descripción del diccionario.
- Cruce → `mex:resumenMunicipal` → conteos agregados por código local y año.

Las columnas de archivo se identifican por recurso, hoja y posición; esto distingue etiquetas repetidas. Si cambia el orden de un archivo, hay que volver a inspeccionarlo: no se promete identidad estable de esas columnas frente a cambios estructurales. Las columnas DataStore conservan su identidad por recurso y nombre.

Las 4,669 correspondencias candidatas no son equivalencias semánticas globales. La comparación elimina acentos y diferencias de mayúsculas y espacios, pero no transforma valores, unidades ni códigos. Se excluyen los casos con más de una definición candidata.

## Cruce ejecutado

Se eligieron matrimonios y divorcios de 2022 porque ambos permiten consulta DataStore, tienen la misma dependencia publicadora y sus diccionarios definen el municipio como «Municipio de registro» y el año como año de registro. La consulta recupera únicamente `_id`, `municipio` y el campo del año, con paginación ordenada. Comprueba IDs únicos, totales exactos y estables y cobertura temporal 2022.

Se agregaron 13,881 filas de matrimonios y 6,064 de divorcios. La unión externa produce 67 códigos locales; 62 aparecen en ambas fuentes. Los 5 sin observaciones de divorcios conservan ausencia, sin inventar un cero. El cruce usa las claves locales de estas dos fuentes: no afirma correspondencias oficiales INEGI ni nombres municipales. La API no ofrece una instantánea transaccional; las comprobaciones no detectan todas las posibles ediciones concurrentes.

No se vinculan personas, cohortes ni matrimonios con sus divorcios. Los conteos no representan una tasa de divorcio. Los resultados completos y fuentes están en [primer-cruce.md](../reports/primer-cruce.md).

## Reproducción y actualización

```powershell
uv sync
uv run python scripts/inspeccionar_contenido.py
uv run python scripts/cruzar_registro_civil.py
uv run python scripts/mapear_cruces.py
uv run python scripts/validar_lote_cruces.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
```

Ejecutar cada paso solo si el anterior termina correctamente. La inspección reutiliza archivos JSON fechados para reanudar el trabajo; `--retry-errors` reintenta fallos y `--refresh` fuerza una nueva consulta completa. No hay monitor programado. Si cambia el catálogo, primero actualizar el catálogo base y el inventario; la ampliación verifica sus identificadores. El cruce actual está fijado a 2022 y sus dos fuentes: una integración de otro año exige revisar sus campos y diccionarios.

Los CSV de datos se inspeccionan con un prefijo de 128 KiB. Los diccionarios se leen completos, hasta 10,000 filas y 20 MiB. Los Excel pequeños se leen en memoria con límite de 20 MiB; los XLSX grandes permiten acceso por rangos HTTP con comprobación de tamaño/ETag y límite de transferencia de 64 MiB. El XLS antiguo de 36.7 MB requirió leer su contenedor completo en memoria. No se guardan esos archivos ni filas de datos; se conservan esquemas, diccionarios, huellas de archivos o rangos y agregados del cruce.

El detector actual revisa hasta 30 filas por hoja para proponer encabezados. Eso no valida todas las filas ni la estabilidad del esquema. En GeoJSON se observan las propiedades de la primera entidad, sin incorporar geometrías. No se establece el linaje de los tableros Power BI.

## Validación y Studio

El grafo generado contiene 90,142 triples y 10,135 individuos. Studio conserva sus etiquetas y ediciones previas y contiene 90,751 triples. Se respaldó el estado previo, se validó con SHACL antes de sincronizar y se comprobó que el resultado coincide con el previsto. No hubo infracciones. Las 23 pruebas cubren también paginación duplicada, códigos inválidos, etiquetas de columna repetidas y valores ausentes.

Volver a abrir Studio permite refrescar el árbol. Buscar las clases «Definición declarada de variable», «Inspección de contenido», «Cruce agregado» y «Resumen por código municipal local». La vista 3D sigue representando clases. El antiguo límite global de 2,000 individuos se corrigió posteriormente: el árbol instalado recupera los 15,904 individuos actuales, incluidas las 6,585 columnas, con filas virtualizadas. Detalles en [studio-limite-individuos.md](studio-limite-individuos.md). La validación completa está en los informes del pipeline.

```powershell
uv run python scripts/consultar_catalogo.py --portal queries/portal/resumen.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/estructuras_pendientes.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/definiciones.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/primer_cruce.rq
```

El catálogo base conserva su estado histórico de inspección. La consulta de pendientes da prioridad al resultado de la nueva inspección; por eso no confunde sus antiguos 408 pendientes con el estado actual de 484 inspecciones correctas y 2 recursos sin acceso.

## Mapa de oportunidades posterior

Se añadió la evaluación de todos los 3,916 pares del catálogo: 1,191 candidatos, 396 con dimensiones insuficientes, 2,328 sin clave reconocida y 1 par con un cruce exploratorio previo. Esto amplía los conteos del grafo indicados en la sección anterior; consultar `reports/portal-carga.json` y `reports/studio-portal-sync.json` para el estado vigente.

`scripts/mapear_cruces.py` usa exclusivamente la evidencia local. Reconoce familias de claves y estratos sin convertir coincidencias nominales en equivalencias. Conserva todos los nombres de campos compartidos como pistas, aunque no sean claves reconocidas. Descarta campos internos y no propone identificación de personas. Las incompatibilidades o sentidos diferentes se registran para revisión, sin presentar el par como aprobado.

Cada conjunto tiene un `mex:PerfilClaves` y cada par una `mex:EvaluacionCruce`, con conjuntos A/B, familias, estado, prioridad de revisión, pendientes y procedencia hacia el informe completo. Los años extraídos de nombres de recursos solo son pistas: no demuestran cobertura temporal ni solapamiento. La prioridad tampoco demuestra compatibilidad.

El par Matrimonios–Divorcios conserva expresamente el alcance de sus dos recursos de 2022; no se presenta como ejecutado para todos los años. No se ejecutaron joins nuevos ni combinaciones de tres o más conjuntos. Para ejecutarlos habrá que elegir medidas, validar dominios/valores y establecer grano y cardinalidad.

Mapa legible: [oportunidades-cruce.md](../reports/oportunidades-cruce.md). Para buscar o inspeccionar un par:

```powershell
uv run python scripts/consultar_cruces.py --buscar salud --limite 10
uv run python scripts/consultar_cruces.py --id ID_DEL_PAR
uv run python scripts/consultar_catalogo.py --portal queries/portal/oportunidades_resumen.rq
```

Se añadieron pruebas de cobertura de todos los pares, diferencias entre registro/residencia, claves código/nombre, contextos de localidad, CLUES, programas educativos y estratos. Total actual: 33 pruebas.

El lote posterior de 98 candidatos está ejecutado y documentado en [validacion-por-lotes.md](validacion-por-lotes.md). El total vigente es de 43 pruebas; dos comparaciones educativas se ejecutaron con alcance exploratorio, y las demás conservan decisiones y causas pendientes.
