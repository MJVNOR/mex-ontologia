# A1-911 v001 — Llamadas Improcedentes <> Procedentes 911: BLOQUEADO

Pregunta: ¿comparar volúmenes procedentes/improcedentes por municipio y mes?
Proporción solo si las categorías particionan el mismo universo: **no consta** → bloqueada, sin join.

## Hallazgos (verificados por código en `scripts/comprobar_a1_911.py`)

- 6 recursos en 2 conjuntos. Diccionarios byte-idénticos (`fcd73b15…`, 7 vars, `Unidad de medida` vacía); no cubren `MOTIVO NO PROCEDENTE`.
- Recurso 54285a13 (conjunto Improcedentes, "Q1") trae hoja **LLAMADAS PROCEDENTES 911** y sha idéntico a 6ce17dd1 (`9d710c…`): duplicado entre conjuntos.
- Improcedentes Q2 (0df8592f) solo tiene FECHA/HORA/MOTIVO: **sin MUNICIPIO** → el corte por municipio es imposible para ese trimestre.
- Muestras n=29 solo en los dos recursos con esquema procedentes; alcance declarado: "no demuestra unicidad ni cobertura integral". Sin muestra de improcedentes Q2. Sin conteos de filas locales (solo bytes).
- Cruce R9: `candidata_por_validar`, `No ejecutado`; lote: `requiere_revision`, sin ejecuciones.
- 6 coincidencias muestrales en MUNICIPIO = coincidencia textual muestral, sin equivalencia demostrada.

## Ficha (resumen; detalle en entrega.json)

claves: sin PK · grano: fila-evento sin agregación validada · unicidad: no acreditable con muestra ·
cardinalidad: no acreditada · población: dos subpoblaciones sin partición acreditada ·
periodo: trimestres nominales 2026 sin verificar contenido · unidades: conteo, sin QUDT ·
cobertura: parcial y asimétrica, sin muestra de improcedentes Q2.

## Reapertura

Fe de erratas/diccionario que declare la partición del mismo universo con su total;
esquema con MUNICIPIO para improcedentes Q2; catálogo de municipios con unicidad;
copias locales de filas para conteos por municipio y mes.
