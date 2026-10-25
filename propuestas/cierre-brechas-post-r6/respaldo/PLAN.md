# Plan: ontología del portal de datos abiertos de Sonora

## Objetivo

Mapear progresivamente todo el portal https://datos.sonora.gob.mx/: primero su catálogo, después las secciones y visualizaciones enlazadas, las estructuras de sus recursos y las entidades compartidas entre contenidos. El objetivo es cruzar información entre fuentes, sin exigir copiar todas las filas al grafo.

Open Ontologies es el motor para cargar RDF, validar, inferir relaciones y consultar el grafo con SPARQL.

## Estado vigente y siguiente trabajo documental

La [ronda 6](reports/ronda-6.md) quedó integrada: 1,392 significados respaldados, 1,075 conceptos, 4,475 correspondencias revisadas, 20 candidatas y cero ambiguas. La depuración posterior, realizada con tres agentes OpenCode en paralelo, conserva los 171 registros históricos como 169 significados pendientes reales y dos encabezados corruptos separados de la vista accionable.

El [informe consolidado](reports/pendientes-depurados.md) y su [JSON](reports/pendientes-depurados.json) enumeran los pendientes por fuente, sus localizadores y criterios de aceptación, junto con 16 brechas de vigencia y la anomalía heredada `des_mpo_res`. Se cotejaron las 171 huellas de fila en 17 diccionarios. No se aprobaron definiciones ni vigencias nuevas, no se contactó a publicadores y el grafo permanece igual.

La [investigación posterior a R6](reports/investigacion-post-r6.md) ya examinó los 169 casos con seis agentes OpenCode en paralelo y auditorías independientes. Se completó el examen por ID del manual SEED 2022 y se preservaron nuevas fuentes SINAC, UES, epidemiología, TIC y CONAPO. No hubo promociones acreditadas; las brechas se mantienen individualizadas. La coincidencia documental de 2129 filas y 28 campos del extracto Sonora de CONAPO acredita procedencia, pero los diccionarios siguen sin definir el objeto clasificado por `CLASIF`. La extensión R7 preparada permanece sin aplicar. Las pruebas adicionales del chat se posponen por decisión del usuario.

## Antecedentes: consolidación semántica inicial

El proyecto vuelve a centrarse en la ontología del portal. Los inventarios y análisis ya realizados se conservan como evidencia; no se prioriza acumular triples ni ejecutar todos los pares. Se consolida la separación entre publicaciones, columnas, definiciones, variables locales, conceptos compartidos, catálogos y entidades de referencia.

La ampliación de cobertura incorpora 980 significados tras la revisión de ocho roles con Muse 1.3: 940 conceptos, 1,212 variables respaldadas, 23 candidatas y 328 definiciones fuera del núcleo, sobre 1,563 definiciones. Conserva seis condiciones de conexión y las 836 correspondencias revisadas. Hay ahora 3,312 candidatas y 12 vínculos ambiguos sobre 6 columnas: el crecimiento de significados no revisa automáticamente columnas. Un sistema de códigos se asocia exclusivamente a su fuente; 16 referencias declaradas tienen un recurso de catálogo identificado y una queda sin resolver: `des_mpo_res`.

Reglas y evidencia fijada en `ontologia/semantica.json`, `ontologia/revision-cobertura.json`, `data/integracion-cobertura/` y [resultado de cobertura](reports/cobertura-muse.md). La [ronda 2](reports/integracion-ronda-2.md) queda como antecedente histórico. La suite actual se ejecuta con `uv run python -m unittest discover -s tests -v`; las pruebas de la ampliación verifican también los calificadores en RDF, la procedencia y la preservación de interpretaciones anteriores. El siguiente trabajo es revisar las nuevas correspondencias candidatas y obtener documentación de los significados pendientes. La auditoría de las 5,523 columnas y las cinco observaciones originales están en [pendientes semánticos](reports/pendientes-semanticos.md).

La capa quedó cargada y sincronizada en Studio con respaldo, conservación del estado previo y SHACL sin infracciones. El estado vigente está en `reports/portal-carga.json` y `reports/studio-portal-sync.json`. La referencia CVEGEO se limita a su columna original; no se generaliza a otros códigos.

Se incorporaron 32 dictámenes de pendientes y 14 preguntas al publicador preparadas sin enviar; estos dictámenes no promueven significados candidatos. Las 16 revisiones de vigencia histórica siguen sin acreditarla. La evaluación histórica del pipeline fuente del chat fue parcial: 20 intentos, 4 respuestas (2 aciertos y 2 fallos de recuperación) y 16 errores HTTP/cuota. Quedan pendientes la evaluación de la interfaz de Studio y la comprobación de identidad con el backend instalado.

## Revisión territorial incorporada

Se leyeron 15 archivos de catálogos con 23 hojas territoriales; las copias idénticas comparten referencia por SHA-256 y hoja conservando todas sus fuentes. Hay nueve referencias distintas y 570 entradas. Se registran 504 correspondencias calificadas con el GeoJSON, dos categorías no municipales; el alias Magdalena de Kino / Magdalena queda revisado por el usuario para las entradas de Sonora. No se transfieren estas correspondencias automáticamente a columnas de datos ni a otros años. La segunda ronda cotejó las 1,850 localidades observadas IML con ITER 2020: coinciden clave, nombre y población. Quedan sin acreditar el motivo de las 5,450 localidades presentes solo en ITER, la equivalencia con el universo del Marco Geoestadístico y la vigencia histórica. Evidencia: [catálogos territoriales](reports/catalogos-territoriales.md), [ronda 2](reports/integracion-ronda-2.md), `data/territorio/` y `ontologia/territorio.json`.

## Enfoque acordado

- Primero el catálogo; después el contenido.
- Consultar la API de CKAN sin descargar masivamente los archivos del portal.
- Usar DCAT como base para describir el catálogo.
- Conservar identificadores, enlaces y procedencia de los datos.
- No elegir todavía un dominio de contenido: la exploración del catálogo ayudará a seleccionarlo.
- La API consulta el portal; Open Ontologies consulta el grafo que hayamos cargado. Prepararemos un proceso que transforme las respuestas de la API a RDF.
- Podemos guardar respuestas o muestras para reproducir una ejecución, sin que eso implique descargar todos los recursos.

## Fase 1. Explorar el catálogo mediante la API

1. Consultar los conjuntos y sus metadatos, usando paginación.
2. Inspeccionar dependencias, temas, etiquetas y recursos disponibles.
3. Identificar qué campos describen cobertura territorial, cobertura temporal, actualización y licencia.
4. Documentar campos ausentes, inconsistentes o ambiguos, sin inventar valores.

Punto de entrada comprobado:

```text
https://datos.sonora.gob.mx/api/3/action/package_search
```

**Entregable:** inventario de campos y propuesta de correspondencias entre CKAN y el modelo semántico.

## Fase 2. Diseñar la ontología del catálogo

Representar, reutilizando DCAT y vocabularios complementarios cuando corresponda:

- Catálogo.
- Conjunto de datos.
- Dependencia u organización publicadora.
- Recurso o distribución descargable.
- Tema y etiquetas.
- Formato y enlaces de acceso o descarga.
- Licencia.
- Fechas de publicación y modificación.
- Cobertura territorial y temporal, cuando esté documentada.

Definir identificadores estables y distinguir el periodo representado por los datos de la fecha de modificación de sus metadatos.

Preguntas iniciales:

- ¿Qué conjuntos publica cada dependencia?
- ¿Qué conjuntos corresponden a un tema?
- ¿Qué recursos y formatos ofrece cada conjunto?
- ¿Qué cobertura territorial y temporal declara cada conjunto?
- ¿Qué metadatos faltan para evaluar posibles cruces?

**Entregable:** modelo del catálogo en Turtle (`.ttl`) y documentación de las decisiones de modelado.

## Fase 3. Incorporar los metadatos al grafo

1. Implementar consultas de lectura a la API.
2. Transformar las respuestas a RDF con las correspondencias acordadas.
3. Cargar el resultado en un almacén persistente de Open Ontologies, separado del almacén de prueba.
4. Registrar fuente y fecha de extracción.
5. Definir cómo actualizar registros, tratar cambios y evitar duplicados.

**Entregable:** proceso reproducible de consulta, transformación y carga del catálogo, sin descargar el contenido de todos los conjuntos.

## Fase 4. Validar y consultar el catálogo

1. Validar sintaxis RDF.
2. Definir reglas SHACL para identificadores, relaciones y metadatos requeridos por nuestro modelo.
3. Reportar faltantes y errores sin confundirlos con información inexistente en el mundo real.
4. Preparar consultas SPARQL que respondan las preguntas iniciales.
5. Comprobar una muestra de resultados contra la API de origen.

**Primer entregable funcional:** catálogo de Sonora consultable en Open Ontologies, con consultas de ejemplo y reporte de calidad de metadatos.

## Fase 5. Inventariar cobertura e identificar cruces potenciales

1. Inventariar las secciones y visualizaciones enlazadas fuera de CKAN, así como todas las organizaciones y grupos registrados.
2. Clasificar todos los recursos y registrar su forma de acceso, esquema observado y cobertura pendiente; priorizar candidatos para integración sin limitar el objetivo global a un dominio.
3. Inspeccionar esquemas o muestras del contenido para confirmar variables compartidas, claves, unidades y granularidad.
4. Revisar si las filas pueden consultarse mediante API o si requieren descargar un archivo específico.

Los metadatos sugieren cruces; no garantizan que dos conjuntos sean compatibles.

**Entregables:** inventario de cobertura actualizable, estructuras observadas y selección justificada del primer módulo de integración.

## Fase 6. Ampliar la ontología por módulos hasta cubrir el portal

1. Modelar las entidades y observaciones necesarias para la pregunta elegida.
2. Definir claves comunes y correspondencias entre identificadores.
3. Consultar o descargar únicamente los recursos necesarios.
4. Normalizar valores, periodos y unidades cuando corresponda.
5. Incorporar el contenido y enlazarlo con sus conjuntos y recursos de origen.
6. Validar relaciones y ejecutar el primer cruce verificable.
7. Repetir el proceso por los demás dominios y recursos, manteniendo un estado explícito de cobertura, pendientes y cambios de estructura.

No inferir relaciones que las fuentes no sostienen. Por ejemplo, la ubicación de una presa en un municipio no demuestra que lo abastezca.

**Entregable incremental:** contenidos de cada módulo consultables y con procedencia trazable. El primer cruce valida el proceso; el objetivo continúa siendo la cobertura del portal completo.

## Antecedentes: catálogo, estructuras y primer cruce

Los resultados y conteos de esta sección y de las etapas siguientes describen sus respectivas integraciones históricas. El resumen inicial y reports/cobertura-muse.md recogen el estado de la ampliación semántica.

- Ejecutable de Open Ontologies en `tools/open-ontologies.exe`.
- Carpeta `tools` agregada al PATH del usuario.
- Prueba de validación, carga, inferencia RDFS y consulta completada correctamente.
- Ejemplo ficticio en `examples/prueba.ttl`; almacén de prueba en `store-prueba`.
- Consulta de lectura de la API de Sonora comprobada; reportó 89 conjuntos al momento de la revisión. El número puede cambiar.
- Exploración sistemática implementada en `scripts/explorar_catalogo.py`, usando Python 3.12 y la biblioteca estándar.
- Diagnóstico e inventario generados en `reports/`; propuesta de correspondencias en `docs/mapeo-catalogo.md`.
- Base provisional acordada: `https://example.org/mex-ontologi/`, configurable en `config.toml`.
- Modelo y grafo generados en `data/catalogo/`; cargados en una instantánea persistente bajo `store/` mediante `scripts/construir_catalogo.py --load`.
- Validación estructural SHACL y consultas por dependencia, tema, formato y recursos sin URL implementadas y ejecutadas. Resultados en `reports/catalogo-carga.json`.
- Studio nativo compilado, instalado y conectado con una copia editable del catálogo en `data/catalogo/studio-live.ttl`. Instalación y correcciones locales documentadas en `docs/studio-instalacion.md`.
- Inventario ampliado implementado en `scripts/inventariar_portal.py`: páginas de datos enlazadas, clasificación de recursos y consulta de esquemas DataStore sin filas. Evidencia en `data/portal/`; reporte en `reports/cobertura-portal.md`.
- Páginas, visualizaciones y esquemas incorporados mediante `scripts/ampliar_portal.py`: 45 páginas, 62 destinos de visualización, 78 esquemas, 910 columnas y 78 servicios DataStore. Se completaron las 31 organizaciones y 8 grupos.
- Grafo ampliado cargado en un almacén nuevo y validado con SHACL, incluido un control negativo. Consultas en `queries/portal/` e informe en `reports/portal-carga.json`.
- Ampliación sincronizada con la copia editable de Studio, con respaldo y comprobación de conservación de sus datos previos. Detalles en `docs/modelo-portal.md`.
- Inspección restante ejecutada: 486 recursos con intento registrado; 484 accesibles y 2 sin URL ni DataStore. Se leyeron los 88 diccionarios completos y se extrajeron 1,563 definiciones con nombre; 7 filas sin nombre permanecen como evidencia sin inventar variables.
- Incorporados 464 esquemas de archivo y 5,675 columnas, además de los esquemas DataStore previos. Detección de encabezados explícitamente heurística y correspondencias candidatas dentro de cada conjunto; 4,669 columnas tienen una definición candidata única.
- Primer cruce ejecutado por API: matrimonios y divorcios registrados en 2022, de la misma dependencia publicadora y con definiciones compatibles de municipio/año de registro. Agregadas 13,881 y 6,064 filas en 67 resúmenes locales, 62 con observaciones en ambas fuentes. Sin conservar microdatos ni inferir equivalencias INEGI.
- Grafo actualizado y sincronizado con respaldo en Studio. SHACL conforme sobre ambos estados y 23 pruebas aprobadas. Evidencia en `reports/contenido-cobertura.md`, `reports/primer-cruce.md` y `reports/portal-carga.json`.
- Los cinco pasos de esta iteración están ejecutados hasta el límite de las fuentes disponibles. Pendiente externo: URL de Ganadería Sonora 2013 y Datos hídricos 1960–1969. La cobertura total de contenidos de dominio y el linaje de tableros continúan como trabajo incremental; el primer cruce no los resuelve.

## Mapa global de oportunidades implementado

- Evaluados los 3,916 pares no ordenados entre los 89 conjuntos, sin autopares ni duplicados.
- Resultado: 1,191 candidatos por validar, 396 pares con dimensiones amplias/tiempo insuficientes, 2,328 sin clave reconocida por las reglas y 1 par con el cruce exploratorio de 2022 ya ejecutado.
- Reconocidas 1,509 columnas candidatas a claves o estratos. Catorce conjuntos no tienen dimensiones reconocidas por estas reglas y quedan para revisión de dominio.
- Cada par conserva familias, columnas, definiciones, sentidos, representaciones, campos de igual nombre y pendientes. No se infieren equivalencias globales ni se ejecutan joins de personas.
- Evidencia completa en `data/portal/oportunidades-cruce.json`, grafo en `data/portal/oportunidades.ttl`, informe en `reports/oportunidades-cruce.md` y buscador en `scripts/consultar_cruces.py`.
- El pipeline incorpora los perfiles y evaluaciones con comprobación de huellas y SHACL. Se añadieron consultas y pruebas; 33 pruebas aprobadas.
- Mapa sincronizado en Studio con respaldo: 140,898 triples, 14,140 individuos, 21 clases; validación SHACL conforme sin infracciones. Hay 98 candidatos priorizados para revisión, sin aprobación automática.
- Siguiente etapa: revisar y ejecutar progresivamente oportunidades sustentadas en claves, periodos, grano, unidades y cardinalidad. Detectar una oportunidad no equivale a validar o ejecutar un cruce.

## Primer lote de candidatos procesado

- Los 98 pares priorizados tienen una decisión y evidencia: 2 con ejecución parcial exploratoria, 53 requieren transformación/catálogo, 41 requieren revisión y 2 fallaron condiciones integrales.
- Recuperadas 51 muestras representativas y evaluados integralmente 24 recursos concretos; 16 superaron sus estrategias. Un diagnóstico de muestra no valida el conjunto completo.
- Ocho recursos de Nacimientos no superaron consistencia de totales o cobertura mensual; sin completar vacíos, alterar fuentes ni forzar agregados anuales.
- Comparados Titulados/Egresados UES y Nuevo ingreso/Reingreso UES por programa/sede y periodos declarados coincidentes; 340 claves resultantes, 113 con valores numéricos en ambas fuentes. No son tasas ni cohortes.
- Referencia de 72 municipios extraída y comprobada internamente desde GeoJSON del portal; no se homologan automáticamente los códigos locales de otras fuentes.
- Scripts, evidencia, resultados y límites en `scripts/validar_lote_cruces.py`, `data/portal/lote-cruces/`, `reports/validacion-lote-cruces.md`, `reports/resultados-lote-educacion.md` y `docs/validacion-por-lotes.md`. Se aprobaron 43 pruebas.
- Lote cargado y sincronizado con respaldo: Studio contiene 144,653 triples, 14,652 individuos y 26 clases. SHACL conforme sin infracciones; la regla de resultados municipales del lote no tuvo casos porque esos cruces no superaron los controles.
- Continuar incorporando estrategias explícitas por dominio, catálogos sustentados y revisión de periodos/grano/unidades. No se afirma que todos los cruces posibles estén validados o ejecutados.

## Fuentes de referencia

- Portal: https://datos.sonora.gob.mx/
- Open Ontologies: https://github.com/fabio-rovai/open-ontologies
- DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- API de CKAN: https://docs.ckan.org/en/2.11/api/index.html

## Antecedente: integración central de las cinco entregas

- Incorporadas las cinco entregas revisadas, con respaldo previo y copias de evidencia fijadas por SHA-256.
- 103 conceptos, 232 variables respaldadas y 162 correspondencias revisadas (62 anteriores preservadas + 100 nuevas).
- 16 referencias de catálogo identificadas; des_mpo_res sigue sin resolver y conserva las dos filas de diccionario.
- 1850 localidades observadas en IML_2020, sin equivalencia oficial ni asignación a otros conjuntos.
- 28 comprobaciones territoriales: 16 compatibles, 11 con excepciones y una ausencia de columna. No implican vigencia histórica ni nuevos cruces.
- Pendientes: 23 significados candidatos, 792 correspondencias candidatas, 3 columnas ambiguas/6 vínculos, 5 inconsistencias documentales, versiones históricas y cotejo INEGI.
- Reproducción y límites: reports/integracion-agentes.md; validación y sincronización: reports/portal-carga.json y reports/studio-portal-sync.json.

## Integración de ronda 2

- Preservadas las 162 revisiones anteriores; incorporadas 674 adicionales: 836 revisadas, 118 candidatas y 6 vínculos ambiguos sobre 3 columnas.
- Se mantienen 103 conceptos, 232 significados respaldados y 23 candidatos.
- 32 dictámenes y 14 preguntas sin enviar; 16 vigencias no acreditadas.
- 1850 coincidencias de clave, nombre y población entre IML 2020 e ITER 2020; sin identidad oficial ni asignación a otras fuentes.
- Evaluación histórica parcial del pipeline fuente: 20 intentos, 4 respuestas, 2 aciertos, 2 fallos de recuperación, 16 errores HTTP/cuota; UI no evaluada.
- Evidencia: data/integracion-ronda-2; informe: reports/integracion-ronda-2.md. Validación y sincronización: reports/portal-carga.json y reports/studio-portal-sync.json.

## Ronda 3 coordinada entre chats

- «Revisar errores de la antología» integró la semántica: 1,212 definiciones respaldadas, 940 conceptos, 328 fuera del núcleo y 23 candidatas. Su evidencia fijada se conserva en data/integracion-cobertura.
- Después del relevo, este chat añadió 29 correspondencias: 865 revisadas, 3,283 candidatas y 12 vínculos ambiguos. Las 836 revisiones anteriores y el resto del núcleo semántico se conservaron exactamente.
- Incorporadas tres fichas de cruces; la nueva comprobación de 2020 conserva 72 comparaciones y 144 evidencias separadas por fuente, sin afirmar identidad de medida ni vigencia.
- Corrección de recuperación del chat instalada con respaldo; seis casos de recuperación por API pasan contra el grafo final. No se certifica una respuesta del modelo desde la interfaz.
- Grafo final en Studio: 284,810 triples, sincronización verificada y SHACL conforme. 108 pruebas centrales aprobadas.
- Procedimiento, comprobantes y límites: docs/orquestacion-ronda-3.md, reports/integracion-ronda-3.md y docs/correspondencias-y-cruces-ronda-3.md.
