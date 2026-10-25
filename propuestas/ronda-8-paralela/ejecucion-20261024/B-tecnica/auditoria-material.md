# Auditoría materialización v001 — B-tecnica (independiente)

- Material: `propuestas/ronda-8-paralela/ejecucion-20261024/materializacion/v001/aceptadas.json`
- SHA (calculado por código): `555c35697c86fd026d84d09a4bc02cc549237c5170c70d93c94ed5056d913fdf` — coincide con `congelada.json` y con el SHA fijado del encargo.
- Alcance auditado: **28 vínculos, 0 reglas, 0 conceptos**. Sin instalar, sin editar material; solo lectura. Detalle máquina en `auditoria-material.json`.

## Resultado: OBSERVADO — no aceptado global (14 aceptar / 14 rechazar)

Criterio aplicado por vínculo (no por nombre solo): nombre exacto + ordinal
columna = fila + `huella_esquema` + `huella_fila_diccionario` recomputadas +
recurso/diccionario/alcance + `definicion_iri` exacta con variable R7
`respaldada_por_definicion` y mismo concepto + correspondencia R7 en estado
`candidata_por_nombre` sin revisión previa.

- **M1 (14/14): aceptar.** `definicion_iri` con `/definition/...%2F<ord>` exacto,
  variable R7 respaldada con mismo concepto y regla, correspondencia candidata,
  huellas física y de fila coinciden.
- **M2 (14/14): rechazar por IRI hasta corrección.** Usan
  `/documented-variable/...` (el `iri` de variable) en vez del
  `/definition/...%2F<ord>` exacto. Lo físico (nombre/ordinal/huellas/
  recurso/diccionario) coincide y la variable R7 con el ordinal
  correspondiente **sí existe respaldada** con el mismo concepto, pero el
  vínculo no enlaza la definición exacta y rompería la cadena
  (`UNIVERSO`/validar exige `/definition/`). El defecto nace en
  `M2-sinac/v001/entrega.json` y se propaga a la materialización.
  Corrección pedida al coordinador: nueva versión con IRI `/definition/`
  exactos, sin editar v001 y sin ampliar evidencia de definiciones.

## Integridad de fuentes y R7

- `congelada.json`: 13/13 SHAs verificados por código, OK; `aceptadas_sha256` coincide.
- Fuentes copiadas idénticas a producción (`aceptadas-r7.json`
  `0d58255d...`, manifiesto R7 `7b5d242f...`, recibo `19705497...`).
- R7 **YA aprobada** (doble aceptar A/B con SHA pinnado, manifiesto intacto);
  **solo R8 está pendiente de auditoría**. La mención de M1 `entrega.md`
  línea 9 a "auditoría A/B pendiente" alude al histórico S2 v002, no a R7;
  no confundir ni reabrir definiciones.
- 16 roles congelados; `comprobar.py`: 0 faltantes, 0 discrepancias;
  conteos 28 propuestas + 172 brechas + 2 accesos = 202 casos. Selección
  final tras auditoría de código, como está previsto.
