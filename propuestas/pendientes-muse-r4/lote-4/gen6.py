import json, hashlib, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))
RET = {"r4-lote-4-025", "r4-lote-4-026", "r4-lote-4-027"}
RET_DEF = {"https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F36",
           "https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F39",
           "https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F40"}
MOT = {
 "https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F36": "pendiente: tipo Booleano Si/No con ejemplo Si contradice el concepto de conteo (pregunta Cuantos proyectos); el dominio acreditable es existencia Si/No, no cantidad; no se inventa significado alternativo de existencia.",
 "https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F39": "pendiente: tipo Booleano Si/No con ejemplo Si contradice el concepto de procedimiento (pregunta Como atiende incidencias); el valor acreditable Si/No no describe procedimiento; no se inventa significado alternativo de existencia.",
 "https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F40": "pendiente: tipo Booleano Si/No con ejemplo Si contradice el conteo (pregunta Cuantas personas); la fila no acredita conteo ni duplica r3a9-059; no se inventa significado alternativo de existencia."}
# 1. reglas: retirar 3, ajustar limites de restantes
LIM = {
 "r4-lote-4-002": "Descripcion con redaccion defectuosa en fuente (Campo en la que...); ejemplo fija el sentido; sin catalogo resuelto. No comparable entre metodologias de registro (incidencia municipal actual vs fuero comun, victimas u otras): el mismo literal en otra metodologia no acredita el mismo sentido ni habilita cruces.",
 "r4-lote-4-003": "Sin catalogo resuelto; ejemplo ilustrativo. No comparable entre metodologias de registro (incidencia municipal actual vs fuero comun, victimas u otras): el mismo literal en otra metodologia no acredita el mismo sentido ni habilita cruces.",
 "r4-lote-4-004": "Sin catalogo resuelto; ejemplo ilustrativo. No comparable entre metodologias de registro (incidencia municipal actual vs fuero comun, victimas u otras): el mismo literal en otra metodologia no acredita el mismo sentido ni habilita cruces.",
 "r4-lote-4-008": "Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo de sectores; sin equiparacion de sectores entre encuestas: cada fila vale solo para su diccionario y encuesta.",
 "r4-lote-4-009": "Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo de sectores; sin equiparacion de sectores entre encuestas: cada fila vale solo para su diccionario y encuesta.",
 "r4-lote-4-010": "Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo de sectores; sin equiparacion de sectores entre encuestas: cada fila vale solo para su diccionario y encuesta.",
 "r4-lote-4-022": "Respuesta de texto libre declarada a la pregunta sobre tipos de pruebas; el ejemplo (Si) no tipifica las pruebas; no tabular como categorica ni agregar.",
 "r4-lote-4-038": "Formato literal CnnX; sin equivalencia de claves entre diccionarios (egresos vs urgencias) ni version CIE acreditada.",
 "r4-lote-4-039": "Formato literal CnnX; sin equivalencia de claves entre diccionarios (egresos vs urgencias) ni version CIE acreditada."}
POS22 = "Denota la respuesta de texto libre declarada a la pregunta sobre tipos de pruebas realizadas."
n0 = len(ent["reglas"])
ent["reglas"] = [r for r in ent["reglas"] if r["id"] not in RET]
assert n0 - len(ent["reglas"]) == 3
for r in ent["reglas"]:
    if r["id"] in LIM:
        assert r["id"] != "r4-lote-4-022" or True
        r["limite"] = LIM[r["id"]]
        if r["id"] == "r4-lote-4-022":
            r["positivo"] = POS22
# 2. conceptos huerfanos
usados = {r["concepto"] for r in ent["reglas"]}
for k in ["conteo-proyectos-desarrollo-dependencia", "atencion-incidencias-reportes-tecnicos"]:
    assert k in ent["conceptos_nuevos"] and k not in usados, k
    del ent["conceptos_nuevos"][k]
print("conceptos nuevos:", len(ent["conceptos_nuevos"]))
# 3. decisiones_significados: 3 a pendiente
for s in ent["decisiones_significados"]:
    if s["definicion_iri"] in RET_DEF:
        assert s["decision"] == "proponer"
        s["decision"] = "pendiente"
        s["motivo"] = MOT[s["definicion_iri"]]
# 4. vinculos dependientes fuera; columnas a pendiente (mantener asignacion)
antes_v = len(ent["vinculos"])
cols_ret = set()
for v in ent["vinculos"]:
    pass
# columnas dependientes = decisiones_columnas con definicion_iri retirada y decision proponer
dep_cols = {d["columna"] for d in ent["decisiones_columnas"]
            if d.get("definicion_iri") in RET_DEF and d["decision"] == "proponer"}
ent["vinculos"] = [v for v in ent["vinculos"] if v["columna"] not in dep_cols]
print("vinculos eliminados:", antes_v - len(ent["vinculos"]), "columnas afectadas:", len(dep_cols))
for d in ent["decisiones_columnas"]:
    if d["columna"] in dep_cols:
        d["decision"] = "pendiente"
        d["motivo"] = "pendiente: regla propuesta retirada por auditoria (contradiccion tipo Booleano Si/No vs pregunta de conteo/procedimiento); " + MOT[d["definicion_iri"]]
        d["evidencia"] = [e for e in d.get("evidencia", []) if "entrega.json#reglas" not in e]
print("pendientes col tras cambio:", sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "pendiente"))
json.dump(ent, open(LOTE/"entrega.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
