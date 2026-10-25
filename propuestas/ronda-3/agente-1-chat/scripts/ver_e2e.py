import json
d = json.load(open("evidencia/e2e_recuperacion.json", encoding="utf-8"))
print(d["motor"], d["fecha_utc"])
for c in d["casos"]:
    print("-", c["pregunta"][:70])
    print("  " + c["resumen"][:500].replace("\n", " | "))
print("contextos:", [len(c["contexto"]) for c in d["casos"]])
