# Auditoría ajuste-tests/v001 — dictamen: aceptar

Estática + 2 tests en staging. Sin editar ni instalar. Sin Gemma/externos. Suite completa final: coordinador.

## Causa (legítima)

Cadena vigente R4→R8: `integrar_ronda_7` delega a `validar_ronda_8`, que exige base + 28 vínculos exactos. Los 2 ERROR de `suite-r8-v001.log` (176 tests) pasan la foto era-R7 (`_reglas_era_r7` = vivo menos delta R8) y R8 la rechaza con causa: `Ronda 8 permite solo la base y los 28 vinculos auditados exactos`. Resto 174/176 OK incl. 9 regresiones R8. Producción confirma R8: 4506 revisadas / 17 candidatas / 1423-124-16 / 1106.

## Delta (exacto, 2 calls)

- `test_ronda_3_integrada.py`: `validar_extension_vinculos(_reglas_era_r7(self.rules),…)` → `(self.rules,…)` + comentario.
- `test_ronda_7.py`: `R7.construir(…, _reglas_era_r7(self.rules), …)` → `(…, self.rules, …)` + comentario.
- Aserciones 836+29 (`865`+deltas) y PROV (`wasDerivedFrom/sha256Evidencia/type`) intactas; cores sin suavizar; nada borrado; helpers retenidos.

## Referencias (SHA-256 programáticos)

- `ajuste-tests/v001/test_ronda_3_integrada.py` `92d823b84afaa2258887fbcd9f7960b68f56368bea3c22bbf9db3f18f198b706`
- `ajuste-tests/v001/test_ronda_7.py` `c618740d3ed6278cfc15c5064d040b7807e36649ef0bfda4b76bd6dbca6c08f2`
- Sello `ajuste-tests/v001/congelada.json` `674e16a33061c85cc314fe325098fcef8b63001802805b0d357ca3e9fef8d8af` (2/2 OK).

## Staging

2/2 OK (`test_extension_exacta_836_mas_29` + `test_construir_emite_solo_procedencia`, root finder OK, R8 presente).

## Aplicar

Sobrescribir `tests/test_ronda_3_integrada.py` y `tests/test_ronda_7.py`; luego suite completa (esperado 176 OK).
