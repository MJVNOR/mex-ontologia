"""Ejecuta una consulta guardada sobre la última carga del catálogo."""

import argparse
import json
from pathlib import Path
from rdflib.util import from_n3
from construir_catalogo import ROOT, motor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("consulta", type=Path, help="Archivo SPARQL .rq")
    parser.add_argument("--raw", action="store_true", help="Conservar términos RDF tal como los devuelve el motor")
    parser.add_argument("--portal", action="store_true", help="Consultar el almacén ampliado de páginas y estructuras")
    args = parser.parse_args()
    manifest = json.loads((ROOT / ("reports/portal-carga.json" if args.portal else "reports/catalogo-carga.json")).read_text(encoding="utf-8"))
    if "store_dir" not in manifest:
        parser.error("Genera y carga el catálogo primero con construir_catalogo.py --load")
    query = args.consulta.read_text(encoding="utf-8").replace("{{BASE_IRI}}", manifest["base_iri"])
    result = motor(["query", query], ROOT / manifest["store_dir"])
    if not args.raw:
        result["results"] = [
            {key: from_n3(value).toPython() for key, value in row.items()}
            for row in result.get("results", [])
        ]
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
