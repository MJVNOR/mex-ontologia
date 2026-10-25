from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
a=read(E/'C-codigo/auditoria-ajuste-tests.json')
assert a['dictamen']=='aceptar'
def verify(x):
    if isinstance(x,dict):
        if x.get('ruta') and x.get('sha256'): assert sha(ROOT/x['ruta'])==x['sha256']
        for v in x.values(): verify(v)
    if isinstance(x,list):
        for v in x: verify(v)
verify(a)
seal=read(E/'ajuste-tests/v001/congelada.json')
refs=seal['archivos'];assert {Path(x['ruta']).name for x in refs}=={'test_ronda_3_integrada.py','test_ronda_7.py'}
prior={x['ruta']:x['sha256_despues'] for x in read(E/'pruebas-aplicadas.json')['cambios']}
changes=[]
for x in refs:
    assert sha(ROOT/x['ruta'])==x['sha256']
    target=ROOT/'tests'/Path(x['ruta']).name;rel=target.relative_to(ROOT).as_posix()
    assert sha(target)==prior[rel]
    changes.append({'ruta':rel,'sha256_antes':sha(target),'sha256_despues':x['sha256']})
for x in refs: shutil.copy2(ROOT/x['ruta'],ROOT/'tests'/Path(x['ruta']).name)
out=E/'ajuste-tests-aplicado.json';assert not out.exists()
out.write_text(json.dumps({'cambios':changes,'auditoria_sha256':sha(E/'C-codigo/auditoria-ajuste-tests.json')},indent=2)+'\n',encoding='utf-8')
print('Dos llamadas de validación actualizadas; aserciones históricas conservadas.')
