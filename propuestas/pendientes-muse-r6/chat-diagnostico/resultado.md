# Resultado — diagnóstico HTTP500 selectivos (chat-diagnostico, R6)

0 llamadas al modelo. Motor intacto (321209 triples antes/después). Sin cambios
fuera de esta carpeta; sin cambios de modelo, claves, procesos, config ni UI.

## Verificado (revisable, re-ejecutable)

- `sonda_request.mjs` → `request-schema.json`: cuerpo QA real idéntico en los 6
  casos salvo `messages[1]`; sin tools; clave solo en header.
- `medir_contextos.mjs` → `medicion.json`: con trim ~6350 tok los 6; sin trim
  C3 9607 < C1 15625 < C2 22778 < C4 42976 < C5 58695 < C6 139862 (~488 KB).
  Scan limpio: 0 controles, 0 sustitutos (las 12 muestras).
- `medir_tools.mjs` → `tools-schema.json`: 114 tools, 132666 bytes (camino runTurn).
- `probar_sidecar.mjs` → `sidecar-protocolo.json`: `chat`/`reset` únicamente;
  `reset` vivo OK contra `dist/index.js` (`ready` → `reset_done`); además muestra
  `Model: default` sin `ONTO_LLM_MODEL`, el mecanismo de H1.

## Decisión

- D1-trim-condicionado-a-env: **propuesto** (`parche-propuesto.patch`, ~15 líneas).
- N1/N2: negativos verificados (contenido limpio; sin health/status).
- P1: ensayo espaciado queda en el integrador (incluye H3: vacío→runTurn).

## Re-ejecutar

`node sonda_request.mjs`, `node medir_contextos.mjs`, `node medir_tools.mjs`,
`node probar_sidecar.mjs [--vivo]`. Ninguna hace llamadas al modelo; las tres
primeras solo leen el motor vivo.

## Adenda 2026-10-23 (encargo integrador; reinicio ya hecho por CLI, no reiniciar)

- `harness_stdio.mjs [--revisar|--handshake|--casos]` + `harness-revisar.json`:
  bundle instalado 564051 bytes, env por puntero (valores jamás impresos),
  321209 triples. Modos vivos bloqueados sin `ONTO_ALLOW_CALLS=1` (solo root).
- `adenda-pacing-retry.md`: pacing 65000 sin consumidor + turnos concurrentes +
  cero reintento (docs primarias Google: 500/503 reintentables).
- `parche-pacing-retry.patch` + `proveedor-retry.mjs` + `test_retry_pacing.mjs`
  6/6 offline (stub, sin red ni modelo).
- Sin llamadas al modelo en esta carpeta: 0. Viva pendiente de root (P2).

## Corrección 2026-10-23 (datos reales R6; D1 refutada como causa)

- `correccion-d1.md`: bundle con Gemma explícita + budget activo y C2 500
  igual → D1 pasa a `robustez-no-causa`; D2 a `sustituido-por-D3`.
- `parche-qa-acotado.patch` (D3): guardia QA sin fallback a runTurn,
  reintento acotado a 1 (500/502/503, 429), RetryInfo piso 65s, consumo único.
- `proveedor-retry.mjs` + `qa-guardia.mjs` + `test_acotado.mjs` 10/10 con
  reloj fake (sin espera real, sin red, sin modelo).
- Root ensaya 6 casos (`harness_stdio.mjs`); auditor-chat revisa.

## Fase codigo TS + Vitest 2026-10-23 (fuentes completas, funciones reales)

- `codigo/`: `providers/types.ts` byte-idéntico; `providers/openai.ts` con
  política acotada Gemma4 (`[GEMMA4]`); `parche-index-qa.patch` (sin fallback
  runTurn en rama miss ni normal; `exigirRespuestaVisible`; pacing al arranque).
- `codigo/tests/politica-gemma.test.ts` 13/13 (`vitest-salida.txt`): reintento 1
  (500/502/503, TimeoutError), jamás 400/401/AbortError, Retry-After/RetryInfo
  con piso 65s y tope 120s con plazo explícito, serie entre instancias,
  no-Gemma intacto, helper puro compartido.
- `evidencia-bundle-r6.md`: mismo bundle + trim activo y C2/C3/C5 500 INTERNAL
  sin cuota + C6 TimeoutError + grafo intacto → D1 no causal (no aplicar como tal).
- Root aplica tras revisión; auditor-chat revisa. Sin modelos ni restart.

## Guardas de revisión temprana 2026-10-23 (gating + mutex)

- Gating estricto: política SOLO host `generativelanguage.googleapis.com` +
  `gemma-4-31b(-it)` (con/sin `models/`); local/Gemma3/Gemini/URL mala →
  camino original (probado).
- Mutex por endpoint+modelo: reserva antes del fetch, libera en finally
  (error/abort incluidos); pacing >=65s dentro del turno. Test con fetch
  bloqueado prueba que el segundo NO EMPIEZA hasta fin del primero + 65000.
- Clave de serie = URL+modelo (sin secretos); `minIntervalMs?` opcional en
  `Provider` (tipos intactos para otros); inyecciones por constructor.
- 16/16 Vitest + `tsc --noEmit` limpio (`codigo/vitest-salida.txt`).

## MARCADOR FINAL 2026-10-24 — tres fallos corregidos, 21/21 + tsc limpio

1. **Pacing antes de CADA fetch**: `ultimosInicios.set` movido dentro del
   bucle de reintento, justo antes de cada `fetchFn`. Nuevo test
   `500->200->nuevo provider` prueba gap >=65s tras el SEGUNDO intento
   (con el fallo anterior el gap era 0).
2. **Cooldown en TODOS los errores con plazo declarado**: `leerEsperaServidor`
   se evalua en cada `!resp.ok` y persiste el deadline aunque el error sea
   terminal (incluido el del segundo intento). Nuevo test: segundo intento
   429-900s deja cooldown y el nuevo provider es rechazado localmente
   con la misma hora y 0 fetch adicional.
3. **Cleanup de cola con la referencia correcta**: se guarda la cola
   (`anterior.then(() => turno)`) y el `finally` compara contra ella, no
   contra el turno; `models/` normalizado en `claveSerie` (misma serie y
   politica). Nuevo test con sonda `_hayTurnoPendienteParaTests`: pendiente
   durante fetch bloqueado, ausente tras completar.
- `exigirRespuestaVisible`: mensaje corregido — ya no afirma que no hubo
  herramientas (el retrieval readonly si ocurre); solo garantiza grafo
  sin modificar.
- Comentarios falsos corregidos en `codigo/providers/openai.ts`: cabecera
  (politica por host+modelo, no `/gemma/i`; sin "no aplicada"), camino
  original descrito por comportamiento (no "byte-identico"),
  `minIntervalMs` sin atribuir a `index.ts`.
- Pruebas reales actuales: **21/21 Vitest** (`codigo/vitest-salida.txt`),
  **`tsc --noEmit` limpio**, 0 llamadas al modelo, 0 red, reloj fake.
  Manifiesto: `listo-codigo-final.json` (SHA actuales).
  No se modifico `index.ts` (lo prepara root) ni el repo real.
