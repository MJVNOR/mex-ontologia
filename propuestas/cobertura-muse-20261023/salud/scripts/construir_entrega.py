"""Construye entrega.json + resultado.md + pendientes.json en TU carpeta salud/.
Solo lee copias congeladas e insumos centrales (lectura). No escribe fuera de
propuestas/cobertura-muse-20261023/salud/. No ejecuta suite central."""
import json, hashlib, os
from datetime import datetime, timezone

SALUD = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/cobertura-muse-20261023/salud"
FUENTES = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/cobertura-muse-20261023/fuentes"
ROOT = "C:/Users/marti/Documents/MEX-Ontologi"
os.makedirs(SALUD, exist_ok=True)

def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

man = json.load(open(FUENTES + "/manifiesto.json", encoding="utf-8"))
frozen = FUENTES + "/agente-6-salud/propuestas.json"
audit = FUENTES + "/agente-12-auditoria-salud/auditoria.json"
assert sha_file(frozen) == next(c["sha256"] for c in man["copias"] if c["copia"].endswith("agente-6-salud/propuestas.json"))
assert sha_file(audit) == next(c["sha256"] for c in man["copias"] if c["copia"].endswith("agente-12-auditoria-salud/auditoria.json"))
for path, sha in man["insumos_centrales"].items():
    assert sha_file(ROOT + "/" + path) == sha, path

prop = json.load(open(frozen, encoding="utf-8"))
aud = json.load(open(audit, encoding="utf-8"))
assert aud["totales"] == {"decisiones": 242, "proponer_significado": 203, "pendientes": 39,
                          "aceptar": 203, "condicionado": 0, "rechazar": 0}
aceptadas = {d["regla"]: d for d in aud["dictamenes"] if d["dictamen"] == "aceptar"}
assert len(aceptadas) == 203

asig = json.load(open(ROOT + "/propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]
assert len(mine) == 242
assert sorted(v["definicion_iri"] for v in mine) == sorted(d["definicion_iri"] for d in prop["decisiones"])

sem = json.load(open(ROOT + "/ontologia/semantica.json", encoding="utf-8"))
cob = json.load(open(ROOT + "/data/semantica/cobertura.json", encoding="utf-8"))
assert len(sem["conceptos"]) == 103
assert sum(1 for v in cob["variables"] if v["estado"] == "respaldada_por_definicion") == 232
assert sum(1 for v in cob["variables"] if v["estado"] == "candidata_sin_definicion_suficiente") == 23
# preservar 23 candidatas y 232 respaldadas: sin choques de slugs ni de alcance
assert not (set(prop["conceptos_nuevos"]) & set(sem["conceptos"]))
import sys as _sys
_sys.path.insert(0, ROOT + "/scripts")
from consolidar_semantica import clave as _clave
vig = []
for r in sem["reglas_descripcion_exacta"]:
    for d in r["descripciones"]:
        vig.append((_clave(d), r.get("conjuntos"), r.get("diccionarios"), r.get("definiciones")))
for rg in prop["reglas"]:
    for d in rg["descripciones"]:
        for vd, cj, dc, df in vig:
            assert not (_clave(d) == vd and (cj is None or rg["conjuntos"][0] in cj)
                        and (dc is None or rg["diccionarios"][0] in dc)
                        and (df is None or rg["definiciones"][0] in df)), rg["id"]

CALIFICADOR = {}
LIMITE_EXTRA = {}
for d in prop["decisiones"]:
    if d["decision"] != "proponer_significado":
        continue
    iri, c = d["definicion_iri"], d["concepto_propuesto"]
    if c == "jurisdiccion-sanitaria":
        if "reside" in d["descripcion_literal"]:
            CALIFICADOR[iri] = {"rol": "residencia del caso"}
        elif "tratante" in d["descripcion_literal"]:
            CALIFICADOR[iri] = {"rol": "unidad tratante"}
        else:
            LIMITE_EXTRA[iri] = ("Jurisdicción del conjunto sin rol específico acreditado "
                                 "en la descripción; sin calificador.")
    elif c.startswith("vigilancia-total-") and c not in ("vigilancia-total-hombres", "vigilancia-total-mujeres"):
        CALIFICADOR[iri] = {"mes": c[len("vigilancia-total-"):]}
    elif c.startswith("vigilancia-personas-"):
        tramo = d["descripcion_literal"]
        for pref in ("Total de personas en vigilancia que son ", "Total de personas en vigilancia "):
            if tramo.startswith(pref):
                tramo = tramo[len(pref):]
        CALIFICADOR[iri] = {"tramo-edad": tramo}
    elif c in ("vigilancia-total-hombres", "vigilancia-total-mujeres"):
        CALIFICADOR[iri] = {"sexo": "Hombres" if c.endswith("hombres") else "Mujeres"}

FR = {"archivo": "propuestas/cobertura-muse-20261023/fuentes/agente-6-salud/propuestas.json",
      "sha256": sha_file(frozen),
      "auditoria": "propuestas/cobertura-muse-20261023/fuentes/agente-12-auditoria-salud/auditoria.json",
      "sha256_auditoria": sha_file(audit),
      "dictamen_integrador": "aceptar 203 / condicionado 0 (auditoría12 v2, 2076 checks)"}

# Auditoría-b: neutralizar sujeto caso/paciente añadido fuera del literal (10 reglas).
# Solo etiqueta/definición al significado literal; sin calificador con sujeto inferido.
NEUTRALIZAR = {
 "localidad-residencia-caso": ("localidad-residencia", "Localidad de residencia",
    "Localidad de residencia según el diccionario; conserva rol de residencia sin acreditar sujeto ni catálogo."),
 "fecha-inicio-fiebre-caso": ("fecha-inicio-fiebre", "Fecha de inicio de fiebre",
    "Fecha de inicio de fiebre según el diccionario (grafía de fuente preservada); conserva evento inicio sin acreditar sujeto."),
 "muestra-lcr-caso": ("muestra-lcr-aspecto-agua-roca", "Muestra de líquido cefalorraquídeo con aspecto de agua de roca",
    "Indicador conjunto de toma de muestra del líquido cefalorraquídeo Y aspecto de agua de roca, 1=Sí 2=No; conserva ambas condiciones literales sin reducir a mera toma, sin acreditar sujeto ni técnica."),
 "resultado-bilirrubina-directa-caso": ("resultado-bilirrubina-directa", "Resultado de bilirrubina directa",
    "Resultado numérico de bilirrubina directa según el diccionario; conserva medida sin acreditar sujeto ni unidad."),
 "resultado-bilirrubina-total-caso": ("resultado-bilirrubina-total", "Resultado total de bilirrubina",
    "Resultado numérico total de bilirrubina según el diccionario; conserva medida sin acreditar sujeto ni unidad."),
 "resultado-dhl-caso": ("resultado-dhl", "Resultados de Deshidrogenasa Láctica",
    "Resultados de Deshidrogenasa Láctica según grafía de fuente; conserva medida sin acreditar sujeto, unidad ni abreviatura."),
 "resultado-alt-caso": ("resultado-alt", "Resultados de Alanina aminotransferasa",
    "Resultados de Alanina aminotransferasa según el diccionario; conserva medida sin acreditar sujeto ni unidad."),
 "resultado-ast-caso": ("resultado-ast", "Resultados de Aspartato aminotransferasa",
    "Resultados de Aspartato aminotransferasa según el diccionario; conserva medida sin acreditar sujeto ni unidad."),
 "defuncion-caso": ("indicador-defuncion", "Defunción indicada",
    "Indicador de defunción, 1=Sí 2=No; conserva codificación sin acreditar sujeto ni causa."),
 "tratamiento-rickettsiosis-caso": ("tratamiento-rickettsiosis", "Tratamiento para rickettsiosis",
    "Indicador de tratamiento registrado para rickettsiosis, 1=Sí 2=No; conserva codificación sin acreditar sujeto."),
}
for _old, (_new, _et, _df) in NEUTRALIZAR.items():
    assert _old in prop["conceptos_nuevos"] and _new not in prop["conceptos_nuevos"] and _new not in sem["conceptos"]
    _padre = prop["conceptos_nuevos"][_old][2]
    del prop["conceptos_nuevos"][_old]
    prop["conceptos_nuevos"][_new] = [_et, _df, _padre]
    for _r in prop["reglas"]:
        if _r["concepto"] == _old:
            _r["concepto"] = _new
    for _d in prop["decisiones"]:
        if _d.get("concepto_propuesto") == _old:
            _d["concepto_propuesto"] = _new
# criterio r3a6-166 sin afirmar población
for _r in prop["reglas"]:
    if _r["id"] == "r3a6-166":
        _lit = next(_d["descripcion_literal"] for _d in prop["decisiones"] if _d.get("regla_id") == "r3a6-166")
        _r["criterio"] = ("Descripción literal %r; conserva toma de muestra y aspecto de agua de roca "
                          "sin acreditar sujeto ni técnica.") % _lit

RENOMBRADO_INV = {_new: _old for _old, (_new, _et, _df) in NEUTRALIZAR.items()}
reglas = []
for r in prop["reglas"]:
    assert r["id"] in aceptadas and aceptadas[r["id"]]["dictamen"] == "aceptar"
    assert aceptadas[r["id"]]["concepto"] in (r["concepto"], RENOMBRADO_INV.get(r["concepto"]))
    e = {"id": r["id"], "concepto": r["concepto"], "representacion": r["representacion"],
         "nombres": r["nombres"], "descripciones": r["descripciones"],
         "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"],
         "definiciones": r["definiciones"],
         "huella_fila_diccionario": next(d["huella_fila_diccionario"] for d in prop["decisiones"]
                                         if d.get("regla_id") == r["id"]),
         "limites": r["limites"], "evidencia": r["evidencia"],
         "criterio": r["criterio"], "fuente_revision": FR["archivo"],
         "sha_fuente_revision": FR["sha256"], "dictamen_auditoria": "aceptar"}
    for d in prop["decisiones"]:
        if d.get("regla_id") == r["id"] and d["definicion_iri"] in CALIFICADOR:
            e["calificador"] = CALIFICADOR[d["definicion_iri"]]
    if any(d.get("regla_id") == r["id"] and d["definicion_iri"] in LIMITE_EXTRA for d in prop["decisiones"]):
        iri0 = next(d["definicion_iri"] for d in prop["decisiones"] if d.get("regla_id") == r["id"])
        e["limites"] = list(e["limites"]) + [LIMITE_EXTRA[iri0]]
    reglas.append(e)

decisiones = []
for d in prop["decisiones"]:
    base = {"definicion_iri": d["definicion_iri"], "variable": d["variable"],
            "conjunto": d["conjunto"], "diccionario": d["diccionario"],
            "descripcion_literal": d["descripcion_literal"],
            "descripcion_raw_literal": d["descripcion_raw_literal"],
            "huella_fila_diccionario": d["huella_fila_diccionario"]}
    if d["decision"] == "proponer_significado":
        base.update({"decision": "proponer", "regla_id": d["regla_id"],
                     "concepto": d["concepto_propuesto"], "representacion": d["representacion"]})
    else:
        base.update({"decision": "pendiente", "motivo": d["razon"], "criterio": d["criterio"]})
    decisiones.append(base)

entrega = {"agente": "salud (especialista 242 definiciones, asignacion agente6)",
           "fecha_utc": datetime.now(timezone.utc).isoformat(),
           "fuente_revision": FR,
           "asignacion": {"cantidad": 242, "sha256_cobertura": asig["sha256_cobertura"]},
           "alcance": "Partición exclusiva del integrador (242 definiciones fuera del núcleo, 6 conjuntos de salud). Sin correspondencias columna-variable. Sin red; evidencia local congelada verificada contra manifiesto.",
           "limites": prop["limites"],
           "delta_v1_v2": "La auditoría antigua era 204 (v1 con 7 condicionados); esta entrega es 203 porque de01_a_04 pasó a pendiente_rango_contradictorio_nombre_descripcion (nombre sugiere 1-4, descripción dice 'entre 1 y 5 años'); sin regla y sin concepto de-1-a-4-anos. Cada una de las 203 propuestas actuales tiene sustento auditado (aceptar, auditoría12 v2).",
           "delta_auditoria_b": "10 reglas con sujeto caso/paciente añadido fuera del literal (r3a6-037/055/166/167/168/169/170/171/177/185): etiquetas y definiciones neutralizadas al significado literal (residencia, fecha inicio fiebre, toma+aspecto agua de roca, resultados declarados, defunción indicada, tratamiento registrado); slugs renombrados sin '-caso' (localidad-residencia, fecha-inicio-fiebre, muestra-lcr-aspecto-agua-roca, resultado-bilirrubina-directa/total, resultado-dhl/alt/ast, indicador-defuncion, tratamiento-rickettsiosis); concepto localidad-residencia compartido por r3a6-037/038 sin pérdida de contexto (el literal de 038 conserva sujeto). Sin calificador con sujeto inferido; evento/medida/codificación y límites intactos.",
           "conceptos_nuevos": prop["conceptos_nuevos"],
           "conceptos_reutilizados_vigentes": sorted(prop["conceptos_reutilizados"]),
           "reglas": reglas,
           "decisiones": decisiones}
entrega["conteos"] = {"decisiones": len(decisiones),
                      "proponer": sum(1 for d in decisiones if d["decision"] == "proponer"),
                      "pendientes": sum(1 for d in decisiones if d["decision"] == "pendiente"),
                      "reglas": len(reglas), "conceptos_nuevos": len(entrega["conceptos_nuevos"])}
assert entrega["conteos"] == {"decisiones": 242, "proponer": 203, "pendientes": 39,
                              "reglas": 203, "conceptos_nuevos": 178}
json.dump(entrega, open(SALUD + "/entrega.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

preg = [d for d in decisiones if d["decision"] == "pendiente"]
pendientes = {"pendientes": len(preg), "items": [
    {"definicion_iri": d["definicion_iri"], "variable": d["variable"], "motivo": d["motivo"],
     "documentacion_faltante": d["criterio"]} for d in preg]}
json.dump(pendientes, open(SALUD + "/pendientes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

md = ["# Salud — entrega cobertura Muse 20261023", "",
      "- Decisiones: 242 (partición asignada completa). Proponer: 203. Pendientes: 39.",
      "- Reglas: 203 (id, concepto, representación, listas unitarias, huella, límites, calificador cuando procede, evidencia y fuente_revision).",
      "- Conceptos nuevos: 178 (slug:[etiqueta,definicion,padre]). Reutilizados vigentes: 6.",
      "- Delta v1→v2: 204→203; de01_a_04 a pendiente por contradicción nombre/descripción; cada propuesta actual con sustento (auditoría12 v2: 203 aceptar / 0 condicionados).",
      "- Núcleo preservado sin choques: 232 respaldadas y 23 candidatas intactas (verificado por alcance restringido). Sin correspondencias columna-variable.",
      "- Delta auditoría-b: 10 etiquetas/definiciones neutralizadas al literal (sin sujeto caso/paciente inferido); slugs sin '-caso'; concepto compartido localidad-residencia (r3a6-037/038) sin pérdida de contexto.",
      "- Verificación: scripts/verificar_entrega.py. SHA en listo.json; tras listo no se modifica hasta devolución del integrador."]
open(SALUD + "/resultado.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("entrega OK:", entrega["conteos"])
