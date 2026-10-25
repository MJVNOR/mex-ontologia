"""Auditoria A del payload R10: comprobaciones documentales y estructurales.

Solo lee. No instala, no escribe fuera de A-payload/v001.
Uso: uv run python <este archivo>
"""
import hashlib
import json
import pathlib

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import PROV

REPO = pathlib.Path(__file__).resolve().parents[5]
E = REPO / "propuestas/ampliacion-post-r9/ejecucion-20261024"
P = E / "payload/v001"
Q = E / "Q-unidades/v002"
MEX = Namespace("https://example.org/mex-ontologi/vocab/")
SH = Namespace("http://www.w3.org/ns/shacl#")

out = []


def nota(linea=""):
    out.append(linea)
    print(linea)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canon(v):
    return hashlib.sha256(json.dumps(
        v, ensure_ascii=False, sort_keys=True,
        separators=(",", ":")).encode("utf-8")).hexdigest()


def read(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


aceptadas = read(P / "aceptadas.json")
casos = read(Q / "casos.json")
por_id = {c["id"]: c for c in casos["casos"]}
sello = read(E / "sello-payload-previo.json")["archivos"]

nota("== 1. filas: payload == casos.json == copia local, y huella canonica ==")
for u in aceptadas["unidades"]:
    uid = u["id"]
    fila_payload = read(P / "filas" / f"{uid}.json")
    caso = por_id[uid]
    copia = read(Q / "fuentes" / uid / "fila.json")
    checks = {
        "payload==casos.fila": fila_payload == caso["fila"],
        "payload==copia.fila.json": fila_payload == copia,
        "huella==canon(payload)": canon(fila_payload) == u["huella_fila_diccionario"],
        "huella==casos": caso["huella_fila"] == u["huella_fila_diccionario"],
        "sha_sello_fila": sha(P / "filas" / f"{uid}.json") == sello[f"filas/{uid}.json"],
    }
    nota(f"{uid}: " + " ".join(f"{k}={'OK' if v else 'FALLA'}" for k, v in checks.items()))

nota()
nota("== 2. fuente local real: definiciones[indice] del JSON inspeccionado ==")
for u in aceptadas["unidades"]:
    uid = u["id"]
    caso = por_id[uid]
    origen = REPO / caso["fuente"]["ruta"]
    copia = Q / "fuentes" / uid / f"{u['diccionario']}.json"
    dato = read(origen)
    info = {
        "origen_existe": origen.is_file(),
        "sha_origen==casos": sha(origen) == caso["fuente"]["sha256"],
        "sha_copia==origen": sha(copia) == sha(origen),
        "http_200": dato.get("http") == 200,
        "ok": dato.get("ok") is True,
        "completo": dato.get("completo") is True,
    }
    defs = dato.get("definiciones") or []
    idx = caso["indice_definicion"]
    fila_origen = defs[idx] if idx < len(defs) else None
    info["fila_origen_existe"] = fila_origen is not None
    info["fila_origen==payload"] = fila_origen == read(P / "filas" / f"{uid}.json")
    info["url_origen==aceptadas"] = dato.get("fuente") == u["fuente_url"]
    nota(f"{uid} (definiciones[{idx}] de {len(defs)}): "
         + " ".join(f"{k}={'OK' if v else 'FALLA'}" for k, v in info.items()))

nota()
nota("== 3. normativa: SHA, version 3.5.3, IRI canonica exacta ==")
for u in aceptadas["unidades"]:
    uid = u["id"]
    t = P / "normativa" / f"{uid}.txt"
    texto = t.read_text(encoding="utf-8")
    info = {
        "sha_sello": sha(t) == sello[f"normativa/{uid}.txt"],
        "sha_aceptadas": sha(t) == u["normativa_sha256"],
        "version_3.5.3": "3.5.3" in texto,
        "iri_en_texto": u["normativa_uri"] in texto,
        "iri==unidad_qudt": u["normativa_uri"] == u["unidad_qudt"],
        "copia_textual_declarada": "COPIA TEXTUAL" in texto,
        "es_http_canonica": u["unidad_qudt"].startswith("http://qudt.org/vocab/unit/"),
    }
    nota(f"{uid} -> {u['unidad_qudt']}: "
         + " ".join(f"{k}={'OK' if v else 'FALLA'}" for k, v in info.items()))

nota()
nota("== 4. datos/unidades.ttl contra la whitelist derivada de aceptadas ==")
g = Graph().parse(P / "datos/unidades.ttl", format="turtle")
units = aceptadas["unidades"]
esperado = set()
for u in units:
    s = URIRef(u["sujeto"])
    esperado |= {
        (s, RDF.type, MEX.UnidadDeclarada),
        (s, MEX.variableDocumentada, URIRef(u["variable"])),
        (s, MEX.definicionFuente, URIRef(u["definicion_iri"])),
        (s, MEX.conjuntoFuente, Literal(u["conjunto"])),
        (s, MEX.diccionarioFuente, Literal(u["diccionario"])),
        (s, MEX.unidadLiteral, Literal(u["unidad_literal"])),
        (s, MEX.unidadQudt, URIRef(u["unidad_qudt"])),
        (s, PROV.wasDerivedFrom, URIRef(u["fuente_url"])),
        (s, PROV.wasDerivedFrom, URIRef(u["normativa_uri"])),
        (s, RDFS.label, Literal(u["etiqueta"])),
        (s, RDFS.comment, Literal(u["comentario"])),
        (s, MEX.evidenciaNormativa, Literal(u["evidencia_normativa"])),
    }
reales = set(g)
nota(f"tripletas reales={len(reales)} esperadas={len(esperado)} "
     f"iguales={reales == esperado}")
nota(f"extra={sorted(map(str, reales - esperado))}")
nota(f"faltan={sorted(map(str, esperado - reales))}")
nota(f"sujetos={len(set(g.subjects()))} (esperados {len(units)})")
prohibidos = {
    "http://qudt.org/schema/qudt/conversionMultiplier",
    "http://qudt.org/schema/qudt/conversionOffset",
    "http://qudt.org/schema/qudt/hasQuantityKind",
    "http://qudt.org/schema/qudt/quantityValue",
    "http://qudt.org/schema/qudt/QuantityValue",
    "http://qudt.org/vocab/unit/M3",
    "https://example.org/mex-ontologi/vocab/factorConversion",
    "https://example.org/mex-ontologi/vocab/datoscore",
}
hallados = [(str(s), str(p2), str(o)) for s, p2, o in reales
            if str(p2) in prohibidos or str(o) in prohibidos]
nota(f"predicados/objetos prohibidos: {hallados if hallados else 'ninguno'}")
nota(f"literal QUDT no sustituye al local (unidadLiteral conserva literal): "
     + ("OK" if all(read(P / "filas" / f"{u['id']}.json")["Unidad de medida"] == u["unidad_literal"]
                    for u in units) else "FALLA"))

nota()
nota("== 5. shapes: ids, sin sh:closed, clase/estado en los datos R9 ==")
gs = Graph().parse(P / "shapes/adicionales.ttl", format="turtle")
shapes = sorted(str(s) for s in gs.subjects(RDF.type, SH.NodeShape))
ids_shapes = sorted({s.rsplit("/", 1)[-1] for s in shapes})
declaradas = sorted(f["id"] for f in aceptadas["formas"])
nota(f"node shapes reales={len(ids_shapes)} declaradas={len(declaradas)} "
     f"iguales={ids_shapes == declaradas}")
nota(f"ids: {ids_shapes}")
closed = list(gs.triples((None, SH.closed, None)))
nota(f"sh:closed presente: {closed if closed else 'no (ninguno)'}")
targets = sorted({str(o) for o in gs.objects(None, SH.targetClass)})
nota(f"targetClass: {targets}")
no_shacl = [(str(s), str(p2)) for s, p2, _ in gs if not str(p2).startswith(str(SH))]
nota(f"predicados fuera de SHACL: {no_shacl if no_shacl else 'ninguno'}")
