# Plan de trabajo posterior a R8

Fecha base: 2026-10-24. R8 está cerrado, integrado, validado y sincronizado. Este plan parte de ese estado y evita repetir la investigación que R8 ya agotó.

## Estado de referencia comprobado

R8 incorporó 28 correspondencias SINAC, sin significados ni conceptos nuevos. El estado informado es:

| Indicador | Estado R8 |
| --- | ---: |
| Significados respaldados | 1,423 |
| Conceptos compartidos | 1,106 |
| Correspondencias revisadas | 4,506 |
| Correspondencias candidatas por nombre | 17 |
| Correspondencias ambiguas | 0 |
| Significados reales pendientes | 138 |
| Vigencias de catálogo pendientes | 16 |
| Columnas físicas examinadas | 5,523 |
| Pruebas Python R8 | 181 OK |
| Triples de `portal-completo.ttl` | 322,343 |
| Triples totales de Studio | 322,952; sincronización verificada |

La cobertura de columnas es una unidad diferente de la cobertura de significados. De 5,523 columnas, 4,506 están revisadas, 17 siguen candidatas, 833 no tienen definición coincidente, 154 tienen definición sin interpretación compartida y 13 pertenecen a conjuntos sin diccionario. El informe cuenta cinco observaciones de esquema pendientes. Los 138 significados reales excluyen dos filas corruptas de encabezado; no se deben sumar o restar columnas como si fueran definiciones.

Siguen anotados `des_mpo_res` sin catálogo aplicable, 16 brechas de vigencia —con V13 y V14 de acceso no resuelto— y 17 candidatas semánticas que dependen de significado respaldado. Los informes previos de 20 candidatas, 12 vínculos ambiguos, 169 significados reales y 3,312 candidatas son históricos y no son la base para el siguiente ciclo.

### Comprobación independiente de recibos

- `reports/ronda-8.json` declara `cerrado_integrado_validado_y_sincronizado`; su SHA-256 coincide con `recibo_r8_sha256` en `propuestas/ronda-8-paralela/ejecucion-20261024/cierre.json`.
- `reports/portal-carga.json` es consistente internamente: carga, estadísticas y grafo combinado reportan 322,343 triples; sintaxis correcta y SHACL conforme con 0 violaciones.
- `reports/studio-portal-sync.json` y la sección Studio de R8 coinciden: 322,952 triples, `verificado=true`, SHACL conforme y 0 violaciones.
- El SHA-256 del log de la suite R8 coincide con el manifiesto del informe: 181 pruebas, resultado `OK`.
- Los 322,343 triples de la carga de portal y los 322,952 de Studio tienen ámbitos distintos. No se deben forzar a ser iguales. El Shape `ResultadoMunicipalLote` aparece sin instancias y está informado como unmatched, no como violación.
- Los SHA-256 posteriores de README, PLAN, plan paralelo R8 y núcleo semántico coinciden con el cierre R8.

## Orden propuesto

### 0. Congelar la base de trabajo R8 — coordinador

Antes de abrir otra ronda, conservar un snapshot recuperable del estado R8. El árbol de trabajo incluye cambios sin confirmar de R6–R8; no crear ramas de agentes desde `origin/main` y asumir que contienen el cierre. Registrar los hashes de los insumos vigentes, en especial `reports/ronda-8.json`, `ontologia/revision-ronda-8.json`, `ontologia/semantica.json`, `data/semantica/cobertura.json`, `reports/pendientes-semanticos.json`, `data/portal/oportunidades-cruce.json` y los recibos de Studio/carga.

El coordinador configura el MCP nativo de OpenCode con `opencode_setup`. Los agentes usan `opencode-go/muse-spark-1.3-contributor`; Obscura se reserva para pistas primarias nuevas y un solo agente controla su sesión compartida. No sustituir el MCP por CLI ni usar Gemma en este plan.

### 1. Auditoría local de cobertura y priorización — ejecutar ahora, en paralelo

Usar los archivos cerrados de R8, sin repetir investigaciones generales ni editar la ontología.

| Agente | Alcance exclusivo | Entrega separada |
| --- | --- | --- |
| C1 — Candidatas | Trazar las 17 candidatas hasta sus definiciones pendientes y pares estructurales existentes; confirmar por qué cada una no se promueve todavía. | `correspondencias-17/entrega.json` y `.md` |
| C2 — Mapa de cruces | Recalcular una vista de prioridad con las correspondencias y cobertura R8; separar oportunidad de cruce de join validado. Señalar si el mapa de oportunidades fechado antes de R8 requiere regeneración. | `oportunidades-r8/entrega.json` y `.md` |
| C3 — Cobertura de columnas | Reconciliar las 5,523 columnas y sus cinco estados con el informe R8; listar las cinco observaciones por recurso/columna y diferenciar los 138 significados reales. | `cobertura-r8/entrega.json` y `.md` |
| C4 — Referencias y anomalías | Cotejar las 16 vigencias, V13/V14, `des_mpo_res` y las dos filas corruptas contra evidencia R8; dejar claro qué está documentado y qué sólo reabriría con evidencia nueva. | `referencias-anomalias/entrega.json` y `.md` |

Los agentes escriben únicamente bajo una carpeta de ejecución nueva y sus propias subcarpetas en `propuestas/plan-tras-r8/`. Son informes derivados, no nuevas resoluciones. Un auditor coteja conteos, IRIs, localizadores y hashes con la base congelada. Si el mapa de oportunidades está obsoleto, se publica una vista nueva fechada; no se reescribe evidencia histórica.

**Puerta 1:** no pasar a una promoción semántica desde una coincidencia de nombre, fila estructural o prioridad de cruce. La promoción necesita una definición respaldada y el enlace físico específico, con sus límites.

### 2. Dependencias documentales — sólo reabrir con una pista concreta

R8 revisó los 202 casos asignados y no encontró pistas primarias nuevas. Los 138 significados, 16 vigencias, 17 candidatas, `des_mpo_res` y los encabezados tienen ya condiciones de reapertura. No volver a lanzar búsquedas genéricas agotadas.

Si aparece un diccionario corregido, codebook, instrumento oficial vinculado a la edición local, evidencia de adopción institucional o acceso recuperado para V13/V14, el coordinador asigna sólo los casos relacionados a un agente OpenCode. Cada agente registra fuente primaria, versión/periodo, localizador preciso, SHA-256, afirmación respaldada y límites. Obscura atiende únicamente URLs o consultas con esa pista concreta. Se pueden preparar preguntas al publicador, pero no se envían en este plan.

**Criterio de aceptación:** aceptar una propuesta sólo si la evidencia respalda el campo, el recurso y la edición/periodo relevantes. Un resultado negativo se limita a lo examinado; no demuestra inexistencia universal. Sin evidencia nueva, conservar el pendiente con la condición exacta para reabrirlo.

### 3. Pilotos de interoperabilidad y estructura — independientes de la respuesta externa

Estos pilotos sí pueden diseñarse con material local, pero no deben cambiar la semántica central hasta revisar las fuentes primarias de cada variable.

| Agente | Piloto y salida | Condición para recomendar integración |
| --- | --- | --- |
| P1 — QUDT | Inventariar variables de medida con unidad explícita en sus fuentes. Proponer un ejemplo mínimo de QUDT y documentar si se modela sólo la unidad de la variable o también valores observados. | La fuente declara la unidad para esa variable/recurso. `qudt:QuantityValue`, valor numérico, unidad o conversión se usan sólo cuando los datos y la escala están documentados. Si no hay un caso respaldado, entregar recomendación de no integrar aún. |
| P2 — OWL-Time | Inventariar periodos escolares y ciclos agrícolas candidatos; proponer un `time:Interval` sólo para un periodo con límites temporales documentados. | La fuente acredita fechas o posiciones de inicio y fin y el calendario/referencia temporal. Un título o año aislado no se convierte en intervalo. |
| P3 — Jerarquía clínica | Revisar los 101 conceptos `caso-con-*` de R8 por contenido, preservando la manifestación distinta en cada definición. Proponer agrupaciones clínicas y relaciones SKOS, no una reducción textual automática. | Un documento fuente justifica cada agrupación y `skos:broader`; la prueba de consultas confirma que se pueden recuperar tanto cada manifestación concreta como su grupo. La semejanza léxica de los nombres no basta. |
| P4 — SHACL y versionado | Proponer una regla de exclusión entre `mex:significadoDocumentado` y `mex:significadoCandidato`, y un esquema de versionado/changelog compatible con hashes y manifiestos. | La forma permite variables pendientes sin ninguno de esos vínculos, impide que una variable tenga ambos, y preserva las rondas aprobadas. `prov:wasDerivedFrom` ya exige al menos dos fuentes en correspondencias; no duplicar esa regla. Separar versión de formato JSON de versión de lanzamiento. |

Cada piloto produce Turtle/JSON de propuesta, ejemplos, fuentes, límites y consultas que deberían funcionar. No modifica `ontologia/semantica.json`, RDF generado, Shapes centrales ni Studio. QUDT, OWL-Time y jerarquía clínica pueden investigarse en paralelo porque sus entregas son independientes; P4 también es independiente mientras se limite a diseño.

### 4. Revisión e integración — un solo escritor de archivos centrales

1. Congelar las propuestas aceptadas y sus hashes.
2. Asignar auditoría A semántica/documental y auditoría B técnica, independientes del autor.
3. El coordinador acepta, devuelve para corrección o conserva como propuesta. Un caso sin evidencia permanece fuera del núcleo.
4. Integrar en una sola secuencia únicamente las decisiones aceptadas. Un solo integrador modifica `ontologia/semantica.json`, `shapes/semantica.ttl`, scripts de generación, manifiesto y artefactos RDF; mantener intactos los manifiestos R1–R8.
5. Sincronizar Studio una sola vez después de generar y validar el estado integrado, con respaldo y comprobación de conservación de triples ajenos.

No mezclar como si fueran una misma decisión: interpretación de significado, correspondencia columna–definición, vigencia de catálogo, unidad de medida, periodo temporal y autorización de cruce.

### 5. Validación y cierre de la siguiente versión

Tras cada integración, ejecutar la suite Python completa y conservar el log y SHA-256; validar sintaxis RDF, SHACL y las consultas afectadas en el grafo generado. Repetir SHACL en Studio con su alcance de validación declarado, registrar Shapes sin instancias y comparar el diff de triples antes/después. Validar en paralelo los informes congelados; ejecutar carga/sincronización con un único operador.

Una siguiente versión se acepta si:

- cada delta corresponde a una propuesta aprobada, con evidencia y huellas verificadas;
- los 17 pares siguen como candidatas mientras el significado no esté respaldado;
- 833 columnas sin definición, 154 columnas con definición sin interpretación compartida y 13 sin diccionario permanecen visibles como estados distintos hasta resolverlos;
- no se añaden unidades, intervalos, códigos, identidad de catálogos, equivalencias ni joins por nombre o convención;
- la suite Python y SHACL terminan conformes; el recibo Studio coincide con la consulta viva y preserva los datos previos;
- los informes distinguen el grafo de carga (322,343 triples en R8) del total vivo de Studio (322,952 en R8), sin exigir que coincidan;
- pendientes y condiciones de reapertura se publican aunque no haya promociones nuevas.

## Qué ejecutar y qué dejar condicionado

**Ejecutable ahora:** reconciliación local de cobertura, prioridad de las 17 candidatas, verificación de las cinco observaciones, documentación de anomalías, inventario de unidades/periodos ya declarados, diseño de los cuatro pilotos y revisión SHACL/versionado.

**Pilotos acotados:** un ejemplo de medida con unidad explícita, un intervalo temporal con bordes explícitos y una jerarquía clínica documentada. Si el inventario no encuentra evidencia suficiente, el resultado aceptable es una propuesta negativa que explique qué dato falta.

**Condicionado a evidencia externa nueva:** resolver los 138 significados, las 16 vigencias, V13/V14, `des_mpo_res`, cualquier concepto/código que dependa de las filas corruptas y las 17 correspondencias que dependen de significados. Preparar solicitudes documentales no implica enviarlas.

**Límite de cobertura:** 833 columnas sin definición coincidente, 154 con definición sin interpretación y 13 de conjuntos sin diccionario requieren trabajo incremental. Cerrar un corte R9 no significa que todos los datos del portal estén modelados para siempre; el catálogo y los recursos cambian.
