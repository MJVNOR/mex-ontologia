"""Fase adicional lote-4: decisiones_columnas + vinculos para asignacion-adicional.json."""
import json, hashlib, pathlib, sys
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
sys.path.insert(0, str(BASE/"scripts"))
from consolidar_semantica import columnas, interpretacion
from integrar_contenido import clave
inv = json.load(open(BASE/"data/portal/inventario.json", encoding="utf-8"))
ins = json.load(open(BASE/"data/portal/contenido-inspeccion.json", encoding="utf-8"))
prop = json.load(open(BASE/"propuestas/pendientes-muse-r4/integrador/semantica-propuesta.json", encoding="utf-8"))
base_cov = json.load(open(BASE/"propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json", encoding="utf-8"))
bvars = {v["definicion_iri"]: v for v in base_cov["variables"]}
names = {}
from collections import Counter
names = Counter((v["conjunto"], clave(v["variable"])) for v in bvars.values())
cols = {c["iri"]: c for c in columnas(inv, ins, "https://example.org/mex-ontologi/")}
ad = json.load(open(LOTE/"asignacion-adicional.json", encoding="utf-8"))
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))
# mapa definicion -> regla mia
rulemap = {}
for r in ent["reglas"]:
    assert len(r["definiciones"]) == 1
    rulemap[r["definiciones"][0]] = r
dec, vinc, pend = [], [], []
for c in ad["columnas"]:
    iri, campo, rec, conj = c["columna"], c["campo"], c["recurso"], c["conjunto"]
    di = c["definiciones_por_nombre"][0] if len(c["definiciones_por_nombre"]) == 1 else None
    col = cols.get(iri)
    v = bvars.get(di) if di else None
    r = rulemap.get(di)
    ok, why = True, ""
    if col is None: ok, why = False, "IRI fisica no reproducida en columnas() local"
    elif v is None: ok, why = False, "definicion sin fila en cobertura base"
    elif r is None: ok, why = False, "destino sin regla propuesta por lote-4"
    elif col["recurso"] != rec or col["campo"] != campo: ok, why = False, "recurso/campo fisicos distintos"
    elif col["conjunto"] != v["conjunto"] or col["conjunto"] != conj: ok, why = False, "conjunto fisico distinto del diccionario"
    elif not col["nombre_unico"] or names[(v["conjunto"], clave(v["variable"]))] != 1: ok, why = False, "nombre ambiguo en esquema/diccionario"
    elif not (v["variable"] == campo or clave(v["variable"]) == clave(campo)): ok, why = False, "campo no coincide con variable de la fila exacta"
    else:
        try:
            m = interpretacion(v["variable"], v["descripcion"], v["conjunto"], prop, v["diccionario"], v["definicion_iri"])
        except ValueError as e: m, why = None, f"conflicto de reglas: {e}"
        if m is None: ok = False
        elif m.get("estado") != "respaldada_por_definicion" or m.get("regla") != r["id"]: ok, why = False, f"propuesta no aplica ({m})"
    if ok:
        dec.append({"columna": iri, "recurso": rec, "campo": campo, "decision": "proponer",
            "definicion_iri": di,
            "motivo": f"Columna fisica verificada (archivo/hoja/posicion, unicidad, huellas) con nombre registrado en mismo conjunto/diccionario; depende explicitamente de regla propuesta {r['id']} ({r['concepto']}), aun no auditada.",
            "evidencia": [f"data/portal/contenido-inspeccion.json#recursos/{rec}",
                f"data/portal/contenido-inspeccion.json#recursos/{v['diccionario']}/definiciones",
                f"propuestas/pendientes-muse-r4/integrador/semantica-propuesta.json#reglas/{r['id']}"]})
        vinc.append({"recurso": rec, "campo": campo, "columna": iri, "diccionario": v["diccionario"],
            "concepto": r["concepto"], "descripcion": v["descripcion"],
            "huella_esquema": col["huella_esquema"], "huella_fila_diccionario": v["huella_fila_diccionario"],
            "criterio": "Vinculo columna fisica -> variable documentada del mismo conjunto: nombre con relacion registrada, descripcion que respalda cada calificador, diccionario y recurso localizados en el conjunto, unicidad en diccionario y esquema, sin alias. Alcance documental. Destino respaldado por regla propuesta aun no auditada."})
    else:
        dec.append({"columna": iri, "recurso": rec, "campo": campo, "decision": "pendiente",
            "definicion_iri": di,
            "motivo": "pendiente: " + why,
            "evidencia": [f"data/portal/contenido-inspeccion.json#recursos/{rec}",
                f"propuestas/pendientes-muse-r4/integrador/semantica-propuesta.json"]})
        pend.append({"columna": iri, "motivo": why})
print("adicional:", len(ad["columnas"]), "proponer:", sum(1 for d in dec if d["decision"]=="proponer"),
      "pendiente:", sum(1 for d in dec if d["decision"]=="pendiente"))
for p in pend: print(" PEND:", p)
json.dump({"dec": dec, "vinc": vinc}, open(LOTE/"_adicional.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
