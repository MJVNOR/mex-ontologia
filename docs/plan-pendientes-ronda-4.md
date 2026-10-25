# Ronda 4: revisión paralela de pendientes

Autorizada el 23 de octubre de 2026. Doce sesiones OpenCode con `opencode-go/muse-spark-1.3-contributor`, hasta seis activas a la vez; Codex integra en secuencia.

Base: 865 correspondencias revisadas, 1212 significados respaldados, 940 conceptos. Pendientes: 3283 columnas candidatas, 351 significados, 12 enlaces ambiguos en seis columnas, cinco inconsistencias documentales, des_mpo_res, 16 vigencias históricas y evaluación real del chat.

| Sesión | Columnas candidatas | Significados pendientes | Responsabilidad adicional |
| --- | ---: | ---: | --- |
| lote-1 | 702 | 20 | Revisión documental por conjunto y diccionario |
| lote-2 | 667 | 28 | Revisión documental por conjunto y diccionario |
| lote-3 | 288 | 123 | Revisión documental por conjunto y diccionario |
| lote-4 | 592 | 47 | Revisión documental por conjunto y diccionario |
| lote-5 | 515 | 67 | Revisión documental por conjunto y diccionario |
| lote-6 | 519 | 66 | Revisión documental por conjunto y diccionario |
| ambiguedades | 6 ambiguas | — | 12 enlaces alternativos y cinco inconsistencias |
| investigacion | — | — | Búsqueda oficial con Obscura; un único propietario del navegador |
| catalogos | — | — | Una referencia sin resolver y 16 vigencias históricas |
| chat | — | — | Respuestas reales, evidencia y límites en Studio |
| auditoria-a | — | — | Significados, conceptos y fuentes de versiones SHA exactas |
| auditoria-b | — | — | Correspondencias, integridad y regresiones de versiones SHA exactas |

Las asignaciones conservan cada conjunto en un único lote y ponderan el esfuerzo de revisar significados. Se fijan en `propuestas/pendientes-muse-r4/fuentes/manifiesto.json`; el respaldo central está en `integrador/antes-r4.zip` dentro de esa carpeta.

Cada agente escribe exclusivamente en su carpeta. Entrega decisiones exhaustivas, propuestas, evidencia localizable, pendientes precisos y marcador final con SHA-256. Una coincidencia de nombre no basta para revisar una correspondencia. No se infieren versiones históricas ni aplicación de catálogos nacionales.

Secuencia: fijar base; investigar y preparar propuestas; auditar los archivos finales; corregir y volver a revisar; integrar únicamente aceptaciones exactas; generar, ejecutar pruebas y SHACL; sincronizar con respaldo y comprobar Studio. La evaluación del chat prepara casos durante la revisión y contrasta el resultado final después de la integración.

El cierre requiere decisión trazable para cada pendiente. La ausencia de documentación puede justificar un pendiente explícito; no una confirmación supuesta. Los informes distinguirán revisión realizada, propuesta aceptada, integración y bloqueo externo.

## Ampliaciones autorizadas durante la ejecución

Los 175 significados propuestos hicieron aparecer 336 columnas candidatas adicionales: 44, 41, 62, 81, 23 y 85 por lote, respectivamente. Se revisan en las mismas sesiones, con asignaciones adicionales fijadas por SHA, conservando las propuestas semánticas.

El usuario pidió aumentar agentes: la ronda pasa a **16 sesiones Muse 1.3**, hasta **8 activas simultáneamente**. Los cuatro roles adicionales son regresiones semánticas adversariales, auditoría transversal de medidas/calificadores, diagnóstico y parche aislado de recuperación F2, y revisión de oráculos del chat. Sus carpetas son exclusivas y no pueden modificar el núcleo ni la instalación.

El usuario también autorizó cambiar el modelo del chat de Studio, indicando Gemini 3.1 Flash Lite o Gemma 4 31B. El evaluador comprobará disponibilidad y configuración activa, conservará los resultados del modelo anterior y distinguirá pruebas por API, sidecar e interfaz.
