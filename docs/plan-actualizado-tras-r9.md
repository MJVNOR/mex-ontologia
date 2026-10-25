# Plan posterior a R9

Fecha base: 2026-10-24. Este plan registra la ejecución completa del plan posterior a R8. El documento [`plan-actualizado-tras-r8.md`](plan-actualizado-tras-r8.md) se conserva como el plan recibido; sus fases ya no son tareas abiertas.

## Cierre R9 verificado

R9 está integrado, validado y sincronizado. Su delta no agrega significados, conceptos ni correspondencias: incorpora dos declaraciones de unidad con alcance local y una regla de exclusión SHACL.

| Indicador | R9 |
| --- | ---: |
| Significados respaldados | 1,423 |
| Conceptos | 1,106 |
| Correspondencias revisadas | 4,506 |
| Candidatas / ambiguas | 17 / 0 |
| Significados reales pendientes | 138 |
| Vigencias pendientes | 16 |
| Columnas examinadas | 5,523 |
| Pares estructurales en la vista de prioridad | 1,191 |
| Suite Python | 204 OK antes y después de generar RDF |
| Portal | 322,405 triples; sintaxis RDF correcta y SHACL conforme |
| Studio | 323,014 triples; sincronizado y verificado |

La cobertura de columnas conserva los estados separados: 4,506 revisadas, 17 candidatas, 833 sin definición coincidente, 154 con definición sin interpretación compartida y 13 de conjuntos sin diccionario. Se conservan cinco observaciones de esquema.

### Recibos y material revisados

- El cierre R9 coincide con sus resúmenes: RDF, carga, estadísticas y `reports/portal-carga.json` reportan 322,405 triples; `reports/studio-portal-sync.json` reporta 323,014, `verificado=true`, SHACL conforme y cero violaciones. Los alcances de carga y Studio son distintos; no se tratan como conteos que deban ser iguales.
- SHACL informa el Shape `ResultadoMunicipalLote` como unmatched porque no tiene instancias; no lo reporta como violación. Su evaluación usa el alcance whole-store/`temporal/2` indicado en el recibo.
- El hash del log postgeneración coincide con `reports/ronda-9.json`: 204 pruebas, `OK`. Los logs pre y postgeneración registran 204 `OK`; la regresión específica R9 registra 23 `OK`.
- Se cotejaron con SHA-256 los archivos que el recibo R9 lista como vistas derivadas: 101 presentes, cero ausentes y cero hashes discrepantes. También coinciden los hashes de base, respaldo, manifiesto R9 y aplicación.
- No se detectó discrepancia material en los recibos R9 examinados.

## Fases R8 marcadas como completadas

| Trabajo del plan R8 | Estado R9 | Evidencia / límite |
| --- | --- | --- |
| Congelar y comprobar la base R8 | **Completado** | Base, respaldo, manifiesto, aplicación y núcleo R8 verificados por SHA; manifiestos R1–R8 preservados. |
| C1: trazar las 17 candidatas | **Completado** | Las 17 están trazadas; ninguna se promovió sin significado respaldado. |
| C2: priorizar oportunidades | **Completado** | 1,191 pares priorizados; top 50 disponible como lista de revisión. Es una prioridad estructural, no una validación ni autorización de joins. |
| C3: reconciliar cobertura | **Completado** | 5,523 columnas reconciliadas; cinco observaciones preservadas. |
| C4: revisar vigencias y anomalías | **Completado** | 19 casos, 104 evidencias y siete necesidades/preguntas documentales registradas. Las preguntas no se enviaron. |
| P1: piloto QUDT | **Completado con dos vínculos acotados** | `Milímetros` → `<http://qudt.org/vocab/unit/MilliM>` y `Hectáreas` → `<http://qudt.org/vocab/unit/HA>`, con literal fuente exacto y alcance por definición. Para hm³, el literal local `Hectómetros cúbicos` sí está documentado; no se encontró/verificó un término precoordinado aplicable en QUDT 3.5.3 (`HectoM3` devolvió 404 y no aparece en el índice revisado), así que no se enlazó ni sustituyó por `M3`. |
| P2: piloto OWL-Time | **Completado, resultado negativo** | Se revisaron cuatro familias; no se incorporaron intervalos porque faltan límites y referencia temporal documentados. |
| P3: jerarquía clínica | **Completado, resultado negativo** | Los 101 conceptos `caso-con-*` se revisaron; las fuentes no justifican relaciones jerárquicas. No se añadieron `skos:broader`. |
| P4: exclusión SHACL y versionado | **Completado** | La forma admite ninguno de los dos significados, prohíbe ambos y se comprobó con las variables/fixtures. La guía separa `format_version` de `release`, sin migración retroactiva. |
| Auditoría e integración | **Completado** | El borrador del integrador I fue rechazado tras defectos demostrados. Se aplicó el material final K, aceptado por auditorías semántica y técnica independientes. |
| Validación y sincronización | **Completado** | 204 pruebas antes y después de generar; RDF y SHACL conformes; Studio verificado con 62 triples insertados y cero retirados gestionados. |

## Aclaración del piloto QUDT

R9 registra **declaraciones locales de unidad** que apuntan a IRIs de unidades QUDT mediante la propiedad del proyecto `mex:unidadQudt`. Conserva el literal exacto de la fuente y la procedencia. Este piloto no declara que se haya adoptado todo el modelo de cantidades de QUDT: no asigna `qudt:QuantityValue`, valores numéricos, conversiones ni una unidad global a otras variables/recursos. Para hm³, `Hectómetros cúbicos` es el literal de unidad documentado en la fuente; lo que falta es un vínculo a un término precoordinado verificado en QUDT 3.5.3. `HectoM3` devolvió 404 y no aparece en el índice revisado; no se usó `M3` como sustituto ni se infirió un factor. El caso queda fuera del grafo aceptado, no porque se desconozca su unidad literal.

Si se quisiera representar mediciones en una futura tarea, primero habrá que comprobar que los valores observados y su contexto respaldan el uso de una cantidad y unidad concretas. El piloto actual no habilita conversiones o comparaciones automáticas.

## Pendientes documentales — no repetir búsquedas agotadas

R9 reconcilió los conteos y conservó los 138 significados como pendientes; no realizó otra ronda de revisión documental individual de esos 138. Esa investigación por caso se realizó en R8 y está documentada en [`investigacion-post-r6.md`](../reports/investigacion-post-r6.md). En R9 se revisaron los 19 casos de vigencia/anomalía y 104 evidencias; no apareció evidencia primaria nueva. Los 138 significados, 16 vigencias, 17 candidatas, `des_mpo_res` y los encabezados tienen ya condiciones de reapertura. No abrir otra ronda genérica ni volver a investigar fuentes agotadas sin una pista concreta.

| Pendiente | Estado exacto | Qué permitiría reabrirlo |
| --- | --- | --- |
| 138 significados | No respaldados con la evidencia examinada; no se promovió ninguno en R9. | Diccionario corregido, codebook, instrumento o respuesta del publicador que vincule pregunta/campo, codificación, recurso y edición local. |
| 16 vigencias | Recurso, edición o periodo de aplicación sin acreditación suficiente. | Evidencia que enlace explícitamente catálogo, recurso local y periodo; V13/V14 requieren además recuperar el acceso a su fuente. |
| `des_mpo_res` | Catálogo aplicable sin identificar. | Corrección/documentación del diccionario que identifique el catálogo y su ámbito, edición o uso en la variable local. |
| Dos encabezados corruptos | Se conservan como evidencia; no cuentan como significados reales. | Fe de erratas o archivo fuente corregido que aclare filas y columnas. |
| 17 candidatas | Los pares siguen dependiendo de significados aún no respaldados. | Resolver el significado aplicable y conservar el enlace físico específico con evidencia y auditoría. |
| Cinco observaciones de esquema | Siguen registradas en cobertura; R9 las reconcilió, pero no las convirtió en resoluciones. | Evidencia del publicador o diccionario corregido para el conflicto de urgencias/egresos, formato CVE_MUN, fecha numérica, encabezado `a–o` y alias de año de Divorcios 2023. |

Hay siete necesidades/preguntas documentales preparadas y no enviadas. No se contactó a publicadores. Si el usuario decide gestionarlas, conviene enviar un paquete breve y rastreable por caso; hasta entonces, mantenerlas como brechas externas.

## Próximo trabajo permitido

No hay una nueva integración semántica que pueda hacerse con los expedientes cerrados sin duplicar búsquedas o debilitar el respaldo. El estado práctico ahora es **espera de evidencia nueva**, con estos trabajos locales opcionales:

1. Mantener el top 50 de pares como lista de priorización. Elegir un par sólo cuando exista una pregunta analítica concreta; antes de cualquier join validar grano, claves, unicidad, cardinalidad, periodo, población y unidades. No ejecutar joins por el ranking.
2. Reutilizar las dos declaraciones QUDT aprobadas sólo para las definiciones y fuentes indicadas. Ampliar unidades, intervalos o jerarquías únicamente cuando aparezca evidencia primaria nueva y específica.
3. Incorporar al tablero/reporte de cobertura los estados R9 y las condiciones de reapertura, si se necesita una vista operativa. Esto no cambia el grafo.
4. Reabrir sólo los casos vinculados a una fuente nueva, cambio verificable del portal o respuesta autorizada del publicador. Un único agente coordina consultas Obscura compartidas; los demás trabajan en entregas separadas con hashes.

Para una futura ronda: congelar una base nueva, crear carpetas de salida separadas por agente, impedir ediciones paralelas de archivos centrales, obtener auditorías independientes del payload exacto e integrar con un solo escritor. Después ejecutar la suite completa, RDF/SHACL y una sincronización Studio controlada. No modificar manifiestos R1–R9.

## Fuentes del cierre

- [Informe R9](../reports/ronda-9.md) y [datos R9](../reports/ronda-9.json).
- [Plan ejecutado](plan-paralelo-ronda-9-sin-gemma.md).
- Expediente: `propuestas/plan-tras-r8/ejecucion-20261024/`.
- Guía de [versionado y lanzamientos](versionado-y-lanzamientos.md).
