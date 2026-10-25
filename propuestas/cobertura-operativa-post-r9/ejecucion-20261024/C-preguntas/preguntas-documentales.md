# C-preguntas — preguntas documentales (preservacion exacta v002, preparadas_no_enviadas)

Fuente unica: `propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json` (v002, corrige_a v001).
Copia: `preguntas-documentales.json` es copia byte-identica de la fuente (tal cual, sin correcciones).
Estado operativo: `preparadas_no_enviadas`. No se afirma envio, no hay 7 correos ni 19 solicitudes.

## Metadatos del expediente original (no afirmaciones de envio)
- 7 necesidades (ND-01..ND-07) + 7 preguntas (PQ-01..PQ-07) preservadas EXACTAS.
- 19 casos / 104 evidencias: metadatos del expediente original (C4 v002 `entrega.json`: `casos_asignados` 19, `casos_cubiertos` 19 = 16 vigencias + 3 anomalias, `evidencias_citadas` 104, `evidencias_verificadas_sha256_por_codigo` 104). Se listan como contexto, NO como 7 correos ni como 19 solicitudes.
- Union de casos en necesidades/preguntas: V01,V02,V03,V04,V05,V06,V07,V08,V09,V10,V11,V12,V13,V14,V15,V16 + 2 IRIs (...%2F177, ...%2F178) + des_mpo_res = 19.

## Limites y condiciones conservados (sin cartas obligatorias ni contactos)
- Criterio general v002: admite cualquier cadena documental primaria suficiente (oficio, lineamiento, nota de version del conjunto u otra); eliminada la exigencia de carta especial. Sin cartas obligatorias.
- Sin contactos, sin nueva busqueda, sin investigacion web. Sin tocar produccion.
- No corregir fuentes cerradas. No modificar grafos ni manifiestos R1-R9/Gemma.
- Cada necesidad/pregunta conserva sus `limites` / `condicion` propios de la fuente; este .md no los reescribe, solo los cita via el .json.

## Verificacion de trazabilidad (local, sin web; si error se alerta, no se inventa)
- ND-01 org=uth (f353bb81-d268-40cd-aa74-d3f53402189a) fuente=api_package_V01_403912fd-5853-4e18-8256-f77206f855bd_2026-10-24.json sha=84b12a9a43b94bc6dc808af9f21bc7ea441847a18b46234a4b646887cd301707 casos=V01,V02,V03,V04
- ND-02 org=sagarhpa (e563936a-2a3c-4f0b-a2d9-203dac8229a8) fuente=api_package_V05_ee8f639f-5e89-46ae-93b9-934b05fc6233_2026-10-24.json sha=2776b9297d47743ea0e18888e03e0a27bb1e7cd778375ada435c6f470472e625 casos=V05
- ND-03 org=sp (e798580f-d450-42ed-9302-ffb1630ecc7e) fuente=api_package_show_2026-10-24.json sha=e751fe481af047f3ffa6facc57c9d04952e5f874186be2d2fb4a6ae20f9a0154 casos=V06,V07,V08
- ND-04 org=coespo (80c1c21d-31ff-4562-97ef-9c1666e2e464) fuente=api-package-0b5f5e16.json sha=4ca156b4619b9bcc9d69b6ced3cc3ed4b1b07e586c674acdfc3f907304bc6749 casos=V09,V10,V11,V12,V15,V16
- ND-05 org=atdt (253b7b9d-72bb-4cee-823f-a422acabc03f) fuente=api_93ca5e1c_2026-10-24.json sha=97bcc5d6f7f7068c2ecfb1fab2be0cdc00fbab48f47cf84ce95f2a7a4354f465 casos=V13
- ND-06 org=atdt (253b7b9d-72bb-4cee-823f-a422acabc03f) fuente=api_caf587a5_2026-10-24.json sha=3ac8a95ddb372a1df97a9c8acec9defbaf917662ec58fb6eff52762c98ee926d casos=V14
- ND-07 org=sp (e798580f-d450-42ed-9302-ffb1630ecc7e) fuente=api_package_show_2026-10-24.json sha=e751fe481af047f3ffa6facc57c9d04952e5f874186be2d2fb4a6ae20f9a0154 casos=https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177,https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178,des_mpo_res
- PQ<->ND: PQ-01->ND-01 (V01-V04); PQ-02->ND-02 (V05); PQ-03->ND-03 (V06-V08); PQ-04->ND-04 (V09,V10,V11,V12,V15,V16); PQ-05->ND-05 (V13); PQ-06->ND-06 (V14); PQ-07->ND-07 (2 IRIs + des_mpo_res).
- SHA256 internos de la fuente: 12 campos `sha256` presentes, todos de 64 hex [0-9a-f] (verificado por codigo).
- SHA256 completo del archivo fuente/copia: `8c180f57898b5e83826d14d69037c353d2bb1dd5bbd9c12ecd2ebab21b7333c4` (20562 bytes), coincidente con `congelada.json` de v002. Copia verificada byte-identica.
- Resultado: sin errores de trazabilidad detectados en IDs / organismo primario (metadato result.organization) / casos / SHA. Si lo hubiera, se alertaria aqui y no se inventaria.
- Exclusion mutua: `preguntas-documentales.json/md` (entrega) y `congelada.json` (manifiesto) se excluyen entre si: la entrega no lista al manifiesto y el manifiesto no se incluye a si mismo.

## Necesidades (texto EXACTO de la fuente)
### ND-01 — org primario `uth` / `Universidad Tecnologica de Hermosillo` / `f353bb81-d268-40cd-aa74-d3f53402189a` — casos: V01, V02, V03, V04
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-uth-presas/evidencia/api_package_V01_403912fd-5853-4e18-8256-f77206f855bd_2026-10-24.json` sha256 `84b12a9a43b94bc6dc808af9f21bc7ea441847a18b46234a4b646887cd301707` localizador: result.organization {name: uth, title, id: f353bb81-d268-40cd-aa74-d3f53402189a}
faceta: F4: adopcion del publicador con rango de aplicacion por conjunto y periodo (F3 acreditada por el documento INEGI)
documento_pedido (EXACTO): Cualquier cadena documental primaria suficiente del publicador (oficio, lineamiento, nota de version del conjunto u otra) que cite edicion CMPE 2016 + recurso + periodos exactos del caso. No se exige carta especial.

### ND-02 — org primario `sagarhpa` / `Secretaria de Agricultura, Ganaderia, Recursos Hidraulicos, Pesca y Acuacultura` / `e563936a-2a3c-4f0b-a2d9-203dac8229a8` — casos: V05
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-uth-presas/evidencia/api_package_V05_ee8f639f-5e89-46ae-93b9-934b05fc6233_2026-10-24.json` sha256 `2776b9297d47743ea0e18888e03e0a27bb1e7cd778375ada435c6f470472e625` localizador: result.organization {name: sagarhpa, id: e563936a-2a3c-4f0b-a2d9-203dac8229a8}
faceta: F3+F4: edicion/version/fecha del Catalogo_estatal + vinculo con 1941-2024; constancia del recurso 1960-1969 (url vacia en API)
documento_pedido (EXACTO): Declaracion del publicador con edicion/version/fecha del Catalogo_estatal (rango 1941-2024) + URL efectiva de descarga del recurso 4d1bb645-19da-407f-8182-b0be2d7b7485.
nota_trazabilidad (EXACTA): DEP-CAT-R6-02 es codigo interno de tarea, no institucion; no figura como organismo.

### ND-03 — org primario `sp` / `Secretaria de Salud Publica` / `e798580f-d450-42ed-9302-ffb1630ecc7e` — casos: V06, V07, V08
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-salud/evidencia/api_package_show_2026-10-24.json` sha256 `e751fe481af047f3ffa6facc57c9d04952e5f874186be2d2fb4a6ae20f9a0154` localizador: result.organization {name: sp, id: e798580f-d450-42ed-9302-ffb1630ecc7e}
faceta: F3+F4 por hoja x 2022-2024
documento_pedido (EXACTO): Declaracion del publicador de edicion/version/fecha del catalogo por hoja con vinculo 2022-2024, mas fe de erratas o diccionario corregido.

### ND-04 — org primario `coespo` / `Consejo Estatal de Poblacion` / `80c1c21d-31ff-4562-97ef-9c1666e2e464` — casos: V09, V10, V11, V12, V15, V16
organismo_fuente: `propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/V3-coespo/trabajo/fuentes/api-package-0b5f5e16.json` sha256 `4ca156b4619b9bcc9d69b6ced3cc3ed4b1b07e586c674acdfc3f907304bc6749` localizador: result.organization {name: coespo, id: 80c1c21d-31ff-4562-97ef-9c1666e2e464} (verificado en los 3 package_show: 0b5f5e16, 943d0723, 960ef0a9)
faceta: F3+F4 por hoja x periodos + desfase de corte vs CONAPO 09-05-2024 (local 1990-2019/2020-2040 vs CONAPO 1990-2020/2021-2040)
documento_pedido (EXACTO): Declaracion del publicador con edicion/version/fecha + recurso + periodos + fecha/firma + aclaracion del desfase de corte. No transferir vigencia del documento CONAPO al catalogo local.
nota_trazabilidad (EXACTA): DEP-CAT-R6-04 es codigo interno de tarea, no institucion.

### ND-05 — org primario `atdt` / `Agencia de Transformacion Digital y Telecomunicaciones` / `253b7b9d-72bb-4cee-823f-a422acabc03f` — casos: V13
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-seguridad/evidencia/api_93ca5e1c_2026-10-24.json` sha256 `97bcc5d6f7f7068c2ecfb1fab2be0cdc00fbab48f47cf84ce95f2a7a4354f465` localizador: result.organization {name: atdt, id: 253b7b9d-72bb-4cee-823f-a422acabc03f}; SESNSP solo aparece en fuentes_extras como URL citada, no como publicador
faceta: F3+F4 + acceso no resuelto al XLSX del Diccionario SESNSP por las vias examinadas (W-v003 definitivo)
documento_pedido (EXACTO): Declaracion del publicador con edicion/version/fecha y corte de cat_municipio x 2015-2025 + copia legible del Diccionario aportada por el publicador. No reintentar descarga/token por las vias agotadas.
nota_trazabilidad (EXACTA): DEP-CAT-R6-05 es codigo interno de tarea. SESNSP es fuente citada en fuentes_extras, no publicador declarado.

### ND-06 — org primario `atdt` / `Agencia de Transformacion Digital y Telecomunicaciones` / `253b7b9d-72bb-4cee-823f-a422acabc03f` — casos: V14
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-seguridad/evidencia/api_caf587a5_2026-10-24.json` sha256 `3ac8a95ddb372a1df97a9c8acec9defbaf917662ec58fb6eff52762c98ee926d` localizador: result.organization {name: atdt, id: 253b7b9d-72bb-4cee-823f-a422acabc03f}; SESNSP solo aparece en fuentes_extras como URL citada, no como publicador
faceta: F3+F4 + acceso no resuelto al XLSX del Diccionario SESNSP por las vias examinadas (W-v003 definitivo)
documento_pedido (EXACTO): Declaracion del publicador con edicion/version/fecha y corte de cat_entidad x 2015-2025 + copia legible del Diccionario aportada por el publicador. No reintentar descarga/token por las vias agotadas.
nota_trazabilidad (EXACTA): DEP-CAT-R6-05 es codigo interno de tarea. SESNSP es fuente citada en fuentes_extras, no publicador declarado.

### ND-07 — org primario `sp` / `Secretaria de Salud Publica` / `e798580f-d450-42ed-9302-ffb1630ecc7e` — casos: https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177, https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178, des_mpo_res
organismo_fuente: `propuestas/cierre-brechas-post-r6/vigencias-salud/evidencia/api_package_show_2026-10-24.json` sha256 `e751fe481af047f3ffa6facc57c9d04952e5f874186be2d2fb4a6ae20f9a0154` localizador: result.organization {name: sp, id: e798580f-d450-42ed-9302-ffb1630ecc7e}; inventario: 5 recursos, version null
faceta: Filas 177/178 corruptas fuera de los 138 + des_mpo_res sin catalogo aplicable en inventario cerrado
documento_pedido (EXACTO): Fe de erratas o diccionario corregido que aclare filas 177/178 y, SOLO si confirma catalogo aplicable a des_mpo_res 2022-2024, su URL con edicion/fecha (si declara que no existe, basta la fe de erratas).

## Preguntas (texto EXACTO de la fuente)
### PQ-01 -> ND-01 — casos: V01, V02, V03, V04
pregunta (EXACTA): Pedir al publicador cualquier cadena documental primaria suficiente (oficio, lineamiento, nota de version del conjunto u otra) que adopte la CMPE 2016 para cada conjunto, citando recurso y periodos exactos del caso.
criterio_aceptacion (EXACTO): Documento del publicador con edicion CMPE 2016 + recurso (UUID) + periodos exactos, verificable por URL o copia local con SHA. Sin esto: conservar brecha, sin afirmar vigencia.

### PQ-02 -> ND-02 — casos: V05
pregunta (EXACTA): Pedir declaracion de edicion/version/fecha del Catalogo_estatal (conjunto ee8f639f-5e89-46ae-93b9-934b05fc6233, recurso f5060479-ee16-49b5-99d4-09aabef8042e, rango 1941-2024) y URL efectiva de descarga del recurso 4d1bb645-19da-407f-8182-b0be2d7b7485.
criterio_aceptacion (EXACTO): Declaracion + URL efectiva verificables (URL viva o copia local con SHA); el texto generico de plantilla HTML no cuenta.

### PQ-03 -> ND-03 — casos: V06, V07, V08
pregunta (EXACTA): Pedir declaracion de edicion/version/fecha del catalogo Rickettsia (recurso 08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8) por hoja con vinculo 2022-2024, mas fe de erratas o diccionario corregido.
criterio_aceptacion (EXACTO): Documento que cite hoja + recurso + periodos 2022-2024, verificable; fechas de carga del portal excluidas como prueba.

### PQ-04 -> ND-04 — casos: V09, V10, V11, V12, V15, V16
pregunta (EXACTA): Pedir declaracion del publicador de edicion/version/fecha de catalogo.xlsx por hoja (Municipios/CLAVE, Estado/CLAVE_ENT) con conjunto/recurso y periodos, mas aclaracion del desfase de corte vs CONAPO 09-05-2024.
criterio_aceptacion (EXACTO): Declaracion con fecha/firma que cite catalogo + recurso (UUID) + periodos + aclaracion de corte; no transferir vigencia del documento CONAPO al catalogo local.

### PQ-05 -> ND-05 — casos: V13
pregunta (EXACTA): Pedir declaracion del publicador de edicion/version/fecha y corte de cat_municipio (recurso 36d3ac85-4327-41f5-9259-538a7723a0ae) x 2015-2025, y copia legible del Diccionario aportada por el publicador.
criterio_aceptacion (EXACTO): Declaracion + copia legible verificables; no reintentar descarga/token por las vias agotadas (W-v003 definitivo); conservar acceso_no_resuelto hasta entonces.

### PQ-06 -> ND-06 — casos: V14
pregunta (EXACTA): Pedir declaracion del publicador de edicion/version/fecha y corte de cat_entidad (recurso 7f3aca28-4251-48b8-a759-69c992580744) x 2015-2025, y copia legible del Diccionario aportada por el publicador.
criterio_aceptacion (EXACTO): Declaracion + copia legible verificables; no reintentar descarga/token por las vias agotadas (W-v003 definitivo); conservar acceso_no_resuelto hasta entonces.

### PQ-07 -> ND-07 — casos: https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177, https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178, des_mpo_res
pregunta (EXACTA): Pedir fe de erratas o diccionario corregido (conjunto 5494daa1-09ca-4750-aeac-2558553700e1, recurso 33d0a99e-c721-496f-a05e-07646e9ae42a) que aclare filas 177/178 y el estado de des_mpo_res (si existe catalogo aplicable 2022-2024, su URL con edicion/fecha; si no existe, declararlo).
criterio_aceptacion (EXACTO): Fe de erratas/diccionario del publicador verificable; no crear vinculo catalogoRecuperado por coincidencia de nombre; EXC-ENC-177/178 no cuentan como significados nuevos.

