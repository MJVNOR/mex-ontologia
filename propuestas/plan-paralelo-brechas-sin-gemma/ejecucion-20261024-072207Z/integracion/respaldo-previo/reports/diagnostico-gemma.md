# Diagnóstico Gemma 4 31B — cierre 2026-10-24

## Hallazgos (evidencia en `propuestas/diagnostico-gemma/`)

1. **Ambos endpoints responden 200** al mismo `gemma-4-31b-it`: OpenAI-compatible
   `.../v1beta/openai/chat/completions` (req1, 12.76 s) y nativo
   `models/gemma-4-31b-it:generateContent` (req2, 9.97 s).
2. **Reasoning activo por defecto**: con límites de 8 tokens el thinking consume
   todo el presupuesto (`finish_reason` length/MAX_TOKENS, solo thought visible).
   Con thinking minimal el mismo endpoint devuelve el texto (`"OK"`, req3, 23.75 s).
3. **C6 real** (system 4453 + user 17673 chars = 22126/22189 bytes): con el código
   original, **TimeoutError local de fetch a los 90 s** por intento (A, 90.09 s,
   `status:null`). 360 s era el **cap de la sonda por caso**, no un timeout observado.
4. Mismo C6 + `thinking_config minimal` (externo): **200/stop en 51.56 s**,
   **9054 input / 606 output**, `sha messages` idéntico al A.
5. El primer B se perdió por bug local de guardado (cp1252); **1 recuperación B
   autorizada y declarada**; presupuesto de requests respetado.
6. **n=1 + 8181 prompt tokens cacheados en B (confusor): NO hay causalidad
   probada** del thinking minimal; tampoco 500/503 con causa establecida ni
   cuota agotada demostrada.
7. **Sonda instalada** (bundle `3c54dcb4…`, handshake `gemma-4-31b-it`):
   `C6-clave-26001` **respondido**: 05:43:18.042Z → 05:45:12.779Z = **~114.7 s
   totales (incluye retrieval/pacing/posible retry; NO es tiempo de un fetch
   ni se afirma 1 intento — sin traza de intentos)**. 1005 chars, `errores:[]`,
   `mutado:false`, grafo **321210 = 321210**. Hechos: 2594/2594, medidas
   `suma_grupos_edad_H_M` (filas 62 H/63 M) y `poblacion_mitad_ano` (fila 32),
   archivos `24301617….xlsx` y `e0e21aad….xlsx`, origen Aconchi; **sin
   afirmación INEGI** (el grafo no la acredita). No confundir con el B externo
   (51.56 s, solicitud HTTP directa con los mismos mensajes capturados).
8. **Conteo requests**: 6 diagnósticos antes de instalar
   (req1/req2/req3/A-timeout/B-perdido/B-recuperación) + sonda instalada de
   1 caso con retry máximo 1 de código; **conteo HTTP real no instrumentado**.
   1 caso respondido **no declara fiabilidad global**; 500/503 sin causa
   establecida; sin cuota agotada demostrada.

## Cambio aplicado (QA-only, modelo intacto)

`provider.step(tools, options?: TurnOptions)`; solo `answerOnce` solicita
`{minimalThinking:true}`; triple puerta (opción + tools vacías +
`usaPoliticaGemma4`) agrega
`extra_body.google.thinking_config={thinking_level:'minimal',include_thoughts:false}`.
Sin estado compartido; el retry lo conserva por parámetro; otros providers
ignoran la opción. Sin cambios de grafo/manifiestos/`.env`/prompts/modelo.

## Verificación, revisión y respaldos

- Tests: **26/26** (21+5 nuevas) · raíz **49 passed/1 skipped** · tsc exit 0 ·
  build esbuild 556.7 kb (solo `dist/` del repo).
- Revisión independiente: `dictamen-qa-minimal.json`
  (**aceptar-instalacion-con-respaldo**); SHAs actuales == marker == dictamen.
- Respaldo fuente+bundle previo en `ajuste-qa-minimal-20261024/respaldo/`;
  instalado anterior `5b190f2c…` en `instalacion/`; nuevo instalado `3c54dcb4…`.
- Reinicio: `reiniciar-studio.ps1` falló en `Get-FileHash` (no reconocido en
  este shell) tras guardar el grafo; mismo procedimiento completado con hash
  python. Respaldo TTL 41 MB, copia canónica verificada, Studio relanzado con
  `gemma-4-31b-it`, grafo 321210 conservado.

## Corrección a informes previos (sin alterar evidencia original)

Se corrigieron `reports/aplicacion-chat.md` y `.json`, con respaldos previos en
`propuestas/diagnostico-gemma/aplicacion-chat.*.respaldo-20261024`. Las sondas
originales se conservan. 360 s era el cap de la sonda; el proveedor limita cada
fetch a 90 s. C6 original duró 266,6 s en total y devolvió `TimeoutError` sin
contador de intentos; el crudo no permite afirmar cuántos intentos hizo.

Fuentes oficiales: <https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api>
· <https://ai.google.dev/gemini-api/docs/openai>
