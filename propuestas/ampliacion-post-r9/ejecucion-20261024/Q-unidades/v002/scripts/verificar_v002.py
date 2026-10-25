"""Verifica Q-unidades v002 contra su sello. Solo lectura.

Uso: uv run python .../v002/scripts/verificar_v002.py
Comprueba: sha256 de cada archivo sellado, sello de congelada.json,
y las invariantes del TTL (6 declaraciones, 0 IRIs QUDT, 0 QuantityValue).
"""
import hashlib
import json
import pathlib
import sys

from rdflib import Graph, URIRef

V = pathlib.Path(__file__).resolve().parents[1]
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


sello = json.loads((V / "congelada.json").read_text(encoding="utf-8"))
fallos = []

for a in sello["archivos"]:
    p = BASE / a["ruta"]
    if not p.is_file():
        fallos.append(f"falta {a['ruta']}")
    elif sha(p) != a["sha256"] or p.stat().st_size != a["bytes"]:
        fallos.append(f"hash/bytes distintos: {a['ruta']}")

esperado = (V / "congelada.sha256").read_text(encoding="utf-8").split()[0]
if esperado != sha(V / "congelada.json"):
    fallos.append("congelada.sha256 no coincide con congelada.json")

for ruta, h in sello.get("base_verificada", {}).items():
    if not (BASE / ruta).is_file() or sha(BASE / ruta) != h:
        fallos.append(f"base alterada: {ruta}")

g = Graph()
g.parse(V / "propuesta-q-unidades.ttl", format="turtle")
q = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
     "SELECT (COUNT(?d) AS ?n) WHERE { ?d a mex:UnidadDeclarada }")
if int(list(g.query(q))[0][0]) != 6:
    fallos.append("no hay 6 declaraciones")
uris = {str(t) for t in set(g.subjects()) | set(g.predicates()) | set(g.objects())
        if isinstance(t, URIRef)}
if any("qudt.org" in u for u in uris):
    fallos.append("hay IRIs QUDT sin sello W")
if any("QuantityValue" in u for u in uris):
    fallos.append("hay QuantityValue")

# Copias fuente: byte a byte contra el origen
for a in json.loads((V / "fuentes/indice-copias.json").read_text(encoding="utf-8"))["copias"]:
    if sha(BASE / a["origen"]) != a["sha256_origen"] or \
            sha(BASE / a["copia"]) != a["sha256_origen"]:
        fallos.append(f"copia distinta: {a['caso']}")

print(f"archivos sellados: {len(sello['archivos'])}")
print("OK" if not fallos else "FALLOS:\n" + "\n".join(fallos))
sys.exit(1 if fallos else 0)
