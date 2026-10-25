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
export async function retrieve(mcp: McpClient, question: string, hops = 2): Promise<Retrieved> {
  const ts = terms(question);
  if (ts.length === 0) {
    return { anchors: [], facts: [], claims: [], provenance: [], conflicts: [] };
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
  if (anchors.length === 0) {
    return { anchors: [], facts: [], claims: [], provenance: [], conflicts: [], correspondenceContext: mappingContext };
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

  return {
    anchors,
    facts: [...new Set(facts)].slice(0, 240),
    claims,
    provenance,
    conflicts: [...new Set(conflicts)],
    correspondenceContext: mappingContext,
  };
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
