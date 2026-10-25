# Orquestación de ronda 3

El usuario autorizó ejecutar sesiones OpenCode en paralelo en modo Build y amplió la autorización al número de agentes necesario. Se iniciaron trece sesiones con Muse Spark 1.3, incluida una sesión para preparar el soporte de calificadores documentales. La asignación posterior entre chats tiene precedencia sobre la distribución inicial de esta página.

## Coordinación entre chats

El usuario indicó: «Coordínate con “Revisar errores de la antología”: que integre la semántica; aquí termina chat, correspondencias y cruces».

- **Revisar errores de la antología** (`01a1685c-0a24-76d0-89e8-776e71e02dbc`) es el único integrador de reglas, conceptos, calificadores y cobertura semántica. Reutiliza las sesiones 6–12 y 4 en carpetas nuevas bajo `propuestas/cobertura-muse-20261023/`, sin sustituir las entregas históricas de ronda 3.
- **Configura Open Ontologies para Son** (`01a1670e-26ce-76b0-9bf3-d1d731c8630d`) termina el chat, las 29 correspondencias aprobadas y la evidencia de cruces de tres fichas. Prepara estos cambios aislados mientras el otro chat escribe el núcleo.
- El integrador semántico publicará `propuestas/cobertura-muse-20261023/integrador/coordinacion.json` con `semantica_lista: true`. Hasta ese relevo, este chat no modifica `ontologia/semantica.json`, ni regenera ni sincroniza el grafo central.
- Después del relevo se incorporan las 29 correspondencias conservando exactamente las 836 anteriores y todas las reglas y conceptos aceptados. La guardia de cobertura debe comprobar explícitamente esas adiciones documentadas, sin permitir cambios arbitrarios.
- La carga final del grafo se hace en secuencia, conservando ediciones ajenas y verificando la procedencia y las consultas.

### Estado comprobado del ámbito de este chat

- Chat: cambios compilados e instalados con respaldo; 44 pruebas del sidecar y seis casos de recuperación por API. Studio reabierto y conectado. La respuesta desde la interfaz no se probó: la guarda detectó actividad del usuario y después la ventana estaba minimizada. No se hicieron llamadas al modelo.
- Correspondencias: 29 aprobadas con huellas; 89 del subconjunto original siguen pendientes y tres columnas mantienen seis vínculos ambiguos. Aplicación central pendiente del relevo.
- Cruces: tres fichas aprobadas; el caso nuevo contrasta 72 claves de proyecciones en 2020 con archivos originales y comprobación independiente. No acredita vigencia, identidad entre medidas ni comparabilidad de todos los 3916 pares del triaje.

Los comprobantes están en `propuestas/ronda-3/integrador/instalacion-chat.json`, `revision-agente-2.json`, `revision-agente-5.json` y `control-cruce-2020.json`.

### Cierre después del relevo

El relevo se recibió con `semantica_lista: true` y se completó la etapa posterior. Hay 865 correspondencias revisadas, tres fichas, 72 comparaciones de 2020 y 144 evidencias por fuente. Studio contiene 284,810 triples, con sincronización verificada y SHACL conforme. Pasan 108 pruebas centrales, 45 del sidecar y seis casos de recuperación HTTP contra el grafo final, sin llamadas al modelo. La respuesta desde la interfaz sigue sin evaluar. Las cifras y pendientes de la sección anterior describen el estado previo al relevo; el cierre comprobado está en `reports/integracion-ronda-3.md` y `.json`.

## Base de partida

Ronda 2 integrada: 836 correspondencias revisadas, 118 candidatas, 3 columnas ambiguas / 6 vínculos, 103 conceptos y 232 variables respaldadas. Quedan 23 significados candidatos; la auditoría de columnas registra 3720 con definición sin interpretación compartida, 833 sin definición coincidente y 13 sin diccionario. Las 16 referencias identificadas siguen sin vigencia temporal acreditada. Estos conteos deben verificarse contra las fuentes actuales.

## Sesiones y propiedad de archivos

| Agente | Sesión OpenCode | Carpeta exclusiva | Trabajo |
| --- | --- | --- | --- |
| 1 | ses_e97b6d2e7ffeWUX2OPHw0hmn2t | propuestas/ronda-3/agente-1-chat/ | Corrección revisable de recuperación y evaluación del chat; fuente copiada, patch y pruebas, sin despliegue |
| 2 | ses_e97b6d265ffePOFbDEVwokVDFL | propuestas/ronda-3/agente-2-correspondencias/ | Revisión de las 118 candidatas y 3 columnas ambiguas; conserva las 836 revisadas |
| 3 | ses_e97b6d1ecffeIEnKNbGH5bqq2I | propuestas/ronda-3/agente-3-cobertura/ | Inventario completo de cobertura y propuestas de significados fuera del núcleo; sin correspondencias |
| 4 | ses_e97b6d17fffeGUYl2jA7kTCO7H | propuestas/ronda-3/agente-4-aclaraciones/ | 23 significados candidatos, 5 observaciones y des_mpo_res; documentación publicada y preguntas sin contactar |
| 5 | ses_e97b6d103ffeI5GgFipPiarob2 | propuestas/ronda-3/agente-5-cruces/ | Inventario de cruces existentes y validación detallada de al menos 3 casos; periodos, claves, grano, unidades y vigencia |
| 6 | ses_e97ae8882ffeKNwnUYF2junU2r | propuestas/ronda-3/agente-6-salud/ | 242 definiciones de salud y vigilancia |
| 7 | ses_e97ae87b1ffeOwyrF4IW4XM8rw | propuestas/ronda-3/agente-7-registro-civil/ | 163 definiciones de nacimientos, defunciones, matrimonios y divorcios |
| 8 | ses_e97ae86e7ffeDHFxVYP2Oz2CnJ | propuestas/ronda-3/agente-8-educacion/ | 126 definiciones de educación |
| 9 | ses_e97ae8610ffe7OyK9rf6MIF62F | propuestas/ronda-3/agente-9-gobierno-digital/ | 243 definiciones de gobierno digital |
| 10 | ses_e97ae851cffekVlauaHUKbPOUn | propuestas/ronda-3/agente-10-territorio-economia/ | 468 definiciones territoriales, sociales y económicas restantes |
| 11 | ses_e97a8d513ffeM1pOL7u5Ubpqdz | propuestas/ronda-3/agente-11-auditoria/ | Auditoría independiente de significados de los agentes 3, 7, 8, 9 y 10; colisiones y alcance |
| 12 | ses_e97a6dd9fffe5cXhVuZWN0eXVE | propuestas/ronda-3/agente-12-auditoria-salud/ | Auditoría independiente de cada propuesta de salud del agente 6 |
| 13 | ses_e97998776ffeJNk5fWPTkgTWLW | propuestas/ronda-3/ | Preparación aislada del soporte de calificadores; el otro integrador implementó el núcleo y no se aplica el patch duplicado |

Los agentes 6–10 tienen una partición exacta de 1242 definiciones sin lectura completa, fijada por IRI en `propuestas/ronda-3/integrador/asignaciones-semanticas.json`. Se excluyen las 66 leídas por el agente 3 y los 23 significados candidatos del agente 4. Una decisión por definición no implica promoción: lo insuficientemente documentado permanece pendiente.

Proveedor/modelo conservado de la ronda anterior: opencode-go / muse-spark-1.3-contributor. Las sesiones se crearon explícitamente con agente build. Los identificadores de sesión permiten continuar sin duplicar ejecuciones ante una desconexión.

## Reglas de coordinación

- Los agentes leen las fuentes centrales y entregas históricas sin modificarlas. No consumen propuestas concurrentes de otros agentes.
- Excepción explícita: los auditores 11 y 12 leen las propuestas asignadas para emitir dictámenes independientes, sin modificarlas.
- Solo el integrador modifica núcleo, informes centrales, scripts centrales o Studio. El agente de chat prepara cambios dentro de su carpeta, sin modificar el repositorio upstream ni la aplicación instalada.
- Cada entrega preserva literales, IRIs y huellas y aporta un verificador con casos negativos. Un resultado pendiente es válido si falta evidencia.
- Las consultas al motor vivo son de lectura. No se envían mensajes a publicadores. No se copian credenciales ni se cambian proveedores para eludir cuotas.
- El agente de chat comienza con pruebas deterministas y tiene un máximo de cuatro solicitudes al modelo configurado; se detiene ante el primer error de cuota o disponibilidad.

## Revisión e integración

1. Revisar cambios, fuentes y alcance de cada entrega; ejecutar verificadores solo después de inspeccionarlos y repetir controles independientes.
2. Devolver correcciones a la sesión responsable. No aprobar por conteos o pruebas que solo reproducen el resumen.
3. Respaldar el núcleo y fijar las entregas aprobadas con manifiesto SHA-256, preservando las rondas históricas.
4. Integrar significados aprobados antes de correspondencias que dependan de ellos. Las propuestas concurrentes no se aplican entre sí automáticamente.
5. Integrar dictámenes y controles como evidencia calificada; no convertirlos en identidad territorial, vigencia ni autorización automática de cruces.
6. Probar el patch del chat, comprobar compatibilidad con las ediciones existentes y respaldar antes de instalarlo. Verificar el componente instalado y distinguir prueba de fuente/API de prueba de interfaz.
7. Ejecutar las pruebas centrales y SHACL, sincronizar Studio conservando ediciones ajenas y verificar consultas contra el grafo vivo.

La integración sigue también `docs/integracion-de-agentes.md`. La finalización de una sesión no implica aprobación ni despliegue. Se documentan las limitaciones que requieran información del publicador, sin inventar una resolución.
