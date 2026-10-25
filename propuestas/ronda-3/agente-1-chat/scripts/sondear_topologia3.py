import json, urllib.request
URL = "http://127.0.0.1:8137/api/query"
P = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
     "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
     "PREFIX dct: <http://purl.org/dc/terms#> ")
RES = "https://example.org/mex-ontologi/resource/7b8638e8-d0d5-4311-b43f-51e2d343efb1"

def q(s):
    req = urllib.request.Request(URL, data=json.dumps({"query": s}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def v(t):
    if isinstance(t, dict):
        t = t.get("value", t)
    if isinstance(t, str) and t.startswith("<") and t.endswith(">"):
        return t[1:-1]
    return t

print("== columnas via esquema (conteo + lista corta)")
r = q(P + f"SELECT ?column WHERE {{ <{RES}> mex:esquema/mex:columna ?column }} ORDER BY ?column")
cols = [v(x["column"]) for x in r["results"]]
print(len(cols))
for c in cols:
    print("  ", c)
print("== mapeos de TODAS esas columnas por estado (DISTINCT)")
ids = " ".join(f"<{c}>" for c in cols)
r = q(P + "SELECT ?status (COUNT(DISTINCT ?mapping) AS ?num) WHERE { VALUES ?column { " + ids + " } "
      "?mapping mex:columnaOrigen ?column ; mex:estadoCorrespondencia ?status . } GROUP BY ?status ORDER BY ?status")
for row in r["results"]:
    print("  ", v(row["status"]), v(row["num"]))
print("== anio como filtro por propiedad (no substring)")
r = q(P + "SELECT ?s ?label WHERE { ?s a mex:RecursoCatalogado ; rdfs:label ?label . "
      "OPTIONAL { ?s mex:inicioDeclarado ?ini } OPTIONAL { ?s mex:finDeclarado ?fin } "
      "FILTER(CONTAINS(LCASE(?label), 'matrimonios') && "
      "(CONTAINS(?label, '2022') || STRSTARTS(STR(?ini), '2022') || STRSTARTS(STR(?fin), '2022'))) } ORDER BY ?s")
for row in r["results"]:
    print("  ", v(row["s"])[:90], "||", v(row["label"]))
print("== recursos matrimonio* (todos, para ver plurales/anios)")
r = q(P + "SELECT ?label WHERE { ?s a mex:RecursoCatalogado ; rdfs:label ?label . "
      "FILTER(CONTAINS(LCASE(?label), 'matrim')) } ORDER BY ?label")
for row in r["results"][:15]:
    print("  ", v(row["label"]))
