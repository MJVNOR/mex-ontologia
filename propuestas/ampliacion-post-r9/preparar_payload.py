"""Prepara material R10 para revisión; no instala ni inventa dictámenes."""
from pathlib import Path
import hashlib
import json
import shutil
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[2]
E = ROOT / 'propuestas/ampliacion-post-r9/ejecucion-20261024'
OUT = E / 'payload/v001'
BASE = 'https://example.org/mex-ontologi/'
MEX = Namespace(BASE+'vocab/')
PROV = Namespace('http://www.w3.org/ns/prov#')
SH = Namespace('http://www.w3.org/ns/shacl#')

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    assert not OUT.exists(), 'No sobrescribir un payload existente'
    OUT.mkdir(parents=True)
    q = read(E/'Q-unidades/v002/casos.json')['casos']
    w = {x['caso']: x for x in read(E/'W-estandares/v002/entrega.json')['resultados']}
    for rel, source in {
        'base-semantica.json': ROOT/'ontologia/semantica.json',
        'cobertura-r9.json': ROOT/'data/semantica/cobertura.json',
        'config-iri-base.toml': ROOT/'config.toml',
        'shapes/adicionales.ttl': E/'S-shacl/v001/shapes.ttl',
    }.items():
        dest = OUT/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    units, graph = [], Graph()
    graph.bind('mex', MEX)
    graph.bind('prov', PROV)
    for case in q:
        if case['id']=='Q-U01':
            continue  # Toneladas no selecciona una variante por sí misma.
        norm = w[case['id']]
        assert norm['estado']=='verificado' and norm['version']=='3.5.3'
        source = ROOT/norm['evidencia']['ruta']
        assert sha(source)==norm['evidencia']['sha256']
        dest = OUT/f"normativa/{case['id']}.txt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        dump(OUT/f"filas/{case['id']}.json", case['fila'])
        comment = 'Declaración limitada a esta definición y su literal original; sin valores, factores ni conversiones.'
        if case['id'] in {'Q-U03','Q-U04'}:
            comment += ' La variable es Unidad de Medida; no se transfiere la unidad a otras columnas ni a valores observados.'
        unit = {
            'id': case['id'], 'diccionario':case['diccionario'],
            'fila':case['indice_definicion'], 'conjunto':case['conjunto'],
            'nombre':case['variable'], 'unidad_literal':case['literal'],
            'unidad_qudt':norm['sujeto_rdf'], 'normativa_uri':norm['sujeto_rdf'],
            'normativa_sha256':norm['evidencia']['sha256'],
            'huella_fila_diccionario':case['huella_fila'], 'fuente_url':case['fuente']['url'],
            'sujeto':BASE+'declaracion-unidad/r10/'+case['id'],
            'variable':case['variable_documentada_iri'], 'definicion_iri':case['definicion_iri'],
            'etiqueta':case['variable']+': '+case['literal'], 'comentario':comment,
            'evidencia_normativa':'QUDT 3.5.3; '+norm['url']+'; SHA256 '+norm['evidencia']['sha256'],
        }
        units.append(unit)
        s = URIRef(unit['sujeto'])
        graph.add((s,RDF.type,MEX.UnidadDeclarada))
        for key,pred in [('variable',MEX.variableDocumentada),('definicion_iri',MEX.definicionFuente),('unidad_qudt',MEX.unidadQudt)]:
            graph.add((s,pred,URIRef(unit[key])))
        for key,pred in [('conjunto',MEX.conjuntoFuente),('diccionario',MEX.diccionarioFuente),('unidad_literal',MEX.unidadLiteral),('etiqueta',RDFS.label),('comentario',RDFS.comment),('evidencia_normativa',MEX.evidenciaNormativa)]:
            graph.add((s,pred,Literal(unit[key])))
        for key in ('fuente_url','normativa_uri'):
            graph.add((s,PROV.wasDerivedFrom,URIRef(unit[key])))
    (OUT/'datos').mkdir()
    graph.serialize(OUT/'datos/unidades.ttl', format='turtle', encoding='utf-8')
    shapes = Graph().parse(OUT/'shapes/adicionales.ttl', format='turtle')
    ids = sorted(str(s).rsplit('/',1)[-1] for s in shapes.subjects(RDF.type,SH.NodeShape))
    assert len(units)==5 and len(ids)==6
    accepted = {'format_version':1,'release':'R10','release_base':'R9',
                'unidades':units,'formas':[{'id':x} for x in ids],
                'archivos_instalables':{'datos':sha(OUT/'datos/unidades.ttl'),
                                       'shapes':sha(OUT/'shapes/adicionales.ttl')}}
    dump(OUT/'aceptadas.json', accepted)
    dump(E/'payload-origenes.json', {'payload':'payload/v001','aprobacion':'pendiente_dos_dictamenes',
        'aceptadas_sha256':sha(OUT/'aceptadas.json'),
        'origenes':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [
            E/'Q-unidades/v002/casos.json',E/'Q-unidades/v002/congelada.json',
            E/'W-estandares/v002/entrega.json',E/'W-estandares/v002/congelada.json',
            E/'S-shacl/v001/shapes.ttl',E/'S-shacl/v001/sello.json']}})
    print(json.dumps({'unidades':len(units),'formas':len(ids),'triples_datos':len(graph),
                      'aceptadas_sha256':sha(OUT/'aceptadas.json')}))

if __name__=='__main__':
    main()
