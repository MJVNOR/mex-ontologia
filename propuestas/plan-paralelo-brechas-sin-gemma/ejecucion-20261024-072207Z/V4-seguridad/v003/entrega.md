# V4-seguridad v003 — V13, V14: acceso no resuelto (corrección a v002)

v001 y v002 intactas. v002 decía "requiere auth": falso.
W-v002 congelado verifica apertura **pública sin login** del SharePoint
(visor readonly, `DD_SESNSP_Metodologia_Actual` existente) con rejilla
en `Loading`, 0 tablas DOM y sin bytes. Causa: **representación/descarga
no legible**, no autenticación ni inexistencia.

## Estado

Ambas: **acceso_no_resuelto**. Manual RNID V1.0 distinguido como contexto
(rige reporte desde 2026; sin mención a recursos locales; su "2015-2025"
es ventana de revisión, p. 61). No se aplica RNID-2026 a 2015–2025.
Ninguna propuesta: F3+F4 siguen sin acreditarse.

## Reapertura (dos ramas)

- W `paquete-v003` trae XLSX legible → examinar edición/corte/periodo (v004).
- No lo trae → sigue `acceso_no_resuelto` por representación no legible.
- En ambos casos sigue faltando, salvo ese examen, la declaración del
  publicador con edición/corte SESNSP vinculada a 2015–2025.
