# Evidencia bundle R6: 500 no es cuota (lectura de prueba-bundle/resultado.json)

Fuente: `propuestas/pendientes-muse-r6/prueba-bundle/resultado.json` (solo lectura).
Bundle: `.../sidecars/agent/dist/index.js`, sha `37f19638…` — coincide con el
bundle auditado en `harness-revisar.json` de esta carpeta (mismo binario).
Handshake: `_Connected: 2 ontology tools. Model: gemma-4-31b-it._` (proxy MCP
solo lectura; 2 tools, no 114). Grafo: 321209 antes y despues (conservado).

| caso | retrieval | resultado |
|---|---|---|
| C1-totales | 13 anchors, 20 facts | respondido (4474/20/2) |
| C2-f2-evidencia | 17 anchors, 20 facts | **HTTP 500** `INTERNAL` "Internal error encountered." |
| C3-f2-igualdad | 16 anchors, 82 facts | **HTTP 500** `INTERNAL` idem |
| C4-definicion | 16 anchors, 6 facts | respondido |
| C5-diferencia | 16 anchors, 6 facts | **HTTP 500** `INTERNAL` idem |
| C6-clave-26001 | 16 anchors, 10 facts | **TimeoutError** (abort 90s) |

Lectura:
- Cuerpo 500: `code 500, status INTERNAL`, SIN `QuotaFailure`, SIN `retryDelay`,
  SIN `RetryInfo`. No es 429 de ningun tipo: **500 no es cuota**.
- Espaciado real entre inicios: 65s exactos (18:46:08 → …:53:33). Con trim activo
  (facts ≤82) y ritmo ≥65s, C2/C3/C5 500 igual: el fallo no es tamano global ni
  rafaga del caller en esta corrida.
- C4 (16/6) responde y C5 (16/6) 500 con la misma forma de retrieval: el 500 es
  selectivo por contenido/respuesta del servidor, no por volumen.
- C6 agota los 90s del `AbortSignal.timeout`: segundo modo de fallo (no 500).
- `mutado: false` en los 6: ningun error escribio el grafo.

Consecuencia: D1 (trim por env) NO se aplica como arreglo causal — queda como
robustez documentada. El parche que atiende esta evidencia es el acotado Gemma4
(`codigo/`): 1 reintento 500/502/503 + TimeoutError, QA sin fallback con tools,
errores clasificados servidor/cuota.
