from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(E/'C-codigo/auditoria-io-retry.json');assert a['dictamen']=='aceptar'
def verify(x):
    if isinstance(x,dict):
        if x.get('ruta') and x.get('sha256'): assert sha(ROOT/x['ruta'])==x['sha256']
        for v in x.values(): verify(v)
    if isinstance(x,list):
        for v in x: verify(v)
verify(a);folder=E/'io-atomico/v002';verify(read(folder/'congelada.json'))
prior={r['ruta']:r['sha256_despues'] for r in read(E/'io-atomico-aplicado.json')['cambios']}
changes=[]
for rel in ('scripts/guardar_rdf.py','tests/test_guardar_json.py'):
    assert sha(ROOT/rel)==prior[rel]
    changes.append({'ruta':rel,'sha256_antes':sha(ROOT/rel),'sha256_despues':sha(folder/rel)})
for c in changes: shutil.copy2(folder/c['ruta'],ROOT/c['ruta'])
out=E/'io-retry-aplicado.json';assert not out.exists()
out.write_text(json.dumps({'cambios':changes,'auditoria_sha256':sha(E/'C-codigo/auditoria-io-retry.json')},indent=2)+'\n',encoding='utf-8')
print('Reintentos Windows acotados aplicados; se conservan errores y archivos previos.')
