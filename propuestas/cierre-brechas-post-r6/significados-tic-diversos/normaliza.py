import json, hashlib, os

M = "propuestas/cierre-brechas-post-r6/significados-tic-diversos"
NEW = {"evidencia/nueva-dgis-egresos-2026-10-24.md",
       "evidencia/nueva-diversos-2026-10-24.md",
       "evidencia/nueva-tic-sonora-2026-10-24.md"}

def b(r):
    return hashlib.sha256(open(r, "rb").read()).hexdigest()

# 1. entrega.json: normalizar SOLO rutas nuevas a relativas-al-proyecto
e = json.load(open(M + "/entrega.json", encoding="utf-8"))
n = 0
for d in e["decisiones"]:
    for v in d["evidencia"]:
        if v["ruta"] in NEW:
            v["ruta"] = M + "/" + v["ruta"]
            n += 1
for f in e["fuentes"]:
    if f["ruta"] in NEW:
        f["ruta"] = M + "/" + f["ruta"]
        n += 1
# verificar: toda ruta resuelve desde raiz y su SHA coincide
bad = []
for d in e["decisiones"]:
    for v in d["evidencia"]:
        if not os.path.exists(v["ruta"]) or b(v["ruta"]) != v["sha256"]:
            bad.append(v["ruta"])
for f in e["fuentes"]:
    if f["ruta"].startswith(M + "/") and (not os.path.exists(f["ruta"]) or b(f["ruta"]) != f["sha256"]):
        bad.append(f["ruta"])
assert not bad, bad
open(M + "/entrega.json", "w", encoding="utf-8").write(json.dumps(e, ensure_ascii=False, indent=1))
json.load(open(M + "/entrega.json", encoding="utf-8"))
print("entrega normalizada:", n, "rutas")

# 2. verifica.py: resolver rutas nuevas como relativas-al-proyecto
s = open(M + "/verifica.py", encoding="utf-8").read()
s = s.replace('ROOT = "../../.."',
              'ROOT = "../../.."\nM = "propuestas/cierre-brechas-post-r6/significados-tic-diversos"')
s = s.replace('''def ab(r):
    return r if r.startswith("evidencia/") else ROOT + "/" + r''',
              '''def ab(r):
    if r.startswith(M + "/"):
        return "../../.." + "/" + r
    return r if r.startswith("evidencia/") else ROOT + "/" + r''')
open(M + "/verifica.py", "w", encoding="utf-8").write(s)

# 3. cierrelisto.json FINAL: rutas relativas-al-proyecto + SHA bytes + congelar
arch = ["entrega.json", "entrega.md", "peticiones-web.json",
        "evidencia/nueva-dgis-egresos-2026-10-24.md",
        "evidencia/nueva-tic-sonora-2026-10-24.md",
        "evidencia/nueva-diversos-2026-10-24.md",
        "verifica.py", "corrige_peticiones.py", "normaliza.py"]
files = [{"ruta": M + "/" + p, "sha256": b(M + "/" + p)} for p in arch]
json.dump({"archivos": files,
           "conteos": {"decisiones": 29, "sigue_pendiente": 29, "propuesta_resolucion": 0,
                       "consultas_web": 5, "atendidas_negativas": 2, "pendientes": 3}},
          open(M + "/cierrelisto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# autocotejo: todo lo listado resuelve desde raiz con SHA coincidente
for f in files:
    assert os.path.exists(f["ruta"]) and b(f["ruta"]) == f["sha256"], f["ruta"]
print("cierrelisto congelado:", len(files), "archivos, autocotejo OK")
