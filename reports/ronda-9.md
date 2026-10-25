# Ronda 9 — plan posterior a R8

Estado: cerrado, integrado, validado y sincronizado.

## Resultado

- Dos declaraciones de unidad cualificadas: milímetros y hectáreas, con términos QUDT verificados y literales de fuente conservados.
- Una regla SHACL impide que una variable tenga significado documentado y candidato simultáneamente; admite variables pendientes sin ninguno.
- Pilotos negativos de periodos e intervalos y de jerarquía clínica: no se incorporaron fechas ni relaciones por suposición. El hm³ permanece sin vínculo QUDT.
- **1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas.**
- **204 pruebas Python OK**, RDF y SHACL conformes.
- Portal: **322405 triples**. Studio: **323014 triples**, verificado y con ediciones ajenas preservadas.

## Auditorías y vistas de trabajo

Se trazaron las 17 candidatas y los 19 casos de vigencia/anomalía; se reconciliaron las 5523 columnas. La nueva prioridad de revisión cubre 1191 pares estructurales y presenta 50 primeros candidatos; no autoriza joins.

Las correcciones de propuestas anteriores —IRIs tentativas, sello autorreferente, hashes truncados, literales sin tildes y etiquetas de organismo— se conservan como antecedentes. Solo se instaló el material final aceptado.

## Pendientes externos

Quedan **138 significados, 16 vigencias y 17 candidatas** dependientes del respaldo documental faltante. V13/V14 mantienen acceso no resuelto; `des_mpo_res` no tiene catálogo aplicable identificado. Las dos filas corruptas de encabezado siguen conservadas, fuera del conteo de significados reales.

El chat solicitado revisó R8 y devolvió el plan que originó esta ejecución. Gemma quedó excluido y no se contactó a publicadores.

Detalle, hashes, pruebas, auditorías y recibos: [ronda-9.json](ronda-9.json).
