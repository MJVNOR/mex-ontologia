/** Harness Gemma4 31B (propuesta aislada, SOLO esta carpeta).
 * Por defecto: recuperacion real + verificacion de presupuesto, CERO
 * llamadas al modelo. Las llamadas reales exigen --con-modelo Y
 * ONTO_ALLOW_MODEL_CALLS=1, con espaciado minimo 65s entre llamadas y
 * respeto a RetryInfo del 429. Evidencia contextual del usuario (captura
 * dashboard Google, Gemma4 31B: RPM 1/30, TPM 13.08K/16K, RPD 1/14.4K):
 * TPM por minuto casi agotado con RPM y RPD holgados. Hipotesis
 * compatible (no probada solo con el dashboard): llamadas sucesivas con
 * 2s entre ellas acumulan TPM aunque cada peticion quepa. Es limite por
 * minuto, NO cuota diaria agotada (RPD 1/14.4K la descarta); tampoco
 * prueba una peticion individual >16K.
 * NO tocar repo externo ni instalacion: importa la COPIA parcheada local.
 * Este rol nunca ejecuta --con-modelo.
 */
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { readFile, writeFile } from 'node:fs/promises';

const HERE = path.dirname(path.resolve(process.argv[1] ?? 'harness_gemma.mjs'));
const MINE = path.resolve(HERE);
const PATCHED = path.join(MINE, 'graphrag.f2.ts');
const CORPUS = path.resolve('propuestas/pendientes-muse-r4/chat/corpus.json');

const g = await import(pathToFileURL(PATCHED).href);
const ENGINE_QUERY = 'http://127.0.0.1:8137/api/query';
const ENGINE_STATS = 'http://127.0.0.1:8137/api/stats';
const MODEL = process.env.ONTO_LLM_MODEL ?? 'gemma-4-31b-it';
const CON_MODELO = process.argv.includes('--con-modelo') && process.env.ONTO_ALLOW_MODEL_CALLS === '1';
// Capturas saneadas: la clave nunca sale en logs ni en el informe.
const SECRETS = [process.env.ONTO_LLM_API_KEY].filter(Boolean);
const clean = (s) =>
  SECRETS.reduce((a, k) => (k && k.length > 8 ? a.split(k).join('[clave omitida]') : a), String(s ?? ''));
const logLine = (o) => console.log(clean(JSON.stringify(o)));

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

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const triplesOf = (s) => Number(String(s.triples ?? s.total ?? -1).replace(/[^0-9]/g, '')) || -1;
/** Espaciado minimo entre llamadas REALES: 65s (>=60s exigidos). Nunca por
 * debajo, aunque un RetryInfo pida menos: el TPM se consume por minuto y
 * la hipotesis compatible es que sucesivas con 2s entre ellas lo agotan. */
const ESPACIADO_MINIMO_MS = 65000;
/** Espera larga maxima que el harness acepta dormir (15 min). Un RetryInfo
 * mayor (p. ej. ~14h de cuota por minuto saturada) no se duerme: el caso
 * queda pendiente_cuota con hora de reanudacion y se sigue sin modelo. */
const ESPERA_MAXIMA_MS = 15 * 60 * 1000;
let ultimaLlamadaRealTs = 0;
let modeloBloqueado = null;

/** Extrae segundos de espera de un 429 (RetryInfo, "retry in Ns",
 * "reintento sugerido Ns"). Sin pista: ESPACIADO_MINIMO_MS. */
function extraerEsperaMs(msg) {
  const m = String(msg ?? '').match(/retry\s*in\s*(\d+(?:\.\d+)?)\s*s|retrydelay["']?\s*:\s*"?(\d+(?:\.\d+)?)s|reintento\s+sugerido\s+(\d+(?:\.\d+)?)\s*s/i);
  const seg = m ? Number(m[1] ?? m[2] ?? m[3]) : NaN;
  return Number.isFinite(seg) ? Math.ceil(seg * 1000) : ESPACIADO_MINIMO_MS;
}
const corpus = JSON.parse(await readFile(CORPUS, 'utf8'));
const budget = g.budgetForModel(MODEL);
if (!(budget.pacingMs >= 60000)) throw new Error('pacing <60s: ' + budget.pacingMs);
logLine({ modelo: MODEL, tpm: g.GEMMA_TPM, budget, pacing_ok: budget.pacingMs >= 60000 });

// Conteos dinamicos del grafo vivo (solo SELECT): el corpus historico queda
// intacto; C1 se evalua contra los numeros vivos, no contra 865 fijados
// pre-sync. Se deja copia vigente en esta carpeta (no se toca el historico).
async function contar(sparql) {
  const r = await fetch(ENGINE_QUERY, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: sparql }),
  });
  if (!r.ok) throw new Error('Engine HTTP ' + r.status);
  const j = await r.json();
  const rows = Array.isArray(j.results) ? j.results : j.results?.bindings ?? [];
  const v = rows[0] ? Object.values(rows[0])[0] : null;
  const raw = typeof v === 'object' && v !== null && 'value' in v ? v.value : String(v ?? '');
  const m = String(raw).match(/"(\d+)"/) ?? String(raw).match(/^(\d+)$/);
  return m ? Number(m[1]) : 0;
}
const live = {
  revisadas: await contar("SELECT (COUNT(DISTINCT ?m) AS ?n) WHERE { ?m ?p ?o . FILTER(REGEX(STR(?p),'estadoCorrespondencia')) FILTER(STR(?o)='documental_revisada') }"),
  comparaciones2020: await contar('SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { ?c a <https://example.org/mex-ontologi/vocab/ComparacionMunicipal2020> }'),
  evidencias: await contar('SELECT (COUNT(DISTINCT ?e) AS ?n) WHERE { ?e a <https://example.org/mex-ontologi/vocab/EvidenciaFuenteComparacion> }'),
};
const vigente = JSON.parse(JSON.stringify(corpus));
{
  const c1 = vigente.casos.find((c) => c.id === 'C1-totales');
  if (c1) c1.debe = [...new Set([...(c1.debe ?? []).filter((f) => !/^\d+$/.test(f)), String(live.revisadas)])];
  vigente.fuente_conteos = 'grafo vivo http://127.0.0.1:8137 (solo SELECT)';
  vigente.verificado_el = new Date().toISOString();
}
await writeFile(path.join(MINE, 'corpus-vigente.json'), clean(JSON.stringify(vigente, null, 2)) + '\n');

const antes = triplesOf(await (await fetch(ENGINE_STATS)).json());
const informe = [];
for (const caso of corpus.casos) {
  const r = await g.retrieve(mcp, caso.pregunta, 2, { model: MODEL });
  const ctx = g.asContext(r);
  const est = g.estimateInputTokens({ question: caso.pregunta, context: ctx });
  const low = ctx.toLowerCase();
  // C1 usa la copia vigente (conteos dinamicos del grafo); el resto, el
  // corpus historico intacto. Corpus C2-C6 con 72/144 confirmados vivos.
  const esperado = caso.id === 'C1-totales'
    ? (vigente.casos.find((c) => c.id === caso.id) ?? caso)
    : caso;
  informe.push({
    id: caso.id,
    contexto_caracteres: ctx.length,
    est_input_tokens: est,
    bajo_presupuesto: est <= budget.maxInputTokens,
    faltan: (esperado.debe ?? []).filter((f) => !low.includes(f.toLowerCase())),
    algunoOk: (esperado.debe_alguno ?? []).length === 0 || (esperado.debe_alguno ?? []).some((f) => low.includes(f.toLowerCase())),
    prohibidos: (esperado.prohibido ?? []).filter((f) => low.includes(f.toLowerCase())),
    conteos_vivos: caso.id === 'C1-totales' ? live : undefined,
  });
  console.log(clean(JSON.stringify(informe[informe.length - 1])));
  if (CON_MODELO && !modeloBloqueado) {
    // Llamadas REALES (solo humano/integrador; este rol nunca entra aqui):
    // modelo fijado a Gemma4 31B (sin ensayos de otros modelos), preflight
    // de presupuesto, espaciado 65s y respeto a RetryInfo.
    const entry = informe[informe.length - 1];
    if (!/gemma-4-31b/i.test(MODEL)) {
      modeloBloqueado = `modelo ${MODEL} no autorizado en este harness (fijado a gemma-4-31b-it)`;
      entry.llamada = { estado: 'rechazada_modelo', motivo: modeloBloqueado };
    } else {
    const esperaBase = Math.max(0, ESPACIADO_MINIMO_MS - (Date.now() - ultimaLlamadaRealTs));
    if (esperaBase > 0) await sleep(esperaBase);
    const baseURL = process.env.ONTO_LLM_BASE_URL, apiKey = process.env.ONTO_LLM_API_KEY;
    if (!baseURL || !apiKey) {
      modeloBloqueado = 'sin credenciales en entorno (ONTO_LLM_BASE_URL/ONTO_LLM_API_KEY): solo recuperacion';
      entry.llamada = { estado: 'pendiente_config', motivo: modeloBloqueado };
    } else if (entry.est_input_tokens > budget.maxInputTokens) {
      entry.llamada = { estado: 'rechazada_presupuesto', motivo: `entrada ${entry.est_input_tokens}tok > ${budget.maxInputTokens}tok` };
    } else try {
      const STUDIO_AGENT = process.env.ONTO_STUDIO_AGENT_DIR ?? 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
      const { OpenAICompatibleProvider } = await import(pathToFileURL(path.join(STUDIO_AGENT, 'providers', 'openai.ts')).href);
      const provider = new OpenAICompatibleProvider({ system: g.QA_SYSTEM_PROMPT, baseURL, model: MODEL, apiKey });
      provider.addUser(`--- RETRIEVED SUBGRAPH ---\n${ctx}\n--- SUBGRAPH END ---\n\nQUESTION: ${caso.pregunta}`);
      const answer = await provider.step([]).then((t) => (t.text ?? []).join('\n'));
      ultimaLlamadaRealTs = Date.now();
      entry.llamada = { estado: 'probado', respuesta_caracteres: answer.length };
    } catch (e) {
      const esperaRetry = extraerEsperaMs(e.message);
      if (esperaRetry > ESPERA_MAXIMA_MS) {
        modeloBloqueado = `429 con espera ${Math.round(esperaRetry / 60000)}min: se deja pendiente_cuota sin dormir; resto solo recuperacion`;
        entry.llamada = { estado: 'pendiente_cuota', motivo: clean(String(e.message).slice(0, 300)), reanudar_tras_ms: esperaRetry };
      } else {
        await sleep(Math.max(esperaRetry, ESPACIADO_MINIMO_MS));
        try {
          const STUDIO_AGENT = process.env.ONTO_STUDIO_AGENT_DIR ?? 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
          const { OpenAICompatibleProvider } = await import(pathToFileURL(path.join(STUDIO_AGENT, 'providers', 'openai.ts')).href);
          const provider = new OpenAICompatibleProvider({ system: g.QA_SYSTEM_PROMPT, baseURL, model: MODEL, apiKey });
          provider.addUser(`--- RETRIEVED SUBGRAPH ---\n${ctx}\n--- SUBGRAPH END ---\n\nQUESTION: ${caso.pregunta}`);
          const answer = await provider.step([]).then((t) => (t.text ?? []).join('\n'));
          ultimaLlamadaRealTs = Date.now();
          entry.llamada = { estado: 'probado_tras_espera', respuesta_caracteres: answer.length };
        } catch (e2) {
          modeloBloqueado = 'segundo 429 consecutivo: pendiente_cuota; resto solo recuperacion';
          entry.llamada = { estado: 'pendiente_cuota', motivo: clean(String(e2.message).slice(0, 300)) };
        }
      }
    }
    } // fin else modelo Gemma4 31B
  }
}
const despues = triplesOf(await (await fetch(ENGINE_STATS)).json());
await writeFile(path.join(MINE, 'informe_gemma.json'), clean(JSON.stringify({
  modelo: MODEL, tpm: g.GEMMA_TPM, pacing_ms: budget.pacingMs,
  espaciado_minimo_ms: ESPACIADO_MINIMO_MS, espera_maxima_ms: ESPERA_MAXIMA_MS,
  max_input_tokens: budget.maxInputTokens, llamadas_modelo: CON_MODELO ? 'solo_con_permiso' : 0,
  corpus_historico: 'propuestas/pendientes-muse-r4/chat/corpus.json (intacto; C1 fijado pre-sync)',
  corpus_vigente: 'propuestas/pendientes-muse-r4/recuperacion-f2/corpus-vigente.json (C1 con conteos dinamicos del grafo)',
  conteos_vivos: { ...live, triples: despues },
  evidencia_contextual_usuario: {
    tipo: 'captura dashboard Google aportada por el usuario',
    modelo_observado: 'gemma-4-31b',
    rpm: '1/30', tpm: '13.08K/16K', rpd: '1/14.4K',
    interpretacion: 'TPM por minuto casi agotado con RPM y RPD holgados: compatible con limite por minuto por llamadas sucesivas (hipotesis; harness anterior con 2s entre ellas). NO prueba peticion individual >16K ni cuota diaria agotada (RPD 1/14.4K).',
  },
  triples_antes: antes, triples_despues: despues, grafo_sin_cambios: antes === despues,
  casos: informe,
}, null, 2)) + '\n');
logLine({ triples_antes: antes, triples_despues: despues, llamadas_modelo: 0 });
