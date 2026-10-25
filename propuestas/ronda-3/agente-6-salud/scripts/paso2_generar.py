"""Agente-6 ronda-3: genera propuestas.json + resultado.md desde evidencia local.

Lee: asignacion del integrador, cobertura, inspeccion, inventario,
ontologia/semantica. Escribe solo dentro de propuestas/ronda-3/agente-6-salud/.
"""
import json, hashlib, re
from datetime import datetime, timezone

A6 = "C:/Users/marti/Documents/MEX-Ontologi/propuestas/ronda-3/agente-6-salud"
ROOT = "C:/Users/marti/Documents/MEX-Ontologi"

def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()

asig = json.load(open(ROOT + "/propuestas/ronda-3/integrador/asignaciones-semanticas.json", encoding="utf-8"))
mine = asig["asignaciones"]["6"]["variables"]
insp = json.load(open(ROOT + "/data/portal/contenido-inspeccion.json", encoding="utf-8"))
inv = json.load(open(ROOT + "/data/portal/inventario.json", encoding="utf-8"))
sem = json.load(open(ROOT + "/ontologia/semantica.json", encoding="utf-8"))
cob = json.load(open(ROOT + "/data/semantica/cobertura.json", encoding="utf-8"))
byid = {r["id"]: r for r in insp["recursos"]}

assert cob["resumen"]["conceptos_compartidos"] == 103 == len(sem["conceptos"])
assert sum(1 for v in cob["variables"] if v["estado"] == "respaldada_por_definicion") == 232
assert cob["resumen"]["estados_correspondencias"]["documental_revisada"] == 836
assert cob["resumen"]["estados_correspondencias"]["candidata_por_nombre"] == 118
assert len(sem["reglas_descripcion_exacta"]) == 116

CENT = {"cobertura.json": ROOT + "/data/semantica/cobertura.json",
        "contenido-inspeccion.json": ROOT + "/data/portal/contenido-inspeccion.json",
        "inventario.json": ROOT + "/data/portal/inventario.json",
        "semantica.json": ROOT + "/ontologia/semantica.json",
        "asignaciones-semanticas.json": ROOT + "/propuestas/ronda-3/integrador/asignaciones-semanticas.json"}
huellas_entrada = {k: sha_file(p) for k, p in CENT.items()}
assert huellas_entrada["cobertura.json"] == asig["sha256_cobertura"]
assert asig["alcance"].startswith("Particion exclusiva")
assert asig["asignaciones"]["6"]["cantidad"] == len(mine) == 242

VIG = "dca16d84-dbf0-4501-b702-dc6372a480ea"
RIK = "5494daa1-09ca-4750-aeac-2558553700e1"

SLUG = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().replace("ñ", "n").replace("ó", "o")
                        .replace("é", "e").replace("í", "i").replace("á", "a").replace("ú", "u")
                        .replace("ü", "u")).strip("-")

import sys as _sys
_sys.path.insert(0, ROOT + "/scripts")
from consolidar_semantica import clave as _clave

def descripcion_raw(row):
    for k in row:
        if _clave(k) == "descripcion":
            return row[k]
    return ""

decisiones, reglas, nuevos, reutilizados = [], [], {}, {}
N = [0]
def rid():
    N[0] += 1
    return "r3a6-%03d" % N[0]

def concepto_nuevo(slug, label, definicion, broader=None):
    if slug not in nuevos:
        nuevos[slug] = [label, definicion, broader]
    return slug

def base_dec(v, row):
    return {"definicion_iri": v["definicion_iri"], "conjunto": v["conjunto"],
            "titulo_conjunto": v["titulo_conjunto"], "diccionario": v["diccionario"],
            "variable": v["variable"], "descripcion_literal": v["descripcion"],
            "descripcion_raw_literal": descripcion_raw(row),
            "raw_difiere_de_central_trim": descripcion_raw(row) != v["descripcion"],
            "tipo_literal": row.get("Tipo de dato", ""), "formato_literal": row.get("Formato", ""),
            "unidad_literal": row.get("Unidad de medida", ""),
            "ejemplo_literal": row.get("Ejemplo de dato", ""),
            "catalogo_literal": v.get("catalogo_declarado", "") or row.get("Catálogo de referencia", ""),
            "detalle_catalogo_literal": row.get("Detalle de relación con catálogos", ""),
            "huella_fila_diccionario": v["huella_fila_diccionario"]}

def proponer(v, row, concepto, rep, criterio, limites, reutilizado=False):
    reg = rid()
    d = base_dec(v, row)
    d.update({"decision": "proponer_significado", "concepto_propuesto": concepto,
              "representacion": rep, "regla_id": reg, "criterio": criterio,
              "limites": limites, "reutiliza_concepto_vigente": reutilizado})
    decisiones.append(d)
    reglas.append({"id": reg, "concepto": concepto, "descripciones": [v["descripcion"]],
                   "nombres": [v["variable"]], "conjuntos": [v["conjunto"]],
                   "diccionarios": [v["diccionario"]], "definiciones": [v["definicion_iri"]],
                   "representacion": rep, "criterio": criterio, "evidencia": {
                       "tipo": row.get("Tipo de dato", ""), "formato": row.get("Formato", ""),
                       "unidad": row.get("Unidad de medida", ""), "ejemplo": row.get("Ejemplo de dato", ""),
                       "catalogo_declarado": v.get("catalogo_declarado", "")},
                   "limites": limites})
    return reg

def pendiente(v, row, razon, criterio):
    d = base_dec(v, row)
    d.update({"decision": "pendiente", "razon": razon, "criterio": criterio})
    decisiones.append(d)

def reuse(cid, motivo):
    label, definicion, broader = sem["conceptos"][cid]
    if cid in reutilizados and motivo not in reutilizados[cid]["motivo"]:
        reutilizados[cid]["motivo"] += " | " + motivo
    else:
        reutilizados[cid] = {"label": label, "definicion": definicion, "broader": broader, "motivo": motivo}

LIM_NOCAT = ["Sin acreditar catálogo oficial, vigencia, identidad ni equivalencia externa."]
LIM_FLAG = ["Bandera de registro del diccionario, no diagnóstico confirmado; sin CIE, catálogo ni identidad."]

# ---------- conceptos nuevos fijos ----------
concepto_nuevo("jurisdiccion-sanitaria", "Jurisdicción sanitaria",
    "Jurisdicción de salud de Sonora según diccionarios de vigilancia y atención (ejemplos Hermosillo, Navojoa, Santa Ana); conserva conjunto, representación y rol sin acreditar catálogo oficial ni vigencia.", None)
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
for m in MESES:
    concepto_nuevo("vigilancia-total-%s" % m, "Vigilancias totales en %s" % m,
        "Total de vigilancias del conjunto Vigilancia Epidemiológica correspondiente al mes de %s según el diccionario; conserva mes sin acreditar año ni regla de agregación." % m, None)
EDADES = [("menores-1-ano", "menores de 1 año"), ("de-5-a-9-anos", "entre 5 y 9 años"),
          ("de-10-a-14-anos", "entre 10 y 14 años"), ("de-15-a-19-anos", "entre 15 y 19 años"), ("de-20-a-24-anos", "entre 20 y 24 años"),
          ("de-25-a-44-anos", "entre 25 y 44 años"), ("de-45-a-49-anos", "entre 45 y 49 años"), ("de-50-a-59-anos", "entre 50 y 59 años"),
          ("de-60-a-64-anos", "entre 60 y 64 años"), ("de-65-y-mas-anos", "de 65 años o más")]
for slug, tramo in EDADES:
    concepto_nuevo("vigilancia-personas-%s" % slug, "Personas en vigilancia %s" % tramo,
        "Total de personas en vigilancia %s según el diccionario de Vigilancia Epidemiológica; conserva población y tramo de edad sin acreditar año ni regla de agregación." % tramo, "grupo-edad")
concepto_nuevo("vigilancia-total-hombres", "Total acumulado de Hombres",
    "Total acumulado de hombres en vigilancia epidemiológica según el diccionario; conserva categorías literales sin homologar.", None)
concepto_nuevo("vigilancia-total-mujeres", "Total acumulado de Mujeres",
    "Total acumulado de mujeres en vigilancia epidemiológica según el diccionario; conserva categorías literales sin homologar.", None)
concepto_nuevo("diagnostico-vigilancia", "Diagnóstico en vigilancia epidemiológica",
    "Diagnóstico declarado en el diccionario de Vigilancia Epidemiológica (clave numérica y descripción textual); conserva representación sin acreditar CIE ni catálogo.", None)
concepto_nuevo("diagnostico-declarado-atencion", "Diagnóstico declarado en atención",
    "Descripción de diagnóstico declarada en diccionarios de atención de urgencias y egresos hospitalarios; texto declarado sin acreditar CIE ni catálogo.", None)
concepto_nuevo("total-urgencias-atendidas", "Total de urgencias atendidas",
    "Total de urgencias atendidas en atención de urgencias según el diccionario; conserva conteo sin acreditar periodo ni regla de agregación.", None)
concepto_nuevo("localidad-residencia-caso", "Localidad de residencia del caso",
    "Localidad donde reside el caso en estudio de fiebre manchada; conserva población y rol de residencia sin acreditar catálogo.", "localidad")
concepto_nuevo("edad-paciente-anos", "Edad del paciente en años",
    "Edad en años del paciente en estudio de fiebre manchada; conserva población y unidad años.", None)
concepto_nuevo("tipo-calle-residencia-caso", "Tipo de calle de residencia del caso",
    "Tipo de calle donde reside el caso en estudio de fiebre manchada; conserva rol de residencia.", None)
concepto_nuevo("colonia-residencia-caso", "Colonia de residencia del caso",
    "Colonia donde reside el caso en estudio de fiebre manchada; conserva rol de residencia sin acreditar catálogo.", None)
concepto_nuevo("codigo-postal-residencia-caso", "Código postal de residencia del caso",
    "Código postal donde reside el caso en estudio de fiebre manchada; conserva rol de residencia sin acreditar catálogo postal.", None)
concepto_nuevo("condicion-indigena-caso", "Condición indígena del caso",
    "Indicador de si el paciente es indígena, 1=Sí 2=No; conserva codificación sin homologar y sin acreditar pertenencia étnica ni catálogo.", None)
concepto_nuevo("habla-lengua-indigena-caso", "Habla de lengua indígena del caso",
    "Indicador de si el paciente habla lengua indígena, 1=Sí 2=No; conserva codificación sin acreditar lengua ni catálogo.", None)
concepto_nuevo("lengua-hablada-caso", "Lengua que habla el paciente",
    "Lengua que habla el paciente según texto libre del diccionario; sin catálogo de lenguas acreditado.", None)
concepto_nuevo("ocupacion-caso", "Ocupación del paciente",
    "Ocupación del paciente en estudio de fiebre manchada según texto del diccionario; sin catálogo de ocupaciones.", None)
concepto_nuevo("estatus-caso-rickettsia", "Estatus del caso de rickettsiosis",
    "Estatus del caso del paciente 1=Probable 2=Confirmado 3=Descartado; conserva categorías sin equiparar a diagnóstico definitivo.", None)
concepto_nuevo("diagnostico-probable-rickettsia", "Diagnóstico probable del paciente",
    "Diagnóstico probable del paciente según texto del diccionario; texto declarado sin acreditar CIE ni catálogo.", None)
concepto_nuevo("diagnostico-final-rickettsia", "Diagnóstico final del paciente",
    "Diagnóstico final del paciente según texto del diccionario; texto declarado sin acreditar CIE ni catálogo.", None)
concepto_nuevo("diagnostico-hospital-rickettsia", "Diagnóstico emitido por el hospital",
    "Diagnóstico emitido por el hospital según texto del diccionario; texto declarado sin acreditar CIE ni catálogo.", None)
concepto_nuevo("contacto-garrapatas-caso", "Contacto del caso con garrapatas",
    "Indicador de si el paciente tuvo contacto con garrapatas, 1=Sí 0=No; conserva codificación literal.", None)
concepto_nuevo("contacto-otro-animal-caso", "Contacto del caso con otro animal",
    "Registro de contacto del paciente con otro animal según texto del diccionario; animal no codificado.", None)
concepto_nuevo("acceso-agua-potable-caso", "Acceso a agua potable del caso",
    "Indicador de acceso a agua potable del entorno del caso, 1=Sí 2=No; conserva codificación.", None)
concepto_nuevo("cobertura-eliminacion-basura-caso", "Cobertura de eliminación de basura del caso",
    "Indicador de cobertura de eliminación de basura al menos un día a la semana, 1=Sí 2=No; conserva definición y codificación.", None)
concepto_nuevo("temperatura-caso", "Temperatura del paciente",
    "Temperatura del paciente en estudio de fiebre manchada; conserva unidad literal Grados celcius sin homologar.", None)
concepto_nuevo("manejo-caso-rickettsia", "Manejo del paciente",
    "Manejo del paciente 1=Hospitalario 2=Ambulatorio; conserva categorías y modalidad sin acreditar servicio concreto.", None)
concepto_nuevo("tipo-servicio-atencion", "Tipo de servicio de atención",
    "Tipo de servicio de atención con catálogo declarado 'Catálogo servicios' no acreditado; conserva descripción y ejemplo sin resolver catálogo.", None)
concepto_nuevo("evolucion-caso-rickettsia", "Evolución del caso",
    "Evolución del caso 1=Estable 2=Grave 3=Mejoría; conserva categorías sin acreditar desenlace clínico.", None)
concepto_nuevo("muestra-lcr-caso", "Muestra de líquido cefalorraquídeo con aspecto de agua de roca",
    "Indicador conjunto de toma de muestra del líquido cefalorraquídeo Y aspecto de agua de roca del caso, 1=Sí 2=No; conserva ambas condiciones literales sin reducir a mera toma ni acreditar técnica.", None)
concepto_nuevo("motivo-egreso-caso", "Motivo de egreso del paciente",
    "Motivo de egreso 1=Alta por mejoría 2=Alta voluntaria 3=Defunción; conserva categorías.", None)
concepto_nuevo("defuncion-caso", "Defunción del paciente",
    "Indicador de defunción del paciente, 1=Sí 2=No; conserva codificación sin acreditar causa.", None)
concepto_nuevo("muestra-laboratorio-caso", "Toma de muestra de laboratorio del caso",
    "Indicador de toma de muestra en laboratorio, 1=Sí 2=No; conserva codificación.", None)
concepto_nuevo("semanas-gestacion-caso", "Semanas de gestación del caso",
    "Semanas de gestación del paciente cuando aplica; conserva medida sin acreditar método.", None)
concepto_nuevo("rechazo-muestra-sangre-rickettsia", "Rechazo de muestra de sangre",
    "Indicador de rechazo de muestra de sangre del paciente, 1=Sí 2=No; conserva codificación.", None)
concepto_nuevo("motivo-rechazo-muestra-sangre", "Motivo de rechazo de muestra de sangre",
    "Motivo de rechazo de la muestra de sangre con catálogo declarado 'Motivos de rechazo' no acreditado; conserva descripción.", None)
concepto_nuevo("resultado-suero-ser1-rickettsia", "Resultado de primera muestra de suero",
    "Resultado de la primera muestra de suero para rickettsiosis 1=Positivo 2=Negativo; conserva categorías.", None)
concepto_nuevo("resultado-inmunofluorescencia-rickettsia", "Resultado declarado de inmunofluorescencia indirecta",
    "Resultado declarado de inmunofluorescencia indirecta 1=Sí 2=No según descripción literal; semántica solo resultado declarado, NO positivo/negativo; conserva codificación sin acreditar técnica.", None)
concepto_nuevo("resultado-rtpcr-rickettsia", "Resultado de PCR en tiempo real",
    "Resultado en tiempo real para rickettsiosis 1=Positivo 2=Negativo 3=Indeterminado; conserva categorías.", None)
concepto_nuevo("especie-rickettsia-rtpcr", "Especie de rickettsia por PCR en tiempo real",
    "Resultado de especie por PCR en tiempo real al INDRE con catálogo declarado 'Especie rickettsiosis' no acreditado; conserva descripción.", None)
concepto_nuevo("tratamiento-rickettsiosis-caso", "Tratamiento del caso para rickettsiosis",
    "Indicador de si el caso recibe tratamiento para rickettsiosis, 1=Sí 2=No; conserva codificación.", None)
concepto_nuevo("medicamento-tratamiento-rickettsia", "Medicamento de tratamiento para rickettsiosis",
    "Medicamento para el tratamiento 1=Doxiciclina 2=Cloramfenicol; conserva categorías literales (grafías de fuente) sin homologar fármacos.", None)
concepto_nuevo("tipo-muerte-donante", "Tipo de muerte del donante",
    "Tipo de muerte de la persona donante según texto del diccionario; categorías no declaradas, sin homologar.", None)
concepto_nuevo("organos-donados", "Órganos donados",
    "Órganos donados por la persona donante según texto del diccionario; texto libre sin catálogo.", None)
concepto_nuevo("cantidad-organos-donados", "Cantidad de órganos donados",
    "Cantidad de órganos donados por la persona donante; conserva conteo sin acreditar regla de agregación.", None)

FECHAS = {
    16: ("fecha-solicitud-atencion-caso", "Fecha de solicitud de atención del caso", "Fecha de la solicitud de atención del paciente en estudio de fiebre manchada; conserva evento solicitud."),
    17: ("fecha-inicio-estudio-caso", "Fecha de inicio de estudios del caso", "Fecha de inicio de estudios del paciente en estudio de fiebre manchada; conserva evento inicio."),
    18: ("fecha-fin-estudio-caso", "Fecha de fin de estudios del caso", "Fecha de fin de estudios del paciente en estudio de fiebre manchada; conserva evento fin."),
    25: ("fecha-inicio-signos-sintomas-caso", "Fecha de inicio de signos y síntomas del caso", "Fecha de inicio de signos y síntomas del cuadro clínico actual; conserva evento inicio."),
    26: ("fecha-inicio-fiebre-caso", "Fecha de inicio de fiebre del caso", "Fecha de inicio de fiebre del paciente; conserva grafía y evento inicio sin corregir la fuente."),
    40: ("fecha-inicio-signos-alarma-caso", "Fecha de inicio de signos de alarma del caso", "Fecha de inicio de signos de alarma; conserva evento inicio."),
    150: ("fecha-egreso-caso", "Fecha de egreso del paciente", "Fecha de egreso del paciente; conserva evento egreso sin acreditar motivo."),
    152: ("fecha-defuncion-caso", "Fecha de defunción del paciente", "Fecha de defunción del paciente; conserva evento defunción sin acreditar causa."),
}
for idx, (slug, label, defin) in FECHAS.items():
    concepto_nuevo(slug, label, defin, "tiempo")

LABS = {
    143: ("resultado-bilirrubina-directa-caso", "Resultado de bilirrubina directa", "Resultado numérico de bilirrubina directa del paciente; conserva medida sin acreditar unidad."),
    144: ("resultado-bilirrubina-total-caso", "Resultado total de bilirrubina", "Resultado numérico total de bilirrubina del paciente; conserva medida sin acreditar unidad."),
    145: ("resultado-dhl-caso", "Resultados de Deshidrogenasa Láctica", "Resultados de Deshidrogenasa Láctica del paciente según grafía de fuente; conserva medida sin acreditar unidad ni abreviatura."),
    146: ("resultado-alt-caso", "Resultados de Alanina aminotransferasa", "Resultados de Alanina aminotransferasa del paciente; conserva medida sin acreditar unidad."),
    147: ("resultado-ast-caso", "Resultados de Aspartato aminotransferasa", "Resultados de Aspartato aminotransferasa del paciente; conserva medida sin acreditar unidad."),
}
for idx, (slug, label, defin) in LABS.items():
    concepto_nuevo(slug, label, defin, None)

FIJOS = {
    # vigilancia
    ("2334deaa-dd0c-444e-b038-4cc556ad715d", 7): ("diagnostico-vigilancia", "codigo", None),
    ("2334deaa-dd0c-444e-b038-4cc556ad715d", 8): ("diagnostico-vigilancia", "nombre", None),
    # rickettsia no-síntoma
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 3): ("edad-paciente-anos", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 4): ("tipo-calle-residencia-caso", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 5): ("colonia-residencia-caso", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 8): ("localidad-residencia-caso", "codigo", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 9): ("localidad-residencia-caso", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 10): ("codigo-postal-residencia-caso", "codigo", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 11): ("condicion-indigena-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 12): ("habla-lengua-indigena-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 13): ("lengua-hablada-caso", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 14): ("ocupacion-caso", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 15): ("estatus-caso-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 19): ("diagnostico-probable-rickettsia", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 20): ("diagnostico-final-rickettsia", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 21): ("contacto-garrapatas-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 22): ("contacto-otro-animal-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 23): ("acceso-agua-potable-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 24): ("cobertura-eliminacion-basura-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 27): ("temperatura-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 121): ("manejo-caso-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 128): ("diagnostico-hospital-rickettsia", "nombre", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 129): ("tipo-servicio-atencion", "no_especificada", ["Catálogo 'Catálogo servicios' identificado en ronda 1; vigencia y valores en registro no acreditados; no se afirma catálogo validado."]),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 139): ("semanas-gestacion-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 141): ("evolucion-caso-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 142): ("muestra-lcr-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 148): (None, None, None),  # síntoma: líquido abdominal
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 149): (None, None, None),  # síntoma: líquido torácico
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 151): ("motivo-egreso-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 153): ("defuncion-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 154): ("muestra-laboratorio-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 158): ("resultado-suero-ser1-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 161): ("rechazo-muestra-sangre-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 162): ("motivo-rechazo-muestra-sangre", "no_especificada", ["Catálogo declarado 'Motivos de rechazo' sin resolver; no se acredita catálogo."]),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 165): ("resultado-inmunofluorescencia-rickettsia", "no_especificada", ["Semántica solo resultado declarado 1=Sí 2=No; NO equivale a positivo/negativo ni acredita técnica."]),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 166): ("resultado-rtpcr-rickettsia", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 168): ("especie-rickettsia-rtpcr", "no_especificada", ["Catálogo declarado 'Especie rickettsiosis' sin resolver; no se acredita catálogo ni especie."]),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 169): ("tratamiento-rickettsiosis-caso", "no_especificada", None),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", 172): ("medicamento-tratamiento-rickettsia", "no_especificada", None),
    # donaciones
    ("52fbcaaa-765b-4c92-8418-ccebc3fcfdcd", 5): ("tipo-muerte-donante", "no_especificada", None),
    ("52fbcaaa-765b-4c92-8418-ccebc3fcfdcd", 6): ("organos-donados", "nombre", None),
    ("52fbcaaa-765b-4c92-8418-ccebc3fcfdcd", 7): ("cantidad-organos-donados", "no_especificada", None),
    # CIE descripciones
    ("355da8aa-8544-4f32-b942-f54e007dd49b", 13): ("diagnostico-declarado-atencion", "nombre", None),
    ("f89137ba-d82e-44fe-80c7-cc355f09f9f5", 13): ("diagnostico-declarado-atencion", "nombre", None),
    ("355da8aa-8544-4f32-b942-f54e007dd49b", 15): ("total-urgencias-atendidas", "no_especificada", None),
}

PEND2 = {
    "2334deaa-dd0c-444e-b038-4cc556ad715d/9": ("descripcion_generica_sin_objeto",
        "La descripción literal es solo 'Clave', sin objeto; el ejemplo sugiere códigos pero el texto no acredita sistema (CIE) ni catálogo. No se promueve código a catálogo por nombre ni ejemplo."),
    "2334deaa-dd0c-444e-b038-4cc556ad715d/10": ("periodo_sin_evento_acreditado",
        "La descripción literal es solo 'Numero de la semana', sin evento ni calendario declarado; no se infiere semana epidemiológica."),
    "2334deaa-dd0c-444e-b038-4cc556ad715d/11": ("objeto_no_especificado",
        "La descripción literal es solo 'Acumulados', sin objeto acumulado ni periodo; no se propone significado."),
    "2334deaa-dd0c-444e-b038-4cc556ad715d/13": ("rango_contradictorio_nombre_descripcion",
        "El nombre de01_a_04 sugiere 1-4 pero la descripción literal dice 'entre 1 y 5 años'. Contradicción preservada sin resolver; no se afirma rango equivocado, queda pendiente sin regla."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/1": ("identificador_sin_significado",
        "La descripción literal es 'Número de identificación'. Es un identificador de registro, no un objeto con significado documental; no se acredita identidad."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/39": ("objeto_indeterminado_texto_libre",
        "La descripción literal es 'Otro síntoma que presente el paciente', objeto indeterminado de texto libre; no se propone concepto."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/60": ("abreviatura_sin_texto_publicado",
        "La descripción contiene 'SNC' sin expansión en el texto publicado; no se reconocen abreviaturas clínicas sin texto."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/130": ("objeto_indeterminado_texto_libre",
        "La descripción literal es 'Otro tipo de servicio', objeto indeterminado; no se propone concepto."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/140": ("objeto_indeterminado_texto_libre",
        "La descripción literal es 'El paciente presenta otra comorbilidad', objeto indeterminado de texto libre; no se propone concepto."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/163": ("abreviatura_sin_texto_publicado",
        "La descripción usa 'CQ' sin expansión en el texto publicado; no se reconoce la abreviatura."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/164": ("abreviatura_sin_texto_publicado",
        "La descripción usa 'CQ' sin expansión en el texto publicado; no se reconoce la abreviatura."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/177": ("fila_diccionario_danada",
        "Fila desplazada/dañada: descripción 'ide_col'; Tipo='ide_sex', Formato='ide_eda_ano', Unidad='des_cal', Ejemplo='ide_cp', catálogo 'des_mpo_res'. Vínculo físico distinto de significado."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/178": ("fila_diccionario_danada",
        "Fila desplazada/dañada: descripción 'ide_col'; Tipo='ide_sex', Formato='ide_eda_ano', Unidad='des_cal', Ejemplo='id_cp', catálogo 'des_mpo_res'. Vínculo físico distinto de significado."),
    "355da8aa-8544-4f32-b942-f54e007dd49b/12": ("codigo_sin_catalogo_acreditado",
        "Descripción literal 'Clave CIE' sin versión ni vigencia declaradas; formato y nombre no acreditan CIE-10. No se promueve código a catálogo."),
    "f89137ba-d82e-44fe-80c7-cc355f09f9f5/12": ("codigo_sin_catalogo_acreditado",
        "Descripción literal 'Clave CIE' sin versión ni vigencia declaradas; no se promueve código a catálogo por nombre ni ejemplo."),
    "f89137ba-d82e-44fe-80c7-cc355f09f9f5/15": ("observacion_vigente_contradiccion",
        "Descripción 'Total de urgencias atendidas' bajo nombre Total_Egresos contradice el objeto (observación vigente egresos-descripcion-urgencias); requiere aclaración de la fuente."),
    "52fbcaaa-765b-4c92-8418-ccebc3fcfdcd/1": ("identificador_sin_significado",
        "Descripción 'Identificador único de cada persona donante'. Identificador de registro; no se acredita identidad de persona."),
}
for i in list(range(23, 45)):
    PEND2["2334deaa-dd0c-444e-b038-4cc556ad715d/%d" % i] = ("descripcion_pendiente_en_fuente",
        "Descripción literal 'Pendiente de especificar'. No se infiere significado por el nombre (aparentes instituciones y grupos con sufijo f); pendiente de la fuente.")

REUSE2 = {
    "2334deaa-dd0c-444e-b038-4cc556ad715d/1": ("entidad", "codigo", "Clave del estado con ejemplo 26 y Nombre del Estado Sonora en el mismo diccionario; entidad federativa exacta."),
    "2334deaa-dd0c-444e-b038-4cc556ad715d/2": ("entidad", "nombre", "Nombre del Estado con ejemplo Sonora; entidad federativa exacta."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/2": ("sexo-declarado", "no_especificada", "Sexo del caso con categorías 1=Masculino 2=Femenino literales; conserva población, categorías y codificación sin homologar."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/7": ("municipio-residencia", "nombre", "Municipio donde reside el caso con ejemplo Hermosillo; municipio de residencia del sujeto exacto."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/123": ("unidad-salud", "codigo", "Clave de la unidad médica tratante con ejemplo SRIMS132154; misma unidad de atención, representación código."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/124": ("unidad-salud", "nombre", "Nombre de la unidad médica tratante con ejemplo hospitalario; unidad de atención de salud exacta."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/126": ("municipio-ubicacion", "nombre", "Municipio donde pertenece la unidad médica tratante; localización municipal de instalación exacta."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/127": ("organizacion", "nombre", "Institución de la unidad tratante con ejemplo IMSS; organización identificada por la fuente, sin catálogo."),
    "33d0a99e-c721-496f-a05e-07646e9ae42a/173": ("organizacion", "nombre", "Nombre de la institución tratante normalizado con ejemplo IMSS Bienestar; 'normalizado' es literal del publicador, no proceso nuestro; organización identificada sin confirmar identidad institucional y sin homologar papel tratante/generador/publicador."),
    "52fbcaaa-765b-4c92-8418-ccebc3fcfdcd/3": ("sexo-declarado", "no_especificada", "Sexo de la persona con formato C y ejemplo M; conserva población, categorías y codificación sin homologar."),
    "355da8aa-8544-4f32-b942-f54e007dd49b/2": ("unidad-salud", "nombre", "Nombre del establecimiento con ejemplo hospital comunitario; unidad de atención de salud exacta."),
    "c1bd5fd4-69d0-426c-afd7-47766b10708b/2": ("unidad-salud", "nombre", "Nombre del establecimiento con ejemplo centro de salud rural; unidad de atención de salud exacta."),
    "f89137ba-d82e-44fe-80c7-cc355f09f9f5/2": ("unidad-salud", "nombre", "Nombre del establecimiento con ejemplo unidad de desintoxicación; unidad de atención de salud exacta."),
}
JURISD = {("2334deaa-dd0c-444e-b038-4cc556ad715d", 3): "codigo", ("2334deaa-dd0c-444e-b038-4cc556ad715d", 4): "nombre",
          ("355da8aa-8544-4f32-b942-f54e007dd49b", 3): "codigo", ("355da8aa-8544-4f32-b942-f54e007dd49b", 4): "nombre",
          ("c1bd5fd4-69d0-426c-afd7-47766b10708b", 3): "codigo", ("c1bd5fd4-69d0-426c-afd7-47766b10708b", 4): "nombre",
          ("f89137ba-d82e-44fe-80c7-cc355f09f9f5", 3): "codigo", ("f89137ba-d82e-44fe-80c7-cc355f09f9f5", 4): "nombre",
          ("33d0a99e-c721-496f-a05e-07646e9ae42a", 6): "nombre", ("33d0a99e-c721-496f-a05e-07646e9ae42a", 125): "nombre"}

SINT = re.compile(r"^El paciente presenta (.+?) 1=Si 2=No$")
MESES_IDX = {"enero": 45, "febrero": 46, "marzo": 47, "abril": 48, "mayo": 49, "junio": 50,
             "julio": 51, "agosto": 52, "septiembre": 53, "octubre": 54, "noviembre": 55, "diciembre": 56}
EDADES_IDX = [12, 14, 15, 16, 17, 18, 19, 20, 21, 22]
EDAD_SLUGS = ["vigilancia-personas-menores-1-ano", "vigilancia-personas-de-5-a-9-anos", "vigilancia-personas-de-10-a-14-anos",
              "vigilancia-personas-de-15-a-19-anos", "vigilancia-personas-de-20-a-24-anos", "vigilancia-personas-de-25-a-44-anos",
              "vigilancia-personas-de-45-a-49-anos", "vigilancia-personas-de-50-a-59-anos", "vigilancia-personas-de-60-a-64-anos",
              "vigilancia-personas-de-65-y-mas-anos"]

for v in mine:
    iri = v["definicion_iri"]
    idx = int(iri.split("%2F")[1])
    row = byid[v["diccionario"]].get("definiciones", [])[idx - 1]
    assert huella(row) == v["huella_fila_diccionario"], iri
    key = (v["diccionario"], idx)
    skey = "%s/%d" % key
    des = v["descripcion"]
    if skey in PEND2:
        razon, crit = PEND2[skey]
        pendiente(v, row, razon, "%s [tipo=%s formato=%s unidad=%s ejemplo=%s]" % (
            crit, row.get("Tipo de dato", ""), row.get("Formato", ""),
            row.get("Unidad de medida", ""), row.get("Ejemplo de dato", "")))
        continue
    if skey in REUSE2:
        cid, rep, motivo = REUSE2[skey]
        reuse(cid, motivo)
        proponer(v, row, cid, rep, "Reutilización exacta de concepto vigente %s: %s" % (cid, motivo),
                 ["Concepto vigente reutilizado sin crear identidad, vigencia, referencia ni equivalencia externa."], True)
        continue
    if key in JURISD:
        rol = "residencia del caso" if (v["diccionario"] == RIK and "reside" in des) else ("unidad tratante" if "tratante" in des else "jurisdicción del conjunto")
        proponer(v, row, "jurisdiccion-sanitaria", JURISD[key],
                 "Jurisdicción de salud según diccionario de salud de Sonora (ejemplo %r); rol: %s." % (row.get("Ejemplo de dato", ""), rol),
                 ["Calificador sanitario desde contexto de salud publicado; sin catálogo oficial ni vigencia acreditados."], False)
        continue
    m = SINT.match(des)
    if m and v["conjunto"] == RIK and key not in FIJOS:
        x = m.group(1)
        slug = "caso-con-" + SLUG(x)
        concepto_nuevo(slug, "Caso con %s" % x,
            "Indicador de si el paciente (caso en estudio de fiebre manchada) presenta %s, codificado 1=Sí 2=No según el diccionario; conserva población, manifestación y codificación sin homologar ni diagnosticar." % x, None)
        proponer(v, row, slug, "no_especificada",
                 "Descripción literal específica con población (paciente), manifestación (%s) y codificación 1=Sí 2=No; ejemplo %r, tipo %s." % (x, row.get("Ejemplo de dato", ""), row.get("Tipo de dato", "")),
                 LIM_FLAG, False)
        continue
    if v["conjunto"] == VIG and idx in MESES_IDX.values():
        mes = [k for k, i in MESES_IDX.items() if i == idx][0]
        proponer(v, row, "vigilancia-total-%s" % mes, "no_especificada",
                 "Total de vigilancias del mes de %s según descripción literal; ejemplo %r." % (mes, row.get("Ejemplo de dato", "")),
                 ["Mes conservado sin acreditar año ni regla de agregación; no sumar entre meses sin evidencia."], False)
        continue
    if v["conjunto"] == VIG and idx in EDADES_IDX:
        slug = EDAD_SLUGS[EDADES_IDX.index(idx)]
        proponer(v, row, slug, "no_especificada",
                 "Total de personas en vigilancia en el tramo literal %r; ejemplo %r." % (des.split("que son ")[-1] if "que son" in des else des.split("entre ")[-1], row.get("Ejemplo de dato", "")),
                 ["Tramo de edad y población conservados; borde de intervalos (p. ej. de01_a_04 dice 'entre 1 y 5 años') preservado literal sin reinterpretar."], False)
        continue
    if v["conjunto"] == VIG and idx == 58:
        proponer(v, row, "vigilancia-total-hombres", "no_especificada",
                 "Total acumulado de Hombres según descripción literal; ejemplo %r." % row.get("Ejemplo de dato", ""),
                 ["Categoría literal Hombres sin homologar a clasificación de sexo."], False)
        continue
    if v["conjunto"] == VIG and idx == 59:
        proponer(v, row, "vigilancia-total-mujeres", "no_especificada",
                 "Total acumulado de Mujeres según descripción literal; ejemplo %r." % row.get("Ejemplo de dato", ""),
                 ["Categoría literal Mujeres sin homologar a clasificación de sexo."], False)
        continue
    if key in FIJOS:
        slug, rep, extra = FIJOS[key]
        if slug is None:  # síntoma 148/149
            x = des[len("El paciente presenta "):]
            slug = "caso-con-" + SLUG(x)
            concepto_nuevo(slug, "Caso con %s" % x,
                "Indicador de si el paciente presenta %s según el diccionario; conserva población, manifestación y codificación sin homologar ni diagnosticar." % x, None)
            proponer(v, row, slug, "no_especificada",
                     "Descripción literal específica con población y manifestación; ejemplo %r." % row.get("Ejemplo de dato", ""), LIM_FLAG, False)
        else:
            lim = list(LIM_NOCAT) if extra is None else (LIM_NOCAT + extra if isinstance(extra, list) else [extra])
            if slug in ("diagnostico-vigilancia", "diagnostico-declarado-atencion", "diagnostico-probable-rickettsia",
                        "diagnostico-final-rickettsia", "diagnostico-hospital-rickettsia"):
                lim = ["Solo texto/clave de diagnóstico declarado; sin expandir CIE por formato, ejemplo o campo; sin catálogo ni vigencia."]
            proponer(v, row, slug, rep,
                     "Descripción literal específica %r con tipo %s, ejemplo %r y contexto %s." % (
                         des, row.get("Tipo de dato", ""), row.get("Ejemplo de dato", ""), v["titulo_conjunto"]),
                     lim, False)
        continue
    if v["conjunto"] == RIK and idx in FECHAS:
        slug, label, defin = FECHAS[idx]
        proponer(v, row, slug, "fecha",
                 "Fecha con evento literal %r, formato %s y ejemplo %r." % (des, row.get("Formato", ""), row.get("Ejemplo de dato", "")),
                 ["Fecha de registro documental; no acredita ocurrencia ni vigencia."], False)
        continue
    if v["conjunto"] == RIK and idx in LABS:
        slug, label, defin = LABS[idx]
        proponer(v, row, slug, "no_especificada",
                 "Resultado numérico literal %r con ejemplo %r." % (des, row.get("Ejemplo de dato", "")),
                 ["Medida conservada sin acreditar unidad; no comparar entre laboratorios sin evidencia."], False)
        continue
    raise AssertionError("sin clasificar: %s %s %r" % (v["diccionario"][:8], v["variable"], des))

assert len(decisiones) == 242
assert len({d["definicion_iri"] for d in decisiones}) == 242
assert len(reglas) == sum(1 for d in decisiones if d["decision"] == "proponer_significado")

# sin colisiones con reglas vigentes (alcance restringido no altera 232 respaldadas)
vigentes = []
for r in sem["reglas_descripcion_exacta"]:
    for d in r["descripciones"]:
        vigentes.append((_clave(d), r.get("conjuntos"), r.get("diccionarios"), r.get("definiciones"), r["id"]))
for rg in reglas:
    for d in rg["descripciones"]:
        for vd, cj, dc, df, rid0 in vigentes:
            if _clave(d) == vd and (cj is None or rg["conjuntos"][0] in cj) \
                    and (dc is None or rg["diccionarios"][0] in dc) \
                    and (df is None or rg["definiciones"][0] in df):
                raise AssertionError("colisión con regla vigente %s en %s" % (rid0, rg["id"]))

salida = {"agente": "agente-6-salud", "fecha_utc": datetime.now(timezone.utc).isoformat(),
          "asignacion": {"cantidad": 242,
                         "sha256_cobertura": asig["sha256_cobertura"],
                         "conjuntos": asig["asignaciones"]["6"].get("conjuntos", {})},
          "alcance": "Partición exclusiva del integrador: 242 definiciones fuera del núcleo actual de 6 conjuntos de salud. Sin nuevas correspondencias columna-variable. Sin leer otras propuestas concurrentes.",
          "limites": ["Evidencia documental, significado y vínculo físico son decisiones distintas.",
                      "Solo evidencia local del proyecto; sin descargas ni red.",
                      "Claves de inspección central con mojibake preservadas tal cual; valores literales intactos sin U+FFFD.",
                      "Grafías y typos de fuente preservados sin corrección (vigilanciade, incio, sonmnolencia, hipercusia, transtornos, inmunoflourecencia, ricketsiosis, romaña, metrorrragia).",
                      "Pipeline central actual no preserva calificadores: cada calificador sustantivo genera concepto estrecho propio; ninguna regla afirma propagación.",
                      "Sin sameAs/exactMatch; broader solo hacia conceptos vigentes existentes o nulo.",
                      "Normalización ñ intacta en literales; slugs ASCII solo como identificadores nuevos.",
                      "descripcion_raw_literal preserva el valor exacto de la fila del diccionario (incluye espacios finales si existen); el trim es del valor() central y no cambia la huella fuente."],
          "fuentes_huellas_entrada": huellas_entrada,
          "totales": {"decisiones": len(decisiones),
                      "proponer_significado": sum(1 for d in decisiones if d["decision"] == "proponer_significado"),
                      "pendientes": sum(1 for d in decisiones if d["decision"] == "pendiente"),
                      "reglas": len(reglas), "conceptos_nuevos": len(nuevos),
                      "conceptos_reutilizados": len(reutilizados)},
          "decisiones": decisiones, "reglas": reglas,
          "conceptos_nuevos": nuevos, "conceptos_reutilizados": reutilizados}
json.dump(salida, open(A6 + "/propuestas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import os
os.makedirs(A6 + "/fuente", exist_ok=True)
json.dump({"archivos": {k: {"sha256": huellas_entrada[k]} for k in huellas_entrada}},
          open(A6 + "/fuente/huellas_entrada.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
prop = sum(1 for d in decisiones if d["decision"] == "proponer_significado")
pen = len(decisiones) - prop
md = ["# Agente 6 Salud — ronda 3", "",
      "Partición exclusiva: 242 definiciones fuera del núcleo actual (Vigilancia Epidemiológica 56, Fiebre manchada 166, Atencion de Urgencias 6, Donaciones 5, Consulta Externa 3, Egresos Hospitalarios 6).",
      "", "## Totales", "",
      "- Decisiones: 242 (partición completa, sin omitidos ni duplicados).",
      "- Proponer significado: %d." % prop, "- Pendientes con razón: %d." % pen,
      "- Reglas nuevas restringidas (conjunto+diccionario+definición+nombre+descripción+representación+huella): %d." % len(reglas),
      "- Conceptos nuevos estrechos: %d. Conceptos vigentes reutilizados: %d (%s)." % (
          len(nuevos), len(reutilizados), ", ".join(sorted(reutilizados))), "",
      "## Pendientes por razón", ""]
from collections import Counter
for razon, n in sorted(Counter(d["razon"] for d in decisiones if d["decision"] == "pendiente").items()):
    md.append("- %s: %d." % (razon, n))
md += ["", "## Verificación", "",
       "- Huellas de fila de diccionario recalculadas desde inspección central: 242/242.",
       "- Cobertura/asignación/semántica verificadas en lectura (103 conceptos, 232 respaldadas, 836 revisadas, 118 candidatas, 116 reglas).",
       "- Sin colisiones con reglas vigentes. Verificador propio: scripts/verificar.py (positivos para las 242 + 9 negativos).",
       "", "## Revisión manual vs automatización", "",
       "- Manual: lectura literal individual de las 242 definiciones (descripción, tipo, formato, unidad, ejemplo, catálogo, detalle de catálogo) desde la inspección central; cada decisión quedó codificada en tablas explícitas por (diccionario, índice) en scripts/paso2_generar.py (PEND2, REUSE2, FIJOS, FECHAS, LABS, JURISD, MESES/EDADES) o en la plantilla de descripción de bandera de síntoma.",
       "- Manual: 22 pendientes por descripción 'Pendiente de especificar' sin inferir por nombre (incluye aparentes instituciones y sufijos f); identificadores, indeterminados, abreviaturas SNC/CQ, CIE sin versión, filas 177/178 dañadas y Total_Egresos con observación vigente.",
       "- Manual: contradicciones nombre vs descripción preservadas sin resolver (p. ej. de01_a_04 dice 'entre 1 y 5 años'; typos vigilanciade/incio/sonmnolencia/hipercusia/transtornos/inmunoflourecencia/ricketsiosis/romaña/metrorrragia).",
       "- Automatizado: aplicación mecánica de esas tablas, generación de reglas/conceptos, recálculo de huellas, simulación de interpretacion() en memoria y negativos. Ninguna regla deduce significado desde regex de nombre: toda propuesta exige descripción exacta + conjunto + diccionario + definición.",
       "- Criterio de unidades: sin unidades añadidas por costumbre (edad conserva 'en años' literal; temperatura conserva 'Grados celcius' sin homologar; conteos conservan objeto literal; sin porcentajes ni monetarios en la partición).",
       "", "## Límites", "",
       "- Sin nuevas correspondencias columna-variable; no se acredita vigencia, identidad, catálogos ni equivalencias.",
       "- Fila 177/178 de fiebre manchada dañada (desplazada); se preserva literal y queda pendiente.",
       "- 'SNC' y 'CQ' sin expansión en texto: pendientes, no se reconocen abreviaturas.",
       "- Códigos CIE sin versión/vigencia: pendientes, no se promueven a catálogo.",
       "- Total_Egresos mantiene observación vigente de contradicción: pendiente."]
open(A6 + "/resultado.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("decisiones=%d proponer=%d pendientes=%d reglas=%d nuevos=%d reut=%s" % (
    len(decisiones), prop, pen, len(reglas), len(nuevos), sorted(reutilizados)))
