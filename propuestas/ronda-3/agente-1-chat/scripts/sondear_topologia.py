"""Sondeo de topologia recurso->columna (solo lectura)."""
import json
import urllib.request

URL = "http://127.0.0.1:8137/api/query"
P = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
     "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
     "PREFIX dct: <http://purl.org/dc/terms#> ")


def q(s):
    req = urllib.request.Request(URL, data=json.dumps({"query": s}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def v(t):
    if isinstance(t, dict):
        return t.get("value", t)
    return t


RES = "https://example.org/mex-ontologi/resource/7b8638e8-d0d5-4311-b43f-51e2d343efb1"
print("== predicados del recurso Matrimonios 2022")
r = q(P + f"SELECT DISTINCT ?p WHERE {{ <{RES}> ?p ?o }} ORDER BY ?p")
for row in r["results"]:
    print("  ", v(row["p"]))
print("== tipos y etiquetas del recurso")
r = q(P + f"SELECT ?p ?o WHERE {{ <{RES}> ?p ?o . FILTER(?p = rdfs:label || ?p = dct:title || ?p = <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) }}")
for row in r["results"]:
    print("  ", v(row["p"]), "=", str(v(row["o"]))[:150])
print("== columnas via esquemaArchivo/columna")
r = q(P + f"SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE {{ <{RES}> mex:esquemaArchivo/mex:columna ?c }}")
print("  ", r["results"])
print("== columnas cuyo IRI contiene el id del recurso")
r = q(P + "SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { ?m mex:columnaOrigen ?c . "
          "FILTER(CONTAINS(STR(?c), '7b8638e8-d0d5-4311-b43f-51e2d343efb1')) }")
print("  ", r["results"])
print("== clases de nodos con etiqueta que contiene 'Matrimonios 2022' (top 20 por tipo)")
r = q(P + "SELECT ?t (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s rdfs:label ?l ; "
          "a ?t . FILTER(CONTAINS(?l, 'Matrimonios 2022')) } GROUP BY ?t ORDER BY DESC(?n)")
for row in r["results"][:20]:
    print("  ", v(row["t"]), v(row["n"]))
print("== recursos (tipo y titulo) que contienen 'Matrimonios' en etiqueta")
r = q(P + "SELECT DISTINCT ?s ?l WHERE { ?s a mex:Recurso ; rdfs:label ?l . "
          "FILTER(CONTAINS(LCASE(?l), 'matrimonios')) } ORDER BY ?s")
for row in r["results"]:
    print("  ", v(row["s"]), "||", str(v(row["l"]))[:120])
