"""Pruebas de A3 ITAMA v002 (stdlib, sin red).

Se ejecutan con `uv run python pruebas/test_a3_itama_v002.py` (main) o con pytest.
Verifican las afirmaciones corregidas: el repo SÍ tiene XLSX, pero 0 copias exactas
ITAMA; periodo documental 2026 vs filas no verificadas; escolaridad insuficiente;
agregado bloqueado; v001 intacta.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

V001_SHA = {
    "entrega.json": "754bae47487e6424a3dda2484229073a46311c42f92627f34acd26763f2fe9f1",
    "entrega.md": "f10261d2201223e7087bebe8bd6262e9a62b6ff826f7a58430a40e9a8a15116c",
    "scripts/analisis_a3_itama.py": "7438d8c17080387d90d7dd835469618bdfa383b51d62b19ef127b5bccfef0f4f",
}
IDS = (
    "56dbfc19-0e71-45dc-bf50-6b5a5a92bd7c",
    "59f89fe2-1999-47c5-b464-5f303377fc04",
    "525d84db-d4aa-480d-9c1a-a3d4e7524ac2",
    "cf589b78-2fee-4fb6-b7c8-434e050a058e",
    "71defd43-bee9-45fa-9463-ce2cac2b9ab8",
    "7f95e924-57cc-4f3a-8b5a-e254e7b97993",
)


def raiz() -> Path:
    for p in Path(__file__).resolve().parents:
        if (p / "pyproject.toml").is_file() and (p / "data" / "catalogo" / "metadatos.json").is_file():
            return p
    raise SystemExit("no se localizó la raíz del repositorio")


ROOT = raiz()
V2 = ROOT / "propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002"
V1 = V2.parent / "v001"


def carga(rel: str) -> dict:
    return json.loads((V2 / rel).read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_decision_bloqueada_y_agregado_separado() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    assert d["decision"] == "BLOQUEADO"
    assert d["analisis_agregado"]["estado"] == "BLOQUEADO"
    assert d["analisis_agregado"]["calculado"] is False
    assert d["analisis_agregado"]["distribuciones_publicadas"] == []
    assert d["escolaridad"]["estado"] == "fuentes_insuficientes"


def test_recursos_y_periodo_metadatos() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    rec = d["universo_documental"]["recursos"]
    assert len(rec["internamiento"]) == 3 and len(rec["externamiento"]) == 3
    for r in rec["internamiento"] + rec["externamiento"]:
        assert r["id"] in IDS
        assert len(r["sha256"]) == 64 and r["completo_reportado"] is True
    assert d["universo_documental"]["periodo_metadatos"] == {"inicio": "2026-01-01", "fin": "2026-09-30"}
    assert d["universo_documental"]["frecuencia_declarada"] == "trimestral"
    assert d["universo_documental"]["periodo_filas"]["estado"] == "no_verificable"


def test_periodo_de_filas_no_verificable() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    for r in d["universo_documental"]["recursos"]["internamiento"] + d["universo_documental"]["recursos"]["externamiento"]:
        poblacion = [h for h in r["hojas"] if h["hoja"].upper().startswith("POBLACION")]
        assert poblacion, r["id"]
        assert all(h["n_columnas_fecha"] == 0 for h in poblacion), r["id"]
        assert all(not h["tiene_escolaridad"] for h in poblacion), r["id"]
    assert d["ficha_8_ejes"]["periodo"]["estado"] == "documental_2026_filas_no_verificado"


def test_escolaridad_fuentes_insuficientes() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    e = d["escolaridad"]
    assert e["publicada_en_hoja_de_poblacion"] is False
    assert set(e["hojas_poblacion_sin_columna"]) == {"POBLACION INTERNAMIENTO", "POBLACION EXTERNAMIENTO"}
    assert e["en_diccionarios"] == {k: False for k in e["en_diccionarios"]}
    assert e["concepto_itama_en_nucleo"] is False
    assert e["presente_solo_en_hoja_heredada"]["7f95e924-57cc-4f3a-8b5a-e254e7b97993"] == []
    assert "FEBRERO 2016" in e["presente_solo_en_hoja_heredada"]["59f89fe2-1999-47c5-b464-5f303377fc04"]


def test_repo_si_tiene_xlsx_pero_cero_copias_itama() -> None:
    inv = carga("resultados/inventario-archivos-repo.json")
    xlsx = [a for a in inv["archivos"] if a["tipo"] == "xlsx"]
    assert inv["xlsx_total"] == len(xlsx) > 0, "v001 afirmaba 0 XLSX en el repo: es falso"
    assert inv["csv_total"] == sum(1 for a in inv["archivos"] if a["tipo"] == "csv")
    assert inv["coincidencias_exactas_itama"] == []
    assert inv["firma_contenido_hojas_itama"] == []
    for uuid in IDS:
        assert inv["busqueda_por_nombre"][uuid] == [], uuid
    assert inv["busqueda_por_nombre"]["itama"] == []
    assert any(a["ruta"].startswith("data/territorio/fuentes/") for a in xlsx)
    assert all(uuid not in a["ruta"] for a in inv["archivos"] for uuid in IDS)


def test_muestras_no_son_cardinalidad() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    unicos = d["analisis_agregado"]["unicos_conteos_disponibles"]
    assert (unicos["internamiento_t2_filas"], unicos["externamiento_t1_filas"]) == (29, 16)
    assert d["ficha_8_ejes"]["cardinalidad"]["estado"] == "no_acreditada"
    assert d["ficha_8_ejes"]["unicidad"]["estado"] == "no_acreditada"
    assert d["ficha_8_ejes"]["claves"]["estado"] == "sin_clave_documentada"
    assert d["ficha_8_ejes"]["poblacion"]["estado"] == "distinta_y_no_sumable"
    assert set(d["ficha_8_ejes"]) == {
        "claves", "grano", "unicidad", "cardinalidad", "poblacion", "periodo", "unidades", "cobertura_datos"
    }


def test_correcciones_documentadas() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    tipos = {c["id"]: c["tipo"] for c in d["correcciones_v001"]}
    assert tipos["C1"] == "falso"
    assert tipos["C3"] == "no_reproducible"
    assert all(c["verificacion"] for c in d["correcciones_v001"])


def test_v001_intacta() -> None:
    for rel, esperado in V001_SHA.items():
        assert sha(V1 / rel) == esperado, rel
    d = carga("resultados/analisis-a3-itama-v002.json")
    assert set(d["v001"]["ausencias"]) == {"pruebas/test_a3_itama.py", "congelada.json"}
    assert {a["ruta"] for a in d["v001"]["archivos"]} == set(V001_SHA)


def test_entrega_json_coincide_con_resultados() -> None:
    d = carga("resultados/analisis-a3-itama-v002.json")
    e = carga("entrega.json")
    assert e["decision"] == d["decision"]
    cifras = e["cifras_verificadas"]
    assert cifras["xlsx_en_repo"] == d["inventario_copias"]["xlsx_total"]
    assert cifras["csv_en_repo"] == d["inventario_copias"]["csv_total"]
    assert cifras["copias_exactas_itama"] == len(d["inventario_copias"]["coincidencias_exactas_itama"])
    assert cifras["recursos_xlsx"] == 6
    assert cifras["periodo_metadatos"] == d["universo_documental"]["periodo_metadatos"]
    assert cifras["muestras"] == {"a": 29, "b": 16}
    assert cifras["escolaridad_nulos_muestra_a"] == 29


def main() -> int:
    pruebas = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    fallos = 0
    for nombre, fn in pruebas:
        try:
            fn()
            print(f"ok   {nombre}")
        except AssertionError as exc:
            fallos += 1
            print(f"FALLA {nombre}: {exc}")
    print(f"\n{len(pruebas) - fallos}/{len(pruebas)} pruebas correctas")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
