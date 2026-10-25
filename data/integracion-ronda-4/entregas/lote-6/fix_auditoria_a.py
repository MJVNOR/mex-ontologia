"""Reentrega lote-6 por auditoria-a: condicion sobre r4-lote-6-dig-sector-nombre.
Solo anade limite explicito + criterio/motivos pertinentes. No revierte nada."""
import hashlib, json
from pathlib import Path

LOTE = Path("C:/Users/marti/Documents/MEX-Ontologi/propuestas/pendientes-muse-r4/lote-6")
entrega = json.loads((LOTE / "entrega.json").read_text(encoding="utf-8"))

LIMITE = ("ejemplo '04 - SECRETARIA DE HACIENDA' conservado como texto declarado sin separar codigo de nombre; "
          "no acredita catalogo de sectores ni autoriza comparar o equiparar sectores entre encuestas")
DEF = "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F2"
COL = "https://example.org/mex-ontologi/file-column/c6f39770-4365-498f-9c59-6407220b5b01%2FHoja1%2F2"

tocadas = 0
for r in entrega["reglas"]:
    if r["id"] == "r4-lote-6-dig-sector-nombre":
        assert r["definiciones"] == [DEF] and r["huella_fila_diccionario"] == "7e4792227b1e57f623212566d266783aa37726e8a6b627b00ec2056839875577"
        assert r["concepto"] == "sector-dependencia-diagnostico" and r["representacion"] == "nombre"
        assert r["nombres"] == ["P2"] and r["descripciones"] == ["Sector"]
        assert r["evidencia"]["ejemplo"] == "04 - SECRETARIA DE HACIENDA"
        if LIMITE not in r["limites"]:
            r["limites"].append(LIMITE)
        r["criterio"] = ("Literal especifico 'Sector' mas contexto publicado del conjunto; tipo 'Texto'; "
                         "ejemplo '04 - SECRETARIA DE HACIENDA' conservado como texto sin separar codigo/nombre. "
                         "Condicion auditoria-a resuelta con limite explicito.")
        tocadas += 1
assert tocadas == 1

for v in entrega["vinculos"]:
    if v["columna"] == COL:
        assert v["dependencia"].endswith("(regla r4-lote-6-dig-sector-nombre)")
        if LIMITE not in v["criterio"]:
            v["criterio"] += " Limite de auditoria: " + LIMITE + "."
        tocadas += 1
assert tocadas == 2

for d in entrega["decisiones_columnas"]:
    if d["columna"] == COL:
        assert d["decision"] == "proponer" and d["definicion_iri"] == DEF
        if "auditoria-a" not in d["motivo"]:
            d["motivo"] += "; condicion auditoria-a: " + LIMITE
        tocadas += 1
assert tocadas == 3

for d in entrega["decisiones_significados"]:
    if d["definicion_iri"] == DEF:
        assert d["decision"] == "proponer"
        if "auditoria-a" not in d["motivo"]:
            d["motivo"] += "; condicion auditoria-a resuelta con limite explicito: " + LIMITE
        tocadas += 1
assert tocadas == 4

# resto intacto: 30 reglas, 27 conceptos, 66 significados, 604 columnas, 599 vinculos
assert len(entrega["reglas"]) == 30 and len(entrega["conceptos_nuevos"]) == 27
assert len(entrega["decisiones_significados"]) == 66 and len(entrega["decisiones_columnas"]) == 604
assert len(entrega["vinculos"]) == 599

(LOTE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
listo = json.loads((LOTE / "listo.json").read_text(encoding="utf-8"))
listo["sha256_entrega"] = sha
(LOTE / "listo.json").write_text(json.dumps(listo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", sha)
