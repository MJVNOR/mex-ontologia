# M1-sinac v001 — 14 correspondencias nuevas SINAC (propuestas para auditar)

Rol M1-sinac: primeras 14 correspondencias nuevas SINAC; evidencia fisica y significado R7 exactos. Modelo opencode-go/muse-spark-1.3-contributor. Escritura exclusiva en M1-sinac; sin Gemma, sin mensajes externos, sin puentes ni CLI OpenCode.

## Resultado

- 14/14 casos verificados como correspondencia formal suficiente: propuesta_para_auditar. 0 brechas, 0 accesos no resueltos.
- Vinculos propuestos con formato ontologia/semantica.json.vinculos_documentales_revisados (columna, campo, recurso, diccionario, definicion_iri, concepto, descripcion, huella_esquema, huella_fila_diccionario, criterio). Sin reglas ni conceptos nuevos.
- Significado ya respaldado en R7 (S2-nacimientos v002, auditoria A/B pendiente); aqui solo se acredita el alcance fisico columna<->fila.
- Expediente R7 revisado (cierre, paquetes W-web v001-v004, S2 v002, reports/ronda-7.json/md): sin busquedas genericas repetidas. Sin pista primaria nueva: no se escribe peticiones-web.json (solo W usa Obscura).

## Pruebas verificables (por caso)

1. Nombre unico en los 106 campos de la hoja SINAC 2022 26-09-22 y en las 106 filas del diccionario; ordinal columna = posicion_original y fila = indice; nombre exacto en ambos.
2. huella_esquema = 9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95 y huella_fila recomputadas por codigo coinciden con R7.
3. cobertura-r7.json: variable en estado respaldada_por_definicion con mismo concepto y regla; correspondencia en estado candidata_por_nombre sin revision previa.

## Decisiones

| # | Campo (pos) | Columna | Variable (fila) | Concepto / regla | Estado |
| --- | --- | --- | --- | --- | --- |
| # | Campo (pos) | Variable (fila) | Concepto / regla | Estado |
| --- | --- | --- | --- | --- |
| 1 | ENTIDADFEDERATIVACERTIFICA (100) | 100 | sinac-entidadfederativacertifica / r7-s2-100 | propuesta_para_auditar |
| 2 | FECHACERTIFICADO (106) | 106 | sinac-fechacertificado / r7-s2-106 | propuesta_para_auditar |
| 3 | ORDENNACIMIENTO (31) | 31 | sinac-ordennacimiento / r7-s2-031 | propuesta_para_auditar |
| 4 | ATENCIONPRENATAL (32) | 32 | sinac-atencionprenatal / r7-s2-032 | propuesta_para_auditar |
| 5 | TRIMESTREPRIMERCONSULTA (34) | 34 | sinac-trimestreprimerconsulta / r7-s2-034 | propuesta_para_auditar |
| 6 | SOBREVIVIOPARTO (37) | 37 | sinac-sobrevivioparto / r7-s2-037 | propuesta_para_auditar |
| 7 | AFILIACION (39) | 39 | sinac-afiliacion / r7-s2-039 | propuesta_para_auditar |
| 8 | INTERRUMPIOESTUDIOS (43) | 43 | sinac-interrumpioestudios / r7-s2-043 | propuesta_para_auditar |
| 9 | CLAVEOCUPACIONHABITUAL (45) | 45 | sinac-claveocupacionhabitual / r7-s2-045 | propuesta_para_auditar |
| 10 | APGAR (57) | 57 | sinac-apgar / r7-s2-057 | propuesta_para_auditar |
| 11 | SILVERMAN (58) | 58 | sinac-silverman / r7-s2-058 | propuesta_para_auditar |
| 12 | TAMIZAUDITIVO (59) | 59 | sinac-tamizauditivo / r7-s2-059 | propuesta_para_auditar |
| 13 | VACUNA_BCG (61) | 61 | sinac-vacuna-bcg / r7-s2-061 | propuesta_para_auditar |
| 14 | VACUNAHEPATITIS_B (63) | 63 | sinac-vacunahepatitis-b / r7-s2-063 | propuesta_para_auditar |

## Evidencia y SHA-256 (calculados por codigo)

| Archivo | SHA-256 |
| --- | --- |
| data/portal/contenido-inspeccion.json | 61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb |
| propuestas/ronda-8-paralela/ejecucion-20261024/cobertura-r7.json | 4627c2baaf9a54d99897c93ee76213eea9a27bedf20219cf3cceda3da5e03bfe |
| propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/v002/entrega.json | 2432f14513f11016dc9488188516d67e1be55a3f98e960a29c4fcc06e583e0f1 |
| v001/entrega.json | daee9beb38cfeb8228784dfe93887dfb5fd49788afa007a0caf6fe489cf638ed |
| asignacion.json | ff5b87e01bb7f4e0cf8851886c3147764c8343d50b24b2b125334138a99c42d6 |
| reports/ronda-7.json | 197054973a25496ed30b393c566b689e43d6cf46d012f79e644cb0521a32d787 |

## Alcance y limites

- Cada afirmacion vale solo para el recurso 46977217-9396-4f9c-bddb-6616e82530b4 (hoja SINAC 2022 26-09-22) y la definicion local fijada; no autoriza otra edicion, adopcion global, totalidad de catalogos, equivalencias, joins ni vigencias.
- Descriptor y catalogos nacionales DGIS pertenecen al registro nacional, no al extracto Sonora; no se invocan como vinculo fisico.
- Congelada: correcciones solo en v002, sin editar v001.
