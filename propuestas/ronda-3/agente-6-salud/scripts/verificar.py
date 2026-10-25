"""Verificador propio agente-6: recalcula huellas, partición, reglas y negativos."""
import json, sys, hashlib

A6 = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/ronda-3/agente-6-salud"
ROOT = "C:/Users/marti/Documents/MEX-Ontologi"
sys.dont_write_bytecode = True
sys.path.insert(0, ROOT + "/scripts")
from consolidar_semantica import huella, interpretacion
from integrar_contenido import clave

ok = []
def check(nombre, cond):
    assert cond, "FALLA: " + nombre
    ok.append(nombre)

prop = json.load(open(A6 + "/propuestas.json", encoding="utf-8"))
asig = json.load(open(ROOT + "/propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]
insp = json.load(open(ROOT + "/data/portal/contenido-inspeccion.json", encoding="utf-8"))
sem = json.load(open(ROOT + "/ontologia/semantica.json", encoding="utf-8"))
byid = {r["id"]: r for r in insp["recursos"]}

# 1. partición exacta
asig_iris = [v["definicion_iri"] for v in mine]
dec_iris = [d["definicion_iri"] for d in prop["decisiones"]]
check("particion_242", len(dec_iris) == 242 == len(asig_iris))
check("sin_omitidos_ni_duplicados", sorted(dec_iris) == sorted(asig_iris) and len(set(dec_iris)) == 242)
check("todos_fuera_del_nucleo", all(v["estado"] == "fuera_del_nucleo_actual" for v in mine))

# 2. huellas recalculadas desde inspección + literales íntegros
for v in mine:
    idx = int(v["definicion_iri"].split("%2F")[1]) - 1
    row = byid[v["diccionario"]].get("definiciones", [])[idx]
    check("huella_" + v["definicion_iri"].split("%2F")[1] + "_" + v["variable"][:12],
          huella(row) == v["huella_fila_diccionario"])
for d in prop["decisiones"]:
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    check("literal_" + d["variable"][:16] + "_" + d["definicion_iri"].split("%2F")[1],
          d["descripcion_literal"] == a["descripcion"] and d["variable"] == a["variable"]
          and d["huella_fila_diccionario"] == a["huella_fila_diccionario"]
          and d["conjunto"] == a["conjunto"] and d["diccionario"] == a["diccionario"])
    for k in ("descripcion_literal", "tipo_literal", "unidad_literal", "ejemplo_literal"):
        check("sin_FFFD_" + d["variable"][:14], "�" not in (d.get(k) or ""))

# 3. reglas bien formadas y restringidas
ids = [r["id"] for r in prop["reglas"]]
check("reglas_prefijo_unicas", all(i.startswith("r3a6-") for i in ids) and len(set(ids)) == len(ids))
check("reglas_una_por_propuesta",
      sorted(ids) == sorted(d["regla_id"] for d in prop["decisiones"] if d["decision"] == "proponer_significado"))
REPS = {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"}
for r in prop["reglas"]:
    check("restringida_" + r["id"],
          len(r["descripciones"]) == 1 and len(r["nombres"]) == 1 and len(r["conjuntos"]) == 1
          and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1 and r["representacion"] in REPS)
    check("concepto_existe_" + r["id"],
          r["concepto"] in prop["conceptos_nuevos"] or r["concepto"] in sem["conceptos"])
for slug, (label, defin, broader) in prop["conceptos_nuevos"].items():
    check("nuevo_slug_" + slug, slug.startswith("caso-con-") or slug in (
        "jurisdiccion-sanitaria",) or slug.startswith(("vigilancia-", "diagnostico-", "total-urgencias",
        "localidad-", "edad-", "tipo-calle-", "colonia-", "codigo-postal-", "condicion-",
        "habla-", "lengua-", "ocupacion-", "estatus-", "contacto-", "acceso-", "cobertura-",
        "temperatura-", "manejo-", "tipo-servicio-", "evolucion-", "muestra-", "motivo-",
        "defuncion-", "semanas-", "rechazo-", "resultado-", "especie-", "tratamiento-",
        "medicamento-", "tipo-muerte-", "organos-", "cantidad-", "fecha-")))
    check("broader_valido_" + slug, broader is None or broader in sem["conceptos"] or broader in prop["conceptos_nuevos"])
    check("nuevo_sin_sameas_" + slug, "sameAs" not in defin and "exactMatch" not in defin)
check("reutilizados_vigentes",
      set(prop["conceptos_reutilizados"]) <= set(sem["conceptos"]) and len(prop["conceptos_reutilizados"]) == 6)

# 4. simulación de interpretacion() en memoria (central + reglas nuevas)
rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
    {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
     "nombres": r["nombres"], "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"],
     "definiciones": r["definiciones"], "representacion": r["representacion"]} for r in prop["reglas"]]}
for d in prop["decisiones"]:
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    res = interpretacion(a["variable"], a["descripcion"], a["conjunto"], rules, a["diccionario"], a["definicion_iri"])
    if d["decision"] == "proponer_significado":
        check("simula_respalda_" + d["variable"][:16],
              res.get("estado") == "respaldada_por_definicion" and res.get("concepto") == d["concepto_propuesto"]
              and res.get("regla") == d["regla_id"] and res.get("representacion") == d["representacion"])
    else:
        check("simula_pendiente_" + d["variable"][:16], res.get("estado") != "respaldada_por_definicion"
              or res.get("regla", "").startswith("pista"))
# 5. negativos reales
neg = [
    ("solo_nombre", "cefalea", "", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("contexto_mutado", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "OTRO-CONJUNTO",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("otra_iri", "cefalea", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F9999"),
    ("descripcion_otro_nombre", "fiebre_x", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
     "33d0a99e-c721-496f-a05e-07646e9ae42a", "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28"),
    ("codigo_no_acreditado", "cve_cie10", "Clave", "dca16d84-dbf0-4501-b702-dc6372a480ea",
     "2334deaa-dd0c-444e-b038-4cc556ad715d", "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F9"),
]
for nombre, nomb, desc, conj, dicc, defi in neg:
    r = interpretacion(nomb, desc, conj, rules, dicc, defi)
    check("negativo_" + nombre, r.get("estado") != "respaldada_por_definicion" or not str(r.get("regla", "")).startswith("r3a6-"))
# unidad es evidencia, no restricción: fila sin unidad sigue matcheando
r = interpretacion("temperatura", "Temperatura del paciente", "5494daa1-09ca-4750-aeac-2558553700e1",
                   rules, "33d0a99e-c721-496f-a05e-07646e9ae42a",
                   "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F27")
check("unidad_es_evidencia_no_restriccion", r.get("regla") == next(
    x["regla_id"] for x in prop["decisiones"] if x["variable"] == "temperatura" and x["decision"] == "proponer_significado"))
# nombre exacto: cefalea_frontal no debe activar la regla de cefalea ni viceversa
r = interpretacion("cefalea_frontal", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
                   rules, "33d0a99e-c721-496f-a05e-07646e9ae42a",
                   "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28")
check("negativo_nombre_no_exacto", r.get("regla", "") != next(
    x["regla_id"] for x in prop["decisiones"] if x["variable"] == "cefalea" and x["decision"] == "proponer_significado"))
# variante de codificación no documentada no matchea plantilla 1=Si 2=No
r = interpretacion("cefalea", "El paciente presenta Cefalea 1=Si 2=No 3=Tal vez", "5494daa1-09ca-4750-aeac-2558553700e1",
                   rules, "33d0a99e-c721-496f-a05e-07646e9ae42a",
                   "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28")
check("negativo_codificacion_distinta", not str(r.get("regla", "")).startswith("r3a6-"))
# mes correcto en conjunto equivocado no matchea (acotación conjunto+diccionario+definición)
r = interpretacion("enero", "Vigilancias totales en enero", "OTRO-CONJUNTO",
                   rules, "2334deaa-dd0c-444e-b038-4cc556ad715d",
                   "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F45")
check("negativo_mes_otro_conjunto", not str(r.get("regla", "")).startswith("r3a6-"))
# ninguna regla deduce por regex de nombre: nombre sugerente con otra descripción no matchea
r = interpretacion("de65_y_maf", "El paciente presenta Cefalea 1=Si 2=No", "5494daa1-09ca-4750-aeac-2558553700e1",
                   rules, "33d0a99e-c721-496f-a05e-07646e9ae42a",
                   "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28")
check("negativo_nombre_sugerente", not str(r.get("regla", "")).startswith("r3a6-"))

# 6. base y huellas de entrada
check("cobertura_sha", prop["fuentes_huellas_entrada"]["cobertura.json"] == asig["sha256_cobertura"])
for k, p in {"cobertura.json": ROOT + "/data/semantica/cobertura.json",
             "semantica.json": ROOT + "/ontologia/semantica.json"}.items():
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    check("huella_entrada_" + k, h == prop["fuentes_huellas_entrada"][k])
check("sin_correspondencias_nuevas", "correspondencias" not in prop or prop.get("correspondencias", []) == [])
check("alcance_sin_red", any("sin descargas" in l.lower() for l in prop["limites"]))

# 7. devolución auditoría: 7 condicionados
de = {d["variable"] + "|" + d["definicion_iri"].split("%2F")[1]: d for d in prop["decisiones"]}
d13 = de["de01_a_04|13"]
check("aud_de01_a_04_pendiente", d13["decision"] == "pendiente" and d13["razon"] == "rango_contradictorio_nombre_descripcion"
      and "regla_id" not in d13)
check("aud_de01_a_04_sin_concepto", "vigilancia-personas-de-1-a-4-anos" not in prop["conceptos_nuevos"])
check("aud_de01_a_04_sin_regla", all("de01_a_04" not in r["nombres"] for r in prop["reglas"]))
lcr = de["lcr|142"]
check("aud_lcr_doble_condicion", lcr["decision"] == "proponer_significado"
      and "agua de roca" in prop["conceptos_nuevos"][lcr["concepto_propuesto"]][1]
      and "muestra" in prop["conceptos_nuevos"][lcr["concepto_propuesto"]][1].lower())
inm = de["res_final_ricket_inmuno|165"]
rl = next(r for r in prop["reglas"] if r["id"] == inm["regla_id"])
check("aud_inmuno_no_positivo", inm["decision"] == "proponer_significado"
      and any("NO equivale a positivo/negativo" in l for l in rl["limites"])
      and "NO positivo/negativo" in prop["conceptos_nuevos"][inm["concepto_propuesto"]][1])
srv = de["servic_atencion|129"]
rl = next(r for r in prop["reglas"] if r["id"] == srv["regla_id"])
check("aud_servicio_acotado", any("ronda 1" in l for l in rl["limites"])
      and any("no se afirma catálogo validado" in l for l in rl["limites"]))
nrm = de["des_ins_uni_trat_norm|173"]
check("aud_norm_literal_publicador", "literal del publicador" in nrm["criterio"]
      and "sin homologar papel" in nrm["criterio"])
for var in ("CIE10_Descrip|13", "des_diagno|8"):
    dd = de[var]
    if dd["decision"] == "proponer_significado":
        rl = next(r for r in prop["reglas"] if r["id"] == dd["regla_id"])
        check("aud_diagnostico_sin_cie_" + var.split("|")[0], any("sin expandir CIE" in l for l in rl["limites"]))
for d in prop["decisiones"]:
    a = next(v for v in mine if v["definicion_iri"] == d["definicion_iri"])
    idx = int(a["definicion_iri"].split("%2F")[1]) - 1
    raw = next(row[k] for row in [byid[a["diccionario"]].get("definiciones", [])[idx]] for k in row if clave(k) == "descripcion")
    check("raw_" + d["variable"][:14], d["descripcion_raw_literal"] == raw
          and d["raw_difiere_de_central_trim"] == (raw != d["descripcion_literal"]))
    if d["decision"] == "proponer_significado":
        check("raw_misma_huella_" + d["variable"][:14], d["huella_fila_diccionario"] == a["huella_fila_diccionario"])
check("nuevos_todos_usados", all(any(r["concepto"] == s for r in prop["reglas"]) for s in prop["conceptos_nuevos"]))

print("verificador OK: %d comprobaciones" % len(ok))
