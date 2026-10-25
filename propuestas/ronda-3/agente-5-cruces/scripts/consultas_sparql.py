"""Ejecuta las 3 consultas SPARQL contra data/portal/oportunidades.ttl (rdflib, sin BD nueva).
Verifica: 3916 pares totales, 1 exploratorio, proyecciones con familias entidad+municipio.
"""
from pathlib import Path
import rdflib

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"


def run(g, nombre):
    q = (BASE / "queries" / nombre).read_text(encoding="utf-8")
    return list(g.query(q))


def main():
    g = rdflib.Graph()
    g.parse(str(RAIZ / "data" / "portal" / "oportunidades.ttl"), format="turtle")
    r1 = run(g, "q1_pares_por_estado.rq")
    tot = sum(int(r[1]) for r in r1)
    estados = {str(r[0]): int(r[1]) for r in r1}
    assert tot == 3916, (tot, estados)
    assert estados.get("exploratorio_ejecutado") == 1, estados
    assert estados.get("candidata_por_validar") == 1191, estados
    assert estados.get("sin_clave_detectada") == 2328, estados
    assert estados.get("solo_dimensiones_amplias_o_tiempo") == 396, estados
    r3 = run(g, "q3_exploratorio.rq")
    assert len(r3) == 1, len(r3)
    r2 = run(g, "q2_proyecciones.rq")
    fams = {str(r[2]) for r in r2}
    assert {"entidad", "municipio"} <= fams, fams
    print("SPARQL OK:", estados)


if __name__ == "__main__":
    main()
