"""Verificador propio del agente 7 ronda 3. Solo lee central (funciones puras) y
mi carpeta; no genera nada central. Falla con assert reales (sin `or True`)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MIA = ROOT / "propuestas" / "ronda-3" / "agente-7-registro-civil"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402
from integrar_contenido import clave  # noqa: E402

REPS = {"codigo", "nombre", "fecha", "hora", "anio", "mes", "dia", "no_especificada"}


def main():
    prop = json.loads((MIA / "propuestas.json").read_text(encoding="utf-8"))
    ext = json.loads((MIA / "fuente" / "inspeccion-extracto.json").read_text(encoding="utf-8"))
    asign = json.loads((ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json").read_text(encoding="utf-8"))
    insp = {r["id"]: r for r in json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))["recursos"]}
    central_concepts = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))["conceptos"]
    vars7 = asign["asignaciones"]["7"]["variables"]

    # 1. Particion exacta: 163, sin omitidos/duplicados, todas fuera_del_nucleo.
    assert len(vars7) == 163, len(vars7)
    assert len(prop["decisiones"]) == 163, len(prop["decisiones"])
    assert {d["definicion_iri"] for d in prop["decisiones"]} == {v["definicion_iri"] for v in vars7}
    assert len({d["definicion_iri"] for d in prop["decisiones"]}) == 163
    assert all(v["estado"] == "fuera_del_nucleo_actual" for v in vars7)
    # Sin solape con otras particiones.
    mias = {v["definicion_iri"] for v in vars7}
    for k, a in asign["asignaciones"].items():
        if k != "7":
            assert not (mias & {x["definicion_iri"] for x in a["variables"]}), k

    # 2. Huellas recalculadas desde inspeccion + literales exactos.
    assert len(ext) == 163
    for v in vars7:
        r = insp[v["diccionario"]]
        idx = int(v["definicion_iri"].rsplit("%2F", 1)[1]) - 1
        assert huella(r["definiciones"][idx]) == v["huella_fila_diccionario"], v["variable"]
    for e in ext:
        assert huella(e["fila"]) == e["huella_fila_diccionario"], e["definicion_iri"]
        assert "\ufffd" not in json.dumps(e["fila"], ensure_ascii=False), e["definicion_iri"]
    for d in prop["decisiones"]:
        v = next(x for x in vars7 if x["definicion_iri"] == d["definicion_iri"])
        assert d["variable"] == v["variable"] and d["descripcion"] == v["descripcion"]
        assert d["huella_fila_diccionario"] == v["huella_fila_diccionario"]
        assert d["conjunto"] == v["conjunto"] and d["diccionario"] == v["diccionario"]

    # 3. Reglas: ids r3a7- unicos, scoping simultaneo exacto, positivos via interpretacion().
    rules = {"reglas_descripcion_exacta": prop["reglas"], "conceptos": {}}
    assert len(prop["reglas"]) == sum(1 for d in prop["decisiones"] if d["decision"] == "propuesta-significado")
    assert all(r["id"].startswith("r3a7-") for r in prop["reglas"])
    assert len({r["id"] for r in prop["reglas"]}) == len(prop["reglas"])
    for r in prop["reglas"]:
        assert r["representacion"] in REPS, r["id"]
        d = next(x for x in prop["decisiones"] if x["regla_id"] == r["id"])
        assert r["descripciones"] == [d["descripcion"]] and r["nombres"] == [d["variable"]]
        assert r["conjuntos"] == [d["conjunto"]] and r["diccionarios"] == [d["diccionario"]]
        assert r["definiciones"] == [d["definicion_iri"]] and r["concepto"] == d["concepto"]
    for d in prop["decisiones"]:
        if d["decision"] == "propuesta-significado":
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], rules, d["diccionario"], d["definicion_iri"])
            assert got["estado"] == "respaldada_por_definicion", d["variable"]
            assert got["concepto"] == d["concepto"], d["variable"]
            assert got["representacion"] == d["representacion"], d["variable"]
        else:
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], rules, d["diccionario"], d["definicion_iri"])
            assert got.get("concepto") is None or got["estado"] != "respaldada_por_definicion", d["variable"]

    # 4. Negativos reales.
    d0 = next(x for x in prop["decisiones"] if x["decision"] == "propuesta-significado")
    ok = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], rules, d0["diccionario"], d0["definicion_iri"])
    assert ok["estado"] == "respaldada_por_definicion"
    # 4a. Solo-nombre: descripcion distinta no casa.
    neg = interpretacion(d0["variable"], "Otra descripcion inexistente", d0["conjunto"], rules, d0["diccionario"], d0["definicion_iri"])
    assert neg["estado"] != "respaldada_por_definicion", "solo-nombre caso"
    # 4b. Contexto mutado: otro conjunto no casa.
    neg = interpretacion(d0["variable"], d0["descripcion"], "conjunto-ajeno", rules, d0["diccionario"], d0["definicion_iri"])
    assert neg["estado"] != "respaldada_por_definicion", "contexto-mutado caso"
    # 4c. Otra IRI de definicion no casa.
    otra = d0["definicion_iri"] + "X"
    neg = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], rules, d0["diccionario"], otra)
    assert neg["estado"] != "respaldada_por_definicion", "otra-IRI caso"
    # 4d. Robustez positiva (no es un negativo): la unidad es metadato, no clave.
    assert d0["unidad"] == "" or isinstance(d0["unidad"], str)
    got = interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], rules, d0["diccionario"], d0["definicion_iri"])
    assert got["concepto"] == d0["concepto"], "robustez-positiva-unidad"
    # 4e. Codigo no acreditado: ningun codigo reclama catalogo/identidad/etnia/diagnostico.
    blob = json.dumps({"r": prop["reglas"], "c": prop["conceptos_nuevos"],
                     "d": [{k: v for k, v in d.items() if k != "criterio"} for d in prop["decisiones"]]})
    assert "sameAs" not in blob and "exactMatch" not in blob
    for d in prop["decisiones"]:
        assert d["catalogo_declarado"] == "", d["variable"]
        if d["representacion"] == "codigo":
            c = (d["concepto"] or "").lower()
            assert not any(w in c for w in ("catalogo", "identidad", "etnia", "indigena", "afro", "diagnostico", "cie")), d["variable"]
    for slug in prop["conceptos_nuevos"]:
        s = slug.lower()
        assert not any(w in s for w in ("catalogo", "identidad", "etnia", "diagnostico", "cie")), slug

    # 5. Conceptos: esquema {slug:[label,definicion,broader]}, broader valido, sin colision central.
    for slug, val in prop["conceptos_nuevos"].items():
        assert isinstance(val, list) and len(val) == 3, slug
        assert all(isinstance(x, str) for x in val[:2]), slug
        assert val[2] is None or val[2] in central_concepts, slug
        assert slug not in central_concepts, slug
    for slug in prop["conceptos_reutilizados"]:
        assert slug in central_concepts, slug
    usados = {d["concepto"] for d in prop["decisiones"] if d["concepto"]}
    assert usados == set(prop["conceptos_nuevos"]) | set(prop["conceptos_reutilizados"]), usados

    # 6. Pendientes con razon y sin concepto/regla.
    for d in prop["decisiones"]:
        if d["decision"] == "pendiente":
            assert d["concepto"] is None and d["regla_id"] is None, d["variable"]
            assert isinstance(d["criterio"], str) and len(d["criterio"]) > 20, d["variable"]

    # 7. Desglose excluyente suma 163 exacto.
    n_prop = sum(1 for d in prop["decisiones"] if d["decision"] == "propuesta-significado")
    n_pen_desc = sum(1 for d in prop["decisiones"] if d["decision"] == "pendiente" and "Pendiente de especificar" in d["criterio"])
    n_pen_id = sum(1 for d in prop["decisiones"] if d["decision"] == "pendiente" and "identidad" in d["criterio"].lower())
    n_pen_gen = sum(1 for d in prop["decisiones"] if d["decision"] == "pendiente" and "generica" in d["criterio"].lower())
    assert n_pen_desc == 75, n_pen_desc
    assert n_pen_id == 10, n_pen_id
    assert n_pen_gen == 2, n_pen_gen
    n_pen_contra = sum(1 for d in prop["decisiones"] if d["decision"] == "pendiente" and d["criterio"].startswith("Contradicción"))
    assert n_pen_contra == 1, n_pen_contra
    assert n_prop + n_pen_desc + n_pen_id + n_pen_gen + n_pen_contra == 163
    assert "163" in (MIA / "resultado.md").read_text(encoding="utf-8")

    # 8. Negativo unidad inferida: ningun concepto de edad declara "años"; unidad preservada vacia.
    for slug, val in prop["conceptos_nuevos"].items():
        if slug.startswith("edad-"):
            assert "años" not in val[0] + val[1], slug
    for d in prop["decisiones"]:
        if d["concepto"] and d["concepto"].startswith("edad-"):
            assert d["unidad"] == "", d["variable"]

    # 9. Evidencia sistematica por representacion en las 76 propuestas.
    for d in prop["decisiones"]:
        if d["decision"] != "propuesta-significado":
            continue
        desc, tipo, ej, rep = d["descripcion"], d["tipo"], d["ejemplo"], d["representacion"]
        if rep == "codigo":
            assert any(w in desc for w in ("Clave", "Identificador", "Indicador", "indicador numerico")), d["variable"]
            assert any(w in tipo.lower().replace("é", "e") for w in ("numerico", "entero", "binario")), d["variable"]
            assert ej == "" or any(c.isdigit() for c in ej), d["variable"]
        elif rep == "nombre":
            assert ej not in ("", "SI", "NO", "NO APLICA") and len(ej) > 2, d["variable"]
            assert "Nombre" in desc or "Nivel" in desc or "textual" in desc or "donde" in desc or "del nacido" in desc or "del difunto" in desc or "de la madre" in desc or "del parto" in desc, d["variable"]
        elif rep == "fecha":
            assert tipo == "Fecha", d["variable"]
        elif rep == "hora":
            assert tipo == "Hora", d["variable"]
    # Sufijo D por si solo no basta: ninguna decision con ejemplo SI/NO/NO APLICA usa codigo/nombre.
    for d in prop["decisiones"]:
        if d["decision"] == "propuesta-significado" and d["ejemplo"] in ("SI", "NO", "NO APLICA"):
            assert d["representacion"] == "no_especificada", d["variable"]

    print("OK agente-7: decisiones=163 propuestas=%d pendientes=%d reglas=%d conceptos_nuevos=%d" % (
        n_prop, 163 - n_prop, len(prop["reglas"]), len(prop["conceptos_nuevos"])))


if __name__ == "__main__":
    main()
