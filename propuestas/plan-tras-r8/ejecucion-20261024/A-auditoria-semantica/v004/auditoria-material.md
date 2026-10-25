# Auditoría material K — v004 (2026-10-24)

Dictamen: **aceptar** (P1-Q1, P1-Q3, P4-exclusión). Solo `A-auditoria-semantica/v004/` modificado; material, scripts y producción intactos. GEMMA excluido.

- aceptadas.json `3f960a47…` = calculado; cubre datos/modelo/shapes + 2 pins (R8 `dba467b6…`, shape `fc301d85…`).
- Datos verbatim P1v003: `Milímetros`/`Hectáreas` con tilde, QUDT http, Q2 y estadoPropuesta ausentes (0).
- Modelo `rdf:Property` x8 (término RDF válido), 0 `rdfs:Property`.
- Fuentes fila/normativa = snapshots reales; base R8 intacta; scope zero joins; loader verbatim con 2 hooks mínimos.
- C4/v002: organismo por `result.organization`, 19/19 y 104/104 intactos, SHA `32478e45…`; versionado revisado.
- I-codigo/v001: borrador descartado, no usado.
