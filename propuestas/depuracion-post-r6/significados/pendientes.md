# Significados sin documentacion suficiente tras R6: 169 reales

Generado (UTC): 2026-10-24T06:06:41.595266+00:00

171 originales R5 − 2 filas corruptas (excluidas solo de esta vista; otro agente documenta la exclusion) = **169 reales** con estado `sin_documentacion_suficiente`. R6 no resolvio ningun significado (solo 1 vinculo de columna presas). Sin definiciones inventadas: donde el detalle por fila no consta, figura `desconocido`.

169+2=171 verificado: 169 IRIs unicos y trazables a R5 + 2 excluidos para cotejo. JSON UTF-8.

**Indices**: las citas historicas R6 usan indice original 1-based (`definiciones[17]` = fila 17) y se conservan como cita; `localizadores_verificados` usa JSON pointer 0-based (`/definiciones/16`).

**Recursos**: `recurso_diccionario_id` conocido (locator del diccionario); `recurso_de_datos` distingue `no_acreditado` de `citado_sin_vinculo:<uuid>` sin inventar mapeo a columnas de datos.

## Resumen por grupo de fuente (6 grupos, suma 169; 16 diccionarios)

| Grupo | n | Nota |
| --- | ---: | --- |
| salud-defunciones | 32 | ADV-SALUD-MANUAL (auditoria R6, advertencia): Manual SEED 2022 autentico preservado (HTTP 200, PDF) no examinado por ID en salud (0/85 motivos lo citan). Linea alternativa acotada: completar examen por ID citando pregunta exacta del manual y por que la correspondencia formal falla (sin mapa campo-codigo/posicion, ejemplo incompatible, ambito fetal vs general) o vinculo del publicador; sin promover definiciones; no se resuelve ahora. Declaraciones publicas necesarias: diccionario SEED corregido + codebook + vinculo manual-recurso-CIE 2022 y nota edicion-recurso-periodo. |
| salud-nacimientos | 53 | Aplica ADV-SALUD-MANUAL como linea alternativa (examen por ID del manual preservado, sin promocion). Declaraciones publicas necesarias: diccionario SINAC corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Nacimientos 2022. No se resuelve ahora. |
| matriculas | 30 | R5 ya reviso reglamentos 2019/2022 y guia 2023; R6 confirma linea agotada. Declaracion publica necesaria: diccionario/matriz con descripciones + codebook + calendario 2022-2 y edicion aplicable distinta de 2019. No se resuelve ahora. |
| epidemiologia | 25 | Linea base negativa reutilizable: C1 (API version=null) + C2 (core-properties). Declaracion publica necesaria: instrumento SUIVE edicion 2022 + diccionario corregido + regla de computo + version CIE + nota borde edad 5. No se resuelve ahora. |
| tic | 24 | Linea portal agotada (S09 negativo, no repetida en R6). Declaraciones publicas necesarias: cuestionarios originales completos y muestras. Que esten en manos del publicador no cierra otras lineas primarias inequivocas futuras. No se resuelve ahora. |
| diversos | 5 | cat_estatal_1.xlsx autentico preservado (VW-33, dominio CCCCC; falta F3/F4); CONAPO 09-05-2024 y SESNSP examinados (falta declaracion del publicador). Resto segun evidencia faltante por fila. No se resuelve ahora. |
| **Total** | **169** | |

## 2 filas excluidas solo de esta vista (cotejo)

- `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177` fila 177: fila corrupta: repite la cabecera del diccionario como valores; catalogo_declarado des_mpo_res es posicion de columna, no referencia real. inspeccion local idx176: Nombre variable=ide_id, Tipo=ide_sex, Formato=ide_eda_ano, Ejemplo=ide_cp. Locator: `data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json` `/definiciones/176` sha `bba195a85b95be89…`.
- `https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178` fila 178: fila corrupta gemela de la 177 (encabezados como valores, difiere solo en id_cp). inspeccion local idx177: Nombre variable=ide_id, Tipo=ide_sex, Formato=ide_eda_ano, Ejemplo=id_cp. Locator: `data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json` `/definiciones/177` sha `bba195a85b95be89…`.

## Fuentes consultadas (SHA256 desde bytes)

- `reports/pendientes-ronda-5.json` sha256 `46f3b6f8826379be5124fb85cf6128b705fbe90deebf2c99bff64098608c8f11` — Base: 171 significados con dictamen documental R5.
- `reports/pendientes-semanticos.json` sha256 `c3a9585a46b6b8d325a37047b3f43a77ecd68b88b7ce170c013f421cae3b9680` — Cotejo: 171 variables pendientes vigentes.
- `data/semantica/cobertura.json` sha256 `7ef11b0a4ad9ee3aa3d3512ab2a431cee29b9295db9da76daae2e054378a39a9` — Cotejo: estados de cobertura actuales.
- `propuestas/pendientes-muse-r6/salud/entrega.json` sha256 `c598972e85c3ef9a94c24c528e6c45c45fd005c87d6c73275755130251f89687` — R6 salud: 85 decisiones pendiente + evidencia faltante exacta.
- `propuestas/pendientes-muse-r6/matriculas/entrega.json` sha256 `157aeea6e69030eb931fd809a4e86771abfc9da115337a6d46cfea9fb3fe35d8` — R6 matriculas: 30 decisiones pendiente + evidencia faltante exacta.
- `propuestas/pendientes-muse-r6/epidemiologia/entrega.json` sha256 `c105170dc193f44edf9e648b8f9dbc85251f8509ab1a9644e92adf3f719c7bed` — R6 epidemiologia: 25 decisiones pendiente + evidencia faltante exacta.
- `propuestas/pendientes-muse-r6/tic/entrega.json` sha256 `555232d0117aa15876d9d7b08402f821f7e2bda5e0d705782dfd76d12ccf700f` — R6 tic: 24 decisiones pendiente + requerido exacto.
- `propuestas/pendientes-muse-r6/diversos-presas/entrega.json` sha256 `aae9211f86f9411a1c90c131226dc26a7f44d394908dad50d477e82465491b67` — R6 diversos-presas: 5 pendiente + 2 artefactos (filas 177/178).
- `data/portal/inspecciones/33d0a99e-c721-496f-a05e-07646e9ae42a.json` sha256 `bba195a85b95be895e09c47dd419b6a55a2197afa7ccbcc6e23c2aab91eed179` — Verificacion independiente filas corruptas 177/178 (178 definiciones, encabezados como valores).
- `reports/ronda-6.json` sha256 `52b6abc5dd2632e9c33d27f13016f01e85e63fb4284f43a1fcc481ee770d1a47` — Cotejo: R6 resolvio 1 vinculo presas (columna), 0 significados; 171 siguen sin respaldo.
- `propuestas/pendientes-muse-r6/auditoria-documental/entrega-final.json` sha256 `4afa516b5d68c0393d4c58a91eae324c075828ee91797b3515d0de3e6b8d42a8` — Auditoria R6: 188 decisiones verificadas + ADV-SALUD-MANUAL y lineas alternativas; conteos 171=169+2.
- `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` sha256 `0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` sha256 `2094c24f84a07d1a7e9e7f3c9e663b6923e51508a71678eea74860232f2c1179` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` sha256 `76fe68223bc861fcdf62cb33f5b9a207503b192c2ef531a4aad31d52e7a7513b` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` sha256 `298786f09028a94004420c08eb28120294b130378a0cf12d609a1bffb950288d` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json` sha256 `e3d0e66563f7525a638a5a5d353d843af598a9910e3721dbddc5b39ba22e07f5` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99.json` sha256 `e463ea718d587e0e5407554a11e03c96643cccaa18e7caca7f57d81052b381c1` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/67156807-2013-4117-9ca9-394aea647127.json` sha256 `c1d42eba568474e6170cc54eba5f26334e11e5ae3e882ea9148a219485b783d3` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/863b9cc8-daeb-4430-b835-6a0ced5abd31.json` sha256 `3281c0dc4105077da1b5a5a7c48adb9dbf154c40bc3dd062708f996aca77a5af` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` sha256 `73c4f6243458d700a99df5d3c55327bc9fde1a94d75f94a443606237327574b2` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/8f8e3cfb-e551-4a95-b382-4999351c5f29.json` sha256 `e474f039c7b0a4b6cbd9a2f70744891c3eb71249b1ab02bf3d3cce4ecc6f4b5e` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json` sha256 `1c2f73fbeee284d10be656eee951558ff8ddc14ac25305829e793579bd71ad85` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` sha256 `2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json` sha256 `1b4660882f2c1d165dc3b4deb9e19b8e1f61f09b1bd9dbcfdead4bd09e8f741a` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/c65eb4e7-a17d-43c7-b08c-05811505edf1.json` sha256 `90116c242b20debee37a0002c763602f57a578a7350a616d89aae4233ad0f9bf` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/f3ecd3d2-2156-4251-82e5-13b079471ee9.json` sha256 `7f0fe9071a5c3cf4b94e9f8a3330447a4ec6ab8263521cb426606a59f6388106` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).
- `data/portal/inspecciones/f89137ba-d82e-44fe-80c7-cc355f09f9f5.json` sha256 `59c6077b4f8bb93f2bf002284cf0c18e0c6c9d1f91ded2e834756dbd45ffd73b` — Inspeccion local del diccionario: /definiciones/<fila-1> verificado por variable (indice 0-based).

## Grupo salud-defunciones (32)

### 1. EDADGESTACIONAL — fila 17

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F17`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 17 / huella `ebf425bc2303aca08a47cb9288db80db817f9dc08cce88172cb8fbb6da0162bb` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `17` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/5` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/16` (variable OK) / auditoria `/dictamenes/79` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[17] = fila 17); no es JSON pointer; el localizador verificado usa /definiciones/16
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[17] (tipo=Numerico entero; ejemplo=vacio; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 2. CLAVEOCUPACIONHABITUAL — fila 30

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F30`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 30 / huella `0c60283efbd7a350ed4b9d718903c3f0960c18af33485b7b9a017ca67f719bb5` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `30` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/6` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/29` (variable OK) / auditoria `/dictamenes/80` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[30] = fila 30); no es JSON pointer; el localizador verificado usa /definiciones/29
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[30] (tipo=Numerico entero; ejemplo=4; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 3. CLAVEOCUPACIONHABITUALD — fila 31

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F31`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 31 / huella `64ea2487a9a3fe6434910ae40db1981ef4d3d2408375db63b2b5b922ab78e73a` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `31` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/7` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/30` (variable OK) / auditoria `/dictamenes/81` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[31] = fila 31); no es JSON pointer; el localizador verificado usa /definiciones/30
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[31] (tipo=Texto; ejemplo=NO OCUPADO, JUBILADO O PENSIONADO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 4. TRABAJAACTUALMENTE — fila 32

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F32`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 32 / huella `68e0eb0630333a74377ee1a914e01b7bd2159a442cac88c128e1ad915b5b9314` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `32` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/8` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/31` (variable OK) / auditoria `/dictamenes/82` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[32] = fila 32); no es JSON pointer; el localizador verificado usa /definiciones/31
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[32] (tipo=Numerico entero; ejemplo=2; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 5. TRABAJAACTUALMENTED — fila 33

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F33`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 33 / huella `7c0c9f6aff97ac480fcb4961dad53c23a648fbc86d083d082966bc9f37becf3c` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `33` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/9` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/32` (variable OK) / auditoria `/dictamenes/83` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[33] = fila 33); no es JSON pointer; el localizador verificado usa /definiciones/32
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[33] (tipo=Texto; ejemplo=NO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 6. AFILIACION — fila 34

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F34`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 34 / huella `ee0d30d660400fc36a12bc9831d65d3a6304da573b574e2014e33bfed04162af` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `34` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/10` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/33` (variable OK) / auditoria `/dictamenes/84` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[34] = fila 34); no es JSON pointer; el localizador verificado usa /definiciones/33
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[34] (tipo=Numerico entero; ejemplo=2; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 7. AFILIACIOND — fila 35

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F35`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 35 / huella `079133f48a66d47887ac95a49b702aa77ffd04c113cabd18585025065710fedf` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `35` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/11` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/34` (variable OK) / auditoria `/dictamenes/85` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[35] = fila 35); no es JSON pointer; el localizador verificado usa /definiciones/34
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[35] (tipo=Texto; ejemplo=IMSS; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 8. SITIODEFUNCION — fila 36

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F36`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 36 / huella `abceafa503e04466cb8ef79aeaebabee4b23d406f15d6537b5a2f2af2524109f` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `36` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/12` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/35` (variable OK) / auditoria `/dictamenes/86` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[36] = fila 36); no es JSON pointer; el localizador verificado usa /definiciones/35
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[36] (tipo=Numerico entero; ejemplo=3; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 9. SITIODEFUNCIOND — fila 37

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F37`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 37 / huella `1a74eb5a4d09d849b4eece5a9d5c07cf36fbcddf88f71fe3ce0373337c32f91e` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `37` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/13` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/36` (variable OK) / auditoria `/dictamenes/87` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[37] = fila 37); no es JSON pointer; el localizador verificado usa /definiciones/36
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[37] (tipo=Texto; ejemplo=IMSS; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 10. CLUES — fila 38

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F38`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 38 / huella `1b32ad8dbecd8c74b4f0bfd3497c88a32c8b2f8590a4a9f42f2b10717804423b` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `38` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/14` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/37` (variable OK) / auditoria `/dictamenes/88` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[38] = fila 38); no es JSON pointer; el localizador verificado usa /definiciones/37
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[38] (tipo=Alfanumerico; ejemplo=SRIMS000915; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' sin vinculo local; no se promueve por nombre. Dictamen previo R4 (pendiente + pista_nombre_o_clasificador_sin_promocion) revisado y confirmado; fuentes externas candidatas R4-investigacion (DGIS/INEGI) revisadas sin vinculo local ni vigencia. Ejemplo aislado no acredita catalogo. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 11. MUERTEACCIDENTALVIOLENTA — fila 53

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F53`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 53 / huella `850bee51801949c2b817587fc192ef3781c98061d02f3e3e3ea968d674a4e73b` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `53` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/15` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/52` (variable OK) / auditoria `/dictamenes/89` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[53] = fila 53); no es JSON pointer; el localizador verificado usa /definiciones/52
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[53] (tipo=Numerico entero; ejemplo=2; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 12. MUERTEACCIDENTALVIOLENTAD — fila 54

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F54`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 54 / huella `4b5b2bc9bbd2800951da01eab22ee5b93cfd35cc7c89fe3ef995b8c196dd9575` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `54` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/16` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/53` (variable OK) / auditoria `/dictamenes/90` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[54] = fila 54); no es JSON pointer; el localizador verificado usa /definiciones/53
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[54] (tipo=Texto; ejemplo=NO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 13. INTENCIONEVENTO — fila 55

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F55`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 55 / huella `b87cc102c25d27cf6df27536027b6d6646efdd5039f47c0cfb3f58e4164047a7` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `55` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/17` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/54` (variable OK) / auditoria `/dictamenes/91` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[55] = fila 55); no es JSON pointer; el localizador verificado usa /definiciones/54
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[55] (tipo=Numerico entero; ejemplo=8; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 14. INTENCIONEVENTOD — fila 56

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F56`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 56 / huella `4131826cf3a9dc83326558466a832f676c04266acdab9f5608d4d8928e6ba26f` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `56` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/18` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/55` (variable OK) / auditoria `/dictamenes/92` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[56] = fila 56); no es JSON pointer; el localizador verificado usa /definiciones/55
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[56] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 15. CIECAUSABASICA — fila 57

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F57`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 57 / huella `81e3f9ef3c87b147379617e9e5be83166d67fbd0aed3a852ed7dbfe66696261f` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `57` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/19` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/56` (variable OK) / auditoria `/dictamenes/93` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[57] = fila 57); no es JSON pointer; el localizador verificado usa /definiciones/56
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[57] (tipo=Alfanumerico; ejemplo=U071; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 16. CIECAUSABASICAD — fila 58

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F58`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 58 / huella `db8f6d2371614ea06fc66dc615ed3e5752e6e29cc4c3df720f5e6fbd10333524` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `58` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/20` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/57` (variable OK) / auditoria `/dictamenes/94` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[58] = fila 58); no es JSON pointer; el localizador verificado usa /definiciones/57
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[58] (tipo=Texto; ejemplo=COVID-19, VIRUS IDENTIFICADO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 17. CAUSAPROPIAEMBARAZO — fila 63

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F63`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 63 / huella `56db546aff8f909eeca13cff3b2cfd9be1fd79d26117c4230b55ff006aaf7113` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `63` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/21` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/62` (variable OK) / auditoria `/dictamenes/95` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[63] = fila 63); no es JSON pointer; el localizador verificado usa /definiciones/62
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[63] (tipo=Numerico entero; ejemplo=8; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 18. CAUSAPROPIAEMBARAZOD — fila 64

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F64`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 64 / huella `f6c8aaa315795f03ce605c8756e3966010f8129eee3b92b62bb5da3645168600` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `64` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/22` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/63` (variable OK) / auditoria `/dictamenes/96` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[64] = fila 64); no es JSON pointer; el localizador verificado usa /definiciones/63
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[64] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 19. SITIOOCURRENCIALESION — fila 67

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F67`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 67 / huella `ece78b819635fc19c837c1159d9d7f26cb08be18ff31821e610ab7c5c19f4f45` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `67` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/23` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/66` (variable OK) / auditoria `/dictamenes/97` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[67] = fila 67); no es JSON pointer; el localizador verificado usa /definiciones/66
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[67] (tipo=Numerico entero; ejemplo=88; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 20. SITIOOCURRENCIALESIOND — fila 68

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F68`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 68 / huella `aa8199d031d2d4cd9334137d566dd3521c716b49eabfac04e7beaf324a09952e` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `68` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/24` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/67` (variable OK) / auditoria `/dictamenes/98` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[68] = fila 68); no es JSON pointer; el localizador verificado usa /definiciones/67
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[68] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 21. PARENTESCOAGRESORD — fila 69

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F69`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 69 / huella `eea42314404fd23e4a20c14f935c013e96331a047aee3335d349e5a568425af2` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `69` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/25` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/68` (variable OK) / auditoria `/dictamenes/99` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[69] = fila 69); no es JSON pointer; el localizador verificado usa /definiciones/68
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[69] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 22. ENTIDADOCURRENCIA — fila 70

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F70`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 70 / huella `fbfa197761cf2332d4e78aa66a5fc4fdab7f0b9088c7bd0eeb7075eda4aec6f3` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `70` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/26` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/69` (variable OK) / auditoria `/dictamenes/100` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[70] = fila 70); no es JSON pointer; el localizador verificado usa /definiciones/69
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[70] (tipo=Numerico entero; ejemplo=88; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 23. ENTIDADOCURRENCIAD — fila 71

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F71`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 71 / huella `3ca265bc2d1d622526135e122abaa60f3b47b1a468401f1cb0a4fa398b326f57` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `71` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/27` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/70` (variable OK) / auditoria `/dictamenes/101` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[71] = fila 71); no es JSON pointer; el localizador verificado usa /definiciones/70
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[71] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 24. MUNICIPIOOCURRENCIA — fila 72

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F72`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 72 / huella `da9a0fcd2979fbcca215523a090a0332d76bfb531c9f92fecae3bd347819febf` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `72` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/28` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/71` (variable OK) / auditoria `/dictamenes/102` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[72] = fila 72); no es JSON pointer; el localizador verificado usa /definiciones/71
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[72] (tipo=Numerico entero; ejemplo=997; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' sin vinculo local; no se promueve por nombre. Dictamen previo R4 (pendiente + pista_nombre_o_clasificador_sin_promocion) revisado y confirmado; fuentes externas candidatas R4-investigacion (DGIS/INEGI) revisadas sin vinculo local ni vigencia. Ejemplo aislado no acredita catalogo. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 25. MUNICIPIOOCURRENCIAD — fila 73

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F73`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 73 / huella `45f58439a5c544c88713e5f5ba62c1a0ddf40f9aa6181a506e30f6d50a6e1b85` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `73` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/29` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/72` (variable OK) / auditoria `/dictamenes/103` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[73] = fila 73); no es JSON pointer; el localizador verificado usa /definiciones/72
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[73] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' sin vinculo local; no se promueve por nombre. Dictamen previo R4 (pendiente + pista_nombre_o_clasificador_sin_promocion) revisado y confirmado; fuentes externas candidatas R4-investigacion (DGIS/INEGI) revisadas sin vinculo local ni vigencia. Ejemplo aislado no acredita catalogo. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 26. LOCALIDADOCURRENCIA — fila 74

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F74`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 74 / huella `0485c56408609aa3a1cab7e67e8e7b1f0b4ee7cd6607fbe8c97de194423cac9d` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `74` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/30` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/73` (variable OK) / auditoria `/dictamenes/104` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[74] = fila 74); no es JSON pointer; el localizador verificado usa /definiciones/73
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[74] (tipo=Numerico entero; ejemplo=9997; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' sin vinculo local; no se promueve por nombre. Dictamen previo R4 (pendiente + pista_nombre_o_clasificador_sin_promocion) revisado y confirmado; fuentes externas candidatas R4-investigacion (DGIS/INEGI) revisadas sin vinculo local ni vigencia. Ejemplo aislado no acredita catalogo. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 27. LOCALIDADOCURRENCIAD — fila 75

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F75`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 75 / huella `6f76513d06bf1de37df4a91e3103ac0e3782913df200633ca0673e907e345bd4` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `75` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/31` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/74` (variable OK) / auditoria `/dictamenes/105` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[75] = fila 75); no es JSON pointer; el localizador verificado usa /definiciones/74
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[75] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' sin vinculo local; no se promueve por nombre. Dictamen previo R4 (pendiente + pista_nombre_o_clasificador_sin_promocion) revisado y confirmado; fuentes externas candidatas R4-investigacion (DGIS/INEGI) revisadas sin vinculo local ni vigencia. Ejemplo aislado no acredita catalogo. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 28. CERTIFICADOPOR — fila 76

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F76`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 76 / huella `07e2bf0f7eb99cfe51edd3e0925dad52e77f11e359e6cfe81f1353c3d5cae30b` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `76` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/32` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/75` (variable OK) / auditoria `/dictamenes/106` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[76] = fila 76); no es JSON pointer; el localizador verificado usa /definiciones/75
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[76] (tipo=Numerico entero; ejemplo=3; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 29. CERTIFICADOPORD — fila 77

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F77`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 77 / huella `3914b430da43fdb8d84bbe502ef1177b055fb7bd251f980511412795339b0e27` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `77` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/33` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/76` (variable OK) / auditoria `/dictamenes/107` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[77] = fila 77); no es JSON pointer; el localizador verificado usa /definiciones/76
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[77] (tipo=Texto; ejemplo=OTRO MÉDICO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 30. FECHACERTIFICACION — fila 78

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F78`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 78 / huella `e9548fa45ee68e370b7d48001c4847ded6deb8d8c5b9571a64e00d9bc6f4078c` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `78` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/34` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/77` (variable OK) / auditoria `/dictamenes/108` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[78] = fila 78); no es JSON pointer; el localizador verificado usa /definiciones/77
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[78] (tipo=Fecha; ejemplo=1/6/2022 0:00; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 31. JURISDICCION_CLUES — fila 79

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F79`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 79 / huella `3d8489ce6c278e749bff0500b4cf2d7980c07857523c335bd5a139edd2ba2c2b` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `79` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/35` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/78` (variable OK) / auditoria `/dictamenes/109` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[79] = fila 79); no es JSON pointer; el localizador verificado usa /definiciones/78
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[79] (tipo=Numerico entero; ejemplo=6; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 32. JURISDICCION_CLUESD — fila 80

- IRI: `https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F80`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `cd3d6e34-3789-479e-9f2b-a717b8419f9c` / diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / fila 80 / huella `8ab02175cd04ccd00ab0c97be6b5b24ad069b254c5b1e3daaaa8f10c580e5d54` / recurso_diccionario `12f684e9-f4d5-4714-933d-aa153a812174` / recurso_datos `citado_sin_vinculo:6f39fc5d-e097-4954-8cd7-10e8f9dea541` / tabla-hoja `desconocido` / pos-fisica `80` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/36` / inspeccion `data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json` `/definiciones/79` (variable OK) / auditoria `/dictamenes/110` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[80] = fila 80); no es JSON pointer; el localizador verificado usa /definiciones/79
  - cita: data/portal/contenido-inspeccion.json#recursos/12f684e9-f4d5-4714-933d-aa153a812174/definiciones[80] (tipo=Texto; ejemplo=SAN LUIS RIO COLORADO; catalogo=no declarado)
  - cita: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar', catalogo_declarado='' y sin literal especifico; dictamen previo R4 lote-6 (pendiente) revisado y confirmado con datastore live 2026-10-23. Ejemplo aislado no acredita codigo, catalogo, unidad ni vigencia. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Vinculo explicito del publicador entre el recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 (2022-01-01 a 2022-09-22) y el Manual SEED Modelo 2022, con tabla pregunta-manual<->columna-local y edicion CIE aplicable a 2022. Base R5: diccionario SEED corregido o nota del publicador con descripcion+codebook+vinculo de catalogo/version aplicable a Defunciones 2022. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

## Grupo salud-nacimientos (53)

### 33. ORDENNACIMIENTO — fila 31

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F31`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 31 / huella `62c0bf687eac569fbf42c780856193d11d16985468fc5bce3aff74ac89877a28` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `31` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/37` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/30` (variable OK) / auditoria `/dictamenes/118` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[31] = fila 31); no es JSON pointer; el localizador verificado usa /definiciones/30
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[31] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de ORDENNACIMIENTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 62c0bf687eac... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ORDENNACIMIENTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 34. ATENCIONPRENATAL — fila 32

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F32`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 32 / huella `e7c4525ef6cfa64a9e43573f8eff37e3db1ca8ef5ccc6b4b133dbae05d3e59a1` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `32` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/38` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/31` (variable OK) / auditoria `/dictamenes/119` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[32] = fila 32); no es JSON pointer; el localizador verificado usa /definiciones/31
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[32] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de ATENCIONPRENATAL en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella e7c4525ef6cf... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ATENCIONPRENATAL en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 35. ATENCIONPRENATALD — fila 33

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F33`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 33 / huella `9c1e7a74998c0992f1b4858221249290f3c19c2d3013e2f1fbc3cd163dbebf20` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `33` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/39` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/32` (variable OK) / auditoria `/dictamenes/120` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[33] = fila 33); no es JSON pointer; el localizador verificado usa /definiciones/32
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[33] (tipo=Texto; ejemplo=SI; catalogo=no declarado)
  - cita: Descripcion publicada de ATENCIONPRENATALD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 9c1e7a74998c... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ATENCIONPRENATALD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 36. TRIMESTREPRIMERCONSULTA — fila 34

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F34`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 34 / huella `d4bd97f8975743e8e7b449527180ca9eb197ea2c23ad6611affd6ddc17ae5e36` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `34` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/40` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/33` (variable OK) / auditoria `/dictamenes/121` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[34] = fila 34); no es JSON pointer; el localizador verificado usa /definiciones/33
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[34] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de TRIMESTREPRIMERCONSULTA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella d4bd97f89757... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TRIMESTREPRIMERCONSULTA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 37. TRIMESTREPRIMERCONSULTAD — fila 35

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F35`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 35 / huella `fd83ec861012297d59ecef868513bceb6cdce90c4302d41cbcde92f103a9cf89` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `35` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/41` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/34` (variable OK) / auditoria `/dictamenes/122` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[35] = fila 35); no es JSON pointer; el localizador verificado usa /definiciones/34
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[35] (tipo=Texto; ejemplo=PRIMER TRIMESTRE; catalogo=no declarado)
  - cita: Descripcion publicada de TRIMESTREPRIMERCONSULTAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella fd83ec861012... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TRIMESTREPRIMERCONSULTAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 38. SOBREVIVIOPARTO — fila 37

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F37`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 37 / huella `14ac2d127fc5b006a7a660acc7ab1834b71ee20d815157034ade96a75f912fef` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `37` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/42` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/36` (variable OK) / auditoria `/dictamenes/123` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[37] = fila 37); no es JSON pointer; el localizador verificado usa /definiciones/36
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[37] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de SOBREVIVIOPARTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 14ac2d127fc5... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de SOBREVIVIOPARTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 39. SOBREVIVIOPARTOD — fila 38

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F38`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 38 / huella `15bbcb6b1edce711390d14bf9107a6fbfbdee09778871580ae8a1e33bb829a17` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `38` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/43` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/37` (variable OK) / auditoria `/dictamenes/124` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[38] = fila 38); no es JSON pointer; el localizador verificado usa /definiciones/37
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[38] (tipo=Texto; ejemplo=SI; catalogo=no declarado)
  - cita: Descripcion publicada de SOBREVIVIOPARTOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 15bbcb6b1edc... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de SOBREVIVIOPARTOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 40. AFILIACION — fila 39

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F39`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 39 / huella `0930442283807eb8c88d9adec21b59bab8233e2766e692ef5ef2d4f588aaf5e1` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `39` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/44` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/38` (variable OK) / auditoria `/dictamenes/125` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[39] = fila 39); no es JSON pointer; el localizador verificado usa /definiciones/38
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[39] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de AFILIACION en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 093044228380... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de AFILIACION en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 41. AFILIACIOND — fila 40

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F40`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 40 / huella `bdba1b01977ef1ce2e804171e157c0a4c96d89eee68fe4ca83c12441e0634df5` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `40` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/45` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/39` (variable OK) / auditoria `/dictamenes/126` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[40] = fila 40); no es JSON pointer; el localizador verificado usa /definiciones/39
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[40] (tipo=Texto; ejemplo=NINGUNA; catalogo=no declarado)
  - cita: Descripcion publicada de AFILIACIOND en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella bdba1b01977e... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de AFILIACIOND en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 42. INTERRUMPIOESTUDIOS — fila 43

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F43`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 43 / huella `a38193f5f7f995f447ce0d10d461cd0434763c9735d61a38f985cdc1d9ff331f` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `43` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/46` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/42` (variable OK) / auditoria `/dictamenes/127` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[43] = fila 43); no es JSON pointer; el localizador verificado usa /definiciones/42
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[43] (tipo=Numérico entero; ejemplo=2; catalogo=no declarado)
  - cita: Descripcion publicada de INTERRUMPIOESTUDIOS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella a38193f5f7f9... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de INTERRUMPIOESTUDIOS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 43. INTERRUMPIOESTUDIOSD — fila 44

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F44`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 44 / huella `b85ad2ff8e7ae91bc0410cb5b25823adcc0bdf3fea1739b05dac447ca289acf4` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `44` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/47` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/43` (variable OK) / auditoria `/dictamenes/128` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[44] = fila 44); no es JSON pointer; el localizador verificado usa /definiciones/43
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[44] (tipo=Texto; ejemplo=NO; catalogo=no declarado)
  - cita: Descripcion publicada de INTERRUMPIOESTUDIOSD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella b85ad2ff8e7a... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de INTERRUMPIOESTUDIOSD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 44. CLAVEOCUPACIONHABITUAL — fila 45

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F45`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 45 / huella `b161763fd6f817c17439a66a18a382c59f3f8a59a48578d3a0272dd55845b9f7` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `45` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/48` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/44` (variable OK) / auditoria `/dictamenes/129` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[45] = fila 45); no es JSON pointer; el localizador verificado usa /definiciones/44
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[45] (tipo=Numérico entero; ejemplo=2; catalogo=no declarado)
  - cita: Descripcion publicada de CLAVEOCUPACIONHABITUAL en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella b161763fd6f8... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CLAVEOCUPACIONHABITUAL en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 45. CLAVEOCUPACIONHABITUALD — fila 46

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F46`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 46 / huella `4c7482453a69ded7c98e1b777dfc79f78d98e5514c3ad5f1ca7bd4ada6c3c038` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `46` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/49` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/45` (variable OK) / auditoria `/dictamenes/130` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[46] = fila 46); no es JSON pointer; el localizador verificado usa /definiciones/45
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[46] (tipo=Texto; ejemplo=NO REMUNERADO, AMA DE CASA; catalogo=no declarado)
  - cita: Descripcion publicada de CLAVEOCUPACIONHABITUALD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 4c7482453a69... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CLAVEOCUPACIONHABITUALD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 46. APGAR — fila 57

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F57`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 57 / huella `fb648dfc6707016c88a6741fe2576147dcef5f2b4d450febd0a45740f7c746e9` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `57` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/50` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/56` (variable OK) / auditoria `/dictamenes/131` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[57] = fila 57); no es JSON pointer; el localizador verificado usa /definiciones/56
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[57] (tipo=Numérico entero; ejemplo=9; catalogo=no declarado)
  - cita: Descripcion publicada de APGAR en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella fb648dfc6707... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de APGAR en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 47. SILVERMAN — fila 58

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F58`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 58 / huella `8cca9f0576b6f1e307429b7193ba4f8ed7eb17ae8e48df3b0d8b7d51150ebcb6` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `58` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/51` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/57` (variable OK) / auditoria `/dictamenes/132` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[58] = fila 58); no es JSON pointer; el localizador verificado usa /definiciones/57
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[58] (tipo=Numérico entero; ejemplo=0; catalogo=no declarado)
  - cita: Descripcion publicada de SILVERMAN en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 8cca9f0576b6... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de SILVERMAN en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 48. TAMIZAUDITIVO — fila 59

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F59`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 59 / huella `dd61c41708d6f169b41ae7619f7d519f82a63b2b4a3753847a746d590629ba1f` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `59` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/52` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/58` (variable OK) / auditoria `/dictamenes/133` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[59] = fila 59); no es JSON pointer; el localizador verificado usa /definiciones/58
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[59] (tipo=Numérico entero; ejemplo=2; catalogo=no declarado)
  - cita: Descripcion publicada de TAMIZAUDITIVO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella dd61c41708d6... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TAMIZAUDITIVO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 49. TAMIZAUDITIVOD — fila 60

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F60`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 60 / huella `bc45d3d55cf992fe18ac27a5fc755df7837fcdb1062063b7ca1aa5275a6d1790` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `60` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/53` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/59` (variable OK) / auditoria `/dictamenes/134` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[60] = fila 60); no es JSON pointer; el localizador verificado usa /definiciones/59
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[60] (tipo=Texto; ejemplo=NO; catalogo=no declarado)
  - cita: Descripcion publicada de TAMIZAUDITIVOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella bc45d3d55cf9... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TAMIZAUDITIVOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 50. VACUNA_BCG — fila 61

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F61`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 61 / huella `68a7b66c7d98226381ae2602b5bab3329c0bc8b38b1b939e522f07c193f2b4d0` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `61` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/54` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/60` (variable OK) / auditoria `/dictamenes/135` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[61] = fila 61); no es JSON pointer; el localizador verificado usa /definiciones/60
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[61] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de VACUNA_BCG en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 68a7b66c7d98... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VACUNA_BCG en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 51. VACUNA_BCGD — fila 62

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F62`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 62 / huella `8d1404d50e5be7e026ed1927e82471b8310e747a6bbb7b0118827a6da86ca855` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `62` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/55` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/61` (variable OK) / auditoria `/dictamenes/136` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[62] = fila 62); no es JSON pointer; el localizador verificado usa /definiciones/61
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[62] (tipo=Texto; ejemplo=SI; catalogo=no declarado)
  - cita: Descripcion publicada de VACUNA_BCGD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 8d1404d50e5b... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VACUNA_BCGD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 52. VACUNAHEPATITIS_B — fila 63

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F63`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 63 / huella `1c1c42a9160be36a55940e175e4873d9df1340fd9664584265cf13a59239d9c0` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `63` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/56` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/62` (variable OK) / auditoria `/dictamenes/137` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[63] = fila 63); no es JSON pointer; el localizador verificado usa /definiciones/62
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[63] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de VACUNAHEPATITIS_B en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 1c1c42a9160b... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VACUNAHEPATITIS_B en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 53. VACUNAHEPATITIS_BD — fila 64

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F64`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 64 / huella `94eb763aae3f3305fccc1729438b05b4e11381d1b981235547fe2837da0ebb64` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `64` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/57` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/63` (variable OK) / auditoria `/dictamenes/138` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[64] = fila 64); no es JSON pointer; el localizador verificado usa /definiciones/63
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[64] (tipo=Texto; ejemplo=SI; catalogo=no declarado)
  - cita: Descripcion publicada de VACUNAHEPATITIS_BD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 94eb763aae3f... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VACUNAHEPATITIS_BD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 54. VITAMINA_A — fila 65

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F65`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 65 / huella `1cb751023a12f3a604fb3abbe8627293b7ad2cc7cc777faa1b53b116c0982429` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `65` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/58` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/64` (variable OK) / auditoria `/dictamenes/139` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[65] = fila 65); no es JSON pointer; el localizador verificado usa /definiciones/64
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[65] (tipo=Numérico entero; ejemplo=0; catalogo=no declarado)
  - cita: Descripcion publicada de VITAMINA_A en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 1cb751023a12... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VITAMINA_A en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 55. VITAMINA_AD — fila 66

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F66`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 66 / huella `27d2b9db3b296e9a52b731c002c266814a26eefb932b474ede6bff8f588789bb` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `66` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/59` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/65` (variable OK) / auditoria `/dictamenes/140` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[66] = fila 66); no es JSON pointer; el localizador verificado usa /definiciones/65
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[66] (tipo=Texto; ejemplo=NO ESPECIFICADO; catalogo=no declarado)
  - cita: Descripcion publicada de VITAMINA_AD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 27d2b9db3b29... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VITAMINA_AD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 56. VITAMINA_K — fila 67

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F67`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 67 / huella `7180af0ba9ef0fa427fa288465c55f66c5d15a0b62f0e769d950f7c72049ff23` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `67` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/60` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/66` (variable OK) / auditoria `/dictamenes/141` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[67] = fila 67); no es JSON pointer; el localizador verificado usa /definiciones/66
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[67] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de VITAMINA_K en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 7180af0ba9ef... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VITAMINA_K en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 57. VITAMINA_KD — fila 68

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F68`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 68 / huella `77a7e92944de778070e0431cb6b7d8f8dda45a4a884f7fbd2f43d7323d22dc4e` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `68` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/61` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/67` (variable OK) / auditoria `/dictamenes/142` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[68] = fila 68); no es JSON pointer; el localizador verificado usa /definiciones/67
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[68] (tipo=Texto; ejemplo=SI; catalogo=no declarado)
  - cita: Descripcion publicada de VITAMINA_KD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 77a7e92944de... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de VITAMINA_KD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 58. PRODUCTOEMBARAZO — fila 69

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F69`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 69 / huella `b66a776bd99ba4884bd6df9804696b53ef6b6de5a0fd9c8a22d70c78fac07881` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `69` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/62` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/68` (variable OK) / auditoria `/dictamenes/143` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[69] = fila 69); no es JSON pointer; el localizador verificado usa /definiciones/68
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[69] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de PRODUCTOEMBARAZO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella b66a776bd99b... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de PRODUCTOEMBARAZO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 59. PRODUCTOEMBARAZOD — fila 70

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F70`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 70 / huella `256dc8ca620cce901066ec75b28f2471a1579a3bdd7f540bf901c7d0528a351d` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `70` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/63` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/69` (variable OK) / auditoria `/dictamenes/144` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[70] = fila 70); no es JSON pointer; el localizador verificado usa /definiciones/69
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[70] (tipo=Texto; ejemplo=ÚNICO; catalogo=no declarado)
  - cita: Descripcion publicada de PRODUCTOEMBARAZOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 256dc8ca620c... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de PRODUCTOEMBARAZOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 60. ORDENPRODUCTO — fila 71

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F71`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 71 / huella `abcad05c885063318a672bd488a1a7d5afe1f258dea83e0fdf5c10fbac4c455c` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `71` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/64` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/70` (variable OK) / auditoria `/dictamenes/145` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[71] = fila 71); no es JSON pointer; el localizador verificado usa /definiciones/70
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[71] (tipo=Numérico entero; ejemplo=vacio; catalogo=no declarado)
  - cita: Descripcion publicada de ORDENPRODUCTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella abcad05c8850... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ORDENPRODUCTO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 61. TOTALPRODUCTOS — fila 72

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F72`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 72 / huella `ebfe8f35dcd87b903edd93c23e54950db3e88042f03c98afff7c55b5735fb5b0` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `72` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/65` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/71` (variable OK) / auditoria `/dictamenes/146` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[72] = fila 72); no es JSON pointer; el localizador verificado usa /definiciones/71
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[72] (tipo=Numérico entero; ejemplo=vacio; catalogo=no declarado)
  - cita: Descripcion publicada de TOTALPRODUCTOS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella ebfe8f35dcd8... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TOTALPRODUCTOS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 62. ANOMALIACIE1 — fila 73

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F73`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 73 / huella `df1529b004a863fce572bf6ec57880bfe4ec32d220590cdfe80f48f77207dc09` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `73` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/66` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/72` (variable OK) / auditoria `/dictamenes/147` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[73] = fila 73); no es JSON pointer; el localizador verificado usa /definiciones/72
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[73] (tipo=Texto; ejemplo=NINGUNA APARENTE; catalogo=no declarado)
  - cita: Descripcion publicada de ANOMALIACIE1 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella df1529b004a8... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ANOMALIACIE1 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 63. CODIGOCIEANOMALIA1 — fila 74

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F74`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 74 / huella `109d0f8a09c2f065e43b67ee1231d75db5b444e2cfac5b515708f543922cc9cb` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `74` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/67` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/73` (variable OK) / auditoria `/dictamenes/148` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[74] = fila 74); no es JSON pointer; el localizador verificado usa /definiciones/73
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[74] (tipo=Numérico entero; ejemplo=0000; catalogo=no declarado)
  - cita: Descripcion publicada de CODIGOCIEANOMALIA1 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 109d0f8a09c2... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CODIGOCIEANOMALIA1 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 64. ANOMALIACIE2 — fila 75

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F75`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 75 / huella `e8dae3f19613e028d8e649d280fbb1ace9a4d6275a916f523ae6a9148f3f0d6e` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `75` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/68` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/74` (variable OK) / auditoria `/dictamenes/149` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[75] = fila 75); no es JSON pointer; el localizador verificado usa /definiciones/74
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[75] (tipo=Texto; ejemplo=NINGUNA APARENTE; catalogo=no declarado)
  - cita: Descripcion publicada de ANOMALIACIE2 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella e8dae3f19613... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ANOMALIACIE2 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 65. CODIGOCIEANOMALIA2 — fila 76

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F76`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 76 / huella `998a3d29cfa98c49c38767c027ea4f7795876b5a2c98b3e47b2e17ed489f1c44` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `76` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/69` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/75` (variable OK) / auditoria `/dictamenes/150` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[76] = fila 76); no es JSON pointer; el localizador verificado usa /definiciones/75
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[76] (tipo=Numérico entero; ejemplo=0000; catalogo=no declarado)
  - cita: Descripcion publicada de CODIGOCIEANOMALIA2 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 998a3d29cfa9... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CODIGOCIEANOMALIA2 en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 66. RESOLUCIONEMBARAZO — fila 77

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F77`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 77 / huella `f4c1bedd6497fb849c4715849b63333ecc867d51d09312f371ac8c75af64759c` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `77` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/70` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/76` (variable OK) / auditoria `/dictamenes/151` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[77] = fila 77); no es JSON pointer; el localizador verificado usa /definiciones/76
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[77] (tipo=Numérico entero; ejemplo=3; catalogo=no declarado)
  - cita: Descripcion publicada de RESOLUCIONEMBARAZO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella f4c1bedd6497... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de RESOLUCIONEMBARAZO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 67. RESOLUCIONEMBARAZOD — fila 78

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F78`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 78 / huella `b7f0279e50883ff21d747355b9d076f08ef55c41b2fc061ea6cfce6decea672d` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `78` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/71` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/77` (variable OK) / auditoria `/dictamenes/152` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[78] = fila 78); no es JSON pointer; el localizador verificado usa /definiciones/77
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[78] (tipo=Texto; ejemplo=CESÁREA; catalogo=no declarado)
  - cita: Descripcion publicada de RESOLUCIONEMBARAZOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella b7f0279e5088... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de RESOLUCIONEMBARAZOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 68. UTILIZOFORCEPS — fila 79

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F79`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 79 / huella `221fff1034855415f2178988e1d14dce40c3a601a3698d286bc14cc365f19018` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `79` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/72` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/78` (variable OK) / auditoria `/dictamenes/153` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[79] = fila 79); no es JSON pointer; el localizador verificado usa /definiciones/78
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[79] (tipo=Numérico entero; ejemplo=8; catalogo=no declarado)
  - cita: Descripcion publicada de UTILIZOFORCEPS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 221fff103485... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de UTILIZOFORCEPS en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 69. UTILIZOFORCEPSD — fila 80

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F80`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 80 / huella `167ceaf4b233d562b419fa9f9ee2143c890d83c50a54b4e2841da2b2a88a536b` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `80` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/73` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/79` (variable OK) / auditoria `/dictamenes/154` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[80] = fila 80); no es JSON pointer; el localizador verificado usa /definiciones/79
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[80] (tipo=Texto; ejemplo=NO APLICA; catalogo=no declarado)
  - cita: Descripcion publicada de UTILIZOFORCEPSD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 167ceaf4b233... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de UTILIZOFORCEPSD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 70. CLUES — fila 83

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F83`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 83 / huella `8acb1135cdd9dbc95750049533a5dacc41a05b4da37d6fe4ea9d19ea5b059a1d` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `83` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/74` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/82` (variable OK) / auditoria `/dictamenes/155` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[83] = fila 83); no es JSON pointer; el localizador verificado usa /definiciones/82
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[83] (tipo=Alfanumerico; ejemplo=SRSMP000314; catalogo=no declarado)
  - cita: Descripcion publicada de CLUES en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 8acb1135cdd9... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CLUES en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 71. TIEMPOTRASLADO — fila 84

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F84`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 84 / huella `1991915d59e2db4cb7632a3ace696000c61a579578a3115399103ac11e2f4404` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `84` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/75` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/83` (variable OK) / auditoria `/dictamenes/156` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[84] = fila 84); no es JSON pointer; el localizador verificado usa /definiciones/83
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[84] (tipo=Hora; ejemplo=12:15:00 AM; catalogo=no declarado)
  - cita: Descripcion publicada de TIEMPOTRASLADO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 1991915d59e2... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TIEMPOTRASLADO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 72. PERSONALATENDIO — fila 87

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F87`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 87 / huella `511637fdd52b46d22a91e644babc50e06be4c5723f1e2783337b591ffe1a79fc` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `87` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/76` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/86` (variable OK) / auditoria `/dictamenes/157` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[87] = fila 87); no es JSON pointer; el localizador verificado usa /definiciones/86
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[87] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de PERSONALATENDIO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 511637fdd52b... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de PERSONALATENDIO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 73. PERSONALATENDIOD — fila 88

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F88`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 88 / huella `fad6728687d3ccc0c6cba7dab4a32649d413d681813329faf7347facdf7f5b73` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `88` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/77` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/87` (variable OK) / auditoria `/dictamenes/158` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[88] = fila 88); no es JSON pointer; el localizador verificado usa /definiciones/87
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[88] (tipo=Texto; ejemplo=MÉDICO; catalogo=no declarado)
  - cita: Descripcion publicada de PERSONALATENDIOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella fad6728687d3... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de PERSONALATENDIOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 74. TIPOMEDICOATENDIO — fila 89

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F89`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 89 / huella `eb4257a20d25073d0b7ba5bb875a53c333163438cc3dfa8cd2f1a1ee3bf80a3c` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `89` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/78` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/88` (variable OK) / auditoria `/dictamenes/159` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[89] = fila 89); no es JSON pointer; el localizador verificado usa /definiciones/88
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[89] (tipo=Numérico entero; ejemplo=11; catalogo=no declarado)
  - cita: Descripcion publicada de TIPOMEDICOATENDIO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella eb4257a20d25... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TIPOMEDICOATENDIO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 75. TIPOMEDICOATENDIOD — fila 90

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F90`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 90 / huella `8c3fb03e75a78f62ffbbd0a3750e590142a094b24ce2c62073de89321d1689b7` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `90` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/79` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/89` (variable OK) / auditoria `/dictamenes/160` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[90] = fila 90); no es JSON pointer; el localizador verificado usa /definiciones/89
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[90] (tipo=Texto; ejemplo=MÉDICO GINECO OBSTETRA; catalogo=no declarado)
  - cita: Descripcion publicada de TIPOMEDICOATENDIOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 8c3fb03e75a7... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de TIPOMEDICOATENDIOD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 76. CERTIFICADOPOR — fila 97

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F97`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 97 / huella `64c94f6639e0ec20742adc78b3a8d1bf1b69a59d2a83467134958b0739ec0b99` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `97` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/80` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/96` (variable OK) / auditoria `/dictamenes/161` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[97] = fila 97); no es JSON pointer; el localizador verificado usa /definiciones/96
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[97] (tipo=Numérico entero; ejemplo=7; catalogo=no declarado)
  - cita: Descripcion publicada de CERTIFICADOPOR en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 64c94f6639e0... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CERTIFICADOPOR en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 77. CERTIFICADOPORD — fila 98

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F98`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 98 / huella `37610ad8c1e9aed27617a1f38ffaeb4f53253c7adbc9aa31bd23bc75f97e9167` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `98` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/81` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/97` (variable OK) / auditoria `/dictamenes/162` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[98] = fila 98); no es JSON pointer; el localizador verificado usa /definiciones/97
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[98] (tipo=Texto; ejemplo=MÉDICO GINECO-OBSTETRA; catalogo=no declarado)
  - cita: Descripcion publicada de CERTIFICADOPORD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 37610ad8c1e9... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CERTIFICADOPORD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 78. CLUESCERTIFICA — fila 99

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F99`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 99 / huella `dc38e62e8b63f4b1bddac667f4a73aa803a86e3ac106b8ffe9f93c88f8f6608a` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `99` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/82` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/98` (variable OK) / auditoria `/dictamenes/163` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[99] = fila 99); no es JSON pointer; el localizador verificado usa /definiciones/98
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[99] (tipo=Alfanumerico; ejemplo=vacio; catalogo=no declarado)
  - cita: Descripcion publicada de CLUESCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella dc38e62e8b63... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de CLUESCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 79. ENTIDADFEDERATIVACERTIFICA — fila 100

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F100`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 100 / huella `0488d75a073d10a01e8233d00ee63b4cb765abdd9bb2ac9b3f3cb4351c402719` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `100` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/83` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/99` (variable OK) / auditoria `/dictamenes/111` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[100] = fila 100); no es JSON pointer; el localizador verificado usa /definiciones/99
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[100] (tipo=Numérico entero; ejemplo=26; catalogo=no declarado)
  - cita: Descripcion publicada de ENTIDADFEDERATIVACERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 0488d75a073d... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ENTIDADFEDERATIVACERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 80. ENTIDADFEDERATIVACERTIFICAD — fila 101

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F101`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 101 / huella `8c3167a1e5018085262e40b414fd59151509cd81961b20785c95a05b4461e42b` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `101` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/84` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/100` (variable OK) / auditoria `/dictamenes/112` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[101] = fila 101); no es JSON pointer; el localizador verificado usa /definiciones/100
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[101] (tipo=Texto; ejemplo=SONORA; catalogo=no declarado)
  - cita: Descripcion publicada de ENTIDADFEDERATIVACERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 8c3167a1e501... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de ENTIDADFEDERATIVACERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 81. MUNICIPIOCERTIFICA — fila 102

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F102`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 102 / huella `21c7fce4e834b211e513fcdc8b55a757dc5afc3da9e2b846db7aba776cfbfdf5` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `102` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/85` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/101` (variable OK) / auditoria `/dictamenes/113` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[102] = fila 102); no es JSON pointer; el localizador verificado usa /definiciones/101
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[102] (tipo=Numérico entero; ejemplo=55; catalogo=no declarado)
  - cita: Descripcion publicada de MUNICIPIOCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 21c7fce4e834... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de MUNICIPIOCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 82. MUNICIPIOCERTIFICAD — fila 103

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F103`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 103 / huella `305e3ccb01619f50cab0ded3a82e6211d21b4dcbebecd506e6911f6b489cf8f3` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `103` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/86` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/102` (variable OK) / auditoria `/dictamenes/114` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[103] = fila 103); no es JSON pointer; el localizador verificado usa /definiciones/102
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[103] (tipo=Texto; ejemplo=SAN LUIS RÍO COLORADO; catalogo=no declarado)
  - cita: Descripcion publicada de MUNICIPIOCERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella 305e3ccb0161... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de MUNICIPIOCERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 83. LOCALIDADCERTIFICA — fila 104

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F104`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 104 / huella `bda091e282317f0b810033ac9f31188dcecfe6208940a47fae73f4fb6ca85499` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `104` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/87` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/103` (variable OK) / auditoria `/dictamenes/115` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[104] = fila 104); no es JSON pointer; el localizador verificado usa /definiciones/103
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[104] (tipo=Numérico entero; ejemplo=1; catalogo=no declarado)
  - cita: Descripcion publicada de LOCALIDADCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella bda091e28231... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de LOCALIDADCERTIFICA en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 84. LOCALIDADCERTIFICAD — fila 105

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F105`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 105 / huella `c77a7050ed8af0bf7ab37ca07a830539d720a02adb9c4722d417fcdcdabd4146` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `105` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/88` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/104` (variable OK) / auditoria `/dictamenes/116` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[105] = fila 105); no es JSON pointer; el localizador verificado usa /definiciones/104
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[105] (tipo=Texto; ejemplo=SAN LUIS RIO COLORADO; catalogo=no declarado)
  - cita: Descripcion publicada de LOCALIDADCERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella c77a7050ed8a... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de LOCALIDADCERTIFICAD en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 85. FECHACERTIFICADO — fila 106

- IRI: `https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F106`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `940de7d8-73ec-4a08-8d26-b7cc97ff17bd` / diccionario `22202305-2d02-4c49-b216-cc98224357f0` / fila 106 / huella `f8189968786a6fc89fa7da1ea5d7a200f9a181d7ad11c67137d978891a306664` / recurso_diccionario `22202305-2d02-4c49-b216-cc98224357f0` / recurso_datos `citado_sin_vinculo:22202305-2d02-4c49-b216-cc98224357f0` / tabla-hoja `desconocido` / pos-fisica `106` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/89` / inspeccion `data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json` `/definiciones/105` (variable OK) / auditoria `/dictamenes/117` (resolucion) / confirma `propuestas/pendientes-muse-r6/salud/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[106] = fila 106); no es JSON pointer; el localizador verificado usa /definiciones/105
  - cita: data/portal/contenido-inspeccion.json#recursos/22202305-2d02-4c49-b216-cc98224357f0/definiciones[106] (tipo=Fecha; ejemplo=1/8/2022; catalogo=no declarado)
  - cita: Descripcion publicada de FECHACERTIFICADO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: salud)
- Motivo R6: pendiente: descripcion 'Pendiente de especificar' en la fila del diccionario (huella f8189968786a... verificada); tipo y ejemplo no definen el significado; no se aprueba por nombre ni por ejemplo. Revisa dictamen previo r4-investigacion que localizo estas filas sin descripcion y r4-lote-3 que prohibe interpretar el nombre: se confirma, la fila sigue sin descripcion en la fuente local. R6: sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripcion publicada de FECHACERTIFICADO en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o catalogo/formato primario aplicable al recurso 46977217-9396-4f9c-bddb-6616e82530b4 (SINAC 2022). R6: o vinculo explicito edicion-recurso-periodo a un manual SINAC edicion 2022 (Modelo 2015 sin vigencia declarada; Guia 2025 post-periodo). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

## Grupo matriculas (30)

### 86. Inscrito ciclo  escolar actual — fila 8

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F8`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 8 / huella `3dd942d8dd7eb14fd47c95b838b12e050c0c674607696cfa614e3793e51cc9f6` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `8` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/124` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/7` (variable OK) / auditoria `/dictamenes/53` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[8] = fila 8); no es JSON pointer; el localizador verificado usa /definiciones/7
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[8] (tipo=Alfanumérico; formato=no declarado; ejemplo=222 (Reing))
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía; el ejemplo '222 (Reing)' parece clave de ciclo con calificador de reingreso pero ningún documento lo define. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Definición del valor '222 (Reing)' y del ciclo actual de referencia en el diccionario o muestra de valores.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 87. Ciclo escolar actual motivo no inscrito — fila 11

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F11`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 11 / huella `1dd4685994413b9b5fdd5a1f362345a209c546c08b25138563091c9048eb7fb3` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `11` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/125` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/10` (variable OK) / auditoria `/dictamenes/24` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[11] = fila 11); no es JSON pointer; el localizador verificado usa /definiciones/10
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[11] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía, tipo Texto y ejemplo vacío: sin dominio ni valores no se fija si es código, motivo en texto libre o indicador. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Dominio de motivos de no inscripción (catálogo o texto libre) con ejemplos por valor.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 88. Inscritos ciclo escolar señalado — fila 12

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F12`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 12 / huella `bee5ed0527cc903199e43aa35596fa40ac6f849f09d98400728cb8eb7350f088` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `12` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/126` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/11` (variable OK) / auditoria `/dictamenes/25` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[12] = fila 12); no es JSON pointer; el localizador verificado usa /definiciones/11
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[12] (tipo=Alfanumérico; formato=no declarado; ejemplo=222 (Reing))
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía; el ejemplo '222 (Reing)' no define qué denota el valor ni a qué ciclo remite 'señalado'. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Definición del valor '222 (Reing)' y del ciclo señalado de referencia.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 89. Grupos asignaturas inscrito en ciclo escolar  señalado — fila 13

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F13`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 13 / huella `cd96c069426c8b03bf31bbc3aff4b85f74358687b4b6283d7f81fa970cfb3803` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `13` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/127` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/12` (variable OK) / auditoria `/dictamenes/26` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[13] = fila 13); no es JSON pointer; el localizador verificado usa /definiciones/12
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[13] (tipo=Alfanumérico; formato=no declarado; ejemplo=AMB04C1-001, AMB06C1-001, FIN15C1-001, MAT29A2-004, SSO01C1-008, TER14C1-001)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-001 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción que fije a qué ciclo remite 'señalado' y qué denotan los códigos de grupo.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 90. Fecha inscripción en ciclo escolar  señalado — fila 14

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F14`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 14 / huella `940c1f77837c39791ee0904bbe8123c69948da90bfc9965f38db9aacf6e680ec` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `14` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/128` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/13` (variable OK) / auditoria `/dictamenes/27` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[14] = fila 14); no es JSON pointer; el localizador verificado usa /definiciones/13
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[14] (tipo=Fecha; formato=no declarado; ejemplo=04/08/2022)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-002 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción que fije evento y ciclo de la fecha de inscripción.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 91. Se realizo equivalencia en el ciclo actual — fila 17

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F17`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 17 / huella `c72f79c67b3d7ea96d457eb05aacd319901dcfdd94433c8867b7058e940bfa80` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `17` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/129` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/16` (variable OK) / auditoria `/dictamenes/28` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[17] = fila 17); no es JSON pointer; el localizador verificado usa /definiciones/16
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[17] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía, tipo Texto y ejemplo vacío: no se fija si es indicador Sí/No, fecha, folio o texto. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Dominio y representación del campo de equivalencia en el diccionario o muestra de valores.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 92. Municipio — fila 20

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F20`
- Texto original: Municipio donde el alumno
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 20 / huella `ad458441825d75edce0abc7e0082d73b2e3fbc9ec36dbb1687451d73ff9d3eba` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `20` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/130` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/19` (variable OK) / auditoria `/dictamenes/29` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[20] = fila 20); no es JSON pointer; el localizador verificado usa /definiciones/19
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[20] (tipo=Texto; formato=no declarado; ejemplo=HERMOSILLO)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-003 RETIRADA (bloqueo auditor r5): Descripción trunca sin verbo ('Municipio donde el alumno': función ausente). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción completa con la función municipal (residencia, registro u otra).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 93. Estimulo Ciclo Actual — fila 25

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F25`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 25 / huella `6c81db2a713a0c8a2f49c1b2395851d585cf59c95242360e1187ed61650b2671` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `25` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/131` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/24` (variable OK) / auditoria `/dictamenes/30` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[25] = fila 25); no es JSON pointer; el localizador verificado usa /definiciones/24
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[25] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía, tipo Texto y ejemplo vacío: no se fija si es tipo de estímulo, monto, indicador o programa. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Dominio del campo Estímulo (catálogo de estímulos o indicador) con ejemplos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 94. Grupo Indig.(Pertenece) — fila 26

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F26`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 26 / huella `efc5620974168fb407fddd931ea38baa0b5ad61298dcefc4fc63b3c73dae24ed` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `26` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/132` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/25` (variable OK) / auditoria `/dictamenes/31` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[26] = fila 26); no es JSON pointer; el localizador verificado usa /definiciones/25
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[26] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la faceta 'pertenece' solo consta en el nombre; representación y dominio sin documentar. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Instrumento de captación o diccionario corregido con descripción, representación y valores de la faceta de pertenencia.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 95. Grupo Indig. (Habla) — fila 27

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F27`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 27 / huella `65ab41f7c96c6137da69aa44b8b72f4365220c57fde711848e1305949f5d0af0` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `27` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/133` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/26` (variable OK) / auditoria `/dictamenes/32` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[27] = fila 27); no es JSON pointer; el localizador verificado usa /definiciones/26
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[27] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la faceta 'habla' solo consta en el nombre; sin valores no se fija indicador ni lengua. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Instrumento de captación o diccionario corregido con descripción y valores de la faceta de habla.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 96. Grupo Indig. (Vive en Comunidad) — fila 28

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F28`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 28 / huella `097d21e65ccbb7ec1bac73f45a22ea46eb49a43038a61fdf9946d399973e9e84` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `28` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/134` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/27` (variable OK) / auditoria `/dictamenes/33` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[28] = fila 28); no es JSON pointer; el localizador verificado usa /definiciones/27
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[28] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la faceta solo consta en el nombre; sin valores no se fija indicador ni comunidad. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Instrumento de captación o diccionario corregido con descripción y valores de la faceta de residencia en comunidad.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 97. Grupo Indig. (Padres) — fila 29

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F29`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 29 / huella `4f809b2005251a58f4449e2ca6319fea6500df31234aaf2c8a3bf32f0cc78e12` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `29` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/135` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/28` (variable OK) / auditoria `/dictamenes/34` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[29] = fila 29); no es JSON pointer; el localizador verificado usa /definiciones/28
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[29] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la faceta solo consta en el nombre; no se fija si refiere a pertenencia, habla o ascendencia de los padres. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Instrumento de captación o diccionario corregido con descripción y valores de la faceta de padres.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 98. Área Bachillerato — fila 35

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F35`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 35 / huella `ca77e79d29f195dcb9be9084d4352373de85538a651d75cc84fc5b331d50c98f` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `35` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/136` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/34` (variable OK) / auditoria `/dictamenes/35` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[35] = fila 35); no es JSON pointer; el localizador verificado usa /definiciones/34
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[35] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo en blanco: sin dominio no se fija si es área de conocimiento, plantel o texto libre. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Dominio del campo Área de Bachillerato (catálogo de áreas o texto libre) con ejemplos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 99. Promedio anterior al ciclo inscrito (Solo asig. aprobadas) — fila 47

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F47`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 47 / huella `9df2a9f55cbfef2f78d5798d2e0e68782f1a422755938281dc3cf71a4b76544c` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `47` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/137` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/46` (variable OK) / auditoria `/dictamenes/36` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[47] = fila 47); no es JSON pointer; el localizador verificado usa /definiciones/46
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[47] (tipo=Numérico flotante; formato=no declarado; ejemplo=8.2)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-004 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción con escala, rango, método y cobertura de asignaturas del promedio.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 100. Promedio anterior al ciclo inscrito (Todas las asignaturas) — fila 48

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F48`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 48 / huella `6a40c43efeecb0fc1db0b2f04bab7ccc589b32d8cb9f040b9107ebd3e727573d` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `48` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/138` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/47` (variable OK) / auditoria `/dictamenes/37` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[48] = fila 48); no es JSON pointer; el localizador verificado usa /definiciones/47
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[48] (tipo=Numérico flotante; formato=no declarado; ejemplo=8.2)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-005 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción con escala, rango, método y cobertura de asignaturas del promedio.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 101. Num. asignaturas reprobadas ciclo anterior al ciclo inscrito — fila 49

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F49`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 49 / huella `57422aa3d40ece38f8a4434b0e62f4d6c190c95c4418eda1e87895ed54433259` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `49` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/139` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/48` (variable OK) / auditoria `/dictamenes/38` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[49] = fila 49); no es JSON pointer; el localizador verificado usa /definiciones/48
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[49] (tipo=Numérico entero; formato=no declarado; ejemplo=0)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-006 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción con método de conteo de asignaturas reprobadas.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 102. Promedio periodo escolar inscrito (Solo asig. aprobadas) — fila 52

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F52`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 52 / huella `518d3dd1d17fdcf7146020e16dc0898f76104fb6319003e07c3227852f0f9f76` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `52` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/140` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/51` (variable OK) / auditoria `/dictamenes/39` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[52] = fila 52); no es JSON pointer; el localizador verificado usa /definiciones/51
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[52] (tipo=Numérico flotante; formato=no declarado; ejemplo=0)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-007 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción con escala y método del promedio del periodo inscrito.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 103. Promedio periodo escolar inscrito (todas las asignaturas) — fila 53

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F53`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 53 / huella `636ef2fcec0d8c30b0aa97bc406864c1140e73287b70a90ee5dc24812e812183` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `53` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/141` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/52` (variable OK) / auditoria `/dictamenes/40` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[53] = fila 53); no es JSON pointer; el localizador verificado usa /definiciones/52
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[53] (tipo=Numérico flotante; formato=no declarado; ejemplo=0)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-008 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción con escala y método del promedio del periodo inscrito.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 104. Inscrito ciclo actual (solo Serv.Soc. y Pract.Prof.) — fila 54

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F54`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 54 / huella `7604572758cf453dde067084f33ae7d7d2faaee3b944554f0f25b7b5fba6a6e0` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `54` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/142` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/53` (variable OK) / auditoria `/dictamenes/41` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[54] = fila 54); no es JSON pointer; el localizador verificado usa /definiciones/53
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[54] (tipo=Numérico entero; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo en blanco con tipo Numérico entero: no se fija indicador, conteo ni clave. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Representación y dominio del campo con muestra de valores no vacíos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 105. Periodo escolar de egreso — fila 58

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F58`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 58 / huella `29d62a8cf94e56924762fd9ecbf15fe7a1cb365700fc7243f326315273388beb` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `58` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/143` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/57` (variable OK) / auditoria `/dictamenes/42` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[58] = fila 58); no es JSON pointer; el localizador verificado usa /definiciones/57
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[58] (tipo=Numérico entero; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío con tipo Numérico entero: no se fija si es clave de periodo, año o conteo. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Definición del periodo escolar de egreso y su representación (clave, año u otra) con ejemplos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 106. Tipo de baja — fila 61

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F61`
- Texto original: Tipo de baja
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 61 / huella `72da417aacf46c2518fa8ef9397a7bd08aff9a3049855e469d785dbba91b0343` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `61` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/144` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/60` (variable OK) / auditoria `/dictamenes/43` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[61] = fila 61); no es JSON pointer; el localizador verificado usa /definiciones/60
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[61] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-009 RETIRADA (bloqueo auditor r5): Descripción tautológica ('Tipo de baja' repite el nombre; sin sujeto, dominio ni valores). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Dominio y valores admisibles del tipo de baja con ejemplos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 107. Cambio de Unidad Académica — fila 62

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F62`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 62 / huella `3ff4624691f3351ee662a0ccffff065246d9216ef3dff79060f2a856849e25a8` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `62` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/145` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/61` (variable OK) / auditoria `/dictamenes/44` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[62] = fila 62); no es JSON pointer; el localizador verificado usa /definiciones/61
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[62] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío con tipo Texto: no se fija si es indicador, nombre de unidad destino o fecha. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Representación y dominio del campo de cambio de unidad con ejemplos.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 108. Alternativa de titulación de no exigibilidad — fila 63

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F63`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 63 / huella `4f697985f3ab526291a07e8bf12510c7b5ad126699989151526ad6af270786ea` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `63` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/146` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/62` (variable OK) / auditoria `/dictamenes/45` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[63] = fila 63); no es JSON pointer; el localizador verificado usa /definiciones/62
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[63] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la alternativa solo consta en el nombre; sin norma de titulación no se fija su contenido. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Norma de titulación UES que defina la alternativa de no exigibilidad y su registro.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 109. Fecha de alternativa de titulación de no exigibilidad — fila 64

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F64`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 64 / huella `6759b8b1157290027ece3602d7dff3c8609984dfbbf14c5408e656de0fe1b612` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `64` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/147` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/63` (variable OK) / auditoria `/dictamenes/46` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[64] = fila 64); no es JSON pointer; el localizador verificado usa /definiciones/63
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[64] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-010 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción del evento y norma UES de la alternativa de no exigibilidad.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 110. Alternativa de titulación de examen profesional — fila 65

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F65`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 65 / huella `874bceffaf3fe861bf15f437f4d4e8dbb8abcbf090300c5e758c2e02556ae293` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `65` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/148` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/64` (variable OK) / auditoria `/dictamenes/47` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[65] = fila 65); no es JSON pointer; el localizador verificado usa /definiciones/64
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[65] (tipo=Texto; formato=no declarado; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: matriculas)
- Motivo R6: Descripción vacía y ejemplo vacío: la alternativa solo consta en el nombre; sin norma no se fija su contenido. Sin regla revisada que respalde el significado; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Norma de titulación UES que defina la alternativa de examen profesional y su registro.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 111. Fecha de alternativa de titulación de examen prof. — fila 66

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F66`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 66 / huella `e7e0a6b9c15be989bb0faca42c9b29e55a557cd16b0d417fbb4ba533330970d2` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `66` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/149` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/65` (variable OK) / auditoria `/dictamenes/48` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[66] = fila 66); no es JSON pointer; el localizador verificado usa /definiciones/65
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[66] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-011 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción del evento y norma UES de la alternativa de examen profesional.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 112. Fecha de titulación del título profesional — fila 67

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F67`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 67 / huella `de5cd0cf3209d047b3dbc8b3a76992f8a52c6e1f6d5b20ca452b762f6b10e993` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `67` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/150` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/66` (variable OK) / auditoria `/dictamenes/49` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[67] = fila 67); no es JSON pointer; el localizador verificado usa /definiciones/66
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[67] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-012 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción que fije el evento de titulación del título profesional.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 113. Fecha de impresión del título profesional — fila 68

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F68`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 68 / huella `0475086a02e3cd9f2d50ded42b978d782edb3e1ea742601c0c0b40fec2e43d58` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `68` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/151` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/67` (variable OK) / auditoria `/dictamenes/50` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[68] = fila 68); no es JSON pointer; el localizador verificado usa /definiciones/67
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[68] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-013 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción que fije el evento de impresión del título profesional.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 114. Fecha de la convalidación — fila 69

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F69`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 69 / huella `a0792669fb9fb33d8e517cc98ef71161b90ee12f10a620cfa84b647522a5c6c1` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `69` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/152` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/68` (variable OK) / auditoria `/dictamenes/51` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[69] = fila 69); no es JSON pointer; el localizador verificado usa /definiciones/68
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[69] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=vacio)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-014 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción del evento y norma de convalidación.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 115. Fecha de la equivalencia — fila 70

- IRI: `https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F70`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `e819466c-7282-46c5-84e9-65917dd8cc85` / diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / fila 70 / huella `1fe84a93ab498ab4d7dc47f0a54b4ad5278e0d9194e5cc00c06c3028927ff3b3` / recurso_diccionario `8c0e76ff-3a86-4b1d-beee-b04bebe7df8d` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `70` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/153` / inspeccion `data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json` `/definiciones/69` (variable OK) / auditoria `/dictamenes/52` (resolucion) / confirma `propuestas/pendientes-muse-r6/matriculas/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[70] = fila 70); no es JSON pointer; el localizador verificado usa /definiciones/69
  - cita: data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json:definiciones[70] (tipo=Fecha; formato=dd/mm/aaaa; ejemplo=30/11/2021)
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: matriculas)
- Motivo R6: Propuesta r5mat-015 RETIRADA (bloqueo auditor r5): Descripción vacía ('Pendiente de especificar'). Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. Sin regla revisada ni evidencia externa vinculada. Sin regla revisada ni evidencia externa vinculada.
- Falta exacta: Descripción del evento y norma de equivalencia.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

## Grupo epidemiologia (25)

### 116. cve_cie10 — fila 9

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F9`
- Texto original: Clave
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 9 / huella `681e909fd28c2155e3b0b4396e185e481355919e4d65c2888506c08869374114` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `9` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/90` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/8` (variable OK) / auditoria `/dictamenes/78` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[9] = fila 9); no es JSON pointer; el localizador verificado usa /definiciones/8
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[9] (tipo=Alfanumerico; formato=no declarado; desc=Clave; ejemplo=A04, A08-A09 excepto A08.0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=9 (esquema fisico 59 campos)
  - cita: Descripcion que fije el objeto de cve_cie10 (clave de que) y version de catalogo vinculada al recurso local.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion generica 'Clave' sin objeto fijado; el ejemplo sugiere CIE pero inferirlo seria interpretar nombre y ejemplo, no respaldo explicito. Catalogo declarado vacio en las 59 filas. Regla r3a6-005 fija no expandir CIE por formato, ejemplo o campo. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion que fije el objeto de cve_cie10 (clave de que) y version de catalogo vinculada al recurso local.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 117. acumulado — fila 11

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F11`
- Texto original: Acumulados
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 11 / huella `f0d809e61ada2173fcef197ce73afddb2e8016b5e60becac65adb4622c52c4d6` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `11` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/91` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/10` (variable OK) / auditoria `/dictamenes/54` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[11] = fila 11); no es JSON pointer; el localizador verificado usa /definiciones/10
  - cita: 'Acumulados' no fija objeto ni periodo de acumulacion; columna fisica pos 11 observada en hoja SUIVE sin documentar su computo. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[11] (tipo=Numérico entero; formato=no declarado; desc=Acumulados; ejemplo=6)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=11 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: 'Acumulados' no fija objeto ni periodo de acumulacion; columna fisica pos 11 observada en hoja SUIVE sin documentar su computo. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Definicion de acumulado (objeto contado y periodo/regla de acumulacion) en documentacion del conjunto.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 118. de01_a_04 — fila 13

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F13`
- Texto original: Total de personas en vigilancia entre 1 y 5 años
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 13 / huella `71e70bde79d363823ea85bc4003883140edd8c635069c12e4772ce021b6909dd` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `13` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/92` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/12` (variable OK) / auditoria `/dictamenes/55` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[13] = fila 13); no es JSON pointer; el localizador verificado usa /definiciones/12
  - cita: Fila contradictoria: nombre de01_a_04 (1 a 4) frente a descripcion literal 'Total de personas en vigilancia entre 1 y 5 anos', que ademas solapa la edad 5 con de05_a_09 ('entre 5 y 9'). Las reglas hermanas r3a6-007..016 conservan ese borde literal sin reinterpretar; proponer exigiria elegir intervalo y curaria la contradiccion con una suposicion. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[13] (tipo=Numérico entero; formato=no declarado; desc=Total de personas en vigilancia entre 1 y 5 años; ejemplo=2)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=13 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Fila contradictoria: nombre de01_a_04 (1 a 4) frente a descripcion literal 'Total de personas en vigilancia entre 1 y 5 anos', que ademas solapa la edad 5 con de05_a_09 ('entre 5 y 9'). Las reglas hermanas r3a6-007..016 conservan ese borde literal sin reinterpretar; proponer exigiria elegir intervalo y curaria la contradiccion con una suposicion. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Nota metodologica del conjunto que fije el intervalo real de de01_a_04 y el tratamiento de la edad 5.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 119. se_ignoran — fila 23

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F23`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 23 / huella `712a4678ea6443e9f58a98c49834483e2c2821fc6c09ff79afffed6d5b5e4d0c` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `23` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/93` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/22` (variable OK) / auditoria `/dictamenes/56` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[23] = fila 23); no es JSON pointer; el localizador verificado usa /definiciones/22
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[23] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=23 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el nombre. Columna fisica pos 23 observada. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de se_ignoran (objeto ignorado: edad, sexo u otro).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 120. menores_1f — fila 24

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F24`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 24 / huella `9c235bec64ee84ac6be73f13281fb34ccfd77466e273cf25a2b893ed8b15694b` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `24` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/94` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/23` (variable OK) / auditoria `/dictamenes/57` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[24] = fila 24); no es JSON pointer; el localizador verificado usa /definiciones/23
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[24] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=24 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 24 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de menores_1f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 121. de01_a_04f — fila 25

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F25`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 25 / huella `96785af1d47c13ccbdd90e122e3686aac5af1b7574f41d22f10ebe0f4fcaf744` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `25` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/95` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/24` (variable OK) / auditoria `/dictamenes/58` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[25] = fila 25); no es JSON pointer; el localizador verificado usa /definiciones/24
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[25] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=25 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 25 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de01_a_04f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 122. de05_a_09f — fila 26

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F26`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 26 / huella `971f30fab7a6a0948bcd4189a83f840ee1752c0668591c84c02a56b312e65893` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `26` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/96` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/25` (variable OK) / auditoria `/dictamenes/59` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[26] = fila 26); no es JSON pointer; el localizador verificado usa /definiciones/25
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[26] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=26 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 26 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de05_a_09f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 123. de10_a_14f — fila 27

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F27`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 27 / huella `37d126eb7fdbc381aba67bb453c6af51c79b342e69a2ceff8428980bfdb1495d` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `27` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/97` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/26` (variable OK) / auditoria `/dictamenes/60` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[27] = fila 27); no es JSON pointer; el localizador verificado usa /definiciones/26
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[27] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=27 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 27 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de10_a_14f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 124. de15_a_19f — fila 28

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F28`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 28 / huella `a42fd90e2204759a31ee32e07cdfd56b4d77ff5eb4620463bae4efebc57514c7` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `28` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/98` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/27` (variable OK) / auditoria `/dictamenes/61` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[28] = fila 28); no es JSON pointer; el localizador verificado usa /definiciones/27
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[28] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=28 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 28 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de15_a_19f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 125. de20_a_24f — fila 29

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F29`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 29 / huella `0cc4157c95452c748982b1c0667684c551a6bdff52e795e20b71f7b7c2b52e14` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `29` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/99` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/28` (variable OK) / auditoria `/dictamenes/62` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[29] = fila 29); no es JSON pointer; el localizador verificado usa /definiciones/28
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[29] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=29 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 29 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de20_a_24f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 126. de25_a_44f — fila 30

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F30`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 30 / huella `bfc6c152db70092a5c576d67ffcc541dee1af624ca1e1b0d95f1a6c6f8349b5a` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `30` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/100` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/29` (variable OK) / auditoria `/dictamenes/63` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[30] = fila 30); no es JSON pointer; el localizador verificado usa /definiciones/29
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[30] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=1)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=30 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 30 observada, ejemplo '1'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de25_a_44f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 127. de45_a_49f — fila 31

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F31`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 31 / huella `91c1f556eee3a0e4d124a37770bc921d895d4e3640fdcf669f6190d9c3ea6435` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `31` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/101` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/30` (variable OK) / auditoria `/dictamenes/64` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[31] = fila 31); no es JSON pointer; el localizador verificado usa /definiciones/30
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[31] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=31 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 31 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de45_a_49f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 128. de50_a_59f — fila 32

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F32`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 32 / huella `0b783d062a8c4d6dc664997cbe2c2f62aac91a0a616b409f953f0c3d9e3f9988` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `32` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/102` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/31` (variable OK) / auditoria `/dictamenes/65` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[32] = fila 32); no es JSON pointer; el localizador verificado usa /definiciones/31
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[32] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=32 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 32 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de50_a_59f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 129. de60_a_64f — fila 33

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F33`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 33 / huella `413000668b1a98f5b920a81d0ef2d809ec4245323b769e2cea0b2d9f793f3cf9` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `33` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/103` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/32` (variable OK) / auditoria `/dictamenes/66` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[33] = fila 33); no es JSON pointer; el localizador verificado usa /definiciones/32
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[33] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=33 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 33 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de60_a_64f (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 130. de65_y_maf — fila 34

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F34`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 34 / huella `dbf3d9f670449df35da5f8973d3e4491e8dd5ba5d334b1f87f0c0c1ab0ad88a6` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `34` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/104` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/33` (variable OK) / auditoria `/dictamenes/67` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[34] = fila 34); no es JSON pointer; el localizador verificado usa /definiciones/33
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[34] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=34 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 34 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de de65_y_maf (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 131. se_ignoraf — fila 35

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F35`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 35 / huella `2ca9f9926c9a1888648ca555419346e0d0d7c0340fa2f3883e4bec38eaa11ea3` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `35` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/105` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/34` (variable OK) / auditoria `/dictamenes/68` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[35] = fila 35); no es JSON pointer; el localizador verificado usa /definiciones/34
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[35] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=35 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpreta el sufijo f por simetria con la serie sin sufijo ni por proximidad a totalf ('Total acumulado de Mujeres'). Columna fisica pos 35 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de se_ignoraf (objeto, tramo de edad y particion que el sufijo f denota).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 132. ssa — fila 36

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F36`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 36 / huella `892a850ba9bee2014e8ea5157ed208a1b7285937ec068a7600f3ced39786d710` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `36` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/106` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/35` (variable OK) / auditoria `/dictamenes/69` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[36] = fila 36); no es JSON pointer; el localizador verificado usa /definiciones/35
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[36] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=3)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=36 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (ssa) como institucion ni como objeto contado. Columna fisica pos 36 observada, ejemplo '3'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de ssa (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 133. imss_ord — fila 37

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F37`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 37 / huella `fed770c9cb25fcea694559f6ed09bb92b1338ec7499cd04ff202607d616af1a1` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `37` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/107` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/36` (variable OK) / auditoria `/dictamenes/70` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[37] = fila 37); no es JSON pointer; el localizador verificado usa /definiciones/36
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[37] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=3)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=37 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (imss_ord) como institucion ni como objeto contado. Columna fisica pos 37 observada, ejemplo '3'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de imss_ord (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 134. issste — fila 38

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F38`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 38 / huella `eefa0119b32476dfc5c023afb1776ab4b3660f5c8c770c13bdfe549f7ea5e5cd` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `38` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/108` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/37` (variable OK) / auditoria `/dictamenes/71` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[38] = fila 38); no es JSON pointer; el localizador verificado usa /definiciones/37
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[38] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=38 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (issste) como institucion ni como objeto contado. Columna fisica pos 38 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de issste (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 135. otras — fila 39

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F39`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 39 / huella `97798bd230f5554b464902d95c2a219314baa597c0011897a29bfbd786833877` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `39` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/109` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/38` (variable OK) / auditoria `/dictamenes/72` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[39] = fila 39); no es JSON pointer; el localizador verificado usa /definiciones/38
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[39] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=39 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (otras) como institucion ni como objeto contado. Columna fisica pos 39 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de otras (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 136. imss_sol — fila 40

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F40`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 40 / huella `ad7ad174a63ee88d244261373816f5c944ba444d1a8308d73d86d36d9bab61e4` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `40` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/110` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/39` (variable OK) / auditoria `/dictamenes/73` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[40] = fila 40); no es JSON pointer; el localizador verificado usa /definiciones/39
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[40] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=40 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (imss_sol) como institucion ni como objeto contado. Columna fisica pos 40 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de imss_sol (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 137. d_if — fila 41

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F41`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 41 / huella `368c74a3fa6a9b27a4cf2338164ecacee7ff4123af36a85f1c94ca5507ad4817` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `41` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/111` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/40` (variable OK) / auditoria `/dictamenes/74` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[41] = fila 41); no es JSON pointer; el localizador verificado usa /definiciones/40
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[41] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=41 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (d_if) como institucion ni como objeto contado. Columna fisica pos 41 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de d_if (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 138. pemex — fila 42

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F42`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 42 / huella `d7071b783b11329835e4809e094c3b21af91de498b2e8c80e51f265a23d687cc` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `42` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/112` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/41` (variable OK) / auditoria `/dictamenes/75` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[42] = fila 42); no es JSON pointer; el localizador verificado usa /definiciones/41
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[42] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=42 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (pemex) como institucion ni como objeto contado. Columna fisica pos 42 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de pemex (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 139. sedena — fila 43

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F43`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 43 / huella `b3b91a250af63c5f1370577f3362b969a442d93312e0089d453949aceb7b93a6` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `43` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/113` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/42` (variable OK) / auditoria `/dictamenes/76` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[43] = fila 43); no es JSON pointer; el localizador verificado usa /definiciones/42
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[43] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=43 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (sedena) como institucion ni como objeto contado. Columna fisica pos 43 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de sedena (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 140. sedemar — fila 44

- IRI: `https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F44`
- Texto original: Pendiente de especificar
- Localizacion: conjunto `dca16d84-dbf0-4501-b702-dc6372a480ea` / diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / fila 44 / huella `72f0cdc5158a36e2aa5078e46ebfe64979885d3d52c8c7f51c9563c955db731f` / recurso_diccionario `2334deaa-dd0c-444e-b038-4cc556ad715d` / recurso_datos `no_acreditado` / tabla-hoja `SUIVE` / pos-fisica `44` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/114` / inspeccion `data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json` `/definiciones/43` (variable OK) / auditoria `/dictamenes/77` (resolucion) / confirma `propuestas/pendientes-muse-r6/epidemiologia/entrega.json`
- Nota indice: citas textuales R6 usan indice original 1-based (p. ej. definiciones[44] = fila 44); no es JSON pointer; el localizador verificado usa /definiciones/43
  - cita: data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json:definiciones[44] (tipo=Numérico entero; formato=no declarado; desc=Pendiente de especificar; ejemplo=0)
  - cita: data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json:hoja=SUIVE:posicion=44 (esquema fisico 59 campos)
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: epidemiologia)
- Motivo R6: Descripcion 'Pendiente de especificar': sin respaldo explicito vinculado a esta definicion; no se interpretan las siglas (sedemar) como institucion ni como objeto contado. Columna fisica pos 44 observada, ejemplo '0'. Sin respaldo explicito vinculado a esta definicion; no se aprueba por nombre.
- Falta exacta: Descripcion publicada de sedemar (objeto contado y papel de la sigla en el conjunto).
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

## Grupo tic (24)

### 141. P10 — fila 8

- IRI: `https://example.org/mex-ontologi/definition/3851f1c3-5045-4703-ba88-93b3d39e0b70%2F8`
- Texto original: Actividades principales:
- Localizacion: conjunto `0ec245ba-6941-4995-a564-52e0a4f3999f` / diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / fila 8 / huella `4f9fb5b377dfbe33f00c46630bfccd6746f2d2d814d9acaeb4ab2cc0975b6657` / recurso_diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P10:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/117` / inspeccion `data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json` `/definiciones/7` (variable OK) / auditoria `/dictamenes/5` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json fila Hoja1 P10: Tipo de dato=Texto, Descripcion='Actividades principales:', Ejemplo de dato='Actividades Principales'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=4f9fb5b377dfbe33f00c46630bfccd6746f2d2d814d9acaeb4ab2cc0975b6657); inspeccion sha256 e3d0e66563f7525a638a5a5d353d843af598a9910e3721dbddc5b39ba22e07f5
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion tautologica ('Actividades principales:') cuyo ejemplo repite el nombre sin definir que actividades. Confirma el pendiente r4-lote-5 tras relectura. Requiere documento que defina P10 (ex solicitud tic-web-02). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Documento que defina que actividades cubre P10 ("Actividades principales:"). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 142. P11 — fila 9

- IRI: `https://example.org/mex-ontologi/definition/3851f1c3-5045-4703-ba88-93b3d39e0b70%2F9`
- Texto original: ¿De qué área depende?
- Localizacion: conjunto `0ec245ba-6941-4995-a564-52e0a4f3999f` / diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / fila 9 / huella `4b88cf48467cccd83f412f108ef17a4f92ef8e2969ccb4f5d3cea31076f6ccab` / recurso_diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P11:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/118` / inspeccion `data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json` `/definiciones/8` (variable OK) / auditoria `/dictamenes/6` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json fila Hoja1 P11: Tipo de dato=Texto, Descripcion='¿De qué área depende?', Ejemplo de dato='Area 1'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=4b88cf48467cccd83f412f108ef17a4f92ef8e2969ccb4f5d3cea31076f6ccab); inspeccion sha256 e3d0e66563f7525a638a5a5d353d843af598a9910e3721dbddc5b39ba22e07f5
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: pregunta sin sujeto explicito (quien depende de que area); el ejemplo no fija el papel y el diccionario no declara vinculo con P9. Confirma el pendiente r4-lote-5. Requiere cuestionario que fije el sujeto (ex solicitud tic-web-02). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que fije el sujeto de P11 ("De que area depende?"). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 143. P15 — fila 13

- IRI: `https://example.org/mex-ontologi/definition/3851f1c3-5045-4703-ba88-93b3d39e0b70%2F13`
- Texto original: Especifique el perfil:
- Localizacion: conjunto `0ec245ba-6941-4995-a564-52e0a4f3999f` / diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / fila 13 / huella `db97f09dc3371524cb030a644dca7e3901ba7ce374c07dc26b7e286b88250f93` / recurso_diccionario `3851f1c3-5045-4703-ba88-93b3d39e0b70` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P15:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/119` / inspeccion `data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json` `/definiciones/12` (variable OK) / auditoria `/dictamenes/7` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json fila Hoja1 P15: Tipo de dato=Texto, Descripcion='Especifique el perfil:', Ejemplo de dato='Computologo'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/3851f1c3-5045-4703-ba88-93b3d39e0b70.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=db97f09dc3371524cb030a644dca7e3901ba7ce374c07dc26b7e286b88250f93); inspeccion sha256 e3d0e66563f7525a638a5a5d353d843af598a9910e3721dbddc5b39ba22e07f5
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: referencia anaforica ('el perfil') sin referente declarado en la propia fila. Confirma el pendiente r4-lote-5. Requiere documento que fije el referente (ex solicitud tic-web-02). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Documento que fije el referente de "el perfil" en P15 (vinculo P14-P15). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 144. P27 — fila 26

- IRI: `https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F26`
- Texto original: ¿Cuáles?
- Localizacion: conjunto `37ab8134-d376-4ebd-94cc-f48bcc7eacd6` / diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / fila 26 / huella `a0e8068c621f1f58f22f7ac54c60c5a5b235a4d3c9d9a1279555b5e45f072b4b` / recurso_diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P27:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/164` / inspeccion `data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json` `/definiciones/25` (variable OK) / auditoria `/dictamenes/18` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json fila Hoja1 P27: Tipo de dato=Texto, Descripcion='¿Cuáles?', Ejemplo='Normatividad 1, normatividad 2'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=a0e8068c621f1f58f22f7ac54c60c5a5b235a4d3c9d9a1279555b5e45f072b4b); inspeccion sha256 1b4660882f2c1d165dc3b4deb9e19b8e1f61f09b1bd9dbcfdead4bd09e8f741a
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion vacua ('¿Cuáles?') sin referente en la propia fila; el vinculo con la pregunta filtro no esta declarado en el diccionario. Confirma el pendiente r4-lote-6 tras relectura de vecinas. Requiere cuestionario que vincule P26-P27 (ex solicitud tic-web-06). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que vincule P26-P27 y fije el referente de "Cuales?". En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 145. P29 — fila 28

- IRI: `https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F28`
- Texto original: ¿Cuáles?
- Localizacion: conjunto `37ab8134-d376-4ebd-94cc-f48bcc7eacd6` / diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / fila 28 / huella `ac2c83b54d1ed131f828e0a762766f5aaaf88164886236f0d40b74e6db9bf4df` / recurso_diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P29:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/165` / inspeccion `data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json` `/definiciones/27` (variable OK) / auditoria `/dictamenes/19` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json fila Hoja1 P29: Tipo de dato=Texto, Descripcion='¿Cuáles?', Ejemplo='Normas especificas'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=ac2c83b54d1ed131f828e0a762766f5aaaf88164886236f0d40b74e6db9bf4df); inspeccion sha256 1b4660882f2c1d165dc3b4deb9e19b8e1f61f09b1bd9dbcfdead4bd09e8f741a
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion vacua ('¿Cuáles?') sin referente propio. Confirma el pendiente r4-lote-6. Requiere cuestionario que vincule P28-P29 (ex solicitud tic-web-06). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que vincule P28-P29. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 146. P31 — fila 30

- IRI: `https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F30`
- Texto original: ¿Cuáles?
- Localizacion: conjunto `37ab8134-d376-4ebd-94cc-f48bcc7eacd6` / diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / fila 30 / huella `4f9b41ed2ebc8bb469abab687d020141c788adc85f7b342b72e8bc66faee8ea6` / recurso_diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P31:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/166` / inspeccion `data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json` `/definiciones/29` (variable OK) / auditoria `/dictamenes/20` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json fila Hoja1 P31: Tipo de dato=Texto, Descripcion='¿Cuáles?', Ejemplo='Normas especificas'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=4f9b41ed2ebc8bb469abab687d020141c788adc85f7b342b72e8bc66faee8ea6); inspeccion sha256 1b4660882f2c1d165dc3b4deb9e19b8e1f61f09b1bd9dbcfdead4bd09e8f741a
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion vacua ('¿Cuáles?') sin referente propio. Confirma el pendiente r4-lote-6. Requiere cuestionario que vincule P30-P31 (ex solicitud tic-web-06). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que vincule P30-P31. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 147. P33 — fila 32

- IRI: `https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F32`
- Texto original: ¿Cuáles?4
- Localizacion: conjunto `37ab8134-d376-4ebd-94cc-f48bcc7eacd6` / diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / fila 32 / huella `ddf4237e2b6938bdc5f24fd12b883882e0cbeb4f803b9b9a64b8e781326de106` / recurso_diccionario `bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P33:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/167` / inspeccion `data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json` `/definiciones/31` (variable OK) / auditoria `/dictamenes/21` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json fila Hoja1 P33: Tipo de dato=Texto, Descripcion='¿Cuáles?4', Ejemplo='Normas especificas'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=ddf4237e2b6938bdc5f24fd12b883882e0cbeb4f803b9b9a64b8e781326de106); inspeccion sha256 1b4660882f2c1d165dc3b4deb9e19b8e1f61f09b1bd9dbcfdead4bd09e8f741a
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion vacua ('¿Cuáles?4') sin referente propio y con marca '4' sin nota que la explique. Confirma el pendiente r4-lote-6. Requiere cuestionario que vincule P32-P33 y aclare la marca (ex solicitud tic-web-06). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que vincule P32-P33 y aclare la marca "4". En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 148. P7 — fila 7

- IRI: `https://example.org/mex-ontologi/definition/f3ecd3d2-2156-4251-82e5-13b079471ee9%2F7`
- Texto original: ¿Cómo se generan?
- Localizacion: conjunto `7c6183e5-5903-47c6-9fce-34f018bbdb6a` / diccionario `f3ecd3d2-2156-4251-82e5-13b079471ee9` / fila 7 / huella `bcdbc5b839080631c8b00c4de5676bae31c8a82953aed84c48f2d17ece70f0d1` / recurso_diccionario `f3ecd3d2-2156-4251-82e5-13b079471ee9` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P7:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/169` / inspeccion `data/portal/inspecciones/f3ecd3d2-2156-4251-82e5-13b079471ee9.json` `/definiciones/6` (variable OK) / auditoria `/dictamenes/23` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/f3ecd3d2-2156-4251-82e5-13b079471ee9.json fila Hoja1 P7: Tipo de dato=Texto, Descripcion='¿Cómo se generan?', Ejemplo='Se generan realizando proyectos'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/f3ecd3d2-2156-4251-82e5-13b079471ee9.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=bcdbc5b839080631c8b00c4de5676bae31c8a82953aed84c48f2d17ece70f0d1); inspeccion sha256 7f0fe9071a5c3cf4b94e9f8a3330447a4ec6ab8263521cb426606a59f6388106
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: pregunta sin sujeto, misma situacion que su gemela de Gobernanza. Confirma el pendiente r4-lote-4. Requiere cuestionario que fije el referente (ex solicitud tic-web-07). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que fije el referente de "Como se generan?" (Fortalezas). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 149. P11 — fila 11

- IRI: `https://example.org/mex-ontologi/definition/8f8e3cfb-e551-4a95-b382-4999351c5f29%2F11`
- Texto original: Si la respuesta es sí a la pregunta anterior ¿cuenta con una planeación presupuestal para este requerimiento?
- Localizacion: conjunto `9208a313-553c-4308-8d58-506e037060b1` / diccionario `8f8e3cfb-e551-4a95-b382-4999351c5f29` / fila 11 / huella `0fda5e0941a806b4b187ba9d4af85fe2336a9ba992fa1f4fdf612b44380aafbf` / recurso_diccionario `8f8e3cfb-e551-4a95-b382-4999351c5f29` / recurso_datos `citado_sin_vinculo:c6d42e45-2193-4e22-a5b1-aa2770e9acf1` / tabla-hoja `Hoja1` / pos-fisica `P11:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/154` / inspeccion `data/portal/inspecciones/8f8e3cfb-e551-4a95-b382-4999351c5f29.json` `/definiciones/10` (variable OK) / auditoria `/dictamenes/8` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: pendiente: el Tipo declarado (Booleano Si/No) contradice el ejemplo (lista 'Tecnologia 1, tecnologia 2'); dominio de valores indeterminado. La remision a 'la pregunta anterior' (P10 respaldada) no resuelve el dominio. Confirma el pendiente r4-lote-5. Requiere muestra de valores de P11 en el recurso c6d42e45-2193-4e22-a5b1-aa2770e9acf1 o cuestionario (ex solicitud tic-web-03). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
  - cita: data/portal/inspecciones/8f8e3cfb-e551-4a95-b382-4999351c5f29.json fila Hoja1 P11: Tipo de dato=Booleano Formato=Si/No, Descripcion='Si la respuesta es sí a la pregunta anterior ¿cuenta con una planeación presupuestal para este requerimiento?', Ejemplo de dato='Tecnologia 1, tecnologia 2'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/8f8e3cfb-e551-4a95-b382-4999351c5f29.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=0fda5e0941a806b4b187ba9d4af85fe2336a9ba992fa1f4fdf612b44380aafbf); inspeccion sha256 e474f039c7b0a4b6cbd9a2f70744891c3eb71249b1ab02bf3d3cce4ecc6f4b5e
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: el Tipo declarado (Booleano Si/No) contradice el ejemplo (lista 'Tecnologia 1, tecnologia 2'); dominio de valores indeterminado. La remision a 'la pregunta anterior' (P10 respaldada) no resuelve el dominio. Confirma el pendiente r4-lote-5. Requiere muestra de valores de P11 en el recurso c6d42e45-2193-4e22-a5b1-aa2770e9acf1 o cuestionario (ex solicitud tic-web-03). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P11 en el recurso c6d42e45-2193-4e22-a5b1-aa2770e9acf1 o cuestionario que fije el dominio. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 150. P7 — fila 7

- IRI: `https://example.org/mex-ontologi/definition/c65eb4e7-a17d-43c7-b08c-05811505edf1%2F7`
- Texto original: ¿Cómo se generan?
- Localizacion: conjunto `a3ea3c02-2e31-40b6-a90b-c12be719f9da` / diccionario `c65eb4e7-a17d-43c7-b08c-05811505edf1` / fila 7 / huella `bcdbc5b839080631c8b00c4de5676bae31c8a82953aed84c48f2d17ece70f0d1` / recurso_diccionario `c65eb4e7-a17d-43c7-b08c-05811505edf1` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P7:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/168` / inspeccion `data/portal/inspecciones/c65eb4e7-a17d-43c7-b08c-05811505edf1.json` `/definiciones/6` (variable OK) / auditoria `/dictamenes/22` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/c65eb4e7-a17d-43c7-b08c-05811505edf1.json fila Hoja1 P7: Tipo de dato=Texto, Descripcion='¿Cómo se generan?', Ejemplo='Se generan realizando proyectos'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/c65eb4e7-a17d-43c7-b08c-05811505edf1.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=bcdbc5b839080631c8b00c4de5676bae31c8a82953aed84c48f2d17ece70f0d1); inspeccion sha256 90116c242b20debee37a0002c763602f57a578a7350a616d89aae4233ad0f9bf
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: pregunta sin sujeto ('¿Cómo se generan?') incompleta por si sola. Confirma el pendiente r4-lote-4 tras relectura de vecina y ejemplo. Requiere cuestionario que fije el referente (ex solicitud tic-web-07). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que fije el referente de "Como se generan?" (Gobernanza). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 151. P10 — fila 10

- IRI: `https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F10`
- Texto original: ¿En su dependencia coordinadora existe interés y apoyo para que el personal de TIC analice las tendencias y nuevas tecnologías en el mercado para identificar oportunidades de innovación que permit…
- Localizacion: conjunto `aa353273-7ef0-4279-987a-40fc49b3d712` / diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / fila 10 / huella `f12d0cae51621dc25907c4b911f4de83803c39e4abc43e700df8a1398384d59e` / recurso_diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P10:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/0` / inspeccion `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` `/definiciones/9` (variable OK) / auditoria `/dictamenes/0` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json fila Hoja1 P10: Tipo de dato=Booleano Formato=Si/No, Descripcion de 197 caracteres que termina a mitad de palabra en '...que permit\u2026', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=f12d0cae51621dc25907c4b911f4de83803c39e4abc43e700df8a1398384d59e); inspeccion sha256 0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion truncada a mitad de palabra en la celda fuente ('...que permit\u2026'); no hay sentido literal completo. Confirma el pendiente r4-lote-5 tras relectura de la fila exacta. Requiere texto completo del cuestionario (ex solicitud tic-web-01). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Texto literal completo de P10 (termina en "...que permit..."). Solo el publicador lo tiene: cuestionario original de Politica Digital.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 152. P11 — fila 11

- IRI: `https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F11`
- Texto original: Enliste algunos ejemplos que reflejen lo anterior:
- Localizacion: conjunto `aa353273-7ef0-4279-987a-40fc49b3d712` / diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / fila 11 / huella `3754e039074ac352b83d8a19025561b2694774713bc34c6a6d4283eeac895af4` / recurso_diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P11:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/1` / inspeccion `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` `/definiciones/10` (variable OK) / auditoria `/dictamenes/1` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json fila Hoja1 P11: Tipo de dato=Texto, Descripcion='Enliste algunos ejemplos que reflejen lo anterior:', Ejemplo='Tecnologia 1, tecnologia 2'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=3754e039074ac352b83d8a19025561b2694774713bc34c6a6d4283eeac895af4); inspeccion sha256 0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: referencia anaforica ('lo anterior') cuyo referente es P10, a su vez truncada y pendiente; sin referente fijado no se fija a que aspecto responde el valor. Confirma el pendiente r4-lote-5. Requiere cuestionario completo (ex solicitud tic-web-01). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que fije el referente de "lo anterior" (P10 truncada). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 153. P16 — fila 16

- IRI: `https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F16`
- Texto original: Antes de la publicación de la Ley de Gobierno Digital ¿Su dependencia coordinadora contaba con reglamentos, políticas, procedimientos o instrumentos que orientarán las estrategias o acciones en ma...
- Localizacion: conjunto `aa353273-7ef0-4279-987a-40fc49b3d712` / diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / fila 16 / huella `b9c90f66d430431c37c00e624c437c76a2d5322baa95bb3e9db8c29526d85748` / recurso_diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P16:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/2` / inspeccion `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` `/definiciones/15` (variable OK) / auditoria `/dictamenes/2` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json fila Hoja1 P16: Tipo de dato=Booleano Formato=Si/No, Descripcion de 199 caracteres que termina en '...en ma...', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=b9c90f66d430431c37c00e624c437c76a2d5322baa95bb3e9db8c29526d85748); inspeccion sha256 0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion truncada a mitad de frase en la celda fuente ('...en ma...'); no hay sentido literal completo. Confirma el pendiente r4-lote-5 tras relectura. Requiere texto completo (ex solicitud tic-web-01). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Texto literal completo de P16 ("...en ma..."). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 154. P18 — fila 18

- IRI: `https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F18`
- Texto original: ¿Actualmente qué reglamentos, políticas, procedimientos o instrumentos se están implementando en la administración pública estatal que han permitido mejorar las estrategias o acciones en materia d...
- Localizacion: conjunto `aa353273-7ef0-4279-987a-40fc49b3d712` / diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / fila 18 / huella `600e59e30fdb8f070c636dbd6a5c7847559a8336a406a459cf96b8d0565e9e3b` / recurso_diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P18:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/3` / inspeccion `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` `/definiciones/17` (variable OK) / auditoria `/dictamenes/3` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json fila Hoja1 P18: Tipo de dato=Booleano Formato=Si/No, Descripcion de 199 caracteres que termina en '...materia d...', Ejemplo='No'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=600e59e30fdb8f070c636dbd6a5c7847559a8336a406a459cf96b8d0565e9e3b); inspeccion sha256 0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion truncada a mitad de frase en la celda fuente ('...materia d...'). Confirma el pendiente r4-lote-5. Requiere texto completo (ex solicitud tic-web-01). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Texto literal completo de P18 ("...materia d..."). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 155. P21 — fila 21

- IRI: `https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F21`
- Texto original: Actualmente, ¿qué reglamentos, políticas, procedimientos o instrumentos se están implementando en la administración pública estatal que han permitido mejorar las estrategias o acciones en materia ...
- Localizacion: conjunto `aa353273-7ef0-4279-987a-40fc49b3d712` / diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / fila 21 / huella `475c015e01c163e51abfb2ba7fc0b9a873014f974371de968b123dfafd77b49e` / recurso_diccionario `063058e6-aed3-4a60-b944-5e653c77b14d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P21:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/4` / inspeccion `data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json` `/definiciones/20` (variable OK) / auditoria `/dictamenes/4` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json fila Hoja1 P21: Tipo de dato=Texto, Descripcion de 199 caracteres que termina en '...materia ...', Ejemplo='El reglamento 120 y el 159'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/063058e6-aed3-4a60-b944-5e653c77b14d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=475c015e01c163e51abfb2ba7fc0b9a873014f974371de968b123dfafd77b49e); inspeccion sha256 0ea3dfe7bd13b50aa647d976a6dd59ac9dd33c102eee2c6bc88b301d9f810be0
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion truncada a mitad de frase en la celda fuente ('...materia ...') aunque el ejemplo este completo. Confirma el pendiente r4-lote-5. Requiere texto completo (ex solicitud tic-web-01). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Texto literal completo de P21 ("...materia ..."). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 156. P22 — fila 22

- IRI: `https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F22`
- Texto original: ¿Cuenta con servicios, plataformas, aplicaciones, respaldos, servidores, equipo en arrendamiento, entre otros, que utilizan las TIC (telecomunicaciones, mantenimientos software y hardware, equipos...
- Localizacion: conjunto `c9a63b8b-4d70-47db-bfc7-cf86a10b0514` / diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / fila 22 / huella `2cdcdd7b899707963cf16780c196ee354d1c472f9475c835d57ae28bc4438754` / recurso_diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P22:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/155` / inspeccion `data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json` `/definiciones/21` (variable OK) / auditoria `/dictamenes/9` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json fila Hoja1 P22: Tipo de dato=Booleano Formato=Si/No, Descripcion cortada a mitad de frase en '...equipos...' (sin cerrar parentesis ni enumeracion), Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=2cdcdd7b899707963cf16780c196ee354d1c472f9475c835d57ae28bc4438754); inspeccion sha256 1c2f73fbeee284d10be656eee951558ff8ddc14ac25305829e793579bd71ad85
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: descripcion truncada a mitad de frase en la celda fuente ('...equipos...'); no se infiere el resto. Confirma el pendiente r4-lote-4 tras relectura de la fila exacta. Requiere texto completo (ex solicitud tic-web-04). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Texto literal completo de P22 ("...equipos..."). En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 157. P36 — fila 36

- IRI: `https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F36`
- Texto original: ¿Cuántos proyectos de desarrollo de software se encuentran en desarrollo actualmente por su dependencia?
- Localizacion: conjunto `c9a63b8b-4d70-47db-bfc7-cf86a10b0514` / diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / fila 36 / huella `a622c78b00fec5c4bbcf724bc106cb906b1673342bc41637a6229270c46d651b` / recurso_diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / recurso_datos `citado_sin_vinculo:91c95c1b-969e-414a-8f70-83576e881281` / tabla-hoja `Hoja1` / pos-fisica `P36:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/156` / inspeccion `data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json` `/definiciones/35` (variable OK) / auditoria `/dictamenes/10` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: pendiente: la pregunta pide un conteo ('Cuántos proyectos') pero el dominio declarado acreditable es Si/No con ejemplo 'Si'; no se distingue conteo de existencia. Confirma el pendiente r4-lote-4 tras relectura. Requiere muestra de valores de P36 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario (ex solicitud tic-web-04). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
  - cita: data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json fila Hoja1 P36: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cuántos proyectos de desarrollo de software se encuentran en desarrollo actualmente por su dependencia?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=a622c78b00fec5c4bbcf724bc106cb906b1673342bc41637a6229270c46d651b); inspeccion sha256 1c2f73fbeee284d10be656eee951558ff8ddc14ac25305829e793579bd71ad85
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: la pregunta pide un conteo ('Cuántos proyectos') pero el dominio declarado acreditable es Si/No con ejemplo 'Si'; no se distingue conteo de existencia. Confirma el pendiente r4-lote-4 tras relectura. Requiere muestra de valores de P36 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario (ex solicitud tic-web-04). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P36 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 158. P39 — fila 39

- IRI: `https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F39`
- Texto original: ¿Cómo atiene las incidencias, reportes de problemas técnicos, solución de dudas, etc.?
- Localizacion: conjunto `c9a63b8b-4d70-47db-bfc7-cf86a10b0514` / diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / fila 39 / huella `97b808090a361a57edc4330ddcb08facbf2df34aab5f81fc389e4dd316ae9729` / recurso_diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / recurso_datos `citado_sin_vinculo:91c95c1b-969e-414a-8f70-83576e881281` / tabla-hoja `Hoja1` / pos-fisica `P39:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/157` / inspeccion `data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json` `/definiciones/38` (variable OK) / auditoria `/dictamenes/11` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json fila Hoja1 P39: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cómo atiene las incidencias, reportes de problemas técnicos, solución de dudas, etc.?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=97b808090a361a57edc4330ddcb08facbf2df34aab5f81fc389e4dd316ae9729); inspeccion sha256 1c2f73fbeee284d10be656eee951558ff8ddc14ac25305829e793579bd71ad85
  - cita: Muestra de valores de P39 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: la pregunta pide una manera ('Cómo atiende...') pero el dominio declarado es Si/No con ejemplo 'Si'; el mecanismo no se fija. Confirma el pendiente r4-lote-4. Requiere muestra de valores o cuestionario (ex solicitud tic-web-04). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P39 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 159. P40 — fila 40

- IRI: `https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F40`
- Texto original: ¿Cuantas personas tiene dedicadas a labores de desarrollo de software?
- Localizacion: conjunto `c9a63b8b-4d70-47db-bfc7-cf86a10b0514` / diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / fila 40 / huella `7ce240ae95790d9120999d9fc11ca42d2fce329e8f002aebc6ffa9bde4d5ac20` / recurso_diccionario `a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d` / recurso_datos `citado_sin_vinculo:91c95c1b-969e-414a-8f70-83576e881281` / tabla-hoja `Hoja1` / pos-fisica `P40:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/158` / inspeccion `data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json` `/definiciones/39` (variable OK) / auditoria `/dictamenes/12` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json fila Hoja1 P40: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cuantas personas tiene dedicadas a labores de desarrollo de software?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=7ce240ae95790d9120999d9fc11ca42d2fce329e8f002aebc6ffa9bde4d5ac20); inspeccion sha256 1c2f73fbeee284d10be656eee951558ff8ddc14ac25305829e793579bd71ad85
  - cita: Muestra de valores de P40 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: la pregunta pide un conteo ('Cuantas personas') pero el dominio declarado es Si/No con ejemplo 'Si'; la fila no acredita conteo. Confirma el pendiente r4-lote-4. Requiere muestra de valores o cuestionario (ex solicitud tic-web-04). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P40 en el recurso 91c95c1b-969e-414a-8f70-83576e881281 o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 160. P8 — fila 8

- IRI: `https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F8`
- Texto original: ¿Qué metodología de planeación utiliza y que documentación se realiza en un proyecto de desarrollo de software?
- Localizacion: conjunto `d175b134-77f4-4201-9409-08b05c1d5ffa` / diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / fila 8 / huella `49268969a6e55b1a9591c2be36f50b3997a81a03ceea3b81a53e33c034f1c898` / recurso_diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P8:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/159` / inspeccion `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` `/definiciones/7` (variable OK) / auditoria `/dictamenes/13` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json fila Hoja1 P8: Tipo de dato=Texto, Descripcion='¿Qué metodología de planeación utiliza y que documentación se realiza en un proyecto de desarrollo de software?', Ejemplo='Metodologia 0.5'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=49268969a6e55b1a9591c2be36f50b3997a81a03ceea3b81a53e33c034f1c898); inspeccion sha256 2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: pregunta doble (metodología Y documentación) en una sola variable; no se fija a qué aspecto responde el valor. Confirma el pendiente r4-lote-2 tras relectura. Requiere cuestionario que separe aspectos o muestra de valores (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Cuestionario que separe metodologia y documentacion en P8, o muestra de valores. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 161. P13 — fila 13

- IRI: `https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F13`
- Texto original: ¿Qué tipo de pruebas realizan?
- Localizacion: conjunto `d175b134-77f4-4201-9409-08b05c1d5ffa` / diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / fila 13 / huella `348163c8632f1c6ca793b7b4bcd827b3f135c6fba5326582f1392d6541d2a95b` / recurso_diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / recurso_datos `no_acreditado` / tabla-hoja `Hoja1` / pos-fisica `P13:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/160` / inspeccion `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` `/definiciones/12` (variable OK) / auditoria `/dictamenes/14` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json fila Hoja1 P13: Tipo de dato=Texto, Descripcion='¿Qué tipo de pruebas realizan?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=348163c8632f1c6ca793b7b4bcd827b3f135c6fba5326582f1392d6541d2a95b); inspeccion sha256 2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: la pregunta pide un tipo pero el ejemplo ('Si') responde existencia; dominio de valores indeterminado. Confirma el pendiente r4-lote-2. Requiere muestra de valores o cuestionario (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P13 o cuestionario que fije el dominio. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 162. P36 — fila 36

- IRI: `https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F36`
- Texto original: ¿Cuántos proyectos de desarrollo de software se encuentran en desarrollo actualmente por su dependencia?
- Localizacion: conjunto `d175b134-77f4-4201-9409-08b05c1d5ffa` / diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / fila 36 / huella `a622c78b00fec5c4bbcf724bc106cb906b1673342bc41637a6229270c46d651b` / recurso_diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / recurso_datos `citado_sin_vinculo:b444876c-8681-4503-98ca-06876a62faae` / tabla-hoja `Hoja1` / pos-fisica `P36:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/161` / inspeccion `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` `/definiciones/35` (variable OK) / auditoria `/dictamenes/15` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: pendiente: conteo pedido ('Cuántos proyectos') frente a dominio Si/No con ejemplo 'Si'. Confirma el pendiente r4-lote-2. Requiere muestra de valores de P36 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
  - cita: data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json fila Hoja1 P36: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cuántos proyectos de desarrollo de software se encuentran en desarrollo actualmente por su dependencia?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=a622c78b00fec5c4bbcf724bc106cb906b1673342bc41637a6229270c46d651b); inspeccion sha256 2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: conteo pedido ('Cuántos proyectos') frente a dominio Si/No con ejemplo 'Si'. Confirma el pendiente r4-lote-2. Requiere muestra de valores de P36 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P36 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 163. P39 — fila 39

- IRI: `https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F39`
- Texto original: ¿Cómo atiene las incidencias, reportes de problemas técnicos, solución de dudas, etc.?
- Localizacion: conjunto `d175b134-77f4-4201-9409-08b05c1d5ffa` / diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / fila 39 / huella `97b808090a361a57edc4330ddcb08facbf2df34aab5f81fc389e4dd316ae9729` / recurso_diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / recurso_datos `citado_sin_vinculo:b444876c-8681-4503-98ca-06876a62faae` / tabla-hoja `Hoja1` / pos-fisica `P39:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/162` / inspeccion `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` `/definiciones/38` (variable OK) / auditoria `/dictamenes/16` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json fila Hoja1 P39: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cómo atiene las incidencias, reportes de problemas técnicos, solución de dudas, etc.?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=97b808090a361a57edc4330ddcb08facbf2df34aab5f81fc389e4dd316ae9729); inspeccion sha256 2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e
  - cita: Muestra de valores de P39 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: manera pedida ('Cómo atiende...') frente a dominio Si/No con ejemplo 'Si'. Confirma el pendiente r4-lote-2. Requiere muestra de valores o cuestionario (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P39 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 164. P40 — fila 40

- IRI: `https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F40`
- Texto original: ¿Cuantas personas tiene dedicadas a labores de desarrollo de software?
- Localizacion: conjunto `d175b134-77f4-4201-9409-08b05c1d5ffa` / diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / fila 40 / huella `7ce240ae95790d9120999d9fc11ca42d2fce329e8f002aebc6ffa9bde4d5ac20` / recurso_diccionario `af14d207-7697-4d52-b99b-46a35a1b76ac` / recurso_datos `citado_sin_vinculo:b444876c-8681-4503-98ca-06876a62faae` / tabla-hoja `Hoja1` / pos-fisica `P40:` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/163` / inspeccion `data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json` `/definiciones/39` (variable OK) / auditoria `/dictamenes/17` (resolucion) / confirma `propuestas/pendientes-muse-r6/tic/entrega.json`
  - cita: data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json fila Hoja1 P40: Tipo de dato=Booleano Formato=Si/No, Descripcion='¿Cuantas personas tiene dedicadas a labores de desarrollo de software?', Ejemplo='Si'
  - cita: r6 2026-10-23: relectura de la fila exacta en data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json: tipo/ejemplo/descripcion byte-identicos a r5 (huella_fila_diccionario=7ce240ae95790d9120999d9fc11ca42d2fce329e8f002aebc6ffa9bde4d5ac20); inspeccion sha256 2950f37c23c5c11ad941bf1bf5845e87b973e5c38fea652cbc023e31c276022e
  - cita: Muestra de valores de P40 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario. En manos del publicador.
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: tic)
- Motivo R6: pendiente: conteo pedido ('Cuantas personas') frente a dominio Si/No con ejemplo 'Si'. Confirma el pendiente r4-lote-2. Requiere muestra de valores o cuestionario (ex solicitud tic-web-05). R6 confirma pendiente: fila byte-identica a r5 y linea web-portal agotada (S09 negativo); el documento exacto requerido esta en manos del publicador.
- Falta exacta: Muestra de valores de P40 en el recurso b444876c-8681-4503-98ca-06876a62faae o cuestionario. En manos del publicador.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

## Grupo diversos (5)

### 165. Total_Egresos — fila 15

- IRI: `https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15`
- Texto original: Total de urgencias atendidas
- Localizacion: conjunto `8993c917-47d8-4304-8141-5f481fe04301` / diccionario `f89137ba-d82e-44fe-80c7-cc355f09f9f5` / fila 15 / huella `98c73e56ff407766447b52e08850d0b8669f6979145b4c66fac1f1f83aec9f05` / recurso_diccionario `f89137ba-d82e-44fe-80c7-cc355f09f9f5` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `desconocido` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/170` / inspeccion `data/portal/inspecciones/f89137ba-d82e-44fe-80c7-cc355f09f9f5.json` `/definiciones/14` (variable OK) / auditoria `/dictamenes/170` (resolucion) / confirma `propuestas/pendientes-muse-r6/diversos-presas/entrega.json`
  - cita: Contradiccion conservada y ahora reforzada: la norma nacional separa egresos (GIIS-B002) de urgencias (GIIS-B014), por lo que 'Total_Egresos = Total de urgencias atendidas' no puede curarse por suposicion en ninguna direccion. Documento exacto necesario: aclaracion del publicador (Servicios de Salud de Sonora) sobre que cuenta la columna (en manos del publicador) o diccionario corregido; alternativa web SW6-DIV-02 (Descripcion de variables del cubo DGIS 2018-2022).
  - cita: data/portal/inspecciones/f89137ba-d82e-44fe-80c7-cc355f09f9f5.json fila 15: variable Total_Egresos, Tipo Numerico entero, Descripcion 'Total de urgencias atendidas', ejemplo 2
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: diversos-presas)
- Motivo R6: Contradiccion conservada y ahora reforzada: la norma nacional separa egresos (GIIS-B002) de urgencias (GIIS-B014), por lo que 'Total_Egresos = Total de urgencias atendidas' no puede curarse por suposicion en ninguna direccion. Documento exacto necesario: aclaracion del publicador (Servicios de Salud de Sonora) sobre que cuenta la columna (en manos del publicador) o diccionario corregido; alternativa web SW6-DIV-02 (Descripcion de variables del cubo DGIS 2018-2022).
- Falta exacta: Aclaracion del publicador (Servicios de Salud de Sonora) sobre Total_Egresos (egresos vs urgencias); la norma DGIS vigente los separa pero es de 2026 y no cubre 2018-2022. Alternativa web SW6-DIV-02. Solo publicador para la aclaracion, no contactar.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 166. CLASIF — fila 5

- IRI: `https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5`
- Texto original: Clasificación
- Localizacion: conjunto `a3320cad-afd3-4840-8c3b-36236df26099` / diccionario `67156807-2013-4117-9ca9-394aea647127` / fila 5 / huella `c16feb711c8027da46df863668671e9f35e699129da382b494d45039abe1f232` / recurso_diccionario `67156807-2013-4117-9ca9-394aea647127` / recurso_datos `no_acreditado` / tabla-hoja `desconocido` / pos-fisica `desconocido` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/121` / inspeccion `data/portal/inspecciones/67156807-2013-4117-9ca9-394aea647127.json` `/definiciones/4` (variable OK) / auditoria `/dictamenes/167` (resolucion) / confirma `propuestas/pendientes-muse-r6/diversos-presas/entrega.json`
  - cita: Descripcion generica 'Clasificacion' sin objeto declarado; la lista de unidad sugiere pero no declara que clasifique el asentamiento. Linea nueva (atributo 'clasificacion de la colonia' INEGI/CONAPO) sin vinculo documental al recurso local. Documento exacto necesario: metodologia COESPO 2020 que defina CLASIF (en manos del publicador) o evidencia web de correspondencia (SW6-DIV-01).
  - cita: data/portal/inspecciones/67156807-2013-4117-9ca9-394aea647127.json fila 5: variable CLASIF, Tipo Categorico, Descripcion 'Clasificacion', Unidad 'Barrio; Colonia; Ejido; Fraccionamiento; Privada; Residencial; Unidad habitacional', ejemplo Colonia, sin catalogo
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: diversos-presas)
- Motivo R6: Descripcion generica 'Clasificacion' sin objeto declarado; la lista de unidad sugiere pero no declara que clasifique el asentamiento. Linea nueva (atributo 'clasificacion de la colonia' INEGI/CONAPO) sin vinculo documental al recurso local. Documento exacto necesario: metodologia COESPO 2020 que defina CLASIF (en manos del publicador) o evidencia web de correspondencia (SW6-DIV-01).
- Falta exacta: Documento metodologico COESPO del Indice de marginacion urbana por colonia 2020 que defina la variable CLASIF (objeto clasificado y lista cerrada de 7 valores), o evidencia web de correspondencia con 'clasificacion de la colonia' INEGI/CONAPO (SW6-DIV-01). Publicador o rol web.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 167. TRIMESTRE — fila 2

- IRI: `https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2`
- Texto original: Trimestre del estrato
- Localizacion: conjunto `c589afac-79f1-4aac-9ade-e949301bcca3` / diccionario `3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99` / fila 2 / huella `799f924f8f10e3831cebdb4fbbc233cb6965caae8902f799881277d12f24320d` / recurso_diccionario `3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99` / recurso_datos `no_acreditado` / tabla-hoja `2020` / pos-fisica `2` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/120` / inspeccion `data/portal/inspecciones/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99.json` `/definiciones/1` (variable OK) / auditoria `/dictamenes/166` (resolucion) / confirma `propuestas/pendientes-muse-r6/diversos-presas/entrega.json`
  - cita: data/portal/inspecciones/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99.json fila 2: variable TRIMESTRE, Tipo Numerico entero, Descripcion 'Trimestre del estrato', ejemplo 1, sin catalogo
  - cita: NUEVO R6: descarga CLI del xlsx 2026-10-23 bloqueada por WAF (HEAD https://datos.sonora.gob.mx/.../conjunto-de-datos-denuncias-1er-trim-2022.xlsx = HTTP 403 text/html cloudflare); sin valores no se verifica si TRIMESTRE es constante 1 (trimestre del recurso) o varia por denuncia
  - cita: Recurso unico 5772b8ec (1er-trim-2022) hoja '2020' campo pos 2; concepto tiempo solo candidato por nombre, no promovido
- Estado: `sin_documentacion_suficiente` (cobertura: `candidata_sin_definicion_suficiente`; rol R6: diversos-presas)
- Motivo R6: Descripcion insuficiente: 'Trimestre del estrato' no define si es trimestre calendario de denuncia o estrato muestral/operativo; tipo entero y ejemplo 1 sin mapa; sin metodologia ni catalogo. No se propone concepto. Documento exacto necesario: metodologia o cuestionario PROAES que defina 'estrato' (en manos del publicador).
- Falta exacta: Metodologia o cuestionario PROAES de Denuncias Ambientales que defina 'estrato' y a que trimestre se refiere TRIMESTRE (calendario de denuncia vs estrato operativo). Solo publicador, no contactar.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 168. CVOTRAS — fila 7

- IRI: `https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7`
- Texto original: Clave de otras
- Localizacion: conjunto `e093cf34-7da0-4efb-89a3-7b473a5013ab` / diccionario `863b9cc8-daeb-4430-b835-6a0ced5abd31` / fila 7 / huella `7b43908359031edee596dab23b179df402c2da718dff957ef86902d8127c49c4` / recurso_diccionario `863b9cc8-daeb-4430-b835-6a0ced5abd31` / recurso_datos `no_acreditado` / tabla-hoja `otras` / pos-fisica `desconocido` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/122` / inspeccion `data/portal/inspecciones/863b9cc8-daeb-4430-b835-6a0ced5abd31.json` `/definiciones/6` (variable OK) / auditoria `/dictamenes/168` (resolucion) / confirma `propuestas/pendientes-muse-r6/diversos-presas/entrega.json`
  - cita: data/portal/inspecciones/863b9cc8-daeb-4430-b835-6a0ced5abd31.json fila 7: variable CVOTRAS, Tipo Numerico Int, Descripcion 'Clave de otras', sin catalogo ni ejemplo
  - cita: NUEVO R6: catalogo.xlsx local b38645a9-bf15-4366-a1e0-63f5cfbd91c1.xlsx re-verificado por bytes 2026-10-23 (15958 bytes, magia PK, sha256 08d345e0b03b54b390fc011ef0390b1c7eb7bdc5f2a61e2bb3251d5806aebcb3 identico a R5): hojas ['Especie_Pesca','Distritos','Municipios','Regiones']; sin hoja 'otras'
  - cita: Posicion 7/15 entre NOFICINA (oficina pesquera, fila 6) y CESPE (especie, fila 9): contexto posicional registrado sin interpretar objeto
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: diversos-presas)
- Motivo R6: Descripcion trunca 'Clave de otras': objeto indeterminado (otras oficinas, especies u origenes). Sin ejemplo, unidad ni catalogo que la resuelva. Documento exacto necesario: diccionario corregido o metodologia de pesca SAGARHPA (en manos del publicador) o evidencia web (SW6-DIV-03).
- Falta exacta: Diccionario corregido o metodologia de Pesca y Acuacultura (SAGARHPA) que complete 'Clave/Nombre de otras' (CVOTRAS/DOTRAS) y su catalogo, o evidencia web (SW6-DIV-03). Publicador o rol web.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.

### 169. DOTRAS — fila 8

- IRI: `https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8`
- Texto original: Nombre de otras
- Localizacion: conjunto `e093cf34-7da0-4efb-89a3-7b473a5013ab` / diccionario `863b9cc8-daeb-4430-b835-6a0ced5abd31` / fila 8 / huella `738de0329c2d2e19f50d85dc13b3e6a05c4d79fda579701c400d01e4ebc806b3` / recurso_diccionario `863b9cc8-daeb-4430-b835-6a0ced5abd31` / recurso_datos `no_acreditado` / tabla-hoja `otras` / pos-fisica `desconocido` / catalogo declarado ``
- Localizadores verificados: R5 `/significados/123` / inspeccion `data/portal/inspecciones/863b9cc8-daeb-4430-b835-6a0ced5abd31.json` `/definiciones/7` (variable OK) / auditoria `/dictamenes/169` (resolucion) / confirma `propuestas/pendientes-muse-r6/diversos-presas/entrega.json`
  - cita: data/portal/inspecciones/863b9cc8-daeb-4430-b835-6a0ced5abd31.json fila 8: variable DOTRAS, Tipo Texto, Descripcion 'Nombre de otras', sin catalogo ni ejemplo
  - cita: NUEVO R6: ver CVOTRAS (catalogo sin hoja 'otras', SHA identico); columna fisica DOTRAS pos 8 verificada en contenido-inspeccion
- Estado: `sin_documentacion_suficiente` (cobertura: `fuera_del_nucleo_actual`; rol R6: diversos-presas)
- Motivo R6: Descripcion trunca gemela de CVOTRAS; mismo objeto indeterminado. Documento exacto necesario: diccionario corregido o metodologia de pesca (en manos del publicador) o evidencia web (SW6-DIV-03).
- Falta exacta: Diccionario corregido o metodologia de Pesca y Acuacultura (SAGARHPA) que complete 'Clave/Nombre de otras' (CVOTRAS/DOTRAS) y su catalogo, o evidencia web (SW6-DIV-03). Publicador o rol web.
- Criterio futuro: Condiciones futuras (basta una; no excluyen otra evidencia primaria inequivoca vinculada a esta definicion): (1) documento del publicador que fije el sentido literal de esta fila (conjunto+diccionario+fila+huella citados) y vincule edicion-recurso-periodo; (2) diccionario corregido, fe de erratas o codebook del publicador aplicable a esta fila; (3) otra evidencia primaria inequivoca vinculada explicitamente a esta definicion. No basta: parecido de nombre, ejemplo aislado, catalogo nacional generico sin vinculo local ni inferencia del texto truncado.
