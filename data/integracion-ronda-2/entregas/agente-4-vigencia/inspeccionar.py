"""Inspeccion read-only de fuentes fijadas + catalogos.json; escribe solo extractos en este dir."""
import json, hashlib, pathlib
BASE = pathlib.Path(__file__).parent
EXT = BASE / "evidencia" / "extractos"
EXT.mkdir(parents=True, exist_ok=True)
CENTRO = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
man = json.loads((CENTRO/"data/integracion/manifiesto.json").read_text(encoding="utf-8"))
print("fuentes manifiesto:", len(man["fuentes"]))
# verificar sha de 3 archivos clave sin copiar
import hashlib as H
for k in ["propuestas\\agente-1-catalogos\\fuentes\\403912fd-5853-4e18-8256-f77206f855bd_6d561451-ff08-45d6-b1af-285ff5f417b1_Catalogo.bin",
 "propuestas\\agente-1-catalogos\\fuentes\\ee8f639f-5e89-46ae-93b9-934b05fc6233_f5060479-ee16-49b5-99d4-09aabef8042e_Catalogo.bin",
 "propuestas\\agente-1-catalogos\\fuentes\\5494daa1-09ca-4750-aeac-2558553700e1_08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8_Catalogo.bin"]:
    arch = CENTRO / man["fuentes"][k]["archivo"]
    h = H.sha256(arch.read_bytes()).hexdigest()
    print(k.split("\\")[-1][:40], arch.stat().st_size, h[:16], "OK" if h==man["fuentes"][k]["sha256"] or h==man["fuentes"][k] else "check-manifiesto")
# catalogos.json: resumir hojas y archivos por sha (para detectar edicion unica ea54...)
cat = json.loads((CENTRO/"data/territorio/catalogos.json").read_text(encoding="utf-8"))
from collections import Counter
print("total refs catalogos.json:", len(cat["referencias"]))
print(Counter((r["archivo_sha256"][:8], r["hoja"]) for r in cat["referencias"]))
# resoluciones territorio 8
ter = json.loads((CENTRO/"ontologia/territorio.json").read_text(encoding="utf-8"))
print("resoluciones:", len(ter["resoluciones"]))
for x in ter["resoluciones"]:
    print(x["diccionario"][:8], x["variable"], x["recurso"][:8], x["hoja"], x["archivo_sha256"][:8])
# guardar extracto resumen (derivado, no copia binaria)
(EXT/"resumen_fuentes.json").write_text(json.dumps({
 "manifiesto_fuentes": len(man["fuentes"]),
 "catalogos_json_refs": len(cat["referencias"]),
 "territorio_resoluciones": len(ter["resoluciones"]),
}, ensure_ascii=False, indent=1), encoding="utf-8")
print("extracto OK")
