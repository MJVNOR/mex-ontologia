"""Inventario local de clases/estados frente a las formas SHACL vigentes.

Lee copias locales (no modifica nada): portal-completo.ttl, shapes.ttl y las
formas fuente en shapes/. Escribe analisis/inspeccion.json.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import Graph, Namespace, RDF, URIRef

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
OUT = Path(__file__).resolve().parent

SH = Namespace("http://www.w3.org/ns/shacl#")
MEX = Namespace("https://example.org/mex-ontologi/vocab/")


def cargar() -> tuple[Graph, Graph]:
    datos = Graph().parse(ROOT / "data/portal/portal-completo.ttl", format="turtle")
    formas = Graph().parse(ROOT / "data/portal/shapes.ttl", format="turtle")
    return datos, formas


def blancos(formas: Graph, datos: Graph) -> list[dict]:
    filas = []
    for forma in formas.subjects(RDF.type, SH.NodeShape):
        clases = [o for o in formas.objects(forma, SH.targetClass)]
        por_sujeto = [o for o in formas.objects(forma, SH.targetSubjectsOf)]
        por_objeto = [o for o in formas.objects(forma, SH.targetObjectsOf)]
        focos: set[URIRef] = set()
        for clase in clases:
            focos |= set(datos.subjects(RDF.type, clase))
        for pred in por_sujeto:
            focos |= set(datos.subjects(pred, None))
        for pred in por_objeto:
            focos |= set(datos.objects(None, pred))
        restricciones = list(formas.objects(forma, SH.property))
        filas.append({
            "forma": str(forma),
            "target_class": [str(c) for c in clases],
            "target_subjects_of": [str(p) for p in por_sujeto],
            "target_objects_of": [str(p) for p in por_objeto],
            "propiedades": len(restricciones),
            "focos": len(focos),
            "sin_instancias": not focos,
        })
    filas.sort(key=lambda f: (f["sin_instancias"], f["forma"]))
    return filas


def inventario_clases(datos: Graph) -> dict[str, int]:
    conteo = Counter(str(o) for o in datos.objects(None, RDF.type))
    return dict(sorted(conteo.items(), key=lambda kv: (-kv[1], kv[0])))


def estados_por_propiedad(datos: Graph) -> dict[str, Counter]:
    """Valores literales por predicado declarativo (los que las formas acotan)."""
    interesantes = {
        "estadoSemantico", "estadoCorrespondencia", "estadoReferenciaCatalogo",
        "estadoDictamen", "estadoContraste", "estadoCoincidenciaCensal",
        "estadoVigenciaRevisada", "estadoEvaluacionUI", "identidadBackend",
        "estadoCasoEvaluacion", "estadoDecision", "tipoEvidencia",
        "estadoCorrespondenciaTerritorial", "estadoVigencia", "estadoOportunidad",
        "prioridadRevision", "resultadoInspeccion", "estadoEstructura",
        "tipoPagina", "decisionLote", "estadoComprobacion", "coberturaComprobacion",
        "estadoReferenciaObservada", "fuenteRol", "estadoFinal",
    }
    salida: dict[str, Counter] = defaultdict(Counter)
    for predicado in datos.predicates(None, None):
        if str(predicado).startswith(str(MEX)) and str(predicado)[len(str(MEX)):] in interesantes:
            for valor in datos.objects(None, predicado):
                salida[str(predicado)][str(valor)] += 1
    return salida


def main() -> None:
    datos, formas = cargar()
    inspeccion = {
        "triples_datos": len(datos),
        "triples_formas": len(formas),
        "clases": inventario_clases(datos),
        "formas": blancos(formas, datos),
        "estados_observados": {k: dict(v.most_common()) for k, v in estados_por_propiedad(datos).items()},
    }
    (OUT / "inspeccion.json").write_text(
        json.dumps(inspeccion, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "triples_datos": inspeccion["triples_datos"],
        "formas": len(inspeccion["formas"]),
        "sin_instancias": [f["forma"].rsplit("/", 1)[-1] for f in inspeccion["formas"] if f["sin_instancias"]],
        "clases": len(inspeccion["clases"]),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
