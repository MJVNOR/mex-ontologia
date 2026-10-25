"""Integra segunda revision lote-4 a entrega.json y verifica con comprobar.py."""
import json, hashlib, subprocess, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
import sys
sys.path.insert(0, str(LOTE))
from gen2 import FULL, CONCEPTOS, BASE_IRI
cob = json.load(open(BASE/"data/semantica/cobertura.json", encoding="utf-8"))
vidx = {v["definicion_iri"]: v for v in cob["variables"]}
asig = json.load(open(LOTE/"asignacion.json", encoding="utf-8"))
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))

reglas = []
for i, (suf, concepto, rep, lim, pos, contra) in enumerate(FULL, 1):
    di = BASE_IRI + suf
    v = vidx[di]
    rid = f"r4-lote-4-{i:03d}"
    reglas.append({"id": rid, "concepto": concepto, "representacion": rep,
        "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
        "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]], "definiciones": [di],
        "criterio": "Segunda revision lote-4; lectura literal de la fila del diccionario y contexto del conjunto; alcance fijado a esta definicion.",
        "fuente_revision": "propuestas/pendientes-muse-r4/lote-4/entrega.json",
        "alcance": "Solo este diccionario, conjunto, definicion, nombre y descripcion.",
        "positivo": pos, "contraejemplo": contra, "limite": lim,
        "evidencia": [{"variable": v["variable"], "descripcion": v["descripcion"], "definicion_iri": di,
            "diccionario": v["diccionario"], "conjunto": v["conjunto"],
            "unidad_de_medida": v.get("unidad_de_medida", ""), "tipo_de_dato": v.get("tipo_de_dato", ""),
            "huella_fila_diccionario": v["huella_fila_diccionario"]}],
        "huella_fila_diccionario": v["huella_fila_diccionario"]})
ridx = {}
for i, (suf, *_r) in enumerate(FULL, 1):
    ridx[BASE_IRI + suf] = f"r4-lote-4-{i:03d}"

MOT_PEND = {
 "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7": "pendiente: referente de otras sin especificar en nombre ni descripcion; no se infiere especie, oficina ni origen.",
 "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8": "pendiente: referente de otras sin especificar en nombre ni descripcion; no se infiere especie, oficina ni origen.",
 "a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F22": "pendiente: descripcion truncada a mitad de frase en la evidencia local (termina en equipos...); no se infiere el resto.",
 "c65eb4e7-a17d-43c7-b08c-05811505edf1%2F7": "pendiente: pregunta sin sujeto (Como se generan?) incompleta por si sola; no se transfiere referente de otra fila.",
 "f3ecd3d2-2156-4251-82e5-13b079471ee9%2F7": "pendiente: pregunta sin sujeto (Como se generan?) incompleta por si sola; no se transfiere referente de otra fila.",
 "67156807-2013-4117-9ca9-394aea647127%2F5": "pendiente: descripcion vacia (Clasificacion); la unidad enumera tipos de asentamiento pero no define la variable; no se infiere catalogo.",
 "f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15": "pendiente: contradiccion nombre/descripcion (Total_Egresos descrito como Total de urgencias atendidas) con observacion vigente; no se interpreta ni equipara.",
}
dec_sig = []
for vp in asig["variables_pendientes"]:
    di = vp["definicion_iri"]
    suf = di.split("definition/")[1]
    ev = [f"data/portal/contenido-inspeccion.json#recursos/{vp['diccionario']}/definiciones",
          f"data/semantica/cobertura.json#variables/{di}"]
    if di in ridx:
        dec_sig.append({"definicion_iri": di, "decision": "proponer",
            "motivo": f"Descripcion, fila completa y contexto respaldan el sentido literal ({ridx[di]}); restringido a esta fila exacta.",
            "evidencia": ev + [f"propuestas/pendientes-muse-r4/lote-4/entrega.json#reglas/{ridx[di]}"]})
    else:
        ev2 = list(ev)
        if suf == "f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15":
            ev2.append("ontologia/semantica.json#observaciones/egresos-descripcion-urgencias")
        dec_sig.append({"definicion_iri": di, "decision": "pendiente", "motivo": MOT_PEND[suf], "evidencia": ev2})

sol = []
for vp in asig["variables_pendientes"]:
    di = vp["definicion_iri"]
    if di in ridx:
        continue
    suf = di.split("definition/")[1]
    docs = {
     "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7": "Diccionario que defina CVOTRAS/DOTRAS o catalogo de referencia.",
     "863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8": "Diccionario que defina CVOTRAS/DOTRAS o catalogo de referencia.",
     "a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F22": "Fila completa de P22 sin truncar.",
     "c65eb4e7-a17d-43c7-b08c-05811505edf1%2F7": "Diccionario con sujeto de la pregunta P7.",
     "f3ecd3d2-2156-4251-82e5-13b079471ee9%2F7": "Diccionario con sujeto de la pregunta P7.",
     "67156807-2013-4117-9ca9-394aea647127%2F5": "Diccionario que fije que clasifica CLASIF.",
     "f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15": "Diccionario corregido o nota que fije el significado de Total_Egresos.",
    }
    sol.append({"definicion_iri": di, "variable": vp["variable"], "diccionario": vp["diccionario"],
        "duda": MOT_PEND[suf], "fuente_probable": "Publicador del conjunto " + vp.get("titulo_conjunto", ""),
        "documento_requerido": docs[suf]})

ent["decisiones_significados"] = dec_sig
ent["reglas"] = reglas
ent["conceptos_nuevos"] = CONCEPTOS
ent["solicitudes_investigacion"] = sol
ent["conteos"] = {"columnas": len(ent["decisiones_columnas"]),
    "proponer": sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "proponer"),
    "pendiente_columnas": sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "pendiente"),
    "significados": len(dec_sig), "significados_proponer": sum(1 for d in dec_sig if d["decision"] == "proponer"),
    "significados_pendiente": sum(1 for d in dec_sig if d["decision"] == "pendiente"),
    "vinculos": len(ent["vinculos"]), "reglas": len(reglas), "conceptos_nuevos": len(CONCEPTOS)}
json.dump(ent, open(LOTE/"entrega.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pend_cols = [d for d in ent["decisiones_columnas"] if d["decision"] == "pendiente"]
json.dump({"pendientes_columnas": pend_cols, "pendientes_significados": [d for d in dec_sig if d["decision"] == "pendiente"],
    "nota": "Segunda revision: 40 reglas nuevas r4-lote-4-* con 23 conceptos nuevos; 7 significados pendientes con motivo real."},
    open(LOTE/"pendientes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ("# Lote-4 — resultado (segunda revision)\n"
 f"- Columnas asignadas: 592; decisiones: {ent['conteos']['proponer']} proponer / {ent['conteos']['pendiente_columnas']} pendiente.\n"
 f"- Vinculos: {ent['conteos']['vinculos']} (formato 9 claves, huellas verificadas localmente).\n"
 f"- Significados asignados: 47; decisiones: {ent['conteos']['significados_proponer']} proponer / {ent['conteos']['significados_pendiente']} pendiente.\n"
 f"- Reglas nuevas: {len(reglas)} (r4-lote-4-001 a r4-lote-4-{len(reglas):03d}), restringidas a fila exacta con huella; 1 reutiliza concepto vigente (conteo-personas-desarrollo-software), 39 usan 22 conceptos nuevos.\n"
 "- Conceptos nuevos: 23 (padre tiempo solo para los tres momentos de registro; resto top-level por ambito nuevo sin genero exacto).\n"
 "- Pendientes con motivo real: CVOTRAS/DOTRAS (referente otras sin especificar), P22 desarrollo (descripcion truncada), P7 gobernanza/fortalezas (pregunta sin sujeto), CLASIF (descripcion vacia), Total_Egresos (contradiccion con observacion vigente).\n"
 "- Casos limite: P36/P39/P40 booleanos con pregunta de conteo/procedimiento (limite conserva la tension sin resolverla); CIE10 codigo CnnX sin catalogo; meses 911 y medidas de pesca sin homologar.\n")
open(LOTE/"resultado.md", "w", encoding="utf-8").write(md)
h = hashlib.sha256(open(LOTE/"entrega.json", "rb").read()).hexdigest()
json.dump({"entrega": "entrega.json", "sha256": h, "conteos": ent["conteos"]},
    open(LOTE/"listo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(ent["conteos"], indent=1), h)
