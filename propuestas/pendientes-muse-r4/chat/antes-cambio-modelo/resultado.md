# Resultado de la evaluacion real del chat (ronda 4)

Fecha: 2026-10-23T17:04:53.156Z | Modelo configurado: gemini-3.5-flash | Triples final: 284810

## Que invoca el harness (no es E2E)

`ejecutar_chat.mjs` reutiliza los modulos del sidecar — `retrieve`/`asContext`/`QA_SYSTEM_PROMPT`
de `graphrag.ts` y `OpenAICompatibleProvider` de `providers/openai.ts` — con un cliente MCP
minimo sobre `/api/query` del motor vivo. NO invoca el binario sidecar completo
(`sidecars/agent/dist/index.js`) ni la UI de Studio. No etiquetar E2E.

## Llamadas al modelo (6 intentos, 2 respuestas)

- Respuestas reales: 2 — C2-f2-evidencia (falla_oraculo) y C3-f2-igualdad (probado).
- Error 503 demanda transitoria: 1 — C1-totales.
- Error 429 cuota diaria Free Tier (~14h): 3 — C4, C5, C6.
- Sin reintentos identicos ni cambio de modelo/proveedor. Sin mas llamadas tras el 429.

## Conteos

- Casos totales: 6
- Chat probado: 1 (C3: igualdad F2 solo-2020, limites correctos, cita fichas y SHA)
- Falla de oraculo con respuesta real: 1 (C2: etiqueta "F2" sin anclaje en recuperacion; el modelo respondio honestamente que no hallo evidencia F2, sin alucinar)
- Bloqueados: 4 (1×503, 3×429), recuperacion real registrada en todos ellos
- Grafo sin cambios en todos los casos: true (284810 antes y despues)

## Capas

- sidecar/API (modulos reutilizados): ejecutada.
- studio-ui: no_ejecutada como prueba de chat — UI LEIDA (estado) pero pregunta NO enviada
  (ver `adenda-ui.json`): el integrador confirmo con @oai/sky del node_repl raiz la ventana
  com.fabio.open-ontologies-studio id 14622614 viva (284810 triples, gemini-3.5-flash, campo
  Ask y Send presentes); el foco por indice 132 fallo por ventana minimizada y no se escribio
  ni envio nada. En este entorno OpenCode @oai/sky no existe (import verificado fallido);
  limitacion del entorno, no del helper raiz. Guarda de actividad respetada sin evadir.

## Base verificada (solo lectura)

- 865 revisadas, 72 comparaciones F2 solo-2020, 144 evidencias: verificados en vivo (oraculo.py).
- 940 conceptos (ontologia/semantica.json), 1212 significados (reports/cobertura-muse.json).

## Reproducibilidad

- Harness: propuestas/pendientes-muse-r4/chat/ejecutar_chat.mjs + corpus.json.
- Repetir con conteos finales tras la ventana de cuota; mismo comando, sin cambiar modelo.
- studio-ui queda para ejecucion con helper raiz (ventana restaurada) o registro manual.
