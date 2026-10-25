# Adenda: pacing no aplicado + reintento ausente + compat Google (solo primaria)

Fuentes primarias (ai.google.dev, 2026-10-22/23): `openai`, `troubleshooting`,
`api-errors`. Sin adivinanza: lo no documentado se marca como tal.

## 1. pacing 65000 NO se aplica en el caller real (evidencia, no hipótesis)

- `GEMMA_PACING_MS=65000` y `budgetForModel().pacingMs` existen en `graphrag.ts`
  (y en el bundle instalado `dist/index.js`), pero `pacingMs` NO tiene ningún
  consumidor en `src/*.ts` ni en `dist` (grep: solo definiciones y retornos).
- `index.ts` solo usa `{ model }` del presupuesto; el intervalo se pierde.
- Lo único parecido en el caller es `paceTo(startedAt, 3000)` para respuestas
  de CACHÉ, no para llamadas vivas.
- `rl.on('line', async ...)` (`index.ts:362`) sin serializar: dos `chat`
  seguidos se solapan (`handleMessage` concurrente) → POSTs concurrentes al
  gateway → ráfagas TPM (16k/min) → 429, y carga que favorece 500/503
  transitorios. El harness de R4 sí serializaba+esperaba; Studio no.

## 2. Sin reintento: cada 500/503/429 es fatal (evidencia + doc)

- `openai.ts:110-112`: primer `!resp.ok` → throw. Cero reintentos.
- Doc `api-errors`: `api_error` 500 → "Retry the request"; 503 → backoff;
  `troubleshooting`: los SDK oficiales reintentan 429 y 5xx por defecto.
- R4 observó 503 "high demand ... usually temporary" en C1: con reintento
  habría sido recuperable; en el código actual es error final. Esto NO afirma
  que los 500 selectivos sean todos transitorios; afirma que el cliente no
  distingue transitorio de final y pierde los primeros.

## 3. Compat Google documentada (sin extrapolar a Gemma)

- `temperature` 0.7 + `top_p` 0.8 se envían siempre: en Gemini 4 / 3.6+ se
  ignoran con aviso (400 en el futuro). Para `gemma-4-31b-it` vía
  `v1beta/openai` la guía no documenta el comportamiento → NO se afirma causa;
  se deja como nota de compat (quitarlos es cambio de 2 líneas si el gateway
  lo exige, a criterio de root con 1 llamada de prueba).
- `recitation` (generation blocked) existe como código documentado: un corte
  por recitación deja `text` vacío → cae al camino `runTurn` con 132 KB de
  tools (H3 de `diagnostico.md`), mecanismo documentado, pendiente de 1
  llamada espaciada para confirmar/denegar.
- `models.list` solo valida la clave, no el tier: el `Model: ...` del
  handshake NO prueba inferencia habilitada.

## 4. Harness STDIO preparado (sin llamadas)

`harness_stdio.mjs`: `--revisar` verificado (bundle 564051 bytes, env por
puntero sin imprimir valores, 321209 triples → `harness-revisar.json`).
`--handshake`/`--casos` bloqueados sin `ONTO_ALLOW_CALLS=1`; los ejecuta root.
Casos serializados con espera ≥65s.

## 5. Parche con prueba

`parche-pacing-retry.patch` + `proveedor-retry.mjs` + `test_retry_pacing.mjs`
6/6 offline (500→reintento, 503→reintento, 429+RetryInfo, 400 sin reintento,
pacing en serie, cuerpo recortado). Serie de turnos en `index.ts` incluida.
