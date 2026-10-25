from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[3]
p=R/'propuestas/pendientes-muse-r4/integrador/gemma-real/respuestas.json'
d=json.loads(p.read_text(encoding='utf-8'))
for row in d['casos']:
 if 'respuesta' in row:
  s=row['respuesta']
  for tag in ['thought','think']:s=re.sub(r'<'+tag+r'\b[^>]*>[\s\S]*?(?:</'+tag+r'\s*>|$)','',s,flags=re.I)
  row['respuesta']=s.strip();row['bloques_internos_filtrados']=True
  if not row['respuesta']:row['estado']='sin_respuesta_final'
tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(p)
print([(r['id'],r['estado'],len(r.get('respuesta',''))) for r in d['casos']])
