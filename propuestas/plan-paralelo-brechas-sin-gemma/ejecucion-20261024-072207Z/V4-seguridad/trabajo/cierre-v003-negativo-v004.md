# Cierre V13/V14 con W-v003 negativo definitivo (trabajo v004)

Resultado real incorporado: `W-web/paquete-v003/fuentes-v003.json`
(F-V003-01-SP-DL, 2026-10-24, congelada-v003 verificada). Sin búsquedas
nuevas, sin navegador repetido, sin tocar otras carpetas.

## Intento final W: qué se probó y qué dio

1. `browser_links` en el visor: "No links found" (sin opción de descarga en DOM).
2. GET con `&download=1`: HTTP 200 text/html 26041 B con URL efectiva
   `login.microsoftonline.com .../oauth2/authorize` → la descarga directa
   exige auth; HTML rechazado como XLSX (no se acepta HTML por XLSX).
3. `network_requests`: GetContentBundle 200 (197420 B en navegador) con
   bundleUrl `.../items/01PQ.../streams/content_preview_O{0}/streamContent?tempauth=v1...`
   (token exp 1792863545); GET del bundle por HTTP → 302 a `/error/error.html`
   (tempauth ligado a sesión del navegador, no reutilizable).
4. Rejilla canvas: innerText 39 chars "Loading...", 9 controles sin etiqueta;
   sin herramienta de descarga en Obscura.

## Cierre preciso (sin generalizar)

- El visor público abre sin login (v002): no hay barrera de autenticación
  en general ni inexistencia del archivo (`DD_SESNSP_Metodologia_Actual`
  verificado existente).
- Lo cerrado: la descarga directa del archivo y la reutilización del token
  de sesión por estas vías. No más intentos por estas vías (W lo declara
  definitivo; V4 no pide otros).
- Reapertura restante (fuera de estas vías): interacción con el viewer
  (Excel online) o copia del publicador; más la declaración del publicador
  con edición/corte SESNSP vinculada a 2015–2025, que sigue faltando.
- Manual RNID V1.0: fuente igual, contexto metodológico nacional
  (rige desde 2026), sin aplicar a 2015–2025. Sin propuesta: F3+F4
  sin acreditarse en ambos IDs.
