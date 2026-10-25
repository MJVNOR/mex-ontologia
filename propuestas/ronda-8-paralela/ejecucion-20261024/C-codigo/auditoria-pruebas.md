# Auditoría T-pruebas/v002 — dictamen: aceptar

Solo lectura sobre la propuesta (más subset staging autorizado). Escritura exclusiva en `C-codigo/`. Sin instalar ni modificar `tests/` prod. Sin Gemma/chat, sin Obscura, sin mensajes externos. No se edita al autor; no se espera a I-codigo.

## Dictamen

**aceptar** — 5 archivos aplicables; suite completa en producción luego por coordinador.

## Referencias (SHA-256 programáticos, recalculados con hashlib sobre bytes en disco)

- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_cobertura_integrada.py` `7f68b7f9ea0d6bc9f524e856031b0ec1e73eff929c1bc571badaedfe9d4095e1`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_integracion_agentes.py` `7602dd39d2dcf101e71dee084bfaa7989833e7401df6a46a7b5419bc54c1f4dd`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_2.py` `1f713c659bd628cf384b4253dfabcbd9b59b64f9a6fc041e2255682b23d4f3ac`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_3_integrada.py` `35a1d14d911dc5548dc48aecc4f5afacb29dc1c0bac4aed256237253b953c1fd`
- `propuestas/ronda-8-paralela/ejecucion-20261024/T-pruebas/v002/codigo/tests/test_ronda_7.py` `e3405ba50b87cd75dab323a760b722f0edf9ceb3a9ad674c5f81996463fa659d`
- `congelada.json` entrega `e4ca8fa73b72dc48d0919905d49147832c69df6dcc57a42551508703ed8e1d91`, entrega.md `7563679d9d2e06acc815a06deb0ecd331d6862accfd900a0865224a65633c658`, generador `1c2676a5ba244da559aae70704188956ad994e1f6c75394660d8c03d82e3b312`, congelada.json `606fe69c8972dbc3387c1e7bb0bf320f028e50f108bbd763abc169fe066bebb4`
- Método: `generar-entrega.py` calcula todo por código; nada tipeado a mano. Coincide en disco.

## Verificado

- Subset staging R7: 35 OK (`unittest discover -s .../v002/codigo/tests -t .../v002/codigo/tests`, re-ejecutado).
- Producción 142 / 6 fallos: confirmado en `propuestas/suite-r7-inicial.log` (3 conteos/promociones + 3 revisadas 4478 vs 4475, 1423 vs 1392, 124 vs 152, 16 vs 19; expectativas pre-R7 sin delta R7).
- Aplicación: 4 sobrescriben + `test_ronda_7.py` alta nueva (ausente en `tests/` prod).
- Invariantes históricas preservadas: conteos por overlay, significados por cargar-congelado, revisadas por ancla cruzado con baseline pinnada.
- Sin vivo-contra-sí-mismo: esperados por deltas de manifiesto validado (cadena revisión→manifiesto→SHAs); igualdad exacta sobre era R7 (vivo menos delta R8 validado).
- Sin hardcode observado: `4506` solo en comentarios; aritmética pinnada + deltas.
- R7 sin R8: `ontologia/revision-ronda-8.json` ausente → bloques R8 no-op, verde en era R7.
- R8 solo 28 vínculos: scope `reglas==[]`, `conceptos=={}`, columnas ⊆ `candidatas_nuevas` M1/M2; aritmética 4478+28=4506, candidatas 45=17+28, respaldadas 1423, conceptos 1106.
- Base r7_sha / config base sha256: `base-semantica.json` == `delta.json base_sha256 a30a28…`; interfaz exacta para I-codigo: `R7.cargar/construir/validar_sobre_base`, `REGLA_KEYS/VINCULO_KEYS`, `PARES_20=20`, `UNIVERSO_31=31`, config con `evidencia+manifiesto_sha256`.
- v001 intacta (22 archivos, congelada coincide). Modelo `opencode-go/muse-spark-1.3-contributor`, MCP nativo, casos `[]`, sin Gemma/Obscura/externos en código.

## Archivos aplicables

Los 5 de Referencias, sobre `tests/` (4 sobrescriben, `test_ronda_7.py` alta).

## Siguiente paso (coordinador)

1. Aplicar los 5 archivos. 2. Suite completa en producción (`-s tests -t .`): esperado todo OK en era R7 y tras R8. 3. No tocar congeladas ni I-codigo/scripts/ontologia/data/docs/reports con este pase.
