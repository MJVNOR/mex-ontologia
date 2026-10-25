import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { readFile } from 'node:fs/promises';
const ORIG = 'C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent/graphrag.ts';
const PATCHED = path.resolve('propuestas/pendientes-muse-r4/recuperacion-f2/graphrag.f2.ts');
const orig = await import(pathToFileURL(ORIG).href);
const patch = await import(pathToFileURL(PATCHED).href);
const ENGINE_QUERY = 'http://127.0.0.1:8137/api/query';
const mcp = { async callTool(n,a){ const r=await fetch(ENGINE_QUERY,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(a)}); if(!r.ok) throw new Error('HTTP '+r.status); return await r.text(); } };
const corpus = JSON.parse(await readFile(path.resolve('propuestas/pendientes-muse-r4/chat/corpus.json'),'utf8'));
function evalCtx(ctx, caso){
  const low=ctx.toLowerCase();
  return {
    faltan:(caso.debe??[]).filter(f=>!low.includes(f.toLowerCase())),
    alguno:(caso.debe_alguno??[]),
    algunoOk:(caso.debe_alguno??[]).length===0||(caso.debe_alguno??[]).some(f=>low.includes(f.toLowerCase())),
    prohibidos:(caso.prohibido??[]).filter(f=>low.includes(f.toLowerCase())),
  };
}
let ok=true;
for(const caso of corpus.casos){
  const rO=await orig.retrieve(mcp,caso.pregunta);
  const cO=orig.asContext(rO);
  const rP=await patch.retrieve(mcp,caso.pregunta);
  const cP=patch.asContext(rP);
  const eO=evalCtx(cO,caso), eP=evalCtx(cP,caso);
  const f2O=cO.includes('cruce-r3/F2'), f2P=cP.includes('cruce-r3/F2');
  console.log(`--- ${caso.id} ---`);
  console.log(`orig: anchors=${rO.anchors.length} hechos=${rO.facts.length} f2=${f2O} faltan=${JSON.stringify(eO.faltan)} algunoOk=${eO.algunoOk} prohib=${JSON.stringify(eO.prohibidos)}`);
  console.log(`patch: anchors=${rP.anchors.length} hechos=${rP.facts.length} f2=${f2P} ficha=${!!rP.cruceFichaContext} faltan=${JSON.stringify(eP.faltan)} algunoOk=${eP.algunoOk} prohib=${JSON.stringify(eP.prohibidos)}`);
  if(caso.id==='C2-f2-evidencia'){
    const need=['cruce-r3/F2','72','144','grandes_grupos','condicionPendiente','condicionVerificada','wasDerivedFrom','F2.json','solo 2020','NO','no identidad de medida','sin equivalencia INEGI','NO ejecutado'];
    // normalizar: contexto usa minusculas en predicados? comprobar contains case-insensitive
    const low=cP.toLowerCase();
    for(const k of ['cruce-r3/f2','72','144','grandes_grupos','condicionpendiente','condicionverificada','f2.json','2020']){
      if(!low.includes(k)){ console.log('FALTA '+k); ok=false; }
    }
    if(eP.prohibidos.length){ console.log('PROHIBIDO PRESENTE'); ok=false; }
    if(!f2P){ console.log('F2 AUSENTE'); ok=false; }
    // no afirmar cobertura cruzada 1990-2040
    if(/cobertura[^.]{0,40}1990(-|–)2040[^.]{0,40}cruzad/i.test(cP) && !/no es cobertura cruzada/i.test(cP)){ console.log('FALSO ALCANCE'); ok=false; }
  } else if (patch.cruceCodigos(caso.pregunta).length) {
    // codigo nombrado (p. ej. 26001): mejora aditiva intencionada (detalle
    // ambas fuentes); el contenido original debe seguir pasando el oraculo.
    if(eP.faltan.length || !eP.algunoOk || eP.prohibidos.length){ console.log('REGRESION CONTENIDO en '+caso.id); ok=false; }
    const low=cP.toLowerCase();
    for(const k of ['26001','grandes_grupos','indicadores','medidaorigen','fuenteoriginal']){ if(!low.includes(k)){ console.log('FALTA '+k+' en '+caso.id); ok=false; } }
  } else {
    // sin alias F ni codigo: contexto debe ser idéntico al original (aditivo estricto)
    if(cO!==cP){ console.log('DIFERENCIA INESPERADA en '+caso.id+' (len '+cO.length+' vs '+cP.length+')'); ok=false; }
  }
}
console.log(ok?'REGRESION OK':'REGRESION FALLA');
if(!ok) process.exit(1);
