# V4-seguridad v001 — V13, V14: brecha externa (sin pista nueva)

Dos IDs asignados, una decisión por ID. Ninguna propuesta acreditada.

## V13 — cat_municipio, Incidencia delictiva municipal (2015–2025)

Puerta: **sin_pista_nueva** → estado **brecha_externa**.
F3+F4 no acreditados: el Diccionario (recurso `5f46e4b8`) solo referencia por nombre
`catalogo_municipios` para `Cve. Municipio`, sin edición/versión/fecha/corte ni vínculo
con 2015–2025; el catálogo local (sha `84bb6fcd…`) no trae versión/periodo;
CKAN en vivo hoy confirma `version=null` y placeholder 1989-06-04 sin cambios.
Documento faltante: declaración del publicador con edición/versión/fecha y corte
SESNSP de cat_municipio (recurso `36d3ac85`) vinculada a 2015–2025.

## V14 — cat_entidad, Víctimas del fuero común (2015–2025)

Puerta: **sin_pista_nueva** → estado **brecha_externa**.
Simétrico a V13: Diccionario (recurso `a8a09044`) solo nombra `catalogo_entidades`
para `Clave_Ent`; catálogo local (sha `96776ca8…`) sin versión/periodo;
CKAN `version=null`, placeholder 1989-06-04, sin cambios.
Documento faltante: declaración del publicador con edición/versión/fecha y corte
SESNSP de cat_entidad (recurso `7f3aca28`) vinculada a 2015–2025.

## Notas

- Verificación CKAN en vivo 2026-10-24 con webfetch (sin Obscura, sin navegador
  compartido). Descarga directa por curl devuelve challenge anti-bots: sin copia
  nueva, no se insiste.
- `W-web/paquete/` ausente: sin resultados que contrastar ni peticiones emitidas.
- Límites: sin vigencia histórica, sin joins por Clave compartida, sin identidad
  automática de catálogos por nombre. Reapertura: documento del publicador con
  edición/corte y vínculo 2015–2025, o anexo no examinado que aporte W-web.
