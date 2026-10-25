# Oráculos del chat (ronda 4) — resultado

## Manual (5 respuestas, gemini-3.1-flash-lite + 3.5-flash; Gemma: 0 utilizables, nada que evaluar)

- C1 totales: **acierto** — 865/3283/12/4160 verificados por SPARQL vivo solo-lectura.
- C2 F2: **falla_real** — responde con el concepto TIC (real pero ajeno) pese a 240 hechos; la 3.5-flash admitía no hallar F2, la 3.1-flash-lite presenta TIC como respuesta (regresión en honestidad, mismo fallo de recuperación).
- C3 igualdad: **acierto** (converge en ambos modelos) — todo el fondo verificado en `F2.json` (72/72, 7344/7344, constructos distintos, INEGI/vigencia/serie pendientes, exploratorio). Reserva: una comilla `[26001-2020]` no está en ningún fichero (Studio caído al verificar nodo vivo).
- C4 definición: **acierto** — "Año de registro", URL diccionario.csv, concepto `anio-registro` e IRI verificados.
- C5 diferencia: **acierto_con_reserva** — definiciones y conteo 10/10 verificados en `semantica.json`; el `falla_oraculo` viejo es **falso rechazo** (exigía literales `2022` y `candidata_por_nombre`). Reserva: IRIs de mapeo no verificables offline.
- C6 26001: **no_evaluable** — bloqueo de cuota, recuperación intacta, triples 284810.

## Defecto del corpus viejo y corrección entregada

Literales (`865`, `364ffa5c`, `candidata_por_nombre`, `2022`) + prohibidos sin negación (`misma medida`) = falsos rechazos. Nuevo corpus: alternativas, negación que cuenta a favor (con `vs.`/`p. ej.` protegidos), oráculos derivados (`oraculo_local.py`), 5 dimensiones (veracidad, completitud, citación, recuperación, bloqueo). Harness: `uv run python propuestas/pendientes-muse-r4/oraculos-chat/evaluador.py` — sin modelo/red/Studio/cuota. `demo()` en ambos scripts como auto-chequeo.
