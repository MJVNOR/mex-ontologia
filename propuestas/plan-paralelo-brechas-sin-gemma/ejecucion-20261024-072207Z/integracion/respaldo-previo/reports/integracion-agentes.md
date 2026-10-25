# Integración central de las cinco entregas — ronda 1

La tabla siguiente conserva los resultados históricos de la primera ronda. El estado vigente se documenta en reports/consolidacion-semantica.md y reports/cobertura-muse.md.

Las carpetas originales de propuestas se conservan. La generación lee copias de evidencia fijadas por SHA-256 en data/integracion; no depende de cambios posteriores en las carpetas de agentes ni consulta la red.

| Resultado | Cantidad |
| --- | ---: |
| Conceptos compartidos | 103 |
| Variables con significado documental | 232 |
| Variables candidatas pendientes | 23 |
| Correspondencias revisadas (62 anteriores + 100) | 162 |
| Correspondencias candidatas por nombre | 792 |
| Columnas ambiguas / vínculos ambiguos | 3 / 6 |
| Referencias a catálogos identificadas (8 anteriores + 8) | 16 |
| Referencias a catálogos sin resolver | 1 |
| Localidades observadas en IML 2020 | 1850 |
| Comprobaciones territoriales | 28 |

## Decisiones y límites

- Agente 1: ocho vínculos documentales a hojas completas. Las cuatro publicaciones educativas conservan sus referencias por conjunto, aunque comparten bytes. Las muestras de datos no se integran: algunos metadatos de muestra del JSON repiten el campo de servicios en otras variables; no se usan como evidencia de pertenencia. La identificación se sustenta en diccionario y catálogo completo. La referencia des_mpo_res sigue sin resolver y conserva las dos definiciones de origen.
- Agente 2: 1850 observaciones con composición cruda exacta 2+3+4, sin padding ni conversión numérica. Son localidades incluidas en IML_2020, no un catálogo oficial completo ni una equivalencia con una edición INEGI. No se importó el contraste externo puntual como acreditación de cobertura.
- Agente 3: 20 conceptos/reglas, restringidos simultáneamente por definición, diccionario, conjunto, nombre y descripción. Esta ronda promocionó 24 significados; entonces quedaron 23 candidatos y 1308 definiciones fuera del núcleo. Las ampliaciones posteriores se registran en la cobertura vigente.
- Agente 4: 99 correspondencias y un alias técnico limitado a la columna de divorcios 2023. a–o de nacimientos 2024 no se promueve. Las 62 revisiones existentes se conservan.
- Agente 5: 16 comprobaciones compatibles, 11 con excepciones y una ausencia de columna. Se vuelven a leer las 25 fuentes y se verifican claves, filas, pertenencia a catálogo y composición exacta. No se asigna un sistema de identificadores a columnas ni se promociona su correspondencia semántica. 26998/26999 siguen siendo categorías no municipales. Víctimas 2015 solo tiene revisión completa de encabezado; validación de Clave_Ent no aplicable.

No se acredita vigencia histórica, no se ejecutan nuevos cruces ni se crean owl:sameAs/skos:exactMatch. Las 5 inconsistencias documentales previas siguen visibles, incluida la limitación del ejemplo de formato municipal.

## Evidencia y reproducción

- ontologia/revision-agentes.json fija el manifiesto y los conteos de la integración aprobada.
- data/integracion/manifiesto.json conserva las huellas de las cinco entregas y 37 archivos fuente únicos.
- scripts/ampliar_portal.py --load regenera las capas y valida SHACL antes de sincronizar Studio.
- scripts/sincronizar_studio_portal.py respalda el grafo vivo y conserva las ediciones ajenas a la ampliación.

Respaldo previo de archivos centrales: data\backups\integracion-agentes-20261023T091931Z.zip
