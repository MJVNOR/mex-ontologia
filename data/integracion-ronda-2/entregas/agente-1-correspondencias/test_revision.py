"""Tests de la revision (agente 1, ronda 2). Sin frameworks: asserts puros."""
import json
import sys
import tomllib
import unicodedata
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

import revisar as R  # noqa: E402
from consolidar_semantica import columnas  # noqa: E402


def norm(s):
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or "").lower())
                if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


def main():
    prop = json.loads((HERE / "propuestas.json").read_text(encoding="utf-8"))
    sem = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    pend = json.loads((ROOT / "reports/pendientes-semanticos.json").read_text(encoding="utf-8"))
    inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
    ins = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
    base = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]

    # 1. Cobertura: 792 = 674 finales + 118 pendientes; preseleccion 675 = 674 + 1 descarte.
    c = prop["conteos"]
    assert c["candidatas_examinadas"] == 792
    assert c["preseleccion_lexica"] == 675
    assert c["propuestas_finales"] == 674
    assert c["descartes_vinculo"] == 1
    assert c["pendientes_clasificados"] == 118
    cand_cols = [x["columna"] for x in pend["columnas"] if x["estado"] == "candidata_por_nombre"]
    assert len(cand_cols) == 792 and len(set(cand_cols)) == 792
    p_cols = [p["columna"] for p in prop["propuestas_revisadas"]]
    q_cols = [p["columna"] for p in prop["pendientes_clasificados"]]
    assert len(p_cols) + len(q_cols) == 792
    assert len(set(p_cols)) == len(p_cols) and len(set(q_cols)) == len(q_cols)
    assert not (set(p_cols) & set(q_cols))
    assert set(p_cols) | set(q_cols) == set(cand_cols)

    # 2. Recalculo real contra el estado central (no solo existencia de campos).
    var_by_iri = {v["iri"]: v for v in cob["variables"] if v.get("iri")}
    cols_calc = {x["iri"]: x for x in columnas(inv, ins, base)}
    rec_by_id = {r["id"]: r for r in inv["recursos"]}
    from collections import Counter
    var_veces = Counter((v["diccionario"], v["variable"]) for v in cob["variables"] if v.get("iri"))
    ndict_conj = Counter(r["conjunto_id"] for r in inv["recursos"] if r["clasificacion"] == "diccionario")
    conceptos = set(sem["conceptos"].keys())
    reglas = {r["id"] for r in sem["reglas_descripcion_exacta"]}
    grupos = {g["id"]: g for g in prop["grupos_vinculo"]}
    assert len(grupos) == c["grupos_vinculo"] == 333
    for p in prop["propuestas_revisadas"]:
        v = var_by_iri.get(p["variable_iri"])
        assert v and v["estado"] == "respaldada_por_definicion"
        assert v["regla"] == p["regla"] and v["concepto"] == p["concepto"]
        assert p["concepto"] in conceptos and p["regla"] in reglas
        assert p["definicion"] == v["descripcion"], f"definicion no literal: {p['columna']}"
        assert p["conjunto"] == v["conjunto"] and p["recurso"] == p["recurso"]
        calc = cols_calc.get(p["columna"])
        assert calc, f"columna fuera del inventario actual: {p['columna']}"
        assert calc["huella_esquema"] == p["huellas"]["huella_esquema"], \
            f"huella esquema recalculada difiere: {p['columna']}"
        assert v["huella_fila_diccionario"] == p["huellas"]["huella_fila_diccionario"]
        assert v["diccionario"] == p["diccionario"]
        assert p["alias_limitado"] is None
        # Unicidad y alcance recalculados.
        assert var_veces[(v["diccionario"], v["variable"])] == 1, f"var duplicada: {p['columna']}"
        assert calc["nombre_unico"] is True, f"columna duplicada: {p['columna']}"
        assert ndict_conj.get(p["conjunto"]) == 1, f"alcance no unico: {p['columna']}"
        dic_inv = rec_by_id.get(p["diccionario"], {})
        assert dic_inv.get("conjunto_id") == p["conjunto"], f"diccionario fuera del conjunto: {p['columna']}"
        # Relacion de nombres recalculada: nunca 'diferente'.
        tipo, _ = R.relacion_nombre(p["campo"], p["variable"])
        assert tipo in ("exacta", "caja", "acentos"), f"nombre diferente: {p['columna']}"
        assert tipo == p["evidencia_vinculo"]["relacion_nombre"]
        # Cada calificador citado ocurre en la descripcion normalizada.
        dnorm = norm(p["definicion"])
        for cal in p["concepto"].split("-"):
            frags = [e["fragmento"] for e in
                     p["evidencia_significado"]["verificacion_por_calificador"]
                     if e["calificador"] == cal]
            assert frags and any(f in dnorm for f in frags), f"calificador sin cita: {cal}"
        # Grupo existente con ficha completa y miembro listado.
        g = grupos.get(p["grupo_vinculo"])
        assert g and g["diccionario"]["url"] and g["recurso"]["id"] == p["recurso"]
        assert p["columna"] in {m["columna"] for m in g["miembros"]}

    # 3. Normalizaciones ortograficas: 21, todas 'acentos', acotadas al recurso.
    norms = prop["normalizaciones_ortograficas"]
    assert len(norms) == 21 == c["normalizaciones_ortograficas"]
    norm_cols = {n["columna"] for n in norms}
    acent_prop = {p["columna"] for p in prop["propuestas_revisadas"]
                  if p["evidencia_vinculo"]["relacion_nombre"] == "acentos"}
    assert norm_cols == acent_prop, "normalizaciones no cubren todos los casos de acentos"
    for n in norms:
        assert n["recurso"] and n["evidencia"] and n["tipo"] == "acentos"

    # 4. El descarte por enie queda pendiente con motivo de vinculo.
    desc = [p for p in prop["pendientes_clasificados"] if p.get("etapa") == "vinculo"]
    assert len(desc) == 1
    assert "nombre_difiere" in desc[0]["motivo"]
    tipo, _ = R.relacion_nombre(desc[0]["campo"], desc[0]["variable"])
    assert tipo == "diferente", "la enie debe clasificarse como diferente"

    # 5. Casos negativos sinteticos: pasan el filtro lexico pero el vinculo falla.
    t, _ = R.relacion_nombre("Año", "ano")
    assert t == "diferente", "enie->ene no es mero acento"
    t, _ = R.relacion_nombre("Institución", "Institucion")
    assert t == "acentos"
    t, _ = R.relacion_nombre("MUNICIPIO", "municipio")
    assert t == "caja"
    d, m, _ = R.dictamen_vinculo("municipio", "municipio", "municipio-registro", "municipio de registro",
                                 "CJ-A", "CJ-B", True, True, True, True, 1)
    assert d == "pendiente" and any("fuera_de_alcance" in x for x in m), "diccionario fuera del conjunto"
    d, m, _ = R.dictamen_vinculo("municipio", "municipio", "municipio-registro", "municipio de registro",
                                 "CJ", "CJ", True, True, True, True, 2)
    assert d == "pendiente" and any("alcance_no_asignado" in x for x in m), "alcance incompatible"
    d, m, _ = R.dictamen_vinculo("Año", "ano", "anio", "ano", "CJ", "CJ", True, True, True, True, 1)
    assert d == "pendiente" and any("nombre_difiere" in x for x in m), "nombres enie/ene"
    d, m, _ = R.dictamen_vinculo("campo", "var", "localidad-residencia-madre",
                                 "clave de la localidad donde reside el difunto",
                                 "CJ", "CJ", True, True, True, True, 1)
    assert d == "pendiente" and any("contradiccion_poblacion" in x for x in m), "contradiccion madre/difunto"
    d, m, _ = R.dictamen_vinculo("campo", "var", "municipio-residencia",
                                 "clave del municipio donde reside la madre",
                                 "CJ", "CJ", True, True, False, True, 1)
    assert d == "pendiente" and any("variable_ambigua" in x for x in m), "variable duplicada"

    # 6. Conservadas, ambiguos y observaciones intactos como contexto.
    assert c["conservadas_existentes"] == 162 and len(prop["conservadas_existentes_iris"]) == 162
    rev_cols = {x["columna"] for x in pend["columnas"] if x["estado"] == "documental_revisada"}
    assert set(prop["conservadas_existentes_iris"]) == rev_cols
    assert not (set(p_cols) & rev_cols)
    assert c["columnas_ambiguas"] == 3 and c["vinculos_ambiguos"] == 6 and len(prop["ambiguos"]) == 3
    assert c["observaciones_contexto"] == 5 and len(prop["observaciones_contexto"]) == 5
    for p in prop["pendientes_clasificados"]:
        assert p.get("motivo") and p.get("etapa") in ("preseleccion", "vinculo")

    print(f"OK: {len(prop['propuestas_revisadas'])} finales "
          f"(preseleccion {c['preseleccion_lexica']}, descarte {c['descartes_vinculo']}), "
          f"{len(prop['pendientes_clasificados'])} pendientes, "
          f"162 conservadas, 3 ambiguas, 5 observaciones.")


if __name__ == "__main__":
    main()
