"""Explora predicados de significado en el grafo vivo (solo lectura)."""
import json
import urllib.request


def q(sparql):
    req = urllib.request.Request(
        "http://127.0.0.1:8137/api/query",
        data=json.dumps({"query": sparql}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


if __name__ == "__main__":
    for name, sparql in {
        "significado_preds": (
            "SELECT DISTINCT ?p (COUNT(*) AS ?n) WHERE { "
            "?s ?p ?o . FILTER(REGEX(STR(?p),'ignificado')) "
            "} GROUP BY ?p ORDER BY DESC(?n)"
        ),
        "definicion_preds": (
            "SELECT DISTINCT ?p (COUNT(*) AS ?n) WHERE { "
            "?s ?p ?o . FILTER(REGEX(STR(?p),'efinicion')) "
            "} GROUP BY ?p ORDER BY DESC(?n)"
        ),
    }.items():
        print(name, json.dumps(q(sparql), ensure_ascii=False)[:3000])
