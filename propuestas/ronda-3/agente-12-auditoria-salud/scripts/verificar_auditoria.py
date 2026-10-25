"""Auditoria v2 agente-12 sobre entrega ACTUAL agente-6-salud (203 reglas).

Claves por IRI (los IDs fueron renumerados). Verifica correctivos anunciados
de forma independiente. v1 (204) queda en auditoria-v1-204.json como historica.
Uso: uv run python propuestas/ronda-3/agente-12-auditoria-salud/scripts/verificar_auditoria.py
"""
import json, sys, hashlib, os
from datetime import datetime, timezone

A12 = "propuestas/ronda-3/agente-12-auditoria-salud"
A6 = "propuestas/ronda-3/agente-6-salud"
ROOT = os.getcwd()
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402

ok = []


def check(nombre, cond, detalle=""):
    if not cond:
        raise AssertionError("FALLA: " + nombre + (" | " + detalle if detalle else ""))
    ok.append(nombre)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


prop = json.load(open(A6 + "/propuestas.json", encoding="utf-8"))
asig = json.load(open("propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
insp = json.load(open("data/portal/contenido-inspeccion.json", encoding="utf-8"))
sem = json.load(open("ontologia/semantica.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]
byid = {r["id"]: r for r in insp["recursos"]}

# ---- totales actuales ----
n_prop = sum(1 for d in prop["decisiones"] if d.get("decision") == "proponer_significado")
n_pen = sum(1 for d in prop["decisiones"] if d.get("decision") == "pendiente")
check("totales_203_39", n_prop == 203 and n_pen == 39, f"{n_prop}/{n_pen}")
check("reglas_203", len(prop["reglas"]) == 203)
check("nuevos_178", len(prop["conceptos_nuevos"]) == 178, str(len(prop["conceptos_nuevos"])))
dec_iris = [d["definicion_iri"] for d in prop["decisiones"]]
check("particion_242", len(dec_iris) == 242 == len(mine) and sorted(dec_iris) == sorted(v["definicion_iri"] for v in mine))

# ---- correctivo de01_a_04 -> pendiente ----
d_a04 = next(d for d in prop["decisiones"] if d.get("variable") == "de01_a_04")
check("a04_pendiente", d_a04["decision"] == "pendiente" and d_a04.get("razon") == "rango_contradictorio_nombre_descripcion")
check("a04_sin_regla", not any(r["nombres"] == ["de01_a_04"] for r in prop["reglas"]))

# ---- correctivo 7 espacios: raw byte-exacto, hash sin modificar ----
ndif = 0
for d in prop["decisiones"]:
    if d.get("raw_difiere_de_central_trim"):
        ndif += 1
        idx = int(d["definicion_iri"].split("%2F")[1]) - 1
        row = byid[d["diccionario"]].get("definiciones", [])[idx]
        check("raw_exact_" + d["variable"], d.get("descripcion_raw_literal") == row.get("Descripci\u00f3n"),
              repr(d.get("descripcion_raw_literal")) + " vs " + repr(row.get("Descripci\u00f3n")))
        check("hash_intacto_" + d["variable"], huella(row) == d["huella_fila_diccionario"])
check("raw_siete", ndif == 7, str(ndif))

# ---- correctivos condicionados v1: verificacion independiente ----
# lcr conserva aspecto
lcr = next(d for d in prop["decisiones"] if d.get("variable") == "lcr")
cd_lcr = prop["conceptos_nuevos"][lcr["concepto_propuesto"]]
check("lcr_conserva_aspecto", "agua de roca" in cd_lcr[0] and "agua de roca" in cd_lcr[1])
# inmuno solo Si/No
inm = next(d for d in prop["decisiones"] if d.get("variable") == "res_final_ricket_inmuno")
check("inm_sin_positivo", "NO equivale" in " ".join(inm.get("limites", [])) or "positivo" in " ".join(inm.get("limites", [])).lower())
# servicios catalogo identificado sin vigencia
srv = next(d for d in prop["decisiones"] if d.get("variable") == "servic_atencion")
idx = int(srv["definicion_iri"].split("%2F")[1]) - 1
rowsrv = byid[srv["diccionario"]].get("definiciones", [])[idx]
check("srv_catalogo_en_fuente", "logo" in json.dumps(rowsrv, ensure_ascii=False).lower() or "Cat" in json.dumps(rowsrv))
check("srv_sin_vigencia", any("vigencia" in l.lower() for l in srv.get("limites", [])))
# norm es literal del publicador
nrm = next(d for d in prop["decisiones"] if d.get("variable") == "des_ins_uni_trat_norm")
idx = int(nrm["definicion_iri"].split("%2F")[1]) - 1
rown = byid[nrm["diccionario"]].get("definiciones", [])[idx]
check("norm_literal_publicador", "normalizado" in (rown.get("Descripci\u00f3n") or ""))
# CIE sin expandir
for v in ("CIE10_Descrip",):
    for d in [x for x in prop["decisiones"] if x.get("variable") == v]:
        check("cie_sin_expandir_" + d["definicion_iri"].split("%2F")[1],
              any("sin expandir" in l.lower() for l in d.get("limites", [])))

# ---- auditoria regla por regla, clave IRI ----
REPS = {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"}
dictamenes = []
for d in prop["decisiones"]:
    if d.get("decision") != "proponer_significado":
        continue
    iri = d["definicion_iri"]
    idx = int(iri.split("%2F")[1]) - 1
    row = byid[d["diccionario"]].get("definiciones", [])[idx]
    tag = iri.split("%2F")[1] + "_" + d["variable"][:14]
    check("lit_" + tag, (row.get("Descripci\u00f3n") or "").strip() == (d["descripcion_literal"] or "").strip())
    check("raw_" + tag, d.get("descripcion_raw_literal") == row.get("Descripci\u00f3n"))
    check("nom_" + tag, row.get("Nombre variable") == d["variable"])
    check("fila_" + tag, huella(row) == d["huella_fila_diccionario"])
    r = next(x for x in prop["reglas"] if x["id"] == d["regla_id"])
    check("restringida_" + tag, len(r["descripciones"]) == 1 and len(r["nombres"]) == 1
          and len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1)
    check("evidencia_" + tag, r["descripciones"][0] == d["descripcion_literal"] and r["nombres"][0] == d["variable"]
          and r["definiciones"][0] == iri and r["representacion"] in REPS)
    if d.get("reutiliza_concepto_vigente"):
        check("reuso_" + tag, r["concepto"] in sem["conceptos"] and r["concepto"] == d["concepto_propuesto"])
    else:
        check("nuevo_" + tag, r["concepto"] in prop["conceptos_nuevos"])
        lab, defi, broader = prop["conceptos_nuevos"][r["concepto"]]
        check("noequiv_" + tag, "sameAs" not in defi and "exactMatch" not in defi)
        check("broader_" + tag, broader is None or broader in sem["conceptos"] or broader in prop["conceptos_nuevos"])
    dictamenes.append({"regla": d["regla_id"], "iri": iri, "variable": d["variable"],
                       "literal": d["descripcion_literal"], "concepto": d["concepto_propuesto"],
                       "dictamen": "aceptar",
                       "razon": "v2: literal/RAW/huella/regla/concepto verificados por IRI; correctivos v1 resueltos."})

check("dictamenes_203", len(dictamenes) == 203)
for d in prop["decisiones"]:
    if d.get("decision") == "pendiente":
        check("pend_" + d["variable"] + "_" + d["definicion_iri"].split("%2F")[1], bool(d.get("razon")))


# ---- simulacion + negativos ----
rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
    {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
     "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
     "representacion": r["representacion"]} for r in prop["reglas"]]}
for d in prop["decisiones"]:
    if d.get("decision") != "proponer_significado":
        continue
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    ri = interpretacion(a["variable"], a["descripcion"], a["conjunto"], rules, a["diccionario"], a["definicion_iri"])
    check("simula_" + d["regla_id"], ri.get("estado") == "respaldada_por_definicion"
          and ri.get("regla") == d["regla_id"] and ri.get("concepto") == d["concepto_propuesto"])
for nombre, nomb, desc, conj, dicc, defi in [
    ("neg_solo_nombre", "cefalea", "", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("neg_contexto", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "OTRO-CONJUNTO",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("neg_otra_iri", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F9999"),
    ("neg_a04_promovido", "de01_a_04", "Total de personas en vigilancia entre 1 y 5 a\u00f1os",
     "dca16d84-dbf0-4501-b702-dc6372a480ea", "2334deaa-dd0c-444e-b038-4cc556ad715d",
     "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F13"),
]:
    rr = interpretacion(nomb, desc, conj, rules, dicc, defi)
    check(nombre, rr.get("estado") != "respaldada_por_definicion"
          or not str(rr.get("regla", "")).startswith("r3a6-"), "debió no respaldar: " + str(rr))

aud = {"auditor": "agente-12-auditoria-salud", "version": "v2-203",
       "superseed": "auditoria-v1-204.json (historica; outcome actual: 203)",
       "fecha_utc": datetime.now(timezone.utc).isoformat(),
       "sha_propuestas_auditada": sha(A6 + "/propuestas.json"),
       "totales": {"decisiones": 242, "proponer_significado": 203, "pendientes": 39,
                   "aceptar": 203, "condicionado": 0, "rechazar": 0},
       "condiciones_v1": {"resueltas_verificadas": ["r3a6-008/v1 slug (a04 pendiente)",
          "lcr conserva aspecto agua de roca", "inmuno solo Si/No", "servicios catalogo sin vigencia",
          "norm literal publicador", "CIE sin expandir x2", "7 RAW/huella intacta"],
          "no_resueltas": []},
       "dictamenes": dictamenes, "comprobaciones": len(ok)}
json.dump(aud, open(A12 + "/auditoria.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("auditoria v2 OK: %d comprobaciones | aceptar=203 condicionado=0 rechazar=0" % len(ok))
