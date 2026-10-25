import json, urllib.request
URL = "http://127.0.0.1:8137/api/query"
P = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
     "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ")
cols = ["https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/_id",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/a%C3%B1o_matrimonio",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/dia_matrimonio",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/edad_cty1",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/edad_cty2",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/mes_matrimonio",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/municipio",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/sexo_cty1",
        "https://example.org/mex-ontologi/column/7b8638e8-d0d5-4311-b43f-51e2d343efb1/sexo_cty2"]
ids = " ".join(f"<{c}>" for c in cols)

def raw(s):
    req = urllib.request.Request(URL, data=json.dumps({"query": s}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode()

s = (P + "SELECT ?status (COUNT(DISTINCT ?mapping) AS ?num) WHERE { VALUES ?column { " + ids + " } "
     "?mapping mex:columnaOrigen ?column ; mex:estadoCorrespondencia ?status . } GROUP BY ?status ORDER BY ?status")
print(raw(s)[:1000])
