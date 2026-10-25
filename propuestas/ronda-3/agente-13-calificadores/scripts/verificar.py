"""Verificador propio agente-13 (ronda 3): patch de calificadores, solo memoria.

Lee el núcleo y las propuestas 3/8 como fixtures (solo lectura). Importa el
staging propio y comprueba que sus imports resuelven al ROOT central original.
Usa construir()/interpretacion() en memoria; NUNCA llama generar() ni escribe
fuera de propuestas/ronda-3/agente-13-calificadores/.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from urllib.parse import quote

A13 = Path(__file__).resolve().parents[1]
ROOT = A13.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))

import consolidar_semantica as orig  # noqa: E402  central original
from rdflib import Literal, Namespace, OWL, RDF, SKOS, URIRef  # noqa: E402
from rdflib.compare import isomorphic  # noqa: E402

BASE = "https://example.org/mex-ontologi/"
SELF = A13 / "fuente" / "verificacion-13.json"

_results = []


def check(name, fn):
    try:
        detail = fn() or {}
        _results.append({"prueba": name, "ok": True, "detalle": detail})
        print("ok  " + name)
    except Exception as e:
        _results.append({"prueba": name, "ok": False, "error": type(e).__name__ + ": " + str(e)[:600]})
        print("FAIL " + name + " -> " + str(e)[:300])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_staging():
    spec = importlib.util.spec_from_file_location(
        "staging_cons_13", str(A13 / "staging" / "consolidar_semantica.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ST = load_staging()


def central_rules():
    return json.loads((ROOT / "ontologia" / "semantica.json").read_text(encoding="utf-8"))


def fixture_rules():
    return json.loads((A13 / "fixture" / "reglas_calificadas.json").read_text(encoding="utf-8"))


def test_imports_resuelven_root_central():
    import construir_catalogo
    assert ST.ROOT == construir_catalogo.ROOT == ROOT, "staging no resuelve al ROOT central"
    assert ST.RULES == orig.RULES, "RULES distinto del central"
    assert ST.generar is orig.generar or callable(ST.generar)
    return {"root": str(ST.ROOT)}


def test_reglas_vigentes_sin_calificador_salida_exacta():
    rules = central_rules()
    muestra = [r for r in rules["reglas_descripcion_exacta"] if "calificador" not in r][:8]
    assert len(muestra) == 8
    for r in muestra:
        desc = r["descripciones"][0]
        # Llamada real con las reglas centrales completas (filtros de conjunto/diccionario/definición):
        full_kw = {}
        if r.get("diccionarios"):
            full_kw["dictionary"] = r["diccionarios"][0]
        if r.get("definiciones"):
            full_kw["definition"] = r["definiciones"][0]
        ds = r["conjuntos"][0] if r.get("conjuntos") else "d"
        name = r["nombres"][0] if r.get("nombres") else "X"
        ao = orig.interpretacion(name, desc, ds, rules, **full_kw)
        ap = ST.interpretacion(name, desc, ds, rules, **full_kw)
        assert ao == ap, "salida distinta en regla " + r["id"]
        assert "calificador" not in ao and "calificador" not in ap, "regla vigente no debe traer calificador"
    return {"reglas_muestreadas": len(muestra)}


def _real_inputs():
    inv = json.loads((ROOT / "data" / "portal" / "inventario.json").read_text(encoding="utf-8"))
    insp = json.loads((ROOT / "data" / "portal" / "contenido-inspeccion.json").read_text(encoding="utf-8"))
    rules = central_rules()
    refp = ROOT / "data" / "portal" / "lote-cruces" / "catalogo-municipal-portal.json"
    ref = json.loads(refp.read_text(encoding="utf-8")) if refp.exists() else None
    return inv, insp, rules, ref


def test_construir_real_sin_calificador_identico():
    inv, insp, rules, ref = _real_inputs()
    go, mo, ro = orig.construir(inv, insp, rules, ref, BASE)
    gp, mp, rp = ST.construir(inv, insp, copy.deepcopy(rules), ref, BASE)
    assert isomorphic(go, gp), "grafo de datos cambió sin calificadores"
    assert ro["resumen"] == rp["resumen"], "resumen cambió"
    assert ro["variables"] == rp["variables"], "records cambiaron"
    assert all("calificador" not in v for v in rp["variables"])
    mex = Namespace(BASE + "vocab/")
    quals = list(gp.subjects(RDF.type, mex.CalificadorDocumental))
    assert quals == [], "nodos calificadores sin reglas calificadas"
    nuevos = set(mp) - set(mo)
    assert len(set(mo) - set(mp)) == 0, "el patch elimina triples del modelo"
    assert len(nuevos) == 0, "el script propuesto debe coincidir con el central integrado, ganó %d" % len(nuevos)
    assert ro["resumen"]["estados_variables"] == {"respaldada_por_definicion": 232,
                                                 "fuera_del_nucleo_actual": 1308,
                                                 "candidata_sin_definicion_suficiente": 23}
    assert ro["resumen"]["estados_correspondencias"]["documental_revisada"] == 836
    assert isomorphic(mo, mp), "modelo propuesto distinto del central"
    return {"data": len(gp), "model": len(mp), "nuevos_modelo": 0}


def _synthetic_inputs(fix):
    by_dic = {}
    for r in fix:
        dic = r["diccionarios"][0]
        idx = int(r["definiciones"][0].rsplit("%2F", 1)[1])
        info = by_dic.setdefault(dic, {"conjunto": r["conjuntos"][0], "filas": {}})
        info["filas"][idx] = r
    for dic, info in by_dic.items():
        top = max(info["filas"])
        rows = []
        for i in range(1, top + 1):
            if i in info["filas"]:
                rr = info["filas"][i]
                rows.append({"Nombre variable": rr["nombres"][0], "Descripción": rr["descripciones"][0]})
            else:
                rows.append({"Nombre variable": "ZZZ_SIN_USO_%d" % i,
                             "Descripción": "Texto sin regla que no casa con nada 000 %d" % i})
        info["rows"] = rows
    inventory = {"recursos": [{"id": d, "conjunto_id": v["conjunto"], "conjunto": "Título " + d[:8],
                               "clasificacion": "diccionario"} for d, v in by_dic.items()]}
    inspection = {"recursos": [{"id": d, "ok": True, "definiciones": v["rows"]} for d, v in by_dic.items()]}
    rules = central_rules()
    rules["vinculos_documentales_revisados"] = []
    rules["observaciones_revision"] = []
    rules["reglas_descripcion_exacta"] = rules["reglas_descripcion_exacta"] + copy.deepcopy(fix)
    return inventory, inspection, rules, by_dic


def test_treinta_reglas_en_rdf_y_records():
    fix = fixture_rules()
    assert len(fix) == 30, len(fix)
    inv, insp, rules, _ = _synthetic_inputs(fix)
    g, _, rep = ST.construir(inv, insp, rules, None, BASE)
    mex = Namespace(BASE + "vocab/")
    recs = [v for v in rep["variables"] if "calificador" in v]
    assert len(recs) == 30, "records con calificador: %d" % len(recs)
    esperados = {(r["diccionarios"][0], r["definiciones"][0]): r["calificador"] for r in fix}
    for v in recs:
        assert v["calificador"] == esperados[(v["diccionario"], v["definicion_iri"])], v["variable"]
    qnodes = list(g.subjects(RDF.type, mex.CalificadorDocumental))
    assert len(qnodes) == 30, len(qnodes)
    ddr = sorted(str(g.value(n, mex.valorCalificador)) for n in qnodes
                 if str(g.value(n, mex.dimensionCalificador)) == "distrito_desarrollo_rural")
    assert ddr == ["139", "140", "141", "142", "143", "144", "147", "148", "149", "193"], ddr
    sedes = sorted(str(g.value(n, mex.valorCalificador)) for n in qnodes
                   if str(g.value(n, mex.dimensionCalificador)) == "sede")
    assert len(sedes) == 20 and len(set(sedes)) == 5, sedes
    assert "San Luis R.C." in sedes, "valor original con puntos perdido"
    assert any("Juárez" in s for s in sedes), "Unicode original perdido: %s" % sedes
    assert "139" in ddr, "cero/original '139' no preservado verbatim"
    for n in qnodes:
        prov = list(g.objects(n, URIRef("http://www.w3.org/ns/prov#wasDerivedFrom")))
        assert len(prov) == 2, "provenance debe ser definición + reglas"
        dims = list(g.objects(n, mex.dimensionCalificador))
        vals = list(g.objects(n, mex.valorCalificador))
        assert len(dims) == 1 and len(vals) == 1
        assert dims[0].datatype is not None and str(dims[0].datatype).endswith("string")
        assert vals[0].datatype is not None and str(vals[0].datatype).endswith("string")
    assert not list(g.triples((None, OWL.sameAs, None))), "sameAs prohibido"
    assert not list(g.triples((None, SKOS.exactMatch, None))), "exactMatch prohibido"
    assert not list(g.subjects(RDF.type, mex.SistemaIdentificadores)), "sin sistemas identificadores"
    return {"records_qual": 30, "nodos_qual": 30, "ddr": ddr}


def test_mismo_concepto_quals_no_mezclados():
    fix = fixture_rules()
    inv, insp, rules, _ = _synthetic_inputs(fix)
    g, _, rep = ST.construir(inv, insp, rules, None, BASE)
    mex = Namespace(BASE + "vocab/")
    grupo = [v for v in rep["variables"]
             if v.get("concepto") == "estudiantes-nuevo-ingreso-sede" and "iri" in v]
    assert len(grupo) == 5, len(grupo)
    a = next(v for v in grupo if v["calificador"] == {"sede": "San Luis R.C."})
    b = next(v for v in grupo if v["calificador"] == {"sede": "Hermosillo"})
    assert a["iri"] != b["iri"] and a["definicion_iri"] != b["definicion_iri"]
    qa = set(g.objects(URIRef(a["iri"]), mex.tieneCalificadorDocumentado))
    qb = set(g.objects(URIRef(b["iri"]), mex.tieneCalificadorDocumentado))
    assert len(qa) == 1 and len(qb) == 1 and qa != qb
    assert g.value(next(iter(qa)), mex.valorCalificador) == Literal("San Luis R.C.", datatype=g.value(next(iter(qa)), mex.valorCalificador).datatype)
    assert str(g.value(next(iter(qa)), mex.valorCalificador)) == "San Luis R.C."
    assert str(g.value(next(iter(qb)), mex.valorCalificador)) == "Hermosillo"
    return {"a": a["variable"], "b": b["variable"]}


def test_deepcopy_sin_mutar_regla():
    fix = fixture_rules()
    r = copy.deepcopy(next(x for x in fix if x["id"] == "r3a8-001"))
    antes = copy.deepcopy(r)
    rules = {"reglas_descripcion_exacta": [r], "conceptos": {}}
    out = ST.interpretacion(r["nombres"][0], r["descripciones"][0], r["conjuntos"][0], rules,
                            r["diccionarios"][0], r["definiciones"][0])
    assert out["calificador"] == {"sede": "San Luis R.C."}
    assert out["calificador"] is not r["calificador"], "debe ser deepcopy, no alias"
    out["calificador"]["sede"] = "MUTADO"
    assert r == antes, "la regla original fue mutada"
    return {}


def test_tipos_invalidos_rechazados_y_verbatim():
    base = {"id": "t", "concepto": "c", "descripciones": ["Desc t"], "representacion": "no_especificada"}
    malos = [None, {}, {"": "x"}, {"k": ""}, {"k": None}, {"k": 139}, {"k": True},
             {"k": ["x"]}, {"k": {"a": "b"}}, {"k": 1.5}, {"k": "x", "": "y"}, "sede",
             [("sede", "X")], {123: "x"}, {"sede": "   "}, {"   ": "San Luis R.C."}]
    rechazados = 0
    for i, malo in enumerate(malos):
        rr = dict(base)
        rr["calificador"] = malo
        rules = {"reglas_descripcion_exacta": [rr], "conceptos": {}}
        try:
            ST.interpretacion("N", "Desc t", "d", rules)
        except ValueError:
            rechazados += 1
        else:
            raise AssertionError("calificador inválido aceptado [%d]: %r" % (i, malo))
    assert rechazados == len(malos), (rechazados, len(malos))
    # Verbatim: el strip solo rechaza, no modifica lo devuelto.
    rr = dict(base)
    rr["calificador"] = {"sede": " San Luis R.C. "}
    out = ST.interpretacion("N", "Desc t", "d", {"reglas_descripcion_exacta": [rr], "conceptos": {}})
    assert out["calificador"] == {"sede": " San Luis R.C. "}, "no debe hacer strip"
    assert out["calificador"]["sede"].startswith(" ") and out["calificador"]["sede"].endswith(" ")
    rr2 = dict(base)
    rr2["calificador"] = {"distrito_desarrollo_rural": "139"}
    out2 = ST.interpretacion("N", "Desc t", "d", {"reglas_descripcion_exacta": [rr2], "conceptos": {}})
    assert out2["calificador"]["distrito_desarrollo_rural"] == "139"
    assert isinstance(out2["calificador"]["distrito_desarrollo_rural"], str)
    return {"rechazados": rechazados}


def test_iris_estables_y_reconstruccion():
    fix = fixture_rules()
    inv, insp, rules, _ = _synthetic_inputs(fix)
    g1, _, _ = ST.construir(inv, insp, copy.deepcopy(rules), None, BASE)
    g2, _, _ = ST.construir(inv, insp, copy.deepcopy(rules), None, BASE)
    mex = Namespace(BASE + "vocab/")
    q1 = sorted(str(s) for s in g1.subjects(RDF.type, mex.CalificadorDocumental))
    q2 = sorted(str(s) for s in g2.subjects(RDF.type, mex.CalificadorDocumental))
    assert q1 == q2 and len(q1) == 30, "IRIs inestables entre construcciones"
    r0 = fix[0]
    dic = r0["diccionarios"][0]
    idx = r0["definiciones"][0].rsplit("%2F", 1)[1]
    dim = list(r0["calificador"])[0]
    esperado = BASE + "documented-qualifier/" + quote(dic + "/" + idx + "/" + dim, safe="")
    assert esperado in q1, "IRI no reconstruible por diccionario/fila/key: " + esperado
    return {"iri_ejemplo": esperado}


def test_candidata_no_autopromueve_ni_califica():
    rules = central_rules()
    c = ST.interpretacion("CLUES", "Clave de la Unidad", "conjunto-inexistente", rules)
    assert c["estado"] == "candidata_sin_definicion_suficiente"
    assert "calificador" not in c, "la candidata no debe inventar calificador"
    f = ST.interpretacion("Total_Egresos", "Total de urgencias atendidas", "d", rules)
    assert f["estado"] == "fuera_del_nucleo_actual" and "calificador" not in f
    return {}


def test_shape_calificador_estructural():
    from rdflib import Graph
    raw = (A13 / "staging" / "semantica.ttl").read_text(encoding="utf-8").replace("{{BASE_IRI}}", BASE)
    g = Graph()
    g.parse(data=raw, format="turtle")
    shape = URIRef(BASE + "shapes/CalificadorDocumental")
    mex = Namespace(BASE + "vocab/")
    from rdflib.namespace import SH
    assert (shape, RDF.type, SH.NodeShape) in g
    assert (shape, SH.targetClass, mex.CalificadorDocumental) in g
    by_path = {}
    for _, _, b in g.triples((shape, SH.property, None)):
        for _, _, p in g.triples((b, SH.path, None)):
            by_path[str(p)] = b
    for prop in (str(mex.dimensionCalificador), str(mex.valorCalificador)):
        assert prop in by_path, prop
        b = by_path[prop]
        assert (b, SH.minLength, Literal(1)) in g, "minLength ausente en " + prop
        pats = [str(o) for o in g.objects(b, SH.pattern)]
        assert any("\\S" in p or p == "\\S" for p in pats), "pattern \\S ausente en " + prop + ": " + str(pats)
    assert "http://www.w3.org/ns/prov#wasDerivedFrom" in by_path
    varshape = URIRef(BASE + "shapes/VariableDocumentada")
    enlace = None
    for _, _, b in g.triples((varshape, SH.property, None)):
        if (b, SH.path, mex.tieneCalificadorDocumentado) in g:
            enlace = b
    assert enlace is not None, "enlace variable->calificador ausente"
    assert (enlace, SH.nodeKind, SH.IRI) in g, "enlace sin nodeKind IRI"
    return {"pattern": "\\\\S"}


def test_loader_sin_cambio_necesario():
    txt = (ROOT / "scripts" / "ampliar_portal.py").read_text(encoding="utf-8")
    assert "shapes/semantica.ttl" in txt, "loader no referencia semantica.ttl"
    return {}


def main():
    check("imports_staging_resuelven_root_central", test_imports_resuelven_root_central)
    check("reglas_vigentes_sin_calificador_salida_exacta", test_reglas_vigentes_sin_calificador_salida_exacta)
    check("construir_real_sin_calificador_identico", test_construir_real_sin_calificador_identico)
    check("treinta_reglas_en_rdf_y_records", test_treinta_reglas_en_rdf_y_records)
    check("mismo_concepto_quals_no_mezclados", test_mismo_concepto_quals_no_mezclados)
    check("deepcopy_sin_mutar_regla", test_deepcopy_sin_mutar_regla)
    check("tipos_invalidos_rechazados_y_verbatim", test_tipos_invalidos_rechazados_y_verbatim)
    check("iris_estables_y_reconstruccion", test_iris_estables_y_reconstruccion)
    check("candidata_no_autopromueve_ni_califica", test_candidata_no_autopromueve_ni_califica)
    check("shape_calificador_estructural", test_shape_calificador_estructural)
    check("loader_sin_cambio_necesario", test_loader_sin_cambio_necesario)
    ok = sum(1 for r in _results if r["ok"])
    total = len(_results)
    payload = {"generado_en_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
               "agente": "ronda-3/agente-13-calificadores",
               "pasadas": ok, "totales": total,
               "huellas_entrada": {"consolidar_original_sha256": sha(ROOT / "scripts" / "consolidar_semantica.py"),
                                   "semantica_sha256": sha(ROOT / "ontologia" / "semantica.json"),
                                   "shape_original_sha256": sha(ROOT / "shapes" / "semantica.ttl"),
                                   "fixture_sha256": sha(A13 / "fixture" / "reglas_calificadas.json")},
               "pruebas": _results}
    SELF.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("pasadas %d/%d -> %s" % (ok, total, SELF))
    if ok != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
