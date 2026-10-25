# Plan posterior a R10

Fecha base: 2026-10-24 (America/Hermosillo). Este plan toma R10 como el corte integrado vigente. Conserva el [plan tras R9](plan-actualizado-tras-r9.md) como historial; sus tareas locales se revaluaron con los recibos de R10.

## Estado del cierre R10

R10 está integrado, validado y sincronizado. Añade cinco declaraciones locales de unidad con vínculo QUDT y seis formas SHACL; no cambia significados, conceptos ni correspondencias. Publica el top 50 actualizado de oportunidades y tres análisis de pares. Ningún análisis autoriza un join ni calculó comparaciones.

| Indicador | R10 |
| --- | ---: |
| Significados respaldados | 1,423 |
| Conceptos | 1,106 |
| Correspondencias revisadas | 4,506 |
| Candidatas / ambiguas | 17 / 0 |
| Columnas examinadas | 5,523 |
| Pares del mapa / candidatas estructurales | 3,916 / 1,191 |
| Filas publicadas en top 50 | 50, todas `NO_JOIN_APROBADO` |
| Análisis de pares | 3, bloqueados por evidencia |
| Declaraciones de unidad QUDT | 7 en total; cinco agregadas en R10 |
| Suite Python | 233 OK, cero omitidas |
| Portal / Studio | 322,495 / 323,104 triples; ambos SHACL conformes |
| Delta de sincronización R10 | +90 triples; cero retirados gestionados |

Las cinco declaraciones nuevas son `Kilogramos` → `KiloGM`, `MW` → `MegaW`, `GWh` → `GigaW-HR`, `Porcentaje` → `PERCENT` y el literal fuente `Grados celcius` → `DEG_C`. MW y GWh se aplican exclusivamente a las filas `Unidad de Medida` documentadas. No se asignan cantidades observadas ni conversiones. La IRI base, `config.toml` y `ontologia/semantica.json` no cambiaron.

## Revisión independiente del cierre

- Se cotejaron contra SHA-256 las 41 entradas históricas, las 28 evidencias listadas por el recibo y los dos respaldos: **71/71 coinciden**. También coinciden por separado los hashes del manifiesto R10, `config.toml` y `ontologia/semantica.json`.
- Los deltas indicados concuerdan con los cortes R9→R10: Portal 322,405→322,495 y Studio 323,014→323,104.
- El JSON de top 50 contiene 50 filas, sobre 3,916 pares y 1,191 candidatas; las 50 filas tienen estado `NO_JOIN_APROBADO`.
- El análisis JSON contiene los tres casos anunciados: 911, Registro Civil e ITAMA. No se calcularon tasas, proporciones, distribuciones ni joins.
- El recibo registra 233 pruebas, 30 consultas, RDF y SHACL conformes, cero violaciones y una sincronización con respaldo. No se regeneró Studio durante esta revisión.
- `ResultadoMunicipalLote` vuelve a aparecer como unmatched por falta de instancias, no como infracción. Se conserva esa limitación al interpretar la conformidad.

## Fases R9 completadas en R10

| Trabajo pendiente tras R9 | Estado R10 | Resultado y límite |
| --- | --- | --- |
| Publicar top 50 reconciliado con R9 | **Completado** | `reports/top50-oportunidades-r9.*`; 50 filas, todas sin aprobación de join. |
| Analizar pares con utilidad potencial | **Completado como análisis bloqueado** | 911, Registro Civil e ITAMA; ocho comprobaciones por par; faltan respaldos concretos. No se hicieron cálculos ni joins. |
| Ampliar el piloto QUDT | **Completado en cinco casos** | Se agregaron Kilogramos, MW, GWh, Porcentaje y Grados celcius con alcance local y evidencia. |
| Agregar validaciones SHACL precisas | **Completado** | Seis NodeShapes acotadas; aceptan propiedades adicionales válidas y no usan `sh:closed` global. |
| Auditar e integrar | **Completado** | Dos dictámenes independientes sobre once casos; payload y código revisados; integración con un solo escritor. |
| Validar y sincronizar | **Completado** | 233 pruebas, 30 consultas, RDF/SHACL conformes, respaldo y delta Studio verificado. |

## Pendientes condicionados a evidencia

No abrir otra búsqueda general ni reinterpretar los negativos de R9/R10 como permiso para inferir. Los siguientes trabajos se reabren cuando llegue material nuevo y verificable:

| Caso | Estado | Evidencia que lo reabre |
| --- | --- | --- |
| 138 significados reales | Sin respaldo suficiente; ninguno se promovió en R10. | Diccionario, codebook, instrumento o respuesta que conecte campo, codificación, recurso y edición local. |
| 16 vigencias | Aplicación temporal no acreditada; V13/V14 además tienen acceso pendiente. | Fuente que relacione explícitamente catálogo, recurso, edición y periodo; acceso recuperado para V13/V14. |
| `des_mpo_res` | Referencia de catálogo sin resolver. | Diccionario corregido que identifique catálogo, ámbito, edición o uso en la variable. |
| Dos encabezados corruptos | Excluidos del conteo de significados. | Archivo corregido o fe de erratas que aclare encabezados y filas. |
| 17 candidatas | No promovidas; dependen de significado respaldado y correspondencia física. | Evidencia primaria para el significado y el enlace concreto con columna/recurso, seguida de auditoría. |
| Toneladas | Literal/variante local sin acreditar. | Unidad exacta de la fuente local y evidencia que la vincule a la definición correspondiente. |
| hm³ | Sin término QUDT exacto verificado en el corte respaldado. | Evidencia de un IRI QUDT aplicable al literal; no sustituir por `M3` ni inferir factores. |
| 911 improcedentes/procedentes | Q1 improcedente está mal etiquetado/duplicado y Q2 no tiene MUNICIPIO. | Recursos correctos, esquema territorial, archivos completos y periodo/agrupación documentados. |
| Registro Civil | Totales no cuadran con hombres+mujeres y faltan meses; preparación de agregados no validada. | Archivos completos, corrección/aclaración de totales y meses y regla documentada de agregación. |
| ITAMA internamiento/externamiento | Copias completas y periodo/escolaridad no acreditados. | Recursos completos, grano, periodo, cobertura y catálogo/definición de escolaridad verificables. |

Los cruces de municipio+año o programa+sede no se aprueban por nombre de clave o prioridad. Cada par necesita una pregunta analítica concreta y comprobaciones de clave compuesta, dominio, unicidad, cardinalidad, grano, población, periodo, cobertura y unidades.

## Próximo plan paralelo con OpenCode

No queda un cambio semántico local que justifique otra integración con la evidencia actual. La siguiente ronda debe iniciarse al recibir una fuente concreta o una pregunta de análisis. Se puede preparar en carriles independientes, cada uno con entregables aislados:

1. **Coordinación y congelamiento:** fijar el corte R10, hashes, pregunta y criterios de aceptación; preservar manifiestos R1–R10.
2. **Carril de evidencia documental:** atender solo los casos cuyo publicador/material nuevo esté disponible. Registrar fuente, edición, ámbito y hash; no repetir fuentes agotadas.
3. **Carril de unidades/QUDT:** revisar únicamente literales respaldados que aún carezcan de vínculo; guardar prueba normativa por IRI y conservar los casos no resueltos fuera del grafo.
4. **Carril de cruces:** retomar una ficha bloqueada solo cuando lleguen datos o documentación que cubra sus bloqueadores. Ejecutar cálculo reproducible únicamente después de acordar pregunta, universo y método; guardar salida separada del grafo.
5. **Carril SHACL:** proponer una forma solo para una restricción observada y comprobable; mantener shapes locales por clase y fixtures positivos/negativos. No modificar centralmente desde agentes paralelos.
6. **Integración única:** un integrador compara entregas y huellas, integra solo material respaldado, actualiza el plan y obtiene auditorías A/B independientes del payload exacto.
7. **Validación de salida:** correr suite, generar/validar RDF y SHACL en almacén aislado, revisar queries afectadas y los deltas. Sincronizar Studio solo con nueva aprobación de contenido respaldado, tras respaldo previo y verificación del delta.

Para nuevas sesiones OpenCode, seguir la reanudación expresamente indicada por el usuario: proveedor `opencode-go`, modelo `muse-spark-1.3-contributor` (**Muse 1.3**). Sustituye la instrucción temporal de DeepSeek Free, cuya cuota también se agotó. Confirmar disponibilidad/model ID mediante el catálogo antes de abrir sesiones y crear sesiones nuevas si las anteriores conservan otro modelo. No cambiar automáticamente de modelo ante una nueva falta de cuota. Usar carpetas por carril y un solo escritor para archivos centrales; no enviar solicitudes a publicadores sin autorización expresa. Gemma continúa excluido.

La decisión de reemplazar la base IRI queda **fuera del alcance de este plan**, por instrucción del usuario. No cambiar `config.toml`, la base de RDF ni identificadores.

## Fuentes

- [Cierre R10](../reports/ronda-10.md) y [recibo R10](../reports/ronda-10.json).
- [Top 50](../reports/top50-oportunidades-r9.md) y [análisis de pares](../reports/analisis-pares-post-r9.md).
- [Cobertura operativa R9](../reports/cobertura-operativa-r9.md) y [seguimiento operativo post-R9](../reports/seguimiento-operativo-post-r9.md).
- Expediente R10: `propuestas/ampliacion-post-r9/ejecucion-20261024/`.
- [Plan tras R9](plan-actualizado-tras-r9.md) y [guía de versionado](versionado-y-lanzamientos.md).
