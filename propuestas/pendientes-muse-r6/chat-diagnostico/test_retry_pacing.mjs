/** Prueba offline del parche reintento+pacing (fetch stub; CERO red, CERO modelo).
 * Uso: node test_retry_pacing.mjs. Sale 0 si todo pasa, 1 si algo falla.
 */
import { ProveedorConReintento, parseRetryDelayMs } from './proveedor-retry.mjs';

let fallos = 0;
const ok = (cond, nombre) => { console.log((cond ? 'PASA' : 'FALLA') + ' ' + nombre); if (!cond) fallos++; };
const resp = (status, cuerpo) => ({ ok: status >= 200 && status < 300, status, json: async () => cuerpo, text: async () => typeof cuerpo === 'string' ? cuerpo : JSON.stringify(cuerpo) });

// 1. 500,500,200 -> exito al tercer intento (doc Google: 500 api_error => reintentar).
let n = 0;
let p = new ProveedorConReintento({ system: 's', baseURL: 'https://x', model: 'm', maxTokens: 16 }, async () =>
  (++n < 3 ? resp(500, { error: { code: 500, message: 'Internal error.' } }) : resp(200, { choices: [{ message: { content: 'hola' } }] })));
p.addUser('q');
const r1 = await p.step([]);
ok(r1.text.join('') === 'hola' && r1.intentos === 3, 'reintento-500-transitorio');

// 2. 400 -> sin reintento, error inmediato con status intacto y cuerpo recortado.
n = 0;
p = new ProveedorConReintento({ system: 's', baseURL: 'https://x', model: 'm' }, async () => (n++, resp(400, { error: { code: 'x', message: 'y'.repeat(5000) } })));
p.addUser('q');
try { await p.step([]); ok(false, '400-no-reintenta'); }
catch (e) { ok(n === 1 && e.message.includes('HTTP 400') && e.message.length < 2500, '400-no-reintenta'); }

// 3. RetryInfo retryDelay 8s se respeta (parse puro, sin dormir 8s aqui).
ok(parseRetryDelayMs('{"details":[{"retryDelay":"8s"}]}') === 8000, 'retryinfo-8s');
ok(parseRetryDelayMs('{}') === 0, 'sin-retryinfo-0');

// 4. 429 con retryDelay corto se espera y reintenta.
n = 0; const t0 = Date.now();
p = new ProveedorConReintento({ system: 's', baseURL: 'https://x', model: 'm' }, async () =>
  (++n === 1 ? resp(429, '{"details":[{"retryDelay":"0.3s"}]}') : resp(200, { choices: [{ message: { content: 'ok' } }] })));
p.addUser('q');
await p.step([]);
ok(n === 2 && Date.now() - t0 >= 300, '429-retryinfo-espera');

// 5. Pacing: dos llamadas seguidas respetan minIntervalMs.
n = 0; const t1 = Date.now();
p = new ProveedorConReintento({ system: 's', baseURL: 'https://x', model: 'm', minIntervalMs: 400 }, async () => (n++, resp(200, { choices: [{ message: { content: 'x' } }] })));
p.addUser('a'); await p.step([]); p.addUser('b'); await p.step([]);
ok(Date.now() - t1 >= 400, 'pacing-serie');

// 6. 503 "high demand" (visto en R4 C1) tambien reintenta.
n = 0;
p = new ProveedorConReintento({ system: 's', baseURL: 'https://x', model: 'm' }, async () =>
  (++n === 1 ? resp(503, { error: { code: 503, message: 'high demand' } }) : resp(200, { choices: [{ message: { content: 'ok' } }] })));
p.addUser('q');
const r6 = await p.step([]);
ok(r6.intentos === 2, 'reintento-503');

console.log(fallos === 0 ? 'TODO OK (6/6, sin red)' : `FALLOS: ${fallos}`);
process.exit(fallos === 0 ? 0 : 1);
