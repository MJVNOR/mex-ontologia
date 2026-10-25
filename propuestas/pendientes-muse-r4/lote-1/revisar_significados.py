"""Segunda revision lote-1: propone reglas nuevas con evidencia literal; conserva vinculos."""
import hashlib, json, sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("C:/Users/marti/Documents/MEX-Ontologi")
STAGE = ROOT / "propuestas/pendientes-muse-r4"
LOTE = STAGE / "lote-1"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion
from integrar_contenido import clave

asig = json.loads((LOTE / "asignacion.json").read_text(encoding="utf-8"))
ent = json.loads((LOTE / "entrega.json").read_text(encoding="utf-8"))
cob = json.loads((STAGE / "fuentes/data/semantica/cobertura.json").read_text(encoding="utf-8"))
sem = json.loads((STAGE / "fuentes/ontologia/semantica.json").read_text(encoding="utf-8"))
insp = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
ib = {r["id"]: r for r in insp["recursos"]}
cov = {v["definicion_iri"]: v for v in cob["variables"] if v.get("definicion_iri")}

def row_of(dic, idx):
    return ib[dic]["definiciones"][idx - 1]

def dec_parts(iri):
    dec = unquote(iri)
    dic = dec.split("/definition/", 1)[1].rsplit("/", 1)[0]
    return dic, int(dec.rsplit("/", 1)[1])

def tipo_fmt(row):
    t = next((str(row[k]).strip() for k in row if clave(k) == "tipo de dato" and str(row[k]).strip()), "")
    f = next((str(row[k]).strip() for k in row if clave(k) == "formato" and str(row[k]).strip()), "")
    u = next((str(row[k]).strip() for k in row if clave(k) in ("unidad de medida", "unidades de medida") and str(row[k]).strip()), "")
    e = next((str(row[k]).strip() for k in row if clave(k) in ("ejemplo de dato", "ejemplo") and str(row[k]).strip()), "")
    c = next((str(row[k]).strip() for k in row if clave(k) in ("catalogo de referencia", "catalago de referencia", "catalogo de referencia".replace(" ", " ")) and str(row[k]).strip()), "")
    return t, f, u, e, c

# concepto, etiqueta, definicion_concepto, representacion, limites, criterio
PLAN = {
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F1": ("numero-identificacion-registro-rickettsia", "N\u00famero de identificaci\u00f3n del registro",
  "N\u00famero de identificaci\u00f3n del registro en el conjunto Fiebre manchada (Rickettsia); entero con ejemplo 13468731. No se interpreta como folio oficial ni identidad de persona.", "codigo",
  ["Solo el n\u00famero de identificaci\u00f3n del registro en este conjunto; no acredita folio oficial, identidad ni equivalencia."],
  "Lectura literal: variable ide_id, descripci\u00f3n de identificaci\u00f3n, tipo Num\u00e9rico, ejemplo 13468731, sin cat\u00e1logo."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F39": ("otro-sintoma-paciente-rickettsia", "Otro s\u00edntoma del paciente",
  "Otro s\u00edntoma que presente el paciente, en texto libre (ejemplo Irritabilidad); campo de desborde textual, no c\u00f3digo ni diagn\u00f3stico.", "no_especificada",
  ["Texto libre del s\u00edntoma adicional; no homologa s\u00edntomas ni diagnostica."],
  "Lectura literal: variable otro_sintoma, texto libre con ejemplo Irritabilidad, sin cat\u00e1logo."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F60": ("caso-con-sangrado-snc", "Caso con sangrado SNC",
  "Indicador de si el paciente (caso en estudio de fiebre manchada) presenta sangrado SNC, codificado 1=Si 2=No seg\u00fan el diccionario; conserva poblaci\u00f3n, manifestaci\u00f3n y codificaci\u00f3n sin homologar ni diagnosticar.", "no_especificada",
  ["Bandera de registro del diccionario, no diagn\u00f3stico confirmado; sin CIE, cat\u00e1logo ni identidad."],
  "Descripci\u00f3n literal con poblaci\u00f3n, manifestaci\u00f3n y codificaci\u00f3n 1=Si 2=No; ejemplo 1, tipo Num\u00e9rico."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F130": ("otro-tipo-servicio-atencion", "Otro tipo de servicio de atenci\u00f3n",
  "Otro tipo de servicio de atenci\u00f3n en texto libre (ejemplo Epidemiolog\u00eda); campo de desborde distinto del campo catalogado servic_atencion.", "no_especificada",
  ["Texto libre adicional; no resuelve cat\u00e1logo ni equivale al campo servic_atencion."],
  "Lectura literal: variable otr_serv_atencion, texto libre con ejemplo, sin cat\u00e1logo."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F140": ("otra-comorbilidad-paciente-rickettsia", "Otra comorbilidad del paciente",
  "Otra comorbilidad que presenta el paciente, en texto libre (ejemplo Tuberculosis pulmonar); no codifica ni diagnostica.", "no_especificada",
  ["Texto libre de comorbilidad adicional; no homologa padecimientos ni diagnostica."],
  "Lectura literal: variable otros_especifique, texto libre con ejemplo, sin cat\u00e1logo."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F163": ("valor-cq-pcr-lesp-rickettsia", "Valor CQ de PCR en LESP",
  "Valor de CQ de resultado PCR en el LESP para rickettsiosis, num\u00e9rico con ejemplo 36.04; laboratorio LESP declarado, unidad no declarada.", "no_especificada",
  ["Unidad no declarada; no se asume ciclo umbral ni equivalencia con InDRE."],
  "Lectura literal: variable ricket_cq_lesp, num\u00e9rico con ejemplo 36.04, laboratorio LESP en la descripci\u00f3n."),
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F164": ("valor-cq-pcr-indre-rickettsia", "Valor CQ de PCR en InDRE",
  "Valor de CQ de resultado PCR en el InDRE para rickettsiosis, num\u00e9rico con ejemplo 32.61; laboratorio InDRE declarado, unidad no declarada.", "no_especificada",
  ["Unidad no declarada; no se asume ciclo umbral ni equivalencia con LESP."],
  "Lectura literal: variable ricket_cq, num\u00e9rico con ejemplo 32.61, laboratorio InDRE en la descripci\u00f3n."),
 "a7591bc9-f905-45cb-ba6c-ae3588d87594%2F3": ("grupo-cultivo-permiso-siembra", "Grupo del cultivo",
  "Grupo del cultivo en Permisos de Siembra de Trigo (ejemplo Trigo); etiqueta textual del grupo, sin cat\u00e1logo resuelto.", "nombre",
  ["Etiqueta textual; no acredita cat\u00e1logo de grupos ni identidad con otros cultivos."],
  "Lectura literal: variable GRUPO, texto con ejemplo Trigo, sin cat\u00e1logo."),
 "6aae6237-91d9-4d4b-9539-a8e41818444e%2F5": ("programa-pertenencia-comite", "Programa de pertenencia del comit\u00e9",
  "Programa al que pertenece la integraci\u00f3n del comit\u00e9 ciudadano (ejemplo COHESION COMUNITARIA); nombre textual, sin cat\u00e1logo.", "nombre",
  ["Nombre textual; no acredita cat\u00e1logo de programas ni identidad entre comit\u00e9s."],
  "Lectura literal: variable programa, texto con ejemplo, sin cat\u00e1logo."),
 "6aae6237-91d9-4d4b-9539-a8e41818444e%2F7": ("tema-integracion-comite", "Tema de la integraci\u00f3n del comit\u00e9",
  "Participaci\u00f3n ciudadana en la integraci\u00f3n del comit\u00e9 (ejemplo PARTICIPACI\u00d3N CIUDADANA); etiqueta textual del tema.", "nombre",
  ["Etiqueta textual; no tipifica temas ni cruza comit\u00e9s."],
  "Lectura literal: variable tema, texto con ejemplo, sin cat\u00e1logo."),
 "6aae6237-91d9-4d4b-9539-a8e41818444e%2F8": ("tipo-poblacion-beneficiaria-comite", "Tipo de poblaci\u00f3n beneficiaria del comit\u00e9",
  "Tipo de poblaci\u00f3n beneficiaria de la integraci\u00f3n del comit\u00e9 (ejemplo ADULTOS); etiqueta textual, sin cat\u00e1logo.", "no_especificada",
  ["Etiqueta textual; no acredita tipolog\u00eda oficial ni cohorte."],
  "Lectura literal: variable de tipo de poblaci\u00f3n, texto con ejemplo, sin cat\u00e1logo."),
 "251309e5-0309-46ed-9711-77a1dd408eeb%2F1": ("clave-geografica-localidad-marginacion", "Clave geogr\u00e1fica de localidad",
  "Clave geogr\u00e1fica declarada de la localidad en marginaci\u00f3n por localidad 2020, formato de 9 d\u00edgitos con ejemplo 260010001 y clasificaci\u00f3n INEGI declarada. Objeto: localidad.", "codigo",
  ["C\u00f3digo sin sistema publicado verificado; no acredita identidad con otras claves ni vigencia. Distinta de la clave de AGEB."],
  "Lectura literal: variable CVE_LOC, formato nnnnnnnnn, ejemplo 260010001, clasificaci\u00f3n INEGI declarada sin sistema verificado."),
 "73c403ec-d50d-4d82-9ef2-8725b9978229%2F3": ("tipo-guarderia", "Tipo de guarder\u00eda",
  "Tipo de guarder\u00eda en texto (ejemplo Publica Imss); etiqueta textual, sin cat\u00e1logo.", "no_especificada",
  ["Etiqueta textual; no acredita cat\u00e1logo de tipos."],
  "Lectura literal: variable Tipo, texto con ejemplo, sin cat\u00e1logo."),
 "73c403ec-d50d-4d82-9ef2-8725b9978229%2F5": ("estatus-guarderia", "Estatus de la guarder\u00eda",
  "Estatus de la guarder\u00eda en texto (ejemplo Inspeccionada); etiqueta textual, sin cat\u00e1logo.", "no_especificada",
  ["Etiqueta textual; no acredita cat\u00e1logo de estatus ni vigencia."],
  "Lectura literal: variable Estatus, texto con ejemplo, sin cat\u00e1logo."),
 "af0cb1b0-baa1-42c8-a581-d37787351d67%2F8": ("estatus-solicitud-apoyo", "Estatus de la solicitud de apoyo",
  "Situaci\u00f3n en la que se encuentra la solicitud de apoyo (ejemplo Apoyado; descripci\u00f3n cita atendido); etiqueta textual.", "no_especificada",
  ["Etiqueta textual; no acredita cat\u00e1logo de estatus ni cohorte."],
  "Lectura literal: variable Estatus, texto con ejemplo, unidad N/A, sin cat\u00e1logo."),
 "af0cb1b0-baa1-42c8-a581-d37787351d67%2F9": ("aclaracion-tipo-apoyo", "Aclaraci\u00f3n del tipo de apoyo",
  "Descripci\u00f3n m\u00e1s clara del tipo de apoyo en texto libre (ejemplo Apoyo para estudios de laboratorios).", "no_especificada",
  ["Texto libre aclaratorio; no tipifica apoyos ni autoriza cruces."],
  "Lectura literal: variable Observaciones, texto libre con ejemplo, sin cat\u00e1logo."),
 "30ed663b-585b-41b1-8f7a-7612f7fcdc12%2F2": ("actividad-lugar-inspeccion", "Actividad del lugar inspeccionado",
  "Actividad que se realiza en el lugar visitado por la PROAES (ejemplo HOSPITAL VETERINARIO); etiqueta textual.", "no_especificada",
  ["Etiqueta textual; no acredita cat\u00e1logo de actividades."],
  "Lectura literal: variable ACTIVIDAD, texto con ejemplo, sin cat\u00e1logo."),
 "30ed663b-585b-41b1-8f7a-7612f7fcdc12%2F3": ("motivo-inspeccion", "Motivo de la inspecci\u00f3n",
  "Motivo de la inspecci\u00f3n de la PROAES (ejemplo PROGRAMA ANUAL DE INSPECCION Y VIGILANCIA); etiqueta textual.", "no_especificada",
  ["Etiqueta textual; no tipifica motivos ni acredita programa."],
  "Lectura literal: variable MOTIVO, texto con ejemplo, sin cat\u00e1logo."),
}

PENDIENTES_REALES = {
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F177": "fila de diccionario corrupta: contiene encabezados de columnas como valores (Tipo de dato=ide_sex, Formato=ide_eda_ano...), descripci\u00f3n 'ide_col' inv\u00e1lida; sin definici\u00f3n real que respaldar.",
 "33d0a99e-c721-496f-a05e-07646e9ae42a%2F178": "fila de diccionario corrupta: contiene encabezados de columnas como valores; descripci\u00f3n 'ide_col' inv\u00e1lida; sin definici\u00f3n real que respaldar.",
}

merged = json.loads(json.dumps(sem))
reglas, conceptos, dec_sig = [], {}, []
for suf, spec in PLAN.items():
    iri = "https://example.org/mex-ontologi/definition/" + suf
    v = cov[iri]
    dic, idx = dec_parts(iri)
    row = row_of(dic, idx)
    t, f, u, ej, cat = tipo_fmt(row)
    cid, etq, defc, rep, lims, crit = spec
    assert iri not in [r["id"] for r in []]
    rid = "r4-lote-1-%03d" % (len(reglas) + 1)
    conceptos[cid] = [etq, defc, None]
    reglas.append({"id": rid, "concepto": cid, "representacion": rep, "nombres": [v["variable"]],
        "descripciones": [v["descripcion"]], "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
        "definiciones": [iri], "huella_fila_diccionario": v["huella_fila_diccionario"], "limites": lims,
        "evidencia": {"tipo": t, "formato": f, "unidad": u, "ejemplo": ej, "catalogo_declarado": cat},
        "criterio": crit, "fuente_revision": "propuestas/pendientes-muse-r4/lote-1/entrega.json"})
    dec_sig.append({"definicion_iri": iri, "decision": "proponer", "regla_id": rid, "concepto": cid,
        "motivo": "descripci\u00f3n + fila completa + contexto respaldan sentido literal limitado; regla restringida a esta definici\u00f3n.",
        "evidencia": ["cobertura estado=" + v.get("estado", "?"), "diccionario " + dic + " fila " + str(idx),
            "huella_fila=" + v["huella_fila_diccionario"], "tipo=" + t + " formato=" + f + " ejemplo=" + ej]})
for suf, motivo in PENDIENTES_REALES.items():
    iri = "https://example.org/mex-ontologi/definition/" + suf
    v = cov.get(iri, {})
    dec_sig.append({"definicion_iri": iri, "decision": "pendiente", "motivo": motivo,
        "evidencia": ["fila diccionario " + suf + " con encabezados como valores", "descripci\u00f3n 'ide_col' inv\u00e1lida"]})
assert {d["definicion_iri"] for d in dec_sig} == {x["definicion_iri"] for x in asig["variables_pendientes"]}

# valida nuevas reglas con el mismo motor del integrador
merged["conceptos"].update(conceptos)
merged["reglas_descripcion_exacta"] = merged["reglas_descripcion_exacta"] + reglas
for r in reglas:
    v = cov[r["definiciones"][0]]
    m = interpretacion(v["variable"], v["descripcion"], v["conjunto"], merged, v["diccionario"], v["definicion_iri"])
    assert m.get("regla") == r["id"] and m["estado"] == "respaldada_por_definicion", "regla no aplicada: " + r["id"]

# CVE_LOC: voltear columna pendiente -> proponer + vinculo con dependencia explicita
CVE = "https://example.org/mex-ontologi/definition/251309e5-0309-46ed-9711-77a1dd408eeb%2F1"
vloc = cov[CVE]
cve_cols = [d for d in ent["decisiones_columnas"] if d.get("definicion_iri") == CVE or (d["campo"] == "CVE_LOC" and d["decision"] == "pendiente")]
assert len(cve_cols) == 1, str(len(cve_cols))
dc = cve_cols[0]
# recomputa huella esquema igual que verificar.py
inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
resources = {r["id"]: r for r in inv["recursos"]}
from urllib.parse import unquote as _uq
_tail = dc["columna"].split("/file-column/", 1)[1]
_rid, _hoja, _pos = _uq(_tail).rsplit("/", 2)
assert _rid == dc["recurso"]
_ri = ib[_rid]
_tabla = [t for t in _ri["tablas"] if t["hoja"] == _hoja][0]
h_esc = huella(_tabla)
dc.update({"decision": "proponer", "definicion_iri": CVE,
    "motivo": "columna fisica verificada + fila exacta + definicion ahora respaldada por regla r4-lote-1 nueva; alcance documental.",
    "evidencia": dc["evidencia"] + ["nueva regla para " + CVE, "huella_esquema=" + h_esc]})
ent["vinculos"].append({"recurso": dc["recurso"], "campo": dc["campo"], "columna": dc["columna"],
    "diccionario": vloc["diccionario"], "concepto": "clave-geografica-localidad-marginacion", "descripcion": vloc["descripcion"],
    "huella_esquema": h_esc, "huella_fila_diccionario": vloc["huella_fila_diccionario"],
    "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto. Alcance documental; sin sistema verificado.",
    "dependencia": CVE})
# valida vinculo nuevo con motor
from consolidar_semantica import columnas as cols_fn
base = "https://example.org/mex-ontologi/"
inventory = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
inspection = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
colmap = {c["iri"]: c for c in cols_fn(inventory, inspection, base)}
names = {}
for vv in cob["variables"]:
    if vv.get("definicion_iri"):
        names[(vv["conjunto"], clave(vv["variable"]))] = names.get((vv["conjunto"], clave(vv["variable"])), 0) + 1
lk = ent["vinculos"][-1]
col = colmap[lk["columna"]]
assert all(lk[k] == col[k] for k in ("recurso", "campo", "huella_esquema"))
assert all(lk[k] == vloc[k] for k in ("diccionario", "descripcion", "huella_fila_diccionario"))
assert col["conjunto"] == vloc["conjunto"] and col["nombre_unico"] and names[(vloc["conjunto"], clave(vloc["variable"]))] == 1
act = interpretacion(vloc["variable"], vloc["descripcion"], vloc["conjunto"], merged, vloc["diccionario"], vloc["definicion_iri"])
assert act["estado"] == "respaldada_por_definicion" and act["concepto"] == lk["concepto"]

ent["decisiones_significados"] = dec_sig
ent["reglas"] = reglas
ent["conceptos_nuevos"] = conceptos
ent["solicitudes_investigacion"] = [
    {"definicion_iri": "https://example.org/mex-ontologi/definition/" + s, "fuente_probable": "publicador del conjunto 5494daa1-09ca-4750-aeac-2558553700e1", "documento_requerido": "diccionario corregido: las filas 177-178 contienen encabezados como valores"}
    for s in PENDIENTES_REALES]
(LOTE / "entrega.json").write_text(json.dumps(ent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# pendientes.json y conteos
pend_cols = [d for d in ent["decisiones_columnas"] if d["decision"] != "proponer"]
pend_sig = [d for d in dec_sig if d["decision"] != "proponer"]
(LOTE / "pendientes.json").write_text(json.dumps({"pendientes_columnas": pend_cols, "pendientes_significados": pend_sig,
    "conteo_columnas": len(pend_cols), "conteo_significados": len(pend_sig)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
n_prop = sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "proponer")
lines = ["# Resultado lote-1 ronda 4 (segunda revisi\u00f3n)", "",
 "Columnas asignadas: %d" % len(ent["decisiones_columnas"]), "proponer: %d" % n_prop,
 "pendiente: %d" % sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "pendiente"),
 "rechazar: %d" % sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "rechazar"),
 "vinculos: %d (1 con dependencia explicita de significado nuevo)" % len(ent["vinculos"]),
 "significados: %d (proponer %d, pendientes %d)" % (len(dec_sig), sum(1 for d in dec_sig if d["decision"] == "proponer"), len(pend_sig)),
 "reglas nuevas: %d, conceptos nuevos: %d" % (len(reglas), len(conceptos)), "",
 "Criterio segunda revisi\u00f3n: regla nueva solo con descripci\u00f3n + fila completa + contexto que respalden sentido literal limitado, restringida a una definici\u00f3n exacta con huella. Filas 177-178 quedan pendientes por fila corrupta real. Sin homologar cat\u00e1logos, medidas, IDs ni vigencia.", ""]
(LOTE / "resultado.md").write_text("\n".join(lines), encoding="utf-8")
sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
(LOTE / "listo.json").write_text(json.dumps({"sha256": sha, "sha256_entrega": sha, "columnas": len(ent["decisiones_columnas"]),
    "proponer": n_prop, "vinculos": len(ent["vinculos"]), "significados": len(dec_sig),
    "reglas": len(reglas), "estado": "completo-segunda-revision"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("reglas", len(reglas), "conceptos", len(conceptos), "proponer_col", n_prop, "vinc", len(ent["vinculos"]), sha)
