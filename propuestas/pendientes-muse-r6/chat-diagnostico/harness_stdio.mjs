/** Harness STDIO del BUNDLE INSTALADO (preparado; SIN llamadas salvo peticion explicita).
 * - Modo por defecto `--revisar`: 100% offline salvo lectura local del motor
 *   (stats, sin modelo): verifica bundle, env seguro, corpus y comando exacto.
 * - Modos vivos `--handshake` y `--casos`: SOLO con `ONTO_ALLOW_CALLS=1` y los
 *   ejecuta root/integrador. `--handshake` captura `_Connected ... Model: ...`
 *   y cierra con `reset` (sin pregunta al modelo). `--casos` envia C1..C6
 *   SERIALIZADOS con espera >=65s entre llamadas (respeta RetryInfo).
 * Secretos: el env seguro se hereda al hijo; TODO log pasa por redact().
 * Uso: node harness_stdio.mjs [--revisar|--handshake|--casos]
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFile, writeFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { CASOS } from './corpus.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const MODO = process.argv[2] ?? '--revisar';
const BUNDLE = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent/dist/index.js';
const ENGINE_STATS = 'http://127.0.0.1:8137/api/stats';
const PUNTEROS = [
  path.join(process.env.LOCALAPPDATA ?? '', 'open-ontologies-studio', 'agent-env-path.txt'),
  'C:/Users/marti/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/open-ontologies-studio/agent-env-path.txt',
];
const CLAVES = ['ONTO_PROVIDER', 'ONTO_LLM_BASE_URL', 'ONTO_LLM_MODEL', 'ONTO_LLM_API_KEY'];

/** Carga SOLO las 4 claves ONTO_* del env seguro de Studio, sin imprimir valores. */
async function cargarEnvSeguro() {
  let puntero = null;
  for (const p of PUNTEROS) { try { await readFile(p, 'utf8'); puntero = p; break; } catch { /* siguiente */ } }
  if (!puntero) throw new Error('sin puntero agent-env-path (Studio no expone configuracion)');
  const destino = (await readFile(puntero, 'utf8')).trim().replace(/^\uFEFF/, '');
  const crudo = (await readFile(destino, 'utf8')).replace(/^\uFEFF/, '');
  const env = {};
  for (const linea of crudo.split(/\r?\n/)) {
    const m = linea.trim().match(/^(ONTO_(?:PROVIDER|LLM_BASE_URL|LLM_MODEL|LLM_API_KEY))\s*=\s*(.*)$/);
    if (m) env[m[1]] = m[2].replace(/^(["'])(.*)\1$/, '$2');
  }
  const faltan = CLAVES.filter(k => !env[k]);
  return { puntero, destino: '[ruta omitida]', claves: Object.keys(env), faltan, env };
}
const hacerRedactor = (secretos) => (s) =>
  secretos.filter(k => k && k.length > 8).reduce((a, k) => a.split(k).join('[clave omitida]'), String(s ?? ''));

if (MODO === '--revisar') {
  const bundle = await readFile(BUNDLE);
  const sha = createHash('sha256').update(bundle).digest('hex');
  let puntero = null;
  for (const p of PUNTEROS) { try { await readFile(p, 'utf8'); puntero = p; break; } catch { /* siguiente */ } }
  let triples = null;
  try { const s = await (await fetch(ENGINE_STATS)).json(); triples = Number(String(s.triples ?? -1).replace(/[^0-9]/g, '')) || -1; }
  catch (e) { triples = 'motor_no_accesible:' + e.message; }
  const informe = {
    modo: 'revisar (sin spawn, sin modelo; solo lectura local)',
    bundle: { ruta: BUNDLE, bytes: bundle.length, sha256: sha },
    env_seguro: { puntero: puntero ?? 'NO_ENCONTRADO', claves_esperadas: CLAVES },
    engine_8137_triples: triples,
    casos: CASOS.map(c => c.id),
    comando_handshake: 'ONTO_ALLOW_CALLS=1 node harness_stdio.mjs --handshake   (solo root)',
    comando_casos: 'ONTO_ALLOW_CALLS=1 node harness_stdio.mjs --casos   (solo root/integrador, >=65s entre llamadas)',
  };
  await writeFile(path.join(HERE, 'harness-revisar.json'), JSON.stringify(informe, null, 2) + '\n');
  console.log(JSON.stringify({ ...informe, env_seguro: { ...informe.env_seguro } }, null, 2));
  process.exit(0);
}

if (process.env.ONTO_ALLOW_CALLS !== '1') {
  console.error('BLOQUEADO: los modos vivos exigen ONTO_ALLOW_CALLS=1 (los autoriza root). Nada ejecutado.');
  process.exit(2);
}

const { env, claves } = await cargarEnvSeguro();
const redact = hacerRedactor([env.ONTO_LLM_API_KEY]);
const hijo = spawn('node', [BUNDLE], { stdio: ['pipe', 'pipe', 'pipe'], env: { ...process.env, ...env } });
const lineas = [];
let mano = null;
const esperar = (ms) => new Promise(r => setTimeout(r, ms));
const matar = setTimeout(() => { lineas.push('[fin] timeout 120s'); try { hijo.kill(); } catch {} }, 120000);
let buf = '';
hijo.stdout.on('data', (d) => {
  buf += String(d); let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const raw = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!raw) continue;
    lineas.push(redact(raw.slice(0, 500)));
    try {
      const msg = JSON.parse(raw);
      if (msg.type === 'ready' && !mano) {
        mano = 'lista';
        if (MODO === '--handshake') { hijo.stdin.write(JSON.stringify({ type: 'reset' }) + '\n'); }
        else if (MODO === '--casos') { void enviarCasos(); }
      } else if (msg.type === 'reset_done' && MODO === '--handshake') {
        clearTimeout(matar); try { hijo.kill(); } catch {}
      }
    } catch { /* texto libre */ }
    if (lineas.length > 400) { lineas.push('[fin] demasiadas lineas'); try { hijo.kill(); } catch {} break; }
  }
});
hijo.stderr.on('data', (d) => lineas.push('[stderr] ' + redact(String(d).slice(0, 200))));
hijo.on('close', async (codigo) => {
  clearTimeout(matar);
  await writeFile(path.join(HERE, MODO === '--casos' ? 'harness-casos.json' : 'harness-handshake.json'),
    JSON.stringify({ modo: MODO, codigo, claves_env: claves, lineas }, null, 2) + '\n');
  console.log(redact(`fin codigo=${codigo} lineas=${lineas.length}`));
});
async function enviarCasos() {
  for (const c of CASOS) {
    hijo.stdin.write(JSON.stringify({ type: 'chat', message: c.pregunta, mode: 'sketch' }) + '\n');
    await esperar(65000); // pacing serie; el integrador puede espaciar mas segun RetryInfo
  }
}
