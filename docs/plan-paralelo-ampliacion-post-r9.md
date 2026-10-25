# Plan de ampliación posterior a R9

## Alcance y límites

Base: R9 y `reports/seguimiento-operativo-post-r9.md`. OpenCode MCP nativo
comprobado disponible. Inicio con `opencode-go/muse-spark-1.3-contributor`;
por instrucción del usuario, continuación con
`opencode/deepseek-v4.1-flash-free` tras agotarse el uso rolling de Muse.
Las entregas previas conservan su autoría; los carriles pendientes usan sesiones
nuevas de DeepSeek Free, cuya disponibilidad se comprobó con el MCP nativo.
La base IRI queda expresamente fuera de alcance: no decidir ni sustituir
`example.org`. Gemma, contactos a publicadores, promoción de candidatas sin
respaldo y joins automáticos al grafo quedan excluidos. Los manifiestos R1–R9
se conservan.

## Carriles independientes

| Carril | Entradas | Salidas separadas | Dependencia |
| --- | --- | --- | --- |
| T — Top 50 | Mapa estructural original, ranking C2, criterios y cobertura R9 | Reconciliación reproducible y vista legible de los 50 pares con límites y evidencia | Base congelada |
| A1 — Llamadas 911 | Par procedentes/improcedentes, diccionarios y datos locales disponibles | Pregunta, ficha de ocho comprobaciones y análisis separado reproducible o bloqueo documentado | Par identificado en ranking |
| A2 — Registro civil | Matrimonios/nacimientos, diccionarios y datos locales disponibles | Comparación de volúmenes registrados, con poblaciones distintas explícitas; ficha y resultado o bloqueo | Par identificado en ranking |
| A3 — ITAMA | Internamiento/externamiento, diccionarios y datos locales disponibles | Comparación de distribuciones agregadas por periodo, sin identificar personas ni sumar universos | Par identificado en ranking |
| Q — Unidades locales | Filas originales con unidad literal, cobertura y declaraciones R9 | Inventario, propuestas cualificadas y exclusiones; petición de términos exactos a W | Base congelada |
| W — Normativa | Peticiones concretas Q, evidencia QUDT 3.5.3 ya respaldada | Fuente primaria, sujeto RDF exacto, versión, copia y SHA por término | Q; único navegador Obscura |
| S — SHACL | Clases/estados reales, formas vigentes y motor instalado | Formas adicionales acotadas, justificación, fixtures positivos/negativos y prueba contra copias completas | Base congelada |
| R — Auditorías | Entregas selladas y payload propuesto | Dictamen semántico/documental y técnico independientes con hashes exactos | T/A/Q/W/S finalizados |
| I — Integración | Únicamente material aceptado | Reportes/scripts/vista y, si procede, evidencia nueva y configuración de extensión | Dos auditorías; un solo escritor central |

Los carriles escriben exclusivamente en subcarpetas de
`propuestas/ampliacion-post-r9/ejecucion-20261024/`. Correcciones en versiones
nuevas; no sobrescribir entregas selladas. El coordinador conserva snapshots
y realiza la única instalación central.

## Preguntas analíticas iniciales

1. **911:** ¿se pueden comparar los volúmenes clasificados como procedentes e
   improcedentes por municipio y mes? Solo calcular una proporción si consta
   que las categorías forman una partición del mismo universo.
2. **Registro civil:** ¿qué volúmenes de matrimonios y nacimientos se registran
   en un periodo y ámbito territorial documentalmente comparables? Son eventos
   y poblaciones distintos; no interpretar causalidad ni tasas poblacionales.
3. **ITAMA:** ¿cómo se distribuyen los registros de internamiento y externamiento
   por sexo/escolaridad en un periodo común? No unir personas ni deduplicar o
   sumar universos sin respaldo.

Por par se comprueban **claves, grano, unicidad, cardinalidad, población, periodo,
unidades y cobertura de los datos**. Una muestra no acredita unicidad o
cardinalidad del recurso completo. Un resultado bloqueado con causa y evidencia
es una entrega válida; no se completan campos por nombre o convención.

## QUDT y SHACL

Las unidades conservan el literal y la definición local. Solo se vinculan a un
término exacto aplicable en una versión respaldada. Para hm³, la unidad literal
es conocida; no se sustituye por M3 ni se infieren factores. No se repite la
búsqueda agotada de HectoM3 sin una pista primaria distinta.

SHACL se limita a clases/estados y propiedades justificadas: patrones, tipos,
cardinalidades o coherencia de estado. No se usa `sh:closed` global ni se
rechazan propiedades válidas ajenas al alcance. Cada regla debe demostrar un
caso negativo y controles positivos con el motor real; registrar restricciones
no evaluadas y Shapes sin instancias.

## Orden de ejecución y aceptación

1. Congelar base, manifiestos y recibos; lanzar T, A1–A3, Q y S en paralelo.
2. W atiende solo peticiones concretas y conserva fuentes primarias; no contacta
   publicadores. Los análisis permanecen separados de la ontología.
3. Congelar payload y someterlo a dos revisiones independientes. Resolver los
   defectos en versiones nuevas y revisar de nuevo los bytes corregidos.
4. El coordinador publica el top 50 y los análisis; integra únicamente unidades
   y formas aceptadas. Si hay delta RDF, crear evidencia/configuración nueva y
   respaldar Studio antes de una sola sincronización. No alterar R1–R9.
5. Ejecutar suite completa, sintaxis RDF, consultas afectadas y SHACL del portal
   y de Studio; comprobar conservación de datos ajenos. Publicar informe con
   archivos, hashes, resultados y pendientes que requieren evidencia externa.

Las tareas locales avanzan sin pedir decisiones que no necesitan. Las que
dependan de documentación nueva se dejan condicionadas con una petición
documental concreta, sin enviar mensajes externos.
