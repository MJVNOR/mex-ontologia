// Preload Node: intercepta fetch a Google ANTES de red, sin headers/secreto.
// Uso: node --import <este archivo> <bundle>
// Solo guarda URL (sin query) + body JSON. Lanza Error de diagnóstico (name=Error, NO TimeoutError) para evitar retry.
import fs from 'node:fs';
const OUT = process.env.C6_OUT ?? process.cwd();
const FILE = OUT + '/payload-intercept.json';
const COUNT = OUT + '/google-count.txt';
const orig = globalThis.fetch;
globalThis.fetch = async (input, init = {}) => {
  const s = typeof input === 'string' ? input : String(input?.url ?? input);
  if (s.includes('generativelanguage.googleapis.com')) {
    let body = null;
    try { body = JSON.parse(String(init?.body ?? '')); }
    catch { body = { _no_json: String(init?.body ?? '').slice(0, 2000) }; }
    const q = s.indexOf('?');
    const rec = {
      url_sin_query: q >= 0 ? s.slice(0, q) : s,
      query_redactada: q >= 0,
      method: init?.method ?? 'POST',
      body,
      intercepted_at: new Date().toISOString(),
      nota: 'Captura offline: NO se emitio a red; sin headers/secreto.'
    };
    try { fs.writeFileSync(FILE, JSON.stringify(rec, null, 2) + '\n'); } catch {}
    try { fs.writeFileSync(COUNT, '1\n'); } catch {}
    const e = new Error('DIAG_CAPTURA_C6: payload interceptado antes de red; llamada real NO emitida (0 requests Google)');
    e.name = 'Error';
    throw e;
  }
  return orig(input, init);
};
