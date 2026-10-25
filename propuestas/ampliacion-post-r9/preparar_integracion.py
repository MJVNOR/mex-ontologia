"""Ensaya y, con --install, instala únicamente el material R10 auditado."""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ampliacion-post-r9/ejecucion-20261024'
M=E/'reanudacion-muse'
K=E/'K-codigo/v001'
PAYLOAD=E/'payload/v001'
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'scripts'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def dump(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def check_seal(folder):
    sealed=read(folder/'sello.json')
    files=sealed.get('archivos',sealed.get('artefactos',{}))
    assert files, ('sello vacío',folder)
    for rel,expected in files.items():
        if isinstance(expected,dict):
            expected=expected['sha256']
        assert sha(folder/rel)==expected,(folder,rel)

def materializar(root):
    folder=root/'data/integracion-ronda-10'
    assert not folder.exists(),folder
    shutil.copytree(PAYLOAD,folder)
    for name,role in [('a','A-auditoria'),('b','B-auditoria')]:
        dest=folder/f'auditorias/{name}.json'
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(M/f'{role}/v001/auditoria-{name}.json',dest)
    manifest={'format_version':1,'release':'R10','archivos':{
        p.relative_to(folder).as_posix():sha(p) for p in sorted(folder.rglob('*')) if p.is_file()}}
    dump(folder/'manifiesto.json',manifest)
    dump(root/'ontologia/revision-ronda-10.json',{'format_version':1,'release':'R10',
         'evidencia':'data/integracion-ronda-10','manifiesto_sha256':sha(folder/'manifiesto.json')})
    return folder

def main(install=False):
    for rel,digest in read(E/'sello-payload-previo.json')['archivos'].items():
        assert sha(PAYLOAD/rel)==digest,rel
    check_seal(K)
    for role in ['A-auditoria','B-auditoria']:
        check_seal(M/f'{role}/v001')
    code=read(M/'B-auditoria/v001/dictamen-codigo.json')
    assert code['veredicto']=='aceptar'
    for rel,digest in code['scripts'].items():
        assert sha(K/rel)==digest,rel
    base=read(E/'base.json')['sha256']
    assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in base.items()),'Base R9 cambió antes de instalar'
    assert (ROOT/'config.toml').read_bytes()==(PAYLOAD/'config-iri-base.toml').read_bytes()
    spec=importlib.util.spec_from_file_location('r10_preflight',K/'scripts/integrar_ronda_10.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix='mex-r10-real-') as tmp:
        root=Path(tmp)
        (root/'ontologia').mkdir()
        shutil.copyfile(ROOT/'config.toml',root/'config.toml')
        shutil.copyfile(ROOT/'ontologia/semantica.json',root/'ontologia/semantica.json')
        folder=materializar(root)
        module.cargar(root)
        report=read(folder/'cobertura-r9.json')
        graph,receipt,_=module.construir(report,read(root/'ontologia/semantica.json'),module.BASE,root)
        shapes=module.cargar_shapes(root)
        assert len(graph)==90 and receipt['declaraciones_unidad']==5 and receipt['formas_shacl']==6
        assert len(shapes)==73
        result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'resultado':'OK',
                'auditorias_reales':['a','b'],'aceptadas_sha256':sha(folder/'aceptadas.json'),
                'triples_extension':len(graph),'triples_shapes':len(shapes),
                'declaraciones_unidad':5,'formas_shacl':6,'base130_intacta':True,
                'codigo_integrador_sha256':sha(K/'scripts/integrar_ronda_10.py'),
                'instalado':False}
    if install:
        folder=materializar(ROOT)
        for name in ('integrar_ronda_10.py','consolidar_semantica.py','ampliar_portal.py'):
            shutil.copyfile(K/'scripts'/name,ROOT/'scripts'/name)
        result.update(instalado=True,manifiesto_sha256=sha(folder/'manifiesto.json'))
    dump(M/('instalacion.json' if install else 'preflight.json'),result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install',action='store_true')
    main(parser.parse_args().install)
