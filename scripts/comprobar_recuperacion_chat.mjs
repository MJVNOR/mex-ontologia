/** Verify the Studio retrieval implementation against its live graph, without an LLM. */
import { pathToFileURL, fileURLToPath } from 'node:url';
import path from 'node:path';
import { readFile, writeFile } from 'node:fs/promises';
import assert from 'node:assert/strict';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.resolve(root, '../open-ontologies/studio/src-tauri/sidecars/agent/graphrag.ts');
const { retrieve, asContext, QA_SYSTEM_PROMPT } = await import(pathToFileURL(source).href);
let queries = 0;
const mcp = { async callTool(name, args) {
  assert.equal(name, 'onto_query');
  queries++;
  const response = await fetch('http://127.0.0.1:8137/api/query', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(args),
  });
  assert.ok(response.ok, `Engine HTTP ${response.status}`);
  return await response.text();
} };
const question = '¿Qué diferencia hay entre año_matrimonio y año_defuncion? Muestra las definiciones originales y distingue lo documentado de lo candidato.';
const started = performance.now();
const retrieved = await retrieve(mcp, question);
const context = asContext(retrieved);
const qualified = retrieved.correspondenceContext;
assert.ok(qualified);
for (const name of ['año_matrimonio', 'año_defuncion']) {
  const line = qualified.split('\n').find(line => line.startsWith('COMPLETE correspondence') && line.includes(JSON.stringify(name)));
  assert.ok(line, `Missing complete count for ${name}`);
  assert.ok(line.includes('"documental_revisada":1'), line);
  assert.ok(line.includes('"candidata_por_nombre":'), line);
}
for (const fragment of ['Año de registro', 'Año en el que fallecio', 'Matrimonios 2022', 'Defunciones 2022',
  '364ffa5c-e1c2-4185-a22f-80bede6735d0/download/diccionario.csv',
  'ab19bd4a-847a-4451-b0db-1249dcb892db/download/diccionario.csv']) assert.ok(qualified.includes(fragment), fragment);
const report = {
  checked_at: new Date().toISOString(), source, question, queries,
  seconds: Math.round((performance.now() - started) / 10) / 100,
  anchors: retrieved.anchors.length, neighbourhood_facts: retrieved.facts.length,
  correspondence_summary: qualified.split('\n').filter(line => line.startsWith('COMPLETE') || line.startsWith('Correspondence examples')),
  reviewed_both_2022: true, original_definitions_and_sources: true,
  context_characters: context.length,
  scope: 'Live retrieval and model context verified; model response requires a separate end-to-end check.',
};
if (process.argv.includes('--model')) {
  // Use the existing Studio configuration without printing credentials.
  const installed = path.join(process.env.LOCALAPPDATA, 'open-ontologies-studio');
  const envPath = (await readFile(path.join(installed, 'agent-env-path.txt'), 'utf8')).trim().replace(/^\uFEFF/, '');
  const settings = {};
  for (const line of (await readFile(envPath, 'utf8')).replace(/^\uFEFF/, '').split(/\r?\n/)) {
    const match = line.trim().match(/^(ONTO_(?:PROVIDER|LLM_BASE_URL|LLM_MODEL|LLM_API_KEY))\s*=\s*(.*)$/);
    if (match) settings[match[1]] = match[2].replace(/^(["'])(.*)\1$/, '$2');
  }
  assert.ok(settings.ONTO_LLM_BASE_URL && settings.ONTO_LLM_MODEL && settings.ONTO_LLM_API_KEY, 'Studio model configuration missing');
  const { OpenAICompatibleProvider } = await import(pathToFileURL(path.join(path.dirname(source), 'providers/openai.ts')).href);
  const provider = new OpenAICompatibleProvider({ system: QA_SYSTEM_PROMPT, baseURL: settings.ONTO_LLM_BASE_URL, model: settings.ONTO_LLM_MODEL, apiKey: settings.ONTO_LLM_API_KEY });
  provider.addUser(`--- RETRIEVED SUBGRAPH ---\n${context}\n--- END SUBGRAPH ---\n\nQUESTION: ${question}`);
  const answer = (await provider.step([])).text.join('\n');
  await writeFile(path.join(root, 'reports/chat-respuesta-comprobada.md'), answer + '\n');
  assert.ok(answer.includes('documental_revisada') && answer.includes('2022'), 'Model failed to report reviewed 2022 mappings');
  assert.ok(answer.includes('año_matrimonio') && answer.includes('año_defuncion') && answer.includes('candidata_por_nombre'), 'Model omitted requested comparison/states');
  report.model = settings.ONTO_LLM_MODEL;
  report.model_answer_checked = true;
  report.scope = 'Live retrieval and model answer checked with the same provider and system prompt as Studio.';
}
await writeFile(path.join(root, 'reports/chat-recuperacion.json'), JSON.stringify(report, null, 2) + '\n');
await writeFile(path.join(root, 'reports/chat-recuperacion-contexto.txt'), context);
console.log(JSON.stringify(report, null, 2));
