"""Evaluacion determinista C05/C06 contra el motor vivo (solo lectura, sin modelos).

Replica las formas de consulta que emite el codigo parchado
(overview nativo GROUP BY + ambito por recurso paginado) y guarda evidencia.
"""
import json
import pathlib
import urllib.request

URL = "http://127.0.0.1:8137/api/query"
P = "PREFIX dcus: <https://w3id.org/dcat-us-demo#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
OUT = pathlib.Path(__file__).resolve().parent.parent / "evidencia"
OUT.mkdir(parents=True, exist_ok=True)


def select(sparql):
    req = urllib.request.Request(
        URL, data=json.dumps({"query": sparql}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read())


def select_all(body, marker=""):
    rows = []
    offset = 0
    while True:
        page = select(f"{P}\n{marker}\n{body}\nLIMIT 200 OFFSET {offset}")["results"]
        rows.extend(page)
        if len(page) < 200:
            return rows, offset // 200 + 1
        offset += 200


def val(term):
    if isinstance(term, dict):
        return term.get("value", term)
    if term.startswith("<") and term.endswith(">"):
        return term[1:-1]
    if term.startswith('"'):
        try:
            return json.loads(term.split("@")[0].split("^^")[0])
        except Exception:
            return term
    return term


def S(marker, body):
    return f"{P}\n{marker}\n{body}"


evidencia = {}

# C06: overview global nativo
overview = select(S("# correspondence-status-overview",
    "SELECT ?status (COUNT(?mapping) AS ?n) WHERE { "
    "?mapping ?p ?status . FILTER(REGEX(STR(?p), \"[/#]estadoCorrespondencia$\")) "
    "} GROUP BY ?status ORDER BY ?status"))
conteos = {val(r["status"]): int(val(r["n"])) for r in overview["results"]}
evidencia["C06_overview"] = conteos
print("C06 overview:", conteos, "total:", sum(conteos.values()))
assert sum(conteos.values()) == 960, conteos
assert set(conteos) == {"ambigua_por_nombre", "candidata_por_nombre", "documental_revisada"}, conteos

# C05: columnas del recurso por etiqueta (anio + palabra no generica)
cols, paginas = select_all(
    "SELECT DISTINCT ?column ?label WHERE { ?column rdfs:label ?label . "
    "FILTER(CONTAINS(LCASE(STR(?label)), \"matrimonios\") && CONTAINS(STR(?label), \"2022\")) "
    "} ORDER BY ?column ?label", marker="# resource-columns")
evidencia["C05_columnas_mat2022"] = [val(c["column"]) for c in cols]
print("C05 columnas Matrimonios 2022:", len(cols), "paginas:", paginas)

ns_rows = select(S("# correspondence-namespace",
    "SELECT DISTINCT ?p WHERE { ?mapping ?p ?status . "
    "FILTER(REGEX(STR(?p), \"[/#]estadoCorrespondencia$\")) } LIMIT 5"))
ns = val(ns_rows["results"][0]["p"])[:-len("estadoCorrespondencia")]
print("namespace descubierto:", ns)
ids = " ".join(f"<{val(c['column'])}>" for c in cols)
conteo_rec = select(S("# resource-status-counts",
    f"SELECT ?status (COUNT(?mapping) AS ?n) WHERE {{ VALUES ?column {{ {ids} }} "
    f"?mapping <{ns}columnaOrigen> ?column ; <{ns}estadoCorrespondencia> ?status . "
    "} GROUP BY ?status ORDER BY ?status"))
talleres = {val(r["status"]): int(val(r["n"])) for r in conteo_rec["results"]}
evidencia["C05_conteos_recurso"] = talleres
print("C05 conteos recurso:", talleres)

det, paginas_det = select_all(
    "SELECT DISTINCT ?mapping ?column ?label ?status WHERE { "
    f"VALUES ?column {{ {ids} }} "
    f"?mapping <{ns}columnaOrigen> ?column ; <{ns}estadoCorrespondencia> ?status . "
    "OPTIONAL { ?column rdfs:label ?label } } ORDER BY ?mapping ?column ?label ?status",
    marker="# resource-mapping-rows")
evidencia["C05_mapeos"] = [
    {"mapping": val(d["mapping"]), "column": val(d["column"]),
     "label": val(d.get("label", "")), "status": val(d["status"])} for d in det]
print("C05 mapeos:", len(det), "paginas:", paginas_det)
rev = [d for d in det if val(d["status"]) == "documental_revisada"]
print("C05 revisadas:", len(rev))
assert len(rev) >= 4, "se esperaban al menos los 4 mapeos revisados de Matrimonios 2022"

# Negativo: filtro sin coincidencias -> cero acotado, no ausencia global
nada, _ = select_all(
    "SELECT DISTINCT ?column ?label WHERE { ?column rdfs:label ?label . "
    "FILTER(CONTAINS(LCASE(STR(?label)), \"matrimonios\") && CONTAINS(STR(?label), \"1999\")) "
    "} ORDER BY ?column ?label", marker="# resource-columns")
evidencia["C05negativo_1999_columnas"] = len(nada)
print("negativo 1999 columnas:", len(nada))
assert nada == []

# Estados de variables (tallaje separado del de correspondencias)
var_est = select(S("# variable-status-overview",
    "SELECT ?status (COUNT(DISTINCT ?variable) AS ?n) WHERE { "
    "?variable ?p ?status . FILTER(REGEX(STR(?p), \"[/#]estadoSemantico$\")) "
    "} GROUP BY ?status ORDER BY ?status"))
var_conteos = {val(r["status"]): int(val(r["n"])) for r in var_est["results"]}
evidencia["variables_por_estado"] = var_conteos
print("variables por estado:", var_conteos)
assert set(var_conteos) != set(conteos), "los tallajes deben ser distintos"

(OUT / "evaluacion_C05_C06.json").write_text(
    json.dumps(evidencia, ensure_ascii=False, indent=2), encoding="utf-8")
print("evidencia guardada en", OUT / "evaluacion_C05_C06.json")
print("OK determinista: recuperacion completa sin modelos")
