/** Sonda 1: captura el request EXACTO que providers/openai.ts envia al modelo,
 * sin ninguna llamada de red ni al modelo (fetch stub que graba y responde minimo).
 * Uso: node sonda_request.mjs  (solo lectura del repo Studio; solo escribe esta carpeta)
 * Salida: request-schema.json
 */
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AGENT_SRC = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const ENGINE_QUERY = 'http://127.0.0.1:8137/api/query';

const captured = [];
// @ts-ignore stub local: registra url/opciones y devuelve respuesta minima valida
globalThis.fetch = async (url, opts) => {
  captured.push({ url: String(url), method: opts?.method, headers: opts?.headers, body: opts?.body });
  return new Response(JSON.stringify({ choices: [{ message: { content: 'ok-sonda' } }] }), { status: 200 });
};

const { OpenAICompatibleProvider } = await import(pathToFileURL(path.join(AGENT_SRC, 'providers', 'openai.ts')).href);
const { QA_SYSTEM_PROMPT } = await import(pathToFileURL(path.join(AGENT_SRC, 'graphrag.ts')).href);

const prov = new OpenAICompatibleProvider({
  system: QA_SYSTEM_PROMPT,
  baseURL: 'https://generativelanguage.googleapis.com/v1beta/openai',
  model: 'gemma-4-31b-it',
  apiKey: 'SONDA-SIN-CLAVE',
});
prov.addUser('--- RETRIEVED SUBGRAPH ---\n(ejemplo)\n--- SUBGRAPH END ---\n\nQUESTION: ejemplo');
await prov.step([]); // via QA: sin tools (igual que answerOnce en index.ts)

const sent = captured.find(c => String(c.url).includes('chat/completions'));
const body = JSON.parse(sent.body);
const bodyBytes = Buffer.byteLength(sent.body, 'utf8');
const authHeader = String(sent.headers?.Authorization ?? '');
const keyInBody = sent.body.includes('SONDA-SIN-CLAVE');

const schema = {
  sonda: 'request-schema (cero red, fetch stub; responde minimo local)',
  archivo_fuente: 'studio/src-tauri/sidecars/agent/providers/openai.ts :: step()',
  url: sent.url,
  method: sent.method,
  body_keys: Object.keys(body),
  body_tipos: Object.fromEntries(Object.entries(body).map(([k, v]) => [k, Array.isArray(v) ? `array[${v.length}]` : typeof v])),
  messages_roles: body.messages.map(m => m.role),
  system_chars: (body.messages.find(m => m.role === 'system')?.content ?? '').length,
  max_tokens: body.max_tokens,
  temperature: body.temperature,
  top_p: body.top_p,
  tools_incluidas: ('tools' in body) ? body.tools.length : 0,
  tool_choice: body.tool_choice ?? null,
  chat_template_kwargs: body.chat_template_kwargs ?? null,
  body_bytes: bodyBytes,
  auth_en_header_no_en_body: authHeader.startsWith('Bearer ') && !keyInBody,
  clave_en_body: keyInBody,
};
await writeFile(path.join(HERE, 'request-schema.json'), JSON.stringify(schema, null, 2) + '\n');
console.log(JSON.stringify(schema, null, 2));
