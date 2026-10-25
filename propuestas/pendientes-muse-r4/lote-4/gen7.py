import json, hashlib, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))
c = ent["conteos"] = {
 "columnas": len(ent["decisiones_columnas"]),
 "proponer": sum(1 for x in ent["decisiones_columnas"] if x["decision"] == "proponer"),
 "pendiente_columnas": sum(1 for x in ent["decisiones_columnas"] if x["decision"] == "pendiente"),
 "significados": len(ent["decisiones_significados"]),
 "significados_proponer": sum(1 for x in ent["decisiones_significados"] if x["decision"] == "proponer"),
 "significados_pendiente": sum(1 for x in ent["decisiones_significados"] if x["decision"] == "pendiente"),
 "vinculos": len(ent["vinculos"]), "reglas": len(ent["reglas"]),
 "conceptos_nuevos": len(ent["conceptos_nuevos"])}
json.dump({"pendientes_columnas": [x for x in ent["decisiones_columnas"] if x["decision"] == "pendiente"],
 "pendientes_significados": [x for x in ent["decisiones_significados"] if x["decision"] == "pendiente"],
 "nota": "Reentrega auditoria-a: retiradas r4-lote-4-025/026/027 con 3 vinculos y 2 conceptos huerfanos; limites reforzados 002/003/004, 008/009/010, 022, 038/039."},
 open(LOTE/"pendientes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ("# Lote-4 — resultado (reentrega auditoria-a)\n"
 f"- Columnas: {c['columnas']} decisiones ({c['proponer']} proponer / {c['pendiente_columnas']} pendiente: Total_Egresos + P36/P39/P40 desarrollo por contradiccion Booleano vs conteo/procedimiento).\n"
 f"- Vinculos: {c['vinculos']} (formato 9 claves, huellas verificadas).\n"
 f"- Significados: 47 ({c['significados_proponer']} proponer / {c['significados_pendiente']} pendiente); reglas: 37; conceptos nuevos: 21.\n"
 "- Limites reforzados: no-comparabilidad entre metodologias (002/003/004); no separar codigo/nombre ni equiparar encuestas (008/009/010); texto libre sin tabular (022); sin equivalencia CIE entre diccionarios ni version (038/039).\n")
open(LOTE/"resultado.md", "w", encoding="utf-8").write(md)
h = hashlib.sha256(open(LOTE/"entrega.json", "rb").read()).hexdigest()
json.dump({"entrega": "entrega.json", "sha256": h, "conteos": c},
          open(LOTE/"listo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(c, h)
