"""Auditoría independiente ronda 3 (agente 11). Solo LEE fuera de su carpeta;
escribe UNICAMENTE en propuestas/ronda-3/agente-11-auditoria/.
Sin red, sin consolidar/ampliar/sincronizar, sin tocar núcleo ni otras propuestas.
Agente 6 excluido (audita agente 12). Agente 7: archivo sin cambios (SHA idéntico)."""
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ROOT = AQUI.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402  funciones puras
from integrar_contenido import valor as cvalor, clave  # noqa: E402  normalizacion central

PROP = {
    "a7": ROOT / "propuestas/ronda-3/agente-7-registro-civil" / "propuestas.json",
    "a3": ROOT / "propuestas/ronda-3/agente-3-cobertura" / "propuestas.json",
    "a8": ROOT / "propuestas/ronda-3/agente-8-educacion" / "propuestas.json",
    "a9": ROOT / "propuestas/ronda-3/agente-9-gobierno-digital" / "propuestas.json",
    "a10": ROOT / "propuestas/ronda-3/agente-10-territorio-economia" / "propuestas.json",
}
BASE_FILES = [
    "data/semantica/cobertura.json",
    "ontologia/semantica.json",
    "data/portal/contenido-inspeccion.json",
    "data/portal/inventario.json",
    "reports/pendientes-semanticos.json",
    "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
]
ESPERADO = {"a7": 163, "a8": 126, "a9": 243, "a10": 468, "a3": None}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def nk(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).strip().lower())
                   if unicodedata.category(c) != "Mn")


def fila_por_iri(insp, diccionario, definicion_iri):
    rec = next(r for r in insp["recursos"] if r["id"] == diccionario)
    idx = int(definicion_iri.rsplit("%2F", 1)[1]) - 1
    return rec, rec["definiciones"][idx]


UNIDADES = ("hectarea", "cabeza", "tonelada", "peso", "pesos", "mxn",
            "kilogramo", "gramo", "litro", "metro", "anos", "gb", "cpu")


def jaccard(a, b):
    def toks(s):
        t = nk(s)
        for w in ("estudiantes", "estudiante", "alumnos", "alumno"):
            t = t.replace(w, "alumn")
        return set(t.split())
    ta, tb = toks(a), toks(b)
    return len(ta & tb) / max(1, len(ta | tb))


def en_base(u, base):
    return any(re.search(r"\b%s\b" % v, base) for v in (u, u + "s", u + "es"))


def unidad_inventada(ctext, referentes):
    base = nk(referentes)
    t = nk(ctext)
    for u in UNIDADES:
        if re.search(r"\b%s\b" % u, t) and not en_base(u, base):
            return u
    return None


POBLACION = ("madre", "padre", "nacido", "alumn", "estudiant", "beneficiad",
             "difunto", "titulad", "egresad", "internad", "externad", "detenid",
             "encuestad", "victima")
SENSIBLE = ("indigena", "etnia", "afro", "lengua", "idioma", "hablante",
            "dialecto", "discapacidad", "enfermedad", "delito", "victima",
            "internad", "externad", "recluid", "detenid", "desaparecid")


def norm_decision(tag, d):
    if tag == "a7":
        return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
                "variable": d["variable"], "descripcion": d["descripcion"], "tipo": d["tipo"],
                "unidad": d["unidad"], "ejemplo": d["ejemplo"], "catalogo": d["catalogo_declarado"],
                "propuesta": d["decision"] == "propuesta-significado", "concepto": d.get("concepto"),
                "regla_id": d.get("regla_id"), "motivo": d.get("criterio")}
    if tag == "a8":
        return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
                "variable": d["variable"], "descripcion": d["descripcion"], "tipo": d["tipo_de_dato"],
                "unidad": d["unidad_de_medida"], "ejemplo": d["ejemplo_de_dato"],
                "catalogo": d["catalogo_de_referencia"], "propuesta": d["decision"] == "propuesta",
                "concepto": d.get("concepto"), "regla_id": d.get("regla_id"),
                "motivo": d.get("criterio") or d.get("motivo")}
    if tag == "a9":
        return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
                "variable": d["variable"], "descripcion": d["descripcion"], "tipo": d["tipo_de_dato"],
                "unidad": d["unidad_de_medida"], "ejemplo": d["ejemplo_de_dato"],
                "catalogo": d["catalogo_de_referencia"], "propuesta": d["veredicto"] == "propuesta",
                "concepto": d.get("concepto"), "regla_id": d.get("regla"), "motivo": d.get("razon") or d.get("motivo")}
    if tag == "a3":
        return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
                "variable": d["variable"], "descripcion": d["descripcion"], "tipo": d["tipo"],
                "unidad": d["unidad"], "ejemplo": d["ejemplo"], "catalogo": d["catalogo_declarado"],
                "propuesta": d["decision"] == "propuesta-significado", "concepto": d["concepto"],
                "regla_id": d["regla_id"], "motivo": d["criterio"]}
    # a10
    return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
            "variable": d["variable"], "descripcion": d["descripcion_literal"], "tipo": d["tipo_de_dato"],
            "unidad": d["unidad_de_medida"], "ejemplo": d["ejemplo_de_dato"],
            "catalogo": d["catalogo_de_referencia"], "propuesta": d["decision"] == "proponer",
            "concepto": d.get("concepto"), "regla_id": d.get("regla"), "motivo": d.get("motivo")}


def rep_justificada(rep, desc, tipo, ej, variable=""):
    t = nk(tipo)
    dl = desc.lower()
    if rep == "codigo":
        if re.match(r"^(cve|cv|clave|cod|codigo|id)[-_ ]|.*(_id$|^id_)", str(variable), re.IGNORECASE):
            return True
        if "clave" in dl or "codigo" in dl or "código" in dl or "identificador" in dl:
            return True
        if "indicador" in dl and any(w in t for w in ("numerico", "entero", "numero", "numeric", "binario")):
            return True
        # clasificacion con ejemplo numerico y catalogo o mencion de clasificacion:
        # lectura codigo sin mapear valores (ejemplos nunca sustituyen descripciones)
        ejs = str(ej).strip()
        if re.fullmatch(r"0*\d+", ejs) and "clasific" in nk(desc):
            return True
        return False
    if rep == "nombre":
        ejs = str(ej).strip()
        if ejs not in ("", "SI", "NO", "NO APLICA", "N") and len(ejs) > 2:
            return True
        return "nombre" in dl or "denomina" in dl
    if rep == "fecha":
        return tipo == "Fecha"
    if rep == "hora":
        return tipo == "Hora" or "hora" in nk(desc)
    if rep in ("anio", "mes"):
        return "ano" in nk(desc) or rep in t or "mes" in nk(desc)
    return True


DUROS = {"iri_en_cobertura", "huella_coincide", "evidencia_exacta", "alcance_simultaneo",
         "sin_mapeo_codigo_nombre", "prosa_sin_literal", "sin_colision_nucleo",
         "broader_valido", "reutilizacion_central", "sin_columna_fisica"}


CURADO = {
    # A7 y A3: archivo sin cambios; se conservan los 26 dictámenes de la entrega anterior.
    "r3a7-nac-fechanacimiento-fecha": "sujeto 'nacido' ausente en literal; inferido de conjunto/vecinas con limite; sin cruces",
    "r3a7-nac-horanacimiento-hora": "sujeto 'nacido' ausente en literal; inferido de conjunto/vecinas con limite; sin cruces",
    "r3a7-nac-hijosnacidosmuertos-no_especificada": "literal sin 'madre'; concepto anade madre por contexto; con limite, sin cruces",
    "r3a7-nac-hijosnacidosvivos-no_especificada": "literal sin 'madre'; concepto anade madre por contexto; con limite, sin cruces",
    "r3a7-nac-hijossobrevivientes-no_especificada": "literal sin 'madre'; concepto anade madre por contexto; con limite, sin cruces",
    "r3a7-nac-condicionhijoanterior-codigo": "literal sin 'madre'; codigo y texto unificados; con limite documental",
    "r3a7-nac-condicionhijoanteriord-nombre": "literal sin 'madre'; codigo y texto unificados; con limite documental",
    "r3a7-nac-vivehijoanterior-codigo": "literal sin 'madre'; valores no documentados; con limite",
    "r3a7-nac-vivehijoanteriord-no_especificada": "literal sin 'madre'; ejemplo NO APLICA; con limite",
    "r3a7-nac-edadpadre-no_especificada": "ejemplo '99' sugiere posible codigo de desconocido; nulos no documentados; verificar nulos",
    "r3a7-nac-resideextranjero-codigo": "DEVUELTO por integrador a A7: residencia-extranjero-madre != residente extranjera (par textual pendiente por contradiccion); separar, no unificar",
    "r3a7-nac-tipocesaread-nombre": "ejemplo 'PROGRAMADO' no corresponde a binario 'si fue cesarea'; posible tipologia no documentada; con limite",
    "r3a7-nac-nacioextranjero-codigo": "contradiccion nombre/descripcion (nacer fuera vs ser extranjera); concepto neutral sin deducir lugar; con limite",
    "r3a7-nac-nacioextranjerod-no_especificada": "contradiccion nombre/descripcion; concepto neutral sin deducir lugar; con limite",
    "r3a3-superficie-sembrada-trigo-ddr-1": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-2": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-3": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-4": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-5": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-6": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-7": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-8": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-9": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-superficie-sembrada-trigo-ddr-10": "concepto compartido x10; distincion solo por calificador: NO aprobar perdiendo DDR; condicionado a implementacion central posterior (integrador)",
    "r3a3-organizacion-1": "reutiliza 'organizacion' para 'Institucion generadora del dato' (ej unico); papel generadora vs publicadora no distinguido; con limite, sin cruces",
}


# equivalencias vacias documentadas en filas (sin catalogo publicado)
VACIO_EQ = {"", "no aplica", "n/a", "no", "ninguno", "ninguna", "na", "-", "vacio", "campo vacio"}


def auditar_regla(tag, rule, dec, conceptos_nuevos, vmap, filas, central, grupos_concepto):
    rid = rule["id"]
    slug = rule["concepto"]
    ev0 = rule.get("evidencia", [{}])[0]
    rep = {"regla": rid, "definicion_iri": rule["definiciones"][0],
           "concepto": slug, "representacion": rule.get("representacion"),
           "variable": ev0.get("variable"), "descripcion": ev0.get("descripcion"),
           "dictamen": None, "motivos": [], "chequeos": {}}
    if "evidencia" in rule:
        ev = rule["evidencia"][0]
    else:  # a7: la evidencia vive en la decision (regla sin evidencia propia)
        ev = {"variable": dec["variable"], "descripcion": dec["descripcion"],
              "definicion_iri": dec["iri"], "diccionario": dec["diccionario"],
              "conjunto": dec["conjunto"], "unidad_de_medida": dec["unidad"],
              "tipo_de_dato": dec["tipo"], "ejemplo_de_dato": dec["ejemplo"],
              "catalogo_de_referencia": dec["catalogo"]}
    iri = rule["definiciones"][0]
    c = rep["chequeos"]
    c["iri_en_cobertura"] = iri in vmap and iri == dec["iri"]
    if iri not in vmap:
        rep["dictamen"] = "rechazar"
        rep["motivos"].append("IRI de definicion inexistente en cobertura base")
        return rep
    vv = vmap[iri]
    _rec, row = fila_por_iri(insp_global, ev["diccionario"], iri)
    c["huella_coincide"] = huella(row) == vv["huella_fila_diccionario"]
    f = filas[(ev["diccionario"], int(iri.rsplit("%2F", 1)[1]))]
    cat_ev, cat_f = nk(ev["catalogo_de_referencia"]), nk(f["catalogo"])
    cat_ok = (cat_ev == cat_f or (cat_ev == "" and cat_f in VACIO_EQ)
              or (cat_f == "" and cat_ev in VACIO_EQ))
    c["evidencia_exacta"] = (ev["descripcion"].strip() == f["descripcion"].strip()
                             and ev["unidad_de_medida"].strip() == f["unidad"].strip()
                             and ev["tipo_de_dato"].strip() == f["tipo"].strip()
                             and str(ev["ejemplo_de_dato"]).strip() == str(f["ejemplo"]).strip()
                             and cat_ok
                             and ev["diccionario"] == vv["diccionario"] and ev["conjunto"] == vv["conjunto"]
                             and ev["variable"] == vv["variable"] and ev["variable"] == dec["variable"]
                             and ev["descripcion"] == dec["descripcion"])
    if ev["catalogo_de_referencia"].strip() == "" and nk(f["catalogo"]) not in ("",):
        c["catalogo_no_aplica_normalizado"] = f["catalogo"]
    c["alcance_simultaneo"] = (len(rule["conjuntos"]) == 1 and len(rule["diccionarios"]) == 1
                               and len(rule["definiciones"]) == 1 and len(rule["nombres"]) == 1
                               and len(rule["descripciones"]) == 1
                               and rule["conjuntos"] == [ev["conjunto"]] and rule["diccionarios"] == [ev["diccionario"]]
                               and rule["nombres"] == [ev["variable"]] and rule["descripciones"] == [ev["descripcion"]])
    c["rep_justificada"] = rep_justificada(rule["representacion"], ev["descripcion"], ev["tipo_de_dato"],
                                           ev["ejemplo_de_dato"], ev["variable"])
    if slug in conceptos_nuevos:
        ctext = conceptos_nuevos[slug][0] + " " + conceptos_nuevos[slug][1]
        m_unidad = ev["unidad_de_medida"]
        m = re.search(r"[Uu]nidad literal de la fila:\s*([^.]+)\.", ctext)
        if m:
            if m.group(1).strip() == m_unidad:
                c["unidad_igual_evidencia"] = True
            else:
                c["unidad_igual_evidencia"] = False
                c["motivo_unidad"] = "formula de unidad '%s' no coincide con evidencia '%s'" % (m.group(1).strip(), m_unidad)
        elif "Sin unidad declarada" in ctext:
            c["unidad_igual_evidencia"] = (m_unidad == "")
            if m_unidad != "":
                c["motivo_unidad"] = "afirma sin unidad pero la fila trae '%s'" % m_unidad
        else:
            inv = unidad_inventada(ctext, " ".join((m_unidad, ev["descripcion"], ev.get("ejemplo_de_dato", ""))))
            c["unidad_igual_evidencia"] = inv is None
            if inv:
                c["motivo_unidad"] = "unidad '%s' afirmada en concepto sin respaldo en literal/unidad/ejemplo" % inv
        blob = (ctext + " " + slug).lower()
        c["sin_mapeo_codigo_nombre"] = not re.search(r"\b\d+\s*=\s*[a-z\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1]", blob)
        prosa = (rule.get("positivo", "") + " " + rule.get("contraejemplo", "") + " " + rule.get("limite", ""))
        c["prosa_sin_literal"] = ev["descripcion"] not in prosa
        c["sin_colision_nucleo"] = slug not in central
        c["broader_valido"] = (conceptos_nuevos[slug][2] is None
                               or conceptos_nuevos[slug][2] in central
                               or conceptos_nuevos[slug][2] in conceptos_nuevos)
    else:
        c["reutilizacion_central"] = slug in central
    c["sin_columna_fisica"] = "/file-column/" not in json.dumps(rule) and "/column/" not in json.dumps(rule)
    # flags suaves
    refs = nk(dec["descripcion"] + " " + dec["variable"] + " " + dec["tipo"] + " " + dec["unidad"])
    ctxt = nk(ctext) if slug in conceptos_nuevos else ""
    # sinonimos alumno<->estudiante: misma poblacion, no inferencia
    refs = re.sub(r"(alumn\w*|estudiant\w*)", "alumnx", refs)
    ctxt = re.sub(r"(alumn\w*|estudiant\w*)", "alumnx", ctxt)
    # alcance acotado al registro/diccionario de origen: observacion, no condicion
    scope = (re.search(r"registro de [\w ]*(?:%s)" % "|".join(POBLACION), ctxt)
             or re.search(r"(?:%s) registrad" % "|".join(POBLACION), ctxt))
    alcance_origen = bool(scope)
    anadida = [] if alcance_origen else [w for w in POBLACION if re.search(r"\b%s" % w, ctxt) and w not in refs]
    c["poblacion_no_anadida"] = anadida == []
    if anadida:
        c["poblacion_anadida"] = anadida
    if alcance_origen:
        c["alcance_acotado_origen"] = True
    t = nk(dec["tipo"])
    ej = str(dec["ejemplo"]).strip()
    c["ejemplo_coherente"] = not (any(w in t for w in ("numerico", "entero", "numero", "numeric"))
                                  and ej != "" and not any(ch.isdigit() for ch in ej))
    sens = sorted({w for w in SENSIBLE if re.search(r"\b%s" % w, nk(dec["descripcion"] + " " + ctxt))})
    c["sin_atributo_sensible"] = sens == []
    if sens:
        c["atributo_sensible"] = sens
    grupo = grupos_concepto.get(slug, [])
    if len(grupo) > 1:
        descs = sorted({g.get("evidencia", [{"descripcion": g["descripciones"][0]}])[0]["descripcion"] for g in grupo})
        reps_g = {g.get("representacion") for g in grupo}
        califs = {json.dumps(g.get("calificador"), sort_keys=True) for g in grupo}
        if len(descs) == 1:
            c["concepto_compartido_mismo_literal"] = True
        elif reps_g <= {"codigo", "nombre", "no_especificada"} and "nombre" in reps_g and len(reps_g) > 1:
            c["concepto_compartido_par_representaciones"] = True
        elif rule.get("calificador") and len(califs) == len(grupo):
            c["concepto_compartido_calificador_distinto"] = True
        elif max(jaccard(descs[i], descs[j]) for i in range(len(descs)) for j in range(i + 1, len(descs))) >= 0.6:
            c["concepto_compartido_casi_identico"] = True
        else:
            c["concepto_compartido_distinto_literal"] = descs[:3]
    duros = [k for k, okv in c.items() if okv is False and k in DUROS]
    if duros:
        rep["dictamen"] = "rechazar"
        rep["motivos"].append("chequeos duros fallidos: " + ",".join(duros))
        return rep
    cond = []
    if rid in CURADO:
        cond.append(CURADO[rid])
    if rule.get("calificador") and rid not in CURADO:
        req = bool(rule.get("requisito_integracion")) or "propaga" in (rule.get("limite", "") or "")
        cond.append("concepto compartido; distincion solo por calificador %s: NO aprobar perdiendo sede/DDR; condicionado a implementacion central posterior (%s)"
                    % (json.dumps(rule["calificador"]), "requisito documentado" if req else "SIN requisito explicito"))
    if c.get("motivo_unidad"):
        cond.append(c["motivo_unidad"] + "; con limite (retirar o respaldar; sin habilitar cruces)")
    if not c["rep_justificada"]:
        cond.append("representacion '%s' no justificada por el literal (descripcion/tipo/ejemplo); con limite, sin tipificar valores" % rule["representacion"])
    if c.get("poblacion_anadida") and rid not in CURADO:
        cond.append("poblacion %s inferida del contexto, ausente en literal; con limite, sin cruces" % c["poblacion_anadida"])
    if not c["ejemplo_coherente"]:
        cond.append("ejemplo '%s' incoherente con tipo %s; no tipificar monto/conteo; con limite" % (ej, dec["tipo"]))
    if c.get("atributo_sensible"):
        cond.append("atributo sensible/vulnerable %s: significado neutro documentado con limite; sin catalogo que defina valores; sin cruces ni promocion" % c["atributo_sensible"])
    if c.get("concepto_compartido_distinto_literal"):
        cond.append("mismo concepto para literales distintos; verificar equivalencia antes de aplicar")
    if c.get("unidad_inventada"):
        cond.append("unidad '%s' afirmada en concepto sin respaldo en literal/unidad/ejemplo; retirar o respaldar" % c["unidad_inventada"])
    if cond:
        rep["dictamen"] = "condicionado"
        rep["motivos"] = cond
    else:
        rep["dictamen"] = "aceptar"
        nota = "literal especifico, alcance simultaneo, representacion conservadora"
        if c.get("concepto_compartido_mismo_literal"):
            nota += "; reutilizacion mismo literal"
        if c.get("concepto_compartido_par_representaciones"):
            nota += "; par de representaciones del mismo objeto"
        if c.get("concepto_compartido_casi_identico"):
            nota += "; literales casi identicos"
        if c.get("alcance_acotado_origen"):
            nota += "; alcance acotado al registro de origen"
        if c.get("catalogo_no_aplica_normalizado"):
            nota += "; catalogo '%s' normalizado a vacio" % c["catalogo_no_aplica_normalizado"]
        rep["motivos"].append(nota)
    return rep


def crudo(row, names):
    for key, value in row.items():
        if clave(key) in names and isinstance(value, str):
            return value
    return ""


def main():
    global insp_global
    antes = {f: sha(ROOT / f) for f in BASE_FILES}
    for tag, p in PROP.items():
        antes[tag] = sha(p)
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    insp_global = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
    asign = json.loads((ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json").read_text(encoding="utf-8"))
    central = set(sem["conceptos"])
    vmap = {v["definicion_iri"]: v for v in cob["variables"]}
    filas = {}
    for rec in insp_global["recursos"]:
        for idx, row in enumerate(rec.get("definiciones", [])):
            filas[(rec["id"], idx + 1)] = {
                "descripcion": crudo(row, {"descripcion", "definicion"}),
                "unidad": crudo(row, {"unidad de medida", "unidades de medida"}),
                "tipo": crudo(row, {"tipo de dato"}),
                "ejemplo": crudo(row, {"ejemplo de dato"}),
                "catalogo": crudo(row, {"catalogo de referencia", "catalago de referencia"})}

    base_ok = (len(cob["conceptos"]) == 103 and len(sem["conceptos"]) == 103
               and sum(1 for v in cob["variables"] if v.get("estado") == "respaldada_por_definicion") == 232
               and sum(1 for v in cob["variables"] if v.get("estado") == "fuera_del_nucleo_actual") == 1308
               and pend["resumen"]["estados_columnas"].get("documental_revisada") == 836
               and pend["resumen"]["estados_columnas"].get("candidata_por_nombre") == 118)
    props = {tag: json.loads(p.read_text(encoding="utf-8")) for tag, p in PROP.items()}
    # particiones exactas, disjuntas, fuera del núcleo
    todas_iris = {}
    particion_ok = True
    for tag, p in props.items():
        if "decisiones" in p:
            nds = [norm_decision(tag, d) for d in p["decisiones"]]
        else:  # a3: sin arreglo de decisiones; se derivan de la evidencia de cada regla
            nds = [{"iri": r["definiciones"][0], "conjunto": r["conjuntos"][0], "diccionario": r["diccionarios"][0],
                    "variable": r["nombres"][0], "descripcion": r["descripciones"][0],
                    "tipo": r["evidencia"][0]["tipo_de_dato"], "unidad": r["evidencia"][0]["unidad_de_medida"],
                    "ejemplo": r["evidencia"][0]["ejemplo_de_dato"],
                    "catalogo": r["evidencia"][0]["catalogo_de_referencia"],
                    "propuesta": True, "concepto": r["concepto"], "regla_id": r["id"],
                    "motivo": r.get("limite", "")} for r in p["reglas"]]
        if tag in ESPERADO and ESPERADO[tag] and len(nds) != ESPERADO[tag]:
            particion_ok = False
        iris = [d["iri"] for d in nds]
        if len(set(iris)) != len(iris):
            particion_ok = False
        todas_iris[tag] = (set(iris), nds)
    vistos = set()
    for tag, (iris, _nds) in todas_iris.items():
        if vistos & iris:
            particion_ok = False
        vistos |= iris

    dicts, resumen, nuevos_todos = {}, {}, {}
    for tag, p in props.items():
        grupos = {}
        for r in p["reglas"]:
            grupos.setdefault(r["concepto"], []).append(r)
        dd = {}
        for r in p["reglas"]:
            dec = next(x for x in todas_iris[tag][1] if x["regla_id"] == r["id"] and x["propuesta"])
            dd[r["id"]] = auditar_regla(tag, r, dec, p["conceptos_nuevos"], vmap, filas, central, grupos)
        # pendientes sin regla ni concepto (a3 documenta sus 3 leidas-sin-propuesta en inventario)
        if tag == "a3":
            noprop = {(v["diccionario"], v["variable"]) for v in vmap.values()
                      if (v["diccionario"], v["variable"]) in {
                          ("863b9cc8-daeb-4430-b835-6a0ced5abd31", "CVOTRAS"),
                          ("863b9cc8-daeb-4430-b835-6a0ced5abd31", "DOTRAS"),
                          ("a7591bc9-f905-45cb-ba6c-ae3588d87594", "GRUPO")}}
            assert len(noprop) == 3
            assert not (noprop & {(ev["diccionario"], ev["variable"]) for r in p["reglas"]
                                  for ev in [r["evidencia"][0]]})
        else:
            for d in todas_iris[tag][1]:
                if not d["propuesta"]:
                    assert d["regla_id"] is None and d["concepto"] is None, (tag, d["iri"])
                    assert isinstance(d["motivo"], str) and len(d["motivo"]) > 5, (tag, d["iri"])
        dicts[tag] = dd
        resumen[tag] = dict(Counter(v["dictamen"] for v in dd.values()))
        assert sum(resumen[tag].values()) == len(p["reglas"])
        nuevos_todos[tag] = set(p["conceptos_nuevos"])
        for s in p.get("conceptos_reutilizados", []):
            assert s in central, (tag, s)

    conflictos = {
        "nuevos_vs_nucleo": sorted(set().union(*[nuevos_todos[t] & central for t in nuevos_todos])),
        "cruzados": sorted({s for t1 in nuevos_todos for t2 in nuevos_todos if t1 < t2
                             for s in nuevos_todos[t1] & nuevos_todos[t2]}),
        "a7_sin_cambios": antes["a7"] == "f075f8841b860f2babfe49707d6554c46dc0b4addfe280830eeaf906fc947049",
    }
    # pipeline: todas las reglas disparan (validador real)
    ext = {}
    for tag, p in props.items():
        ext[tag] = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
            {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
             "representacion": r["representacion"], "nombres": r.get("nombres"),
             "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
             "definiciones": r.get("definiciones")} for r in p["reglas"]]}
    npos = 0
    for tag, p in props.items():
        for r in p["reglas"]:
            dec = next(x for x in todas_iris[tag][1] if x["regla_id"] == r["id"])
            got = interpretacion(dec["variable"], dec["descripcion"], dec["conjunto"], ext[tag],
                                 dec["diccionario"], dec["iri"])
            assert got.get("estado") == "respaldada_por_definicion" and got.get("concepto") == r["concepto"], r["id"]
            npos += 1
    # calificador no propagado (SHD + sedes)
    shd = next(r for r in props["a3"]["reglas"] if r.get("calificador"))
    vv = vmap[shd["definiciones"][0]]
    sede = next(r for r in props["a8"]["reglas"] if r.get("calificador"))
    vvs = vmap[sede["definiciones"][0]]
    comportamiento = {
        "positivos_totales": npos,
        "a3_calificador_no_propagado": "calificador" not in interpretacion(
            vv["variable"], vv["descripcion"], vv["conjunto"], ext["a3"], vv["diccionario"], shd["definiciones"][0]),
        "a8_calificador_no_propagado": "calificador" not in interpretacion(
            vvs["variable"], vvs["descripcion"], vvs["conjunto"], ext["a8"], vvs["diccionario"], sede["definiciones"][0]),
        "nota_negativos": "A7/A8/A9 alimentan interpretacion()/validar centrales con entradas mutadas; ninguno se auto-lanza ValueError",
        "a10_verificador_local": "scripts/verificar.py de A10 define interpretacion() local (matcher de tuplas exactas, muestra de 40 reglas); no alimenta el pipeline central: esta auditoria re-ejecuta las 419 con consolidar_semantica.interpretacion real",
    }
    despues = {f: sha(ROOT / f) for f in BASE_FILES}
    for tag, p in PROP.items():
        despues[tag] = sha(p)
    estable = antes == despues
    auditoria = {
        "agente": "ronda-3/agente-11-auditoria",
        "rol": "auditor independiente; excluye agente 6 (audita agente 12); no propone conceptos ni reglas",
        "base_verificada": base_ok and particion_ok,
        "conteos_base": {"conceptos": 103, "respaldadas": 232, "fuera_nucleo": 1308,
                         "revisadas": 836, "candidatas": 118, "candidatas_ag4": 23},
        "huellas_antes": antes, "huellas_despues": despues, "fuentes_estables": estable,
        "dictamenes": dicts, "resumen": resumen, "conflictos_iris": conflictos,
        "comportamiento_pipeline": comportamiento,
        "limites": ["solo significado documental; vinculo fisico, vigencia e identidad no acreditados",
                    "condicionados requieren accion del integrador; no habilitan cruces ni promociones",
                    "SHD/sedes bloqueados hasta propagar calificador o crear conceptos estrechos",
                    "A10 sin scripts/verificar.py: positivos re-ejecutados por esta auditoria"],
    }
    (AQUI / "auditoria.json").write_text(json.dumps(auditoria, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "fuente" / "huellas.json").write_text(json.dumps(
        {"antes": antes, "despues": despues, "estables": estable}, ensure_ascii=False, indent=1), encoding="utf-8")
    print({t: resumen[t] for t in resumen}, "base_ok=", base_ok and particion_ok, "estable=", estable)


if __name__ == "__main__":
    main()
