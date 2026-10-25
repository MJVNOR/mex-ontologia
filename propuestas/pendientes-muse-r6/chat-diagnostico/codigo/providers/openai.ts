/**
 * OpenAI-compatible provider con politica acotada Gemma4-Google.
 * Base: studio/src-tauri/sidecars/agent/providers/openai.ts (5291 bytes).
 * Cambios marcados con [GEMMA4]: la politica (mutex, pacing >=65s, reintento
 * acotado a 1, cooldown) solo aplica con hostname
 * generativelanguage.googleapis.com + modelo gemma-4-31b(-it); el resto
 * conserva el comportamiento original.
 */

import type { Provider, ToolSpec, ToolCall, ToolOutcome, TurnResult } from './types.js';

interface ChatMessage {
  role: 'system' | 'user' | 'assistant' | 'tool';
  content: string | null;
  tool_calls?: Array<{ id: string; type: 'function'; function: { name: string; arguments: string } }>;
  tool_call_id?: string;
}

/** [GEMMA4] Reloj inyectable: produccion usa el real; tests usan fake (sin esperas). */
export interface Reloj {
  ahora(): number;
  dormir(ms: number): Promise<void>;
}
const relojReal: Reloj = { ahora: () => Date.now(), dormir: (ms) => new Promise(r => setTimeout(r, ms)) };

/** [GEMMA4] La politica acotada aplica SOLO al provider Google Gemma4 actual:
 * hostname generativelanguage.googleapis.com + modelo gemma-4-31b(-it),
 * con o sin prefijo `models/`. Local, Gemma3, Gemini u otro host/modelo
 * recorren el camino original intacto. */
export function usaPoliticaGemma4(baseURL: string, model: string): boolean {
  let host = '';
  try {
    host = new URL(baseURL).hostname.toLowerCase();
  } catch {
    return false;
  }
  if (host !== 'generativelanguage.googleapis.com') return false;
  const id = String(model ?? '').replace(/^models\//i, '').toLowerCase();
  return id === 'gemma-4-31b-it' || id === 'gemma-4-31b';
}

/** [GEMMA4] Espera minima entre llamadas Gemma (ritmo TPM). */
export const PISO_GEMMA_MS = 65000;
/** [GEMMA4] Tope: por encima no se espera ni se reintenta; error con plazo. */
export const TOPE_ESPERA_MS = 120000;
/** [GEMMA4] Un solo reintento (2 intentos) y solo para estos estados. */
const REINTENTABLES = new Set([429, 500, 502, 503]);

/** [GEMMA4] Mutex/cola por endpoint+modelo (sin secretos en la clave: solo URL y modelo).
 * El turno se reserva ANTES del await fetch y se libera en finally incluso con
 * error/abort; dentro del turno, pacing >=65s. Asi no hay overlap posible. */
const turnos = new Map<string, Promise<void>>();
const ultimosInicios = new Map<string, number>();
/** [GEMMA4] Cooldown declarado por el servidor (deadline ms): nuevas
 * instancias/preguntas no hacen fetch antes del plazo. */
const cooldowns = new Map<string, number>();
export function claveSerie(baseURL: string, model: string): string {
  // Normaliza `models/`: el mismo modelo con o sin prefijo comparte politica y cola.
  return `${baseURL}::${String(model ?? '').replace(/^models\//i, '')}`;
}
/** Solo tests: limpia la serie entre casos (cola, inicios y cooldowns). */
export function _limpiarSerieParaTests(): void { turnos.clear(); ultimosInicios.clear(); cooldowns.clear(); }
/** Solo tests: indica si queda un turno encolado para la clave. */
export function _hayTurnoPendienteParaTests(key: string): boolean { return turnos.has(key); }

/**
 * [GEMMA4] Lee la espera exigida por el servidor: cabecera Retry-After
 * (segundos o fecha HTTP) y RetryInfo del cuerpo (`retryDelay: "Ns"`).
 * Devuelve milisegundos (>= 0). Nunca recorta: el tope se aplica fuera.
 */
export function leerEsperaServidor(resp: Response, cuerpo: string, ahoraMs: number): number {
  let ms = 0;
  try {
    const ra = resp.headers?.get?.('retry-after');
    if (ra) {
      if (/^\d+$/.test(ra.trim())) ms = Math.max(ms, Number(ra.trim()) * 1000);
      else {
        const t = Date.parse(ra);
        if (Number.isFinite(t)) ms = Math.max(ms, t - ahoraMs);
      }
    }
  } catch { /* sin cabecera valida */ }
  try {
    const m = String(cuerpo ?? '').match(/"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"/);
    if (m) ms = Math.max(ms, Math.round(Number(m[1]) * 1000));
  } catch { /* sin RetryInfo */ }
  return ms;
}

function esTimeoutReintentable(e: unknown): boolean {
  return e instanceof Error && (e as { name?: string }).name === 'TimeoutError';
}

export class OpenAICompatibleProvider implements Provider {
  readonly name = 'openai-compatible';

  private baseURL: string;
  private apiKey: string;
  private model: string;
  private system: string;
  private maxTokens: number;
  private messages: ChatMessage[] = [];
  private fetchFn: typeof fetch;
  private reloj: Reloj;
  /** Espera minima configurable entre llamadas; el piso efectivo es PISO_GEMMA_MS. */
  public minIntervalMs = 0;

  constructor(opts: { system: string; baseURL: string; apiKey?: string; model?: string; fetchFn?: typeof fetch; reloj?: Reloj }) {
    this.system = opts.system;
    this.baseURL = opts.baseURL.replace(/\/$/, '');
    this.apiKey = opts.apiKey ?? 'not-needed';
    this.model = opts.model ?? '';
    this.maxTokens = Number(process.env.ONTO_MAX_OUTPUT_TOKENS ?? 4096);
    this.fetchFn = opts.fetchFn ?? fetch;
    this.reloj = opts.reloj ?? relojReal;
  }

  /** Resolve a usable model id. MLX servers 404 on a mismatched id. */
  private async resolveModel(): Promise<string> {
    if (this.model) return this.model;
    try {
      const resp = await fetch(`${this.baseURL}/models`, {
        headers: { Authorization: `Bearer ${this.apiKey}` },
      });
      const json: any = await resp.json();
      const first = json?.data?.[0]?.id;
      if (first) {
        this.model = first;
        return first;
      }
    } catch {
      /* fall through */
    }
    this.model = 'default';
    return this.model;
  }

  async describe(): Promise<string> {
    return this.resolveModel();
  }

  setSystem(system: string): void {
    this.system = system;
  }

  reset(): void {
    this.messages = [];
  }

  addUser(text: string): void {
    if (this.messages.length === 0) {
      this.messages.push({ role: 'system', content: this.system });
    }
    this.messages.push({ role: 'user', content: text });
  }

  async step(tools: ToolSpec[]): Promise<TurnResult> {
    const model = await this.resolveModel();
    // Sin Gemma4-Google: camino original intacto (sin mutex, espera ni reintento).
    if (!usaPoliticaGemma4(this.baseURL, model)) return this.pasoDirecto(tools, model);

    const key = claveSerie(this.baseURL, model);
    const anterior = turnos.get(key) ?? Promise.resolve();
    let liberar!: () => void;
    const turno = new Promise<void>(res => { liberar = res; });
    // Se guarda la cola (tail), no el turno: el cleanup compara con la cola.
    const cola = anterior.then(() => turno);
    turnos.set(key, cola);
    try {
      await anterior;
      // [GEMMA4] Cooldown declarado: vale tambien para nuevas instancias y
      // otras preguntas. Si queda >120s se rechaza localmente con la hora
      // (sin fetch); si queda <=120s se espera el resto dentro de la cola.
      const limite = cooldowns.get(key);
      if (limite !== undefined) {
        const resto = limite - this.reloj.ahora();
        if (resto <= 0) {
          cooldowns.delete(key);
        } else if (resto > TOPE_ESPERA_MS) {
          throw new Error(`Model endpoint ${this.baseURL} (${model}): rechazo local, el servidor exige esperar hasta ${new Date(limite).toISOString()} (quedan ${Math.round(resto / 1000)}s); no se hizo ninguna llamada.`);
        } else {
          await this.reloj.dormir(resto);
          cooldowns.delete(key);
        }
      }
      return await this.pasoGemma(tools, model, key);
    } finally {
      if (turnos.get(key) === cola) turnos.delete(key);
      liberar();
    }
  }

  /** Camino original (Gemini, local, Gemma3, otros): mismo comportamiento, sin mutex/espera/reintento. */
  private async pasoDirecto(tools: ToolSpec[], model: string): Promise<TurnResult> {
    const resp = await this.fetchFn(`${this.baseURL}/chat/completions`, this.opcionesFetch(tools, model));

    if (!resp.ok) {
      throw new Error(`Model endpoint ${this.baseURL} returned HTTP ${resp.status}: ${await resp.text()}`);
    }

    return this.consumirRespuesta(await resp.json());
  }

  /** [GEMMA4] Turno exclusivo Gemma4-Google: pacing >=65s + reintento acotado a 1. */
  private async pasoGemma(tools: ToolSpec[], model: string, key: string): Promise<TurnResult> {
    const intervalo = Math.max(this.minIntervalMs, PISO_GEMMA_MS);

    for (let intento = 1; ; intento++) {
      // Pacing antes de CADA fetch (tambien del reintento): el siguiente turno
      // sale >=65s despues del inicio del fetch anterior.
      const ultimo = ultimosInicios.get(key);
      if (ultimo !== undefined) {
        const falta = intervalo - (this.reloj.ahora() - ultimo);
        if (falta > 0) await this.reloj.dormir(falta);
      }
      ultimosInicios.set(key, this.reloj.ahora());

      let resp: Response;
      try {
        resp = await this.fetchFn(`${this.baseURL}/chat/completions`, this.opcionesFetch(tools, model));
      } catch (e) {
        if (intento < 2 && esTimeoutReintentable(e)) {
          await this.reloj.dormir(PISO_GEMMA_MS);
          continue;
        }
        throw e;
      }
      if (!resp.ok) {
        const cuerpo = await resp.text();
        const clase = resp.status === 429 ? 'cuota' : 'servidor';
        // El plazo declarado se conserva en TODOS los errores, incluso el
        // terminal: nuevas instancias/preguntas no haran fetch antes del plazo.
        const declarado = leerEsperaServidor(resp, cuerpo, this.reloj.ahora());
        if (declarado > 0) cooldowns.set(key, this.reloj.ahora() + declarado);
        if (!REINTENTABLES.has(resp.status) || intento >= 2) {
          throw new Error(`Model endpoint ${this.baseURL} returned HTTP ${resp.status} (${clase}, intento ${intento}/2): ${cuerpo.slice(0, 2000)}`);
        }
        const espera = Math.max(declarado, PISO_GEMMA_MS);
        if (espera > TOPE_ESPERA_MS) {
          const limite = new Date(this.reloj.ahora() + espera).toISOString();
          throw new Error(`Model endpoint ${this.baseURL} returned HTTP ${resp.status} (${clase}): el servidor exige esperar ${Math.round(espera / 1000)}s (hasta ${limite}); no se reintenta antes del plazo.`);
        }
        await this.reloj.dormir(espera);
        continue;
      }
      cooldowns.delete(key); // el servidor respondio: se levanta el cooldown
      return this.consumirRespuesta(await resp.json());
    }
  }

  /** Cuerpo del POST, identico para ambos caminos (no diverge la firma). */
  private opcionesFetch(tools: ToolSpec[], model: string) {
    return {
      method: 'POST',
      signal: AbortSignal.timeout(90_000),
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model,
        messages: this.messages,
        ...(tools.length ? { tools: tools.map(t => ({
          type: 'function' as const,
          function: {
            name: t.name,
            description: t.description.slice(0, 1024),
            parameters: t.inputSchema,
          },
        })),
        tool_choice: 'auto' } : {}),
        temperature: 0.7,
        top_p: 0.8,
        max_tokens: this.maxTokens,
        // Gemini rejects this Qwen extension as an unknown JSON field.
        ...(new URL(this.baseURL).hostname === 'generativelanguage.googleapis.com'
          ? {} : { chat_template_kwargs: { enable_thinking: false } }),
      }),
    };
  }

  /** Registra el turno assistant 1 sola vez y solo tras exito (ambos caminos). */
  private consumirRespuesta(completion: any): TurnResult {
    const message = completion?.choices?.[0]?.message;
    if (!message) throw new Error('Model returned no message');
    const rawCalls = message.tool_calls ?? [];
    this.messages.push({
      role: 'assistant',
      content: message.content ?? null,
      ...(rawCalls.length ? { tool_calls: rawCalls } : {}),
    });
    const toolCalls: ToolCall[] = rawCalls.map((c: any) => {
      let input: Record<string, unknown> = {};
      try {
        input = c.function?.arguments ? JSON.parse(c.function.arguments) : {};
      } catch {
        // Some models emit not-quite-JSON arguments. Surface it as an empty
        // input rather than crashing the turn.
        input = {};
      }
      return { id: c.id, name: c.function?.name ?? '', input };
    });
    return {
      text: message.content ? [message.content] : [],
      toolCalls,
      stopReason: toolCalls.length > 0 ? 'tool_use' : 'end_turn',
    };
  }

  addToolResults(outcomes: ToolOutcome[]): void {
    for (const o of outcomes) {
      this.messages.push({
        role: 'tool',
        tool_call_id: o.call.id,
        content: o.content,
      });
    }
  }
}

/**
 * Oculta bloques de razonamiento (<thought>, <think>) de un texto final:
 * cerrados o incompletos (truncados a mitad). El resto se conserva
 * verbatim. Funcion pura: no toca tool calls ni firmas de pensamiento
 * (thought_signature viaja en tool_calls, intacto).
 */
export function stripThoughtBlocks(text: string): string {
  return text.replace(/<(thought|think)\b[^>]*>[\s\S]*?(<\/\1\s*>|$)/gi, '').trim();
}

/**
 * [GEMMA4] Helper puro compartido: exige respuesta final visible tras limpiar
 * pensamiento. Lanza error claro si queda vacio; index.ts lo usa en answerOnce
 * y los tests lo importan de aqui (misma funcion, no copia).
 */
export function exigirRespuestaVisible(texto: string | null | undefined): string {
  const limpio = stripThoughtBlocks(texto ?? '').trim();
  if (!limpio) throw new Error('El modelo devolvio una respuesta vacia (sin contenido final visible). No se modifico el grafo. Reintente la pregunta.');
  return limpio;
}
