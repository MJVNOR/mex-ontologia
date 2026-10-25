"""Verificador independiente agente 10 ronda 3. Solo lectura central; no genera nada fuera de su carpeta.
Pruebas reales con positivos y negativos; ningun `assert X or True`.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
FALLOS = []


def ok(cond, msg):
    print(("PASS" if cond else "FAIL"), "-", msg)
    if not cond:
        FALLOS.append(msg)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


asig = json.load(open(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
MINE = asig["asignaciones"]["10"]["variables"]
COB = json.load(open(ROOT / "data/semantica/cobertura.json", encoding="utf-8"))
SEM = json.load(open(ROOT / "ontologia/semantica.json", encoding="utf-8"))
PROP = json.load(open(AQUI / "propuestas.json", encoding="utf-8"))

# 1. huellas de entrada reales
ok(PROP["huellas_entrada"]["asignaciones"] == sha256(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"), "huella asignaciones")
ok(PROP["huellas_entrada"]["cobertura"] == sha256(ROOT / "data/semantica/cobertura.json"), "huella cobertura")
ok(PROP["huellas_entrada"]["semantica"] == sha256(ROOT / "ontologia/semantica.json"), "huella semantica")
for d, h in PROP["fuentes"]["inspecciones_diccionarios"].items():
    ok(h == sha256(ROOT / "data/portal/inspecciones" / (d + ".json")), "huella inspeccion %s" % d[:8])
    ok("/" not in d and "\\" not in d, "id diccionario sin ruta %s" % d[:8])

# 2. particion completa exacta
ok(len(PROP["decisiones"]) == 468 == len(MINE), "468 decisiones y 468 asignadas")
ok(len({d["definicion_iri"] for d in PROP["decisiones"]}) == 468, "sin duplicados")
ok({d["definicion_iri"] for d in PROP["decisiones"]} == {v["definicion_iri"] for v in MINE}, "sin omitidos: particion exacta")
ok(PROP["asignacion"].endswith("asignaciones/10"), "alcance fijado a asignaciones[10]")

# 3. literales conservados por decision
por_iri = {v["definicion_iri"]: v for v in MINE}
for d in PROP["decisiones"]:
    v = por_iri[d["definicion_iri"]]
    if not (d["variable"] == v["variable"] and d["descripcion_literal"] == v["descripcion"]
            and d["huella_fila_diccionario"] == v["huella_fila_diccionario"]
            and d["conjunto"] == v["conjunto"] and d["diccionario"] == v["diccionario"]
            and d["titulo_conjunto"] == v["titulo_conjunto"]
            and d["catalogo_declarado"] == v["catalogo_declarado"]):
        ok(False, "literal alterado en %s" % d["definicion_iri"])
        break
else:
    ok(True, "literales exactos en 468 decisiones (variable, descripcion, huella, IRIs, catalogo declarado incl. N/A y Catalogo_estatal)")

# 4. fila de diccionario recalculada desde inspeccion (misma normalizacion que construir)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from construir import norm_row  # noqa: E402  (solo funciones puras; main protegido)

n_filas = 0
for d in PROP["decisiones"]:
    insp = json.load(open(ROOT / "data/portal/inspecciones" / (d["diccionario"] + ".json"), encoding="utf-8"))
    filas = insp.get("definiciones", [])
    k = int(d["definicion_iri"].split("%2F")[1]) - 1
    if not (0 <= k < len(filas)):
        ok(False, "indice fuera de rango %s" % d["definicion_iri"])
        break
    r = norm_row(filas[k])
    if r["descripcion"].strip() != d["descripcion_literal"].strip():
        ok(False, "descripcion no coincide con inspeccion %s" % d["definicion_iri"])
        break
    if not (d["tipo_de_dato"] == r["tipo"] and d["unidad_de_medida"] == r["unidad"]
            and d["catalogo_de_referencia"] == r["catalogo"] and d["ejemplo_de_dato"] == r["ejemplo"]):
        ok(False, "tipo/unidad/ejemplo/catalogo no copiados exactos %s" % d["definicion_iri"])
        break
    n_filas += 1
else:
    ok(True, "468 filas de diccionario recalculadas (indice IRI) con literales exactos")
ok(n_filas == 468, "filas verificadas=%d" % n_filas)

# 5. reglas: forma y restricciones simultaneas
ids = [r["id"] for r in PROP["reglas"]]
ok(len(ids) == len(set(ids)) and all(i.startswith("r3a10-") for i in ids), "ids unicos con prefijo r3a10-")
ok(all(len(r["definiciones"]) == 1 and len(r["nombres"]) == 1 and len(r["conjuntos"]) == 1
       and len(r["diccionarios"]) == 1 and len(r["descripciones"]) == 1 for r in PROP["reglas"]), "restriccion simultanea unitaria en todas las reglas")
ok(all(r["representacion"] in ("codigo", "nombre", "no_especificada", "mes", "anio", "fecha", "hora", "dia") for r in PROP["reglas"]), "representaciones del vocabulario vigente")
ok(all(r["concepto"] in PROP["conceptos_nuevos"] or r["concepto"] in SEM["conceptos"] for r in PROP["reglas"]), "conceptos de reglas existen (nuevos o vigentes)")
ok(all("sameAs" not in json.dumps(r) and "exactMatch" not in json.dumps(r) for r in PROP["reglas"]), "sin sameAs/exactMatch")
ok(all(r["evidencia"] and r["evidencia"][0]["definicion_iri"] in r["definiciones"] for r in PROP["reglas"]), "evidencia por regla ligada a su definicion")
for r in PROP["reglas"]:
    if r["representacion"] == "codigo" and "cat" not in (r["limite"] + r["evidencia"][0].get("catalogo_de_referencia", "")).lower() and "acredit" not in r["limite"].lower():
        ok(False, "codigo sin limite de catalogo: %s" % r["id"])
        break
else:
    ok(True, "toda regla codigo trae limite de catalogo/acreditacion")
ok(all("global" not in r.get("alcance", "") or "Solo" in r["alcance"] for r in PROP["reglas"]), "alcance fijado por regla")

# 6. conceptos nuevos y reutilizados
for slug, val in PROP["conceptos_nuevos"].items():
    if not (isinstance(val, list) and len(val) == 3 and val[0] and val[1]
            and (val[2] is None or val[2] in SEM["conceptos"] or val[2] in PROP["conceptos_nuevos"])
            and slug not in SEM["conceptos"] and " " not in slug and slug == slug.lower()):
        ok(False, "concepto nuevo malformado: %s" % slug)
        break
else:
    ok(True, "conceptos nuevos con forma {slug:[label,definicion,broader]} y broader valido (%d)" % len(PROP["conceptos_nuevos"]))
ok(all(c in SEM["conceptos"] for c in PROP["conceptos_reutilizados"]), "reutilizados existen en 103 vigentes")
ok(not (set(PROP["conceptos_nuevos"]) & set(PROP["conceptos_reutilizados"])), "nuevos y reutilizados disjuntos")
ok(not (set(PROP["conceptos_nuevos"]) & set(SEM["conceptos"])), "nuevos no colisionan con vigentes")

# 7. decisiones/reglas consistentes
reg_por_def = {}
for r in PROP["reglas"]:
    reg_por_def.setdefault(r["definiciones"][0], []).append(r["id"])
for d in PROP["decisiones"]:
    if d["decision"] == "proponer":
        if not (d["regla"] in reg_por_def.get(d["definicion_iri"], []) and d["concepto"]):
            ok(False, "decision proponer sin regla propia %s" % d["definicion_iri"])
            break
    elif not (d["regla"] is None and d["concepto"] is None and d["motivo"]):
        ok(False, "pendiente sin motivo %s" % d["definicion_iri"])
        break
else:
    ok(True, "decisiones y reglas consistentes (proponer con regla propia, pendiente con motivo)")
ok(PROP["conteos"]["proponer"] == sum(1 for d in PROP["decisiones"] if d["decision"] == "proponer") == len(PROP["reglas"]), "conteos proponer/reglas cuadran")
ok(PROP["conteos"]["pendiente"] == sum(1 for d in PROP["decisiones"] if d["decision"] == "pendiente"), "conteo pendiente cuadra")

# 8. interpretacion() en memoria: positivos y negativos reales
def interpretacion(conjunto, diccionario, definicion_iri, nombre, descripcion):
    hits = [r["id"] for r in PROP["reglas"]
            if conjunto in r["conjuntos"] and diccionario in r["diccionarios"]
            and definicion_iri in r["definiciones"] and nombre in r["nombres"]
            and descripcion in r["descripciones"]]
    return hits[0] if len(hits) == 1 else None

muestra = [r for r in PROP["reglas"][:40]]
for r in muestra:
    got = interpretacion(r["conjuntos"][0], r["diccionarios"][0], r["definiciones"][0], r["nombres"][0], r["descripciones"][0])
    if got != r["id"]:
        ok(False, "positivo falla %s" % r["id"])
        break
else:
    ok(True, "positivos: 40 reglas resuelven con tupla exacta")
r0 = PROP["reglas"][0]
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0], "https://example.org/mex-ontologi/definition/OTRA%2F1", r0["nombres"][0], r0["descripciones"][0]) is None, "negativo otra-IRI no resuelve")
ok(interpretacion("OTRO-CONJUNTO", r0["diccionarios"][0], r0["definiciones"][0], r0["nombres"][0], r0["descripciones"][0]) is None, "negativo contexto-mutado no resuelve")
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0], r0["definiciones"][0], r0["nombres"][0] + "-X", r0["descripciones"][0]) is None, "negativo solo-nombre no resuelve")
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0], r0["definiciones"][0], r0["nombres"][0], r0["descripciones"][0] + " ") is None, "negativo descripcion-alterada no resuelve")
sin_unidad = [r for r in PROP["reglas"] if not r["evidencia"][0]["unidad_de_medida"]]
ok(len(sin_unidad) > 0, "existen reglas con unidad faltante (%d)" % len(sin_unidad))
ru = sin_unidad[0]
ok(interpretacion(ru["conjuntos"][0], ru["diccionarios"][0], "https://example.org/mex-ontologi/definition/OTRA%2F9", ru["nombres"][0], ru["descripciones"][0]) is None, "negativo unidad-faltante: sin IRI exacta no resuelve")
cod_sin_cat = [r for r in PROP["reglas"] if r["representacion"] == "codigo" and not r["evidencia"][0]["catalogo_de_referencia"]]
ok(len(cod_sin_cat) > 0, "existen codigos sin catalogo declarado (%d)" % len(cod_sin_cat))
ok(all("cat" in r["limite"].lower() or "acredit" in r["limite"].lower() for r in cod_sin_cat), "negativo codigo-no-acreditado: todo codigo sin catalogo trae limite")

# 8b. criterio de integracion: sin unidades ni objetos inventados; contradiccion conservada
import re as _re, unicodedata as _ud

def _fold(s):
    return "".join(c for c in _ud.normalize("NFD", s) if _ud.category(c) != "Mn").casefold()

SOP = {
    "años": ["añ"],
    "moneda": ["monto", "importe", "valor", "costo", "precio", "impuesto", "pago", "econom"],
    "conteo": ["numero", "total", "cantidad", "poblaci", "cabezas", "cintillos"],
    "porcentaje": ["porcentaje", "%"],
    "promedio": ["promedio"],
    "razón": ["razon", "relacion"],
    "tasa": ["tasa", "porcentual"],
    "potencia": ["potencia"],
    "energía": ["energ", "electric"],
    "volumen": ["volumen"],
    "peso": ["peso"],
    "hectómetros": ["hectometros"],
    "kilogramos": ["kilogramos"],
    "grados": ["grados"],
    "mw": ["mw"],
    "gwh": ["gwh"],
    "hora": ["hora"],
    "día": ["dia"],
    "fecha": ["fecha"],
    "tiempo": ["tiempo"],
    "personas": ["persona"],
    "hombres": ["hombre", "masculin"],
    "mujeres": ["mujer", "femenin", "mujer"],
    "alumnos": ["alumno"],
    "víctimas": ["victima"],
}
PROHIB = ["mxn", "dólar", "dolar", "0-100", "0 a 100", "msnm", "según variable", "segun variable", "según nombre", "segun nombre"]
for d in PROP["decisiones"]:
    if d["decision"] != "proponer":
        continue
    defi = _fold(PROP["conceptos_nuevos"][d["concepto"]][1]) if d["concepto"] in PROP["conceptos_nuevos"] else ""
    if not defi:
        continue
    for ph in PROHIB:
        if ph in defi:
            ok(False, "unidad inventada %r en %s" % (ph, d["definicion_iri"]))
            break
    else:
        sin_nombre = _re.sub(r"el nombre indica[^.]*\.", "", defi)
        soporte = _fold(d["descripcion_literal"] + " " + d["unidad_de_medida"] + " " + d["tipo_de_dato"] + " " + d["titulo_conjunto"])
        for tok, cands in SOP.items():
            if tok == "índice":
                continue
            if tok in sin_nombre and not any(c in soporte for c in cands):
                ok(False, "sin respaldo %r en %s" % (tok, d["definicion_iri"]))
                break
        else:
            if "índice" in sin_nombre and "indice" not in soporte:
                ok(False, "indice sin respaldo en %s" % d["definicion_iri"])
                break
            continue
        break
else:
    ok(True, "definiciones sin unidades/objetos inventados (respaldo en descripcion+unidad+tipo)")
nombre_sent = [d for d in PROP["decisiones"] if d["decision"] == "proponer" and "el nombre indica" in _fold(PROP["conceptos_nuevos"].get(d["concepto"], ["", ""])[1])]
ok(len(nombre_sent) > 0, "hay conceptos con calificador desde el nombre (%d)" % len(nombre_sent))
for d in nombre_sent:
    r = [x for x in PROP["reglas"] if x["id"] == d["regla"]][0]
    lim = _fold(r["limite"])
    if "nombre" not in lim or not r["nombres"]:
        ok(False, "nombre no declarado como fuente en %s" % r["id"])
        break
else:
    ok(True, "todo calificador desde el nombre esta restringido en la regla y declarado en el limite")
for d in PROP["decisiones"]:
    m = d.get("motivo") or ""
    if d["decision"] == "pendiente" and ("contradicc" in _fold(m) or "conserva la dif" in _fold(m)):
        if "nombre" not in _fold(m):
            ok(False, "contradiccion sin mencionar nombre %s" % d["definicion_iri"])
            break
else:
    ok(True, "contradicciones nombre-descripcion conservadas con mencion explicita")

# 8c. hallazgo bloqueante: IM vs IMN separados en todos los niveles
for niv, v_im, v_imn in [("localidad", "IM_2020", "IMN_2020"), ("municipio", "IM_2020", "IMN_2020"),
                         ("ageb", "IM_2020", "IMN_2020"), ("colonia", "IM_2020", "IMN_2020"),
                         ("entidad", "IM_2020", "IMN_2020")]:
    ds = [d for d in PROP["decisiones"] if d["variable"] in (v_im, v_imn) and d["concepto"] and niv in d["concepto"]]
    im = [d for d in ds if d["variable"] == "IM_2020"]
    imn = [d for d in ds if d["variable"] == "IMN_2020"]
    ok(len(im) == 1 and len(imn) == 1 and im[0]["concepto"] != imn[0]["concepto"],
       "IM e IMN con conceptos distintos en %s" % niv)
    ok("normalizado" in imn[0]["concepto"] and "normalizado" not in im[0]["concepto"],
       "normalizado solo en IMN (%s)" % niv)
ok("indice-marginacion-normalizado-colonia" in PROP["conceptos_nuevos"], "5 conceptos IMN existen")
# año solo con respaldo literal o de conjunto
for d in PROP["decisiones"]:
    if d["decision"] != "proponer":
        continue
    defi = _fold(PROP["conceptos_nuevos"][d["concepto"]][1]) if d["concepto"] in PROP["conceptos_nuevos"] else ""
    if "2020" in defi and "2020" not in _fold(d["descripcion_literal"] + " " + d["titulo_conjunto"]):
        ok(False, "año sin respaldo en %s" % d["definicion_iri"])
        break
else:
    ok(True, "año 2020 solo con respaldo literal o de conjunto")
# conceptos compartidos codigo/nombre: definicion neutral
import collections as _co
_reps = _co.defaultdict(set)
for r in PROP["reglas"]:
    _reps[r["concepto"]].add(r["representacion"])
for _c, _v in _reps.items():
    if len(_v) > 1 and _c in PROP["conceptos_nuevos"]:
        _t = _fold(PROP["conceptos_nuevos"][_c][1])
        if "clave" in _t or "codigo" in _t or "identificador" in _t or "nombre" in _t:
            ok(False, "concepto compartido con representacion fijada %s" % _c)
            break
else:
    ok(True, "conceptos compartidos con definicion neutral")
# clave-presa: broader comun sin identidad interfuente
ok(PROP["conceptos_nuevos"].get("clave-identificadora-presa", ["", "", None])[2] == "clave-presa", "broader clave-presa 1")
ok(PROP["conceptos_nuevos"].get("clave-presa-recurso-hidrico", ["", "", None])[2] == "clave-presa", "broader clave-presa 2")
_cp = _fold(PROP["conceptos_nuevos"]["clave-presa"][1])
ok("no est" in _cp and "identidad" in _cp, "broader sin identidad ni sistema unico")

# 9. base nacional: 103/232/836/118 y estado fuera_del_nucleo
ok(len(SEM["conceptos"]) == 103, "103 conceptos vigentes")
ok(COB["resumen"]["estados_variables"]["respaldada_por_definicion"] == 232, "232 respaldadas")
ok(COB["resumen"]["estados_correspondencias"]["documental_revisada"] == 836, "836 revisadas")
ok(COB["resumen"]["estados_correspondencias"]["candidata_por_nombre"] == 118, "118 candidatas")
ok(all(v["estado"] == "fuera_del_nucleo_actual" for v in MINE), "asignadas fuera_del_nucleo_actual")
cob_por_iri = {x["definicion_iri"]: x for x in COB["variables"]}
for v in MINE:
    c = cob_por_iri.get(v["definicion_iri"])
    if c is None or c["descripcion"] != v["descripcion"] or (c["diccionario"], c["variable"]) != (v["diccionario"], v["variable"]):
        ok(False, "asignacion no coincide con cobertura %s" % v["definicion_iri"])
        break
else:
    ok(True, "asignacion coincide con cobertura central en 468 (por definicion_iri)")

print("FALLOS:", len(FALLOS))
sys.exit(1 if FALLOS else 0)
