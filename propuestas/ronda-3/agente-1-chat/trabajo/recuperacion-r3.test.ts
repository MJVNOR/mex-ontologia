import { describe, expect, it, vi } from 'vitest';
import {
  asContext,
  correspondenceStatusOverview,
  keywordVariants,
  questionRange,
  questionYears,
  resourceCorrespondenceContext,
  resourceKeywords,
  retrieve,
  strictYearVerdict,
  variableStatusOverview,
  wantsCorrespondenceOverview,
  wantsResourceScope,
  wantsVariableOverview,
  QA_SYSTEM_PROMPT,
} from './graphrag.js';
import type { McpClient } from './mcp.js';

const NS = 'https://custom.example/vocab/';
const J = (v: unknown) => JSON.stringify({ results: v });

function fakeMcp(handlers: Array<[RegExp, unknown]>, calls: string[] = []): McpClient {
  return {
    callTool: vi.fn(async (_tool: string, args: { query: string }) => {
      for (const [re, payload] of handlers) {
        if (re.test(args.query)) return JSON.stringify(payload);
      }
      return '{"results":[]}';
    }),
  } as unknown as McpClient;
}

function trackedFake(
  impl: (query: string) => unknown,
  calls: string[] = [],
): McpClient {
  return {
    callTool: vi.fn(async (_tool: string, args: { query: string }) => {
      calls.push(args.query);
      return JSON.stringify(impl(args.query));
    }),
  } as unknown as McpClient;
}

const BERLIN_ANCHOR = [{ e: 'https://custom.example/dataset/matrimonios', l: 'Matrimonios' }];
const VOCAB = {
  results: [
    { pred: NS + 'estadoCorrespondencia' },
    { pred: NS + 'columnaOrigen' },
    { pred: NS + 'esquema' },
    { pred: NS + 'columna' },
    { pred: NS + 'inicioDeclarado' },
    { pred: NS + 'finDeclarado' },
  ],
};

describe('intent and keyword extraction (deterministic, no model)', () => {
  it('triggers the global overview for count/state questions without a variable name', () => {
    expect(wantsCorrespondenceOverview('¿Qué conteos registra el grafo? Cita totales por estado.')).toBe(true);
    expect(wantsCorrespondenceOverview('Saluda brevemente en español.')).toBe(false);
  });
  it('needs a year or resource word for the resource scope', () => {
    expect(wantsResourceScope('correspondencias de Matrimonios 2022: estados y lista')).toBe(true);
    expect(wantsResourceScope('estados de correspondencias semánticas, conteos por estado')).toBe(false);
  });
  it('keeps politeness and state words out of resource keywords', () => {
    expect(resourceKeywords('Dime cuántas correspondencias tienen los Matrimonios de 2022, por favor')).toEqual(['matrimonios']);
    expect(resourceKeywords('cuáles están revisadas de Matrimonios 2022')).toEqual(['matrimonios']);
    expect(resourceKeywords('correspondencias de Matrimonios 2022')).toEqual(['matrimonios']);
  });
  it('extracts every year, ranges, and singular/plural variants', () => {
    expect(questionYears('Matrimonios 2022 y 2023, comparados')).toEqual(['2022', '2023']);
    expect(questionYears('sin años aquí')).toEqual([]);
    expect(questionYears('serie 20220? no')).toEqual([]);
    expect(questionRange('cobertura entre 1990 y 2040')).toEqual({ from: 1990, to: 2040 });
    expect(questionRange('periodo 2015–2024')).toEqual({ from: 2015, to: 2024 });
    expect(questionRange('solo 2022')).toBeNull();
    expect(keywordVariants('matrimonios')).toContain('matrimonio');
    expect(keywordVariants('matrimonio')).toEqual(['matrimonio']);
  });
  it('applies the strict year rule: delimited years, period first, ranges by overlap', () => {
    expect(strictYearVerdict('Matrimonios 20220', undefined, undefined, ['2022'], null).match).toBe(false);
    expect(strictYearVerdict('Matrimonios 2022', '2022-01-01', '2022-12-31', ['2022'], null)).toMatchObject({ match: true, rule: 'declared-period' });
    const contra = strictYearVerdict('Matrimonios 2022', '2020-01-01', '2020-12-31', ['2022'], null);
    expect(contra.match).toBe(false);
    expect(contra.note).toContain('takes precedence');
    const overlap = strictYearVerdict('Serie 2015', '2015-01-01', '2024-12-31', [], { from: 1990, to: 2040 });
    expect(overlap.match).toBe(true);
    expect(overlap.note).toContain('not observed coverage');
    const outside = strictYearVerdict('Serie 1980', '1980-01-01', '1985-12-31', [], { from: 1990, to: 2040 });
    expect(outside.match).toBe(false);
  });
  it('separates variable-state questions from mapping-state questions', () => {
    expect(wantsVariableOverview('¿Qué estados tienen las variables? Conteos por estado.')).toBe(true);
    expect(wantsVariableOverview('¿Qué conteos de correspondencias registra el grafo?')).toBe(false);
  });
});

describe('global correspondence overview (native aggregation)', () => {
  it('reports current server-side counts as COMPLETE with a total', async () => {
    const calls: string[] = [];
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-status-overview')) {
        return {
          results: [
            { status: 'ambigua_por_nombre', n: '"6"^^<http://www.w3.org/2001/XMLSchema#integer>' },
            { status: 'candidata_por_nombre', n: '"118"^^<http://www.w3.org/2001/XMLSchema#integer>' },
            { status: 'documental_revisada', n: '"836"^^<http://www.w3.org/2001/XMLSchema#integer>' },
          ],
        };
      }
      return { results: [] };
    }, calls);
    const text = await correspondenceStatusOverview(mcp);
    expect(text).toContain('COMPLETE global correspondence state counts');
    expect(text).toContain('"documental_revisada":836');
    expect(text).toContain('Total 960');
    expect(text).toContain('never substitute');
    expect(calls.some((q) => q.includes('COUNT(DISTINCT'))).toBe(true);
  });

  it('answers count questions with no named variable from the overview, not the neighbourhood', async () => {
    const mcp = fakeMcp([
      [/SELECT DISTINCT \?e \?l \?score/, { results: BERLIN_ANCHOR }],
      [/correspondence-status-overview/, {
        results: [
          { status: 'candidata_por_nombre', n: '"118"' },
          { status: 'documental_revisada', n: '"836"' },
        ],
      }],
    ]);
    const r = await retrieve(mcp, 'estados de correspondencias semánticas. ¿Qué conteos registra el grafo? Cita totales por estado.');
    expect(r.correspondenceOverview).toContain('Total 954');
    expect(r.resourceContext).toBeUndefined();
    const ctx = asContext(r);
    expect(ctx).toContain('GLOBAL CORRESPONDENCE COUNTS (COMPLETE)');
    expect(ctx).toContain('Total 954');
  });

  it('propagates a failed overview instead of reporting a false zero', async () => {
    const mcp = {
      callTool: vi.fn(async (t: string, a: { query: string }) => {
        if (a.query.includes('# correspondence-status-overview')) throw new Error('Engine offline');
        if (a.query.includes('SELECT DISTINCT ?e ?l ?score')) return J(BERLIN_ANCHOR);
        return '{"results":[]}';
      }),
    } as unknown as McpClient;
    await expect(retrieve(mcp, '¿Qué conteos de correspondencias registra el grafo por estado?')).rejects.toThrow('Engine offline');
  });
});

describe('resource scope over resolved IRIs (C05 pattern, >200 records)', () => {
  function resourceWorld(calls: string[], opts: {
    andEmpty?: boolean;
    orResources?: Array<{ iri: string; label: string; ini?: string; fin?: string }>;
    resolveRows?: Array<{ resource: string; label: string; ini?: string; fin?: string }>;
    sharedColumn?: boolean;
    duplicateLabels?: boolean;
  } = {}) {
    const all = Array.from({ length: 250 }, (_, i) => ({
      mapping: `https://custom.example/m/${i}`,
      column: `https://custom.example/c/${i % 4}`,
      label: `"col${i % 4} — Matrimonios 2022 — Matrimonios"@es`,
      status: i >= 240 ? 'documental_revisada' : 'candidata_por_nombre',
      resource: 'https://custom.example/r/mat2022',
    }));
    return trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        if (opts.resolveRows) return { results: opts.resolveRows };
        if (opts.andEmpty && query.includes('divorcios')) {
          return {
            results: (opts.orResources ?? []).map((r) => ({
              resource: r.iri, label: `"${r.label}"@es`, ini: r.ini ?? '"2022-01-01"', fin: r.fin ?? '"2022-12-31"',
            })),
          };
        }
        if (opts.andEmpty) return { results: [] };
        return {
          results: [{
            resource: 'https://custom.example/r/mat2022',
            label: '"Matrimonios 2022"@es',
            ini: '"2022-01-01"',
            fin: '"2022-12-31"',
          }],
        };
      }
      if (query.includes('# resource-candidates')) return { results: [{ label: '"Matrimonios 2021"@es' }, { label: '"Divorcios 2022"@es' }] };
      if (query.includes('# resource-columns')) {
        return { results: [0, 1, 2, 3].map((i) => ({ resource: 'https://custom.example/r/mat2022', column: `https://custom.example/c/${i}` })) };
      }
      if (query.includes('# resource-status-counts')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', status: 'candidata_por_nombre', num: '"240"' },
            { resource: 'https://custom.example/r/mat2022', status: 'documental_revisada', num: '"10"' },
          ],
        };
      }
      if (query.includes('# resource-labels')) {
        return opts.duplicateLabels
          ? {
            results: [
              { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' },
              { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' },
            ],
          }
          : { results: [{ resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' }] };
      }
      if (query.includes('# resource-grand-total')) {
        return { results: [{ num: opts.sharedColumn ? '"241"' : '"250"' }] };
      }
      if (query.includes('# resource-mapping-rows')) {
        const offset = Number(query.match(/OFFSET (\d+)/)?.[1] ?? 0);
        const rows = opts.sharedColumn && offset === 0
          ? [{ mapping: 'https://custom.example/m/shared', column: 'https://custom.example/c/shared', label: '"shared"@es', status: 'candidata_por_nombre', resource: 'https://custom.example/r/other' }, ...all]
          : all;
        return { results: rows.slice(offset, offset + 200) };
      }
      if (query.includes('SELECT DISTINCT ?e ?l ?score')) return { results: BERLIN_ANCHOR };
      return { results: [] };
    }, calls);
  }

  it('resolves the resource by IRI, filters years by declared period, and reads every page', async () => {
    const calls: string[] = [];
    const mcp = resourceWorld(calls);
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. ¿Qué estados y lista registra? Cita mapeos y columnas.');
    expect(text).toContain('COMPLETE correspondence counts for resolved resource');
    expect(text).toContain('"Matrimonios 2022"');
    expect(text).toContain('"documental_revisada":10');
    expect(text).toContain('Grand total 250 distinct mappings');
    expect(text).toContain('Mapping <https://custom.example/m/249>');
    expect(text).toContain('80/250');
    expect(text).toContain('PARTIAL');
    expect(calls.some((q) => q.includes('# resource-mapping-rows') && q.includes('OFFSET 200'))).toBe(true);
    const resolve = calls.find((q) => q.includes('# resource-resolve')) ?? '';
    expect(resolve).toContain('RecursoCatalogado');
    expect(resolve).toContain('inicioDeclarado');
    expect(resolve).toContain('[^0-9]');
    expect(resolve).not.toContain('CONTAINS(STR(?label), "2022")');
    expect(calls.some((q) => q.includes('# correspondence-vocab') && q.includes('esquema|columna'))).toBe(true);
    expect(calls.some((q) => q.includes('# resource-columns') && q.includes('/esquema') && q.includes('/columna'))).toBe(true);
  });

  it('resolves a polite singular paraphrase to the same resource (no false zero)', async () => {
    const calls: string[] = [];
    const mcp = resourceWorld(calls);
    const text = await resourceCorrespondenceContext(mcp, 'Dime cuántas correspondencias tienen los Matrimonio de 2022, por favor.');
    expect(text).toContain('COMPLETE correspondence counts for resolved resource');
    expect(text).toContain('"Matrimonios 2022"');
    expect(text).not.toContain('UNRESOLVED');
  });

  it('falls back to per-keyword resolution for two resources and reports per-resource tallies', async () => {
    const calls: string[] = [];
    let resolves = 0;
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        resolves += 1;
        if (resolves === 1) return { results: [] };
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
            { resource: 'https://custom.example/r/div2022', label: '"Divorcios 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
          ],
        };
      }
      if (query.includes('# resource-columns')) {
        return { results: [{ resource: 'https://custom.example/r/mat2022', column: 'https://custom.example/c/0' }, { resource: 'https://custom.example/r/div2022', column: 'https://custom.example/c/9' }] };
      }
      if (query.includes('# resource-status-counts')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', status: 'documental_revisada', num: '"4"' },
            { resource: 'https://custom.example/r/div2022', status: 'candidata_por_nombre', num: '"6"' },
          ],
        };
      }
      if (query.includes('# resource-labels')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' },
            { resource: 'https://custom.example/r/div2022', label: '"Divorcios 2022"@es' },
          ],
        };
      }
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"10"' }] };
      if (query.includes('# resource-mapping-rows')) return { results: [] };
      return { results: [] };
    }, calls);
    const text = await resourceCorrespondenceContext(mcp, 'compara correspondencias de Matrimonios y Divorcios 2022 por estado.');
    expect(text).toContain('multi-resource OR fallback');
    expect(text).toContain('"Matrimonios 2022"');
    expect(text).toContain('"Divorcios 2022"');
    expect(text).toContain('Grand total 10 distinct mappings');
  });

  it('lists candidates without claiming zero when nothing resolves', async () => {
    const mcp = fakeMcp([
      [/correspondence-vocab/, VOCAB],
      [/resource-resolve/, { results: [] }],
      [/resource-candidates/, { results: [{ label: '"Matrimonios 2021"@es' }] }],
    ]);
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 1999. Lista y estados.');
    expect(text).toContain('UNRESOLVED');
    expect(text).toContain('"Matrimonios 2021"');
    expect(text).toContain('no zero claimed');
    expect(text).not.toContain('COMPLETE correspondence counts');
  });

  it('never matches label 20220 for year 2022', async () => {
    const mcp = fakeMcp([
      [/correspondence-vocab/, VOCAB],
      [/resource-resolve/, {
        results: [{ resource: 'https://custom.example/r/mat20220', label: '"Matrimonios 20220"@es' }],
      }],
      [/resource-candidates/, { results: [{ label: '"Matrimonios 20220"@es' }] }],
    ]);
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. Lista y estados.');
    expect(text).toContain('UNRESOLVED');
    expect(text).not.toContain('COMPLETE correspondence counts');
    expect(text).toContain('20220 never matches 2022');
  });

  it('lets the declared period win over a contradicting label year', async () => {
    const mcp = fakeMcp([
      [/correspondence-vocab/, VOCAB],
      [/resource-resolve/, {
        results: [{ resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es', ini: '"2020-01-01"', fin: '"2020-12-31"' }],
      }],
      [/resource-candidates/, { results: [{ label: '"Matrimonios 2022"@es' }] }],
    ]);
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. Lista y estados.');
    expect(text).toContain('UNRESOLVED');
    expect(text).not.toContain('COMPLETE correspondence counts');
  });

  it('notes when the label year differs but the declared period still covers the asked year', async () => {
    const calls: string[] = [];
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        return {
          results: [{ resource: 'https://custom.example/r/mat2223', label: '"Matrimonios 2025"@es', ini: '"2022-01-01"', fin: '"2023-12-31"' }],
        };
      }
      if (query.includes('# resource-columns')) return { results: [{ resource: 'https://custom.example/r/mat2223', column: 'https://custom.example/c/0' }] };
      if (query.includes('# resource-status-counts')) {
        return { results: [{ resource: 'https://custom.example/r/mat2223', status: 'documental_revisada', num: '"2"' }] };
      }
      if (query.includes('# resource-labels')) return { results: [{ resource: 'https://custom.example/r/mat2223', label: '"Matrimonios 2023"@es' }] };
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"2"' }] };
      if (query.includes('# resource-mapping-rows')) return { results: [] };
      return { results: [] };
    }, calls);
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. Lista y estados.');
    expect(text).toContain('COMPLETE correspondence counts for resolved resource');
    expect(text).toContain('takes precedence');
  });

  it('matches two asked years against their own resources', async () => {
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
            { resource: 'https://custom.example/r/mat2024', label: '"Matrimonios 2024"@es', ini: '"2024-01-01"', fin: '"2024-12-31"' },
          ],
        };
      }
      if (query.includes('# resource-columns')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', column: 'https://custom.example/c/0' },
            { resource: 'https://custom.example/r/mat2024', column: 'https://custom.example/c/4' },
          ],
        };
      }
      if (query.includes('# resource-status-counts')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', status: 'documental_revisada', num: '"4"' },
            { resource: 'https://custom.example/r/mat2024', status: 'documental_revisada', num: '"3"' },
          ],
        };
      }
      if (query.includes('# resource-labels')) {
        return {
          results: [
            { resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' },
            { resource: 'https://custom.example/r/mat2024', label: '"Matrimonios 2024"@es' },
          ],
        };
      }
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"7"' }] };
      if (query.includes('# resource-mapping-rows')) return { results: [] };
      return { results: [] };
    });
    const text = await resourceCorrespondenceContext(mcp, 'compara correspondencias de Matrimonios 2022 y 2024 por estado.');
    expect(text).toContain('COMPLETE correspondence counts for resolved resources');
    expect(text).toContain('https://custom.example/r/mat2022');
    expect(text).toContain('https://custom.example/r/mat2024');
    expect(text).toContain('Grand total 7 distinct mappings');
  });

  it('groups by resource IRI when two resources share the same label', async () => {
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', label: '"Matrimonios 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
            { resource: 'https://custom.example/r/b', label: '"Matrimonios 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
          ],
        };
      }
      if (query.includes('# resource-columns')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', column: 'https://custom.example/c/0' },
            { resource: 'https://custom.example/r/b', column: 'https://custom.example/c/1' },
          ],
        };
      }
      if (query.includes('# resource-status-counts')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', status: 'documental_revisada', num: '"4"' },
            { resource: 'https://custom.example/r/b', status: 'candidata_por_nombre', num: '"2"' },
          ],
        };
      }
      if (query.includes('# resource-labels')) {
        return { results: [{ resource: 'https://custom.example/r/a', label: '"Matrimonios 2022"@es' }, { resource: 'https://custom.example/r/b', label: '"Matrimonios 2022"@es' }] };
      }
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"6"' }] };
      if (query.includes('# resource-mapping-rows')) return { results: [] };
      return { results: [] };
    });
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. Lista y estados.');
    expect(text.match(/Resource <https:\/\/custom\.example\/r\/a>/g)).toHaveLength(1);
    expect(text.match(/Resource <https:\/\/custom\.example\/r\/b>/g)).toHaveLength(1);
    expect(text).toContain('Grand total 6 distinct mappings');
  });

  it('counts a shared column mapping once in the grand total', async () => {
    const mcp = trackedFake((query) => {
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', label: '"Serie 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
            { resource: 'https://custom.example/r/b', label: '"Serie 2022"@es', ini: '"2022-01-01"', fin: '"2022-12-31"' },
          ],
        };
      }
      if (query.includes('# resource-columns')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', column: 'https://custom.example/c/shared' },
            { resource: 'https://custom.example/r/b', column: 'https://custom.example/c/shared' },
          ],
        };
      }
      if (query.includes('# resource-status-counts')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', status: 'candidata_por_nombre', num: '"1"' },
            { resource: 'https://custom.example/r/b', status: 'candidata_por_nombre', num: '"1"' },
          ],
        };
      }
      if (query.includes('# resource-labels')) {
        return {
          results: [
            { resource: 'https://custom.example/r/a', label: '"Serie 2022"@es' },
            { resource: 'https://custom.example/r/b', label: '"Serie 2022"@es' },
          ],
        };
      }
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"1"' }] };
      if (query.includes('# resource-mapping-rows')) return { results: [] };
      return { results: [] };
    });
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Serie 2022. Lista y estados.');
    expect(text).toContain('Grand total 1 distinct mappings');
  });

  it('collapses duplicated language-tagged labels into one resource line', async () => {
    const mcp = resourceWorld([], { duplicateLabels: true });
    const text = await resourceCorrespondenceContext(mcp, 'correspondencias de Matrimonios 2022. Lista y estados.');
    expect(text.match(/Resource <https:\/\/custom\.example\/r\/mat2022>/g)).toHaveLength(1);
    expect(text).toContain('Grand total 250 distinct mappings');
  });

  it('retrieve() attaches global + resource contexts to a C05-style question', async () => {
    const calls: string[] = [];
    const mcp = trackedFake((query) => {
      if (query.includes('SELECT DISTINCT ?e ?l ?score')) return { results: BERLIN_ANCHOR };
      if (query.includes('# correspondence-status-overview')) return { results: [{ status: 'documental_revisada', num: '"4"' }] };
      if (query.includes('# correspondence-vocab')) return VOCAB;
      if (query.includes('# resource-resolve')) {
        return {
          results: [{
            resource: 'https://custom.example/r/mat2022',
            label: '"Matrimonios 2022"@es',
            ini: '"2022-01-01"',
            fin: '"2022-12-31"',
          }],
        };
      }
      if (query.includes('# resource-columns')) return { results: [{ resource: 'https://custom.example/r/mat2022', column: 'https://custom.example/c/0' }] };
      if (query.includes('# resource-status-counts')) {
        return { results: [{ resource: 'https://custom.example/r/mat2022', status: 'documental_revisada', num: '"4"' }] };
      }
      if (query.includes('# resource-labels')) {
        return { results: [{ resource: 'https://custom.example/r/mat2022', label: '"Matrimonios 2022"@es' }] };
      }
      if (query.includes('# resource-grand-total')) return { results: [{ num: '"4"' }] };
      if (query.includes('# resource-mapping-rows')) {
        return {
          results: [{
            mapping: 'https://custom.example/m/c92a',
            column: 'https://custom.example/c/0',
            label: '"año_matrimonio — Matrimonios 2022 — Matrimonios"@es',
            status: 'documental_revisada',
            resource: 'https://custom.example/r/mat2022',
          }],
        };
      }
      return { results: [] };
    }, calls);
    const r = await retrieve(mcp, 'correspondencias de Matrimonios 2022. ¿Qué registra el grafo sobre sus estados y lista? Cita mapeos y columnas.');
    expect(r.correspondenceOverview).toContain('COMPLETE global');
    expect(r.resourceContext).toContain('Matrimonios 2022');
    expect(r.resourceContext).toContain('https://custom.example/m/c92a');
    expect(asContext(r)).toContain('RESOURCE-SCOPED CORRESPONDENCES (COMPLETE FOR THE STATED FILTER)');
  });
});

describe('variable states vs correspondence states', () => {
  it('keeps estadoSemantico and estadoCorrespondencia in separate tallies', async () => {
    const mcp = fakeMcp([
      [/SELECT DISTINCT \?e \?l \?score/, { results: BERLIN_ANCHOR }],
      [/variable-status-overview/, {
        results: [
          { status: 'respaldada_por_definicion', n: '"232"' },
          { status: 'candidata_sin_definicion_suficiente', n: '"23"' },
        ],
      }],
    ]);
    const r = await retrieve(mcp, '¿Qué estados tienen las variables documentadas? Conteos por estado.');
    expect(r.variableOverview).toContain('"respaldada_por_definicion":232');
    expect(r.variableOverview).toContain('never be merged');
    expect(r.variableOverview).toContain('estadoSemantico');
    expect(QA_SYSTEM_PROMPT).toContain('estadoSemantico belongs to the variable');
  });
});

describe('no-result and prompt guards', () => {
  it('qualifies empty overviews as scoped zeros and forbids absence claims', async () => {
    const mcp = fakeMcp([[/correspondence-status-overview/, { results: [] }]]);
    expect(await correspondenceStatusOverview(mcp)).toContain('scoped zero');
    const emptyVar = fakeMcp([[/variable-status-overview/, { results: [] }]]);
    expect(await variableStatusOverview(emptyVar)).toContain('scoped zero');
    expect(QA_SYSTEM_PROMPT).toContain('Never turn "not retrieved" into "does not exist in the graph"');
    expect(asContext({ anchors: [], facts: [], claims: [], provenance: [], conflicts: [] }))
      .toContain('Zero document claims does not mean no dictionary');
  });
});
