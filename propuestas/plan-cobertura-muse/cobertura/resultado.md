# Plan de cobertura semántica con agentes Muse (ronda 3 existente, sin integrar)

Plan ejecutable, no integración. Base recalculada y partición verificada con
`scripts/comprobar.py` (52 comprobaciones PASS, 0 fallos). Todo verificado
contra archivos reales; nada promete confirmar lo no documentado.

## 1. Base recalculada (`data/semantica/cobertura.json`)

SHA-256 actual `38d0e7cb…9bde` = el fijado en `asignaciones-semanticas.json`:
base sin cambios.

| Medida | Valor |
| --- | ---: |
| Variables totales | 1563 |
| Respaldadas | 232 |
| Fuera del núcleo | 1308 |
| Candidatas agente 4 (aparte) | 23 |
| Núcleo: conceptos / reglas | 103 / 116 |

## 2. Partición exacta: 1242 + 66, 23 aparte

| Lote | Variables |
| --- | ---: |
| Agente 6 (salud) | 242 |
| Agente 7 (registro civil) | 163 |
| Agente 8 (educación) | 126 |
| Agente 9 (gobierno digital) | 243 |
| Agente 10 (territorio-economía) | 468 |
| **Subtotal partición** | **1242, sin duplicados, dentro de fuera del núcleo, sin tocar las 23** |
| Agente 3 (resto leído) | 66 = 1308 − 1242, verificado idéntico a su cobertura (63 reglas + 3 sin propuesta) |
| **Total** | **1308** |

Cero solapes entre los 6 lotes; cero decisiones/reglas fuera de partición;
cero toques a candidatas del agente 4.

## 3. Decisiones por entrega (proponer / pendiente)

| Agente | Decisiones | Proponer | Pendiente | Reglas | Vars únicas | Conc nuevos | Reutil | Calif |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 cobertura | 66 | 63 | 3 | 63 | 63 | 55 | 1 | 10 |
| 6 salud | 242 | 203 | 39 | 203 | 203 | 178 | 6 | 0 |
| 7 registro civil | 163 | 75 | 88 | 75 | 75 | 50 | 1 | 0 |
| 8 educación | 126 | 99 | 27 | 99 | 99 | 66 | 1 | 20 |
| 9 gobierno digital | 243 | 121 | 122 | 121 | 121 | 85 | 0 | 0 |
| 10 territorio-economía | 468 | 419 | 49 | 419 | 419 | 398 | 5 | 0 |
| **Total** | **1308** | **980** | **328** | **980** | **980** | **832** | **14** | **30** |

Reglas 1:1 con variables únicas en las 6 entregas (una regla por definición).
Conceptos vs interpretaciones: 832 nuevos + 103 vigentes; 980 interpretaciones.

## 4. Entregas en evolución: SHA antes (control 03:43:21) / después

| Agente | SHA control | SHA actual | Reglas antes → ahora | Estado |
| --- | --- | --- | --- | --- |
| 3 | `29f1dadf…` | `29f1dadf…` | 63 → 63 | Sin cambios |
| 6 | `f89424dc…` | `2b12af0c…` | 204 → 203, conceptos 179 → 178 | Evolucionó post-control |
| 7 | `f075f884…` | `c0523fc8…` | 76 → 75 | Evolucionó post-control |
| 8 | `9672a4ba…` | `9672a4ba…` | 99 → 99 | Sin cambios |
| 9 | `4fa16db1…` | `d730f00d…` | 121 → 121 (mismos conteos, contenido distinto) | Evolucionó post-control |
| 10 | sin_entrega | `b266283b…` (03:49:14) | — → 419 | Entregó post-control |

Hallazgo que bloquea: los `conteos` incrustados del agente 10 dicen 417/51
pero el contenido trae 419/49 (sigue evolucionando). Huellas de entrada de
las 6 entregas coinciden con los archivos actuales
(cobertura `38d0e7cb…`, semántica `b36ea6c6…`, inspección `61861aab…`,
inventario `783f1255…`, asignaciones `360cb7f7…`, pendientes `9294f997…`).

## 5. Fases y reparto por dominio (completar TODO el inventario)

- **Fase 0 — hecha aquí:** base y partición verificadas; 23 aparte.
- **Fase 1 — re-congelar:** fijar SHAs actuales de 6, 7, 9 y 10; exigir
  conteos incrustados = contenido (bloquea agente 10).
- **Fase 2 — revisión por dominio con validador común** (reglas restringidas,
  literales exactos, sin correspondencias; calificadores SHD/sede con
  requisito de propagación): 6 salud/vigilancia (242), 7 registro civil
  (163), 8 educación (126), 9 gobierno digital (243), 10
  territorio-economía (468), 3 agro/pesca cerrada (66).
- **Fase 3 — 328 pendientes** (325 partición + 3 agente 3): clasificar con
  razón (vacía/genérica/fuera de alcance) o segunda lectura. Lo no
  documentado queda pendiente, nunca confirmado.
- **Fase 4 — integración diferida, fuera de este plan:** simulación,
  propagación de calificadores, aplicación; sin auto-cruces ni sameAs.

## 6. Archivos y reproducción

- `propuestas/plan-cobertura-muse/cobertura/inventario.json`
- `propuestas/plan-cobertura-muse/cobertura/resultado.md`
- `propuestas/plan-cobertura-muse/cobertura/scripts/comprobar.py`

```powershell
uv run python propuestas/plan-cobertura-muse/cobertura/scripts/comprobar.py
```

Sin red, sin modelos adicionales, sin modificaciones centrales, sin
generación ni sincronización. No se modificó ninguna entrega anterior.
