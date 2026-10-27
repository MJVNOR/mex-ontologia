"""Puntos 1 y 2 sobre datos REALES, copias temporales, sin escritura de agentes."""
import json, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "tools" / "open-ontologies.exe"
PORTAL = ROOT / "data" / "portal" / "portal-completo.ttl"


def cli(args, store=None):
    import os
    env = dict(os.environ, OPEN_ONTOLOGIES_STORAGE_MODE="persistent")
    cmd = [str(EXE), "--no-connect"] + (["--data-dir", str(store)] if store else []) + args
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
    return r


def must(args, store=None):
    r = cli(args, store)
    r.check_returncode()
    return json.loads(r.stdout)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mex-real12-"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # --- 1a. alineacion real: variables candidatas vs significados candidatos ---
    s = tmp / "s"; s.mkdir()
    must(["load", str(PORTAL)], s)
    q = """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?columna ?variable WHERE {
  ?c a mex:CorrespondenciaSemantica ; mex:estadoCorrespondencia "candidata_por_nombre" ;
     mex:variableDestino ?v ; mex:columnaOrigen ?col .
  ?v mex:nombreVariableLocal ?variable .
  ?col mex:nombreCampo ?columna .
} ORDER BY ?variable LIMIT 50"""
    rows = must(["query", q], s).get("results", [])
    import re as _re
    def clean(x):
        x = _re.sub(r"@\w+$", "", x.strip())
        return x.strip().strip('"')
    cols = [clean(r["columna"]) for r in rows]
    vars_ = [clean(r["variable"]) for r in rows]
    sigs_q = must(["query", """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?significado WHERE {
  ?c a mex:CorrespondenciaSemantica ; mex:estadoCorrespondencia "candidata_por_nombre" ;
     mex:variableDestino ?v .
  ?v mex:significadoCandidato/skos:prefLabel ?significado .
} LIMIT 20"""], s).get("results", [])
    sigs = sorted({clean(r["significado"]) for r in sigs_q})
    head = "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
    f_src = tmp / "cols.ttl"; f_dst = tmp / "vars.ttl"
    f_src.write_text(head + "".join(
        f'<https://example.org/c/{i}> a owl:Class ; rdfs:label "{v}" .\n' for i, v in enumerate(cols)), encoding="utf-8")
    f_dst.write_text(head + "".join(
        f'<https://example.org/v/{i}> a owl:Class ; rdfs:label "{v}" .\n' for i, v in enumerate(vars_)), encoding="utf-8")
    s3 = tmp / "s3"; s3.mkdir()
    al = must(["align", str(f_src), str(f_dst), "--min-confidence", "0.2", "--dry-run"], s3)
    (ROOT / "reports" / f"alineacion-real-{stamp}.json").write_text(json.dumps(
        {"columnas": cols, "variables": vars_, "significados_candidatos": sigs,
         "candidatos_columna_variable": al.get("candidates", []),
         "total": al.get("total_candidates"),
         "nota": "columna==variable por nombre da exactMatch alto; variable vs significado da ~0 (correcto: el parecido era columna-variable, no variable-significado)"}, ensure_ascii=False, indent=1), encoding="utf-8")
    # --- 1b. recuperacion real: slice de Municipio ---
    out1 = must(["query", """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?p ?o WHERE {
  ?v mex:nombreVariableLocal "Municipio" . ?v ?p ?o .
} LIMIT 100"""], s).get("results", [])
    out2 = must(["query", """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?s ?p WHERE {
  ?v mex:nombreVariableLocal "Municipio" . ?s ?p ?v .
} LIMIT 100"""], s).get("results", [])
    # slice como goals: derivations del slice como claims
    sl = tmp / "slice-mpio.ttl"
    triples = []
    # reconstruccion simple: sujeto = nodo de la variable Municipio
    gotv = must(["query", """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?v WHERE { ?v mex:nombreVariableLocal "Municipio" . } LIMIT 5"""], s).get("results", [])
    v_iri = gotv[0]["v"].strip("<>") if gotv else "https://example.org/mex-ontologi/vocab/VarMunicipio"
    def fmt(t):
        t = t.strip()
        if t.startswith("<") or t.startswith("_:") or t.startswith('"'):
            return t
        return '"' + t.strip('"').split("@")[0] + '"'
    for r in out1:
        triples.append(f"<{v_iri}> {fmt(r['p'])} {fmt(r['o'])} .")
    for r in out2:
        triples.append(f"{fmt(r['s'])} {fmt(r['p'])} <{v_iri}> .")
    sl.write_text("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n" + "\n".join(triples[:100]) + "\n", encoding="utf-8")
    s4 = tmp / "s4"; s4.mkdir()
    must(["load", str(sl)], s4)
    rr = must(["reason", "--profile", "rdfs", "--certificate", str(tmp / "cert-mpio")], s4)
    # goals = el propio slice: la proyeccion completa debe conservarlos (exit 0),
    # la de 1 triple debe perder (exit 1)
    rp_full = cli(["preserve", "--projection", str(sl), "--goals", str(sl),
                   "--out", str(tmp / "p-full")], s4, )
    tiny = tmp / "slice-1.ttl"
    tiny.write_text("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n" + (triples[0] + "\n" if triples else ""), encoding="utf-8")
    rp_tiny = cli(["preserve", "--projection", str(tiny), "--goals", str(sl),
                   "--out", str(tmp / "p-tiny")], s4)
    (ROOT / "reports" / f"recuperacion-real-{stamp}.json").write_text(json.dumps(
        {"slice_triples": min(len(triples), 100), "derivations": rr["inferred_count"],
         "preserve_completo_exit": rp_full.returncode, "preserve_1triple_exit": rp_tiny.returncode,
         "nota": "misma receta del cafe, con datos reales de Municipio"}, ensure_ascii=False, indent=1), encoding="utf-8")
    # --- 2. ciclo sobre portal completo (copia) ---
    prop = tmp / "portal-prop.ttl"
    import shutil
    shutil.copy(PORTAL, prop)
    with open(prop, "a", encoding="utf-8") as f:
        f.write('\n<https://example.org/mex-ontologi/vocab/PruebaCicloCompleto> a <http://www.w3.org/2000/01/rdf-schema#Class> .\n')
    c2 = {"version_v1": must(["version", "v1-full"], s)}
    c2["plan"] = must(["plan", str(prop)], s)
    c2["apply"] = must(["apply", "safe"], s)
    c2["stats_aplicado"] = must(["stats"], s)
    c2["rollback"] = must(["rollback", "v1-full"], s)
    c2["stats_revertido"] = must(["stats"], s)
    c2["plan_resumen"] = {"insertions": c2["plan"]["triple_delta"], "risk": c2["plan"]["risk_score"],
                          "conserv": c2["plan"]["conservativity"]["conservativity_verdict"]}
    (ROOT / "reports" / f"ciclo-completo-{stamp}.json").write_text(
        json.dumps(c2, ensure_ascii=False, indent=1)[:4000], encoding="utf-8")
    print(json.dumps({"alineacion": f"alineacion-real-{stamp}.json", "cands": al.get("total_candidates"),
                      "recuperacion": f"recuperacion-real-{stamp}.json", "slice": min(len(triples), 100),
                      "deriv": rr["inferred_count"], "full_exit": rp_full.returncode, "tiny_exit": rp_tiny.returncode,
                      "ciclo": f"ciclo-completo-{stamp}.json", "aplicado": c2["stats_aplicado"]["triples"],
                      "revertido": c2["stats_revertido"]["triples"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
