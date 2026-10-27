"""Revisión de razonamiento y calidad sobre COPIA temporal (no toca el store real)."""
import hashlib, json, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "tools" / "open-ontologies.exe"
PORTAL = ROOT / "data" / "portal" / "portal-completo.ttl"
ONTOLOGIA = ROOT / "data" / "portal" / "ontologia-portal.ttl"
CONTENIDO = ROOT / "data" / "portal" / "contenido.ttl"


def run(args, store):
    env = dict(__import__("os").environ, OPEN_ONTOLOGIES_STORAGE_MODE="persistent")
    r = subprocess.run([str(EXE), "--no-connect", "--data-dir", str(store)] + args,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    r.check_returncode()
    return json.loads(r.stdout)


def run_file(args):
    r = subprocess.run([str(EXE), "--no-connect"] + args,
                       capture_output=True, text=True, encoding="utf-8")
    r.check_returncode()
    return json.loads(r.stdout)


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mex-rev-"))
    store = tmp / "store"
    store.mkdir()
    out = {"generado_en_utc": datetime.now(timezone.utc).isoformat(),
           "portal_sha256": sha256(PORTAL), "store_tmp": str(store)}
    out["stats"] = run(["load", str(PORTAL)], store)
    out["stats"] = run(["stats"], store)
    cert = tmp / "cert-rdfs"
    out["rdfs"] = run(["reason", "--profile", "rdfs", "--certificate", str(cert)], store)
    # ponytail: una sola carga; owl-rl mide el extra sobre lo ya materializado
    cert_owl = tmp / "cert-owl"
    out["owl_rl"] = run(["reason", "--profile", "owl-rl", "--certificate", str(cert_owl)], store)
    out["cert_rdfs"] = {"derivations": out["rdfs"]["certificate"]["derivations"],
                        "by_rule": out["rdfs"]["certificate"]["by_rule"],
                        "asserted_sha256": out["rdfs"]["certificate"]["asserted_sha256"]}
    out["cert_owl"] = {"derivations": out["owl_rl"]["certificate"]["derivations"],
                       "by_rule": out["owl_rl"]["certificate"].get("by_rule", {})}
    rep = ROOT / "reports" / f"razonamiento-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    rep.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    cal = {"generado_en_utc": out["generado_en_utc"], "portal_sha256": out["portal_sha256"]}
    cal["lint_ontologia"] = {"issues": run_file(["lint", str(ONTOLOGIA)])["issue_count"]}
    cal["lint_contenido"] = {"issues": run_file(["lint", str(CONTENIDO)])["issue_count"]}
    cal["defects_ontologia"] = run_file(["defects", str(ONTOLOGIA)])["defect_count"]
    cal["defects_portal"] = run_file(["defects", str(PORTAL)])["defect_count"]
    cal["enforce_generic"] = {k: run_file(["enforce", "generic"])[k] for k in ("compliance", "passed_rules", "total_rules")}
    v = run(["vocab-check", str(CONTENIDO)], store)
    cal["vocab_contenido_vs_completo"] = {"hallucinated": v["hallucinated_terms"],
                                          "ontology_terms": v["ontology_terms"]}
    rep2 = ROOT / "reports" / f"calidad-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    rep2.write_text(json.dumps(cal, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.rmtree(tmp, ignore_errors=True)
    print(json.dumps({"razonamiento": rep.name, "calidad": rep2.name,
                      "rdfs_inferred": out["rdfs"]["inferred_count"],
                      "owl_inferred": out["owl_rl"]["inferred_count"],
                      "lint": cal["lint_contenido"], "defects": cal["defects_portal"],
                      "vocab_hallucinated": cal["vocab_contenido_vs_completo"]["hallucinated"]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
