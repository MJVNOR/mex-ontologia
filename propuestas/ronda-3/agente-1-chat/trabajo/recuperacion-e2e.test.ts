import { describe, expect, it } from 'vitest';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { asContext, retrieve } from './graphrag.js';
import type { McpClient } from './mcp.js';

/**
 * End-to-end de RECUPERACION (sin modelo): ejecuta el retrieve()/asContext()
 * reales del codigo parchado contra el motor HTTP vivo mediante un adaptador
 * onto_query -> POST /api/query. Solo SELECT; nunca UPDATE; sin peticiones
 * a modelos. Requiere MEX_E2E_LIVE=1; en caso contrario los casos se omiten.
 */
const LIVE = process.env.MEX_E2E_LIVE === '1';
const ENGINE = process.env.MEX_ENGINE_URL ?? 'http://127.0.0.1:8137/api/query';

function httpMcp(): McpClient {
  return {
    callTool: async (tool: string, args: { query: string }) => {
      if (tool !== 'onto_query') throw new Error(`adaptador e2e: herramienta no soportada ${tool}`);
      const res = await fetch(ENGINE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: args.query }),
      });
      if (!res.ok) throw new Error(`motor HTTP ${res.status}`);
      return await res.text();
    },
  } as unknown as McpClient;
}

const PREGUNTAS = [
  'Consulta el grafo y muestra la evidencia con procedencia, sin editar ni corregir: estados de correspondencias semánticas. ¿Qué conteos registra el grafo? Cita totales por estado.',
  'Consulta el grafo y muestra la evidencia con procedencia, sin editar ni corregir: correspondencias de Matrimonios 2022. ¿Qué registra el grafo sobre sus estados y lista? Cita mapeos y columnas.',
  'Dime cuántas correspondencias tienen los Matrimonios de 2022, por favor.',
  '¿Cuáles de las correspondencias del Matrimonio de 2022 están revisadas?',
  '¿Qué estados tienen las variables documentadas? Conteos por estado.',
  'Compara correspondencias de Matrimonios 2022 y 2024 por estado, con evidencia y procedencia.',
];

describe.skipIf(!LIVE)('e2e recuperacion real sobre el motor vivo (sin modelo)', () => {
  it('C06 global, C05 recurso, parafrasis y estados de variable con evidencia guardada', async () => {
    const mcp = httpMcp();
    const salidas: Array<{ pregunta: string; contexto: string; resumen: string }> = [];
    for (const pregunta of PREGUNTAS) {
      const r = await retrieve(mcp, pregunta, 2);
      const contexto = asContext(r);
      const resumen = [
        `anchors=${r.anchors.length} facts=${r.facts.length} claims=${r.claims.length}`,
        `overview=${r.correspondenceOverview ? r.correspondenceOverview.split('\n')[0].slice(0, 220) : 'ausente'}`,
        `recurso=${r.resourceContext ? r.resourceContext.split('\n')[0].slice(0, 220) : 'ausente'}`,
        `variables=${r.variableOverview ? r.variableOverview.split('\n')[0].slice(0, 220) : 'ausente'}`,
      ].join(' | ');
      salidas.push({ pregunta, contexto, resumen });
    }

    const [c06, c05, parafrasis, singular, vars, dosAnios] = salidas;
    expect(c06.resumen).toContain('"documental_revisada":836');
    expect(c06.resumen).toContain('Total 960');
    expect(c06.contexto).toContain('GLOBAL CORRESPONDENCE COUNTS (COMPLETE)');
    expect(c05.contexto).toContain('COMPLETE correspondence counts for resolved resource');
    expect(c05.contexto).toContain('Matrimonios 2022');
    expect(c05.contexto).toContain('semantic-mapping/c92aecbb076e2efd7d2dc0f31c469576a9b3ef32fce50445035ee34758bc973a');
    expect(parafrasis.contexto).toContain('COMPLETE correspondence counts for resolved resource');
    expect(parafrasis.contexto).not.toContain('UNRESOLVED');
    expect(singular.contexto).toContain('COMPLETE correspondence counts for resolved resource');
    expect(vars.contexto).toContain('VARIABLE STATES (COMPLETE)');
    expect(vars.contexto).toContain('"respaldada_por_definicion":232');
    expect(dosAnios.contexto).toContain('COMPLETE correspondence counts for resolved resource');
    expect(dosAnios.contexto).toContain('Matrimonios 2022');
    expect(dosAnios.contexto).toContain('Matrimonios 2024');
    expect(dosAnios.contexto).not.toContain('UNRESOLVED');

    const aqui = dirname(fileURLToPath(import.meta.url));
    const destino = resolve(aqui, '..', 'evidencia', 'e2e_recuperacion.json');
    mkdirSync(dirname(destino), { recursive: true });
    writeFileSync(destino, JSON.stringify({
      motor: ENGINE,
      fecha_utc: new Date().toISOString(),
      casos: salidas,
    }, null, 2), 'utf-8');
  }, 300000);
});
