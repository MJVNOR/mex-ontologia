# A3 — ITAMA Internamiento/Externamiento (2026-10-24)

**Decisión: BLOQUEADO. Sin distribución computable. Entrega válida con causa y evidencia.**

Pregunta: ¿cómo se distribuyen los registros de internamiento y externamiento
por sexo/escolaridad en un periodo común?
Par `27a5c80c…--4d27a1c4…` (prioridad `revisar_primero`, estado
`candidata_por_validar`, decisión de lote `requiere_transformacion_o_catalogo`).

## 1. Qué se revisó (solo local, sin red ni grafo)

- `data/catalogo/metadatos.json` — 6 recursos XLSX trimestrales T1–T3 2026
  (internamiento: `56dbfc19…/59f89fe2…/525d84db…`; externamiento:
  `cf589b78…/71defd43…/7f95e924…`) + 2 diccionarios CSV.
- `data/portal/oportunidades-cruce.json` (reglas v1, 2026-10-23) — 8 familias,
  columnas por hoja (`POBLACION …`, `TIEMPO LIBRE`, `DIVERSO PROCESO`,
  `SENTENCIAS`, `ORAL`, `FEBRERO 2016`), pendientes heurísticas.
- `data/portal/lote-cruces/validacion-lote.json` — muestras históricas acotadas
  (A: n=29, 2026-10-23T06:59:45Z; B: n=16, 2026-10-23T06:59:46Z), no refetcheadas.
- `data/semantica/cobertura.json` — variables documentadas por diccionario.
- `data/semantica/nucleo.ttl` — conceptos `sexo-persona-internada/externada-itama`;
  escolaridad solo existe para Mano con Mano, difunto y madre (13 ocurrencias,
  ninguna ITAMA).
- Repo: 0 copias locales `*.xlsx` (excluidos `node_modules/.venv`).

## 2. Ficha de 8 ejes (detalle en `entrega.json:ficha_8_ejes`)

1. **Claves** — sin clave detectada; todo heurístico.
2. **Grano** — indefinido (hojas múltiples; fila=¿persona? sin definir).
3. **Unicidad** — no acreditada (muestra ≠ archivo entero).
4. **Cardinalidad** — no acreditada (sin conteos totales; coincidencia muestral
   sexo=1 valor `HOMBRE`, delito=0, sin equivalencia demostrada).
5. **Población** — distinta y no sumable (recluidos vs salidos de reclusión).
6. **Periodo** — común solo a nivel metadatos (2026-01-01 a 2026-09-30);
   periodo por fila no verificado.
7. **Unidades** — no declaradas (`no_especificada`, `Sin valores publicados`).
8. **Cobertura** — ESCOLARIDAD sin definición y 29/29 nulos en la única muestra
   que la midió; SEXO muestral A=`HOMBRE` (n=29), B=`HOMBRE+MUJER` (n=16).

## 3. Por qué no hay distribución

Sin archivos completos locales no hay conteo; sin catálogo de valores no hay
agregación válida; sin grano/unidad no hay medida; las poblaciones no se suman
y las personas no se unen. Publicar porcentajes con n=29/n=16 sería inventar
cobertura. Agregado sin identificadores personales: esta entrega solo publica
conteos y metadatos (ver `entrega.json:evidencia`).

## 4. Desbloqueo (petición documental concreta, sin enviar)

Copias locales completas de los 6 XLSX + catálogo de valores de sexo/escolaridad
del publicador + definición de grano y unidad por hoja. Entonces recalcular en
versión nueva (v002); nunca sobrescribir esta.

## 5. Límites respetados

Sin person matching, sin sumar universos, sin completar periodos/sujetos,
sin joins al grafo ni promociones, sin Gemma/contactos/búsquedas, sin tocar
base IRI ni R1–R9. Reproducible: `scripts/analisis_a3_itama.py`;
verificación: `pruebas/test_a3_itama.py`; sellado: `congelada.json`.
