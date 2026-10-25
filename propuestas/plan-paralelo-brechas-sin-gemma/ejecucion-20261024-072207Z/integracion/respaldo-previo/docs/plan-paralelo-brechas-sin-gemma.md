# Plan paralelo para las brechas documentales, sin Gemma

Estado: plan de ejecución; esta planificación no lanza agentes ni cambia el núcleo.

## 1. Objetivo y punto de partida

Resolver todos los casos que permitan las fuentes primarias disponibles y dejar identificadas las dependencias documentales restantes. La cantidad de agentes no garantiza que aparezcan documentos que todavía no están publicados o localizados.

Base: [última revisión completa](../reports/cierre-brechas-post-r6.md), [cierre y hashes](../propuestas/cierre-brechas-post-r6/cierre.json) y [registro estructural](../data/revision-estructural-post-r6/revisiones.json).

- 169 significados pendientes: 32 defunciones, 53 nacimientos, 30 matrículas, 25 epidemiología, 24 TIC y 5 diversos.
- 20 correspondencias semánticas candidatas: sus pares columna–diccionario ya están documentados estructuralmente. La dependencia pendiente es el significado, no volver a demostrar la asociación física.
- 16 vigencias de catálogos, V01–V16.
- Una anomalía de referencia, `des_mpo_res`, relacionada con dos encabezados corruptos. Estos tres registros no son tres significados nuevos.
- Núcleo vigente: 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y cero ambiguas.

## 2. Equipo y reparto

Diez frentes temáticos pueden trabajar en paralelo, con un investigador web compartido y dos revisores independientes. El coordinador asigna casos, comprueba las dependencias e integra únicamente lo aprobado.

| Frente | Asignación exclusiva | Evidencia que permitiría avanzar |
| --- | --- | --- |
| S1 — Defunciones | 32 significados | Codebook o correspondencia formal campo–pregunta–código–edición; distinguir certificado general y fetal. El examen por ID de SEED 2022 ya está hecho. |
| S2 — Nacimientos | 53 significados | Instrumento SINAC aplicable al recurso y edición local, con definición y codificación de los campos concretos. |
| S3 — Matrículas | 30 significados | Diccionario del sistema escolar o documentación institucional aplicable a 2022-2; definiciones de eventos, escalas y alternativas de titulación. |
| S4 — Epidemiología | 25 significados | Definiciones operativas y catálogos del instrumento efectivamente usado, con edición y vínculo al recurso. |
| S5 — TIC | 24 significados | Cuestionario completo del Diagnóstico del Entorno Digital, instrucciones, saltos y referentes de preguntas incompletas o anafóricas. |
| S6 — Diversos | 5 significados | Aclaraciones de egresos/urgencias, periodo de denuncias, campos de pesca y objeto de clasificación de `CLASIF`. La identidad documental del extracto CONAPO ya está acreditada. |
| V1 — UTH y Presas | V01–V05 | Adopción institucional y edición aplicable de CMPE; edición y respaldo histórico del catálogo de Presas para los periodos reclamados. |
| V2 — Salud y anomalía | V06–V08; `des_mpo_res`; encabezados 177/178 | Ediciones de los catálogos Rickettsia vinculadas a sus periodos; diccionario corregido o fe de erratas que aclare las filas y la falsa referencia. |
| V3 — COESPO | V09–V12 y V15–V16 | Versión del catálogo y vínculo documentado con recursos y periodos; explicar los desfases respecto a productos CONAPO. |
| V4 — Seguridad | V13–V14 | Edición y corte del catálogo SESNSP vinculados a los recursos y años publicados. |

Servicios compartidos:

| Rol | Responsabilidad |
| --- | --- |
| W — Web con Obscura | Buscar y recuperar fuentes primarias para las peticiones de los diez frentes; investigar contenido renderizado, marcos y enlaces que la lectura simple no resuelva. Un único agente maneja el navegador compartido. |
| A — Auditoría documental | Verificar que la fuente realmente respalda la afirmación, su ámbito y edición; contrastar las propuestas sin depender de las conclusiones del autor. |
| B — Auditoría técnica | Cotejar IDs, originales, SHA-256, archivos, localizadores, alcance de reglas, compatibilidad con las validaciones históricas y ausencia de cambios adicionales. |
| Coordinador | Mantener la cola de casos, resolver dependencias, registrar aprobaciones y aplicar los cambios documentados con respaldo. |

Todos los agentes se orquestan con el MCP nativo de OpenCode, comenzando por `opencode_setup`, y usan `opencode-go/muse-spark-1.3-contributor`. Seguir las [instrucciones de Obscura](investigacion-opencode-obscura.md). No crear puentes ni sustituir OpenCode MCP por CLI.

## 3. Fase inicial: comprobar qué investigación nueva es posible

Antes de abrir otra búsqueda por cada caso:

1. Fijar una base nueva de IDs y hashes, conservando los informes y manifiestos anteriores.
2. Leer la evidencia y las búsquedas ya cerradas de R5, R6 y las dos revisiones posteriores.
3. Crear por caso una ficha con la afirmación pendiente, la evidencia que falta y una pista nueva verificable: URL, documento, revisión publicada, archivo o enlace todavía no examinado.
4. Clasificar la entrada como `pista_nueva`, `cambio_de_fuente_por_comprobar` o `sin_pista_nueva`.
5. Activar investigación donde exista una pista concreta. Los casos sin pista conservan su brecha y su investigación previa; no se vuelve a ejecutar una búsqueda genérica para aparentar avance.

Prioridad: fuentes con capacidad de resolver varios casos, como un codebook SINAC, un cuestionario TIC o una declaración de edición de catálogo. No repetir el cotejo CONAPO de 2129 filas ni el examen SEED por ID salvo que aparezca una edición o fuente distinta relevante.

## 4. Investigación paralela y peticiones web

Cada frente conserva una carpeta propia en un expediente nuevo, por ejemplo `propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-<fecha>/`. Las entregas y fuentes anteriores se consultan en lectura.

El frente trabaja con documentos locales y herramientas de consulta independientes mientras W atiende las peticiones que requieren navegador. W entrega resultados por petición; no todos los agentes tienen que esperar a que termine la cola completa.

Cada petición web debe contener:

- ID de petición y lista de IDs completos de los casos relacionados.
- Pregunta documental precisa y motivo por el que una fuente podría responderla.
- Fuentes ya descartadas o examinadas, para evitar repeticiones.
- URL o consulta focalizada, prioridad y alcance: todos los casos indicados o muestra explícita.
- Resultado: fuente recuperada, sin hallazgo en lo examinado, acceso fallido o pista adicional. Registrar el método realmente usado: Obscura, otra herramienta web o material local.

Se pueden examinar publicaciones oficiales, anexos, archivos públicos y versiones históricas localizadas. Una copia histórica sirve solo para lo que su contenido y fecha acrediten: no demuestra por sí sola adopción institucional o vigencia en otro recurso. No contactar publicadores ni enviar mensajes externos.

## 5. Dependencia de las 20 correspondencias

El coordinador mantiene una tabla que enlaza cada uno de los 20 pares estructurales con su definición pendiente y el frente S1–S6 responsable.

Cuando un frente proponga resolver una definición que afecta a uno de esos pares:

1. Auditar primero el significado propuesto y su vínculo con el recurso.
2. Revalidar la evidencia estructural existente contra las huellas actuales.
3. Evaluar la promoción semántica del par con los requisitos actuales del núcleo.
4. Si ambos niveles quedan aprobados, integrar el significado y su correspondencia como cambios explícitos y trazables.

Mientras falte el significado, el par permanece en `par_estructural_revisado_significado_pendiente` y la correspondencia semántica sigue candidata. No se relaja el requisito `respaldada_por_definicion` para conseguir cero candidatas.

## 6. Entregas congeladas y revisión continua

Los casos pueden pasar a revisión a medida que terminan; no es necesario esperar a los diez frentes. Los dos revisores pueden trabajar en paralelo sobre una misma versión congelada.

Cada entrega contiene:

- Una decisión por ID, con original, huella, afirmación propuesta o brecha exacta que subsiste.
- Fuentes originales separadas de extracciones, notas del agente y datos derivados.
- URL, fecha de consulta real, página o localizador y SHA-256 calculado de los bytes. Si no se registró una hora, no inventarla.
- Límites sobre ámbito, periodo, códigos, catálogos y posibles usos.
- JSON serializado y cargable; rutas relativas al proyecto; marcador final con los hashes de todos los archivos entregados.

Flujo de versiones:

`asignado → investigación → entrega congelada → auditorías A y B → aprobado o corrección → integrado / brecha externa`

Una entrega congelada no se edita mientras se revisa. Si se pide una corrección, crear una versión nueva y conservar la anterior; los revisores comprueban el cambio y los nuevos hashes. Esto evita dictámenes que apuntan a archivos modificados después de su revisión.

## 7. Criterios para resolver o cerrar una línea

| Tipo | Se considera resoluble cuando… | No basta con… |
| --- | --- | --- |
| Significado | Una fuente primaria define el campo y acredita el vínculo al instrumento/recurso y edición pertinentes. | Nombre parecido, ejemplo plausible, norma general o coincidencia de distribuciones. |
| Correspondencia semántica | Quedan acreditados el significado y el par estructural bajo las reglas actuales. | Tener el par estructural documentado. |
| Vigencia | Existe evidencia explícita de edición/adopción aplicable al periodo reclamado. | Fecha de descarga, nombre del archivo, versión actual o metadato placeholder. |
| Anomalía o encabezado | Una corrección o aclaración documental de la fuente resuelve la interpretación afectada. | Reconfirmar que la fila está corrupta o eliminarla del inventario original. |

Cerrar la investigación de una línea como `brecha_externa` cuando las pistas concretas se hayan examinado y siga faltando el documento requerido. Identificar qué aportación permitiría reabrirla. Un fallo de acceso queda como `acceso_no_resuelto`, sin declararlo inexistencia. No prometer que otra ronda de agentes resolverá una dependencia documental externa.

## 8. Integración y cierre del lote

Solo tras las aprobaciones A y B:

1. Respaldar el estado que se vaya a modificar.
2. Fijar las nuevas fuentes, aprobaciones y adiciones en un manifiesto nuevo. No modificar manifiestos de rondas anteriores.
3. Preparar la extensión mínima que requiera el tipo de evidencia; no reutilizar automáticamente el staging R7 rechazado de `CLASIF`.
4. Mantener las comprobaciones históricas y la exactitud de la extensión. Regenerar los artefactos afectados y cotejar que el delta coincida con lo aprobado.
5. Aplicar las validaciones de datos y SHACL pertinentes si cambia el RDF. Las pruebas de código se añaden o ejecutan cuando el usuario las solicite.
6. Sincronizar Studio con respaldo únicamente si existe un cambio de grafo aprobado. Si solo se mejora evidencia documental, conservar el grafo y sus conteos.
7. Cerrar con un informe que separe resoluciones semánticas, avances estructurales, vigencias acreditadas, correcciones de fuente y brechas externas. No sumar categorías solapadas como si fueran casos distintos resueltos.

Resultado mínimo verificable: todos los IDs tienen una decisión actualizada y evidencia o dependencia concreta; ninguna promoción carece de aprobación y ninguna búsqueda ya agotada se presenta como nueva. Gemma queda fuera de asignaciones, cambios, pruebas y reinicios.
