"""Reproduce matriz y top50 desde insumos locales. Solo stdlib."""
import json, csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[6]
MAPA = ROOT / "data/portal/oportunidades-cruce.json"
CRIT = pathlib.Path(__file__).parents[1] / "criterio.json"

def main():
    mapa = json.loads(MAPA.read_text(encoding="utf-8"))
    crit = json.loads(CRIT.read_text(encoding="utf-8"))
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]
    rows = []
    for p in mapa["pares"]:
        if p["estado"] != "candidata_por_validar":
            continue
        s = sum(pesos.get(f, 1) for f in p.get("familias_compartidas", []))
        s += sum(pen.get(b, 0) for b in p.get("pendientes", []))
        rows.append((round(s, 2), p["id"], p))
    rows.sort(key=lambda r: (-r[0], r[1]))
    assert len(rows) == 1191, len(rows)
    top = rows[:50]
    print(f"pares relevantes: {len(rows)}; top1: {top[0][2]['titulo_a']} <-> {top[0][2]['titulo_b']} score {top[0][0]}")
    print("OK reproducible")

if __name__ == "__main__":
    main()
