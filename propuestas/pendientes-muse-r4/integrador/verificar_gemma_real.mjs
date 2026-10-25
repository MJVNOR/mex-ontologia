import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../..');
const OUT=path.join(ROOT,'propuestas/pendientes-muse-r4/integrador/gemma-real');
await fs.mkdir(OUT,{recursive:true});
const src='C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent';
const envFile=(await fs.readFile('C:/Users/marti/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/open-ontologies-studio/agent-env-path.txt','utf8')).replace(/^\uFEFF/,'').trim();
const settings={};
for(const line of (await fs.readFile(envFile,'utf8')).replace(/^\uFEFF/,'').split(/\r?\n/)){
 const m=line.trim().match(/^(ONTO_(?:LLM_MODEL|LLM_BASE_URL|LLM_API_KEY))\s*=\s*(.*)$/);
 if(m)settings[m[1]]=m[2].replace(/^(["'])(.*)\1$/,'$2');
}
if(settings.ONTO_LLM_MODEL!=='gemma-4-31b-it')throw new Error('Modelo distinto de Gemma solicitado');
if(!settings.ONTO_LLM_API_KEY||!settings.ONTO_LLM_BASE_URL)throw new Error('Falta configuración');
const clean=s=>String(s??'').split(settings.ONTO_LLM_API_KEY).join('[clave omitida]');
process.env.ONTO_MAX_OUTPUT_TOKENS='4096';
const visible=s=>s.replace(/<thought\b[^>]*>[\s\S]*?(?:<\/thought\s*>|$)/gi,'').replace(/<think\b[^>]*>[\s\S]*?(?:<\/think\s*>|$)/gi,'').trim();
const g=await import(pathToFileURL(path.join(src,'graphrag.ts')).href);
const {OpenAICompatibleProvider}=await import(pathToFileURL(path.join(src,'providers/openai.ts')).href);
const originalFetch=globalThis.fetch;
let usage=null,serverModel=null,lastHTTP=null;
globalThis.fetch=async(...args)=>{
 const resp=await originalFetch(...args);
 if(String(args[0]).endsWith('/chat/completions')){
  lastHTTP=resp.status;
  if(resp.ok){const j=await resp.clone().json();usage=j.usage??null;serverModel=j.model??null;}
 }
 return resp;
};
const api=async(p,payload)=>{const r=await fetch('http://127.0.0.1:8137/api'+p,payload?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}:undefined);if(!r.ok)throw new Error('Engine HTTP '+r.status);return r.json();};
const mcp={async callTool(name,args){if(name!=='onto_query')throw new Error('Solo SELECT');return JSON.stringify(await api('/query',args));}};
const corpus=JSON.parse(await fs.readFile(path.join(ROOT,'propuestas/pendientes-muse-r4/oraculos-chat/corpus_mejorado.json'),'utf8'));
const report={modelo_solicitado:settings.ONTO_LLM_MODEL,fuente:'retrieve y proveedor reales del source Studio; no certifica interfaz gráfica',inicio:new Date().toISOString(),triples_antes:(await api('/stats')).triples,intervalo_minimo_ms:65000,max_salida_tokens:4096,casos:[]};
let lastStart=0;
const save=()=>fs.writeFile(path.join(OUT,'respuestas.json'),clean(JSON.stringify(report,null,2))+'\n');
for(const c of corpus.casos.filter(c=>!process.env.ONTO_TEST_CASES||process.env.ONTO_TEST_CASES.split(',').includes(c.id))){
 const retrieved=await g.retrieve(mcp,c.pregunta,2,{model:settings.ONTO_LLM_MODEL});
 const context=g.asContext(retrieved);const est=g.estimateInputTokens({question:c.pregunta,context});
 const row={id:c.id,pregunta:c.pregunta,entrada_tokens_estimados:est,contexto_sha256:createHash('sha256').update(context).digest('hex'),intentos:[]};report.casos.push(row);
 if(est>10000){row.estado='presupuesto_excedido';await save();continue;}
 for(let retry=0;retry<2;retry++){
  const delay=Math.max(0,65000-(Date.now()-lastStart));if(delay)await new Promise(r=>setTimeout(r,delay));
  usage=null;serverModel=null;lastHTTP=null;lastStart=Date.now();
  const attempt={inicio:new Date(lastStart).toISOString()};row.intentos.push(attempt);
  try{
   const provider=new OpenAICompatibleProvider({system:g.QA_SYSTEM_PROMPT,baseURL:settings.ONTO_LLM_BASE_URL,model:settings.ONTO_LLM_MODEL,apiKey:settings.ONTO_LLM_API_KEY});
   provider.addUser(`--- RETRIEVED SUBGRAPH ---\n${context}\n--- SUBGRAPH END ---\n\nQUESTION: ${c.pregunta}`);
   const result=await provider.step([]);
   row.respuesta=visible(clean((result.text??[]).join('\n')));row.estado=row.respuesta?'respondido':'sin_respuesta_final';attempt.http=lastHTTP;attempt.modelo_servidor=serverModel;attempt.uso=usage;break;
  }catch(e){
   attempt.http=lastHTTP;attempt.error=clean(e.message).slice(0,5000);
   if(lastHTTP!==429){row.estado='error_modelo';break;}
   const match=attempt.error.match(/retry(?:\s+in|Delay["':\s]+)\s*([\d.]+)s/i);
   const wait=match?Number(match[1])*1000:65000;
   attempt.espera_sugerida_ms=wait;
   if(wait>15*60000||retry===1){row.estado='pendiente_cuota';break;}
   await save();await new Promise(r=>setTimeout(r,Math.max(65000,wait)));
  }
 }
 await save();console.log(JSON.stringify({id:row.id,estado:row.estado,http:lastHTTP,caracteres:row.respuesta?.length??0}));
 if(row.estado==='pendiente_cuota'){report.detencion='Cuota persistente: no emitir más solicitudes';break;}
}
report.fin=new Date().toISOString();report.triples_despues=(await api('/stats')).triples;await save();
