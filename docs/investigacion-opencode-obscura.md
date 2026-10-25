# Investigación web con OpenCode y Obscura

Instrucción del usuario: los agentes OpenCode pueden usar el MCP de Obscura para investigar en la web lo que no esté suficientemente documentado. Esta autorización forma parte del trabajo paralelo de cierre de brechas del proyecto.

- Orquestar agentes mediante el MCP nativo de OpenCode, comenzando por `opencode_setup`; modelo solicitado: `opencode-go/muse-spark-1.3-contributor`.
- Usar el MCP de Obscura disponible en OpenCode para consultar páginas, documentos y enlaces relevantes. Comprobar primero su disponibilidad real; no confundir las herramientas visibles al coordinador con las herramientas accesibles dentro de OpenCode.
- No crear puentes, scripts de conexión ni sustituir el MCP de OpenCode por su CLI. Si Obscura no está disponible en una sesión, registrar el límite y continuar con las herramientas web nativas disponibles o el material local preservado.
- Las búsquedas sirven para descubrir evidencia. Las conclusiones técnicas se sustentan en fuentes primarias, con URL, fecha de consulta, página o localizador y copia local con SHA-256 cuando sea posible.
- Conservar separados el documento original, la extracción de texto y el análisis del agente. Verificar el contenido y la URL antes de atribuir una afirmación a una fuente.
- Evitar interferencias entre agentes en un navegador compartido: asignar la navegación Obscura a un agente de investigación web y entregar peticiones y resultados a través de archivos del expediente. Los demás agentes trabajan en paralelo con su evidencia local y herramientas de consulta independientes.
- Examinar primero la investigación ya cerrada. Una consulta repetida debe responder una pista nueva o verificar un cambio concreto; no volver a presentar material conocido como evidencia nueva.
- No inventar definiciones, códigos, vigencias, equivalencias ni autorizaciones de cruces. Una búsqueda negativa o un error HTTP no prueban inexistencia ni posesión exclusiva de un documento.
- No contactar publicadores ni enviar mensajes externos. No modificar el chat de Gemma.
- Preparar propuestas en staging. Someter los cambios acreditados a revisión independiente antes de integrarlos; conservar rondas y manifiestos anteriores.

Expediente de esta ejecución: `propuestas/cierre-brechas-post-r6/`. Los resultados deben distinguir casos resueltos, propuestas sin aprobar y brechas que continúan abiertas.
