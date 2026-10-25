import { spawn } from 'node:child_process';
const child = spawn(process.execPath, ['C:/Users/marti/.codex/integrations/opencode-mcp/source-v2/opencode-mcp-d173d13d38961d350ad07f9644ddd5bd2b21ffd9/dist/index.js'], {env:{...process.env, OPENCODE_BACKEND:'v2', OPENCODE_TOOL_PROFILE:'essential'}, windowsHide:true, stdio:['pipe','pipe','pipe']});
let buffer = '', nextId = 1;
const pending = new Map();
child.stdout.on('data', chunk => {
  buffer += chunk;
  while (buffer.includes('\n')) {
    const index = buffer.indexOf('\n');
    const line = buffer.slice(0,index); buffer = buffer.slice(index+1);
    try {const message = JSON.parse(line); if (pending.has(message.id)) {pending.get(message.id)(message); pending.delete(message.id);}} catch {}
  }
});
child.stderr.on('data', () => {});
function request(method, params) {
  const id = nextId++;
  return new Promise(resolve => {pending.set(id, resolve); child.stdin.write(JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n');});
}
const timeout = setTimeout(() => {console.error('MCP verification timed out'); child.kill(); process.exit(1);},30000);
try {
 const init = await request('initialize',{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'installation-check',version:'1.0.0'}});
 if (init.error) throw new Error(JSON.stringify(init.error));
 child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
 const listing = await request('tools/list',{});
 if (listing.error) throw new Error(JSON.stringify(listing.error));
 console.log(JSON.stringify({server:init.result.serverInfo,toolCount:listing.result.tools.length,tools:listing.result.tools.map(t=>t.name)}));
 const health = await request('tools/call',{name:'opencode_setup',arguments:{directory:'C:/Users/marti/Documents/MEX-Ontologi'}});
 console.log(JSON.stringify(health.result ?? health.error));
 if (health.error || health.result?.isError) process.exitCode=1;
} catch(error) {console.error(error.message);process.exitCode=1;}
finally {clearTimeout(timeout);child.kill();}
