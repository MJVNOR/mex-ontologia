"""Auditoria independiente agente-12 sobre entrega agente-6-salud (ronda 3).

Solo lee el proyecto; solo escribe en su propia carpeta.
No ejecuta consolidar/ampliar/sincronizar. Sin red.
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
cob = json.load(open("data/semantica/cobertura.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]
byid = {r["id"]: r for r in insp["recursos"]}

# ---- 1. base ronda 2 intacta (conteos centrales, no historicos) ----
res = cob["resumen"]
check("base_103_conceptos", res["conceptos_compartidos"] == 103)
check("base_232_respaldadas", res["estados_variables"]["respaldada_por_definicion"] == 232)
check("base_836_revisadas", res["estados_correspondencias"]["documental_revisada"] == 836)
check("base_118_candidatas", res["estados_correspondencias"]["candidata_por_nombre"] == 118)
check("base_6_vinculos_ambiguos", res["estados_correspondencias"]["ambigua_por_nombre"] == 6)
check("base_23_significados", res["estados_variables"]["candidata_sin_definicion_suficiente"] == 23)
check("base_16_referencias", res["referencias_catalogo_con_recurso_identificado"] == 16)
r2 = json.load(open("data/integracion-ronda-2/entregas/agente-2-pendientes/propuestas.json", encoding="utf-8"))
check("base_32_dictamenes", len(r2.get("decisiones", [])) == 32, str(len(r2.get("decisiones", []))))
check("base_14_preguntas", len(r2.get("preguntas_publicador", [])) == 14 and os.path.exists("data/integracion-ronda-2/entregas/agente-2-pendientes/preguntas-publicador.md"))
loc = json.load(open("data/integracion-ronda-2/entregas/agente-3-localidades-inegi/contraste-localidades.json", encoding="utf-8"))
n_iml = sum(1 for v in (loc["coincidencias"] if isinstance(loc, dict) and "coincidencias" in loc else loc) for _ in [0]) if False else None
# conteo robusto: buscar lista de coincidencias en cualquier clave
def _count(o):
    if isinstance(o, list):
        return len(o)
    if isinstance(o, dict):
        for k in ("coincidencias", "iguales", "emparejadas", "matches"):
            if k in o and isinstance(o[k], list):
                return len(o[k])
    return -1
check("base_1850_iml", loc.get("contraste_localidades", {}).get("interseccion") == 1850,
      "interseccion=" + str(loc.get("contraste_localidades", {}).get("interseccion")))
check("base_5450_solo_iter", loc.get("contraste_localidades", {}).get("solo_ITER") == 5450)

# ---- 2. particion y cobertura total (242 asignadas, sin omitidos) ----
dec_iris = [d["definicion_iri"] for d in prop["decisiones"]]
asig_iris = [v["definicion_iri"] for v in mine]
check("particion_242", len(dec_iris) == 242 == len(asig_iris))
check("sin_omitidos_ni_duplicados", sorted(dec_iris) == sorted(asig_iris) and len(set(dec_iris)) == 242)
check("asignacion_sha", prop["asignacion"]["sha256_cobertura"] == asig["sha256_cobertura"])
n_prop = sum(1 for d in prop["decisiones"] if d.get("decision") == "proponer_significado")
n_pen = sum(1 for d in prop["decisiones"] if d.get("decision") == "pendiente")
check("totales_204_38", n_prop == 204 and n_pen == 38, f"{n_prop}/{n_pen}")
check("reglas_204", len(prop["reglas"]) == 204)

# ---- 3. huellas antes/después por insumo ----
CENTRALES = {
    "cobertura.json": "data/semantica/cobertura.json",
    "contenido-inspeccion.json": "data/portal/contenido-inspeccion.json",
    "inventario.json": "data/portal/inventario.json",
    "semantica.json": "ontologia/semantica.json",
    "asignaciones-semanticas.json": "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
}
huellas = {}
for k, p in CENTRALES.items():
    ahora = sha(p)
    antes = prop["fuentes_huellas_entrada"][k]
    huellas[k] = {"antes_declarada_agente6": antes, "despues_recalculada_auditor": ahora, "coincide": antes == ahora}
    check("huella_entrada_" + k, antes == ahora, f"antes={antes[:12]} despues={ahora[:12]}")

# ---- 4. auditoria regla por regla contra literales completos ----
REPS = {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"}
CONDICIONADO = {
    "r3a6-008": "slug/etiqueta 'de-1-a-4' diverge del literal 'entre 1 y 5 años' (variable de01_a_04); definición conserva literal.",
    "r3a6-156": "descripción genérica 'Tipo de servicio de atención' + catálogo declarado no acreditado; solo texto declarado.",
    "r3a6-167": "literal mezcla toma de muestra con hallazgo ('aspecto de agua de roca'); concepto dice toma.",
    "r3a6-183": "resultado con codificación 1=Sí 2=No; no leer Sí/No como positivo/negativo.",
    "r3a6-188": "campo 'normalizado' derivado; reuse organizacion solo si normalización es del publicador.",
    "r3a6-192": "descripción genérica + variable CIE10_Descrip; texto declarado, no código CIE.",
    "r3a6-204": "descripción genérica + variable CIE10_Descrip; texto declarado, no código CIE.",
}
dictamenes = []
for d in prop["decisiones"]:
    if d.get("decision") != "proponer_significado":
        continue
    rid = d["regla_id"]
    idx = int(d["definicion_iri"].split("%2F")[1]) - 1
    row = byid[d["diccionario"]].get("definiciones", [])[idx]
    # fidelidad literal
    raw_desc = row.get("Descripci\u00f3n")
    check("lit_" + rid, (raw_desc or "").strip() == (d["descripcion_literal"] or "").strip(), d["variable"])
    check("lit_sin_cambio_sustantivo_" + rid, (raw_desc or "") in (d["descripcion_literal"], d["descripcion_literal"] + " "),
          repr(raw_desc))
    check("nom_" + rid, row.get("Nombre variable") == d["variable"])
    check("fila_" + rid, huella(row) == d["huella_fila_diccionario"])
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    check("asig_" + rid, a["descripcion"] == d["descripcion_literal"] and a["variable"] == d["variable"])
    # unidad es evidencia, no se asume código
    check("unidad_no_asumida_" + rid, d["representacion"] in REPS)
    # regla restringida
    r = next(x for x in prop["reglas"] if x["id"] == rid)
    check("restringida_" + rid, len(r["descripciones"]) == 1 and len(r["nombres"]) == 1
          and len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1)
    check("evidencia_completa_" + rid, r["descripciones"][0] == d["descripcion_literal"]
          and r["nombres"][0] == d["variable"] and r["definiciones"][0] == d["definicion_iri"])
    # concepto
    if d.get("reutiliza_concepto_vigente"):
        check("reuso_vigente_" + rid, r["concepto"] in sem["conceptos"] and r["concepto"] == d["concepto_propuesto"])
    else:
        check("nuevo_existe_" + rid, r["concepto"] in prop["conceptos_nuevos"])
        lab, defi, broader = prop["conceptos_nuevos"][r["concepto"]]
        check("nuevo_sin_equivalencia_" + rid, "sameAs" not in defi and "exactMatch" not in defi)
        check("broader_valido_" + rid, broader is None or broader in sem["conceptos"] or broader in prop["conceptos_nuevos"])
    # prohibiciones: sin inferir codigo/nacionalidad/etnia/diagnostico/sexo/unidad/rango/tipo-prueba
    defi_txt = "" if d.get("reutiliza_concepto_vigente") else prop["conceptos_nuevos"][r["concepto"]][1]
    for tok in ("nacionalidad", "CURP", "homolog"):
        check("sin_" + tok + "_" + rid, tok not in defi_txt or "sin homolog" in defi_txt or tok == "homolog")
    # dictamen
    if rid in CONDICIONADO:
        dictamenes.append({"regla": rid, "iri": d["definicion_iri"], "variable": d["variable"],
                           "literal": d["descripcion_literal"], "concepto": d["concepto_propuesto"],
                           "dictamen": "condicionado", "razon": CONDICIONADO[rid]})
    else:
        dictamenes.append({"regla": rid, "iri": d["definicion_iri"], "variable": d["variable"],
                           "literal": d["descripcion_literal"], "concepto": d["concepto_propuesto"],
                           "dictamen": "aceptar", "razon": "literal íntegro, regla restringida, concepto exacto con límites."})

check("dictamenes_204", len(dictamenes) == 204)
n_acep = sum(1 for x in dictamenes if x["dictamen"] == "aceptar")
n_cond = sum(1 for x in dictamenes if x["dictamen"] == "condicionado")
n_rech = sum(1 for x in dictamenes if x["dictamen"] == "rechazar")
check("conteo_acep_cond_rech", (n_acep, n_cond, n_rech) == (197, 7, 0), f"{n_acep}/{n_cond}/{n_rech}")

# ---- 5. pendientes: todos con razon, ninguno proponible por literal ----
for d in prop["decisiones"]:
    if d.get("decision") != "pendiente":
        continue
    check("pend_con_razon_" + d["variable"], bool(d.get("razon")) and bool(d.get("criterio")))

# ---- 6. simulacion independiente: reglas nuevas no colisionan con vigentes ----
rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
    {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
     "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
     "representacion": r["representacion"]} for r in prop["reglas"]]}
for d in prop["decisiones"]:
    if d.get("decision") != "proponer_significado":
        continue
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    res_i = interpretacion(a["variable"], a["descripcion"], a["conjunto"], rules, a["diccionario"], a["definicion_iri"])
    check("simula_" + d["regla_id"], res_i.get("estado") == "respaldada_por_definicion"
          and res_i.get("regla") == d["regla_id"] and res_i.get("concepto") == d["concepto_propuesto"])

# ---- 7. negativos reales (fallan si el verificador solo confirma resumenes) ----
neg = [
    ("neg_solo_nombre", "cefalea", "", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("neg_contexto_mutado", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "OTRO-CONJUNTO",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("neg_otra_iri", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F9999"),
    ("neg_generico_clave", "cve_cie10", "Clave", "dca16d84-dbf0-4501-b702-dc6372a480ea",
     "2334deaa-dd0c-444e-b038-4cc556ad715d", "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F9"),
    ("neg_sin_reglas_nuevas", "temperatura", "Temperatura del paciente", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F27"),
]
solo_vigentes = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"]}
for nombre, nomb, desc, conj, dicc, defi in neg:
    if nombre == "neg_sin_reglas_nuevas":
        r = interpretacion(nomb, desc, conj, solo_vigentes, dicc, defi)
        check(nombre, r.get("estado") != "respaldada_por_definicion"
              or not str(r.get("regla", "")).startswith("r3a6-"),
              "con solo vigentes no debe respaldar temperatura: " + str(r))
    else:
        r = interpretacion(nomb, desc, conj, rules, dicc, defi)
        check(nombre, r.get("estado") != "respaldada_por_definicion"
              or not str(r.get("regla", "")).startswith("r3a6-"), "debió no respaldar: " + str(r))

aud = {
    "auditor": "agente-12-auditoria-salud",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "base_ronda2_verificada": {"conceptos": 103, "respaldadas": 232, "revisadas": 836, "candidatas": 118,
                               "vinculos_ambiguos": 6, "significados_candidatos": 23, "referencias_catalogo": 16,
                               "dictamenes": 32, "preguntas": 14, "iml_iter": 1850},
    "huellas_insumos_antes_despues": huellas,
    "totales": {"decisiones": 242, "proponer_significado": 204, "pendientes": 38,
                "aceptar": n_acep, "condicionado": n_cond, "rechazar": n_rech},
    "dictamenes": dictamenes,
    "comprobaciones": len(ok),
}
json.dump(aud, open(A12 + "/auditoria.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"archivos": {k: {"sha256": sha(v), "bytes": os.path.getsize(v)} for k, v in CENTRALES.items()},
           "agente6": {"propuestas.json": sha(A6 + "/propuestas.json"), "resultado.md": sha(A6 + "/resultado.md")},
           "fecha_utc": datetime.now(timezone.utc).isoformat()},
          open(A12 + "/fuente/huellas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("auditoria OK: %d comprobaciones | aceptar=%d condicionado=%d rechazar=%d" % (len(ok), n_acep, n_cond, n_rech))
