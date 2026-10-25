# M2-sinac v003 — 14 correspondencias nuevas SINAC (propuestas para auditar)

Corrige v002 (descripcion adoptaba el descriptor nacional; v001/v002 intactas). Descripcion = literal local exacto.
Rol M2-sinac: ultimas 14 correspondencias nuevas SINAC; evidencia fisica y significado R7 exactos. Modelo opencode-go/muse-spark-1.3-contributor.

## Resultado

- 14/14 casos verificados como correspondencia formal suficiente: propuesta_para_auditar. 0 brechas, 0 accesos no resueltos.
- Vinculos propuestos con formato ontologia/semantica.json.vinculos_documentales_revisados (columna, campo, recurso, diccionario, definicion_iri, concepto, descripcion, huella_esquema, huella_fila_diccionario, criterio). Sin reglas ni conceptos nuevos.
- Significado ya respaldado en R7 (S2-nacimientos v002, auditoria A/B pendiente); aqui solo se acredita el alcance fisico columna<->fila.
- Expediente R7 revisado (cierre, paquetes W-web v001-v004, S2 v002, reports/ronda-7.json/md): sin busquedas genericas repetidas. Sin pista primaria nueva: no se escribe peticiones-web.json (solo W usa Obscura).

## Pruebas verificables (por caso)

1. Nombre unico en los 106 campos de la hoja SINAC 2022 26-09-22 y en las 106 filas del diccionario; ordinal columna = posicion_original y fila = indice; nombre exacto en ambos.
2. huella_esquema = 9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95 y huella_fila recomputadas por codigo coinciden con R7.
3. cobertura-r7.json: variable en estado respaldada_por_definicion con mismo concepto, regla, definicion_iri, descripcion y huella; correspondencia en estado candidata_por_nombre con variable exacta, sin revision previa.

## Decisiones

| # | Campo (pos) | Variable (fila) | Concepto / regla | Estado |
| --- | --- | --- | --- | --- |
| 1 | VITAMINA_A (65) | 65 | sinac-vitamina-a / r7-s2-065 | propuesta_para_auditar |
| 2 | VITAMINA_K (67) | 67 | sinac-vitamina-k / r7-s2-067 | propuesta_para_auditar |
| 3 | PRODUCTOEMBARAZO (69) | 69 | sinac-productoembarazo / r7-s2-069 | propuesta_para_auditar |
| 4 | ORDENPRODUCTO (71) | 71 | sinac-ordenproducto / r7-s2-071 | propuesta_para_auditar |
| 5 | TOTALPRODUCTOS (72) | 72 | sinac-totalproductos / r7-s2-072 | propuesta_para_auditar |
| 6 | CODIGOCIEANOMALIA1 (74) | 74 | sinac-codigocieanomalia1 / r7-s2-074 | propuesta_para_auditar |
| 7 | CODIGOCIEANOMALIA2 (76) | 76 | sinac-codigocieanomalia2 / r7-s2-076 | propuesta_para_auditar |
| 8 | RESOLUCIONEMBARAZO (77) | 77 | sinac-resolucionembarazo / r7-s2-077 | propuesta_para_auditar |
| 9 | UTILIZOFORCEPS (79) | 79 | sinac-utilizoforceps / r7-s2-079 | propuesta_para_auditar |
| 10 | TIEMPOTRASLADO (84) | 84 | sinac-tiempotraslado / r7-s2-084 | propuesta_para_auditar |
| 11 | PERSONALATENDIO (87) | 87 | sinac-personalatendio / r7-s2-087 | propuesta_para_auditar |
| 12 | TIPOMEDICOATENDIO (89) | 89 | sinac-tipomedicoatendio / r7-s2-089 | propuesta_para_auditar |
| 13 | CERTIFICADOPOR (97) | 97 | sinac-certificadopor / r7-s2-097 | propuesta_para_auditar |
| 14 | CLUESCERTIFICA (99) | 99 | sinac-cluescertifica / r7-s2-099 | propuesta_para_auditar |

## Evidencia y SHA-256 (calculados por codigo)

| Archivo | SHA-256 |
| --- | --- |
| data/portal/contenido-inspeccion.json | 61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb |
| propuestas/ronda-8-paralela/ejecucion-20261024/cobertura-r7.json | 4627c2baaf9a54d99897c93ee76213eea9a27bedf20219cf3cceda3da5e03bfe |
| propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/v002/entrega.json | 2432f14513f11016dc9488188516d67e1be55a3f98e960a29c4fcc06e583e0f1 |
| asignacion.json | 6e45351db797a65d426875a01e17888d7f3cf8969821d58f313b08c687e88184 |
| reports/ronda-7.json | 197054973a25496ed30b393c566b689e43d6cf46d012f79e644cb0521a32d787 |

## Alcance y limites

- Cada afirmacion vale solo para el recurso 46977217-9396-4f9c-bddb-6616e82530b4 (hoja SINAC 2022 26-09-22) y la definicion local fijada; no autoriza otra edicion, adopcion global, totalidad de catalogos, equivalencias, joins ni vigencias.
- Descriptor y catalogos nacionales DGIS pertenecen al registro nacional, no al extracto Sonora; no se invocan como vinculo fisico.
- Congelada: correcciones solo en v004, sin editar v003.

