"""Prepara material R9 revisable; no instala ni crea auditorías de aprobación."""
from pathlib import Path
import sys,json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
K=E/'K-integracion/v001'
sys.path.insert(0,str(K/'scripts'));sys.path.insert(1,str(ROOT/'scripts'))
import integrar_ronda_9 as r9
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
M=K/'material'
assert not (K/'material-preparado.json').exists(),'Material ya sellado para revisión'
M.mkdir(exist_ok=True)
for name in ['datos','modelo','shapes','filas','normativa','auditorias']:(M/name).mkdir(exist_ok=True)
copies={'datos/unidades.ttl':E/'P1-qudt/v003/propuesta-qudt.ttl',
        'modelo/unidades.ttl':E/'P1-qudt/v003/vocabulario.ttl',
        'shapes/exclusion-significado.ttl':E/'P4-shacl-versionado/v001/propuesta/shape-exclusion-significado.ttl',
        'base-semantica.json':ROOT/'ontologia/semantica.json',
        'cobertura-r8.json':ROOT/'data/semantica/cobertura.json'}
for rel,p in copies.items():shutil.copyfile(p,M/rel)
# RDF define Property; el borrador P1 usaba rdfs:Property, término no definido.
# Se conserva el original sellado y se revisa este payload corregido por separado.
from rdflib import Graph,RDF,RDFS,URIRef
model=Graph().parse(M/'modelo/unidades.ttl',format='turtle')
bad_property=URIRef(str(RDFS)+'Property')
for subject in list(model.subjects(RDF.type,bad_property)):
    model.remove((subject,RDF.type,bad_property))
    model.add((subject,RDF.type,RDF.Property))
model.serialize(M/'modelo/unidades.ttl',format='turtle',encoding='utf-8')
for case,p in r9.PIN.items():
    shutil.copyfile(E/f'P1-qudt/v003/fixtures/{case}-{p["nombre"]}.json',M/f'filas/{case}.json')
    term=p['unidad_qudt'].rsplit('/',1)[1]
    shutil.copyfile(E/f'W-estandares/v002/normativa/unit-{term}-evidencia.txt',M/f'normativa/{case}.txt')
accepted={'format_version':1,'release':'R9','release_base':'R8',
          'declaraciones':[{'id':case,**p} for case,p in r9.PIN.items()],
          'archivos_instalables':{k:sha(M/v) for k,v in r9.ARCHIVOS.items()}}
write(M/'aceptadas.json',accepted)
r9._datos(M,accepted,r9.read(M/'cobertura-r8.json'));r9._modelo(M)
assert sha(M/'base-semantica.json')==r9.PIN_REGLAS
assert sha(M/r9.ARCHIVOS['shapes'])==r9.SHAPE_SHA
for name in ('consolidar_semantica.py','ampliar_portal.py'):
    before=(ROOT/'scripts'/name).read_text(encoding='utf-8')
    if name=='consolidar_semantica.py':
        point="    report['huellas_entrada'] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}"
        block="""    if (ROOT / 'ontologia/revision-ronda-9.json').exists():
        from integrar_ronda_9 import construir as integrar_ronda_9
        r9_data, r9_report, r9_sources = integrar_ronda_9(report, rules, base, ROOT)
        data += r9_data
        report['integracion_ronda_9'] = r9_report
        sources.update(r9_sources)
"""
        assert before.count(point)==1
        after=before.replace(point,block+point)
    else:
        after=before.replace('from guardar_rdf import serializar_atomico','from guardar_rdf import serializar_atomico, escribir_json_atomico')
        point='    serializar_atomico(shapes, output / "shapes.ttl")'
        assert after.count(point)==1
        after=after.replace(point,"""    if (ROOT / 'ontologia/revision-ronda-9.json').exists():
        from integrar_ronda_9 import cargar_shapes
        shapes += cargar_shapes(ROOT)
"""+point)
        old='    (ROOT / "reports/portal-carga.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")'
        assert after.count(old)==1
        after=after.replace(old,'    escribir_json_atomico(report, ROOT / "reports/portal-carga.json")')
    (K/'scripts'/name).write_text(after,encoding='utf-8')
write(K/'material-preparado.json',{'format_version':1,'release_propuesta':'R9',
    'estado':'para_auditoria_no_instalado','aceptadas_sha256':sha(M/'aceptadas.json'),
    'archivos':{p.relative_to(ROOT).as_posix():sha(p) for p in K.rglob('*') if p.is_file() and '__pycache__' not in p.parts}})
print(json.dumps({'material':str(M),'aceptadas_sha256':sha(M/'aceptadas.json')}))
