"""Reconciliacion Top50 C2 v001 contra mapa portal + cobertura R9. Solo stdlib.

Lee (sin modificar):
  data/portal/oportunidades-cruce.json (3916 pares)
  propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json
  propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv
  propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv
  reports/cobertura-operativa-r9.json

Escribe (solo dentro de este v001):
  top50-oportunidades-r9.json / .md (contenido previsto para reports/, staging)
  vista-top50-r9.html (vista legible en staging)
  congelada.json (SHA256 por codigo; no se incluye a si misma)

Ningun join, ningun rate, ningun cambio al mapa original.
Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v001/scripts/reproducir_top50_r9.py
"""
import csv
import hashlib
import html
import json
import pathlib

V001 = pathlib.Path(__file__).resolve().parents[1]
ROOT = pathlib.Path(__file__).resolve().parents[6]
MAPA = ROOT / "data/portal/oportunidades-cruce.json"
C2 = ROOT / "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001"
CRIT = C2 / "criterio.json"
TOP50_CSV = C2 / "prioridades_top50.csv"
MATRIZ_CSV = C2 / "matriz_pares_relevantes.csv"
COB_R9 = ROOT / "reports/cobertura-operativa-r9.json"

# Pares A1-A3 del plan por ID exacto (solo identificacion, sin join ni calculo).
A_PARES = {
    "A1-911": "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92",
    "A2-matrimonios-nacimientos": "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5",
    "A3-itama": "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848",
}
NO_JOIN = "NO_JOIN_APROBADO"


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def score(p: dict, pesos: dict, pen: dict) -> float:
    s = sum(pesos.get(f, 1) for f in p.get("familias_compartidas", []))
    s += sum(pen.get(b, 0) for b in p.get("pendientes", []))
    return round(s, 2)


def main() -> None:
    mapa = json.loads(MAPA.read_text(encoding="utf-8"))
    crit = json.loads(CRIT.read_text(encoding="utf-8"))
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]
    pares = mapa["pares"]
    assert len(pares) == 3916, len(pares)
    cand = [p for p in pares if p["estado"] == "candidata_por_validar"]
    assert len(cand) == 1191, len(cand)
    calc = sorted(((score(p, pesos, pen), p["id"], p) for p in cand),
                  key=lambda r: (-r[0], r[1]))
    assert len({r[1] for r in calc}) == 1191

    with open(TOP50_CSV, encoding="utf-8") as f:
        top_csv = list(csv.DictReader(f))
    with open(MATRIZ_CSV, encoding="utf-8") as f:
        mat_csv = list(csv.DictReader(f))
    assert len(top_csv) == 50 and len(mat_csv) == 1191, (len(top_csv), len(mat_csv))
    assert len({r["id"] for r in top_csv}) == 50
    assert len({r["id"] for r in mat_csv}) == 1191
    byid = {p["id"]: (s, p) for s, _, p in [(s, i, p) for s, i, p in calc]}
    for r in mat_csv:  # score recomputado == matriz 1191
        assert float(r["score"]) == byid[r["id"]][0], r["id"]
    for n, r in enumerate(top_csv):  # orden y score == top50
        s, _, _ = calc[n]
        assert r["id"] == calc[n][1] and float(r["score"]) == s, r["id"]
        assert int(r["rango"]) == n + 1
    for tag, pid in A_PARES.items():  # A1-A3 presentes en top50
        assert pid in {r["id"] for r in top_csv}, tag

    cob = json.loads(COB_R9.read_text(encoding="utf-8"))
    inv = {p["id"]: p for p in pares}
    a_tag = {v: k for k, v in A_PARES.items()}
    filas = []
    for r in top_csv:
        p = inv[r["id"]]
        filas.append({
            "rango": int(r["rango"]),
            "id": r["id"],
            "titulo_a": p["titulo_a"],
            "titulo_b": p["titulo_b"],
            "score": float(r["score"]),
            "familias": p["familias_compartidas"],
            "bloqueadores": p["pendientes"],
            "fuentes": {"conjunto_a": p["conjunto_a"], "conjunto_b": p["conjunto_b"]},
            "estado": NO_JOIN,
            "carril_analitico": a_tag.get(r["id"]),
        })
    meta = {
        "rol": "T-top50",
        "mapa": {"ruta": "data/portal/oportunidades-cruce.json", "sha256": sha256(MAPA),
                 "pares": 3916, "candidatas": 1191},
        "criterio_c2": {"ruta": str(CRIT.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(CRIT)},
        "cobertura_r9": {"ruta": "reports/cobertura-operativa-r9.json", "sha256": sha256(COB_R9),
                         "estado": cob["estado"],
                         "significados_respaldados": cob["indicadores"]["significados_respaldados"]},
        "pares_a1_a3": A_PARES,
        "estado_filas": NO_JOIN,
        "nota": "Oportunidad != join aprobado. Ningun join ni rate se deriva de este ranking.",
    }
    (V001 / "top50-oportunidades-r9.json").write_text(
        json.dumps({"meta": meta, "filas": filas}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# Top 50 oportunidades cruce — reconciliacion R9 (staging)",
          "", f"Mapa `{meta['mapa']['ruta']}` SHA `{meta['mapa']['sha256'][:12]}…`: "
              f"{meta['mapa']['pares']} pares, {meta['mapa']['candidatas']} candidatas. "
              f"Criterio C2 v001 SHA `{meta['criterio_c2']['sha256'][:12]}…`. "
              f"Cobertura R9: {meta['cobertura_r9']['estado']}.",
          "Estado de todas las filas: **NO_JOIN_APROBADO**. Ningun join ni rate se deriva del ranking.",
          "", "| rango | id | A | B | score | bloqueadores |",
          "| --- | --- | --- | --- | --- | --- |"]
    for f in filas:
        md.append(f"| {f['rango']} | `{f['id']}` | {f['titulo_a']} | {f['titulo_b']} | "
                  f"{f['score']} | {'; '.join(f['bloqueadores'])} |")
    md += ["", "Fuentes por fila: conjuntos A/B en `top50-oportunidades-r9.json` → `filas[].fuentes`."]
    (V001 / "top50-oportunidades-r9.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    trs = "\n".join(
        f"<tr><td>{f['rango']}</td><td><code>{html.escape(f['id'])}</code></td>"
        f"<td>{html.escape(f['titulo_a'])}</td><td>{html.escape(f['titulo_b'])}</td>"
        f"<td>{f['score']}</td><td>{html.escape('; '.join(f['bloqueadores']))}</td>"
        f"<td>{NO_JOIN}</td></tr>" for f in filas)
    (V001 / "vista-top50-r9.html").write_text(
        "<!doctype html>\n<html lang=\"es\">\n<head><meta charset=\"utf-8\">\n"
        "<title>Top 50 oportunidades cruce — R9 (staging)</title></head>\n<body>\n"
        "<h1>Top 50 oportunidades de cruce — reconciliacion R9</h1>\n"
        f"<p>Mapa {meta['mapa']['pares']} pares / {meta['mapa']['candidatas']} candidatas. "
        f"Criterio C2 v001. Cobertura R9: {html.escape(meta['cobertura_r9']['estado'])}. "
        "Todas las filas: <strong>NO_JOIN_APROBADO</strong>.</p>\n"
        "<table>\n<thead><tr><th>rango</th><th>id</th><th>A</th><th>B</th>"
        "<th>score</th><th>bloqueadores</th><th>estado</th></tr></thead>\n<tbody>\n"
        f"{trs}\n</tbody>\n</table>\n</body>\n</html>\n", encoding="utf-8")

    archivos = []
    for p in sorted(V001.rglob("*")):
        if p.is_file() and p.name != "congelada.json":
            b = p.read_bytes()
            archivos.append({"ruta": str(p.relative_to(ROOT)).replace("\\", "/"),
                             "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    (V001 / "congelada.json").write_text(
        json.dumps({"rol": "T-top50", "nota": "Congelada v001 por codigo. No editar; corregir en v002.",
                    "archivos": archivos}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK 3916/1191/50 verificados; A1-A3 en top50; R9 {cob['estado']}; "
          f"{len(archivos)} archivos congelados")


if __name__ == "__main__":
    main()
