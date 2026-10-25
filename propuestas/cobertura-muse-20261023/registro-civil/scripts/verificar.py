"""Verificador propio cobertura-muse registro civil. Solo lee congeladas/central
(solo lectura) y mi carpeta; no genera nada central ni reescribe entregas.
No ejecuta suite central. Falla con asserts reales."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MIA = ROOT / "propuestas" / "cobertura-muse-20261023" / "registro-civil"
FROZ = ROOT / "propuestas" / "cobertura-muse-20261023" / "fuentes"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402

REPS = {"codigo", "nombre", "fecha", "hora", "anio", "mes", "dia", "no_especificada"}
CAL_ESPERADO = {
    "r3a7-nac-condicionhijoanterior-codigo", "r3a7-nac-condicionhijoanteriord-nombre",
    "r3a7-nac-edad-no_especificada", "r3a7-nac-edadpadre-no_especificada",
    "r3a7-nac-fechanacimiento-fecha", "r3a7-nac-fechanacimientomadre-fecha",
    "r3a7-nac-hijosnacidosmuertos-no_especificada", "r3a7-nac-hijosnacidosvivos-no_especificada",
    "r3a7-nac-hijossobrevivientes-no_especificada", "r3a7-nac-horanacimiento-hora",
    "r3a7-nac-nacioextranjero-codigo", "r3a7-nac-nacioextranjerod-no_especificada",
    "r3a7-nac-tipocesarea-codigo", "r3a7-nac-tipocesaread-nombre",
    "r3a7-nac-vivehijoanterior-codigo", "r3a7-nac-vivehijoanteriord-no_especificada",
    "r3a7-seed-atencionmedica-codigo", "r3a7-seed-atencionmedicad-no_especificada",
    "r3a7-seed-practiconecropsia-codigo", "r3a7-seed-practiconecropsiad-no_especificada",
    "r3a7-seed-realizo-cirugia-codigo", "r3a7-seed-realizo-cirugiad-no_especificada",
    "r3a7-seed-resideextranjero-no_especificada",
}


def main():
    # 0. Insumos estables contra manifiesto.
    m = json.loads((FROZ / "manifiesto.json").read_text(encoding="utf-8"))
    for c in m["copias"]:
        assert hashlib.sha256((ROOT / c["copia"]).read_bytes()).hexdigest() == c["sha256"], c["copia"]
    for p, h in m["insumos_centrales"].items():
        assert hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h, p

    ent = json.loads((MIA / "entrega.json").read_text(encoding="utf-8"))
    froz = json.loads((FROZ / "agente-7-registro-civil" / "propuestas.json").read_text(encoding="utf-8"))
    aud = json.loads((FROZ / "agente-11-auditoria" / "auditoria.json").read_text(encoding="utf-8"))
    insp = {r["id"]: r for r in json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))["recursos"]}
    central_concepts = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))["conceptos"]
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))

    # 1. Decisiones: 163, una por definición asignada, valores exactos.
    assert len(ent["decisiones"]) == 163
    assert {d["definicion_iri"] for d in ent["decisiones"]} == {d["definicion_iri"] for d in froz["decisiones"]}
    for d in ent["decisiones"]:
        assert d["decision"] in ("proponer", "pendiente"), d["definicion_iri"]
        if d["decision"] == "proponer":
            assert "regla_id" in d and "motivo" not in d, d["definicion_iri"]
        else:
            assert "motivo" in d and len(d["motivo"]) > 20 and "regla_id" not in d, d["definicion_iri"]
        v = next(x for x in froz["decisiones"] if x["definicion_iri"] == d["definicion_iri"])
        for k in ("variable", "descripcion", "huella_fila_diccionario", "conjunto", "diccionario"):
            assert d[k] == v[k], d["definicion_iri"]
        r = insp[d["diccionario"]]
        idx = int(d["definicion_iri"].rsplit("%2F", 1)[1]) - 1
        assert huella(r["definiciones"][idx]) == d["huella_fila_diccionario"], d["variable"]

    # 2. Reglas: mismo alcance que la copia (nombres/descripciones/conjuntos/diccionarios/definiciones/huella).
    assert len(ent["reglas"]) == 75 and len({r["id"] for r in ent["reglas"]}) == 75
    assert {r["id"] for r in ent["reglas"]} == {r["id"] for r in froz["reglas"]}
    for r in ent["reglas"]:
        fr = next(x for x in froz["reglas"] if x["id"] == r["id"])
        for k in ("nombres", "descripciones", "conjuntos", "diccionarios", "definiciones", "representacion"):
            assert r[k] == fr[k], r["id"]
        assert r["representacion"] in REPS, r["id"]
        assert r["huella_fila_diccionario"] == next(
            x["huella_fila_diccionario"] for x in ent["decisiones"] if x.get("regla_id") == r["id"])
        assert isinstance(r["limites"], list) and len(r["limites"]) >= 1, r["id"]
        assert r["fuente_revision"] == "propuestas/cobertura-muse-20261023/registro-civil/entrega.json", r["id"]
        assert set(r["evidencia"]) >= {"descripcion", "tipo", "unidad", "ejemplo", "catalogo_declarado"}, r["id"]
    assert {r["id"] for r in ent["reglas"] if "calificador" in r} == CAL_ESPERADO
    for r in ent["reglas"]:
        if "calificador" in r:
            assert r["calificador"].get("alcance") == "inferencia-contextual-publicada", r["id"]

    # 3. Conceptos: esquema, sin colisión, broader válido, neutros sin sujeto añadido.
    assert len(ent["conceptos_nuevos"]) == 49
    for slug, val in ent["conceptos_nuevos"].items():
        assert isinstance(val, list) and len(val) == 3, slug
        assert slug not in central_concepts, slug
        assert val[2] is None or val[2] in central_concepts, slug
    assert ent["conceptos_reutilizados"] == ["sexo-difunto"]
    # Neutros no añaden población fuera del calificador.
    for slug in ("atencion-medica-segun-definicion", "cirugia-segun-definicion", "autopsia-segun-definicion",
                 "hijos-nacidos-muertos-segun-definicion", "hijos-nacidos-vivos-segun-definicion",
                 "hijos-sobrevivientes-segun-definicion", "condicion-hijo-anterior-segun-definicion",
                 "supervivencia-hijo-anterior-segun-definicion", "fecha-nacimiento-segun-definicion",
                 "hora-nacimiento-segun-definicion"):
        txt = ent["conceptos_nuevos"][slug][1]
        assert "difunto" not in txt and "madre" not in txt and "nacido" not in txt, slug
    for slug in ("fecha-nacimiento-madre", "edad-madre", "edad-padre"):
        assert "del nacido" not in ent["conceptos_nuevos"][slug][1], slug

    # 4. Evidencia por representación (sistemático) + sufijo D insuficiente + sin años inferidos.
    for d in ent["decisiones"]:
        if d["decision"] != "proponer":
            continue
        r = next(x for x in ent["reglas"] if x["id"] == d["regla_id"])
        desc, tipo, ej, rep = d["descripcion"], d["tipo"], d["ejemplo"], r["representacion"]
        if rep == "codigo":
            assert any(w in desc for w in ("Clave", "Identificador", "Indicador", "indicador numerico")), d["variable"]
            assert any(w in tipo.lower().replace("é", "e") for w in ("numerico", "entero", "binario")), d["variable"]
        elif rep == "nombre":
            assert ej not in ("", "SI", "NO", "NO APLICA") and len(ej) > 2, d["variable"]
        elif rep == "fecha":
            assert tipo == "Fecha", d["variable"]
        elif rep == "hora":
            assert tipo == "Hora", d["variable"]
        if ej in ("SI", "NO", "NO APLICA"):
            assert rep == "no_especificada", d["variable"]
    for slug, val in ent["conceptos_nuevos"].items():
        if slug.startswith("edad-"):
            assert "años" not in val[0] + val[1], slug

    # 5. Preservación: 0 intersección con respaldadas/candidatas (definiciones e ids).
    central_defs = set()
    for r in sem["reglas_descripcion_exacta"]:
        central_defs.update(r.get("definiciones", []))
    assert not ({d["definicion_iri"] for d in ent["decisiones"]} & central_defs)
    assert not ({r["id"] for r in ent["reglas"]} & {r["id"] for r in sem["reglas_descripcion_exacta"]})
    assert "sameAs" not in json.dumps(ent["reglas"]) and "exactMatch" not in json.dumps(ent["reglas"])
    assert all(d["catalogo_declarado"] == "" for d in ent["decisiones"])

    # 6. Positivos en pipeline + negativos reales.
    rules = {"reglas_descripcion_exacta": ent["reglas"], "conceptos": {}}
    for d in ent["decisiones"]:
        if d["decision"] == "proponer":
            r = next(x for x in ent["reglas"] if x["id"] == d["regla_id"])
            got = interpretacion(d["variable"], d["descripcion"], d["conjunto"], rules, d["diccionario"], d["definicion_iri"])
            assert got["estado"] == "respaldada_por_definicion" and got["concepto"] == r["concepto"], d["variable"]
    d0 = next(x for x in ent["decisiones"] if x["decision"] == "proponer")
    assert interpretacion(d0["variable"], "Otra descripcion inexistente", d0["conjunto"], rules,
                          d0["diccionario"], d0["definicion_iri"])["estado"] != "respaldada_por_definicion"
    assert interpretacion(d0["variable"], d0["descripcion"], "conjunto-ajeno", rules,
                          d0["diccionario"], d0["definicion_iri"])["estado"] != "respaldada_por_definicion"
    assert interpretacion(d0["variable"], d0["descripcion"], d0["conjunto"], rules,
                          d0["diccionario"], d0["definicion_iri"] + "X")["estado"] != "respaldada_por_definicion"

    # 7. Desglose excluyente + pendientes.json + resultado.
    n_prop = sum(1 for d in ent["decisiones"] if d["decision"] == "proponer")
    mots = [d.get("motivo", "") for d in ent["decisiones"] if d["decision"] == "pendiente"]
    assert n_prop == 75
    assert sum("Pendiente de especificar" in m for m in mots) == 75
    assert sum("identidad" in m.lower() for m in mots) == 10
    assert sum("generica" in m.lower() for m in mots) == 2
    assert sum(m.startswith("Contradicción") for m in mots) == 1
    assert n_prop + len(mots) == 163
    pen = json.loads((MIA / "pendientes.json").read_text(encoding="utf-8"))
    assert len(pen["preguntas"]) >= 6
    mias = {d["definicion_iri"] for d in ent["decisiones"]}
    for q in pen["preguntas"]:
        assert set(q["definiciones"]) <= mias, q["id"]
    assert (MIA / "resultado.md").read_text(encoding="utf-8").count("163") >= 1
    if (MIA / "listo.json").exists():
        li = json.loads((MIA / "listo.json").read_text(encoding="utf-8"))
        assert li["sha256"] == hashlib.sha256((MIA / "entrega.json").read_bytes()).hexdigest()
        assert li["conteos"] == {"decisiones": 163, "proponer": 75, "pendiente": 88, "reglas": 75, "conceptos_nuevos": 49}

    print("OK cobertura-muse registro-civil: 163/75/88/75/49; 23 condicionados corregidos; 23+232 preservadas")


if __name__ == "__main__":
    main()
