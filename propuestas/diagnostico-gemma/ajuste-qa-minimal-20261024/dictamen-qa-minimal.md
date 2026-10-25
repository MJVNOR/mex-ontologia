# Dictamen independiente: ajuste QA thinking minimal

**Veredicto: aceptar instalación con respaldo. Sin issues P1/P2 de código.**

## Verificado (fuente actual vs respaldo + diffs + marker)

- Respaldo íntegro: `respaldo/manifiesto.json` con SHAs `1bccefb8/5bb7e973/ac193661/ea2f8458`
  == dictamen aplicar; instalado `5b190f2c` intacto (`bundle-instalado.json`).
- SHAs current == `logs/shas-post.json` 5/5 (`bbfc4eb8`, `35b81ab2`, `cb68dc21`,
  `a37788b1` nuevo test, `ea2f8458` inalterado).
- Triple puerta `extra_body` (`providers/openai.ts:258-260,283`): solo con
  `minimalThinking===true` + `tools.length===0` + `usaPoliticaGemma4`.
- Sin fuga: `index.ts:101` (`runTurn`) sin opciones; único solicitante
  `answerOnce` (`index.ts:206`); `anthropic.ts:75`/`claudecli.ts:48` sin cambios
  (parámetro opcional, `types.ts:96`); sin estado compartido (todo por parámetro).
- Reintento conserva la opción (único fetch en el bucle, `openai.ts:223`; test l.72-84).
- Reglas 65 s / 90 s / retry / cooldown, grafo, prompts y modelo intactos (sin hunks).
- Tests del autor: 26/26 QA+Gemma, 49 passed/1 skipped raíz, tsc limpio
  (log vacío; exit declarado, observación menor), build repo 556.7 kb sin tocar instalado.

## Riesgo residual P3 (no bloqueante)

Aceptación del servidor de `extra_body.google.thinking_config` no demostrada
(0 llamadas por diseño; justificación n=1 con confusión de caché documentada en
el propio `listo.json`). Contenido por diseño: un 400 no reintenta y no muta.
Mitigar con instalación con respaldo + 1 sonda QA.
