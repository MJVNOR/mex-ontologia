"""Cuenta sujetos/objetos distintos para el oraculo 1212 (solo lectura)."""
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


V = "https://example.org/mex-ontologi/vocab/"
if __name__ == "__main__":
    for name, sparql in {
        "sigdoc_sujetos": (
            "SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { "
            f"?s <{V}significadoDocumentado> ?o }}"
        ),
        "sigdoc_objetos": (
            "SELECT (COUNT(DISTINCT ?o) AS ?n) WHERE { "
            f"?s <{V}significadoDocumentado> ?o }}"
        ),
        "defvars_distintas": (
            "SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE { "
            f"?v <{V}definicionVariable> ?d }}"
        ),
        "deforig_distintas": (
            "SELECT (COUNT(DISTINCT ?d) AS ?n) WHERE { "
            f"?s <{V}definicionOriginal> ?d }}"
        ),
    }.items():
        print(name, q(sparql)["results"])
