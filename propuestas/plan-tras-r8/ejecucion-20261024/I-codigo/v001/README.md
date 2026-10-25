# STAGING R9 — I-codigo/v001 (NO instalado, NO produccion)

Integracion propuesta post-R8: **solo pilotos aceptados**.

- **P1-QUDT v002**: 2 declaraciones cualificadas (`P1-Q1` MilliM, `P1-Q3` HA,
  IRI HTTP canonicas verificadas por W). `P1-Q2` hm3 **fuera**: sin vinculo,
  sin conversiones, sin `QuantityValue`.
- **P4 v002**: shape de exclusion `significadoDocumentado`/`significadoCandidato`
  via `sh:sparql` (forma exacta v001) + 4 fixtures re-ejecutadas en store temporal.
- **P2/P3 negativas**: 0 intervalos, 0 jerarquias. **C1-C4**: vistas derivadas,
  no se materializan.

## Estructura

- `scripts/integrar_ronda_9.py` — `cargar(root)` / `construir(report,rules,base,root)` /
  `cargar_shapes(root)`. Verifica SHA + rutas confinas, payload exacto aprobado por
  A+B global y por caso, pin de semantica actual = snapshot, pin R8
  (1423/1106/4506/17/1442), fila local (huella+unidad+normativa W) contra
  cobertura/inspeccion, grafo extra de solo 2 declaraciones, shape por hash.
- `scripts/consolidar_semantica.py` — copia COMPLETA de produccion + hook R9
  **despues de R8** (9 lineas; sin tocar cadena R1-R8).
- `scripts/ampliar_portal.py` — copia COMPLETA de produccion + `carga_shapesR9`
  y `escribir_json_atomico` para `reports/portal-carga.json` (mismos bloqueos Windows).
- `data-integracion-ronda-9/` — `aceptadas.json` (2 declaraciones, `format_version`
  separado de `release`), `datos/` + `modelo/` + `shapes/` TTL, plantillas de
  `auditorias/a+b.json`, `materializar.py` (**solo lo corre el coordinador**).
- `tests/test_integrar_ronda_9.py` — 17 regresiones sobre tmp sintetico
  (payload, provenance, auditorias, shapes, rutas, nucleo, reporte vivo).
- `plantilla-ontologia-revision-ronda-9.json` — lo que el coordinador escribe en
  `ontologia/revision-ronda-9.json` tras fijar el manifiesto.

## Auditar (sin instalar nada)

`uv run python propuestas/plan-tras-r8/ejecucion-20261024/I-codigo/v001/tests/test_integrar_ronda_9.py`
→ `OK` (17 pruebas). No toca produccion: evidencia sintetica en tmp.

## Instalacion (coordinador, tras auditoria A+B)

1. `uv run python .../I-codigo/v001/data-integracion-ronda-9/materializar.py`
   (verifica pins vivos, genera `data/integracion-ronda-9/` + imprime SHAs).
2. Fijar `aceptadas_sha256` en `auditoria-a/b.json`, re-ejecutar `materializar.py`
   (el SHA cambia), escribir `ontologia/revision-ronda-9.json`.
3. Copiar los 3 `scripts/*.py` a `scripts/`, correr el pipeline completo y Studio.

Prohibido: regenerar, instalar o correr Studio desde este staging.
Modelo: ModelMuse solicitado; sin Gemma, sin contactos. R8 no se rehace.
