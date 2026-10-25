# Brechas de vigencia de catálogos V01–V16 + referencia des_mpo_res

Matriz local de documentos faltantes. Borrador local: sin envío, sin contactos externos, sin cambios al núcleo.
Fuente: `propuestas/pendientes-muse-r6/catalogos/entrega.json` (R6, 17 pendiente) + base R4 + `reports/solicitudes-publicador-ronda-5.*` + `reports/ronda-6.*`.
Detalle máquina: `brechas.json`. SHAs de fuentes en `brechas.json → fuentes_consultadas`.

**Conteos: 16 vigencias + 1 anomalía/referencia heredada = 17 casos, 17 pendientes, 0 propuestas al núcleo.**
Los periodos citados son declarados por títulos CKAN/notas (NO cobertura observada, NO vigencia acreditada).

**Presas:** resuelta solo como vínculo documental `cat_estatal/Clave → /4` (dictamen-presas, R6). Sin joins, sin identidad de dominios, sin vigencia. **V05 sigue pendiente.**

## A. UTH / CMPE 2016 — falta F4 (F3 acreditada: pdf `66ba2fd2…`, p.2/p.8)

xlsx `53bd5e97…` (Hoja1 / Campo de Formación Académica). R6-C1: `version=null` ×4, fechas placeholder 1989-06-04. R6-C2: creator Ramón Eduardo Sandoval.

- **V01** Promedio Académico (`403912fd…`, catálogo `6d561451…`) — periodos: 2022 C1-3, 2023 C1-3, 2024 C1-3, 2025 C1-3, 2026 C1. Doc: nota de adopción UTH de CMPE 2016 con ese rango. Criterio: documento UTH cita CMPE 2016 + recurso + periodos, verificable. Límite: no extender a otros conjuntos/periodos.
- **V02** Matrículas (`e5aad52d…`, catálogo `aaf0c6c1…`) — periodos: 2022 C1-3 … 2025 C1-3, 2026 C1-2. Doc/criterio/límite: igual que V01 con su rango.
- **V03** Titulados (`e7a3d62f…`, catálogo `0e69d911…`) — periodos: 2022–2025 anual. Doc: adopción UTH CMPE 2016 anual 2022-2025. Criterio/límite: idem.
- **V04** Egresados (`85ee0e2b…`, catálogo `af7a9aba…`) — periodos: 2022–2025 anual. Doc: idem V03. Límite extra: cobertura API 2016-01-01/2025-01-01 es cobertura manual, no adopción.

Campos mínimos (V01–V04): emisor UTH; edición CMPE 2016 vinculada al publicador; recurso catálogo; periodos; fecha/firma.

## B. Recursos Hídricos — faltan F3+F4

- **V05** Catálogo_estatal / Clave (conjunto `ee8f639f…`, recurso `f5060479…`, sha `612b2b11…`) — periodos: 1941-49 … 2020-24 por décadas. R6-C1: recurso 1960-1969 id `4d1bb645`, state active, size 541916, **url vacía** (constancia API del hueco). R6-C2: creator Admin. Doc: declaración edición/versión/fecha + vínculo por décadas + constancia 1960-1969. Criterio: documento cita edición + recurso + periodos, verificable. Límites: no joins por Clave; no extender; vínculo Presas /4 no acredita vigencia.

## C. Salud / Rickettsia — faltan F3+F4 (V06–V08); referencia sin recurso (des_mpo_res)

xlsx `3b8546ac…`. R6-C1: `version=null`, cobertura 2022-01-01/2026-12-31 (cobertura, no edición). R6-C2: creator openpyxl, created 2026-04-15 (export posterior a 2022-2024, sin versión).

- **V06** Catalogo Servicios / servic_atencion (conjunto `5494daa1…`, recurso `08d3b1a7…`) — 2022, 2023, 2024. Doc: edición/versión/fecha + vínculo 2022-2024.
- **V07** Catalogo rechazo / motiv_rech_ricket_sangre — idem V06 (misma hoja-archivo).
- **V08** Catalogo especie / ricket_especie — idem V06.
- **des_mpo_res** (anomalía/referencia heredada, NO vigencia y NO catálogo afirmado) — la variable genuina es la fila 7 del diccionario `33d0a99e…`: `des_mpo_res` = "Municipio donde reside el caso", Texto, catálogo vacío, ejemplo Hermosillo (texto libre). La supuesta referencia nace de las filas corruptas 177 (`…/177`, huella `4b17625c8fea607228fe4f2a790744687a6e8bc45a712f66d4833d6ac541da79`) y 178 (`…/178`, huella `b5dbcdf58fd1b6e4d87f2396986629d2aa2350d35f1c1291e59d3d79515a0f60`, 64 hex copiadas programáticamente de `reports/pendientes-ronda-5.json`): repiten encabezados como valores y su celda "des_mpo_res" es posición de columna, no referencia real (dictamen R6 diversos: artefacto_documental). Catálogo no identificado en inventario revisado (API 2026-10-23: Diccionario + Catalogo + 3 datos; xlsx `3b8546ac` sin ocurrencias) — no inexistencia universal. Vínculo: EXC-ENC-177/178 (`encabezados/exclusiones.json`), que no cuentan como significados nuevos. Doc: fe de erratas o diccionario corregido que aclare 177/178; URL del catálogo SOLO si el publicador confirma que existe (aplicable 2022-2024). Criterio: se cierra con la aclaración y, en su caso, URL con edición/fecha verificable; si declara que no existe, se archiva como anomalía aclarada. Límites: no usar la coincidencia con la fila 7; no crear vínculo catalogoRecuperado; no presentar existencia/vigencia de catálogo como hecho.

Campos mínimos (V06–V08): emisor Salud; edición/versión/fecha (hoja/campo, sha `3b8546ac`); recurso; periodos 2022-2024; fecha/firma.

## D. Proyecciones / CONAPO — faltan F3+F4 (F3 parcial citada, desfase de corte)

xlsx `ea54aad3…` compartido en 3 conjuntos. R6-C1: `version=null` ×3, fuentes_extras CONAPO confirmadas sin edición del xlsx. R6-C2: creator Estephania Pivac Alcaraz 2024-09-02, sin versión. Desfase: local 1990-2019/2020-2040 vs CONAPO 1990-2020/2021-2040 (09-05-2024).

- **V09** Catalogo_Municipios / CLAVE, Grupos quinquenales (`0b5f5e16…`, recurso `de5c06c7…`) — reconstrucción 1990-2019 + proyecciones 2020-2040 + aclarar desfase.
- **V10** Catalogo_Estado / CLAVE_ENT, mismo conjunto — idem sin desfase (mismo archivo).
- **V11** Catalogo_Municipios / CLAVE, Grandes grupos (`943d0723…`, recurso `d7c4b8b2…`) — idem V09.
- **V12** Catalogo_Estado / CLAVE_ENT, mismo conjunto — idem V10.
- **V15** Catalogo_Municipios / CLAVE, Indicadores (`960ef0a9…`, recurso `e0d2acc2…`) — 1990-2040.
- **V16** Catalogo_Estado / CLAVE_ENT, mismo conjunto — 1990-2040.

Doc (D): declaración edición/versión/fecha + vínculo a reconstrucción/proyecciones + aclaración del desfase vs CONAPO. Criterio: documento COESPO cita edición + recurso + periodos + corte aclarado, verificable. Límite: no transferir vigencia del documento CONAPO al catálogo local.

## E. Delictivos / SESNSP — faltan F3+F4 (procedencia declarada, sin edición/corte)

- **V13** cat_municipio / Cve. Municipio (conjunto `93ca5e1c…`, recurso `36d3ac85…`, sha `84bb6fcd…`) — 2015–2025. R6-C1: fuentes_extras SESNSP confirmadas. R6-C2: creator SESNSP 2015-06-05. Doc: edición/versión/fecha y corte SESNSP + vínculo 2015-2025. Límites: no extender; no joins por Clave.
- **V14** cat_entidad / Clave_Ent (conjunto `caf587a5…`, recurso `7f3aca28…`, sha `96776ca8…`) — 2015–2025. R6-C2: creator Practicante2 2026-01-22. Doc/límite: idem V13.
