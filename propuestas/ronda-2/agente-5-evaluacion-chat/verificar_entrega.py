"""Verificador de solo lectura de la entrega agente-5 ronda 2. No llama a modelos ni escribe fuera de stdout."""
import json, pathlib
root = pathlib.Path("propuestas/ronda-2/agente-5-evaluacion-chat")
casos = json.load(open(root / "casos.json", encoding="utf-8"))
registro = json.load(open(root / "registro.json", encoding="utf-8"))
alcance = json.load(open(root / "alcance.json", encoding="utf-8"))
errores = []
ids = [c["id"] for c in casos]
if len(ids) != 20 or len(set(ids)) != 20:
    errores.append(f"casos no son 20 unicos: {len(ids)} total, {len(set(ids))} unicos")
rids = [r["id"] for r in registro]
if set(rids) != set(ids):
    errores.append("registro no cubre exactamente los 20 casos")
ej = [r for r in registro if r["estado"] in ("acierto", "fallo_recuperacion_contexto_parcial")]
noej = [r for r in registro if r["estado"].startswith("no_ejecutado")]
ac = [r for r in registro if r["estado"] == "acierto"]
fa = [r for r in registro if r["estado"].startswith("fallo")]
for r in registro:
    md = root / "respuestas_brutas" / (r["id"] + ".md")
    ctx = root / "respuestas_brutas" / (r["id"] + ".contexto.txt")
    if not md.exists():
        errores.append(f"falta {md}")
    if not ctx.exists():
        errores.append(f"falta {ctx}")
    if r["estado"] in ("acierto", "fallo_recuperacion_contexto_parcial") and not r.get("obtenida"):
        errores.append(f"{r['id']}: ejecutado sin obtenida")
    if r["estado"].startswith("no_ejecutado") and r.get("obtenida"):
        errores.append(f"{r['id']}: no_ejecutado con obtenida inventada")
    if "ONTO_LLM_API_KEY" in json.dumps(r) or "AIza" in json.dumps(r):
        errores.append(f"{r['id']}: posible secreto en registro")
sparql = list((root / "fuentes" / "sparql").glob("*.rq"))
if len(sparql) < 20:
    errores.append(f"pocas consultas sparql: {len(sparql)}")
for rq in [q for q in sparql if q.name != "_meta.json"]:
    js = rq.with_suffix(".json")
    if not js.exists():
        errores.append(f"falta respuesta bruta {js.name}")
        continue
    try:
        d = json.load(open(js, encoding="utf-8"))
    except Exception as e:
        errores.append(f"{js.name} no es JSON: {e}")
        continue
    if not isinstance(d, dict) or ("results" not in d and "error" not in d):
        errores.append(f"{js.name} sin results ni error")
if alcance.get("identidad_backend", "").upper().startswith("NO") is False:
    errores.append("alcance no declara identidad NO demostrada")
if alcance.get("configuracion_efectiva_ui") != "NO comprobada":
    errores.append("alcance no declara coincidencia UI NO comprobada")
print(json.dumps({"casos": len(casos), "ejecutados_pipeline": len(ej), "aciertos": len(ac), "fallos": len(fa), "no_ejecutados": len(noej), "errores": errores}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errores else 0)
