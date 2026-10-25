"""Publica el Top 50 de oportunidades de cruce (reconciliacion R9). Solo stdlib.

Script publicable: instalado como ``scripts/publicar_top50_r9.py``, la
invocacion sin ``--out-dir`` escribe en ``reports/`` del repositorio. Una
carpeta de version no usa el valor por defecto: invoca SIEMPRE ``--out-dir``.

    uv run python scripts/publicar_top50_r9.py
    uv run python .../T-top50/v002/scripts/publicar_top50_r9.py --out-dir .../T-top50/v002

API: ``generar(root, outdir)``. CLI: ``main()``.
Lee solo fuentes (mapa, criterio C2, CSV top50/matriz, cobertura R9,
seguimiento R9 y plan). Nunca escribe en las fuentes ni en carpetas selladas
(detectadas por ``congelada.json``). Escribe tres archivos en ``outdir``:
``top50-oportunidades-r9.json``, ``.md`` y ``.html``.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
from pathlib import Path

PARES = 3916
CANDIDATAS = 1191
FILAS = 50
NO_JOIN = "NO_JOIN_APROBADO"
NOMBRE = "top50-oportunidades-r9"

# Pares A1-A3 del plan por ID exacto (identificacion, sin join ni calculo).
A_PARES = {
    "A1-911": "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92",
    "A2-matrimonios-nacimientos": "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5",
    "A3-itama": "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848",
}

FUENTES = {
    "mapa": "data/portal/oportunidades-cruce.json",
    "criterio": "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json",
    "top50_csv": "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv",
    "matriz_csv": "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv",
    "cobertura_r9": "reports/cobertura-operativa-r9.json",
    "seguimiento_r9": "reports/seguimiento-operativo-post-r9.json",
    "plan": "docs/plan-paralelo-ampliacion-post-r9.md",
}


def raiz(desde: str | Path | None = None) -> Path:
    """Sube desde ``desde`` (o este archivo) hasta el repositorio."""
    p = Path(desde or __file__).resolve()
    for d in (p, *p.parents):
        if (d / "pyproject.toml").is_file() and (d / "data/portal/oportunidades-cruce.json").is_file():
            return d
    raise SystemExit("no se localizo la raiz del repositorio")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def destino_publicacion(root: str | Path, out_dir: str | Path | None = None,
                        script: str | Path | None = None) -> Path:
    """Destino efectivo. Sin ``out_dir`` solo vale si esta instalado en scripts/."""
    if out_dir:
        return Path(out_dir)
    script = Path(script or __file__).resolve()
    if script.parent == (Path(root) / "scripts").resolve():
        return Path(root) / "reports"
    raise SystemExit("carpeta de version: use --out-dir explicito")


def score(p: dict, pesos: dict, pen: dict) -> float:
    s = sum(pesos.get(f, 1) for f in p.get("familias_compartidas", []))
    s += sum(pen.get(b, 0) for b in p.get("pendientes", []))
    return round(s, 2)


def _comprobar_destino(root: Path, outdir: Path) -> None:
    outdir = outdir.resolve()
    propia = Path(__file__).resolve().parents[1]
    fuentes = [(root / r).resolve() for r in FUENTES.values()]
    es_publicacion = outdir == (root / 'reports').resolve()
    for extension in ('.json', '.md', '.html'):
        destino = (outdir / (NOMBRE + extension)).resolve()
        if destino in fuentes or destino.parent != outdir:
            raise SystemExit(f'destino de salida fuera de carpeta o sobre fuente: {destino}')
    for f in fuentes:
        if not es_publicacion and (outdir == f.parent or f.parent in outdir.parents):
            raise SystemExit(f"destino prohibido (fuente): {outdir}")
    for d in (outdir, *outdir.parents):
        if d == propia:  # la propia carpeta de version puede regenerar sus artefactos
            continue
        if (d / "congelada.json").is_file():
            raise SystemExit(f"destino prohibido (version sellada): {outdir}")


def _fuentes_actuales(root: Path) -> list[dict]:
    return [{"clave": k, "ruta": r, "sha256": sha256(root / r), "bytes": (root / r).stat().st_size}
            for k, r in FUENTES.items()]


def _verificar(root: Path) -> tuple[dict, dict, list[dict], list[dict]]:
    mapa = json.loads((root / FUENTES["mapa"]).read_text(encoding="utf-8"))
    crit = json.loads((root / FUENTES["criterio"]).read_text(encoding="utf-8"))
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]
    pares = mapa["pares"]
    assert len(pares) == PARES, len(pares)
    cand = [p for p in pares if p["estado"] == "candidata_por_validar"]
    assert len(cand) == CANDIDATAS, len(cand)
    calc = sorted(((score(p, pesos, pen), p["id"], p) for p in cand),
                  key=lambda r: (-r[0], r[1]))
    assert len({r[1] for r in calc}) == CANDIDATAS

    with open(root / FUENTES["top50_csv"], encoding="utf-8") as f:
        top = list(csv.DictReader(f))
    with open(root / FUENTES["matriz_csv"], encoding="utf-8") as f:
        mat = list(csv.DictReader(f))
    assert len(top) == FILAS and len(mat) == CANDIDATAS, (len(top), len(mat))
    assert len({r["id"] for r in top}) == FILAS
    assert len({r["id"] for r in mat}) == CANDIDATAS
    byid = {i: s for s, i, _ in calc}
    for r in mat:  # 1191 scores recomputados == matriz
        assert float(r["score"]) == byid[r["id"]], r["id"]
    for n, r in enumerate(top):  # 50 rangos/ids/scores == recomputo
        s, i, _ = calc[n]
        assert r["id"] == i and float(r["score"]) == s and int(r["rango"]) == n + 1, r["id"]
    ids = {r["id"] for r in top}
    for tag, pid in A_PARES.items():
        assert pid in ids, tag
    return mapa, crit, top, mat


def _filas(mapa: dict, top: list[dict]) -> list[dict]:
    inv = {p["id"]: p for p in mapa["pares"]}
    a_tag = {v: k for k, v in A_PARES.items()}
    return [{
        "rango": int(r["rango"]),
        "id": r["id"],
        "titulo_a": inv[r["id"]]["titulo_a"],
        "titulo_b": inv[r["id"]]["titulo_b"],
        "score": float(r["score"]),
        "familias": inv[r["id"]]["familias_compartidas"],
        "bloqueadores": inv[r["id"]]["pendientes"],
        "fuentes": {"conjunto_a": inv[r["id"]]["conjunto_a"],
                    "conjunto_b": inv[r["id"]]["conjunto_b"]},
        "estado": NO_JOIN,
        "carril_analitico": a_tag.get(r["id"]),
    } for r in top]


def _markdown(meta: dict, filas: list[dict]) -> str:
    md = ["# Top 50 oportunidades de cruce — reconciliacion R9", "",
          f"Mapa `{FUENTES['mapa']}`: {meta['pares']} pares, {meta['candidatas']} candidatas. "
          f"Criterio C2 (sha256 `{meta['fuentes'][1]['sha256'][:12]}…`). "
          f"Cobertura R9: {meta['cobertura_r9']['estado']} "
          f"({meta['cobertura_r9']['significados_respaldados']} significados, "
          f"{meta['cobertura_r9']['conceptos']} conceptos).",
          "Estado de todas las filas: **NO_JOIN_APROBADO**. "
          "Ningun join ni rate se deriva del ranking.",
          "", "| rango | id | A | B | score | carril | bloqueadores |",
          "| --- | --- | --- | --- | --- | --- | --- |"]
    for f in filas:
        md.append(f"| {f['rango']} | `{f['id']}` | {f['titulo_a']} | {f['titulo_b']} | "
                  f"{f['score']} | {f['carril_analitico'] or '—'} | "
                  f"{'; '.join(f['bloqueadores']) or '—'} |")
    md += ["", "Fuentes por fila (conjuntos A/B) y huellas SHA256 completas de los "
               f"insumos: `{NOMBRE}.json` (`meta.fuentes`, `filas[].fuentes`).", ""]
    return "\n".join(md)


def _html(meta: dict, filas: list[dict]) -> str:
    trs = "\n".join(
        f"<tr><td class=\"n\">{f['rango']}</td><td><code>{html.escape(f['id'])}</code></td>"
        f"<td>{html.escape(f['titulo_a'])}</td><td>{html.escape(f['titulo_b'])}</td>"
        f"<td class=\"n\">{f['score']}</td><td>{html.escape(f['carril_analitico'] or '—')}</td>"
        f"<td>{html.escape('; '.join(f['bloqueadores']) or '—')}</td>"
        f"<td><strong>{NO_JOIN}</strong></td></tr>" for f in filas)
    return (
        "<!doctype html>\n<html lang=\"es\">\n<head><meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Top 50 oportunidades de cruce — R9</title>\n"
        "<style>\n"
        "body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:2rem;color:#1b1f24;background:#fbfbfa}\n"
        "h1{font-size:1.4rem;margin:0 0 .5rem} p{max-width:75ch;line-height:1.45}\n"
        "table{border-collapse:collapse;width:100%;font-size:.85rem;background:#fff}\n"
        "th,td{border:1px solid #d8d8d4;padding:.35rem .5rem;text-align:left;vertical-align:top}\n"
        "th{background:#efece4;position:sticky;top:0} tbody tr:nth-child(even){background:#f7f6f2}\n"
        "td.n{text-align:right;font-variant-numeric:tabular-nums} code{font-size:.78rem}\n"
        "caption{caption-side:bottom;text-align:left;padding-top:.6rem;font-size:.8rem;color:#555}\n"
        "</style></head>\n<body>\n"
        "<h1>Top 50 oportunidades de cruce — reconciliacion R9</h1>\n"
        f"<p>{meta['pares']} pares del mapa, {meta['candidatas']} candidatas. "
        f"Cobertura R9: {html.escape(meta['cobertura_r9']['estado'])} "
        f"({meta['cobertura_r9']['significados_respaldados']} significados, "
        f"{meta['cobertura_r9']['conceptos']} conceptos). "
        f"Todas las filas: <strong>{NO_JOIN}</strong>. Ningun join ni rate se deriva del ranking.</p>\n"
        "<table>\n<caption>Orden: score descendente, id ascendente. Huellas completas "
        f"de los insumos en {NOMBRE}.json.</caption>\n<thead><tr><th>rango</th><th>id</th>"
        "<th>A</th><th>B</th><th>score</th><th>carril</th><th>bloqueadores</th>"
        "<th>estado</th></tr></thead>\n<tbody>\n"
        f"{trs}\n</tbody>\n</table>\n</body>\n</html>\n")


def generar(root: str | Path, outdir: str | Path) -> dict:
    """Genera los tres artefactos publicables en ``outdir`` (nunca en fuentes)."""
    root = Path(root).resolve()
    outdir = Path(outdir)
    _comprobar_destino(root, outdir)

    mapa, _crit, top, _mat = _verificar(root)
    filas = _filas(mapa, top)
    cob = json.loads((root / FUENTES["cobertura_r9"]).read_text(encoding="utf-8"))
    meta = {
        "titulo": "Top 50 oportunidades de cruce — reconciliacion R9",
        "rol": "T-top50",
        "fecha_corte": "2026-10-24",
        "pares": PARES,
        "candidatas": CANDIDATAS,
        "filas": FILAS,
        "estado_filas": NO_JOIN,
        "formula": "score = suma(pesos_familia) + suma(penalizaciones); "
                   "orden score desc, id asc",
        "cobertura_r9": {
            "estado": cob["estado"],
            "significados_respaldados": cob["indicadores"]["significados_respaldados"],
            "conceptos": cob["indicadores"]["conceptos"],
        },
        "pares_a1_a3": A_PARES,
        "nota": "Oportunidad != join aprobado. Ningun join ni rate se deriva de este ranking.",
        "publicacion": {"destino": f"reports/{NOMBRE}.json|.md|.html",
                        "escritor": "unico integrador central"},
        "fuentes": _fuentes_actuales(root),
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{NOMBRE}.json").write_text(
        json.dumps({"meta": meta, "filas": filas}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8", newline="\n")
    (outdir / f"{NOMBRE}.md").write_text(_markdown(meta, filas), encoding="utf-8", newline="\n")
    (outdir / f"{NOMBRE}.html").write_text(_html(meta, filas), encoding="utf-8", newline="\n")
    return {"outdir": str(outdir), "filas": len(filas), "estado_filas": NO_JOIN,
            "archivos": [f"{NOMBRE}.json", f"{NOMBRE}.md", f"{NOMBRE}.html"]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Publica el Top 50 de oportunidades (R9).")
    ap.add_argument("--root", default=None, help="raiz del repositorio (autodetectada)")
    ap.add_argument("--out-dir", default=None,
                    help="destino; por defecto reports/ solo si el script esta en scripts/")
    args = ap.parse_args(argv)
    root = raiz(args.root)
    outdir = destino_publicacion(root, args.out_dir)
    res = generar(root, outdir)
    print(f"OK {res['filas']} filas, estado {res['estado_filas']} -> {res['outdir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
