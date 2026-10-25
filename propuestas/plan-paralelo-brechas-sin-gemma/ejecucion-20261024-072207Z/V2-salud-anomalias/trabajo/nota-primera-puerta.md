# V2 — Nota de primera puerta (2026-10-24)

Alcance: V06, V07, V08, fila 177, fila 178, des_mpo_res.

## Verificación previa

- Los 18 archivos de evidencia previa citados en los antecedentes existen y sus
  SHA-256 calculados hoy coinciden byte a byte con los registrados
  (incl. `api_package_show_2026-10-24.json` = `e751fe48…`,
  diccionario CSV = `2c8ce131…`, catálogo xlsx preservado = `3b8546ac…`).
- No se re-descargó nada: sería repetir lo ya verificado en vivo el 2026-10-24.

## Búsquedas acotadas nuevas (herramienta web independiente, sin navegador)

1. `datos.sonora.gob.mx fiebre manchada Rickettsia diccionario catálogo fe de erratas edición`
   → sólo páginas conocidas del conjunto, noticias y un artículo clínico 2026
   sin vínculo campo/recurso/edición/periodo. Sin pista nueva.
2. `"datos.sonora.gob.mx" Rickettsia catalogo "versión" OR "edición" OR "fe de erratas" …`
   → resultados irrelevantes (ruido). Sin pista nueva.

## Puerta por ID

| ID | Puerta | Justificación |
|----|--------|---------------|
| V06 | sin_pista_nueva | Ninguna URL/documento/anexo no examinado con edición del catálogo (sha `3b8546ac`) vinculada a 2022-2024 |
| V07 | sin_pista_nueva | Ídem, hoja Catalogo rechazo |
| V08 | sin_pista_nueva | Ídem, hoja Catalogo especie |
| …%2F177 | sin_pista_nueva | Sin fe de erratas ni diccionario corregido del publicador |
| …%2F178 | sin_pista_nueva | Ídem, fila gemela |
| des_mpo_res | sin_pista_nueva | Sin fe de erratas; inventario API cerrado sin recurso de catálogo aplicable |

## Límite

`W-web/paquete/` no existe aún: no hay resultados del navegador compartido.
No se emitió `peticiones-web.json` porque no hay pista concreta que requiera
navegador; pedir búsquedas genéricas sería repetir lo agotado. Si W encuentra
evidencia resolutiva, corresponderá una adenda del coordinador (v002).
