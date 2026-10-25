# Auditoría io-atomico/v001 — dictamen: aceptar

Solo lectura + 3 tests staging (dirs TMP). Sin editar ni instalar. Sin Gemma/externos. Sin reiniciar Studio/Gemma. Suite 179 + portal serial: coordinador tras instalar.

## Causa (real)

`portal-r8-v002.log`: `OSError 22` al truncar `cobertura.json` en `consolidar_semantica.generar()` (Windows, archivo abierto/mapeado). Precedente válido: reemplazo atómico idéntico para portal-completo tras WinError 5 funcionó.

## Delta (mínimo)

- `guardar_rdf.py` +18: `escribir_json_atomico(value, destination)` — espejo de `serializar_atomico`: tempfile en mismo dir, cerrar, `os.replace`, cleanup en `finally`.
- `consolidar_semantica.py`: +1 import, 2 swaps (`verificacion.json`, `cobertura.json`). Sin tocar core/gates/RDF.
- Si `os.replace` falla por bloqueo: tmp limpio, previo intacto, excepción visible (no se oculta).
- Menor: `cobertura.json` gana `\n` final (como ya tenía `verificacion.json`); `json.loads` idéntico.

## Referencias (SHA-256 programáticos)

- `io-atomico/v001/scripts/guardar_rdf.py` `939dd5ece81a2236c6c3a18d09b1bc3b9a12114b73b96ee3744ae5eebda755ab`
- `io-atomico/v001/scripts/consolidar_semantica.py` `2a2e79d1b54ba393c05b913055cff0ec488bb22fcf4554e5ba541707c442d2f8`
- `io-atomico/v001/tests/test_guardar_json.py` `9583b5f6a49b289db05cfe1fec131970c09826473d831ff58d3b0facd56df9de`
- Sello `io-atomico/v001/congelada.json` `59cece29bcd74258ba09f3914f5185cfcfc3d534a3c16964a99ab4d8942b02f0` (4/4 OK).

## Staging

3/3 OK (léxico, TypeError conserva previo, PermissionError conserva previo).

## Aplicar

Sobrescribir los 2 scripts (el test es evidencia, no se instala); luego suite + portal serial.
