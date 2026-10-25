# Auditoría io-atomico/v002 — dictamen: aceptar

Solo lectura + 5 tests staging (TMP, sleeps simulados). Sin editar ni instalar. Sin Gemma/externos/kill. Suite 181 + portal serial: coordinador después.

## Causa (real)

`portal-r8-v003.log`: `PermissionError WinError 5` en `os.replace` tmp → `portal-completo.ttl`. Bloqueo intermitente de lector; reemplazo idéntico rápido sí funcionó antes.

## Delta (mínimo, solo `guardar_rdf.py`)

- +`import time`, 2 swaps (`serializar_atomico` y `escribir_json_atomico`) a `_reemplazar_con_reintentos`.
- Helper +13 líneas: 10 intentos / 9 pausas (0.05…16, total 31.9 s) **solo** winerror 5/32/1224; resto inmediato; al agotar relanza.
- Sin fallback silencioso (retorna o relanza), sin truncate (destino jamás abierto en escritura), previo siempre conservado + tmp limpio.

## Referencias (SHA-256 programáticos)

- `io-atomico/v002/scripts/guardar_rdf.py` `90400803bd56491e9cf7f22711a1f17f3e0b614d41b21db1a8aa1d1bdd9e88ce`
- `io-atomico/v002/tests/test_guardar_json.py` `3146da2bc3b4182d58fdd1b0771ff3372761089c661f70750647935b54d04f33`
- Sello `io-atomico/v002/congelada.json` `9e3dcb28c8ba1ccdbb9059ca74aaec3e96fd3136340fb009a8c6fe1bfb587271` (2/2 OK).

## Staging

5/5 OK (3 previos + transitorio con éxito real + persistente acotado que conserva).

## Aplicar

Sobrescribir `scripts/guardar_rdf.py` (consolidar sin cambios en v002; test es evidencia); luego suite + portal serial.
