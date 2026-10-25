"""Verificacion v003 (solo lee). v001/v002 intactas; v003 sello sin autoinclusion; fuentes OK."""
import json, hashlib, pathlib
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"

def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()

for v in ("v001", "v002"):
    c = json.loads((MIO / v / "congelada.json").read_text(encoding="utf-8"))
    a = {r: h for r, h in c["archivos"].items() if r != f"{v}/congelada.json"}
    ok = all((MIO / r).is_file() and H(MIO / r) == h for r, h in a.items())
    print(f"{v}_historica_intacta:", ok, f"({len(a)} archivos; sellos previos no revalidados)")

c3 = json.loads((MIO / "v003/congelada.json").read_text(encoding="utf-8"))
a3 = dict(c3["archivos"])
self_ok = "v003/congelada.json" not in a3
mal = [r for r, h in a3.items() if not (MIO / r).is_file() or H(MIO / r) != h]
reales = sorted(p.relative_to(MIO).as_posix() for p in MIO.rglob("*") if p.is_file()
                and "v001" not in p.relative_to(MIO).parts and "v002" not in p.relative_to(MIO).parts
                and p.name != "congelada.json")
extra = [r for r in reales if r not in a3]
print("v003_sello:", self_ok and not mal and not extra, f"({len(a3)}) mal={mal} extra={extra}")

raw = (MIO / "v003/propuesta-qudt.ttl").read_bytes()
print("bytes exactos:", "Milímetros".encode("utf-8") in raw, "Hectáreas".encode("utf-8") in raw,
      "sin_ascii_plano:", b"Milimetros" not in raw and b"Hectareas" not in raw)

ent = json.loads((MIO / "v003/entrega.json").read_text(encoding="utf-8"))
mf = [f["ruta"] for f in ent["fuentes"] if H(BASE / f["ruta"]) != f["sha256"]]
nodos = len(list(__import__("rdflib").Graph().parse(str(MIO / 'v003/propuesta-qudt.ttl'), format="turtle")
                 .query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?d WHERE { ?d a mex:UnidadDeclarada }")))
print("fuentes_ok:", not mf, mf, "| nodos_grafo:", nodos, "| estado:", ent["estado"])
print("TOTAL_OK:", self_ok and not mal and not extra and not mf and nodos == 2)
