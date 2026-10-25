# Materialización revisable R7 — v002 (no instalada)

Cambio único respecto a v001 (preservada intacta): descripción del concepto
`sinac-cluescertifica` (r7-s2-099) = texto_aceptable EXACTO de
`B-tecnica/lote-2.json` ID99 (definición, no shorthand de A). Ejemplo vacío y
límites conservados. Hashes y `aceptadas_sha256` recalculados.

Intersección restrictiva de `A-documental/lote-2.json` y `B-tecnica/lote-2.json`
sobre las 31 propuestas de `S2-nacimientos/v002/entrega.json`. Donde A y B
difieren, rige el corte más restrictivo (no la unión):

- A1 (17 reglas): solo el código con ejemplo local documentado; sin `tabla
  determinada`, sin totalidad del catálogo/adopción global/otra edición.
- 74/76: sin `0000=NINGUNA` ni `DIAGNOSTICOS=CIE`; ejemplo `0000` sin lectura.
- 83: sin estatus `EN OPERACION` (estatus `1` sin catálogo de estatus).
- 99: significado sin valor local verificado (ejemplo vacío).
- 84: tipo Hora + ejemplo como instancia de formato, sin unidad/duración.
- Significado solo para el recurso 2022 (46977217) y la definición local fijada.

## Contenido

- `aceptadas.json`: 31 reglas exactas (ID + nombre + `Pendiente de especificar`
  + huella de fila + diccionario/conjunto/repr/criterio/límites), 31 conceptos
  nuevos `sinac-*` (descripción = texto aprobado, sin redefinir existentes),
  3 vínculos (83/102/104, huella de esquema `9b46e1c0…` recalculada, concepto
  igual al de su regla). D103/105 y 22 brechas `...D` siguen pendientes.
- `base-semantica.json`: copia byte-idéntica de `ontologia/semantica.json`
  (sha `a30a2842…fc68ca`, estado post-R6). Sin reescritura.
- `fuentes/`: copias inmutables (S2, estructural vieja, A/B lote-2, descriptor
  y codebook ZIP, cats xlsx citados, filas de inspecciones). Inventario con
  SHA en `fuentes.json` (origen + sha por copia; renombres `(2)` anotados).
- `auditorias/`: plantillas PENDIENTES con `aceptadas_sha256` pinnado y
  `dictamenes: []`. A/B escriben los dictámenes tras revisar este SHA exacto;
  esta entrega no emite aprobaciones.
- `delta.json`: 31 reglas + 3 vínculos; `respaldada_por_definicion` 1392→1423,
  `documental_revisada` 4475→4478, `candidata_por_nombre` 20→17.
- `codigo/`: copia del código v003 (R7 con pin `aceptadas_sha256` en ambas
  auditorías; R6/consolidar idénticos a `integracion/v002`).

## Pendiente (no en esta entrega)

Revisión A/B de este SHA → dictámenes finales → manifiesto
`data/integracion-ronda-7/` → instalación → regeneración y cotejo del delta →
SHACL/Studio si aplica. Sin manifiesto final aún.
