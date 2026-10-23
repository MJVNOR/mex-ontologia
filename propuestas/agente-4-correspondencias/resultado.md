# Agente 4 — Revisión de correspondencias (propuesta, sin aplicar)

Unidad: vínculo columna física → variable documentada. Solo significados
respaldados vigentes (`respaldada_por_definicion`, 208 variables) con regla
concreta de `ontologia/semantica.json`. No se crean conceptos, no se comprueba
pertenencia a catálogos, no se sincroniza Studio. Todo vive en esta carpeta.

Fuentes leídas (solo lectura): `reports/pendientes-semanticos.json`,
`data/semantica/cobertura.json`, `ontologia/semantica.json` (+ inventario
e inspección para huellas). Huellas de entrada conservadas en `propuestas.json`.

## Conteos

| Grupo | Cantidad |
| --- | ---: |
| Candidatas examinadas | 891 |
| Propuestas `documental_revisada` (99 candidatas + 1 alias divorcios) | 100 |
| Pendientes clasificados (de candidatas) | 792 |
| Columnas ambiguas / vínculos ambiguos | 3 / 6 |
| Inconsistencias revisadas | 5 |
| Revisiones existentes conservadas | 62 |

Aclaración aprobada: 3 columnas ambiguas y 6 vínculos ambiguos son conteos
compatibles (cada columna ambigua apunta a ~2 definiciones).
Cobertura verificada en tests: 99 + 792 = 891 candidatas, sin duplicados
ni solapes entre propuestas, pendientes y ambiguos.

## Criterio aplicado (ajustes aprobados)

1. **Variables, no reglas.** Se comprueba `estado=respaldada_por_definicion`
   de cada variable y su `regla` concreta en `reglas_descripcion_exacta`.
   141 candidatas apuntan a variable sin respaldo
   (60 `fuera_del_nucleo_actual`, 81 `candidata_sin_definicion_suficiente`)
   y quedan pendientes: sin regla vigente no hay promoción posible.
2. **Sin promoción masiva; sinónimos no bastan.** Nombre exacto (salvo caja) +
   descripción distintiva (igual a regla o con función+objeto, ≥15 caracteres) +
   contexto conjunto/recurso/hoja con el **calificador literal**
   (registro, censo, inspección…) + representación específica + concepto
   calificado (con `-`). Los sinónimos temáticos (delito≈registro,
   alumno≈educativo, víctima≈registro, divorcio≈matrimonio…) son pistas:
   motivan el pendiente (`pista_tematica_insuficiente`) pero no promocionan.
   El nombre del propio campo no cuenta como contexto (evita confirmación
   circular). Si solo reconfirma el emparejamiento por nombre, queda pendiente.
3. **Inconsistencias individuales** (ver tabla). Una con alias específico
   (divorcios 2023, misma hoja CSV y posición, diccionario único compartido);
   una hipótesis no verificada que sigue candidata (nacimientos 2024);
   dos mantienen su revisión con limitación; una requiere al publicador.
4. **Tests** (`test_revision.py`) comprueban cobertura total de las 891,
   duplicados, separación de grupos, que ninguna propuesta contradice
   o sustituye a las 62, que ningún alias es global y que ningún
   `detalle_contexto` usa sinónimos.

## Propuestas por concepto y regla

| Concepto | N | Regla |
| --- | ---: | --- |
| fecha-donacion | 21 | fecha-donacion |
| fecha-inspeccion | 15 | fecha-inspeccion |
| hora-defuncion | 10 | hora-defuncion |
| anio-subasta | 9 | anio-subasta |
| anio-defuncion | 9 | anio-fallecimiento |
| mes-defuncion | 9 | mes-defuncion |
| dia-defuncion | 9 | dia-defuncion |
| fecha-ingreso-llamada | 4 | fecha-ingreso-llamada |
| anio-censo | 3 | anio-censo |
| fecha-comite | 3 | fecha-comite |
| municipio-nacimiento-madre | 2 | municipio-nacimiento-madre-* |
| municipio-defuncion | 2 | municipio-defuncion-* |
| localidad-defuncion | 2 | localidad-defuncion-* |
| municipio-entrega-apoyo | 1 | municipio-entrega-apoyo |
| anio-registro (alias divorcios 2023) | 1 | anio-registro |
| anio-registro (candidata) | 1 | anio-registro |

Cada objeto en `propuestas_revisadas[]` trae: columna (IRI exacta), campo,
recurso, conjunto, variable + `variable_iri` + `definicion_iri`, definición
original, concepto, regla, representación, diccionario, evidencia
(descripción, contexto, detalle_descripcion, detalle_contexto),
huellas (`huella_esquema`, `huella_fila_diccionario`), criterio, alias
limitado (`solo_columna:<IRI>` o null) y limitaciones.

- `column/09f17090…/mes` → NO promovida (contexto Nacimientos sin
  corroboración literal de `registro`; queda pendiente).
- `Programa Educativo` → NO promovido (solo pista temática `alumno`, sin
  `programa`/`educativo` literal; queda pendiente).
- `file-column/…/FECHA DE EJECUCIÓN` (Guarderías, hoja
  `GUARDERÍAS INSPECCIONADAS`) → `Fecha de ejecución`,
  `fecha-inspeccion`, contexto literal `inspeccion`, huellas fijadas.

## Ambiguos (3 columnas, 6 vínculos)

| Columna | Campo | Recurso | Dictamen |
| --- | --- | --- | --- |
| `file-column/30b18862…/Hoja1/1` | ide_id | Fiebre manchada 2023 | no promovible |
| `file-column/4121cf57…/Hoja1/1` | ide_id | (mismo diccionario) | no promovible |
| `file-column/cc6c566f…/Hoja1/1` | ide_id | (mismo diccionario) | no promovible |

Las 6 apuntan a variables `ide_id` con descripción críptica `ide_col`,
`estado=fuera_del_nucleo_actual`, sin concepto ni regla. Se conservan
ambiguas; requieren diccionario inteligible o aclaración del publicador.
Detalle por vínculo (IRIs, huellas de fila) en `propuestas.json:ambiguos`.

## Pendientes clasificados (792, de candidatas)

| Motivo | N |
| --- | ---: |
| contexto insuficiente (solo reconfirma nombre) | 262 |
| contexto insuficiente + representación no especificada | 190 |
| contexto insuficiente + concepto genérico sin función | 86 |
| variable candidata sin definición suficiente | 81 |
| variable fuera del núcleo actual | 60 |
| pista temática insuficiente: registro | 38 |
| representación no especificada | 27 |
| descripción corta + contexto insuficiente | 18 |
| pista temática insuficiente: educativo | 15 |
| pista temática insuficiente: matrimonio | 9 |
| otros (genérico/corto/alias/agrícola) | 6 |

Cada fila trae columna, variable, concepto/regla y detalle. Ninguna se
promueve por coincidencia de nombre o por sinónimo temático solos.

## Inconsistencias (revisión individual)

| ID | Dictamen | Pregunta / evidencia |
| --- | --- | --- |
| egresos-descripcion-urgencias | pendiente aclaración publicador | ¿`Total_Egresos` cuenta egresos o urgencias? Nombre vs `Total de urgencias atendidas`; variable sin respaldo. No interpretar ni cruzar. |
| municipio-formato-ejemplo | revisión existente mantenida | Formato `nnn` vs ejemplo `26048`. Concepto municipal conservado; composición del código y equivalencia CVEGEO no resueltas. |
| fecha-ejemplo-numerico | revisión existente mantenida | Formato `DD/MM/AAAA` vs `45658` (serial). Significado conservado; no convertir ni cruzar fechas hasta comprobar codificación. |
| anio-nacimientos-2024 | hipótesis no verificada, sigue candidata | `a–o` (U+2013) podría ser `año`, pero faltan bytes crudos del datastore, aplicabilidad del diccionario CSV al recurso API y fila concreta (órdenes distintos). Sin propuesta. |
| anio-divorcios-2023 | alias específico propuesto | `anio_registro` (ASCII) → `año_registro`; mismo conjunto, diccionario único compartido 10357304, misma hoja CSV, misma posición 3, misma descripción de regla. Solo esa columna. |

No se contacta a terceros; las preguntas quedan documentadas con huellas.

## Limitaciones

- Alcance documental: no valida filas, unidades, codificaciones ni catálogos.
- Alias solo a su columna (`solo_columna:<IRI>`); sin normalizaciones globales.
- No transfiere revisiones entre años/recursos salvo alias explícito aquí.
- Las 62 revisiones se conservan intactas y sin contradicción (ver tests).
- Para integrar: verificar huellas contra el estado vigente antes de aplicar;
  cualquier cambio de esquema o fila invalida la propuesta correspondiente.

## Reproducir

```sh
uv run python propuestas/agente-4-correspondencias/revisar.py
uv run python propuestas/agente-4-correspondencias/test_revision.py
```
