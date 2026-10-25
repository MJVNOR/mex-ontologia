"""Correccion devolucion integrador (territorio-economia).

1. huella_fila_diccionario a nivel top-level de cada regla (valor real
   verificado: evidencia == decision == cobertura; no se re-hashea nada).
2. Slugs/etiquetas 'proyectada' -> literal 'reconstruida y ajustada'
   (quinquenios) o literal exacto (grandes grupos); limite explicito de
   no homologacion. Sin colisiones; decisiones y reglas actualizadas.
Solo escribe en TU carpeta.
"""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
ENTREGA = AQUI / "entrega.json"

FALLOS = []


def ok(cond, msg):
    if not cond:
        FALLOS.append(msg)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


e = json.load(open(ENTREGA, encoding="utf-8"))
cob = {x["definicion_iri"]: x for x in json.load(open(ROOT / "data/semantica/cobertura.json", encoding="utf-8"))["variables"]}
dec = {d["definicion_iri"]: d for d in e["decisiones"]}
sem = json.load(open(ROOT / "ontologia/semantica.json", encoding="utf-8"))

# ---- 1. huella top-level verificada ----
for r in e["reglas"]:
    iri = r["definiciones"][0]
    h_ev = r["evidencia"][0].get("huella_fila_diccionario", "")
    h_dec = dec[iri]["huella_fila_diccionario"]
    h_cob = cob.get(iri, {}).get("huella_fila_diccionario", "")
    ok(h_ev and h_ev == h_dec == h_cob, "huella distinta en " + r["id"])
    r["huella_fila_diccionario"] = h_ev

# ---- 2. renombres ----
REN = {}
for k, v in list(e["conceptos_nuevos"].items()):
    if k.startswith("poblacion-proyectada-edad-") and k.endswith("-grandes"):
        banda = k[len("poblacion-proyectada-edad-"):-len("-grandes")]
        lab = v[0].replace("Población proyectada de ", "Población total de ")
        if "años" not in lab:
            lab = lab.replace(" (grandes grupos)", " años (grandes grupos)")
        REN[k] = ("poblacion-total-edad-%s-grandes" % banda, lab)
    elif k.startswith("poblacion-proyectada-edad-"):
        banda = k[len("poblacion-proyectada-edad-"):]
        lab = v[0].replace("Población proyectada de ", "Población reconstruida y ajustada de ")
        REN[k] = ("poblacion-reconstruida-ajustada-edad-" + banda, lab + " (grupos quinquenales)")
REN["poblacion-total-proyectada-quinquenios"] = (
    "poblacion-total-reconstruida-ajustada-quinquenios",
    "Población total reconstruida y ajustada (grupos quinquenales)")
REN["poblacion-total-proyectada-grandes-grupos"] = (
    "suma-poblacion-total-grandes-grupos",
    "Suma de población total (grandes grupos)")
PEND = {o: v for o, v in REN.items() if o in e["conceptos_nuevos"]}
for old, (new, lab) in PEND.items():
    ok(new not in e["conceptos_nuevos"] and new not in sem["conceptos"], "colision " + new)
    e["conceptos_nuevos"][new] = [lab, e["conceptos_nuevos"][old][1], e["conceptos_nuevos"][old][2]]
    del e["conceptos_nuevos"][old]
for r in e["reglas"]:
    if r["concepto"] in REN:
        r["concepto"] = REN[r["concepto"]][0]
for d in e["decisiones"]:
    if d.get("concepto") in REN:
        d["concepto"] = REN[d["concepto"]][0]
_SENT = ("No se homologa población reconstruida/ajustada con proyección;"
         " la mención a proyección viene solo del título del conjunto.")
for r in e["reglas"]:
    if _SENT in r["limite"]:
        continue
    if (r["conjuntos"][0] in ("0b5f5e16-2de3-4be1-811f-4b0976ed82d3",
                              "943d0723-afbb-470a-8fe8-d62e8671de84",
                              "960ef0a9-73ed-4191-ae0b-b868d7e48292")
            or r["diccionarios"][0] in ("03a33e71-d447-47b1-aa0d-b341996e023c",
                                        "1b6d0817-66a9-4b25-9468-efca73e3ce20",
                                        "f1bbd13b-3364-441c-81b4-7b7c548be39f")):
        r["limite"] = r["limite"] + " " + _SENT

# ---- 2b. sincronizar concepto decision<-regla y año condicional ----
_rmap = {r["id"]: r for r in e["reglas"]}
for d in e["decisiones"]:
    if d["decision"] == "proponer":
        d["concepto"] = _rmap[d["regla_id"]]["concepto"]
_YEARSENT = "No se añade año desde el nombre de la variable."
for r in e["reglas"]:
    if r["concepto"] not in e["conceptos_nuevos"]:
        continue
    _defi = e["conceptos_nuevos"][r["concepto"]][1]
    if "2020" in _defi:
        _d = next(x for x in e["decisiones"] if x["definicion_iri"] == r["definiciones"][0])
        if "2020" not in (_d["descripcion_literal"] + " " + _d["titulo_conjunto"]):
            e["conceptos_nuevos"][r["concepto"]][1] = _defi.replace(", 2020", "")
            if _YEARSENT not in r["limite"]:
                r["limite"] = r["limite"].replace(
                    "2020 declarado",
                    "año no declarado en la descripción ni en el conjunto") + " " + _YEARSENT

# ---- 3. validacion final ----
ok(len(e["decisiones"]) == 534 and len({d["definicion_iri"] for d in e["decisiones"]}) == 534, "particion 534")
ok(sum(1 for d in e["decisiones"] if d["decision"] == "proponer") == 482, "482 proponer")
ok(sum(1 for d in e["decisiones"] if d["decision"] == "pendiente") == 52, "52 pendientes")
ok(len(e["reglas"]) == 482 and len({r["id"] for r in e["reglas"]}) == 482, "482 reglas")
shd = [r for r in e["reglas"] if r["concepto"] == "superficie-sembrada-trigo-ddr"]
ok(len(shd) == 10 and all(r.get("calificador", {}).get("distrito_desarrollo_rural") for r in shd), "10 DDR")
ok(all(r.get("huella_fila_diccionario") == r["evidencia"][0]["huella_fila_diccionario"] for r in e["reglas"]),
   "huella top-level igual a evidencia")
for r in e["reglas"]:
    d = dec[r["definiciones"][0]]
    ok(r["huella_fila_diccionario"] == d["huella_fila_diccionario"], "huella igual a decision " + r["id"])
    ok(r["descripciones"] == [d["descripcion_literal"]] and r["nombres"] == [d["variable"]]
       and r["conjuntos"] == [d["conjunto"]] and r["diccionarios"] == [d["diccionario"]], "alcance " + r["id"])
ok(all("sameAs" not in json.dumps(r) and "exactMatch" not in json.dumps(r) for r in e["reglas"]), "sin equivalencias")
for slug, val in e["conceptos_nuevos"].items():
    ok(val[2] is None or val[2] in sem["conceptos"] or val[2] in e["conceptos_nuevos"], "padre " + slug)
    ok("proyectada" not in slug and "royectada" not in val[0], "resto proyeccion en " + slug)
e["conteos"] = {"decisiones": len(e["decisiones"]),
                "proponer": sum(1 for d in e["decisiones"] if d["decision"] == "proponer"),
                "pendiente": sum(1 for d in e["decisiones"] if d["decision"] == "pendiente"),
                "reglas": len(e["reglas"]), "conceptos_nuevos": len(e["conceptos_nuevos"]),
                "calificadores_ddr": 10}

if FALLOS:
    print("FALLOS:", len(FALLOS))
    for m in FALLOS:
        print("FAIL -", m)
    sys.exit(1)

with open(ENTREGA, "w", encoding="utf-8") as f:
    json.dump(e, f, ensure_ascii=False, indent=1)
print("OK decisiones=%d reglas=%d nuevos=%d" % (len(e["decisiones"]), len(e["reglas"]), len(e["conceptos_nuevos"])))
