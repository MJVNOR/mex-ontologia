# Diagnóstico del catálogo de Sonora

Consulta UTC: 2026-10-23T04:57:19.215143+00:00

Fuente: https://datos.sonora.gob.mx/api/3/action/package_search

Metadatos de conjuntos públicos devueltos por package_search; sin descargar recursos.

- Conjuntos: 89
- Recursos referenciados: 486
- Organizaciones con conjuntos: 25

Los conteos describen esta consulta; no prueban la disponibilidad de las descargas ni la calidad del contenido.

## Formatos declarados

| Formato | Recursos |
| --- | ---: |
| XLSX | 333 |
| CSV | 148 |
| XLS | 4 |
| JSON | 1 |

## Hallazgos para el modelo

- 40 conjuntos sin grupo temático.
- 2 recursos sin URL.
- 97 recursos con región declarada como guion; no tratarlo como un lugar.
- 108 recursos declaran inicio y fin iguales a 1989-06-04. Es un patrón que requiere revisión; no se ha confirmado si es un valor por defecto o una cobertura real.
- datastore_active indica una posible vía para consultar filas; todavía no se verificaron esas consultas.
- Se cuentan organizaciones presentes en conjuntos, no todas las organizaciones registradas en el portal.

## Campos de los conjuntos

| Campo | Presente | Con valor | Sin valor o ausente |
| --- | ---: | ---: | ---: |
| `author` | 89 | 0 | 89 |
| `author_email` | 89 | 0 | 89 |
| `creator_user_id` | 89 | 89 | 0 |
| `data_source` | 89 | 89 | 0 |
| `frequency` | 89 | 89 | 0 |
| `fuentes_extras` | 89 | 17 | 72 |
| `granularidad_datos` | 89 | 89 | 0 |
| `groups` | 89 | 49 | 40 |
| `id` | 89 | 89 | 0 |
| `isopen` | 89 | 89 | 0 |
| `jurisdiccion` | 89 | 89 | 0 |
| `license_id` | 89 | 89 | 0 |
| `license_title` | 89 | 89 | 0 |
| `license_url` | 89 | 89 | 0 |
| `maintainer` | 89 | 0 | 89 |
| `maintainer_email` | 89 | 0 | 89 |
| `metadata_created` | 89 | 89 | 0 |
| `metadata_modified` | 89 | 89 | 0 |
| `name` | 89 | 89 | 0 |
| `notes` | 89 | 89 | 0 |
| `num_resources` | 89 | 89 | 0 |
| `num_tags` | 89 | 89 | 0 |
| `numero_variables` | 89 | 89 | 0 |
| `organization` | 89 | 89 | 0 |
| `owner_org` | 89 | 89 | 0 |
| `private` | 89 | 89 | 0 |
| `relationships_as_object` | 89 | 0 | 89 |
| `relationships_as_subject` | 89 | 0 | 89 |
| `resources` | 89 | 89 | 0 |
| `state` | 89 | 89 | 0 |
| `tags` | 89 | 60 | 29 |
| `title` | 89 | 89 | 0 |
| `type` | 89 | 89 | 0 |
| `url` | 89 | 0 | 89 |
| `version` | 89 | 0 | 89 |

## Campos de los recursos

| Campo | Presente | Con valor | Sin valor o ausente |
| --- | ---: | ---: | ---: |
| `cache_last_updated` | 486 | 0 | 486 |
| `cache_url` | 486 | 0 | 486 |
| `created` | 486 | 486 | 0 |
| `datastore_active` | 486 | 486 | 0 |
| `description` | 486 | 0 | 486 |
| `email_publisher` | 440 | 440 | 46 |
| `end_date` | 486 | 486 | 0 |
| `format` | 486 | 486 | 0 |
| `hash` | 486 | 0 | 486 |
| `id` | 486 | 486 | 0 |
| `last_modified` | 486 | 486 | 0 |
| `metadata_modified` | 486 | 486 | 0 |
| `mimetype` | 486 | 484 | 2 |
| `mimetype_inner` | 486 | 0 | 486 |
| `name` | 486 | 486 | 0 |
| `package_id` | 486 | 486 | 0 |
| `position` | 486 | 486 | 0 |
| `publisher` | 440 | 439 | 47 |
| `publisher_area` | 440 | 437 | 49 |
| `publisher_puesto` | 440 | 440 | 46 |
| `publisher_telefono` | 66 | 66 | 420 |
| `region` | 486 | 486 | 0 |
| `resource_type` | 486 | 0 | 486 |
| `responsible` | 486 | 486 | 0 |
| `responsible_puesto` | 486 | 486 | 0 |
| `size` | 486 | 486 | 0 |
| `start_date` | 486 | 486 | 0 |
| `state` | 486 | 486 | 0 |
| `url` | 486 | 484 | 2 |
| `url_type` | 486 | 484 | 2 |

## Alcance de los indicadores

‘Con valor’ excluye null, cadenas vacías, listas vacías y objetos vacíos. No verifica significado, vigencia ni validez de URLs.

Las fechas metadata_created y metadata_modified describen el registro del catálogo; no deben asumirse como fechas de los datos.

Los valores de campos especiales y el inventario de conjuntos están en catalogo-perfil.json.
