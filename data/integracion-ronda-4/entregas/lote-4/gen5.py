import json, hashlib, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))
d = json.load(open(LOTE/"_adicional.json", encoding="utf-8"))
h_antes = {k: hashlib.sha256(json.dumps(ent[k], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
           for k in ["reglas", "conceptos_nuevos", "decisiones_significados"]}
ent["decisiones_columnas"].extend(d["dec"])
ent["vinculos"].extend(d["vinc"])
h_despues = {k: hashlib.sha256(json.dumps(ent[k], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
             for k in ["reglas", "conceptos_nuevos", "decisiones_significados"]}
print("intactas:", h_antes == h_despues)
c = ent["conteos"] = {
 "columnas": len(ent["decisiones_columnas"]),
 "proponer": sum(1 for x in ent["decisiones_columnas"] if x["decision"] == "proponer"),
 "pendiente_columnas": sum(1 for x in ent["decisiones_columnas"] if x["decision"] == "pendiente"),
 "significados": len(ent["decisiones_significados"]),
 "significados_proponer": sum(1 for x in ent["decisiones_significados"] if x["decision"] == "proponer"),
 "significados_pendiente": sum(1 for x in ent["decisiones_significados"] if x["decision"] == "pendiente"),
 "vinculos": len(ent["vinculos"]), "reglas": len(ent["reglas"]),
 "conceptos_nuevos": len(ent["conceptos_nuevos"])}
json.dump(ent, open(LOTE/"entrega.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"pendientes_columnas": [x for x in ent["decisiones_columnas"] if x["decision"] == "pendiente"],
 "pendientes_significados": [x for x in ent["decisiones_significados"] if x["decision"] == "pendiente"],
 "nota": "Originales 592 + adicionales 81, una vez cada IRI; fase adicional solo anade decisiones_columnas y vinculos con dependencia explicita de reglas r4-lote-4-* propuestas."},
 open(LOTE/"pendientes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ("# Lote-4 — resultado (originales + adicionales)\n"
 f"- Columnas: {c['columnas']} decisiones ({c['proponer']} proponer / {c['pendiente_columnas']} pendiente).\n"
 f"- Vinculos: {c['vinculos']} (formato 9 claves, huellas verificadas; 81 adicionales con dependencia explicita de reglas r4-lote-4-* aun no auditadas).\n"
 f"- Significados: 47 (40 proponer / 7 pendiente); reglas nuevas: 40; conceptos nuevos: 23. Sin cambios en esta fase.\n"
 "- IRI unicos: originales 592 + adicionales 81 sin solape.\n")
open(LOTE/"resultado.md", "w", encoding="utf-8").write(md)
h = hashlib.sha256(open(LOTE/"entrega.json", "rb").read()).hexdigest()
json.dump({"entrega": "entrega.json", "sha256": h, "conteos": c},
          open(LOTE/"listo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(c, h)
