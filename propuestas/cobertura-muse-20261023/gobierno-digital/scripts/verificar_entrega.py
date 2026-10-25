"""Verificador propio de la entrega gobierno-digital. Solo lee el nucleo;
solo escribe en stdout. Uso:
PYTHONDONTWRITEBYTECODE=1 uv run python propuestas/cobertura-muse-20261023/gobierno-digital/scripts/verificar_entrega.py
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import io
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
assert AQUI.name == "gobierno-digital", AQUI
ROOT = AQUI.parents[2]
COB = ROOT / "propuestas" / "cobertura-muse-20261023"
FZ9 = COB / "fuentes" / "agente-9-gobierno-digital" / "propuestas.json"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402
from integrar_contenido import clave  # noqa: E402

FALLOS = []


def check(cond, msg):
    if not cond:
        FALLOS.append(msg)
    return cond


def validar_calificador(regla):
    # Contrato del generador del integrador: si la clave existe, dict no vacio str->str
    if "calificador" not in regla:
        return True
    cal = regla["calificador"]
    return (isinstance(cal, dict) and len(cal) > 0
            and all(isinstance(k, str) and k and isinstance(x, str) and x for k, x in cal.items()))


def main():
    ent = json.load(io.open(str(AQUI / "entrega.json"), encoding="utf-8"))
    fz = json.load(open(str(FZ9), encoding="utf-8"))
    mani = json.load(open(str(COB / "fuentes" / "manifiesto.json"), encoding="utf-8"))
    sem = json.load(open(str(ROOT / "ontologia/semantica.json"), encoding="utf-8"))
    cob = json.load(open(str(ROOT / "data/semantica/cobertura.json"), encoding="utf-8"))
    check(not (AQUI / "listo.json").exists(), "listo.json ya existe: el verificador corre antes del cierre")

    # 1. Fidelidad del manifiesto: copias congeladas e insumos centrales (file sha)
    for c in mani["copias"]:
        h = hashlib.sha256((ROOT / c["copia"]).read_bytes()).hexdigest()
        check(h == c["sha256"], "copia difiere del manifiesto: " + c["copia"])
    for k, v in mani["insumos_centrales"].items():
        h = hashlib.sha256((ROOT / k).read_bytes()).hexdigest()
        check(h == v, "insumo central difiere: " + k)
    for k, v in ent["huellas_entrada"].items():
        src = {"manifiesto_fuentes": COB / "fuentes/manifiesto.json",
               "copia_agente9_propuestas": FZ9,
               "copia_agente9_resultado": COB / "fuentes/agente-9-gobierno-digital/resultado.md",
               "asignaciones_semanticas": ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json",
               "cobertura": ROOT / "data/semantica/cobertura.json",
               "inspeccion": ROOT / "data/portal/contenido-inspeccion.json",
               "inventario": ROOT / "data/portal/inventario.json",
               "pendientes": ROOT / "reports/pendientes-semanticos.json",
               "semantica": ROOT / "ontologia/semantica.json"}[k]
        check(hashlib.sha256(src.read_bytes()).hexdigest() == v, "huella de entrada difiere: " + k)

    # 2. Particion completa: decisiones == asignacion congelada
    asig = json.load(open(str(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"), encoding="utf-8"))
    vars9 = [x for x in asig["asignaciones"]["9"]["variables"]]
    dec = ent["decisiones"]
    check(len(dec) == 243 and len(vars9) == 243, "particion != 243")
    check({d["definicion_iri"] for d in dec} == {x["definicion_iri"] for x in vars9}, "decisiones != asignacion exacta")
    check(len({d["definicion_iri"] for d in dec}) == 243, "decisiones duplicadas")
    for d in dec:
        check(d["decision"] in ("proponer", "pendiente"), "decision invalida: " + d["definicion_iri"])
        if d["decision"] == "proponer":
            check(bool(d.get("regla_id")) and "motivo" not in d, "proponer sin regla_id: " + d["definicion_iri"])
        else:
            check(bool(d.get("motivo")) and "regla_id" not in d, "pendiente sin motivo: " + d["definicion_iri"])

    # 3. Reglas: esquema, listas unitarias, huella real, limites, calificador
    reglas = ent["reglas"]
    check(len(reglas) == 121, "reglas != 121: %d" % len(reglas))
    check(len({r["id"] for r in reglas}) == 121, "reglas duplicadas")
    for r in reglas:
        check(r["id"].startswith("r3a9-"), "id sin prefijo: " + r["id"])
        for c in ["nombres", "descripciones", "conjuntos", "diccionarios", "definiciones"]:
            check(isinstance(r.get(c), list) and len(r[c]) == 1 and isinstance(r[c][0], str) and r[c][0],
                  "regla %s: %s no es lista unitaria" % (r["id"], c))
        check(re.fullmatch(r"[0-9a-f]{64}", r.get("huella_fila_diccionario", "")) is not None,
              "huella irreal en " + r["id"])
        check(isinstance(r.get("limites"), list) and len(r["limites"]) >= 1 and all(r["limites"]),
              "sin limite(s) en " + r["id"])
        check(r.get("fuente_revision", "").endswith("cobertura-muse-20261023/gobierno-digital/entrega.json"),
              "fuente_revision no apunta a esta entrega: " + r["id"])
        check(r["concepto"] in ent["conceptos_nuevos"], "concepto inexistente: " + r["id"])
        check(bool(r.get("evidencia")), "regla sin evidencia: " + r["id"])
    usada = {}
    for d in dec:
        if d["decision"] == "proponer":
            usada.setdefault(d["regla_id"], []).append(d["definicion_iri"])
    check(set(usada) == {r["id"] for r in reglas}, "reglas sin decision o viceversa")
    check(all(len(v) == 1 for v in usada.values()), "regla usada por mas de una decision")
    # huellas de regla == huella de su decision
    dec_h = {d["definicion_iri"]: d["huella_fila_diccionario"] for d in dec}
    for r in reglas:
        check(r["huella_fila_diccionario"] == dec_h[r["definiciones"][0]], "huella regla/decision difiere: " + r["id"])

    # 4. Conceptos: esquema, sin colision con nucleo, sin sameAs
    check(len(ent["conceptos_nuevos"]) == 86, "conceptos != 86")
    for slug, triple in ent["conceptos_nuevos"].items():
        check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug) is not None, "slug invalido: " + slug)
        check(isinstance(triple, list) and len(triple) == 3 and triple[2] is None, "concepto mal formado: " + slug)
    check(set(ent["conceptos_nuevos"]) & set(sem["conceptos"]) == set(), "colision de slugs con nucleo")
    check(isinstance(ent["conceptos_reutilizados"], list) and not ent["conceptos_reutilizados"], "reutilizados debe ser []")
    txt = json.dumps(ent, ensure_ascii=False).lower()
    check(all(p not in txt for p in ['"sameas":', '"exactmatch":', "#sameas", "#exactmatch"]), "sameAs/exactMatch")
    check('"columna_origen"' not in txt and '"variable_destino"' not in txt, "hay correspondencias columna-variable")

    # 5. Preservar nucleo: 103 conceptos, 232 respaldadas, 23 candidatas, 836/118
    check(len(sem["conceptos"]) == 103, "nucleo alterado: conceptos != 103")
    check(cob["resumen"]["estados_variables"] == {"respaldada_por_definicion": 232, "fuera_del_nucleo_actual": 1308,
          "candidata_sin_definicion_suficiente": 23}, "estados de variables alterados")
    check(cob["resumen"]["estados_correspondencias"] == {"documental_revisada": 836, "candidata_por_nombre": 118,
          "ambigua_por_nombre": 6}, "correspondencias alteradas")

    # 6. Sin colision con reglas centrales: mis positivos no resuelven en el nucleo
    centrales = sem["reglas_descripcion_exacta"]
    check(len(centrales) == 116, "reglas centrales != 116")
    for d in dec:
        if d["decision"] != "proponer":
            continue
        try:
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"],
                                 {"reglas_descripcion_exacta": centrales}, dictionary=d["diccionario"],
                                 definition=d["definicion_iri"])
        except ValueError:
            got = {"estado": "conflicto-central"}
        check(got.get("estado") != "respaldada_por_definicion", "colision con regla central: " + d["definicion_iri"])

    # 7. Positivos con mis reglas + negativos reales
    sim = [{"id": r["id"], "concepto": r["concepto"], "representacion": r["representacion"],
            "descripciones": r["descripciones"], "nombres": r["nombres"], "conjuntos": r["conjuntos"],
            "diccionarios": r["diccionarios"], "definiciones": r["definiciones"]} for r in reglas]
    pos = 0
    for d in dec:
        if d["decision"] != "proponer":
            continue
        try:
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], {"reglas_descripcion_exacta": sim},
                                 dictionary=d["diccionario"], definition=d["definicion_iri"])
        except ValueError as e:
            FALLOS.append("conflicto en positivo %s: %s" % (d["definicion_iri"], e))
            continue
        if got.get("regla") == d["regla_id"] and got.get("estado") == "respaldada_por_definicion":
            pos += 1
        else:
            FALLOS.append("positivo no resuelve: " + d["definicion_iri"])
    check(pos == 121, "positivos != 121: %d" % pos)
    neg = 0
    d0 = next(d for d in dec if d["decision"] == "proponer")
    base = "https://example.org/mex-ontologi/"
    casos = [("solo-nombre", "PX_FALSO", d0["descripcion"], d0["conjunto"], d0["diccionario"], d0["definicion_iri"]),
             ("contexto-mutado", d0["variable"], d0["descripcion"], "00000000-0000-0000-0000-000000000000",
              d0["diccionario"], d0["definicion_iri"]),
             ("otra-iri", d0["variable"], d0["descripcion"], d0["conjunto"], d0["diccionario"], base + "definition/falso%2F999"),
             ("descripcion-extendida", d0["variable"], d0["descripcion"] + " texto inventado", d0["conjunto"],
              d0["diccionario"], d0["definicion_iri"])]
    for nombre, a, b, c, e, f in casos:
        got = interpretacion(a, b, c, {"reglas_descripcion_exacta": sim}, dictionary=e, definition=f)
        if got.get("estado") != "respaldada_por_definicion":
            neg += 1
        else:
            FALLOS.append("negativo fallo: " + nombre)
    dp = next(d for d in dec if d["decision"] == "pendiente")
    got = interpretacion(dp["variable"], dp["descripcion"], dp["conjunto"], {"reglas_descripcion_exacta": sim},
                         dictionary=dp["diccionario"], definition=dp["definicion_iri"])
    if got.get("estado") != "respaldada_por_definicion":
        neg += 1
    else:
        FALLOS.append("pendiente resolvio a regla")
    check(neg == 5, "negativos != 5: %d" % neg)

    # 8. Criterios de integracion
    _O = chr(0xF3)
    _N = chr(0xF1)
    BOILER = re.compile("diagn[" + _O + "o]stico del entorno digital", re.IGNORECASE)
    PRESENTE = [("personas", "persona"), ("a" + _N + "o", "a" + _N + "o"), ("gb", "gb"), ("cpu", "cpu"),
                ("conteo", "cuant"), ("monto", "presupuesto")]
    AUSENTE = ["mxn", "pesos", "moneda", "porcentaje", "nacionalidad", "extranjeria",
               "titulacion", "egreso", "diagnostico", "diagn" + _O + "stico"]
    for r in reglas:
        triple = ent["conceptos_nuevos"][r["concepto"]]
        ctext = (triple[0] + " " + triple[1].split(". ")[0]).lower()
        lit = next(d for d in dec if d.get("regla_id") == r["id"])["descripcion"].lower()
        for pal, tok in PRESENTE:
            if re.search(r"\b" + pal + r"\b", ctext):
                check(tok in lit, "unidad '%s' sin respaldo literal en %s" % (pal, r["id"]))
        limpio = BOILER.sub("", ctext)
        for pal in AUSENTE:
            check(re.search(r"\b" + pal + r"\b", limpio) is None, "termino '%s' en %s" % (pal, r["id"]))
        check(re.fullmatch(r"P\d+|ID", r["nombres"][0]) is not None, "nombre no neutro en " + r["id"])
    check("unidad-coordinadora-tic" not in ent["conceptos_nuevos"], "fusion existencia/nombre no revertida")
    rex = next(r for r in reglas if r["nombres"] == ["P8"] and r["diccionarios"] == ["3851f1c3-5045-4703-ba88-93b3d39e0b70"])
    rno = next(r for r in reglas if r["nombres"] == ["P9"] and r["diccionarios"] == ["3851f1c3-5045-4703-ba88-93b3d39e0b70"])
    check(rex["concepto"] == "existencia-unidad-coordinadora-tic" and rex["representacion"] == "no_especificada",
          "P8 debe ser existencia, no nombre")
    check(rno["concepto"] == "nombre-unidad-coordinadora-tic" and rno["representacion"] == "nombre",
          "P9 debe ser nombre, no existencia")
    check(rex["concepto"] != rno["concepto"], "existencia y nombre comparten concepto")
    rep_por_concepto = {}
    for r in reglas:
        rep_por_concepto.setdefault(r["concepto"], set()).add(r["representacion"])
    for slug, reps in rep_por_concepto.items():
        check(len(reps) == 1, "concepto con varias representaciones (fusion encubierta): " + slug)
    usos = {}
    for r in reglas:
        usos.setdefault(r["concepto"], set()).update(r["conjuntos"])
    for r in reglas:
        if len(usos[r["concepto"]]) > 1:
            check(isinstance(r.get("calificador"), dict) and r["calificador"].get("instrumento"),
                  "falta calificador en " + r["id"])
            decr = next(d for d in dec if d.get("regla_id") == r["id"])
            check(r["calificador"]["instrumento"] == decr.get("titulo_conjunto"), "calificador erroneo en " + r["id"])
        else:
            check("calificador" not in r, "calificador innecesario en " + r["id"])
    for r in reglas:
        check(validar_calificador(r), "calificador invalido (clave existe sin dict no vacio str->str) en " + r["id"])
    check(sum(1 for r in reglas if "calificador" in r) == 70, "reglas con calificador != 70")
    check(sum(1 for r in reglas if "calificador" not in r) == 51, "reglas sin calificador != 51")

    # 9. Contradicciones tipo<->ejemplo declaradas como limite tecnico
    esperadas = {(("bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1", "P11"), "Numerico", "No"),
                 (("bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1", "P12"), "Numerico", "Si"),
                 (("8f8e3cfb-e551-4a95-b382-4999351c5f29", "P7"), "Entero", "Platicas, reuniones, etc")}
    for (key, tipo, ej) in esperadas:
        r = next(r for r in reglas if (r["diccionarios"][0], r["nombres"][0]) == key)
        check(any("Contradiccion tecnica" in lim for lim in r["limites"]), "sin limite tecnico en " + r["id"])
        check(r["evidencia"][0]["tipo_de_dato"] == tipo and r["evidencia"][0]["ejemplo_de_dato"] == ej,
              "evidencia tipo+ejemplo no capturada en " + r["id"])
        check(r["representacion"] == "no_especificada", "representacion no reducida en " + r["id"])

    # 10. Caracteres: sin U+FFFD, NBSP preservado
    FFFD = chr(0xFFFD)
    assert FFFD not in json.dumps(ent, ensure_ascii=False), "U+FFFD en entrega"
    n_nbsp = sum(1 for d in dec if chr(0xA0) in d["descripcion"])
    check(n_nbsp == 3, "NBSP != 3")

    # 11. Conteos recalculados + pendientes.json + disjuncion con hermanos
    check(ent["conteos"] == {"decisiones": 243,
          "proponer": sum(1 for d in dec if d["decision"] == "proponer"),
          "pendiente": sum(1 for d in dec if d["decision"] == "pendiente"),
          "reglas": len(reglas), "conceptos_nuevos": len(ent["conceptos_nuevos"])}, "conteos no recalculados")
    pen = json.load(open(str(AQUI / "pendientes.json"), encoding="utf-8"))
    check(pen["total"] == 122 and len(pen["pendientes"]) == 122, "pendientes.json inconsistente")
    check({p["definicion_iri"] for p in pen["pendientes"]} == {d["definicion_iri"] for d in dec if d["decision"] == "pendiente"},
          "pendientes.json no refleja decisiones")
    for ag in ["agente-3-cobertura", "agente-6-salud", "agente-7-registro-civil", "agente-8-educacion",
               "agente-10-territorio-economia"]:
        try:
            sib = json.load(open(str(COB / ("fuentes/" + ag + "/propuestas.json")), encoding="utf-8"))
        except (FileNotFoundError, KeyError):
            continue
        defs = set()
        for r in sib.get("reglas", []):
            defs.update(r.get("definiciones", []))
        check(defs & {d["definicion_iri"] for d in dec} == set(), "solape de definiciones con " + ag)

    resumen = {"huellas_manifiesto_ok": True, "particion": 243, "positivos": pos, "negativos": neg,
               "reglas": len(reglas), "conceptos": len(ent["conceptos_nuevos"]),
               "proponer": ent["conteos"]["proponer"], "pendiente": ent["conteos"]["pendiente"],
               "fallos": FALLOS}
    print(json.dumps({k: v for k, v in resumen.items() if k != "fallos"}, indent=1))
    if FALLOS:
        print("FALLOS:")
        for m in FALLOS:
            print(" -", m)
        sys.exit(1)
    print("VERIFICACION ENTREGA: TODO OK")


if __name__ == "__main__":
    main()
