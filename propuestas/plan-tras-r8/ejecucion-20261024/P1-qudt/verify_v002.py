"""Verificacion v002 (solo lee). 1) v001 intacta 2) v002 congelada OK 3) fuentes OK."""
import json, hashlib, pathlib
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"

c1 = json.loads((MIO / "v001/congelada.json").read_text(encoding="utf-8"))
a1 = dict(c1["archivos"]); a1.pop("v001/congelada.json", None)
# v001 historica: sello con autosha imposible de mantener (rechazada para integrar); solo se preserva.
# Se comprueba que sus archivos listados siguen intactos, sin validar el autosello.
v001_ok = all(
    (MIO / r).is_file() and hashlib.sha256((MIO / r).read_bytes()).hexdigest() == h for r, h in a1.items())
print("v001_historica_intacta:", v001_ok, f"({len(a1)} archivos; autosello no validado por diseno)")

c2 = json.loads((MIO / "v002/congelada.json").read_text(encoding="utf-8"))
a2 = dict(c2["archivos"])
self_ok = "v002/congelada.json" not in a2
mal = [r for r, h in a2.items() if not (MIO / r).is_file() or hashlib.sha256((MIO / r).read_bytes()).hexdigest() != h]
reales = sorted(p.relative_to(MIO).as_posix() for p in MIO.rglob("*") if p.is_file()
                and "v001" not in p.relative_to(MIO).parts and p.name != "congelada.json")
extra = [r for r in reales if r not in a2]
print("v002_congelada:", self_ok and not mal and not extra, f"({len(a2)} archivos) mal={mal} extra={extra}")

ent = json.loads((MIO / "v002/entrega.json").read_text(encoding="utf-8"))
mf = [f["ruta"] for f in ent["fuentes"]
      if hashlib.sha256((BASE / f["ruta"]).read_bytes()).hexdigest() != f["sha256"]]
print("fuentes_ok:", not mf, mf, "| estado:", ent["estado"],
      "| casos:", [(c["id"], c["resultado"]) for c in ent["casos"]])
print("TOTAL_OK:", v001_ok and self_ok and not mal and not extra and not mf)
