from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[3];S=R/'propuestas/pendientes-muse-r5';D=R/'data/integracion-ronda-5-web'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 if D.exists():raise ValueError('Seguimiento web ya fijado; no repetir')
 source=S/'catalogos-web';marker=read(source/'listo-seguimiento.json')
 for rel,h in marker['sha_archivos'].items():
  if sha(source/rel)!=h:raise ValueError('Cierre web no coincide: '+rel)
 for p in source.rglob('*.pdf'):
  if not p.read_bytes().startswith(b'%PDF-'):raise ValueError('Documento no es PDF auténtico: '+str(p))
 copies={}
 for p in source.rglob('*'):
  if p.is_file() and p.suffix.lower() in {'.json','.md','.pdf'}:copies['investigacion/'+p.relative_to(source).as_posix()]=p
 for role,names in [('matriculas',['adenda-web.json','adenda-web.md']),('diversos',['solicitudes-publicador.json','solicitudes-publicador.md'])]:
  for name in names:
   p=S/role/name
   if not p.exists():raise ValueError('Falta adenda final: '+str(p))
   copies[role+'/'+name]=p
 for rel,p in copies.items():
  dest=D/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 manifest={'alcance':'Investigación ampliada y borradores; no promueve significados ni acredita vigencia por sí sola.','documentos_pdf':len(list(D.rglob('*.pdf'))),'respuestas_web':len(read(source/'respuestas_web.json')['respuestas']),'solicitudes_unicas':33,'archivos':{rel:sha(D/rel) for rel in copies}}
 (D/'manifiesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'archivos':len(copies),'pdf':manifest['documentos_pdf'],'manifiesto_sha256':sha(D/'manifiesto.json')}))
if __name__=='__main__':main()
