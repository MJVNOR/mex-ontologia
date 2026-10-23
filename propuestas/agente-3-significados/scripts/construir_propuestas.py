"""Construye propuestas.json desde cobertura.json sin tocar nada fuera de propuestas/agente-3-significados/."""
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
COB = ROOT / "data/semantica/cobertura.json"
OUT = HERE / "propuestas.json"

cob = json.loads(COB.read_text(encoding="utf-8"))
cands = {v["definicion_iri"]: v for v in cob["variables"] if v.get("estado") == "candidata_sin_definicion_suficiente"}
assert len(cands) == 47, f"se esperaban 47, hay {len(cands)}"

# (decision, motivo_pendiente, concepto_id, regla_id)
# decision: mantener | proponer
PEND = "mantener_pendiente"
PROP = "proponer"

PLAN = {
    # SEED defunciones — 5 pendientes explícitos
    "definition/12f684e9-f4d5-4714-933d-aa153a812174%2F38": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/12f684e9-f4d5-4714-933d-aa153a812174%2F72": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/12f684e9-f4d5-4714-933d-aa153a812174%2F73": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/12f684e9-f4d5-4714-933d-aa153a812174%2F74": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/12f684e9-f4d5-4714-933d-aa153a812174%2F75": (PEND, "descripcion_pendiente_explicita", None, None),
    # Nacimientos — 5 pendientes explícitos
    "definition/22202305-2d02-4c49-b216-cc98224357f0%2F83": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/22202305-2d02-4c49-b216-cc98224357f0%2F102": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/22202305-2d02-4c49-b216-cc98224357f0%2F103": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/22202305-2d02-4c49-b216-cc98224357f0%2F104": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/22202305-2d02-4c49-b216-cc98224357f0%2F105": (PEND, "descripcion_pendiente_explicita", None, None),
    # Marginación localidad / Ceresos — genéricas insuficientes
    "definition/251309e5-0309-46ed-9711-77a1dd408eeb%2F1": (PEND, "descripcion_generica_insuficiente", None, None),
    "definition/2fc2fbc6-e918-4d5d-b907-1191e266b131%2F5": (PEND, "descripcion_generica_insuficiente", None, None),
    # Rickettsia — 9 propuestas clínicas diferenciadas
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F122": (PROP, None, "fecha-ingreso-paciente", "fecha-ingreso-paciente"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F155": (PROP, None, "fecha-toma-suero-rickettsia-ser1", "fecha-toma-suero-rickettsia-ser1"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F156": (PROP, None, "fecha-recepcion-suero-rickettsia-ser1", "fecha-recepcion-suero-rickettsia-ser1"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F157": (PROP, None, "fecha-resultado-suero-rickettsia-ser1", "fecha-resultado-suero-rickettsia-ser1"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F159": (PROP, None, "fecha-toma-sangre-rickettsia", "fecha-toma-sangre-rickettsia"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F160": (PROP, None, "fecha-recepcion-sangre-rickettsia", "fecha-recepcion-sangre-rickettsia"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F167": (PROP, None, "fecha-resultado-pcr-tiempo-real-rickettsia", "fecha-resultado-pcr-tiempo-real-rickettsia"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F170": (PROP, None, "fecha-inicio-tratamiento-rickettsia", "fecha-inicio-tratamiento-rickettsia"),
    "definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F171": (PROP, None, "fecha-fin-tratamiento-rickettsia", "fecha-fin-tratamiento-rickettsia"),
    # Titulados posgrado + licenciatura — 4 conceptos compartidos, 8 variables
    "definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F2": (PROP, None, "fecha-nacimiento-titulado", "fecha-nacimiento-titulado"),
    "definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F5": (PROP, None, "fecha-ingreso-institucion-titulado", "fecha-ingreso-institucion-titulado"),
    "definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F6": (PROP, None, "fecha-egreso-institucion-titulado", "fecha-egreso-institucion-titulado"),
    "definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F7": (PROP, None, "fecha-titulacion-titulado", "fecha-titulacion-titulado"),
    "definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F2": (PROP, None, "fecha-nacimiento-titulado", "fecha-nacimiento-titulado"),
    "definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F5": (PROP, None, "fecha-ingreso-institucion-titulado", "fecha-ingreso-institucion-titulado"),
    "definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F6": (PROP, None, "fecha-egreso-institucion-titulado", "fecha-egreso-institucion-titulado"),
    "definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F7": (PROP, None, "fecha-titulacion-titulado", "fecha-titulacion-titulado"),
    # Denuncias
    "definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2": (PEND, "descripcion_generica_insuficiente", None, None),
    "definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F4": (PROP, None, "fecha-denuncia", "fecha-denuncia"),
    # Donaciones
    "definition/52fbcaaa-765b-4c92-8418-ccebc3fcfdcd%2F4": (PROP, None, "unidad-hospitalaria-donacion", "unidad-hospitalaria-donacion"),
    # Minería — genérica insuficiente
    "definition/587a3ccd-a814-4190-8e6f-dfb20ccf44c4%2F1": (PEND, "descripcion_generica_insuficiente", None, None),
    # Desaparecidas
    "definition/5e430f3c-09d9-4402-9f75-4cae840d5421%2F2": (PROP, None, "fecha-nacimiento-victima", "fecha-nacimiento-victima"),
    # Matrículas
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F10": (PROP, None, "fecha-inscripcion-alumno", "fecha-inscripcion-alumno"),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F14": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F20": (PEND, "descripcion_truncada", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F38": (PROP, None, "fecha-reinscripcion-alumno", "fecha-reinscripcion-alumno"),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F59": (PROP, None, "fecha-baja-alumno", "fecha-baja-alumno"),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F64": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F66": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F67": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F68": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F69": (PEND, "descripcion_pendiente_explicita", None, None),
    "definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F70": (PEND, "descripcion_pendiente_explicita", None, None),
    # Presas / Atenciones
    "definition/bfb8788b-8ce3-475e-8bbd-dd1c5154c877%2F2": (PEND, "descripcion_generica_insuficiente", None, None),
    "definition/e2b59a36-0fe1-4106-9756-ed9aca7dd9d0%2F1": (PROP, None, "mes-atencion", "mes-atencion"),
}

CONCEPTOS = {
    "fecha-ingreso-paciente": ("Fecha de ingreso del paciente", "Fecha de ingreso del paciente según su diccionario; no especifica servicio ni institución de ingreso.", "tiempo", "fecha"),
    "fecha-toma-suero-rickettsia-ser1": ("Fecha de toma de primera muestra de suero", "Fecha en la que se toma la primera muestra de suero para rickettsiosis según su definición; conserva la expresión documentada «primera muestra de suero». «ser1» se conserva como identificador de la variable sin deducir tipo de prueba serológica. No equivale a recepción ni a resultado.", "tiempo", "fecha"),
    "fecha-recepcion-suero-rickettsia-ser1": ("Fecha de recepción de primera muestra de suero", "Fecha de recepción de la primera muestra de suero para rickettsiosis según su definición; conserva «primera muestra de suero». «ser1» es identificador de la variable, no prueba tipificada. No equivale a toma ni a resultado.", "tiempo", "fecha"),
    "fecha-resultado-suero-rickettsia-ser1": ("Fecha de resultado de primera muestra de suero", "Fecha de resultado de la primera muestra de suero para rickettsiosis según su definición (texto original «suer»); conserva «primera muestra de suero». «ser1» es identificador de la variable sin deducir prueba. No equivale a toma, recepción ni a «PCR tiempo real».", "tiempo", "fecha"),
    "fecha-toma-sangre-rickettsia": ("Fecha de toma de sangre", "Fecha de toma de muestra de sangre para rickettsiosis; conserva muestra sangre. La definición no precisa secuencia ni prueba posterior.", "tiempo", "fecha"),
    "fecha-recepcion-sangre-rickettsia": ("Fecha de recepción de sangre", "Fecha de recepción de la primera muestra de sangre para rickettsiosis; conserva muestra sangre y secuencia primera. No equivale a toma ni a resultado.", "tiempo", "fecha"),
    "fecha-resultado-pcr-tiempo-real-rickettsia": ("Fecha de resultado PCR tiempo real", "Fecha de resultado «PCR tiempo real» para rickettsiosis según su definición; conserva la expresión documentada sin tipificar ensayo. No equivale a toma, recepción ni a resultado de suero.", "tiempo", "fecha"),
    "fecha-inicio-tratamiento-rickettsia": ("Fecha de inicio de tratamiento", "Fecha de inicio de tratamiento para rickettsiosis; conserva evento inicio y enfermedad. Población paciente implícita por contexto, no declarada en la definición.", "tiempo", "fecha"),
    "fecha-fin-tratamiento-rickettsia": ("Fecha de término de tratamiento", "Fecha de término de tratamiento para rickettsiosis; conserva evento término y enfermedad. Población paciente solo contextual.", "tiempo", "fecha"),
    "fecha-nacimiento-titulado": ("Fecha de nacimiento del titulado", "Fecha de nacimiento del titulado; conserva población titulado y evento nacimiento. No precisa lugar.", "tiempo", "fecha"),
    "fecha-ingreso-institucion-titulado": ("Fecha de ingreso del titulado", "Fecha de ingreso del titulado a la institución; conserva población y evento ingreso. La definición no identifica institución concreta.", "tiempo", "fecha"),
    "fecha-egreso-institucion-titulado": ("Fecha de egreso del titulado", "Fecha de egreso del titulado de la institución; conserva población y evento egreso. Institución no identificada en la definición.", "tiempo", "fecha"),
    "fecha-titulacion-titulado": ("Fecha de titulación del titulado", "Fecha en que el titulado se tituló; distinta de ingreso y egreso. Conserva población titulado.", "tiempo", "fecha"),
    "fecha-denuncia": ("Fecha de la denuncia", "Fecha de la denuncia según Denuncias Ambientales; conserva evento denuncia. El nombre de la variable menciona recepción pero la descripción no la confirma; no se asume recepción ni fecha de ocurrencia de los hechos.", "tiempo", "fecha"),
    "unidad-hospitalaria-donacion": ("Unidad hospitalaria de donación", "Unidad hospitalaria donde se realizó la donación; conserva objeto hospitalario y evento donación. No acredita pertenencia a catálogo CLUES ni distingue publicadora/capturadora.", "organizacion", "no_especificada"),
    "fecha-nacimiento-victima": ("Fecha de nacimiento de la víctima", "Fecha de nacimiento de la víctima; conserva población víctima y evento nacimiento. Distinta de nacimiento de titulado o alumno.", "tiempo", "fecha"),
    "fecha-inscripcion-alumno": ("Fecha de inscripción del alumno", "Fecha de inscripción del alumno al ciclo escolar actual; conserva población alumno y evento inscripción. Ciclo referenciado sin resolver periodo.", "tiempo", "fecha"),
    "fecha-reinscripcion-alumno": ("Fecha de reinscripción del alumno", "Fecha de reinscripción del alumno; conserva población y evento reinscripción. Distinta de inscripción inicial y de baja.", "tiempo", "fecha"),
    "fecha-baja-alumno": ("Fecha de baja del alumno", "Fecha de baja del alumno; conserva población y evento baja. Distinta de inscripción y reinscripción.", "tiempo", "fecha"),
    "mes-atencion": ("Mes de atención", "Meses en que se brindó la atención según Atenciones brindadas; conserva evento atención. Población no precisada en la definición (contexto: personas atendidas); requiere año como contexto y no equivale a registro o captura.", "tiempo", "mes"),
}

EJEMPLOS = {
    "fecha-ingreso-paciente": (["Fecha de ingreso del paciente = 2024-05-01"], ["Fecha de egreso del paciente (no es ingreso)", "Fecha de ingreso de la llamada (otra población)"]),
    "fecha-toma-suero-rickettsia-ser1": (["Fecha en la que se toma la primera muestra de suero para rickettsiosis"], ["Fecha de recepción de esa muestra (evento distinto)", "Fecha de toma de sangre (muestra distinta)"]),
    "fecha-recepcion-suero-rickettsia-ser1": (["Fecha de recepción de primera muestra de suero para rickettsiosis"], ["Fecha de toma (evento distinto)", "Fecha de recepción de sangre (muestra distinta)"]),
    "fecha-resultado-suero-rickettsia-ser1": (["Fecha de resultado de la primera muestra de suero para rickettsiosis"], ["Fecha de resultado «PCR tiempo real» (expresión distinta)", "Fecha de toma (evento distinto)"]),
    "fecha-toma-sangre-rickettsia": (["Fecha de toma muestra de sangre para rickettsiosis"], ["Fecha de toma de suero (muestra distinta)", "Fecha de recepción de sangre (evento distinto)"]),
    "fecha-recepcion-sangre-rickettsia": (["Fecha de recepción de primera muestra de sangre para rickettsiosis"], ["Fecha de recepción de suero (muestra distinta)", "Fecha de toma de sangre (evento distinto)"]),
    "fecha-resultado-pcr-tiempo-real-rickettsia": (["Fecha de resultado PCR tiempo real para rickettsiosis"], ["Fecha de resultado de primera muestra de suero (muestra/expresión distinta)", "Fecha de toma con «PCR tiempo real» (evento distinto)"]),
    "fecha-inicio-tratamiento-rickettsia": (["Fecha de inicio de tratamiento para rickettsiosis"], ["Fecha de término (evento distinto)", "Fecha de ingreso (evento distinto)"]),
    "fecha-fin-tratamiento-rickettsia": (["Fecha de termino de tratamiento para rickettsiosis"], ["Fecha de inicio (evento distinto)", "Fecha de egreso (evento distinto)"]),
    "fecha-nacimiento-titulado": (["Fecha de nacimiento del titulado"], ["Fecha de nacimiento de la víctima (población distinta)", "Fecha de ingreso del titulado (evento distinto)"]),
    "fecha-ingreso-institucion-titulado": (["Fecha en la que el titulado ingreso a la institucion"], ["Fecha de egreso (evento distinto)", "Fecha de ingreso del paciente (población distinta)"]),
    "fecha-egreso-institucion-titulado": (["Fecha en la que el titulado egreso de la institucion"], ["Fecha de ingreso (evento distinto)", "Fecha de titulación (evento distinto)"]),
    "fecha-titulacion-titulado": (["Fecha en la que el titulado se tituló"], ["Fecha de egreso (evento distinto)", "Fecha de titulación del título profesional con descripción pendiente (sin respaldo)"]),
    "fecha-denuncia": (["Fecha de la denuncia en Denuncias Ambientales"], ["TRIMESTRE del estrato (granularidad y evento distintos)", "Fecha de ocurrencia de los hechos (no documentada)"]),
    "unidad-hospitalaria-donacion": (["Unidad Hospitalaria donde se realizo la donacion"], ["CLUES con descripción pendiente (sin respaldo)", "Dependencia que capturó (papel distinto)"]),
    "fecha-nacimiento-victima": (["Fecha de nacimiento de la víctima"], ["Fecha del reporte de la víctima (evento distinto)", "Fecha de nacimiento del titulado (población distinta)"]),
    "fecha-inscripcion-alumno": (["Fecha en la que el alumno se inscribio al ciclo escolar actual"], ["Fecha de reinscripción (evento distinto)", "Fecha de baja (evento distinto)"]),
    "fecha-reinscripcion-alumno": (["Fecha en la que se reinscribió el alumno"], ["Fecha de inscripción inicial (evento distinto)", "Fecha de baja (evento distinto)"]),
    "fecha-baja-alumno": (["Fecha en la que el alumno se dio de baja"], ["Fecha de reinscripción (evento distinto)", "Periodo de la baja / Tipo de baja (no son fecha)"]),
    "mes-atencion": (["meses en que se brindó la atención"], ["Año de captura (evento distinto)", "Mes de registro genérico de otro conjunto (contexto distinto)"]),
}

MOTIVO_TXT = {
    "descripcion_pendiente_explicita": "Descripción literal «Pendiente de especificar»: sin respaldo documental; no se deduce por el nombre (nucleo-semantico.md:52).",
    "descripcion_generica_insuficiente": "Descripción genérica o ambigua: no precisa evento, papel, unidad o representación para respaldar concepto/regla.",
    "descripcion_truncada": "Descripción truncada/incompleta: «Municipio donde el alumno» sin verbo ni papel territorial; no se infiere residencia, escuela ni nacimiento.",
}

variables = []
for iri_suffix, (dec, motivo, cid, rid) in PLAN.items():
    iri = "https://example.org/mex-ontologi/" + iri_suffix
    v = cands[iri]
    cope = CONCEPTOS.get(cid) if cid else None
    if dec == PROP:
        etiqueta, definicion, padre, rep = cope
        pos, neg = EJEMPLOS[cid]
        variables.append({
            "variable": v["variable"],
            "conjunto": v["conjunto"],
            "titulo_conjunto": v["titulo_conjunto"],
            "diccionario": v["diccionario"],
            "descripcion_literal": v["descripcion"],
            "definicion_iri": v["definicion_iri"],
            "huella_fila_diccionario": v["huella_fila_diccionario"],
            "catalogo_declarado": v.get("catalogo_declarado", ""),
            "estado_previo": "candidata_sin_definicion_suficiente",
            "concepto_pista_previo": v.get("concepto"),
            "decision": "proponer",
            "motivo_pendiente": None,
            "concepto_propuesto": {"id": cid, "etiqueta": etiqueta, "definicion": definicion, "padre": padre, "existente": False},
            "regla_propuesta": {"id": rid, "representacion": rep, "descripciones_cubiertas": [v["descripcion"]], "definiciones_objetivo": [v["definicion_iri"]], "diccionarios_objetivo": [v["diccionario"]], "conjuntos_objetivo": [v["conjunto"]], "variables_objetivo": [v["variable"]]},
            "evidencia": {"descripcion_literal": v["descripcion"], "definicion_iri": v["definicion_iri"], "huella": v["huella_fila_diccionario"], "diccionario": v["diccionario"], "conjunto": v["conjunto"]},
            "alcance": f"Solo la variable documentada {v['variable']} del diccionario {v['diccionario']} ({v['titulo_conjunto']}), definición {v['definicion_iri']}. No declara correspondencia con columnas físicas ni se aplica al vocabulario central.",
            "limitaciones": [definicion.split(";")[-1].strip() if ";" in definicion else "Población/contexto según definición; no homologar entre poblaciones o eventos."],
            "documentado_vs_inferencia": f"Documentado: {repr(v['descripcion'])}. Inferencia separada: el concepto/regla propuestos interpretan ese texto; no se validan valores ni catálogos.",
            "ejemplos_positivos": pos,
            "contraejemplos": neg,
        })
    else:
        variables.append({
            "variable": v["variable"],
            "conjunto": v["conjunto"],
            "titulo_conjunto": v["titulo_conjunto"],
            "diccionario": v["diccionario"],
            "descripcion_literal": v["descripcion"],
            "definicion_iri": v["definicion_iri"],
            "huella_fila_diccionario": v["huella_fila_diccionario"],
            "catalogo_declarado": v.get("catalogo_declarado", ""),
            "estado_previo": "candidata_sin_definicion_suficiente",
            "concepto_pista_previo": v.get("concepto"),
            "decision": "mantener_pendiente",
            "motivo_pendiente": motivo,
            "motivo_detalle": MOTIVO_TXT[motivo],
            "concepto_propuesto": None,
            "regla_propuesta": None,
            "evidencia": {"descripcion_literal": v["descripcion"], "definicion_iri": v["definicion_iri"], "huella": v["huella_fila_diccionario"], "diccionario": v["diccionario"], "conjunto": v["conjunto"]},
            "alcance": f"Solo la variable documentada {v['variable']} del diccionario {v['diccionario']} ({v['titulo_conjunto']}). Permanece candidata; no se propone concepto ni regla.",
            "limitaciones": ["Sin respaldo suficiente en la definición; no deducir por el nombre de la variable."],
            "documentado_vs_inferencia": f"Documentado: {repr(v['descripcion'])}. Inferencia separada: ninguna; mantener pendiente.",
        })

variables.sort(key=lambda x: (x["titulo_conjunto"], x["diccionario"], x["variable"]))
n_prop = sum(1 for x in variables if x["decision"] == "proponer")
n_pend = sum(1 for x in variables if x["decision"] == "mantener_pendiente")
motivos = {}
for x in variables:
    if x["motivo_pendiente"]:
        motivos[x["motivo_pendiente"]] = motivos.get(x["motivo_pendiente"], 0) + 1

conceptos_nuevos = [{"id": k, "etiqueta": v[0], "definicion": v[1], "padre": v[2]} for k, v in CONCEPTOS.items()]
reglas_nuevas = []
for k, v in CONCEPTOS.items():
    pos, neg = EJEMPLOS[k]
    rep = v[3]
    objetivo = [x for x in variables if x.get("regla_propuesta") and x["regla_propuesta"]["id"] == k]
    descs = sorted({x["descripcion_literal"] for x in objetivo})
    reglas_nuevas.append({
        "id": k, "concepto": k, "representacion": rep,
        "descripciones_cubiertas": descs,
        "definiciones_objetivo": sorted({x["definicion_iri"] for x in objetivo}),
        "diccionarios_objetivo": sorted({x["diccionario"] for x in objetivo}),
        "conjuntos_objetivo": sorted({x["conjunto"] for x in objetivo}),
        "variables_objetivo": sorted({f"{x['diccionario']}|{x['variable']}" for x in objetivo}),
        "ejemplos_positivos": pos, "contraejemplos": neg,
        "alcance": f"Solo {len(objetivo)} definición/variable objetivo listadas en definiciones_objetivo; no se aplica al vocabulario central ni declara correspondencias con columnas.",
        "alcance_verificable": True,
    })
reglas_nuevas.sort(key=lambda r: r["id"])

OUT.write_text(json.dumps({
    "generado_en_utc": datetime.now(timezone.utc).isoformat(),
    "alcance": "Propuestas no aplicadas al vocabulario central (ontologia/semantica.json, data/semantica/*). Unidad de trabajo: variable documentada y su definición. Sin correspondencias con columnas físicas. Sin ampliar a las 1,308 fuera del núcleo.",
    "fuentes_revisadas": ["data/semantica/cobertura.json", "ontologia/semantica.json", "docs/nucleo-semantico.md"],
    "resumen": {"total": len(variables), "proponer": n_prop, "mantener_pendiente": n_pend, "motivos_pendiente": motivos, "conceptos_nuevos": len(conceptos_nuevos), "reglas_nuevas": len(reglas_nuevas)},
    "variables": variables,
    "conceptos_nuevos": conceptos_nuevos,
    "reglas_nuevas": reglas_nuevas,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"total": len(variables), "proponer": n_prop, "mantener_pendiente": n_pend, "motivos": motivos}, ensure_ascii=False, indent=2))
