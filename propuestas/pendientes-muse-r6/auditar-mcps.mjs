import {spawn,execFileSync} from 'node:child_process';
import {writeFileSync} from 'node:fs';
const cli='C:/Users/marti/AppData/Local/OpenAI/Codex/bin/37f54d68e5533a51/codex.exe';
const configs=JSON.parse(execFileSync(cli,['mcp','list','--json'],{encoding:'utf8',windowsHide:true}));
async function probe(c){
 const out={nombre:c.name,habilitado_config_cli:c.enabled,transporte:c.transport.type};
 const t=c.transport;
 if(t.type!=='stdio')return {...out,resultado:'no probado: transporte no stdio'};
 let command=t.command,args=t.args??[];
 if(command==='dart'){command='cmd.exe';args=['/d','/s','/c','dart mcp-server'];}
 const child=spawn(command,args,{cwd:t.cwd??process.cwd(),env:{...process.env,...(t.env??{})},stdio:['pipe','pipe','pipe'],windowsHide:true});
 let buffer='',nextId=1,timeout; const pending=new Map();
 child.stderr.on('data',()=>{});
 child.stdin.on('error',()=>{});
 child.stdout.on('data',chunk=>{
  buffer+=chunk;
  while(buffer.includes('\n')){
   const i=buffer.indexOf('\n'),line=buffer.slice(0,i);buffer=buffer.slice(i+1);
   try{const m=JSON.parse(line);if(pending.has(m.id)){pending.get(m.id).resolve(m);pending.delete(m.id);}}catch{}
  }
 });
 const request=(method,params)=>new Promise((resolve,reject)=>{
  const id=nextId++;pending.set(id,{resolve,reject});child.stdin.write(JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n');
 });
 const failed=new Promise((_,reject)=>{
  timeout=setTimeout(()=>reject(new Error('Tiempo agotado de initialize/tools-list (30s)')),30000);
  child.once('error',e=>reject(new Error(`Proceso no inició: ${e.code??e.name}`)));
  child.once('exit',code=>reject(new Error(`Proceso terminó antes de completar protocolo: ${code}`)));
 });
 try{
  const run=async()=>{
   const init=await request('initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'mcp-readonly-audit',version:'1.0.0'}});
   if(init.error)throw new Error('Error initialize: '+JSON.stringify(init.error));
   child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
   const listing=await request('tools/list',{});
   if(listing.error)throw new Error('Error tools/list: '+JSON.stringify(listing.error));
   const ts=listing.result?.tools??[];
   const si=init.result.serverInfo;
   return {...out,resultado:'initialize y tools/list correctos',servidor:{name:si.name,version:si.version},herramientas:ts.length,nombres:ts.map(x=>x.name)};
  };
  return await Promise.race([run(),failed]);
 }catch(e){return {...out,resultado:'error',error:String(e.message).slice(0,1000)};}
 finally{clearTimeout(timeout);child.kill();}
}
const results=await Promise.all(configs.map(probe));
const report={fecha_utc:new Date().toISOString(),alcance:`${configs.length} servidores configurados. Procesos de prueba efímeros: solo initialize y tools/list. Sin habilitar/deshabilitar configuración, sin llamadas de escritura, sin inferencias ni credenciales en informe.`,servidores:results};
writeFileSync(new URL('./auditoria-mcps.json',import.meta.url),JSON.stringify(report,null,2));
for(const r of results) console.log(JSON.stringify(r));
