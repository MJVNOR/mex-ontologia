/** Sonda 4: mide los tool schemas reales (lectura tools/list) para cuantificar
 * el request del camino runTurn (fallback cuando answerOnce devuelve vacio).
 * Cliente MCP minimo de SOLO LECTURA (initialize + tools/list; misma
 * cabecera Accept y sesion que mcp.ts, sin importar ese modulo: node22
 * type-stripping no admite `constructor(private ...)`).
 * CERO llamadas al modelo. Uso: node medir_tools.mjs. Salida: tools-schema.json
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ENDPOINT = 'http://127.0.0.1:8137/mcp';
let sessionId;
let nextId = 1;
async function rpc(method, params) {
  const headers = { 'Content-Type': 'application/json', Accept: 'application/json, text/event-stream' };
  if (sessionId) headers['Mcp-Session-Id'] = sessionId;
  const resp = await fetch(ENDPOINT, { method: 'POST', headers, body: JSON.stringify({ jsonrpc: '2.0', id: nextId++, method, params }) });
  const sid = resp.headers.get('Mcp-Session-Id');
  if (sid) sessionId = sid;
  if (!resp.ok) throw new Error(`MCP ${method}: HTTP ${resp.status} ${await resp.text()}`);
  const text = (await resp.text()).trim();
  const frame = text.startsWith('{') ? JSON.parse(text)
    : text.split('\n').filter(l => l.startsWith('data:')).map(l => l.slice(5).trim()).filter(d => d && d !== '[DONE]').map(d => { try { return JSON.parse(d); } catch { return null; } }).find(f => f && (f.result !== undefined || f.error !== undefined));
  if (frame?.error) throw new Error(`MCP ${method}: ${frame.error.message}`);
  return frame?.result;
}
await rpc('initialize', { protocolVersion: '2025-03-26', capabilities: {}, clientInfo: { name: 'sonda-lectura', version: '0' } });
const tools = (await rpc('tools/list', {})).tools ?? [];
// Replica exacta del mapeo tools->body de providers/openai.ts step():
const mapped = tools.map(t => ({
  type: 'function',
  function: { name: t.name, description: String(t.description ?? '').slice(0, 1024), parameters: t.inputSchema },
}));
const toolsBytes = Buffer.byteLength(JSON.stringify(mapped), 'utf8');
const out = {
  sonda: 'tools-schema (lectura tools/list; cero modelo)',
  n_tools: tools.length,
  nombres: tools.map(t => t.name),
  tools_json_bytes: toolsBytes,
  por_herramienta: tools.map(t => ({ name: t.name, schema_bytes: Buffer.byteLength(JSON.stringify(t.inputSchema ?? {}), 'utf8') })),
};
await writeFile(path.join(HERE, 'tools-schema.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ n_tools: out.n_tools, tools_json_bytes: toolsBytes }, null, 2));
