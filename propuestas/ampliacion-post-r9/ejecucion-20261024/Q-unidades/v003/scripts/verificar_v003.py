"""Q-unidades v003: verificacion de solo lectura del sello y del TTL.

No escribe nada. Replica los sha256 de congelada.json, comprueba las copias
contra sus originales, ejecuta las consultas y confirma que v002 y W v002
siguen intactos.
"""
import hashlib
import json
import pathlib

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
EJ = BASE / "propuestas/ampliacion-post-r9/ejecucion-20261024"
V = EJ / "Q-unidades/v003"
W = EJ / "W-estandares/v002"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


sello = json.loads((V / "congelada.json").read_text(encoding="utf-8"))
assert sello["rol"] == "Q-unidades" and sello["version"] == "v003"

for a in sello["archivos"]:
    p = BASE / a["ruta"]
    assert p.is_file(), a["ruta"]
    assert sha(p) == a["sha256"], f"hash distinto: {a['ruta']}"
    assert p.stat().st_size == a["bytes"], f"bytes distintos: {a['ruta']}"
    assert a["ruta"].startswith(V.relative_to(BASE).as_posix() + "/")

en_disco = sorted(p.relative_to(BASE).as_posix() for p in V.rglob("*")
                  if p.is_file() and p.name not in
                  ("congelada.json", "congelada.sha256"))
assert en_disco == sorted(a["ruta"] for a in sello["archivos"]), "archivos sin sellar"

for ruta, esperado in sello["base_verificada"].items():
    assert sha(BASE / ruta) == esperado, f"base alterada: {ruta}"
for ruta, esperado in sello["predecesora_w_observada"].items():
    if ruta.startswith("propuestas/"):
        assert sha(BASE / ruta) == esperado, f"W v002 alterado: {ruta}"

indice = json.loads((V / "fuentes/indice-copias.json").read_text(encoding="utf-8"))
for grupo in ("locales", "normativas"):
    for c in indice[grupo]:
        assert sha(BASE / c["origen"]) == c["sha256_origen"], c["origen"]
        assert sha(BASE / c["copia"]) == c["sha256_copia"], c["copia"]
        assert c["sha256_origen"] == c["sha256_copia"], c["caso"]
assert len(indice["locales"]) == 5 and len(indice["normativas"]) == 5

from rdflib import Graph, URIRef

g = Graph()
g.parse(V / "propuesta-q-unidades.ttl", format="turtle")
P = "PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
rows = list(g.query(P + "SELECT ?d ?lit ?u ?ev WHERE { ?d a mex:UnidadDeclarada ;"
                       " mex:unidadLiteral ?lit ; mex:unidadQudt ?u ;"
                       " mex:evidenciaNormativa ?ev }"))
assert len(rows) == 5, len(rows)
assert all(str(r[2]).startswith("http://qudt.org/vocab/unit/") for r in rows)
assert len({str(r[2]) for r in rows}) == 5
assert all("sha256=" in str(r[3]) and "sello W v002" in str(r[3]) for r in rows)

todas = {str(t) for t in set(g.subjects()) | set(g.predicates()) | set(g.objects())
         if isinstance(t, URIRef)}
assert not any("qudt.org" in u and not u.startswith("http://qudt.org/") for u in todas)
assert not any(x in " ".join(todas) for x in ("QuantityValue", "TON_Metric", "unit/M3",
                                             "HectoM3", "conversion"))

entrega = json.loads((V / "entrega.json").read_text(encoding="utf-8"))
assert entrega["resumen"]["declaraciones"] == 5
assert entrega["grafo"]["sha256"] == sha(V / "propuesta-q-unidades.ttl")
assert entrega["fuentes"]["sha256_indice"] == sha(V / "fuentes/indice-copias.json")
assert entrega["predecesoras"]["w_v002"]["sha256"] == sha(W / "congelada.json")
assert [c["id"] for c in entrega["casos"]] == ["Q-U02", "Q-U03", "Q-U04",
                                               "Q-U05", "Q-U06"]

print(f"OK verificacion v003: {len(sello['archivos'])} archivos sellados, "
      f"5 declaraciones, 10 copias, W v002 {sha(W / 'congelada.json')[:12]}")
print(f"sello congelada.json = {sha(V / 'congelada.json')}")
