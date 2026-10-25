"""Verificacion de oraculos contra el grafo vivo (solo lectura)."""
import json
import urllib.request

BASE = "http://127.0.0.1:8137"


def q(sparql):
    req = urllib.request.Request(
        BASE + "/api/query",
        data=json.dumps({"query": sparql}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


QUERIES = {
    "triples": "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }",
    "revisadas": (
        "SELECT (COUNT(DISTINCT ?m) AS ?n) WHERE { "
        "?m ?p ?o . "
        "FILTER(REGEX(STR(?p),'estadoCorrespondencia')) "
        "FILTER(STR(?o)='documental_revisada') }"
    ),
    "comparaciones2020": (
        "SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { "
        "?c a <https://example.org/mex-ontologi/vocab/ComparacionMunicipal2020> }"
    ),
    "evidencias": (
        "SELECT (COUNT(DISTINCT ?e) AS ?n) WHERE { "
        "?e a <https://example.org/mex-ontologi/vocab/EvidenciaFuenteComparacion> }"
    ),
}

if __name__ == "__main__":
    for name, sparql in QUERIES.items():
        try:
            print(name, q(sparql)["results"])
        except Exception as exc:  # noqa: BLE001
            print(name, "ERROR", str(exc)[:300])
