"""Control de partición, cierre y alcance de las propuestas; no aprueba semántica."""
import collections,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
S=Path(__file__).resolve().parent
ROLES=['nacimientos','defunciones','matriculas','epidemiologia','tic','diversos','presas','catalogos-web']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check():
 base=read(S/'base.json')
 for rel,h in base['huellas'].items():
  if sha(R/rel)!=h:raise ValueError('Base cambió durante investigación: '+rel)
 seen=set();result={};errors=[]
 for role in ROLES:
  f=S/role; a=read(f/'asignacion.json'); src=f/'entrega.json';marker=f/'listo.json'
  if not src.exists() or not marker.exists():result[role]={'estado':'en_curso'};continue
  d=read(src);m=read(marker)
  h=m.get('sha256_entrega',m.get('sha256',m.get('sha256_entrega_json')))
  if h!=sha(src):errors.append(role+': cierre no coincide con SHA de entrega')
  rules=d.get('reglas',[]);links=d.get('vinculos',[])
  if 'significados' in a:
   ids={x['definicion_iri']:x for x in a['significados']}
   rows=d.get('decisiones_significados',[]); got=[x.get('definicion_iri') for x in rows]
   if len(got)!=len(set(got)) or set(got)!=set(ids):errors.append(role+': decisiones no cubren exactamente asignación')
   if seen.intersection(ids):errors.append(role+': asignación solapada')
   seen.update(ids)
   proposed={x['definicion_iri'] for x in rows if x.get('decision')=='proponer'}
   targets=[]
   for rule in rules:
    ds=rule.get('definiciones',[])
    if len(ds)!=1 or ds[0] not in proposed:errors.append(role+': regla sin decisión individual propuesta');continue
    v=ids[ds[0]];targets+=ds
    for k,expected in [('conjuntos',[v['conjunto']]),('diccionarios',[v['diccionario']]),('nombres',[v['variable']]),('descripciones',[v['descripcion']])]:
     if rule.get(k)!=expected:errors.append(role+': alcance de regla distinto a fila original '+rule.get('id','?')+' / '+k)
    if rule.get('huella_fila_diccionario')!=v.get('huella_fila_diccionario'):errors.append(role+': huella de fila distinta')
    if not rule.get('limites') or not rule.get('criterio'):errors.append(role+': faltan límites/criterio')
   if set(targets)!=proposed or len(targets)!=len(set(targets)):errors.append(role+': reglas y decisiones propuestas no coinciden')
  result[role]={'estado':'entregado','sha256':sha(src),'decisiones':len(d.get('decisiones_significados',[])),'reglas':len(rules),'vinculos':len(links)}
 if all(result[x]['estado']=='entregado' for x in ROLES) and len(seen)!=179:errors.append('Partición global incompleta')
 out={'roles':result,'errores':errors,'limite':'Verifica estructura y fuentes fijadas; las aprobaciones requieren revisión documental independiente.'}
 (S/'control.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(out,ensure_ascii=False,indent=2))
 return out
if __name__=='__main__':check()
