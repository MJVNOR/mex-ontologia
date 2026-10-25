# Modelo ampliado: páginas, visualizaciones y estructuras

Actualización: ya se incorporaron estructuras de archivo, filas de diccionarios y un primer cruce agregado. El estado vigente está en [contenido-y-cruces.md](contenido-y-cruces.md) y [cobertura de contenido](../reports/contenido-cobertura.md). Los conteos de las secciones siguientes describen la primera ampliación, anterior a esa integración.

El catálogo base se conserva. La ampliación está en `data/portal/ampliacion.ttl` y el grafo combinado en `data/portal/portal-completo.ttl`. La primera ampliación se generó desde el inventario guardado, sin consultar filas; la integración posterior sí consulta diccionarios y campos de los dos recursos del cruce.

## Entidades incorporadas

| Entidad | Cantidad | Representación |
| --- | ---: | --- |
| Páginas | 45 | 40 páginas de herramientas/análisis y 5 secciones de navegación |
| Visualizaciones declaradas | 62 | Destinos únicos encontrados en iframes o configuración de la página |
| Esquemas observados | 78 | Uno por recurso consultado mediante DataStore |
| Columnas observadas | 910 | Cada columna pertenece a un recurso y esquema específicos |
| Servicios de consulta | 78 | Endpoints DataStore comprobados mediante consultas sin filas |
| Organizaciones | 31 en total | Se completaron las 6 ausentes del catálogo base |
| Temas | 8 en total | Se completó el grupo que no estaba usado por conjuntos |

Los 89 conjuntos y 486 recursos permanecen representados. Todos los recursos tienen clasificación inicial por metadatos y estado de inspección; 408 siguen pendientes de estructura.

## Relaciones

- Catálogo → `mex:paginaPortal` → página.
- Página → `mex:visualizacionDeclarada` → destino de visualización.
- Recurso → `mex:servicioConsulta` → `dcat:DataService` con su endpoint.
- Recurso → `mex:esquema` → esquema → `mex:columna` → columna.
- Columna → `dct:isPartOf` → esquema.

Páginas y visualizaciones conservan sus URLs originales con `foaf:page`. Las nuevas entidades tienen procedencia y actividad de generación. El manifiesto `reports/portal-carga.json` registra la huella SHA-256 del inventario utilizado.

## Identidad y límites semánticos

Las páginas y destinos usan identificadores derivados de la huella de su URL completa. Las columnas usan el UUID del recurso más el nombre original codificado; reordenar campos no cambia su identidad. La base de identificadores se toma de `config.toml`.

Dos columnas llamadas `municipio` son entidades distintas. No se afirma equivalencia, identidad territorial ni compatibilidad de sus valores. La consulta de ejemplo encuentra ese campo en 36 recursos de datos; eso no equivale a 36 municipios ni a 36 conjuntos distintos.

De las 910 columnas, 78 son campos internos de DataStore. Hay 388 columnas en esquemas de recursos de datos y 522 en esquemas de diccionarios. Estas últimas son las columnas del archivo diccionario (por ejemplo «Nombre variable» o «Descripción»), no las variables definidas en sus filas. Todavía no se interpretaron esas filas.

Un destino de visualización enlazado no demuestra qué conjunto lo alimenta. Por ello no se generaron relaciones `dcat:servesDataset` entre tableros y conjuntos ni equivalencias `owl:sameAs` entre columnas. Los tipos declarados por DataStore se conservan como texto; no se transformaron automáticamente en semántica de dominio o unidades.

## Consultar el grafo ampliado

```powershell
uv run python scripts/ampliar_portal.py --load
uv run python scripts/consultar_catalogo.py --portal queries/portal/resumen.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/paginas_visualizaciones.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/columnas_municipio.rq
uv run python scripts/consultar_catalogo.py --portal queries/portal/estructuras_pendientes.rq
```

Cada carga crea un almacén persistente nuevo; no sobrescribe los anteriores. La generación comprueba que el inventario y el catálogo contengan los mismos identificadores de recursos. Sin `--load` solo se exportan los archivos RDF.

## Studio

La ampliación ya fue sincronizada en el motor activo y guardada en `data/catalogo/studio-live.ttl`. Esa copia contiene **21,617 triples**, incluidos los datos y etiquetas que ya tenía Studio. El grafo combinado del pipeline contiene **21,008 triples**; la diferencia corresponde a la copia editable y sus etiquetas preexistentes.

Vuelve a abrir Studio para refrescar sus vistas. En el árbol 2D aparecen «Página del portal», «Visualización declarada», «Esquema observado», «Columna observada» y «Servicio de consulta de datos». Seleccionar una entidad permite inspeccionar sus enlaces y procedencia. La vista 3D sigue siendo una proyección de clases, no la red de todas las instancias.

Para sincronizar una futura generación, con Studio abierto y sin editar durante la operación:

```powershell
uv run python scripts/sincronizar_studio_portal.py
```

La sincronización respalda primero el estado vivo, calcula cambios únicamente sobre los triples que administra, valida el estado previsto con las reglas combinadas y comprueba el resultado antes de guardar. Conserva las demás ediciones. El primer respaldo está registrado en `reports/studio-portal-sync.json`; los archivos quedan en `data/backups/`. Si detecta cambios concurrentes, detiene la operación y conserva la evidencia para revisión.

Los endpoints de esta utilidad corresponden al puerto local 8137 de la instalación actual. Si Studio está cerrado, debe abrirse antes de sincronizar.

## Validación realizada

- Sintaxis RDF y consultas SPARQL verificadas en Open Ontologies.
- SHACL combinado conforme, sin infracciones, sobre el grafo generado y sobre el estado previsto de Studio.
- Control negativo: quitar el nombre a una columna produce una infracción real de SHACL.
- Pruebas de identidad de columnas, límites de inferencia y conservación de ediciones.
- Comprobación de conservación de los 8,851 triples previos de Studio y de que repetir la sincronización no genera cambios.

Las reglas completas están en `data/portal/shapes.ttl`. El panel nativo de Studio conserva su configuración anterior de formas del catálogo base; la validación de esta ampliación se ejecuta mediante los scripts indicados y queda registrada en los informes.

## Siguiente trabajo

La inspección de los 408 recursos restantes y la lectura de los diccionarios ya se ejecutaron. El primer módulo de contenido agrega matrimonios y divorcios de 2022. Para nuevos módulos faltan correspondencias de dominio verificadas, catálogos de códigos y, cuando aplique, unidades compatibles; los enlaces de tableros siguen sin demostrar linaje de datos.
