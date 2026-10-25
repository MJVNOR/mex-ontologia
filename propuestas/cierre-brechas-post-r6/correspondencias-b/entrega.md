# Correspondencias-b: registro estructural separado (10/10 par_estructural_revisado_significado_pendiente)

Correccion por dictamen de auditoria (`requiere_correccion`): ningun par es aprobacion; ningun significado cambia de estatus; sin concepto aprobado (el `original` preserva el concepto asignado solo como referencia). NO aplicable a `vinculos_documentales_revisados`: el core exige variable `respaldada_por_definicion`. Herramienta: lectura local con SHA-256 (python hashlib), 2026-10-24.

| # | campo (pos) | concepto original (no aprobado) | estado | significado |
|---|-------------|--------------------------------|--------|-------------|
| 1 | `Fecha de titulación del título profesional` (67) | tiempo | par_estructural_revisado_significado_pendiente | pendiente |
| 2 | `Fecha de impresión del título profesional` (68) | tiempo | par_estructural_revisado_significado_pendiente | pendiente |
| 3 | `Fecha de la convalidación` (69) | tiempo | par_estructural_revisado_significado_pendiente | pendiente |
| 4 | `Fecha de la equivalencia` (70) | tiempo | par_estructural_revisado_significado_pendiente | pendiente |
| 5 | `CLUES` (38) | unidad-salud | par_estructural_revisado_significado_pendiente | pendiente |
| 6 | `MUNICIPIOOCURRENCIA` (72) | municipio | par_estructural_revisado_significado_pendiente | pendiente |
| 7 | `MUNICIPIOOCURRENCIAD` (73) | municipio | par_estructural_revisado_significado_pendiente | pendiente |
| 8 | `LOCALIDADOCURRENCIA` (74) | localidad | par_estructural_revisado_significado_pendiente | pendiente |
| 9 | `LOCALIDADOCURRENCIAD` (75) | localidad | par_estructural_revisado_significado_pendiente | pendiente |
| 10 | `Total_Egresos` (15) | None | par_estructural_revisado_significado_pendiente | pendiente |

## Alineacion en secuencia completa (`alineacion.json`)

- defunciones-seed: 80 filas diccionario = 80 columnas recurso = numero_variables 80; secuencia identica 80/80.
- egresos: 15 = 15 = numero_variables 15; secuencia identica 15/15.
- matriculas: 70 = 70 = numero_variables 70, pero 2 desalineaciones ajenas a los IDs (pos 21 `'Sexo '` vs `'Sexo'`; pos 32 `' Promedio de bachillerato'` vs `'Promedio de bachillerato'`): NO se afirma 1:1 en secuencia completa; los IDs 67-70 son exactos en ambos artefactos.

## Contexto (no prueba del par)

- `distribuciones.json` y `reports/investigacion-post-r6.json`: derivados; informan compatibilidad de formato y ultimo resultado por ID.
- `cobertura.json` (EGR 15): fija el pendiente conservado `pendiente_aclaracion_o_revision`.

## Historial

- Propuesta anterior (`propuesta_resolucion` / `documental_revisada` con concepto) rechazada por auditoria; guardada por ID en `historial_propuesta_rechazada`, inactiva como aprobacion.

## Limites

- Sin joins/cruces/identidad de catalogos; sin vigencia nueva del vinculo; sin promocion semantica (EST 68 sin muestra; SEED ambiguedad general-fetal; EGR 15 sin fe de erratas).
