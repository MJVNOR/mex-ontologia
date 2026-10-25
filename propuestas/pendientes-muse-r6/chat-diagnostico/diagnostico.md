# Diagnóstico: HTTP500 selectivos con Gemma4 31B (chat Studio)

Alcance: solo lectura del repo Studio y del motor vivo; 0 llamadas al modelo;
0 cambios fuera de `propuestas/pendientes-muse-r6/chat-diagnostico/`.
No re-estima trabajo R4/R5: los reutiliza como base y los cita.

## 1. Request schema real (verificado byte a byte, sin red)

`sonda_request.mjs` ejecuta el `OpenAICompatibleProvider.step()` REAL con fetch
stub: el cuerpo del camino QA (`answerOnce`, `index.ts:198-214`, `step([])`) es:

`{model: string, messages: [system, user], temperature: 0.7, top_p: 0.8, max_tokens: 4096}`

- Sin `tools`/`tool_choice` en este camino (claves ausentes, no nulas).
- `chat_template_kwargs` ausente ante host `generativelanguage.googleapis.com`
  (lógica correcta en `openai.ts:105`).
- Clave solo en header `Authorization`; cuerpo sin secretos (`request-schema.json`).
- `QA_SYSTEM_PROMPT`: 4453 caracteres, constante en los 6 casos.

Conclusión schema: los 6 requests difieren ÚNICAMENTE en `messages[1]` (pregunta +
subgrafo). Un 500 selectivo NO puede venir de `tools`, `tool_choice`,
`temperature/top_p` ni `max_tokens`: son idénticos en los 6 casos.

## 2. Diferencia F2 vs C1/C4/C5/C6: el tamaño (medido hoy, motor 321209 triples)

`medir_contextos.mjs` (retrieve real + `asContext` real, solo SELECT):

| caso | con presupuesto (model=gemma-4-31b-it) | sin presupuesto (model ausente) |
|---|---|---|
| C1-totales | 6337 tok est | 15625 tok est |
| C2-f2-evidencia | 6333 | 22778 |
| C3-f2-igualdad | 6353 | **9607** (menor) |
| C4-definicion | 6371 | 42976 |
| C5-diferencia | 6381 | 58695 |
| C6-clave-26001 | 6351 | **139862 (~488 KB)** |

- Con trim: los 6 quedan ~6350 (uniformes) → un 500 selectivo por tamaño es
  IMPOSIBLE en este régimen.
- Sin trim: C3 (único <10k) pasa; C1/C2/C4/C5/C6 (15k→140k) caen. Con el factor
  medido R4 (est→real ×1.43–1.49), C1 ≈ 22–23k reales y C6 ≈ 200k reales.
- El trim solo entra si `retrieve()` recibe `model` (`maybeFit`, `graphrag.ts:573`).
  `index.ts` lo pasa únicamente desde `EFFECTIVE_MODEL = ONTO_LLM_MODEL ?? ''`:
  **sidecar arrancado sin esa variable → trim jamás aplica aunque el request lleve
  un model id válido** (el fallback `/models` de `resolveModel()` resuelve el id
  para el request pero no para el presupuesto). Causa raíz candidata H1.
- Evidencia viva del mecanismo: la sonda `reset` contra el binario real arranca
  con `Model: default` cuando la variable falta (ver `sidecar-protocolo.json`).

## 3. Hipótesis descartadas con evidencia (no por nombre)

- H-contenido (bytes que tumban al gateway): ESCANEO LIMPIO. 0 caracteres de
  control y 0 sustitutos sueltos en los 6 contextos, ambas ramas
  (`medicion.json` → `scan`). No repetir esta línea.
- H-cuota: un HTTP500 no es un 429. El cuerpo del 500 (gateway) y el del 429
  (RESOURCE_EXHAUSTED + RetryInfo) son distinguibles; el parche propuesto
  conserva el status intacto. No culpar cuotas ante 500.
- H-cache (éxito F2 = replay): el sidecar relee `_chat_cache.json` por clave
  `pregunta+contexto+modelo+prompt`. No se encontró caché en el repo Studio
  (`demo/derived/` inexistente); si Studio define `ONTO_CHAT_CACHE` en otro
  cwd, el integrador lo verifica listando claves (sin exponer respuestas).

## 4. Hipótesis secundaria H3 (condicional, pendiente de 1 llamada espaciada)

Si `answerOnce` devuelve vacío (p. ej. respuesta solo-`<thought>` recortada por
`stripThoughtBlocks`), `answerFromGraph` cae a `runTurn(context)` CON las 114
tools: **132666 bytes** de schemas (`tools-schema.json`) + `tool_choice:auto`.
Ese segundo request es de otra liga y puede 500 donde el primero pasó. Solo el
integrador puede confirmarlo (1 llamada espaciada registrando status + camino).

## 5. Parche mínimo + verificación

`parche-propuesto.patch` (2 ficheros, ~15 líneas, sin cambio de modelo):
1. `index.ts`: resolver el id vía `describe()` una vez si `ONTO_LLM_MODEL` falta,
   para que el trim ya instalado siempre aplique.
2. `openai.ts`: recortar el cuerpo del error a 2000 chars (status intacto).
Verificación (integrador): arranque `Model: gemma-4-31b-it`, repetir C3+C6
espaciados; si C6 500 persiste con trim activo, escalar con status+cuerpo.

## 6. Sidecar JSON-RPC health/model.status/message

NO admitidos: la auditoría estática de `index.ts` prueba que la entrada solo
entiende `chat` y `reset` (salidas: `text/error/tool_call/progress/retrieval/
done/ready/reset_done`). No se inventó prueba para lo inexistente; la prueba
viva cubre `reset` contra `dist/index.js` real: `ready` → `reset_done` OK, sin
modelo y sin mutar el grafo (`sidecar-protocolo.json`).
