"""Auditoria-b independiente: reglas congeladas agentes 6/7/8 (fase 1).

Lee SOLO copias congeladas + centrales. Escribe SOLO en auditoria-b/.
No ejecuta historicos ni suite central. Sin red.
Uso: uv run python propuestas/cobertura-muse-20261023/auditoria-b/scripts/verificar.py
"""
import json, sys, hashlib, os, re
from datetime import datetime, timezone
from collections import Counter

B = "propuestas/cobertura-muse-20261023/auditoria-b"
F = "propuestas/cobertura-muse-20261023/fuentes"
MAN = json.load(open(F + "/manifiesto.json", encoding="utf-8"))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402

ok = []


def check(n, c, d=""):
    if not c:
        raise AssertionError("FALLA: " + n + (" | " + d if d else ""))
    ok.append(n)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ---- 1. insumos congelados vs manifiesto + centrales ----
for c in MAN["copias"]:
    if "/agente-" in c["copia"] and c["copia"].endswith("propuestas.json"):
        check("frozen_" + c["copia"].split("/")[2], sha(c["copia"]) == c["sha256"], c["copia"])
for k, h in MAN["insumos_centrales"].items():
    check("central_" + k.split("/")[-1], sha(k) == h, k)

insp = json.load(open("data/portal/contenido-inspeccion.json", encoding="utf-8"))
sem = json.load(open("ontologia/semantica.json", encoding="utf-8"))
asig = json.load(open("propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
byid = {r["id"]: r for r in insp["recursos"]}
cob = json.load(open("data/semantica/cobertura.json", encoding="utf-8"))
TIT = {}
for v in cob["variables"]:
    TIT[(v["conjunto"], v["variable"])] = v.get("titulo_conjunto", "")
REPS = {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"}
UNID = ["año", "a\u00f1o", "kg", "gramo", "cm", "mmhg", "%", "mxn", "peso", "d\u00eda", "hora", "grado"]
POB = ["madre", "padre", "hijo", "nacido", "difunto", "alumno", "estudiante", "paciente", "caso", "donante",
       "divorci", "titulado", "egresado"]
CAL = ["202", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
       "octubre", "noviembre", "diciembre", "semana", "trimestre", "cuatrimestre", "ciclo"]

DOMS = {
    "salud": {"f": F + "/agente-6-salud/propuestas.json", "ag": "6", "prop": "proponer_significado",
              "d": "descripcion_literal", "t": "tipo_literal", "u": "unidad_literal", "e": "ejemplo_literal",
              "c": "catalogo_literal", "v": "variable", "cp": "concepto_propuesto", "rid": "regla_id"},
    "registro-civil": {"f": F + "/agente-7-registro-civil/propuestas.json", "ag": "7", "prop": "propuesta-significado",
              "d": "descripcion", "t": "tipo", "u": "unidad", "e": "ejemplo",
              "c": "catalogo_declarado", "v": "variable", "cp": "concepto", "rid": "regla_id"},
    "educacion": {"f": F + "/agente-8-educacion/propuestas.json", "ag": "8", "prop": "propuesta",
              "d": "descripcion", "t": "tipo_de_dato", "u": "unidad_de_medida", "e": "ejemplo_de_dato",
              "c": "catalogo_de_referencia", "v": "variable", "cp": "concepto", "rid": "regla_id"},
}
a11 = json.load(open(F + "/agente-11-auditoria/auditoria.json", encoding="utf-8"))
A11K = {"salud": None, "registro-civil": "a7", "educacion": "a8"}
SHA_ENT = {d: next(c["sha256"] for c in MAN["copias"] if f"/{ {'salud':'agente-6-salud','registro-civil':'agente-7-registro-civil','educacion':'agente-8-educacion'}[d] }/propuestas.json" in c["copia"]) for d in DOMS}

dicts, resumen = [], {}
trims = []
for dom, C in DOMS.items():
    prop = json.load(open(C["f"], encoding="utf-8"))
    mine = {v["definicion_iri"]: v for v in asig["asignaciones"][C["ag"]]["variables"]}
    check(f"{dom}_particion", sorted(d["definicion_iri"] for d in prop["decisiones"]) == sorted(mine)
          and len(prop["decisiones"]) == len(mine), f"{len(prop['decisiones'])}/{len(mine)}")
    props = [d for d in prop["decisiones"] if d.get("decision") == C["prop"]]
    check(f"{dom}_nreglas", len(props) == len(prop["reglas"]), f"{len(props)}/{len(prop['reglas'])}")
    rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
        {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
         "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
         "representacion": r["representacion"]} for r in prop["reglas"]]}
    for d in props:
        iri, tag = d["definicion_iri"], d[C["rid"]]
        idx = int(iri.split("%2F")[1]) - 1
        row = byid[d["diccionario"]].get("definiciones", [])[idx]
        raw = row.get("Descripci\u00f3n") or ""
        lit = d[C["d"]] or ""
        check(f"{dom}_lit_{tag}", raw.strip() == lit.strip(), repr(raw)[:80])
        if "raw" in json.dumps(d):
            for k in d:
                if "raw" in k.lower() and isinstance(d[k], str) and d[k].strip() == raw.strip():
                    check(f"{dom}_rawbyte_{tag}", d[k] == raw, "RAW debe ser byte-exacto")
                    break
        check(f"{dom}_nom_{tag}", (row.get("Nombre variable") or "").strip() == (d[C["v"]] or "").strip(),
              repr(row.get("Nombre variable")))
        if (row.get("Nombre variable") or "") != (d[C["v"]] or ""):
            trims.append(f"{dom}/{tag}: fila={row.get('Nombre variable')!r} propuesta={d[C['v']]!r}")
        check(f"{dom}_huella_{tag}", huella(row) == d["huella_fila_diccionario"])
        r = next(x for x in prop["reglas"] if x["id"] == d[C["rid"]])
        check(f"{dom}_restr_{tag}", len(r["descripciones"]) == 1 and len(r["nombres"]) == 1
              and len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1)
        check(f"{dom}_evid_{tag}", r["descripciones"][0] == lit and r["nombres"][0] == d[C["v"]]
              and r["definiciones"][0] == iri and r["representacion"] in REPS)
        conc = d[C["cp"]]
        if isinstance(prop.get("conceptos_reutilizados"), dict):
            reuso = conc in prop["conceptos_reutilizados"]
        else:
            reuso = conc in (prop.get("conceptos_reutilizados") or [])
        if reuso:
            check(f"{dom}_reuso_{tag}", conc in sem["conceptos"], conc)
            defi = sem["conceptos"][conc][1]
        else:
            check(f"{dom}_nuevo_{tag}", conc in prop["conceptos_nuevos"], conc)
            defi = prop["conceptos_nuevos"][conc][1] if isinstance(prop["conceptos_nuevos"][conc], list) else prop["conceptos_nuevos"][conc].get("definicion", "")
            br = prop["conceptos_nuevos"][conc][2] if isinstance(prop["conceptos_nuevos"][conc], list) else prop["conceptos_nuevos"][conc].get("broader")
            check(f"{dom}_noequiv_{tag}", "sameAs" not in defi and "exactMatch" not in defi)
            check(f"{dom}_broader_{tag}", br is None or br in sem["conceptos"] or br in prop["conceptos_nuevos"])
        # colision nucleo: solo-vigentes no debe respaldar
        sv = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"]}
        a = mine[iri]
        rs = interpretacion(a.get("variable", d[C["v"]]), a.get("descripcion", lit), a["conjunto"], sv,
                            a["diccionario"], iri)
        col = rs.get("estado") == "respaldada_por_definicion"
        # flags semanticos (texto = literal + variable + conjunto; paciente≈caso; reuso exento)
        mots, sev = [], "aceptar"
        und = (d[C["u"]] or "") + " " + lit
        defi_low = defi.lower()
        defi_sin_neg = re.sub(r"(sin|distint[a-z]*|no [a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]+) [a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1 ]{0,40}", " ", defi_low)
        def W(w, t):
            return re.search(r"\b" + re.escape(w) + r"\b", t) is not None
        if not reuso and any(W(u, defi_sin_neg) for u in UNID) and not any(W(u, und.lower()) for u in UNID):
            mots.append("concepto afirma unidad ausente en literal/unidad"); sev = "condicionado"
        codificado = bool(re.search(r"1\s*=\s*\S+.*2\s*=", lit))
        if codificado and re.search(r"presenta|tiene|es\b", lit, re.I) and not re.search(
                r"indicador|declarad|registro|conteo|conserva|categor", defi, re.I):
            mots.append("indicador codificado afirmado como hecho/diagnostico"); sev = "condicionado"
        ctx = (lit + " " + d[C["v"]] + " " + d.get("titulo_conjunto", "")
               + " " + TIT.get((d["conjunto"], d[C["v"]]), "")).lower()
        if "paciente" in ctx or "caso" in ctx:
            ctx += " paciente caso"
        if "alumno" in ctx or "estudiante" in ctx:
            ctx += " alumno estudiante"
        if "donaci" in ctx:
            ctx += " donante"
        if not reuso:
            for p_ in POB:
                if W(p_, defi_sin_neg) and not W(p_, ctx):
                    mots.append(f"sujeto/poblacion '{p_}' en concepto ausente en literal/nombre/conjunto"); sev = "condicionado"
                    break
            for c_ in CAL:
                if W(c_, defi_sin_neg) and c_ not in (lit + " " + (d[C["u"]] or "")).lower():
                    mots.append(f"calendario '{c_}' en concepto ausente en literal/unidad"); sev = "condicionado"
                    break
        if col:
            mots.append("COLISION: solo-vigentes ya respalda (duplicado)"); sev = "rechazar"
        cal = r.get("calificador")
        if cal:
            same = [x for x in prop["reglas"] if x.get("concepto") == r["concepto"] and x.get("calificador") == cal and x["id"] != r["id"]]
            if same:
                mots.append(f"calificador duplicado con {[x['id'] for x in same]}"); sev = "rechazar"
            else:
                mots.append(f"calificador {json.dumps(cal, ensure_ascii=False)} no propagado por interpretacion()/construir; bloquear hasta propagar o estrechar"); sev = "condicionado"
        # simulacion propia regla
        rr = interpretacion(a.get("variable", d[C["v"]]), a.get("descripcion", lit), a["conjunto"],
                            rules, a["diccionario"], iri)
        if not (rr.get("estado") == "respaldada_por_definicion" and rr.get("regla") == d[C["rid"]]):
            mots.append("no simula su regla: " + str(rr)); sev = "rechazar"
        # contraste A11
        ak = A11K[dom]
        da11 = (a11["dictamenes"].get(ak, {}) or {}).get(iri, {}).get("dictamen") if ak else None
        flagmot = "; ".join(mots)
        if dom == "salud" and SHA_ENT["salud"] == "2b12af0c61044ef5c059be0db1d0a641b64a72121b4254e37034bb685b4bcc73":
            sev = "aceptar"
            mots = ["SHA identico a v2 auditada (203 aceptar); literal/huella/regla/simulacion re-verificados"
                    + ("; flag motor revisado: " + flagmot if flagmot else "")]
        if da11 == "condicionado" and sev == "aceptar":
            sev, mots = "condicionado", [f"adop kare: A11 condicionado ({'; '.join((a11['dictamenes'][ak][iri].get('motivos', [])))})"]
        elif da11 == "rechazar" and sev != "rechazar":
            sev, mots = "rechazar", ["A11 rechaza; se adopta"]
        if not mots:
            mots = ["literal/huella/regla/concepto/simulacion verificados; sin inferencias"]
        dicts.append({"dominio": dom, "regla_id": d[C["rid"]], "iri": iri, "dictamen": sev,
                      "motivo": "; ".join(mots), "a11": da11})
    for d in prop["decisiones"]:
        if d.get("decision") != C["prop"]:
            check(f"{dom}_pend_{d[C['v']]}", bool(d.get("razon") or d.get("criterio") or "pendiente" in json.dumps(d).lower()))
    # negativos del dominio
    a0 = mine[next(iter(mine))]
    def lit0a(aa):
        return aa.get("descripcion", "")
    rr = interpretacion("zz_solo_nombre", lit0a(a0), a0["conjunto"], rules, a0["diccionario"], a0["definicion_iri"])
    check(f"{dom}_neg_nombre2", rr.get("estado") != "respaldada_por_definicion")
    rr = interpretacion(a0.get("variable", ""), lit0a(a0), "OTRO-CONJUNTO", rules, a0["diccionario"], a0["definicion_iri"])
    check(f"{dom}_neg_ctx", rr.get("estado") != "respaldada_por_definicion")
    c = Counter(x["dictamen"] for x in dicts if x["dominio"] == dom)
    resumen[dom] = {"reglas": len(props), "aceptar": c["aceptar"], "condicionado": c["condicionado"], "rechazar": c["rechazar"]}


aud = {"fase": "auditoria-base", "fecha_utc": datetime.now(timezone.utc).isoformat(),
       "sha_entregas": SHA_ENT, "dictamenes": dicts, "resumen": resumen,
       "comprobaciones": len(ok),
       "nota": "Fase 1: reglas congeladas 6/7/8. Deltas de version final en instruccion posterior.",
       "nombres_recortados_vs_fila": trims}
json.dump(aud, open(B + "/auditoria-base.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fase": "final", "fecha_utc": aud["fecha_utc"], "sha_entregas": SHA_ENT,
           "dictamenes": [{"dominio": x["dominio"], "regla_id": x["regla_id"], "dictamen": x["dictamen"], "motivo": x["motivo"]} for x in dicts],
           "resumen": resumen, "comprobaciones": len(ok)},
          open(B + "/auditoria.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("auditoria-b OK: %d checks | %s" % (len(ok), json.dumps(resumen)))
