# Auditoría-a FINAL — gobierno-digital (243) + territorio-economía (534)

Auditor independiente. Solo escribe en `auditoria-a/`. Alcance: entregas
originales nuevas. NO UI/backend ni chat instalado. Sin red, sin suite central,
sin scripts históricos, sin modificar entregas ni núcleo. Sin bucles: se audita
lo que hay en disco con SHA coincidente con `listo.json`.

## Insumos (SHA actual verificado)

Copias congeladas `fuente/manifiesto.json`: 17/17 OK.
Evidencia base intacta (inspección/inventario/asignaciones = manifiesto).
Núcleo aplicado por el integrador durante la auditoría (se registra, no se toca).

| Entrega auditada | SHA-256 (= `listo.json`) | Reglas |
| --- | --- | ---: |
| `gobierno-digital/entrega.json` | `0909aea8…` | 121 |
| `territorio-economia/entrega.json` | `6f02a6c5…` | 482 |

Nota: el SHA anunciado `4571f753…` no existe en disco ni en `listo.json`;
`listo` y archivo real coinciden en `6f02a6c5…` (con huella top-level en las
482 reglas y 0 etiquetas "proyectada": corrección ya contenida). Si llega una
entrega nueva con SHA distinto, re-auditar.

## Dictámenes (603/603; `{dominio,regla_id,dictamen,motivo}`)

`auditoria.json` exacto + `detalle_por_regla` con chequeos en `auditoria-base.json`.
Revisión literal de cada regla (no estructural, no por conteos): IRI/fila/huella,
literales byte-exactos, alcance simultáneo, representación, concepto y herencia
(unidad, sujeto, población, periodo, metodología, padres), colisiones.

| Dominio | Aceptar | Condicionado | Rechazar |
| --- | ---: | ---: | ---: |
| gobierno-digital | 118 | 3 | 0 |
| territorio-economía | 471 | 11 | 0 |

Reconsiderados por doctrina del integrador (verificado en archivo actual):
sensibilidad de tema/etnia/víctima/discapacidad por sí sola NO niega un
significado literal documentado (informativo, sin asignar identidad);
población respaldada por contexto publicado explícito NO se condiciona;
calificadores DDR/instrumento se propagan en el pipeline real (verificado
regla por regla, 80/80) y el integrador ya ejecutó `construir` real
(980 reglas, 149 calificadas, 58149 triples, límites preservados).

## Accionables (14 condicionados, 0 rechazos)

- BLOQUEANTE DEVUELTO (10): IM vs IMN marginación, separar normalizado/original
  en todos los niveles. No integrar.
- Ejemplos incoherentes con tipo (Platicas/No/Si, "Bajo"): no tipificar.
- NDDR agro congelado queda fuera de esta fase (TE ya trae `no_especificada`).

## Verificación propia (read-only fuera de esta carpeta)

```powershell
uv run python -B propuestas/cobertura-muse-20261023/auditoria-a/scripts/auditar.py
uv run python -B propuestas/cobertura-muse-20261023/auditoria-a/scripts/verificar.py
```

OK: 603/603 positivos con pipeline real y reglas COMPLETAS (calificador
propagado y verificado), 9 negativos, huellas estables, 0 colisiones, 0
U+FFFD, 0 sameAs/exactMatch.

## Archivos (solo carpeta asignada)

`auditoria.json` (final) + `auditoria-base.json` (detalle), `fuente/huellas.json`,
`scripts/auditar.py`, `scripts/verificar.py`, `resultado.md`.

## Pendientes

1. Integrador: 14 condicionados (10 DEVUELTOS, 4 ejemplos). 2. Agente 2:
candidatas y pendientes. 3. Re-auditar si llega entrega con SHA nuevo.
