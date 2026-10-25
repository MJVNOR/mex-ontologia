# mex-ontologia

Ontología del portal de datos abiertos de Sonora: publicaciones, estructuras, variables, significados y condiciones para conectar información. Plan: [PLAN.md](PLAN.md).

## Estado vigente: ronda 6 y pendientes depurados

R6 conserva 1,392 significados respaldados, 1,075 conceptos, 4,475 correspondencias revisadas, 20 candidatas y cero ambiguas. Presas quedó vinculado exclusivamente con su definición /4; ese vínculo no acredita vigencia histórica ni autoriza cruces. [Integración y validación R6](reports/ronda-6.md).

Tres agentes OpenCode con Muse 1.3 organizaron los pendientes: **169 significados reales y dos filas de encabezado corruptas**, conservadas con su procedencia. La matriz documental mantiene **16 vigencias de catálogos y una anomalía de referencia heredada, `des_mpo_res`**. Cada caso identifica evidencia faltante y criterios de aceptación. Esta depuración no agrega significados ni cambia el grafo. [Informe de pendientes depurados](reports/pendientes-depurados.md) · [Detalle completo JSON](reports/pendientes-depurados.json).

La investigación posterior examinó los 169 pendientes con seis agentes OpenCode en paralelo y revisión independiente. Incluye el examen por ID del manual SEED 2022, documentación SINAC, el archivo de matrículas 2022-2 y fuentes adicionales. No se aprobaron promociones: la identidad documental del extracto Sonora de CONAPO se acreditó, pero no resolvió el significado de `CLASIF`. [Resultados, evidencia y límites](reports/investigacion-post-r6.md). Las nuevas pruebas del chat quedan para después.

La revisión completa de las brechas documentó **20 pares columna–fila de diccionario** en un registro estructural separado. Sus significados continúan pendientes: no se cambió el requisito semántico de `documental_revisada`, y el núcleo conserva 4475 revisadas y 20 candidatas. Los 169 significados, las 16 vigencias y la anomalía `des_mpo_res` con los dos encabezados siguen sin evidencia suficiente para su resolución. [Informe de revisión](reports/cierre-brechas-post-r6.md) · [Alcance del registro estructural](docs/correspondencias-estructurales-post-r6.md).

Los agentes OpenCode tienen autorizado usar el MCP de Obscura para investigar dudas en la web. Su disponibilidad y uso real quedaron comprobados en esta ejecución. [Instrucciones de investigación](docs/investigacion-opencode-obscura.md).

## Antecedentes de consolidación semántica

El límite global de 2,000 individuos del árbol de Studio está corregido en la instalación local. La consulta recupera todos los individuos del grafo y mantiene el renderizado virtualizado. [Ver corrección y comprobaciones](docs/studio-limite-individuos.md).

El chat consulta las correspondencias semánticas de las variables nombradas con paginación completa y distingue los conteos totales de los ejemplos mostrados. [Corrección de recuperación y prueba reproducible](docs/studio-recuperacion-chat.md). La evaluación posterior del pipeline fuente fue parcial: 4 respuestas (2 aciertos y 2 fallos de recuperación) y 16 intentos sin respuesta por errores HTTP/cuota. La interfaz de Studio no se evaluó ni se demostró identidad entre el pipeline fuente y el backend instalado. [Alcance del diagnóstico](reports/integracion-ronda-2.md).

La ampliación de cobertura con Muse 1.3 incorpora 980 significados revisados: el núcleo contiene 940 conceptos y 1,212 variables respaldadas documentalmente, de 1,563 definiciones (77.5%). Quedan 23 interpretaciones candidatas y 328 definiciones fuera del núcleo. Se conservan sujetos, eventos, unidades declaradas y límites, sin completar documentación ausente. [Resultado y evidencia de la ampliación](reports/cobertura-muse.md).

Se separan columna física, definición original, variable local, concepto y sistema de códigos. Se preservan las 836 correspondencias columna/variable revisadas; las nuevas interpretaciones dejan 3,312 correspondencias candidatas y 12 vínculos ambiguos sobre 6 columnas. Las coincidencias nuevas no están revisadas ni habilitan cruces. Un sistema CVEGEO se asocia únicamente a su fuente; 16 referencias declaradas tienen un recurso de catálogo identificado y una sigue sin resolver: `des_mpo_res`.

La segunda ronda también incorpora 32 dictámenes y 14 preguntas al publicador preparadas sin enviar. Las 1,850 localidades IML coinciden con ITER 2020 en clave, nombre y población, sin acreditar completitud oficial ni equivalencia con el universo cartográfico. Las 16 revisiones de vigencia histórica siguen sin acreditarla. Se conservan las cinco observaciones documentales originales y no se ejecutaron nuevos cruces.

- [Explicación del núcleo y sus límites](docs/nucleo-semantico.md).
- [Antecedente y evidencia de la segunda ronda](reports/integracion-ronda-2.md).
- [Resultado y evidencia de las interpretaciones](reports/consolidacion-semantica.md).
- [Cobertura de las 5,523 columnas y pendientes documentados](reports/pendientes-semanticos.md).
- [Catálogos territoriales recuperados y correspondencias](reports/catalogos-territoriales.md).

```powershell
uv run python scripts/consolidar_semantica.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_significados.rq
```

Esta secuencia usa la evidencia existente y no ejecuta análisis nuevos. Los mapas de cruces y lotes siguientes se conservan como antecedentes y pruebas del modelo. El estado vigente y la validación están en `reports/portal-carga.json`; el respaldo y estado de Studio, en `reports/studio-portal-sync.json`. La sección «Verificar el proyecto» indica cómo ejecutar la suite actual; los conteos de pruebas de etapas anteriores son históricos.

## Mapa de oportunidades de cruce

El primer lote de 98 candidatos ya se procesó: 2 comparaciones educativas ejecutadas parcialmente, 53 pares requieren transformación o catálogo, 41 revisión adicional y 2 no superaron las comprobaciones integrales. Se recuperaron muestras de 51 recursos y se examinaron integralmente 24 recursos específicos; 16 superaron sus reglas. Ninguno de estos conteos aprueba automáticamente conjuntos completos.

- [Decisiones, fuentes y límites del lote](reports/validacion-lote-cruces.md).
- [Resultados educativos completos](reports/resultados-lote-educacion.md): 340 claves programa/sede; 113 tienen valores numéricos en ambas fuentes.

```powershell
uv run python scripts/validar_lote_cruces.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/lote_resumen.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/lote_educacion.rq
```

El lote reutiliza evidencia fechada. `--refresh` vuelve a consultar; `--retry-errors` reintenta fallos integrales. La referencia municipal de 72 códigos se recuperó del GeoJSON del portal; no establece equivalencias con códigos locales de otras fuentes. Las discrepancias de Nacimientos requieren revisar fuente/definición, sin corregir valores ni asumir meses ausentes como cero.

Ya se evaluaron los 3,916 pares entre los 89 conjuntos: 1,191 candidatos por validar, 396 que solo comparten dimensiones amplias/tiempo, 2,328 sin clave común reconocida por las reglas y 1 cruce exploratorio previamente ejecutado. El resultado no autoriza automáticamente joins entre filas.

[Ver mapa completo](reports/oportunidades-cruce.md). Las claves candidatas abarcan territorio, periodos, centros de trabajo, unidades de salud CLUES, programas educativos y categorías sectoriales. Los estratos como sexo o nivel educativo no se tratan como identificadores suficientes. Cada par registra evidencia y comprobaciones pendientes; los datos completos están en `data/portal/oportunidades-cruce.json`.

```powershell
uv run python scripts/consultar_cruces.py --buscar agricultura --estado candidata_por_validar
uv run python scripts/consultar_cruces.py --buscar titulados --limite 10
uv run python scripts/consultar_cruces.py --id ID_DEL_PAR
uv run python scripts/consultar_catalogo.py --portal queries/portal/oportunidades_resumen.rq
```

El identificador de cada par aparece en la primera consulta. Con `--id`, se muestran sus perfiles completos, columnas, definiciones y diferencias. La ausencia de una oportunidad detectada no demuestra que un cruce sea imposible. Después de actualizar las fuentes, regenerar el mapa antes de ampliar: se comprueban las huellas de los archivos para evitar un mapa desactualizado.

## Resultado actual

Se inspeccionaron los 486 recursos: 484 accesibles y 2 sin URL ni DataStore. Se leyeron los 88 diccionarios y se incorporaron 1,563 definiciones con nombre, 464 esquemas de archivo y 5,675 columnas de archivo, además de los esquemas DataStore anteriores. Los encabezados de archivo y las correspondencias por nombre se conservan como candidatos, sujetos a revisión de dominio.

El primer cruce agrega matrimonios y divorcios registrados en 2022 por código municipal local: 13,881 y 6,064 filas, respectivamente. Conserva 67 resúmenes; 62 códigos aparecen en ambas fuentes. No vincula personas ni asigna nombres oficiales a códigos sin catálogo de correspondencia.

- [Cobertura y recursos inaccesibles](reports/contenido-cobertura.md).
- [Primer cruce y límites de interpretación](reports/primer-cruce.md).
- [Modelo y actualización](docs/contenido-y-cruces.md).

Al terminar el lote anterior, el grafo generado tenía 144,044 triples y se aprobaron 43 pruebas. La consolidación semántica posterior amplía ese estado; sus conteos y validación vigentes están en `reports/portal-carga.json`. El estado de Studio y su respaldo se registran en `reports/studio-portal-sync.json`. No se requiere una base de datos externa.

## Actualizar estructuras, diccionarios y cruce

```powershell
uv sync
uv run python scripts/inspeccionar_contenido.py
uv run python scripts/cruzar_registro_civil.py
uv run python scripts/mapear_cruces.py
uv run python scripts/validar_lote_cruces.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/primer_cruce.rq
```

Ejecutar cada paso solo si el anterior terminó correctamente. El último paso de sincronización necesita Studio abierto. El inspector reutiliza evidencia fechada; `--retry-errors` reintenta solo fallos y `--refresh` vuelve a consultar todos los recursos del inventario. Los scripts posteriores se ejecutan de nuevo para publicar esa nueva evidencia en el grafo. Para incorporar conjuntos nuevos hay que actualizar también el catálogo y el inventario antes de esta secuencia.

## Requisitos

- `uv` y Python 3.12 (versión fijada en `.python-version`).
- Open Ontologies para cargar y consultar el grafo. No requiere una base de datos externa.

## Explorar el catálogo

Desde la carpeta del proyecto:

```powershell
uv sync
uv run python scripts/explorar_catalogo.py
```

El script de exploración usa únicamente la biblioteca estándar de Python. Consulta metadatos por páginas de 25 registros, verifica que no haya IDs repetidos y genera:

- `reports/catalogo-diagnostico.md`: conteos, presencia de campos y hallazgos.
- `reports/catalogo-perfil.json`: inventario, campos y valores declarados para revisión.

No descarga CSV, Excel ni otros archivos de los recursos. Las ejecuciones posteriores reemplazan los dos informes con una nueva consulta. La API no ofrece aquí una instantánea transaccional: los chequeos de cantidad e IDs no detectan todas las posibles modificaciones concurrentes.

Opciones:

```powershell
uv run python scripts/explorar_catalogo.py --page-size 50 --output reports
```

Propuesta de correspondencias: [docs/mapeo-catalogo.md](docs/mapeo-catalogo.md).

## Generar y cargar el catálogo RDF

El nombre es **mex-ontologi**. La base provisional `https://example.org/mex-ontologi/` se configura en `config.toml`; no requiere registrar un dominio. El pipeline usa RDFLib para construir RDF y Open Ontologies para almacenarlo y consultarlo.

```powershell
uv run python scripts/construir_catalogo.py --load
```

Consulta la API, genera el modelo y el grafo en `data/catalogo/`, valida su sintaxis, los carga en un nuevo almacén persistente, ejecuta SHACL y cuatro consultas. Conserva el resumen en `reports/catalogo-carga.json`, que señala el almacén utilizado.

Cada ejecución crea un almacén nuevo bajo `store/`. Así una nueva carga no acumula registros retirados ni borra almacenes anteriores. Los archivos RDF, metadatos seleccionados y el informe se reemplazan con la ejecución más reciente; conserva copias si necesitas archivar cada exportación. No ejecutar dos cargas simultáneamente. Las consultas locales reflejan la última carga, no una conexión en vivo al portal.

Sin `--load` solo se genera la exportación y el informe, sin almacén asociado.

```powershell
uv run python scripts/consultar_catalogo.py queries/dependencias.rq
uv run python scripts/consultar_catalogo.py queries/temas.rq
uv run python scripts/consultar_catalogo.py queries/formatos.rq
uv run python scripts/consultar_catalogo.py queries/recursos_sin_url.rq
```

El script sustituye `{{BASE_IRI}}` por la base de la última carga. Devuelve valores JSON legibles; `--raw` conserva los tipos e idiomas RDF del motor.

## Modelo y límites

- Catálogo, conjuntos, registros, organizaciones y temas reutilizan DCAT, Dublin Core, FOAF y SKOS.
- Cada conjunto y recurso tiene procedencia hacia su registro de la API y la actividad de extracción.
- Los recursos CKAN se representan inicialmente como `mex:RecursoCatalogado`, vinculados con `mex:recurso`. No se afirma todavía que todos sean distribuciones equivalentes del mismo conjunto: hay recursos con periodos diferentes que requieren revisión.
- Región, fechas del recurso, frecuencia y granularidad quedan como declaraciones originales; no se infiere cobertura territorial o temporal.
- SHACL comprueba la estructura del modelo. No exige URL a todos los recursos ni tema a todos los conjuntos: esos faltantes aparecen en el reporte de calidad y no impiden conservar los registros.
- La generación del catálogo base solo consulta metadatos: no descarga archivos de contenido ni comprueba sus enlaces. Las etapas posteriores de inspección y cruces sí recuperan archivos o consultan filas de recursos seleccionados; sus resultados y límites se documentan por separado.

## Inventariar la cobertura de todo el portal

```powershell
uv run python scripts/inventariar_portal.py
```

Consulta el catálogo, lista las organizaciones y grupos registrados, clasifica recursos por sus metadatos, inspecciona las páginas de datos enlazadas en la portada y verifica esquemas DataStore con `limit=0`. No descarga todos los CSV/Excel ni guarda filas de los recursos.

Genera `reports/cobertura-portal.md` y `data/portal/inventario.json`, con acceso, clasificación, procedencia, estado del esquema y coincidencia con los identificadores del grafo. La portada se conserva en `data/portal/portada-enlaces.json`; si una consulta posterior falla, usa esa evidencia e indica su fecha. Sin evidencia previa ni acceso a la portada, la ejecución falla en lugar de fabricar un inventario.

El alcance de navegación son las páginas `/datos/` enlazadas desde la portada. Los enlaces institucionales y sociales quedan como referencias sin rastrear. Los destinos de visualización se registran sin consultar sus APIs internas. Enlaces accesibles y esquemas recuperados no prueban que el contenido completo esté integrado.

El inventario describe evidencia de acceso y compara el catálogo base. La incorporación de páginas y columnas al grafo se realiza en el paso siguiente.

## Ampliar el grafo con páginas y estructuras

```powershell
uv run python scripts/ampliar_portal.py --load
uv run python scripts/consultar_catalogo.py --portal queries/portal/resumen.rq
```

Genera la ampliación desde el inventario existente, la une al catálogo en `data/portal/portal-completo.ttl` y la valida con SHACL. Las columnas mantienen identidad por recurso, sin asumir equivalencias por nombre.

La ampliación ya está guardada también en la copia de Studio. Para una actualización posterior, con Studio abierto:

```powershell
uv run python scripts/sincronizar_studio_portal.py
```

Esta operación respalda el estado vivo y conserva los triples ajenos a la ampliación. Detalles, consultas y límites: [docs/modelo-portal.md](docs/modelo-portal.md).

## Verificar el proyecto

Comprobación del motor HTTP/MCP usado por Studio:

```powershell
uv run python scripts/comprobar_studio.py
```

La prueba conserva el contrato del lector original del repositorio. Se encontró una incompatibilidad de formato y se corrigió en la copia local de Studio, que ya está instalada y conectada al catálogo. Uso, límites y ajustes: [docs/studio-instalacion.md](docs/studio-instalacion.md).

```powershell
uv run python -m unittest discover -s tests -v
```

Las pruebas cubren identidad estable ante cambios de título, aislamiento de fechas de metadatos, preservación de texto al serializar, base configurable y tratamiento conservador de datos ambiguos.

## Entregas de revisión integradas

La integración central añade significados documentados, correspondencias revisadas, catálogos identificados, localidades observadas y comprobaciones de claves. Evidencia, conteos y límites: [reports/integracion-agentes.md](reports/integracion-agentes.md). Las cinco carpetas originales de propuestas se conservan; la generación usa copias fijadas por SHA-256. La referencia de localidades es derivada de IML_2020 y no acredita un catálogo oficial completo.

## Segunda ronda de revisión

Procedimiento completo de revisión, respaldo, integración, regeneración y sincronización: [docs/integracion-de-agentes.md](docs/integracion-de-agentes.md).

La ronda 2 incorpora 674 correspondencias documentales (836 revisadas en total, 118 candidatas), 32 dictámenes de pendientes, 1850 coincidencias IML/ITER2020 y revisiones de vigencia. La evaluación del pipeline de consulta se conserva con su alcance parcial, sin certificar la interfaz de Studio. Evidencia, límites y reproducción: [reports/integracion-ronda-2.md](reports/integracion-ronda-2.md).

## Estado después de la ronda 3

La ampliación semántica revisada cuenta con 1,212 significados respaldados y 940 conceptos; su evidencia está en [reports/cobertura-muse.md](reports/cobertura-muse.md). La etapa posterior incorpora 29 correspondencias documentales, para un total de 865 revisadas, y tres fichas de cruces. El caso nuevo documenta 72 comparaciones de proyecciones en 2020 con 144 evidencias por fuente. Studio está sincronizado y validado con SHACL.

Resultados y pruebas: [reports/integracion-ronda-3.md](reports/integracion-ronda-3.md). Uso y límites: [docs/correspondencias-y-cruces-ronda-3.md](docs/correspondencias-y-cruces-ronda-3.md). La corrección del chat está instalada y su recuperación por API comprobada; la respuesta del modelo desde la interfaz sigue sin evaluar.
