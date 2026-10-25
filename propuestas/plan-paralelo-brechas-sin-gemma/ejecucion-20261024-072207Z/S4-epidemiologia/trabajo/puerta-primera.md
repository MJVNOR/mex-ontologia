# S4-epidemiología — puerta primera (2026-10-24)

25 IDs. Verificación con herramientas independientes (webfetch/websearch + bytes locales). Obscura no tocado (solo W-web).

## Comprobaciones del día

1. `package_show` en vivo (webfetch, 2026-10-24): `metadata_modified=2025-08-19T16:50:42.517487`, `version=null`, `fuentes_extras=''`, 2 recursos sin cambios. **Sin cambio de fuente.** No se guardó copia local (GET directa da 403 Cloudflare desde este entorno); valores citados como observación, no como fuente de bytes.
2. `package_revision_list` API: 400. El activity stream solo es visible en página renderizada → petición WEB-S4-01 a W-web (pendiente).
3. Índice web del CSV del diccionario: reproduce las mismas 59 descripciones ya documentadas (`Clave`, `Acumulados`, `Total ... entre 1 y 5 años`, 22× `Pendiente de especificar`). Confirma evidencia previa, no aporta instrumento nuevo.
4. `DefinicionesOperacionales_Padecimientos_Sujetos_a_VE.pdf` (DGE, mar-2021): no examinado antes, pero es referente nacional genérico (146 padecimientos + CIE-10) sin vínculo a conjunto/recurso/edición/periodo local. Descargarlo repetiría la línea genérica ya agotada (manual SUIVE-32 + formato SUIVE-1 2021, F-SUIVE-01); no puede fijar objeto de `cve_cie10`, regla de `acumulado`, intervalo `de01_a_04`, convención del sufijo `f`, ni las 22 descripciones pendientes. Se registra como evaluado y descartado, no como pista.
5. SHAs de las 5 evidencias previas re-verificados desde bytes: idénticos a los citados en asignación.

## Clasificación por ID

Los 25 IDs: `sin_pista_nueva` → `brecha_externa`. Ninguno admite `documental_revisada`: las descripciones del diccionario local (`Clave`, `Acumulados`, `entre 1 y 5 años`) no son definiciones respaldadas con vínculo campo/recurso/edición, y los 22 `Pendiente de especificar` carecen de definición. No se aplica CIE por homonimia.

Petición WEB-S4-01 pendiente en `peticiones-web.json`. Si W-web aporta diccionario corregido o nota del publicador, se reabre por adenda/v002.
