# Dictamen — auditoría correspondencias-a/b (20 casos)

Veredicto: **aceptar SOLO registro separado**. Detalle máquina en `dictamen.json` (`resoluciones_estructurales_aprobadas` 20/20, `resoluciones_aprobadas` [], `defectos` [], `defectos_resueltos` 21, referencias con SHA-256 refrescados).

## Invariante

`scripts/consolidar_semantica.py:271` intacto (sin adaptar): `documental_revisada` exige `respaldada_por_definicion`. Aceptación solo de `par_estructural_revisado_significado_pendiente`.

## Cambios verificados

- 20/20 campos activos en estado separado, sin concepto en propuesta, significado pendiente, sin cambio semántico.
- `alineacion.json` fila por fila: SINAC 106/106, denuncias 9/9, matrículas 68/70 + 2 diferencias honestas (pos 21/32, ajenas), SEED 80/80, egresos 15/15.
- Derivados recategorizados a contexto; historial de propuesta rechazada preservado (menciones restantes inactivas).
- SHAs recomputados; base fijada intacta.

## Efecto

Coordinador creará `data/revision-estructural-post-r6/revisiones.json` tras esta aprobación; no consumido por `consolidar_semantica`. Sin joins, vigencia, codebook ni fe de erratas.
