# Resultado instalación — fase 2 gemma-real (presupuesto 6500 + strip thought)

Medición del integrador (`integrador/gemma-real/respuestas.json`, solo metadatos, sin publicar razonamiento): 9845 est → 14072 prompt_tokens reales (×1.43); 9607 est → 14279 reales (×1.49); C1/C4-C5 HTTP 500 externo; C2 HTTP 200 con bloque `<thought>` + final truncada; C3 solo thought sin final (0 completion, max_salida 1200). Conclusión: 10000 estimados ≈ 14300 reales, demasiado cerca de 16K TPM → presupuesto estimado 6500 (≈9300 reales + 4096 salida < 16000).

Cambios aplicados al repo (`open-ontologies/studio/src-tauri/sidecars/agent`, con backup+SHA):
- `graphrag.ts`: presupuesto Gemma 10000→6500 con nota del factor medido.
- `providers/openai.ts`: solo helper puro exportado `stripThoughtBlocks` (cerrados/incompletos, `<thought>`/`<think>`); `step`, tool_calls y `thought_signature` intactos; otros proveedores sin tocar.
- `index.ts`: `answerOnce` filtra el texto final; si queda vacío no se afirma ni se cachea (los `if` ya existentes lo garantizan).
- `openai.test.ts`: 5 casos sintéticos nuevos (sin reasoning real).

Verificación: repo vitest 49 passed/1 skipped (44 previos + 5 nuevos); mis suites REGRESION/FICHAS/PRESUPUESTO/RECORTE OK (6/6 ≤6500 est, sin truncar, sin prohibidos); harness 6/6 con C1 dinámico (4466/72/144 vivos), 0 llamadas, grafo intacto.

Bundle instalado en la instalación efectiva Codex (`.../open-ontologies-studio/sidecars/agent/dist/index.js`, exe idéntico al release, `package.json` main=dist/index.js): `c1d2ac0e…` → `37f19638…` (= build fresco con parche+strip), backup incremental `dist-index.js.codex-instalado.pre6500.orig` + SHA. Árbol `target/release` sincronizado al mismo build (no es la instalación efectiva). Sin reiniciar (prueba espaciada de root en curso); sin tocar proceso/engine/UI/grafo/.env.

Reporte honesto: 429 = cuota por minuto (TPM 13.08K/16K, RPM 1/30, RPD 1/14.4K); causalidad por llamadas sucesivas = hipótesis compatible, NO probada solo con el dashboard; C4/C5 con 1401/1508 est también dieron 500 externo; sin cuota diaria (RPD 1/14.4K); tokens siempre ESTIMADOS salvo `prompt_tokens`/`completion_tokens` del informe del integrador. Entrega congelada intacta.
