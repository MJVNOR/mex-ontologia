import { describe, expect, it, vi } from 'vitest';
import { queryRows, retrieve, terms, asContext, correspondenceContext, QA_SYSTEM_PROMPT } from './graphrag.js';
import { graphAnswerCacheKey } from './cache-key.js';
import type { McpClient } from './mcp.js';

describe('graph retrieval', () => {
  it('preserves Spanish identifiers and prefers them over generic dictionary words', () => {
    expect(terms('¿Qué significa la variable año_matrimonio según su diccionario? Consulta el grafo y muestra la evidencia.')).toEqual(['año_matrimonio']);
    expect(terms('Saluda brevemente en español. No modifiques el grafo.')).toEqual([]);
  });

  it('keeps complete IRIs and escaped dictionary text in both result formats', () => {
    const iri = 'https://example.org/mex-ontologi/definition/one#row';
    const text = 'Descripción: "Año de registro"\nFormato: NNNN';
    expect(queryRows(JSON.stringify({ results: [{ e: `<${iri}>`, l: JSON.stringify(text) + '@es' }] })))
      .toEqual([{ e: iri, l: text }]);
    expect(queryRows(JSON.stringify({ results: { bindings: [{ e: { type: 'uri', value: iri }, l: { type: 'literal', value: text } }] } })))
      .toEqual([{ e: iri, l: text }]);
  });

  it('does not present failed queries as empty evidence', async () => {
    expect(() => queryRows('{"error":"invalid query"}')).toThrow('invalid query');
    expect(() => queryRows('{}')).toThrow('SPARQL');
    const mcp = { callTool: vi.fn().mockRejectedValue(new Error('Engine offline')) } as unknown as McpClient;
    await expect(retrieve(mcp, 'año_matrimonio')).rejects.toThrow('Engine offline');
  });

  it('walks from the variable through its definition to dictionary evidence using full IRIs', async () => {
    const variable = 'https://example.org/mex-ontologi/documented-variable/one';
    const definition = 'https://example.org/mex-ontologi/definition/one';
    const source = 'https://datos.example/diccionario.csv';
    const calls: string[] = [];
    const mcp = { callTool: vi.fn(async (_tool: string, args: { query: string }) => {
      calls.push(args.query);
      if (calls.length === 1) return JSON.stringify({ results: [{ e: `<${variable}>`, l: '"año_matrimonio — Matrimonios"@es' }] });
      if (args.query.includes('SELECT DISTINCT ?s ?sl ?p ?o ?ol')) {
        if (args.query.includes('VALUES ?anchor')) return JSON.stringify({ results: [{ s: `<${variable}>`, p: '<https://example.org/vocab/definicionOriginal>', o: `<${definition}>` }] });
        return JSON.stringify({ results: [
          { s: `<${definition}>`, p: '<http://purl.org/dc/terms/description>', o: '"Año de registro"@es' },
          { s: `<${definition}>`, p: '<http://www.w3.org/ns/prov#wasDerivedFrom>', o: `<${source}>` },
        ] });
      }
      return '{"results":[]}';
    }) } as unknown as McpClient;
    const retrieved = await retrieve(mcp, '¿Qué significa año_matrimonio?', 2);
    expect(retrieved.anchors).toEqual([{ iri: variable, label: 'año_matrimonio — Matrimonios' }]);
    expect(retrieved.facts.join('\n')).toContain('Año de registro');
    expect(retrieved.facts.join('\n')).toContain(source);
    expect(calls.slice(1).some(query => query.includes(`dcus:${variable}`))).toBe(false);
    expect(calls.some(query => query.includes(`VALUES ?s { <${definition}> }`))).toBe(true);
  });

  it('does not label multiple provenance sources as a contradiction', () => {
    expect(asContext({ anchors: [], facts: [], claims: [], provenance: [{ thing: 'variable', sources: ['dictionary', 'mapping'] }], conflicts: [] }))
      .not.toContain('DISPUTED');
  });
});

describe('qualified correspondence coverage', () => {
  it('reads all pages and keeps reviewed incoming mappings beyond the first 200 candidates', async () => {
    const ns = 'https://custom.example/vocab/';
    const variable = 'https://custom.example/variable';
    const calls: string[] = [];
    const mcp = { callTool: vi.fn(async (_tool: string, args: { query: string }) => {
      const q = args.query;
      calls.push(q);
      if (q.includes('# correspondence-variables')) return JSON.stringify({ results: [{ variable, name: 'año_matrimonio', namePredicate: ns + 'nombreVariableLocal' }] });
      if (q.includes('# correspondence-records')) {
        const offset = Number(q.match(/OFFSET (\d+)/)![1]);
        const all = Array.from({ length: 202 }, (_, i) => ({ mapping: `https://custom.example/m/${i}`, variable, column: `https://custom.example/c/${i}`, status: i === 201 ? 'documental_revisada' : 'candidata_por_nombre' }));
        return JSON.stringify({ results: all.slice(offset, offset + 200) });
      }
      if (q.includes('# correspondence-evidence')) return JSON.stringify({ results: [{ s: variable, p: 'http://purl.org/dc/terms/description', o: '"Año de registro"@es' }] });
      return '{"results":[]}';
    }) } as unknown as McpClient;
    const context = await correspondenceContext(mcp, ['año_matrimonio']);
    expect(context).toContain('"candidata_por_nombre":201');
    expect(context).toContain('"documental_revisada":1');
    expect(context).toContain('Mapping <https://custom.example/m/201>');
    expect(context).toContain('80/202');
    expect(context).toContain('PARTIAL');
    expect(context).toContain('Año de registro');
    expect(calls.some(q => q.includes('# correspondence-records') && q.includes('OFFSET 200'))).toBe(true);
    expect(calls.find(q => q.includes('# correspondence-evidence'))).toContain(`<${ns}definicionOriginal>`);
  });

  it('reports scoped zero counts without claiming the graph has no evidence', async () => {
    const mcp = { callTool: vi.fn(async (_tool: string, args: { query: string }) => JSON.stringify({ results: args.query.includes('# correspondence-variables') ? [{ variable: 'https://custom.example/v', name: 'año_defuncion', namePredicate: 'https://custom.example/vocab#nombreVariableLocal' }] : [] })) } as unknown as McpClient;
    expect(await correspondenceContext(mcp, ['año_defuncion'])).toContain('counts for "año_defuncion" <https://custom.example/v>: {}');
    expect(QA_SYSTEM_PROMPT).toContain('Never turn "not retrieved"');
    expect(asContext({ anchors: [], facts: [], claims: [], provenance: [], conflicts: [] })).toContain('Zero document claims does not mean no dictionary');
  });

  it('propagates a failed page instead of reporting complete counts', async () => {
    const mcp = { callTool: vi.fn(async (_tool: string, args: { query: string }) => {
      if (args.query.includes('# correspondence-variables')) return JSON.stringify({ results: [{ variable: 'https://custom.example/v', name: 'año_defuncion', namePredicate: 'https://custom.example/vocab#nombreVariableLocal' }] });
      throw new Error('Query interrupted');
    }) } as unknown as McpClient;
    await expect(correspondenceContext(mcp, ['año_defuncion'])).rejects.toThrow('Query interrupted');
  });
});

describe('answer cache evidence binding', () => {
  it('invalidates old answers when the evidence, model or instructions change', () => {
    const key = graphAnswerCacheKey('Meaning?', 'Año de registro', 'gemini', 'system');
    expect(graphAnswerCacheKey('Meaning?', 'Año de registro', 'gemini', 'system')).toBe(key);
    expect(graphAnswerCacheKey('Meaning?', 'old empty graph', 'gemini', 'system')).not.toBe(key);
    expect(graphAnswerCacheKey('Meaning?', 'Año de registro', 'other-model', 'system')).not.toBe(key);
    expect(graphAnswerCacheKey('Meaning?', 'Año de registro', 'gemini', 'new instructions')).not.toBe(key);
    expect(key).not.toBe('meaning?');
  });
});
