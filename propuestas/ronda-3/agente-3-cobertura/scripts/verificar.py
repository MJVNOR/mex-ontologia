"""Verifica la entrega del agente 3 (ronda 3) contra las fuentes reales.

Solo LEE fuera de su carpeta; no escribe fuera. Sin red. Requiere las
dependencias del proyecto (rdflib) para reutilizar clave() e
interpretacion() del pipeline central.

Uso desde la raiz:
  uv run python propuestas/ronda-3/agente-3-cobertura/scripts/verificar.py

Sale con codigo != 0 si alguna comprobacion falla, incluidos los negativos.
"""
import hashlib
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ROOT = AQUI.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from integrar_contenido import clave  # noqa: E402
from consolidar_semantica import interpretacion, columnas  # noqa: E402

FALLOS = []


def ok(cond, mensaje):
    print(("PASS " if cond else "FAIL ") + mensaje)
    if not cond:
        FALLOS.append(mensaje)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    prop = json.loads((AQUI / "propuestas.json").read_text(encoding="utf-8"))
    inv = json.loads((AQUI / "inventario-cobertura.json").read_text(encoding="utf-8"))
    fuen = json.loads((AQUI / "fuente" / "huellas.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports" / "pendientes-semanticos.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data" / "semantica" / "cobertura.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia" / "semantica.json").read_text(encoding="utf-8"))

    # 1. huellas reales
    reales = {"pendientes": sha(ROOT / "reports" / "pendientes-semanticos.json"),
              "cobertura": sha(ROOT / "data" / "semantica" / "cobertura.json"),
              "semantica": sha(ROOT / "ontologia" / "semantica.json"),
              "inventario": sha(ROOT / "data" / "portal" / "inventario.json"),
              "inspeccion": sha(ROOT / "data" / "portal" / "contenido-inspeccion.json")}
    ok(fuen["insumos"] and all(
        next(i["sha256"] for i in fuen["insumos"] if i["ruta"].endswith(k)) == v
        for k, v in {"pendientes-semanticos.json": reales["pendientes"],
                     "cobertura.json": reales["cobertura"],
                     "semantica.json": reales["semantica"],
                     "inventario.json": reales["inventario"],
                     "contenido-inspeccion.json": reales["inspeccion"]}.items()),
        "huellas de fuentes coinciden con archivos reales")
    ok(prop["huellas_entrada"] == reales, "propuestas fijan las huellas reales")
    ok(inv["huellas_entrada"] == reales, "inventario fija las huellas reales")

    # 2. conteos base actuales
    est = pend["resumen"]["estados_columnas"]
    ok(est.get("definicion_sin_interpretacion_compartida") == 3720, "base 3720 definicion_sin_interpretacion")
    ok(est.get("sin_definicion_coincidente") == 833, "base 833 sin_definicion")
    ok(est.get("sin_diccionario_en_conjunto") == 13, "base 13 sin_diccionario")
    ok(est.get("documental_revisada") == 836, "base 836 revisadas intactas")
    ok(est.get("candidata_por_nombre") == 118, "base 118 candidatas intactas")
    ok(est.get("ambigua_por_nombre") == 3, "base 3 ambiguas intactas")
    fuera = [v for v in pend["variables_pendientes"] if v["estado"] == "fuera_del_nucleo_actual"]
    cand4 = [v for v in pend["variables_pendientes"] if v["estado"] == "candidata_sin_definicion_suficiente"]
    ok(len(fuera) == 1308, "base 1308 fuera del nucleo")
    ok(len(cand4) == 23, "frontera 23 candidatos agente 4")
    ok(len(cob["variables"]) == 1563, "cobertura con 1563 variables")
    ok(inv["conteos_verificados"]["columnas"] == est, "inventario reproduce conteos de columnas")

    vmap = {v["definicion_iri"]: v for v in cob["variables"]}
    set4 = {v["definicion_iri"] for v in cand4}
    ids_regla = {r["id"] for r in sem["reglas_descripcion_exacta"]}
    conceptos = set(sem["conceptos"])
    permitidas = {r.get("representacion") for r in sem["reglas_descripcion_exacta"]}

    # 3. propuestas contra fuentes reales
    ok(len(prop["reglas"]) == 63, "63 reglas propuestas (una por definicion)")
    ok(len(prop["conceptos_nuevos"]) == 55, "55 conceptos nuevos estrechos")
    ok(len(prop["familias_revisadas"]) == 4, "4 familias documentadas")
    import sys as _sys
    _sys.path.insert(0, str(AQUI / "scripts"))
    from validar import validar_propuestas  # noqa: E402
    import copy
    insp_full = json.loads((ROOT / "data" / "portal" / "contenido-inspeccion.json").read_text(encoding="utf-8"))
    _filas = {}
    import unicodedata

    def _nk(s):
        return "".join(c for c in unicodedata.normalize("NFD", s.strip().lower())
                       if unicodedata.category(c) != "Mn")

    for _rec in insp_full["recursos"]:
        for _row in _rec.get("definiciones", []):
            _desc = next((v for k, v in _row.items()
                          if _nk(k) in ("descripcion", "definicion")
                          and isinstance(v, str)), "")
            _filas[(_rec["id"], _row.get("Nombre variable"))] = {
                "descripcion": _desc,
                "unidad": _row.get("Unidad de medida", ""),
                "tipo": _row.get("Tipo de dato", ""),
                "ejemplo": _row.get("Ejemplo de dato", "")}
    fuentes = {"variables_por_iri": vmap, "ids_reglas": ids_regla,
               "conceptos": conceptos, "representaciones": permitidas, "filas": _filas}
    _FAMS4 = {"045da7ba-ee72-498a-9b7a-071176e2a4ea", "94215f51-9c89-414d-8c3d-92792e609a2a",
              "863b9cc8-daeb-4430-b835-6a0ced5abd31", "a7591bc9-f905-45cb-ba6c-ae3588d87594"}
    _NOPROP = {("863b9cc8-daeb-4430-b835-6a0ced5abd31", "CVOTRAS"),
               ("863b9cc8-daeb-4430-b835-6a0ced5abd31", "DOTRAS"),
               ("a7591bc9-f905-45cb-ba6c-ae3588d87594", "GRUPO")}
    _esperadas = {(v["diccionario"], v["variable"]) for v in fuera if v["diccionario"] in _FAMS4} - _NOPROP
    ok(len(_esperadas) == 63, "asignacion esperada con 63 pares")
    asignacion = {"frontera": set4, "cubiertas_esperadas": _esperadas}

    # Positivo real por el validador compartido.
    errores = validar_propuestas(prop, fuentes, asignacion)
    ok(errores == [], "validacion integra sin errores" + ("" if not errores else ": " + str(errores[:3])))

    tocadas = {(vmap[i]["diccionario"], vmap[i]["variable"])
               for r in prop["reglas"] for i in r["definiciones"] if i in vmap}
    usados_conc = {r["concepto"] for r in prop["reglas"]}
    es_broader = {b for (_, _, b) in prop["conceptos_nuevos"].values() if b}
    for c in prop["conceptos_nuevos"]:
        ok(c in usados_conc or c in es_broader, "concepto usado o agrupador: " + c)
    # 3b-3c cubiertos por validar_propuestas (evidencia exacta, prosa sin
    # literales, calificadores). Aqui solo consistencia unidad-concepto,
    # que el validador no dictamina.
    por_concepto = {}
    for r in prop["reglas"]:
        por_concepto.setdefault(r["concepto"], []).append(r)
    # 3d. unidades declaradas en conceptos coinciden con la evidencia
    import re as _re
    for c, rs in sorted(por_concepto.items()):
        if c not in prop["conceptos_nuevos"]:
            continue
        definicion = prop["conceptos_nuevos"][c][1]
        m = _re.search(r"Unidad literal de la fila: ([^.]+)\.", definicion)
        unis = {x["evidencia"][0]["unidad_de_medida"] for x in rs}
        if m:
            ok(unis == {m.group(1)}, "unidad del concepto igual a evidencia: " + c)
        elif "Sin unidad declarada" in definicion:
            ok(unis == {""}, "concepto sin unidad con evidencia vacia: " + c)
        else:
            ok(all("unidad_de_medida" in x["evidencia"][0] for x in rs),
               "evidencia de unidad registrada: " + c)
    texto = json.dumps(prop, ensure_ascii=False)
    ok("/file-column/" not in texto and "/column/" not in texto,
       "sin IRIs fisicas de columna en propuestas")
    _claves_prohibidas = {"columna", "columna_origen", "variable_destino", "mapping", "correspondencia"}
    ok(not any(set(r) & _claves_prohibidas for r in prop["reglas"]),
       "reglas sin claves de correspondencia columna-variable")

    # 4. las reglas disparan con la semantica del pipeline
    extendidas = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
        {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
         "representacion": r["representacion"], "nombres": r.get("nombres"),
         "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
         "definiciones": r.get("definiciones")} for r in prop["reglas"]]}
    aciertos = 0
    for r in prop["reglas"]:
        for iri, desc, nom in zip(r["definiciones"], r["descripciones"], r["nombres"]):
            v = vmap[iri]
            res = interpretacion(nom, desc, v["conjunto"], extendidas,
                                 v["diccionario"], iri)
            if res.get("estado") == "respaldada_por_definicion" and res.get("concepto") == r["concepto"]:
                aciertos += 1
            else:
                ok(False, "la regla no dispara en pipeline: " + r["id"] + " " + nom)
    ok(aciertos == sum(len(r["definiciones"]) for r in prop["reglas"]),
       "las 63 definiciones disparan su regla en el pipeline (%d)" % aciertos)

    # 4b. aritmetica simulada con reglas extendidas sobre las 1563 variables
    from collections import Counter
    sim = Counter()
    for v in cob["variables"]:
        r = interpretacion(v["variable"], v["descripcion"], v["conjunto"], extendidas,
                           v["diccionario"], v["definicion_iri"])
        sim[r["estado"]] += 1
    ok(sim["respaldada_por_definicion"] == 295, "simulacion: 295 respaldadas (232 + 63)")
    ok(sim["fuera_del_nucleo_actual"] == 1245, "simulacion: 1245 fuera (1308 - 63)")
    ok(sim["candidata_sin_definicion_suficiente"] == 23, "simulacion: 23 agente 4 intactos")
    ok(len(sem["conceptos"]) + len(prop["conceptos_nuevos"]) == 158, "simulacion: 158 conceptos")
    ok(sum(sim.values()) == 1563, "simulacion cubre las 1563 variables")

    # 4c. 709 candidatas nuevas corroboradas con columnas fisicas reales
    import tomllib
    _inv = json.loads((ROOT / "data" / "portal" / "inventario.json").read_text(encoding="utf-8"))
    _insp = json.loads((ROOT / "data" / "portal" / "contenido-inspeccion.json").read_text(encoding="utf-8"))
    _base = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]
    _cols = columnas(_inv, _insp, _base)
    _mine = {(r["conjuntos"][0], clave(r["nombres"][0])) for r in prop["reglas"]}
    _alln = Counter((v["conjunto"], clave(v["variable"])) for v in cob["variables"])
    _est = {c["columna"]: c["estado"] for c in pend["columnas"]}
    _nuevas = [c for c in _cols if (c["conjunto"], clave(c["campo"])) in _mine]
    ok(len(_nuevas) == 709, "709 columnas fisicas matchean las 63 definiciones")
    ok(all(_est.get(c["iri"]) == "definicion_sin_interpretacion_compartida" for c in _nuevas),
       "las 709 son definicion_sin_interpretacion hoy (serian candidatas, no revisadas)")
    ok(all(c["nombre_unico"] for c in _nuevas), "las 709 con nombre unico")
    ok(all(_alln[(c["conjunto"], clave(c["campo"]))] == 1 for c in _nuevas),
       "las 709 con definicion unica")
    ok(118 + len(_nuevas) == 827, "candidatas tras integrar: 827 (118 + 709)")

    # 4d. limitacion del pipeline: interpretacion() no propaga calificador.
    # Detector en base: pasa mientras la limitacion exista; si el pipeline la
    # corrige, falla a proposito para revisar el requisito. No afirma conservacion.
    _shd = [r for r in prop["reglas"] if r.get("calificador")]
    ok(len(_shd) == 10, "10 reglas SHD con calificador")
    ok(all("requisito_integracion" in r for r in _shd),
       "las 10 SHD documentan el requisito de integracion")
    _v0 = vmap[_shd[0]["definiciones"][0]]
    _res0 = interpretacion(_v0["variable"], _v0["descripcion"], _v0["conjunto"], extendidas,
                           _v0["diccionario"], _v0["definicion_iri"])
    ok("calificador" not in _res0,
       "limitacion detectada: interpretacion() no propaga calificador (requisito pendiente)")
    _req = prop.get("requisitos_integracion", {})
    ok(_req.get("aritmetica_simulada", {}).get("candidatas_nuevas_no_revisadas") == 709,
       "propuesta documenta las 709 no revisadas")
    ok("NO" in _req.get("calificador_shd", "") and "no propagan" in _req.get("calificador_shd", ""),
       "propuesta declara que el pipeline no preserva el calificador")

    # 5. inventario con particiones exactas e identidades sin solapes
    _todas = [i for g in inv["columnas_3720_por_conjunto"] for i in g["columna_iris"]]
    ok(len(_todas) == 3720 and len(set(_todas)) == 3720, "inventario particiona 3720 sin solapes")
    ok(sum(g["columnas"] for g in inv["columnas_3720_por_conjunto"]) == 3720, "inventario 3720 con ==")
    _todas833 = [i for g in inv["columnas_833_por_conjunto"] for i in g["columna_iris"]]
    ok(len(_todas833) == 833 and len(set(_todas833)) == 833, "inventario particiona 833 sin solapes")
    ok(sum(g["columnas"] for g in inv["columnas_833_por_conjunto"]) == 833, "inventario 833 con ==")
    ok(len(inv["columnas_13_sin_diccionario"]["columnas"]) == 13, "inventario lista las 13")
    _todas1308 = [i for g in inv["fuera_1308_por_conjunto"] for i in g["definicion_iris"]]
    ok(len(_todas1308) == 1308 and len(set(_todas1308)) == 1308, "inventario particiona 1308 sin solapes")
    ok(sum(g["variables"] for g in inv["fuera_1308_por_conjunto"]) == 1308, "inventario cubre 1308")
    comp = [g for g in inv["fuera_1308_por_conjunto"] if g["lectura"] == "completa"]
    ok(sum(g["variables"] for g in comp) == 66, "lectura completa cubre 66 variables")
    inv_vars = {(v2["diccionario"], v2["variable"]) for g in inv["fuera_1308_por_conjunto"]
                for v2 in [v for v in fuera if v["conjunto"] == g["conjunto"]]}
    ok(tocadas <= inv_vars, "toda variable propuesta esta inventariada")
    puntajes = [p["puntaje"] for p in inv["prioridades_pendientes"]]
    ok(puntajes == sorted(puntajes, reverse=True), "prioridades ordenadas")
    _arit = inv.get("aritmetica_post_integracion", {})
    ok(_arit.get("fuera_del_nucleo") == 1245, "inventario: 1245 fuera tras integrar (1308 - 63)")
    ok(_arit.get("sin_lectura") == 1242, "inventario: 1242 sin lectura (1308 - 66)")
    ok(_arit.get("leidas_sin_propuesta") == 3, "inventario: 3 leidas sin propuesta")
    ok(_arit.get("sin_lectura", 0) + _arit.get("leidas_sin_propuesta", 0) == 1245,
       "inventario distingue 1242 sin leer + 3 leidas de 1245 pendientes")

    # 6. sin secretos en la entrega (solo entregas de datos; este script se excluye
    # de su propio escaneo para no auto-detectar su patron)
    todo = "".join((AQUI / f).read_text(encoding="utf-8")
                   for f in ("propuestas.json", "inventario-cobertura.json", "resultado.md",
                             "fuente/huellas.json", "scripts/construir.py", "scripts/validar.py"))
    import re
    ok(not re.search(r"(?i)(\bapi[_-]?key\b|\bpassword\b|\bsecret\b|bearer\s+[A-Za-z0-9]{8,}|AKIA[0-9A-Z]{16})", todo),
       "sin secretos en la entrega")

    # 7. negativos reales: deepcopy + mutacion + EL MISMO validar_propuestas,
    # verificando el codigo de error especifico.
    def mut(codigo_esperado, mensaje, fn):
        mala = copy.deepcopy(prop)
        fn(mala)
        errs = validar_propuestas(mala, fuentes, asignacion)
        codigos = [e["codigo"] for e in errs]
        ok(codigo_esperado in codigos, "negativo " + mensaje + " -> " + codigo_esperado)

    def n1(mala):
        del mala["reglas"][0]["alcance"]

    def n2(mala):
        mala["reglas"][0]["definiciones"] = []
        mala["reglas"][0]["diccionarios"] = []
        mala["reglas"][0]["conjuntos"] = []

    def n3(mala):
        mala["reglas"][0]["definiciones"][0] = "https://example.org/mex-ontologi/definition/inexistente%2F1"

    def n4(mala):
        mala["reglas"][0]["descripciones"][0] = mala["reglas"][0]["descripciones"][0] + " X"

    def n5(mala):
        ag4 = next(iter(set4))
        v4 = vmap[ag4]
        mala["reglas"][0]["definiciones"][0] = ag4
        mala["reglas"][0]["descripciones"][0] = v4["descripcion"]
        mala["reglas"][0]["nombres"][0] = v4["variable"]
        mala["reglas"][0]["diccionarios"] = [v4["diccionario"]]
        mala["reglas"][0]["conjuntos"] = [v4["conjunto"]]

    def n6(mala):
        mala["reglas"][0]["definiciones"][0] = "https://example.org/mex-ontologi/file-column/a%2Fb%2F1"

    def n7(mala):
        mala["reglas"].append(copy.deepcopy(mala["reglas"][1]))

    mut("CAMPO_FALTANTE", "N1 borrar alcance", n1)
    mut("SIN_RESTRICCION", "N2 regla global sin conjunto/diccionario/definicion", n2)
    mut("IRI_DESCONOCIDA", "N3 definicion IRI inexistente", n3)
    mut("LITERAL_DIFERENTE", "N4 descripcion mutada", n4)
    mut("FRONTERA_AGENTE4", "N5 definicion del agente 4", n5)
    mut("IRI_COLUMNA", "N6 IRI fisica de columna como definicion", n6)
    mut("ID_DUPLICADO", "N7 regla duplicada", n7)

    print("---")
    print("fallos: %d" % len(FALLOS))
    if FALLOS:
        raise SystemExit(1)
    print("verificacion completa: %d reglas, %d conceptos nuevos, 66 variables leidas" % (
        len(prop["reglas"]), len(prop["conceptos_nuevos"])))


if __name__ == "__main__":
    main()
