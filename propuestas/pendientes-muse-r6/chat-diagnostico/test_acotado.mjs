/** Pruebas aisladas (fetch stub + reloj fake; CERO red, CERO modelo, CERO espera real).
 * Uso: node test_acotado.mjs. Sale 0 si todo pasa.
 */
import { ProveedorAcotado, parseRetryDelayMs, PISO_GEMMA_MS } from './proveedor-retry.mjs';
import { decidirRespuestaQA } from './qa-guardia.mjs';

let fallos = 0;
const ok = (cond, nombre) => { console.log((cond ? 'PASA' : 'FALLA') + ' ' + nombre); if (!cond) fallos++; };
const resp = (status, cuerpo) => ({ ok: status >= 200 && status < 300, status, json: async () => cuerpo, text: async () => typeof cuerpo === 'string' ? cuerpo : JSON.stringify(cuerpo) });
// Reloj fake: el tiempo solo avanza cuando se "duerme"; jamas espera real.
const relojFake = () => { let t = 1000; const dormidas = []; return { ahora: () => t, dormir: async (ms) => { dormidas.push(ms); t += ms; }, dormidas }; };

// 1. 500 -> 1 reintento y exito; espera = piso 65s (sin RetryInfo).
let r = relojFake(); let n = 0;
let p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'gemma-4-31b-it' },
  async () => (++n === 1 ? resp(500, { error: { code: 500, message: 'Internal' } }) : resp(200, { choices: [{ message: { content: 'hola' } }] })), r);
p.addUser('q');
const r1 = await p.step([]);
ok(r1.text.join('') === 'hola' && r1.intentos === 2 && r.dormidas[0] === 65000, '500-1-reintento-piso-65s');

// 2. 500 persistente -> error clasificado `servidor`, 2 intentos, sin 3er intento.
r = relojFake(); n = 0;
p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'm' }, async () => (n++, resp(500, 'e')), r);
p.addUser('q');
try { await p.step([]); ok(false, '500-clasificado'); }
catch (e) { ok(n === 2 && e.message.includes('(servidor,') && e.message.includes('HTTP 500'), '500-clasificado'); }

// 3. 429 con RetryInfo 8s -> espera max(8s, 65s)=65s; error clasificado `cuota`.
r = relojFake(); n = 0;
p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'm' }, async () => (n++, resp(429, '{"details":[{"retryDelay":"8s"}]}')), r);
p.addUser('q');
try { await p.step([]); ok(false, '429-clasificado'); }
catch (e) { ok(n === 2 && e.message.includes('(cuota,') && r.dormidas[0] === 65000, '429-clasificado'); }

// 4. RetryInfo mayor que el piso manda (90s).
ok(parseRetryDelayMs('{"retryDelay":"90s"}') === 90000, 'retryinfo-90s-manda');

// 5. 400 -> sin reintento, 1 intento, cuerpo recortado.
r = relojFake(); n = 0;
p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'm' }, async () => (n++, resp(400, 'x'.repeat(5000))), r);
p.addUser('q');
try { await p.step([]); ok(false, '400-sin-reintento'); }
catch (e) { ok(n === 1 && e.message.includes('HTTP 400') && e.message.length < 2500, '400-sin-reintento'); }

// 6. Consumo unico: tras 500+exito, historial = system+user+1 assistant (sin fantasmas).
r = relojFake(); n = 0;
p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'm' },
  async () => (++n === 1 ? resp(502, 'bad gateway') : resp(200, { choices: [{ message: { content: 'ok' } }] })), r);
p.addUser('q'); await p.step([]);
ok(p.messages.length === 3 && p.messages.filter(m => m.role === 'assistant').length === 1, 'consumo-unico');

// 7. Pacing serie con reloj fake: dos llamadas respetan minIntervalMs sin dormir real.
r = relojFake(); n = 0;
p = new ProveedorAcotado({ system: 's', baseURL: 'https://x', model: 'm', minIntervalMs: 65000 }, async () => (n++, resp(200, { choices: [{ message: { content: 'x' } }] })), r);
p.addUser('a'); await p.step([]); p.addUser('b'); await p.step([]);
ok(r.dormidas.some(d => d === 65000) && n === 2, 'pacing-fake-sin-espera-real');

// 8-10. Guardia QA: vacio -> error sin fallback; blancos -> error; texto -> responder+cachear.
const g1 = decidirRespuestaQA('');
ok(g1.accion === 'error-sin-fallback' && g1.cachear === false && g1.mutacion === false, 'qa-vacio-error');
ok(decidirRespuestaQA('   \n  ').accion === 'error-sin-fallback', 'qa-blancos-error');
const g3 = decidirRespuestaQA('respuesta util');
ok(g3.accion === 'responder' && g3.cachear === true, 'qa-texto-responder');

console.log(fallos === 0 ? 'TODO OK (10/10, fake clock, sin red)' : `FALLOS: ${fallos}`);
process.exit(fallos === 0 ? 0 : 1);
