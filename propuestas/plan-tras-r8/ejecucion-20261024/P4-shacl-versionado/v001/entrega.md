# P4-shacl-versionado v001

Piloto de diseno (0 casos asignados): exclusion documentado/candidato + versionado. Estado: propuesta_para_auditar.
Motor real open-ontologies en stores aislados (sin Studio), via scripts/construir_catalogo.motor:
| fixture | esperado | conforms | violaciones | filas con ambos |
| --- | --- | --- | --- | --- |
| fixtures/fixture-neither.ttl | True | True | 0 | 0 |
| fixtures/fixture-doc.ttl | True | True | 0 | 0 |
| fixtures/fixture-cand.ttl | True | True | 0 | 0 |
| fixtures/fixture-both.ttl | False | False | 1 | 1 |

Operador: sh:sparql (determinado). Evitados sh:not/sh:xone (no implementados en el evaluador por defecto; xone ademas prohibiria NEITHER).
--verified no disponible en el exe distribuido (bloqueo honesto, no simulado).
No se toca produccion/shapes centrales/manifiestos/grafo/Studio. Versionado: format_version (esquema entrega) separado de release (ronda).
Navegador no usado; sin peticiones-web.json.
