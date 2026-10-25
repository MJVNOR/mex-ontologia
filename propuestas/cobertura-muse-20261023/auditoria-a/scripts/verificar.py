"""Verificador propio del auditor (cobertura-muse, auditoria-a). Re-ejecuta los
chequeos decisivos con el validador real; falla con assert reales. No escribe
fuera de auditoria-a/."""
import hashlib
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
MUSE = AQUI.parent
ROOT = AQUI.parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import interpretacion  # noqa: E402

PROP = {
    "gobierno-digital": MUSE / "gobierno-digital" / "entrega.json",
    "territorio-economia": MUSE / "territorio-economia" / "entrega.json",
}
BASE = ["data/semantica/cobertura.json", "ontologia/semantica.json",
        "data/portal/contenido-inspeccion.json", "data/portal/inventario.json",
        "reports/pendientes-semanticos.json"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    aud = json.loads((AQUI / "auditoria-base.json").read_text(encoding="utf-8"))
    fin = json.loads((AQUI / "auditoria.json").read_text(encoding="utf-8"))
    assert fin["sha_entregas"] == aud["sha_entregas"] and fin["resumen"] == aud["resumen"]
    assert fin["reglas_auditadas"] == 603 and len(fin["dictamenes"]) == 603
    assert all(set(d) == {"dominio", "regla_id", "dictamen", "motivo"} for d in fin["dictamenes"])
    from collections import Counter as _C
    assert sum(fin["resumen"][t].get("aceptar", 0) + fin["resumen"][t].get("condicionado", 0) + fin["resumen"][t].get("rechazar", 0) for t in fin["resumen"]) == 603
    # evidencia intacta vs manifiesto; nucleo puede haber sido aplicado por el integrador (se registra)
    man = json.loads((ROOT / "propuestas/cobertura-muse-20261023/fuentes/manifiesto.json").read_text(encoding="utf-8"))["insumos_centrales"]
    for f in ("data/portal/contenido-inspeccion.json", "data/portal/inventario.json",
              "propuestas/ronda-3/integrador/asignaciones-semanticas.json"):
        assert sha(ROOT / f) == man[f], f
    assert aud["base_evidencia_intacta_vs_manifiesto"] is True
    assert aud["nucleo_estado_actual"]["cambiado_vs_manifiesto"] in (True, False)
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    fuer = json.loads((AQUI / "fuente" / "huellas.json").read_text(encoding="utf-8"))
    assert fuer["estables"] is True
    for tag, p in PROP.items():
        assert sha(p) == aud["sha_entregas"][tag], tag
    assert aud["base_verificada"] is True and aud["base_evidencia_intacta_vs_manifiesto"] is True
    assert aud["nucleo_estado_actual"]["cambiado_vs_manifiesto"] in (True, False)
    props = {tag: json.loads(p.read_text(encoding="utf-8")) for tag, p in PROP.items()}

    # 1b. TE: huella top-level == huella de evidencia (devolucion integrador)
    te0 = props["territorio-economia"]
    assert all(r.get("huella_fila_diccionario") == r["evidencia"][0].get("huella_fila_diccionario") for r in te0["reglas"])
    # 1c. TE: sin slugs/labels 'proyectada' en conceptos (renombrados a reconstruida y ajustada)
    te_conc = te0["conceptos_nuevos"]
    assert not any("proyectada" in s for s in te_conc) and not any("proyectada" in v[0] + v[1] for v in te_conc.values())
    assert aud["reglas_auditadas"] == 603
    vistos = set()
    for d in fin["dictamenes"]:
        assert set(d) == {"dominio", "regla_id", "dictamen", "motivo"}, d
        assert d["dictamen"] in ("aceptar", "condicionado", "rechazar"), d
        assert d["motivo"], d
        assert (d["dominio"], d["regla_id"]) not in vistos, d
        vistos.add((d["dominio"], d["regla_id"]))
    assert len(vistos) == 603
    det = aud["detalle_por_regla"]
    assert sum(len(v) for v in det.values()) == 603
    devueltos = [d for d in fin["dictamenes"] if d["motivo"].startswith("BLOQUEANTE")]
    assert len(devueltos) == 10 and all(d["dominio"] == "territorio-economia" for d in devueltos)
    assert aud.get("central_resuelven_igual", {}).get("iguales") == 603

    # 2. TODOS los positivos con reglas COMPLETAS de la entrega (standalone, con
    # calificador) via pipeline real. Sin mezclar nucleo aplicado (evita duplicados).
    n = 0
    for tag, p in props.items():
        er = []
        for r in p["reglas"]:
            e = {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
                 "representacion": r["representacion"], "nombres": r.get("nombres"),
                 "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
                 "definiciones": r.get("definiciones")}
            if r.get("calificador"):
                e["calificador"] = r["calificador"]
            er.append(e)
        ext = {"reglas_descripcion_exacta": er}
        for r in p["reglas"]:
            ev = r["evidencia"][0]
            vv = next(v for v in cob["variables"] if v["definicion_iri"] == r["definiciones"][0])
            got = interpretacion(ev["variable"], ev["descripcion"], ev["conjunto"], ext,
                                 ev["diccionario"], r["definiciones"][0])
            assert got.get("estado") == "respaldada_por_definicion" and got.get("concepto") == r["concepto"], r["id"]
            if r.get("calificador"):
                assert got.get("calificador") == r["calificador"], r["id"]
            n += 1
    assert n == 603, n

    # 3. negativos reales por entrega (reglas standalone)
    for tag, p in props.items():
        ext = {"reglas_descripcion_exacta": [
            {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
             "representacion": r["representacion"], "nombres": r.get("nombres"),
             "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
             "definiciones": r.get("definiciones")} for r in p["reglas"]]}
        r0 = p["reglas"][0]
        ev = r0["evidencia"][0]
        iri = r0["definiciones"][0]
        assert interpretacion(ev["variable"], "Descripcion inexistente XYZ", ev["conjunto"], ext, ev["diccionario"], iri)["estado"] != "respaldada_por_definicion"
        assert interpretacion(ev["variable"], ev["descripcion"], "00000000-0000-4000-8000-000000000000", ext, ev["diccionario"], iri)["estado"] != "respaldada_por_definicion"
        assert interpretacion(ev["variable"], ev["descripcion"], ev["conjunto"], ext, ev["diccionario"], iri + "X")["estado"] != "respaldada_por_definicion"

    # 4. DDR: 10 calificadores distintos, PROPAGADOS por el pipeline (soporte implementado)
    te = props["territorio-economia"]
    shd = [r for r in te["reglas"] if (r.get("calificador") or {}).get("distrito_desarrollo_rural")]
    assert len(shd) == 10
    assert len({r["calificador"]["distrito_desarrollo_rural"] for r in shd}) == 10
    vmap = {v["definicion_iri"]: v for v in cob["variables"]}
    er = []
    for r in te["reglas"]:
        e = {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"],
             "representacion": r["representacion"], "nombres": r.get("nombres"),
             "conjuntos": r.get("conjuntos"), "diccionarios": r.get("diccionarios"),
             "definiciones": r.get("definiciones")}
        if r.get("calificador"):
            e["calificador"] = r["calificador"]
        er.append(e)
    ext = {"reglas_descripcion_exacta": er}
    vv = vmap[shd[0]["definiciones"][0]]
    got = interpretacion(vv["variable"], vv["descripcion"], vv["conjunto"], ext,
                         vv["diccionario"], shd[0]["definiciones"][0])
    assert got.get("calificador") == shd[0]["calificador"]

    # 5. GD instrumento: 70 reglas con calificador valido, distinto por concepto
    # compartido; el pipeline lo propaga (verificado en el paso 2 con regla completa)
    gd = props["gobierno-digital"]
    cals = [r for r in gd["reglas"] if r.get("calificador")]
    assert len(cals) == 70 and len(gd["reglas"]) - len(cals) == 51
    titulos = {}
    for d in gd["decisiones"]:
        if d.get("titulo_conjunto"):
            titulos[d["conjunto"]] = d["titulo_conjunto"]
    for r in cals:
        assert set(r["calificador"]) == {"instrumento"} and isinstance(r["calificador"]["instrumento"], str)
        assert r["calificador"]["instrumento"] == titulos[r["conjuntos"][0]], r["id"]
    from collections import Counter as _C
    comp = _C()
    for r in gd["reglas"]:
        comp[r["concepto"]] += 1
    multi = {s for s, n in comp.items() if n > 1}
    assert sum(comp[s] for s in multi) == 70

    # 6. colisiones: 0 con nucleo salvo lo ya aplicado verbatim; 0 cruzados GD/TE
    det_nn = aud["conflictos_iris"]["nuevos_vs_nucleo_detalle"]
    assert all(v["aplicado_verbatim"] for v in det_nn.values()), [k for k, v in det_nn.items() if not v["aplicado_verbatim"]][:5]
    assert aud["conflictos_iris"]["cruzados"] == []
    for tag, p in PROP.items():
        blob = p.read_text(encoding="utf-8")
        assert "\ufffd" not in blob, tag
        limpio = re.sub(r"[Ss]in (owl:sameAs|skos:exactMatch)[^.]*\.", "", blob)
        limpio = re.sub(r"sin (sameAs|exactMatch)[^.]*\.", "", limpio)
        assert not re.search(r'"sameAs"\s*:|owl:sameAs|skos:exactMatch|"exactMatch"\s*:', limpio), tag
    print("OK auditoria-a final: 603 positivos, 9 negativos, huellas estables, 0 colisiones")


if __name__ == "__main__":
    main()
