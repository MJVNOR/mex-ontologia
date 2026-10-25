# Agente 10 territorio-economía — ronda 3

Asignadas: 468. Decisiones: 468 (partición completa, sin omitidos ni duplicados).
Lectura literal individual de fila de diccionario (descripción, tipo, unidad, ejemplo, catálogo, contexto de conjunto) verificada por índice de definición_iri contra inspecciones locales.

| Resultado | Cantidad |
| --- | ---: |
| Proponer (con regla restringida) | 419 |
| Pendiente con razón | 49 |
| Reglas nuevas | 419 |
| Conceptos nuevos estrechos | 404 |
| Conceptos vigentes reutilizados | 5 |

## Pendientes por motivo

- 6 × Clasificación delictiva sin catálogo de tipos publicado. Queda pendiente.
- 4 × Clasificación delictiva sin catálogo publicado. Queda pendiente.
- 3 × Folio de orden de la entrada; sin significado documental propio. Queda pendiente.
- 3 × Descripción genérica sin tipología publicada. Queda pendiente.
- 2 × Identificador sin sistema de identidad publicado. Queda pendiente.
- 2 × Clasificación sin catálogo de valores publicado. Queda pendiente.
- 2 × Actividad sin referente publicado. Queda pendiente.
- 2 × Motivo sin catálogo de motivos publicado. Queda pendiente.
- 2 × El nombre (Bien jurídico afectado) contradice la descripción (campo del delito); se conserva la contradicción y queda pendiente sin promover categoría. Queda pendiente.
- 2 × Tipo sin tipología publicada. Queda pendiente.
- 2 × Estado sin catálogo de valores publicado. Queda pendiente.
- 1 × Clasificación delictiva sin catálogo de modalidades publicado. Queda pendiente.
- 1 × Folio de convocatoria; sin significado documental propio. Queda pendiente.
- 1 × Canal de recepción sin catálogo de valores publicado. Queda pendiente.
- 1 × Texto libre de hechos; sin referente codificable publicado. Queda pendiente.
- 1 × Descripción genérica sin materia publicada. Queda pendiente.
- 1 × Descripción de una palabra sin referente publicado. Queda pendiente.
- 1 × Programa sin catálogo publicado. Queda pendiente.
- 1 × El nombre (tema) no fija el objeto de la descripción; se conserva la diferencia y queda pendiente sin medida declarada. Queda pendiente.
- 1 × Tipo sin referente publicado. Queda pendiente.
- 1 × Valor de estado sin catálogo de estados publicado. Queda pendiente.
- 1 × Giro del establecimiento sin tipología publicada. Queda pendiente.
- 1 × Clasificación sin catálogo publicado. Queda pendiente.
- 1 × Tipo de ayuda sin catálogo publicado. Queda pendiente.
- 1 × Nivel sin escala publicada. Queda pendiente.
- 1 × Sector sin referente publicado. Queda pendiente.
- 1 × Grupo sin referente publicado. Queda pendiente.
- 1 × El nombre (Cantidad de apoyos otorgados) contradice la descripción (unidad de apoyos); se conserva la contradicción y queda pendiente. Queda pendiente.
- 1 × Importe de una palabra sin medida ni objeto declarados. Queda pendiente.
- 1 × El nombre (Comentarios/Observaciones) contradice la descripción imprecisa (literal con errata); se conserva la contradicción y queda pendiente. Queda pendiente.

## Verificación

`uv run python propuestas/ronda-3/agente-10-territorio-economia/scripts/verificar.py`: huellas SHA-256 de entradas, partición exacta,
literales y filas recalculadas, reglas unitarias con prefijo r3a10-, 40 positivos y 6 negativos
(solo-nombre, contexto-mutado, otra-IRI, descripcion-alterada, unidad-faltante, codigo-no-acreditado),
base 103/232/836/118. Sin red, sin escritura fuera de la carpeta, sin correspondencias nuevas,
sin sameAs/exactMatch, sin identidad ni vigencia inventadas.

## Revisión manual vs automatización

Manual (humano, en `scripts/construir.py`): lectura literal de las 468 descripciones y su contexto
de conjunto; política explícita por grupo (proponer concepto estrecho o dejar pendiente con razón);
redacción de cada definición, positivo, contraejemplo y límite sin inventar unidades
(edad sin unidad≠años, conteo sin objeto≠personas, monetarios sin moneda≠MXN, sin rangos 0–100),
sin deducir representación desde el nombre (el nombre solo restringe la regla) y conservando
contradicciones nombre↔descripción como pendientes neutros.

Automático (verificable): indexado de filas por `definicion_iri`, recomputo de huellas SHA-256,
con positivos y 6 familias de negativos (ver `scripts/verificar.py`, 132 comprobaciones).

## Límites y pendientes

- Sin correspondencias columna→variable nuevas; la revisión posterior decide vínculos.
- Códigos sin catálogo publicado no acreditan identidad, vigencia ni adopción oficial.
- Metodología anterior y actual no son comparables; meses de registro no implican ocurrencia.
- Proyecciones son estimaciones; periodos no declarados no se inventan.
- 49 pendientes quedan para aclaración del publicador o revisión posterior (folios, clasificaciones sin catálogo, tipos/estados sin valores publicados).
