# -*- coding: utf-8 -*-
"""Verificador propio del agente 8 (ronda 3). Solo lee fuera de esta carpeta.

Reproduce y comprueba: huellas, particion exacta, literales byte-exactos,
simulacion con interpretacion() real del pipeline (positivos), 8 negativos
reales, no-regresion de las 232 respaldadas, y limites (sin sameAs, sin
columnas, sin colisiones, sin U+FFFD, sin unidades inventadas).
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, "C:/Users/marti/Documents/MEX-Ontologi/scripts")
from consolidar_semantica import interpretacion, huella  # noqa: E402 (funciones puras)
from integrar_contenido import clave  # noqa: E402 (funcion pura)

BASE = Path(__file__).resolve().parent.parent
CENTRO = Path("C:/Users/marti/Documents/MEX-Ontologi")
P = json.load(open(BASE / "propuestas.json", encoding="utf-8"))
SEM = json.load(open(CENTRO / "ontologia/semantica.json", encoding="utf-8"))
COB = json.load(open(CENTRO / "data/semantica/cobertura.json", encoding="utf-8"))
ASIG = json.load(open(CENTRO / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
MINE = ASIG["asignaciones"]["8"]["variables"]
INSP = {r["iri"]: r for r in json.load(open(BASE / "fuente/inspeccion-126.json", encoding="utf-8"))}

ok = []
fail = []


def check(nombre, cond, detalle=""):
    (ok if cond else fail).append(nombre)
    if not cond:
        print("FALLA:", nombre, detalle)


# 1. huellas de entrada -----------------------------------------------------
for k, v in P["huellas_entrada"].items():
    pth = CENTRO / v["ruta"]
    h = hashlib.sha256(open(pth, "rb").read()).hexdigest()
    check("huella-" + k, h == v["sha256"] and pth.stat().st_size == v["bytes"], v["ruta"])
check("n-huellas", len(P["huellas_entrada"]) == 4)

# 2. particion exacta --------------------------------------------------------
iris = [v["definicion_iri"] for v in MINE]
check("n-asignadas", len(iris) == 126, str(len(iris)))
check("sin-duplicados", len(set(iris)) == 126)
dec_iris = [d["definicion_iri"] for d in P["decisiones"]]
check("particion-completa", sorted(dec_iris) == sorted(iris))
check("sin-duplicados-dec", len(set(dec_iris)) == 126)
check("todas-fuera-nucleo", all(v["estado"] == "fuera_del_nucleo_actual" for v in MINE))
pend = json.load(open(CENTRO / "reports/pendientes-semanticos.json", encoding="utf-8"))
pend_by_iri = {x["definicion_iri"]: x for x in pend["variables_pendientes"]}
check("pendientes-coinciden", all(i in pend_by_iri for i in iris))

# 3. literales byte-exactos + huellas de fila recalculadas -------------------
asig_by = {v["definicion_iri"]: v for v in MINE}
for d in P["decisiones"]:
    a = asig_by[d["definicion_iri"]]
    r = INSP[d["definicion_iri"]]
    check("lit-" + d["definicion_iri"].split("%2F")[1] + d["diccionario"][:4],
          d["variable"] == a["variable"] == r["var"] and d["descripcion"] == a["descripcion"] == r["desc"]
          and d["huella_fila_diccionario"] == a["huella_fila_diccionario"] == r["huella"]
          and d["tipo_de_dato"] == r["tipo"] and d["unidad_de_medida"] == r["unidad"]
          and d["catalogo_de_referencia"] == r["catalogo"] and d["ejemplo_de_dato"] == r["ejemplo"],
          d["definicion_iri"])
# huella de fila recalculada con la funcion central desde la inspeccion cruda
DIC2ROWS = {}
for dic in sorted({v["diccionario"] for v in MINE}):
    DIC2ROWS[dic] = json.load(open(CENTRO / ("data/portal/inspecciones/%s.json" % dic), encoding="utf-8"))["definiciones"]
for iri in iris:
    a = asig_by[iri]
    n = int(iri.split("%2F")[1])
    row = DIC2ROWS[a["diccionario"]][n - 1]
    check("huella-recalc-" + iri.split("%2F")[1] + a["diccionario"][:4],
          huella(row) == a["huella_fila_diccionario"], iri)
# sin dano U+FFFD en los 126 literales
check("sin-ufffd", all("�" not in (r["desc"] + r["var"]) for r in INSP.values()))

# 4. reglas: forma y simulacion positiva --------------------------------------
REGLAS = {"reglas_descripcion_exacta": SEM["reglas_descripcion_exacta"] + P["reglas"]}
check("n-reglas", len(P["reglas"]) == 99, str(len(P["reglas"])))
check("ids-r3a8-unicos", len({r["id"] for r in P["reglas"]}) == 99
      and all(r["id"].startswith("r3a8-") for r in P["reglas"]))
check("conceptos-nuevos-66", len(P["conceptos_nuevos"]) == 66, str(len(P["conceptos_nuevos"])))
check("sin-colision-conceptos",
      not (set(P["conceptos_nuevos"]) & set(SEM["conceptos"])))
check("broader-existentes", all(
    (v[2] is None or v[2] in SEM["conceptos"] or v[2] in P["conceptos_nuevos"])
    for v in P["conceptos_nuevos"].values()))
check("sin-sameas", "sameAs" not in json.dumps({"r": P["reglas"], "c": P["conceptos_nuevos"],
      "d": P["decisiones"]}) and "exactMatch" not in json.dumps(P["reglas"]))
check("sin-columnas", "file-column" not in json.dumps(P))
check("reutilizado-existe", all(c in SEM["conceptos"] for c in P["conceptos_reutilizados"]))
for r in P["reglas"]:
    check("forma-" + r["id"],
          set(r) >= {"id", "concepto", "representacion", "descripciones", "nombres",
                     "conjuntos", "diccionarios", "definiciones", "criterio", "evidencia"}
          and len(r["descripciones"]) == 1 and len(r["nombres"]) == 1
          and len(r["conjuntos"]) == 1 and len(r["diccionarios"]) == 1 and len(r["definiciones"]) == 1
          and len(r["evidencia"]) == 1 and r["representacion"] in
          {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"},
          r["id"])
# positivos: cada definicion propuesta dispara su regla con su concepto
n_pos = 0
for d in P["decisiones"]:
    if d["decision"] != "propuesta":
        continue
    got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], REGLAS,
                         d["diccionario"], d["definicion_iri"])
    check("pos-" + d["regla_id"],
          got["estado"] == "respaldada_por_definicion" and got["concepto"] == d["concepto"]
          and got["regla"] == d["regla_id"], str(got))
    n_pos += 1
check("n-positivos", n_pos == 99, str(n_pos))

# 5. negativos reales ----------------------------------------------------------
def interp(*a):
    return interpretacion(*a, REGLAS if len(a) > 3 else REGLAS)


d0 = next(d for d in P["decisiones"] if d["decision"] == "propuesta")
# N1 solo-nombre: mismo nombre/conjunto/dic/iri pero descripcion ajena
n1 = interpretacion(d0["variable"], "Texto libre sin relación alguna", d0["conjunto"], REGLAS,
                    d0["diccionario"], d0["definicion_iri"])
check("N1-solo-nombre", n1["estado"] != "respaldada_por_definicion"
      or not str(n1.get("regla", "")).startswith("r3a8-"), str(n1))
# N2 contexto-mutado: literal exacto pero conjunto distinto
n2 = interpretacion(d0["variable"], d0["descripcion"], "00000000-0000-4000-8000-000000000000",
                    REGLAS, d0["diccionario"], d0["definicion_iri"])
check("N2-contexto-mutado", n2["estado"] != "respaldada_por_definicion"
      or not str(n2.get("regla", "")).startswith("r3a8-"), str(n2))
# N3 otra-IRI: todo exacto salvo la IRI de definicion
otra = d0["definicion_iri"].replace("%2F", "%2F999")
n3 = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS,
                    d0["diccionario"], otra)
check("N3-otra-iri", n3["estado"] != "respaldada_por_definicion"
      or not str(n3.get("regla", "")).startswith("r3a8-"), str(n3))
# N4 diccionario-distinto
n4 = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS,
                    "00000000-0000-4000-8000-000000000000", d0["definicion_iri"])
check("N4-diccionario-distinto", n4["estado"] != "respaldada_por_definicion"
      or not str(n4.get("regla", "")).startswith("r3a8-"), str(n4))
# N5 codigos no equivalentes: descripciones cruzadas entre 'Clave ...' no matchean
cod_a = next(d for d in P["decisiones"] if d["variable"] == "Plan de Estudio")
cod_b = next(d for d in P["decisiones"] if d["variable"] == "Clave de Formación Académica")
n5a = interpretacion(cod_a["variable"], cod_b["descripcion"], cod_a["conjunto"], REGLAS,
                     cod_a["diccionario"], cod_a["definicion_iri"])
n5b = interpretacion(cod_b["variable"], cod_a["descripcion"], cod_b["conjunto"], REGLAS,
                     cod_b["diccionario"], cod_b["definicion_iri"])
check("N5-codigos-no-equivalentes",
      (n5a["estado"] != "respaldada_por_definicion" or not str(n5a.get("regla", "")).startswith("r3a8-"))
      and (n5b["estado"] != "respaldada_por_definicion" or not str(n5b.get("regla", "")).startswith("r3a8-")),
      str((n5a, n5b)))
# N5b catalogo no acreditado: ninguna regla cuya DESCRIPCION hable de clave
# resuelve a concepto de identidad central
ident = {"municipio", "entidad", "localidad", "territorio", "escuela", "unidad-salud", "organizacion"}
check("N5b-clave-sin-identidad",
      all(interpretacion(d["variable"], d["descripcion"], d["conjunto"], REGLAS,
                         d["diccionario"], d["definicion_iri"])["concepto"] not in ident
          for d in P["decisiones"] if d["decision"] == "propuesta" and "clave" in clave(d["descripcion"])))
# N6 pendiente sin regla: descripcion vacia/generica no dispara propuesta
pen = next(d for d in P["decisiones"] if d["variable"] == "Alumno")
n6 = interpretacion(pen["variable"], pen["descripcion"], pen["conjunto"], REGLAS,
                    pen["diccionario"], pen["definicion_iri"])
check("N6-pendiente-sin-regla", n6["estado"] != "respaldada_por_definicion"
      or not str(n6.get("regla", "")).startswith("r3a8-"), str(n6))
# N7 IRI de columna fisica no dispara regla de definicion
n7 = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], REGLAS, d0["diccionario"],
                    "https://example.org/mex-ontologi/file-column/abc%2F1")
check("N7-columna-no-definicion", n7["estado"] != "respaldada_por_definicion"
      or not str(n7.get("regla", "")).startswith("r3a8-"), str(n7))
# N8 los 23 candidatos del agente 4 no los toca ninguna regla r3a8
cand23 = [x for x in COB["variables"] if x["estado"] == "candidata_sin_definicion_suficiente"]
check("n-candidatas-23", len(cand23) == 23, str(len(cand23)))
tocadas = []
for x in cand23:
    g = interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], REGLAS,
                       x["diccionario"], x["definicion_iri"])
    if g["estado"] == "respaldada_por_definicion" and str(g.get("regla", "")).startswith("r3a8-"):
        tocadas.append(x["definicion_iri"])
check("N8-agente4-intacto", not tocadas, str(tocadas))

# 6. no-regresion: las 232 respaldadas resuelven igual --------------------------
mal = []
for x in COB["variables"]:
    if x["estado"] != "respaldada_por_definicion":
        continue
    g = interpretacion(x["variable"], x.get("descripcion", ""), x["conjunto"], REGLAS,
                       x["diccionario"], x["definicion_iri"])
    if g != {"estado": "respaldada_por_definicion", "concepto": x["concepto"],
             "regla": x["regla"], "representacion": x["representacion"]}:
        mal.append((x["definicion_iri"], g))
check("no-regresion-232", not mal, str(mal[:3]))

# 7. unidades no inventadas + huella en evidencia + aritmetica ------------------
check("unidades-literales", all(
    r["evidencia"][0]["unidad_de_medida"] == INSP[r["definiciones"][0]]["unidad"]
    for r in P["reglas"]))
check("evidencia-con-huella", all(
    r["evidencia"][0].get("huella_fila_diccionario") == INSP[r["definiciones"][0]]["huella"]
    and r["evidencia"][0]["huella_fila_diccionario"] == next(
        d["huella_fila_diccionario"] for d in P["decisiones"]
        if d["definicion_iri"] == r["definiciones"][0])
    for r in P["reglas"]))
check("aritmetica", P["requisitos_integracion"]["aritmetica_simulada"] == {
    "respaldadas": 232 + 99, "fuera_del_nucleo": 1308 - 99, "candidatas_agente4": 23,
    "conceptos": 103 + 66, "revisadas_intactas": 836, "candidatas_columna": 118})

print("PASS=%d FAIL=%d" % (len(ok), len(fail)))
sys.exit(1 if fail else 0)
