"""Consultas canónicas de la ontología para agentes LLM.

Uso:
  uv run python scripts/consultar_ontologia.py significado --variable anio --limite 20
  uv run python scripts/consultar_ontologia.py correspondencias --variable matrimonios
  uv run python scripts/consultar_ontologia.py resumen
  uv run python scripts/consultar_ontologia.py sparql "SELECT ... LIMIT 10"

Los cruces van por scripts/consultar_cruces.py (JSON, no RDF).
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from construir_catalogo import ROOT, motor
from rdflib.util import from_n3

ESCRITURA = re.compile(r"\b(INSERT|DELETE|LOAD|CLEAR|DROP|CREATE|WITH|COPY|MOVE|ADD)\b", re.I)


def manifest():
    m = json.loads((ROOT / "reports/portal-carga.json").read_text(encoding="utf-8"))
    if "store_dir" not in m:
        raise SystemExit("Genera y carga el portal primero con ampliar_portal.py --load")
    return m


def run(sparql, limite=None):
    m = manifest()
    q = sparql.replace("{{BASE_IRI}}", m["base_iri"])
    verificar(q)
    payload = motor(["query", q], ROOT / m["store_dir"])
    rows = [{k: from_n3(v).toPython() for k, v in row.items()}
            for row in payload.get("results", [])]
    return {"alcance": "portal-completo", "total": len(rows),
            "parcial": limite is not None and len(rows) >= limite,
            "resultados": rows[:limite] if limite else rows}


def verificar(q):
    if ESCRITURA.search(q):
        raise ValueError("Solo lectura: INSERT/DELETE/LOAD no permitidos")
    qs = q.lstrip().upper()
    if qs.startswith("SELECT") and "LIMIT" not in q.upper():
        raise ValueError("SELECT sin LIMIT: añade LIMIT (máx 2000)")


def lit(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def cmd_significado(args):
    filtro = f'FILTER(CONTAINS(LCASE(?variable), LCASE("{lit(args.variable)}")))' if args.variable else ""
    return run("""PREFIX mex: <{{BASE_IRI}}vocab/> PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?conjunto ?variable ?significado ?definicion WHERE {
  ?dataset mex:variableDocumentada ?v ; dct:title ?conjunto .
  ?v mex:nombreVariableLocal ?variable ; mex:significadoDocumentado/skos:prefLabel ?significado ; dct:description ?definicion .
  %s
} ORDER BY ?significado ?conjunto ?variable LIMIT %d""" % (filtro, args.limite), args.limite)


def cmd_correspondencias(args):
    # ponytail: paginación OFFSET, conteo total separado; ejemplos capados, conteo completo
    base = """PREFIX mex: <{{BASE_IRI}}vocab/> PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?variable ?estado ?columna ?significado WHERE {
  ?c a mex:CorrespondenciaSemantica ; mex:estadoCorrespondencia ?estado ; mex:variableDestino ?v .
  ?v mex:nombreVariableLocal ?variable .
  OPTIONAL { ?c mex:columnaOrigen/mex:nombreCampo ?columna }
  OPTIONAL { ?v mex:significadoDocumentado/skos:prefLabel ?significado }
  FILTER(CONTAINS(LCASE(?variable), LCASE("%s")))
} ORDER BY ?variable ?estado""" % lit(args.variable)
    total_q = """PREFIX mex: <{{BASE_IRI}}vocab/>
SELECT (COUNT(?c) AS ?n) WHERE {
  ?c a mex:CorrespondenciaSemantica ; mex:variableDestino ?v .
  ?v mex:nombreVariableLocal ?variable .
  FILTER(CONTAINS(LCASE(?variable), LCASE("%s")))
}""" % lit(args.variable)
    total = run(total_q)["resultados"][0]["n"]
    filas, offset, pagina = [], 0, 200
    while True:
        lote = run(base + f" LIMIT {pagina} OFFSET {offset}")["resultados"]
        filas.extend(lote)
        if len(lote) < pagina:
            break
        offset += pagina
    return {"alcance": "correspondencias de %s" % args.variable, "total": int(total),
            "parcial": len(filas) > args.muestra,
            "conteo_completo": True, "ejemplos_mostrados": min(args.muestra, len(filas)),
            "resultados": filas[:args.muestra]}


def cmd_resumen(_args):
    q = (ROOT / "queries/portal/resumen.rq").read_text(encoding="utf-8")
    return run(q)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("significado"); s.add_argument("--variable", default=""); s.add_argument("--limite", type=int, default=50)
    c = sub.add_parser("correspondencias"); c.add_argument("--variable", required=True); c.add_argument("--muestra", type=int, default=80)
    sub.add_parser("resumen")
    q = sub.add_parser("sparql"); q.add_argument("consulta"); q.add_argument("--limite", type=int, default=200)
    args = p.parse_args()
    fn = {"significado": cmd_significado, "correspondencias": cmd_correspondencias,
          "resumen": cmd_resumen}[args.cmd] if args.cmd != "sparql" else None
    try:
        out = fn(args) if fn else run(args.consulta, args.limite)
    except ValueError as e:
        p.error(str(e))
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
