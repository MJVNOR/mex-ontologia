# Núcleo semántico de MEX-Ontologi

El objetivo actual es describir qué significa la información del portal y bajo qué condiciones puede conectarse. El inventario, las evaluaciones de pares y los cruces anteriores permanecen como evidencia y pruebas del modelo. La generación de esta capa reutiliza evidencia local. La actualización territorial consulta solo los catálogos seleccionados, sin ejecutar nuevos análisis sobre filas de personas.

## Cobertura vigente R9

1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas. R8 revisó las 28 correspondencias SINAC; R9 conserva ese núcleo y añade dos declaraciones de unidad sobre definiciones concretas y la exclusión SHACL documentado/candidato. Una declaración de unidad no se atribuye globalmente a otros archivos o periodos. No se integraron intervalos ni jerarquías clínicas sin respaldo.

Quedan 138 significados reales sin respaldo y dos encabezados corruptos. Se conserva el requisito de significado respaldado para una correspondencia revisada. [Evidencia y límites R9](../reports/ronda-9.md). [Formato y lanzamientos](versionado-y-lanzamientos.md).

## Separar las entidades

| Entidad | Qué representa | Ejemplo |
| --- | --- | --- |
| Conjunto y recurso | Publicación y archivo/API del catálogo | Matrimonios y su recurso de 2022 |
| Columna observada | Campo físico dentro de un esquema concreto | `año_matrimonio` de ese recurso |
| Definición original | Fila del diccionario publicado | «Año de registro» |
| Variable documentada | Variable local descrita por esa definición y ese conjunto | Variable `año_matrimonio` del diccionario de Matrimonios |
| Concepto compartido | Aspecto de significado que puede aparecer en distintas fuentes | Año de registro |
| Correspondencia semántica | Afirmación cualificada sobre una columna y una variable, con estado y evidencia | Enlace documental revisado, candidato o ambiguo |
| Sistema y entrada de códigos | Convención de identificación y sus símbolos dentro de una fuente | CVEGEO y código `26001` del GeoJSON |
| Municipio según fuente | Unidad municipal identificada dentro de esa referencia | Municipio que denota una entrada del GeoJSON |

Un concepto compartido no es una columna, un municipio concreto ni una prueba de igualdad entre valores. Las variables permanecen locales al diccionario y conjunto que las define. Los códigos de una fuente no se asignan a entidades de otra por apariencia o coincidencia numérica.

## Significados distintos que ahora se conservan

- Año de registro y año de fallecimiento.
- Municipio de registro, residencia, ocurrencia de la defunción, parto, nacimiento de la madre, ubicación y origen de una llamada.
- Organización publicadora y capturadora.
- Nombre y código como representaciones diferentes de un programa o referencia municipal.
- Periodo escolar y referencia anual: necesitan conservar calendario, institución, evento y cobertura.

Por ejemplo, `año_matrimonio` significa **año de registro** según su diccionario, aunque el nombre sugiera el evento. `año_defuncion` se define como año de fallecimiento. No se homologan. Un campo de nacimiento de la madre tampoco se interpreta como lugar del parto ni lugar de nacimiento del recién nacido.

Los papeles de población y objetos concretos se conservan en las descripciones originales: madre, difunto, planta, presa, etc. Compartir un aspecto más amplio como «Municipio de residencia» no elimina ese contexto. La referencia de organización publicadora ya se expresa con `dct:publisher` en el catálogo; una variable de dependencia capturadora no se equipara a ese publicador.

## Evidencia y estados

Se examinaron las 1,563 definiciones con nombre ya recuperadas. Tras la ampliación de cobertura con Muse 1.3, el núcleo contiene 940 conceptos y seis condiciones de conexión. **1,212 variables** tienen una interpretación respaldada documentalmente; **23** conservan un significado candidato y **328** permanecen fuera del núcleo. Las búsquedas oficiales con Obscura se fijan como evidencia contextual; no confirmaron catálogos para las variables locales examinadas. [Resultado de la ampliación](../reports/cobertura-muse.md).

Se materializaron 1,238 variables documentadas: las respaldadas, las candidatas y otras con una referencia a catálogo u observación que conviene conservar. Materializar una variable no confirma su interpretación. Las referencias a «N/A», «No aplica» y vacías no se inventan como catálogos.

| Estado | Qué permite afirmar |
| --- | --- |
| `respaldada_por_definicion` | La definición publicada respalda ese aspecto del significado de la variable local |
| `candidata_sin_definicion_suficiente` | El nombre sugiere un concepto, sin confirmación documental suficiente |
| `candidata_por_nombre` | Una columna y una variable coinciden nominalmente dentro del mismo conjunto; falta revisar la correspondencia |
| `ambigua_por_nombre` | Hay varias definiciones o encabezados repetidos; no se elige una interpretación silenciosamente |
| `documental_revisada` | Se revisó explícitamente esa columna y su definición concreta, con regla y procedencia |

Las correspondencias candidatas están materializadas como afirmaciones cualificadas, sin agregar significado confirmado directamente a la columna. Hay 3,312 candidatas, 12 ambiguas y 836 revisadas: **4,160 correspondencias** sobre **4,154 columnas**. El crecimiento de candidatas refleja las variables recién interpretadas; no una revisión automática de sus vínculos físicos.

Las 62 revisiones iniciales, conservadas íntegramente, corresponden a nueve recursos: Matrimonios, Nacimientos, Defunciones y Divorcios de 2022; marginación municipal de 2020; precipitaciones de 2025; Consulta Externa, Atención de Urgencias y Egresos Hospitalarios. La ronda 1 añade 100 revisiones concretas y la ronda 2 añade otras 674. La lista exacta por columna está en las reglas y la auditoría; no se revisaron todos los años ni todos los campos de esos conjuntos. La revisión comprueba estructura y significado declarado; no confirma todos los valores ni resuelve los problemas de calidad detectados en Nacimientos. La revisión documental fue realizada por el asistente y está expresada en reglas; no se presenta como una aprobación del usuario o de las dependencias.

Las reglas están en `ontologia/semantica.json`, con descripciones exactas, límites de contexto y vínculos explícitos. Las 836 revisiones fijan la IRI física, la huella SHA-256 del esquema y de la fila del diccionario, y su descripción literal. Si cambia esa evidencia, la generación se detiene para revisar de nuevo. El alias `Precipitacion (mm)` → `Precipitacion_mm` se acepta únicamente en la columna revisada de Lluvias 2025; no se normalizan nombres globalmente. Se normalizan acentos y mayúsculas para comparar esas descripciones aceptadas; no se usa esa normalización para homologar códigos o entidades. Cambiar una definición o volver ambiguo un vínculo revisado detiene la generación. Las variables apuntan a la fila original, sin reemplazar sus textos.

Un campo CLUES con descripción «Pendiente de especificar» queda candidato. Incluso «Clave de la Unidad» solo se interpreta como unidad de salud en los tres conjuntos de salud revisados, y tampoco acredita pertenencia a un catálogo CLUES concreto.

## Observaciones documentales

Se conservan cinco observaciones pendientes en el grafo mediante `mex:limiteSemantico`: `Total_Egresos` descrito como urgencias; formato municipal `nnn` frente al ejemplo `26048`; fecha `DD/MM/AAAA` frente al ejemplo `45658`; el campo `a–o` de Nacimientos 2024; y `anio_registro` de Divorcios 2023. No se corrigen los textos originales. El alias de Divorcios 2023 está revisado únicamente para su columna física y su diccionario; a–o de Nacimientos 2024 sigue sin confirmar.

Un año o mes genérico documenta solo esa referencia temporal, sin inventar evento. Los conceptos distinguen registro, captura, fallecimiento, inspección, residencia, escuela y atención. No equivalen a claves listas para unir. Los calificadores documentales de distrito, sede, instrumento o contexto se conservan en el reporte y mediante `mex:tieneCalificadorDocumentado`, `mex:dimensionCalificador` y `mex:valorCalificador`; sus límites se conservan en `mex:limiteSemantico`.

## Sistemas de identificadores

Se conserva un sistema observado: CVEGEO municipal del GeoJSON del portal, con 72 entradas y componentes entidad/municipio comprobados en esa referencia. Se asocia **solo a la columna CVEGEO de ese recurso**. No se declara que los códigos numéricos locales del Registro Civil, salud o seguridad utilicen ese sistema.

De las 17 referencias a catálogos declaradas inicialmente, 16 tienen ya un recurso identificado mediante revisión del diccionario y la hoja del catálogo en el mismo conjunto (`recurso_catalogo_identificado`); una conserva `solo_referencia_declarada_sin_resolver`. Identificar ese recurso no prueba vigencia histórica ni pertenencia de las filas de datos. Nombres como «Municipios» o `catalogo_municipios` se conservan por conjunto, con su definición de origen. No se fusionan por nombre. Los catálogos territoriales recuperados añaden correspondencias calificadas entre entradas y el GeoJSON, sin convertirlas en identidad oficial ni habilitar otros códigos automáticamente. Las entradas mantienen los códigos como cadenas, incluidos ceros a la izquierda.

Los municipios representados están identificados dentro de la referencia de origen. No se añaden identidades oficiales externas ni `owl:sameAs`. Tampoco se crean `skos:exactMatch` entre columnas, variables o catálogos.

## Catálogos territoriales recuperados

La revisión incorpora 23 hojas de 15 archivos, reducidas a nueve referencias distintas por igualdad exacta del archivo y la hoja. Las 570 entradas preservan códigos, nombres originales, coordenadas de celda y fuentes. Las columnas del propio catálogo enlazan a la referencia que definen; las columnas de datos conservan sus revisiones previas.

Las 504 correspondencias con el GeoJSON conservan su estado de comparación: 146 por código/nombre exacto, 203 con normalización de nombre y 154 con reparación reversible de codificación y una con alias revisado por el usuario. Los textos originales no se sustituyen. `26998` y `26999` quedan como categorías no municipales; el alias Magdalena de Kino / Magdalena quedó revisado por el usuario, conservando ambos textos y su evidencia. No se identificó un catálogo de localidades entre las hojas examinadas.

Ver [catálogos territoriales y evidencia](../reports/catalogos-territoriales.md). La vigencia de estas instantáneas permanece `no_documentada`; ninguna correspondencia autoriza asumir que una clave del Registro Civil usa el mismo sistema.

## Condiciones para conectar información

Cada concepto del núcleo enlaza con las seis comprobaciones que debe considerar una conexión de datos:

1. Catálogo de identificadores o correspondencia explícita y su versión.
2. Papel semántico y población/objeto de referencia.
3. Evento temporal, calendario y cobertura declarada frente a observada.
4. Contexto de claves compuestas, como entidad para municipio y entidad/municipio para localidad.
5. Grano, unicidad, cardinalidad y agregación previa.
6. Unidades y regla de agregación de las medidas elegidas.

Son requisitos explícitos del modelo; su existencia no significa que ya estén satisfechos por cada par de conjuntos. Los enlaces de visualizaciones siguen sin demostrar qué recursos las alimentan. Las unidades se conservan literalmente y no se homologan a partir de nombres parecidos.

## Archivos y consultas

- `ontologia/semantica.json`: conceptos, reglas documentales y revisión explícita de columnas.
- `data/semantica/nucleo.ttl`: vocabulario y glosario reutilizable.
- `data/semantica/interpretaciones.ttl`: variables, correspondencias y referencia de códigos.
- `data/semantica/cobertura.json`: cobertura de todas las definiciones examinadas y estados individuales.
- `reports/pendientes-semanticos.md` y `.json`: cobertura completa de las 5,523 columnas y lista de pendientes con evidencia.
- `reports/consolidacion-semantica.md`: lectura del resultado y evidencia textual de las 1,212 variables respaldadas.

```powershell
uv run python scripts/consolidar_semantica.py
uv run python scripts/ampliar_portal.py --load
uv run python scripts/sincronizar_studio_portal.py
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_significados.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_columnas_revisadas.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_correspondencias.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_catalogos.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_sistemas_observados.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_evidencia_revisada.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/semantica_observaciones.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/territorio_catalogos.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/territorio_correspondencias.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/territorio_pendientes.rq
```

El primer comando genera únicamente el módulo semántico sin red ni motor. Sus interpretaciones referencian columnas y definiciones del inventario anterior; para validarlas conjuntamente se carga el grafo completo con el segundo comando. Este regenera el módulo, registra huellas de sus entradas y valida SHACL. La sincronización conserva las otras ediciones y respalda Studio. No hace falta repetir los análisis ni actualizar sus fuentes para cambiar las reglas semánticas con la misma evidencia.

El límite global de 2,000 individuos del árbol se corrigió en la instalación local. El contexto general del chat sigue siendo parcial; las correspondencias de variables nombradas se consultan con paginación completa. Las consultas SPARQL anteriores recorren el grafo completo. Las clases «Concepto compartido», «Variable documentada», «Correspondencia semántica de columna» y «Sistema de identificadores observado» permiten reconocer esta capa en Studio.

## Verificación y siguiente alcance

85 pruebas verifican también diferencias de papeles temporales/territoriales, ausencia de promoción por nombre, CLUES pendiente, referencias sin resolver, definiciones contradictorias y conservación de códigos. SHACL comprueba tipos, estados, cardinalidades y procedencia. Esto valida la estructura del modelo, no la verdad externa de todas las fuentes.

Antecedente histórico de las rondas 1 y 2: la integración de las cinco entregas incorporó 20 conceptos y reglas, 24 significados y 100 correspondencias adicionales. Al terminar la ronda 2 había 103 conceptos, 232 variables respaldadas, 23 candidatas y 836 correspondencias revisadas. Hay 16 referencias a catálogos identificadas y una sin resolver. La referencia derivada IML_2020 conserva 1850 localidades observadas; las 28 comprobaciones territoriales conservan 16 resultados compatibles, 11 con excepciones y una ausencia de columna. Quedan por revisar las 23 interpretaciones candidatas, 118 correspondencias por nombre, 3 columnas ambiguas, la referencia des_mpo_res y las inconsistencias documentales. La vigencia histórica de los catálogos sigue sin acreditarse. La ronda 2 coteja las 1850 localidades IML con ITER Censo 2020 Sonora: claves, nombres y población coinciden. No es una equivalencia con el universo cartográfico ni acredita idéntico corte del estudio IML. Los conceptos particulares de otros dominios y el linaje de tableros siguen pendientes. No es necesario generar más análisis para continuar esa consolidación.

## Referencias

El glosario y sus relaciones de organización usan [SKOS, recomendación del W3C](https://www.w3.org/TR/skos-reference/). La procedencia se representa con [PROV-O](https://www.w3.org/TR/prov-o/). Las clases, propiedades y estados bajo el espacio `mex:` son decisiones locales del proyecto, no un vocabulario oficial de Sonora.

## Integración de entregas revisadas

La evidencia se conserva en `data/integracion/entregas/` y `data/integracion/fuentes/`, fijada por `ontologia/revision-agentes.json` y su manifiesto SHA-256. Las carpetas originales de agentes se mantienen como entregas históricas sin modificar. Las reglas nuevas requieren definición, diccionario, conjunto, nombre y descripción concretos; no alcanzan otras variables por semejanza.

Las clases «Catálogo publicado identificado», «Localidad observada en IML 2020» y «Comprobación de claves territoriales» permiten explorar las incorporaciones. Las comprobaciones de valores no cambian el estado semántico de las columnas ni asignan sistemas de identificadores. El contraste puntual externo de INEGI y las muestras de datos del agente 1 no se importan como validación de cobertura. Detalles y decisiones: `reports/integracion-agentes.md`.

Consultas nuevas: `queries/portal/integracion_catalogos.rq`, `integracion_localidades.rq` e `integracion_comprobaciones.rq`. La generación normal sigue siendo sin red.

## Ronda 2 integrada

674 correspondencias adicionales quedan revisadas; 118 permanecen candidatas y 3 columnas conservan 6 vínculos ambiguos. Las 162 revisiones previas se preservan exactamente. Las normalizaciones de acento agudo están fijadas por recurso; Año/ano sigue pendiente.

Se incorporan 32 dictámenes y 14 preguntas preparadas sin contactar al publicador. Las 16 revisiones de vigencia documentan falta de evidencia temporal; no significan invalidez. Las 1850 coincidencias con ITER registran clave, nombre, población, filas fuente y fecha censal 2020-03-15, sin asignar identidades a otros conjuntos.

El diagnóstico del chat es histórico y parcial: pipeline fuente, 4 respuestas (2 aciertos y 2 fallos de recuperación), 16 errores HTTP/cuota, UI sin evaluar e identidad con el bundle instalado no demostrada. Sus conteos 162/792 describen el grafo evaluado antes de integrar, frente al cierre de ronda 2 (836/118); la ampliación posterior está documentada arriba.

Evidencia y decisiones: `reports/integracion-ronda-2.md`, `data/integracion-ronda-2/` y `ontologia/revision-ronda-2.json`. Consultas: `queries/portal/ronda2_pendientes.rq`, `ronda2_localidades.rq`, `ronda2_vigencia.rq`, `ronda2_evaluacion.rq`. La generación normal sigue sin consultar red ni modelos.
