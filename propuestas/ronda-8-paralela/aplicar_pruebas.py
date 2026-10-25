"""Aplica exclusivamente cinco pruebas con revisión independiente y respaldo previo."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
audit=read(E/'C-codigo/auditoria-pruebas.json')
assert audit['dictamen']=='aceptar'
backup=read(E/'respaldo-previo.json')
expected={'test_cobertura_integrada.py','test_integracion_agentes.py','test_ronda_2.py','test_ronda_3_integrada.py','test_ronda_7.py'}
refs=audit['referencias']['archivos_codigo']
assert {Path(r['ruta']).name for r in refs}==expected
for r in refs:
    assert sha(ROOT/r['ruta'])==r['sha256'],r['ruta']
assert sha(E/'T-pruebas/v002/congelada.json')==audit['referencias']['congelada_json_sha256']
changes=[]
for r in refs:
    target=ROOT/'tests'/Path(r['ruta']).name
    rel=target.relative_to(ROOT).as_posix()
    before=sha(target) if target.exists() else None
    if rel in backup['archivos']:
        assert before==backup['archivos'][rel]['sha256'],rel
    else: assert before is None
    changes.append({'ruta':rel,'sha256_antes':before,'sha256_despues':r['sha256']})
out=E/'pruebas-aplicadas.json'
assert not out.exists()
for r in refs:
    shutil.copy2(ROOT/r['ruta'],ROOT/'tests'/Path(r['ruta']).name)
out.write_text(json.dumps({'cambios':changes,'auditoria_sha256':sha(E/'C-codigo/auditoria-pruebas.json'),'estado':'aplicadas_pendiente_suite_completa'},indent=2)+'\n',encoding='utf-8')
(E/'validacion').mkdir(exist_ok=True)
print(json.dumps({'archivos':len(changes),'estado':'aplicadas'}))
