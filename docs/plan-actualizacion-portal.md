# Plan de actualización ante novedades del portal de Sonora

Fecha: 2026-10-26, America/Mexico_City. Estado: propuesta de implementación; no se ejecutó una actualización ni se configuró un monitor.

## Objetivo

Detectar publicaciones nuevas y modificaciones, recuperar su evidencia y preparar un nuevo corte verificable sin perder el historial ni convertir hipótesis en significados aceptados. Normalmente se actualizan las instancias y su evidencia; solo se cambia el vocabulario o las reglas SHACL si el contenido nuevo exige representar algo que el modelo actual no contempla.

## Revisión realizada y límites

- Se revisaron README, AGENTS, la guía de versionado y los scripts de catálogo, inventario, inspección, ampliación y cruces. Existen piezas para reconstruir y validar; falta unirlas en un procedimiento incremental con un registro de cambios y publicación controlada.
- El MCP respondió correctamente a `onto_status`. No se consultaron archivos Turtle para investigar el grafo.
- Se probó `package_search` con `rows=1` y orden de modificación mediante `api()` de `scripts/descargar_ckan.py`, conservando su User-Agent. La respuesta ofrece identificadores y campos de modificación de conjuntos y recursos, además de `hash` y `size`; su presencia no garantiza que tengan valores útiles o actualizados.
- Esta prueba no fue un inventario completo ni una comparación contra la carga local. No acredita documentos nuevos, retirados ni ausencia de novedades.
- El acceso web genérico al portal devolvió 403. La prueba con el helper autorizado sí respondió.
- Referencia de la API: [documentación oficial CKAN](https://docs.ckan.org/en/2.11/api/index.html). La disponibilidad de cada función debe comprobarse en Sonora; no se presupone que exponga historial, notificaciones o webhooks.

## Hallazgos que condicionan la implementación

| Pieza existente | Qué aporta | Ajuste necesario |
| --- | --- | --- |
| `explorar_catalogo.py` | Paginación por ID; comprueba total y duplicados | Un total estable no detecta todas las modificaciones durante el recorrido. Incorporar conciliación y huellas. |
| `construir_catalogo.py` | Identidades por UUID y exportación del catálogo | Su snapshot de recursos no conserva todos los campos de modificación/hash/tamaño. Añadir un manifiesto específico para detección. |
| `inventariar_portal.py` | Recursos, páginas enlazadas y esquemas DataStore | Genera archivos de uso corriente; necesita salida por ejecución. Si usa portada guardada por error HTTP, declarar ese alcance como antiguo/parcial. |
| `inspeccionar_contenido.py` | Estructuras, diccionarios y caché por recurso | La reutilización depende principalmente de la URL. Un archivo sustituido en la misma URL puede pasar inadvertido. `--refresh` existe, pero opera sobre el conjunto procesado y falta selección incremental por recurso. |
| `descargar_ckan.py` | Descarga autorizada con User-Agent | Centralizar también las lecturas remotas que hoy hace el inspector. Añadir límites, huellas, reintentos y selección explícita de recurso; la CLI actual tiene filtros particulares para ciertos conjuntos de Hermosillo. |
| `ampliar_portal.py` | Comprueba IDs y huellas de algunos derivados | Inventario y catálogo deben pertenecer al mismo corte. Un cambio puede invalidar oportunidades, validaciones y evidencias históricas dependientes. |
| Guía de versionado | Historial, hashes, auditorías y un escritor | Aplicarla a cada corte nuevo. Preservar dictámenes y manifiestos cerrados. |
| Carga y Studio | Nueva instantánea y sincronización con respaldo | Revisar la ruta de publicación antes de ejecutarla: los scripts históricos de carga invocan el motor y el contrato vigente de agentes permite solo lectura por MCP/CLI. No asumir que esos comandos están autorizados por este plan. |

## Flujo propuesto por actualización

### 1. Congelar una base de comparación

Registrar el manifiesto de la última carga aceptada, hashes de insumos y derivados, configuración/base IRI y referencia al store vigente. Conservar los archivos históricos y trabajar en un directorio independiente, por ejemplo `data/actualizaciones/<id-ejecucion>/`.

La primera ejecución crea una línea base. Si el snapshot histórico omite campos necesarios, declarar esa limitación; no inventar diferencias retrospectivas. La consulta al grafo se mantiene en MCP o CLI canónica, sin abrir el store desde otro proceso ni borrar LOCK.

### 2. Detectar altas, modificaciones y posibles retiradas

Recorrer el catálogo público completo por API y comparar por UUID de conjunto y recurso. Guardar los campos necesarios, excluyendo contactos personales. Verificar `success`, paginación, duplicados y cobertura; si el catálogo cambia durante el recorrido, repetir o dejar la ejecución incompleta.

Comparar nombre, descripción, organización, URL, formato, fechas, tamaño, hash publicado y estado DataStore. Las fechas son señales de revisión; no prueban por sí mismas si cambió el archivo. Separar una huella normalizada de metadatos de la huella de bytes para evitar falsos cambios por orden o fecha local de ejecución.

Producir un delta con: nuevo conjunto, nuevo recurso, cambio de metadatos, cambio de archivo, cambio de estructura, cambio de diccionario, posible retirada, error y sin cambios observados. Incluir estado de cobertura y procedencia de cada detección.

Una URL reutilizada exige revalidación del contenido: usar ETag/Last-Modified cuando estén disponibles y contrastar bytes con SHA-256 según la política de descarga. Programar comprobaciones de contenido aun sin cambios de metadatos. Una lectura parcial solo acredita el fragmento leído; no demuestra identidad del archivo completo.

Una ausencia solo se convierte en posible retirada después de un inventario completo y una comprobación individual. Un 403, timeout o fallo de página deja acceso pendiente. Preservar la evidencia histórica; confirmar el cambio de disponibilidad en otra ejecución antes de modificar su representación vigente.

### 3. Recuperar evidencia de los recursos afectados

Descargar exclusivamente por `scripts/descargar_ckan.py` o sus funciones, ampliadas para el flujo nuevo. Conservar URL original y final, UUID, fecha UTC de captura, estado HTTP, bytes leídos, alcance completo/parcial y SHA-256 claramente identificado. No sobrescribir evidencia previa.

Para datos tabulares, comparar hojas, columnas, tipos y estructura. Para diccionarios, recuperar las definiciones y conservar su ubicación original. Para PDF/DOCX u otros documentos narrativos, incorporar un extractor específico con referencia a página/sección y revisión; la inspección tabular existente no acredita por sí sola su contenido. El texto extraído u OCR será evidencia candidata hasta comprobarlo contra el documento.

Si solo cambia un dato de catálogo, no reinterpretar variables innecesariamente. Si cambia el archivo de datos, revisar estructura y perfiles afectados. Si cambia el diccionario, revisar las definiciones y correspondencias que dependían de su versión anterior. Si falta diccionario, registrar el recurso y declarar el hueco documental.

### 4. Evaluar el impacto semántico

Crear un expediente por cambio con IRI de conjunto/recurso/columna pertinentes, URL y versión del diccionario, fecha de captura y referencia a la carga que lo incorpora. Mantener identidades estables cuando siga siendo la misma entidad; una reutilización de nombre con otro significado necesita historial/versionado explícito.

Localizar dependencias: definición → variable → correspondencia → perfiles/catálogos → oportunidades de cruce e informes. Una aceptación anterior queda asociada a la evidencia que la respaldó. Si esa evidencia cambia, marcar la aplicación a la versión nueva como pendiente de revisión, sin borrar el dictamen histórico ni transferirlo automáticamente.

Conservar separados `estadoSemantico` y `estadoCorrespondencia`. Las coincidencias de nombres permanecen candidatas. Revisar periodo, población, unidad, granularidad y códigos antes de aceptar equivalencias; un diccionario nuevo tampoco autoriza un join.

Preparar propuestas trazables y obtener los dos dictámenes independientes exigidos por la guía de versionado antes de integrar un corte. Si posteriormente se emplea OpenCode, usar sesiones nuevas con `opencode-go/muse-spark-1.3-contributor`; si falta cuota, informar y esperar instrucciones conforme a la instrucción vigente.

### 5. Regenerar derivados y validar en aislamiento

Con un solo escritor, reconstruir catálogo e inventario coherentes desde la misma captura y regenerar las capas afectadas. El flujo debe poder consumir un snapshot guardado: ejecutar dos consultas remotas independientes para catálogo e inventario puede mezclar cortes.

Revisar las huellas y contratos de todas las rondas instaladas antes de recomponerlas; no alterar manifiestos históricos para hacer pasar la validación. Los derivados vigentes que dependan de entradas modificadas deben recalcularse o declararse no vigentes. `mapear_cruces.py` y `validar_lote_cruces.py` son piezas existentes a revisar según el impacto; no ejecutar cruces nuevos como consecuencia automática de una novedad.

Generar Turtle mediante el pipeline y comprobar sintaxis, SHACL, referencias, identidades, cobertura, preservación del historial y consultas afectadas. Los hashes de entrada deben corresponder a los usados realmente. SHACL conforme es una condición necesaria, no una certificación de exactitud documental.

### 6. Preparar y publicar el corte

Generar un informe con altas, cambios, acceso pendiente, revisiones aceptadas/rechazadas, dependencias invalidadas, hashes y resultados de validación. La detección puede terminar correctamente aunque haya recursos pendientes; no presentar esa ejecución como cobertura documental completa.

La ruta de publicación debe quedar compatible con el contrato vigente antes de ejecutar escrituras. Después, crear una instantánea separada, comprobarla y promover el manifiesto activo únicamente al final. Reconectar el MCP al nuevo store según corresponda; evitar cambiar archivos del store en uso. Conservar la instantánea anterior para reversión.

Si se actualiza Studio, respaldar primero, preservar ediciones ajenas al pipeline y verificar el resultado sincronizado. Si falla una fase de publicación, mantener o restaurar el corte aceptado y registrar exactamente qué componentes llegaron a cambiar.

## Implementación por fases

| Fase | Entregable propuesto | Criterio de terminación |
| --- | --- | --- |
| A. Detector | `detectar_cambios_portal.py`, snapshots y manifiesto del delta; nombres propuestos, aún no existen | Detecta recurso nuevo, metadatos cambiados y cobertura incompleta sin tocar la carga activa. |
| B. Evidencia incremental | Helper de descarga ampliado, inspector con selección por ID y caché versionada | Detecta reemplazos en la misma URL y distingue huella parcial de completa. |
| C. Revisión e impacto | Expedientes documentales, dependencias y propuestas de revisión | Un diccionario modificado identifica todas las decisiones afectadas y conserva su historial. |
| D. Construcción y publicación | Orquestador con staging, validaciones, recibo y reversión | Un fallo no sustituye la carga aceptada; una segunda ejecución idéntica no duplica entidades ni propuestas. |
| E. Operación periódica | Monitor programado y política de alertas, solo después de validar A–D | Informa cambios útiles y fallos; permanece silencioso ante ejecuciones sin novedades. |

Orden recomendado: implementar A y probar un delta real; continuar con B; resolver un caso documental en C; ensayar D con reversión; finalmente programar E. No hace falta reconstruir todo el significado del portal en cada revisión.

## Frecuencia propuesta

Consulta diaria de metadatos y revisión semanal del contenido/diccionarios, ajustable al volumen y a los límites del portal. Realizar conciliación completa semanal y verificaciones de contenido escalonadas para detectar sustituciones silenciosas. Informar por separado qué recursos se revisaron y cuáles no; una revisión escalonada no prueba ausencia global de cambios.

No se configuró ninguna automatización en esta revisión. La primera etapa operará en modo diagnóstico y entregará el delta para revisión.

## Casos de aceptación del futuro actualizador

1. Nuevo archivo en un conjunto existente: aparece una alta sin duplicar el conjunto.
2. Archivo reemplazado conservando URL y UUID: se detecta al revalidar contenido y se conserva la versión anterior.
3. Cambio exclusivamente descriptivo: actualiza metadatos sin promover nuevos significados.
4. Diccionario modificado: identifica correspondencias y afirmaciones afectadas; exige revisión para la nueva evidencia.
5. Archivo sin diccionario o extracción parcial: registra el hueco y el alcance sin completar significados por suposición.
6. API incompleta o inaccesible: no informa retiradas ni ausencia global de novedades.
7. Columna retirada o renombrada: conserva su historial y deja explícitas las correspondencias pendientes de revisión.
8. Validación fallida o cambio concurrente: no promueve la carga candidata.
9. Reejecución con los mismos insumos: no genera altas ni propuestas duplicadas; distingue observación de cambio material.
10. Publicación y reversión de prueba: el MCP vuelve al corte previsto y Studio conserva sus ediciones propias.

## Referencias locales

- [Contrato de agentes](../AGENTS.md).
- [Construcción y actualización](../README.md#construcción-y-actualización).
- [Versionado y lanzamientos](versionado-y-lanzamientos.md).
- [Modelo del portal](modelo-portal.md).
- [Plan tras R10](plan-actualizado-tras-r10.md).

Este plan añade un procedimiento de mantenimiento; no sustituye los cierres ni las decisiones semánticas de rondas anteriores.
