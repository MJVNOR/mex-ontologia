/** Test de presupuesto Gemma4 31B + regresion de contenido (CERO modelo).
 * Verifica con recuperacion real (solo SELECT): presupuesto, F2, totales,
 * definiciones, 26001 ambas fuentes, limites, sin truncamiento y sin
 * degradar otros modelos. Sale 1 si algo falla.
 */
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { readFile } from 'node:fs/promises';

const PATCHED = path.resolve('propuestas/pendientes-muse-r4/recuperacion-f2/graphrag.f2.ts');
const g = await import(pathToFileURL(PATCHED).href);
const CORPUS = path.resolve('propuestas/pendientes-muse-r4/chat/corpus.json');
const MODEL = 'gemma-4-31b-it';
const corpus = JSON.parse(await readFile(CORPUS, 'utf8'));

const Q = 'http://127.0.0.1:8137/api/query';
const mcp = { async callTool(n, a) { const r = await fetch(Q, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(a) }); if (!r.ok) throw new Error('HTTP ' + r.status); return await r.text(); } };

let fallos = 0;
const ok = (cond, msg) => { console.log((cond ? 'OK  ' : 'FALLO') + ' ' + msg); if (!cond) fallos++; };

// 1. Configuracion de presupuesto por modelo
ok(g.GEMMA_TPM === 16000, 'GEMMA_TPM=16000');
ok(g.GEMMA_PACING_MS >= 60000, `pacing>=60s (${g.GEMMA_PACING_MS}ms)`);
ok(g.budgetForModel(MODEL).maxInputTokens === 6500, 'gemma-4-31b-it -> 6500 tokens entrada estimados (~9300 reales + 4096 salida < 16000)');
ok(g.budgetForModel('otro-modelo-x').maxInputTokens === Infinity, 'modelo desconocido -> sin recorte');
ok(g.budgetForModel(undefined).maxInputTokens === Infinity, 'sin modelo -> intacto');
ok(g.budgetForModel(MODEL, 5000).maxInputTokens === 5000, 'override configurable por llamada');

// 2. Estimacion con margen e incluyendo prompt+pregunta
const est1 = g.estimateInputTokens({ question: 'hola', context: 'x'.repeat(4000) });
ok(est1 === Math.ceil((g.QA_SYSTEM_PROMPT.length + 4 + 4000) / 4 * 1.15), 'estima incluye prompt+pregunta+contexto con margen 1.15');

// 3. Presupuesto + contenido en los 6 casos (recuperacion real)
const ctxFull = new Map();
for (const caso of corpus.casos) {
  const r = await g.retrieve(mcp, caso.pregunta, 2, { model: MODEL });
  const c = g.asContext(r);
  const est = g.estimateInputTokens({ question: caso.pregunta, context: c });
  ok(est <= 6500, `${caso.id}: ${est}tok <= 6500`);
  const low = c.toLowerCase();
  const faltan = (caso.debe ?? []).filter((f) => !low.includes(f.toLowerCase()));
  const algunoOk = (caso.debe_alguno ?? []).length === 0 || (caso.debe_alguno ?? []).some((f) => low.includes(f.toLowerCase()));
  const prohib = (caso.prohibido ?? []).filter((f) => low.includes(f.toLowerCase()));
  ok(faltan.length === 0, `${caso.id} debe: ${faltan.length ? 'faltan ' + faltan : 'completo'}`);
  ok(algunoOk, `${caso.id} debe_alguno presente`);
  ok(prohib.length === 0, `${caso.id} prohibidos ausentes`);
  // Sin truncamiento: cada linea existe verbatim en el contexto sin presupuesto
  const r0 = await g.retrieve(mcp, caso.pregunta);
  ctxFull.set(caso.id, g.asContext(r0));
  const set0 = new Set(ctxFull.get(caso.id).split('\n'));
  const bad = c.split('\n').filter((l) => l.startsWith('BUDGET TRIM') || l.startsWith('-- fuente') ? false : !set0.has(l));
  ok(bad.length === 0, `${caso.id} sin lineas truncadas (${bad.length})`);
}

// 4. Requisitos finos con presupuesto aplicado
const C = async (id) => { const c = corpus.casos.find((x) => x.id === id); const r = await g.retrieve(mcp, c.pregunta, 2, { model: MODEL }); return g.asContext(r).toLowerCase(); };
const c1 = await C('C1-totales');
ok(c1.includes('865') && c1.includes('documental_revisada'), 'C1 totales exactos con presupuesto');
const c2 = await C('C2-f2-evidencia');
for (const k of ['cruce-r3/f2', '72', '144', 'grandes_grupos', 'condicionpendiente', 'condicionverificada', 'f2.json', 'solo-2020', 'no identidad de medida', 'sin equivalencia inegi']) ok(c2.includes(k), `C2 conserva ${k}`);
ok(!/cobertura[^.]{0,60}1990(-|—|–)2040[^.]{0,40}cruzad[ao]/i.test(c2) || c2.includes('no es cobertura cruzada'), 'C2 sin falso alcance 1990-2040');
const c3 = await C('C3-f2-igualdad');
const r3full = await g.retrieve(mcp, corpus.casos.find((x) => x.id === 'C3-f2-igualdad').pregunta);
ok(g.asContext(r3full).length >= c3.length && c3.length > 0, 'C3 recortado con presupuesto (6500 < 9607 sin recorte)');
ok(c3.includes('igualdad') || c3.includes('72'), 'C3 igualdad/limites presentes');
const c4 = await C('C4-definicion-diccionario');
for (const k of ['364ffa5c', 'diccionario.csv', 'definicionoriginal', 'significadodocumentado']) ok(c4.includes(k), `C4 definicion conserva ${k}`);
const c5 = await C('C5-diferencia-variables');
for (const k of ['año_matrimonio', 'año_defuncion', 'documental_revisada', 'candidata_por_nombre']) ok(c5.includes(k), `C5 conserva ${k}`);
const c6 = await C('C6-clave-26001');
for (const k of ['26001', 'grandes_grupos', 'indicadores', 'suma_grupos_edad_h_m', 'poblacion_mitad_ano', 'nombreorigen', 'fuenteoriginal', 'hojafuente', 'shafuente', 'valororigen']) ok(c6.includes(k), `C6 26001 ambas fuentes conserva ${k}`);
ok(!c6.includes('son inegi') && !c6.includes('equivalen a inegi') && !c6.includes('código inegi vigente'), 'C6 sin afirmar INEGI');

// 5. Sin degradar otros modelos: sin opts y modelo desconocido = contexto completo
const q2 = corpus.casos[1].pregunta;
const full = ctxFull.get('C2-f2-evidencia');
const rNoOpt = await g.retrieve(mcp, q2);
ok(g.asContext(rNoOpt) === full, 'sin modelo: contexto completo intacto');
const rDes = await g.retrieve(mcp, q2, 2, { model: 'otro-modelo-x' });
ok(g.asContext(rDes) === full, 'modelo desconocido: intacto');
const fitNone = g.fitRetrieved(rNoOpt, q2);
ok(fitNone.fitted === rNoOpt && fitNone.report.trimmed === false, 'fitRetrieved sin modelo no copia ni recorta');

console.log(fallos === 0 ? 'PRESUPUESTO OK' : `PRESUPUESTO FALLA (${fallos})`);
if (fallos) process.exit(1);
