# Nota de análisis — compatibilidad del dominio CLASIF Sonora (2026-10-24)

Método: lectura directa de los tres archivos (DBF por struct, XLSX por
openpyxl read_only). Generador: `gen_diversos.py` (modos dbfval/dbfson/
xlsxson/xlsxloc). No se equipara localidad/AGEB con colonia: los tres
objetos son a nivel colonia.

## Resultado

| Fuente | Filas con clave | Valores CLASIF distintos (conteo) |
|---|---|---|
| `sonora-imc2020-local.xlsx` (portal Sonora, hoja IMC_2020) | 2129 | Colonia 1050, Fraccionamiento 854, `-` 119, Barrio 89, Unidad habitacional 7, Residencial 7, Privada 2, Ejido 1 |
| `conapo-IMC_2020.zip:IMUC_2020_*` (CVE_ENT=26) | 2129 (subset) | idéntico: 1050 / 854 / 119 / 89 / 7 / 7 / 2 / 1 |
| `conapo-imc2020_shp.zip:colonias_imc2020.dbf` (CVE_ENT=26) | 2129 | idéntico: 1050 / 854 / 119 / 89 / 7 / 7 / 2 / 1 |

El subset Sonora del archivo local coincide en valores con el subset Sonora
del producto nacional (2129 filas, distribución exacta, formato de clave
`26001_0001`, esquema de 28 columnas). No se declara igualdad universal de
todo el producto nacional: solo se cotejó el subset Sonora y el esquema.

## Conteo nacional (corrección 74227 vs 74226)

`IMUC_2020_AGS-MOR`: 40036 filas de datos, 40035 con clave + **1 fila vacía**;
`IMUC_2020_NAY-ZAC`: 34191 filas, todas con clave. Válidas totales:
74226 = registros del shapefile. La diferencia era una fila vacía, no un
registro adicional.

## Dominio nacional observado (74226 filas válidas, 38 valores distintos; no es catálogo)

Colonia, Fraccionamiento, Barrio, Unidad habitacional, Pueblo, `-`,
Residencial, Ampliación, Localidad, Condominio, Conjunto habitacional,
Sección, Ejido, Rancho, Parque industrial, Sector, Rinconada, Paraje,
Supermanzana, Región, Villa, Zona industrial, Zona militar, Hacienda,
Unidad, Ex-Hacienda, Manzana, Privada, Cuartel, Granja, Fracción, Ciudad,
Cantón, Corredor industrial, Ciudad industrial, Ranchería, Zona federal,
Puerto. (Nota: un registro con artefacto de codificación en `Ranchería`.)

Los 7 valores de la unidad local están contenidos en el dominio nacional
**observado** (38 valores; ver lista abajo: no es un catálogo publicado, es
conteo de valores observados en los datos); `-` es el marcador de nulo
declarado en el diccionario local ("Identificador de valores nulos: `-`",
obligatoriedad: No). La compatibilidad de valores no autoriza joins por
CLASIF ni identidad de catálogos entre el recurso local y el producto
nacional.

## Contraste INEGI (contexto, sin vínculo)

El catálogo nacional INEGI v_tip_asen (RNM) usa 43 categorías con códigos
numéricos 1–43 (+Ninguno/Otro); el producto CONAPO usa texto libre con 38
valores observados. No se adoptan los códigos INEGI: el vínculo
acreditable es con el producto CONAPO IMC_2020, no con el catálogo INEGI.
