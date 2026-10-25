# Agente 8 — Educación (cobertura-muse-20261023)

126 definiciones asignadas revisadas fila por fila contra copias congeladas
(SHA verificados contra `fuentes/manifiesto.json`): 99 propuestas con regla,
27 pendientes con motivo. 66 conceptos nuevos estrechos, 1 reutilización
(`programa-educativo`). 20 reglas con calificador de sede basado en literal;
el integrador los propagará al RDF.

Unidades y medidas: conteos con objeto literal de la descripción, sin tasas
ni porcentajes; edad sin unidad declarada (sin afirmar años); promedios sin
rango afirmado; sin monetarios. Poblaciones, eventos y sexos separados por
concepto; egreso≠titulación; nacimiento≠nacionalidad. Sin vigencia inferida,
sin identidad municipal, sin catálogos promovidos, sin correspondencias
columna-variable, sin sameAs/exactMatch.

Las 232 respaldadas y 23 candidatas centrales se preservan (simulación en
memoria sin cambios centrales). Conteos recalculados desde contenido:
decisiones=126, proponer=99, pendiente=27, reglas=99, conceptos_nuevos=66.

Ajuste auditor 11 + integrador: r3a8-034 (Nacionalidad) con representación
no afirmada (tipo Texto y ejemplo vacío no demuestran nombre ni código);
r3a8-013/017/081 (campo de formación) documentados como código por tipo,
ejemplo y catálogo publicado, sin validar valores ni equiparar 7 con 07.

Ajuste auditoría-b: r3a8-080 (Modalidad) y r3a8-082 (Grado) con definiciones
neutralizadas al literal, sin sujeto/población añadida ni calificador
inferido; dominio textual y límites intactos.

Reproducir (solo lee fuera de esta carpeta, sin red):
```powershell
uv run python propuestas/cobertura-muse-20261023/educacion/scripts/construir.py
$env:PYTHONDONTWRITEBYTECODE='1'
uv run python propuestas/cobertura-muse-20261023/educacion/scripts/verificar.py
```
