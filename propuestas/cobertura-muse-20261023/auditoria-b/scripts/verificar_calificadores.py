"""Regresion calificadores: reglas COMPLETAS originales (69) con interpretacion() real.

1. interpretacion() real por regla completa -> assignment calificador == validar_calificador(original).
2. Triples RDF in-memory REPLICADOS del patron exacto de construir (lineas 211-219):
   variable -tieneCalificadorDocumentado-> q; q dimension/valor; luego la
   consulta queries/portal/semantica_calificadores.rq contra el grafo.
   NO es construir real: la prueba con construir REAL es la independiente del
   integrador (integrador/verificacion-generador.json + verificar_generador.py).
No escribe fuera de auditoria-b. No ejecuta suite central ni generar().
"""
import json, sys, os
from datetime import datetime, timezone
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.plugins.sparql import prepareQuery

B = "propuestas/cobertura-muse-20261023/auditoria-b"
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
from consolidar_semantica import huella, interpretacion, validar_calificador  # noqa: E402
from integrar_contenido import clave  # noqa: E402

ok = []


def check(n, c, d=""):
    if not c:
        raise AssertionError("FALLA: " + n + (" | " + d if d else ""))
    ok.append(n)


BASE = "https://example.org/mex-ontologi/"
mex = Namespace(BASE + "vocab/")
asig = json.load(open("propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
mine = {}
for ag in ("6", "7", "8"):
    for v in asig["asignaciones"][ag]["variables"]:
        mine[v["definicion_iri"]] = v
sem = json.load(open("ontologia/semantica.json", encoding="utf-8"))
ENT = {"salud": "propuestas/cobertura-muse-20261023/salud/entrega.json",
       "registro-civil": "propuestas/cobertura-muse-20261023/registro-civil/entrega.json",
       "educacion": "propuestas/cobertura-muse-20261023/educacion/entrega.json"}

g = Graph()
for pfx, ns in [("mex", mex), ("rdfs", RDFS)]:
    g.bind(pfx, ns)
rep = []
n = 0
for dom, f in ENT.items():
    prop = json.load(open(f, encoding="utf-8"))
    rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
        {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
         "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
         "representacion": r["representacion"],
         **({"calificador": r["calificador"]} if "calificador" in r else {}),
         **({"limites": r["limites"]} if "limites" in r else {}),
         **({"limite": r["limite"]} if "limite" in r else {})} for r in prop["reglas"]]}
    for r in prop["reglas"]:
        if "calificador" not in r:
            continue
        n += 1
        iri = r["definiciones"][0]
        a = mine[iri]
        res = interpretacion(a.get("variable", r["nombres"][0]), a.get("descripcion", r["descripciones"][0]),
                             a["conjunto"], rules, a["diccionario"], iri)
        check(f"asig_{r['id']}", res.get("estado") == "respaldada_por_definicion" and res.get("regla") == r["id"])
        check(f"calif_{r['id']}", res.get("calificador") == validar_calificador(r["calificador"]), str(res.get("calificador")))
        # patron exacto construir L211-219 (+ L193-209 para que corra la query portal)
        variable = URIRef(iri.replace("/definition/", "/documented-variable/"))
        g.add((variable, mex.nombreVariableLocal, Literal(r["nombres"][0])))
        g.add((variable, mex.significadoDocumentado, URIRef(BASE + "concept/" + r["concepto"])))
        for dimension, value in res["calificador"].items():
            q = URIRef(iri.replace("/definition/", "/documented-qualifier/") + "/" + dimension)
            g.add((variable, mex.tieneCalificadorDocumentado, q))
            g.add((q, RDF.type, mex.CalificadorDocumental))
            g.add((q, RDFS.label, Literal(dimension + ": " + value, lang="es")))
            g.add((q, mex.dimensionCalificador, Literal(dimension)))
            g.add((q, mex.valorCalificador, Literal(value)))
        rep.append({"regla": r["id"], "dominio": dom, "iri": iri,
                    "calificador_original": r["calificador"], "calificador_propagado": res["calificador"]})
check("total_69", n == 69, str(n))
# consulta portal real contra el grafo
rq = open("queries/portal/semantica_calificadores.rq", encoding="utf-8").read().replace("{{BASE_IRI}}", BASE)
rows = list(g.query(rq))
check("sparql_filas_115", len(rows) == 115, str(len(rows)))
check("sparql_69_variables", len({str(r[0]) for r in rows}) == 69)
g.serialize(B + "/calificadores.ttl", format="turtle")
json.dump({"fecha_utc": datetime.now(timezone.utc).isoformat(), "reglas": n,
           "triples_sparql": len(rows), "detalle": rep,
           "nota": "Reglas completas originales; motor actual propaga en reporte y RDF."},
          open(B + "/reporte_calificadores.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("calificadores OK: %d reglas, %d filas SPARQL, %d checks" % (n, len(rows), len(ok)))
