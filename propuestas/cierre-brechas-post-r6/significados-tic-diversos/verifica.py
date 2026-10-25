import json, hashlib

base = "."
e = json.load(open(base + "/entrega.json", encoding="utf-8"))
ids = [d["id"] for d in e["decisiones"]]
assert len(ids) == 29 and len(set(ids)) == 29, "dupes/faltantes"
a = json.load(open(base + "/asignacion.json", encoding="utf-8"))
assert set(ids) == set(c["definicion_iri"] for c in a["casos"]), "IDs no exactos"
assert all(d["estado"] == "sigue_pendiente" and "propuesta" not in d for d in e["decisiones"])
n = 0
ROOT = "../../.."
M = "propuestas/cierre-brechas-post-r6/significados-tic-diversos"
def ab(r):
    if r.startswith(M + "/"):
        return "../../.." + "/" + r
    return r if r.startswith("evidencia/") else ROOT + "/" + r
for d in e["decisiones"]:
    for v in d["evidencia"]:
        h = hashlib.sha256(open(ab(v["ruta"]), "rb").read()).hexdigest()
        assert h == v["sha256"], v["ruta"]
        n += 1
for f in e["fuentes"]:
    if f["ruta"].startswith("evidencia/"):
        h = hashlib.sha256(open(f["ruta"], "rb").read()).hexdigest()
        assert h == f["sha256"], f["ruta"]
md = ["# Entrega — significados-tic-diversos (29 IDs)",
      "Fecha (UTC): 2026-10-24. Solo se escribio en esta carpeta.",
      "29/29 sigue_pendiente, 0 propuestas. Brechas exactas por ID en entrega.json.",
      ""]
for d in e["decisiones"]:
    var = d["original"].get("variable", "?")
    suf = d["id"].split("definition/")[1]
    falta = (d["original"].get("evidencia_faltante") or "")[:110]
    md.append("- " + suf + " (" + str(var) + "): sigue_pendiente — " + falta + "...")
open(base + "/entrega.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
arch = ["entrega.json", "entrega.md", "peticiones-web.json",
        "evidencia/nueva-dgis-egresos-2026-10-24.md",
        "evidencia/nueva-tic-sonora-2026-10-24.md",
        "evidencia/nueva-diversos-2026-10-24.md",
        "verifica.py", "corrige_peticiones.py", "normaliza.py"]
files = []
for p in arch:
    files.append({"ruta": M + "/" + p, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest()})
json.dump({"archivos": files, "conteos": {"decisiones": 29, "sigue_pendiente": 29,
          "propuesta_resolucion": 0, "evidencias_verificadas": n}},
          open(base + "/cierrelisto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK arch:", len(files), "ev:", n)
