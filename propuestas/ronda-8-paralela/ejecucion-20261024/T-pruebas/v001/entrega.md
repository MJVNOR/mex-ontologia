# T-pruebas v001 — suite R7

Fecha UTC: 2026-10-24T08:48:55.407784+00:00
Modelo: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, sin Obscura, sin contactos externos.

## Casos asignados

Asignación con `casos: []`: cero ids, cero decisiones (una decisión exacta por cada id asignado).

## Afirmación exacta acotada

Los 6 fallos de propuestas/suite-r7-inicial.log (142 pruebas) se deben a expectativas pre-R7 que no contemplan el delta aprobado R7 (31 significados + 3 vínculos; 1392+31=1423 respaldadas, 152-28=124 fuera, 19-3=16 candidatas, 4475+3=4478 revisadas). Producción verifica íntegro (manifiestos, doble auditoría A+B con aceptadas_sha256 pinnado, base exacta, materialización fiel): no se propone ningún cambio en scripts/tests/ontologia/data. Se proponen copias corregidas de los 4 tests con expectativas derivadas de manifiestos (sin hardcodear conteos observados) + test_ronda_7.py (12 pruebas: integridad, aprobación SHA, base exacta, deltas cruzados, materialización, scope, 4 negativas, gancho R8). Staging: 154 pruebas OK.

## Pruebas verificables

- Staging: `uv run python -m unittest discover -s propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests -t propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests` → 154 pruebas OK.
- Producción solo leída; nada instalado ni modificado fuera de `T-pruebas/`.

## Diagnóstico de los 6 fallos iniciales

- test_cobertura_integrada (3): conteos/promociones calculan solo deltas R4/R5; faltan R6 (sin reglas, verificado) y R7 (28 fuera + 3 candidatas -> respaldadas, estados previos derivados de base post-R4 salvo promoción R4/R5).
- test_integracion_agentes/test_ronda_2/test_ronda_3_integrada (3): esperados de revisadas suman solo r6n; falta r7n derivado de aceptadas.json validado (4475+3=4478).
- Causa común: suite anterior a R7. reports/ronda-7.md ya anticipa adaptadores de conteos; producción íntegra, tests desactualizados.

## Instrucciones de aplicación

- 1. Auditar esta v001 con dos revisores independientes (código + pruebas).
- 2. Tras aprobar: copiar v001/codigo/tests/test_cobertura_integrada.py, test_integracion_agentes.py, test_ronda_2.py y test_ronda_3_integrada.py sobre tests/ (sobrescriben expectativas; aserciones históricas preservadas).
- 3. Añadir v001/codigo/tests/test_ronda_7.py como tests/test_ronda_7.py (alta nueva, sin colisiones).
- 4. El resto de copias son idénticas a producción salvo resolución de raíz por marcador (equivalente en ubicación final); no requieren copia.
- 5. Verificar: uv run python -m unittest discover -s tests -t . (esperado: todo OK).
- 6. No instalar ni modificar scripts/, ontologia/, data/, docs/ ni reports/ con este pase.

## Archivos de código (SHA-256 calculados por `generar-entrega.py`)

- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_calificadores.py` `4acbdc9f0cce59afa8f3ff9eeecf4fd558d3bb5dbe4cec298c7e3e49b2cde7f9`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_catalogo.py` `bc37d88f7b7cc8c23d8de9e7ffdb3de1bf88f356bdd007644d89bb509a228583`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_cobertura_evidencia.py` `2cd2f5d3b39c7e80cc0cdcc4682ab7dee07baef2311f55efa451fc11363e7422`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_cobertura_integrada.py` `440cc77bf82ebe9a3839198a416755cc2e9cc39e3d2a42348b9a3ab4575e8a0b`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_contenido.py` `f3760e63dea5fc79f837bb385ebaa65536b3508faeda182196a05f96e4f6e492`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_dictamen_historico.py` `0dc59b3791f6182d7e64a2f39a8ca8ef315dd671cd90b8a60c0ca910f4729963`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_guardar_rdf.py` `c60d5ad9ace5a5b58ca329ed2a1d76cc73b957d70bcad939f992113ddcf71338`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_integracion_agentes.py` `68f90c0314c96b01d6b4365c2b462b1169ad7eb160e0eae541c21cc0ef80629a`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_inventario.py` `24fe2c19267d5c242aef28b7cfa5d00b124d783bbd5456721f358e47a700485a`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_lote.py` `ea86f4cb58cfec5aba06c6fc837adf25436ca52809de807f369ad0d15739b233`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_oportunidades.py` `5bfb8414ca5fdcd94fc6b89af0c663adad3942850b0b5243786c5cb2d1a61167`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_portal.py` `9f344d6bc1c70ed9a1b7b96f5a48cf0dfdda3ba901f190d7688800a4a3cc2cb7`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_2.py` `6879daf92bc7fd74a987571c1499fd1ef0fc8de1ad7cabbea203e0083b36665c`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_3_integrada.py` `c54c0c5541a7a8cb8fa3dc41b0c9820e6a58044606cc763aadbee17f0addb1a2`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_4.py` `716b58c3381aae253b2a20ca1d834f284c8a6e71f76fa8f0f88fc369afcd86c3`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_5.py` `4e20a49c2bcd2f3cf96027c2b4cf9249e64638cc9b614c3f02c5e46632f46c16`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_6.py` `7422f63b15b2cc9a95f35e452f3329b6559489ebc2a8bab93a6f63de006b7717`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_ronda_7.py` `14e78033205645af994449c43669750947d108bac980b98d8f30a4f945eaa4c7`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_seleccion_documental.py` `0a1623ca6a2478f63dba00fe805c0430c308f643b920955aa059e397801af387`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_semantica.py` `8de204db04c993f535b77563b4adcdc1dce3aca85f9185d2c07650c8336479a0`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_sync_cadenas.py` `1c666d70332e078d21423dba43634b7806c793eec42cbee972c0e9b6ac6a6f9c`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v001/codigo/tests/test_territorio.py` `754e2603ad9c5f59a4aa39f59e2d4994d80c202b8687da01ceef34e43f81cbb0`

## Base leída (punto de partida R7)

- `ontologia/semantica.json` `f6b6754555d97f929658f94e34461320d27e7db26c4d84b1e313a46af4323366`
- `data/semantica/cobertura.json` `c1585ad942935b06917d62cb98d3c7bf3799ee524c3a7f13586a693ec053ecd2`
- `ontologia/revision-ronda-7.json` `c061e436e9675b0d1156a490bc6b954bee1af85ac69e8a6021631d6444547e00`
- `data/integracion-ronda-7/manifiesto.json` `7b5d242feeaf23bd6f54f44b6314e8afb829a88fd1ee9bb5a70807c900cf7a55`
- `data/integracion-ronda-7/aceptadas.json` `0d58255de0ecf9b417c3a7d70439b22c11b16c6628334203f30fa40f37ef7684`
- `data/integracion-ronda-7/delta.json` `f4143ffec283adc6315015eba44dfc2e3124b1fa640a422270beb00af3757f70`
- `reports/ronda-7.json` `197054973a25496ed30b393c566b689e43d6cf46d012f79e644cb0521a32d787`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/asignacion.json` `e77cbcea5d06d776efd4c81e8219b234608858cded63c460e739e3fdb23e1c7a`

## Gancho R8

Expectativas por deltas aprobados de manifiestos (aceptadas.json validados), nunca vivo contra sí mismo. Si R8 añade reglas/vínculos (28 vínculos previstos), extender el mismo patrón con integrar_ronda_8; test_r8_hook_por_deltas_aprobados falla a propósito hasta entonces.
