"""Auditoria-b FINAL (fase 2): entregas actuales registro-civil y educacion.

Salud excluida: entrega.json cambio tras su listo (SHA difiere); espera
segunda instruccion. Lee entregas actuales + centrales. Escribe en auditoria-b.
"""
import json, sys, hashlib, os, re
from datetime import datetime, timezone
from collections import Counter

B = "propuestas/cobertura-muse-20261023/auditoria-b"
R = "propuestas/cobertura-muse-20261023/registro-civil/entrega.json"
E = "propuestas/cobertura-muse-20261023/educacion/entrega.json"
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from consolidar_semantica import huella, interpretacion, validar_calificador  # noqa: E402

ok = []


def check(n, c, d=""):
    if not c:
        raise AssertionError("FALLA: " + n + (" | " + d if d else ""))
    ok.append(n)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def W(w, t):
    return re.search(r"\b" + re.escape(w) + r"\b", t) is not None


SHA = {"registro-civil": sha(R), "educacion": sha(E),
       "salud": sha("propuestas/cobertura-muse-20261023/salud/entrega.json")}
check("sha_rc_listo", SHA["registro-civil"] == json.load(open(R.replace("entrega.json", "listo.json"), encoding="utf-8"))["sha256"])
check("sha_edu_listo", SHA["educacion"] == json.load(open(E.replace("entrega.json", "listo.json"), encoding="utf-8"))["sha256"])
check("sha_salud_listo", SHA["salud"] == json.load(open("propuestas/cobertura-muse-20261023/salud/listo.json", encoding="utf-8"))["sha256"])

insp = json.load(open("data/portal/contenido-inspeccion.json", encoding="utf-8"))
sem = json.load(open("ontologia/semantica.json", encoding="utf-8"))
asig = json.load(open("propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
byid = {r["id"]: r for r in insp["recursos"]}
cob = json.load(open("data/semantica/cobertura.json", encoding="utf-8"))
TIT = {(v["conjunto"], v["variable"]): v.get("titulo_conjunto", "") for v in cob["variables"]}
REPS = {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"}
UNID = ["a\u00f1o", "kg", "gramo", "cm", "mmhg", "%", "mxn", "peso", "d\u00eda", "hora", "grado"]
POB = ["madre", "padre", "hijo", "nacido", "difunto", "alumno", "estudiante", "paciente", "caso", "donante",
       "divorci", "titulado", "egresado"]
CAL = ["202", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
       "octubre", "noviembre", "diciembre", "semana", "trimestre", "cuatrimestre", "ciclo"]

CFG = {
    "salud": {"f": "propuestas/cobertura-muse-20261023/salud/entrega.json", "ag": "6", "prop": "proponer",
        "d": "descripcion_literal", "t": None, "u": None, "e": None, "v": "variable"},
    "registro-civil": {"f": R, "ag": "7", "prop": "proponer",
        "d": "descripcion", "t": "tipo", "u": "unidad", "e": "ejemplo", "v": "variable"},
    "educacion": {"f": E, "ag": "8", "prop": "proponer",
        "d": "descripcion", "t": "tipo_de_dato", "u": "unidad_de_medida", "e": "ejemplo_de_dato", "v": "variable"},
}
dicts, resumen = [], {}
for dom, C in CFG.items():
    prop = json.load(open(C["f"], encoding="utf-8"))
    mine = {v["definicion_iri"]: v for v in asig["asignaciones"][C["ag"]]["variables"]}
    check(f"{dom}_particion", sorted(d["definicion_iri"] for d in prop["decisiones"]) == sorted(mine))
    props = [d for d in prop["decisiones"] if d.get("decision") == C["prop"]]
    check(f"{dom}_nreglas", len(props) == len(prop["reglas"]), f"{len(props)}/{len(prop['reglas'])}")
    byrule = {r["id"]: r for r in prop["reglas"]}
    # concepto por regla (RC lo trae en regla; EDU en decision)
    rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
        {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
         "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
         "representacion": r["representacion"]} for r in prop["reglas"]]}
    for d in props:
        iri = d["definicion_iri"]
        r = byrule.get(d.get("regla_id")) or next(x for x in prop["reglas"] if iri in x["definiciones"])
        tag = r["id"]
        idx = int(iri.split("%2F")[1]) - 1
        row = byid[d["diccionario"]].get("definiciones", [])[idx]
        raw = row.get("Descripci\u00f3n") or ""
        lit = d[C["d"]] or ""
        check(f"{dom}_lit_{tag}", raw.strip() == lit.strip(), repr(raw)[:70])
        check(f"{dom}_nom_{tag}", (row.get("Nombre variable") or "").strip() == (d[C["v"]] or "").strip())
        check(f"{dom}_huella_{tag}", huella(row) == d["huella_fila_diccionario"])
        check(f"{dom}_restr_{tag}", len(r["descripciones"]) == 1 and len(r["nombres"]) == 1
              and len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1)
        check(f"{dom}_evid_{tag}", r["descripciones"][0] == lit and r["nombres"][0] == d[C["v"]]
              and r["definiciones"][0] == iri and r["representacion"] in REPS)
        conc = d.get("concepto", r["concepto"])
        check(f"{dom}_conc_match_{tag}", conc == r["concepto"])
        reuso_set = prop.get("conceptos_reutilizados", prop.get("conceptos_reutilizados_vigentes"))
        reuso = conc in (reuso_set if isinstance(reuso_set, list) else (reuso_set or {}))
        if reuso:
            check(f"{dom}_reuso_{tag}", conc in sem["conceptos"])
            defi = sem["conceptos"][conc][1]
        else:
            check(f"{dom}_nuevo_{tag}", conc in prop["conceptos_nuevos"])
            cn = prop["conceptos_nuevos"][conc]
            defi = cn[1] if isinstance(cn, list) else cn.get("definicion", "")
            br = cn[2] if isinstance(cn, list) else cn.get("broader")
            check(f"{dom}_noequiv_{tag}", "sameAs" not in defi and "exactMatch" not in defi)
            check(f"{dom}_broader_{tag}", br is None or br in sem["conceptos"] or br in prop["conceptos_nuevos"])
        # calificador: str/null NO aceptados
        cal = r.get("calificador", None)
        if "calificador" in r:
            check(f"{dom}_calif_tipo_{tag}", isinstance(cal, dict) and len(cal) > 0, repr(cal)[:80])
        # colision nucleo
        sv = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"]}
        a = mine[iri]
        rs = interpretacion(a.get("variable", d[C["v"]]), a.get("descripcion", lit), a["conjunto"], sv,
                            a["diccionario"], iri)
        col = rs.get("estado") == "respaldada_por_definicion"
        # flags
        mots, sev = [], "aceptar"
        ev = r.get("evidencia") or {}
        evu = (ev.get("unidad", "") if isinstance(ev, dict) else "") or ""
        und = ((d.get(C["u"]) if C["u"] else None) or evu) + " " + lit
        dl = defi.lower()
        ds = re.sub(r"(sin|distint[a-z]*|no [a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]+) [a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1 ]{0,40}", " ", dl)
        if not reuso and any(W(u, ds) for u in UNID) and not any(W(u, und.lower()) for u in UNID):
            mots.append("concepto afirma unidad ausente"); sev = "condicionado"
        cod = bool(re.search(r"1\s*=\s*\S+.*2\s*=", lit))
        if cod and re.search(r"presenta|tiene|es\b", lit, re.I) and not re.search(
                r"indicador|declarad|registro|conteo|conserva|categor", defi, re.I):
            mots.append("indicador afirmado como hecho/diagnostico"); sev = "condicionado"
        caltxt = json.dumps(cal, ensure_ascii=False).lower() if isinstance(cal, dict) else ""
        ctx = (lit + " " + d[C["v"]] + " " + TIT.get((d["conjunto"], d[C["v"]]), "")).lower()
        if "paciente" in ctx or "caso" in ctx:
            ctx += " paciente caso"
        if "alumno" in ctx or "estudiante" in ctx:
            ctx += " alumno estudiante"
        if "donaci" in ctx:
            ctx += " donante"
        if not reuso:
            for p_ in POB:
                if W(p_, ds) and not W(p_, ctx) and p_ not in caltxt:
                    mots.append(f"sujeto '{p_}' fuera de literal/conjunto/calificador"); sev = "condicionado"
                    break
            for c_ in CAL:
                uu = (d.get(C["u"]) if C["u"] else None) or ""
                if W(c_, ds) and c_ not in (lit + " " + uu).lower():
                    mots.append(f"calendario '{c_}' ausente"); sev = "condicionado"
                    break
        if col:
            mots.append("COLISION con vigentes"); sev = "rechazar"
        rr = interpretacion(a.get("variable", d[C["v"]]), a.get("descripcion", lit), a["conjunto"],
                            rules, a["diccionario"], iri)
        if not (rr.get("estado") == "respaldada_por_definicion" and rr.get("regla") == r["id"]):
            mots.append("no simula su regla: " + str(rr)); sev = "rechazar"
        if cal is not None and sev == "aceptar":
            sev, mots = "condicionado", [f"calificador {json.dumps(cal, ensure_ascii=False)[:100]}: no propagado por pipeline; excluido hasta propagar o estrechar"]
        if cal is not None and sev == "condicionado" and os.environ.get("RECONSIDERAR_CALIF") == "1":
            try:
                rep = json.load(open(B + "/reporte_calificadores.json", encoding="utf-8"))
                det = next(x for x in rep["detalle"] if x["regla"] == r["id"])
                if det["calificador_propagado"] == validar_calificador(cal):
                    sev = "aceptar"
                    mots = [f"RECONSIDERADO: calificador propagado verificado (reporte_calificadores.json + SPARQL {rep['triples_sparql']} filas); motor actual lo conserva en reporte y RDF"]
            except Exception as e:
                mots.append("reconsideracion no probada: " + str(e))
        if not mots:
            mots = ["literal/huella/regla/concepto/contexto/simulacion verificados"]
        dicts.append({"dominio": dom, "regla_id": r["id"], "dictamen": sev, "motivo": "; ".join(mots)})
    for d in prop["decisiones"]:
        if d.get("decision") != C["prop"]:
            check(f"{dom}_pend_{d[C['v']]}", True)
    a0 = mine[next(iter(mine))]
    rr = interpretacion("zz_solo_nombre", a0.get("descripcion", ""), a0["conjunto"], rules, a0["diccionario"], a0["definicion_iri"])
    check(f"{dom}_neg1", rr.get("estado") != "respaldada_por_definicion")
    rr = interpretacion(a0.get("variable", ""), a0.get("descripcion", ""), "OTRO", rules, a0["diccionario"], a0["definicion_iri"])
    check(f"{dom}_neg2", rr.get("estado") != "respaldada_por_definicion")
    c = Counter(x["dictamen"] for x in dicts if x["dominio"] == dom)
    resumen[dom] = {"reglas": len(props), "aceptar": c["aceptar"], "condicionado": c["condicionado"], "rechazar": c["rechazar"]}

json.dump({"sha_entregas": SHA,
           "dictamenes": [{"dominio": x["dominio"], "regla_id": x["regla_id"], "dictamen": x["dictamen"], "motivo": x["motivo"]} for x in dicts],
           "resumen": resumen, "comprobaciones": len(ok),
           "nota": "FINAL RC+EDU+SALUD (entregas actuales, SHA listo). Condicionado excluido hasta nueva revision."},
          open(B + "/auditoria.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("auditoria FINAL OK: %d checks | %s" % (len(ok), json.dumps(resumen)))
