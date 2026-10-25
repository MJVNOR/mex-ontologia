"""Entrega territorio-economia (cobertura-muse-20261023).

Base: copias congeladas (agente-3 + agente-10) verificadas contra manifiesto.
Corrige lo observado por auditoria-11 y el criterio de integracion.
No crea correspondencias columna-variable. No toca el nucleo.
"""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
FZ = ROOT / "propuestas/cobertura-muse-20261023/fuentes"
MI_ENTREGA = "propuestas/cobertura-muse-20261023/territorio-economia/entrega.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from correcciones import NUEVOS_IMN, CONCEPTO_SET, REP_SET, LIM_ADD, LIM_CONJUNTO, DEF_FIX, SUFIJOS  # noqa: E402


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


FALLOS = []


def ok(cond, msg):
    if not cond:
        FALLOS.append(msg)
    return cond


# ---- 1. insumos congelados verificados ----
man = load(FZ / "manifiesto.json")
for c in man["copias"]:
    if c["copia"].startswith("propuestas/cobertura-muse-20261023/fuentes/agente-10") or \
       c["copia"].startswith("propuestas/cobertura-muse-20261023/fuentes/agente-3"):
        ok(sha256(ROOT / c["copia"]) == c["sha256"], "manifiesto " + c["copia"])
for p in ("ontologia/semantica.json", "data/semantica/cobertura.json",
          "propuestas/ronda-3/integrador/asignaciones-semanticas.json"):
    ok(sha256(ROOT / p) == man["insumos_centrales"][p], "central " + p)

a10 = load(FZ / "agente-10-territorio-economia/propuestas.json")
a3 = load(FZ / "agente-3-cobertura/propuestas.json")
cob = load(ROOT / "data/semantica/cobertura.json")
sem = load(ROOT / "ontologia/semantica.json")
asig10 = load(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json")["asignaciones"]["10"]["variables"]
cob_por_iri = {x["definicion_iri"]: x for x in cob["variables"]}

# ---- 2. particion asignada ----
iris10 = {v["definicion_iri"] for v in asig10}
dec10 = {d["definicion_iri"] for d in a10["decisiones"]}
ok(dec10 == iris10 and len(a10["decisiones"]) == 468, "particion A10 468 exacta")
iris_a3_reglas = [r["definiciones"][0] for r in a3["reglas"]]
iris_a3_pen = [s["definicion_iri"] for s in a3["sin_propuesta_tras_lectura"]]
ok(len(iris_a3_reglas) == 63 and len(iris_a3_pen) == 3, "A3 63+3")
ok(len(set(iris_a3_reglas) | set(iris_a3_pen)) == 66, "A3 66 unicas")
ok(not (set(iris_a3_reglas + iris_a3_pen) & iris10), "A3 y A10 disjuntos")
fams = {}
for s in a3["sin_propuesta_tras_lectura"]:
    fams.setdefault(s["diccionario"], []).append(s["variable"])
for r in a3["reglas"]:
    fams.setdefault(r["diccionarios"][0], []).append(r["nombres"][0])
ok(sorted(fams) == sorted(["045da7ba-ee72-498a-9b7a-071176e2a4ea", "94215f51-9c89-414d-8c3d-92792e609a2a",
                           "863b9cc8-daeb-4430-b835-6a0ced5abd31", "a7591bc9-f905-45cb-ba6c-ae3588d87594"]),
   "A3 4 diccionarios familiares")
for iri in iris_a3_reglas + iris_a3_pen:
    c = cob_por_iri.get(iri)
    ok(c is not None and c["estado"] == "fuera_del_nucleo_actual", "A3 fuera del nucleo " + iri[-12:])

# ---- 3. conceptos y reglas ----
nuevos = {}
nuevos.update(copy.deepcopy(a3["conceptos_nuevos"]))
nuevos.update(copy.deepcopy(a10["conceptos_nuevos"]))
nuevos.update(copy.deepcopy(NUEVOS_IMN))
ok(len(set(a3["conceptos_nuevos"]) & set(a10["conceptos_nuevos"])) == 0, "sin colision A3-A10")
for slug, val in nuevos.items():
    ok(isinstance(val, list) and len(val) == 3 and val[0] and val[1], "forma concepto " + slug)
    ok(slug not in sem["conceptos"], "no colisiona vigente " + slug)
    ok(val[2] is None or val[2] in sem["conceptos"] or val[2] in nuevos, "padre valido " + slug)
# definiciones corregidas
for slug, defi in DEF_FIX.items():
    nuevos[slug][1] = defi
for slug in list(nuevos):
    for old, new in SUFIJOS:
        if old in nuevos[slug][1]:
            nuevos[slug][1] = nuevos[slug][1].replace(old, new)

reglas = []
for r in a3["reglas"] + a10["reglas"]:
    nr = copy.deepcopy(r)
    if nr["id"] in CONCEPTO_SET:
        nr["concepto"] = CONCEPTO_SET[nr["id"]]
    if nr["id"] in REP_SET:
        nr["representacion"] = REP_SET[nr["id"]]
    if nr["id"] in LIM_ADD:
        nr["limite"] = nr["limite"] + LIM_ADD[nr["id"]]
    cj = nr["conjuntos"][0]
    if cj in LIM_CONJUNTO:
        nr["limite"] = nr["limite"] + LIM_CONJUNTO[cj]
    nr["fuente_revision"] = MI_ENTREGA
    for ev in nr["evidencia"]:
        if "huella_fila_diccionario" not in ev:
            c = cob_por_iri.get(ev["definicion_iri"], {})
            ev["huella_fila_diccionario"] = c.get("huella_fila_diccionario", "")
    reglas.append(nr)

ids = [r["id"] for r in reglas]
ok(len(ids) == len(set(ids)) == 482, "482 reglas unicas")
ok(all(len(r["definiciones"]) == 1 and len(r["nombres"]) == 1 and len(r["conjuntos"]) == 1
       and len(r["diccionarios"]) == 1 and len(r["descripciones"]) == 1 for r in reglas),
   "alcance simultaneo unitario")
ok(all(r["representacion"] in ("codigo", "nombre", "no_especificada", "mes", "anio", "fecha", "hora", "dia") for r in reglas),
   "representaciones del vocabulario")
ok(all(r["concepto"] in nuevos or r["concepto"] in sem["conceptos"] for r in reglas), "conceptos existen")
ok(all("sameAs" not in json.dumps(r) and "exactMatch" not in json.dumps(r) for r in reglas), "sin equivalencias")
ok(all(r["fuente_revision"] == MI_ENTREGA and r["evidencia"] and
       r["evidencia"][0]["definicion_iri"] in r["definiciones"] and
       r["evidencia"][0].get("huella_fila_diccionario") for r in reglas),
   "evidencia con huella ligada a la definicion")

# calificadores DDR preservados
shd = [r for r in reglas if r["concepto"] == "superficie-sembrada-trigo-ddr"]
ok(len(shd) == 10 and all(r.get("calificador", {}).get("distrito_desarrollo_rural") for r in shd),
   "10 calificadores DDR preservados")
ok(all(r.get("requisito_integracion") for r in shd), "requisito de integracion en SHD")

# ---- 4. decisiones 534 ----
decisiones = []
for d in a10["decisiones"]:
    nd = dict(d)
    nd["regla_id"] = nd.pop("regla")
    decisiones.append(nd)
for r in a3["reglas"]:
    iri = r["definiciones"][0]
    c = cob_por_iri[iri]
    ev = r["evidencia"][0]
    decisiones.append({
        "definicion_iri": iri, "conjunto": r["conjuntos"][0],
        "titulo_conjunto": c.get("titulo_conjunto", ""), "diccionario": r["diccionarios"][0],
        "variable": ev["variable"], "descripcion_literal": ev["descripcion"],
        "huella_fila_diccionario": ev.get("huella_fila_diccionario", c.get("huella_fila_diccionario", "")),
        "catalogo_declarado": c.get("catalogo_declarado", ""),
        "tipo_de_dato": ev.get("tipo_de_dato", ""), "unidad_de_medida": ev.get("unidad_de_medida", ""),
        "ejemplo_de_dato": ev.get("ejemplo_de_dato", ""), "catalogo_de_referencia": ev.get("catalogo_de_referencia", ""),
        "decision": "proponer", "concepto": r["concepto"], "regla_id": r["id"], "motivo": None,
    })
for s in a3["sin_propuesta_tras_lectura"]:
    iri = s["definicion_iri"]
    c = cob_por_iri.get(iri, {})
    decisiones.append({
        "definicion_iri": iri, "conjunto": s["conjunto"],
        "titulo_conjunto": c.get("titulo_conjunto", ""), "diccionario": s["diccionario"],
        "variable": s["variable"], "descripcion_literal": s["descripcion"],
        "huella_fila_diccionario": c.get("huella_fila_diccionario", ""),
        "catalogo_declarado": c.get("catalogo_declarado", ""),
        "tipo_de_dato": "", "unidad_de_medida": "", "ejemplo_de_dato": "", "catalogo_de_referencia": "",
        "decision": "pendiente", "concepto": None, "regla_id": None, "motivo": s["motivo"],
    })
ok(len(decisiones) == 534 and len({d["definicion_iri"] for d in decisiones}) == 534, "534 decisiones unicas")
for d in decisiones:
    if d["decision"] == "proponer":
        ok(d["regla_id"] in ids, "regla existe " + d["definicion_iri"][-12:])
    else:
        ok(d["regla_id"] is None and d["motivo"], "pendiente con motivo " + d["definicion_iri"][-12:])
ok(sum(1 for d in decisiones if d["decision"] == "proponer") == 482, "482 proponer")
ok(sum(1 for d in decisiones if d["decision"] == "pendiente") == 52, "52 pendientes")

# ---- 5. base preservada ----
ok(len(sem["conceptos"]) == 103, "103 vigentes")
ok(cob["resumen"]["estados_variables"]["respaldada_por_definicion"] == 232, "232 respaldadas")
ok(cob["resumen"]["estados_variables"]["candidata_sin_definicion_suficiente"] == 23, "23 candidatas")
ok(cob["resumen"]["estados_correspondencias"]["documental_revisada"] == 836, "836 revisadas")
ok(cob["resumen"]["estados_correspondencias"]["candidata_por_nombre"] == 118, "118 candidatas col")

# ---- 6. sin unidades/objetos inventados ----
import re as _re
import unicodedata as _ud


def _fold(s):
    return "".join(c for c in _ud.normalize("NFD", s) if _ud.category(c) != "Mn").casefold()


SOP = {
    "años": ["añ"], "moneda": ["monto", "importe", "valor", "costo", "precio", "impuesto", "pago", "econom"],
    "conteo": ["numero", "total", "cantidad", "poblaci", "cabezas", "cintillos"],
    "porcentaje": ["porcentaje", "%"], "promedio": ["promedio"], "razón": ["razon", "relacion"],
    "tasa": ["tasa", "porcentual"], "potencia": ["potencia"], "energía": ["energ", "electric"],
    "volumen": ["volumen"], "peso": ["peso"], "hectómetros": ["hectometros"],
    "kilogramos": ["kilogramos"], "grados": ["grados"], "mw": ["mw"], "gwh": ["gwh"],
    "hora": ["hora"], "día": ["dia"], "fecha": ["fecha"], "tiempo": ["tiempo"],
    "personas": ["persona"], "hombres": ["hombre", "masculin"], "mujeres": ["mujer", "femenin", "mujer"],
    "alumnos": ["alumno"], "víctimas": ["victima"],
}
PROHIB = ["dólar", "dolar", "0-100", "0 a 100", "msnm", "según variable", "segun variable",
          "según nombre", "segun nombre"]
reg_map = {r["id"]: r for r in reglas}
for d in decisiones:
    if d["decision"] != "proponer":
        continue
    c = d.get("concepto") or reg_map[d["regla_id"]]["concepto"]
    defi = _fold(nuevos[c][1]) if c in nuevos else ""
    if not defi:
        continue
    r = reg_map[d["regla_id"]]
    ev = r["evidencia"][0]
    soporte = _fold(d["descripcion_literal"] + " " + d["unidad_de_medida"] + " " + d["tipo_de_dato"]
                     + " " + d["titulo_conjunto"] + " " + ev.get("unidad_de_medida", ""))
    for ph in PROHIB + ["mxn"]:
        if ph in defi and ph not in soporte:
            ok(False, "inventado %r en %s" % (ph, r["id"]))
    sin = _re.sub(r"el nombre indica[^.]*\.", "", defi)
    for tok, cands in SOP.items():
        if tok == "índice":
            continue
        if tok in sin and not any(x in soporte for x in cands):
            ok(False, "sin respaldo %r en %s" % (tok, r["id"]))
    if "índice" in sin and "indice" not in soporte:
        ok(False, "indice sin respaldo en %s" % r["id"])
ok(True, "sin unidades ni objetos inventados")
nombre_sent = [d for d in decisiones if d["decision"] == "proponer"
               and "el nombre indica" in _fold((nuevos.get(d.get("concepto") or reg_map[d["regla_id"]]["concepto"], ["", ""])[1]))]
ok(len(nombre_sent) > 0, "calificadores desde el nombre presentes")
for d in nombre_sent:
    r = reg_map[d["regla_id"]]
    if "nombre" not in _fold(r["limite"]) or not r["nombres"]:
        ok(False, "nombre no declarado en %s" % r["id"])
        break
else:
    ok(True, "nombre restringe la regla y se declara en el limite")
for d in decisiones:
    m = d.get("motivo") or ""
    if d["decision"] == "pendiente" and ("contradicc" in _fold(m) or "conserva la dif" in _fold(m)):
        if "nombre" not in _fold(m):
            ok(False, "contradiccion sin mencionar nombre")
            break
else:
    ok(True, "contradicciones conservadas con mencion explicita")

# ---- 7. interpretacion en memoria: positivos y negativos ----
def interpretacion(conjunto, diccionario, definicion_iri, nombre, descripcion):
    hits = [r["id"] for r in reglas
            if conjunto in r["conjuntos"] and diccionario in r["diccionarios"]
            and definicion_iri in r["definiciones"] and nombre in r["nombres"]
            and descripcion in r["descripciones"]]
    return hits[0] if len(hits) == 1 else None


for r in reglas[:60]:
    if interpretacion(r["conjuntos"][0], r["diccionarios"][0], r["definiciones"][0],
                      r["nombres"][0], r["descripciones"][0]) != r["id"]:
        ok(False, "positivo falla " + r["id"])
        break
else:
    ok(True, "positivos: 60 reglas resuelven con tupla exacta")
r0 = reglas[0]
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0],
                  "https://example.org/mex-ontologi/definition/OTRA%2F1",
                  r0["nombres"][0], r0["descripciones"][0]) is None, "negativo otra-IRI")
ok(interpretacion("OTRO-CONJUNTO", r0["diccionarios"][0], r0["definiciones"][0],
                  r0["nombres"][0], r0["descripciones"][0]) is None, "negativo contexto-mutado")
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0], r0["definiciones"][0],
                  r0["nombres"][0] + "-X", r0["descripciones"][0]) is None, "negativo solo-nombre")
ok(interpretacion(r0["conjuntos"][0], r0["diccionarios"][0], r0["definiciones"][0],
                  r0["nombres"][0], r0["descripciones"][0] + " ") is None, "negativo descripcion-alterada")
# IM vs IMN son conceptos distintos
rim = [r for r in reglas if r["id"] == "r3a10-0129"][0]
rimn = [r for r in reglas if r["id"] == "r3a10-0131"][0]
ok(rim["concepto"] != rimn["concepto"], "IM e IMN en conceptos distintos")
# codigo/nombre del mismo objeto comparten concepto con distinta representacion.
# Solo estos pares estan permitidos; cualquier otro concepto compartido es colision.
COMPARTIDOS_OK = {
    "clave-identificadora-presa", "nombre-presa-ubicacion", "cuenca-presa-ubicacion",
    "region-hidrologica-presa", "ddr-registro-pecuario", "clave-especie-pecuaria",
    "tipo-ganado-subasta", "mes-registro", "municipio-registro",
    "ddr-registro-cultivo", "mes-registro-cultivo", "municipio-registro-cultivo",
    "cultivo-registrado", "variedad-cultivo", "ddr-registro-pesquero",
    "municipio-registro-pesquero", "oficina-pesquera-registro", "especie-producida-pesca",
    "origen-produccion-pesquera", "variedad-trigo-sembrada", "superficie-sembrada-trigo-ddr",
    "clave-especie-fauna-caza",
}
for r in reglas:
    reps = {x["representacion"] for x in reglas if x["concepto"] == r["concepto"]}
    if len(reps) > 1:
        ok(r["concepto"] in COMPARTIDOS_OK, "concepto compartido no documentado " + r["concepto"])
for c in COMPARTIDOS_OK:
    rr = [r for r in reglas if r["concepto"] == c]
    if len({x["representacion"] for x in rr}) > 1 or c == "superficie-sembrada-trigo-ddr":
        ds = {x["descripciones"][0] for x in rr}
        ok(len(ds) == len(rr), "reglas del concepto compartido distinguen literales " + c)

if FALLOS:
    print("FALLOS:", len(FALLOS))
    for m in FALLOS:
        print("FAIL -", m)
    sys.exit(1)

# ---- 8. escritura de entrega ----
n_prop = sum(1 for d in decisiones if d["decision"] == "proponer")
n_pen = sum(1 for d in decisiones if d["decision"] == "pendiente")
entrega = {
    "generado_en_utc": datetime.now(timezone.utc).isoformat(),
    "agente": "territorio-economia",
    "base": "propuestas/cobertura-muse-20261023/fuentes (manifiesto 2026-10-23)",
    "alcance": "534 definiciones = 468 agente-10 + 66 agente-3 (4 familias agro/pesca); sin correspondencias columna-variable; sin sameAs/exactMatch.",
    "huellas_entrada": {
        "agente-10": sha256(FZ / "agente-10-territorio-economia/propuestas.json"),
        "agente-3": sha256(FZ / "agente-3-cobertura/propuestas.json"),
        "asignaciones": sha256(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"),
        "cobertura": sha256(ROOT / "data/semantica/cobertura.json"),
        "semantica": sha256(ROOT / "ontologia/semantica.json"),
    },
    "conteos": {
        "decisiones": len(decisiones),
        "proponer": n_prop,
        "pendiente": n_pen,
        "reglas": len(reglas),
        "conceptos_nuevos": len(nuevos),
        "calificadores_ddr": 10,
    },
    "conceptos_nuevos": nuevos,
    "reglas": reglas,
    "decisiones": decisiones,
    "limites": [
        "Ninguna regla crea correspondencias columna-variable.",
        "Ningún concepto nuevo declara sameAs ni exactMatch.",
        "Códigos sin catálogo publicado no acreditan identidad, vigencia ni adopción oficial.",
        "Metodología anterior y actual no son comparables; meses de registro no implican ocurrencia.",
        "Proyecciones: la descripción dice reconstruida y ajustada; 'proyección' viene del título del conjunto.",
        "Los 10 calificadores DDR requieren soporte del integrador antes de aplicar (pipeline actual no los propaga).",
    ],
}
with open(AQUI / "entrega.json", "w", encoding="utf-8") as f:
    json.dump(entrega, f, ensure_ascii=False, indent=1)
pent = {}
for d in decisiones:
    if d["decision"] == "pendiente":
        pent.setdefault(d["motivo"], []).append(d["definicion_iri"])
pendientes = {
    "generado_en_utc": entrega["generado_en_utc"],
    "preguntas_documentacion_faltante": [
        {"motivo": m, "definiciones": v,
         "pregunta": "Publicador: catálogo/valores/leyenda que fije el referente.",
         "documentacion_faltante": "Diccionario publicado con referente codificable."}
        for m, v in sorted(pent.items())
    ],
}
with open(AQUI / "pendientes.json", "w", encoding="utf-8") as f:
    json.dump(pendientes, f, ensure_ascii=False, indent=1)
with open(AQUI / "resultado.md", "w", encoding="utf-8") as f:
    f.write("# territorio-economia — cobertura-muse-20261023\n\n")
    f.write("Decisiones: %d (proponer %d, pendiente %d). Reglas: %d. Conceptos nuevos: %d.\n\n"
            % (len(decisiones), n_prop, n_pen, len(reglas), len(nuevos)))
    f.write("Base: 103 conceptos, 232 respaldadas, 23 candidatas iniciales, 836 revisadas, 118 candidatas: preservadas (sin correspondencias nuevas).\n\n")
    f.write("## Revision manual vs automatizacion\n\n")
    f.write("Manual: lectura literal de cada regla y definicion; 5 conceptos IMN separados de IM;\n")
    f.write("6 representaciones a no_especificada; limites de reconstruida-vs-proyeccion, conjunto-poblacion,\n")
    f.write("ejemplo incoherente y contradicciones nombre-descripcion; 10 calificadores DDR conservados.\n\n")
    f.write("Automatico: huellas manifiesto, particion 468+66 sin solapes, literales, filas por IRI,\n")
    f.write("interpretacion() con positivos y negativos, respaldo de unidades/objetos, padres validos.\n\n")
    f.write("## Pendientes\n\nQuedan %d pendientes (%d heredados A10 + %d A3) para aclaracion del publicador.\n"
            % (n_pen, sum(1 for d in a10["decisiones"] if d["decision"] == "pendiente"), 3))
with open(AQUI / "listo.json", "w", encoding="utf-8") as f:
    json.dump({"entrega": "entrega.json", "sha256": sha256(AQUI / "entrega.json"),
               "generado_en_utc": entrega["generado_en_utc"]}, f, ensure_ascii=False, indent=1)
print("OK decisiones=%d proponer=%d pendiente=%d reglas=%d nuevos=%d"
      % (len(decisiones), n_prop, n_pen, len(reglas), len(nuevos)))