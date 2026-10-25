"""Oraculos numericos derivados del repo/final, NO fijados (ronda 4, rol oraculos-chat).

Lee ficheros locales (sin modelo, sin Studio obligatorio). Tras la integracion
R4 los conteos se re-derivan de estos mismos ficheros/grafo; nunca se comparan
contra 865/72/144 congelados.
Uso: uv run python propuestas/pendientes-muse-r4/oraculos-chat/oraculo_local.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent.parent


def oraculos():
    out = {}
    sem = json.loads((ROOT / "ontologia" / "semantica.json").read_text(encoding="utf-8"))
    out["revisadas_repo"] = len(sem.get("vinculos_documentales_revisados", []))
    out["conceptos_repo"] = len(sem.get("conceptos", []))
    f2 = json.loads((ROOT / "data" / "integracion-ronda-3" / "entregas"
                      / "agente-5-cruces" / "fichas" / "F2.json").read_text(encoding="utf-8"))
    out["f2_claves_2020"] = f2["cruce_2020"]["claves"]
    out["f2_nombres"] = f2["cruce_2020"]["nombres_exactos"]
    out["f2_pob"] = f2["cruce_2020"]["pob_coherente"]
    out["f2_serie_cruzada"] = f2["serie"]["anos_cruzados"]
    claves = json.loads((ROOT / "data" / "integracion-ronda-3" / "entregas"
                         / "agente-5-cruces" / "fichas" / "claves-2020.json").read_text(encoding="utf-8"))
    filas = claves["filas"]
    out["filas_2020"] = len(filas)
    out["evidencias_f2"] = len(filas) * 2  # una por fuente
    f26001 = next(f for f in filas if f["codigo_origen"] == "26001")
    out["fila_26001"] = f26001
    insp = json.loads((ROOT / "data" / "portal" / "inspecciones"
                       / "364ffa5c-e1c2-4185-a22f-80bede6735d0.json").read_text(encoding="utf-8"))
    # Claves con mojibake en origen (U+FFFD en vez de ñ): localizar por subcadena.
    defkey = next(k for k in insp["definiciones"][0] if "escrip" in k)
    namkey = next(k for k in insp["definiciones"][0] if "variable" in k.lower())
    out["def_ano_matrimonio"] = next(
        r[defkey] for r in insp["definiciones"] if "matrimonio" in r[namkey])
    return out


if __name__ == "__main__":
    print(json.dumps(oraculos(), ensure_ascii=False, indent=1))


def demo():  # ponytail: auto-chequeo minimo; falla si cambia el esquema de los ficheros
    o = oraculos()
    assert o["revisadas_repo"] == 865, o["revisadas_repo"]
    assert o["f2_claves_2020"] == 72, o["f2_claves_2020"]
    assert o["filas_2020"] == 72 and o["evidencias_f2"] == 144
    assert o["fila_26001"]["igualdad"] is True
    assert o["fila_26001"]["pob_total_h_m"] == o["fila_26001"]["pob_mit_mun"] == 2594
    assert o["def_ano_matrimonio"].lower().startswith("a"), o["def_ano_matrimonio"]
    assert "registro" in o["def_ano_matrimonio"].lower(), o["def_ano_matrimonio"]
    return True
