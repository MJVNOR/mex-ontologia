# Pares estructurales con significado pendiente

La revisión posterior a R6 documentó 20 asociaciones entre columnas físicas y filas de sus diccionarios. La evidencia por caso combina la publicación del diccionario y los datos en el mismo conjunto, el nombre y ordinal de la columna y la fila, y las huellas de los archivos y registros inspeccionados. Los expedientes incluyen matrices de alineación; los límites y diferencias se conservan en cada revisión.

Estas asociaciones se guardan en [el registro documental separado](../data/revision-estructural-post-r6/revisiones.json), con estado `par_estructural_revisado_significado_pendiente`. Cada entrada enlaza la evidencia del par y la brecha semántica que sigue abierta.

## Relación con el núcleo

`documental_revisada` en la capa semántica exige además una variable con estado `respaldada_por_definicion`. La asociación física no satisface por sí sola ese requisito. Por ello, el registro estructural no se incorpora a `vinculos_documentales_revisados` ni cambia los conteos semánticos de R6: 4475 revisadas y 20 candidatas.

El nuevo registro no es consumido por la generación semántica. No aprueba conceptos, interpretaciones de códigos, vigencias históricas, identidad entre catálogos ni cruces entre filas. Tampoco corrige las contradicciones del diccionario original: por ejemplo, la descripción de `Total_Egresos` continúa pendiente de aclaración.

## Fuentes y reproducción

- [Informe de revisión completa](../reports/cierre-brechas-post-r6.md).
- [Auditoría independiente de los 20 pares](../propuestas/cierre-brechas-post-r6/auditoria-correspondencias/dictamen.json).
- [Investigación con OpenCode y Obscura](investigacion-opencode-obscura.md).
- Generación del registro y el informe: `uv run python propuestas/cierre-brechas-post-r6/consolidar.py`. El proceso comprueba los originales, las fuentes fijadas y la aprobación por identificador antes de escribirlos.
