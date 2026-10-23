"""Reconsulta SPARQL de solo lectura (sin modelos).

Por defecto: consulta el grafo vivo y compara en memoria con las evidencias
guardadas en fuentes/sparql/*.json, sin modificar ningún archivo.

Con --refresh: guarda una nueva corrida fechada en
fuentes/sparql/corridas/<sello>/ (*.rq + *.json), sin sobrescribir los
originales. Todo queda dentro de esta carpeta.
"""
import datetime
import json
import pathlib
import sys
import urllib.request

BASE = "https://example.org/mex-ontologi/"
OUT = pathlib.Path("propuestas/ronda-2/agente-5-evaluacion-chat/fuentes/sparql")
URL = "http://127.0.0.1:8137/api/query"


def consultar(q):
    req = urllib.request.Request(
        URL, data=json.dumps({"query": q}).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def normalizar(d):
    if not isinstance(d, dict):
        return d
    return {"results": sorted([json.dumps(r, sort_keys=True) for r in d.get("results", [])]),
            "variables": sorted(d.get("variables", []))}


refresh = "--refresh" in sys.argv[1:]
dest = None
if refresh:
    sello = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = OUT / "corridas" / sello
    dest.mkdir(parents=True, exist_ok=False)

iguales, distintas, errores = [], [], []
for rq in sorted(OUT.glob("*.rq")):
    if rq.name == "_meta.json":
        continue
    q = rq.read_text(encoding="utf-8")
    try:
        raw = consultar(q)
        viva = json.loads(raw.decode())
    except Exception as e:  # noqa: BLE001 - se registra y se sigue
        errores.append({"consulta": rq.name, "error": str(e)[:300]})
        continue
    if dest is not None:
        (dest / rq.name).write_text(q, encoding="utf-8")
        (dest / (rq.stem + ".json")).write_bytes(raw)
    base = json.loads((rq.with_suffix(".json")).read_text(encoding="utf-8"))
    (iguales if normalizar(viva) == normalizar(base) else distintas).append(rq.name)

print(json.dumps({"comparadas": len(iguales) + len(distintas), "iguales": iguales,
                  "distintas": distintas, "errores": errores,
                  "corrida_guardada_en": str(dest) if dest else None},
                 ensure_ascii=False, indent=2))
raise SystemExit(1 if (distintas or errores) else 0)
