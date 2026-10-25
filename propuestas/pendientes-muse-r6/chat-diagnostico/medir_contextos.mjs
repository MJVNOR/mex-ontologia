/** Sonda 2: mide el contexto REAL que index.ts enviaria al modelo por caso,
 * con y sin presupuesto (EFFECTIVE_MODEL presente vs ausente), mas escaneo
 * de contenido hostil al gateway (controles, sustitutos sueltos, lineas gigantes).
 * CERO llamadas al modelo: solo SELECT de lectura contra el motor vivo.
 * Uso: node medir_contextos.mjs
 * Salida: medicion.json
 */
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';
import { CASOS } from './corpus.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AGENT_SRC = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const ENGINE_STATS = 'http://127.0.0.1:8137/api/stats';
const ENGINE_QUERY = 'http://127.0.0.1:8137/api/query';
const MODEL = 'gemma-4-31b-it';

const { retrieve, asContext, QA_SYSTEM_PROMPT, estimateInputTokens, budgetForModel } =
  await import(pathToFileURL(path.join(AGENT_SRC, 'graphrag.ts')).href);

const mcp = {
  async callTool(name, args) {
    if (name !== 'onto_query') throw new Error('solo onto_query');
    const r = await fetch(ENGINE_QUERY, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(args) });
    if (!r.ok) throw new Error('Engine HTTP ' + r.status);
    return await r.text();
  },
};

function scan(s) {
  const controles = (s.match(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g) || []).length;
  let sustitutos = 0;
  for (let i = 0; i < s.length; i++) {
    const c = s.charCodeAt(i);
    if (c >= 0xD800 && c <= 0xDBFF) { const n = s.charCodeAt(i + 1); if (!(n >= 0xDC00 && n <= 0xDFFF)) sustitutos++; }
    else if (c >= 0xDC00 && c <= 0xDFFF) sustitutos++;
  }
  let maxLinea = 0;
  for (const ln of s.split('\n')) if (ln.length > maxLinea) maxLinea = ln.length;
  return { controles, sustitutos_sueltos: sustitutos, linea_max_chars: maxLinea, bytes: Buffer.byteLength(s, 'utf8') };
}

const stats = await (await fetch(ENGINE_STATS)).json();
const triples = Number(String(stats.triples ?? -1).replace(/[^0-9]/g, '')) || -1;
const filas = [];
for (const c of CASOS) {
  // Con presupuesto: lo que index.ts hace cuando ONTO_LLM_MODEL esta fijado (EFFECTIVE_MODEL).
  const rCon = await retrieve(mcp, c.pregunta, 2, { model: MODEL });
  const ctxCon = asContext(rCon);
  // Sin presupuesto: lo que ocurre si el sidecar arranco sin ONTO_LLM_MODEL (modelo '' -> Infinity).
  const rSin = await retrieve(mcp, c.pregunta, 2);
  const ctxSin = asContext(rSin);
  filas.push({
    id: c.id,
    anchors: rCon.anchors?.length ?? 0,
    hechos: rCon.facts?.length ?? 0,
    secciones: {
      correspondencias: !!(rCon.correspondenceOverview || rCon.correspondenceContext),
      recurso: !!rCon.resourceContext, variable: !!rCon.variableOverview,
      ficha: !!rCon.cruceFichaContext, codigo: !!rCon.cruceCodigoContext,
    },
    con_presupuesto: {
      contexto_chars: ctxCon.length,
      est_input_tokens: estimateInputTokens({ question: c.pregunta, context: ctxCon }),
      presupuesto: budgetForModel(MODEL),
      scan: scan(ctxCon),
    },
    sin_presupuesto: {
      contexto_chars: ctxSin.length,
      est_input_tokens: estimateInputTokens({ question: c.pregunta, context: ctxSin }),
      presupuesto: budgetForModel(undefined),
      scan: scan(ctxSin),
    },
  });
}
const out = {
  sonda: 'medicion (cero modelo; solo SELECT contra motor vivo)',
  triples, modelo: MODEL, qa_system_prompt_chars: QA_SYSTEM_PROMPT.length,
  onta_max_output_tokens_efectivo: '4096 (defecto openai.ts; suma a la ventana junto a la entrada)',
  casos: filas,
};
await writeFile(path.join(HERE, 'medicion.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ triples, resumen: filas.map(f => ({ id: f.id, con: f.con_presupuesto.est_input_tokens, sin: f.sin_presupuesto.est_input_tokens })) }, null, 2));
