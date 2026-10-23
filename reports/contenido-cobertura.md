# Cobertura de estructuras y contenido

Fecha UTC: 2026-10-23T06:30:11.751235+00:00

| Indicador | Total |
| --- | ---: |
| inspeccionados | 486 |
| inspecciones_correctas | 484 |
| diccionarios_leidos | 88 |
| filas_diccionario | 1570 |
| definiciones_con_nombre | 1563 |
| filas_sin_nombre_variable | 7 |
| esquemas_archivo | 464 |
| columnas_archivo | 5675 |
| columnas_con_definicion_candidata | 4669 |

## Recursos sin estructura disponible

| Conjunto | Recurso | Causa |
| --- | --- | --- |
| Recursos Hídricos | Datos hídricos 1960-1969 | ValueError: Sin URL |
| Ganadería Sonora | Ganadería Sonora año 2013 | ValueError: Sin URL |

## Conexiones candidatas

Las coincidencias de nombre se limitan al mismo conjunto y requieren una única definición. No se crean equivalencias globales ni identidades de municipios.

| Rol según diccionario | Columnas |
| --- | ---: |
| codigo_municipio | 113 |
| municipio_declarado | 154 |
| anio_registro | 157 |
| municipio_registro | 49 |

## Alcance y límites

- Todos los recursos tienen un intento registrado, con fecha y fuente. Un fallo no se presenta como un esquema recuperado.
- Los esquemas de archivo describen cada hoja, conservan posiciones y etiquetas repetidas. Los encabezados detectados son candidatos y requieren revisión; no equivalen a un contrato de datos validado.
- Se leen hasta 30 filas para detectar encabezados. Las filas de datos no se guardan ni se incorporan al grafo. Excel usa copias acotadas en memoria o rangos HTTP; CSV de datos usa un prefijo acotado.
- Los diccionarios sí se leen completos, hasta 10,000 filas y con límite de bytes. Se conservan los valores originales. Las filas sin nombre de variable quedan en la evidencia JSON, sin inventar definiciones.
- La lectura completa del diccionario no valida la exactitud de sus definiciones ni resuelve sus referencias a catálogos externos.
- El primer cruce consulta solo tres campos por fila en dos recursos. Se conservan agregados, comprobando totales, IDs únicos y año.
- Las visualizaciones siguen inventariadas por URL; este proceso no demuestra de qué conjuntos se alimentan.
- La cobertura del catálogo original está en reports/cobertura-portal.md; este documento describe la inspección posterior.

Resultados del cruce: [primer-cruce.md](primer-cruce.md). Evidencia estructurada: `data/portal/contenido-inspeccion.json`, `data/portal/inspecciones/` y `data/portal/cruce-registro-civil.json`.
