"""Verificacion independiente del congelado P1-QUDT v001 (solo lee)."""
import json, hashlib, pathlib
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"
congel = json.loads((MIO / "v001/congelada.json").read_text(encoding="utf-8"))
arch = dict(congel["archivos"])
self_sha = arch.pop("v001/congelada.json")
canon = json.dumps({"fecha_utc": congel["fecha_utc"], "nota_autohash": congel["nota_autohash"],
                    "rol": congel["rol"], "version": congel["version"], "archivos": arch},
                   sort_keys=True, ensure_ascii=False)
ok_self = hashlib.sha256(canon.encode("utf-8")).hexdigest() == self_sha
print("autohash_ok:", ok_self)
mal = []
for rel, h in arch.items():
    p = MIO / rel
    if not p.is_file():
        mal.append((rel, "FALTA")); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != h:
        mal.append((rel, "HASH_DISTINTO"))
reales = sorted(p.relative_to(MIO).as_posix() for p in MIO.rglob("*") if p.is_file())
extra = [r for r in reales if r not in arch and r != "v001/congelada.json"]
print("archivos_revisados:", len(arch), "mismatch:", mal, "no_congelados:", extra)
ent = json.loads((MIO / "v001/entrega.json").read_text(encoding="utf-8"))
print("estado:", ent["estado"], "casos:", [c["id"] for c in ent["casos"]])
mf = []
for f in ent["fuentes"]:
    p = BASE / f["ruta"]
    if hashlib.sha256(p.read_bytes()).hexdigest() != f["sha256"]:
        mf.append(f["ruta"])
print("fuentes_con_sha_ok:", not mf, mf)
print("TOTAL_OK:", ok_self and not mal and not extra and not mf)
