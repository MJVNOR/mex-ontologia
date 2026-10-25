# V3-coespo — nota de primera puerta (2026-10-24)

Alcance: V09–V12, V15–V16. Criterio común: declaración del publicador con
edición/versión/fecha de catalogo.xlsx (sha ea54aad3) + recurso + periodos.
Fechas de portal/API y core-properties excluidas por el criterio.

## Pistas nuevas investigadas hoy (herramientas independientes, sin Obscura)

1. Re-verificación API CKAN `package_show` de los 3 conjuntos (2026-10-24,
   `trabajo/fuentes/api-package-*.json`): `version=null` en los tres,
   Catalogo size 83769 (= local ea54aad3), placeholder 1989-06-04.
   Cambio_de_fuente_por_comprobar verificado SIN cambio respecto a R6-C1.
2. Interior de los 3 recursos Diccionario (documentos concretos nunca
   examinados en R5/R6/post-R6; `trabajo/fuentes/diccionario-*.xlsx`,
   sha 07a21407…, c439f577…, 33864ebc…): diccionarios de variables del
   recurso de DATOS; CLAVE/CLAVE_ENT remiten a "Municipios"/"Estados" y a la
   clasificación INEGI (procedencia, no vigencia). Ninguno declara
   edición/versión/fecha de catalogo.xlsx, cita recurso de catálogo
   (de5c06c7/d7c4b8b2/e0d2acc2) ni periodos de aplicación.
   Pista_nueva investigada con resultado NEGATIVO para el documento exacto.
3. `package_revision_list` (historial de versiones): API deshabilitada
   (HTTP 400). Sin historial accesible; no prueba inexistencia.

## Puerta por ID

- V09, V10 (conj. 0b5f5e16, rec. de5c06c7): pista_nueva = diccionario
  03a33e71 (negativo) + API sin cambio → brecha_externa.
- V11, V12 (conj. 943d0723, rec. d7c4b8b2): pista_nueva = diccionario
  1b6d0817 (negativo) + API sin cambio → brecha_externa.
- V15, V16 (conj. 960ef0a9, rec. e0d2acc2): pista_nueva = diccionario
  f1bbd13b (negativo) + API sin cambio → brecha_externa.

No se repitieron búsquedas genéricas (páginas COESPO, dataset quinquenales,
metadatos de recurso, interior xlsx: ya agotadas en antecedentes).
No se propone documental_revisada: sin definición/edición respaldada.
Anexos COESPO (DICCIONARIO_DATOS_2023_v3_07082023.pdf,
NotaMetodologica2010-2030.pdf, de otros productos/periodos) no examinados;
quedan como reapertura opcional, no como petición (baja plausibilidad,
pedir su extracción sería aparentar avance).
Paquete W-web pendiente al cierre local; sin dependencia bloqueante:
las pistas al alcance ya se agotaron con herramientas independientes.
