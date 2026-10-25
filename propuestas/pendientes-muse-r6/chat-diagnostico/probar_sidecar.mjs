/** Sonda 3: protocolo del sidecar (index.ts) para health/model.status/message.
 * Parte A (estatica, siempre): audita que tipos de mensaje admite el sidecar.
 * Parte B (viva, --vivo): handshake `reset` contra el binario REAL dist/index.js
 * por stdin/stdout. `reset` no llama al modelo ni muta el grafo: solo limpia el
 * historial en memoria del proceso sonda y devuelve reset_done. Engine: solo
 * initialize/listTools (lectura). Si la API no admite health/model.status/message,
 * se registra como "no_admitido" y NO se inventa la prueba.
 * Uso: node probar_sidecar.mjs [--vivo]
 * Salida: sidecar-protocolo.json
 */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFile, writeFile } from 'node:fs/promises';
import { spawn } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const AGENT_SRC = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const src = await readFile(path.join(AGENT_SRC, 'index.ts'), 'utf8');

const inbound = [...src.matchAll(/msg\.type\s*===\s*'([^']+)'/g)].map(m => m[1]);
const outbound = [...new Set([...src.matchAll(/type:\s*'([a-z_]+)'/g)].map(m => m[1]))];
const audit = {
  admite_health: inbound.includes('health'),
  admite_model_status: inbound.includes('model.status') || inbound.includes('model_status'),
  admite_message: inbound.includes('message'),
  tipos_entrada_reales: [...new Set(inbound)],
  tipos_salida_reales: outbound,
};
let viva = null;
if (process.argv.includes('--vivo')) {
  viva = await new Promise((resolve) => {
    const out = { lineas: [], ok: false, error: null };
    let child;
    try {
      child = spawn('node', [path.join(AGENT_SRC, 'dist', 'index.js')], { stdio: ['pipe', 'pipe', 'pipe'] });
    } catch (e) { out.error = String(e); resolve(out); return; }
    const kill = setTimeout(() => { out.error = 'timeout 45s sin ready/reset_done'; try { child.kill(); } catch {} resolve(out); }, 45000);
    let buf = '';
    child.stdout.on('data', (d) => {
      buf += String(d);
      let i;
      while ((i = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
        if (!line) continue;
        out.lineas.push(line.slice(0, 300));
        try {
          const msg = JSON.parse(line);
          if (msg.type === 'ready' && !out.reset_enviado) {
            out.reset_enviado = true;
            child.stdin.write(JSON.stringify({ type: 'reset' }) + '\n');
          } else if (msg.type === 'reset_done') {
            out.ok = true; clearTimeout(kill);
            try { child.kill(); } catch {}
            resolve(out);
          }
        } catch { /* linea no JSON: se conserva recortada */ }
        if (out.lineas.length > 12) { out.error = 'demasiadas lineas sin reset_done'; clearTimeout(kill); try { child.kill(); } catch {} resolve(out); break; }
      }
    });
    child.stderr.on('data', (d) => { out.lineas.push('[stderr] ' + String(d).slice(0, 200)); });
    child.on('error', (e) => { out.error = String(e); clearTimeout(kill); resolve(out); });
  });
}
const resultado = {
  sonda: 'sidecar-protocolo',
  conclusion: (audit.admite_health || audit.admite_model_status || audit.admite_message) ? 'n/a' : 'health/model.status/message NO admitidos por index.ts: solo chat y reset; la prueba viva cubre reset (sin modelo)',
  auditoria_estatica: audit,
  prueba_viva_reset: viva ?? 'no_ejecutada (usar --vivo; la coordina el integrador si hace falta repetirla)',
};
await writeFile(path.join(HERE, 'sidecar-protocolo.json'), JSON.stringify(resultado, null, 2) + '\n');
console.log(JSON.stringify(resultado, null, 2));
