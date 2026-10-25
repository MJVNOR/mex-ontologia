"""Integridad offline de Q-unidades v001: sello, grafo y peticiones a W."""
import hashlib
import json
import pathlib

V = pathlib.Path(__file__).resolve().parents[1]
Q = V.parent


def test_congelada_cubre_los_archivos_sellados():
    sello = json.loads((V / "congelada.json").read_text(encoding="utf-8"))
    archivos = sello["archivos"]
    reales = {p.relative_to(V).as_posix() for p in V.rglob("*")
              if p.is_file() and p.name != "congelada.json"
              and "__pycache__" not in p.parts}
    assert reales == set(archivos)
    for ruta, sha in archivos.items():
        assert hashlib.sha256((V / ruta).read_bytes()).hexdigest() == sha, ruta


def test_grafo_solo_cualificado():
    from rdflib import Graph, RDF, URIRef

    g = Graph()
    g.parse(V / "propuesta-q-unidades.ttl", format="turtle")
    decl = list(g.subjects(RDF.type, URIRef(
        "https://example.org/mex-ontologi/vocab/UnidadDeclarada")))
    assert len(decl) == 6
    uris = {str(t) for t in set(g.subjects()) | set(g.predicates()) | set(g.objects())}
    assert not any("qudt.org/vocab/unit" in u for u in uris)
    assert not any("QuantityValue" in u or "conversion" in u.lower() for u in uris)


def test_peticiones_cubren_los_seis_casos():
    pet = json.loads((Q / "peticiones-web.json").read_text(encoding="utf-8"))
    entrega = json.loads((V / "entrega.json").read_text(encoding="utf-8"))
    assert {p["caso"] for p in pet["solicitudes"]} == {c["id"] for c in entrega["casos"]}
    assert all("QUDT 3.5.3" in p["pide"] for p in pet["solicitudes"])
