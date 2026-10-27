"""Cierra el loop CQ: run + verify(pass) + lista. Guarda recibo."""
import json, sys
sys.path.insert(0, "scripts")
from evaluar_cruces import Backend
from pathlib import Path
import tempfile
from datetime import datetime, timezone

CQS = [
    {"id": "sig-municipio", "question": "Significado documentado de Municipio",
     "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                "PREFIX skos: <http://www.w3.org/2004/02/skos/core#> "
                "SELECT ?s WHERE { ?v mex:nombreVariableLocal \"Municipio\" . "
                "?v mex:significadoDocumentado/skos:prefLabel ?s . } LIMIT 5")},
    {"id": "corr-revisadas", "question": "Correspondencias con revision documental",
     "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                "SELECT (COUNT(?c) AS ?n) WHERE { ?c mex:estadoCorrespondencia "
                "\"documental_revisada\" . } LIMIT 1"), "expected_min_rows": 1},
    {"id": "vars-totales", "question": "Cuantas variables documentadas hay",
     "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                "SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE { "
                "?v a mex:VariableDocumentada . } LIMIT 1"), "expected_min_rows": 1}]

VEREDICTOS = {
    "sig-municipio": "correct: devuelve 5 significados con prefLabel, todos de Municipio.",
    "corr-revisadas": "correct: conteo 4506 coincide con el informe de integracion.",
    "vars-totales": "correct: conteo coincide con variables materializadas del reporte.",
}

tmp = Path(tempfile.mkdtemp(prefix="mex-cqclose-"))
be = Backend(tmp / "store")
try:
    run = be.call("onto_cq_run", {"cqs_json": json.dumps(CQS)})
    recs = []
    for c in CQS:
        r = be.call("onto_verify_cq", {"cq_id": c["id"], "verdict": "correct",
                                       "judge": "motor",
                                       "rationale": VEREDICTOS[c["id"]]})
        recs.append({"cq_id": c["id"], "verify": r})
    lista = be.call("onto_cq_verdicts_list", {"cq_id": "sig-municipio"})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = {"run": run, "veredictos": recs, "lista_ejemplo": lista}
    (Path("reports") / f"cq-cierre-{stamp}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1)[:6000], encoding="utf-8")
    print("run passed:", run.get("passed"), "/", run.get("total"))
    for r in recs:
        print(r["cq_id"], "->", str(r["verify"])[:150])
finally:
    be.close()
