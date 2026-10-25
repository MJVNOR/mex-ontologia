# ENTREGA — STAGING R9 I-codigo/v001

Fecha UTC: 2026-10-24. Estado: `propuesta_para_auditar`. Produccion intacta
(todo vive en `propuestas/plan-tras-r8/ejecucion-20261024/I-codigo/v001/`).

## Sello SHA-256 (archivos staging)

- `094e3ebacf8b8d50` `data-integracion-ronda-9/aceptadas.json`
- `0b0d3b0cdd9bd9ca` `data-integracion-ronda-9/auditorias/auditoria-a.TEMPLATE.json`
- `7f9fbe75baa1e407` `data-integracion-ronda-9/auditorias/auditoria-b.TEMPLATE.json`
- `1e97409e648b4d2c` `data-integracion-ronda-9/datos/propuesta-qudt.ttl`
- `ec2ab62a659ae28b` `data-integracion-ronda-9/materializar.py`
- `9dcff9420cb6e31b` `data-integracion-ronda-9/modelo/vocabulario-minimo.ttl`
- `fc301d854b6c9175` `data-integracion-ronda-9/shapes/shape-exclusion-significado.ttl` (= P4 v001)
- `7178ca15f36b5965` `plantilla-ontologia-revision-ronda-9.json`
- `54a4d03bc5fec84b` `README.md`
- `63d2fc8248649a0b` `scripts/ampliar_portal.py` (produccion + 9 lineas: `carga_shapesR9` + atomico)
- `db2d3441ac4f159f` `scripts/consolidar_semantica.py` (produccion + 9 lineas: hook R9 tras R8)
- `8bf6fb9bfe7c2fe3` `scripts/integrar_ronda_9.py`
- `31b2db7e58f8eb85` `tests/fixtures/declaraciones-ejemplo.json`
- `33068f834565943f` `tests/test_integrar_ronda_9.py` (17/17 OK en tmp, sin produccion)

## Pins externos verificados

- R8 vivo: respaldadas `1423`, conceptos `1106`, revisadas `4506`, candidatas `17`,
  materializadas `1442` (`reports/ronda-8.json` + `data/semantica/cobertura.json`).
- W normativa: MilliM `5e636911…`, HA `90959683…`, negativo HectoM3 `ffe0ff44…`.
- Shape P4 v001 `fc301d85…` = staging; fidelidad triple-a-triple Q1/Q3 vs P1 v002.
- Huellas fila: Q1 `dec3bb83…`, Q3 `208a95e2…` (recomputadas contra inspeccion viva).

## Decisiones (lo no integrado, a proposito)

Q2 hm3, P2 intervalos, P3 jerarquias: fuera (negativos documentados, 0 instancias).
C1-C4: vistas derivadas, no materializan. Sin `QuantityValue`, sin conversiones,
sin columna fisica en TTL, sin edicion del nucleo (reglas/conceptos/vinculos = 0/{}).
`format_version: 1` va separado de `release: R8→R9`; manifiestos R1-R8 intactos.

## Para el coordinador

Sin instalar ni regenerar desde aqui. Tras A+B: `materializar.py` →
fijar `aceptadas_sha256` en ambas auditorias → re-materializar →
escribir `ontologia/revision-ronda-9.json` → copiar `scripts/` → pipeline + Studio.
Si P1 v002 cambia antes de instalar, `materializar.py` lo detecta y se rehace v002.
