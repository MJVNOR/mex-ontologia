# Agente 1 (ronda 2) — Revisión de correspondencias candidatas por nombre

Unidad: vínculo columna física → variable documentada del mismo conjunto.
Solo significados `respaldada_por_definicion` con regla vigente en
`ontologia/semantica.json`. No se crean conceptos, no se proponen alias,
no se depende de propuestas de otros agentes. Todo vive en esta carpeta.

Fuentes (solo lectura): `reports/pendientes-semanticos.json`,
`data/semantica/cobertura.json`, `ontologia/semantica.json`,
`data/portal/inventario.json` + `contenido-inspeccion.json` (huellas).
El script anterior de agente-4 se usó solo como referencia técnica.

## Conteos

| Grupo | Cantidad |
| --- | ---: |
| Candidatas examinadas | 792 |
| Preselección léxica | 675 |
| Propuestas finales (vínculo verificado) | 674 |
| Descartes de vínculo | 1 (Año→ano, ñ) |
| Pendientes clasificados | 118 (117 preselección + 1 vínculo) |
| Revisiones existentes conservadas | 162 |
| Grupos documentales (conjunto, diccionario, recurso) | 333 |
| Normalizaciones ortográficas (acentos, acotadas al recurso) | 21 |
| Columnas ambiguas / vínculos (contexto) | 3 / 6 |
| Observaciones documentales (contexto) | 5 |

Cobertura verificada en tests: 674 + 118 = 792, sin duplicados ni solapes;
675 = 674 + 1 descarte. El informe ya no presenta 675 como aprobadas:
**675 preseleccionadas originalmente, 674 finalmente defendibles**.

## Criterio aplicado

1. **Preselección léxica (evidencia de significado).** La descripción del
   diccionario del mismo conjunto respalda explícitamente cada calificador
   del concepto (fragmento citado por calificador). Longitud, guion y
   literal por sí solos no bastan; la semejanza temática sola no promociona.
   Esto confirma que el concepto está en la definición —ya respaldado
   centralmente— pero **no prueba por sí solo que esa definición aplique a
   cada columna física**.
2. **Evaluación del vínculo por grupo documental.** Para cada grupo
   (conjunto, diccionario, recurso) la ficha registra: referencia exacta de
   diccionario (id, nombre, URL) y de recurso (id, título, URL), hojas
   cubiertas, alcance (diccionario único del conjunto según inventario:
   N recursos de datos + 1 diccionario), y por miembro: unicidad del nombre
   de variable en el diccionario, unicidad de la columna en el esquema,
   relación exacta de nombres, representación declarada y diferencias o
   contradicciones. El contexto (títulos de conjunto/recurso/hoja) se marca
   como **solo contexto**, nunca como prueba.
3. **Nombres.** Solo `exacta`, `caja` o `acentos`. Las 21 diferencias por
   acento agudo (`Institución`→`Institucion`) se registran como
   normalización ortográfica separada, acotada a cada recurso, con evidencia.
   **ñ→n NO es mero acento**: `Año`→`ano` queda pendiente (1 descarte);
   sin alias técnicos en este alcance. El informe ya no afirma cero alias:
   afirma cero alias propuestos, 21 normalizaciones registradas y 1 caso ñ
   pendiente.
4. **Contradicciones.** Población específica del concepto frente a otra
   población en la descripción (p. ej. madre frente a difunto) deja
   pendiente. Diferencia campo/definitiva (`fecha_hechos` frente a reporte)
   se registra con limitación: vale la definición.
5. Cada propuesta trae: columna (IRI exacta), campo, recurso, conjunto,
   variable + `variable_iri` + `definicion_iri`, definición literal,
   concepto, regla, representación, diccionario, grupo de vínculo,
   `evidencia_significado`, `evidencia_vinculo`, huellas
   (`huella_esquema`, `huella_fila_diccionario`), criterio,
   `alias_limitado` (siempre null) y limitaciones.

## Propuestas finales por concepto (674)

| N | Concepto |
| ---: | --- |
| 110 | anio-registro (81 regla ampliada + 29 regla base) |
| 79 | programa-educativo (77 nombre + 2 código) |
| 45 | municipio-registro |
| 40 | municipio (26 código + 14 nombre) |
| 34 | entidad (16 nombre + 12 código + 6 nom-ent) |
| 32 | mes-registro |
| 30 | ciclo-agricola |
| 22 | municipio-ubicacion |
| 21 | unidad-hospitalaria-donacion |
| 18 | anio-captura |
| 16 | dia-registro |
| 14 | nacimientos-masculino / 14 femenino / 14 total |
| 13 | anio-reporte |
| 10 | sexo-difunto |
| 9 | fecha-registro |
| 9 | edad-fallecimiento |
| 9 | localidad-ubicacion |
| 8 | entidad-registro |
| 8 | fecha-captura-hidrica |
| 7 | municipio-registro-delito |
| 6 | localidad-delito |
| 6 | localidad (código / nombre) |
| 5 | mes-atencion |
| 5 | municipio-atencion |
| 5 | localidad-atencion |
| 5 | escuela |
| 5 | municipio-escuela |
| 5 | municipio-residencia (madre / difunto / beneficiario) |
| 5 | anio-agricola |
| 4 | poblacion-total |
| 3 | municipio-detencion |
| 3 | fecha-toma-sangre-rickettsia |
| 3 | fecha-recepcion-sangre-rickettsia |
| 3 | fecha-resultado-pcr-tiempo-real-rickettsia |
| 3 | municipio-nacimiento-internado |
| 3 | municipio-nacimiento-externado |
| 3 | municipio-comite |
| 3 | localidad-comite |
| 3 | municipio-origen-llamada |
| 3 | localidad-origen-llamada |
| 8 | fecha-nacimiento/ingreso/egreso/titulacion de titulado (2+2+2+2) |
| 4 | municipio-parto / localidad-parto (2 + 2) |
| 2 | localidad-residencia-madre |
| 2 | localidad-residencia-difunto |
| 1 | anio (no especificado) |
| 1 | fecha-apoyo |
| 1 | fecha-denuncia |
| 1 | municipio-denuncia |
| 1 | municipio-pertenencia-beneficiario |
| 1 | localidad-residencia-beneficiario |
| 1 | entidad-ubicacion |
| 1 | entidad-residencia-alumno |
| 3 | fecha-nacimiento/reporte/localizacion de victima (1+1+1) |
| 3 | fecha-inscripcion/reinscripcion/baja-alumno (1 + 1 + 1) |
| 1 | conteo-consultas |

Suma de la tabla: 674. Detalle por columna y ficha por grupo en
`propuestas.json` (`propuestas_revisadas` + `grupos_vinculo`).

Ejemplos trazables:

- `file-column/…/Matriculas…/Programa educativo` → `programa-educativo`:
  significado (programa + educativo literales en la descripción del mismo
  diccionario) + vínculo (grupo G-xxx: diccionario único del conjunto,
  variable única, columna única en su hoja, nombre caja). Contexto
  `Matriculas / …` solo como dominio.
- `column/…/fecha_hechos` → `fecha-reporte-victima`: el campo sugiere
  ocurrencia pero la definición dice reporte; se registra la diferencia y
  vale la definición, con limitación.
- `column/…/Año` → pendiente: `Año` vs `ano` difiere en ñ→n; requiere alias
  técnico fuera de este alcance. No se delega al agente 2.

## Pendientes clasificados (118)

| Motivo | N | Etapa |
| --- | ---: | --- |
| variable sin respaldo: fuera del núcleo actual | 60 | preselección |
| variable sin respaldo: candidata sin definición suficiente | 24 | preselección |
| calificador sin respaldo: registro (captura ≠ registro) | 11 | preselección |
| calificador sin respaldo: previo (anterioridad no explícita) | 9 | preselección |
| calificador sin respaldo: ser1 / suero+ser1 (identificador sin respaldo) | 9 | preselección |
| descripción sin aporte (repite el nombre: Año, Sexo) | 3 | preselección |
| calificador sin respaldo: educativo (`Programa de estudios`) | 1 | preselección |
| nombre difiere ñ→n (`Año`→`ano`, alias fuera de alcance) | 1 | vínculo |

## Contexto (sin resolución; corresponde al agente 2)

- **Ambiguos** (3 columnas, 6 vínculos): variables `ide_col` con descripción
  críptica, fuera del núcleo.
- **Observaciones** (5): `egresos-descripcion-urgencias`,
  `municipio-formato-ejemplo`, `fecha-ejemplo-numerico`,
  `anio-nacimientos-2023…2024` (sigue candidata, sin alias),
  `anio-divorcios-2023` (sin alias propuesto en esta ronda).

## Limitaciones

- Alcance documental: no valida filas, valores, unidades, codificaciones
  ni pertenencia a catálogos. Representación `no_especificada` se señala
  por propuesta cuando aplica.
- Sin alias y sin transferencia entre recursos/años: cada promoción vale
  solo para su columna (IRI exacta, ficha de grupo citada).
- Las 162 revisiones se conservan intactas y sin contradicción (tests).
- Para integrar: verificar huellas contra el estado vigente; cualquier
  cambio de esquema o fila invalida la propuesta correspondiente.

## Reproducir y tests

```sh
uv run python propuestas/ronda-2/agente-1-correspondencias/revisar.py
uv run python propuestas/ronda-2/agente-1-correspondencias/test_revision.py
```

Los tests recalculan `huella_esquema` y `huella_fila_diccionario` contra el
estado central, comparan la definición literal y conjunto/recurso,
reverifican unicidad, alcance y relación de nombres, e incluyen casos
negativos sintéticos (diccionario fuera del conjunto, alcance con dos
diccionarios, nombres ñ/n, contradicción madre/difunto, variable
duplicada) que pasan el filtro léxico pero fallan el vínculo.
