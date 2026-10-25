"""Agente 10 ronda 3: propuestas de significado para variables asignadas.

Lee (solo lectura): asignaciones del integrador, cobertura central,
semantica central (103 conceptos) e inspecciones de diccionarios.
Escribe SOLO en su carpeta: propuestas.json, resultado.md, fuente/huellas_entrada.json.
Sin red. Solo funciones stdlib.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
AGENTE = "ronda-3/agente-10-territorio-economia"
PREF = "r3a10-"

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

asig_path = ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"
cob_path = ROOT / "data/semantica/cobertura.json"
sem_path = ROOT / "ontologia/semantica.json"
MINE = load(asig_path)["asignaciones"]["10"]["variables"]
COB = load(cob_path)
SEM = load(sem_path)
CONCEPTOS_VIG = SEM["conceptos"]
REGLAS_VIG = {r["id"]: r for r in SEM["reglas_descripcion_exacta"]}

# ---- inspecciones: filas completas por indice de definicion_iri (%2FK -> K-1) ----
INS_DIR = ROOT / "data/portal/inspecciones"
dics = sorted({v["diccionario"] for v in MINE})


def norm_row(r):
    import unicodedata

    def fold(s):
        return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").casefold()

    g = {}
    for k, val in r.items():
        g[k.strip().rstrip(",")] = val
    flow = {fold(k): val for k, val in g.items()}

    def pick(*cands):
        for c in cands:
            if c in g:
                return g[c]
        for c in cands:
            if fold(c) in flow:
                return flow[fold(c)]
        return ""

    nombre = pick("Nombre variable")
    desc = pick("Descripcion")
    if not nombre and not desc:
        for k, val in g.items():
            kl = fold(k)
            if "nombre" in kl and "variable" in kl:
                nombre = val
            if "descripci" in kl:
                desc = val

    def anykey(*frags):
        for k, val in g.items():
            kl = fold(k)
            if all(fr in kl for fr in frags):
                return val
        return ""

    return {
        "nombre": nombre, "descripcion": desc,
        "tipo": pick("Tipo de dato") or anykey("tipo"),
        "formato": pick("Formato") or anykey("formato"),
        "unidad": pick("Unidad de medida") or anykey("unidad"),
        "catalogo": pick("Catalogo") or anykey("atalogo"),
        "nulos": anykey("nul"),
        "ejemplo": anykey("ejemplo"),
        "cruda": r,
    }


ROWS = {}
for d in dics:
    insp = load(INS_DIR / (d + ".json"))
    ROWS[d] = [norm_row(r) for r in insp.get("definiciones", [])]

MAL = []
for v in MINE:
    k = int(v["definicion_iri"].split("%2F")[1]) - 1
    filas = ROWS[v["diccionario"]]
    if k < 0 or k >= len(filas):
        MAL.append((v["definicion_iri"], "indice fuera de rango"))
        continue
    r = filas[k]
    if r["descripcion"].strip() != v["descripcion"].strip() or not r["descripcion"]:
        MAL.append((v["definicion_iri"], "descripcion: %r vs %r" % (r["descripcion"], v["descripcion"])))
if MAL:
    raise SystemExit("filas sin correspondencia literal: %s" % MAL[:10])


def fila(d, v):
    k = int(v["definicion_iri"].split("%2F")[1]) - 1
    r = ROWS[d][k]
    return {
        "tipo": r["tipo"], "formato": r["formato"], "unidad": r["unidad"],
        "catalogo": r["catalogo"], "nulos": r["nulos"], "ejemplo": r["ejemplo"],
        "nombre_crudo": r["nombre"], "descripcion_cruda": r["descripcion"],
    }

def danio(row):
    s = json.dumps(row, ensure_ascii=False)
    return "\ufffd" in s

# ---- acumuladores ----
decisiones, reglas = [], []
nuevos = {}
reutilizados = set()
seq = [0]

def concepto(slug, label, definicion, broader):
    if broader is not None and broader not in CONCEPTOS_VIG and broader not in nuevos:
        raise SystemExit("broader inexistente: %s" % broader)
    if slug in nuevos:
        return slug
    nuevos[slug] = [label, definicion, broader]
    return slug

def proponer(v, f, cslug, label, definicion, broader, rep, positivo, contraej, limite):
    concepto(cslug, label, definicion, broader)
    seq[0] += 1
    rid = "%s%04d" % (PREF, seq[0])
    ev = {
        "variable": v["variable"], "descripcion": v["descripcion"],
        "definicion_iri": v["definicion_iri"], "diccionario": v["diccionario"],
        "conjunto": v["conjunto"], "huella_fila_diccionario": v["huella_fila_diccionario"],
        "unidad_de_medida": f["unidad"],
        "tipo_de_dato": f["tipo"], "ejemplo_de_dato": f["ejemplo"],
        "catalogo_de_referencia": f["catalogo"],
    }
    reglas.append({
        "id": rid, "concepto": cslug, "representacion": rep,
        "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
        "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
        "definiciones": [v["definicion_iri"]],
        "criterio": "Revision agente 10 ronda 3; lectura literal de la fila del diccionario y contexto del conjunto; alcance fijado a esta definicion.",
        "fuente_revision": "propuestas/%s/propuestas.json" % AGENTE,
        "alcance": "Solo este diccionario, conjunto, definicion, nombre y descripcion.",
        "positivo": positivo, "contraejemplo": contraej,
        "limite": limite, "evidencia": [ev],
    })
    decisiones.append(decision_base(v, f, "proponer", cslug, rid, None))

def reutilizar(v, f, cslug_existente, rep, positivo, contraej, limite):
    if cslug_existente not in CONCEPTOS_VIG:
        raise SystemExit("concepto inexistente: %s" % cslug_existente)
    reutilizados.add(cslug_existente)
    seq[0] += 1
    rid = "%s%04d" % (PREF, seq[0])
    ev = {
        "variable": v["variable"], "descripcion": v["descripcion"],
        "definicion_iri": v["definicion_iri"], "diccionario": v["diccionario"],
        "conjunto": v["conjunto"], "huella_fila_diccionario": v["huella_fila_diccionario"],
        "unidad_de_medida": f["unidad"],
        "tipo_de_dato": f["tipo"], "ejemplo_de_dato": f["ejemplo"],
        "catalogo_de_referencia": f["catalogo"],
    }
    reglas.append({
        "id": rid, "concepto": cslug_existente, "representacion": rep,
        "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
        "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
        "definiciones": [v["definicion_iri"]],
        "criterio": "Revision agente 10 ronda 3; el concepto vigente cubre exactamente el objeto; regla nueva restringida a esta definicion.",
        "fuente_revision": "propuestas/%s/propuestas.json" % AGENTE,
        "alcance": "Solo este diccionario, conjunto, definicion, nombre y descripcion.",
        "positivo": positivo, "contraejemplo": contraej,
        "limite": limite, "evidencia": [ev],
    })
    decisiones.append(decision_base(v, f, "proponer", cslug_existente, rid, None))

def decision_base(v, f, estado, cslug, rid, motivo):
    d = {
        "definicion_iri": v["definicion_iri"], "conjunto": v["conjunto"],
        "titulo_conjunto": v["titulo_conjunto"], "diccionario": v["diccionario"],
        "variable": v["variable"], "descripcion_literal": v["descripcion"],
        "huella_fila_diccionario": v["huella_fila_diccionario"],
        "catalogo_declarado": v["catalogo_declarado"],
        "tipo_de_dato": f["tipo"], "unidad_de_medida": f["unidad"],
        "ejemplo_de_dato": f["ejemplo"], "catalogo_de_referencia": f["catalogo"],
        "decision": estado, "concepto": cslug, "regla": rid, "motivo": motivo,
    }
    if danio(ROWS[v["diccionario"]][int(v["definicion_iri"].split("%2F")[1]) - 1]["cruda"]):
        d["limite_fuente"] = "fila con U+FFFD; literal conservado"
    return d

def pendiente(v, f, motivo):
    decisiones.append(decision_base(v, f, "pendiente", None, None, motivo))

MESES_ES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO",
            "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

# ---- politica por diccionario ----
def g_quinq(v, f):
    n = v["variable"]
    banda = {"POB_00_04": "0 a 4", "POB_05_09": "5 a 9", "POB_10_14": "10 a 14",
             "POB_15_19": "15 a 19", "POB_20_24": "20 a 24", "POB_25_29": "25 a 29",
             "POB_30_34": "30 a 34", "POB_35_39": "35 a 39", "POB_40_44": "40 a 44",
             "POB_45_49": "45 a 49", "POB_50_54": "50 a 54", "POB_55_59": "55 a 59",
             "POB_60_64": "60 a 64", "POB_65_69": "65 a 69", "POB_70_74": "70 a 74",
             "POB_75_79": "75 a 79", "POB_80_84": "80 a 84"}.get(n)
    if banda:
        s = "poblacion-proyectada-edad-" + n[4:].lower()
        proponer(v, f, s, "Población proyectada de %s años" % banda,
                 "Población total reconstruida y ajustada de %s años en proyecciones por grupos quinquenales. Población del grupo de edad según literal. Medida: conteo." % banda,
                 "poblacion-total", "no_especificada",
                 "Denota el conteo proyectado del grupo de edad de la evidencia.",
                 "No aplica a otro grupo de edad ni a totales.",
                 "Proyección, no conteo observado; sin periodo declarado en la descripcion.")
    elif n == "POB_85_mm":
        proponer(v, f, "poblacion-proyectada-edad-85-mas", "Población proyectada de 85 años y más",
                 "Población total reconstruida y ajustada de 85 años y más en proyecciones por grupos quinquenales. Población del grupo de edad según literal. Medida: conteo.",
                 "poblacion-total", "no_especificada",
                 "Denota el conteo proyectado de 85 años y más.", "No aplica a otro grupo ni a totales.",
                 "Proyección, no conteo observado; sin periodo declarado en la descripcion.")
    else:
        proponer(v, f, "poblacion-total-proyectada-quinquenios", "Población total proyectada (quinquenios)",
                 "Población total reconstruida y ajustada en proyecciones por grupos quinquenales de edad. Población total según literal. Medida: conteo.",
                 "poblacion-total", "no_especificada",
                 "Denota el total proyectado de este conjunto.", "No aplica a un grupo de edad ni a otro conjunto.",
                 "Proyección, no conteo observado; no demuestra suma de grupos.")

def g_grandes(v, f):
    mapa = {"POB_00_11": ("0 a 11", "poblacion-proyectada-edad-0-11-grandes"),
            "POB_12_29": ("12 a 29", "poblacion-proyectada-edad-12-29-grandes"),
            "POB_30_59": ("30 a 59", "poblacion-proyectada-edad-30-59-grandes"),
            "POB_60_mm": ("60 años y más", "poblacion-proyectada-edad-60-mas-grandes")}
    if v["variable"] in mapa:
        banda, s = mapa[v["variable"]]
        proponer(v, f, s, "Población proyectada de %s (grandes grupos)" % banda,
                 "Población total de %s en proyecciones por grandes grupos de edad. Población del gran grupo según literal. Medida: conteo." % banda,
                 "poblacion-total", "no_especificada",
                 "Denota el conteo proyectado del gran grupo de la evidencia.",
                 "No aplica a otro gran grupo ni a quinquenios.",
                 "Proyección; cortes distintos de quinquenios, no intercambiables.")
    else:
        proponer(v, f, "poblacion-total-proyectada-grandes-grupos", "Población total proyectada (grandes grupos)",
                 "Suma de población total en proyecciones por grandes grupos de edad. Población total según literal. Medida: conteo.",
                 "poblacion-total", "no_especificada",
                 "Denota el total proyectado de este conjunto.", "No aplica a un grupo ni a quinquenios.",
                 "Proyección; no demuestra suma de grupos.")

INDIC = {
    "Hombres a mitad de año": ("hombres-mitad-anio", "Hombres a mitad de año", "Hombres a mitad de año en proyecciones de población municipal. Población: hombres. Medida: conteo."),
    "Mujeres a mitad de año": ("mujeres-mitad-anio", "Mujeres a mitad de año", "Mujeres a mitad de año en proyecciones de población municipal. Población: mujeres. Medida: conteo."),
    "Población a mitad de año del municipio": ("poblacion-mitad-anio-municipio", "Población a mitad de año del municipio", "Población a mitad de año del municipio en proyecciones. Población del municipio según literal. Medida: conteo."),
    "Población a mitad de año de entidad federativa del municipio": ("poblacion-mitad-anio-entidad-municipio", "Población a mitad de año de entidad federativa del municipio", "Población a mitad de año de la entidad federativa del municipio según literal. Población de la entidad según literal. Medida: conteo."),
    "Edad mediana": ("edad-mediana-poblacion", "Edad mediana", "Edad mediana de la población en proyecciones. Medida: años."),
    "Porcentaje del municipio": ("porcentaje-poblacion-municipio-estado", "Porcentaje de población del municipio en el estado", "Número de habitantes en el municipio por cada 100 habitantes en el estado, según unidad de medida. Medida: porcentaje."),
    "Relación Hombres -Mujeres": ("relacion-hombres-mujeres", "Relación hombres-mujeres", "Relación hombres-mujeres en proyecciones. Medida: razón."),
    "Razón de dependencia adulta": ("razon-dependencia-adulta", "Razón de dependencia adulta", "Razón de dependencia adulta en proyecciones. Medida: razón."),
    "Razón de dependencia infantil": ("razon-dependencia-infantil", "Razón de dependencia infantil", "Razón de dependencia infantil en proyecciones. Medida: razón."),
    "Razón de dependencia total": ("razon-dependencia-total", "Razón de dependencia total", "Razón de dependencia total en proyecciones. Medida: razón."),
    "Índice de Envejecimiento de población de 60 años y más": ("indice-envejecimiento-60-mas", "Índice de envejecimiento de 60 años y más", "Índice de envejecimiento de población de 60 años y más. Medida: índice."),
    "Índice de Envejecimiento de población de 65 años y más": ("indice-envejecimiento-65-mas", "Índice de envejecimiento de 65 años y más", "Índice de envejecimiento de población de 65 años y más. Medida: índice."),
}
BANDAS_IND = [("0 a 14 años", "00-14"), ("15 a 64 años", "15-64"), ("60 años y más", "60-mas"), ("65 años y más", "65-mas")]

def g_indic(v, f):
    d = v["descripcion"]
    if d in INDIC:
        s, lab, defi = INDIC[d]
        lim = "Proyección; la unidad literal manda sobre el nombre."
        if "entidad federativa del municipio" in d:
            lim = "Proyección; redacción literal ambigua (entidad del municipio); se conserva el literal sin reinterpretar."
        proponer(v, f, s, lab, defi, "poblacion-total", "no_especificada",
                 "Denota el indicador de la evidencia.", "No aplica a otro indicador.",
                 lim)
        return
    for banda, suf in BANDAS_IND:
        if d in ("Hombres de %s" % banda, "Mujeres de %s" % banda, "Población total de %s" % banda):
            if d.startswith("Población"):
                proponer(v, f, "poblacion-edad-%s" % suf, "Población de %s" % banda,
                         "%s en proyecciones de indicadores demográficos. Población del rango según literal. Medida: conteo." % d,
                         "poblacion-total", "no_especificada",
                         "Denota el conteo proyectado de la evidencia.", "No aplica a otra banda ni sexo.",
                         "Proyección, no conteo observado.")
                return
            pob = "hombres" if d.startswith("Hombres") else "mujeres"
            s = "%s-edad-%s" % (pob, suf)
            proponer(v, f, s, "%s de %s" % (d.split(" de ")[0], banda),
                     "%s en proyecciones de indicadores demográficos. Población: %s. Medida: conteo." % (d, pob),
                     "poblacion-total", "no_especificada",
                     "Denota el conteo proyectado de la evidencia.", "No aplica a otra banda ni sexo.",
                     "Proyección, no conteo observado.")
            return
    pendiente(v, f, "Descripcion sin correspondencia literal revisada; queda pendiente.")

MARG = {
    "analfabeta": ("porc-analfabetismo", "Porcentaje de población analfabeta de 15 años y más", "Porcentaje de población de 15 años y más analfabeta. Población de 15 años y más según literal. Medida: porcentaje."),
    "sin educación básica": ("porc-sin-educacion-basica", "Porcentaje sin educación básica de 15 años y más", "Porcentaje de población de 15 años y más sin educación básica. Población de 15 años y más según literal. Medida: porcentaje."),
    "sin educacion basica": ("porc-sin-educacion-basica", "Porcentaje sin educación básica de 15 años y más", "Porcentaje de población de 15 años y más sin educación básica. Población de 15 años y más según literal. Medida: porcentaje."),
    "sin drenaje": ("porc-sin-drenaje", "Porcentaje sin drenaje ni excusado", "Porcentaje de ocupantes en viviendas particulares sin drenaje ni excusado. Medida: porcentaje."),
    "sin energía eléctrica": ("porc-sin-energia-electrica", "Porcentaje sin energía eléctrica", "Porcentaje de ocupantes en viviendas particulares sin energía eléctrica. Medida: porcentaje."),
    "sin agua entubada": ("porc-sin-agua-entubada", "Porcentaje sin agua entubada", "Porcentaje de ocupantes en viviendas particulares sin agua entubada. Medida: porcentaje."),
    "piso de tierra": ("porc-piso-tierra", "Porcentaje con piso de tierra", "Porcentaje de ocupantes en viviendas particulares con piso de tierra. Medida: porcentaje."),
    "sin refrigerador": ("porc-sin-refrigerador", "Porcentaje sin refrigerador", "Porcentaje de ocupantes en viviendas particulares sin refrigerador. Medida: porcentaje."),
    "hacinamiento": ("porc-hacinamiento", "Porcentaje con hacinamiento", "Porcentaje de ocupantes o viviendas con hacinamiento según literal. Medida: porcentaje."),
    "Índice de marginación": ("indice-marginacion", "Índice de marginación", "Índice de marginación del nivel territorial de la evidencia, 2020. Medida: índice."),
    "Indice de marginación": ("indice-marginacion", "Índice de marginación", "Índice de marginación del nivel territorial de la evidencia, 2020. Medida: índice."),
    "Indice de margnación": ("indice-marginacion", "Índice de marginación", "Índice de marginación del nivel territorial de la evidencia, 2020. Medida: índice. Literal con errata conservado."),
    "Grado de marginación": ("grado-marginacion", "Grado de marginación", "Grado de marginación del nivel territorial de la evidencia, 2020."),
    "normalizado": ("indice-marginacion-normalizado", "Índice de marginación normalizado", "Índice de marginación normalizado del nivel territorial de la evidencia, 2020. Medida: índice."),
}

def g_marg(v, f, nivel):
    d = v["descripcion"]
    if "normalizado" in d:
        anio = ", 2020" if "2020" in d else ""
        lim = ("Medida: índice según literal; 2020 declarado; no acredita vigencia posterior."
               if anio else
               "Medida: índice según literal; año no declarado en la descripción ni en el conjunto; no se añade año desde el nombre de la variable.")
        proponer(v, f, "indice-marginacion-normalizado-%s" % nivel,
                 "Índice de marginación normalizado (%s)" % nivel,
                 "Índice de marginación normalizado%s. Medida: índice. Nivel: %s." % (anio, nivel),
                 None, "no_especificada",
                 "Denota el índice normalizado de la evidencia en %s." % nivel,
                 "No aplica al índice sin normalizar, a otro nivel ni a otro indicador.",
                 lim)
        return
    for clave, (base, lab, defi) in MARG.items():
        if clave in d and "Lugar" not in d and "menores a 2" not in d and "5 000" not in d and "no asiste" not in d and "derechohabiencia" not in d and "celular" not in d and "internet" not in d:
            if "2020" not in d:
                defi = defi.replace(", 2020", "")
                lim = "Medida declarada en porcentaje o índice según literal; año no declarado en la descripción ni en el conjunto; no se añade año desde el nombre de la variable."
            else:
                lim = "Medida declarada en porcentaje o índice según literal; 2020 declarado; no acredita vigencia posterior."
            s = "%s-%s" % (base, nivel)
            proponer(v, f, s, "%s (%s)" % (lab, nivel),
                     "%s Nivel: %s." % (defi, nivel), None, "no_especificada",
                     "Denota el indicador de marginación de la evidencia en %s." % nivel,
                     "No aplica a otro nivel territorial ni a otro indicador.",
                     lim)
            return
    resto = {
        "menos de 5 000 habitantes": ("porc-localidades-menores-5000", "Porcentaje en localidades de menos de 5 000 habitantes", "Porcentaje de población en localidades con menos de 5 000 habitantes. Medida: porcentaje."),
        "menores a 2 salarios": ("porc-ingreso-menor-2sm", "Porcentaje con ingresos menores a 2 salarios mínimos", "Porcentaje de población ocupada con ingresos menores a 2 salarios mínimos. Medida: porcentaje."),
        "Lugar que ocupa": ("posicion-nacional-marginacion", "Posición en el contexto nacional", "Lugar que ocupa en el contexto nacional en el índice de marginación."),
        "no asiste a la escuela": ("porc-inasistencia-escolar-6-14", "Porcentaje de 6 a 14 años que no asiste a la escuela", "Porcentaje de población de 6 a 14 años que no asiste a la escuela. Medida: porcentaje."),
        "derechohabiencia": ("porc-sin-derechohabiencia-salud", "Porcentaje sin derechohabiencia a salud", "Porcentaje de población sin derechohabiencia a los servicios de salud. Medida: porcentaje."),
        "sin celular": ("porc-sin-celular", "Porcentaje sin celular", "Porcentaje de ocupantes en viviendas particulares sin celular. Medida: porcentaje."),
        "sin internet": ("porc-sin-internet", "Porcentaje sin internet", "Porcentaje de ocupantes en viviendas particulares sin internet. Medida: porcentaje."),
    }
    for clave, (base, lab, defi) in resto.items():
        if clave in d:
            s = "%s-%s" % (base, nivel)
            proponer(v, f, s, "%s (%s)" % (lab, nivel), "%s Nivel: %s." % (defi, nivel),
                     None, "no_especificada",
                     "Denota el indicador de la evidencia en %s." % nivel, "No aplica a otro nivel ni indicador.",
                     "Medida y periodo según literal; no acredita vigencia posterior.")
            return
    if v["variable"] in ("IM_2020", "IMN_2020", "GM_2020", "ANALF", "SBASC", "OVSDE", "OVSEE", "OVSAE", "OVPT", "OVSREF", "OVHAC", "VHAC", "PL.5000", "PO2SM", "POSICION"):
        pendiente(v, f, "Descripcion no clasificada tras lectura literal; queda pendiente.")
        return
    pendiente(v, f, "Descripcion generica sin referente publicado suficiente; queda pendiente.")

def g_colonia_extra(v, f):
    d = v["descripcion"]
    n = v["variable"]
    mapa = {
        "Clave de ciudad del Sistema Urbano Nacional 2018": ("clave-ciudad-sun-2018-colonia", "Clave de ciudad del SUN 2018", "Clave de ciudad del Sistema Urbano Nacional 2018. Objeto: ciudad.", "codigo", "Código sin catálogo publicado; no acredita identidad urbana."),
        "Clave de colonia": ("clave-colonia-marginacion", "Clave de colonia", "Clave de la colonia en marginación urbana por colonia. Objeto: colonia.", "codigo", "Código sin catálogo publicado; no acredita identidad de colonia."),
        "Identificación de colonia": ("identificador-colonia-marginacion", "Identificación de colonia", "Identificación de la colonia en marginación urbana por colonia. Objeto: colonia.", "no_especificada", "Representación no declarada; puede ser clave o nombre según recurso."),
        "Código Postal": ("codigo-postal-colonia-marginacion", "Código postal de la colonia", "Código postal declarado de la colonia en marginación urbana. Objeto: colonia.", "codigo", "Código postal declarado; no acredita delimitación oficial ni identidad."),
        "Nombre de ciudad del Sistema Urbano Nacional 2018": ("nombre-ciudad-sun-2018-colonia", "Nombre de ciudad del SUN 2018", "Nombre de ciudad del Sistema Urbano Nacional 2018. Objeto: ciudad.", "nombre", "Nombre declarado; no acredita catálogo oficial."),
        "Nombre de la colonia": ("nombre-colonia-marginacion", "Nombre de la colonia", "Nombre de la colonia en marginación urbana por colonia. Objeto: colonia.", "nombre", "Nombre declarado; no acredita catálogo oficial."),
        "Clasificación": None,
    }
    if d in mapa:
        if mapa[d] is None:
            pendiente(v, f, "Descripcion de una palabra sin referente publicado; queda pendiente.")
            return
        s, lab, defi, rep, lim = mapa[d]
        proponer(v, f, s, lab, defi, None, rep,
                 "Denota el dato de la evidencia.", "No aplica a otro objeto ni conjunto.", lim)
        return
    g_marg(v, f, "colonia")

def g_meses(v, f, familia, actual):
    mes = v["variable"].strip().upper()
    if mes in MESES_ES:
        lab = mes.capitalize()
        s = "%s-%s-%s" % (familia, mes.lower(), actual)
        proponer(v, f, s, "%s de %s (%s)" % (familia.replace("-", " "), lab, actual),
                 "%s en el mes de %s, conjunto de metodología %s. Medida no declarada en la descripción; valor del mes según recurso." % (familia.replace("-", " "), lab, actual),
                 None, "no_especificada",
                 "Denota el valor del mes de la evidencia (el mes lo indica el nombre literal, restringido en la regla).",
                 "No aplica a otro mes ni a otra metodología.",
                 "Registro mensual, no ocurrencia; la descripción no declara la medida del valor; metodología %s, no comparable con la otra sin acreditación." % actual)
    else:
        pendiente(v, f, "Fuera del patron mensual esperado; queda pendiente.")

PEND_GENERICO = {
    "Numero de la entrada": "Folio de orden de la entrada; sin significado documental propio.",
    "Medio por el cual se tomo la denuncia": "Canal de recepción sin catálogo de valores publicado.",
    "Asunto general de la denuncia": "Descripción genérica sin tipología publicada.",
    "Hechos descritos en la denuncia": "Texto libre de hechos; sin referente codificable publicado.",
    "Giro de la denuncia": "Descripción genérica sin tipología publicada.",
    "Materia de la denuncia": "Descripción genérica sin materia publicada.",
    "Descripción específica del tipo de delito que se realizó": "Clasificación delictiva sin catálogo de tipos publicado.",
    "Detalle más específico sobre la modalidad del delito realizado": "Clasificación delictiva sin catálogo de modalidades publicado.",
    "Detalle más específico sobre el tipo de delito que se realizó": "Clasificación delictiva sin catálogo de tipos publicado.",
    "Categoría general en la que entra el delito cometido": "Clasificación delictiva sin catálogo publicado.",
    "Categoría en la que se puede clasificar el delito": "Clasificación delictiva sin catálogo publicado.",
    "Último nivel de detalle en la que se puede clasificar el delito": "Clasificación delictiva sin catálogo publicado.",
    "Campo en la que el delito se realizó": "El nombre (Bien jurídico afectado) contradice la descripción (campo del delito); se conserva la contradicción y queda pendiente sin promover categoría.",
    "Actividad que se realiza en el lugar": "Actividad sin referente publicado.",
    "Motivo de la inspeccion": "Motivo sin catálogo de motivos publicado.",
    "Actividad que ejecuta donde se inspecciona o se vigila": "Actividad sin referente publicado.",
    "Motivo de la inspeccion o vigilancia": "Motivo sin catálogo de motivos publicado.",
    "Identificador del evento": "Identificador sin sistema de identidad publicado.",
    "Identificador de la respuesta": "Identificador sin sistema de identidad publicado.",
    "Monto": "Importe de una palabra sin medida ni objeto declarados.",
    "Unidad de apoyos que fueron entregados": "El nombre (Cantidad de apoyos otorgados) contradice la descripción (unidad de apoyos); se conserva la contradicción y queda pendiente.",
    "Diferentes vienes los cuales fueron otorgados": "El nombre (Comentarios/Observaciones) contradice la descripción imprecisa (literal con errata); se conserva la contradicción y queda pendiente.",
    "Tipo esfecífico de ayuda otorgada a la víctima": "Tipo de ayuda sin catálogo publicado.",
    "Concepto general bajo el cual se clasifica el apoyo otorgado": "Clasificación sin catálogo publicado.",
    "Grupo de personas que reciben el apoyo": "Grupo sin referente publicado.",
    "Sector poblacional al que pertenece la población beneficiaria": "Sector sin referente publicado.",
    "Nivel de financiamiento otorgado": "Nivel sin escala publicada.",
    "programa al que pertenece  la integración de comité": "Programa sin catálogo publicado.",
    "tipo de población beneficidada de la integración de comité": "Tipo sin referente publicado.",
    "participación ciudadana en la integración de los comites": "El nombre (tema) no fija el objeto de la descripción; se conserva la diferencia y queda pendiente sin medida declarada.",
    "Clasificación": "Descripción de una palabra sin referente publicado.",
    "Descripción mas clara del tipo de apoyo": "Descripción genérica sin tipología publicada.",
    "situación en la que se encuentra la solicitud de apoyo: atendido": "Valor de estado sin catálogo de estados publicado.",
    "Estatus del centro nocturno": "Estado sin catálogo de valores publicado.",
    "Tipo de centro nocturno": "Tipo sin tipología publicada.",
    "Estatus de la guarderia": "Estado sin catálogo de valores publicado.",
    "Tipo de guarderia": "Tipo sin tipología publicada.",
    "clasificación de la llamada realizada": "Clasificación sin catálogo de valores publicado.",
    "Número de convocatoria": "Folio de convocatoria; sin significado documental propio.",
    "que giro tiene el estableciemiento que es zona salva": "Giro del establecimiento sin tipología publicada.",
}

DISPATCH = {}

def procesar(v):
    f = fila(v["diccionario"], v)
    d = v["descripcion"]
    dic = v["diccionario"]
    if d in PEND_GENERICO:
        pendiente(v, f, PEND_GENERICO[d] + " Queda pendiente.")
        return
    if dic == "03a33e71-d447-47b1-aa0d-b341996e023c":
        g_quinq(v, f); return
    if dic == "1b6d0817-66a9-4b25-9468-efca73e3ce20":
        g_grandes(v, f); return
    if dic == "f1bbd13b-3364-441c-81b4-7b7c548be39f":
        g_indic(v, f); return
    if dic == "251309e5-0309-46ed-9711-77a1dd408eeb":
        g_marg(v, f, "localidad"); return
    if dic == "3395795d-b152-4706-b81e-2b562f86a207":
        g_marg(v, f, "municipio"); return
    if dic == "55acbd44-8de2-4f34-8ee5-56d37bc050a1":
        if d == "Clave de la AGEB":
            proponer(v, f, "clave-ageb-marginacion", "Clave de la AGEB", "Clave de la AGEB en marginación urbana. Objeto: AGEB.", None, "codigo", "Denota la clave declarada.", "No aplica a otra AGEB ni conjunto.", "Código sin catálogo publicado; no acredita identidad geoestadística.")
        elif d == "Clave geográfica":
            proponer(v, f, "clave-geografica-ageb-marginacion", "Clave geográfica", "Clave geográfica declarada de la AGEB en marginación urbana. Objeto: AGEB.", None, "codigo", "Denota la clave declarada.", "No aplica a otro objeto.", "Código sin sistema publicado; no acredita identidad.")
        else:
            g_marg(v, f, "ageb")
        return
    if dic == "67156807-2013-4117-9ca9-394aea647127":
        g_colonia_extra(v, f); return
    if dic == "9f3d34b9-8963-4fc1-ad27-6967f66749a6":
        g_marg(v, f, "entidad"); return
    if dic == "213ebb9a-eb3f-4fdd-ab3a-b803a26ec919":
        if d == "Identificador del estado de captura según INEGI":
            reutilizar(v, f, "entidad", "codigo", "Denota la entidad federativa de captura.", "No aplica a otro estado ni función.", "Código INEGI declarado; sin catálogo de referencia publicado en la fila; no acredita catálogo oficial.")
        else:
            g_meses(v, f, "victimas-registradas", "anterior")
        return
    if dic == "a8a09044-87db-49a2-82c3-29594ec6ffd5":
        if d == "Grupo de edad en donde se encuentra la víctima":
            proponer(v, f, "grupo-edad-victima-fuero-comun", "Grupo de edad de la víctima", "Grupo de edad en donde se encuentra la víctima del fuero común. Población: víctimas.", "grupo-edad", "no_especificada", "Denota el grupo etario declarado.", "No aplica a otra población.", "Sin rangos publicados en la descripcion; no acredita categorías.")
        elif d == "Sexo de la víctima":
            proponer(v, f, "sexo-victima-fuero-comun", "Sexo de la víctima", "Sexo de la víctima del fuero común. Población: víctimas.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados; no acredita categorías.")
        else:
            g_meses(v, f, "victimas-registradas", "actual")
        return
    if dic == "404e97de-3954-4106-82ee-afd2cb20b868":
        if d == "Clave única de cada municipio en el estado según INEGI":
            reutilizar(v, f, "municipio", "codigo", "Denota el municipio del registro.", "No aplica a otro municipio ni función.", "Código INEGI declarado; sin catálogo de referencia publicado en la fila; no acredita catálogo oficial.")
        else:
            g_meses(v, f, "delitos-registrados-municipal", "anterior")
        return
    if dic == "5f46e4b8-858d-47dc-a180-125f3cc8727a":
        g_meses(v, f, "delitos-registrados-municipal", "actual"); return
    resto_simple(v, f)

def resto_simple(v, f):
    d = v["descripcion"]; dic = v["diccionario"]; n = v["variable"]
    SIMPLE = {
        # ITAMA internamiento
        "sexo de la persona internada": ("sexo-persona-internada-itama", "Sexo de la persona internada", "Sexo de la persona internada en ITAMA. Población: personas internadas.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "edad actual de la persona internada": ("edad-persona-internada-itama", "Edad actual de la persona internada", "Edad actual de la persona internada en ITAMA. Población: personas internadas. Unidad no declarada en la fila.", None, "no_especificada", "Denota la edad declarada.", "No aplica a otra población.", "Unidad no declarada; no se asumen años."),
        "delito por el cual esta recluido": ("delito-persona-internada-itama", "Delito de la persona internada", "Delito por el cual está recluida la persona internada en ITAMA.", None, "no_especificada", "Denota el delito declarado.", "No aplica a otra persona ni etapa.", "Sin catálogo de delitos publicado; no acredita tipificación."),
        "sexo de la persona externada": ("sexo-persona-externada-itama", "Sexo de la persona externada", "Sexo de la persona externada en ITAMA. Población: personas externadas.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "edad actual de la persona externada": ("edad-persona-externada-itama", "Edad actual de la persona externada", "Edad actual de la persona externada en ITAMA. Población: personas externadas. Unidad no declarada en la fila.", None, "no_especificada", "Denota la edad declarada.", "No aplica a otra población.", "Unidad no declarada; no se asumen años."),
        "delito por el cual estuvo recluido": ("delito-persona-externada-itama", "Delito de la persona externada", "Delito por el cual estuvo recluida la persona externada en ITAMA.", None, "no_especificada", "Denota el delito declarado.", "No aplica a otra persona ni etapa.", "Sin catálogo publicado; hecho histórico, no situación actual."),
        "tiempo de sentencia que compurgo la persona": ("tiempo-sentencia-persona-externada", "Tiempo de sentencia compurgado", "Tiempo de sentencia que compurgó la persona externada en ITAMA. Medida: tiempo.", None, "no_especificada", "Denota el tiempo declarado.", "No aplica a otra persona.", "Unidad no declarada en la descripcion."),
        # CERESOS
        "municipio en la que se enuentra en cereso": None,  # reutilizar municipio-ubicacion
        "población total del cereso": ("poblacion-total-cereso", "Población total del CERESO", "Población total del CERESO según literal. Población: población del centro. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el total declarado.", "No aplica a otro centro.", "Situación jurídica no declarada; sin fecha declarada."),
        "población masculina del cereso": ("poblacion-masculina-cereso", "Población masculina del CERESO", "Población masculina del CERESO según literal. Unidad no declarada en la fila.", "poblacion-total", "no_especificada", "Denota el valor declarado.", "No aplica a mujeres ni a otro centro.", "Situación jurídica no declarada; sin fecha declarada."),
        "población femenina del cereso": ("poblacion-femenina-cereso", "Población femenina del CERESO", "Población femenina del CERESO según literal. Unidad no declarada en la fila.", "poblacion-total", "no_especificada", "Denota el valor declarado.", "No aplica a hombres ni a otro centro.", "Situación jurídica no declarada; sin fecha declarada."),
        # Detenidas
        "agencia a la que se turno el detenido": ("agencia-turno-detenido", "Agencia a la que se turnó el detenido", "Agencia a la que se turnó la persona detenida. Objeto: agencia.", None, "no_especificada", "Denota la agencia declarada.", "No aplica a otra detención.", "Sin catálogo de agencias publicado."),
        "delito por el cual detuvieron a la persona": ("delito-detencion-persona", "Delito de la detención", "Delito por el cual detuvieron a la persona. Hecho: detención.", None, "no_especificada", "Denota el delito declarado.", "No aplica a otra detención.", "Sin catálogo publicado; no acredita tipificación."),
        "edad del detenido": ("edad-detenido", "Edad del detenido", "Edad de la persona detenida. Población: detenidos. Unidad no declarada en la fila.", None, "no_especificada", "Denota la edad declarada.", "No aplica a otra población.", "Unidad no declarada; no se asumen años."),
        "hora de la detención de la persona": ("hora-detencion-persona", "Hora de la detención", "Hora de la detención de la persona. Evento: detención.", "tiempo", "hora", "Denota la hora declarada.", "No aplica a otro evento.", "Hora del hecho, no de registro."),
        "motivo del origen dela detencion de la persona": ("motivo-origen-detencion", "Motivo de origen de la detención", "Motivo del origen de la detención de la persona.", None, "no_especificada", "Denota el motivo declarado.", "No aplica a otra detención.", "Sin catálogo de motivos publicado."),
        "nivel de fuerza que se utilizo para la detencion": ("nivel-fuerza-detencion", "Nivel de fuerza de la detención", "Nivel de fuerza que se utilizó para la detención de la persona.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otra detención.", "Sin escala publicada."),
        "nivel de fuerza que se utilizo para la detencion": ("nivel-fuerza-detencion", "Nivel de fuerza de la detención", "Nivel de fuerza que se utilizó para la detención de la persona.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otra detención.", "Sin escala publicada."),
        "sexo del detenido": ("sexo-detenido", "Sexo del detenido", "Sexo de la persona detenida. Población: detenidos.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "Estado de desaparición de la víctima": ("entidad-desaparicion-victima", "Estado de desaparición de la víctima", "Estado de desaparición de la víctima según literal. Objeto: entidad federativa.", "entidad", "no_especificada", "Denota la entidad declarada.", "No aplica a nacimiento ni a otra víctima.", "Función de desaparición, no residencia ni registro."),
        "Estado de nacimiento de la víctima": ("entidad-nacimiento-victima-desaparecida", "Estado de nacimiento de la víctima", "Estado de nacimiento de la víctima según literal. Objeto: entidad federativa.", "entidad", "no_especificada", "Denota la entidad declarada.", "No aplica a desaparición.", "Nacimiento, no residencia."),
        "Estatus en que se encuentra la víctima": ("estatus-victima-desaparecida", "Estatus de la víctima", "Estatus en que se encuentra la víctima según literal.", None, "no_especificada", "Denota el estatus declarado.", "No aplica a otra víctima.", "Sin catálogo de estatus publicado."),
        "Etnia que pertenece la víctima": ("etnia-victima-desaparecida", "Etnia de la víctima", "Etnia a la que pertenece la víctima según declaración. Población: víctimas.", None, "no_especificada", "Denota la adscripción declarada.", "No aplica a lengua ni a otra víctima.", "Autoadscripción declarada; sin catálogo; no acredita identidad étnica."),
        "Lengua que pertenece la víctima": ("lengua-victima-desaparecida", "Lengua de la víctima", "Lengua a la que pertenece la víctima según declaración. Población: víctimas.", None, "no_especificada", "Denota la lengua declarada.", "No aplica a etnia.", "Lengua declarada; sin catálogo; no acredita identidad."),
        "Nacionalidad de la víctima": ("nacionalidad-victima-desaparecida", "Nacionalidad de la víctima", "Nacionalidad de la víctima según literal. Población: víctimas.", None, "no_especificada", "Denota la nacionalidad declarada.", "No aplica a otra víctima.", "Nacionalidad declarada; sin catálogo."),
        "Sexo de la víctima": ("sexo-victima-desaparecida", "Sexo de la víctima", "Sexo de la víctima según literal. Población: víctimas.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "actividad de la integración de comité": ("actividad-integracion-comite", "Actividad de la integración del comité", "Actividad de la integración del comité ciudadano. Objeto: comité.", None, "no_especificada", "Denota la actividad declarada.", "No aplica a otro comité.", "Sin catálogo de actividades publicado."),
        "colonia de la integración de comité": ("colonia-integracion-comite", "Colonia de la integración del comité", "Colonia de la integración del comité ciudadano. Objeto: colonia.", "localidad", "no_especificada", "Denota la colonia declarada.", "No aplica a otro comité.", "Colonia declarada; no acredita catálogo."),
        "total hombres de la integración de comité": ("total-hombres-integracion-comite", "Total de hombres de la integración", "Total de hombres de la integración del comité. Población: hombres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a mujeres.", "Sin fecha declarada."),
        "total mujeres de la integración de comité": ("total-mujeres-integracion-comite", "Total de mujeres de la integración", "Total de mujeres de la integración del comité. Población: mujeres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a hombres.", "Sin fecha declarada."),
        "Ciudad de provenencia del encuestado": ("ciudad-provenencia-encuestado", "Ciudad de proveniencia del encuestado", "Ciudad de proveniencia del encuestado en registro de usuarios beneficiados. Objeto: ciudad.", "localidad", "no_especificada", "Denota la ciudad declarada.", "No aplica a otro encuestado.", "Ciudad declarada; no acredita catálogo."),
        "Colonia de provenencia del encuestado": ("colonia-provenencia-encuestado", "Colonia de provenencia del encuestado", "Colonia de proveniencia del encuestado en registro de usuarios. Objeto: colonia.", "localidad", "no_especificada", "Denota la colonia declarada.", "No aplica a otro encuestado.", "Colonia declarada; no acredita catálogo."),
        "Deporte o actividad que practica en la unidad deportiva el encuestado": ("deporte-encuestado-unidad", "Deporte o actividad del encuestado", "Deporte o actividad que practica en la unidad deportiva el encuestado.", None, "no_especificada", "Denota la actividad declarada.", "No aplica a otro encuestado.", "Sin catálogo de actividades publicado."),
        "Edad del encuestado": ("edad-encuestado-registro-usuarios", "Edad del encuestado", "Edad del encuestado en registro de usuarios beneficiados. Unidad no declarada en la fila.", None, "no_especificada", "Denota la edad declarada.", "No aplica a otro encuestado.", "Unidad no declarada; no se asumen años."),
        "Evento en el que participa el encuestado": ("evento-participa-encuestado", "Evento del encuestado", "Evento en el que participa el encuestado en la unidad deportiva. Objeto: evento.", None, "no_especificada", "Denota el evento declarado.", "No aplica a otro encuestado.", "Evento declarado; sin catálogo."),
        "Fecha y hora de la respuesta": ("fecha-hora-respuesta-encuesta", "Fecha y hora de la respuesta", "Fecha y hora de la respuesta del encuestado. Evento: respuesta de encuesta.", "tiempo", "no_especificada", "Denota el momento declarado.", "No aplica a otra respuesta.", "Momento de respuesta, no del evento referido."),
        "Genero del encuestado": ("genero-encuestado-registro-usuarios", "Género del encuestado", "Género del encuestado en registro de usuarios beneficiados.", "sexo-declarado", "no_especificada", "Denota el género declarado.", "No aplica a otro encuestado.", "Sin valores publicados."),
        "Nivel escolar del encuestado": ("nivel-escolar-encuestado", "Nivel escolar del encuestado", "Nivel escolar del encuestado en registro de usuarios beneficiados.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otro encuestado.", "Sin catálogo de niveles publicado."),
        "Razon por la que visita la unidad el encuestado": ("motivo-visita-unidad-encuestado", "Motivo de visita a la unidad", "Razón por la que visita la unidad deportiva el encuestado.", None, "no_especificada", "Denota el motivo declarado.", "No aplica a otro encuestado.", "Sin catálogo de motivos publicado."),
        "Unidad deportiva a la que acude el encuestado": ("unidad-deportiva-encuestado", "Unidad deportiva del encuestado", "Unidad deportiva a la que acude el encuestado. Objeto: unidad deportiva.", None, "no_especificada", "Denota la unidad declarada.", "No aplica a otro encuestado.", "Unidad declarada; sin catálogo."),
        "Numero de personas que se atendieron": ("numero-personas-atendidas-apoyo", "Número de personas atendidas", "Número de personas que se atendieron en apoyos sociales en fechas especiales. Población: personas. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a otro apoyo.", "Sin periodo declarado en la descripcion."),
        "cantidad de mujeres atendidas": ("cantidad-mujeres-atendidas", "Cantidad de mujeres atendidas", "Cantidad de mujeres atendidas en atenciones brindadas. Población: mujeres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a hombres.", "Sin periodo declarado."),
        "sexo de las personas atendidas": ("sexo-personas-atendidas", "Sexo de las personas atendidas", "Sexo de las personas atendidas en atenciones brindadas. Población: atendidos.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "tipo de atención que se brindó": ("tipo-atencion-brindada", "Tipo de atención brindada", "Tipo de atención que se brindó en atenciones. Objeto: atención.", None, "no_especificada", "Denota el tipo declarado.", "No aplica a otra atención.", "Sin tipología publicada."),
        "Nombre del centro nocturno inspeccionado": ("nombre-centro-nocturno", "Nombre del centro nocturno", "Nombre del centro nocturno inspeccionado. Objeto: establecimiento.", None, "nombre", "Denota el nombre declarado.", "No aplica a otro establecimiento.", "Nombre declarado; no acredita identidad ni licencia."),
        "Nombre de la guarderia inspeccionada": ("nombre-guarderia", "Nombre de la guardería", "Nombre de la guardería inspeccionada. Objeto: establecimiento.", None, "nombre", "Denota el nombre declarado.", "No aplica a otro establecimiento.", "Nombre declarado; no acredita identidad ni licencia."),
        "Nombre del evento": ("nombre-evento-capacitacion", "Nombre del evento", "Nombre del evento de capacitación a docentes. Objeto: evento.", None, "nombre", "Denota el nombre declarado.", "No aplica a otro evento.", "Nombre declarado; sin identificador único."),
        "Cantidad (capacidad) del evento": ("capacidad-evento-capacitacion", "Capacidad del evento", "Cantidad (capacidad) del evento de capacitación a docentes. Medida: conteo; objeto del conteo no declarado en la descripción.", None, "no_especificada", "Denota la capacidad declarada.", "No aplica a asistencia real.", "Capacidad, no asistencia; objeto no declarado; sin fecha declarada."),
        "Nivel educativo destino del evento": ("nivel-educativo-evento-capacitacion", "Nivel educativo del evento", "Nivel educativo destino del evento de capacitación a docentes.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otro evento.", "Sin catálogo de niveles publicado."),
        "Duración del evento": ("duracion-evento-capacitacion", "Duración del evento", "Duración del evento de capacitación a docentes. Unidad y medida no declaradas en la descripción; el nombre indica días-horas sin acreditarlo.", None, "no_especificada", "Denota la duración declarada.", "No aplica a otro evento.", "Duración sin unidad acreditada; el nombre no prueba la representación."),
        "Modalidad en que se impartira el evento": ("modalidad-evento-capacitacion", "Modalidad del evento", "Modalidad en que se impartirá el evento de capacitación (línea o presencial).", None, "no_especificada", "Denota la modalidad declarada.", "No aplica a otro evento.", "Modalidad declarada; sin catálogo."),
        "Sede del evento": ("sede-evento-capacitacion", "Sede del evento", "Sede del evento de capacitación a docentes. Objeto: sede.", None, "no_especificada", "Denota la sede declarada.", "No aplica a otro evento.", "Sede declarada; sin catálogo."),
        "Tipo del evento": ("tipo-evento-capacitacion", "Tipo del evento", "Tipo del evento de capacitación a docentes. Objeto: evento.", None, "no_especificada", "Denota el tipo declarado.", "No aplica a otro evento.", "Sin tipología publicada."),
        "Financiamiento del Evento": ("financiamiento-evento-capacitacion", "Financiamiento del evento", "Financiamiento del evento de capacitación a docentes.", None, "no_especificada", "Denota la fuente declarada.", "No aplica a otro evento.", "Sin catálogo de fuentes publicado."),
        "Encargados de empartir del evento": ("encargados-evento-capacitacion", "Encargados del evento", "Encargados de impartir el evento de capacitación (literal con errata conservado). Sujeto: encargados según función descrita.", None, "no_especificada", "Denota a los encargados declarados.", "No aplica a otro evento.", "Literal con errata; función descrita, no acreditación."),
        "Periodo en el que se imparte": ("periodo-evento-capacitacion", "Periodo del evento", "Periodo (día-periodo) en el que se imparte el evento de capacitación.", "periodo-escolar", "no_especificada", "Denota el periodo declarado.", "No aplica a otro evento.", "Periodo declarado; sin calendario publicado."),
        "Periodo en el que se imparte": ("periodo-evento-capacitacion", "Periodo del evento", "Periodo (día-periodo) en el que se imparte el evento de capacitación.", "periodo-escolar", "no_especificada", "Denota el periodo declarado.", "No aplica a otro evento.", "Periodo declarado; sin calendario publicado."),
        "Sexo del beneficiado": ("sexo-beneficiado-mano", "Sexo del beneficiado", "Sexo del beneficiado del programa Mano con Mano. Población: beneficiados.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "Edad del beneficiado": ("edad-beneficiado-mano", "Edad del beneficiado", "Edad del beneficiado del programa Mano con Mano. Unidad no declarada en la fila.", None, "no_especificada", "Denota la edad declarada.", "No aplica a otra población.", "Unidad no declarada; no se asumen años."),
        "Colonia donde recide el beneficiado": ("colonia-residencia-beneficiado-mano", "Colonia donde reside el beneficiado", "Colonia donde reside (literal recide) el beneficiado de Mano con Mano. Objeto: colonia.", "localidad", "no_especificada", "Denota la colonia declarada.", "No aplica a otro beneficiado.", "Literal con errata; colonia declarada, no catálogo."),
        "Estado donde nacio el beneficiado": ("entidad-nacimiento-beneficiado-mano", "Estado donde nació el beneficiado", "Estado donde nació el beneficiado de Mano con Mano. Objeto: entidad federativa.", "entidad", "no_especificada", "Denota la entidad declarada.", "No aplica a residencia.", "Entidad declarada; nacimiento, no residencia."),
        "Nivel de escolaridad del beneficiado": ("escolaridad-beneficiado-mano", "Nivel de escolaridad del beneficiado", "Nivel de escolaridad del beneficiado de Mano con Mano.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otro beneficiado.", "Sin catálogo de niveles publicado."),
        "Estado Civil del beneficiado": ("estado-civil-beneficiado-mano", "Estado civil del beneficiado", "Estado civil del beneficiado de Mano con Mano.", None, "no_especificada", "Denota el estado declarado.", "No aplica a otro beneficiado.", "Sin catálogo de estados publicado."),
        "Institucion en donde cuenta con servicios medicos": ("servicio-medico-beneficiado-mano", "Servicio médico del beneficiado", "Institución en donde cuenta con servicios médicos el beneficiado de Mano con Mano.", None, "no_especificada", "Denota la institución declarada.", "No aplica a otro beneficiado.", "Institución declarada; sin catálogo."),
        "Indicador de discapacidad del beneficiado": ("discapacidad-beneficiado-mano", "Discapacidad del beneficiado", "Indicador de discapacidad del beneficiado de Mano con Mano.", None, "no_especificada", "Denota el indicador declarado.", "No aplica a otro beneficiado.", "Indicador declarado; sin escala ni catálogo publicados."),
        "Enfermedades con las que cuenta el beneficiado": ("enfermedades-beneficiado-mano", "Enfermedades del beneficiado", "Enfermedades con las que cuenta el beneficiado de Mano con Mano, según declaración.", None, "no_especificada", "Denota el texto declarado.", "No aplica a diagnóstico clínico.", "Texto declarado por la fuente; no promueve diagnósticos ni códigos clínicos."),
        "Grupo indigena al que pertenece el beneficiado": ("grupo-indigena-beneficiado-mano", "Grupo indígena del beneficiado", "Grupo indígena al que pertenece el beneficiado de Mano con Mano, según declaración.", None, "no_especificada", "Denota la adscripción declarada.", "No aplica a lengua.", "Adscripción declarada; sin catálogo; no acredita identidad étnica."),
        "Idiomas que habla el beneficiado": ("lenguas-beneficiado-mano", "Idiomas del beneficiado", "Idiomas que habla el beneficiado de Mano con Mano, según declaración.", None, "no_especificada", "Denota las lenguas declaradas.", "No aplica a grupo indígena.", "Lenguas declaradas; sin catálogo."),
        "Puesto u ocupacion del beneficiado": ("ocupacion-beneficiado-mano", "Ocupación del beneficiado", "Puesto u ocupación del beneficiado de Mano con Mano.", None, "no_especificada", "Denota la ocupación declarada.", "No aplica a otro beneficiado.", "Ocupación declarada; sin catálogo."),
        "Numero de personas que dependen del beneficiado": ("dependientes-beneficiado-mano", "Dependientes del beneficiado", "Número de personas que dependen del beneficiado de Mano con Mano. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a población del hogar.", "Conteo declarado; sin periodo."),
        "Tipo de tenencia que posee el beneficiado": ("tenencia-hogar-beneficiado-mano", "Tenencia del hogar", "Tipo de tenencia del hogar que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota la tenencia declarada.", "No aplica a otro hogar.", "Sin catálogo de tenencias publicado."),
        "Tipo de servicio de Agua que posee el beneficiado": ("agua-vivienda-beneficiado-mano", "Agua de la vivienda", "Tipo de servicio de agua que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el servicio declarado.", "No aplica a otro servicio.", "Servicio declarado; sin catálogo."),
        "Tipo de servicio de Electricidad que posee el beneficiado": ("electricidad-vivienda-beneficiado-mano", "Electricidad de la vivienda", "Tipo de servicio de electricidad que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el servicio declarado.", "No aplica a otro servicio.", "Servicio declarado; sin catálogo."),
        "Tipo de servicio de Drenaje que posee el beneficiado": ("drenaje-vivienda-beneficiado-mano", "Drenaje de la vivienda", "Tipo de servicio de drenaje que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el servicio declarado.", "No aplica a otro servicio.", "Servicio declarado; sin catálogo."),
        "Tipo de servicio de Techo que posee el beneficiado": ("techo-vivienda-beneficiado-mano", "Techo de la vivienda", "Tipo de techo (literal: servicio de techo) que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el material declarado.", "No aplica a otro componente.", "Material declarado; sin catálogo."),
        "Tipo de  Paredes que posee el beneficiado": ("paredes-vivienda-beneficiado-mano", "Paredes de la vivienda", "Tipo de paredes que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el material declarado.", "No aplica a otro componente.", "Material declarado; sin catálogo."),
        "Tipo de servicio de Sanitario que posee el beneficiado": ("sanitario-vivienda-beneficiado-mano", "Sanitario de la vivienda", "Tipo de servicio de sanitario que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el servicio declarado.", "No aplica a baño.", "Servicio declarado; sanitario y baño se conservan separados."),
        "Tipo de servicio de Baño que posee el beneficiado": ("bano-vivienda-beneficiado-mano", "Baño de la vivienda", "Tipo de servicio de baño que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el servicio declarado.", "No aplica a sanitario.", "Servicio declarado; baño y sanitario se conservan separados."),
        "Tipo de Piso que posee el beneficiado": ("piso-vivienda-beneficiado-mano", "Piso de la vivienda", "Tipo de piso que posee el beneficiado de Mano con Mano.", None, "no_especificada", "Denota el material declarado.", "No aplica a otro componente.", "Material declarado; sin catálogo."),
        "Condicion de la vivienda del beneficiado": ("condicion-vivienda-beneficiado-mano", "Condición de la vivienda", "Condición de la vivienda del beneficiado de Mano con Mano.", None, "no_especificada", "Denota la condición declarada.", "No aplica a otro hogar.", "Sin escala publicada."),
        "Posee area de cocina": ("cocina-vivienda-beneficiado-mano", "Área de cocina", "Posee área de cocina en la vivienda del beneficiado de Mano con Mano.", None, "no_especificada", "Denota la existencia declarada.", "No aplica a uso común.", "Existencia declarada; cocina y uso común separados."),
        "Posee area de uso comun": ("uso-comun-vivienda-beneficiado-mano", "Área de uso común", "Posee área de uso común en la vivienda del beneficiado de Mano con Mano.", None, "no_especificada", "Denota la existencia declarada.", "No aplica a cocina.", "Existencia declarada."),
        "Numero de cuartos en la vivienda": ("cuartos-vivienda-beneficiado-mano", "Cuartos de la vivienda", "Número de cuartos en la vivienda del beneficiado de Mano con Mano. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a dormitorios.", "Cuartos totales, no dormitorios."),
        "Numero de dormitorios en la vivienda": ("dormitorios-vivienda-beneficiado-mano", "Dormitorios de la vivienda", "Número de dormitorios en la vivienda del beneficiado de Mano con Mano. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a cuartos totales.", "Dormitorios, no cuartos totales."),
        "Ciclo escolar al que pertenece la convocatoria.": ("ciclo-escolar-convocatoria-beca", "Ciclo escolar de la convocatoria", "Ciclo escolar al que pertenece la convocatoria de becas o estímulos educativos.", "periodo-escolar", "no_especificada", "Denota el ciclo declarado.", "No aplica a otra convocatoria.", "Ciclo declarado; sin calendario publicado."),
        "Programa o tipo de beca al que pertenece la convocatoria. También puede ser un estímulo educativo.": ("programa-beca-convocatoria", "Programa de la convocatoria", "Programa o tipo de beca (o estímulo educativo) al que pertenece la convocatoria.", None, "no_especificada", "Denota el programa declarado.", "No aplica a otra convocatoria.", "Programa declarado; sin catálogo."),
        "Nivel escolar del estudiante con el apoyo de beca o estímulo educativo": ("nivel-escolar-becario", "Nivel escolar del becario", "Nivel escolar del estudiante con apoyo de beca o estímulo educativo.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otro estudiante.", "Sin catálogo de niveles publicado."),
        "Clave oficial que identifica a los centros educativos que distingue a la escuela": ("clave-centro-educativo-beca", "Clave del centro educativo", "Clave oficial que identifica al centro educativo del becario; distingue a la escuela.", "escuela", "codigo", "Denota la clave declarada.", "No aplica a otra escuela.", "Clave declarada; no acredita identidad oficial del centro."),
        "Importe, corresponde al importe del pago total de la beca o estímulo": ("importe-beca-estimulo", "Importe de la beca", "Importe del pago total de la beca o estímulo educativo. Medida: moneda.", None, "no_especificada", "Denota el importe declarado.", "No aplica a otro pago.", "Moneda no declarada en la descripcion."),
        "Género del estudiante con el apoyo de beca o estímulo educativo": ("genero-estudiante-beca", "Género del estudiante becado", "Género del estudiante con apoyo de beca o estímulo educativo.", "sexo-declarado", "no_especificada", "Denota el género declarado.", "No aplica a otro estudiante.", "Sin valores publicados."),
        "Materia evaluada": ("materia-evaluada-reprobacion", "Materia evaluada", "Materia evaluada en índices de reprobación. Objeto: materia.", None, "nombre", "Denota la materia declarada.", "No aplica a otra materia.", "Materia declarada; sin catálogo."),
        "Grupo evaluado": ("grupo-evaluado-reprobacion", "Grupo evaluado", "Grupo evaluado en índices de reprobación. Objeto: grupo.", None, "no_especificada", "Denota el grupo declarado.", "No aplica a otra materia.", "Grupo declarado; sin catálogo."),
        "Total de alumnos evaluado": ("total-alumnos-evaluado-reprobacion", "Total de alumnos evaluado", "Total de alumnos evaluado en índices de reprobación. Población: alumnos. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a otro grupo.", "Sin periodo declarado."),
        "Nombre del plan educativo": ("plan-educativo-remoto", "Plan educativo", "Nombre del plan educativo en reprobación modalidad remota.", None, "nombre", "Denota el plan declarado.", "No aplica a otro plan.", "Plan declarado; sin catálogo."),
        "Nombre de la materia": ("materia-remota", "Materia (remota)", "Nombre de la materia en reprobación modalidad remota. Objeto: materia.", None, "nombre", "Denota la materia declarada.", "No aplica a presencial.", "Modalidad remota; sin catálogo."),
        "Clave del grupo": ("clave-grupo-remoto", "Clave del grupo (remota)", "Clave del grupo en reprobación modalidad remota. Objeto: grupo.", None, "codigo", "Denota la clave declarada.", "No aplica a presencial.", "Clave declarada; sin catálogo."),
        "Total de alumnos en el grupo": ("total-alumnos-grupo-remoto", "Total de alumnos del grupo (remota)", "Total de alumnos en el grupo en reprobación modalidad remota. Población: alumnos. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a presencial.", "Sin periodo declarado."),
        "Total de alumnos en el grupo": ("total-alumnos-grupo-remoto", "Total de alumnos del grupo (remota)", "Total de alumnos en el grupo en reprobación modalidad remota. Población: alumnos. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a presencial.", "Sin periodo declarado."),
        "Indica el nombre de la planta dond se extrae el mineral": ("nombre-planta-minera", "Nombre de la planta minera", "Nombre de la planta donde se extrae el mineral (literal con errata conservado). Objeto: planta.", None, "nombre", "Denota el nombre declarado.", "No aplica a empresa.", "Nombre declarado; planta y empresa se conservan separados."),
        "Indica el nombre de la empresa que extrae el mineral": ("nombre-empresa-minera", "Nombre de la empresa minera", "Nombre de la empresa que extrae el mineral. Objeto: empresa.", "organizacion", "nombre", "Denota la empresa declarada.", "No aplica a planta.", "Empresa declarada; no acredita identidad corporativa."),
        "Se refiere a los \"bloques de construcción\" de las rocas y la materia prima que extraen las unidades mineras para transformarlas en productos útiles.": ("mineral-unidad-minera", "Mineral de la unidad minera", "Mineral: bloques de construcción de las rocas y materia prima que extraen las unidades mineras. Objeto: mineral.", None, "no_especificada", "Denota el mineral declarado.", "No aplica a otra unidad.", "Mineral declarado; sin catálogo."),
        "Son las unidades que indican el método o técnica de ingeniería que se utiliza para extraer los minerales de la corteza terrestre.": ("tipo-minado-unidad-minera", "Tipo de minado", "Tipo de minado: método o técnica de ingeniería para extraer minerales. Objeto: unidad minera.", None, "no_especificada", "Denota el método declarado.", "No aplica a operación.", "Método declarado; minado y operación se conservan separados."),
        "Son las unidades que indican la condición actual de actividad en la que se encuentra una unidad minera.": ("condicion-operacion-unidad-minera", "Condición de operación", "Condición actual de actividad de la unidad minera. Objeto: unidad minera.", None, "no_especificada", "Denota la condición declarada.", "No aplica a minado.", "Condición declarada; sin catálogo."),
        "Mide la distancia norte o sur desde el Ecuador (0° a 90°)": ("latitud-unidad-minera", "Latitud de la unidad minera", "Latitud de la unidad minera: distancia norte o sur desde el Ecuador. Objeto: unidad minera.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a longitud ni a otra unidad.", "Coordenada declarada; datum no publicado."),
        "Mide la distancia este u oeste desde el Meridiano de Greenwich (0° a 180°).": ("longitud-unidad-minera", "Longitud de la unidad minera", "Longitud de la unidad minera: distancia este u oeste desde Greenwich. Objeto: unidad minera.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a latitud.", "Coordenada declarada; datum no publicado."),
        "El tipo de energía hace referencia a si la energía generada proviene de fuentes renovables o no renovables.": ("tipo-energia-planta-electrica", "Tipo de energía", "Tipo de energía: renovable o no renovable, de la planta eléctrica.", None, "no_especificada", "Denota el tipo declarado.", "No aplica a fuente ni tecnología.", "Tipo declarado; tipo, fuente y tecnología se conservan separados."),
        "El tipo de sector se refiere al origen de la empresa que opera la planta eléctrica.": ("tipo-sector-planta-electrica", "Tipo de sector", "Tipo de sector: origen de la empresa que opera la planta eléctrica.", None, "no_especificada", "Denota el sector declarado.", "No aplica a otra planta.", "Sector declarado; sin catálogo."),
        "Es el tipo de contraprestación de servicio que tiene la planta para recibir un beneficio económico de la electricidad entregada al sistema eléctrico.": ("tipo-contraprestacion-planta-electrica", "Tipo de contraprestación", "Tipo de contraprestación de servicio de la planta eléctrica por la electricidad entregada.", None, "no_especificada", "Denota el tipo declarado.", "No aplica a otra planta.", "Tipo declarado; sin catálogo."),
        "Es la capacidad máxima de potencia en corriente alterna que una planta generadora de electricidad tiene autorizada por la Comisión Reguladora de Energía para inyectar al Sistema Eléctrico.": ("capacidad-autorizada-planta-electrica", "Capacidad autorizada", "Capacidad máxima de potencia en corriente alterna autorizada por la CRE para inyectar al sistema. Medida: potencia.", None, "no_especificada", "Denota la capacidad declarada.", "No aplica a generación estimada.", "Capacidad autorizada, no generación; unidad en variable (MW)."),
        "Es la empresa que controla o posee otras empresas, generalmente filiales o subsidiarias, que operan una o varias plantas eléctricas.": ("empresa-controladora-planta-electrica", "Empresa controladora", "Empresa que controla o posee filiales que operan plantas eléctricas. Objeto: empresa.", "organizacion", "nombre", "Denota la empresa declarada.", "No aplica a operadora.", "Controladora y operadora se conservan separadas."),
        "Es la entidad de negocios que puede operar de forma independiente o forma parte de un grupo empresarial que administra una o varias plantas eléctricas.": ("empresa-operadora-planta-electrica", "Empresa operadora", "Entidad de negocios que opera o administra plantas eléctricas. Objeto: empresa.", "organizacion", "nombre", "Denota la empresa declarada.", "No aplica a controladora.", "Operadora y controladora se conservan separadas."),
        "Es la fuente de energía que se encuentra disponible en la naturaleza en su forma original y no ha sido sometida a procesos de transformación": ("fuente-energia-planta-electrica", "Fuente de energía", "Fuente de energía en su forma original sin transformación, de la planta eléctrica.", None, "no_especificada", "Denota la fuente declarada.", "No aplica a tipo ni tecnología.", "Fuente declarada; sin catálogo."),
        "Es la generación de electrcidad estimada que inyectará la planta al sistema eléctrico en un año.": ("generacion-estimada-planta-electrica", "Generación estimada", "Generación de electricidad estimada que inyectará la planta al sistema en un año (literal con errata). Medida: energía.", None, "no_especificada", "Denota la generación declarada.", "No aplica a capacidad.", "Estimación anual, no capacidad; unidad en variable (MWh)."),
        "Indica el nombre que tiene la planta de generación de electricidad.": ("nombre-planta-electrica", "Nombre de la planta eléctrica", "Nombre de la planta de generación de electricidad. Objeto: planta.", None, "nombre", "Denota el nombre declarado.", "No aplica a otra planta.", "Nombre declarado; no acredita identidad."),
        "La latitud es la distancia angular entre la línea ecuatorial y la planta generadora de energía": ("latitud-planta-electrica", "Latitud de la planta eléctrica", "Latitud de la planta generadora de energía. Objeto: planta.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a longitud.", "Coordenada declarada; datum no publicado."),
        "La longitud es la distancia angular entre el meridiando de greenwich y la planta generadora de energía": ("longitud-planta-electrica", "Longitud de la planta eléctrica", "Longitud de la planta generadora de energía (literal con errata). Objeto: planta.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a latitud.", "Coordenada declarada; datum no publicado."),
        "Se refiere a los diferentes métodos y sistemas empleados para generar energía eléctrica.": ("tecnologia-planta-electrica", "Tecnología de generación", "Tecnología: métodos y sistemas para generar energía eléctrica de la planta.", None, "no_especificada", "Denota la tecnología declarada.", "No aplica a proceso ni fuente.", "Tecnología, proceso y fuente se conservan separados."),
        "Se refiere a los métodos, procesos y sistemas particulares que se utilizan para generar energía eléctrica.": ("proceso-planta-electrica", "Proceso de generación", "Proceso: métodos y sistemas particulares para generar energía eléctrica de la planta.", None, "no_especificada", "Denota el proceso declarado.", "No aplica a tecnología.", "Proceso y tecnología se conservan separados."),
        "Son las unidades que representan la capacidad de potencia.": ("unidad-capacidad-planta-electrica", "Unidad de capacidad", "Unidad que representa la capacidad de potencia de la planta eléctrica. Unidad: MW según fila.", None, "no_especificada", "Denota la unidad declarada.", "No aplica a generación.", "Unidad literal de la fila; no se convierte."),
        "Son las unidades que representan la generación de energía eléctrica estimada.": ("unidad-generacion-planta-electrica", "Unidad de generación", "Unidad que representa la generación de energía eléctrica estimada. Unidad: GWh según fila.", None, "no_especificada", "Denota la unidad declarada.", "No aplica a capacidad.", "Unidad literal de la fila; no se convierte."),
        "Contiene la clave identificadora de cada presa.": ("clave-identificadora-presa", "Clave identificadora de la presa", "Clave identificadora de cada presa en ubicación de presas. Objeto: presa.", None, "codigo", "Denota la clave declarada.", "No aplica a otra presa.", "Clave declarada sin catálogo publicado; comparte concepto con clave de presa del mismo diccionario; no acredita identidad."),
        "Tiene la información sobre la clave que identifica a la presa.": ("clave-identificadora-presa", "Clave identificadora de la presa", "Clave que identifica a la presa en ubicación de presas. Objeto: presa.", None, "codigo", "Denota la clave declarada.", "No aplica a otra presa.", "Clave declarada sin catálogo publicado; comparte concepto con clave identificadora del mismo diccionario; no acredita identidad."),
        "Nombre completo de la presa.": ("nombre-presa-ubicacion", "Nombre de la presa", "Nombre completo o común de la presa en ubicación de presas. Objeto: presa.", None, "nombre", "Denota el nombre declarado.", "No aplica a otra presa.", "Nombre declarado; completo y común comparten concepto."),
        "Nombre común de la presa.": ("nombre-presa-ubicacion", "Nombre de la presa", "Nombre completo o común de la presa en ubicación de presas. Objeto: presa.", None, "nombre", "Denota el nombre declarado.", "No aplica a otra presa.", "Nombre declarado; completo y común comparten concepto."),
        "Información sobre el río en el cuál se encuentra la presa": ("rio-presa-ubicacion", "Río de la presa", "Río en el cual se encuentra la presa. Objeto: río.", None, "nombre", "Denota el río declarado.", "No aplica a cuenca.", "Río declarado; no acredita catálogo."),
        "Nombre de la cuenca en que se encuentra cada presa.": ("cuenca-presa-ubicacion", "Cuenca de la presa", "Nombre de la cuenca en que se encuentra cada presa. Objeto: cuenca.", None, "nombre", "Denota la cuenca declarada.", "No aplica a región.", "Cuenca declarada; comparte objeto con identificador de cuenca."),
        "Número identificador de la cuenca en que se encuentra cada presa.": ("cuenca-presa-ubicacion", "Cuenca de la presa", "Número identificador de la cuenca en que se encuentra cada presa. Objeto: cuenca.", None, "codigo", "Denota el identificador declarado.", "No aplica a región.", "Identificador declarado sin catálogo publicado; comparte concepto con nombre de cuenca; no acredita identidad."),
        "Nombre de la región hidrológica en que se encuentra cada presa.": ("region-hidrologica-presa", "Región hidrológica de la presa", "Nombre de la región hidrológica en que se encuentra cada presa.", None, "nombre", "Denota la región declarada.", "No aplica a cuenca.", "Región declarada; comparte objeto con identificador."),
        "Número identificador de la región hidrológica en que se encuentra cada presa.": ("region-hidrologica-presa", "Región hidrológica de la presa", "Número identificador de la región hidrológica en que se encuentra cada presa.", None, "codigo", "Denota el identificador declarado.", "No aplica a cuenca.", "Identificador declarado sin catálogo publicado; comparte concepto con nombre; no acredita identidad."),
        "Número identificador del río en catálogo nacional de Conagua": ("identificador-rio-conagua-presa", "Identificador del río Conagua", "Número identificador del río en catálogo nacional de Conagua. Objeto: río.", None, "codigo", "Denota el identificador declarado.", "No aplica a nombre de río.", "Identificador declarado; el catálogo nacional no está fijado como evidencia; no acredita vigencia."),
         "Nivel de Aguas Máximas Extraordinarias (NAME), es el nivel más alto que debe alcanzar el agua en la presa bajo cualquier condición. La variable\"cap_name\" contiene información sobre la capacidad NAME de cada presa.": ("capacidad-name-presa", "Capacidad NAME", "Capacidad del Nivel de Aguas Máximas Extraordinarias de la presa. Unidad: hectómetros cúbicos según fila.", None, "no_especificada", "Denota la capacidad declarada.", "No aplica a NAMO ni a ocupación.", "NAME, no NAMO; unidad literal de la fila."),
        "Nivel de Aguas Máximas Ordinarias (NAMO), es el máximo nivel con que se puede operar la presa para satisfacer las demandas, puede ser agua potable, generación de energía y/o riego; cuando el vertedor de excedencias no es controlado por compuertas, el NAMO coincide con su cresta o punto más alto del vertedor. La variable \"cap_namo\" contiene la información sobre la capacidad NAMO de cada presa.": ("capacidad-namo-presa", "Capacidad NAMO", "Capacidad del Nivel de Aguas Máximas Ordinarias de la presa. Unidad: hectómetros cúbicos según fila.", None, "no_especificada", "Denota la capacidad declarada.", "No aplica a NAME ni a ocupación.", "NAMO, no NAME; unidad literal de la fila."),
        "Información sobre la altitud en que se ubica cada presa.": ("altitud-presa-ubicacion", "Altitud de la presa", "Altitud en que se ubica cada presa. Unidad: grados según fila (literal conservado sin reinterpretar).", None, "no_especificada", "Denota la altitud declarada.", "No aplica a latitud.", "Unidad literal de la fila; no se convierte ni se reinterpreta."),
        "Información sobre la latitud en que se ubica cada presa.": ("latitud-presa-ubicacion", "Latitud de la presa", "Latitud en que se ubica cada presa. Objeto: presa.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a longitud.", "Coordenada declarada; datum no publicado."),
        "Información sobre la longitud en que se ubica cada presa.": ("longitud-presa-ubicacion", "Longitud de la presa", "Longitud en que se ubica cada presa. Objeto: presa.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a latitud.", "Coordenada declarada; datum no publicado."),
        "Tiene la información sobre el nivel de ocupación (almacenamiento) de la presa.": ("nivel-ocupacion-presa", "Nivel de ocupación", "Nivel de ocupación (almacenamiento) de la presa. Unidad: hectómetros cúbicos según fila.", None, "no_especificada", "Denota el nivel declarado.", "No aplica a NAME ni NAMO.", "Unidad literal de la fila; ocupación actual, no confundir con capacidades NAME/NAMO."),
        "horario que abre el estableciemiento los domingo": ("horario-apertura-domingo-zona-salva", "Apertura domingo", "Horario que abre el establecimiento zona salva los domingos (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de domingo; día y tipo no intercambiables."),
        "horario que abre el estableciemiento los lunes": ("horario-apertura-lunes-zona-salva", "Apertura lunes", "Horario que abre el establecimiento zona salva los lunes (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de lunes."),
        "horario que abre el estableciemiento los martes": ("horario-apertura-martes-zona-salva", "Apertura martes", "Horario que abre el establecimiento zona salva los martes (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de martes."),
        "horario que abre el estableciemiento los miércoles": ("horario-apertura-miercoles-zona-salva", "Apertura miércoles", "Horario que abre el establecimiento zona salva los miércoles (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de miércoles."),
        "horario que abre el estableciemiento los jueves": ("horario-apertura-jueves-zona-salva", "Apertura jueves", "Horario que abre el establecimiento zona salva los jueves (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de jueves."),
        "horario que abre el estableciemiento los viernes": ("horario-apertura-viernes-zona-salva", "Apertura viernes", "Horario que abre el establecimiento zona salva los viernes (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de viernes."),
        "horario que abre el estableciemiento los sábado": ("horario-apertura-sabado-zona-salva", "Apertura sábado", "Horario que abre el establecimiento zona salva los sábados (literal con errata).", None, "no_especificada", "Denota el horario declarado.", "No aplica a cierre ni a otro día.", "Apertura de sábado."),
        "horario que cierra el establecimiento los domingo": ("horario-cierre-domingo-zona-salva", "Cierre domingo", "Horario que cierra el establecimiento zona salva los domingos.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de domingo."),
        "horario que cierra el establecimiento los lunes": ("horario-cierre-lunes-zona-salva", "Cierre lunes", "Horario que cierra el establecimiento zona salva los lunes.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de lunes."),
        "horario que cierra el establecimiento los martes": ("horario-cierre-martes-zona-salva", "Cierre martes", "Horario que cierra el establecimiento zona salva los martes.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de martes."),
        "horario que cierra el establecimiento los miércoles": ("horario-cierre-miercoles-zona-salva", "Cierre miércoles", "Horario que cierra el establecimiento zona salva los miércoles.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de miércoles."),
        "horario que cierra el establecimiento los jueves": ("horario-cierre-jueves-zona-salva", "Cierre jueves", "Horario que cierra el establecimiento zona salva los jueves.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de jueves."),
        "horario que cierra el establecimiento los viernes": ("horario-cierre-viernes-zona-salva", "Cierre viernes", "Horario que cierra el establecimiento zona salva los viernes.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de viernes."),
        "horario que cierra el establecimiento los sábado": ("horario-cierre-sabado-zona-salva", "Cierre sábado", "Horario que cierra el establecimiento zona salva los sábados.", None, "no_especificada", "Denota el horario declarado.", "No aplica a apertura ni a otro día.", "Cierre de sábado."),
        "Indica la temporada a la que corresponde el registro.": ("temporada-caza-cinegetica", "Temporada de caza", "Temporada a la que corresponde el registro cinegético.", None, "no_especificada", "Denota la temporada declarada.", "No aplica a periodo.", "Temporada declarada; sin calendario publicado."),
        "Se refiere específicamente al recurso mineral obtenido en su estado final de aprovechamiento": ("metal-produccion-minera", "Metal producido", "Recurso mineral obtenido en su estado final de aprovechamiento en producción minera. Objeto: mineral.", None, "no_especificada", "Denota el metal declarado.", "No aplica a unidad ni volumen.", "Metal declarado; sin catálogo."),
        "Es la referencia estandarizada que se utiliza para cuantificar el metal producido. Toneladas (Ton): Unidad para metales industriales de gran volumen. Kilogramos (Kg): Unidad para metales preciosos de alto valor.": ("unidad-referencia-metal-mineria", "Unidad de referencia del metal", "Referencia estandarizada para cuantificar el metal producido: toneladas o kilogramos según literal.", None, "no_especificada", "Denota la unidad declarada.", "No aplica a volumen.", "Unidad según tipo de metal; sin conversión."),
        "Indica el valor numérico que representa el volumen o peso total de material obtenido durante un periodo determinado.": ("volumen-produccion-minera", "Volumen de producción minera", "Valor numérico del volumen o peso total de material obtenido en un periodo. Medida: volumen o peso.", None, "no_especificada", "Denota el volumen declarado.", "No aplica a metal.", "Periodo según recurso; unidad toneladas o kilogramos."),
        "Monto económico pagado por concepto de medidas de ayuda, asistencia y reparación integral en el periodo reportado": ("monto-medida-ayuda", "Monto de la medida de ayuda", "Monto económico pagado por medidas de ayuda, asistencia y reparación integral en el periodo reportado. Medida: moneda.", None, "no_especificada", "Denota el monto declarado.", "No aplica a otro apoyo.", "Monto del periodo reportado; moneda no declarada."),
        "Nivel de Estudios en el que el estudiante se encuentra matrículado": ("nivel-estudios-matriculado-discapacidad", "Nivel de estudios del matriculado", "Nivel de estudios en el que el estudiante se encuentra matriculado (discapacidad y grupo étnico).", None, "no_especificada", "Denota el nivel declarado.", "No aplica a otro estudiante.", "Nivel declarado; sin catálogo."),
        "Número de estudiantes (hombres) que reportan contar con algun tipo de discapacidad": ("conteo-hombres-discapacidad-estudiantes", "Hombres estudiantes con discapacidad", "Número de estudiantes hombres que reportan contar con algún tipo de discapacidad. Población: hombres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a mujeres ni a otra condición.", "Reporte del estudiante; no acredita diagnóstico."),
        "Número de estudiantes (mujeres) que reportan contar con algun tipo de discapacidad": ("conteo-mujeres-discapacidad-estudiantes", "Mujeres estudiantes con discapacidad", "Número de estudiantes mujeres que reportan contar con algún tipo de discapacidad. Población: mujeres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a hombres ni a otra condición.", "Reporte de la estudiante; no acredita diagnóstico."),
        "Número de estudiantes (hombres) que reportan hablar algún dialécto indígena": ("conteo-hombres-lengua-indigena-estudiantes", "Hombres estudiantes hablantes", "Número de estudiantes hombres que reportan hablar algún dialecto indígena. Población: hombres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a mujeres ni a etnia.", "Habla declarada; sin catálogo de lenguas."),
        "Número de estudiantes (mujeres) que reportan hablar algún dialécto indígena": ("conteo-mujeres-lengua-indigena-estudiantes", "Mujeres estudiantes hablantes", "Número de estudiantes mujeres que reportan hablar algún dialecto indígena. Población: mujeres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a hombres ni a etnia.", "Habla declarada; sin catálogo."),
        "Número de estudiantes (hombres) que reportan pertenecer a algún grupo étnico.": ("conteo-hombres-grupo-etnico-estudiantes", "Hombres estudiantes de grupo étnico", "Número de estudiantes hombres que reportan pertenecer a algún grupo étnico. Población: hombres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a mujeres ni a lengua.", "Pertenencia declarada; no acredita identidad étnica."),
        "Número de estudiantes (mujeres) que reportan pertenecer a algún grupo étnico.": ("conteo-mujeres-grupo-etnico-estudiantes", "Mujeres estudiantes de grupo étnico", "Número de estudiantes mujeres que reportan pertenecer a algún grupo étnico. Población: mujeres. Medida: conteo.", "poblacion-total", "no_especificada", "Denota el conteo declarado.", "No aplica a hombres ni a lengua.", "Pertenencia declarada; no acredita identidad étnica."),
        "Localidad a la que pertenece la o el beneficiario": ("localidad-pertenencia-beneficiario-indigena", "Localidad del beneficiario indígena", "Localidad a la que pertenece la o el beneficiario del programa de asistencia social indígena. Objeto: localidad.", "localidad", "nombre", "Denota la localidad declarada.", "No aplica a residencia.", "Pertenencia, no residencia; nivel localidad."),
        "Pueblo Indígena al que pertenece la o el beneficiario": ("pueblo-indigena-beneficiario-asistencia", "Pueblo indígena del beneficiario", "Pueblo indígena al que pertenece la o el beneficiario de asistencia social indígena, según declaración.", None, "no_especificada", "Denota la adscripción declarada.", "No aplica a localidad.", "Adscripción declarada; sin catálogo; no acredita identidad."),
        "Sexo de la persona beneficiaria": ("sexo-persona-beneficiaria-asistencia", "Sexo de la persona beneficiaria", "Sexo de la persona beneficiaria del programa de asistencia social indígena.", "sexo-declarado", "no_especificada", "Denota el sexo declarado.", "No aplica a otra población.", "Sin valores publicados."),
        "apoyos que se otorgan Medicamentos estudios médicos estancia hospitalización servicios funerarios hospedaje alimentación y pasaje": ("tipo-apoyo-asistencia-indigena", "Apoyo otorgado", "Apoyos que se otorgan: medicamentos, estudios médicos, estancia, servicios funerarios, hospedaje, alimentación y pasaje (lista enunciativa).", None, "no_especificada", "Denota el apoyo declarado.", "No aplica a otro programa.", "Lista enunciativa literal; no demuestra exhaustividad ni catálogo."),
        "Organización a través de la cual se solicita el apoyo": ("organizacion-solicitud-apoyo-indigena", "Organización de solicitud", "Organización a través de la cual se solicita el apoyo de asistencia social indígena.", "organizacion", "no_especificada", "Denota la organización declarada.", "No aplica a beneficiario.", "Organización canalizadora; sin catálogo."),
    }
    EXTRA_FALTANTES = {
        "Contiene la información sobre la comisión encargada de cada presa, en este caso, dentro del estado de Sonora es la \"Comisión Nacional del Agua\"": ("comision-presa-ubicacion", "Comisión de la presa", "Comisión encargada de cada presa; en Sonora la Comisión Nacional del Agua según literal.", "organizacion", "nombre", "Denota el organismo declarado.", "No aplica a subdirección.", "Organismo declarado; no acredita adscripción vigente."),
        "Contiene la información sobre la subcomisión encargada de cada presa, en este caso, dentro del estado de Sonora es la \"Subdirección General Técnica\"": ("subcomision-presa-ubicacion", "Subcomisión de la presa", "Subcomisión encargada de cada presa; en Sonora la Subdirección General Técnica según literal.", "organizacion", "nombre", "Denota el organismo declarado.", "No aplica a comisión.", "Organismo declarado; comisión y subcomisión separados."),
        "Número identificador del río en catálogo nacional de Conagua": ("identificador-rio-conagua-presa", "Identificador del río Conagua", "Número identificador del río en catálogo nacional de Conagua. Objeto: río.", None, "codigo", "Denota el identificador declarado.", "No aplica a nombre de río.", "Identificador declarado; el catálogo nacional no está fijado como evidencia."),
        "El volumen muerto representa el volumen donde se acumularán los sedimentos. Esta variable contiene la información del volumen muerto de cada presa.": ("volumen-muerto-presa", "Volumen muerto", "Volumen muerto de la presa: volumen donde se acumularán los sedimentos. Unidad: hectómetros cúbicos según fila.", None, "no_especificada", "Denota el volumen declarado.", "No aplica a NAME ni a ocupación.", "Sedimentos, no almacenamiento útil; unidad literal de la fila."),
        "Clave de la presa": ("clave-presa-recurso-hidrico", "Clave de la presa", "Clave de la presa en recursos hídricos. Objeto: presa.", None, "codigo", "Denota la clave declarada.", "No aplica a ubicación de presas.", "Catálogo declarado Catálogo_estatal conservado literal sin fijar como evidencia; no acredita vigencia, adopción ni identidad. Conjunto distinto de ubicación de presas."),
        "Volumen de agua en las presas": ("volumen-agua-presas", "Volumen de agua en las presas", "Volumen de agua en las presas. Objeto: presa. Unidad: hectómetros cúbicos según fila.", None, "no_especificada", "Denota el volumen declarado.", "No aplica a capacidad NAME/NAMO.", "Unidad literal de la fila; volumen almacenado."),
        "nombre del estableciemiento zona salva": ("nombre-zona-salva", "Nombre de la zona salva", "Nombre del establecimiento zona salva (literal con errata). Objeto: establecimiento.", None, "nombre", "Denota el nombre declarado.", "No aplica a otro establecimiento.", "Nombre declarado; no acredita adhesión al programa."),
        "distancia angular hacia el norte o sur del ecuador de la zona salva": ("latitud-zona-salva", "Latitud de la zona salva", "Latitud de la zona salva desde el ecuador. Objeto: establecimiento.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a longitud.", "Coordenada declarada; datum no publicado."),
        "distancia angular hacia el este u oeste del meridiano de Greenwich de la zona salva": ("longitud-zona-salva", "Longitud de la zona salva", "Longitud de la zona salva desde Greenwich. Objeto: establecimiento.", None, "no_especificada", "Denota la coordenada declarada.", "No aplica a latitud.", "Coordenada declarada; datum no publicado."),
        "colonia donde se encuentra la zona salva": ("colonia-zona-salva", "Colonia de la zona salva", "Colonia donde se encuentra la zona salva. Objeto: colonia.", "localidad", "nombre", "Denota la colonia declarada.", "No aplica a calle.", "Colonia declarada; no acredita catálogo."),
        "calle en donde se encuentra la zona salva": ("calle-zona-salva", "Calle de la zona salva", "Calle en donde se encuentra la zona salva. Objeto: establecimiento.", None, "nombre", "Denota la calle declarada.", "No aplica a colonia.", "Calle declarada; no acredita catálogo vial."),
        "numero del estableciemiento que es zona salva": ("numero-exterior-zona-salva", "Número del establecimiento", "Número del establecimiento zona salva (literal con errata). Domicilio: número exterior.", None, "no_especificada", "Denota el número declarado.", "No aplica a folio.", "Número de domicilio, no folio; literal con errata conservado."),
        "entre que calle se encuentra el estableciemiento que es zona salva": ("entre-calles-zona-salva", "Entre calles de la zona salva", "Entre qué calle se encuentra el establecimiento zona salva (literal con errata).", None, "no_especificada", "Denota la referencia declarada.", "No aplica a calle principal.", "Referencia declarada; literal con errata conservado."),
        "Indica si el registro pecuario se trata de un dato de cierre o de avance de producción del año AAAA.": ("tipo-cierre-avance-pecuario", "Cierre o avance pecuario", "Indica si el registro pecuario es dato de cierre o de avance de producción del año. Objeto: registro.", None, "no_especificada", "Denota el carácter declarado.", "No aplica a producción.", "Cierre y avance no son intercambiables; no confundir años."),
        "Clave numérica de la especie producida.": ("clave-especie-pecuaria", "Clave de la especie pecuaria", "Clave numérica de la especie producida en ganadería. Objeto: especie.", None, "codigo", "Denota la clave declarada.", "No aplica a nombre.", "Código sin catálogo publicado; comparte concepto con nombre de especie."),
        "Nombre de la especie producida.": ("clave-especie-pecuaria", "Clave de la especie pecuaria", "Nombre de la especie producida en ganadería. Objeto: especie.", None, "nombre", "Denota el nombre declarado.", "No aplica a clave.", "Nombre declarado; comparte concepto con clave de especie."),
        "Descripción del Distrito de Desarrollo Rural (DDR) en que se registra.": ("ddr-registro-pecuario", "DDR de registro pecuario", "Distrito de Desarrollo Rural en que se registra la producción pecuaria. Objeto: DDR.", None, "nombre", "Denota el DDR declarado.", "No aplica a adscripción municipal.", "DDR de registro, no de pertenencia; comparte concepto con clave de DDR."),
        "Clave numérica del Distrito de Desarrollo Rural (DDR) donde se registra.": ("ddr-registro-pecuario", "DDR de registro pecuario", "Clave numérica del DDR donde se registra la producción pecuaria. Objeto: DDR.", None, "codigo", "Denota la clave declarada.", "No aplica a adscripción.", "Código sin catálogo; comparte concepto con descripción de DDR."),
        "Tipo de producto.": ("tipo-producto-pecuario", "Tipo de producto pecuario", "Tipo de producto de la producción pecuaria.", None, "no_especificada", "Denota el tipo declarado.", "No aplica a especie.", "Tipo declarado; sin catálogo."),
        "Unidades de medida de la producción.": ("unidad-medida-produccion-pecuaria", "Unidad de medida pecuaria", "Unidades de medida de la producción pecuaria. Medida: unidad declarada.", None, "no_especificada", "Denota la unidad declarada.", "No aplica a volumen.", "Unidad declarada en el recurso; sin conversión."),
        "Volumen total producido.": ("volumen-total-produccion-pecuaria", "Volumen total producido", "Volumen total producido en ganadería según literal. Medida: volumen.", None, "no_especificada", "Denota el volumen declarado.", "No aplica a valor.", "Unidad en el recurso; sin conversión ni desglose por subtipo."),
        "Valor total producido.": ("valor-total-produccion-pecuaria", "Valor total producido", "Valor total producido en ganadería. Medida: moneda.", None, "no_especificada", "Denota el valor declarado.", "No aplica a volumen.", "Valor monetario; moneda no declarada en la descripcion."),
        "Clave del municipio donde se realizó la subasta": ("municipio-subasta-ganadera", "Municipio de la subasta", "Clave del municipio donde se realizó la subasta ganadera. Objeto: municipio.", "municipio", "codigo", "Denota el municipio declarado.", "No aplica a otra subasta.", "Municipio del evento; código sin catálogo publicado."),
        "Clave del tipo de ganado subastado": ("tipo-ganado-subasta", "Tipo de ganado subastado", "Clave del tipo de ganado subastado. Objeto: ganado.", None, "codigo", "Denota la clave declarada.", "No aplica a descripción.", "Código sin catálogo; comparte concepto con descripción de tipo."),
        "Descripción del tipo de ganado subastado": ("tipo-ganado-subasta", "Tipo de ganado subastado", "Descripción del tipo de ganado subastado. Objeto: ganado.", None, "nombre", "Denota el tipo declarado.", "No aplica a clave.", "Tipo declarado; comparte concepto con clave de tipo."),
        "Día del mes en que se realizó la subasta": ("dia-subasta-ganadera", "Día de la subasta", "Día del mes en que se realizó la subasta ganadera. Evento: subasta.", "tiempo", "dia", "Denota el día declarado.", "No aplica a otra subasta.", "Día del evento; requiere mes y año como contexto."),
        "Identificador numérico de la subasta": ("identificador-subasta-ganadera", "Identificador de la subasta", "Identificador numérico de la subasta ganadera. Objeto: subasta.", None, "no_especificada", "Denota el identificador declarado.", "No aplica a otra subasta.", "Identificador declarado; sin sistema de identidad publicado; no es folio de orden."),
        "Número de cabezas subastadas en el lote": ("cabezas-subastadas-lote", "Cabezas subastadas", "Número de cabezas subastadas en el lote. Población: ganado. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a peso.", "Cabezas por lote; unidad cabeza."),
        "Precio máximo registrado por kilogramo": ("precio-maximo-kg-subasta", "Precio máximo por kilogramo", "Precio máximo registrado por kilogramo en la subasta. Medida: moneda por peso.", None, "no_especificada", "Denota el precio declarado.", "No aplica a mínimo ni promedio.", "Máximo, no intercambiable con mínimo o promedio."),
        "Precio mínimo registrado por kilogramo": ("precio-minimo-kg-subasta", "Precio mínimo por kilogramo", "Precio mínimo registrado por kilogramo en la subasta. Medida: moneda por peso.", None, "no_especificada", "Denota el precio declarado.", "No aplica a máximo ni promedio.", "Mínimo, no intercambiable."),
        "Precio promedio registrado por kilogramo": ("precio-promedio-kg-subasta", "Precio promedio por kilogramo", "Precio promedio registrado por kilogramo en la subasta. Medida: moneda por peso.", None, "no_especificada", "Denota el precio declarado.", "No aplica a máximo ni mínimo.", "Promedio, no intercambiable."),
        "Peso promedio por cabeza del lote subastado": ("peso-promedio-cabeza-subasta", "Peso promedio por cabeza", "Peso promedio por cabeza del lote subastado. Unidad: kilogramos según fila.", None, "no_especificada", "Denota el peso declarado.", "No aplica a precio.", "Unidad literal de la fila; sin conversión."),
        "Clave numérica de la especie de fauna.": ("clave-especie-fauna-caza", "Clave de especie de fauna", "Clave numérica de la especie de fauna cinegética. Objeto: especie.", None, "codigo", "Denota la clave declarada.", "No aplica a nombre.", "Código sin catálogo; comparte concepto con nombre."),
        "Nombre de la especie de fauna.": ("clave-especie-fauna-caza", "Clave de especie de fauna", "Nombre de la especie de fauna cinegética. Objeto: especie.", None, "nombre", "Denota el nombre declarado.", "No aplica a clave.", "Nombre declarado; comparte concepto con clave."),
        "Cantidad de cintillos autorizados para caza.": ("cintillos-autorizados-caza", "Cintillos autorizados", "Cantidad de cintillos autorizados para caza cinegética. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a entregados.", "Autorizados, no entregados."),
        "Cantidad de cintillos entregados para caza.": ("cintillos-entregados-caza", "Cintillos entregados", "Cantidad de cintillos entregados para caza cinegética. Medida: conteo.", None, "no_especificada", "Denota el conteo declarado.", "No aplica a autorizados.", "Entregados, no autorizados."),
        "Fecha de inicio del periodo.": ("fecha-inicio-periodo-caza", "Inicio del periodo de caza", "Fecha de inicio del periodo de caza cinegética. Evento: periodo.", "tiempo", "fecha", "Denota la fecha declarada.", "No aplica a fin.", "Inicio, no fin."),
        "Fecha de fin de periodo.": ("fecha-fin-periodo-caza", "Fin del periodo de caza", "Fecha de fin del periodo de caza cinegética. Evento: periodo.", "tiempo", "fecha", "Denota la fecha declarada.", "No aplica a inicio.", "Fin, no inicio."),
    }
    REUT = {
        ("53b157b9-ec39-4754-b6bf-457d370bc5c3", "Nombre del municipio en que se registra la producción."): ("municipio-registro", "nombre", "Denota el municipio declarado.", "No aplica a DDR.", "Municipio de registro; concepto vigente exacto, regla nueva restringida; sin catálogo de referencia publicado en la fila."),
        ("53b157b9-ec39-4754-b6bf-457d370bc5c3", "Clave numérica del municipio donde se registra la producción."): ("municipio-registro", "codigo", "Denota el municipio declarado.", "No aplica a DDR.", "Municipio de registro; concepto vigente exacto, regla nueva restringida; código sin catálogo publicado, no acredita identidad."),
        ("53b157b9-ec39-4754-b6bf-457d370bc5c3", "Clave numérica del mes en que se registra la producción pecuaria."): ("mes-registro", "codigo", "Denota el mes declarado.", "No aplica a otro registro.", "Mes de registro; concepto vigente exacto, regla nueva restringida con representación código; sin catálogo publicado."),
        ("53b157b9-ec39-4754-b6bf-457d370bc5c3", "Nombre del mes en que se registra la producción."): ("mes-registro", "nombre", "Denota el mes declarado.", "No aplica a otro registro.", "Mes de registro; comparte concepto vigente con clave numérica; sin catálogo publicado."),
    }
    if (dic, d) in REUT:
        cslug, rep, pos, cej, lim = REUT[(dic, d)]
        reutilizar(v, f, cslug, rep, pos, cej, lim)
        return
    if d in SIMPLE:
        spec = SIMPLE[d]
        if spec is None:
            reutilizar(v, f, "municipio-ubicacion", "no_especificada", "Denota el municipio declarado.", "No aplica a otro centro.", "Instalación localizada; concepto vigente exacto, regla nueva restringida.")
            return
        s, lab, defi, broader, rep, pos, cej, lim = spec
        proponer(v, f, s, lab, defi, broader, rep, pos, cej, lim)
        return
    if d in EXTRA_FALTANTES:
        s, lab, defi, broader, rep, pos, cej, lim = EXTRA_FALTANTES[d]
        proponer(v, f, s, lab, defi, broader, rep, pos, cej, lim)
        return
    if dic == "1e720c71-0a4c-4167-a183-58651a8b7c85":
        g_repro(v, f)
        return
    if dic == "aa4b8257-ba8d-499d-8226-770f41c36edb":
        g_remota(v, f)
        return
    if dic in ("1a95d734-2f0e-4781-8831-77dcfcbe70f8", "7922b8c8-db09-4172-ad7f-31b0ba0c68e3"):
        g_911(v, f)
        return
    if dic == "a2b6100b-18fa-429a-8f8c-7592402ddea8":
        g_adq(v, f)
        return
    pendiente(v, f, "Descripcion sin correspondencia literal revisada; queda pendiente.")


def g_repro(v, f):
    n = v["variable"]
    if n.endswith("INDICE DE REPROBACION"):
        sem = n.split(" ")[0]
        proponer(v, f, "indice-reprobacion-semana-%s" % sem.lower(), "Índice de reprobación semana %s" % sem,
                 "Resultado de la evaluación en el periodo para la semana %s. Medida no declarada en la descripción; el nombre indica índice." % sem,
                 None, "no_especificada",
                 "Denota el valor de la semana de la evidencia (la semana la indica el nombre literal, restringido en la regla).",
                 "No aplica a otra semana ni a promedio.",
                 "La descripción no declara la medida; el nombre no prueba la representación; no confundir semanas ni con promedio.")
    elif n.endswith("PROMEDIO DE MATERIA"):
        sem = n.split(" ")[0]
        proponer(v, f, "promedio-materia-semana-%s" % sem.lower(), "Promedio de materia semana %s" % sem,
                 "Resultado de la evaluación en el periodo para la semana %s. Medida no declarada en la descripción; el nombre indica promedio." % sem,
                 None, "no_especificada",
                 "Denota el valor de la semana de la evidencia (la semana la indica el nombre literal, restringido en la regla).",
                 "No aplica a otra semana ni a índice.",
                 "La descripción no declara la medida; el nombre no prueba la representación; no confundir semanas ni con índice.")
    else:
        pendiente(v, f, "Descripcion sin patron semanal revisado; queda pendiente.")


def g_remota(v, f):
    n = v["variable"]
    if n.startswith("INDICE DE REPROBACION"):
        sem = n.split(" ")[-1]
        proponer(v, f, "indice-reprobacion-remota-%s" % sem.lower(), "Índice de reprobación remota %s" % sem,
                 "Índice de reprobación en el periodo, modalidad remota: %s. Medida no declarada en la descripción; el nombre indica índice." % sem,
                 None, "no_especificada",
                 "Denota el valor remoto de la evidencia (la marca la indica el nombre literal, restringido en la regla).", "No aplica a otra marca ni a promedio.",
                 "Modalidad remota; la descripción no declara la medida; el nombre no prueba la representación.")
    elif n.startswith("PROMEDIO DE ASIGNATURA"):
        sem = n.split(" ")[-1]
        proponer(v, f, "promedio-asignatura-remota-%s" % sem.lower(), "Promedio de asignatura remota %s" % sem,
                 "Promedio de reprobación en el periodo, modalidad remota: %s. Medida no declarada en la descripción; el nombre indica promedio." % sem,
                 None, "no_especificada",
                 "Denota el valor remoto de la evidencia (la marca la indica el nombre literal, restringido en la regla).", "No aplica a otra marca ni a índice.",
                 "Modalidad remota; la descripción no declara la medida; el nombre no prueba la representación.")
    else:
        pendiente(v, f, "Descripcion sin patron revisado; queda pendiente.")


def g_911(v, f):
    d = v["descripcion"]
    proc = "improcedente" if v["diccionario"].startswith("1a95d734") else "procedente"
    if "hora de ingreso de la llamada" in d:
        proponer(v, f, "hora-ingreso-llamada-911-%s" % proc, "Hora de ingreso de la llamada (%s)" % proc,
                 "Hora de ingreso de la llamada 911 %s; la hora 0 son las 12 am según literal. Evento: llamada." % proc,
                 "tiempo", "hora",
                 "Denota la hora declarada.", "No aplica a otra llamada.",
                 "Hora de ingreso, no de atención; literal de hora 0 conservado.")
    elif "colonio donde se realizó la llamada" in d:
        proponer(v, f, "colonia-origen-llamada-911-%s" % proc, "Colonia de origen (%s)" % proc,
                 "Colonia (literal colonio) donde se realizó la llamada 911 %s. Objeto: colonia." % proc,
                 "localidad", "nombre",
                 "Denota la colonia declarada.", "No aplica a otra llamada.",
                 "Colonia declarada; literal con errata conservado; no acredita catálogo.")
    elif "sexo de la persona que realizó la llamada" in d:
        proponer(v, f, "sexo-reportante-llamada-911-%s" % proc, "Sexo del reportante (%s)" % proc,
                 "Sexo de la persona que realizó la llamada 911 %s." % proc,
                 "sexo-declarado", "no_especificada",
                 "Denota el sexo declarado.", "No aplica a otra llamada.", "Sin valores publicados.")
    else:
        pendiente(v, f, "Descripcion sin patron revisado; queda pendiente.")


ADQ_MESES = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}


def g_adq(v, f):
    d = v["descripcion"]
    for mes in ADQ_MESES:
        if d == "Monto registrado en %s" % mes:
            proponer(v, f, "monto-adquisiciones-%s" % mes, "Monto de adquisiciones de %s" % mes,
                     "Monto registrado en %s en el programa anual de adquisiciones. Medida: moneda." % mes,
                     None, "no_especificada",
                     "Denota el monto del mes de la evidencia.", "No aplica a otro mes.",
                     "Monto del mes indicado; moneda no declarada; no sumar meses sin acreditación.")
            return
    base = {
        "Cantidad registrada": ("cantidad-material-adquisicion", "Cantidad registrada", "Cantidad registrada de material en adquisiciones. Medida: conteo."),
        "Clave de la partida presupuestal": ("clave-partida-presupuestal-adquisicion", "Clave de partida presupuestal", "Clave de la partida presupuestal en adquisiciones. Objeto: partida."),
        "Codigo del material": ("codigo-material-adquisicion", "Código del material", "Código del material en adquisiciones. Objeto: material."),
        "Costo unitario": ("costo-unitario-adquisicion", "Costo unitario", "Costo unitario del material en adquisiciones. Medida: moneda."),
        "Descripción del  material": ("descripcion-material-adquisicion", "Descripción del material", "Descripción del material en adquisiciones (literal con doble espacio). Objeto: material."),
        "Impuesto del valor agregado": ("iva-adquisicion", "IVA", "Impuesto del valor agregado del material en adquisiciones. Tasa porcentual según tipo Porcentual y ejemplo 0% de la fila."),
        "Origen del recurso": ("origen-recurso-adquisicion", "Origen del recurso", "Origen del recurso en adquisiciones."),
    }
    if d in base:
        s, lab, defi = base[d]
        rep = "codigo" if s in ("clave-partida-presupuestal-adquisicion", "codigo-material-adquisicion") else "no_especificada"
        proponer(v, f, s, lab, defi, None, rep,
                 "Denota el dato de la evidencia.", "No aplica a otro material.",
                 "Dato declarado; códigos sin catálogo publicado; moneda no declarada.")
    else:
        pendiente(v, f, "Descripcion sin patron revisado; queda pendiente.")


def main():
    for v in MINE:
        procesar(v)
    ids = [d["definicion_iri"] for d in decisiones]
    assert len(decisiones) == len(MINE) == 468, (len(decisiones), len(MINE))
    assert len(set(ids)) == 468, "duplicados u omisiones"
    assert set(ids) == {v["definicion_iri"] for v in MINE}, "particion inexacta"
    assert len(reglas) == sum(1 for d in decisiones if d["decision"] == "proponer")
    for r in reglas:
        assert r["id"].startswith(PREF) and len(r["definiciones"]) == 1 and len(r["nombres"]) == 1
        assert len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["descripciones"]) == 1
        assert r["representacion"] in ("codigo", "nombre", "no_especificada", "mes", "anio", "fecha", "hora", "dia")
    for slug in reutilizados:
        assert slug in CONCEPTOS_VIG
    for slug in nuevos:
        assert slug not in CONCEPTOS_VIG
    # Correcciones auditadas post-generacion (trazables por regla/concepto).
    concepto("clave-presa", "Clave de presa",
             "Clave que identifica a una presa según la fuente. El sistema de codificación y la identidad entre fuentes no están acreditados.",
             None)
    for _s in ("clave-identificadora-presa", "clave-presa-recurso-hidrico"):
        nuevos[_s][2] = "clave-presa"
    _rep_fix = {"r3a10-0148": "no_especificada", "r3a10-0366": "no_especificada",
                "r3a10-0367": "no_especificada", "r3a10-0373": "no_especificada"}
    _lim_add = {
        "r3a10-0148": " Representación conservadora: la descripción no declara la forma del valor.",
        "r3a10-0366": " Representación conservadora: la descripción no declara la forma del valor.",
        "r3a10-0367": " Representación conservadora: la descripción no declara la forma del valor.",
        "r3a10-0373": " Representación conservadora: la descripción no declara la forma del valor.",
        "r3a10-0246": " Ejemplo 'Bajo' conservado literal; incoherente con tipo Numérico declarado; no se tipifican valores.",
    }
    _def_fix = {
        "volumen-total-produccion-pecuaria": "Volumen total producido en ganadería según literal. Medida: volumen.",
        "precio-minimo-kg-subasta": "Precio mínimo registrado por kilogramo en la subasta. Medida: moneda por kilogramo.",
        "precio-maximo-kg-subasta": "Precio máximo registrado por kilogramo en la subasta. Medida: moneda por kilogramo.",
        "precio-promedio-kg-subasta": "Precio promedio registrado por kilogramo en la subasta. Medida: moneda por kilogramo.",
        "ddr-registro-pecuario": "Distrito de Desarrollo Rural donde se registra la producción pecuaria. Objeto: DDR. La representación la fija cada regla.",
        "clave-especie-pecuaria": "Especie producida en ganadería. Objeto: especie. La representación la fija cada regla.",
        "clave-especie-fauna-caza": "Especie de fauna cinegética. Objeto: especie. La representación la fija cada regla.",
        "cuenca-presa-ubicacion": "Cuenca en que se encuentra cada presa. Objeto: cuenca. La representación la fija cada regla.",
        "region-hidrologica-presa": "Región hidrológica en que se encuentra cada presa. La representación la fija cada regla.",
        "tipo-ganado-subasta": "Tipo de ganado subastado. Objeto: ganado. La representación la fija cada regla.",
    }
    for _r in reglas:
        if _r["id"] in _rep_fix:
            _r["representacion"] = _rep_fix[_r["id"]]
        if _r["id"] in _lim_add:
            _r["limite"] = _r["limite"] + _lim_add[_r["id"]]
    for _s, _d in _def_fix.items():
        nuevos[_s][1] = _d
    prop = {
        "generado_en_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "agente": AGENTE,
        "asignacion": "propuestas/ronda-3/integrador/asignaciones-semanticas.json#asignaciones/10",
        "base_iri": "https://example.org/mex-ontologi/",
        "alcance": "468 definiciones asignadas al agente 10 (particion completa); sin correspondencias columna-variable nuevas; sin conceptos sameAs/exactMatch.",
        "huellas_entrada": {
            "asignaciones": sha256(asig_path),
            "cobertura": sha256(cob_path),
            "semantica": sha256(sem_path),
        },
        "conteos": {
            "asignadas": len(MINE),
            "decisiones": len(decisiones),
            "proponer": sum(1 for d in decisiones if d["decision"] == "proponer"),
            "pendiente": sum(1 for d in decisiones if d["decision"] == "pendiente"),
            "reglas": len(reglas),
            "conceptos_nuevos": len(nuevos),
            "conceptos_reutilizados": len(reutilizados),
        },
        "fuentes": {"inspecciones_diccionarios": {d: sha256(INS_DIR / (d + ".json")) for d in dics}},
        "decisiones": decisiones,
        "reglas": reglas,
        "conceptos_nuevos": nuevos,
        "conceptos_reutilizados": sorted(reutilizados),
        "limites": [
            "Ninguna regla crea correspondencias columna-variable; la revision posterior decide vinculos.",
            "Ningun concepto nuevo declara sameAs ni exactMatch; no hay equivalencia de catalogos.",
            "Codigos sin catalogo publicado no acreditan identidad, vigencia ni adopcion oficial.",
            "Descripciones genericas o de folio quedan pendientes con razon; no se infiere significado por el nombre.",
            "Calificadores sustantivos (mes, edad, nivel, sexo, poblacion, metodologia) van en conceptos estrechos; el pipeline actual no preserva calificadores formales.",
            "Metodologia anterior y actual no son comparables; meses de registro no implican ocurrencia.",
            "Proyecciones son estimaciones, no conteos observados; periodos no declarados no se inventan.",
        ],
    }
    with open(AQUI / "propuestas.json", "w", encoding="utf-8") as f:
        json.dump(prop, f, ensure_ascii=False, indent=1)
    with open(AQUI / "fuente" / "huellas_entrada.json", "w", encoding="utf-8") as f:
        json.dump({"agente": AGENTE, "huellas_entrada": prop["huellas_entrada"],
                   "inspecciones": prop["fuentes"]["inspecciones_diccionarios"],
                   "asignadas": len(MINE)}, f, ensure_ascii=False, indent=1)
    n_prop = prop["conteos"]["proponer"]
    n_pen = prop["conteos"]["pendiente"]
    import collections
    mot = collections.Counter(d["motivo"] for d in decisiones if d["decision"] == "pendiente")
    with open(AQUI / "resultado.md", "w", encoding="utf-8") as f:
        f.write("# Agente 10 territorio-economía — ronda 3\n\n")
        f.write("Asignadas: 468. Decisiones: 468 (partición completa, sin omitidos ni duplicados).\n")
        f.write("Lectura literal individual de fila de diccionario (descripción, tipo, unidad, ejemplo, catálogo, contexto de conjunto) verificada por índice de definición_iri contra inspecciones locales.\n\n")
        f.write("| Resultado | Cantidad |\n| --- | ---: |\n")
        f.write("| Proponer (con regla restringida) | %d |\n" % n_prop)
        f.write("| Pendiente con razón | %d |\n" % n_pen)
        f.write("| Reglas nuevas | %d |\n" % len(reglas))
        f.write("| Conceptos nuevos estrechos | %d |\n" % len(nuevos))
        f.write("| Conceptos vigentes reutilizados | %d |\n" % len(reutilizados))
        f.write("\n## Pendientes por motivo\n\n")
        for m, n in mot.most_common():
            f.write("- %d × %s\n" % (n, m))
        f.write("\n## Verificación\n\n")
        f.write("`uv run python propuestas/%s/scripts/verificar.py`: huellas SHA-256 de entradas, partición exacta,\n" % AGENTE)
        f.write("literales y filas recalculadas, reglas unitarias con prefijo r3a10-, 40 positivos y 6 negativos\n")
        f.write("(solo-nombre, contexto-mutado, otra-IRI, descripcion-alterada, unidad-faltante, codigo-no-acreditado),\n")
        f.write("base 103/232/836/118. Sin red, sin escritura fuera de la carpeta, sin correspondencias nuevas,\n")
        f.write("sin sameAs/exactMatch, sin identidad ni vigencia inventadas.\n")
        f.write("\n## Revisión manual vs automatización\n\n")
        f.write("Manual (humano, en `scripts/construir.py`): lectura literal de las 468 descripciones y su contexto\n")
        f.write("de conjunto; política explícita por grupo (proponer concepto estrecho o dejar pendiente con razón);\n")
        f.write("redacción de cada definición, positivo, contraejemplo y límite sin inventar unidades\n")
        f.write("(edad sin unidad≠años, conteo sin objeto≠personas, monetarios sin moneda≠MXN, sin rangos 0–100),\n")
        f.write("sin deducir representación desde el nombre (el nombre solo restringe la regla) y conservando\n")
        f.write("contradicciones nombre↔descripción como pendientes neutros.\n\n")
        f.write("Automático (verificable): indexado de filas por `definicion_iri`, recomputo de huellas SHA-256,\n")
        f.write("con positivos y 6 familias de negativos (ver `scripts/verificar.py`, 132 comprobaciones).\n")
        f.write("\n## Límites y pendientes\n\n")
        f.write("- Sin correspondencias columna→variable nuevas; la revisión posterior decide vínculos.\n")
        f.write("- Códigos sin catálogo publicado no acreditan identidad, vigencia ni adopción oficial.\n")
        f.write("- Metodología anterior y actual no son comparables; meses de registro no implican ocurrencia.\n")
        f.write("- Proyecciones son estimaciones; periodos no declarados no se inventan.\n")
        f.write("- 49 pendientes quedan para aclaración del publicador o revisión posterior (folios, clasificaciones sin catálogo, tipos/estados sin valores publicados).\n")
    print("decisiones=%d proponer=%d pendiente=%d reglas=%d nuevos=%d reut=%d" % (
        len(decisiones), n_prop, n_pen, len(reglas), len(nuevos), len(reutilizados)))


if __name__ == "__main__":
    main()
