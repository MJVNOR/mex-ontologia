"""Puntos 2,3,4 sobre COPIAS temporales (no toca el store real)."""
import json, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "tools" / "open-ontologies.exe"
ONTO = ROOT / "data" / "portal" / "ontologia-portal.ttl"
BASE = "https://example.org/mex-ontologi/vocab/"


def sh(args, store=None, check=True):
    import os
    env = dict(os.environ, OPEN_ONTOLOGIES_STORAGE_MODE="persistent")
    cmd = [str(EXE), "--no-connect"] + (["--data-dir", str(store)] if store else []) + args
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
    if check:
        r.check_returncode()
        return json.loads(r.stdout) if r.stdout.strip() else {}
    return r


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mex-234-"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    # --- 2. ciclo ---
    s2 = tmp / "s2"; s2.mkdir()
    c2 = {}
    c2["load"] = sh(["load", str(ONTO)], s2)
    c2["version_v1"] = sh(["version", "v1-ciclo"], s2)
    c2["history_v1"] = sh(["history"], s2)
    c2["lock"] = sh(["lock", BASE + "ConjuntoDatos", BASE + "RecursoPortal",
                     "--reason", "demo ciclo"], s2)
    prop = tmp / "propuesta.ttl"
    base_txt = ONTO.read_text(encoding="utf-8")
    prop.write_text(base_txt + f'\n<{BASE}PruebaCiclo> a <http://www.w3.org/2000/01/rdf-schema#Class> ; <http://www.w3.org/2000/01/rdf-schema#label> "Prueba ciclo" .\n',
                    encoding="utf-8")
    c2["plan"] = sh(["plan", str(prop)], s2)
    c2["drift"] = sh(["drift", str(ONTO), str(prop)], s2)
    c2["apply"] = sh(["apply", "safe"], s2)
    c2["stats_aplicado"] = sh(["stats"], s2)
    c2["version_v2"] = sh(["version", "v2-ciclo"], s2)
    c2["rollback"] = sh(["rollback", "v1-ciclo"], s2)
    c2["stats_revertido"] = sh(["stats"], s2)
    (ROOT / "reports" / f"ciclo-{stamp}.json").write_text(
        json.dumps(c2, ensure_ascii=False, indent=2), encoding="utf-8")
    # --- 3. alineacion ---
    f_src = tmp / "fuente.ttl"; f_dst = tmp / "destino.ttl"
    head = "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix ex: <https://example.org/a/> .\n@prefix ey: <https://example.org/b/> .\n"
    f_src.write_text(head + 'ex:Matrimonio a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "matrimonios" .\nex:Municipio a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "municipio" .\nex:Nube a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "nube abstracta xyz" .\n', encoding="utf-8")
    f_dst.write_text(head + 'ey:Matrimonios a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "matrimonio" .\ney:Municipios a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "municipios" .\ney:Tornillo a <http://www.w3.org/2002/07/owl#Class> ; rdfs:label "tornillo industrial qrs" .\n', encoding="utf-8")
    s3 = tmp / "s3"; s3.mkdir()
    c3 = {"candidatos": sh(["align", str(f_src), str(f_dst), "--min-confidence", "0.3", "--dry-run"], s3)}
    cands = c3["candidatos"] if isinstance(c3["candidatos"], list) else c3["candidatos"].get("candidates", c3["candidatos"])
    first = (cands if isinstance(cands, list) else [])[:1]
    if first:
        c = first[0]
        src_iri = c.get("source_iri") or c.get("source") or ""
        dst_iri = c.get("target_iri") or c.get("target") or ""
        if src_iri and dst_iri:
            c3["feedback_accept"] = sh(["align-feedback", "--source", src_iri, "--target", dst_iri, "--accept"], s3)
    c3["feedback_reject"] = sh(["align-feedback", "--source", "https://example.org/a/Nube",
                                "--target", "https://example.org/b/Tornillo", "--reject"], s3)
    (ROOT / "reports" / f"alineacion-{stamp}.json").write_text(
        json.dumps(c3, ensure_ascii=False, indent=2), encoding="utf-8")
    # --- 4. recuperacion (cafe 3 triples) ---
    demo = Path(r"C:\Users\marti\AppData\Local\Temp\opencode\mex-demo-cafe")
    cafe = demo / "cafe.ttl"
    deriv = demo / "cert" / "derivations.tsv"
    s4 = tmp / "s4"; s4.mkdir()
    sh(["load", str(cafe)], s4)
    full = tmp / "slice-full.ttl"; full.write_text(cafe.read_text(encoding="utf-8"), encoding="utf-8")
    lines = [l for l in cafe.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("@prefix")]
    partial = tmp / "slice-parcial.ttl"
    partial.write_text("@prefix ex: <https://example.org/> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n" + lines[0] + "\n", encoding="utf-8")
    c4 = {}
    r = sh(["preserve", "--projection", str(full), "--goals", str(deriv),
            "--goals-skip-columns", "1", "--out", str(tmp / "p-full")], s4, check=False)
    c4["preserve_completo"] = {"exit": r.returncode, "out": r.stdout[:2000]}
    r = sh(["preserve", "--projection", str(partial), "--goals", str(deriv),
            "--goals-skip-columns", "1", "--out", str(tmp / "p-parcial")], s4, check=False)
    c4["preserve_parcial"] = {"exit": r.returncode, "out": r.stdout[:2000]}
    r = sh(["closure-diff", "--projection", str(full), "--out", str(tmp / "cd-full")], s4, check=False)
    c4["closure_diff"] = {"exit": r.returncode, "out": r.stdout[:2000]}
    (ROOT / "reports" / f"recuperacion-{stamp}.json").write_text(
        json.dumps(c4, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ciclo": f"ciclo-{stamp}.json", "alineacion": f"alineacion-{stamp}.json",
                      "recuperacion": f"recuperacion-{stamp}.json",
                      "plan_insertions": c2["plan"].get("triple_delta"),
                      "aplicado_triples": c2["stats_aplicado"].get("triples"),
                      "candidatos": cands if isinstance(cands, list) else str(cands)[:500],
                      "preserve_full_exit": c4["preserve_completo"]["exit"],
                      "preserve_parcial_exit": c4["preserve_parcial"]["exit"],
                      "closure_exit": c4["closure_diff"]["exit"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
