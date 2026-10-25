"""Comprueba consulta y SHACL de cruces en un almacén aislado del motor nativo."""
import json
import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'propuestas/ronda-3/agente-5-cruces/staging'))
from construir_catalogo import motor
from integrar_cruces_r3 import construir, BASE_DEF, STAGING


def main():
    graph, summary, _ = construir()
    shapes = HERE / 'cruces-shapes.ttl'
    shapes.write_text((HERE / 'ronda-3.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', BASE_DEF), encoding='utf-8')
    query = (STAGING / 'cruces_r3.rq').read_text(encoding='utf-8')
    rows = list(graph.query(query))
    if len(rows) != 72:
        raise ValueError('La consulta no devuelve exactamente 72 comparaciones')
    mex = Namespace(BASE_DEF + 'vocab/')
    scenarios = {'positivo': graph}
    broken = Graph() + graph
    ev = next(broken.subjects(RDF.type, mex.EvidenciaFuenteComparacion))
    broken.remove((ev, mex.shaFuente, None))
    scenarios['negativo_sin_sha'] = broken
    broken = Graph() + graph
    comp = next(broken.subjects(RDF.type, mex.ComparacionMunicipal2020))
    broken.set((comp, mex.periodoCruzado, Literal('2021')))
    scenarios['negativo_otro_periodo'] = broken
    broken = Graph() + graph
    ev = next(s for s in broken.subjects(mex.fuenteRol, Literal('grandes_grupos')))
    broken.add((ev, mex.filaOrigen, Literal(3)))
    scenarios['negativo_fila_sin_rol'] = broken
    results = {}
    for name, data in scenarios.items():
        path = HERE / (name + '.ttl')
        data.serialize(path, format='turtle', encoding='utf-8')
        store = HERE / 'store-shacl' / name
        motor(['load', str(path)], store)
        result = motor(['shacl', str(shapes)], store)
        expected = name == 'positivo'
        if result.get('conforms') is not expected:
            raise ValueError('Resultado SHACL inesperado: ' + name + ': ' + str(result))
        results[name] = result
    report = {'consulta_filas': len(rows), 'fichas': summary['fichas'],
              'comparaciones': summary['comparaciones_2020'], 'shacl_nativo': results,
              'studio_modificado': False}
    (HERE / 'control-cruces-staging.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
