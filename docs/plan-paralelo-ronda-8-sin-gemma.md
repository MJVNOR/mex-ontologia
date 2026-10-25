# Plan y ejecución paralela R8 — sin Gemma

Estado: **ejecutado, validado y cerrado**. [Resultados R8](../reports/ronda-8.md). El reparto y la secuencia siguientes conservan el plan original.

Inicio: 2026-10-24T08:40:30.027809+00:00

## Reparto

| Agente | Casos | Trabajo |
| --- | ---: | --- |
| M1-sinac | 14 | Primeras 14 correspondencias nuevas SINAC; verificar evidencia física y significado R7 exactos. |
| M2-sinac | 14 | Últimas 14 correspondencias nuevas SINAC; verificar evidencia física y significado R7 exactos. |
| M3-anteriores | 17 | 17 candidatas previas; identidad física ya revisada, dependencia semántica pendiente; no promover sin significado. |
| S1-defunciones | 32 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| S2-nacimientos | 22 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| S3-matriculas | 30 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| S4-epidemiologia | 25 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| S5-tic | 24 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| S6-diversos | 5 | Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas. |
| V1-uth-presas | 5 | Vigencias: distinguir publicación, periodo de datos, edición y aplicabilidad; sólo casos de vigencia. |
| V2-salud-anomalias | 3 | Vigencias: distinguir publicación, periodo de datos, edición y aplicabilidad; sólo casos de vigencia. |
| V3-coespo | 6 | Vigencias: distinguir publicación, periodo de datos, edición y aplicabilidad; sólo casos de vigencia. |
| V4-seguridad | 2 | Vigencias: distinguir publicación, periodo de datos, edición y aplicabilidad; sólo casos de vigencia. |
| X-anomalias | 3 | Aclarar des_mpo_res y dos encabezados corruptos; conservar original, no inventar catálogo ni significados. |
| T-pruebas | 0 | Suite Python R7: corregir fallos preservando invariantes históricos, ampliar cobertura específica R7 y proponer adaptación futura R8. |
| W-web | 0 | Único navegador Obscura compartido. Atender peticiones por archivo; fuentes primarias y evidencia real, sin repetir consultas agotadas. |

## Secuencia

1. Revisar en paralelo las 45 correspondencias, 138 significados, 16 vigencias y tres registros de anomalía; ejecutar suite R7.
2. Congelar cada entrega y sus fuentes. Investigación web centralizada por MCP Obscura, sólo pistas nuevas o cambios comprobables.
3. Auditar propuestas con dos revisores independientes; auditar código y pruebas.
4. Respaldar y crear nueva evidencia/manifiesto R8. Integrar sólo decisiones acreditadas, preservando rondas anteriores.
5. Regenerar, ejecutar suite completa, validar RDF/SHACL y sincronizar Studio con respaldo.
6. Cerrar con resultados y condiciones concretas para reabrir brechas externas.

Modelo de agentes: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, mensajes externos, definiciones o vigencias inventadas.
