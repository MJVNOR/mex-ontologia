# V4-seguridad v004 (final) — V13, V14: acceso no resuelto, sin tarea W pendiente

V001–v003 intactas. Se incorpora el resultado real W-v003 congelado
(F-V003-01-SP-DL, negativo definitivo por estas vías); la rama
"si W trae XLSX" queda cerrada: sin bytes recuperados.

## Resultado W-v003

- Sin descarga en DOM; `download=1` → HTML 26041 B a login oauth2
  (descarga directa exige auth, HTML rechazado como XLSX).
- Token de sesión observado → 302 a `/error/error.html` (no reutilizable).
- Rejilla canvas en `Loading`, 9 controles sin etiqueta.
- Preciso: visor público abre sin login; descarga directa cerrada;
  archivo `DD_SESNSP_Metodologia_Actual` existente. No autenticación
  general, no inexistencia, no más intentos por estas vías.

## Estado

Ambas: **acceso_no_resuelto**, sin tarea W pendiente. Manual RNID V1.0
fuente igual (contexto nacional desde 2026, sin aplicar a 2015–2025).
Ninguna propuesta: F3+F4 sin acreditarse. Reapertura solo fuera de las
vías agotadas (viewer interactivo o copia del publicador + declaración
con edición/corte vinculada a 2015–2025).
