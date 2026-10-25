/** Recorte de razonamiento y presupuesto 6500 (dirigido, sintético).
 * Fixtures propios cortos: NADA de respuestas reales del modelo aquí.
 * CERO llamadas al modelo, solo importaciones puras + SELECT del harness.
 */
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const PATCHED = path.resolve('propuestas/pendientes-muse-r4/recuperacion-f2/graphrag.f2.ts');
const g = await import(pathToFileURL(PATCHED).href);
const { stripThoughtBlocks } = await import(pathToFileURL('C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent/providers/openai.ts').href);

let fallos = 0;
const ok = (cond, msg) => { console.log((cond ? 'OK  ' : 'FALLO') + ' ' + msg); if (!cond) fallos++; };

// Presupuesto recalibrado con factor medido (9845 est -> 14072 reales)
ok(g.budgetForModel('gemma-4-31b-it').maxInputTokens === 6500, 'gemma-4-31b-it -> 6500 estimados');
ok(g.budgetForModel('gemma-4-31b-it').pacingMs >= 65000, 'pacing >=65s intacto');
ok(g.GEMMA_TPM === 16000, 'TPM 16000');

// Bloque thought cerrado: se oculta, final intacto verbatim
ok(stripThoughtBlocks('<thought>pienso</thought>\n72 comparaciones.') === '72 comparaciones.', 'cierra thought, final intacto');
// Variante think + multiples
ok(stripThoughtBlocks('<think>a</think>Uno<thought>b</thought>Dos') === 'UnoDos', 'think y multiples');
// Incompleto (truncado sin cierre): se oculta hasta el final
ok(stripThoughtBlocks('Respuesta visible.\n<think>corte a mitad') === 'Respuesta visible.', 'incompleto truncado');
ok(stripThoughtBlocks('<thought>solo razonamiento') === '', 'solo-thought -> vacio (no afirmar)');
// Solo razonamiento cerrado -> vacio falsy: el caller no debe afirmar respuesta
const soloRazon = stripThoughtBlocks('<thought>nada final</thought>');
ok(soloRazon === '' && !soloRazon, 'vacio falsy: caller no afirma ni cachea');
// Sin bloques: intacto
ok(stripThoughtBlocks('F2: 72/72, nombres 72/72.') === 'F2: 72/72, nombres 72/72.', 'sin bloques intacto');
// Atributos y mayusculas
ok(stripThoughtBlocks('<THOUGHT id="1">x</THOUGHT>Fin') === 'Fin', 'atributos/mayusculas');
// Apertura sin cierre al final tras respuesta larga
const largo = 'A'.repeat(3000) + '\n<thought>' + 'B'.repeat(500);
ok(stripThoughtBlocks(largo) === 'A'.repeat(3000), 'incompleto final tras respuesta larga');

console.log(fallos === 0 ? 'RECORTE OK' : `RECORTE FALLA (${fallos})`);
if (fallos) process.exit(1);
