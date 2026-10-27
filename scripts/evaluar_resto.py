"""Item 2 resto: conservative_check sobre pares 'revisar'. Guarda incremental."""
import json, sys
sys.path.insert(0, "scripts")
from evaluar_cruces import Backend
from pathlib import Path
import glob, tempfile
from datetime import datetime, timezone

stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
out = Path("reports") / f"cruces-resto-{stamp}.jsonl"
tmp = Path(tempfile.mkdtemp(prefix="mex-resto-"))
d = json.load(open("data/portal/oportunidades-cruce.json", encoding="utf-8"))
pares = [p for p in d["pares"] if p.get("prioridad_revision") == "revisar"
         and p.get("evaluacion_claves")]
print("pares:", len(pares), flush=True)
be = Backend(tmp / "store")
try:
    for i, p in enumerate(pares):
        ev = p["evaluacion_claves"][0]
        try:
            ca = (ev.get("columnas_a") or [None])[0]
            cb = (ev.get("columnas_b") or [None])[0]
            if not ca or not cb:
                row = {"id": p["id"], "verdict": "sin_clave_direccionable"}
            else:
                ext = f"<{ca}> <http://www.w3.org/2002/07/owl#sameAs> <{cb}> ."
                r = be.call("onto_conservative_check",
                            {"extension_ttl": ext, "out_dir": str(tmp / p["id"][:8]),
                             "profile": "rdfs"})
                row = {"id": p["id"], "a": p["titulo_a"], "b": p["titulo_b"],
                       "familia": ev.get("familia"),
                       "verdict": r.get("conservativity_verdict"),
                       "err": r.get("_error") or r.get("_tool_error")}
        except Exception as e:
            row = {"id": p["id"], "err": str(e)[:200]}
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        if (i + 1) % 50 == 0:
            print(f"{i + 1}/{len(pares)}", flush=True)
finally:
    be.close()
print("OK " + str(out))
