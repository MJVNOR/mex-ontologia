"""Comprueba la consulta del árbol con más de 2000 entidades y el grafo vivo."""
from datetime import datetime, timezone
import json
from pathlib import Path
import time

from rdflib import BNode, Graph, Namespace, OWL, RDF, RDFS, URIRef, Literal
from rdflib.util import from_n3
from sincronizar_studio_portal import api
from construir_catalogo import ROOT


def main():
    source = ROOT.parent / 'open-ontologies/studio/src/lib/tree-queries.ts'
    query = source.read_text(encoding='utf-8').split('= `', 1)[1].split('`;', 1)[0]
    fixture = Graph()
    ex = Namespace('https://example.org/test/')
    for i in range(2505):
        fixture.add((ex[str(i)], RDF.type, ex.TipoSinDeclaracion))
    fixture.add((ex['0'], RDF.type, OWL.NamedIndividual))
    fixture.add((ex['0'], RDFS.label, Literal('Uno', lang='es')))
    fixture.add((ex['0'], RDFS.label, Literal('One', lang='en')))
    fixture.add((ex.Clase, RDF.type, OWL.Class))
    fixture.add((ex.Ontologia, RDF.type, OWL.Ontology))
    fixture.add((ex.Propiedad, RDF.type, OWL.ObjectProperty))
    fixture.add((BNode(), RDF.type, ex.TipoSinDeclaracion))
    ids = {row.ind for row in fixture.query(query)}
    assert len(ids) == 2505 and ex['2504'] in ids, 'El árbol pierde instancias después de 2000 o sin declaración de clase'
    assert ex.Clase not in ids and ex.Ontologia not in ids and ex.Propiedad not in ids
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = ROOT / 'data/backups' / ('studio-antes-limite-' + stamp + '.ttl')
    backup.parent.mkdir(parents=True, exist_ok=True)
    api('/save', {'path': str(backup), 'format': 'turtle'})
    graph = Graph().parse(backup, format='turtle')
    excluded = {OWL.Class, RDFS.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology}
    expected = {s for s, _, c in graph.triples((None, RDF.type, None)) if c not in excluded and not isinstance(s, BNode)}
    started = time.perf_counter()
    rows = api('/query', {'query': query})['results']
    elapsed = time.perf_counter() - started
    actual = {from_n3(r['ind']) for r in rows}
    assert actual == expected, f'Faltan {len(expected - actual)} individuos; sobran {len(actual - expected)}'
    report = {'comprobado_en_utc': datetime.now(timezone.utc).isoformat(), 'consulta_fuente': str(source),
              'fixture_individuos': len(ids), 'individuos_grafo': len(expected), 'individuos_consulta_arbol': len(actual),
              'filas_con_tipos_y_etiquetas': len(rows), 'consulta_segundos': round(elapsed, 3),
              'respaldo': str(backup.relative_to(ROOT)), 'triples_respaldo': len(graph), 'conjunto_completo_verificado': True}
    (ROOT / 'reports/studio-limite-individuos.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
