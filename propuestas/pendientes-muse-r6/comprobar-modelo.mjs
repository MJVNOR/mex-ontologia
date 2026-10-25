import fs from 'node:fs/promises';
const root='C:/Users/marti/Documents/MEX-Ontologi';
const settings={};for(const l of (await fs.readFile(root+'/.env','utf8')).replace(/^\uFEFF/,'').split(/\r?\n/)){const m=l.match(/^\s*(ONTO_[A-Z_]+)\s*=(.*)$/);if(m)settings[m[1]]=m[2].trim().replace(/^(["'])(.*)\1$/,'$2');}
const base=settings.ONTO_LLM_BASE_URL.replace(/\/$/,'');const model=settings.ONTO_LLM_MODEL;
if(model!=='gemma-4-31b-it')throw new Error('Modelo inesperado');
const r=await fetch(base+'/models',{headers:{Authorization:'Bearer '+settings.ONTO_LLM_API_KEY}});
const data=await r.json();const selected=(data.data??[]).find(m=>m.id.replace(/^models\//,'')===model);
const report={fecha:new Date().toISOString(),modelo:model,http:r.status,modelo_publicado:selected??null};
await fs.writeFile(root+'/propuestas/pendientes-muse-r6/modelo-disponible.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
