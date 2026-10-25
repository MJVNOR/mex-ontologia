"""Comprobaciones sobre el grafo R9 real y el snapshot de cobertura.

Solo lee. No escribe nada fuera de A-payload/v001.
"""
import json
import pathlib
from collections import Counter

from rdflib import Graph, Literal, Namespace, RDF, URIRef

REPO = pathlib.Path(__file__).resolve().parents[5]
E = REPO / "propuestas/ampliacion-post-r9/ejecucion-20261024"
P = E / "payload/v001"
MEX = Namespace("https://example.org/mex-ontologi/vocab/")

aceptadas = json.loads((P / "aceptadas.json").read_text(encoding="utf-8"))

print("== grafo R9 vivo: data/portal/portal-completo.ttl ==", flush=True)
g = Graph().parse(REPO / "data/portal/portal-completo.ttl", format="turtle")
print("triples:", len(g), flush=True)

print("\ntipos de interes:")
for clase in ("VariableDocumentada", "CorrespondenciaSemantica", "UnidadDeclarada",
              "DefinicionVariable", "Significado"):
    print(f"  mex:{clase}: {len(set(g.subjects(RDF.type, MEX[clase])))}")

print("\nestadoSemantico:", Counter(str(o) for o in g.objects(None, MEX.estadoSemantico)).most_common())
print("estadoCorrespondencia:", Counter(str(o) for o in g.objects(None, MEX.estadoCorrespondencia)).most_common())
for pred in ("significadoDocumentado", "significadoCandidato", "variableDestino",
             "unidadLiteral", "unidadQudt", "definicionFuente", "variableDocumentada"):
    print(f"  {pred}: {len(list(g.triples((None, MEX[pred], None))))}")

print("\naserciones ya existentes (posible duplicado R10):")
vivos = set(g)
for u in aceptadas["unidades"]:
    s = URIRef(u["sujeto"])
    print(f"  {u['id']}: sujeto_en_grafo={s in set(g.subjects())} "
          f"definicion_en_grafo={URIRef(u['definicion_iri']) in set(g.subjects())}")

print("\nlas 5 definiciones y variables del payload en el grafo R9:")
for u in aceptadas["unidades"]:
    v = URIRef(u["variable"])
    d = URIRef(u["definicion_iri"])
    est = list(g.objects(v, MEX.estadoSemantico))
    print(f"  {u['id']}: variable_tipos={[str(t) for t in g.objects(v, RDF.type)]} "
          f"estado={[str(e) for e in est]} definicion_tipos={[str(t) for t in g.objects(d, RDF.type)]}")

print("\nUnidadDeclarada ya presentes en R9 (patron previo):")
for s in sorted(set(g.subjects(RDF.type, MEX.UnidadDeclarada)), key=str):
    print(" ", s)
    for p, o in sorted(g.predicate_objects(s), key=lambda x: str(x[0])):
        print("    ", p, "=", o)

print("\n== cobertura-r9.json: respaldo de las 5 unidades ==")
cob = json.loads((P / "cobertura-r9.json").read_text(encoding="utf-8"))
print("resumen:", json.dumps(cob.get("resumen"), ensure_ascii=False, sort_keys=True)[:400])
idx = {v.get("definicion_iri"): v for v in cob.get("variables", [])}
for u in aceptadas["unidades"]:
    v = idx.get(u["definicion_iri"])
    if v is None:
        print(f"  {u['id']}: SIN ENTRADA en cobertura-r9")
        continue
    campos = {
        "variable/iri": (u["variable"], v.get("iri")),
        "variable/nombre": (u["nombre"], v.get("variable")),
        "conjunto": (u["conjunto"], v.get("conjunto")),
        "diccionario": (u["diccionario"], v.get("diccionario")),
        "huella": (u["huella_fila_diccionario"], v.get("huella_fila_diccionario")),
    }
    estado = v.get("estado")
    malos = {k: par for k, par in campos.items() if par[0] != par[1]}
    print(f"  {u['id']}: estado={estado} campos_ok={not malos} "
          f"{'' if not malos else malos}")
