import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
const ROOT='C:/Users/marti/Documents/MEX-Ontologi';
const OUT=ROOT+'/propuestas/pendientes-muse-r6/prueba-bundle';await fs.mkdir(OUT,{recursive:true});
const cfg=JSON.parse(await fs.readFile(ROOT+'/scripts/studio-gemini.json','utf8'));
const bundle=path.join(path.dirname(cfg.executable),'sidecars/agent/dist/index.js');
const env={...process.env};
for(const line of (await fs.readFile(ROOT+'/.env','utf8')).replace(/^\uFEFF/,'').split(/\r?\n/)){
 const m=line.match(/^\s*(ONTO_(?:PROVIDER|LLM_BASE_URL|LLM_MODEL|LLM_API_KEY))\s*=(.*)$/);if(m)env[m[1]]=m[2].trim().replace(/^(["'])(.*)\1$/,'$2');
}
if(env.ONTO_LLM_MODEL!=='gemma-4-31b-it')throw new Error('Modelo distinto del solicitado');
const visible=s=>String(s??'').split(env.ONTO_LLM_API_KEY).join('[clave omitida]').replace(/<(thought|think)\b[^>]*>[\s\S]*?(?:<\/\1\s*>|$)/gi,'').trim();
const stats=async()=>await(await fetch('http://127.0.0.1:8137/api/stats')).json();
const report={inicio:new Date().toISOString(),modelo:env.ONTO_LLM_MODEL,bundle,bundle_sha256:createHash('sha256').update(await fs.readFile(bundle)).digest('hex'),grafo_antes:await stats(),metodo:'Bundle instalado por STDIO; mismo motor que Studio a través de proxy MCP solo lectura; no es interacción de interfaz gráfica.',bloqueos:[],casos:[]};
const parseFrame=s=>{if(s.trim().startsWith('{'))return JSON.parse(s);for(const l of s.split('\n'))if(l.startsWith('data:')){try{return JSON.parse(l.slice(5).trim());}catch{}}return null;};
const proxy=http.createServer(async(req,res)=>{
 try{
  const chunks=[];for await(const c of req)chunks.push(c);const frame=JSON.parse(Buffer.concat(chunks).toString());
  const readonly=frame.method==='initialize'||frame.method==='tools/list'||(frame.method==='tools/call'&&['onto_query','onto_stats'].includes(frame.params?.name));
  if(!readonly){report.bloqueos.push({metodo:frame.method,herramienta:frame.params?.name});res.writeHead(200,{'Content-Type':'application/json'});res.end(JSON.stringify({jsonrpc:'2.0',id:frame.id,error:{code:-32601,message:'Prueba solo lectura: operación bloqueada'}}));return;}
  const headers={'Content-Type':'application/json',Accept:'application/json, text/event-stream'};if(req.headers['mcp-session-id'])headers['Mcp-Session-Id']=req.headers['mcp-session-id'];
  const upstream=await fetch('http://127.0.0.1:8137/mcp',{method:'POST',headers,body:JSON.stringify(frame)});
  const raw=await upstream.text();let body=raw;
  if(frame.method==='tools/list'&&upstream.ok){const f=parseFrame(raw);if(f?.result?.tools){f.result.tools=f.result.tools.filter(t=>['onto_query','onto_stats'].includes(t.name));body=JSON.stringify(f);}}
  const rh={'Content-Type':frame.method==='tools/list'?'application/json':(upstream.headers.get('content-type')??'application/json')};const session=upstream.headers.get('mcp-session-id');if(session)rh['Mcp-Session-Id']=session;
  res.writeHead(upstream.status,rh);res.end(body);
 }catch(e){res.writeHead(500,{'Content-Type':'application/json'});res.end(JSON.stringify({error:visible(e.message)}));}
});
await new Promise(r=>proxy.listen(0,'127.0.0.1',r));env.ONTO_ENGINE_URL=`http://127.0.0.1:${proxy.address().port}/mcp`;env.ONTO_CHAT_CACHE=OUT+'/cache-'+Date.now()+'.json';env.ONTO_MAX_ROUNDS='1';env.ONTO_MAX_OUTPUT_TOKENS='4096';
const child=spawn(cfg.node,[bundle],{env,cwd:OUT,windowsHide:true,stdio:['pipe','pipe','pipe']});
let buffer='',readyResolve,readyReject,active=null;
const ready=new Promise((r,j)=>{readyResolve=r;readyReject=j;});
const timer=setTimeout(()=>readyReject(new Error('Sin ready en 40s')),40000);
child.stdout.on('data',d=>{buffer+=String(d);let i;while((i=buffer.indexOf('\n'))>=0){const line=buffer.slice(0,i);buffer=buffer.slice(i+1);try{const m=JSON.parse(line);if(m.type==='text')m.content=visible(m.content);if(m.type==='error')m.error=visible(m.error);if(!active){if(m.type==='text'&&m.content.includes('Model:'))report.handshake=m.content;if(m.type==='ready'){clearTimeout(timer);readyResolve();}}else{active.events.push(m);if(m.type==='done'){active.resolve();active=null;}}}catch{}}});
child.stderr.on('data',d=>{report.stderr=(report.stderr??[]).concat(visible(String(d)).slice(0,1500));});
child.on('error',readyReject);
const save=()=>fs.writeFile(OUT+'/resultado.json',JSON.stringify(report,null,2)+'\n');
try{
 await ready;if(!report.handshake?.includes('gemma-4-31b-it'))throw new Error('Handshake no acredita Gemma');await save();console.log(JSON.stringify({handshake:report.handshake}));
 const corpus=JSON.parse(await fs.readFile(ROOT+'/propuestas/pendientes-muse-r4/chat/corpus.json','utf8'));
 const selection=process.env.ONTO_TEST_CASES?.split(',');let lastStart=0;
 for(const c of corpus.casos.filter(c=>!selection||selection.includes(c.id))){
  const delay=Math.max(0,65000-(Date.now()-lastStart));if(delay)await new Promise(r=>setTimeout(r,delay));
  const row={id:c.id,pregunta:c.pregunta,inicio:new Date().toISOString(),events:[]};report.casos.push(row);lastStart=Date.now();
  await new Promise((resolve,reject)=>{const timeout=setTimeout(()=>{active=null;reject(new Error('Timeout de caso 360s'));},360000);active={events:row.events,resolve:()=>{clearTimeout(timeout);resolve();}};child.stdin.write(JSON.stringify({type:'chat',message:c.pregunta,mode:'sketch'})+'\n');});
  row.respuesta=row.events.filter(e=>e.type==='text'&&!/^_Retrieved|^_No entity/.test(e.content??'')).map(e=>e.content).join('\n');row.errores=row.events.filter(e=>e.type==='error').map(e=>e.error);row.estado=row.errores.length?'error':row.respuesta?'respondido':'sin_respuesta';row.mutado=row.events.some(e=>e.type==='done'&&e.mutated);
  await save();console.log(JSON.stringify({id:row.id,estado:row.estado,caracteres:row.respuesta.length,mutado:row.mutado}));
 }
}catch(e){report.error=visible(e.message);console.log(JSON.stringify({error:report.error}));}
finally{clearTimeout(timer);child.kill();proxy.close();report.fin=new Date().toISOString();report.grafo_despues=await stats();report.grafo_conservado=report.grafo_antes.triples===report.grafo_despues.triples;await save();}
