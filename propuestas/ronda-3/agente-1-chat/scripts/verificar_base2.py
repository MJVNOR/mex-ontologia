"""Verificacion de base (solo lectura, motor HTTP 8137, SELECT)."""
import json
import urllib.request

URL = "http://127.0.0.1:8137/api/query"
MEX = "PREFIX mex: <https://example.org/mex-ontologi/vocab/> "

QUERIES = {
    "conceptos": MEX + "SELECT (COUNT(?c) AS ?n) WHERE { ?c a mex:ConceptoCompartido }",
    "variables_por_estado": MEX + "SELECT ?e (COUNT(DISTINCT ?v) AS ?n) WHERE { ?v a mex:VariableDocumentada; mex:estadoSemantico ?e } GROUP BY ?e ORDER BY ?e",
    "correspondencias_por_estado": MEX + "SELECT ?e (COUNT(?c) AS ?n) WHERE { ?c a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia ?e } GROUP BY ?e ORDER BY ?e",
    "total_correspondencias": MEX + "SELECT (COUNT(?c) AS ?n) WHERE { ?c a mex:CorrespondenciaSemantica }",
    "anio_matrimonio_var": MEX + 'SELECT ?v ?e WHERE { ?v mex:nombreVariableLocal "año_matrimonio"; mex:estadoSemantico ?e }',
    "anio_matrimonio_corr": MEX + 'SELECT ?est (COUNT(?m) AS ?n) WHERE { ?m mex:variableDestino ?v; mex:estadoCorrespondencia ?est . ?v mex:nombreVariableLocal "año_matrimonio" } GROUP BY ?est',
    "mat2022_revisadas": MEX + 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?map ?col ?et WHERE { ?map mex:variableDestino ?vv; mex:estadoCorrespondencia "documental_revisada"; mex:columnaOrigen ?cc . ?cc rdfs:label ?et . BIND(STR(?cc) AS ?col) FILTER(CONTAINS(STR(?et), "Matrimonios 2022")) } ORDER BY ?et',
    "predicados_nombrevar": "SELECT DISTINCT ?p WHERE { ?s ?p ?o . FILTER(CONTAINS(STR(?p), 'nombreVariableLocal')) } LIMIT 5",
}


def consultar(q):
    req = urllib.request.Request(
        URL, data=json.dumps({"query": q}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    resumen = {}
    for nombre, q in QUERIES.items():
        try:
            r = consultar(q)
            print("=" * 24, nombre)
            print(json.dumps(r, ensure_ascii=False)[:2000])
            resumen[nombre] = r
        except Exception as e:  # noqa: BLE001
            print("=" * 24, nombre, "ERROR:", str(e)[:300])
            resumen[nombre] = {"error": str(e)[:300]}
    with open("resumen_base.json", "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print("resumen guardado en resumen_base.json")
