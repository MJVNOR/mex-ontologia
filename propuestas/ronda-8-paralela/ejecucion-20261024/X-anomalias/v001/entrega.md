# X-anomalias R8 v001 — 3 casos, 0 promovidos

Revalidación local por código 2026-10-24 (`v001/verifica.py`, verde): los 5 SHA-256
coinciden con el cierre R7 y el contenido citado se comprobó por lectura directa
(CSV 178 filas; inspección 178 definiciones; CKAN version null con 5 recursos;
xlsx 12702 B con 3 hojas nominales y 0 menciones a `des_mpo_res`). Sin cambios,
sin fe de erratas del publicador. Gemma excluido; sin contactos externos;
navegador Obscura no tocado (sin pista primaria nueva, no hay `peticiones-web.json`).

## https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177

- estado: brecha_externa
- motivo: Artefacto documental confirmado y SIN CAMBIOS: el CSV auténtico en vivo
  trae 178 filas de datos y sus últimas 2 filas repiten la cabecera como valores
  (fila 177 con ejemplo `ide_cp`); la búsqueda acotada de fe de erratas solo
  devuelve clínica sin vínculo al conjunto. Se conserva sin curar; no acredita
  concepto, código, catálogo ni conteo.
- evidencia_faltante: Fe de erratas o diccionario corregido del publicador
  (conjunto 5494daa1, recurso 33d0a99e) que aclare la fila 177 (huella 4b17625c).
  - `propuestas/cierre-brechas-post-r6/anomalias/evidencia/diccionario_ricket_1_2026-10-24.csv` [2c8ce131bf0e…] filas de datos 177-178: fila corrupta 177 con encabezados como valores.
  - `propuestas/cierre-brechas-post-r6/anomalias/evidencia/ckan-package_5494daa1_2026-10-24.json` [e751fe481af0…] diccionario sin versión ni errata; tamaño API = CSV vivo (51040 B).
  - `data/portal/contenido-inspeccion.json` [61861aab5bc2…] definiciones[176], misma fila corrupta.
- condición_reapertura: que el publicador publique la fe de erratas o diccionario
  corregido citado; entonces verificar contra el recurso y su edición.
- límites: excluir SOLO de vista accionable; sin concepto/código/catálogo/conteo;
  no es significado nuevo.

## https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178

- estado: brecha_externa
- motivo: Artefacto gemelo confirmado y SIN CAMBIOS: fila 178 idéntica a la 177
  salvo ejemplo `id_cp` (variante sin e); misma ausencia de fe de erratas.
  Se conserva sin curar; no acredita nada.
- evidencia_faltante: Fe de erratas o diccionario corregido que aclare la fila 178
  (huella b5dbcdf5).
  - Mismas tres fuentes que /177 (csv fila 178; package sin cambios; inspección definiciones[177]).
- condición_reapertura: fe de erratas o diccionario corregido del publicador para
  la fila 178; verificar contra el recurso.
- límites: iguales que /177.

## des_mpo_res

- estado: brecha_externa
- motivo: Anomalía heredada ABIERTA y sin cambios: inventario API cerrado
  (Diccionario + Catálogo + 3 datos), version null, sin recurso de municipios de
  residencia; fila 7 genuina sigue texto libre (ejemplo Hermosillo). La única
  coincidencia externa es homonimia de otro sistema sin vínculo
  campo/recurso/edición/periodo y no acredita. Solo el publicador puede aclararlo.
- evidencia_faltante: Fe de erratas o diccionario corregido que aclare 177/178 y,
  SOLO si confirma catálogo aplicable a des_mpo_res 2022-2024, su URL con
  edición/fecha; si confirma que no existe, basta la fe de erratas.
  - ckan-package_5494daa1_2026-10-24.json [e751fe481af0…] 5 recursos, version null, sin recurso de municipios.
  - diccionario_ricket_1_2026-10-24.csv [2c8ce131bf0e…] fila 7: texto libre, catálogo vacío.
  - busquedas_2026-10-24.json [62a94db34f34…] negativa acotada; único hallazgo, homónimo sin vínculo.
  - 3b8546ac…xlsx [3b8546acad74…] 12702 B = Catálogo API; 3 hojas sin des_mpo_res (verificado por código).
- condición_reapertura: fe de erratas del publicador (+ URL de catálogo con
  edición/fecha SOLO si confirma que existe).
- límites: no usar la coincidencia de nombre con la fila 7; no afirmar
  existencia/vigencia de catálogo (no identificado en inventario revisado, no
  inexistencia universal); EXC-ENC-177/178 no son significados nuevos.

Novedad frente a R7: ninguna promoción; mejora puntual: interior del xlsx
verificado por código (antes citado solo por tamaño + evidencia R6).
