"""Agente 1 (ronda 2) — revision de correspondencias candidatas por nombre.

Lee el estado central integrado (solo lectura) y escribe propuestas en esta
carpeta. No modifica ontologia/, data/, reports/ ni otras propuestas.
No crea conceptos ni depende de propuestas de otros agentes.

Dos niveles separados:
  1. Preseleccion lexica: la descripcion del diccionario (mismo conjunto)
     respalda explicitamente cada calificador del concepto.
  2. Evaluacion del VINCULO por grupo documental (conjunto, diccionario,
     recurso): referencia exacta de diccionario y recurso, unicidad de nombre
     de variable y de columna, alcance conocido, representacion declarada,
     relacion exacta de nombres y contradicciones. Solo lo que supera ambos
     niveles se promueve.
"""
import json
import sys
import tomllib
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from consolidar_semantica import huella, columnas  # noqa: E402
from integrar_contenido import clave  # noqa: E402


def norm(s):
    return " ".join("".join(
        c for c in unicodedata.normalize("NFD", str(s or "").lower())
        if unicodedata.category(c) != "Mn").split())


# Marcas combinantes de acento agudo/grave/circunflejo/dieresis.
# La tilde de la enie (U+0303) se conserva: enie->ene NO es mero acento.
AGUDOS = {"\u0300", "\u0301", "\u0302", "\u0308"}


def sin_agudos(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                   if c not in AGUDOS)


def relacion_nombre(campo, variable):
    """Tipo de relacion entre nombre de columna y de variable.

    exacta: identicos. caja: solo mayusculas. acentos: solo diacriticos de
    acento agudo & co (se registra como normalizacion ortografica acotada al
    recurso, con evidencia). diferente: cualquier otro caso (incluye enie->ene).
    """
    if campo == variable:
        return "exacta", "nombres identicos"
    if (campo or "").lower() == (variable or "").lower():
        return "caja", "difieren solo en mayusculas/minusculas"
    if sin_agudos(campo).lower() == sin_agudos(variable).lower():
        return ("acentos",
                f"difieren solo en acento agudo & co: {campo!r} vs {variable!r}; "
                "normalizacion ortografica acotada a este recurso")
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
    """Poblacion especifica del concepto vs otra poblacion en la descripcion."""
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


def dictamen_vinculo(campo, variable, concepto, dnorm, var_conjunto,
                     col_conjunto, dic_en_conjunto, rec_en_conjunto,
                     var_unica, col_unica, ndict_conjunto):
    """Evaluacion del vinculo columna->definicion. Devuelve (dictamen, motivos, notas)."""
    motivos, notas = [], {}
    if var_conjunto != col_conjunto or not dic_en_conjunto or not rec_en_conjunto:
        motivos.append("fuera_de_alcance:variable/diccionario/recurso no documentan el mismo conjunto")
        return "pendiente", motivos, notas
    if ndict_conjunto != 1:
        motivos.append("alcance_no_asignado:el conjunto tiene mas de un diccionario")
        return "pendiente", motivos, notas
    if not var_unica:
        motivos.append("variable_ambigua:nombre repetido en el diccionario")
    if not col_unica:
        motivos.append("columna_ambigua:nombre repetido en el esquema")
    tipo, detalle = relacion_nombre(campo, variable)
    notas["relacion_nombre"] = tipo
    notas["detalle_nombre"] = detalle
    if tipo == "diferente":
        motivos.append("nombre_difiere:requiere alias tecnico, fuera de alcance")
    contra = contradiccion_poblacion(concepto, dnorm)
    if contra:
        motivos.append("contradiccion_poblacion:" + contra)
    notas["diferencia_campo_definicion"] = None
    if "hechos" in norm(campo) and "reporte" in concepto:
        notas["diferencia_campo_definicion"] = (
            "el campo sugiere ocurrencia (hechos) pero la definicion dice reporte; "
            "vale la definicion, el nombre no determina el significado")
    if motivos:
        return "pendiente", motivos, notas
    return "promovida", [], notas


CALIFICADOR_EVIDENCIA = {
    "municipio": [("municipio", "literal"), ("municipal", "adjetivo explicito")],
    "nacimiento": [("nacim", "flexion explicita nacimiento/nacio"),
                   ("naciem", "errata documentada naciemiento=nacimiento"),
                   ("natal", "equivalencia explicita natalidad")],
    "madre": [("madre", "literal"), ("materna", "explicito")],
    "registro": [("registr", "flexion explicita registro/registra/registraron"),
                 ("inscripc", "equivalencia explicita inscripcion")],
    "residencia": [("resid", "flexion explicita residencia/reside"),
                   ("recid", "errata documentada recide/recidia=reside")],
    "defuncion": [("defunc", "literal/flexion defuncion"),
                  ("fallec", "evento de fallecimiento explicito"),
                  ("difunto", "poblacion/evento del difunto explicito"),
                  ("muerte", "explicito"), ("mortal", "explicito mortalidad")],
    "fallecimiento": [("fallec", "evento de fallecimiento explicito (fallecer/fallecio)"),
                      ("defunc", "literal/flexion defuncion"),
                      ("difunto", "poblacion/evento del difunto explicito")],
    "inscripcion": [("inscrib", "flexion explicita inscripcion/inscribio")],
    "reinscripcion": [("reinscrib", "flexion explicita reinscripcion")],
    "rickettsia": [("rickett", "enfermedad rickettsiosis/rickett explicita")],
    "parto": [("parto", "literal")],
    "internado": [("internad", "flexion explicita internada/o")],
    "externado": [("externad", "flexion explicita externada/o")],
    "entidad": [("entidad", "literal"),
                ("estado", "estado=entidad federativa en diccionarios estatales")],
    "ubicacion": [("ubica", "relacion de ubicacion explicita"),
                  ("encuentra", "relacion de ubicacion explicita (se encuentra)"),
                  ("localiza", "explicito"), ("situa", "explicito")],
    "origen": [("origen", "literal"),
               ("donde", "relacion de origen explicita (de donde se realizo)")],
    "llamada": [("llamada", "literal")],
    "anio": [("ano", "ano/anio normalizados"), ("anio", "literal")],
    "mes": [("mes", "literal/flexion meses")],
    "fecha": [("fecha", "literal")],
    "dia": [("dia", "literal")],
    "hora": [("hora", "literal")],
    "subasta": [("subasta", "literal")],
    "censo": [("censo", "literal"), ("censad", "flexion censados")],
    "captura": [("captura", "literal"), ("captur", "flexion")],
    "agricola": [("agricola", "literal"), ("cultivo", "objeto agricola explicito"),
                 ("siembra", "explicito"), ("cosecha", "explicito")],
    "reporte": [("report", "flexion explicita reporte/reporta")],
    "hidrica": [("hidric", "flexion explicita hidrico/a/os")],
    "ciclo": [("ciclo", "literal")],
    "atencion": [("atenc", "flexion explicita atencion/atenciones")],
    "apoyo": [("apoyo", "literal/flexion apoyos")],
    "escuela": [("escuela", "literal")],
    "denuncia": [("denuncia", "literal")],
    "detencion": [("detenc", "flexion explicita"), ("deten", "flexion")],
    "comite": [("comite", "literal")],
    "delito": [("delito", "literal/flexion delitos")],
    "donacion": [("donac", "flexion explicita donacion/donaciones")],
    "inspeccion": [("inspecc", "flexion explicita")],
    "programa": [("programa", "literal")],
    "educativo": [("educativ", "literal/flexion"), ("educacion", "literal")],
    "hospitalaria": [("hospital", "explicito hospitalaria/hospital")],
    "unidad": [("unidad", "literal")],
    "total": [("total", "literal")],
    "masculino": [("masculino", "literal")],
    "femenino": [("femenino", "literal")],
    "sexo": [("sexo", "literal")],
    "difunto": [("difunto", "literal")],
    "poblacion": [("poblac", "flexion poblacion")],
    "victima": [("victima", "literal")],
    "titulado": [("titulad", "flexion titulada/o")],
    "titulacion": [("titulac", "flexion"), ("titulo", "objeto titulo explicito")],
    "alumno": [("alumno", "literal")],
    "baja": [("baja", "literal")],
    "sangre": [("sangre", "literal")],
    "suero": [("suero", "literal")],
    "toma": [("toma", "literal")],
    "recepcion": [("recepc", "flexion recepcion")],
    "resultado": [("resultado", "literal")],
    "rickett": [("rickett", "literal")],
    "pcr": [("pcr", "literal")],
    "real": [("real", "literal (PCR tiempo real)")],
    "tiempo": [("tiempo", "literal")],
    "matrimonio": [("matrimonio", "literal")],
    "localidad": [("localidad", "literal")],
    "beneficiario": [("benefic", "flexion beneficiario/beneficiado")],
    "pertenencia": [("pertenec", "flexion pertenece/pertenencia")],
    "entrega": [("entreg", "flexion entrega/entregaron")],
    "consultas": [("consult", "flexion consulta/consultas")],
    "conteo": [("conteo", "literal"), ("total", "cuantificacion total explicita")],
    "declarado": [("declara", "flexion declarada/o")],
}


def verifica_calificadores(concepto, dnorm):
    partes = concepto.split("-")
    evidencias, faltantes = [], []
    for cal in partes:
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


def main():
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
    inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
    ins = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    base = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]

    reglas = {r["id"]: r for r in sem["reglas_descripcion_exacta"]}
    conceptos = set(sem["conceptos"].keys())
    var_by_iri = {v["iri"]: v for v in cob["variables"] if v.get("iri")}
    corr_by_iri = {c["iri"]: c for c in cob["correspondencias"]}
    cols_calc = {c["iri"]: c for c in columnas(inv, ins, base)}
    rec_by_id = {r["id"]: r for r in inv["recursos"]}
    conj_nombres = {}
    for r in inv["recursos"]:
        conj_nombres.setdefault(r["conjunto_id"], r.get("conjunto"))

    # Unicidad de nombre de variable dentro de cada diccionario.
    var_veces = Counter((v["diccionario"], v["variable"]) for v in cob["variables"] if v.get("iri"))
    # Diccionarios por conjunto en inventario.
    ndict_conj = Counter(r["conjunto_id"] for r in inv["recursos"] if r["clasificacion"] == "diccionario")
    ndata_conj = Counter(r["conjunto_id"] for r in inv["recursos"] if r["clasificacion"] == "datos_estructurados")

    candidatas = [c for c in pend["columnas"] if c["estado"] == "candidata_por_nombre"]
    revisadas = [c for c in pend["columnas"] if c["estado"] == "documental_revisada"]
    ambiguas = [c for c in pend["columnas"] if "ambigua" in c["estado"]]

    preseleccion, pendientes = [], []
    motivos = Counter()

    for col in candidatas:
        ci = col["correspondencias"][0]
        corr = corr_by_iri.get(ci, {})
        var = var_by_iri.get(corr.get("variable"), {})
        info = {"columna": col["columna"], "campo": col["campo"],
                "recurso": col["recurso"], "conjunto": col["conjunto"],
                "titulo_recurso": col.get("titulo_recurso"),
                "fuente_esquema": col.get("fuente_esquema"),
                "correspondencia_iri": ci,
                "variable": corr.get("variable")}
        estado_var = var.get("estado")
        if not var or estado_var != "respaldada_por_definicion":
            motivos[f"variable_sin_respaldo:{estado_var or 'sin_variable'}"] += 1
            pendientes.append({**info, "motivo": f"variable_sin_respaldo:{estado_var or 'sin_variable'}",
                               "etapa": "preseleccion",
                               "detalle": (corr.get("evidencia_textual") or "")[:160]})
            continue
        if var.get("regla") not in reglas or var.get("concepto") not in conceptos:
            motivos["regla_o_concepto_no_vigente"] += 1
            pendientes.append({**info, "motivo": "regla_o_concepto_no_vigente",
                               "etapa": "preseleccion", "detalle": str(var.get("regla"))})
            continue
        if var.get("conjunto") != col["conjunto"]:
            motivos["conjunto_no_coincide"] += 1
            pendientes.append({**info, "motivo": "conjunto_no_coincide",
                               "etapa": "preseleccion",
                               "detalle": f"col={col['conjunto']} var={var.get('conjunto')}"})
            continue
        descripcion = (var.get("descripcion") or "").strip()
        dnorm = clave(descripcion)
        if not dnorm or "pendiente de especificar" in dnorm:
            motivos["descripcion_pendiente_o_vacia"] += 1
            pendientes.append({**info, "motivo": "descripcion_pendiente_o_vacia",
                               "etapa": "preseleccion", "detalle": descripcion[:160]})
            continue
        if dnorm == clave(var.get("variable") or ""):
            motivos["descripcion_sin_aporte_solo_reconfirma_nombre"] += 1
            pendientes.append({**info, "motivo": "descripcion_sin_aporte_solo_reconfirma_nombre",
                               "etapa": "preseleccion", "detalle": descripcion[:160]})
            continue
        evidencias, faltantes = verifica_calificadores(var["concepto"], dnorm)
        if faltantes:
            motivos[f"calificador_sin_respaldo:{'+'.join(faltantes)}"] += 1
            pendientes.append({**info, "variable_iri": var.get("iri"),
                               "concepto": var.get("concepto"), "regla": var.get("regla"),
                               "motivo": f"calificador_sin_respaldo:{'+'.join(faltantes)}",
                               "etapa": "preseleccion", "detalle": descripcion[:200]})
            continue
        calc = cols_calc.get(col["columna"], {})
        preseleccion.append({"base": info, "var": var, "descripcion": descripcion,
                             "dnorm": dnorm, "evidencias": evidencias, "calc": calc})

    # Evaluacion del vinculo por grupo documental (conjunto, diccionario, recurso).
    grupos, propuestas, normalizaciones = [], [], []
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
            "diccionario": {"id": dic, "nombre": dic_inv.get("nombre"),
                            "url": dic_inv.get("url")},
            "recurso": {"id": rec, "titulo": rec_inv.get("nombre"),
                        "url": rec_inv.get("url") or miembros[0]["base"].get("fuente_esquema")},
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
            dictamen, motivos_m, notas = dictamen_vinculo(
                info["campo"], var["variable"], var["concepto"], pre["dnorm"],
                var["conjunto"], info["conjunto"],
                bool(dic_inv) and dic_inv.get("conjunto_id") == info["conjunto"],
                bool(rec_inv) and rec_inv.get("conjunto_id") == info["conjunto"],
                var_unica, col_unica, ndict_conj.get(cj))
            contexto = " / ".join(t for t in [var.get("titulo_conjunto"),
                                              info.get("titulo_recurso"),
                                              hoja_de(info["columna"])] if t)
            rep = var.get("representacion")
            item = {
                "columna": info["columna"], "campo": info["campo"],
                "variable": var["variable"], "variable_iri": var["iri"],
                "definicion_iri": var["definicion_iri"],
                "huellas": {"huella_esquema": calc.get("huella_esquema"),
                            "huella_fila_diccionario": var["huella_fila_diccionario"]},
                "unicidad": {"variable_unica_en_diccionario": var_unica,
                             "columna_unica_en_esquema": col_unica},
                "relacion_nombre": notas["relacion_nombre"],
                "detalle_nombre": notas["detalle_nombre"],
                "representacion": rep,
                "diferencia_campo_definicion": notas["diferencia_campo_definicion"],
                "contexto_solo_contexto": contexto,
                "dictamen": dictamen,
                "motivos_vinculo": motivos_m,
            }
            if dictamen == "promovida":
                if notas["relacion_nombre"] == "acentos":
                    normalizaciones.append({
                        "columna": info["columna"], "campo": info["campo"],
                        "variable": var["variable"], "recurso": info["recurso"],
                        "conjunto": info["conjunto"],
                        "tipo": "acentos",
                        "evidencia": notas["detalle_nombre"]})
                propuestas.append({
                    "columna": info["columna"], "campo": info["campo"],
                    "recurso": info["recurso"], "conjunto": info["conjunto"],
                    "titulo_recurso": info.get("titulo_recurso"),
                    "fuente_esquema": info.get("fuente_esquema"),
                    "correspondencia_iri": info["correspondencia_iri"],
                    "variable": var["variable"], "variable_iri": var["iri"],
                    "definicion_iri": var["definicion_iri"],
                    "definicion": pre["descripcion"], "concepto": var["concepto"],
                    "regla": var["regla"], "representacion": rep,
                    "diccionario": var["diccionario"],
                    "grupo_vinculo": ficha["id"],
                    "huellas": {"huella_esquema": calc.get("huella_esquema"),
                                "huella_fila_diccionario": var["huella_fila_diccionario"]},
                    "evidencia_significado": {
                        "descripcion_original": pre["descripcion"],
                        "verificacion_por_calificador": pre["evidencias"]},
                    "evidencia_vinculo": {
                        "diccionario": ficha["diccionario"],
                        "recurso": ficha["recurso"],
                        "hoja": hoja_de(info["columna"]) or None,
                        "variable_unica_en_diccionario": var_unica,
                        "columna_unica_en_esquema": col_unica,
                        "relacion_nombre": notas["relacion_nombre"],
                        "detalle_nombre": notas["detalle_nombre"],
                        "representacion_declarada": rep,
                        "alcance": ficha["alcance"]["nota"],
                        "diferencia_campo_definicion": notas["diferencia_campo_definicion"],
                        "contexto_solo_contexto": contexto},
                    "criterio": ("Vinculo columna fisica -> variable documentada del mismo conjunto: "
                                 "nombre con relacion registrada, descripcion que respalda cada "
                                 "calificador, diccionario y recurso localizados en el conjunto, "
                                 "unicidad en diccionario y esquema, sin alias. Alcance documental."),
                    "alias_limitado": None,
                    "limitaciones": ("Solo esta columna (ver ficha de grupo); no se generaliza a "
                                     "otros recursos/anios; no valida valores, unidades, "
                                     "codificaciones ni pertenencia a catalogos."
                                     + (" Representacion no especificada en el diccionario."
                                        if rep in (None, "", "no_especificada") else "")),
                })
            else:
                for m in motivos_m:
                    motivos_vinculo[m.split(":")[0]] += 1
                pendientes.append({**info, "variable_iri": var.get("iri"),
                                   "concepto": var.get("concepto"), "regla": var.get("regla"),
                                   "grupo_vinculo": ficha["id"],
                                   "motivo": motivos_m[0], "motivos": motivos_m,
                                   "etapa": "vinculo",
                                   "detalle": pre["descripcion"][:200]})
            items.append(item)
        grupos.append({**ficha, "miembros": items,
                       "promovidos": sum(1 for i in items if i["dictamen"] == "promovida"),
                       "pendientes": sum(1 for i in items if i["dictamen"] == "pendiente")})

    amb_out = []
    for col in ambiguas:
        calc = cols_calc.get(col["columna"], {})
        vinc = []
        for ci in col["correspondencias"]:
            corr = corr_by_iri.get(ci, {})
            var = var_by_iri.get(corr.get("variable"), {})
            vinc.append({"correspondencia_iri": ci, "variable": corr.get("variable"),
                         "variable_nombre": var.get("variable"),
                         "definicion_iri": var.get("definicion_iri"),
                         "descripcion": corr.get("evidencia_textual"),
                         "estado_variable": var.get("estado"),
                         "huella_fila_diccionario": var.get("huella_fila_diccionario")})
        amb_out.append({"columna": col["columna"], "campo": col["campo"],
                        "recurso": col["recurso"], "conjunto": col["conjunto"],
                        "titulo_recurso": col.get("titulo_recurso"),
                        "fuente_esquema": col.get("fuente_esquema"),
                        "huella_esquema": calc.get("huella_esquema"),
                        "definiciones_por_nombre": col.get("definiciones_por_nombre"),
                        "vinculos": vinc,
                        "dictamen": "No promovible en esta ronda: variables fuera del nucleo o "
                                    "descripcion pendiente; su resolucion corresponde al agente 2.",
                        "limitaciones": "Requiere diccionario inteligible o aclaracion del publicador."})

    salida = {
        "generado_en_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": ("Revision de las 792 correspondencias candidata_por_nombre: preseleccion "
                    "lexica (675) + evaluacion del vinculo por grupo documental. Las 162 "
                    "revisiones existentes se conservan; las 3 columnas ambiguas y las 5 "
                    "observaciones quedan como contexto (agente 2)."),
        "conteos": {"candidatas_examinadas": len(candidatas),
                    "preseleccion_lexica": len(preseleccion),
                    "propuestas_finales": len(propuestas),
                    "descartes_vinculo": len(preseleccion) - len(propuestas),
                    "pendientes_clasificados": len(pendientes),
                    "conservadas_existentes": len(revisadas),
                    "columnas_ambiguas": len(ambiguas),
                    "vinculos_ambiguos": sum(len(a["vinculos"]) for a in amb_out),
                    "observaciones_contexto": len(pend.get("observaciones_revision", [])),
                    "grupos_vinculo": len(grupos),
                    "normalizaciones_ortograficas": len(normalizaciones),
                    "motivos_preseleccion": dict(motivos),
                    "motivos_vinculo": dict(motivos_vinculo)},
        "huellas_entrada": {"reglas": huella(sem["reglas_descripcion_exacta"]),
                            "pendientes": huella(pend["resumen"]),
                            "variables": huella([(v.get("iri"), v.get("estado")) for v in cob["variables"]])},
        "conservadas_existentes_iris": [c["columna"] for c in revisadas],
        "normalizaciones_ortograficas": normalizaciones,
        "grupos_vinculo": grupos,
        "propuestas_revisadas": propuestas,
        "pendientes_clasificados": pendientes,
        "ambiguos": amb_out,
        "observaciones_contexto": pend.get("observaciones_revision", []),
    }
    (OUT / "propuestas.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK: preseleccion {len(preseleccion)}, finales {len(propuestas)}, "
          f"pendientes {len(pendientes)}, conservadas {len(revisadas)}, grupos {len(grupos)}.")


if __name__ == "__main__":
    main()
