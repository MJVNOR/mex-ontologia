"""Agente 2 ronda 3 - revision de las 118 candidatas + 3 ambiguas actuales.

Lee el estado central integrado (solo lectura) y escribe propuestas en ESTA
carpeta. No modifica ontologia/, data/, reports/, scripts/ ni otras propuestas.
No crea conceptos ni reglas. Solo conceptos/reglas vigentes.

Puertas de promocion (todas deben cumplirse):
  1. Variable respaldada_por_definicion con concepto y regla vigentes.
  2. Mismo conjunto columna/variable; diccionario unico del conjunto.
  3. Nombre: exacta/caja/acentos (enie preservada: ano/Ano != ano).
  4. Descripcion con aporte mas alla del nombre (puerta solo-nombre).
  5. Descripcion distintiva: cada calificador del concepto respaldado por
     fragmento literal, con equivalencias documentadas y acotadas
     (estado=entidad, captura=registro segun definicion del concepto,
     ser1=identificador segun definicion del concepto, previo via
     poblacion divorciados + preterito segun definicion del concepto).
  6. Vinculo fisico: variable unica en diccionario, columna unica en esquema,
     hoja registrada, representacion declarada, sin contradiccion de
     poblacion, huellas exactas recalculadas.
"""
import hashlib
import json
import tomllib
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
import sys

sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, columnas  # noqa: E402
from integrar_contenido import clave  # noqa: E402

AGUDOS = {"\u0300", "\u0301", "\u0302", "\u0308"}


def sin_agudos(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if c not in AGUDOS)


def relacion_nombre(campo, variable):
    if campo == variable:
        return "exacta", "nombres identicos"
    if (campo or "").lower() == (variable or "").lower():
        return "caja", "difieren solo en mayusculas/minusculas"
    if sin_agudos(campo).lower() == sin_agudos(variable).lower():
        return ("acentos",
                f"difieren solo en acento agudo & co: {campo!r} vs {variable!r}")
    return ("diferente",
            f"nombres distintos mas alla de caja/acentos: {campo!r} vs {variable!r}")


POBLACION_MARCAS = {
    "madre": ["madre", "materna"],
    "difunto": ["difunto", "difunta"],
    "beneficiario": ["benefic"],
    "alumno": ["alumno"],
    "titulado": ["titulad"],
    "victima": ["victima"],
}


def contradiccion_poblacion(concepto, dnorm):
    quals = set(concepto.split("-"))
    esperadas = {p for p in POBLACION_MARCAS if p in quals}
    if not esperadas:
        return None
    for pob, marcas in POBLACION_MARCAS.items():
        if pob in esperadas:
            continue
        if any(m in dnorm for m in marcas):
            return (f"la descripcion menciona {pob} pero el concepto exige "
                    f"{'/'.join(sorted(esperadas))}")
    return None


CALIFICADOR_EVIDENCIA = {
    "entidad": [("entidad", "literal"),
                ("estado", "estado=entidad federativa en diccionarios estatales")],
    "registro": [("registr", "flexion explicita registro/registra"),
                 ("captura", "captura=registro segun definicion del concepto entidad-registro («registra o captura»)")],
    "captura": [("captura", "literal")],
    "fecha": [("fecha", "literal")],
    "matrimonio": [("matrimonio", "literal")],
    "previo": [("divorci", "anterioridad: poblacion divorciados + preterito; el concepto define previo como matrimonio de divorciados, no fecha del divorcio")],
    "toma": [("toma", "literal")],
    "recepcion": [("recepc", "flexion recepcion")],
    "resultado": [("resultado", "literal")],
    "suero": [("suero", "literal"),
              ("suer", "errata documentada «suer»=suero en la definicion del concepto fecha-resultado-suero-rickettsia-ser1")],
    "sangre": [("sangre", "literal")],
    "rickettsia": [("rickett", "enfermedad rickettsiosis/rickett explicita")],
    "rickett": [("rickett", "literal")],
    "programa": [("programa", "literal")],
    "educativo": [("educativ", "literal/flexion"),
                  ("estudi", "programa de estudios: objeto educativo explicito; descripcion aceptada por la regla vigente programa-nombre")],
    "anio": [("ano", "ano/anio"), ("anio", "literal")],
    "sexo": [("sexo", "literal")],
    "declarado": [("declara", "flexion declarada/o")],
}


def verifica_calificadores(concepto, dnorm, nombre_variable=""):
    evidencias, faltantes = [], []
    for cal in concepto.split("-"):
        if cal == "ser1":
            # «ser1» es identificador de la variable segun la propia definicion
            # del concepto; se acepta solo si figura en el nombre fisico.
            if "ser1" in (nombre_variable or "").lower():
                evidencias.append({"calificador": "ser1", "fragmento": "ser1",
                                   "justificacion": "identificador en el nombre de la variable; la definicion del concepto lo conserva como identificador sin deducir prueba"})
            else:
                faltantes.append("ser1")
            continue
        variantes = CALIFICADOR_EVIDENCIA.get(cal, [(cal, "literal")])
        hallada = next(((cal, s, j) for s, j in variantes if s in dnorm), None)
        if hallada:
            evidencias.append({"calificador": hallada[0], "fragmento": hallada[1],
                               "justificacion": hallada[2]})
        else:
            faltantes.append(cal)
    return evidencias, faltantes


def hoja_de(iri_columna):
    try:
        if "/file-column/" in iri_columna:
            tail = unquote(iri_columna.split("/file-column/")[1])
            segs = tail.split("/")
            if len(segs) >= 3:
                return segs[1]
    except Exception:
        pass
    return ""


def sha256_archivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def main():
    entradas = {
        "semantica": ROOT / "ontologia/semantica.json",
        "cobertura": ROOT / "data/semantica/cobertura.json",
        "pendientes": ROOT / "reports/pendientes-semanticos.json",
        "inventario": ROOT / "data/portal/inventario.json",
        "inspeccion": ROOT / "data/portal/contenido-inspeccion.json",
        "config": ROOT / "config.toml",
    }
    huellas_entrada = {k: sha256_archivo(p) for k, p in entradas.items()}
    sem = json.loads(entradas["semantica"].read_text(encoding="utf-8"))
    cob = json.loads(entradas["cobertura"].read_text(encoding="utf-8"))
    pend = json.loads(entradas["pendientes"].read_text(encoding="utf-8"))
    inv = json.loads(entradas["inventario"].read_text(encoding="utf-8"))
    ins = json.loads(entradas["inspeccion"].read_text(encoding="utf-8"))
    base = tomllib.loads(entradas["config"].read_text(encoding="utf-8"))["catalogo"]["base_iri"]

    # Verificacion de base actual (no conteos historicos).
    assert len(sem["conceptos"]) == 103, len(sem["conceptos"])
    assert len(sem["vinculos_documentales_revisados"]) == 836
    assert sum(1 for v in cob["variables"] if v.get("estado") == "respaldada_por_definicion") == 232
    candidatas = [c for c in pend["columnas"] if c["estado"] == "candidata_por_nombre"]
    revisadas = [c for c in pend["columnas"] if c["estado"] == "documental_revisada"]
    ambiguas = [c for c in pend["columnas"] if c["estado"] == "ambigua_por_nombre"]
    assert len(candidatas) == 118, len(candidatas)
    assert len(revisadas) == 836, len(revisadas)
    assert len(ambiguas) == 3, len(ambiguas)
    assert sum(len(c["correspondencias"]) for c in ambiguas) == 6
    assert all(len(c["correspondencias"]) == 1 for c in candidatas)

    reglas = {r["id"]: r for r in sem["reglas_descripcion_exacta"]}
    conceptos = sem["conceptos"]
    var_by_iri = {v["iri"]: v for v in cob["variables"] if v.get("iri")}
    corr_by_iri = {c["iri"]: c for c in cob["correspondencias"]}
    cols_calc = {c["iri"]: c for c in columnas(inv, ins, base)}
    rec_by_id = {r["id"]: r for r in inv["recursos"]}
    insp_by_id = {r["id"]: r for r in ins["recursos"]}
    conj_nombres = {}
    for r in inv["recursos"]:
        conj_nombres.setdefault(r["conjunto_id"], r.get("conjunto"))
    var_veces = Counter((v["diccionario"], v["variable"]) for v in cob["variables"] if v.get("iri"))
    ndict_conj = Counter(r["conjunto_id"] for r in inv["recursos"] if r["clasificacion"] == "diccionario")
    ndata_conj = Counter(r["conjunto_id"] for r in inv["recursos"] if r["clasificacion"] == "datos_estructurados")

    propuestas, pendientes, motivos = [], [], Counter()
    preseleccion = []

    for col in sorted(candidatas, key=lambda c: c["columna"]):
        ci = col["correspondencias"][0]
        corr = corr_by_iri.get(ci, {})
        var = var_by_iri.get(corr.get("variable"), {})
        info = {"columna": col["columna"], "campo": col["campo"],
                "recurso": col["recurso"], "conjunto": col["conjunto"],
                "titulo_recurso": col.get("titulo_recurso"),
                "correspondencia_iri": ci,
                "variable": corr.get("variable")}
        estado_var = var.get("estado")
        if not var or estado_var != "respaldada_por_definicion":
            motivos[f"variable_sin_respaldo:{estado_var or 'sin_variable'}"] += 1
            pendientes.append({**info, "motivo": f"variable_sin_respaldo:{estado_var or 'sin_variable'}",
                               "etapa": "preseleccion",
                               "detalle": (corr.get("evidencia_textual") or "")[:200]})
            continue
        if var.get("regla") not in reglas or var.get("concepto") not in conceptos:
            motivos["regla_o_concepto_no_vigente"] += 1
            pendientes.append({**info, "motivo": "regla_o_concepto_no_vigente",
                               "etapa": "preseleccion", "detalle": str(var.get("regla"))})
            continue
        if var.get("conjunto") != col["conjunto"]:
            motivos["conjunto_no_coincide"] += 1
            pendientes.append({**info, "motivo": "conjunto_no_coincide", "etapa": "preseleccion",
                               "detalle": f"col={col['conjunto']} var={var.get('conjunto')}"})
            continue
        tipo, detalle_nombre = relacion_nombre(col["campo"], var.get("variable"))
        if tipo == "diferente":
            motivos["nombre_difiere:requiere alias tecnico, fuera de alcance"] += 1
            pendientes.append({**info, "variable_iri": var.get("iri"),
                               "concepto": var.get("concepto"), "regla": var.get("regla"),
                               "motivo": "nombre_difiere:requiere alias tecnico, fuera de alcance",
                               "etapa": "vinculo", "detalle": detalle_nombre})
            continue
        descripcion = (var.get("descripcion") or "").strip()
        dnorm = clave(descripcion)
        if not dnorm or "pendiente de especificar" in dnorm:
            motivos["descripcion_pendiente_o_vacia"] += 1
            pendientes.append({**info, "motivo": "descripcion_pendiente_o_vacia",
                               "etapa": "preseleccion", "detalle": descripcion[:200]})
            continue
        if dnorm == clave(var.get("variable") or ""):
            motivos["descripcion_solo_reconfirma_nombre"] += 1
            pendientes.append({**info, "variable_iri": var.get("iri"),
                               "concepto": var.get("concepto"), "regla": var.get("regla"),
                               "motivo": "descripcion_solo_reconfirma_nombre",
                               "etapa": "preseleccion", "detalle": descripcion[:200]})
            continue
        evidencias, faltantes = verifica_calificadores(var["concepto"], dnorm, var.get("variable"))
        if faltantes:
            motivos[f"calificador_sin_respaldo:{'+'.join(faltantes)}"] += 1
            pendientes.append({**info, "variable_iri": var.get("iri"),
                               "concepto": var.get("concepto"), "regla": var.get("regla"),
                               "motivo": f"calificador_sin_respaldo:{'+'.join(faltantes)}",
                               "etapa": "preseleccion", "detalle": descripcion[:200]})
            continue
        preseleccion.append({"base": info, "var": var, "descripcion": descripcion,
                             "dnorm": dnorm, "evidencias": evidencias,
                             "relacion": (tipo, detalle_nombre),
                             "calc": cols_calc.get(col["columna"], {})})

    grupos, normalizaciones = [], []
    motivos_vinculo = Counter()
    miembros_por_grupo = defaultdict(list)
    for pre in preseleccion:
        info, var = pre["base"], pre["var"]
        miembros_por_grupo[(info["conjunto"], var["diccionario"], info["recurso"])].append(pre)

    for gid, ((cj, dic, rec), miembros) in enumerate(sorted(miembros_por_grupo.items()), 1):
        rec_inv = rec_by_id.get(rec, {})
        dic_inv = rec_by_id.get(dic, {})
        hojas = sorted({hoja_de(m["base"]["columna"]) for m in miembros if hoja_de(m["base"]["columna"])})
        ficha = {
            "id": f"G-{gid:03d}",
            "conjunto": {"id": cj, "titulo": conj_nombres.get(cj)},
            "diccionario": {"id": dic, "nombre": dic_inv.get("nombre"), "url": dic_inv.get("url")},
            "recurso": {"id": rec, "titulo": rec_inv.get("nombre"),
                        "url": rec_inv.get("url") or miembros[0]["calc"].get("fuente")},
            "hojas": hojas,
            "alcance": {
                "recursos_datos_en_conjunto": ndata_conj.get(cj),
                "diccionarios_en_conjunto": ndict_conj.get(cj),
                "nota": ("Diccionario unico del conjunto segun inventario "
                         f"({ndata_conj.get(cj)} recursos de datos, "
                         f"{ndict_conj.get(cj)} diccionario); documenta las variables "
                         "del conjunto, incluido este recurso.") if ndict_conj.get(cj) == 1 else
                        "Alcance no asignado: el conjunto tiene mas de un diccionario.",
            },
        }
        items = []
        for pre in miembros:
            info, var = pre["base"], pre["var"]
            calc = pre["calc"]
            var_unica = var_veces.get((var["diccionario"], var["variable"]), 0) == 1
            col_unica = bool(calc.get("nombre_unico", False))
            m_motivos = []
            if var.get("conjunto") != info["conjunto"]:
                m_motivos.append("fuera_de_alcance:conjunto no coincide")
            if ndict_conj.get(info["conjunto"]) != 1:
                m_motivos.append("alcance_no_asignado:el conjunto tiene mas de un diccionario")
            nombre_rec = (rec_inv.get("nombre") or "")
            hoja_item = hoja_de(info["columna"])
            if "catalogo" in sin_agudos(nombre_rec).lower() or hoja_item.lower().startswith("cat_"):
                m_motivos.append("catalogo_no_observacion:el recurso/hoja es catalogo, no tabla de "
                                 "observaciones; el papel documentado (p. ej. estado de captura) no se "
                                 "transfiere a una entrada de catalogo sin evidencia publicada explicita "
                                 "de aplicacion del campo a esa hoja y papel")
            if not var_unica:
                m_motivos.append("variable_ambigua:nombre repetido en el diccionario")
            if not col_unica:
                m_motivos.append("columna_ambigua:nombre repetido en el esquema")
            contra = contradiccion_poblacion(var["concepto"], pre["dnorm"])
            if contra:
                m_motivos.append("contradiccion_poblacion:" + contra)
            tipo, detalle_nombre = pre["relacion"]
            if tipo == "acentos":
                normalizaciones.append({"columna": info["columna"], "campo": info["campo"],
                                        "variable": var["variable"], "recurso": info["recurso"],
                                        "detalle": detalle_nombre,
                                        "alcance": "normalizacion ortografica acotada a este recurso"})
            item = {"columna": info["columna"], "campo": info["campo"],
                    "variable": var["variable"], "variable_iri": var.get("iri"),
                    "definicion_iri": var.get("definicion_iri"),
                    "huellas": {"huella_esquema": calc.get("huella_esquema"),
                                "huella_fila_diccionario": var.get("huella_fila_diccionario")},
                    "unicidad": {"variable_unica_en_diccionario": var_unica,
                                 "columna_unica_en_esquema": col_unica},
                    "relacion_nombre": tipo, "detalle_nombre": detalle_nombre,
                    "representacion": var.get("representacion"),
                    "contexto_solo_contexto": f"{ficha['conjunto']['titulo']} / {ficha['recurso']['titulo']} / {'+'.join(hojas) if hojas else 'datastore'}",
                    "dictamen": "promovida" if not m_motivos else "pendiente",
                    "motivos_vinculo": m_motivos}
            items.append(item)
            if m_motivos:
                for m in m_motivos:
                    motivos_vinculo[m.split(":")[0]] += 1
                pendientes.append({**info, "variable_iri": var.get("iri"),
                                   "concepto": var.get("concepto"), "regla": var.get("regla"),
                                   "motivo": ";".join(m_motivos), "etapa": "vinculo",
                                   "detalle": pre["descripcion"][:200]})
        ficha["miembros"] = items
        ficha["promovidos"] = sum(1 for i in items if i["dictamen"] == "promovida")
        ficha["pendientes"] = sum(1 for i in items if i["dictamen"] != "promovida")
        grupos.append(ficha)
        for it, pre in zip(items, miembros):
            if it["dictamen"] != "promovida":
                continue
            info, var = pre["base"], pre["var"]
            calc = pre["calc"]
            hoja = hoja_de(info["columna"])
            propuestas.append({
                "columna": info["columna"], "campo": info["campo"],
                "recurso": info["recurso"], "conjunto": info["conjunto"],
                "titulo_recurso": info["titulo_recurso"],
                "fuente_esquema": calc.get("fuente"),
                "correspondencia_iri": info["correspondencia_iri"],
                "variable": var["variable"], "variable_iri": var.get("iri"),
                "definicion_iri": var.get("definicion_iri"),
                "definicion": pre["descripcion"], "concepto": var.get("concepto"),
                "descripcion": pre["descripcion"],
                "regla": var.get("regla"), "representacion": var.get("representacion"),
                "diccionario": var.get("diccionario"),
                "catalogo_declarado": var.get("catalogo_declarado"),
                "grupo_vinculo": ficha["id"],
                "huellas": {"huella_esquema": calc.get("huella_esquema"),
                            "huella_fila_diccionario": var.get("huella_fila_diccionario")},
                "evidencia_significado": {"descripcion_original": pre["descripcion"],
                                          "verificacion_por_calificador": pre["evidencias"]},
                "evidencia_vinculo": {
                    "diccionario": ficha["diccionario"], "recurso": ficha["recurso"],
                    "hoja": hoja if hoja else "datastore",
                    "variable_unica_en_diccionario": it["unicidad"]["variable_unica_en_diccionario"],
                    "columna_unica_en_esquema": it["unicidad"]["columna_unica_en_esquema"],
                    "relacion_nombre": it["relacion_nombre"], "detalle_nombre": it["detalle_nombre"],
                    "representacion_declarada": var.get("representacion"),
                    "alcance": ficha["alcance"]["nota"],
                    "contexto_solo_contexto": it["contexto_solo_contexto"]},
                "criterio": ("Vinculo columna fisica -> variable documentada del mismo conjunto: "
                             "nombre con relacion registrada, descripcion que respalda cada calificador, "
                             "diccionario y recurso localizados en el conjunto, unicidad en diccionario y "
                             "esquema, sin alias. Alcance documental."),
                "alias_limitado": None,
                "limitaciones": ("Solo esta columna (ver ficha de grupo); no se generaliza a otros "
                                 "recursos/anios; no valida valores, unidades, codificaciones ni "
                                 "pertenencia a catalogos.")})

    ambiguos_out = []
    for col in sorted(ambiguas, key=lambda c: c["columna"]):
        vinculos = []
        for ci in col["correspondencias"]:
            corr = corr_by_iri.get(ci, {})
            var = var_by_iri.get(corr.get("variable"), {})
            vinculos.append({"correspondencia_iri": ci,
                             "variable": corr.get("variable"),
                             "variable_nombre": var.get("variable"),
                             "definicion_iri": var.get("definicion_iri"),
                             "descripcion": var.get("descripcion"),
                             "estado_variable": var.get("estado"),
                             "huella_fila_diccionario": var.get("huella_fila_diccionario")})
        calc = cols_calc.get(col["columna"], {})
        ambiguos_out.append({
            "columna": col["columna"], "campo": col["campo"], "recurso": col["recurso"],
            "conjunto": col["conjunto"], "titulo_recurso": col.get("titulo_recurso"),
            "fuente_esquema": calc.get("fuente") or col.get("fuente_esquema"),
            "huella_esquema": calc.get("huella_esquema"),
            "definiciones_por_nombre": col["definiciones_por_nombre"],
            "vinculos": vinculos,
            "dictamen": ("No promovible en esta ronda: filas de diccionario degeneradas "
                         "(descripciones «ide_col») y variables fuera del nucleo; "
                         "se conservan ambas alternativas."),
            "pregunta_publicador": ("¿Que significa la columna ide_id en este recurso y cual "
                                    "de las filas 1/177/178 del diccionario la documenta? "
                                    "Sin respuesta no se asigna vinculo."),
            "limitaciones": "Requiere diccionario inteligible o aclaracion del publicador."})

    salida = {
        "generado_en_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": ("Revision de las 118 correspondencias candidata_por_nombre actuales y "
                    "las 3 columnas ambiguas (6 vinculos). Se conservan las 836 revisadas "
                    "exactas. Solo conceptos y reglas vigentes; sin conceptos nuevos, sin alias. "
                    "El diccionario unico del conjunto es condicion necesaria pero no suficiente: "
                    "cada propuesta exige ademas columna unica en el esquema de ese recurso/hoja, "
                    "nombre exacto y descripcion distintiva; las hojas de catalogo no heredan el "
                    "papel de las tablas de observaciones."),
        "nota_formato": ("Traduccion explicita al formato integrador: la clave 'descripcion' trae la "
                         "descripcion literal original del diccionario; la clave 'definicion' repite el "
                         "mismo literal y se conserva por compatibilidad con ronda 2."),
        "conteos": {"candidatas_examinadas": 118, "propuestas_finales": len(propuestas),
                    "pendientes_clasificados": len(pendientes),
                    "conservadas_existentes": 836, "columnas_ambiguas": 3,
                    "vinculos_ambiguos": 6, "grupos_vinculo": len(grupos),
                    "normalizaciones_ortograficas": len(normalizaciones),
                    "motivos_preseleccion": dict(motivos),
                    "motivos_vinculo": dict(motivos_vinculo)},
        "huellas_entrada": huellas_entrada,
        "conservadas_existentes_iris": sorted(c["correspondencias"][0] for c in revisadas),
        "normalizaciones_ortograficas": normalizaciones,
        "grupos_vinculo": grupos,
        "propuestas_revisadas": sorted(propuestas, key=lambda p: p["columna"]),
        "pendientes_clasificados": sorted(pendientes, key=lambda p: p["columna"]),
        "ambiguos": ambiguos_out,
    }
    assert len(propuestas) + len(pendientes) == 118, (len(propuestas), len(pendientes))
    (OUT / "propuestas.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    print(json.dumps(salida["conteos"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
