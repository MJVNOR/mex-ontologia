"""Genera preguntas-publicador.md: 14 originales intactas + estado ronda-3."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
BASE = AQUI.parents[2]
r2 = (BASE / "data" / "integracion-ronda-2" / "entregas"
      / "agente-2-pendientes" / "preguntas-publicador.md").read_text(encoding="utf-8")
prop = json.loads((AQUI / "propuestas.json").read_text(encoding="utf-8"))
estado = {q["id"]: q["estado_ronda3"] for q in prop["preguntas_publicador"]}

cab = ("# Preguntas al publicador (sin contactar; redactadas para tramite)\n\n"
       "14 preguntas originales de ronda-2 preservadas textualmente (trazabilidad). "
       "Ronda-3 anade bajo cada pregunta una linea de estado con la "
       "evidencia actual; ninguna pregunta se envio ni se elimina.\n")

# Divide el original en preambulo + secciones ## Q-...
partes = re.split(r"(?m)^## ", r2)
preambulo = partes[0]
# Quita solo la primera linea de titulo del preambulo original y la conserva
assert preambulo.startswith("# Preguntas"), "preambulo inesperado"
preambulo_sin_titulo = preambulo.split("\n", 1)[1]

salida = [cab.rstrip(), preambulo_sin_titulo.rstrip()]
for p in partes[1:]:
    qid = p.split("\n", 1)[0].strip()
    bloque = "## " + p.rstrip()
    if qid in estado:
        bloque += "\n\nEstado ronda-3: " + estado[qid] + "."
    salida.append(bloque)

(AQUI / "preguntas-publicador.md").write_text("\n\n".join(salida) + "\n", encoding="utf-8")
print("OK preguntas-publicador.md")
