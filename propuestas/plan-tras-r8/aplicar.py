"""Instala K R9 solo después de dictámenes nativos reales; no aprueba material."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,sys,tempfile
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024';K=E/'K-integracion/v001'
sys.path.insert(0,str(K/'scripts'));sys.path.insert(1,str(ROOT/'scripts'))
import integrar_ronda_9 as r9
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    require(len(sys.argv)==2,'Uso: aplicar.py ruta/auditoria-material-b.json')
    audit_paths={'a':E/'A-auditoria-semantica/v004/auditoria-material.json',
                 'b':ROOT/sys.argv[1]}
    require(not (E/'aplicacion.json').exists(),'Ya aplicado')
    dest=ROOT/r9.EVIDENCIA
    require(not dest.exists() and not (ROOT/'ontologia/revision-ronda-9.json').exists(),'R9 ya existe')
    # Rechazar cambios del staging revisado o de la base viva antes de instalar.
    for rel,h in read(K/'congelada.json')['archivos'].items():
        require(sha(ROOT/rel)==h,'Staging alterado: '+rel)
    for rel,h in read(E/'base.json')['sha256'].items():
        require(sha(ROOT/rel)==h,'Base R8 alterada: '+rel)
    for name,path in audit_paths.items():
        audit=read(path)
        require(audit['auditor']==name and audit['dictamen']=='aceptar','Dictamen no acepta')
        require(audit['aceptadas_sha256']==sha(K/'material/aceptadas.json'),'Auditoría distinta del payload')
        for rel,h in audit.get('archivos_revisados',{}).items():
            p=ROOT/rel if rel.startswith('propuestas/') or rel.startswith('docs/') else E/rel
            require(sha(p)==h,'Archivo auditado cambió: '+rel)
    # Ambos dictámenes auténticos se copian; no se usan plantillas de autor.
    with tempfile.TemporaryDirectory() as tmp:
        t=Path(tmp);folder=t/r9.EVIDENCIA
        shutil.copytree(K/'material',folder)
        for name,path in audit_paths.items():shutil.copyfile(path,folder/f'auditorias/auditoria-{name}.json')
        manifest={'format_version':1,'release':'R9',
            'archivos':{p.relative_to(folder).as_posix():sha(p) for p in folder.rglob('*') if p.is_file()}}
        write(folder/'manifiesto.json',manifest)
        config={'format_version':1,'release':'R9','evidencia':r9.EVIDENCIA,
                'manifiesto_sha256':sha(folder/'manifiesto.json')}
        (t/'ontologia').mkdir()
        shutil.copyfile(ROOT/'ontologia/semantica.json',t/'ontologia/semantica.json')
        write(t/'ontologia/revision-ronda-9.json',config)
        r9.cargar(t)
        r9.construir(read(folder/'cobertura-r8.json'),read(folder/'base-semantica.json'),r9.BASE,t)
        shutil.copytree(folder,dest)
    changes=[]
    for rel in ['scripts/integrar_ronda_9.py','scripts/consolidar_semantica.py',
                'scripts/ampliar_portal.py','tests/test_ronda_9.py']:
        source=K/rel;target=ROOT/rel
        compile(source.read_text(encoding='utf-8'),str(source),'exec')
        before=sha(target) if target.exists() else None
        shutil.copyfile(source,target)
        changes.append({'ruta':rel,'sha256_antes':before,'sha256_despues':sha(target)})
    write(ROOT/'ontologia/revision-ronda-9.json',config)
    r9.cargar(ROOT)
    write(E/'aplicacion.json',{'fecha_utc':datetime.now(timezone.utc).isoformat(),
        'material':K.relative_to(ROOT).as_posix(),'aceptadas_sha256':sha(dest/'aceptadas.json'),
        'auditorias':{n:{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for n,p in audit_paths.items()},
        'manifiesto_sha256':sha(dest/'manifiesto.json'),'cambios':changes,'nucleo_r8':'sin_cambios'})
    print(json.dumps({'estado':'instalado_pendiente_suite_publicacion_y_studio','cambios':changes}))

if __name__=='__main__':main()
