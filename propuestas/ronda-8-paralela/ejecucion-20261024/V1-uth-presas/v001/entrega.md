# V1-uth-presas — entrega v001 (2026-10-24)

Rol: vigencias UTH + presas. 5 casos, 0 propuestas para auditar, 5 brechas externas.

## Decisiones

| id | estado | motivo resumido |
|----|--------|-----------------|
| V01 | brecha_externa | F3 acreditada (CMPE 2016). F4 ausente: sin documento UTH que vincule CMPE 2016 + recurso 6d561451 + cuatrimestres 2022-2026. |
| V02 | brecha_externa | F3 acreditada. F4 ausente: nota del conjunto sin edicion ni adopcion CMPE 2022-2026 (recurso aaf0c6c1). |
| V03 | brecha_externa | F3 acreditada. F4 ausente: sin vinculo CMPE 2016 + anuales 2022-2025 (recurso 0e69d911). |
| V04 | brecha_externa | F3 acreditada. F4 ausente: cobertura 2016-01-01/2025-01-01 es manual, no adopcion (recurso af7a9aba). |
| V05 | brecha_externa | F3+F4 ausentes: hueco de descarga 1960-1969 (url vacia, API+HTML) y catalogo de presas sin edicion/version/fecha. |

## Verificacion local por codigo

- Los 10 SHA256 de evidencia se recalcularon con `certutil -hashfile` y coinciden con lo citado (ver `congelada.json`).
- Confirmado `version: null` en API V01 y `url: ""` del recurso 1960-1969 (id 4d1bb645) en API V05.
- Expediente R7 revisado: entrega/cierre/peticiones/busquedas de `vigencias-uth-presas` post-R6 + paquete `web-obscura` congelado. Sin pista nueva; no se repiten busquedas genericas (W08) ni se toca el navegador Obscura (rol W exclusivo).
- Sin `peticiones-web.json`: no hay pista primaria nueva concreta.

## Limites

Sin joins, sin identidad de catalogos, sin inferir vigencia de nombres de archivo o titulos CKAN. Negativas acotadas a lo revisado 2026-10-24; no inexistencia universal. Condiciones de reapertura por caso en `entrega.json`.
