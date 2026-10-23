import { pathToFileURL } from 'node:url';
import path from 'node:path';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
const root = 'C:/Users/marti/Documents/MEX-Ontologi';
const outDir = root + '/propuestas/ronda-2/agente-5-evaluacion-chat/respuestas_brutas';
await mkdir(outDir, { recursive: true });
const agentDir = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const { retrieve, asContext, QA_SYSTEM_PROMPT } = await import(pathToFileURL(agentDir + '/graphrag.ts').href);
const { OpenAICompatibleProvider } = await import(pathToFileURL(agentDir + '/providers/openai.ts').href);
const envText = await readFile(root + '/.env', 'utf8');
const settings = {};
for (const line of envText.split(/\r?\n/)) {
  const m = line.trim().match(/^(ONTO_(?:PROVIDER|LLM_BASE_URL|LLM_MODEL|LLM_API_KEY))\s*=\s*(.*)$/);
  if (m) settings[m[1]] = m[2].trim().replace(/^(["'])(.*)\1$/, '$2');
}
if (!settings.ONTO_LLM_BASE_URL || !settings.ONTO_LLM_MODEL || !settings.ONTO_LLM_API_KEY) throw new Error('missing model config');
const casos = JSON.parse(await readFile(root + '/propuestas/ronda-2/agente-5-evaluacion-chat/casos.json', 'utf8'));
const mcp = { async callTool(name, args) {
  if (name !== 'onto_query') throw new Error('unexpected tool ' + name);
  const r = await fetch('http://127.0.0.1:8137/api/query', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(args) });
  if (!r.ok) throw new Error('Engine HTTP ' + r.status);
  return await r.text();
}};
const registro = [];
for (const c of casos) {
  const t0 = Date.now();
  let estado = 'ejecutado', errores = '', respuesta = '', contexto = '', resumenRec = '';
  try {
    const retrieved = await retrieve(mcp, c.pregunta);
    contexto = asContext(retrieved);
    resumenRec = 'anchors=' + retrieved.anchors.length + ' facts=' + retrieved.facts.length;
    const provider = new OpenAICompatibleProvider({ system: QA_SYSTEM_PROMPT, baseURL: settings.ONTO_LLM_BASE_URL, model: settings.ONTO_LLM_MODEL, apiKey: settings.ONTO_LLM_API_KEY });
    provider.addUser('--- RETRIEVED SUBGRAPH ---\n' + contexto + '\n--- END SUBGRAPH ---\n\nQUESTION: ' + c.pregunta);
    const ans = await provider.step([]);
    respuesta = ans.text.join('\n');
    if (!respuesta.trim()) { estado = 'no_ejecutado'; errores = 'respuesta vacia del modelo'; }
  } catch (e) {
    estado = 'no_ejecutado';
    errores = String(e).slice(0, 500);
  }
  await writeFile(outDir + '/' + c.id + '.md', '# ' + c.id + ' ' + c.tema + '\n\n## Pregunta\n' + c.pregunta + '\n\n## Respuesta (canal: sidecar-Studio mismo retrieve+QA_PROMPT+Gemini, sin UI)\n' + (respuesta || ('NO_EJECUTADO: ' + errores)) + '\n', 'utf8');
  await writeFile(outDir + '/' + c.id + '.contexto.txt', contexto, 'utf8');
  registro.push({ id: c.id, pregunta: c.pregunta, esperada: c.esperada, obtenida: respuesta.slice(0, 2000), errores, estado, canal: 'sidecar-Studio (retrieve+QA_PROMPT+Gemini ' + settings.ONTO_LLM_MODEL + '), sin UI; studio-ui: no_ejecutado sin automatizacion GUI', ms: Date.now() - t0, resumenRecuperacion: resumenRec });
  console.log(c.id, estado, (errores || respuesta.slice(0, 80)).replace(/\n/g, ' '));
  await writeFile(root + '/propuestas/ronda-2/agente-5-evaluacion-chat/registro_parcial.json', JSON.stringify(registro, null, 2), 'utf8');
}
console.log('DONE ejecutados=' + registro.filter(r => r.estado === 'ejecutado').length);
