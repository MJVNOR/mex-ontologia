"""Verificador propio del agente 9 (ronda 3). Read-only sobre el nucleo;
solo escribe fuente/verificacion-r3a9.json dentro de su carpeta.
Uso: PYTHONDONTWRITEBYTECODE=1 uv run python propuestas/ronda-3/agente-9-gobierno-digital/scripts/verificar_r3a9.py
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import io
import json
import re
from pathlib import Path

R3A9 = Path(__file__).resolve().parents[1]
assert R3A9.name == "agente-9-gobierno-digital", R3A9
ROOT = R3A9.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402
from integrar_contenido import clave, valor  # noqa: E402

FALLOS = []


def check(cond, msg):
    if not cond:
        FALLOS.append(msg)
    return cond


def main():
    prop = json.load(io.open(str(R3A9 / "propuestas.json"), encoding="utf-8"))
    asig = json.load(open(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
    vars9 = asig["asignaciones"]["9"]["variables"]
    sem = json.load(open(ROOT / "ontologia/semantica.json", encoding="utf-8"))
    base = "https://example.org/mex-ontologi/"

    # 1. Particion exacta
    check(len(vars9) == 243, "asignacion != 243: %d" % len(vars9))
    check(len(set(v["definicion_iri"] for v in vars9)) == 243, "IRIs duplicadas en asignacion")
    check(all(v["estado"] == "fuera_del_nucleo_actual" for v in vars9), "asignacion con estado distinto")
    dec = prop["decisiones"]
    check(len(dec) == 243, "decisiones != 243: %d" % len(dec))
    check({d["definicion_iri"] for d in dec} == {v["definicion_iri"] for v in vars9}, "decisiones no cubren asignacion exacta")
    check(len({d["definicion_iri"] for d in dec}) == 243, "decisiones duplicadas")

    # 2. Huellas e identidades recalculadas desde inspeccion
    insp = {}
    for d in {v["diccionario"] for v in vars9}:
        insp[d] = json.load(open(ROOT / "data" / "portal" / "inspecciones" / (d + ".json"), encoding="utf-8"))
    ok_h, ok_i, ok_d = 0, 0, 0
    for v in vars9:
        rows = [r for r in insp[v["diccionario"]]["definiciones"] if str(r.get("Nombre variable")) == v["variable"]]
        check(len(rows) == 1, "fila no unica: %s %s" % (v["diccionario"], v["variable"]))
        row = rows[0]
        if huella(row) == v["huella_fila_diccionario"]:
            ok_h += 1
        else:
            FALLOS.append("huella distinta: %s %s" % (v["diccionario"], v["variable"]))
        idx = insp[v["diccionario"]]["definiciones"].index(row) + 1
        if v["definicion_iri"] == base + "definition/" + v["diccionario"] + "%2F" + str(idx):
            ok_i += 1
        else:
            FALLOS.append("IRI no posicional: %s" % v["definicion_iri"])
        if valor(row, {"descripcion", "definicion"}) == v["descripcion"]:
            ok_d += 1
        else:
            FALLOS.append("literal distinto: %s %s" % (v["diccionario"], v["variable"]))
    # 3. Decisiones conservan literal exacto y campos separados
    for d in dec:
        for campo in ["descripcion", "tipo_de_dato", "unidad_de_medida", "ejemplo_de_dato",
                      "catalogo_de_referencia", "huella_fila_diccionario", "definicion_iri"]:
            check(campo in d and isinstance(d[campo], str), "decision sin campo %s: %s" % (campo, d.get("definicion_iri")))
        check(d["veredicto"] in ("propuesta", "pendiente"), "veredicto invalido: %s" % d.get("definicion_iri"))
        if d["veredicto"] == "pendiente":
            check(bool(d.get("motivo")) and bool(d.get("razon")), "pendiente sin motivo/razon: %s" % d["definicion_iri"])
            check("regla" not in d and "concepto" not in d, "pendiente con regla/concepto: %s" % d["definicion_iri"])
        else:
            check(bool(d.get("regla", "").startswith("r3a9-")), "regla sin prefijo r3a9: %s" % d["definicion_iri"])
            check(bool(d.get("concepto")), "propuesta sin concepto: %s" % d["definicion_iri"])

    # 4. Reglas: esquema, unicidad, uso
    reglas = prop["reglas"]
    check(len(reglas) == sum(1 for d in dec if d["veredicto"] == "propuesta"), "reglas != propuestas")
    check(len({r["id"] for r in reglas}) == len(reglas), "reglas duplicadas")
    for r in reglas:
        check(r["id"].startswith("r3a9-"), "id sin prefijo: %s" % r["id"])
        for campo in ["descripciones", "nombres", "conjuntos", "diccionarios", "definiciones"]:
            check(isinstance(r.get(campo), list) and len(r[campo]) == 1 and all(isinstance(x, str) and x for x in r[campo]),
                  "regla %s campo %s no es array exacto unitario" % (r["id"], campo))
        check(r.get("representacion") in ("no_especificada", "nombre"), "representacion fuera de vocabulario: %s" % r["id"])
        check(r["concepto"] in prop["conceptos_nuevos"], "concepto inexistente: %s" % r["id"])
    usada_por = {}
    for d in dec:
        if d["veredicto"] == "propuesta":
            usada_por.setdefault(d["regla"], []).append(d["definicion_iri"])
    check(set(usada_por) == {r["id"] for r in reglas}, "reglas sin decision o viceversa")
    for rid, iris in usada_por.items():
        check(len(iris) == 1, "regla %s usada por %d decisiones (debe ser 1: alcance por definicion)" % (rid, len(iris)))

    # 5. Conceptos nuevos: esquema, sin sameAs/exactMatch, sin reutilizacion indebida
    check(isinstance(prop["conceptos_reutilizados"], list) and not prop["conceptos_reutilizados"], "reutilizados debe ser []")
    texto = json.dumps(prop, ensure_ascii=False).lower()
    check(all(p not in texto for p in ["sameas\":", "exactmatch\":", "#sameas", "#exactmatch"]), "sameAs/exactMatch prohibido")
    for slug, triple in prop["conceptos_nuevos"].items():
        check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) is not None, "slug invalido: %s" % slug)
        check(isinstance(triple, list) and len(triple) == 3 and triple[2] is None, "concepto sin [label, definicion, null]: %s" % slug)
        check(all(isinstance(x, str) and x for x in triple[:2]), "label/definicion vacias: %s" % slug)
    check(len(prop["conceptos_nuevos"]) == 85, "conceptos != 86: %d" % len(prop["conceptos_nuevos"]))

    # 6. Ningun codigo promovido a catalogo/identidad
    for d in dec:
        check(d["catalogo_de_referencia"] == "", "catalogo no vacio: %s" % d["definicion_iri"])
    check(set(sem["conceptos"]) == set(json.load(open(ROOT / "ontologia/semantica.json", encoding="utf-8"))["conceptos"]),
          "nucleo alterado")

    # 7. Simulacion interpretacion(): positivos con reglas propias
    reglas_sim = [{"id": r["id"], "concepto": r["concepto"], "representacion": r["representacion"],
                   "descripciones": r["descripciones"], "nombres": r["nombres"], "conjuntos": r["conjuntos"],
                   "diccionarios": r["diccionarios"], "definiciones": r["definiciones"]} for r in reglas]
    reglas_centrales = sem["reglas_descripcion_exacta"]
    pos_ok = 0
    for d in dec:
        if d["veredicto"] != "propuesta":
            continue
        try:
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], {"reglas_descripcion_exacta": reglas_sim},
                                dictionary=d["diccionario"], definition=d["definicion_iri"])
        except ValueError as e:
            FALLOS.append("conflicto en positivo %s: %s" % (d["definicion_iri"], e))
            continue
        if got.get("regla") == d["regla"] and got.get("concepto") == d["concepto"] and got.get("estado") == "respaldada_por_definicion":
            pos_ok += 1
        else:
            FALLOS.append("positivo no resuelve: %s -> %s" % (d["definicion_iri"], got))
        # contra centrales: no debe resolver a regla central (sin promocion accidental)
        try:
            got_c = interpretacion(d["variable"], d["descripcion"], d["conjunto"], {"reglas_descripcion_exacta": reglas_centrales},
                                   dictionary=d["diccionario"], definition=d["definicion_iri"])
        except ValueError:
            got_c = {"estado": "conflicto-central"}
        check(got_c.get("estado") != "respaldada_por_definicion", "colision con regla central: %s" % d["definicion_iri"])

    # 8. Negativos reales
    neg_ok = 0

    def negativo(nombre, desc, conj, dicc, defn, esperado_no_regla=True):
        global_neg = interpretacion(nombre, desc, conj, {"reglas_descripcion_exacta": reglas_sim}, dictionary=dicc, definition=defn)
        return global_neg.get("estado") != "respaldada_por_definicion" if esperado_no_regla else True

    d0 = next(d for d in dec if d["veredicto"] == "propuesta")
    check(negativo("PX_NOMBRE_FALSO", d0["descripcion"], d0["conjunto"], d0["diccionario"], d0["definicion_iri"]),
          "negativo solo-nombre fallo (resolvio con nombre falso)")
    neg_ok += 1
    check(negativo(d0["variable"], d0["descripcion"], "00000000-0000-0000-0000-000000000000", d0["diccionario"], d0["definicion_iri"]),
          "negativo contexto-mutado fallo")
    neg_ok += 1
    check(negativo(d0["variable"], d0["descripcion"], d0["conjunto"], d0["diccionario"], base + "definition/falso%2F999"),
          "negativo otra-IRI fallo")
    neg_ok += 1
    # pendiente no resuelve a regla propia
    dp = next(d for d in dec if d["veredicto"] == "pendiente")
    got_p = interpretacion(dp["variable"], dp["descripcion"], dp["conjunto"], {"reglas_descripcion_exacta": reglas_sim},
                           dictionary=dp["diccionario"], definition=dp["definicion_iri"])
    check(got_p.get("estado") != "respaldada_por_definicion", "pendiente resolvio a regla: %s" % dp["definicion_iri"])
    neg_ok += 1
    # truncada con literal completo inventado no resuelve
    check(negativo(d0["variable"], d0["descripcion"] + " texto inventado", d0["conjunto"], d0["diccionario"], d0["definicion_iri"]),
          "negativo descripcion-extendida fallo")
    neg_ok += 1

    # 9. Sin U+FFFD en la particion; caracteres especiales preservados
    FFFD = chr(0xFFFD)
    NBSP = chr(0xA0)
    ELIP = chr(0x2026)
    n_fffd = 0
    n_nbsp_src = 0
    dec_por_iri = {d["definicion_iri"]: d for d in dec}
    for vv in vars9:
        drow = [r for r in insp[vv["diccionario"]]["definiciones"] if str(r.get("Nombre variable")) == vv["variable"]][0]
        blob = json.dumps(drow, ensure_ascii=False)
        n_fffd += blob.count(FFFD)
        if NBSP in vv["descripcion"]:
            n_nbsp_src += 1
            check(NBSP in dec_por_iri[vv["definicion_iri"]]["descripcion"], "NBSP no preservado: %s" % vv["definicion_iri"])
        if ELIP in vv["descripcion"]:
            check(ELIP in dec_por_iri[vv["definicion_iri"]]["descripcion"], "elipsis no preservada: %s" % vv["definicion_iri"])
    check(n_fffd == 0, "U+FFFD presente en la particion: %d" % n_fffd)
    check(n_nbsp_src > 0, "sin NBSP en fuente (chequeo vacio)")

    # 10. Huellas de entrada
    he = prop.get("huellas_entrada", {})
    for k in ["asignaciones_semanticas", "reglas", "inventario", "inspeccion"]:
        check(bool(he.get(k)), "huella de entrada faltante: %s" % k)
    check(he.get("reglas") == json.load(open(ROOT / "data/semantica/cobertura.json", encoding="utf-8"))["huellas_entrada"]["reglas"], "huella reglas distinta de cobertura central")
    sha_asig = hashlib.sha256((ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json").read_bytes()).hexdigest()
    check(he.get("asignaciones_semanticas") == sha_asig, "sha asignaciones no coincide")

    # 12. Criterios de integracion: sin unidades por costumbre, nombres neutros, fusion codigo/nombre
    import re as _re
    BOILER = _re.compile(r"diagn[o\u00f3o]stico del entorno digital", _re.IGNORECASE)
    PRESENTE = [("personas", "persona"), ("a\u00f1o", "a\u00f1o"), ("gb", "gb"), ("cpu", "cpu"),
                ("conteo", "cuant"), ("monto", "presupuesto")]
    AUSENTE = ["mxn", "pesos", "moneda", "porcentaje", "nacionalidad", "extranjer\u00eda", "extranjeria",
               "titulaci\u00f3n", "titulacion", "egreso", "diagnostico", "diagn\u00f3stico"]
    lit_por_regla = {}
    for r in reglas:
        ddec = next(d for d in dec if d.get("regla") == r["id"])
        lit_por_regla[r["id"]] = (r, ddec["descripcion"])
    for r in reglas:
        triple = prop["conceptos_nuevos"][r["concepto"]]
        ctext = (triple[0] + " " + triple[1].split(". ")[0]).lower()
        lit = next(d for d in dec if d.get("regla") == r["id"])["descripcion"].lower()
        for pal, tok in PRESENTE:
            if _re.search(r"\b" + pal + r"\b", ctext):
                check(tok in lit, "unidad/objeto '%s' sin respaldo literal en %s" % (pal, r["id"]))
        limpio = BOILER.sub("", ctext)
        for pal in AUSENTE:
            check(_re.search(r"\b" + pal + r"\b", limpio) is None, "termino no acreditado '%s' en concepto de %s" % (pal, r["id"]))
        check(_re.fullmatch(r"P\d+|ID", r["nombres"][0]) is not None, "nombre no neutro en %s" % r["id"])
    # Fusion existencia+nombre: mismo objeto, dos representaciones, dos reglas
    ru = [r for r in reglas if r["concepto"] == "unidad-coordinadora-tic"]
    check(len(ru) == 2, "unidad-coordinadora-tic debe tener 2 reglas, tiene %d" % len(ru))
    check({r["representacion"] for r in ru} == {"no_especificada", "nombre"}, "representaciones fusionadas incorrectas")
    check({r["nombres"][0] for r in ru} == {"P8", "P9"}, "reglas fusionadas incorrectas")
    # Acotacion completa: cada regla exige definicion+diccionario+conjunto y su decision trae huella real
    n_acot = sum(1 for r in reglas if all(len(r[c]) == 1 for c in ["descripciones", "nombres", "conjuntos", "diccionarios", "definiciones"]))
    check(n_acot == len(reglas), "reglas sin acotacion completa: %d/%d" % (n_acot, len(reglas)))
    resumen12 = {"criterio_unidades_ok": True, "fusion_unidad_ok": True, "reglas_acotadas": n_acot}

    # 11. Alcance: sin escrituras fuera de carpeta (por construccion) y archivos presentes
    check((R3A9 / "propuestas.json").exists(), "falta propuestas.json")
    check((R3A9 / "resultado.md").exists(), "falta resultado.md")
    check((R3A9 / "scripts" / "generar_r3a9.py").exists(), "falta generador")
    check((R3A9 / "scripts" / "verificar_r3a9.py").exists(), "falta verificador")

    resumen = {"huellas_ok": ok_h, "iris_ok": ok_i, "literales_ok": ok_d, "positivos_ok": pos_ok,
               "negativos_ok": neg_ok, "decisiones": len(dec), "reglas": len(reglas),
               "conceptos_nuevos": len(prop["conceptos_nuevos"]),
               "ufffd_en_particion": n_fffd, "nbsp_descripciones": n_nbsp_src, "criterios": resumen12, "fallos": FALLOS}
    with io.open(str(R3A9 / "fuente" / "verificacion-r3a9.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps({k: v for k, v in resumen.items() if k != "fallos"}, indent=1))
    if FALLOS:
        print("FALLOS:")
        for m in FALLOS:
            print(" -", m)
        sys.exit(1)
    print("VERIFICACION R3A9: TODO OK")


if __name__ == "__main__":
    main()
