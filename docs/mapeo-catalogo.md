# Propuesta de correspondencias CKAN → DCAT 3

Estado: primera implementación generada y cargada. Las correspondencias ambiguas siguen pendientes y se preservan como declaraciones de origen.

Referencia normativa: https://www.w3.org/TR/vocab-dcat-3/

## Entidades e identificadores

- Portal: `dcat:Catalog`.
- Conjunto: `dcat:Dataset`, identificado a partir del UUID `id` de CKAN.
- Registro de metadatos: `dcat:CatalogRecord`, vinculado al conjunto mediante `foaf:primaryTopic`.
- Organización: `foaf:Organization`, identificada por `organization.id`.
- Recurso: `mex:RecursoCatalogado`, identificado por `resources[].id` y enlazado con `mex:recurso`. Revisar si es una representación descargable del conjunto, una partición temporal o un servicio antes de promoverlo a `dcat:Distribution` u otra clase DCAT.
- Grupo temático: `skos:Concept`, identificado por el ID del grupo. No fabricar temas para conjuntos sin grupo.

Base acordada: `https://example.org/mex-ontologi/`, configurable en `config.toml`. UUID de CKAN para `dataset/`, `resource/`, `record/`, `organization/` y `theme/`; propiedades locales bajo `vocab/`. Es independiente de títulos y nombres modificables; no representa un espacio oficial del Gobierno de Sonora.

## Correspondencias propuestas

| Campo CKAN | Destino | Criterio |
| --- | --- | --- |
| `id` | `dct:identifier` del conjunto | Conservar UUID original. |
| `title` | `dct:title` | Conservar texto original. |
| `notes` | `dct:description` | Conservar descripción y su formato original. |
| `organization` | `dct:publisher` → organización | Conservar nombre e identificador publicados. |
| `groups[]` | `dcat:theme` → concepto | Normalizar espacios de etiquetas sin cambiar identidad. |
| `tags[].name` | `dcat:keyword` | Etiquetas textuales; no equipararlas automáticamente con conceptos temáticos. |
| `resources[]` | `dcat:distribution` | Correspondencia provisional sujeta a revisión de la estructura de los recursos. |
| `resources[].name` | `dct:title` de la distribución | Conservar nombre original. |
| `resources[].url` | `dcat:accessURL`; `dcat:downloadURL` cuando corresponda | Verificar tipo de enlace; no asumir que toda URL es descarga directa. Omitir si está vacía y emitir hallazgo. |
| `resources[].format` | `dct:format` | Conservar formato declarado; normalizar etiquetas. |
| `resources[].mimetype` | `dcat:mediaType` | Validar y convertir al identificador del tipo de medio cuando corresponda. |
| `resources[].size` | `dcat:byteSize` | Confirmar unidad y valor numérico no negativo. |
| `license_url` | `dct:license` | Conservar la URI exacta; no asumir versión a partir de `cc-by`. Documentar alcance de la licencia antes de propagarla a recursos. |
| `metadata_created` | `dct:issued` del registro | Fecha del registro, no del contenido del conjunto. |
| `metadata_modified` | `dct:modified` del registro | No representa necesariamente una actualización de los datos. |
| `frequency` | `dct:accrualPeriodicity` del conjunto | Definir correspondencias explícitas con un vocabulario de frecuencias; preservar el valor original. |
| `resources[].start_date`, `end_date` | Candidatos a cobertura temporal | Confirmar semántica, validar fechas y resolver patrones sospechosos antes de afirmar cobertura. Si el periodo distingue particiones, revisar modelado como conjuntos relacionados o serie. |
| `resources[].region` | Candidato a `dct:spatial` del conjunto o partición correspondiente | Resolver lugares con identificadores y revisar alcance. No afirmar cobertura municipal a partir de texto ambiguo. |

## Campos que necesitan decisiones adicionales

### Decisiones de la primera implementación

La tabla anterior documenta destinos potenciales. Esta versión implementa los campos básicos de conjuntos, organización, temas, etiquetas, licencia URI y fechas del registro. En recursos implementa identificador, nombre y formato. La URL válida se conserva con `mex:urlDeclarada`, sin afirmar descarga directa. Las URLs ausentes o inválidas se reportan.

Fechas y región de recursos se conservan con `mex:inicioDeclarado`, `mex:finDeclarado` y `mex:regionDeclarada`. Frecuencia, jurisdicción, granularidad y categorías de origen usan propiedades locales declarativas. DataStore activo se conserva como booleano.

Las correspondencias de tamaño, tipo de medio, frecuencia normalizada, cobertura, fechas del contenido y distribuciones DCAT quedan pendientes. No se propagó automáticamente la licencia del conjunto a los recursos.

Las marcas de tiempo del registro conservan su zona original cuando existe; no se agrega una zona si CKAN no la proporciona. La hora de extracción sí se registra explícitamente en UTC. El reporte y la copia de metadatos permiten revisar las declaraciones originales.

- `jurisdiccion`: expresa nivel nacional, estatal o municipal; no identifica por sí sola un lugar. Conservar como metadato de origen hasta definir su semántica.
- `granularidad_datos`: mezcla valores temporales con categorías como ubicación y evento/transacción. No mapear todo a resolución temporal.
- `data_source`: contiene categorías de origen, no necesariamente URLs ni conjuntos identificables. No convertirlas automáticamente en `dct:source` hacia una fuente concreta.
- `fuentes_extras`: revisar estructura y significado antes de generar relaciones de procedencia.
- `datastore_active`: señal para explorar la API de filas de CKAN; no prueba que el recurso sea consultable sin comprobarlo.
- `last_modified` de recursos: confirmar qué evento representa antes de usarlo como fecha de actualización del contenido.

## Hallazgos de la primera exploración

Ver cifras reproducibles en `reports/catalogo-diagnostico.md` y valores en `reports/catalogo-perfil.json`.

Hay recursos con región `-` y un patrón repetido de inicio y fin `1989-06-04` que exige revisión. Preservar lo declarado como evidencia y separar las correspondencias pendientes de los hechos normalizados.

Los recursos pueden tener periodos distintos dentro de un mismo conjunto. No trasladar todas sus fechas al conjunto sin analizar si representan particiones, versiones o formatos alternativos.
