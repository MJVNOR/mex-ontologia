import {spawn} from 'node:child_process';
import {readFileSync,writeFileSync} from 'node:fs';
const child=spawn(process.execPath,['C:/Users/marti/.codex/integrations/opencode-mcp/source-v2/opencode-mcp-d173d13d38961d350ad07f9644ddd5bd2b21ffd9/dist/index.js'],{env:{...process.env,OPENCODE_BACKEND:'v2',OPENCODE_TOOL_PROFILE:'essential'},windowsHide:true,stdio:['pipe','pipe','pipe']});
let buffer='',id=0;const pending=new Map();
child.stderr.on('data',()=>{});child.stdin.on('error',()=>{});
child.stdout.on('data',chunk=>{buffer+=chunk;while(buffer.includes('\n')){const i=buffer.indexOf('\n'),line=buffer.slice(0,i);buffer=buffer.slice(i+1);try{const m=JSON.parse(line);if(pending.has(m.id)){pending.get(m.id)(m);pending.delete(m.id);}}catch{}}});
const request=(method,params)=>new Promise(resolve=>{const k=++id;pending.set(k,resolve);child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:k,method,params})+'\n');});
const timer=setTimeout(()=>{console.error('MCP request timeout');child.kill();process.exit(1);},55000);
try{
 const init=await request('initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'ontology-mcp-coordinator',version:'1.0.0'}});
 if(init.error)throw Error(JSON.stringify(init.error));
 child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
 const spec=JSON.parse(readFileSync(process.argv[2],'utf8').replace(/^\uFEFF/,''));
 const response=await request(spec.method??'tools/call',spec.params??spec);
 const result=response.result??response.error;
 if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(result,null,2));
 if(result?.content){for(const c of result.content)if(c.type==='text')console.log(c.text);}else console.log(JSON.stringify(result));
 if(response.error||result?.isError)process.exitCode=1;
}catch(e){console.error(e.message);process.exitCode=1;}finally{clearTimeout(timer);child.kill();}
