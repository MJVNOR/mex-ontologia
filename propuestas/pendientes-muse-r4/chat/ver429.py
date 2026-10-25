"""Inspecciona el error 429 de C6 (solo clasificacion, sin secretos)."""
import json
import re

e = json.load(open("propuestas/pendientes-muse-r4/chat/evaluacion.json", encoding="utf-8"))
c = [x for x in e["casos"] if x["id"] == "C6-clave-26001"][0]
causa = c["causa"].replace("\n", " ")
for patron in ["quotaMetric[^,]*", "quotaId[^,]*", "GenerateRequests[^\"\\\\]*", "retry in [^\"\\\\]*", "per minute[^\"\\\\]*", "per day[^\"\\\\]*"]:
    m = re.search(patron, causa)
    if m:
        print(patron, "=>", m.group(0)[:160])
