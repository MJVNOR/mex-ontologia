# A3 — ITAMA Internamiento/Externamiento (v002, 2026-10-24)

**Decisión: BLOQUEADO. Sin distribución computable. v002 corrige el alcance de
la búsqueda de copias; no cambia el veredicto.**

Pregunta: ¿cómo se distribuyen los registros de internamiento y externamiento
por sexo/escolaridad en un periodo común?
Par `27a5c80c…--4d27a1c4…` (estado `candidata_por_validar`, decisión de lote
`requiere_transformacion_o_catalogo`).

## 0. Corrección respecto a v001

| v001 afirmaba | v002 registra |
| --- | --- |
| «Repo: 0 copias locales `*.xlsx`» | **138 XLSX locales de otros conjuntos** (territorio/presas, catálogos, salud, nacimientos) y **0 copias ITAMA** (0 de 8 IDs) |
| Barrido implícitamente repo-wide | Consulta acotada por ID, nombre y contenido XML; lo ajeno a ITAMA no se evalúa ni se niega |

La afirmación de v001 era falsa para todo el repo. Su script tampoco era
ejecutable desde su ruta (`ROOT=parents[3]` apuntaba a `ejecucion-20261024`) y
además invertía `min`/`max` del periodo: su assert repo-wide nunca se evaluó.
v001 se conserva intacta; el hash de sus 3 archivos queda fijado en
`entrega.json:v001_intacta`.

## 1. Búsqueda registrada (patrón → rutas → resultado)

| ID | Patrón | Resultado |
| --- | --- | --- |
| P1 | `**/*.{xlsx,xls,xlsm}` (sin `.git`, `.venv`, `node_modules`) | 138 libros; **0 ITAMA** |
| P2 | nombre con alguno de los 8 IDs ITAMA | 16 JSON de inspección (8 IDs × original + respaldo); **0 XLSX y 0 CSV** |
| P3 | contenido XML: token `\bITAMA\b` + IDs | 0 con token; 0 con IDs; 4 subcadenas `ITAMAR`, `CHITAMA`, `IXCATITAMAN` (localidades, falsos positivos) |

Registro completo, con las 138 rutas y el SHA256 de cada archivo consultado:
`evidencia-busqueda.json`, producido por `scripts/registrar_busqueda_itama.py`.

- **Permitido afirmar:** no hay copias locales de los 6 XLSX ni de los 2 CSV de
  ITAMA (0 de 8 IDs, por nombre y por contenido).
- **Prohibido afirmar:** que el repositorio no contiene XLSX.

## 2. Núcleo: sexo con IDs respaldados, escolaridad sin ellos

Extracto verbatim en `nucleo.ttl` (fuente `data/semantica/nucleo.ttl`, SHA256
`e570e590…`; no sustituye al núcleo):

- **Sexo ITAMA:** 2 conceptos con IRI (`sexo-persona-internada-itama`,
  `sexo-persona-externada-itama`), respaldados por 2 diccionarios con ID
  (`07781b38…`, `a7ee5717…`) que definen `sexo`, y por valores muestrales
  (`HOMBRE` en A, n=29; `HOMBRE`+`MUJER` en B, n=16).
- **Escolaridad ITAMA:** 0 conceptos, 0 definiciones en los diccionarios ITAMA,
  29/29 nulos en la muestra A y no solicitada en B. Los 3 conceptos de
  escolaridad del núcleo pertenecen a Mano con Mano, difunto y madre.
- `tiempo-sentencia-persona-externada` se define en ITAMA pero su IRI no lleva
  sufijo `-itama`; queda fuera del extracto y anotado en su cabecera.

## 3. Ficha de 8 ejes (detalle en `entrega.json:ficha_8_ejes`)

Claves sin detectar; grano indefinido; unicidad y cardinalidad no acreditadas;
poblaciones distintas y no sumables; periodo común solo documental
(2026-01-01 a 2026-09-30); unidades no declaradas; cobertura insuficiente.

## 4. Por qué no hay distribución

Sin archivos ITAMA completos no hay conteo; sin catálogo de valores no hay
agregación válida; sin grano/unidad no hay medida; las poblaciones no se suman
y las personas no se unen. Publicar porcentajes con n=29/n=16 inventaría
cobertura. Esta entrega solo publica conteos y metadatos agregados, sin
identificadores personales.

## 5. Desbloqueo (versión nueva, v003)

Copias locales completas de los 6 XLSX + catálogo de valores de sexo/escolaridad
del publicador + definición de grano y unidad por hoja. Entonces recalcular en
v003; nunca sobrescribir v001 ni v002.

## 6. Límites y reproducibilidad

Sin person matching, sin sumar universos, sin completar periodos/sujetos, sin
joins al grafo, sin Gemma/contactos y sin búsqueda web. No se toca la base IRI,
el núcleo, los manifiestos R1–R9 ni la producción; todo se escribe en
`A3-itama/v002`.

```
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/scripts/analisis_a3_itama_v002.py
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/tests/test_a3_itama_v002.py -v
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/scripts/sellar_v002.py
```

Sello: `congelada.json` + `congelada.sha256` (SHA256 por archivo, sin
autohash).
