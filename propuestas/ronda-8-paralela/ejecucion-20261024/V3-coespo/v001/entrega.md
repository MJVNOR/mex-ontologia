# V3-coespo — entrega v001 (2026-10-24)

Rol: vigencias COESPO (catalogo local vs periodos). 6 casos, 0 propuestas para auditar, 6 brechas externas.

## Decisiones

| id | estado | motivo resumido |
|----|--------|-----------------|
| V09 | brecha_externa | F3+F4 ausentes: sin edicion/version/fecha de catalogo.xlsx (rec. de5c06c7, hoja Catalogo_Municipios/CLAVE) ni vinculo con 1990-2019/2020-2040 |
| V10 | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V11 | brecha_externa | Igual, conj. 943d0723 rec. d7c4b8b2, hoja Catalogo_Municipios/CLAVE |
| V12 | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |
| V15 | brecha_externa | Igual, conj. 960ef0a9 rec. e0d2acc2, periodo 1990-2040 |
| V16 | brecha_externa | Igual, hoja Catalogo_Estado/CLAVE_ENT |

## Verificacion local por codigo

- Los 12 SHA256 de evidencia se recalcularon por codigo (hashlib) y coinciden con lo citado en `entrega.json`.
- Interiores xlsx inspeccionados por codigo (sharedStrings): sin celdas de version/periodo/vigencia/edicion; 2475 municipios = procedencia, no vigencia.
- Expediente R7 revisado: decisiones V09-V12,V15-V16 v002 + evidencias post-R6 + paquetes W-web v001..v004 (V3 declarado sin pista nueva, paginas COESPO/CONAPO agotadas). Sin busquedas genericas repetidas ni navegador Obscura (rol W exclusivo).
- Sin `peticiones-web.json`: no hay pista primaria nueva concreta.

## Limites

Sin joins, sin identidad de catalogos, sin transferir vigencia CONAPO 09-05-2024 al catalogo local (desfase de corte intacto). Negativas acotadas a lo revisado 2026-10-24; no inexistencia universal. Condiciones de reapertura por caso en `entrega.json`.
