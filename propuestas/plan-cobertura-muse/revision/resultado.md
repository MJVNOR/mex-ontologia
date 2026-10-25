# Plan de aceptación e integración — cobertura semántica (revisión)

Auditor independiente. Solo archivos nuevos en
`propuestas/plan-cobertura-muse/revision/`. Sin red, sin modelos, sin tocar
núcleo/Studio, sin generar ni sincronizar. No se auditan centenares de reglas
aquí: se separa lo auditado de lo pendiente y nada se aprueba por conteos.

## Lo auditado (verificado en sus auditorías, no re-auditado)

- Agente 3 (63 reglas: 52 aceptar / 11 condicionado) y agente 7 (76
  auditadas: 61 / 15 / 0) — `agente-11-auditoria/auditoria.json`.
- Agente 6 (204 reglas: 197 / 7 / 0) —
  `agente-12-auditoria-salud/auditoria.json`.
- Base preservada en ambas: 103 conceptos, 232 respaldadas, 836 revisadas,
  118 candidatas, 23 significados, 16 catálogos, 32/14, 1850 IML.

## Lo pendiente de auditoría (637 reglas, NO integrar antes)

- Agente 8 educación: 99 reglas / 66 nuevos / 27 pendientes.
- Agente 9 gobierno digital: 121 reglas / 85 nuevos / 122 pendientes.
- Agente 10 territorio-economía: 419 reglas / 398 nuevos / 51 pendientes.

## Bloqueos reales

1. **Calificadores perdidos (pipeline):** `interpretacion()/construir()` no
   propagan calificador — 10 SHD-DDR (A3) + 20 sede (A8) perderían su
   distinción en el grafo. Propagar + validar o estrechar a 30 conceptos.
2. **Control desfasado:** `control-propuestas.json` marca A10 `sin_entrega`
   (hay entrega) y discrepa en conteos A10 (417/396 vs 419/398 en archivo) y
   A9 (86 vs 85). Regenerar antes de integrar. A7: entrega dice 75,
   auditoría 76 — aclarar 1.
3. **Condicionados sin aplicar:** 26 (A11) + 7 (A12); ninguno habilita cruces.
4. **709 candidatas A3** no revisadas → agente 2, no son correspondencias.

## Secuencia

L1 aplica A3+A7 aceptadas · L2 aplica A6 + 5 espacios finales · L3 audita
A8/A9/A10 · L4 resuelve calificadores · L5 integra por lotes. Detalle,
criterios de entrada/salida, preguntas semánticas y negativos obligatorios
en `plan-validacion.json`.

## Rutas

- `propuestas/plan-cobertura-muse/revision/plan-validacion.json`
- `propuestas/plan-cobertura-muse/revision/resultado.md`
- Fuentes leídas: `propuestas/ronda-3/agente-*/resultado.md`,
  `agente-11-auditoria/{resultado.md,propuestas.json}`,
  `agente-12-auditoria-salud/resultado.md`,
  `propuestas/ronda-3/integrador/control-propuestas.json`,
  `docs/integracion-de-agentes.md`, `scripts/consolidar_semantica.py`.
