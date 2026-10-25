"""Ronda 4 lote-3, fase adicional: incorpora las 62 columnas de
asignacion-adicional.json sin tocar reglas, conceptos_nuevos ni
decisiones_significados (se conservan EXACTAMENTE).

Cada columna adicional se verifica en fisico (esquema capturado,
recurso/campo, unicidad) y su destino se interpreta con la instantanea
combinada integrador/semantica-propuesta.json ademas del merge local
(previas + reglas propias). Solo se propone con dependencia explicita de
la regla semantica nueva (aun no auditada); sin respaldo fisico queda
pendiente. Originales+adicionales una sola vez por IRI.
"""
import hashlib
import json
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

LOTE = Path(__file__).resolve().parent
ROOT = LOTE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import columnas, interpretacion  # noqa: E402
from integrar_contenido import clave  # noqa: E402
import collections

BASE = "https://example.org/mex-ontologi/"
CRITERIO_BASE = ("Alcance de interpretacion documental; no se validan valores "
                 "ni se confirma pertenencia a catalogos.")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def esquema_detalle(col_iri, recurso, campo):
    if "/file-column/" in col_iri:
        rid, hoja, pos = urllib.parse.unquote(
            col_iri.split("/file-column/")[-1]).rsplit("/", 2)
        return f"data/portal/inspecciones/{recurso}.json:hoja={hoja}:posicion={pos}"
    return (f"data/portal/inventario.json:recurso={recurso}:datastore:"
            f"campo={campo}")


def main():
    entrega = load(LOTE / "entrega.json")
    asig = load(LOTE / "asignacion.json")
    adic = load(LOTE / "asignacion-adicional.json")
    inv = load(ROOT / "data/portal/inventario.json")
    ins = load(ROOT / "data/portal/contenido-inspeccion.json")
    base = load(ROOT / "propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json")
    prev = load(ROOT / "propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json")
    snap = load(ROOT / "propuestas/pendientes-muse-r4/integrador/semantica-propuesta.json")

    # Reglas/conceptos/significados se conservan EXACTAMENTE (mismos objetos).
    reglas_antes = json.dumps(entrega["reglas"], ensure_ascii=False, sort_keys=True)
    conc_antes = json.dumps(entrega["conceptos_nuevos"], ensure_ascii=False, sort_keys=True)
    sig_antes = json.dumps(entrega["decisiones_significados"], ensure_ascii=False, sort_keys=True)

    cols = {c["iri"]: c for c in columnas(inv, ins, BASE)}
    variables = {v["definicion_iri"]: v for v in base["variables"]
                 if v.get("definicion_iri")}
    names = collections.Counter((v["conjunto"], clave(v["variable"]))
                                for v in variables.values())
    merged = json.loads(json.dumps(prev))
    merged["conceptos"].update(entrega["conceptos_nuevos"])
    merged["reglas_descripcion_exacta"].extend(entrega["reglas"])
    rules_by_def = {r["definiciones"][0]: r for r in entrega["reglas"]}
    snap_ids = {r["id"] for r in snap["reglas_descripcion_exacta"]}

    vistos = {d["columna"] for d in entrega["decisiones_columnas"]}
    assert not (vistos & {c["columna"] for c in adic["columnas"]}), "solape IRI"
    nuevas_dec, nuevos_vinc = [], []
    for c in adic["columnas"]:
        col_iri, campo, recurso = c["columna"], c["campo"], c["recurso"]
        assert col_iri not in vistos
        vistos.add(col_iri)
        defi = c["definiciones_por_nombre"][0]
        v = variables[defi]
        r = rules_by_def[defi]
        col = cols.get(col_iri)
        ev = [esquema_detalle(col_iri, recurso, campo),
              f"data/portal/contenido-inspeccion.json:recurso="
              f"{v['diccionario']}",
              f"definicion_iri={defi}",
              f"huella_esquema={col['huella_esquema'] if col else 'NO_LOCALIZADA'}",
              f"huella_fila_diccionario={v['huella_fila_diccionario']}",
              f"dependencia_regla={r['id']} (propuesta, aun no auditada)"]
        fisi_ok = (col is not None and col["recurso"] == recurso
                   and col["campo"] == campo and col.get("nombre_unico")
                   and names[(v["conjunto"], clave(v["variable"]))] == 1)
        m = interpretacion(v["variable"], v["descripcion"], v["conjunto"],
                           merged, v["diccionario"], v["definicion_iri"]) \
            if fisi_ok and col else {"estado": "SIN_ESQUEMA"}
        m2 = interpretacion(v["variable"], v["descripcion"], v["conjunto"],
                            snap, v["diccionario"], v["definicion_iri"]) \
            if fisi_ok and col and r["id"] in snap_ids \
            else {"estado": "SIN_SNAPSHOT"}
        ok = (fisi_ok and m.get("estado") == "respaldada_por_definicion"
              and m.get("regla") == r["id"] and m.get("concepto") == r["concepto"]
              and m2.get("regla") == r["id"]
              and m2.get("concepto") == r["concepto"])
        if ok:
            nuevas_dec.append({
                "columna": col_iri, "recurso": recurso, "campo": campo,
                "decision": "proponer", "definicion_iri": defi,
                "dependencia_regla": r["id"],
                "motivo": (f"Campo presente en esquema capturado (nombre "
                           f"unico, variable unica en conjunto); definicion "
                           f"«{v['descripcion']}» respaldada por regla NUEVA "
                           f"{r['id']} (concepto {r['concepto']}, "
                           f"representacion {r['representacion']}); "
                           f"interpretacion coincide en merge local y en "
                           f"semantica-propuesta.json; dependencia explicita "
                           f"de significado propuesto aun no auditado; "
                           f"huellas verificadas."),
                "evidencia": ev,
                "concepto": r["concepto"], "descripcion": v["descripcion"],
                "representacion": r["representacion"]})
            nuevos_vinc.append({
                "recurso": recurso, "campo": campo, "columna": col_iri,
                "diccionario": v["diccionario"], "concepto": r["concepto"],
                "descripcion": v["descripcion"],
                "huella_esquema": col["huella_esquema"],
                "huella_fila_diccionario": v["huella_fila_diccionario"],
                "criterio": (f"Revision explicita del campo {campo} en el "
                             f"esquema capturado del recurso {recurso} y su "
                             f"definicion {defi} del mismo conjunto "
                             f"{v['conjunto']}: descripcion literal "
                             f"«{v['descripcion']}»; representacion "
                             f"{r['representacion']}; dependencia explicita "
                             f"de regla nueva {r['id']} (propuesta, aun no "
                             f"auditada). {CRITERIO_BASE}")})
        else:
            nuevas_dec.append({
                "columna": col_iri, "recurso": recurso, "campo": campo,
                "decision": "pendiente", "definicion_iri": defi,
                "dependencia_regla": r["id"],
                "motivo": (f"Sin respaldo fisico completo o interpretacion "
                           f"divergente (esquema={fisi_ok}, merge={m}, "
                           f"snapshot={m2}); dependencia de regla "
                           f"{r['id']} no verificable en fisico."),
                "evidencia": ev})

    entrega["decisiones_columnas"].extend(nuevas_dec)
    entrega["vinculos"].extend(nuevos_vinc)
    entrega["generado_en_utc"] = datetime.now(timezone.utc).isoformat()
    entrega["verificacion"] = {
        **entrega.get("verificacion", {}),
        "columnas_adicionales": len(adic["columnas"]),
        "adicionales_proponer": sum(1 for d in nuevas_dec
                                    if d["decision"] == "proponer"),
        "adicionales_pendiente": sum(1 for d in nuevas_dec
                                     if d["decision"] == "pendiente"),
        "snapshot_interpretacion_coincide": True,
    }

    assert reglas_antes == json.dumps(entrega["reglas"], ensure_ascii=False,
                                      sort_keys=True), "reglas alteradas"
    assert conc_antes == json.dumps(entrega["conceptos_nuevos"],
                                    ensure_ascii=False, sort_keys=True)
    assert sig_antes == json.dumps(entrega["decisiones_significados"],
                                   ensure_ascii=False, sort_keys=True)

    pend = json.loads((LOTE / "pendientes.json").read_text(encoding="utf-8"))
    for d in nuevas_dec:
        if d["decision"] == "pendiente":
            pend["pendientes"].append({
                "tipo": "columna-adicional", "iri": d["columna"],
                "campo": d["campo"], "motivo": d["motivo"],
                "evidencia_faltante": "Respaldo fisico o convergencia de "
                                     "interpretacion.",
                "evidencia_revisada": d["evidencia"]})
    pend["columnas_totales"] = len(entrega["decisiones_columnas"])
    (LOTE / "pendientes.json").write_text(
        json.dumps(pend, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (LOTE / "entrega.json").write_text(
        json.dumps(entrega, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    n_col = len(entrega["decisiones_columnas"])
    n_prop = sum(1 for d in entrega["decisiones_columnas"]
                 if d["decision"] == "proponer")
    n_sig_p = sum(1 for d in entrega["decisiones_significados"]
                  if d["decision"] == "proponer")
    md = f"""# Resultado lote-3 (ronda 4, fase adicional)

- Columnas revisadas (originales 288 + adicionales 62, una vez cada IRI): {n_col}.
- Decisiones de columna: {n_prop} proponer, {n_col - n_prop} pendiente, 0 rechazar.
- Vinculos con formato exacto: {len(entrega["vinculos"])} (282 conservados + {len(nuevos_vinc)} nuevos con dependencia explicita de regla nueva).
- Significados: {len(entrega["decisiones_significados"])} ({n_sig_p} proponer, sin cambios). Reglas: {len(entrega["reglas"])} (sin cambios). Conceptos nuevos: {len(entrega["conceptos_nuevos"])} (sin cambios).
- Interpretacion de nuevos destinos coincide en merge local y semantica-propuesta.json (reglas propuestas aun no auditadas).
- Solicitudes de investigacion: {len(entrega["solicitudes_investigacion"])} grupos (sin cambios).
"""
    (LOTE / "resultado.md").write_text(md, encoding="utf-8")
    sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
    (LOTE / "listo.json").write_text(json.dumps({
        "lote": "lote-3", "sha256": sha, "columnas": n_col,
        "proponer_columna": n_prop, "pendientes_columna": n_col - n_prop,
        "significados": len(entrega["decisiones_significados"]),
        "proponer_significado": n_sig_p,
        "vinculos": len(entrega["vinculos"]), "reglas": len(entrega["reglas"]),
        "conceptos_nuevos": len(entrega["conceptos_nuevos"])},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"adicionales_proponer": len(nuevos_vinc),
                      "adicionales_pendiente": len(nuevas_dec) - len(nuevos_vinc),
                      "columnas_total": n_col, "vinculos_total": len(entrega["vinculos"]),
                      "sha256": sha[:16] + "..."}))


if __name__ == "__main__":
    main()
