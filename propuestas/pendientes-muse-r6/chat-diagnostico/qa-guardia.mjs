/** Guardia QA: decision ante respuesta final vacia (logica del parche index.ts).
 * Regla: si `answerOnce` devuelve vacio (thought-only recortado, recitacion,
 * mensaje sin contenido), NO caer a runTurn con las 114 tools: emitir error
 * claro, sin mutacion del grafo y sin escribir la cache (un vacio cacheado
 * envenena futuras preguntas con la misma clave).
 */
export function decidirRespuestaQA(respuesta) {
  const texto = String(respuesta ?? '').trim();
  if (texto) return { accion: 'responder', cachear: true };
  return {
    accion: 'error-sin-fallback',
    cachear: false,
    mutacion: false,
    error: 'El modelo devolvio una respuesta vacia (sin contenido final). No se ejecuto ninguna herramienta ni se modifico el grafo. Reintente la pregunta.',
  };
}
