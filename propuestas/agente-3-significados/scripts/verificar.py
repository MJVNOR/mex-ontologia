"""Verificación de la devolución (solo lee; no toca el motor ni Studio)."""
import json
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
PROP = HERE / "propuestas.json"
COB = ROOT / "data/semantica/cobertura.json"
ONT = ROOT / "ontologia/semantica.json"

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    return " ".join(s.lower().strip(" ,;:\t\n").split())

prop = json.loads(PROP.read_text(encoding="utf-8"))
cob_all = json.loads(COB.read_text(encoding="utf-8"))["variables"]
cob = {v["definicion_iri"]: v for v in cob_all}
ont = json.loads(ONT.read_text(encoding="utf-8"))
central = {norm(d) for r in ont["reglas_descripcion_exacta"] for d in r["descripciones"]}

assert prop["resumen"]["total"] == 47
assert prop["resumen"]["proponer"] + prop["resumen"]["mantener_pendiente"] == 47
assert sum(prop["resumen"]["motivos_pendiente"].values()) == prop["resumen"]["mantener_pendiente"]
assert prop["resumen"]["motivos_pendiente"].get("descripcion_pendiente_explicita") == 17
assert len(prop["variables"]) == 47

# 1. Fecha de la denuncia: denominación neutral, sin recepción confirmada.
ids = {c["id"] for c in prop["conceptos_nuevos"]} | {r["id"] for r in prop["reglas_nuevas"]}
assert "fecha-denuncia" in ids, "falta fecha-denuncia"
assert "fecha-recepcion-denuncia" not in ids, "recepción no confirmada"
fd = next(c for c in prop["conceptos_nuevos"] if c["id"] == "fecha-denuncia")
assert fd["etiqueta"] == "Fecha de la denuncia", fd
assert "recepción" not in fd["etiqueta"].lower() or "no" in fd["definicion"].lower()
assert "no se asume recepci" in fd["definicion"].lower() or "no la confirma" in fd["definicion"].lower(), fd["definicion"]

# 2. Muestras clínicas: literalidad sin deducción.
suero = [c for c in prop["conceptos_nuevos"] if "suero" in c["id"]]
assert len(suero) == 3
for c in suero:
    assert "primera muestra de suero" in c["definicion"].lower(), c["id"]
    assert "prueba serologica ser1" not in norm(c["definicion"]), c["id"]
    assert ("sin deducir" in c["definicion"].lower() or "no prueba tipificada" in c["definicion"].lower() or "sin tipificar" in c["definicion"].lower()), c["id"]
    assert "ser1" in c["definicion"].lower(), c["id"]
assert "fecha-resultado-rtpcr-rickettsia" not in ids
pcr = next(c for c in prop["conceptos_nuevos"] if "pcr-tiempo-real" in c["id"])
assert "PCR tiempo real" in pcr["definicion"], pcr
assert "RT-PCR" not in pcr["definicion"] and "rt-pcr" not in pcr["definicion"].lower().replace("pcr tiempo real", ""), pcr

# 3. Alcance estructurado y verificable.
for r in prop["reglas_nuevas"]:
    assert r.get("alcance_verificable") is True, r["id"]
    for k in ("definiciones_objetivo", "diccionarios_objetivo", "conjuntos_objetivo", "variables_objetivo"):
        assert r.get(k), (r["id"], k)
    assert r["ejemplos_positivos"] and r["contraejemplos"], r["id"]
    # Cada objetivo existe y propone esta regla.
    for iri in r["definiciones_objetivo"]:
        x = next(v for v in prop["variables"] if v["definicion_iri"] == iri)
        assert x["decision"] == "proponer" and x["regla_propuesta"]["id"] == r["id"], (r["id"], iri)
    # Ninguna descripción nueva colisiona con el vocabulario central.
    for d in r["descripciones_cubiertas"]:
        assert norm(d) not in central, (r["id"], d)
    # Ninguna descripción nueva alcanza variables fuera de su objetivo.
    for v in cob_all:
        if norm(v["descripcion"]) in {norm(d) for d in r["descripciones_cubiertas"]}:
            assert v["definicion_iri"] in r["definiciones_objetivo"], (r["id"], v["definicion_iri"])

for x in prop["variables"]:
    c = cob[x["definicion_iri"]]
    assert x["descripcion_literal"] == c["descripcion"], x["definicion_iri"]
    assert x["huella_fila_diccionario"] == c["huella_fila_diccionario"], x["definicion_iri"]
    assert x["estado_previo"] == "candidata_sin_definicion_suficiente"
    assert x["documentado_vs_inferencia"].startswith("Documentado:")
    if (c["descripcion"] or "").strip().lower() == "pendiente de especificar":
        assert x["decision"] == "mantener_pendiente", x["definicion_iri"]
    if x["decision"] == "proponer":
        assert x["concepto_propuesto"] and x["regla_propuesta"]
        assert x["regla_propuesta"]["definiciones_objetivo"] == [x["definicion_iri"]]
    else:
        assert x["concepto_propuesto"] is None and x["regla_propuesta"] is None
        # Pendientes no alcanzados por ninguna regla nueva.
        for r in prop["reglas_nuevas"]:
            assert norm(x["descripcion_literal"]) not in {norm(d) for d in r["descripciones_cubiertas"]}, (x["definicion_iri"], r["id"])

print("OK: denuncia neutral, muestras literales y alcance estructurado verificados; sin tocar el motor.")
print(json.dumps(prop["resumen"], ensure_ascii=False, indent=2))
