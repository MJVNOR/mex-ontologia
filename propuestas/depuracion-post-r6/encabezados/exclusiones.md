# Exclusiones: 2 encabezados corruptos (R6)

Separación de vista accionable. No se borra ni se cura nada; fuentes y conteos históricos intactos.

## Derivación

- Total histórico: **171** (`reports/pendientes-ronda-5.json`, 171 entradas en `/significados`; coincide con `variables_pendientes: 171` en `reports/pendientes-semanticos.json` y `152+19=171` en `data/semantica/cobertura.json`).
- Vista accionable: **169** = 171 − 2 artefactos.
- Regla: filtrar por `definicion_iri` en consultas/vistas; no restar en fuentes.

## Exclusiones

### EXC-ENC-177 — `.../33d0a99e-c721-496f-a05e-07646e9ae42a%2F177`

- Localizador: `reports/pendientes-ronda-5.json#/significados/115`; fila 177 (1-based) del diccionario `33d0a99e…` en `data/portal/contenido-inspeccion.json` (`definiciones[176]`).
- Diccionario/recurso/fila: diccionario `33d0a99e-c721-496f-a05e-07646e9ae42a`, conjunto Fiebre manchada `5494daa1-…`, variable `ide_id`.
- Texto original: Nombre `ide_id`, Tipo `ide_sex`, Formato `ide_eda_ano`, Descripción `ide_col`, Catálogo `des_mpo_res`, Ejemplo `ide_cp`.
- Evidencia R6: `diversos-presas/asignacion.json` + `entrega.json` → `artefacto_documental`, "fila corrupta: repite la cabecera como valores; `des_mpo_res` es posición de columna, no referencia real"; `resultado.md` añade que la fila 7 genuina `des_mpo_res` es texto libre ("Municipio donde reside el caso", ej. "Hermosillo"); `auditoria-documental/entrega-final.json` verifica con marker exacto y registra "2 artefactos vs 169 carencias".
- Clasificación: `encabezado_corrupto/no_significado_interpretable`.
- Efecto: excluir SOLO de vista accionable; conservar origen/evidencia/conteos; requiere fe de erratas del publicador (no contactar).

### EXC-ENC-178 — `.../33d0a99e-c721-496f-a05e-07646e9ae42a%2F178`

- Localizador: `reports/pendientes-ronda-5.json#/significados/116`; fila 178 (1-based) en `data/portal/contenido-inspeccion.json` (`definiciones[177]`).
- Diccionario/recurso/fila: mismo diccionario/conjunto/variable que 177.
- Texto original: idéntico a 177 salvo Ejemplo **`id_cp`** (sin `e`) — prueba de registro único.
- Evidencia R6: `diversos-presas/*` → `artefacto_documental`, "fila corrupta gemela de la 177 (difiere solo en `id_cp`)"; `auditoria-documental/entrega-final.json` verifica con marker exacto.
- Clasificación: `encabezado_corrupto/no_significado_interpretable`.
- Efecto: excluir SOLO de vista accionable; conservar origen/evidencia/conteos; requiere fe de erratas del publicador (no contactar).

## Dos registros únicos (no borrado, no resolución)

Huellas distintas (`4b17625c…` vs `b5dbcdf5…`), Ejemplo distinto (`ide_cp` vs `id_cp`), JSONpointer distinto (`/115` vs `/116`). Se excluyen de la vista, no se eliminan ni se les asigna definición.

## Discrepancia

Sin discrepancia: premisa de 2 corruptos confirmada por evidencia.

## Fuentes (SHA256)

- `reports/pendientes-ronda-5.json` — `46f3b6f8826379be5124fb85cf6128b705fbe90deebf2c99bff64098608c8f11`
- `data/semantica/cobertura.json` — `7ef11b0a4ad9ee3aa3d3512ab2a431cee29b9295db9da76daae2e054378a39a9`
- `data/portal/contenido-inspeccion.json` — `61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb`
- `propuestas/pendientes-muse-r6/diversos-presas/asignacion.json` — `f5270ccfa3a551203b743f8f245fcdac59b8044d76e7a7312b1bfa269e678fd5`
- `propuestas/pendientes-muse-r6/diversos-presas/entrega.json` — `aae9211f86f9411a1c90c131226dc26a7f44d394908dad50d477e82465491b67`
- `propuestas/pendientes-muse-r6/diversos-presas/resultado.md` — `202874283768f29f6efb4252fec61863f9bba47fd80ef3fa53c32660f71065b7`
- `propuestas/pendientes-muse-r6/auditoria-documental/entrega-final.json` — `4afa516b5d68c0393d4c58a91eae324c075828ee91797b3515d0de3e6b8d42a8`
- `propuestas/pendientes-muse-r5/diversos/evidencia/extractos.json` — `5e2d575b34c7511813b05e98d5bea765b39635c4151c69c8b4ba5df3b2338a25`
