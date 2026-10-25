"""Sondeo 2: titulo, esquema->columna, conjunto/dataset del recurso."""
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
    return t.get("value", t) if isinstance(t, dict) else t


RES = "https://example.org/mex-ontologi/resource/7b8638e8-d0d5-4311-b43f-51e2d343efb1"
print("== titulo e identificadores")
for pred in ["dct:title", "dct:identifier", "mex:inicioDeclarado",
             "mex:finDeclarado", "mex:urlDeclarada", "mex:regionDeclarada"]:
    try:
        r = q(P + f"SELECT ?o WHERE {{ <{RES}> {pred} ?o }}")
        for row in r.get("results", []):
            print("  ", pred, "=", str(v(row["o"]))[:160])
    except Exception as e:  # noqa: BLE001
        print("  ", pred, "ERROR", str(e)[:120])
print("== esquema->columna desde el recurso")
for row in q(P + f"SELECT ?e ?col WHERE {{ <{RES}> mex:esquema ?e . "
             "?e mex:columna ?col }} ORDER BY ?col")["results"]:
    print("  ", v(row["e"]).split("/")[-1][:40], "->", v(row["col"])[:100])
print("== columnas mapeadas del recurso (origen) con estado")
for row in q(P + "SELECT ?col ?est WHERE { ?m mex:columnaOrigen ?col ; mex:estadoCorrespondencia ?est . "
             "FILTER(CONTAINS(STR(?col), '7b8638e8-d0d5-4311-b43f-51e2d343efb1')) } ORDER BY ?col")["results"]:
    print("  ", v(row["col"])[:100], v(row["est"]))
print("== columnas observadas con etiqueta Matrimonios 2022 (todas, con IRI)")
for row in q(P + "SELECT ?col WHERE { ?col a mex:ColumnaObservada ; rdfs:label ?l . "
             "FILTER(CONTAINS(?l, 'Matrimonios 2022')) } ORDER BY ?col")["results"]:
    print("  ", v(row["col"]))
print("== recursos RecursoCatalogado con 'matrimonio' (cualquier caso) en etiqueta o titulo")
for row in q(P + "SELECT ?s ?l ?t WHERE { ?s a mex:RecursoCatalogado . "
             "{ ?s rdfs:label ?l } UNION { ?s dct:title ?t } "
             "FILTER(CONTAINS(LCASE(STR(?l)), 'matrimonio') || CONTAINS(LCASE(STR(?t)), 'matrimonio')) "
             "} ORDER BY ?s")["results"]:
    print("  ", v(row["s"])[:80], "||", str(v(row.get("l", "")))[:60], "||", str(v(row.get("t", "")))[:80])
