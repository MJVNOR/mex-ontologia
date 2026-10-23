# Cobertura del portal de datos abiertos de Sonora

Inventario generado en UTC: 2026-10-23T05:55:36.021084+00:00

## Alcance

Inventario de metadatos públicos CKAN y páginas enlazadas desde la portada. No es un inventario de todo el dominio del Gobierno de Sonora ni una copia de todas las filas de sus archivos.

## Cobertura por capa

| Capa | Inventariado | Estado |
| --- | ---: | --- |
| Conjuntos CKAN | 89 | Metadatos consultados por API |
| Recursos CKAN | 486 | Clasificados por metadatos |
| Organizaciones registradas | 31 | Listado simple y detalles de API |
| Grupos registrados | 8 | Listado de API |
| Páginas en sonora.gob.mx/datos/ | 40 | Enlaces únicos de la portada |
| DataStore declarado activo | 78 | Se intentó consulta de esquema sin filas |
| DataStore verificado | 78 | API respondió y devolvió esquema |

## Clasificación de recursos

Clasificación inicial por nombre y formato, no por inspección completa del contenido.

| Tipo | Recursos |
| --- | ---: |
| diccionario | 88 |
| datos_estructurados | 396 |
| candidato_geoespacial | 2 |

## Estado del mapeo del catálogo base

486 recursos coinciden por identificador con catalogo.ttl. Quedan 408 recursos sin esquema inspeccionado. Este inventario compara el archivo base y no evalúa ampliaciones posteriores; para el grafo ampliado consultar docs/modelo-portal.md y reports/portal-carga.json.

Organizaciones representadas en el grafo: 25 de 31. Grupos representados: 7 de 8. El grafo inicial solo incluía organizaciones y temas usados por los conjuntos.

## Columnas observadas por API

Frecuencia entre recursos de datos con esquema verificado; se excluyen diccionarios y campos internos que empiezan con guion bajo. Compartir un nombre de columna no demuestra equivalencia de significado, unidad o clave.

| Campo | Recursos de datos |
| --- | ---: |
| `municipio` | 36 |
| `mes` | 14 |
| `hombres` | 14 |
| `mujeres` | 14 |
| `total` | 14 |
| `año` | 13 |
| `fecha_registro` | 9 |
| `hora_defuncion` | 9 |
| `sexo` | 9 |
| `edad` | 9 |
| `año_defuncion` | 9 |
| `mes_defuncion` | 9 |
| `dia_defuncion` | 9 |
| `edad_cty1` | 6 |
| `edad_cty2` | 6 |
| `sexo_cty1` | 6 |
| `sexo_cty2` | 6 |
| `año_matrimonio` | 6 |
| `mes_matrimonio` | 6 |
| `fecha_matrimonio` | 6 |
| `año_registro` | 6 |
| `mes_registro` | 6 |
| `edad_div1` | 6 |
| `edad_div2` | 6 |
| `sexo_div1` | 6 |

## Páginas fuera del catálogo

Herramientas, historias y análisis del Datatón se inventarían como páginas; una coincidencia temática con un conjunto no demuestra que ese conjunto alimente el tablero.

| Página | Tipo inicial | Inspección | Destinos visualización |
| --- | --- | --- | ---: |
| [Agricultura](https://www.sonora.gob.mx/datos/agricultura) | herramienta | http_html | 2 |
| [Ganadería](https://www.sonora.gob.mx/datos/ganaderia) | herramienta | http_html | 2 |
| [Pesca](https://www.sonora.gob.mx/datos/pesca) | herramienta | http_html | 2 |
| [Capacidad hídrica](https://www.sonora.gob.mx/datos/capacidad-hidrica) | herramienta | http_html | 2 |
| [Cinegética](https://www.sonora.gob.mx/datos/caza) | herramienta | http_html | 2 |
| [Seguridad](https://www.sonora.gob.mx/datos/seguridad) | herramienta | http_html | 2 |
| [Nacimientos](https://www.sonora.gob.mx/datos/nacimientos) | herramienta | http_html | 2 |
| [Defunciones](https://www.sonora.gob.mx/datos/defunciones) | herramienta | http_html | 2 |
| [Matrimonios](https://www.sonora.gob.mx/datos/matrimonios) | herramienta | http_html | 2 |
| [Divorcios](https://www.sonora.gob.mx/datos/divorcios) | herramienta | http_html | 2 |
| [Energía](https://www.sonora.gob.mx/datos/energia) | herramienta | http_html | 2 |
| [Proyección poblacional](https://www.sonora.gob.mx/datos/proyecciones-poblacion) | herramienta | http_html | 2 |
| [Marginación](https://www.sonora.gob.mx/datos/marginacion) | herramienta | http_html | 2 |
| [Lluvias](https://www.sonora.gob.mx/datos/lluvias) | herramienta | http_html | 2 |
| [Subastas ganaderas](https://www.sonora.gob.mx/datos/subastas) | herramienta | http_html | 2 |
| [Rickettsia](https://www.sonora.gob.mx/datos/rickettsia) | herramienta | http_html | 2 |
| [Acceso a Internet](https://www.sonora.gob.mx/datos/accesointernet) | herramienta | http_html | 1 |
| [Brechas digitales](https://www.sonora.gob.mx/datos/brechas-digitales) | herramienta | http_html | 2 |
| [Telemedicina](https://www.sonora.gob.mx/datos/telemedicina) | herramienta | http_html | 2 |
| [Población](https://www.sonora.gob.mx/datos/poblacion) | historia | http_html | 2 |
| [Educación](https://www.sonora.gob.mx/datos/educacion) | historia | http_html | 2 |
| [Vivienda](https://www.sonora.gob.mx/datos/vivienda) | historia | http_html | 2 |
| [Diagnóstico Integral del Entorno Digital](https://www.sonora.gob.mx/datos/diagnostico-entorno-digital) | diagnostico | http_html | 1 |
| [Diagnóstico de Salud Digital](https://www.sonora.gob.mx/datos/diagnostico-salud-digital) | diagnostico | http_html | 2 |
| [Ganadería](https://www.sonora.gob.mx/datos/equipo1dataton) | analisis_dataton | http_html | 1 |
| [Matrimonios](https://www.sonora.gob.mx/datos/equipo2dataton) | analisis_dataton | http_html | 1 |
| [Presas](https://www.sonora.gob.mx/datos/equipo3dataton) | analisis_dataton | http_html | 1 |
| [Defunciones](https://www.sonora.gob.mx/datos/equipo4dataton) | analisis_dataton | http_html | 1 |
| [Divorcios](https://www.sonora.gob.mx/datos/equipo5dataton) | analisis_dataton | http_html | 1 |
| [Ganadería](https://www.sonora.gob.mx/datos/equipo6dataton) | analisis_dataton | http_html | 1 |
| [Proyección poblacional](https://www.sonora.gob.mx/datos/equipo7dataton) | analisis_dataton | http_html | 1 |
| [Ganadería](https://www.sonora.gob.mx/datos/equipo8dataton) | analisis_dataton | http_html | 1 |
| [Nacimientos](https://www.sonora.gob.mx/datos/equipo9dataton) | analisis_dataton | http_html | 1 |
| [Marginación](https://www.sonora.gob.mx/datos/equipo10dataton) | analisis_dataton | http_html | 1 |
| [Presas](https://www.sonora.gob.mx/datos/equipo11dataton) | analisis_dataton | http_html | 1 |
| [Matrimonios](https://www.sonora.gob.mx/datos/equipo12dataton) | analisis_dataton | http_html | 1 |
| [Defunciones](https://www.sonora.gob.mx/datos/equipo13dataton) | analisis_dataton | http_html | 1 |
| [Agricultura](https://www.sonora.gob.mx/datos/equipo14dataton) | analisis_dataton | http_html | 1 |
| [Proyección poblacional](https://www.sonora.gob.mx/datos/equipo15dataton) | analisis_dataton | http_html | 1 |
| [Nacimientos](https://www.sonora.gob.mx/datos/equipo16dataton) | analisis_dataton | http_html | 1 |

Los destinos declarados se extraen de iframes y configuraciones literales para escritorio/tableta/móvil. No se consultaron las APIs internas de las visualizaciones ni se verificaron todas las vistas dentro de cada tablero.

## Secciones del portal

| Sección | URL |
| --- | --- |
| @GobiernoSonora | https://datos.sonora.gob.mx/ |
| Todos los conjuntos de datos | https://datos.sonora.gob.mx/dataset |
| Todas las organizaciones | https://datos.sonora.gob.mx/organization |
| 8 Grupos | https://datos.sonora.gob.mx/group |
| Acerca de Portal de Datos Abiertos del Gobierno del Estado de Sonora | https://datos.sonora.gob.mx/about |

## Destinos de visualización por proveedor

| Dominio | URLs únicas declaradas |
| --- | ---: |
| app.powerbi.com | 61 |
| inteligenciadedatos.sonora.gob.mx | 1 |

## Pendientes y límites

- Identificar columnas y claves de recursos sin DataStore mediante diccionarios, muestras o acceso específico a los archivos.
- Confirmar clasificación geoespacial y distinguir archivos de datos de diccionarios.
- Identificar los datos que alimentan cada tablero; los iframes identifican destinos de visualización, no necesariamente APIs ni fuentes de datos.
- Resolver coberturas temporales y territoriales ambiguas antes de crear equivalencias entre fuentes.
- Páginas inaccesibles, enlaces no rastreados y datos generados dinámicamente permanecen pendientes; inventariar una URL no equivale a mapear su contenido.
- Los enlaces de navegación institucional, redes sociales, acceso de usuarios y trámites se registran como referencias, sin rastrear esas plataformas.
- Los informes nuevos no modifican la copia editable abierta en Studio ni incorporan automáticamente contenido al grafo.

## Evidencia reproducible

`data/portal/inventario.json` contiene URLs, procedencia, estados de acceso, recursos y esquemas recuperados. `data/portal/portada-enlaces.json` conserva la evidencia de la portada. Los metadatos CKAN completos usados se guardan de forma seleccionada, sin campos de contacto personal, en el inventario.
