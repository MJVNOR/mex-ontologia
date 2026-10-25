# C4-referencias — entrega v001 (auditoria derivada, sin evidencia para integrar)

Fecha UTC: 2026-10-24T10:04:39.041338+00:00 · Modelo: opencode-go/muse-spark-1.3-contributor · MCP nativo OpenCode.
Base R8: reports/ronda-8.json sha 5ac384bc (cerrado_integrado_validado_y_sincronizado).

## Resultado
- 19/19 casos cubiertos: 16 vigencias + 3 anomalias. 104/104 evidencias verificadas por codigo (SHA-256 coincidente).
- 0 propuestas para integrar. Todo queda en sin_evidencia_para_integrar con su condicion exacta de reapertura.
- Se conservan: 138 significados reales (2 headers corruptos fuera), V13/V14 acceso_no_resuelto, des_mpo_res sin catalogo.

## Casos (puerta y detalle)
- V01 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V02 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V03 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V04 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V05 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V06 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V07 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V08 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V09 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V10 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V11 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V12 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V15 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V16 [vigencias] puerta=sin_pista_nueva detalle=brecha_externa
- V13 [vigencias] puerta=pista_nueva detalle=acceso_no_resuelto
- V14 [vigencias] puerta=pista_nueva detalle=acceso_no_resuelto
- https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177 [anomalias] puerta=sin_pista_nueva detalle=brecha_externa
- https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178 [anomalias] puerta=sin_pista_nueva detalle=brecha_externa
- des_mpo_res [anomalias] puerta=sin_pista_nueva detalle=brecha_externa

## Necesidades deduplicadas (7)
- ND-01 UTH casos=V01,V02,V03,V04 faceta=F4: adopcion UTH con rango por cuatrimestre/anual por conjunto
- ND-02 UTH/DEP-CAT-R6-02 (presas) casos=V05 faceta=F3+F4: edicion/version/fecha del Catalogo_estatal + vinculo 1941-2024 y URL descarga 1960-1969 (id 4d1bb645, url vacia)
- ND-03 Salud Sonora (Rickettsia) casos=V06,V07,V08 faceta=F3+F4 por hoja: Servicios/servic_atencion, rechazo/motiv_rech_ricket_sangre, especie/ricket_especie x 2022-2024
- ND-04 COESPO/DEP-CAT-R6-04 casos=V09,V10,V11,V12,V15,V16 faceta=F3+F4: Catalogo_Municipios/CLAVE y Catalogo_Estado/CLAVE_ENT x reconstruccion 1990-2019 / proyecciones 2020-2040 (V15/V16: 1990-2040) + desfase vs CONAPO 1990-2020/2021-2040
- ND-05 SESNSP/ATDT via publicador Sonora (seguridad) casos=V13 faceta=F3+F4: edicion/version/fecha y corte SESNSP de cat_municipio x 2015-2025; acceso XLSX Diccionario SESNSP no resuelto por estas vias
- ND-06 SESNSP/ATDT via publicador Sonora (seguridad) casos=V14 faceta=F3+F4: edicion/version/fecha y corte SESNSP de cat_entidad x 2015-2025; acceso XLSX Diccionario SESNSP no resuelto por estas vias
- ND-07 Salud Sonora (Rickettsia, anomalias) casos=.../177,.../178,des_mpo_res faceta=Filas 177/178 corruptas (huellas 4b17625c/b5dbcdf5) + des_mpo_res texto libre sin catalogo; inventario cerrado 5 recursos

## Preguntas preparadas sin envio (7: PQ-01..PQ-07)
Ver v001/matriz-preguntas.json. Criterio general: solo integra documento del publicador que cite campo+recurso+edicion/periodo exactos, verificable por URL o copia local con SHA. Negativo limitado a lo examinado.

## Peticiones web
Ninguna (v001/peticiones-web.json con lista vacia y motivo). Sin pista primaria concreta nueva.

## Limites y aceptacion
- Gemma excluido; sin contactos externos; preguntas preparadas sin envio.
- Escritura exclusiva en propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/. Sin tocar produccion/semantica/shapes centrales/manifiestos previos/grafo/Studio.
- Solo cotejo R8; sin investigacion generica repetida ni busquedas agotadas (W08 y re-descargas API/portal no son novedad).
- No inferir vigencia del nombre del archivo, titulos CKAN, conteos, cobertura manual ni fechas operativas de portal/API.
- No afirmar posesion exclusiva del documento; pedir carta especial si otra cadena formal primaria resuelve.
- V13/V14 conservan acceso_no_resuelto; 2 headers corruptos fuera de los 138; des_mpo_res sin vinculo catalogoRecuperado.
- Un resultado negativo se limita a lo examinado; no demuestra inexistencia universal.
