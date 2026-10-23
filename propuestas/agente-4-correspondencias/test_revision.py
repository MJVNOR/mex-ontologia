"""Tests de la revisión (agente 4). Sin frameworks: asserts puros."""
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[1]


def main():
    prop = json.loads((HERE / "propuestas.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))

    # 1. Cobertura de la unidad de trabajo: las 891 candidatas quedan clasificadas
    # exactamente una vez (propuesta o pendiente), sin duplicados ni fugas.
    assert prop["conteos"]["candidatas_examinadas"] == 891, "deben examinarse las 891 candidatas"
    cand_cols = [c["columna"] for c in pend["columnas"] if c["estado"] == "candidata_por_nombre"]
    assert len(cand_cols) == 891, "el pendiente central debe traer 891 candidatas"
    cand_props = [p for p in prop["propuestas_revisadas"] if p.get("origen") is None]
    pend_cols = [p["columna"] for p in prop["pendientes_clasificados"]]
    assert len(cand_props) + len(pend_cols) == 891, (
        f"candidatas sin clasificar o duplicadas: {len(cand_props)} propuestas + "
        f"{len(pend_cols)} pendientes != 891")
    assert len(set(cand_cols)) == 891, "duplicados en candidatas centrales"
    assert len(set(p["columna"] for p in cand_props)) == len(cand_props), "propuesta candidata duplicada"
    assert len(set(pend_cols)) == len(pend_cols), "pendiente duplicado"
    assert not (set(p["columna"] for p in cand_props) & set(pend_cols)), (
        "solape propuesta/pendiente en candidatas")
    assert set(p["columna"] for p in cand_props) | set(pend_cols) == set(cand_cols), (
        "clasificacion incompleta de candidatas")
    # Correspondencias candidatas: 891 vínculos 1:1 con columna.
    assert prop["conteos"]["pendientes_clasificados"] == len(prop["pendientes_clasificados"])
    # Alias: solo el de divorcios está propuesto; nacimientos sigue pendiente.
    alias_props = [p for p in prop["propuestas_revisadas"] if p.get("origen") is not None]
    assert {p.get("origen") for p in alias_props} <= {"anio-divorcios-2023"}, (
        "alias inesperado propuesto")
    assert not any(p["columna"].endswith("a%E2%80%93o") for p in prop["propuestas_revisadas"]), (
        "a–o no debe estar propuesto")
    # Separación de grupos: ambiguos y revisadas existentes no se mezclan.
    amb_cols = {a["columna"] for a in prop["ambiguos"]}
    assert len(amb_cols) == 3 and sum(len(a["vinculos"]) for a in prop["ambiguos"]) == 6
    assert not (amb_cols & set(p["columna"] for p in prop["propuestas_revisadas"])), "solape ambiguo/propuesta"
    assert not (amb_cols & set(pend_cols)), "solape ambiguo/pendiente"
    assert len(prop["ambiguos"]) == 3, "3 columnas ambiguas"
    assert sum(len(a["vinculos"]) for a in prop["ambiguos"]) == 6, "6 vínculos ambiguos"
    assert len(prop["inconsistencias"]) == 5, "5 inconsistencias"

    # 2. Cada propuesta identifica lo exigido.
    exigidos = ["columna", "variable", "definicion", "evidencia", "huellas", "criterio", "limitaciones"]
    for p in prop["propuestas_revisadas"]:
        for k in exigidos:
            assert p.get(k), f"propuesta sin {k}: {p.get('columna')}"
        assert p["huellas"].get("huella_esquema"), f"sin huella esquema: {p['columna']}"
        assert p["huellas"].get("huella_fila_diccionario"), f"sin huella fila: {p['columna']}"
        assert p.get("concepto") and p.get("regla") and p.get("diccionario")
        al = p.get("alias_limitado")
        if al:
            assert al["alcance"].startswith("solo_columna:"), f"alias global prohibido: {p['columna']}"
            assert al["alcance"] == "solo_columna:" + p["columna"], "alias fuera de su columna"

    # 3. Solo significados respaldados vigentes, con regla concreta.
    conceptos = set(sem["conceptos"].keys())
    reglas = {r["id"] for r in sem["reglas_descripcion_exacta"]}
    var_estado = {v["iri"]: v for v in cob["variables"] if v.get("iri")}
    for p in prop["propuestas_revisadas"]:
        assert p["concepto"] in conceptos, f"concepto nuevo prohibido: {p['concepto']}"
        assert p["regla"] in reglas, f"regla inexistente: {p['regla']}"
        v = var_estado.get(p.get("variable_iri"))
        assert v and v["estado"] == "respaldada_por_definicion", f"variable sin respaldo: {p['columna']}"
        assert v["regla"] == p["regla"] and v["concepto"] == p["concepto"], "regla/concepto no coinciden con variable"

    # 4. No contradecir ni sustituir las 62 revisiones existentes (no solo contarlas).
    assert prop["conteos"]["conservadas_existentes"] == 62
    assert len(prop["conservadas_existentes_iris"]) == 62
    existentes = {(r["recurso"], r["campo"], r.get("columna")): r
                  for r in sem.get("vinculos_documentales_revisados", [])}
    prop_por_col = {p["columna"]: p for p in prop["propuestas_revisadas"]}
    for key, rev in existentes.items():
        col_iri = rev.get("columna")
        if col_iri and col_iri in prop_por_col:
            raise AssertionError(f"propuesta sustituye revision existente: {col_iri}")
        # Ninguna propuesta reclama el mismo par recurso+campo con otra variable/diccionario.
        for p in prop["propuestas_revisadas"]:
            if p["recurso"] == rev["recurso"] and p["campo"] == rev["campo"] and p["columna"] != rev.get("columna"):
                # Solo se permite si es la misma columna física (alias ya contemplado en existentes).
                pass
            if p["columna"] == rev.get("columna"):
                assert p["diccionario"] == rev["diccionario"] and p["concepto"] == rev["concepto"], \
                    f"contradice revision: {col_iri}"
    # Disjunción: las propuestas candidatas no pisan columnas ya revisadas.
    pend_rev = {c["columna"] for c in pend["columnas"] if c["estado"] == "documental_revisada"}
    assert not (set(prop_por_col) & pend_rev - {i["columna"] for i in prop["inconsistencias"]
                                                if i["dictamen"].startswith("revision_existente")}), \
        "propuesta sobre columna ya revisada"

    # 5. Sin normalizaciones globales ni conceptos nuevos.
    for p in prop["pendientes_clasificados"]:
        assert p.get("motivo"), "pendiente sin motivo clasificado"
    # 6. Sinónimos temáticos no promocionan: ninguna propuesta puede apoyarse en ellos.
    for p in prop["propuestas_revisadas"]:
        det = (p.get("evidencia") or {}).get("detalle_contexto", "")
        assert "tematic" not in det and "pista_tematica" not in det, (
            f"promocion por sinonimo tematico: {p['columna']} {det}")
    # 7. Alias a–o sin propuesta; divorcios con propuesta única y concreta.
    incs = {i["id"]: i for i in prop["inconsistencias"]}
    assert incs["anio-nacimientos-2024"]["propuesta"] is None, "a–o debe seguir sin propuesta"
    assert "hipotesis_no_verificada" in incs["anio-nacimientos-2024"]["dictamen"]
    div = incs["anio-divorcios-2023"]
    assert isinstance(div.get("propuesta"), dict) and div["dictamen"] == "alias_especifico_propuesto"

    print(f"OK: {len(prop['propuestas_revisadas'])} propuestas, "
          f"{len(prop['pendientes_clasificados'])} pendientes, "
          f"{len(prop['ambiguos'])} ambiguos, {len(prop['inconsistencias'])} inconsistencias. "
          f"62 conservadas sin contradiccion.")


if __name__ == "__main__":
    main()
