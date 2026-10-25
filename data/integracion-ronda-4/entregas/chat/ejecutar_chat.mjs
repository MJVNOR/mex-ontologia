/** Harness reproducible de evaluacion real del chat de Studio (ronda 4, rol chat).
 * Adaptado de scripts/comprobar_recuperacion_chat.mjs (solo referencia, no se modifica).
 * Lee la configuracion YA existente del modelo de Studio; no cambia proveedor,
 * modelo, claves, grafo ni compilacion. Solo escribe en su propia carpeta.
 * Uso: node ejecutar_chat.mjs  (node >= 22, type stripping para graphrag.ts)
 */
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { readFile, writeFile } from 'node:fs/promises';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..');
const MINE = path.resolve(ROOT, 'propuestas', 'pendientes-muse-r4', 'chat');
const AGENT_SRC = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const ENGINE_STATS = 'http://127.0.0.1:8137/api/stats';
const ENGINE_QUERY = 'http://127.0.0.1:8137/api/query';

const corpus = JSON.parse(await readFile(path.join(MINE, 'corpus.json'), 'utf8'));

const { retrieve, asContext, QA_SYSTEM_PROMPT } = await import(pathToFileURL(path.join(AGENT_SRC, 'graphrag.ts')).href);
const { OpenAICompatibleProvider } = await import(pathToFileURL(path.join(AGENT_SRC, 'providers', 'openai.ts')).href);

// Configuracion ya existente del modelo (misma que Studio). Sin imprimir valores.
async function loadSettings() {
  const cands = [
    path.join(process.env.LOCALAPPDATA ?? '', 'open-ontologies-studio', 'agent-env-path.txt'),
    'C:/Users/marti/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/open-ontologies-studio/agent-env-path.txt',
  ];
  let envPath = null;
  for (const c of cands) {
    try { await readFile(c, 'utf8'); envPath = c; break; } catch { /* siguiente */ }
  }
  if (!envPath) throw new Error('Sin archivo agent-env-path (Studio no expone configuracion)');
  const target = (await readFile(envPath, 'utf8')).trim().replace(/^\uFEFF/, '');
  const settings = {};
  for (const line of (await readFile(target, 'utf8')).replace(/^\uFEFF/, '').split(/\r?\n/)) {
    const m = line.trim().match(/^(ONTO_(?:PROVIDER|LLM_BASE_URL|LLM_MODEL|LLM_API_KEY))\s*=\s*(.*)$/);
    if (m) settings[m[1]] = m[2].replace(/^(["'])(.*)\1$/, '$2');
  }
  if (!settings.ONTO_LLM_BASE_URL || !settings.ONTO_LLM_MODEL || !settings.ONTO_LLM_API_KEY) {
    throw new Error('Configuracion de modelo de Studio incompleta');
  }
  return settings;
}

const settings = await loadSettings();
const SECRETS = [settings.ONTO_LLM_API_KEY].filter(Boolean);
const clean = (s) => SECRETS.reduce((a, k) => (k && k.length > 8 ? a.split(k).join('[clave omitida]') : a), String(s ?? ''));

async function stats() {
  const r = await fetch(ENGINE_STATS);
  if (!r.ok) throw new Error('stats HTTP ' + r.status);
  return r.json();
}
const triplesOf = (s) => Number(String(s.triples ?? s.total ?? -1).replace(/[^0-9]/g, '')) || -1;

const mcp = {
  async callTool(name, args) {
    if (name !== 'onto_query') throw new Error('herramienta no soportada: ' + name);
    const r = await fetch(ENGINE_QUERY, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(args),
    });
    if (!r.ok) throw new Error('Engine HTTP ' + r.status);
    return await r.text();
  },
};

function evalAnswer(answer, caso) {
  const low = answer.toLowerCase();
  const faltan = (caso.debe ?? []).filter((f) => !low.includes(f.toLowerCase()));
  const alguno = (caso.debe_alguno ?? []);
  const algunoOk = alguno.length === 0 || alguno.some((f) => low.includes(f.toLowerCase()));
  const prohibidos = (caso.prohibido ?? []).filter((f) => low.includes(f.toLowerCase()));
  return { faltan, algunoOk, alguno, prohibidos, pasa: faltan.length === 0 && algunoOk && prohibidos.length === 0 };
}

const registro = [];
const t0 = Date.now();
let bloqueos = 0;
let sinModelo = false; // ante 429: detener llamadas al modelo; resto solo recuperacion
for (const caso of corpus.casos) {
  const antes = triplesOf(await stats());
  let retrieved = null;
  try {
    retrieved = await retrieve(mcp, caso.pregunta);
  } catch (e) {
    registro.push({ id: caso.id, pregunta: caso.pregunta, chat: 'no_probado', causa: 'recuperacion: ' + clean(e.message), triples_antes: antes, triples_despues: antes });
    continue;
  }
  const context = asContext(retrieved);
  const recOk = (retrieved.facts?.length ?? 0) > 0 || !!(retrieved.correspondenceOverview || retrieved.correspondenceContext);
  const entry = {
    id: caso.id, pregunta: caso.pregunta, modelo: settings.ONTO_LLM_MODEL,
    canal: 'sidecar-Studio (retrieve+QA_SYSTEM_PROMPT+modelo configurado), sin UI',
    triples_antes: antes, recuperacion: { anchors: retrieved.anchors?.length ?? 0, hechos: retrieved.facts?.length ?? 0 },
  };
  if (sinModelo) {
    Object.assign(entry, {
      chat: 'pendiente_cuota', causa: 'cuota 429 en caso previo: sin llamadas al modelo',
      respuesta: null,
      evaluacion: { recuperacion_ok: recOk, nota: 'recuperacion real registrada; respuesta del modelo pendiente' },
      triples_despues: antes, grafo_sin_cambios: true,
      contexto_caracteres: context.length,
    });
  } else try {
    const provider = new OpenAICompatibleProvider({ system: QA_SYSTEM_PROMPT, baseURL: settings.ONTO_LLM_BASE_URL, model: settings.ONTO_LLM_MODEL, apiKey: settings.ONTO_LLM_API_KEY });
    provider.addUser(`--- RETRIEVED SUBGRAPH ---\n${context}\n--- SUBGRAPH END ---\n\nQUESTION: ${caso.pregunta}`);
    const answer = clean(await Promise.race([
      provider.step([]).then((t) => (t.text ?? []).join('\n')),
      new Promise((_, rej) => setTimeout(() => rej(new Error('tiempo de modelo agotado (150s)')), 150000)),
    ]));
    const despues = triplesOf(await stats());
    const ev = evalAnswer(answer, caso);
    Object.assign(entry, {
      chat: ev.pasa && recOk ? 'probado' : 'falla_oraculo', respuesta: answer,
      evaluacion: { ...ev, recuperacion_ok: recOk }, triples_despues: despues, grafo_sin_cambios: antes === despues,
    });
  } catch (e) {
    const msg = clean(e.message);
    const clase = /401|403|api key|auth|unauthorized/i.test(msg) ? 'auth' : /429|quota|exceed|insufficient/i.test(msg) ? 'cuota' : /tiempo|timeout|fetch|network|ECONN/i.test(msg) ? 'red' : 'otro';
    bloqueos++;
    if (clase === 'cuota') sinModelo = true; // detener modelo: no seguir llamadas de ese modelo
    Object.assign(entry, {
      chat: 'bloqueado_' + clase, causa: msg, respuesta: null,
      evaluacion: { recuperacion_ok: recOk, nota: 'recuperacion real registrada; respuesta del modelo pendiente' },
      triples_despues: antes, grafo_sin_cambios: true,
      contexto_caracteres: context.length,
    });
  }
  registro.push(entry);
  await new Promise((r) => setTimeout(r, 2000));
}

const despues = triplesOf(await stats());
const probados = registro.filter((r) => r.chat === 'probado').length;
const informe = {
  checked_at: new Date().toISOString(), ms_total: Date.now() - t0,
  modelo: settings.ONTO_LLM_MODEL, proveedor: settings.ONTO_PROVIDER ?? 'openai-compatible',
  triples_final: despues, casos_probados: probados, casos_totales: registro.length, bloqueos,
  capas: {
    'sidecar/api': 'ejecutada en este harness (retrieve real + mismo prompt y modelo que Studio)',
    'studio-ui': 'no_ejecutada: sin herramienta nativa (@oai/sky no instalado) y guarda de actividad respetada; ventana e investigador ajenos',
  },
  casos: registro,
};
await writeFile(path.join(MINE, 'respuestas-saneadas.json'), JSON.stringify(registro.map((r) => ({ id: r.id, pregunta: r.pregunta, chat: r.chat, causa: r.causa ?? null, respuesta: r.respuesta ?? null })), null, 2) + '\n');
await writeFile(path.join(MINE, 'evaluacion.json'), JSON.stringify(informe, null, 2) + '\n');
console.log(JSON.stringify({ casos_totales: informe.casos_totales, probados, bloqueos, triples_final: despues, por_caso: registro.map((r) => ({ id: r.id, chat: r.chat })) }, null, 2));
