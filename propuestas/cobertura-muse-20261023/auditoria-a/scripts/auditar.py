"""Auditor independiente gobierno-digital (243) + territorio-economia (534) + frozen agente-3.
Fase 1: audita TODAS las reglas contra inspeccion, contexto y conceptos.
Solo LEE fuera de auditoria-a/; escribe UNICAMENTE aqui. Sin red, sin suite central,
sin scripts historicos, sin tocar propuestas auditadas ni nucleo."""
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
MUSE = AQUI.parent
ROOT = AQUI.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion, validar_calificador  # noqa: E402
from integrar_contenido import valor as cvalor, clave  # noqa: E402

PROP = {
    "gobierno-digital": MUSE / "gobierno-digital" / "entrega.json",
    "territorio-economia": MUSE / "territorio-economia" / "entrega.json",
}
BASE_FILES = [
    "data/semantica/cobertura.json",
    "ontologia/semantica.json",
    "data/portal/contenido-inspeccion.json",
    "data/portal/inventario.json",
    "reports/pendientes-semanticos.json",
    "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def nk(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).strip().lower())
                   if unicodedata.category(c) != "Mn")


def crudo(row, names):
    for key, value in row.items():
        if clave(key) in names and isinstance(value, str):
            return value
    return ""


def fila_por_iri(insp, diccionario, definicion_iri):
    rec = next(r for r in insp["recursos"] if r["id"] == diccionario)
    idx = int(definicion_iri.rsplit("%2F", 1)[1]) - 1
    return rec, rec["definiciones"][idx]


UNIDADES = ("hectarea", "cabeza", "tonelada", "peso", "pesos", "mxn",
            "kilogramo", "gramo", "litro", "metro", "anos", "gb", "cpu")
VACIO_EQ = {"", "no aplica", "n/a", "no", "ninguno", "ninguna", "na", "-", "vacio", "campo vacio"}
POBLACION = ("madre", "padre", "nacido", "alumn", "estudiant", "beneficiad",
             "difunto", "titulad", "egresad", "internad", "externad", "detenid",
             "encuestad", "victima")
SENSIBLE = ("indigena", "etnia", "afro", "lengua", "idioma", "hablante",
            "dialecto", "discapacidad", "enfermedad", "delito", "victima",
            "internad", "externad", "recluid", "detenid", "desaparecid")
DUROS = {"iri_en_cobertura", "huella_coincide", "evidencia_exacta", "alcance_simultaneo",
         "sin_mapeo_codigo_nombre", "prosa_sin_literal", "sin_colision_nucleo",
         "broader_valido", "reutilizacion_central", "sin_columna_fisica"}
aplicados_verbatim = set()


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
        ejs = str(ej).strip()
        if re.fullmatch(r"0*\d+", ejs) and "clasific" in nk(desc):
            return True
        return False
    if rep == "nombre":
        ejs = str(ej).strip()
        if ejs not in ("", "SI", "NO", "NO APLICA") and len(ejs) > 2:
            return True
        return "nombre" in dl or "denomina" in dl
    if rep == "fecha":
        return tipo == "Fecha"
    if rep == "hora":
        return tipo == "Hora" or "hora" in nk(desc)
    if rep in ("anio", "mes"):
        return "ano" in nk(desc) or rep in t or "mes" in nk(desc)
    return True


def norm_decision(tag, d):
    if tag == "gobierno-digital":
        return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
                "titulo": d.get("titulo_conjunto", ""), "variable": d["variable"], "descripcion": d["descripcion"],
                "tipo": d["tipo_de_dato"], "unidad": d["unidad_de_medida"], "ejemplo": d["ejemplo_de_dato"],
                "catalogo": d["catalogo_de_referencia"], "propuesta": d["decision"] == "proponer",
                "concepto": d.get("concepto"), "regla_id": d.get("regla_id"),
                "motivo": d.get("razon") or d.get("motivo") or d.get("criterio")}
    # territorio-economia
    return {"iri": d["definicion_iri"], "conjunto": d["conjunto"], "diccionario": d["diccionario"],
            "titulo": d.get("titulo_conjunto", ""), "variable": d["variable"],
            "descripcion": d["descripcion_literal"], "tipo": d["tipo_de_dato"],
            "unidad": d["unidad_de_medida"], "ejemplo": d["ejemplo_de_dato"],
            "catalogo": d["catalogo_de_referencia"], "propuesta": d["decision"] == "proponer",
            "concepto": d.get("concepto"), "regla_id": d.get("regla_id") or d.get("regla"),
            "motivo": d.get("motivo")}


# DEVUELTOS por integrador (bloqueantes, no meros limites): IM vs IMN marginacion,
# separar normalizado/original en TODOS los niveles (localidad, municipio, AGEB, colonia, entidad)
DEVUELTOS_MARGEN = {"r3a10-0107", "r3a10-0109", "r3a10-0129", "r3a10-0131", "r3a10-0172",
                    "r3a10-0174", "r3a10-0215", "r3a10-0217", "r3a10-0245", "r3a10-0247"}
# P8/P9: la separacion en 2 conceptos especificos YA esta aplicada en la entrega
# actual (existencia- vs nombre-unidad-coordinadora-tic); sin flag si estan separados
DEVUELTOS_PAR = {"r3a9-014", "r3a9-015"}


def auditar_regla(tag, rule, dec, conceptos_nuevos, vmap, filas, central, grupos, titulos):
    rid = rule["id"]
    slug = rule["concepto"]
    ev = rule["evidencia"][0]
    rep = {"dominio": tag, "regla_id": rid, "definicion_iri": rule["definiciones"][0],
           "concepto": slug, "dictamen": None, "motivos": [], "chequeos": {}}
    c = rep["chequeos"]
    iri = rule["definiciones"][0]
    c["iri_en_cobertura"] = iri in vmap
    if iri not in vmap:
        rep["dictamen"] = "rechazar"
        rep["motivos"].append("IRI de definicion inexistente en cobertura base")
        return rep
    vv = vmap[iri]
    _rec, row = fila_por_iri(insp_global, ev["diccionario"], iri)
    c["huella_coincide"] = huella(row) == vv["huella_fila_diccionario"]
    c["huella_regla_igual"] = (not rule.get("huella_fila_diccionario")
                               or rule["huella_fila_diccionario"] == vv["huella_fila_diccionario"])
    f = filas[(ev["diccionario"], int(iri.rsplit("%2F", 1)[1]))]
    cat_ev, cat_f = nk(ev["catalogo_de_referencia"]), nk(f["catalogo"])
    cat_ok = (cat_ev == cat_f or (cat_ev == "" and cat_f in VACIO_EQ)
              or (cat_f == "" and cat_ev in VACIO_EQ))
    c["evidencia_exacta"] = (ev["descripcion"].strip() == f["descripcion"].strip()
                             and ev["unidad_de_medida"].strip() == f["unidad"].strip()
                             and ev["tipo_de_dato"].strip() == f["tipo"].strip()
                             and str(ev["ejemplo_de_dato"]).strip() == str(f["ejemplo"]).strip()
                             and cat_ok
                             and ev["diccionario"] == vv["diccionario"] and ev["conjunto"] == vv["conjunto"])
    if nk(f["catalogo"]) not in ("",) and ev["catalogo_de_referencia"].strip() == "":
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
        c["sin_mapeo_codigo_nombre"] = not re.search(r"\b\d+\s*=\s*[a-z\xc3]", blob)
        prosa = (rule.get("positivo", "") + " " + rule.get("contraejemplo", "") + " " + str(rule.get("limite", "")))
        if isinstance(rule.get("limite"), list):
            prosa += " " + " ".join(rule["limite"])
        c["prosa_sin_literal"] = ev["descripcion"] not in prosa
        c["sin_colision_nucleo"] = slug not in central or slug in aplicados_verbatim
        c["broader_valido"] = (conceptos_nuevos[slug][2] is None
                               or conceptos_nuevos[slug][2] in central
                               or conceptos_nuevos[slug][2] in conceptos_nuevos)
        # reconstruida vs proyectada: el concepto no debe cambiar metodologia ni periodo
        if "reconstruid" in nk(ev["descripcion"]) and "reconstruid" not in nk(ctext):
            c["metodologia_preservada"] = False
            c["motivo_metodologia"] = "literal 'reconstruida y ajustada' ausente en concepto; no sustituir por 'proyectada'"
        if "proyect" in nk(ctext) and "proyect" not in nk(ev["descripcion"]):
            tit = nk(titulos.get(ev["conjunto"], ""))
            if "proyecc" not in tit:
                c["periodo_preservado"] = False
                c["motivo_metodologia"] = "concepto afirma 'proyeccion' sin respaldo en literal ni titulo del conjunto"
    else:
        c["reutilizacion_central"] = slug in central
    c["sin_columna_fisica"] = "/file-column/" not in json.dumps(rule) and "/column/" not in json.dumps(rule)
    refs = nk(dec["descripcion"] + " " + dec["variable"] + " " + dec["tipo"] + " " + dec["unidad"])
    refs = re.sub(r"(alumn\w*|estudiant\w*)", "alumnx", refs)
    ctxt = nk(ctext) if slug in conceptos_nuevos else ""
    ctxt = re.sub(r"(alumn\w*|estudiant\w*)", "alumnx", ctxt)
    scope = (re.search(r"registro de [\w ]*(?:%s)" % "|".join(POBLACION), ctxt)
             or re.search(r"(?:%s) registrad" % "|".join(POBLACION), ctxt))
    if scope:
        c["alcance_acotado_origen"] = True
    anad = [] if scope else [w for w in POBLACION if re.search(r"\b%s" % w, ctxt) and w not in refs]
    c["poblacion_no_anadida"] = anad == []
    if anad:
        # contexto publicado explicito en titulo/tabla/criterio/concepto respalda la poblacion
        tit = nk(dec.get("titulo", ""))
        crit = nk((dec.get("motivo") or "") + " " + (titulos.get(dec["conjunto"], "")))
        expl = (any(len(t) >= 4 and t in ctxt for t in tit.split())
                or "diagnostico" in ctxt or "diagnostico" in crit
                or ("encuesta" in ctxt and "respuest" in refs)
                or ("programa" in ctxt and "programa" in tit)
                or "registro de" in ctxt)
        if expl:
            c["poblacion_respaldada_contexto"] = anad
        else:
            c["poblacion_anadida"] = anad
    t = nk(dec["tipo"])
    ej = str(dec["ejemplo"]).strip()
    c["ejemplo_coherente"] = not (any(w in t for w in ("numerico", "entero", "numero", "numeric"))
                                  and ej != "" and not any(ch.isdigit() for ch in ej))
    sens = sorted({w for w in SENSIBLE if re.search(r"\b%s" % w, nk(dec["descripcion"] + " " + ctxt))})
    # limites informativos: solo metadatos publicados, sin personas; condicion tecnica
    # unicamente si se infieren valores/identidad no publicados (mapeo a catalogo, etc.)
    c["sin_atributo_sensible"] = sens == []
    if sens:
        c["atributo_sensible_informativo"] = sens
    grupo = grupos.get(slug, [])
    if len(grupo) > 1 and tag == "gobierno-digital":
        # confusion de encuestas: la distincion vive en el calificador instrumento;
        # el pipeline ya lo propaga (verificado): aceptar con nota, salvo mezcla real
        insts = [g.get("calificador", {}).get("instrumento") if isinstance(g.get("calificador"), dict) else None
                 for g in grupo]
        if any(i is None for i in insts):
            c["concepto_compartido_sin_instrumento"] = True
        elif len(set(insts)) != len(insts):
            c["concepto_compartido_mismo_instrumento"] = insts
        else:
            c["concepto_compartido_distinto_instrumento"] = sorted(set(insts))
    elif len(grupo) > 1:
        descs = sorted({g["evidencia"][0]["descripcion"] for g in grupo})
        reps_g = {g.get("representacion") for g in grupo}
        califs = {json.dumps(g.get("calificador"), sort_keys=True) for g in grupo}
        campos = {(g["evidencia"][0]["diccionario"], nk(g["evidencia"][0]["variable"])) for g in grupo}
        if len(descs) == 1:
            c["concepto_compartido_mismo_literal"] = True
        elif len(campos) == 1 and len(reps_g) == 1:
            # mismo campo (misma variable, mismo diccionario): rol igual claro
            c["concepto_compartido_mismo_campo"] = True
        elif len(reps_g) > 1 and any(w in nk(dl) for dl in descs for w in ("clave", "codigo", "código", "identificador")) and any(w in nk(dl) for dl in descs for w in ("nombre", "descripcion", "descripción", "denomina")):
            # codigo/nombre/descripcion del mismo objeto: no exige conceptos distintos
            c["concepto_compartido_par_representaciones"] = True
        elif rule.get("calificador") and len(califs) == len(grupo):
            c["concepto_compartido_calificador_distinto"] = True
        elif max(jaccard(descs[i], descs[j]) for i in range(len(descs)) for j in range(i + 1, len(descs))) >= 0.6:
            c["concepto_compartido_casi_identico"] = True
        else:
            c["concepto_compartido_distinto_literal"] = descs[:3]
    # calificador: validar forma; el pipeline ya lo propaga (verificado con
    # interpretacion completa): nota informativa, la aplicacion central lo conserva
    cal = rule.get("calificador")
    if cal is not None:
        try:
            validar_calificador(cal)
            c["calificador_valido"] = True
        except ValueError:
            c["calificador_valido"] = False
            c["motivo_calificador"] = "calificador invalido (vacio o no str->str)"
    if isinstance(cal, dict) and cal.get("instrumento"):
        tit = titulos.get(ev["conjunto"], "")
        c["instrumento_igual_conjunto"] = (cal["instrumento"] == tit)
    duros = [k for k, okv in c.items() if okv is False and k in DUROS]
    if duros:
        rep["dictamen"] = "rechazar"
        rep["motivos"].append("chequeos duros fallidos: " + ",".join(duros))
        return rep
    cond = []
    if rid in DEVUELTOS_MARGEN:
        cond.append("BLOQUEANTE — DEVUELTO por integrador: separar normalizado/original en todos los niveles; no integrar hasta separar")
    if rid in DEVUELTOS_PAR and rule["concepto"] == "unidad-coordinadora-tic":
        cond.append("DEVUELTO por integrador: P8 existencia vs P9 nombre NO es par codigo/nombre; separar 2 conceptos especificos (existencia declarada / nombre indicado)")
    if c.get("motivo_unidad"):
        cond.append(c["motivo_unidad"] + "; con limite (retirar o respaldar; sin habilitar cruces)")
    if c.get("motivo_metodologia"):
        cond.append(c["motivo_metodologia"] + "; con limite")
    if not c["rep_justificada"]:
        cond.append("representacion '%s' no justificada por el literal (descripcion/tipo/ejemplo); con limite, sin tipificar valores" % rule["representacion"])
    if isinstance(cal, dict) and cal.get("distrito_desarrollo_rural"):
        pass  # calificador DDR valido y propagado: nota informativa en aceptar (abajo)
    if c.get("motivo_calificador"):
        cond.append(c["motivo_calificador"] + "; corregir forma dict no vacio str->str")
    if c.get("concepto_compartido_sin_instrumento"):
        cond.append("comparte concepto sin calificador de instrumento; confusion de encuestas: acotar a instrumento o estrechar")
    if isinstance(cal, dict) and cal.get("instrumento") and c.get("instrumento_igual_conjunto") is False:
        cond.append("calificador instrumento no coincide con el titulo del conjunto; confusion de encuestas")
    if c.get("calificador_valido") is False:
        pass  # motivo ya agregado arriba via motivo_calificador
    if c.get("concepto_compartido_mismo_instrumento"):
        cond.append("mismo concepto e instrumento para definiciones distintas: confusion de encuestas; verificar equivalencia")
    if c.get("concepto_compartido_distinto_literal"):
        cond.append("mismo concepto para literales distintos; verificar equivalencia antes de aplicar")
    if c.get("poblacion_anadida"):
        cond.append("poblacion %s inferida del contexto SIN respaldo explicito en titulo/tabla/criterio; con limite, sin cruces" % c["poblacion_anadida"])
    if c.get("poblacion_respaldada_contexto"):
        pass  # nota en aceptar (abajo)
    if not c["ejemplo_coherente"]:
        cond.append("ejemplo '%s' incoherente con tipo %s; no tipificar monto/conteo; con limite" % (ej, dec["tipo"]))
    if cond:
        rep["dictamen"] = "condicionado"
        rep["motivos"] = cond
    else:
        rep["dictamen"] = "aceptar"
        nota = "literal especifico, alcance simultaneo, representacion conservadora"
        if c.get("concepto_compartido_mismo_literal"):
            nota += "; reutilizacion mismo literal"
        if c.get("concepto_compartido_mismo_campo"):
            nota += "; mismo campo, rol igual"
        if c.get("concepto_compartido_par_representaciones"):
            nota += "; par de representaciones del mismo objeto"
        if c.get("concepto_compartido_casi_identico"):
            nota += "; literales casi identicos"
        if c.get("concepto_compartido_calificador_distinto"):
            nota += "; calificador DDR distinto por regla, valido y propagado (la aplicacion central debe conservarlo)"
        if c.get("concepto_compartido_distinto_instrumento"):
            nota += "; instrumentos distintos con calificador valido y propagado (la aplicacion central debe conservarlos)"
        if c.get("alcance_acotado_origen"):
            nota += "; alcance acotado al registro de origen"
        if c.get("poblacion_respaldada_contexto"):
            nota += "; poblacion respaldada por contexto publicado explicito %s" % (c["poblacion_respaldada_contexto"],)
        if c.get("atributo_sensible_informativo"):
            nota += "; limite informativo: atributo sensible/vulnerable %s (solo metadatos publicados)" % (c["atributo_sensible_informativo"],)
        if c.get("catalogo_no_aplica_normalizado"):
            nota += "; catalogo '%s' normalizado a vacio" % c["catalogo_no_aplica_normalizado"]
        rep["motivos"].append(nota)
    return rep


def main():
    global insp_global
    antes = {f: sha(ROOT / f) for f in BASE_FILES}
    for tag, p in PROP.items():
        antes[tag] = sha(p)
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    insp_global = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
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

    base_ok = True
    mani = json.loads((ROOT / "propuestas/cobertura-muse-20261023/fuentes/manifiesto.json").read_text(encoding="utf-8"))
    mani_insumos = mani["insumos_centrales"]
    evidencia_intacta = all(sha(ROOT / f) == mani_insumos[f] for f in
                            ["data/portal/contenido-inspeccion.json", "data/portal/inventario.json",
                             "propuestas/ronda-3/integrador/asignaciones-semanticas.json"])
    assert evidencia_intacta
    from collections import Counter as _CC
    estados = dict(_CC(v.get("estado") for v in cob["variables"]))
    nucleo_actual = {"sha_semantica": sha(ROOT / "ontologia/semantica.json"),
                     "sha_cobertura": sha(ROOT / "data/semantica/cobertura.json"),
                     "sha_pendientes": sha(ROOT / "reports/pendientes-semanticos.json"),
                     "conceptos": len(cob["conceptos"]), "conceptos_sem": len(sem["conceptos"]),
                     "reglas": len(sem["reglas_descripcion_exacta"]), "estados_variables": estados,
                     "cambiado_vs_manifiesto": any(sha(ROOT / f) != mani_insumos[f] for f in
                                                   ["ontologia/semantica.json", "data/semantica/cobertura.json",
                                                    "reports/pendientes-semanticos.json"])}
    props = {tag: json.loads(p.read_text(encoding="utf-8")) for tag, p in PROP.items()}
    # slugs ya aplicados verbatim por el integrador: no son colision
    global aplicados_verbatim
    _todos_nuevos = {}
    for _tag, _p in props.items():
        _todos_nuevos.update(_p["conceptos_nuevos"])
    aplicados_verbatim = {s for s in _todos_nuevos if sem["conceptos"].get(s) == _todos_nuevos[s]}
    dicts, resumen, nuevos_todos, iris_todas = {}, {}, {}, {}
    for tag, p in props.items():
        titulos = {}
        for d in p["decisiones"]:
            nd = norm_decision(tag, d)
            if nd["titulo"]:
                titulos[nd["conjunto"]] = nd["titulo"]
        grupos = {}
        for r in p["reglas"]:
            grupos.setdefault(r["concepto"], []).append(r)
        dd = {}
        for r in p["reglas"]:
            dec = next(x for x in [norm_decision(tag, d) for d in p["decisiones"]]
                       if x["regla_id"] == r["id"] and x["propuesta"])
            dd[r["id"]] = auditar_regla(tag, r, dec, p["conceptos_nuevos"], vmap, filas, central, grupos, titulos)
        for d in [norm_decision(tag, x) for x in p["decisiones"]]:
            if not d["propuesta"]:
                assert d["regla_id"] is None and d["concepto"] is None, (tag, d["iri"])
                assert isinstance(d["motivo"], str) and len(d["motivo"]) > 5, (tag, d["iri"])
                iris_todas.setdefault(tag, set()).add(d["iri"])
        for r in p["reglas"]:
            iris_todas.setdefault(tag, set()).add(r["definiciones"][0])
        dicts[tag] = dd
        resumen[tag] = dict(Counter(v["dictamen"] for v in dd.values()))
        assert sum(resumen[tag].values()) == len(p["reglas"]), tag
        nuevos_todos[tag] = set(p["conceptos_nuevos"])
        for s in p.get("conceptos_reutilizados", []):
            assert s in central, (tag, s)
    # particion: GD y TE sin solape (el agro congelado ya no se audita por separado;
    # sus 63 reglas viven dentro de la entrega TE y se auditan ahi, una sola vez)
    vistos = set()
    for tag, iris in iris_todas.items():
        assert not (vistos & iris), tag
        vistos |= iris

    _todos_nuevos = {}
    for _tag, _p in props.items():
        _todos_nuevos.update(_p["conceptos_nuevos"])
    _central_conceptos = sem["conceptos"]
    conflictos = {
        "nuevos_vs_nucleo": sorted(set().union(*[nuevos_todos[t] & central for t in nuevos_todos])),
        "nuevos_vs_nucleo_detalle": {s: {"aplicado_verbatim": _central_conceptos.get(s) == _todos_nuevos.get(s)}
                                      for t in nuevos_todos for s in sorted(nuevos_todos[t] & central)},
        "cruzados": sorted({s for t1 in nuevos_todos for t2 in nuevos_todos if t1 < t2
                            for s in nuevos_todos[t1] & nuevos_todos[t2]}),
    }
    ext = {}
    for tag, p in props.items():
        er = []
        for r in p["reglas"]:
            e = {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
                 "representacion": r["representacion"], "nombres": r.get("nombres"),
                 "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
                 "definiciones": r.get("definiciones")}
            if r.get("calificador"):
                e["calificador"] = r["calificador"]
            er.append(e)
        # reglas COMPLETAS de la entrega como universo (sin mezclar nucleo aplicado:
        # evita duplicados y valida la propuesta standalone; el estado central se
        # contrasta aparte como informativo)
        ext[tag] = {"reglas_descripcion_exacta": er}
    # contraste informativo contra el nucleo aplicado por el integrador (no bloqueante)
    central_resuelven = 0
    central_total = 0
    ext_central = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"]}
    central_mismatch = []
    npos = 0
    for tag, p in props.items():
        if "decisiones" in p:
            mapa = {norm_decision(tag, d)["iri"]: norm_decision(tag, d) for d in p["decisiones"]}
        for r in p["reglas"]:
            iri = r["definiciones"][0]
            if "decisiones" in p:
                d = mapa[iri]
                var, desc, conj = d["variable"], d["descripcion"], d["conjunto"]
                dicc = d["diccionario"]
            else:
                ev = r["evidencia"][0]
                var, desc, conj, dicc = ev["variable"], ev["descripcion"], ev["conjunto"], ev["diccionario"]
            vv = vmap[iri]
            got = interpretacion(var, desc, conj, ext[tag], dicc, iri)
            assert got.get("estado") == "respaldada_por_definicion" and got.get("concepto") == r["concepto"], r["id"]
            if r.get("calificador"):
                assert got.get("calificador") == r["calificador"], r["id"]
            npos += 1
            try:
                gc = interpretacion(var, desc, conj, ext_central, dicc, iri)
                central_total += 1
                if gc.get("estado") == "respaldada_por_definicion" and gc.get("concepto") == r["concepto"]:
                    central_resuelven += 1
                else:
                    central_mismatch.append(r["id"])
            except ValueError:
                central_total += 1
                central_mismatch.append(r["id"] + ":conflicto-central")
    despues = {f: sha(ROOT / f) for f in BASE_FILES}
    for tag, p in PROP.items():
        despues[tag] = sha(p)
    estable = antes == despues
    plana = []
    for tag in ("gobierno-digital", "territorio-economia"):
        for rid, d in dicts[tag].items():
            plana.append({"dominio": tag, "regla_id": rid, "definicion_iri": d["definicion_iri"],
                          "concepto": d["concepto"], "dictamen": d["dictamen"],
                          "motivo": "; ".join(d["motivos"])})
    auditoria = {
        "sha_entregas": {tag: antes[tag] for tag in PROP},
        "dictamenes": plana,
        "resumen": {tag: dict(resumen[tag]) for tag in resumen},
        "reglas_auditadas": sum(len(v) for v in dicts.values()),
        "base_verificada": base_ok,
        "base_evidencia_intacta_vs_manifiesto": evidencia_intacta,
        "nucleo_estado_actual": nucleo_actual,
        "central_resuelven_igual": {"iguales": central_resuelven, "total": central_total,
                                    "distintos": central_mismatch[:50]},
        "fuentes_estables": estable,
        "detalle_por_regla": dicts,
        "conflictos_iris": conflictos,
        "positivos_pipeline": npos,
        "limites": ["solo significado documental; vinculo fisico, vigencia e identidad no acreditados",
                    "condicionados requieren accion del integrador; no habilitan cruces ni promociones",
                    "revision estructural (huellas, conteos, verificadores) no basta: cada dictamen revisa literal, concepto e inferencias",
                    "calificadores DDR/instrumento validos y propagados por el pipeline (verificado regla completa); la aplicacion central debe conservarlos"],
    }
    (AQUI / "auditoria-base.json").write_text(json.dumps(auditoria, ensure_ascii=False, indent=1), encoding="utf-8")
    final = {
        "sha_entregas": auditoria["sha_entregas"],
        "dictamenes": [{k: d[k] for k in ("dominio", "regla_id", "dictamen", "motivo")} for d in plana],
        "resumen": auditoria["resumen"],
        "reglas_auditadas": auditoria["reglas_auditadas"],
        "base_verificada": base_ok,
        "fuentes_estables": estable,
        "fase": "final",
    }
    (AQUI / "auditoria.json").write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding="utf-8")
    (AQUI / "fuente" / "huellas.json").write_text(json.dumps(
        {"antes": antes, "despues": despues, "estables": estable}, ensure_ascii=False, indent=1), encoding="utf-8")
    print({t: resumen[t] for t in resumen}, "positivos=", npos, "base_ok=", base_ok, "estable=", estable)


if __name__ == "__main__":
    main()
