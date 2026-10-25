# Vigencias COESPO — entrega 2026-10-24 (6/6 siguen pendientes)

Tarea `vigencias-coespo`, tipo `vigencias`. Detalle serializado: `entrega.json`
(generado con `json.dumps`; IDs exactos de `asignacion.json`, sin duplicados).

## V09 — Catalogo_Municipios/CLAVE, 1990-2019 + 2020-2040 → sigue_pendiente
Pistas nuevas (página COESPO Proyecciones; publicación COESPO 11-07-2024; recurso
d7c4b8b2) no declaran edición/versión/fecha de catalogo.xlsx (sha `ea54aad3…`)
ni vínculo con los periodos. Falta: declaración del publicador con edición,
recurso `de5c06c7…` y periodos + aclaración del desfase vs CONAPO 09-05-2024.

## V10 — Catalogo_Estado/CLAVE_ENT, 1990-2019 + 2020-2040 → sigue_pendiente
Mismo archivo y motivo que V09 para la hoja Catalogo_Estado. Falta: declaración
con recurso `de5c06c7…` y periodos.

## V11 — Catalogo_Municipios/CLAVE (conj. 943d0723), 1990-2019 + 2020-2040 → sigue_pendiente
Mismo archivo compartido (sha `ea54aad3…`); sin declaración de edición ni
vínculo (conjunto 943d0723). Falta: declaración con recurso `d7c4b8b2…`.

## V12 — Catalogo_Estado/CLAVE_ENT (conj. 943d0723), 1990-2019 + 2020-2040 → sigue_pendiente
Igual que V11 para Catalogo_Estado. Falta: declaración con recurso `d7c4b8b2…`.

## V15 — Catalogo_Municipios/CLAVE (conj. 960ef0a9), 1990-2040 → sigue_pendiente
Sin declaración de edición del catálogo; F4 ausente para 1990-2040. Falta:
declaración con recurso `e0d2acc2…` y periodo 1990-2040.

## V16 — Catalogo_Estado/CLAVE_ENT (conj. 960ef0a9), 1990-2040 → sigue_pendiente
Igual que V15 para Catalogo_Estado. Falta: declaración con recurso `e0d2acc2…`.

## Novedades frente a investigación previa
Nuevas (2026-10-24, fuera de W01-W09 y R6-C1/C2): página COESPO y publicación
11-07-2024 — contexto F3 parcial de la fuente de DATOS, negativas para el
documento exacto. Re-verificado sin novedad: dataset CKAN, metadatos de portal,
interior xlsx. Conteo 2475 = procedencia, no vigencia. Nada conocido presentado
como nuevo.

## Límites
Sin joins ni identidad de catálogos automática; sin transferir vigencia CONAPO
al catálogo local; fechas de portal/API excluidas por criterio; error HTTP 404
de una variante de URL no confundido con inexistencia; sin contacto externo.
