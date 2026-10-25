"""Verificador propio del auditor (ronda 3, agente 11). Re-ejecuta los chequeos
decisivos con el validador real del pipeline; falla con assert reales."""
import hashlib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ROOT = AQUI.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella, interpretacion  # noqa: E402
from integrar_contenido import valor as cvalor  # noqa: E402

PROP = {
    "a7": ROOT / "propuestas/ronda-3/agente-7-registro-civil" / "propuestas.json",
    "a3": ROOT / "propuestas/ronda-3/agente-3-cobertura" / "propuestas.json",
    "a8": ROOT / "propuestas/ronda-3/agente-8-educacion" / "propuestas.json",
    "a9": ROOT / "propuestas/ronda-3/agente-9-gobierno-digital" / "propuestas.json",
    "a10": ROOT / "propuestas/ronda-3/agente-10-territorio-economia" / "propuestas.json",
}
BASE = ["data/semantica/cobertura.json", "ontologia/semantica.json",
        "data/portal/contenido-inspeccion.json", "data/portal/inventario.json",
        "reports/pendientes-semanticos.json",
        "propuestas/ronda-3/integrador/asignaciones-semanticas.json"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def norm(tag, d):
    if tag == "a7":
        return (d["definicion_iri"], d["conjunto"], d["diccionario"], d["variable"],
                d["descripcion"], d.get("regla_id"), d["decision"] == "propuesta-significado")
    if tag == "a8":
        return (d["definicion_iri"], d["conjunto"], d["diccionario"], d["variable"],
                d["descripcion"], d.get("regla_id"), d["decision"] == "propuesta")
    if tag == "a9":
        return (d["definicion_iri"], d["conjunto"], d["diccionario"], d["variable"],
                d["descripcion"], d.get("regla"), d["veredicto"] == "propuesta")
    return (d["definicion_iri"], d["conjunto"], d["diccionario"], d["variable"],
            d["descripcion_literal"], d.get("regla"), d["decision"] == "proponer")


def main():
    aud = json.loads((AQUI / "auditoria.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    fuer = json.loads((AQUI / "fuente/huellas.json").read_text(encoding="utf-8"))
    assert fuer["estables"] is True
    for tag, p in PROP.items():
        assert sha(p) == aud["huellas_antes"][tag], tag
    assert len(cob["conceptos"]) == 103 and len(sem["conceptos"]) == 103
    assert aud["base_verificada"] is True

    props = {tag: json.loads(p.read_text(encoding="utf-8")) for tag, p in PROP.items()}
    vmap = {v["definicion_iri"]: v for v in cob["variables"]}
    # 1. dictamenes completos con motivo; sin rechazos duros pendientes de explicar
    for tag, dd in aud["dictamenes"].items():
        assert len(dd) == len(props[tag]["reglas"]), tag
        for rid, d in dd.items():
            assert d["dictamen"] in ("aceptar", "condicionado", "rechazar"), rid
            assert d["regla"] == rid and d["definicion_iri"] and d["concepto"], rid
            assert len(d["motivos"]) >= 1, rid
    # 2. TODAS las reglas disparan (777 positivos via interpretacion real)
    n = 0
    for tag, p in props.items():
        ext = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
            {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
             "representacion": r["representacion"], "nombres": r.get("nombres"),
             "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
             "definiciones": r.get("definiciones")} for r in p["reglas"]]}
        decs = {norm(tag, d)[0]: norm(tag, d) for d in p.get("decisiones", [])} if tag != "a3" else None
        for r in p["reglas"]:
            iri = r["definiciones"][0]
            if tag == "a3":
                ev = r["evidencia"][0]
                got = interpretacion(ev["variable"], ev["descripcion"], ev["conjunto"], ext,
                                     ev["diccionario"], iri)
            else:
                iri0, conj, dicc, var, desc, _rid, _es = decs[iri]
                got = interpretacion(var, desc, conj, ext, dicc, iri)
            assert got.get("estado") == "respaldada_por_definicion" and got.get("concepto") == r["concepto"], r["id"]
            n += 1
    assert n == sum(len(p["reglas"]) for p in props.values()) == 777, n
    # 3. negativos reales por agente (solo-nombre, contexto-mutado, otra-IRI)
    for tag, p in props.items():
        ext = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
            {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
             "representacion": r["representacion"], "nombres": r.get("nombres"),
             "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
             "definiciones": r.get("definiciones")} for r in p["reglas"]]}
        r0 = p["reglas"][0]
        iri = r0["definiciones"][0]
        if tag == "a3":
            ev = r0["evidencia"][0]
            var, desc, conj, dicc = ev["variable"], ev["descripcion"], ev["conjunto"], ev["diccionario"]
        else:
            d0 = next(d for d in p["decisiones"] if (d.get("regla_id") or d.get("regla")) == r0["id"])
            _i, conj, dicc, var, desc = norm(tag, d0)[:5]
        assert interpretacion(var, "Descripcion inexistente XYZ", conj, ext, dicc, iri)["estado"] != "respaldada_por_definicion"
        assert interpretacion(var, desc, "00000000-0000-4000-8000-000000000000", ext, dicc, iri)["estado"] != "respaldada_por_definicion"
        assert interpretacion(var, desc, conj, ext, dicc, iri + "X")["estado"] != "respaldada_por_definicion"
    # 4. calificadores no propagados (SHD + sedes): limite real del pipeline
    for tag, key in (("a3", "distrito_desarrollo_rural"), ("a8", "sede")):
        p = props[tag]
        cal = [r for r in p["reglas"] if r.get("calificador")]
        assert len(cal) == (10 if tag == "a3" else 20), (tag, len(cal))
        por_concepto = {}
        for r in cal:
            por_concepto.setdefault(r["concepto"], []).append(json.dumps(r["calificador"], sort_keys=True))
        for slug, vals in por_concepto.items():
            assert len(set(vals)) == len(vals), (tag, slug)
        r = cal[0]
        vv = vmap[r["definiciones"][0]]
        ext = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
            {"id": x["id"], "concepto": x["concepto"], "descripciones": x["descripciones"],
             "representacion": x["representacion"], "nombres": x.get("nombres"),
             "conjuntos": x.get("conjuntos"), "diccionarios": x.get("diccionarios"),
             "definiciones": x.get("definiciones")} for x in p["reglas"]]}
        assert "calificador" not in interpretacion(vv["variable"], vv["descripcion"], vv["conjunto"], ext,
                                                  vv["diccionario"], r["definiciones"][0]), tag
    # 5. colisiones, sameAs, U+FFFD
    assert aud["conflictos_iris"]["nuevos_vs_nucleo"] == []
    assert aud["conflictos_iris"]["cruzados"] == []
    for tag, p in PROP.items():
        blob = p.read_text(encoding="utf-8")
        assert "\ufffd" not in blob, tag
        limpio = re.sub(r"[Ss]in (owl:sameAs|skos:exactMatch)[^.]*\.", "", blob)
        limpio = re.sub(r"sin (sameAs|exactMatch)[^.]*\.", "", limpio)
        assert not re.search(r'"sameAs"\s*:|owl:sameAs|skos:exactMatch|"exactMatch"\s*:', limpio), tag
    # 6. A10 usa interpretacion() local en su verificador: se senala y se compensa
    # re-ejecutando las 419 con el pipeline real (paso 2 OK). Solo se exige existencia.
    assert (ROOT / "propuestas/ronda-3/agente-10-territorio-economia/scripts/verificar.py").exists()
    assert aud["comportamiento_pipeline"]["a10_verificador_local"].startswith("scripts/verificar.py")
    print("OK auditoria-11: 777 positivos, 15 negativos, huellas estables, 0 colisiones")


if __name__ == "__main__":
    main()
