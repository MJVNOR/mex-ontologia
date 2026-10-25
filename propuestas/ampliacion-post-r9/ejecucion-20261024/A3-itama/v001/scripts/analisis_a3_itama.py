"""A3 ITAMA: ficha reproducible solo con archivos locales/documentacion.

Lee metadatos, cruce, lote, cobertura y nucleo; rederiva la ficha de 8 ejes y
falla si alguna premisa del bloqueo deja de cumplirse (entonces toca v002).
Sin red, sin grafo, sin escritura fuera de stdout. Solo stdlib.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
A = "27a5c80c-514a-4170-a2e5-7ef40d818641"
B = "4d27a1c4-381d-4ce0-a663-0d3e23a93848"
PAR = f"{A}--{B}"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main():
    meta = load("data/catalogo/metadatos.json")
    cruce = load("data/portal/oportunidades-cruce.json")
    lote = load("data/portal/lote-cruces/validacion-lote.json")
    cob = load("data/semantica/cobertura.json")
    nuc = (ROOT / "data/semantica/nucleo.ttl").read_text(encoding="utf-8")

    conjuntos = {c["id"]: c for c in meta}
    ra = sorted((r["id"], r["start_date"], r["end_date"]) for r in conjuntos[A]["resources"] if r["format"] == "XLSX")
    rb = sorted((r["id"], r["start_date"], r["end_date"]) for r in conjuntos[B]["resources"] if r["format"] == "XLSX")
    assert len(ra) == 3 and len(rb) == 3, "se esperaban 3+3 recursos XLSX"
    periodo_comun = (max(s for _, s, _ in ra + rb), min(e for _, _, e in ra + rb))
    assert periodo_comun == ("2026-01-01", "2026-09-30"), periodo_comun

    pares = [p for p in cruce["pares"] if p["id"] == PAR]
    assert len(pares) == 1, "par unico en cruce"
    fams = {e["familia"]: e for e in pares[0]["evaluacion_claves"]}
    assert {"estrato_escolaridad", "estrato_sexo", "periodo"} <= set(fams)

    def find(o, tid):
        if isinstance(o, dict):
            if o.get("id") == tid:
                return o
            for v in o.values():
                r = find(v, tid)
                if r is not None:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = find(v, tid)
                if r is not None:
                    return r
        return None

    diag = find(lote, PAR)["diagnostico_muestras"]
    assert diag["a"]["filas_muestra"] == 29 and diag["b"]["filas_muestra"] == 16
    assert diag["a"]["campos"]["ESCOLARIDAD"]["nulos"] == 29
    assert diag["a"]["campos"]["SEXO"]["distintos_muestra"] == 1
    assert diag["b"]["campos"]["SEXO"]["distintos_muestra"] == 2
    assert "ESCOLARIDAD" not in diag["b"]["campos"]

    vars_cob = [v for v in cob["variables"] if v["conjunto"] in (A, B)]
    assert "escolaridad" not in {v["variable"] for v in vars_cob}, "escolaridad aun sin definir"
    assert sum("ITAMA" in v["titulo_conjunto"] for v in vars_cob) == 11
    assert "escolaridad-persona" not in nuc and "escolaridad-intern" not in nuc.lower()

    xlsx = [p for p in ROOT.rglob("*.xlsx")
            if "node_modules" not in p.parts and ".venv" not in p.parts]
    assert not xlsx, f"aparecieron copias locales: {xlsx}"

    ficha = {
        "recursos_xlsx": {"internamiento": len(ra), "externamiento": len(rb)},
        "periodo_comun_metadatos": {"inicio": periodo_comun[0], "fin": periodo_comun[1]},
        "muestras": {"a_filas": 29, "b_filas": 16,
                     "a_sexo_distintos": 1, "b_sexo_distintos": 2,
                     "a_escolaridad_nulos": 29, "b_escolaridad_medida": False},
        "escolaridad_definida_en_diccionarios": False,
        "copias_locales_completas": 0,
        "decision": "BLOQUEADO",
    }
    print(json.dumps(ficha, indent=2))
    return ficha


if __name__ == "__main__":
    main()
