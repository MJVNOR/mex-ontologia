"""Extrae las 47 variables candidatas sin modificar nada fuera de propuestas/agente-3-significados/."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COB = ROOT / "data" / "semantica" / "cobertura.json"
OUT = Path(__file__).resolve().parents[1] / "resultado_extraccion.json"

cob = json.loads(COB.read_text(encoding="utf-8"))
cands = [v for v in cob["variables"] if v.get("estado") == "candidata_sin_definicion_suficiente"]
cands.sort(key=lambda v: (v["titulo_conjunto"], v["diccionario"], v["variable"]))

resumen = {
    "total": len(cands),
    "pendiente_explicito": sum(1 for v in cands if (v.get("descripcion") or "").strip().lower() == "pendiente de especificar"),
    "otros": sum(1 for v in cands if (v.get("descripcion") or "").strip().lower() != "pendiente de especificar"),
}
OUT.write_text(json.dumps({"resumen": resumen, "variables": cands}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(resumen, ensure_ascii=False, indent=2))
for v in cands:
    print(f"{v['titulo_conjunto'][:45]:45} | {v['variable']:38} | {repr(v['descripcion'])}")
