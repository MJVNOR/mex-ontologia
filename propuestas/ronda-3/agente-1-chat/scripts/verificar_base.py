import urllib.request, json

ENDPOINT = "http://127.0.0.1:8137/api/query"

def q(sparql):
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"query": sparql}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

queries = {
    "conceptos": "SELECT (COUNT(DISTINCT ?s) AS ?c) WHERE { ?s a <https://example.org/mex-ontologi/ConceptoCompartido> }",
    "vars_por_estado": "SELECT ?estado (COUNT(DISTINCT ?s) AS ?c) WHERE { ?s <https://example.org/mex-ontologi/estadoSemantico> ?estado } GROUP BY ?estado ORDER BY ?estado",
    "corr_por_estado": "SELECT ?estado (COUNT(*) AS ?c) WHERE { ?s <https://example.org/mex-ontologi/estadoCorrespondencia> ?estado } GROUP BY ?estado ORDER BY ?estado",
    "ns_nombrevar": "SELECT DISTINCT ?p WHERE { ?s ?p ?o . FILTER(CONTAINS(STR(?p), 'nombreVariableLocal')) } LIMIT 10",
    "corr_vocab": "SELECT DISTINCT ?p WHERE { ?m ?p ?v . FILTER(CONTAINS(STR(?p), 'variableDestino')) } LIMIT 10",
    "columna_origen": "SELECT DISTINCT ?p WHERE { ?m ?p ?v . FILTER(CONTAINS(STR(?p), 'columnaOrigen')) } LIMIT 10",
    "mat2022": "SELECT (COUNT(*) AS ?c) WHERE { ?m <https://example.org/mex-ontologi/variableDestino> ?v ; <https://example.org/mex-ontologi/columnaOrigen> ?col . FILTER(CONTAINS(STR(?col), '7b8638e8-d0d5-4311-b43f-51e2d343efb1')) }",
    "mat2022_estados": "SELECT ?e (COUNT(*) AS ?c) WHERE { ?m <https://example.org/mex-ontologi/variableDestino> ?v ; <https://example.org/mex-ontologi/columnaOrigen> ?col ; <https://example.org/mex-ontologi/estadoCorrespondencia> ?e . FILTER(CONTAINS(STR(?col), '7b8638e8-d0d5-4311-b43f-51e2d343efb1')) } GROUP BY ?e ORDER BY ?e",
}

for name, sparql in queries.items():
    print("=" * 20, name)
    try:
        print(json.dumps(q(sparql), indent=1, ensure_ascii=False)[:3000])
    except Exception as e:
        print("ERROR:", e)
