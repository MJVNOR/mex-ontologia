"""Revisión de correspondencias candidatas (agente 4).

Lee los archivos centrales (solo lectura) y escribe propuestas en esta carpeta.
No modifica ontologia/, data/, reports/ ni sincroniza Studio.
"""
import json
import sys
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from consolidar_semantica import huella, columnas  # noqa: E402
from integrar_contenido import clave  # noqa: E402

GENERICOS = {"territorio", "municipio", "entidad", "localidad", "tiempo",
             "anio", "organizacion", "mes", "fecha", "programa-educativo",
             "unidad-salud", "sexo", "edad"}

# Palabras que corroboran contexto por familia de concepto.
CONTEXTO_CLAVE = {
    "registro": {"registro", "divorcio", "matrimonio", "nacimiento", "defuncion",
                 "delito", "victima", "denuncia", "detencion"},
    "residencia": {"residencia", "madre", "difunto", "beneficiario", "alumno"},
    "defuncion": {"defuncion", "fallecimiento", "difunto", "muerte"},
    "subasta": {"subasta", "ganadera"},
    "precipitacion": {"precipitacion", "lluvia", "hidrico", "cuenca"},
    "donacion": {"donacion", "donante"},
    "inspeccion": {"inspeccion"},
    "censo": {"censo", "marginacion"},
    "captura": {"captura"},
    "agricola": {"agricola", "ciclo", "cultivo", "rural"},
    "educativo": {"escuela", "educacion", "programa", "plantel", "alumno"},
    "salud": {"salud", "hospital", "egreso", "urgencia", "consulta", "clues"},
}


def contexto_texto(col_iri, campo, titulo_conjunto, titulo_recurso):
    partes = [titulo_conjunto or "", titulo_recurso or ""]
    # Solo la hoja aporta contexto adicional; nunca el propio campo (evita
    # corroboración circular donde el nombre del campo se confirma a sí mismo).
    try:
        if "/file-column/" in col_iri:
            tail = unquote(col_iri.split("/file-column/")[1])
            segs = tail.split("/")
            if len(segs) >= 3:
                partes.append(segs[1])  # hoja
    except Exception:
        pass
    return clave(" ".join(partes))


def descripcion_distintiva(descripcion, regla):
    d = (descripcion or "").strip()
    if len(d) < 15:
        return False, "descripcion_corta_o_vacia"
    norm = clave(d)
    for rd in regla.get("descripciones", []):
        if norm == clave(rd):
            return True, "descripcion_igual_a_regla"
    # Contiene función/evento explícito más allá del nombre.
    funciones = ["registro", "residencia", "defuncion", "fallec", "nacimiento",
                 "parto", "matrimonio", "divorcio", "subasta", "precipitacion",
                 "donacion", "inspeccion", "captura", "censo", "agricola",
                 "consulta", "egreso", "escuela", "programa", "municipio",
                 "entidad", "localidad", "año", "ano", "mes", "fecha", "dia",
                 "hora", "sexo", "edad", "poblacion", "clave", "nombre"]
    hits = [f for f in funciones if f in norm]
    if len(hits) >= 2:
        return True, "descripcion_con_funcion_y_objeto:" + ",".join(hits[:4])
    return False, "descripcion_generica_sin_funcion"


SINONIMOS_CALIFICADOR = {
    "registro": {"registro", "delito", "victima", "denuncia", "incidencia", "reporte", "registro civil"},
    "residencia": {"residencia", "madre", "difunto", "beneficiario", "alumno", "reside"},
    "defuncion": {"defuncion", "fallec", "difunto", "muerte", "mortalidad"},
    "subasta": {"subasta", "ganadera"},
    "precipitacion": {"precipitacion", "lluvia", "hidrico", "cuenca"},
    "donacion": {"donacion", "organo", "tejido"},
    "inspeccion": {"inspeccion", "vigilancia", "visita", "proaes"},
    "censo": {"censo", "ganadero", "marginacion", "censo"},
    "captura": {"captura"},
    "agricola": {"agricola", "ciclo", "cultivo", "rural"},
    "educativo": {"escuela", "educacion", "programa", "plantel", "alumno"},
    "salud": {"salud", "hospital", "egreso", "urgencia", "consulta", "clues"},
    "llamada": {"llamada", "improcedente", "911"},
    "delito": {"delito", "incidencia", "victima", "denuncia", "fuero"},
    "nacimiento": {"nacimiento", "natalidad"},
    "matrimonio": {"matrimonio", "divorcio", "conyugal"},
}


def contexto_coherente(concepto, ctx):
    partes = (concepto or "").split("-")
    fam, calificadores = partes[0], partes[1:]
    # Palabras contradictorias: no promover registro cuando el contexto grita residencia y viceversa.
    if "residencia" in concepto and "registro" in ctx and "residencia" not in ctx:
        return False, "contexto_contradice_residencia_vs_registro"
    if "registro" in concepto and "residencia" in ctx and "registro" not in ctx:
        return False, "contexto_contradice_registro_vs_residencia"
    if "defuncion" in concepto and not any(w in ctx for w in ("defuncion", "fallec", "difunto", "muerte", "mortalidad")):
        # Exigir corroboración explícita para funciones sensibles.
        return False, "contexto_sin_corroboracion_defuncion"
    # Criterio estricto: el calificador debe aparecer literalmente en el contexto
    # conjunto/recurso/hoja. Los sinónimos temáticos (delito≈registro,
    # alumno≈educativo, víctima≈registro...) son pistas, no evidencia suficiente
    # para confirmar un papel semántico; solo motivan el pendiente.
    if calificadores:
        for cal in calificadores:
            if cal in ctx:
                return True, "contexto_corroborado:" + cal
        for cal in calificadores:
            for sin in SINONIMOS_CALIFICADOR.get(cal, set()):
                if sin in ctx:
                    return False, "pista_tematica_insuficiente:" + cal
        ctx_words = set(ctx.split())
        if fam in ctx_words:
            return False, "contexto_insuficiente_solo_reconfirma_nombre"
        return False, "contexto_insuficiente_solo_reconfirma_nombre"
    # Concepto genérico sin calificador: el contexto por sí solo no basta.
    return False, "contexto_insuficiente_solo_reconfirma_nombre"


def main():
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
    inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
    ins = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    base = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]

    reglas = {r["id"]: r for r in sem["reglas_descripcion_exacta"]}
    conceptos = set(sem["conceptos"].keys())
    revisadas = sem.get("vinculos_documentales_revisados", [])
    cons_rev = {(r["recurso"], r["campo"], r.get("columna")) for r in revisadas}

    var_by_iri = {v["iri"]: v for v in cob["variables"] if v.get("iri")}
    corr_by_iri = {c["iri"]: c for c in cob["correspondencias"]}
    cols_calc = {c["iri"]: c for c in columnas(inv, ins, base)}
    rec_titulo = {c["columna"]: (c.get("titulo_recurso") or "") for c in pend["columnas"]}

    propuestas, pendientes = [], []
    motivos = Counter()

    for col in pend["columnas"]:
        if col["estado"] != "candidata_por_nombre":
            continue
        calc = cols_calc.get(col["columna"], {})
        huella_esq = calc.get("huella_esquema")
        for ci in col["correspondencias"]:
            corr = corr_by_iri.get(ci)
            if not corr:
                continue
            var = var_by_iri.get(corr["variable"])
            base_info = {
                "columna": col["columna"], "campo": col["campo"],
                "recurso": col["recurso"], "conjunto": col["conjunto"],
                "titulo_recurso": col.get("titulo_recurso"),
                "fuente_esquema": col.get("fuente_esquema"),
                "correspondencia_iri": ci,
            }
            if not var or var.get("estado") != "respaldada_por_definicion":
                motivo = "variable_sin_respaldo:" + (var.get("estado") if var else "sin_variable_materializada")
                motivos[motivo] += 1
                pendientes.append({**base_info, "variable": corr.get("variable"),
                                   "motivo": motivo,
                                   "detalle": (corr.get("evidencia_textual") or "")[:160]})
                continue
            regla = reglas.get(var.get("regla"))
            if not regla or var.get("concepto") not in conceptos:
                motivos["regla_o_concepto_no_vigente"] += 1
                pendientes.append({**base_info, "variable": corr.get("variable"),
                                   "motivo": "regla_o_concepto_no_vigente",
                                   "detalle": str(var.get("regla"))})
                continue
            # Ajuste 2: exigir evidencia adicional al emparejamiento por nombre.
            nombre_exact = (col["campo"] == var["variable"]
                            or col["campo"].lower() == var["variable"].lower())
            nombre_norm = clave(col["campo"]) == clave(var["variable"])
            ok_desc, det_desc = descripcion_distintiva(var.get("descripcion"), regla)
            ctx = contexto_texto(col["columna"], col["campo"], var.get("titulo_conjunto"), col.get("titulo_recurso"))
            ok_ctx, det_ctx = contexto_coherente(var["concepto"], ctx)
            rep_esp = var.get("representacion") not in (None, "", "no_especificada")
            conc_esp = "-" in (var.get("concepto") or "")
            if not nombre_norm:
                motivos["nombre_no_coincide_ni_normalizado"] += 1
                pendientes.append({**base_info, "motivo": "nombre_no_coincide_ni_normalizado",
                                   "detalle": f"campo={col['campo']} variable={var['variable']}"})
                continue
            if nombre_exact and ok_desc and ok_ctx and rep_esp and conc_esp:
                alias = None
                if col["campo"] != var["variable"]:
                    alias = {"de": col["campo"], "a": var["variable"],
                             "alcance": "solo_columna:" + col["columna"]}
                propuestas.append({
                    "columna": col["columna"], "campo": col["campo"],
                    "recurso": col["recurso"], "conjunto": col["conjunto"],
                    "titulo_recurso": col.get("titulo_recurso"),
                    "fuente_esquema": col.get("fuente_esquema"),
                    "variable": var["variable"], "variable_iri": var["iri"],
                    "definicion_iri": var["definicion_iri"],
                    "definicion": var["descripcion"], "concepto": var["concepto"],
                    "regla": var["regla"], "representacion": var["representacion"],
                    "diccionario": var["diccionario"],
                    "evidencia": {"descripcion_original": var["descripcion"],
                                  "contexto": var.get("titulo_conjunto") + " / " + str(col.get("titulo_recurso")),
                                  "detalle_descripcion": det_desc, "detalle_contexto": det_ctx,
                                  "nombre_exact": True},
                    "huellas": {"huella_esquema": huella_esq,
                                "huella_fila_diccionario": var["huella_fila_diccionario"]},
                    "criterio": ("Revision explicita de campo en esquema de este recurso y fila de "
                                 "diccionario en mismo conjunto: nombre exacto (salvo caja), descripcion "
                                 "distintiva igual a regla o con funcion+objeto, contexto que corrobora, "
                                 "representacion especifica. Alcance documental; no valida valores ni catalogos."),
                    "alias_limitado": alias,
                    "limitaciones": ("Solo esta columna; no se generaliza a otros recursos/anios; "
                                     "no valida codificacion, unidades ni pertenencia a catalogos."),
                })
            else:
                faltan = []
                if not nombre_exact:
                    faltan.append("alias_requiere_revision_explicita")
                if not ok_desc:
                    faltan.append(det_desc)
                if not ok_ctx:
                    faltan.append(det_ctx)
                if not rep_esp:
                    faltan.append("representacion_no_especificada")
                if not conc_esp:
                    faltan.append("concepto_generico_sin_funcion")
                motivo = "evidencia_insuficiente:" + "+".join(faltan)
                motivos[motivo] += 1
                pendientes.append({**base_info, "variable": var["iri"],
                                   "concepto": var.get("concepto"), "regla": var.get("regla"),
                                   "motivo": motivo,
                                   "detalle": (var.get("descripcion") or "")[:160]})

    # Ambiguas: 3 columnas / 6 vínculos.
    ambiguos = []
    for col in pend["columnas"]:
        if "ambigua" not in col["estado"]:
            continue
        calc = cols_calc.get(col["columna"], {})
        vinculos = []
        for ci in col["correspondencias"]:
            corr = corr_by_iri.get(ci, {})
            var = var_by_iri.get(corr.get("variable"), {})
            vinculos.append({"correspondencia_iri": ci, "variable": corr.get("variable"),
                             "variable_nombre": var.get("variable"),
                             "definicion_iri": var.get("definicion_iri"),
                             "descripcion": corr.get("evidencia_textual"),
                             "estado_variable": var.get("estado"),
                             "huella_fila_diccionario": var.get("huella_fila_diccionario")})
        ambiguos.append({"columna": col["columna"], "campo": col["campo"],
                         "recurso": col["recurso"], "conjunto": col["conjunto"],
                         "titulo_recurso": col.get("titulo_recurso"),
                         "fuente_esquema": col.get("fuente_esquema"),
                         "huella_esquema": calc.get("huella_esquema"),
                         "definiciones_por_nombre": col.get("definiciones_por_nombre"),
                         "vinculos": vinculos,
                         "dictamen": ("No promovible: variables fuera_del_nucleo_actual, descripcion "
                                      "criptica 'ide_col', sin regla vigente. Se conserva ambigua."),
                         "limitaciones": "Requiere diccionario inteligible o aclaracion del publicador."})

    # Inconsistencias: revisión individual.
    inconsistencias = [
        {"id": "egresos-descripcion-urgencias", "recurso": "ad6f77b8-569d-4826-8ce0-3c6efddcb098",
         "campo": "Total_Egresos",
         "columna": "https://example.org/mex-ontologi/file-column/ad6f77b8-569d-4826-8ce0-3c6efddcb098%2FEgresos%20Hospitalarios%202018-2022%2F15",
         "dictamen": "pendiente_aclaracion_publicador",
         "pregunta": "¿Total_Egresos cuenta egresos hospitalarios o urgencias atendidas? El nombre dice egresos y la descripcion 'Total de urgencias atendidas' dice urgencias; no son equiparables.",
         "evidencia": "Esquema y diccionario usan Total_Egresos; descripcion original 'Total de urgencias atendidas'; variable sin respaldo (concepto None).",
         "propuesta": None,
         "limitaciones": "No interpretar ni cruzar hasta aclaracion."},
        {"id": "municipio-formato-ejemplo", "recurso": "046c2f52-72aa-4059-bf05-5ad52e191d1b",
         "campo": "CVE_MUN",
         "columna": "https://example.org/mex-ontologi/file-column/046c2f52-72aa-4059-bf05-5ad52e191d1b%2FIMM_2020%2F3",
         "dictamen": "revision_existente_mantenida_con_limitacion",
         "pregunta": "El diccionario declara formato nnn pero el ejemplo es 26048 (5 caracteres). ¿nnn es solo municipio o incluye entidad? ¿CVE_MUN equivale a CVEGEO?",
         "evidencia": "Vinculo documental_revisada vigente (concepto municipio, 'Clave del municipio'); huella_fila 35fb21e0; formato vs ejemplo contradictorios.",
         "propuesta": "Conservar revision de concepto; no resolver composicion de codigo ni correspondencia con CVEGEO.",
         "limitaciones": "No valida codificacion ni habilita cruce territorial por si sola."},
        {"id": "fecha-ejemplo-numerico", "recurso": "c07fe117-9789-48b3-9e3d-0e21eefc7476",
         "campo": "Fecha",
         "columna": "https://example.org/mex-ontologi/file-column/c07fe117-9789-48b3-9e3d-0e21eefc7476%2FLluvias%202025%2F5",
         "dictamen": "revision_existente_mantenida_con_limitacion",
         "pregunta": "El diccionario declara DD/MM/AAAA pero muestra 45658 (serial numerico). ¿Las fechas estan en texto o en serial Excel? ¿Zona horaria y hora de corte?",
         "evidencia": "Vinculo vigente (concepto fecha-precipitacion); huella_fila 30327f4d; formato vs ejemplo incompatibles.",
         "propuesta": "Conservar significado documental; no convertir ni cruzar fechas hasta comprobar representacion.",
         "limitaciones": "Significado no valida codificacion."},
        {"id": "anio-nacimientos-2024", "recurso": "ffca84a8-155e-41af-8223-0e098966cadf",
         "campo": "a–o",
         "columna": "https://example.org/mex-ontologi/column/ffca84a8-155e-41af-8223-0e098966cadf/a%E2%80%93o",
         "dictamen": "hipotesis_no_verificada_sigue_candidata",
         "pregunta": ("El campo datastore 'a–o' (a + U+2013 + o) podría ser 'año' mal codificado, "
                      "pero no está verificado: faltan los bytes crudos del datastore, la aplicabilidad "
                      "del diccionario CSV 6bcf5b63 al recurso API 2024 y la fila concreta (el orden "
                      "datastore difiere del orden del diccionario). Sigue candidata/pendiente, sin propuesta."),
         "evidencia": ("Recurso API 2024 sin tablas; diccionario 6bcf5b63 (hoja CSV) con variable 'año' "
                       "'Año de registro' respaldada (regla anio-registro). Hipótesis de mojibake no comprobada; "
                       "en-dash no es la corrupción habitual de ñ."),
         "propuesta": None,
         "limitaciones": "No proponer alias ni transferir revisión 2022 hasta verificar bytes, diccionario y fila."},
        {"id": "anio-divorcios-2023", "recurso": "f05dfd7e-88c9-42c4-ab88-e849fc277155",
         "campo": "anio_registro",
         "columna": "https://example.org/mex-ontologi/file-column/f05dfd7e-88c9-42c4-ab88-e849fc277155%2FCSV%2F3",
         "dictamen": "alias_especifico_propuesto",
         "pregunta": ("Alias explícito solo para esta columna: esquema 2023 trae 'anio_registro' (ASCII, con i) "
                      "y el diccionario único compartido 10357304 del mismo conjunto trae 'año_registro'. "
                      "Misma hoja CSV, misma posición 3, misma descripción de regla. No se extiende a otros recursos."),
         "evidencia": ("Diccionario 10357304 (único del conjunto Divorcios c6140d53, hoja CSV) variable "
                       "'año_registro' descripción 'Año de registro del divorcio', respaldada, regla anio-registro, "
                       "concepto anio-registro, formato NNNN; esquema 2023 hoja CSV posición 3 'anio_registro'."),
         "propuesta": {"variable": "año_registro", "diccionario": "10357304-e171-44ca-a453-f989e6a2ff83",
                        "concepto": "anio-registro", "regla": "anio-registro",
                        "alias_limitado": {"de": "anio_registro", "a": "año_registro",
                                           "alcance": "solo_columna:https://example.org/mex-ontologi/file-column/f05dfd7e-88c9-42c4-ab88-e849fc277155%2FCSV%2F3"},
                        "nota": "Propuesta, no aplicacion."},
         "limitaciones": "Solo esta columna 2023; no extiende revision 2022."},
    ]

    # Completar huellas de la propuesta por alias (buscar variable + esquema).
    var_by_key = {(v["conjunto"], v["diccionario"], v["variable"]): v for v in cob["variables"] if v.get("iri")}
    for inc in inconsistencias:
        p = inc.get("propuesta")
        if isinstance(p, dict) and "huellas" not in p:
            v = None
            for vv in cob["variables"]:
                if vv.get("iri") and vv["variable"] == p["variable"] and vv["diccionario"] == p["diccionario"]:
                    v = vv
                    break
            calc = cols_calc.get(inc["columna"], {})
            p["huellas"] = {"huella_esquema": calc.get("huella_esquema"),
                            "huella_fila_diccionario": v["huella_fila_diccionario"] if v else None}
            p["definicion"] = v["descripcion"] if v else None
            p["definicion_iri"] = v["definicion_iri"] if v else None
            p["variable_iri"] = v["iri"] if v else None
            p["representacion"] = v.get("representacion") if v else None

    # El alias propuesto cuenta como revisada adicional (fuera de las 891 candidatas).
    for inc in inconsistencias:
        if inc["dictamen"] == "alias_especifico_propuesto":
            p = inc["propuesta"]
            propuestas.append({
                "columna": inc["columna"], "campo": inc["campo"],
                "recurso": inc["recurso"],
                "conjunto": "df2d60f5-2243-4bb0-885a-941aa8a657f5" if "nacimientos" in inc["id"] else "c6140d53-1f16-4dd8-8ab3-d2b47f03a921",
                "variable": p["variable"], "variable_iri": p.get("variable_iri"),
                "definicion_iri": p.get("definicion_iri"), "definicion": p.get("definicion"),
                "concepto": p["concepto"], "regla": p["regla"],
                "representacion": p.get("representacion"), "diccionario": p["diccionario"],
                "evidencia": {"descripcion_original": p.get("definicion"),
                              "contexto": inc["evidencia"],
                              "nombre_exact": False, "alias_tecnico": p["alias_limitado"]},
                "huellas": p["huellas"],
                "criterio": ("Alias especifico para esta columna con evidencia tecnica "
                             "(mojibake/ASCII) + misma posicion, conjunto y descripcion de regla. No global."),
                "alias_limitado": p["alias_limitado"],
                "limitaciones": p.get("nota", "") + " " + inc["limitaciones"],
                "origen": inc["id"],
            })

    salida = {
        "generado_en_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": ("Propuestas, no aplicacion. Unidad columna fisica -> variable documentada. "
                    "Solo significados respaldados vigentes; sin conceptos nuevos ni normalizaciones globales."),
        "conteos": {"candidatas_examinadas": 891,
                    "columnas_ambiguas": len(ambiguos), "vinculos_ambiguos": sum(len(a["vinculos"]) for a in ambiguos),
                    "propuestas_revisadas": len(propuestas),
                    "pendientes_clasificados": len(pendientes),
                    "conservadas_existentes": len(revisadas),
                    "motivos_pendientes": dict(motivos)},
        "huellas_entrada": pend.get("huellas_entrada"),
        "conservadas_existentes_iris": sorted(cons_rev),
        "propuestas_revisadas": propuestas,
        "ambiguos": ambiguos,
        "pendientes_clasificados": pendientes,
        "inconsistencias": inconsistencias,
    }
    (OUT / "propuestas.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"propuestas={len(propuestas)} pendientes={len(pendientes)} ambiguos={len(ambiguos)}")
    print(dict(motivos).items())


if __name__ == "__main__":
    main()
