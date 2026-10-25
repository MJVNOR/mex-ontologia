# T-pruebas v002 — suite compatible R8

Fecha UTC: 2026-10-24T08:53:32.999387+00:00
Modelo: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, sin Obscura, sin contactos externos. v001 preservada y congelada.

## Casos asignados

Asignación con `casos: []`: cero ids, cero decisiones.

## Afirmación exacta acotada

v002 preserva v001 y hace los 5 tests finales compatibles con R8 (28 vínculos M1/M2, 0 reglas, 0 conceptos) por deltas aceptados validados (cadena revision→manifiesto→SHAs, sin importar ni diseñar integrador) y baseline R7 pinnada (base_sha256 verificado), sin hardcodear 4506 ni comparar el vivo consigo mismo. Revisadas = base pinnada + deltas R7+R8; candidatas = 17 + 28 − promovidas R8. Validadores de igualdad exacta R4→R7 corren sobre era R7 (vivo menos delta R8 validado). Scope R7, doble aprobación A+B y negativas intactos. Subset staging en R7: 35 OK.

## Pruebas verificables

- Subset staging: `uv run python -m unittest discover -s propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests -t propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests` → 35 pruebas OK.
- Producción solo leída; nada instalado ni modificado fuera de `T-pruebas/v002/`.

## Cambios frente a v001

- Helper _aceptadas_ronda(n) por deltas validados (reemplaza vía R8 sin integrador).
- test_conteos: estados previos desde base de cobertura + overlay de promociones; bucle R8 general.
- test_significados/condicionados: cargar congelado en vez de validar vivo; promociones R8 no-op.
- Revisadas: + r8n validado en agentes/ronda_2/ronda_3/test_ronda_7; ancla cruzado con baseline pinnada.
- test_ronda_3: validador histórico sobre era R7.
- test_ronda_7: exactitud por aritmética pinnada; candidatas descuentan R8; scope R8 solo-vínculos; construir sobre era; hook sustituido por test real (verde antes y después de instalar R8).

## Instrucciones de aplicación

- 1. Auditar esta v002 con dos revisores independientes (código + pruebas).
- 2. Tras aprobar, aplicar sobre tests/ los 5 archivos finales de v002/codigo/tests/ (4 sobrescriben a v001 ya aplicada o a producción pre-R7; test_ronda_7.py es alta).
- 3. Al instalar R8 (config + manifiesto + aceptadas + regeneración), la suite debe seguir en verde sin tocar tests: los bloques R8 se activan solos por deltas validados.
- 4. Verificar en era R7 y tras R8: uv run python -m unittest discover -s tests -t <dir-tests>.
- 5. No editar v001 (congelada), I-codigo/, scripts/, ontologia/, data/, docs/ ni reports/ con este pase.

## Archivos de código (SHA-256 programáticos)

- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_cobertura_integrada.py` `7f68b7f9ea0d6bc9f524e856031b0ec1e73eff929c1bc571badaedfe9d4095e1`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_integracion_agentes.py` `7602dd39d2dcf101e71dee084bfaa7989833e7401df6a46a7b5419bc54c1f4dd`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_2.py` `1f713c659bd628cf384b4253dfabcbd9b59b64f9a6fc041e2255682b23d4f3ac`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_3_integrada.py` `35a1d14d911dc5548dc48aecc4f5afacb29dc1c0bac4aed256237253b953c1fd`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_7.py` `e3405ba50b87cd75dab323a760b722f0edf9ceb3a9ad674c5f81996463fa659d`

## Base leída

- `ontologia/semantica.json` `f6b6754555d97f929658f94e34461320d27e7db26c4d84b1e313a46af4323366`
- `data/semantica/cobertura.json` `c1585ad942935b06917d62cb98d3c7bf3799ee524c3a7f13586a693ec053ecd2`
- `ontologia/revision-ronda-7.json` `c061e436e9675b0d1156a490bc6b954bee1af85ac69e8a6021631d6444547e00`
- `data/integracion-ronda-7/manifiesto.json` `7b5d242feeaf23bd6f54f44b6314e8afb829a88fd1ee9bb5a70807c900cf7a55`
- `data/integracion-ronda-7/aceptadas.json` `0d58255de0ecf9b417c3a7d70439b22c11b16c6628334203f30fa40f37ef7684`
- `data/integracion-ronda-7/delta.json` `f4143ffec283adc6315015eba44dfc2e3124b1fa640a422270beb00af3757f70`
- `data/integracion-ronda-7/base-semantica.json` `a30a2842d10699a1a78ddeae6121dad42b2166af1cd9aac6a5ed52f047fc68ca`
- `reports/ronda-7.json` `197054973a25496ed30b393c566b689e43d6cf46d012f79e644cb0521a32d787`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/asignacion.json` `e77cbcea5d06d776efd4c81e8219b234608858cded63c460e739e3fdb23e1c7a`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/congelada.json` `a7248aa6d4c3bd50915eafd56e62a9c5a0da555427febeb3f5ab656e73b2a5bf`
