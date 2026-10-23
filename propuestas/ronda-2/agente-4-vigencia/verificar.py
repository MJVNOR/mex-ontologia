"""Verificacion reproducible (agente 4, ronda 2). Solo lectura fuera de este dir."""
import json, hashlib, pathlib, sys
BASE = pathlib.Path(__file__).parent
CENTRO = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
ok = True
def check(cond, msg):
    global ok
    print(("OK  " if cond else "FALLO ") + msg)
    if not cond: ok = False

mat = json.loads((BASE / "matriz-vigencia.json").read_text(encoding="utf-8"))
props = json.loads((BASE / "propuestas.json").read_text(encoding="utf-8"))
ckman = json.loads((BASE / "evidencia" / "ckan_manifiesto.json").read_text(encoding="utf-8"))
mani = json.loads((CENTRO / "data/integracion/manifiesto.json").read_text(encoding="utf-8"))
cob = json.loads((CENTRO / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
terr = json.loads((CENTRO / "ontologia/territorio.json").read_text(encoding="utf-8"))
a1 = json.loads((CENTRO / "data/integracion/entregas/agente-1-catalogos/propuestas.json").read_text(encoding="utf-8"))

# 1. Conteos y fechas de proceso
check(mat["total"] == 16 and len(mat["referencias"]) == 16, "matriz total 16")
check(props["total"] == 16 and len(props["propuestas"]) == 16, "propuestas total 16")
check(len(mat["fuera_de_matriz"]) == 1, "fuera de matriz 1")
check(mat["fecha_consulta_ckan_utc"] == ckman["fecha_utc"], "consulta matriz == manifiesto CKAN")
check(props.get("fecha_consulta_ckan_utc") == ckman["fecha_utc"], "consulta propuestas == manifiesto CKAN")
check("fecha_utc" not in mat, "sin fecha_utc ambigua en matriz")
check(cob["resumen"]["referencias_catalogo_con_recurso_identificado"] == 16, "cobertura 16 con recurso")
check(cob["resumen"]["referencias_catalogo_sin_resolver"] == 1, "cobertura 1 sin resolver")
check(len(terr["resoluciones"]) == 8, "territorio 8 resoluciones")
check(all(r["vigencia"] == "no_acreditada" for r in mat["referencias"]), "16 no_acreditada (sin cambios)")
check(all(p["no_aplicado"] for p in props["propuestas"]), "propuestas no aplicadas")

# 2. F1 completos vs package originales (todos los campos, microsegundos incluidos)
check(len(ckman["paquetes"]) == 11, "ckan 11 paquetes")
for r in mat["referencias"]:
    pid, rec = r["conjunto"], r["f1_ckan"]["catalogo_recurso"]
    meta = ckman["paquetes"][pid]
    f = BASE / "evidencia" / "ckan" / f"package_{pid}.json"
    check(hashlib.sha256(f.read_bytes()).hexdigest() == meta["sha256"], f"sha package {pid[:8]}")
    orig = json.loads(f.read_text(encoding="utf-8"))["result"]
    ro = next(x for x in orig["resources"] if x["id"] == rec)
    f1 = r["f1_ckan"]
    check(f1["paquete_created"] == orig["metadata_created"] and f1["paquete_modified"] == orig["metadata_modified"], f"F1 paquete {r['id']}")
    check(f1["catalogo_created"] == ro["created"] and f1["catalogo_last_modified"] == ro["last_modified"] and f1["catalogo_metadata_modified"] == ro["metadata_modified"], f"F1 recurso {r['id']}")

# 3. SHAs de catalogos de las 16 (dedup) verificados en fuentes centrales
shas = sorted({r["f1_ckan"]["catalogo_sha256"] for r in mat["referencias"]})
check(len(shas) == 6, f"6 archivos unicos: {[s[:8] for s in shas]}")
for sha in shas:
    cands = [p for p in (CENTRO / "data").rglob(sha + "*")]
    if not cands:  # territorio: archivo nombrado por recurso
        recs = [r["f1_ckan"]["catalogo_recurso"] for r in mat["referencias"] if r["f1_ckan"]["catalogo_sha256"] == sha]
        cands = [CENTRO / "data" / "territorio" / "fuentes" / (rec + ".xlsx") for rec in recs]
        cands = [p for p in cands if p.exists()]
    check(len(cands) >= 1, f"archivo central sha {sha[:8]}")
    if cands:
        check(hashlib.sha256(cands[0].read_bytes()).hexdigest() == sha, f"sha verificado {sha[:8]}")

# 4. Identidad referencia/conjunto/hoja/campo vs fuentes centrales
a1map = {p["referencia_original"]["id"]: p for p in a1["propuestas"]}
tmap = {(t["diccionario"], t["variable"]): t for t in terr["resoluciones"]}
for r in mat["referencias"]:
    rid = r["referencia_iri"].rsplit("/", 1)[-1]
    if r["id"] in ("V01","V02","V03","V04","V05","V06","V07","V08"):
        check(rid in a1map, f"{r['id']} en agente-1")
        if rid in a1map:
            p = a1map[rid]
            check(p["conjunto"] == r["conjunto"] and p["recurso"]["recurso"] == r["f1_ckan"]["catalogo_recurso"], f"{r['id']} conjunto+recurso")
            check(p["recurso"]["hoja"] in r["hoja_campo"], f"{r['id']} hoja")
    else:
        d = next((t for t in terr["resoluciones"] if t["diccionario"] == r["diccionario"] and t["variable"] == r["variable"]), None)
        check(d is not None, f"{r['id']} en territorio.json")
        if d:
            check(d["recurso"] == r["f1_ckan"]["catalogo_recurso"] and d["hoja"] in r["hoja_campo"], f"{r['id']} recurso+hoja")
            check(d["archivo_sha256"] == r["f1_ckan"]["catalogo_sha256"], f"{r['id']} sha territorio")

# 5. Facetas matriz<->propuestas iguales
for rm, p in zip(mat["referencias"], props["propuestas"]):
    check(p["id_propuesta"] == rm["id"] and p["referencia_iri"] == rm["referencia_iri"] and p["conjunto"] == rm["conjunto"], f"identidad {rm['id']}")
    check(p["facetas"]["f1_ckan"] == rm["f1_ckan"] and p["facetas"]["f2_periodos_declarados"] == rm["f2_periodos_declarados"] and p["facetas"]["f3_edicion"] == rm["f3_edicion"] and p["facetas"]["f4_aplicabilidad"] == rm["f4_aplicabilidad"], f"facetas {rm['id']}")

# 6. Evidencia externa CMPE
ext = BASE / "evidencia" / "externa" / "cmpe2016_inegi.pdf"
check(ext.exists(), "pdf cmpe existe")
if ext.exists():
    check(hashlib.sha256(ext.read_bytes()).hexdigest() == mat["evidencia_externa_cmpe2016"]["sha256"], "sha pdf cmpe")

print("RESULTADO:", "TODO OK" if ok else "HAY FALLOS")
sys.exit(0 if ok else 1)
