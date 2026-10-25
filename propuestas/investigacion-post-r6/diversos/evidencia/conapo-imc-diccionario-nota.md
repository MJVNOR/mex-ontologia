# Nota de análisis — Diccionario nacional IMUC_2020 y encabezado de datos (2026-10-24)

Fuente: `conapo-IMC_2020.zip` (sha256 5d93b314…, 43415698 bytes) →
`IMUC_2020.xlsx`, hojas `BaseMarginación2020_*` (localidad),
`IMUC_2020_*` (colonia), `Diccionario`. Método: openpyxl read_only.
No se equipara localidad/AGEB con colonia: todo lo citado abajo es de las
hojas `IMUC_2020_*` y del `Diccionario` del mismo libro.

## Hoja Diccionario (transcripción íntegra de filas con contenido)

Encabezado: `Variable | Descripción`.

| Variable | Descripción |
|---|---|
| CVE_COL | Clave de colonia |
| ID_COL | Identificación de colonia |
| NOM_COLONIA | Nombre de la colonia |
| CP | Código Postal |
| CLASIF | Clasificación |
| CVE_ENT | Clave de la entidad |
| NOM_ENT | Entidad federativa |
| CVE_MUN | Clave del municipio |
| NOM_MUN | Nombre del municipio |
| CVE_LOC | Clave de localidad |
| NOM_LOC | Nombre de localidad |
| SUN_2018 | Clave de ciudad del Sistema Urbano Nacional 2018 |
| NOM_SUN | Nombre de ciudad del Sistema Urbano Nacional 2018 |
| POB_TOT | Población total |
| P6A14NAE | Porcentaje de población de 6 a 14 años que no asiste a la escuela |
| SBASC | …sin educación básica (15+ años) |
| PSDSS | …sin derechohabiencia a servicios de salud |
| OVSDE / OVSEE / OVSAE / OVPT / OVHAC / OVSREF / OVSINT / OVSCEL | Indicadores de carencias en vivienda (8) |
| IM_2020 | Índice de marginación |
| GM_2020 | Grado de marginación |
| IMN_2020 | Índice de marginación normalizado |

Pie: `Fuente: Estimaciones del CONAPO con base en el INEGI, Censo …` (2020).

Lectura: el diccionario local (28 filas, CLASIF = "Clasificacion") es espejo
de este diccionario nacional (28 variables, mismo orden y nombres salvo
`COLONIA` local vs `NOM_COLONIA` nacional). El propio diccionario nacional
describe CLASIF solo como "Clasificación" (genérico también a nivel nacional).

## Encabezado de datos (hoja IMUC_2020_NAY-ZAC, fila 1)

`CVE_COL | ID_COL | COLONIA | CP | CLASIF | CVE_ENT | NOM_ENT | CVE_MUN |
NOM_MUN | CVE_LOC | NOM_LOC | SUN_2018 | …` (28 columnas).
Filas de ejemplo: `18001_0001 | 52584 | Ali Chumacero | 63400 | Colonia |
18 | Nayarit | …`. Formato de clave `nnnnn_nnnn`, idéntico al local.
