# A2 — Registro civil: Matrimonios / Nacimientos (análisis separado, v002)

Par: `1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5`.
Solo datos/documentos locales existentes. Sin red, sin grafo, sin Studio,
sin causalidad, sin tasas poblacionales, sin joins.

v002 reproduce el análisis de v001 sin cambiar veredicto, cifras ni ejes.
Corrige H-02 y H-04 del dictamen `R-documental/v001` (trazabilidad/redacción).

## Pregunta

¿Qué volúmenes de matrimonios y nacimientos se registran en un periodo
y ámbito territorial documentalmente comparables? Son eventos y poblaciones
distintos.

## Ficha: 8 ejes (resumen; detalle verificable en `resultados.json`)

| # | Eje | Veredicto | Evidencia local |
|---|-----|-----------|-----------------|
| 1 | Claves | no acreditada | Par `candidata_por_validar`; coincidencia solo textual de `municipio`; pendiente `verificar_catalogo_dominio_unicidad_y_contexto_de_clave` (`data/portal/oportunidades-cruce.json`) |
| 2 | Grano | distinto, bloquea join | Matrimonios: fila = evento (día, edad/sexo contrayentes). Nacimientos: fila = agregado (hombres/mujeres/total por municipio-año-mes). Diccionarios en `data/portal/contenido-inspeccion.json` (SHA `0b6ee6ce…`, `7683a054…`) |
| 3 | Unicidad | no acreditada | Muestras n=100: "no demuestra unicidad ni cobertura integral" (`data/portal/lote-cruces/validacion-lote.json`) |
| 4 | Cardinalidad | no acreditada | `fallo_validacion_integral`: total ≠ hombres+mujeres (5/6 pruebas); meses faltantes (2016) |
| 5 | Población | distinta | Actos matrimoniales vs conteos de nacidos; sin id de persona; sin vínculo entre conjuntos |
| 6 | Periodo/ámbito | solo registro, no join | Años coincidentes solo en nombres (2015–2024); ambos: "Municipio de registro", "Año de registro" y "Mes de registro" (Matrimonios incluye "Dia de registro"); ningún campo de residencia; sin catálogo de correspondencia |
| 7 | Unidades | no homologables | Fila-evento vs fila-agregado; pendiente `validar_unidades_de_medidas_seleccionadas`; unidad = eventos/conteos, no personas |
| 8 | Cobertura | no acreditada | "Faltan meses por municipio; ausencia no equivale a cero"; muestras ≠ universo |

## Inventario (H-02 precisado)

- Matrimonios: **10 recursos de datos** (2015–2024) **+ 1 diccionario = 11**.
- Nacimientos: **15 recursos de datos** (2010–2024) **+ 1 diccionario = 16**.

Los conteos incluyen el recurso `Diccionario` de cada conjunto; los años
corresponden solo a los recursos de datos.

## Veredicto

**BLOQUEADO**: sin comparación de volúmenes ni join. Causas en `resultados.json`.
Reproducible: `.venv/Scripts/python.exe scripts/analizar.py` regenera
`resultados.json`. Sello: `scripts/sellar.py` escribe `sello.json` y
`sello.sha256` (hash propio en sidecar, sin autorreferencia ni cachés).
Pruebas: `.venv/Scripts/python.exe -B -m unittest discover -s tests`.
