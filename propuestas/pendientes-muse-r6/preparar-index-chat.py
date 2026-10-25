from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2]
src=Path('C:/Users/marti/Documents/open-ontologies/studio/src-tauri/sidecars/agent/index.ts')
out=R/'propuestas/pendientes-muse-r6/chat-diagnostico/codigo/index.ts'
text=src.read_text(encoding='utf-8')
replacements={
 "import { stripThoughtBlocks } from './providers/openai.js';":"import { exigirRespuestaVisible } from './providers/openai.js';",
 "return stripThoughtBlocks(result.text.join('\\n').trim());":"return exigirRespuestaVisible(result.text.join('\\n'));",
 "return runTurn(question);":"throw new Error('El modelo no devolvió una respuesta final.');",
 "return await runTurn(context);":"throw new Error('El modelo no devolvió una respuesta final.');",
}
for before,after in replacements.items():
 if text.count(before)!=1:raise ValueError('Código de base inesperado: '+before)
 text=text.replace(before,after)
out.write_text(text,encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(out.parent/'index-recibo.json').write_text(json.dumps({'antes_sha256':sha(src),'despues_sha256':sha(out),'cambios':list(replacements)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(sha(out))
