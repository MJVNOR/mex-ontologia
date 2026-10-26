# Instrucciones para agentes

## Consulta de la ontología (contrato para LLMs)

- Habla con el grafo solo vía MCP `mex-ontologia` (`opencode.json`, tools
  `onto_query/onto_stats/onto_status/onto_validate/onto_shacl`, modo persistente).
  Sin MCP, usa `uv run python scripts/consultar_ontologia.py <significado|correspondencias|resumen|sparql>`.
  Nunca `tools/open-ontologies.exe` directo ni `.ttl` a mano.
- El lanzador MCP y la CLI canónica comparten un backend persistente por almacén.
  Para consultas simultáneas, crear sesiones MCP independientes sobre ese backend;
  no abrir el store desde cada agente. No borrar archivos LOCK. Después de migrar
  desde el lanzador antiguo, reconectar una vez las sesiones que retenían el store.
- `estadoSemantico` de la variable ≠ `estadoCorrespondencia` del enlace columna↔variable.
  Una `candidata_por_nombre` es hipótesis, no dato; 4506 revisadas no autorizan ningún join.
- "No recuperado" ≠ "no existe". La ausencia exige consulta de alcance completo;
  el vecindario parcial se declara parcial (`parcial: true`, conteo completo aparte).
- Toda afirmación con dato lleva IRI de conjunto/recurso/columna, URL del diccionario
  y fecha de carga; sin evidencia se declara el hueco, no se rellena.
- Solo lectura. `sparql` libre exige `LIMIT` (máx 2000); `INSERT/DELETE/LOAD` se rechazan.
  Cruces: `scripts/consultar_cruces.py`, no SPARQL.
- Descargas CKAN (`datos.sonora.gob.mx`) solo vía `scripts/descargar_ckan.py` (`User-Agent` obligatorio; sin él el portal da 403). No `urlretrieve`/`curl` sin cabecera ni `.ttl` a mano.

## Modelos de OpenCode

- **Instrucción vigente del usuario (2026-10-24, reanudación):** continuar con **Muse 1.3**, proveedor `opencode-go`, modelo `muse-spark-1.3-contributor`. Sustituye la instrucción temporal de usar DeepSeek Free, cuya cuota también se agotó. No cambiar automáticamente de modelo si vuelve a faltar cuota; informar y esperar indicación.
- Las sesiones existentes de OpenCode V2 conservan su modelo: para retomar con Muse las tareas interrumpidas de DeepSeek, crear sesiones nuevas con el proveedor y modelo indicados.
- Usar siempre **Muse 1.3** (`opencode-go/muse-spark-1.3-contributor`) como modelo principal en OpenCode para todas las tareas de este proyecto.
- Si se agota la suscripción o la cuota de OpenCode que permite utilizar Muse 1.3, continuar con **DeepSeek V4.1 Flash Free** como modelo de respaldo.
- Antes de utilizar el respaldo, consultar el catálogo de modelos de OpenCode para obtener su identificador exacto; no inventarlo ni seleccionar una variante de pago.
- Mantener esta prioridad salvo que el usuario indique expresamente otra cosa.
