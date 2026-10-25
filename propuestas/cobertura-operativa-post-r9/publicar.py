"""Publica la vista documental auditada sin modificar la ontología R9."""
from pathlib import Path
import json,hashlib,shutil,sys,subprocess
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/cobertura-operativa-post-r9/ejecucion-20261024'
B=E/'B-cobertura/v002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    require(len(sys.argv)==2,'Indicar el dictamen independiente final')
    audit=ROOT/sys.argv[1]
    approval=read(audit)
    require(approval.get('dictamen_global')=='ACEPTAR','Sin dictamen final aceptar')
    for rel,h in approval['aprobacion']['archivos_sha256'].items():
        require(sha(E/rel)==h,'Archivo auditado cambió: '+rel)
    require(not (E/'publicacion.json').exists(),'Ya publicado')
    for rel,h in read(E/'base.json')['sha256'].items():
        require(sha(ROOT/rel)==h,'Insumo/histórico cambió: '+rel)
    for rel,h in read(B/'congelada.json')['archivos'].items():
        require(sha(B/rel)==h,'Propuesta cambió: '+rel)
    changes=[]
    for rel in ('scripts/generar_cobertura_operativa.py','tests/test_generar_cobertura_operativa.py'):
        target=ROOT/rel;require(not target.exists(),'Archivo ya existe: '+rel)
        source=B/rel;compile(source.read_text(encoding='utf-8'),str(source),'exec')
        shutil.copyfile(source,target)
        changes.append({'ruta':rel,'sha256':sha(target)})
    outputs=['reports/cobertura-operativa-r9.json','reports/cobertura-operativa-r9.md']
    for rel in outputs:require(not (ROOT/rel).exists(),'Salida ya existe: '+rel)
    subprocess.run([sys.executable,str(ROOT/'scripts/generar_cobertura_operativa.py')],check=True,cwd=ROOT)
    for rel in outputs:
        target=ROOT/rel
        require(sha(target)==sha(B/'salida'/target.name),'Salida instalada difiere de auditada')
        changes.append({'ruta':rel,'sha256':sha(target)})
    backup=E/'respaldo-documentacion';backup.mkdir()
    for name in ('README.md','PLAN.md'):
        p=ROOT/name;shutil.copyfile(p,backup/name)
        before=sha(p);text=p.read_text(encoding='utf-8')
        text=text.replace('La suite completa pasa **204 pruebas**','El cierre R9 pasó **204 pruebas**',1)
        text+='''
## Seguimiento operativo posterior a R9

Se publicó el [reporte operativo de cobertura](reports/cobertura-operativa-r9.md),
con los estados R9 y condiciones de reapertura para todos los frentes pendientes.
Las siete preguntas documentales se conservan [en el expediente](propuestas/cobertura-operativa-post-r9/ejecucion-20261024/C-preguntas/preguntas-documentales.md), sin enviar.
La revisión de Presas no aportó evidencia nueva: su correspondencia está resuelta
desde R6 y la vigencia histórica sigue pendiente.

La [validación de este seguimiento](reports/seguimiento-operativo-post-r9.md)
conserva los recibos de pruebas y comprobación del grafo. No abre una nueva ronda semántica.
'''
        p.write_text(text,encoding='utf-8')
        changes.append({'ruta':name,'sha256_antes':before,'sha256':sha(p),'respaldo':(backup/name).relative_to(ROOT).as_posix()})
    receipt={'dictamen':{'ruta':audit.relative_to(ROOT).as_posix(),'sha256':sha(audit)},
             'version_instalada':'B-cobertura/v002','archivos':changes,'cambios_grafo':0,
             'preguntas_enviadas':0,'estado':'publicado_pendiente_suite_final'}
    (E/'publicacion.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt))

if __name__=='__main__':main()
