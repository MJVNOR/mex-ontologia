# C4-referencias — entrega v002 (corrige tabla documental de v001; v001 preservada)

Fecha UTC: 2026-10-24T10:26:22.162062+00:00 · Modelo: opencode-go/muse-spark-1.3-contributor · MCP nativo OpenCode.
Base R8: reports/ronda-8.json sha 5ac384bc (cerrado_integrado_validado_y_sincronizado).

## Resultado (sin cambios respecto a v001)
- 19/19 casos cubiertos: 16 vigencias + 3 anomalias. 104/104 evidencias verificadas por codigo, intactas (sin re-derivacion).
- 0 propuestas para integrar. Se conservan: 138 significados reales (2 headers corruptos fuera), V13/V14 acceso_no_resuelto, des_mpo_res sin catalogo.
- 7 agrupaciones documentales (ND-01..ND-07) y 7 preguntas preparadas sin envio (PQ-01..PQ-07).

## Correcciones v002 (ruido material de v001)
- ND-01: eliminado el fragmento borroso '612b2b11(no; presas)' del campo de recurso (pertenece a ND-02/V05, no a V01-V04); recursos ahora por conjunto con UUID completo + periodos en `conjuntos[]`; CMPE con archivo y SHA-256 completo calculado por codigo.
- ND-02: organismo corregido a sagarhpa (metadato result.organization de la API package, fuente primaria CKAN); 'UTH/DEP-CAT-R6-02' retirado de organismo — UTH era inferencia por nombre del rol y DEP-CAT-R6-02 es codigo interno de tarea (ver nota_trazabilidad). Recurso del hueco con UUID completo 4d1bb645-19da-407f-8182-b0be2d7b7485 (antes solo prefijo).
- ND-03/ND-07 y ND-04/ND-05/ND-06: organismo fijado al metadato exacto result.organization (sp / coespo / atdt con organization_id); DEP-CAT-* movidos a nota_trazabilidad; SESNSP queda como fuente citada en fuentes_extras, no como publicador.
- Criterio PQ-01 (y resto): admite cualquier cadena documental primaria suficiente; eliminada la exigencia de 'carta especial'.
- ND-07: casos con IDs completos (IRIs de asignacion), no truncados '.../177'.
- 104 evidencias de casos[] intactas de v001 (sin re-derivacion); solo cambia la tabla documental (necesidades/preguntas) y sus criterios.

## Tabla documental corregida (resumen)
- ND-01 org=uth (f353bb81-d268-40cd-aa74-d3f53402189a) casos=V01,V02,V03,V04
- ND-02 org=sagarhpa (e563936a-2a3c-4f0b-a2d9-203dac8229a8) casos=V05
- ND-03 org=sp (e798580f-d450-42ed-9302-ffb1630ecc7e) casos=V06,V07,V08
- ND-04 org=coespo (80c1c21d-31ff-4562-97ef-9c1666e2e464) casos=V09,V10,V11,V12,V15,V16
- ND-05 org=atdt (253b7b9d-72bb-4cee-823f-a422acabc03f) casos=V13
- ND-06 org=atdt (253b7b9d-72bb-4cee-823f-a422acabc03f) casos=V14
- ND-07 org=sp (e798580f-d450-42ed-9302-ffb1630ecc7e) casos=https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F177,https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F178,des_mpo_res

## Criterio general
Aceptar solo documento primario que respalde campo + recurso (UUID) + edicion/periodo exactos del caso, verificable por URL o copia local con SHA. Admite cualquier cadena documental primaria suficiente; no exige carta especial. Negativo limitado a lo examinado.

## Peticiones web
Ninguna (v002/peticiones-web.json con lista vacia y motivo). Sin contactos, sin nueva busqueda, sin tocar produccion.
