# codigo/ — fuentes TS propuestas + tests Vitest (funciones reales)

Copia de trabajo del provider real con la politica acotada Gemma4.
Solo se escribe esta carpeta (y este README); repo/instalacion intactos.

## Contenido

- `providers/types.ts`: copia del source real Studio + campo opcional
  `minIntervalMs?` (autorizado; no rompe ningun otro Provider).
- `providers/openai.ts`: copia del source real + cambios marcados `[GEMMA4]`:
  politica SOLO si host `generativelanguage.googleapis.com` + modelo
  `gemma-4-31b(-it)` (Gemma3/local/Gemini: camino original intacto). Mutex por
  endpoint+modelo (reserva antes del fetch, libera en finally; pacing >=65s
  dentro del turno), reintento acotado a 1 (429/500/502/503, TimeoutError;
  jamas 400/401/AbortError), espera Retry-After/RetryInfo con piso 65s y tope
  120s (por encima: error con plazo), historial assistant 1 vez solo tras
  exito, `exigirRespuestaVisible` compartido.
- `parche-index-qa.patch`: hunks para `index.ts` (answerOnce exigente, sin
  fallback a runTurn en rama miss ni normal, sin cachear vacios; pacing al arranque).
- `tests/politica-gemma.test.ts`: 16 pruebas Vitest que importan las funciones
  reales (fetch stub + reloj fake; cero red/modelo/espera real).
- `vitest.config.ts`, `package.json`: config minima; `node_modules` es un
  symlink de SOLO LECTURA al del sidecar (sin instalar nada); cache en
  `.vitest-cache/` (esta carpeta).

## Ejecutar (root/integrador; local, sin modelo)

```
cd codigo
node <sidecar>/node_modules/vitest/vitest.mjs run
```

16/16 en 2026-10-23 (ver `vitest-salida.txt`) + `tsc --noEmit` limpio. Root aplica tras revision.
