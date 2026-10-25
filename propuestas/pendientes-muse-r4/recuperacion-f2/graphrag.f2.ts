/**
 * GraphRAG: retrieval where the knowledge graph supplies the topology.
 *
 * Classic RAG retrieves text chunks ranked by embedding similarity. The
 * retrieval unit has no structure, so multi-hop, aggregation, absence and
 * contradiction questions are unanswerable in principle rather than in
 * practice.
 *
 * Here the retrieval unit is a SUBGRAPH. The pipeline is:
 *
 *   question -> anchors      entities whose labels the question mentions
 *            -> neighbourhood  bounded traversal outward from those anchors
 *            -> claims         the document passages attached to them
 *            -> provenance     which upstream source asserted what
 *
 * The graph's own edges decide what is relevant, which is what "the topology
 * structures the retrieval" means concretely. Nothing is chunked, and nothing
 * is ranked by cosine distance.
 *
 * Everything returned carries its source, so the model can cite rather than
 * paraphrase, and a claim with no support is visibly unsupported.
 *
 * This module runs unrestricted: it has no notion of a viewer role, and every
 * document the graph holds is reachable through it. Access control is a
 * separate concern, layered on top of retrieval rather than into it.
 */

import type { McpClient } from './mcp.js';

const NS = process.env.ONTO_NS ?? 'https://w3id.org/dcat-us-demo#';
const P = `PREFIX dcus: <${NS}>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX prov: <http://www.w3.org/ns/prov#>
`;

const STOP = new Set(
  ('the a an of to in for is are be and or that this with by on at as it its what which who whom ' +
   'why how when where does do did can could would should may might will shall about any all some ' +
   'there their they them we our you your i me my show tell give list find explain').split(' '),
);

export interface Retrieved {
  anchors: Array<{ iri: string; label: string }>;
  facts: string[];
  claims: Array<{ text: string; doc: string; section: string }>;
  provenance: Array<{ thing: string; sources: string[] }>;
  conflicts: string[];
  correspondenceContext?: string;
  correspondenceOverview?: string;
  resourceContext?: string;
  variableOverview?: string;
  cruceFichaContext?: string;
  cruceCodigoContext?: string;
}

/** Fichas de cruce ronda-3 por alias corto (F1, F2, ...).
 * terms() exige >=3 caracteres y el anclaje por etiqueta con LIMIT 16
 * expulsa la ficha cuando la pregunta trae genéricos ("otros", "2020"...).
 * Esto resuelve el alias ANTES del vecindario: si la pregunta nombra F2,
 * la ficha se recupera por IRI exacto, sin depender de terms()/anchors.
 * Solo lectura SELECT; no toca el grafo ni otros caminos. */
const CRUCE_BASE = 'https://example.org/mex-ontologi/cruce-r3/';

export function cruceAliases(question: string): string[] {
  const out: string[] = [];
  for (const m of question.normalize('NFC').matchAll(/\bF\s?(\d{1,3})\b/gi)) {
    const alias = `F${m[1]}`;
    if (!out.includes(alias)) out.push(alias);
  }
  return out.slice(0, 4);
}

export async function cruceFichaContext(
  mcp: McpClient,
  question: string,
): Promise<{ context: string; anchors: Array<{ iri: string; label: string }> }> {
  const aliases = cruceAliases(question);
  if (!aliases.length) return { context: '', anchors: [] };
  const sections: string[] = [];
  const anchors: Array<{ iri: string; label: string }> = [];
  for (const alias of aliases) {
    const iri = `${CRUCE_BASE}${alias}`;
    const ficha = await selectAll(mcp, `${P}
      # cruce-ficha
      SELECT DISTINCT ?p ?o ?ol WHERE {
        VALUES ?s { <${iri}> }
        ?s ?p ?o .
        OPTIONAL { ?o rdfs:label ?ol }
        FILTER(!isBlank(?o))
      } ORDER BY ?p ?o ?ol`);
    if (!ficha.length) continue;
    const label = ficha.find(r => r.p === 'http://www.w3.org/2000/01/rdf-schema#label')?.o ?? alias;
    anchors.push({ iri, label });
    const compCount = await selectAll(mcp, `${P}
      # cruce-comp-count
      SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE {
        ?c <https://example.org/mex-ontologi/vocab/comparacionDe> <${iri}> .
      }`);
    const evCount = await selectAll(mcp, `${P}
      # cruce-ev-count
      SELECT (COUNT(DISTINCT ?e) AS ?n) WHERE {
        ?c <https://example.org/mex-ontologi/vocab/comparacionDe> <${iri}> .
        ?e <https://example.org/mex-ontologi/vocab/evidenciaDeFuente> ?c .
      }`);
    const nComp = compCount[0]?.n ?? '0';
    const nEv = evCount[0]?.n ?? '0';
    // Resumen derivado del RDF real de ESTA ficha (periodos, roles y
    // medidas observados por agregacion nativa). Nada hardcodeado de F2:
    // F1/F3 tienen sus propios periodos/medidas (o cero comparaciones).
    const periods = await selectAll(mcp, `${P}
      # cruce-periodos
      SELECT DISTINCT ?per WHERE {
        ?c <https://example.org/mex-ontologi/vocab/comparacionDe> <${iri}> .
        ?c <https://example.org/mex-ontologi/vocab/periodoCruzado> ?per .
      } ORDER BY ?per`);
    const rolesMed = await selectAll(mcp, `${P}
      # cruce-roles-medidas
      SELECT DISTINCT ?rol ?med WHERE {
        ?c <https://example.org/mex-ontologi/vocab/comparacionDe> <${iri}> .
        ?e <https://example.org/mex-ontologi/vocab/evidenciaDeFuente> ?c .
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/fuenteRol> ?rol }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/medidaOrigen> ?med }
      } ORDER BY ?rol ?med`);
    const perList = [...new Set(periods.map(r => r.per).filter(Boolean))];
    const roleList = [...new Set(rolesMed.map(r => r.rol).filter(Boolean))];
    const medList = [...new Set(rolesMed.map(r => r.med).filter(Boolean))];
    const perTxt = perList.length
      ? ` (periodo(s) cruzado(s) en RDF: ${perList.map(p => JSON.stringify(p)).join(', ')})`
      : ' (sin comparaciones municipales en RDF)';
    const rmTxt =
      roleList.length || medList.length
        ? ` (roles: ${roleList.map(r => JSON.stringify(r)).join(', ') || '—'}; medidas: ${medList.map(m => JSON.stringify(m)).join(', ') || '—'})`
        : '';
    const sampleAll = await selectAll(mcp, `${P}
      # cruce-sample
      SELECT DISTINCT ?c ?cl ?per WHERE {
        ?c <https://example.org/mex-ontologi/vocab/comparacionDe> <${iri}> .
        OPTIONAL { ?c <https://example.org/mex-ontologi/vocab/periodoCruzado> ?per }
        OPTIONAL { ?c rdfs:label ?cl }
      } ORDER BY ?c`);
    const sample = sampleAll.slice(0, 3);
    const evSample = sample.length
      ? (await selectAll(mcp, `${P}
      # cruce-ev-sample
      SELECT DISTINCT ?e ?rol ?medida ?nombre ?fuente ?hoja ?sha ?valor WHERE {
        VALUES ?c { ${iriValues(sample.map(r => r.c))} }
        ?e <https://example.org/mex-ontologi/vocab/evidenciaDeFuente> ?c .
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/fuenteRol> ?rol }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/medidaOrigen> ?medida }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/nombreOrigen> ?nombre }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/fuenteOriginal> ?fuente }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/hojaFuente> ?hoja }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/shaFuente> ?sha }
        OPTIONAL { ?e <https://example.org/mex-ontologi/vocab/valorOrigen> ?valor }
      } ORDER BY ?e ?rol`)).slice(0, 12)
      : [];
    const lines = ficha.map(r => {
      const o = isIri(r.o) ? (r.ol ? `${JSON.stringify(r.ol)} <${r.o}>` : `<${r.o}>`) : JSON.stringify(r.o);
      return `- <${iri}> --[<${r.p}>]--> ${o}`;
    });
    sections.push(
      `COMPLETE ficha ${alias} <${iri}> (${JSON.stringify(label)}): ${nComp} comparaciones${perTxt} y ${nEv} evidencias${rmTxt}. Todas las paginas leidas; conteo por agregacion nativa sobre comparacionDe/evidenciaDeFuente.`,
      perList.length === 1
        ? `ALCANCE SOLO-${perList[0]}: unico periodo cruzado ${JSON.stringify(perList[0])} en RDF; no extrapoles a otros periodos ni anos.`
        : perList.length
          ? `ALCANCE: periodos cruzados en RDF: ${perList.map(p => JSON.stringify(p)).join(', ')}; no extrapoles fuera de ellos.`
          : `ALCANCE: sin comparaciones municipales en RDF para ${alias}; periodos y medidas estan en la propia ficha (ver triples); no extrapoles.`,
      ...lines,
      ...sample.map(r => `- Comparacion ${JSON.stringify(r.cl ?? r.c)} <${r.c}> comparacionDe <${iri}>; periodoCruzado ${JSON.stringify(r.per ?? 'no declarado en RDF')}.`),
      ...evSample.map(r => `- Evidencia <${r.e}>: fuenteRol=${JSON.stringify(r.rol ?? '')} medidaOrigen=${JSON.stringify(r.medida ?? '')} nombreOrigen=${JSON.stringify(r.nombre ?? '')} fuenteOriginal=${JSON.stringify(r.fuente ?? '')} hoja=${JSON.stringify(r.hoja ?? '')} sha=${JSON.stringify(r.sha ?? '')} valor=${JSON.stringify(r.valor ?? '')}.`),
    );
  }
  if (!sections.length) return { context: '', anchors: [] };
  return { context: sections.join('\n'), anchors };
}

/** Evidencia por codigo municipal nombrado (p. ej. 26001).
 * El vecindario hop-1 trae el enlace evidenciaDeFuente pero nunca las
 * medidas de cada fuente (el nodo evidencia es ?s, no entra al frontier),
 * asi que la pregunta "muestra los dos valores con medida..." quedaba sin
 * respuesta aunque el grafo la tiene. Se resuelve por literal exacto
 * codigoTextual (5 digitos: no colisiona con anos) + detalle completo de
 * la comparacion y sus dos evidencias. Solo SELECT. */
const CODIGO_RE = /\b(\d{5})\b/g;

export function cruceCodigos(question: string): string[] {
  const out: string[] = [];
  for (const m of question.normalize('NFC').matchAll(CODIGO_RE)) {
    if (!out.includes(m[1])) out.push(m[1]);
  }
  return out.slice(0, 2);
}

export async function cruceCodigoContext(
  mcp: McpClient,
  question: string,
): Promise<{ context: string; anchors: Array<{ iri: string; label: string }> }> {
  const codigos = cruceCodigos(question);
  if (!codigos.length) return { context: '', anchors: [] };
  const sections: string[] = [];
  const anchors: Array<{ iri: string; label: string }> = [];
  for (const codigo of codigos) {
    // Solo el nodo comparacion (tiene periodoCruzado): las evidencias
    // tambien llevan codigoTextual y hay que excluirlas aqui.
    const comps = await selectAll(mcp, `${P}
      # codigo-comparacion
      SELECT DISTINCT ?c ?cl ?per WHERE {
        ?c <https://example.org/mex-ontologi/vocab/codigoTextual> ${JSON.stringify(codigo)} ;
           <https://example.org/mex-ontologi/vocab/periodoCruzado> ?per .
        OPTIONAL { ?c rdfs:label ?cl }
      } ORDER BY ?c ?per`);
    if (!comps.length) continue;
    for (const comp of comps.slice(0, 2)) {
      anchors.push({ iri: comp.c, label: comp.cl ?? `${codigo} — ${comp.per}` });
      const det = await selectAll(mcp, `${P}
        # codigo-detalle
        SELECT DISTINCT ?s ?sl ?p ?o ?ol WHERE {
          { VALUES ?s { <${comp.c}> } ?s ?p ?o . }
          UNION {
            ?e <https://example.org/mex-ontologi/vocab/evidenciaDeFuente> <${comp.c}> .
            ?e ?p ?o . BIND(?e AS ?s)
          }
          OPTIONAL { ?s rdfs:label ?sl }
          OPTIONAL { ?o rdfs:label ?ol }
          FILTER(!isBlank(?o) && !isBlank(?s))
        } ORDER BY ?s ?p ?o`);
      const compLines: string[] = [];
      const byFuente = new Map<string, string[]>();
      for (const r of det) {
        const s = r.sl ? `${JSON.stringify(r.sl)} <${r.s}>` : `<${r.s}>`;
        const o = isIri(r.o)
          ? r.ol
            ? `${JSON.stringify(r.ol)} <${r.o}>`
            : `<${r.o}>`
          : JSON.stringify(r.o);
        const line = `- ${s} --[<${r.p}>]--> ${o}`;
        if (r.s === comp.c) compLines.push(line);
        else {
          const rol = det.find(
            d => d.s === r.s && d.p === 'https://example.org/mex-ontologi/vocab/fuenteRol',
          )?.o;
          const key = rol ?? r.s;
          if (!byFuente.has(key)) byFuente.set(key, []);
          byFuente.get(key)!.push(line);
        }
      }
      const roles = [...byFuente.keys()];
      sections.push(
        `COMPLETE codigo ${codigo} <${comp.c}>: comparacion periodo ${JSON.stringify(comp.per ?? '')} y ${byFuente.size} evidencias de fuente (${roles.map(r => JSON.stringify(r)).join(', ') || 'sin rol'}). Todas las paginas leidas; detalle por codigoTextual exacto, sin extrapolar a otros codigos ni anos.`,
        `LIMITES: ver limiteInterpretativo de cada comparacion y evidencia en los triples; los codigos son literales coincidentes.`,
        ...compLines,
        ...[...byFuente.entries()].flatMap(([rol, ls]) => [
          `-- fuente ${JSON.stringify(rol)} (${ls.length} triples):`,
          ...ls,
        ]),
      );
    }
  }
  if (!sections.length) return { context: '', anchors: [] };
  return { context: sections.join('\n'), anchors };
}

/** Presupuesto de contexto por modelo: Gemma4 31B expone 16000
 * tokens/minuto y el contexto actual (47k-253k caracteres) provoca
 * 429 TPM. El ajuste es SOLO recorte por lineas completas del
 * Retrieved ya recuperado (SELECT identicos, grafo intacto):
 * - Resumenes COMPLETE (conteos nativos) y ficha F2: siempre integros.
 * - Resto: lineas completas por prioridad de intencion, sin cortar
 *   literales ni JSON por la mitad; repetidas exactas fuera.
 * Modelos no listados: sin recorte (Infinity), sin degradacion. */
export const GEMMA_TPM = 16000;
/** Pausa minima entre llamadas REALES al modelo (>=60s exigidos). */
export const GEMMA_PACING_MS = 65000;

export const MODEL_CONTEXT_BUDGETS: Array<{
  match: RegExp;
  maxInputTokens: number;
  pacingMs: number;
  note: string;
}> = [
  {
    match: /gemma-4-31b/i,
    maxInputTokens: 6500,
    pacingMs: GEMMA_PACING_MS,
    note: 'Gemma4 31B via proveedor 16000 TPM: medido 9845 est -> 14072 reales (x1.43) y 9607 est -> 14279 reales (x1.49); 6500 est ~= 9300 reales + 4096 salida < 16000 en ventana de 65s.',
  },
  {
    match: /gemma/i,
    maxInputTokens: 6500,
    pacingMs: GEMMA_PACING_MS,
    note: 'Familia Gemma en proveedor 16000 TPM: mismo presupuesto medido.',
  },
];

/** Configurable: overrideTokens gana; si no, tabla por modelo; si no,
 * Infinity (comportamiento original). Env ONTO_CTX_BUDGET_TOKENS opcional. */
export function budgetForModel(
  model?: string,
  overrideTokens?: number,
): { maxInputTokens: number; pacingMs: number } {
  const envRaw =
    typeof process !== 'undefined' ? process.env?.ONTO_CTX_BUDGET_TOKENS : undefined;
  const envTokens = envRaw != null && envRaw !== '' ? Number(envRaw) : NaN;
  if (Number.isFinite(overrideTokens as number))
    return { maxInputTokens: overrideTokens as number, pacingMs: GEMMA_PACING_MS };
  if (Number.isFinite(envTokens))
    return { maxInputTokens: envTokens, pacingMs: GEMMA_PACING_MS };
  for (const b of MODEL_CONTEXT_BUDGETS) {
    if (model && b.match.test(model))
      return { maxInputTokens: b.maxInputTokens, pacingMs: b.pacingMs };
  }
  return { maxInputTokens: Infinity, pacingMs: 0 };
}

/** ~4 caracteres por token con margen 1.15 (conservador p. es). */
export function estimateTokensFromChars(chars: number): number {
  return Math.ceil(Math.max(0, chars) / 4 * 1.15);
}

export function estimateInputTokens(args: {
  systemPrompt?: string;
  question: string;
  context: string;
}): number {
  const sys = args.systemPrompt ?? QA_SYSTEM_PROMPT;
  return estimateTokensFromChars(sys.length + args.question.length + args.context.length);
}

/** Pines de la pregunta: alias F, identificadores con _ y codigos
 * numericos (26001), en forma cruda y URL-encoded (el grafo encodes
 * ñ: a%C3%B1o_matrimonio). Solo especificos: los terminos genericos
 * (clave, medida, 2020...) ya tienen sus marcadores de prioridad.
 * Todo en minusculas para includes(). */
export function questionPins(question: string): string[] {
  const q = question.normalize('NFC');
  const pins = new Set<string>();
  for (const a of cruceAliases(q)) pins.add(a.toLowerCase());
  for (const m of q.matchAll(/[\p{L}\p{N}]+[_-][\p{L}\p{N}_-]+/gu)) {
    const raw = m[0].toLowerCase();
    pins.add(raw);
    pins.add(encodeURIComponent(raw).toLowerCase());
  }
  for (const m of q.matchAll(/\b\d{4,6}\b/g)) pins.add(m[0]);
  return [...pins];
}

/** Intencion de definicion: la pregunta pide significado/diccionario o
 * distingue documentado de candidato. Su backbone (definicionOriginal,
 * significadoDocumentado, definicionVariable) sube a rango de pin. */
export function wantsDefinitions(question: string): boolean {
  return /significa|definici|diccionario|documentad|candidat/i.test(question.normalize('NFC'));
}

const BONUS_DEFINICION = ['definicionoriginal', 'significadodocumentado', 'definicionvariable', 'diccionariocsv'];

const PRIORITY_MARKERS = [
  'documental_revisada',
  'definicionoriginal',
  'significadodocumentado',
  'definicionvariable',
  'diccionario',
  'comparacionde',
  'evidenciadefuente',
  'igualdadvalores',
  'medidaorigen',
  'nombreorigen',
  'fuenteoriginal',
  'hojafuente',
  'filaorigen',
  'shafuente',
  'valororigen',
  'periodocruzado',
  'codigotextual',
  'condicionpendiente',
  'condicionverificada',
  'limiteinterpretativo',
  'candidata_por_nombre',
];

/** Recorte por lineas completas: COMPLETE siempre, luego pines,
 * luego prioridad, luego resto en orden; repetidas exactas fuera.
 * Nunca corta una linea por la mitad. */
function trimSectionLines(
  lines: string[],
  capChars: number,
  pins: string[],
  bonus: string[] = [],
  reserveChars = 0,
): { kept: string[]; dropped: number } {
  const seen = new Set<string>();
  const uniq: string[] = [];
  for (const l of lines) {
    if (!l.trim() || seen.has(l)) continue;
    seen.add(l);
    uniq.push(l);
  }
  const low = uniq.map(l => l.toLowerCase());
  const isComplete = uniq.map(l => l.startsWith('COMPLETE'));
  const norm = (s: string) => s.replace(/[^a-z0-9]/g, '');
  const lowNorm = low.map(norm);
  const hasAny = (i: number, words: string[]) => words.some(w => w && lowNorm[i].includes(norm(w)));
  const isPin = low.map(l => pins.some(p => p && l.includes(p)));
  const isBonus = low.map((_, i) => hasAny(i, bonus));
  const isMapping = uniq.map(l => l.startsWith('Mapping '));
  const isPriority = low.map((_, i) => PRIORITY_MARKERS.some(m => lowNorm[i].includes(m)));
  const rankOf = (i: number): number =>
    isComplete[i] ? 0 : isPin[i] && isMapping[i] ? 1 : isBonus[i] ? 2 : isPin[i] ? 3 : isPriority[i] ? 4 : 5;
  const order = uniq
    .map((_, i) => i)
    .sort((a, b) => {
      // COMPLETE (resumen exacto) > mapping revisado pineado > definicion
      // pedida > resto pineado > prioridad > resto. Sin cortar lineas.
      // (Solo 'Mapping ' en rango 1: las evidencias con documental_revisada
      // son muchas y taparian definiciones y anos 2022.)
      return rankOf(a) - rankOf(b) || a - b;
    });
  const kept: string[] = [];
  let used = 0;
  let dropped = 0;
  // Reserva para definiciones y evidencia del periodo: los mappings son
  // ejemplos PARTIAL (conteos COMPLETE ya exactos); lo solicitado
  // (definicion, periodo) no puede quedarse sin hueco.
  const tier1Cap = Math.max(0, capChars - reserveChars);
  for (const i of order) {
    const r = rankOf(i);
    const limit = r <= 1 ? tier1Cap : capChars;
    // COMPLETE (resumen numerico exacto) nunca se recorta.
    if (r !== 0 && used + uniq[i].length + 1 > limit) {
      dropped++;
      continue;
    }
    kept.push(uniq[i]);
    used += uniq[i].length + 1;
  }
  // Orden original para contexto legible y estable.
  kept.sort((a, b) => uniq.indexOf(a) - uniq.indexOf(b));
  return { kept, dropped };
}

export interface FitReport {
  model: string;
  maxInputTokens: number;
  estInputTokens: number;
  contextChars: number;
  trimmed: boolean;
  keptLines: number;
  droppedLines: number;
  note?: string;
}

/** Ajusta un Retrieved al presupuesto del modelo. Sin modelo listado:
 * devuelve el original intacto (misma referencia). */
export function fitRetrieved(
  r: Retrieved,
  question: string,
  model?: string,
  systemPrompt: string = QA_SYSTEM_PROMPT,
): { fitted: Retrieved; report: FitReport } {
  const budget = budgetForModel(model);
  const fullLen = asContext(r).length;
  const base = {
    model: model ?? '',
    maxInputTokens: budget.maxInputTokens,
    estInputTokens: estimateTokensFromChars(systemPrompt.length + question.length + fullLen),
    contextChars: fullLen,
    trimmed: false,
    keptLines: 0,
    droppedLines: 0,
  };
  if (!Number.isFinite(budget.maxInputTokens)) return { fitted: r, report: base };
  // Holgura de 100 tokens: la estimacion es aproximada y el tope es duro.
  const target = budget.maxInputTokens - 100;
  if (base.estInputTokens <= target) return { fitted: r, report: base };
  const maxCtxChars =
    Math.floor((target * 4) / 1.15) - systemPrompt.length - question.length;
  const fixedChars =
    (r.correspondenceOverview ?? '').length +
    (r.cruceFichaContext ?? '').length +
    (r.cruceCodigoContext ?? '').length +
    (r.variableOverview ?? '').length +
    r.anchors.map(a => a.label.length + a.iri.length + 4).reduce((x, y) => x + y, 0) +
    r.claims.map(c => c.text.length + c.doc.length + 6).reduce((x, y) => x + y, 0) +
    r.provenance.map(p => p.thing.length + p.sources.join('').length + 4).reduce((x, y) => x + y, 0) +
    r.conflicts.join('').length +
    700; // cabeceras de asContext
  const remaining = Math.max(0, maxCtxChars - fixedChars);
  const pins = questionPins(question);
  const bonus = wantsDefinitions(question) ? BONUS_DEFINICION : [];
  // Codigo nombrado sin variable: las correspondencias genericas son ruido;
  // conservar solo sus conteos COMPLETE y dar el resto al vecindario.
  const hasVarId = /[\p{L}\p{N}]+[_-][\p{L}\p{N}_-]+/u.test(question.normalize('NFC'));
  const corrMinimal = cruceCodigos(question).length > 0 && !hasVarId;
  const corrLines = (r.correspondenceContext ?? '').split('\n');
  const resLines = (r.resourceContext ?? '').split('\n');
  // Reparto: lo scoped-COMPLETE (conteos+mappings+definiciones) manda
  // sobre el vecindario (ya declarado PARTIAL). 80/10/resto. Reserva 3000
  // en correspondencias para definiciones y evidencia del periodo: los
  // mappings son ejemplos PARTIAL y no pueden taparlos.
  const corrCap = corrMinimal ? 0 : Math.floor(remaining * 0.8);
  const resCap = Math.floor(remaining * 0.1);
  const corr = r.correspondenceContext
    ? corrMinimal
      ? {
          // Codigo nombrado sin variable: las correspondencias genericas son
          // ruido; solo sus conteos COMPLETE, el resto al vecindario/ codigo.
          kept: corrLines.filter(l => l.startsWith('COMPLETE')),
          dropped: corrLines.length - corrLines.filter(l => l.startsWith('COMPLETE')).length,
        }
      : trimSectionLines(corrLines, corrCap, pins, bonus, 3000)
    : { kept: [] as string[], dropped: 0 };
  const res = r.resourceContext
    ? trimSectionLines(resLines, resCap, pins, bonus)
    : { kept: [] as string[], dropped: 0 };
  const usedSmall =
    corr.kept.join('').length + res.kept.join('').length + corr.kept.length + res.kept.length;
  const factsCap = Math.max(0, remaining - usedSmall);
  const factTrim = trimSectionLines(r.facts, factsCap, pins, bonus);
  // ponytail: garantia minima — si hay pines (26001, variable) y el recorte
  // los elimino todos, se reponen hasta 12 (se reporta sobre-presupuesto).
  let factKept = factTrim.kept;
  let overPins = 0;
  if (pins.length && r.facts.some(f => pins.some(p => p && f.toLowerCase().includes(p)))) {
    const hasPin = factKept.some(f => pins.some(p => p && f.toLowerCase().includes(p)));
    if (!hasPin) {
      const seen = new Set(factKept);
      const add = r.facts.filter(f => pins.some(p => p && f.toLowerCase().includes(p)) && !seen.has(f));
      factKept = [...add.slice(0, 12), ...factKept];
      overPins = add.slice(0, 12).join('').length;
    }
  }
  const noteParts: string[] = [];
  if (corr.dropped) noteParts.push(`correspondencias ${corr.kept.length}/${corrLines.length}`);
  if (res.dropped) noteParts.push(`recursos ${res.kept.length}/${resLines.length}`);
  if (factTrim.dropped) noteParts.push(`vecindario ${factKept.length}/${r.facts.length}`);
  const fitted: Retrieved = {
    ...r,
    correspondenceContext: corr.kept.length
      ? corr.kept.join('\n') +
        (corr.dropped
          ? `\nBUDGET TRIM (${model}): ${corr.kept.length}/${corrLines.length} lineas; conteos COMPLETE intactos, ejemplos ahora PARTIAL.`
          : '')
      : r.correspondenceContext ?? '',
    resourceContext: res.kept.length
      ? res.kept.join('\n') +
        (res.dropped ? `\nBUDGET TRIM (${model}): ejemplos ahora PARTIAL.` : '')
      : r.resourceContext,
    facts: factKept,
  };
  // Si el recorte vacio una seccion con contenido, conservar una nota honesta.
  if (r.correspondenceContext && !corr.kept.length && !fitted.correspondenceContext) {
    fitted.correspondenceContext =
      'BUDGET TRIM: correspondencias fuera de presupuesto; ver resumen global si se pidio.';
  }
  const fittedLen = asContext(fitted).length;
  return {
    fitted,
    report: {
      model: model ?? '',
      maxInputTokens: budget.maxInputTokens,
      estInputTokens: estimateTokensFromChars(systemPrompt.length + question.length + fittedLen + overPins),
      contextChars: fittedLen,
      trimmed: true,
      keptLines: corr.kept.length + res.kept.length + factKept.length,
      droppedLines: corr.dropped + res.dropped + factTrim.dropped,
      note: `BUDGET TRIM (${model}): ${noteParts.join('; ') || 'sin recorte necesario'}. ` +
        `Conteos COMPLETE y ficha integros; recorte por lineas completas, sin truncar literales.${overPins ? ' Pines repuestos sobre presupuesto.' : ''}`,
    },
  };
}

/** Aplica el presupuesto solo cuando el modelo lo exige; si no, intacto. */
export function maybeFit(
  ret: Retrieved,
  question: string,
  model?: string,
  systemPrompt: string = QA_SYSTEM_PROMPT,
): Retrieved {
  if (!model) return ret;
  if (!Number.isFinite(budgetForModel(model).maxInputTokens)) return ret;
  return fitRetrieved(ret, question, model, systemPrompt).fitted;
}

/** Read every result page; page size is not a cap on the answer set. */
async function selectAll(mcp: McpClient, query: string): Promise<Array<Record<string, string>>> {
  const rows: Array<Record<string, string>> = [];
  for (let offset = 0; ; offset += 200) {
    const page = await select(mcp, `${query}\nLIMIT 200 OFFSET ${offset}`);
    rows.push(...page);
    if (page.length < 200) return rows;
  }
}

function fact(r: Record<string, string>): string {
  const s = r.sl ? `${JSON.stringify(r.sl)} <${r.s}>` : `<${r.s}>`;
  const o = isIri(r.o) ? (r.ol ? `${JSON.stringify(r.ol)} <${r.o}>` : `<${r.o}>`) : JSON.stringify(r.o);
  return `${s} --[<${r.p}>]--> ${o}`;
}

/** Qualified mappings point INTO variables. Retrieve them independently of
 * anchor/neighbourhood budgets, then separate exhaustive counts from examples.
 * Discover the vocabulary namespace instead of assuming a project base IRI.
 */
export async function correspondenceContext(mcp: McpClient, names: string[]): Promise<string> {
  if (!names.length) return '';
  const variables = await selectAll(mcp, `${P}
    # correspondence-variables
    SELECT DISTINCT ?variable ?name ?namePredicate WHERE {
      ?variable ?namePredicate ?name .
      FILTER(REGEX(STR(?namePredicate), "[/#]nombreVariableLocal$"))
      FILTER(LCASE(STR(?name)) IN (${names.map(n => JSON.stringify(n)).join(', ')}))
    } ORDER BY ?variable ?name ?namePredicate`);
  if (!variables.length) return '';
  const namespaces = [...new Set(variables.map(v => v.namePredicate.slice(0, -'nombreVariableLocal'.length)))];
  const sections: string[] = [];
  for (const ns of namespaces) {
    if (!isIri(ns + 'variableDestino')) throw new Error('Invalid correspondence vocabulary IRI');
    const matched = variables.filter(v => v.namePredicate === ns + 'nombreVariableLocal');
    const ids = iriValues(matched.map(v => v.variable));
    const rows = await selectAll(mcp, `${P}
      # correspondence-records
      SELECT DISTINCT ?mapping ?variable ?column ?status WHERE {
        VALUES ?variable { ${ids} }
        ?mapping <${ns}variableDestino> ?variable ; <${ns}columnaOrigen> ?column ; <${ns}estadoCorrespondencia> ?status .
      } ORDER BY ?variable ?mapping ?column ?status`);
    for (const v of matched) {
      const counts = new Map<string, Set<string>>();
      for (const row of rows.filter(r => r.variable === v.variable)) {
        if (!counts.has(row.status)) counts.set(row.status, new Set());
        counts.get(row.status)!.add(row.mapping);
      }
      sections.push(`COMPLETE correspondence status counts for ${JSON.stringify(v.name)} <${v.variable}>: ${JSON.stringify(Object.fromEntries([...counts].map(([status, mappings]) => [status, mappings.size])))}. All result pages were read; this is scoped to this variable, not the entire graph.`);
    }
    // Bound model context, not graph search. Reviewed evidence comes first.
    const shown = [...rows].sort((a, b) => Number(b.status === 'documental_revisada') - Number(a.status === 'documental_revisada') || a.mapping.localeCompare(b.mapping)).slice(0, 80);
    sections.push(`Correspondence examples shown: ${shown.length}/${rows.length}; examples are ${shown.length === rows.length ? 'complete' : 'PARTIAL'}. Counts above include every status, including records not shown.`);
    sections.push(...shown.map(r => `Mapping <${r.mapping}>: variable <${r.variable}>; column <${r.column}>; estadoCorrespondencia=${JSON.stringify(r.status)}.`));
    const nodes = [...matched.map(v => v.variable), ...shown.filter(r => r.status === 'documental_revisada').map(r => r.mapping)];
    const evidence = await selectAll(mcp, `${P}
      # correspondence-evidence
      SELECT DISTINCT ?s ?sl ?p ?o ?ol WHERE {
        { VALUES ?s { ${iriValues(nodes)} } ?s ?p ?o }
        UNION {
          VALUES ?variable { ${ids} }
          ?variable <${ns}definicionOriginal> ?s . ?s ?p ?o .
        }
        UNION {
          VALUES ?s { ${iriValues(shown.map(r => r.column))} }
          VALUES ?p { rdfs:label prov:wasDerivedFrom <http://purl.org/dc/terms/isPartOf> <${ns}significadoDocumentado> }
          ?s ?p ?o .
        }
        OPTIONAL { ?s rdfs:label ?sl }
        OPTIONAL { ?o rdfs:label ?ol }
        FILTER(!isBlank(?s) && !isBlank(?o))
      } ORDER BY ?s ?p ?o ?sl ?ol`);
    sections.push('CORRESPONDENCE AND ORIGINAL DICTIONARY EVIDENCE', ...evidence.map(fact));
  }
  return sections.join('\n');
}

/** Questions about counts, states or listings need COMPLETE scoped queries,
 * not the bounded neighbourhood. Intent is keyword-based and deterministic;
 * generic questions without a named variable still trigger the overview.
 */
const OVERVIEW_HINTS = /correspondencia|mapeo|estado|conteo|conteos|total|totales|cuánt|cuant|lista|listado|revisad|candidat|ambigu|distribu/i;
const YEAR_HINT = /\b(19|20)\d{2}\b/;
/** Generic correspondence words never identify a resource on their own. */
const RESOURCE_GENERIC = new Set([
  'correspondencia', 'correspondencias', 'mapeo', 'mapeos', 'mapping',
  'estado', 'estados', 'conteo', 'conteos', 'total', 'totales', 'lista',
  'listado', 'columna', 'columnas', 'variable', 'variables', 'grafo',
  'evidencia', 'procedencia', 'registra', 'registro', 'semantica',
  'semanticas', 'semántica', 'semánticas', 'recurso', 'recursos',
  'revisada', 'revisadas', 'revisado', 'revisados',
  'candidata', 'candidatas', 'candidato', 'candidatos',
  'ambigua', 'ambiguas', 'ambiguo', 'ambiguos',
  'tiene', 'tienen', 'cuantas', 'cuántas', 'cuantos', 'cuántos',
  'cuales', 'cuáles', 'donde', 'dónde', 'dime', 'significa',
  'estan', 'están', 'consulta', 'consultar', 'corregir', 'editar',
  'describir', 'detallar', 'indicar', 'explicar', 'comparar', 'compara',
]);

export function wantsCorrespondenceOverview(question: string): boolean {
  return OVERVIEW_HINTS.test(question.normalize('NFC'));
}

export function wantsResourceScope(question: string): boolean {
  const q = question.normalize('NFC');
  return wantsCorrespondenceOverview(q) && (YEAR_HINT.test(q) || /\brecurso\b/i.test(q));
}

export function wantsVariableOverview(question: string): boolean {
  const q = question.normalize('NFC').toLowerCase();
  return q.includes('variable') && (q.includes('estado') || q.includes('conteo') || q.includes('total') || q.includes('cuánt') || q.includes('cuant'));
}

/** Global state counts via native aggregation: one row per state, no paging
 * cap on the answer. Predicate-agnostic (discovers estadoCorrespondencia by
 * suffix) so vocabulary moves do not silently zero the counts.
 */
export async function correspondenceStatusOverview(mcp: McpClient): Promise<string> {
  const rows = await selectAll(mcp, `${P}
    # correspondence-status-overview
    SELECT ?status (COUNT(DISTINCT ?mapping) AS ?n) WHERE {
      ?mapping ?p ?status .
      FILTER(REGEX(STR(?p), "[/#]estadoCorrespondencia$"))
    } GROUP BY ?status ORDER BY ?status`);
  if (!rows.length) return 'COMPLETE global correspondence state counts: {} (no mappings carry estadoCorrespondencia; scoped zero, not a claim about other predicates).';
  const counts = Object.fromEntries(rows.map(r => [r.status, Number(r.n)]));
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return `COMPLETE global correspondence state counts (native aggregation over every mapping): ${JSON.stringify(counts)}. Total ${total}. Scoped to estadoCorrespondencia across the whole graph; per-variable or neighbourhood counts never substitute for these.`;
}

/** Variable-level states are a different tally from mapping states. */
export async function variableStatusOverview(mcp: McpClient): Promise<string> {
  const rows = await selectAll(mcp, `${P}
    # variable-status-overview
    SELECT ?status (COUNT(DISTINCT ?variable) AS ?n) WHERE {
      ?variable ?p ?status .
      FILTER(REGEX(STR(?p), "[/#]estadoSemantico$"))
    } GROUP BY ?status ORDER BY ?status`);
  if (!rows.length) return 'COMPLETE variable state counts: {} (no variables carry estadoSemantico; scoped zero).';
  const counts = Object.fromEntries(rows.map(r => [r.status, Number(r.n)]));
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return `COMPLETE variable state counts (native aggregation over every variable): ${JSON.stringify(counts)}. Total ${total}. This is the variable's estadoSemantico, not the mapping's estadoCorrespondencia; the two tallies must never be merged.`;
}

/** Vocabulary predicates discovered by local-name suffix, never hardcoded. */
async function discoverVocab(mcp: McpClient, names: string[]): Promise<Map<string, string>> {
  const alt = names.join('|');
  const rows = await selectAll(mcp, `${P}
    # correspondence-vocab
    SELECT DISTINCT ?pred WHERE {
      ?s ?pred ?o .
      FILTER(REGEX(STR(?pred), "[/#](${alt})$"))
    }`);
  const map = new Map<string, string>();
  for (const r of rows) {
    for (const n of names) {
      if (r.pred.endsWith('/' + n) || r.pred.endsWith('#' + n)) map.set(n, r.pred);
    }
  }
  return map;
}

/** Singular/plural variants so «matrimonio» matches «Matrimonios» and back. */
export function keywordVariants(kw: string): string[] {
  const out = [kw];
  if (kw.endsWith('es') && kw.length > 5) out.push(kw.slice(0, -2));
  else if (kw.endsWith('s') && kw.length > 4) out.push(kw.slice(0, -1));
  return [...new Set(out)];
}

/** Identifying keywords: long, non-generic, non-numeric question terms. */
export function resourceKeywords(question: string): string[] {
  return terms(question.normalize('NFC'))
    .filter(t => t.length >= 5 && !RESOURCE_GENERIC.has(t.toLowerCase()) && !/^\d+$/.test(t))
    .slice(0, 3);
}

/** Years are filters on the resource's declared period, never mere substrings. */
export function questionYears(question: string): string[] {
  return [...new Set([...question.normalize('NFC').matchAll(/\b((?:19|20)\d{2})\b/g)].map(m => m[1]))].slice(0, 4);
}

/** An explicit year interval in the question (1990–2040, entre 1990 y 2040). */
export function questionRange(question: string): { from: number; to: number } | null {
  const q = question.normalize('NFC');
  const between = q.match(/entre\s+((?:19|20)\d{2})\s+y\s+((?:19|20)\d{2})/i);
  const dash = q.match(/((?:19|20)\d{2})\s*[–—-]\s*((?:19|20)\d{2})/);
  const m = between ?? dash;
  if (!m) return null;
  const a = Number(m[1]), b = Number(m[2]);
  return { from: Math.min(a, b), to: Math.max(a, b) };
}

function delimitedYearPattern(y: string): string {
  return `(^|[^0-9])${y}`;
}

/** Coarse SPARQL pre-filter (recall side only): a delimited year in the label
 * or after a non-digit in the declared period. The strict decision happens in
 * TypeScript below, so "20220" can pass the pre-filter but never match 2022.
 */
function yearPrefilter(years: string[]): string {
  if (!years.length) return '';
  const ors = years.flatMap(y => [
    `REGEX(STR(?label), ${JSON.stringify(delimitedYearPattern(y))})`,
    `REGEX(STR(?ini), ${JSON.stringify(delimitedYearPattern(y))})`,
    `REGEX(STR(?fin), ${JSON.stringify(delimitedYearPattern(y))})`,
  ]);
  return ` && (${ors.join(' || ')})`;
}

function keywordFilter(variants: string[][]): string {
  return variants
    .map(vs => `(${vs.map(k => `CONTAINS(LCASE(STR(?label)), ${JSON.stringify(k.toLowerCase())})`).join(' || ')})`)
    .join(' && ');
}

function parseYearPrefix(value: string | undefined): number | null {
  const m = value?.match(/^((?:19|20)\d{2})/);
  return m ? Number(m[1]) : null;
}

function labelYears(label: string): number[] {
  return [...label.matchAll(/(?:^|[^0-9])((?:19|20)\d{2})(?![0-9])/g)].map(m => Number(m[1]));
}

export interface ResourceYearVerdict {
  match: boolean;
  rule: 'declared-period' | 'label-fallback';
  matchedYears: number[];
  note?: string;
}

/**
 * Strict year decision in TypeScript: the declared period wins whenever it is
 * interpretable; the label is only a bounded fallback. A label year outside
 * the declared period is reported as a contradiction, never as a match.
 * Intervals match by declared-range overlap and never assert observed
 * coverage of any single year inside the range.
 */
export function strictYearVerdict(
  label: string,
  ini: string | undefined,
  fin: string | undefined,
  years: string[],
  range: { from: number; to: number } | null,
): ResourceYearVerdict {
  const iniY = parseYearPrefix(ini);
  const finY = parseYearPrefix(fin);
  const ly = labelYears(label);
  if (iniY != null || finY != null) {
    const start = iniY ?? finY as number;
    const end = finY ?? iniY as number;
    const contradicted = ly.filter(y => y < start || y > end);
    const contraNote = contradicted.length
      ? ` Label year(s) ${contradicted.join(', ')} outside declared period ${start}–${end}; period takes precedence.`
      : '';
    if (range) {
      const overlap = start <= range.to && end >= range.from;
      return {
        match: overlap,
        rule: 'declared-period',
        matchedYears: overlap ? [Math.max(start, range.from), Math.min(end, range.to)] : [],
        note: `Question asks declared range ${range.from}–${range.to}: matched by declared-period overlap, not observed coverage of any single year.${contraNote}`,
      };
    }
    const matched = years.map(Number).filter(y => y >= start && y <= end);
    return {
      match: matched.length > 0,
      rule: 'declared-period',
      matchedYears: matched,
      note: contraNote ? contraNote.trim() : undefined,
    };
  }
  if (range) {
    const matched = [range.from, range.to].filter(y => ly.includes(y));
    return {
      match: matched.length > 0,
      rule: 'label-fallback',
      matchedYears: matched,
      note: `No interpretable declared period; label fallback for range endpoints only, not observed coverage.`,
    };
  }
  const wanted = years.map(Number);
  const matched = wanted.filter(y => ly.includes(y));
  return { match: matched.length > 0, rule: 'label-fallback', matchedYears: matched };
}

/**
 * Resource-scoped listing over REAL resolved resources, never over bare
 * label substrings. Resolution: RecursoCatalogado nodes whose label matches
 * the identifying keywords, narrowed by year through the declared period
 * (inicioDeclarado/finDeclarado, label match only as fallback). Columns come
 * from the resource→esquema→columna path; mappings aggregate with
 * COUNT(DISTINCT ?mapping) so predicate aliases cannot double-count.
 *
 * COMPLETE is claimed only for an explicit resolved-IRI set with all pages
 * read. Anything else is UNRESOLVED (candidates listed, no counts) or PARTIAL
 * (missing vocabulary path), and never a zero claim about the graph.
 */
export async function resourceCorrespondenceContext(mcp: McpClient, question: string): Promise<string> {
  const keywords = resourceKeywords(question);
  const years = questionYears(question);
  if (!keywords.length && !years.length) return '';
  const vocab = await discoverVocab(mcp, ['estadoCorrespondencia', 'columnaOrigen', 'esquema', 'columna', 'inicioDeclarado', 'finDeclarado']);
  for (const need of ['estadoCorrespondencia', 'columnaOrigen', 'esquema', 'columna']) {
    if (!vocab.get(need)) return `Resource listing PARTIAL: vocabulary predicate ${need} not found; no resource scope computed and no absence claimed.`;
  }
  const ini = vocab.get('inicioDeclarado'), fin = vocab.get('finDeclarado');
  const period = (ini && fin)
    ? `OPTIONAL { ?resource <${ini}> ?ini } OPTIONAL { ?resource <${fin}> ?fin }`
    : `OPTIONAL { BIND("" AS ?ini) } OPTIONAL { BIND("" AS ?fin) }`;
  const variants = keywords.map(keywordVariants);
  const range = questionRange(question);
  const preYears = [...years, ...(range ? [String(range.from), String(range.to)] : [])];
  interface Candidate { iri: string; label: string; ini?: string; fin?: string }
  const fetchCandidates = async (andAll: boolean): Promise<Candidate[]> => {
    const parts = andAll ? [keywordFilter(variants)] : variants.map(vs => `(${keywordFilter([vs])})`);
    const kwFilter = parts.length ? `FILTER(${andAll ? parts[0] : `(${parts.join(' || ')})`}${yearPrefilter(preYears)})` : (preYears.length ? `FILTER(${yearPrefilter(preYears).slice(4)})` : '');
    const rows = await selectAll(mcp, `${P}
    # resource-resolve
    SELECT DISTINCT ?resource ?label ?ini ?fin WHERE {
      ?resource a ?rtype ; rdfs:label ?label .
      FILTER(REGEX(STR(?rtype), "[/#]RecursoCatalogado$"))
      ${period}
      ${kwFilter}
    } ORDER BY ?resource ?label ?ini ?fin`);
    return rows.map(r => ({ iri: r.resource, label: r.label, ini: r.ini, fin: r.fin }));
  };
  interface Decided { iri: string; labels: string[]; ini?: string; fin?: string; verdict: ResourceYearVerdict }
  const decide = (cands: Candidate[]): Decided[] => {
    const byIri = new Map<string, Decided>();
    for (const c of cands) {
      const verdict = strictYearVerdict(c.label, c.ini, c.fin, years, range);
      if (!verdict.match) continue;
      const known = byIri.get(c.iri);
      if (known) {
        if (!known.labels.includes(c.label)) known.labels.push(c.label);
      } else {
        byIri.set(c.iri, { iri: c.iri, labels: [c.label], ini: c.ini, fin: c.fin, verdict });
      }
    }
    return [...byIri.values()];
  };
  let decided = decide(await fetchCandidates(true));
  let multi = false;
  if (!decided.length && variants.length > 1) {
    decided = decide(await fetchCandidates(false));
    multi = decided.length > 0;
  }
  if (!decided.length) {
    const cands = await selectAll(mcp, `${P}
    # resource-candidates
    SELECT DISTINCT ?label WHERE {
      ?resource a ?rtype ; rdfs:label ?label .
      FILTER(REGEX(STR(?rtype), "[/#]RecursoCatalogado$"))
      ${keywords.length ? `FILTER(${keywordFilter(variants)})` : ''}
    } ORDER BY ?label LIMIT 10`);
    const shown = cands.map(c => JSON.stringify(c.label)).join(', ') || 'none';
    return `Resource scope UNRESOLVED for keywords ${JSON.stringify(keywords)}${years.length ? ` and years ${JSON.stringify(years)}` : ''}${range ? ` and range ${range.from}–${range.to}` : ''}: no catalogued resource matched under the strict year rule (delimited years; declared period first, so a label like 20220 never matches 2022). Similar labels: ${shown}. No counts computed and no zero claimed for any unresolved resource.`;
  }
  const scopeName = decided.map(r => r.labels.map(l => JSON.stringify(l)).join('/')).join(', ');
  const rids = iriValues(decided.map(r => r.iri));
  const columns = await selectAll(mcp, `${P}
    # resource-columns
    SELECT DISTINCT ?resource ?column WHERE {
      VALUES ?resource { ${rids} }
      ?resource <${vocab.get('esquema')}>/<${vocab.get('columna')}> ?column .
    } ORDER BY ?resource ?column`);
  if (!columns.length) {
    return `Resource scope PARTIAL for resolved ${scopeName}: no esquema/columna triples observed; the source files may contain columns not observed in the graph. Mapping counts not computed and no absence of mappings claimed.`;
  }
  const path = `VALUES ?resource { ${rids} } ?resource <${vocab.get('esquema')}>/<${vocab.get('columna')}> ?column .`;
  const counts = await selectAll(mcp, `${P}
    # resource-status-counts
    SELECT ?resource ?status (COUNT(DISTINCT ?mapping) AS ?num) WHERE {
      ${path}
      ?mapping <${vocab.get('columnaOrigen')}> ?column ; <${vocab.get('estadoCorrespondencia')}> ?status .
    } GROUP BY ?resource ?status ORDER BY ?resource ?status`);
  const labels = await selectAll(mcp, `${P}
    # resource-labels
    SELECT DISTINCT ?resource ?label WHERE {
      VALUES ?resource { ${rids} }
      ?resource rdfs:label ?label .
    } ORDER BY ?resource ?label`);
  const labelByIri = new Map<string, string[]>();
  for (const r of labels) {
    const known = labelByIri.get(r.resource) ?? [];
    if (!known.includes(r.label)) known.push(r.label);
    labelByIri.set(r.resource, known);
  }
  const byIri = new Map<string, { states: Record<string, number> }>();
  for (const r of counts) {
    if (!byIri.has(r.resource)) byIri.set(r.resource, { states: {} });
    byIri.get(r.resource)!.states[r.status] = Number(r.num);
  }
  const grandRows = await selectAll(mcp, `${P}
    # resource-grand-total
    SELECT (COUNT(DISTINCT ?mapping) AS ?num) WHERE {
      ${path}
      ?mapping <${vocab.get('columnaOrigen')}> ?column .
    }`);
  const grandTotal = Number(grandRows[0]?.num ?? 0);
  const detail = await selectAll(mcp, `${P}
    # resource-mapping-rows
    SELECT DISTINCT ?resource ?mapping ?column ?label ?status WHERE {
      ${path}
      ?mapping <${vocab.get('columnaOrigen')}> ?column ; <${vocab.get('estadoCorrespondencia')}> ?status .
      OPTIONAL { ?column rdfs:label ?label }
    } ORDER BY ?resource ?mapping ?column ?label ?status`);
  const perResource = [...byIri.entries()].map(([iri, e]) => {
    const lbs = (labelByIri.get(iri) ?? []).map(l => JSON.stringify(l)).join('/');
    return `Resource <${iri}> ${lbs || '(label missing)'}: ${JSON.stringify(e.states)}`;
  }).join(' | ');
  const notes = decided.map(d => d.verdict.note ? `Note for <${d.iri}>: ${d.verdict.note}` : '').filter(Boolean);
  const shown = [...detail].sort((a, b) => Number(b.status === 'documental_revisada') - Number(a.status === 'documental_revisada') || a.mapping.localeCompare(b.mapping)).slice(0, 80);
  const out = [
    `COMPLETE correspondence counts for resolved resource${decided.length > 1 ? 's' : ''} (${scopeName})${multi ? '; multi-resource OR fallback' : ''}: ${perResource || '{}'}. Grand total ${grandTotal} distinct mappings across ${columns.length} observed columns and ${decided.length} resolved resources; all result pages were read. Observed columns triangulated via resource→esquema→columna only; not a claim about the full content of the original source files.`,
    `Correspondence examples shown: ${shown.length}/${detail.length}; examples are ${shown.length === detail.length ? 'complete' : 'PARTIAL'}. Counts above include every status, including records not shown.`,
    ...notes,
    ...shown.map(r => `Mapping <${r.mapping}>: column <${r.column}>${r.label ? ` ${JSON.stringify(r.label)}` : ''}; estadoCorrespondencia=${JSON.stringify(r.status)}; resource <${r.resource}>.`),
  ];
  return out.join('\n');
}

function termValue(term: unknown): string {
  if (typeof term === 'object' && term !== null && 'value' in term && typeof term.value === 'string') return term.value;
  if (typeof term !== 'string') throw new Error('Invalid RDF term returned by onto_query');
  if (term.startsWith('<') && term.endsWith('>')) return term.slice(1, -1);
  const literal = term.match(/^("(?:[^"\\]|\\.)*")(?:@[\w-]+|\^\^<[^>]*>)?$/s);
  return literal ? JSON.parse(literal[1]) : term;
}

export function queryRows(raw: string): Array<Record<string, string>> {
  const parsed = JSON.parse(raw);
  if (parsed.error) throw new Error(`Graph query failed: ${typeof parsed.error === 'string' ? parsed.error : JSON.stringify(parsed.error)}`);
  const rows = Array.isArray(parsed.results) ? parsed.results : parsed.results?.bindings;
  if (!Array.isArray(rows)) throw new Error('onto_query returned no SPARQL result rows');
  return rows.map((row: Record<string, unknown>) => Object.fromEntries(
    Object.entries(row).filter(([, value]) => value != null).map(([key, value]) => [key, termValue(value)]),
  ));
}

async function select(mcp: McpClient, sparql: string): Promise<Array<Record<string, string>>> {
  // Query errors must reach the chat, not masquerade as an empty graph.
  return queryRows(await mcp.callTool('onto_query', { query: sparql }));
}

function isIri(value: string): boolean {
  return /^[a-z][a-z0-9+.-]*:/i.test(value) && !/[<>"{}|^`\\\s\u0000-\u001f]/u.test(value);
}

function iriValues(iris: string[]): string {
  if (iris.some(iri => !isIri(iri))) throw new Error('Graph query returned an invalid entity IRI');
  return [...new Set(iris)].map(iri => `<${iri}>`).join(' ');
}

/** Terms worth anchoring on: long enough to be discriminating, not stopwords. */
const SPANISH_STOP = new Set(('qué que cuál cual cuáles cuales cómo como dónde donde quién quien cuándo cuando por para del los las una unos unas este esta estos estas eso esa esos esas sobre según segun significa significado consulta consultar grafo muestra mostrar evidencia favor puede puedes podría podria información informacion brevemente responde saluda español modifiques datos variable').split(' '));

export function terms(question: string): string[] {
  const words = question.normalize('NFC').toLowerCase().match(/[\p{L}\p{N}][\p{L}\p{N}_-]{2,}/gu) ?? [];
  const unique = [...new Set(words.filter(word => !STOP.has(word) && !SPANISH_STOP.has(word) && word.length >= 4))];
  // A named identifier is more specific than generic words such as diccionario.
  const identifiers = unique.filter(word => /[_-]/.test(word));
  return (identifiers.length ? identifiers : unique).slice(0, 8);
}

/**
 * Retrieve the subgraph relevant to a question.
 *
 * `hops` bounds the traversal. One hop is usually enough for a factual
 * question; two is needed for the chain questions that defeat chunk
 * retrieval, and costs more context.
 */
export async function retrieve(
  mcp: McpClient,
  question: string,
  hops = 2,
  opts?: { model?: string; systemPrompt?: string },
): Promise<Retrieved> {
  const ts = terms(question);
  const sys = opts?.systemPrompt ?? QA_SYSTEM_PROMPT;
  // Scoped COMPLETE queries start alongside anchoring: generic count/state
  // questions must not depend on the bounded neighbourhood.
  const scoped = (async () => {
    const out: Pick<Retrieved, 'correspondenceOverview' | 'resourceContext' | 'variableOverview' | 'cruceFichaContext' | 'cruceCodigoContext'> = {};
    if (wantsCorrespondenceOverview(question)) out.correspondenceOverview = await correspondenceStatusOverview(mcp);
    if (wantsResourceScope(question)) out.resourceContext = await resourceCorrespondenceContext(mcp, question);
    if (wantsVariableOverview(question)) out.variableOverview = await variableStatusOverview(mcp);
    const ficha = await cruceFichaContext(mcp, question);
    if (ficha.context) out.cruceFichaContext = ficha.context;
    const codigo = await cruceCodigoContext(mcp, question);
    if (codigo.context) out.cruceCodigoContext = codigo.context;
    (out as { __fichaAnchors?: Retrieved['anchors'] }).__fichaAnchors = [...ficha.anchors, ...codigo.anchors];
    return out;
  })();
  if (ts.length === 0) {
    const s = await scoped;
    const { __fichaAnchors, ...rest } = s as typeof s & { __fichaAnchors?: Retrieved['anchors'] };
    if (!rest.correspondenceOverview && !rest.resourceContext && !rest.variableOverview && !rest.cruceFichaContext && !rest.cruceCodigoContext) {
      return maybeFit({ anchors: [], facts: [], claims: [], provenance: [], conflicts: [] }, question, opts?.model, sys);
    }
    return maybeFit({ anchors: [...(__fichaAnchors ?? [])], facts: [], claims: [], provenance: [], conflicts: [], ...rest }, question, opts?.model, sys);
  }

  // 1. ANCHORS. Entities whose label or local name matches a question term.
  const filter = ts.map(t => `CONTAINS(LCASE(STR(?l)), ${JSON.stringify(t)}) || CONTAINS(LCASE(STR(?e)), ${JSON.stringify(encodeURIComponent(t).toLowerCase())})`).join(' || ');
  const score = ts.map(t => `IF(LCASE(STR(?l)) = ${JSON.stringify(t)}, 100, IF(STRSTARTS(LCASE(STR(?l)), ${JSON.stringify(t + ' ')}), 50, 0))`).join(' + ');
  // Ordered by label length, shortest first, and this is load-bearing rather
  // than cosmetic. A corpus about a specific dataset contains many entities
  // whose names merely CONTAIN it (e.g. DISTRIBUTION_COVERAGE_RATIO_FOR_THAT_
  // DATASET and friends). An unordered LIMIT let those crowd out the dataset
  // node itself, and every claim in the corpus hangs off that one node, so
  // the retrieval returned eighty relationships, zero claims, and an honest
  // report that the graph knew nothing. Shortest-label-first puts the exact
  // match at the front.
  const anchorRows = await select(mcp, `${P}
    SELECT DISTINCT ?e ?l ?score WHERE {
      ?e rdfs:label ?l .
      FILTER(${filter})
      BIND((${score}) AS ?score)
    } ORDER BY DESC(?score) STRLEN(STR(?l)) STR(?e) LIMIT 16`);
  const anchors = anchorRows.map(r => ({ iri: r.e, label: r.l }));
  const mappingContext = await correspondenceContext(mcp, ts);
  const extra = await scoped;
  const { __fichaAnchors, ...cleanExtra } = extra as typeof extra & { __fichaAnchors?: Retrieved['anchors'] };
  for (const fa of __fichaAnchors ?? []) {
    if (!anchors.some(a => a.iri === fa.iri)) anchors.unshift(fa);
  }
  if (anchors.length === 0) {
    if (!__fichaAnchors?.length) {
      return maybeFit({ anchors: [], facts: [], claims: [], provenance: [], conflicts: [], correspondenceContext: mappingContext, ...cleanExtra }, question, opts?.model, sys);
    }
    // Solo-alias (p. ej. pregunta mínima "F2"): sin vecindario genérico.
    return maybeFit({ anchors, facts: [], claims: [], provenance: [], conflicts: [], correspondenceContext: mappingContext, ...cleanExtra }, question, opts?.model, sys);
  }

  // A question naming a CLASS ("dataset conformance") anchors on the class
  // node, which carries a label and nothing else: the facts live on its
  // instances. Expand class anchors to their instances so the neighbourhood
  // walk starts where the claims are.
  const classValues = iriValues(anchors.map(a => a.iri));
  const instanceRows = await select(mcp, `${P}
    SELECT DISTINCT ?i ?il WHERE {
      VALUES ?c { ${classValues} }
      ?i a ?c .
      OPTIONAL { ?i rdfs:label ?il }
    } LIMIT 12`);
  for (const r of instanceRows) {
    if (!anchors.some(a => a.iri === r.i)) {
      anchors.push({ iri: r.i, label: r.il ?? r.i.replace(/^.*[#/]/, '') });
    }
  }

  const values = iriValues(anchors.map(a => a.iri));

  // 2. NEIGHBOURHOOD. Traverse outward and inward. This is the topology doing
  //    the selection: relevance is adjacency in the model, not cosine distance.
  const depth = Math.max(1, Math.min(hops, 3));
  const facts: string[] = [];
  const visited = new Set(anchors.map(a => a.iri));
  let frontier = anchors.map(a => a.iri);
  for (let hop = 1; hop <= depth; hop++) {
    const neighbourhood = hop === 1
      ? `VALUES ?anchor { ${iriValues(frontier)} }
         { ?anchor ?p ?o . BIND(?anchor AS ?s) }
         UNION { ?s ?p ?anchor . BIND(?anchor AS ?o) }`
      : `VALUES ?s { ${iriValues(frontier)} } ?s ?p ?o .`;
    const rows = await select(mcp, `${P}
      SELECT DISTINCT ?s ?sl ?p ?o ?ol WHERE {
        ${neighbourhood}
        OPTIONAL { ?s rdfs:label ?sl }
        OPTIONAL { ?o rdfs:label ?ol }
        FILTER(!isBlank(?o) && !isBlank(?s))
      } ORDER BY ?s ?p ?o LIMIT 120`);
    const next = new Set<string>();
    for (const r of rows) {
      const s = r.sl ? `${JSON.stringify(r.sl)} <${r.s}>` : `<${r.s}>`;
      const o = isIri(r.o) ? (r.ol ? `${JSON.stringify(r.ol)} <${r.o}>` : `<${r.o}>`) : JSON.stringify(r.o);
      if (r.s && r.o && r.p) facts.push(`${s} --[<${r.p}>]--> ${o}`);
      // Do not walk through rdf:type into every other instance of a class.
      if (!['http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://www.w3.org/2000/01/rdf-schema#subClassOf'].includes(r.p)) {
        if (isIri(r.o) && !visited.has(r.o)) next.add(r.o);
      }
    }
    frontier = [...next].slice(0, 24);
    for (const iri of frontier) visited.add(iri);
    if (!frontier.length) break;
  }

  // 3. CLAIMS. The document passages attached to the anchors, with their
  //    section and document, so the answer can cite rather than paraphrase.
  //
  //    `statedIn` points at either a section or a document depending on which
  //    extraction shape produced the claim, so both are matched. Binding only
  //    the section shape leaves every typing claim attributed to
  //    "unattributed", which silently strips the citations the answer needs.
  const claimRows = await select(mcp, `${P}
    SELECT DISTINCT ?text ?doc ?sec WHERE {
      VALUES ?anchor { ${values} }
      ?c a dcus:Claim ; dcus:claimText ?text ; dcus:aboutEntity ?anchor ; dcus:statedIn ?target .
      {
        ?target dcus:docId ?doc .
        BIND(?target AS ?docNode)
      } UNION {
        ?docNode dcus:hasSection ?target ; dcus:docId ?doc .
        OPTIONAL { ?target dcus:sectionNumber ?sec }
      }
    } LIMIT 60`);
  const claims = claimRows.map(r => ({ text: r.text, doc: r.doc ?? 'unattributed', section: r.sec ?? '' }));

  // 4. PROVENANCE. Which upstream source asserted each anchor. Two sources on
  //    one entity is the signal that something is disputed.
  //
  //    Identity here is the document NODE, not its label. Documents carry more
  //    than one label (the id "DCAT-001" and the title "Open Data Catalogue
  //    Conformance Report"), and grouping by label reported a single document
  //    as two sources, which then read as a dispute between a document and
  //    itself.
  const provRows = await select(mcp, `${P}
    SELECT ?thing ?s ?doc ?src WHERE {
      VALUES ?thing { ${values} }
      ?thing prov:wasDerivedFrom ?s .
      OPTIONAL { ?s dcus:docId ?doc }
      OPTIONAL { ?s rdfs:label ?src }
    }`);
  const byThing = new Map<string, Map<string, string>>();
  for (const r of provRows) {
    if (!byThing.has(r.thing)) byThing.set(r.thing, new Map());
    // Prefer the document id; fall back to a label only when there is no id.
    const name = r.doc || r.src ? `${r.doc || r.src} (${r.s})` : r.s;
    byThing.get(r.thing)!.set(r.s, name);
  }
  const provenance = [...byThing.entries()].map(([thing, sources]) => ({
    thing,
    sources: [...new Set(sources.values())],
  }));

  // 5. CONFLICTS.
  //
  //    The structural check asks the ontology directly: is this anchor typed
  //    into two classes declared disjoint? Cheap, exact, and the thing a
  //    chunk retriever cannot represent at all.
  const conflictRows = await select(mcp, `${P}
    SELECT DISTINCT ?subject ?a ?b WHERE {
      VALUES ?subject { ${values} }
      ?subject a ?a, ?b .
      FILTER(STR(?a) < STR(?b))
      ?a rdfs:subClassOf* ?da . ?b rdfs:subClassOf* ?db .
      { ?da owl:disjointWith ?db } UNION { ?db owl:disjointWith ?da }
    }`);
  const conflicts: string[] = conflictRows.map(
    r => `${r.subject} is typed as both ${r.a} and ${r.b}, which the ontology declares disjoint`,
  );

  const detailed = disagreements(claims);

  // A structural conflict and a document-level disagreement about the SAME
  // entity are the same finding told twice, and the detailed one strictly
  // dominates: it names who said what. Keeping both padded the panel with a
  // restatement, so the generic line is dropped when the specific one exists.
  const named = new Set(detailed.map(d => d.split(' is typed as ')[0]));
  const kept = conflicts.filter(c => ![...named].some(n => c.startsWith(`${n} is typed`)));
  conflicts.length = 0;
  conflicts.push(...kept, ...detailed);

  return maybeFit({
    anchors,
    facts: [...new Set(facts)].slice(0, 240),
    claims,
    provenance,
    conflicts: [...new Set(conflicts)],
    correspondenceContext: mappingContext,
    ...cleanExtra,
  }, question, opts?.model, sys);
}

/**
 * Typing disagreements visible in a set of claims.
 *
 * Typing claims read "DOC types ENTITY as CLASS". Grouping by entity and
 * collecting the distinct classes asserted about it finds disagreement using
 * only what was retrieved.
 */
function disagreements(claims: Retrieved['claims']): string[] {
  const byEntity = new Map<string, Map<string, Set<string>>>();

  for (const c of claims) {
    const m = /^(\S+)\s+types\s+(\S+)\s+as\s+(\S+)$/.exec(c.text.trim());
    if (!m) continue;
    const [, , entity, type] = m;
    if (!byEntity.has(entity)) byEntity.set(entity, new Map());
    const types = byEntity.get(entity)!;
    if (!types.has(type)) types.set(type, new Set());
    types.get(type)!.add(c.doc);
  }

  const out: string[] = [];
  for (const [entity, types] of byEntity) {
    if (types.size < 2) continue;
    const parts = [...types.entries()].map(
      ([type, docs]) => `${type} per ${[...docs].sort().join(', ')}`,
    );
    out.push(`${entity} is typed as ${parts.join(' but ')}`);
  }
  return out;
}

/** Render the subgraph as context for the model. */
export function asContext(r: Retrieved): string {
  const parts: string[] = [];
  parts.push('RETRIEVAL SCOPE: The general neighbourhood is a bounded, PARTIAL subgraph. Missing facts here do not establish absence in the graph. Only explicitly COMPLETE scoped queries below support absence/count claims for their stated scope. Zero document claims does not mean no dictionary or graph evidence.');
  if (r.correspondenceContext) parts.push(`QUALIFIED SEMANTIC CORRESPONDENCES\n${r.correspondenceContext}`);
  if (r.correspondenceOverview) parts.push(`GLOBAL CORRESPONDENCE COUNTS (COMPLETE)\n${r.correspondenceOverview}`);
  if (r.cruceFichaContext) parts.push(`CRUCE FICHA (COMPLETE FOR THE NAMED FICHA ONLY)\n${r.cruceFichaContext}`);
  if (r.cruceCodigoContext) parts.push(`CRUCE CODIGO (COMPLETE FOR THE NAMED CODE ONLY)\n${r.cruceCodigoContext}`);
  if (r.resourceContext) parts.push(`RESOURCE-SCOPED CORRESPONDENCES (COMPLETE FOR THE STATED FILTER)\n${r.resourceContext}`);
  if (r.variableOverview) parts.push(`VARIABLE STATES (COMPLETE)\n${r.variableOverview}`);
  parts.push(`ANCHOR ENTITIES\n${r.anchors.map(a => `- ${a.label} (${a.iri})`).join('\n')}`);
  if (r.facts.length) parts.push(`\nGRAPH NEIGHBOURHOOD\n${r.facts.map(f => `- ${f}`).join('\n')}`);
  if (r.claims.length) {
    parts.push(
      `\nDOCUMENT CLAIMS (cite these by document and section)\n` +
        r.claims.map(c => `- [${c.doc}${c.section ? ` S${c.section}` : ''}] ${c.text}`).join('\n'),
    );
  }
  if (r.provenance.length) {
    parts.push(
      `\nPROVENANCE\n` +
        r.provenance
          .map(p => `- ${p.thing}: ${p.sources.join(', ')}`)
          .join('\n'),
    );
  }
  if (r.conflicts.length) {
    parts.push(`\nREASONER CONFLICTS\n${r.conflicts.map(c => `- ${c}`).join('\n')}`);
  }
  return parts.join('\n');
}

export const QA_SYSTEM_PROMPT = `You answer questions about a knowledge graph derived from a document corpus.

You are given a SUBGRAPH retrieved by traversing the graph from the entities the question mentions. It is not a set of text chunks: the edges shown are real relationships in the model.

Rules:
- The general neighbourhood is PARTIAL. Never turn "not retrieved" into "does not exist in the graph". State "not found in the retrieved evidence" when coverage is partial. Absence claims require an explicitly COMPLETE query for that exact scope.
- For semantic correspondences, use COMPLETE correspondence status counts and the qualified mapping records, including incoming variableDestino links. Distinguish the variable's estadoSemantico from each column mapping's estadoCorrespondencia. Report documental_revisada alongside candidata_por_nombre when both occur; do not generalize one resource/year's state to all resources. Counts cover all pages even when displayed examples are partial.
- Global correspondence counts come ONLY from the COMPLETE global overview (native aggregation over every mapping). Per-variable counts and neighbourhood facts never substitute for them.
- A resource/year scope (for example Matrimonios 2022) is resolved to explicit catalogued resource IRIs first; counts cover exactly those resources via their esquema/columna path, with per-resource tallies. The declared period takes precedence over label years; the grand total counts distinct mappings; observed triangulated columns only, never the full source file. Report the resolved resource labels and, when UNRESOLVED, the candidate labels without any zero claim. Never generalize one resource or year to others.
- estadoSemantico belongs to the variable; estadoCorrespondencia belongs to each column/variable mapping. When asked about states, report both tallies separately and never merge them into one.
- A column may retain an older definicionCandidata link alongside a newer qualified documental_revisada mapping. The candidate link alone does not negate the explicitly reviewed mapping. Cite the mapping URI and its state for the specific column/resource.
- When reporting reviewed correspondences, identify their column's resource/year from the supplied column label (for example Matrimonios 2022). A variable-level status count alone is not the evidence for a specific resource. Include the reviewed mapping URI and distinguish other candidate resources.
- Answer ONLY from the supplied subgraph. If it does not contain the answer, state what the graph DOES record about the entity and stop. Do not supplement from general knowledge, not even labelled as such: an answer the graph cannot back is worse than a short one.
- Values like TOK_KIND_hex are tokens standing in for protected values. Repeat them verbatim; never guess what they hide.
- Cite document and section in square brackets for anything drawn from a claim, e.g. [DCAT-001 S3].
- Multiple provenance sources alone do not imply a dispute. Only report a contradiction when the evidence or REASONER CONFLICTS supports it.
- Anchor labels are names, not class membership. Never call a node an instance of a class without an explicit rdf:type fact.
- For a variable's meaning, use the original dictionary description, even when its name suggests a different meaning. Do not infer definitions from variable names.
- Cite graph facts using the full definition/entity URI and original source URL present in the subgraph. Preserve exact descriptions and evidence identifiers. When present, include datatype, format and requiredness from the dictionary row.
- If REASONER CONFLICTS is non-empty, lead with it. A contradiction in the model outranks any other finding.
- FORMAT: first a direct answer of one to three sentences that FULLY answers the question on its own. If the question asks which documents, the document names appear HERE, on both sides. If it asks for a value, the value appears here. The reader may never expand further.
- Then a line containing only --- . Then supporting detail: per-document claims, section citations, counts. Nothing before the answer.
- DETAIL LIMIT: at most six short lines. One line per document claim. Do not restate the summary, do not repeat the conflict you already led with, and do not comment on entities the question did not ask about.
- Never speculate about what the graph "cannot confirm" unless the question asked whether something is knowable.
- Be concise. No preamble. No emoji.`;
