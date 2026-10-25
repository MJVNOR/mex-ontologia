# -*- coding: utf-8 -*-
"""Verificador propio del agente 8 (educacion). Solo lee fuera de esta carpeta.
No toca otras propuestas concurrentes: coteja solo nucleo central + propios.
Simula interpretacion() real en memoria; no genera nada central; sin red.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/marti/Documents/MEX-Ontologi/scripts")
from consolidar_semantica import interpretacion, huella  # noqa: E402
from integrar_contenido import clave  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
CENTRO = Path("C:/Users/marti/Documents/MEX-Ontologi")
E = json.load(open(BASE / "entrega.json", encoding="utf-8"))
SEM = json.load(open(CENTRO / "ontologia/semantica.json", encoding="utf-8"))
COB = json.load(open(CENTRO / "data/semantica/cobertura.json", encoding="utf-8"))
ASIG = json.load(open(CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
MINE = {v["definicion_iri"]: v for v in ASIG["asignaciones"]["8"]["variables"]}
PEND = json.load(open(BASE / "pendientes.json", encoding="utf-8"))

ok, fail = [], []


def check(nombre, cond, detalle=""):
    (ok if cond else fail).append(nombre)
    if not cond:
        print("FALLA:", nombre, detalle)


# 1. fuentes SHA ----------------------------------------------------------------
for k, v in E["fuentes"].items():
    pth = CENTRO / v["ruta"]
    check("fuente-" + k, hashlib.sha256(open(pth, "rb").read()).hexdigest() == v["sha256"]
          and pth.stat().st_size == v["bytes"], v["ruta"])

# 2. particion completa ----------------------------------------------------------
check("n-decisiones", len(E["decisiones"]) == 126, str(len(E["decisiones"])))
check("particion", sorted(d["definicion_iri"] for d in E["decisiones"]) == sorted(MINE))
check("sin-duplicados", len({d["definicion_iri"] for d in E["decisiones"]}) == 126)
check("todas-fuera-nucleo", all(v["estado"] == "fuera_del_nucleo_actual" for v in MINE.values()))
rec = {"proponer": 99, "pendiente": 27}
for k, v in rec.items():
    check("conteo-" + k, sum(1 for d in E["decisiones"] if d["decision"] == k) == v)
check("ajuste-034", next(r for r in E["reglas"] if r["id"] == "r3a8-034")["representacion"] == "no_especificada"
      and next(r for r in E["reglas"] if r["id"] == "r3a8-034")["concepto"] == "nacionalidad-alumno"
      and any("no demuestran" in l and "10 espacios" in l for l in next(r for r in E["reglas"] if r["id"] == "r3a8-034")["limites"]))
check("ajuste-campo-codigo", all(
    (r["representacion"] == "codigo" and r["evidencia"][0]["tipo_de_dato"] == "Número entero"
     and r["evidencia"][0]["ejemplo_de_dato"] == "7" and r["evidencia"][0]["catalogo_de_referencia"]
     and "sin validar valores" in r["criterio"] and "7 con 07" in r["criterio"])
    for r in E["reglas"] if r["id"] in ("r3a8-013", "r3a8-017", "r3a8-081")))
check("ajuste-b-modalidad", E["conceptos_nuevos"]["modalidad-cursada"][1] == "Modalidad cursada según el diccionario, con dominio publicado: Escolarizada, No escolarizada o Mixta."
      and "estudiante" not in E["conceptos_nuevos"]["modalidad-cursada"][1])
check("ajuste-b-grado", E["conceptos_nuevos"]["grado-cuatrimestre-cursado"][1] == "Grado o cuatrimestre cursado según el diccionario. Denota el tramo curricular en curso."
      and "estudiante" not in E["conceptos_nuevos"]["grado-cuatrimestre-cursado"][1])
check("conteos-coinciden", E["conteos"] == {"decisiones": 126, "proponer": 99, "pendiente": 27,
                                            "reglas": 99, "conceptos_nuevos": 66})

# 3. literales + huellas recalculadas --------------------------------------------
DIC2ROWS = {}
for d in E["decisiones"]:
    if d["diccionario"] not in DIC2ROWS:
        DIC2ROWS[d["diccionario"]] = json.load(
            open(CENTRO / ("data/portal/inspecciones/%s.json" % d["diccionario"]), encoding="utf-8"))["definiciones"]
    a = MINE[d["definicion_iri"]]
    n = int(d["definicion_iri"].split("%2F")[1])
    row = DIC2ROWS[d["diccionario"]][n - 1]
    check("lit-" + str(n) + d["diccionario"][:4],
          d["variable"] == a["variable"] == (row.get("Nombre variable") or "").strip()
          and d["descripcion"] == a["descripcion"]
          and d["huella_fila_diccionario"] == a["huella_fila_diccionario"] == huella(row)
          and d["tipo_de_dato"] == (row.get("Tipo de dato") or "")
          and d["unidad_de_medida"] == (row.get("Unidad de medida") or "")
          and d["ejemplo_de_dato"] == (row.get("Ejemplo de dato") or "")
          and d["catalogo_de_referencia"] == (row.get("Catálogo de referencia") or ""),
          d["definicion_iri"])
check("sin-ufffd", all("�" not in (d["descripcion"] + d["variable"]) for d in E["decisiones"]))

# 4. reglas: forma + simulacion positiva ------------------------------------------
REGLAS = {"reglas_descripcion_exacta": SEM["reglas_descripcion_exacta"]}
for r in E["reglas"]:
    REGLAS["reglas_descripcion_exacta"].append(
        {"id": r["id"], "concepto": r["concepto"], "representacion": r["representacion"],
         "descripciones": r["descripciones"], "nombres": r["nombres"],
         "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"],
         "definiciones": r["definiciones"]})
check("n-reglas", len(E["reglas"]) == 99, str(len(E["reglas"])))
check("ids-unicos", len({r["id"] for r in E["reglas"]}) == 99)
check("listas-unitarias", all(
    len(r["nombres"]) == 1 and len(r["descripciones"]) == 1 and len(r["conjuntos"]) == 1
    and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1 for r in E["reglas"]))
check("evidencia-huella", all(
    r["huella_fila_diccionario"] == r["evidencia"][0]["huella_fila_diccionario"]
    == next(d["huella_fila_diccionario"] for d in E["decisiones"]
            if d["definicion_iri"] == r["definiciones"][0]) for r in E["reglas"]))
check("fuente-revision-propia", all(
    r["fuente_revision"] == "propuestas/cobertura-muse-20261023/educacion/entrega.json"
    and r["evidencia"] for r in E["reglas"]))
check("sin-columnas", "file-column" not in json.dumps(E["reglas"]))
check("sin-sameas", "sameAs" not in json.dumps(
    {"r": E["reglas"], "c": E["conceptos_nuevos"], "d": E["decisiones"]}))
check("conceptos-nuevos-66", len(E["conceptos_nuevos"]) == 66)
check("sin-colision-nucleo", not (set(E["conceptos_nuevos"]) & set(SEM["conceptos"])))
check("conceptos-forma", all(isinstance(v, list) and len(v) == 3 for v in E["conceptos_nuevos"].values()))
check("broader-ok", all(v[2] is None or v[2] in SEM["conceptos"] or v[2] in E["conceptos_nuevos"]
                        for v in E["conceptos_nuevos"].values()))
check("reutilizados-nucleo", all(c in SEM["conceptos"] for c in E["conceptos_reutilizados"]))
check("calificadores-20", sum(1 for r in E["reglas"] if "calificador" in r) == 20)
check("calificador-literal", all(
    r["calificador"] == {"sede": r["nombres"][0]} and r["nombres"][0] in r["descripciones"][0]
    for r in E["reglas"] if "calificador" in r))
check("unidades-literales", all(
    r["evidencia"][0]["unidad_de_medida"] == next(
        d["unidad_de_medida"] for d in E["decisiones"] if d["definicion_iri"] == r["definiciones"][0])
    for r in E["reglas"]))

n_pos = 0
for d in E["decisiones"]:
    if d["decision"] != "proponer":
        continue
    g = interpretacion(d["variable"], d["descripcion"], d["conjunto"], REGLAS,
                       d["diccionario"], d["definicion_iri"])
    if g["estado"] == "respaldada_por_definicion" and g["concepto"] == d["concepto"] \
            and g["regla"] == d["regla_id"]:
        n_pos += 1
    else:
        check("pos-" + d["regla_id"], False, str(g))
check("n-positivos", n_pos == 99, str(n_pos))

# 5. negativos --------------------------------------------------------------------
d0 = next(d for d in E["decisiones"] if d["decision"] == "proponer")


def no_r3(g):
    return g["estado"] != "respaldada_por_definicion" or not str(g.get("regla", "")).startswith("r3a8-")


check("N1-solo-nombre", no_r3(interpretacion(
    d0["variable"], "Texto libre sin relación alguna", d0["conjunto"], REGLAS, d0["diccionario"], d0["definicion_iri"])))
check("N2-contexto-mutado", no_r3(interpretacion(
    d0["variable"], d0["descripcion"], "00000000-0000-4000-8000-000000000000", REGLAS, d0["diccionario"], d0["definicion_iri"])))
check("N3-otra-iri", no_r3(interpretacion(
    d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS, d0["diccionario"], d0["definicion_iri"] + "X")))
check("N4-dic-distinto", no_r3(interpretacion(
    d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS, "00000000-0000-4000-8000-000000000000", d0["definicion_iri"])))
ca = next(d for d in E["decisiones"] if d["variable"] == "Plan de Estudio")
cb = next(d for d in E["decisiones"] if d["variable"] == "Clave de Formación Académica")
check("N5-codigos-no-equivalentes",
      no_r3(interpretacion(ca["variable"], cb["descripcion"], ca["conjunto"], REGLAS, ca["diccionario"], ca["definicion_iri"]))
      and no_r3(interpretacion(cb["variable"], ca["descripcion"], cb["conjunto"], REGLAS, cb["diccionario"], cb["definicion_iri"])))
ident = {"municipio", "entidad", "localidad", "territorio", "escuela", "unidad-salud", "organizacion"}
check("N5b-clave-sin-identidad", all(
    interpretacion(d["variable"], d["descripcion"], d["conjunto"], REGLAS, d["diccionario"], d["definicion_iri"])["concepto"] not in ident
    for d in E["decisiones"] if d["decision"] == "proponer" and "clave" in clave(d["descripcion"])))
pen = next(d for d in E["decisiones"] if d["variable"] == "Alumno")
check("N6-pendiente-sin-regla", no_r3(interpretacion(
    pen["variable"], pen["descripcion"], pen["conjunto"], REGLAS, pen["diccionario"], pen["definicion_iri"])))
check("N7-columna-no-definicion", no_r3(interpretacion(
    d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS, d0["diccionario"],
    "https://example.org/mex-ontologi/file-column/abc%2F1")))
cand23 = [x for x in COB["variables"] if x["estado"] == "candidata_sin_definicion_suficiente"]
check("n-candidatas-23", len(cand23) == 23, str(len(cand23)))
toc = [x["definicion_iri"] for x in cand23
       if not no_r3(interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], REGLAS,
                                   x["diccionario"], x["definicion_iri"]))]
check("N8-candidatas-intactas", not toc, str(toc))

# 6. no-regresion 232 respaldadas ----------------------------------------------------
CENTRAL = {"reglas_descripcion_exacta": SEM["reglas_descripcion_exacta"]}
mal = []
for x in COB["variables"]:
    if x["estado"] != "respaldada_por_definicion":
        continue
    g = interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], REGLAS,
                       x["diccionario"], x["definicion_iri"])
    g0 = interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], CENTRAL,
                        x["diccionario"], x["definicion_iri"])
    if g != g0:
        mal.append(x["definicion_iri"])
check("no-regresion-232", not mal, str(mal[:3]))
n_resp = sum(1 for x in COB["variables"] if x["estado"] == "respaldada_por_definicion"
             and interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], REGLAS,
                                x["diccionario"], x["definicion_iri"])["estado"] == "respaldada_por_definicion")
check("respaldadas-232-absoluto", n_resp == 232, str(n_resp))

# 7. pendientes.json ------------------------------------------------------------------
check("n-pendientes", len(PEND) == 27, str(len(PEND)))
check("pendientes-coinciden", sorted(p["definicion_iri"] for p in PEND) == sorted(
    d["definicion_iri"] for d in E["decisiones"] if d["decision"] == "pendiente"))
check("pendientes-forma", all(
    set(p) >= {"definicion_iri", "variable", "descripcion", "motivo", "documentacion_faltante"} for p in PEND))

print("PASS=%d FAIL=%d" % (len(ok), len(fail)))
sys.exit(1 if fail else 0)
