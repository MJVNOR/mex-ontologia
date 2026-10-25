# Catálogos territoriales y correspondencias

Esta revisión identifica referencias publicadas y contrasta sus entradas con la instantánea del GeoJSON del portal. No valida todas las filas de los conjuntos ni habilita cruces sin comprobar periodo, papel territorial y grano.

| Indicador | Resultado |
| --- | ---: |
| archivos_leidos | 15 |
| hojas_por_recurso | 23 |
| referencias_distintas_por_archivo_hoja | 9 |
| entradas_distintas | 570 |
| referencias_declaradas_con_recurso_identificado | 8 |
| catalogos_localidad_en_los_archivos_examinados | 0 |

Los archivos con el mismo SHA-256 y la misma hoja comparten una referencia y sus entradas. Se conservan las URL de todas las publicaciones; no se confunden sus conjuntos ni publicadores.

## Referencias declaradas con recurso identificado

| Conjunto | Variable | Hoja | Fuente |
| --- | --- | --- | --- |
| Proyecciones de población - Grupos quinquenales de edad | CLAVE | Catalogo_Municipios | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/0b5f5e16-2de3-4be1-811f-4b0976ed82d3/resource/de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0/download/catalogo.xlsx) |
| Proyecciones de población - Grupos quinquenales de edad | CLAVE_ENT | Catalogo_Estado | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/0b5f5e16-2de3-4be1-811f-4b0976ed82d3/resource/de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0/download/catalogo.xlsx) |
| Proyecciones de población - Grandes grupos de edad | CLAVE | Catalogo_Municipios | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/943d0723-afbb-470a-8fe8-d62e8671de84/resource/d7c4b8b2-568f-4349-a1ed-23fa93189e83/download/catalogo.xlsx) |
| Proyecciones de población - Grandes grupos de edad | CLAVE_ENT | Catalogo_Estado | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/943d0723-afbb-470a-8fe8-d62e8671de84/resource/d7c4b8b2-568f-4349-a1ed-23fa93189e83/download/catalogo.xlsx) |
| Incidencia delictiva municipal | Cve. Municipio | cat_municipio | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/93ca5e1c-702e-4e62-bc61-638907be184a/resource/36d3ac85-4327-41f5-9259-538a7723a0ae/download/catalogo.xlsx) |
| Víctimas del fuero común en el estado | Clave_Ent | cat_entidad | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/caf587a5-23ac-496b-85d4-6ceb1d615d78/resource/7f3aca28-4251-48b8-a759-69c992580744/download/catalogo.xlsx) |
| Proyecciones de población - Indicadores demográficos | CLAVE | Catalogo_Municipios | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/960ef0a9-73ed-4191-ae0b-b868d7e48292/resource/e0d2acc2-9841-4f6d-baea-88ba86710a7d/download/catalogo.xlsx) |
| Proyecciones de población - Indicadores demográficos | CLAVE_ENT | Catalogo_Estado | [Catálogo publicado](https://datos.sonora.gob.mx/dataset/960ef0a9-73ed-4191-ae0b-b868d7e48292/resource/e0d2acc2-9841-4f6d-baea-88ba86710a7d/download/catalogo.xlsx) |

Identificar el recurso no demuestra que todos los códigos de sus archivos de datos pertenezcan al catálogo, ni confirma la versión aplicable a cada año. Esta capa territorial identifica ocho referencias. El resultado combinado con las entregas revisadas se registra en reports/integracion-agentes.md y data/semantica/cobertura.json.

## Contraste municipal entre referencias

| Estado | Entradas comparadas |
| --- | ---: |
| codigo_y_nombre_con_reparacion_codificacion | 154 |
| codigo_y_nombre_normalizado | 203 |
| codigo_y_nombre_exacto | 146 |
| categoria_no_municipal | 2 |
| codigo_y_alias_revisado | 1 |

Estas cantidades cuentan pares de entradas por referencia distinta, no municipios únicos. Los estados de coincidencia de código/nombre o alias explícitamente revisado reciben un destino; las coincidencias siguen siendo afirmaciones calificadas, sin `owl:sameAs` ni `skos:exactMatch`.

Los códigos locales se conservan tal como aparecen. Cuando se contrasta `MUNI`, la transformación `26 + municipio a tres dígitos` se registra en cada correspondencia; no se aplica a otros campos ni al Registro Civil.

## Textos y casos pendientes

Los nombres del GeoJSON se conservan con su codificación original. Para comparar, se registra una reparación reversible de UTF-8 interpretado como Latin-1 o Windows-1252, seguida de comparación sin diferencias de mayúsculas, tildes y espacios. Se mantienen ambas representaciones; no se sobrescribe la fuente.

- Alias revisado por el usuario el 2026-10-23: Magdalena de Kino / Magdalena, códigos 36 / 26036. Se conservan los textos originales; la revisión se limita a estas entradas de Sonora.
- `26998` — No Especificado: `categoria_no_municipal`. Nombre del destino consultado: sin entrada. No se creó enlace a un municipio destino.
- `26999` — Otros Municipios: `categoria_no_municipal`. Nombre del destino consultado: sin entrada. No se creó enlace a un municipio destino.

## Localidades y alcance

No se encontró una hoja de catálogo de localidades entre los archivos territoriales examinados. Los catálogos municipales de conjuntos llamados «marginación por localidad» siguen siendo catálogos de municipios; el título del conjunto no los convierte en referencias de localidad. No se asignan claves de localidad sin entidad, municipio y una referencia documental adecuada.

Los códigos y nombres de las hojas de catálogos sí se enlazan con la referencia que definen mediante `mex:defineReferenciaTerritorial`. Las columnas de los archivos de datos conservan sus estados semánticos anteriores; esta revisión no acredita automáticamente su pertenencia al catálogo.

## Evidencia y reproducción

- `data/territorio/catalogos.json`: extracción completa de las hojas y selección de Sonora en las tablas municipales nacionales, con códigos originales, celdas, tipos y SHA-256.
- `data/territorio/verificacion.json`: estados de cada correspondencia y recursos identificados.
- `ontologia/territorio.json`: las ocho resoluciones documentales revisadas, fijadas a las huellas de archivo y de fila de diccionario.
- `data/territorio/territorio.ttl`: capa RDF generada, integrada con el núcleo semántico.

La generación normal no consulta la red. Para actualizar los catálogos, ejecutar `uv run python scripts/extraer_catalogos_territoriales.py --refresh`, revisar los cambios y actualizar las resoluciones solo si su evidencia sigue siendo válida. Luego ejecutar `scripts/ampliar_portal.py --load` y `scripts/sincronizar_studio_portal.py`.
