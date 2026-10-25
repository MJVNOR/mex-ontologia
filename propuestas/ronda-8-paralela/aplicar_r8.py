"""Integra sólo el lote R8 con doble aprobación exacta, código auditado y respaldo."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,copy
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
M=E/'materializacion/v003';I=E/'I-codigo/v003'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok: raise ValueError(msg)
def verify_refs(value):
    if isinstance(value,dict):
        if value.get('ruta') and value.get('sha256'):
            p=(ROOT/value['ruta']).resolve()
            require(p.is_relative_to(ROOT) and p.is_file() and sha(p)==value['sha256'],'Referencia cambió: '+value['ruta'])
        for v in value.values(): verify_refs(v)
    elif isinstance(value,list):
        for v in value: verify_refs(v)
accepted=read(M/'aceptadas.json');accepted_sha=sha(M/'aceptadas.json')
cols={r['columna'] for r in accepted['vinculos']}
require(len(cols)==28 and accepted['reglas']==[] and accepted['conceptos']=={},'Lote no es 0/28/0')
verify_refs(read(M/'congelada.json'))
for role in ('A-documental','B-tecnica'):
    a=read(E/role/'auditoria-material-v003.json')
    require(a['dictamen']=='aceptar' and a['aceptadas_sha256']==accepted_sha,'Falta aceptación exacta '+role)
    ok={r['id'] for r in a['dictamenes'] if r['tipo']=='vinculos' and r['dictamen']=='aceptar'}
    require(cols<=ok,'Aprobación incompleta '+role)
    verify_refs(a.get('referencias',[]))
code_audit=read(E/'B-tecnica/auditoria-codigo-v003.json')
require(code_audit['dictamen']=='aceptar','Código no aprobado')
verify_refs(code_audit.get('referencias',[]))
verify_refs(read(I/'congelada.json'))
test_audit=read(E/'C-codigo/auditoria-pruebas-r8.json')
require(test_audit['dictamen']=='aceptar','Regresiones R8 no aprobadas')
verify_refs(test_audit.get('referencias',[]))
for rel,h in read(E/'base.json')['sha256'].items():
    require(sha(ROOT/rel)==h,'Base cambió antes de integrar: '+rel)
backup=read(E/'respaldo-previo.json')
tests={x['ruta']:x for x in read(E/'pruebas-aplicadas.json')['cambios']}
for rel,m in backup['archivos'].items():
    expected=tests[rel]['sha256_despues'] if rel in tests else m['sha256']
    require(sha(ROOT/rel)==expected,'Cambio no previsto desde respaldo: '+rel)
require(sha(ROOT/'ontologia/semantica.json')==sha(M/'base-semantica.json'),'Base R7 no exacta')
dest=ROOT/'data/integracion-ronda-8'
config=ROOT/'ontologia/revision-ronda-8.json'
require(not dest.exists() and not config.exists(),'R8 ya existe')
require(not (ROOT/'scripts/integrar_ronda_8.py').exists() and not (ROOT/'scripts/r8_proyeccion.py').exists(),'Módulos R8 ya existen')
script_names={'integrar_ronda_8.py','r8_proyeccion.py','integrar_ronda_7.py','consolidar_semantica.py','integrar_entregas.py','integrar_ronda_2.py'}
require({p.name for p in (I/'scripts').glob('*.py')}==script_names,'Lista de scripts no exacta')
dest.mkdir()
for p in M.rglob('*'):
    if p.is_file() and p.name!='congelada.json':
        target=dest/p.relative_to(M);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
shutil.copy2(M/'congelada.json',dest/'materializacion-congelada.json')
shutil.copy2(E/'cobertura-r7.json',dest/'cobertura-r7.json')
(dest/'auditorias').mkdir()
for role,name in [('A-documental','auditoria-a'),('B-tecnica','auditoria-b')]:
    for suffix in ('.json','.md'):
        shutil.copy2(E/role/('auditoria-material-v003'+suffix),dest/'auditorias'/(name+suffix))
(dest/'codigo').mkdir()
for p in (I/'scripts').glob('*.py'): shutil.copy2(p,dest/'codigo'/p.name)
for src,name in [(E/'B-tecnica/auditoria-codigo-v003.json','auditoria-codigo.json'),(E/'C-codigo/auditoria-pruebas-r8.json','auditoria-pruebas-r8.json')]:
    shutil.copy2(src,dest/'auditorias'/name)
manifest={'ronda':8,'alcance':accepted['alcance'],'archivos':{p.relative_to(dest).as_posix():sha(p) for p in sorted(dest.rglob('*')) if p.is_file()},'insumos':{},'aceptadas_sha256':accepted_sha}
(dest/'manifiesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
record=[]
for name in sorted(script_names):
    target=ROOT/'scripts'/name
    record.append({'ruta':target.relative_to(ROOT).as_posix(),'sha256_antes':sha(target) if target.exists() else None,'sha256_despues':sha(I/'scripts'/name)})
    shutil.copy2(I/'scripts'/name,target)
for p in sorted((I/'tests').glob('test_*.py'))+[E/'codigo-coordinador/test_ronda_8.py']:
    target=ROOT/'tests'/p.name
    require(not target.exists(),'Prueba nueva ya existe: '+target.name)
    shutil.copy2(p,target)
    record.append({'ruta':target.relative_to(ROOT).as_posix(),'sha256_antes':None,'sha256_despues':sha(target)})
cfg={'evidencia':dest.relative_to(ROOT).as_posix(),'manifiesto_sha256':sha(dest/'manifiesto.json'),'aceptadas_sha256':accepted_sha,'base_sha256':sha(dest/'base-semantica.json'),'alcance':accepted['alcance']}
config.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
new=read(M/'base-semantica.json');new['vinculos_documentales_revisados'].extend(accepted['vinculos'])
target=ROOT/'ontologia/semantica.json';before=sha(target)
target.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
record.append({'ruta':target.relative_to(ROOT).as_posix(),'sha256_antes':before,'sha256_despues':sha(target)})
receipt={'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'aplicado_pendiente_regeneracion_suite_SHACL_Studio','aceptadas_sha256':accepted_sha,'manifiesto_sha256':sha(dest/'manifiesto.json'),'cambios':record,'delta':{'significados':0,'conceptos':0,'correspondencias':28},'gemma':'sin cambios'}
(E/'aplicacion.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
