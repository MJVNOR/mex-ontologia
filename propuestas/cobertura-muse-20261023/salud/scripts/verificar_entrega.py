"""Verificador independiente de la entrega salud (solo lectura fuera de TU carpeta)."""
import json, hashlib, sys

SALUD = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/cobertura-muse-20261023/salud"
FUENTES = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/cobertura-muse-20261023/fuentes"
ROOT = "C:/Users/marti/Documents/MEX-Ontologi"
sys.dont_write_bytecode = True

ok = []
def check(nombre, cond):
    assert cond, "FALLA: " + nombre
    ok.append(nombre)

def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

ent = json.load(open(SALUD + "/entrega.json", encoding="utf-8"))
man = json.load(open(FUENTES + "/manifiesto.json", encoding="utf-8"))
frozen = json.load(open(FUENTES + "/agente-6-salud/propuestas.json", encoding="utf-8"))
aud = json.load(open(FUENTES + "/agente-12-auditoria-salud/auditoria.json", encoding="utf-8"))
asig = json.load(open(ROOT + "/propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
sem = json.load(open(ROOT + "/ontologia/semantica.json", encoding="utf-8"))
cob = json.load(open(ROOT + "/data/semantica/cobertura.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]

# insumos congelados intactos
for c in man["copias"]:
    check("frozen_" + c["copia"].split("/")[-2], sha_file(ROOT + "/" + c["copia"]) == c["sha256"])
for path, sha in man["insumos_centrales"].items():
    check("insumo_" + path.split("/")[-1], sha_file(ROOT + "/" + path) == sha)

# partición completa
check("particion_242", len(ent["decisiones"]) == 242 == len(mine))
check("iris_exactas", sorted(d["definicion_iri"] for d in ent["decisiones"]) == sorted(v["definicion_iri"] for v in mine))
check("sin_duplicados", len({d["definicion_iri"] for d in ent["decisiones"]}) == 242)

# decisiones↔reglas
por_regla = {}
for d in ent["decisiones"]:
    check("decision_valida_" + d["variable"][:14], d["decision"] in ("proponer", "pendiente"))
    if d["decision"] == "proponer":
        check("regla_id_" + d["variable"][:14], "regla_id" in d and "motivo" not in d)
        por_regla.setdefault(d["regla_id"], []).append(d["definicion_iri"])
    else:
        check("motivo_" + d["variable"][:14], "motivo" in d and "regla_id" not in d)
check("reglas_203", len(ent["reglas"]) == 203)
for r in ent["reglas"]:
    check("regla_forma_" + r["id"], r["id"].startswith("r3a6-")
          and len(r["nombres"]) == len(r["descripciones"]) == len(r["conjuntos"])
          == len(r["diccionarios"]) == len(r["definiciones"]) == 1
          and r["representacion"] in {"codigo", "nombre", "fecha", "anio", "mes", "dia", "hora", "no_especificada"})
    check("regla_evidencia_" + r["id"], all(k in r["evidencia"] for k in ("tipo", "formato", "unidad", "ejemplo"))
          and r["fuente_revision"] == ent["fuente_revision"]["archivo"]
          and r["sha_fuente_revision"] == ent["fuente_revision"]["sha256"]
          and r.get("dictamen_auditoria") == "aceptar" and len(r["limites"]) >= 1)
    check("regla_decision_" + r["id"], por_regla.get(r["id"], []) == r["definiciones"])
    fd = next(d for d in frozen["decisiones"] if d.get("regla_id") == r["id"])
    _fd_concepto = {"localidad-residencia": "localidad-residencia-caso", "fecha-inicio-fiebre": "fecha-inicio-fiebre-caso",
        "muestra-lcr-aspecto-agua-roca": "muestra-lcr-caso", "resultado-bilirrubina-directa": "resultado-bilirrubina-directa-caso",
        "resultado-bilirrubina-total": "resultado-bilirrubina-total-caso", "resultado-dhl": "resultado-dhl-caso",
        "resultado-alt": "resultado-alt-caso", "resultado-ast": "resultado-ast-caso",
        "indicador-defuncion": "defuncion-caso", "tratamiento-rickettsiosis": "tratamiento-rickettsiosis-caso"}.get(r["concepto"], r["concepto"])
    check("regla_huella_" + r["id"], r["huella_fila_diccionario"] == fd["huella_fila_diccionario"]
          and _fd_concepto == fd["concepto_propuesto"] and r["descripciones"] == [fd["descripcion_literal"]]
          and r["definiciones"] == [fd["definicion_iri"]])

# conceptos
check("nuevos_178", len(ent["conceptos_nuevos"]) == 178)
for slug, v in ent["conceptos_nuevos"].items():
    check("nuevo_forma_" + slug[:30], isinstance(v, list) and len(v) == 3
          and (v[2] is None or v[2] in sem["conceptos"] or v[2] in ent["conceptos_nuevos"]))
    check("nuevo_sin_choque_" + slug[:30], slug not in sem["conceptos"])
    check("nuevo_usado_" + slug[:30], any(r["concepto"] == slug for r in ent["reglas"]))
check("reutilizados_6", set(ent["conceptos_reutilizados_vigentes"]) == {"entidad", "municipio-residencia", "municipio-ubicacion", "organizacion", "sexo-declarado", "unidad-salud"})

# núcleo preservado: 232 respaldadas + 23 candidatas, sin choques de alcance
check("respaldadas_232", sum(1 for v in cob["variables"] if v["estado"] == "respaldada_por_definicion") == 232)
check("candidatas_23", sum(1 for v in cob["variables"] if v["estado"] == "candidata_sin_definicion_suficiente") == 23)
sys.path.insert(0, ROOT + "/scripts")
from consolidar_semantica import clave as _clave, validar_calificador
vig = [(_clave(d), r.get("conjuntos"), r.get("diccionarios"), r.get("definiciones"))
       for r in sem["reglas_descripcion_exacta"] for d in r["descripciones"]]
for r in ent["reglas"]:
    for vd, cj, dc, df in vig:
        check("sin_choque_" + r["id"], not (_clave(r["descripciones"][0]) == vd
              and (cj is None or r["conjuntos"][0] in cj) and (dc is None or r["diccionarios"][0] in dc)
              and (df is None or r["definiciones"][0] in df)))

# conteos recalculados desde contenido + sin correspondencias
check("conteos", ent["conteos"] == {"decisiones": len(ent["decisiones"]),
      "proponer": sum(1 for d in ent["decisiones"] if d["decision"] == "proponer"),
      "pendientes": sum(1 for d in ent["decisiones"] if d["decision"] == "pendiente"),
      "reglas": len(ent["reglas"]), "conceptos_nuevos": len(ent["conceptos_nuevos"])})
check("sin_correspondencias", "correspondencias" not in ent)
pend = json.load(open(SALUD + "/pendientes.json", encoding="utf-8"))
check("pendientes_39", pend["pendientes"] == 39 == len(pend["items"])
      == sum(1 for d in ent["decisiones"] if d["decision"] == "pendiente"))

# auditoría-b: 10 conceptos neutralizados al literal, sin sujeto inferido
import re as _re
_SUJ = _re.compile(r"\b(caso|paciente)\b")
_NEUTROS = {"localidad-residencia": 2, "fecha-inicio-fiebre": 1, "muestra-lcr-aspecto-agua-roca": 1,
    "resultado-bilirrubina-directa": 1, "resultado-bilirrubina-total": 1, "resultado-dhl": 1,
    "resultado-alt": 1, "resultado-ast": 1, "indicador-defuncion": 1, "tratamiento-rickettsiosis": 1}
for slug, uso in _NEUTROS.items():
    check("neutro_existe_" + slug, slug in ent["conceptos_nuevos"])
    _et, _df, _pa = ent["conceptos_nuevos"][slug]
    check("neutro_sin_sujeto_" + slug, not _SUJ.search(_et.lower()) and not _SUJ.search(_df.lower()))
    check("neutro_slug_sin_caso_" + slug, "caso" not in slug and "paciente" not in slug)
    check("neutro_uso_" + slug, sum(1 for r in ent["reglas"] if r["concepto"] == slug) == uso)
check("neutro_sin_calificador_sujeto",
      all("calificador" not in r for r in ent["reglas"]
          if r["concepto"] in _NEUTROS or r["id"] in ("r3a6-037", "r3a6-038", "r3a6-055", "r3a6-166")))
for _rid in ("r3a6-037", "r3a6-055", "r3a6-166", "r3a6-167", "r3a6-168", "r3a6-169", "r3a6-170", "r3a6-171", "r3a6-177", "r3a6-185"):
    _r = next(r for r in ent["reglas"] if r["id"] == _rid)
    check("neutro_criterio_" + _rid, not _SUJ.search(_r["criterio"].lower()))
    check("neutro_concepto_esperado_" + _rid, _r["concepto"] in _NEUTROS)
# negativos: solo-nombre / contexto mutado / otra IRI no activan reglas nuevas
# calificadores: dict no vacío str->str validado con soporte central real
n_cal = 0
for r in ent["reglas"]:
    if "calificador" in r:
        n_cal += 1
        check("calificador_dict_" + r["id"], validar_calificador(r["calificador"]) == r["calificador"])
        check("calificador_sin_invento_" + r["id"],
              all(v in (r["descripciones"][0] + " " + r["nombres"][0] + " " + r["evidencia"].get("ejemplo", ""))
                  or k in ("mes", "tramo-edad", "sexo", "rol") for k, v in r["calificador"].items()))
    if r["concepto"] == "jurisdiccion-sanitaria" and "calificador" not in r:
        check("jurisdiccion_sin_rol_a_limite_" + r["id"],
              any("sin rol específico" in l for l in r["limites"]))
check("calificadores_26", n_cal == 26)
sys.path.insert(0, ROOT + "/scripts")
from consolidar_semantica import interpretacion
rules = {"reglas_descripcion_exacta": sem["reglas_descripcion_exacta"] + [
    {k: v for k, v in {"id": r["id"], "concepto": r["concepto"], "descripciones": r["descripciones"], "nombres": r["nombres"],
     "conjuntos": r["conjuntos"], "diccionarios": r["diccionarios"], "definiciones": r["definiciones"],
     "representacion": r["representacion"], "calificador": r.get("calificador")}.items() if v is not None}
    for r in ent["reglas"]]}
base = ("5494daa1-09ca-4750-aeac-2558553700e1", "33d0a99e-c721-496f-a05e-07646e9ae42a",
        "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F28")
for nombre, (desc, conj, dicc, defi) in {
    "solo_nombre": ("",) + base, "contexto_mutado": ("El paciente presenta Cefalea 1=Si 2=No", "OTRO", base[1], base[2]),
    "otra_iri": ("El paciente presenta Cefalea 1=Si 2=No", base[0], base[1], base[2].replace("%2F28", "%2F9999")),
    "a04_promovido": ("Total de personas en vigilancia entre 1 y 5 años", "dca16d84-dbf0-4501-b702-dc6372a480ea",
                       "2334deaa-dd0c-444e-b038-4cc556ad715d", "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F13"),
}.items():
    n = "cefalea" if nombre != "a04_promovido" else "de01_a_04"
    r = interpretacion(n, desc, conj, rules, dicc, defi)
    check("neg_" + nombre, not str(r.get("regla", "")).startswith("r3a6-"))
# positivo real con calificador propagado por interpretacion central
r = interpretacion("des_jur_res", "Jurisdicción donde reside el caso",
                   "5494daa1-09ca-4750-aeac-2558553700e1", rules,
                   "33d0a99e-c721-496f-a05e-07646e9ae42a",
                   "https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F6")
check("pos_calificador_propagado", r.get("calificador") == {"rol": "residencia del caso"})
r = interpretacion("enero", "Vigilancias totales en enero",
                   "dca16d84-dbf0-4501-b702-dc6372a480ea", rules,
                   "2334deaa-dd0c-444e-b038-4cc556ad715d",
                   "https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F45")
check("pos_calificador_mes", r.get("calificador") == {"mes": "enero"})

print("verificador_entrega OK: %d comprobaciones" % len(ok))
