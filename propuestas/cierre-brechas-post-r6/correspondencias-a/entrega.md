# Correspondencias-a — registro separado ESTRUCTURAL (post-auditoría)

Dictamen `auditoria-correspondencias/dictamen.json`: **requiere_correccion** aplicado. Las 10 decisiones quedan en estado `par_estructural_revisado_significado_pendiente`, con `propuesta.estado_propuesto` igual, sin concepto aprobado, `estado_semantico_actual: candidata_por_nombre`, `significado: pendiente`. La propuesta anterior (`propuesta_resolucion`) se conserva solo en `historial/` como rechazada, sin efecto. NO aplicable a `vinculos_documentales_revisados` (el core exige `respaldada_por_definicion`; invariante no relajado).

## Base del par (estructural, sin semántica)

`package_show` fresco 2026-10-24 de los 3 conjuntos CKAN: Diccionario (pos 0) + archivo de datos (pos 1) co-publicados, con `numero_variables` declarado = conteo de columnas = conteo de filas (106/70/9). Detalle fila por fila en `alineacion.json` (esquema completo + fila completa por par, con SHA de fuentes primarias; distribuciones y reportes derivados tratados solo como contexto).

Conteos reales: SINAC 106/106 exactas (1:1 exacta); denuncias 9/9 exactas (1:1 exacta); matrículas 68/70 exactas + 2 diferencias solo-espacios del portal en pos 21 y 32, ajenas a los IDs asignados (NO se afirma 1:1 exacta ahí).

## Decisiones (10/10 par_estructural_revisado_significado_pendiente)

| # | Columna (pos) | Fila diccionario | Descripción fila |
|---|---|---|---|
| 1 | SINAC …/102 MUNICIPIOCERTIFICA | 22202305…/102 | Pendiente de especificar |
| 2 | SINAC …/103 MUNICIPIOCERTIFICAD | 22202305…/103 | Pendiente de especificar |
| 3 | SINAC …/104 LOCALIDADCERTIFICA | 22202305…/104 | Pendiente de especificar |
| 4 | SINAC …/105 LOCALIDADCERTIFICAD | 22202305…/105 | Pendiente de especificar |
| 5 | SINAC …/83 CLUES | 22202305…/83 | Pendiente de especificar |
| 6 | Denuncias …/2020/2 TRIMESTRE | 3f6942e3…/2 | Trimestre del estrato |
| 7 | Estudiantes …/14 Fecha inscripción… | 8c0e76ff…/14 | Pendiente de especificar |
| 8 | Estudiantes …/20 Municipio | 8c0e76ff…/20 | Municipio donde el alumno |
| 9 | Estudiantes …/64 Fecha…no exigibilidad | 8c0e76ff…/64 | Pendiente de especificar |
| 10 | Estudiantes …/66 Fecha…examen prof. | 8c0e76ff…/66 | Pendiente de especificar |

`original` preserva el concepto original de la asignación; la propuesta no aprueba concepto alguno.

## Límites

- Sin joins, cruces, homologaciones, equivalencias ni identidad de catálogos.
- Sin nuevas vigencias (periodos CKAN = metadato del recurso).
- Sin promoción semántica; el estatus de las correspondencias no cambia.
- `peticiones-web.json` (significado: manual SINAC 2022, norma UES, metodología PROAES) sigue pendiente del agente web-obscura; no bloquea este registro.

## Archivos

- `entrega.json` (serializado con `json.dumps`; 10 decisiones, 9 fuentes primarias + ref. `alineacion`)
- `alineacion.json` (esquema/fila completos por par + SHA primarias + diferencias)
- `evidencia/package_*_2026-10-24.json` (copias CKAN verificadas)
- `historial/entrega-2026-10-24-propuesta_resolucion-RECHAZADA-por-auditoria.json` (rechazada, sin efecto)
- `gen_entrega.py`, `peticiones-web.json`, `cierre-listos.json`
