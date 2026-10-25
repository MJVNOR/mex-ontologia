/** Regresion anti-falsa-afirmacion: F1/F3 conservan lo suyo, F9 no inventa.
 * La ficha resume SOLO con agregados RDF de ESA ficha (conteos nativos,
 * periodos/roles/medidas observados); nada hardcodeado de F2 fuera de F2.
 * CERO llamadas al modelo, solo SELECT contra el motor vivo.
 */
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const PATCHED = path.resolve('propuestas/pendientes-muse-r4/recuperacion-f2/graphrag.f2.ts');
const g = await import(pathToFileURL(PATCHED).href);
const Q = 'http://127.0.0.1:8137/api/query';
const mcp = { async callTool(n, a) { const r = await fetch(Q, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(a) }); if (!r.ok) throw new Error('HTTP ' + r.status); return await r.text(); } };

let fallos = 0;
const ok = (cond, msg) => { console.log((cond ? 'OK  ' : 'FALLO') + ' ' + msg); if (!cond) fallos++; };
const F2_TEXTO = ['cruce-r3/F2', 'grandes_grupos', 'suma_grupos_edad', 'poblacion_mitad_ano', 'F2.json', 'SOLO-2020', 'solo 2020 cruzado', 'dos evidencias por comparacion', '1990-2040', 'indicadores'];

const QF1 = 'Explica la evidencia F1 de Matrimonios y Divorcios y sus condiciones pendientes. No extrapoles a otros años.';
const QF3 = 'Explica la evidencia F3 de Titulados y Egresados y sus condiciones pendientes. No extrapoles a otros periodos.';
const QF9 = 'Explica la evidencia F9 y sus condiciones pendientes.';
const QF2 = 'Explica la evidencia F2 de proyecciones en 2020 y sus condiciones pendientes. No extrapoles a otros años.';

// F1: lo suyo (2022, Registro Civil, F1.json, 0 comparaciones), nada de F2
{
  const { context, anchors } = await g.cruceFichaContext(mcp, QF1);
  ok(context.length > 0, 'F1 recupera ficha');
  ok(context.includes('cruce-r3/F1'), 'F1 menciona su IRI');
  ok(context.includes('F1.json'), 'F1 cita su documento');
  ok(context.includes('2022'), 'F1 conserva su periodo 2022');
  ok(context.includes('0 comparaciones') && context.includes('sin comparaciones municipales en RDF'), 'F1 declara 0 comparaciones en RDF (no inventa cruce)');
  for (const t of F2_TEXTO) ok(!context.includes(t), `F1 sin texto F2: ${t}`);
  ok(anchors.some(a => a.iri.includes('cruce-r3/F1')), 'F1 ancla propia');
  const r = await g.retrieve(mcp, QF1, 2, { model: 'gemma-4-31b-it' });
  const c = g.asContext(r);
  ok(g.estimateInputTokens({ question: QF1, context: c }) <= 10000, 'F1 bajo presupuesto Gemma');
  ok(c.includes('cruce-r3/F1') && !c.includes('cruce-r3/F2'), 'F1 con presupuesto: su ficha, sin F2');
}

// F3: lo suyo (2020-2021/2021-2022, UES, F3.json, 0 comparaciones), nada de F2
{
  const { context, anchors } = await g.cruceFichaContext(mcp, QF3);
  ok(context.length > 0, 'F3 recupera ficha');
  ok(context.includes('cruce-r3/F3'), 'F3 menciona su IRI');
  ok(context.includes('F3.json'), 'F3 cita su documento');
  ok(context.includes('2020-2021') && context.includes('2021-2022'), 'F3 conserva sus periodos');
  ok(context.includes('0 comparaciones') && context.includes('sin comparaciones municipales en RDF'), 'F3 declara 0 comparaciones en RDF');
  for (const t of F2_TEXTO) ok(!context.includes(t), `F3 sin texto F2: ${t}`);
  ok(anchors.some(a => a.iri.includes('cruce-r3/F3')), 'F3 ancla propia');
  const r = await g.retrieve(mcp, QF3, 2, { model: 'gemma-4-31b-it' });
  const c = g.asContext(r);
  ok(g.estimateInputTokens({ question: QF3, context: c }) <= 10000, 'F3 bajo presupuesto Gemma');
  ok(c.includes('cruce-r3/F3') && !c.includes('cruce-r3/F2'), 'F3 con presupuesto: su ficha, sin F2');
}

// F9: alias inexistente -> vacio, sin crash, sin seccion ficha
{
  const { context, anchors } = await g.cruceFichaContext(mcp, QF9);
  ok(context === '' && anchors.length === 0, 'F9 inexistente: contexto vacio');
  const r = await g.retrieve(mcp, QF9);
  const c = g.asContext(r);
  ok(!c.includes('CRUCE FICHA') && !c.includes('cruce-r3/F9'), 'F9 sin seccion ficha ni IRI inventado');
}

// F2: resumen derivado coincide con su RDF (72, 2020, roles/medidas reales)
{
  const { context } = await g.cruceFichaContext(mcp, QF2);
  ok(context.includes('72 comparaciones'), 'F2 72 comparaciones (conteo nativo)');
  ok(context.includes('144 evidencias'), 'F2 144 evidencias (conteo nativo)');
  ok(context.includes('"2020"'), 'F2 periodo 2020 observado en RDF');
  ok(context.includes('grandes_grupos') && context.includes('suma_grupos_edad_H_M'), 'F2 rol/medida reales');
  ok(context.includes('indicadores') && context.includes('poblacion_mitad_ano'), 'F2 segunda fuente real');
  ok(context.includes('SOLO-2020'), 'F2 alcance derivado (unico periodo)');
}

console.log(fallos === 0 ? 'FICHAS OK' : `FICHAS FALLA (${fallos})`);
if (fallos) process.exit(1);
