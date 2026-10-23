"""Prepara una copia del catálogo con etiquetas para el inspector nativo de Studio."""

from pathlib import Path
from rdflib import DCAT, DCTERMS as DCT, FOAF, Graph, Literal, OWL, RDF, RDFS, SKOS, URIRef

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "data/catalogo/studio-live.ttl"
    if output.exists():
        raise SystemExit("La copia de Studio ya existe; conserva sus ediciones antes de sustituirla.")
    g = Graph()
    for name in ("ontologia.ttl", "catalogo.ttl"):
        g.parse(ROOT / "data/catalogo" / name, format="turtle")
    for clase, label in (
        (DCAT.Catalog, "Catálogo"), (DCAT.Dataset, "Conjunto de datos"),
        (DCAT.CatalogRecord, "Registro de metadatos"), (FOAF.Organization, "Dependencia"),
        (SKOS.Concept, "Tema"), (URIRef("http://www.w3.org/ns/prov#Activity"), "Extracción de metadatos"),
    ):
        g.add((clase, RDF.type, OWL.Class))
        g.add((clase, RDFS.label, Literal(label, lang="es")))
    for predicate in (DCT.title, FOAF.name, SKOS.prefLabel):
        for subject, label in list(g.subject_objects(predicate)):
            if not any(g.objects(subject, RDFS.label)):
                g.add((subject, RDFS.label, label))
    g.serialize(output, format="turtle", encoding="utf-8")
    print(f"Copia de Studio: {output} ({len(g)} triples)")


if __name__ == "__main__":
    main()
