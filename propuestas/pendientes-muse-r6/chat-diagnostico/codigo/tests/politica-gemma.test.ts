// Pruebas de la politica acotada Gemma4 contra las FUNCIONES REALES de
// codigo/providers/openai.ts (sin red, sin modelo; reloj fake, sin esperas).
import { describe, it, expect, beforeEach } from 'vitest';
import {
  OpenAICompatibleProvider,
  usaPoliticaGemma4,
  claveSerie,
  leerEsperaServidor,
  exigirRespuestaVisible,
  PISO_GEMMA_MS,
  _limpiarSerieParaTests,
  _hayTurnoPendienteParaTests,
} from '../providers/openai.js';

type FetchFn = (url: any, opts?: any) => Promise<Response>;
const GOOGLE = 'https://generativelanguage.googleapis.com/v1beta/openai';
const R = (status: number, cuerpo: string, headers: Record<string, string> = {}) =>
  new Response(cuerpo, { status, headers });

// Reloj fake compartido: el tiempo solo avanza al "dormir"; jamas espera real.
function relojFake() {
  let t = 1_000_000;
  const dormidas: number[] = [];
  return { ahora: () => t, dormir: async (ms: number) => { dormidas.push(ms); t += ms; }, dormidas };
}
function prov(modelo: string, fetchFn: FetchFn, reloj: ReturnType<typeof relojFake>, baseURL = GOOGLE) {
  return new OpenAICompatibleProvider({ system: 's', baseURL, model: modelo, fetchFn: fetchFn as typeof fetch, reloj });
}

beforeEach(() => _limpiarSerieParaTests());

describe('alcance: solo Gemma4-Google', () => {
  it('gating por host + modelo (con/sin prefijo models/)', () => {
    expect(usaPoliticaGemma4(GOOGLE, 'gemma-4-31b-it')).toBe(true);
    expect(usaPoliticaGemma4(GOOGLE, 'models/gemma-4-31b-it')).toBe(true);
    expect(usaPoliticaGemma4(GOOGLE, 'gemma-4-31b')).toBe(true);
    expect(usaPoliticaGemma4('https://generativelanguage.googleapis.com/v1beta/openai/', 'gemma-4-31b-it')).toBe(true);
    expect(usaPoliticaGemma4(GOOGLE, 'gemma-3-27b-it')).toBe(false);
    expect(usaPoliticaGemma4(GOOGLE, 'gemini-3.1-flash-lite')).toBe(false);
    expect(usaPoliticaGemma4(GOOGLE, '')).toBe(false);
    expect(usaPoliticaGemma4('http://localhost:8081/v1', 'gemma-4-31b-it')).toBe(false);
    expect(usaPoliticaGemma4('http://127.0.0.1:11434/v1', 'gemma-4-31b-it')).toBe(false);
    expect(usaPoliticaGemma4('no-es-url', 'gemma-4-31b-it')).toBe(false);
  });

  it('clave de serie sin secretos (solo URL + modelo)', () => {
    const clave = 'CLAVE-ULTRA-SECRETA-12345';
    const k = claveSerie(GOOGLE, 'gemma-4-31b-it');
    expect(k).toBe(`${GOOGLE}::gemma-4-31b-it`);
    expect(k).not.toContain(clave);
    // `models/` normalizado: mismo modelo, misma serie y politica.
    expect(claveSerie(GOOGLE, 'models/gemma-4-31b-it')).toBe(k);
    void clave;
  });

  it('local con modelo gemma: camino original (500 sin reintento ni espera)', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => (n++, R(500, 'err-local')), r, 'http://localhost:8081/v1');
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow('HTTP 500: err-local');
    expect(n).toBe(1);
    expect(r.dormidas).toEqual([]);
  });

  it('gemini en google: camino original integro (cuerpo entero, 1 intento)', async () => {
    const r = relojFake();
    let n = 0;
    const cuerpo = 'E'.repeat(3000);
    const p = prov('gemini-3.1-flash-lite', async () => (n++, R(500, cuerpo)), r);
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow(`HTTP 500: ${cuerpo}`);
    expect(n).toBe(1);
    expect(r.dormidas).toEqual([]);
  });
});

describe('reintento acotado Gemma4-Google', () => {
  it('500 -> 1 reintento y exito; espera = piso 65s', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () =>
      (++n === 1 ? R(500, '{"error":{"code":500,"message":"Internal error encountered.","status":"INTERNAL"}}') : R(200, '{"choices":[{"message":{"content":"hola"}}]}')), r);
    p.addUser('q');
    const out = await p.step([]);
    expect(out.text.join('')).toBe('hola');
    expect(n).toBe(2);
    expect(r.dormidas).toEqual([PISO_GEMMA_MS]);
  });

  it('500 persistente: 2 intentos, error clasificado servidor', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => (n++, R(500, 'e')), r);
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow(/HTTP 500 \(servidor, intento 2\/2\)/);
    expect(n).toBe(2);
  });

  it('429 con RetryInfo 8s: espera max(8s, 65s); clase cuota', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => (n++, R(429, '{"details":[{"retryDelay":"8s"}]}')), r);
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow(/HTTP 429 \(cuota, intento 2\/2\)/);
    expect(r.dormidas).toEqual([PISO_GEMMA_MS]);
  });

  it('Retry-After cabecera manda si supera al piso', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => (n++, R(503, 'busy', { 'retry-after': '90' })), r);
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow(/503/);
    expect(r.dormidas).toEqual([90000]);
  });

  it('espera >120s: error explicito con plazo, sin esperar ni reintentar', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => (n++, R(503, 'busy', { 'retry-after': '300' })), r);
    p.addUser('q');
    await expect(p.step([])).rejects.toThrow(/exige esperar 300s.*hasta .*; no se reintenta antes del plazo/);
    expect(n).toBe(1);
    expect(r.dormidas).toEqual([]);
  });

  it('400 y 401 jamas se reintentan', async () => {
    for (const st of [400, 401]) {
      const r = relojFake();
      let n = 0;
      const p = prov('gemma-4-31b-it', async () => (n++, R(st, 'x'.repeat(5000))), r);
      p.addUser('q');
      await expect(p.step([])).rejects.toThrow(new RegExp(`HTTP ${st} `));
      expect(n).toBe(1);
    }
  });

  it('TimeoutError se reintenta 1 vez; AbortError jamas', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () => {
      n++;
      if (n === 1) { const e = new Error('timeout'); e.name = 'TimeoutError'; throw e; }
      return R(200, '{"choices":[{"message":{"content":"ok"}}]}');
    }, r);
    p.addUser('q');
    const out = await p.step([]);
    expect(out.text.join('')).toBe('ok');
    expect(r.dormidas).toEqual([PISO_GEMMA_MS]);

    const r2 = relojFake();
    _limpiarSerieParaTests();
    let m = 0;
    const p2 = prov('gemma-4-31b-it', async () => { m++; const e = new Error('cancel'); e.name = 'AbortError'; throw e; }, r2);
    p2.addUser('q');
    await expect(p2.step([])).rejects.toThrow('cancel');
    expect(m).toBe(1);
    expect(r2.dormidas).toEqual([]);
  });

  it('historial: assistant 1 sola vez y solo tras exito', async () => {
    const r = relojFake();
    let n = 0;
    const p = prov('gemma-4-31b-it', async () =>
      (++n === 1 ? R(502, 'bad gateway') : R(200, '{"choices":[{"message":{"content":"ok"}}]}')), r);
    p.addUser('q');
    await p.step([]);
    const roles = (p as unknown as { messages: Array<{ role: string }> }).messages.map(m => m.role);
    expect(roles).toEqual(['system', 'user', 'assistant']);
  });

  it('reintento actualiza pacing: nuevo provider espera >=65s tras el SEGUNDO intento', async () => {
    const r = relojFake();
    const tiempos: number[] = [];
    let n = 0;
    const f: FetchFn = async () => {
      tiempos.push(r.ahora()); n++;
      return n === 1
        ? R(500, '{"error":{"code":500}}')
        : R(200, '{"choices":[{"message":{"content":"ok"}}]}');
    };
    const a = prov('gemma-4-31b-it', f, r);
    a.addUser('q');
    const outA = await a.step([]);
    expect(outA.text.join('')).toBe('ok');
    expect(n).toBe(2);
    expect(tiempos[1] - tiempos[0]).toBe(PISO_GEMMA_MS);
    const b = prov('gemma-4-31b-it', f, r);
    b.addUser('q2');
    const outB = await b.step([]);
    expect(outB.text.join('')).toBe('ok');
    expect(n).toBe(3);
    // Con el fallo anterior (timestamp solo antes del bucle) este gap era 0.
    expect(tiempos[2] - tiempos[1]).toBeGreaterThanOrEqual(65000);
  });

  it('cooldown persiste en error terminal del segundo intento; nuevo provider sin fetch', async () => {
    const r = relojFake();
    let n = 0;
    const f: FetchFn = async () => {
      n++;
      if (n === 1) return R(429, 'q', { 'retry-after': '60' });
      return R(429, 'q', { 'retry-after': '900' });
    };
    const a = prov('gemma-4-31b-it', f, r);
    a.addUser('q');
    const errA = await a.step([]).catch(e => e);
    expect(n).toBe(2);
    expect(String(errA?.message)).toMatch(/HTTP 429 \(cuota, intento 2\/2\)/);
    // El segundo 429 declaro 900s desde t=1_065_000: mismo plazo bloquea al siguiente.
    const plazoISO = new Date(1000000 + 65000 + 900000).toISOString();
    const b = prov('gemma-4-31b-it', f, r);
    b.addUser('otra pregunta');
    const errB = await b.step([]).catch(e => e);
    expect(n).toBe(2); // 0 fetch adicional
    expect(String(errB?.message)).toContain('rechazo local');
    expect(String(errB?.message)).toContain(plazoISO);
  });
});

describe('mutex por endpoint+modelo (sin overlap)', () => {
  it('el segundo NO EMPIEZA hasta que termina el primero + 65000', async () => {
    const r = relojFake();
    const eventos: string[] = [];
    let liberarFetch1!: (v: Response) => void;
    let llamadas = 0;
    const f: FetchFn = () => {
      llamadas++;
      const id = llamadas;
      eventos.push(`fetch${id}@t=${r.ahora()}`);
      if (id === 1) return new Promise<Response>(res => { liberarFetch1 = res; });
      return Promise.resolve(R(200, '{"choices":[{"message":{"content":"b"}}]}'));
    };
    const a = prov('gemma-4-31b-it', f, r);
    const b = prov('gemma-4-31b-it', f, r);
    a.addUser('a'); b.addUser('b');
    const ta = a.step([]);
    await Promise.resolve();
    await new Promise(res => setTimeout(res, 0));
    const tb = b.step([]);
    await Promise.resolve();
    await new Promise(res => setTimeout(res, 0));
    // Primer fetch bloqueado: el segundo ni siquiera ha llamado a fetch.
    expect(llamadas).toBe(1);
    liberarFetch1(R(200, '{"choices":[{"message":{"content":"a"}}]}'));
    const [ra, rb] = await Promise.all([ta, tb]);
    expect(ra.text.join('')).toBe('a');
    expect(rb.text.join('')).toBe('b');
    // Segunda llamada: 65s despues del inicio de la primera (mutex + pacing).
    expect(r.dormidas).toEqual([65000]);
    expect(eventos).toHaveLength(2);
    const t1 = Number(eventos[0].split('t=')[1]);
    const t2 = Number(eventos[1].split('t=')[1]);
    expect(t2 - t1).toBeGreaterThanOrEqual(65000);
  });

  it('dos instancias secuenciales: una sola espera de intervalo', async () => {
    const r = relojFake();
    const p = prov('gemma-4-31b-it', async () => R(200, '{"choices":[{"message":{"content":"x"}}]}'), r);
    p.addUser('a'); await p.step([]);
    p.addUser('b'); await p.step([]);
    expect(r.dormidas).toEqual([65000]);
  });

  it('la cola se limpia al terminar el turno (sin fugas)', async () => {
    const r = relojFake();
    const key = claveSerie(GOOGLE, 'gemma-4-31b-it');
    let liberarFetch!: (v: Response) => void;
    let llamadas = 0;
    const p = prov('gemma-4-31b-it', () => {
      llamadas++;
      return new Promise<Response>(res => { liberarFetch = res; });
    }, r);
    p.addUser('q');
    const prom = p.step([]);
    for (let i = 0; i < 10; i++) await Promise.resolve();
    expect(llamadas).toBe(1);
    expect(_hayTurnoPendienteParaTests(key)).toBe(true);
    liberarFetch(R(200, '{"choices":[{"message":{"content":"x"}}]}'));
    const out = await prom;
    expect(out.text.join('')).toBe('x');
    // Con el fallo anterior (comparar con el turno en vez de la cola) esto quedaba en true.
    expect(_hayTurnoPendienteParaTests(key)).toBe(false);
  });
});

describe('cooldown declarado por el servidor (un solo ciclo; el beforeEach limpiaria el estado)', () => {
  it('429-900s guarda plazo; nuevo provider es rechazado sin fetch; tras vencer, fetch', async () => {
    const r = relojFake();
    let n = 0;
    const okBody = '{"choices":[{"message":{"content":"ok"}}]}';
    const criada = () => prov('gemma-4-31b-it', async () => (n++, R(200, okBody)), r);

    // 1. 429 con 900s: error con plazo, 1 fetch, cooldown guardado.
    const a = prov('gemma-4-31b-it', async () => (n++, R(429, 'q', { 'retry-after': '900' })), r);
    a.addUser('q');
    const errA = await a.step([]).catch(e => e);
    expect(n).toBe(1);
    expect(r.dormidas).toEqual([]);
    const m = String(errA?.message).match(/exige esperar 900s \(hasta (\S+?)\)/);
    expect(m).toBeTruthy();
    const plazoISO = m![1];

    // 2. Nuevo provider antes del plazo: 0 fetch adicional y misma hora.
    const b = criada();
    b.addUser('otra pregunta');
    const errB = await b.step([]).catch(e => e);
    expect(n).toBe(1);
    expect(r.dormidas).toEqual([]);
    expect(String(errB?.message)).toContain('rechazo local');
    expect(String(errB?.message)).toContain(plazoISO);

    // 3. Restante <=120s: espera el resto dentro de la cola y llama.
    await r.dormir(800000); // simula paso del tiempo: quedan 100s
    const d = criada();
    d.addUser('q4');
    const outD = await d.step([]);
    expect(outD.text.join('')).toBe('ok');
    expect(n).toBe(2);
    expect(r.dormidas.slice(-1)).toEqual([100000]);

    // 4. Tras exito se levanta el cooldown: siguiente llama sin espera extra.
    const e = criada();
    e.addUser('q5');
    const outE = await e.step([]);
    expect(outE.text.join('')).toBe('ok');
    expect(n).toBe(3);
  });
});

describe('cooldown superado: fetch permitido', () => {
  it('avanzado el clock hasta vencimiento: si fetch', async () => {
    const r2 = relojFake();
    let m = 0;
    const a = prov('gemma-4-31b-it', async () => (m++, R(429, 'q', { 'retry-after': '900' })), r2);
    a.addUser('q');
    await a.step([]).catch(e => e);
    expect(m).toBe(1);
    await r2.dormir(900000); // hasta el vencimiento exacto
    const c = prov('gemma-4-31b-it', async () => (m++, R(200, '{"choices":[{"message":{"content":"ok"}}]}')), r2);
    c.addUser('q2');
    const out = await c.step([]);
    expect(out.text.join('')).toBe('ok');
    expect(m).toBe(2);
  });
});

describe('leerEsperaServidor', () => {
  it('segundos, fecha HTTP y RetryInfo; toma el maximo', () => {
    const ahora = 1_000_000;
    expect(leerEsperaServidor(new Response('x', { headers: { 'retry-after': '30' } }), '{}', ahora)).toBe(30000);
    const fecha = new Date(ahora + 45000).toUTCString();
    expect(leerEsperaServidor(new Response('x', { headers: { 'retry-after': fecha } }), '{}', ahora)).toBe(45000);
    expect(leerEsperaServidor(new Response('x'), '{"retryDelay":"90s"}', ahora)).toBe(90000);
    expect(leerEsperaServidor(new Response('x', { headers: { 'retry-after': '10' } }), '{"retryDelay":"20s"}', ahora)).toBe(20000);
    expect(leerEsperaServidor(new Response('x'), '{}', ahora)).toBe(0);
  });
});

describe('exigirRespuestaVisible (helper puro compartido)', () => {
  it('vacio/blancos/solo-pensamiento lanzan; visible pasa', () => {
    expect(() => exigirRespuestaVisible('')).toThrow(/respuesta vacia/);
    expect(() => exigirRespuestaVisible('   \n ')).toThrow(/respuesta vacia/);
    expect(() => exigirRespuestaVisible('<thought>razono</thought>')).toThrow(/respuesta vacia/);
    expect(() => exigirRespuestaVisible('<think>hmm')).toThrow(/respuesta vacia/);
    expect(exigirRespuestaVisible('<thought>x</thought>respuesta util')).toBe('respuesta util');
    expect(exigirRespuestaVisible('  hola  ')).toBe('hola');
  });
});
