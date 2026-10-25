"""Aplica únicamente una materialización R7 con dos auditorías del mismo SHA."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,shutil,copy

ROOT=Path(__file__).resolve().parents[2]
folder=(ROOT/sys.argv[1]).resolve()
material=(folder/sys.argv[2]).resolve()
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:
        raise ValueError(message)
accepted=read(material/'aceptadas.json')
accepted_sha=sha(material/'aceptadas.json')
seal=read(material/'congelada.json')
for ref in seal['archivos']:
    require(sha(ROOT/ref['ruta'])==ref['sha256'],'Materialización cambió: '+ref['ruta'])
audit_paths={role:folder/role/'auditoria-reglas-vinculos.json' for role in ('A-documental','B-tecnica')}
rule_ids={r['id'] for r in accepted['reglas']}
link_ids={r['columna'] for r in accepted['vinculos']}
for role,path in audit_paths.items():
    audit=read(path)
    require(audit.get('dictamen')=='aceptar','Falta aceptación: '+role)
    require(audit.get('aceptadas_sha256')==accepted_sha,'Aprobación no corresponde al texto: '+role)
    for kind,ids in (('reglas',rule_ids),('vinculos',link_ids)):
        approved={r['id'] for r in audit['dictamenes'] if r['tipo']==kind and r['dictamen']=='aceptar'}
        require(ids <= approved,'Aprobación incompleta: '+role+'/'+kind)
    for ref in audit.get('codigo_revisado',[])+audit.get('referencias',[]):
        require(sha(ROOT/ref['ruta'])==ref['sha256'],'Referencia auditada cambió: '+ref['ruta'])
backup=read(folder/'integracion/respaldo-previo/manifiesto-respaldo.json')
for entry in backup['copias']:
    require(sha(ROOT/entry['original'])==entry['sha256'],'Un archivo cambió desde el respaldo: '+entry['original'])
baseline=read(material/'base-semantica.json')
require(sha(material/'base-semantica.json')==sha(ROOT/'ontologia/semantica.json'),'Base no es copia byte-idéntica R6')
new=copy.deepcopy(baseline)
require(not (set(new['conceptos']) & set(accepted['conceptos'])),'Concepto nuevo colisiona con anterior')
new['reglas_descripcion_exacta'].extend(accepted['reglas'])
new['vinculos_documentales_revisados'].extend(accepted['vinculos'])
new['conceptos'].update(accepted['conceptos'])
dest=ROOT/'data/integracion-ronda-7'
config_path=ROOT/'ontologia/revision-ronda-7.json'
new_module=ROOT/'scripts/integrar_ronda_7.py'
require(not dest.exists() and not config_path.exists() and not new_module.exists(),'R7 ya existe: no sobrescribir')
dest.mkdir(parents=True)
for source in material.rglob('*'):
    if not source.is_file() or '__pycache__' in source.parts:
        continue
    rel=source.relative_to(material)
    if rel.parts[0]=='auditorias' or rel.as_posix()=='congelada.json':
        continue
    out=dest/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,out)
(dest/'auditorias').mkdir(exist_ok=True)
for role,name in (('A-documental','auditoria-a'),('B-tecnica','auditoria-b')):
    shutil.copy2(audit_paths[role],dest/'auditorias'/f'{name}.json')
    md=audit_paths[role].with_suffix('.md')
    if md.is_file():
        shutil.copy2(md,dest/'auditorias'/f'{name}.md')
manifest={'ronda':7,'alcance':'31 significados SINAC mínimos auditados y sólo sus vínculos físicos respaldados; sin vigencias ni equivalencias nuevas','materializacion_origen':material.relative_to(ROOT).as_posix(),'materializacion_congelada_sha256':sha(material/'congelada.json'),'archivos':{p.relative_to(dest).as_posix():sha(p) for p in sorted(dest.rglob('*')) if p.is_file()},'insumos':{}}
(dest/'manifiesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
config={'evidencia':dest.relative_to(ROOT).as_posix(),'manifiesto_sha256':sha(dest/'manifiesto.json'),'alcance':'Adiciones exactas R7 auditadas en ambas revisiones'}
changes=[]
for filename in ('integrar_ronda_7.py','integrar_ronda_6.py','consolidar_semantica.py'):
    target=ROOT/'scripts'/filename
    before=sha(target) if target.is_file() else None
    shutil.copy2(material/'codigo'/filename,target)
    changes.append({'ruta':target.relative_to(ROOT).as_posix(),'sha256_antes':before,'sha256_despues':sha(target)})
config_path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=ROOT/'ontologia/semantica.json'
before=sha(target)
target.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
changes.append({'ruta':target.relative_to(ROOT).as_posix(),'sha256_antes':before,'sha256_despues':sha(target)})
record={'fecha_utc':datetime.now(timezone.utc).isoformat(),'estado':'aplicado_pendiente_regeneracion_y_SHACL','aceptadas_sha256':accepted_sha,'manifiesto':(dest/'manifiesto.json').relative_to(ROOT).as_posix(),'manifiesto_sha256':sha(dest/'manifiesto.json'),'base_r6_sha256':sha(material/'base-semantica.json'),'adiciones':{'reglas':len(rule_ids),'conceptos':len(accepted['conceptos']),'vinculos':len(link_ids)},'cambios':changes,'chat_gemma':'sin cambios'}
(folder/'integracion/aplicacion.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=True))
