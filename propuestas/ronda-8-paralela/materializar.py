"""Fija las propuestas M1/M2 sin dar por aprobada ninguna correspondencia."""
from pathlib import Path
import json,hashlib,shutil,sys
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
version=sys.argv[1] if len(sys.argv)>1 else 'v001'
out=E/'materializacion'/version
assert not (out/'congelada.json').exists()
(out/'fuentes').mkdir(parents=True,exist_ok=True)
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
vinculos=[];origin={};sources={}
for role in ('M1-sinac','M2-sinac'):
    folder=E/role/(version if version!='v001' and role=='M2-sinac' else 'v001')
    marker=read(folder/'congelada.json')
    for x in marker.get('archivos',[]):
        assert sha(ROOT/x['ruta'])==x['sha256']
    assert sha(folder/'entrega.json')==marker.get('entrega_json_sha256',marker.get('entrega_sha256'))
    assert sha(folder/'entrega.md')==marker['entrega_md_sha256']
    proposal=read(folder/'entrega.json')
    assert len(proposal['vinculos_propuestos'])==14
    vinculos+=proposal['vinculos_propuestos']
    for name in ('entrega.json','entrega.md','congelada.json'):
        rel='fuentes/'+role+'-'+name
        shutil.copy2(folder/name,out/rel)
    for row in proposal['vinculos_propuestos']:
        origin[row['columna']]=['fuentes/'+role+'-entrega.json','fuentes/inspeccion-contenido.json','fuentes/aceptadas-r7.json','fuentes/cobertura-r7.json']
assert len({r['columna'] for r in vinculos})==28
assert {r['columna'] for r in vinculos}==set(read(ROOT/'reports/ronda-7.json')['candidatas_nuevas'])
cov=read(E/'cobertura-r7.json')
variables={r['definicion_iri']:r for r in cov['variables']}
mapping={r['columna']:r for r in cov['correspondencias']}
for row in vinculos:
    variable=variables[row['definicion_iri']]
    assert variable['estado']=='respaldada_por_definicion'
    assert mapping[row['columna']]['variable']==variable['iri']
    assert row['concepto']==variable['concepto']
    assert row['huella_fila_diccionario']==variable['huella_fila_diccionario']
    assert row['diccionario']==variable['diccionario']
    assert row['descripcion']==variable['descripcion']
    assert row['criterio']
for src,dest in [('ontologia/semantica.json','base-semantica.json'),('data/portal/contenido-inspeccion.json','fuentes/inspeccion-contenido.json'),('data/integracion-ronda-7/aceptadas.json','fuentes/aceptadas-r7.json'),('reports/ronda-7.json','fuentes/recibo-r7.json'),('data/integracion-ronda-7/manifiesto.json','fuentes/manifiesto-r7.json')]:
    shutil.copy2(ROOT/src,out/dest)
shutil.copy2(E/'cobertura-r7.json',out/'fuentes/cobertura-r7.json')
accepted={'reglas':[],'conceptos':{},'vinculos':sorted(vinculos,key=lambda r:r['columna']),'origenes':origin,'resumen':{'significados_nuevos':0,'conceptos_nuevos':0,'vinculos_nuevos':28,'significados_respaldados':1423,'conceptos_totales':1106,'correspondencias_revisadas':4506,'correspondencias_candidatas':17,'ambiguas':0},'alcance':'Sólo 28 correspondencias físicas SINAC con significado respaldado R7; sin reglas, conceptos, códigos, vigencias, joins ni identidad de catálogos nuevos.'}
write(out/'aceptadas.json',accepted)
write(out/'congelada.json',{'aceptadas_sha256':sha(out/'aceptadas.json'),'archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file()]})
print(json.dumps({'aceptadas_sha256':sha(out/'aceptadas.json'),'vinculos':len(vinculos),'carpeta':out.relative_to(ROOT).as_posix()}))
