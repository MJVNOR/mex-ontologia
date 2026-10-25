# Ronda 5 — Presas: resultado

Rol: resolver la unica columna pendiente del contexto (cat_estatal/Clave,
recurso 4219d141-5084-4308-bda3-d44ca28a4f53). Solo se escribe en
`propuestas/pendientes-muse-r5/presas/`. Sin control de Obscura; sin cambios
al nucleo, fuentes, configuracion, chat, Studio ni entregas ajenas.

## Decision por columna (1)

| Columna | Campo | Decisión | Motivo |
| --- | --- | --- | --- |
| `…/cat_estatal/1` | Clave | pendiente | /1 (Historico_presas) vs /4 (Catalogo_estatal): mismo concepto, distinta hoja y descripcion; hoja fisica `cat_estatal` no iguala exactamente a ninguna (cat≠catalogo); dominio compartido no verificable localmente. No se fuerza. |

Evidencia fresca re-verificada 2026-10-23 (no repetida sin revisar):

- Huellas re-computadas identicas a r4 y base r5: esquema fisico
  `29af60e8…`, fila /1 `87295257…`, fila /4 `d1208344…`, cobertura
  `ee3f6a1b…`, semantica `0d8ffc75…`.
- Diccionario completo (`diccionario_completo=true`, 22 filas, 2 hojas).
- Mapa del recurso: 14/17 columnas `documental_revisada` (todas a filas
  Catalogo_estatal), 1 ambigua (Clave), 3 sin correspondencia (pos 3, 15, 16).
  La hoja fisica no es espejo del Catalogo_estatal: trae `Cuenca hidrologica`
  (pos 3) sin fila en el diccionario y omite Comision/Subdireccion/Rio; pos 15
  y 16 tienen homonimo exacto (/19, /21) y siguen sin correspondencia:
  precedente de que la homonimia exacta no basta.
- Sin valores: no hay recurso Historico_presas en el conjunto (solo
  diccionario + cat_estatal_1.xlsx), sin datastore del recurso; la re-descarga
  CLI esta bloqueada (HEAD 2026-10-23: HTTP 403 Forbidden, Content-Type
  text/html, Server cloudflare; GET = pagina WAF sha `f4836e42…`, sin magia PK,
  eliminada y no usada como evidencia). Escaneo de todos los .xlsx en
  `data/integracion/fuentes` y `data/territorio/fuentes` por hoja: sin copia
  autentica (el proximo, `612b2b11…` de Recursos Hidricos, es otro conjunto).
  Rige la inspeccion fijada http 200; la captura original no se reemplaza.
  Búsqueda negativa documentada en `entrega.json` (fuentes).

## Decisiones por significado (2)

- `/1` y `/4`: ambas `respaldada_por_definicion` (reglas vigentes r3a10-0363 y
  r3a10-0365); sin cambio de significado. El pendiente es solo el vinculo
  columna→definicion. Limite registrado: no usar una fila para habilitar joins
  con la otra por compartir Clave.

## Cuentas verificadas

- Columnas: 1 → proponer 0, pendiente 1, rechazar 0, artefacto 0.
- Vinculos nuevos: 0. Reglas nuevas: 0. Conceptos nuevos: 0.
- Significados constatados: 2 (sin cambio). Solicitudes web: 1.
- Observaciones del contexto: 4 vigentes + 1 nota historica, conservadas sin
  decision (no son de este rol).

## Solicitud web

`solicitudes_web.json`: 1 pedido a catalogos-web sobre la pagina del dataset
`8c1f452e…` (correspondencia de hoja, existencia de Historico_presas,
comparacion de dominios o constancia de ausencia, con fecha y captura).
