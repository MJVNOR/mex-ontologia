# Adenda técnica v003 — Excel SESNSP: `acceso_no_resuelto` (2026-10-24)

Fecha: 2026-10-24. Actualización real: 2026-10-24T07:40:24+00:00.
Paquetes v001/v002 intactos. Sin login, sin credenciales, sin endpoints inventados.

## Intentos concretos (todos sobre el enlace observado o su network log)

1. `browser_links` en el visor → `No links found` (sin opción de descarga en DOM).
2. URL observada + `&download=1` → HTTP 200 `text/html` 26041 B con URL efectiva
   `login.microsoftonline.com/.../oauth2/authorize`. HTML rechazado: es login, no XLSX.
3. `browser_network_requests` → `GetContentBundle` observado (200, 197420 B en navegador)
   con `bundleUrl` al stream `content_preview_O{0}` con `tempauth` (exp 1792863545).
4. GET de ese bundle por HTTP → HTTP 302 a `/error/error.html` (token de sesión, solo navegador).
5. Rejilla canvas: `innerText` 39 chars (`Loading...`), 9 controles sin etiqueta;
   sin herramienta de descarga en Obscura; clic a ciegas no justificado.

## Cierre

`acceso_no_resuelto` para la copia XLSX por estas vías. **No** se atribuye a
autenticación en general: el visor público abre sin login (v002); lo cerrado es la
descarga directa y la reutilización del token de sesión.

**Notificación V4**: XLSX **no** recuperable por estas vías. V4 mantiene F-W01/F-V002-01
(manual RNID + nombre `DD_SESNSP_Metodología_Actual` verificado). Sin dato resolutivo nuevo.
