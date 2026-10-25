from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(E/'C-codigo/auditoria-io-atomico.json');assert a['dictamen']=='aceptar'
def verify(x):
    if isinstance(x,dict):
        if x.get('ruta') and x.get('sha256'): assert sha(ROOT/x['ruta'])==x['sha256']
        for v in x.values(): verify(v)
    if isinstance(x,list):
        for v in x: verify(v)
verify(a)
folder=E/'io-atomico/v001'
verify(read(folder/'congelada.json'))
before={x['ruta']:x['sha256_despues'] for x in read(E/'aplicacion.json')['cambios']}
backup=read(E/'respaldo-previo.json')['archivos']
changes=[]
for rel in ('scripts/guardar_rdf.py','scripts/consolidar_semantica.py','tests/test_guardar_json.py'):
    target=ROOT/rel;prior=sha(target) if target.exists() else None
    if rel in before: assert prior==before[rel]
    elif rel in backup: assert prior==backup[rel]['sha256']
    else: assert prior is None
    changes.append({'ruta':rel,'sha256_antes':prior,'sha256_despues':sha(folder/rel)})
for c in changes: shutil.copy2(folder/c['ruta'],ROOT/c['ruta'])
out=E/'io-atomico-aplicado.json';assert not out.exists()
out.write_text(json.dumps({'cambios':changes,'auditoria_sha256':sha(E/'C-codigo/auditoria-io-atomico.json'),'alcance':'Publicación JSON atómica y regresiones; sin cambio semántico.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('IO atómico aplicado con tres pruebas permanentes de regresión.')
