/** Provider con politica acotada (propuesta; logica identica al parche).
 * Fuente: studio/.../providers/openai.ts :: step().
 * Politica: 1 solo reintento (2 intentos max) SOLO para 500/502/503 y 429,
 * SOLO en completion ANTES de ejecutar herramientas (este step() no ejecuta
 * nada: devuelve texto o toolCalls; el llamante decide). Misma Gemma.
 * Espera: RetryInfo declarado con piso 65000ms (ritmo Gemma). 500 vs 429 se
 * clasifican distinto en el error (`servidor` vs `cuota`). Cuerpo recortado.
 * Reloj inyectable para probar sin esperas reales. Sin red: fetch inyectable.
 */
export function parseRetryDelayMs(bodyText) {
  try {
    const m = String(bodyText ?? '').match(/"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"/);
    if (m) return Math.min(Math.round(Number(m[1]) * 1000), 120000);
  } catch { /* sin retardo declarado */ }
  return 0;
}
export const PISO_GEMMA_MS = 65000;
const REINTENTABLES = new Set([429, 500, 502, 503]);

export class ProveedorAcotado {
  constructor(opts, fetchFn, reloj) {
    this.system = opts.system;
    this.baseURL = opts.baseURL.replace(/\/$/, '');
    this.apiKey = opts.apiKey ?? 'not-needed';
    this.model = opts.model ?? '';
    this.maxTokens = opts.maxTokens ?? 4096;
    this.minIntervalMs = opts.minIntervalMs ?? 0;
    this.ultimoFin = 0;
    this.fetchFn = fetchFn ?? fetch;
    this.ahora = (reloj && reloj.ahora) || (() => Date.now());
    this.dormir = (reloj && reloj.dormir) || ((ms) => new Promise(r => setTimeout(r, ms)));
    this.messages = [];
    this.intentosUltimaLlamada = 0;
    this.esperasMs = [];
  }
  addUser(text) {
    if (this.messages.length === 0) this.messages.push({ role: 'system', content: this.system });
    this.messages.push({ role: 'user', content: text });
  }
  async step(tools = []) {
    const model = this.model || 'default';
    const falta = this.minIntervalMs - (this.ahora() - this.ultimoFin);
    if (falta > 0) { this.esperasMs.push(falta); await this.dormir(falta); }
    let ultimoError = null;
    for (let intento = 1; intento <= 2; intento++) {
      this.intentosUltimaLlamada = intento;
      const resp = await this.fetchFn(`${this.baseURL}/chat/completions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${this.apiKey}` },
        body: JSON.stringify({
          model, messages: this.messages,
          ...(tools.length ? { tools, tool_choice: 'auto' } : {}),
          temperature: 0.7, top_p: 0.8, max_tokens: this.maxTokens,
        }),
      });
      this.ultimoFin = this.ahora();
      if (resp.ok) {
        const completion = await resp.json();
        const message = completion?.choices?.[0]?.message;
        if (!message) throw new Error('Model returned no message');
        // Consumo unico: el mensaje assistant se registra 1 sola vez, solo en exito.
        this.messages.push({ role: 'assistant', content: message.content ?? null });
        return { text: message.content ? [message.content] : [], intentos: intento };
      }
      const cuerpo = await resp.text();
      const clase = resp.status === 429 ? 'cuota' : 'servidor';
      ultimoError = new Error(`Model endpoint ${this.baseURL} returned HTTP ${resp.status} (${clase}, intento ${intento}/2): ${cuerpo.slice(0, 2000)}`);
      if (!REINTENTABLES.has(resp.status) || intento >= 2) throw ultimoError;
      const esperaMs = Math.max(parseRetryDelayMs(cuerpo), PISO_GEMMA_MS);
      this.esperasMs.push(esperaMs);
      await this.dormir(esperaMs);
    }
    throw ultimoError;
  }
}
