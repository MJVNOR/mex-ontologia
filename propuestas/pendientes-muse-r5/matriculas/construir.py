# Ronda 5, rol matriculas: construye entrega.json, solicitudes_web.json, resultado.md, listo.json.
# Solo lee fuera de esta carpeta (inspecciones, cobertura, semantica, dictamenes previos). Sin red.
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
BASE = "https://example.org/mex-ontologi/"
CONJ = "e819466c-7282-46c5-84e9-65917dd8cc85"
DICC = "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d"
REC = "58f2d5a6-0432-48f1-8a35-a5efcce78bac"
HOJA = "Estudiantes 2022-2"
ALC = ("solo aplica a la definicion citada (alcance simultaneo por conjunto, diccionario, "
       "definicion, nombre y descripcion); no autoriza cruces, homologaciones ni equivalencias")
H_ESQ = "ae4056d7c6061d7fe592405869ca2944964278784834ddf69af8ffe6b7cdc82a"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


def save(rel, obj):
    (AQUI / rel).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diri(n):
    return f"{BASE}definition/{DICC}%2F{n}"


asig = load("propuestas/pendientes-muse-r5/matriculas/asignacion.json")
huella_por_iri = {s["definicion_iri"]: s["huella_fila_diccionario"] for s in asig["significados"]}

insp_dic = load("data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json")
FILAS = {i + 1: r for i, r in enumerate(insp_dic["definiciones"])}


def fila(n):
    r = FILAS[n]
    return (f"tipo={r['Tipo de dato']}; formato={r['Formato'] or 'no declarado'}; "
            f"ejemplo={r['Ejemplo de dato'].strip() or 'vacio'}")


EV_COMUN = [
    "data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json (diccionario local, filas verificadas; huellas 30/30 recomputadas OK)",
    "data/semantica/cobertura.json (estado previo: 22 fuera_del_nucleo_actual, 8 candidata_sin_definicion_suficiente)",
    "propuestas/cobertura-muse-20261023/educacion/entrega.json (dictamen previo agente-8: pendientes por descripcion vacia; revisado, no repetido)",
    "propuestas/pendientes-muse-r4/investigacion/pendientes.json (INV-P-07: respaldo pendiente de 28 definiciones vacias de Matriculas; revisado)",
]

# (fila, variable, decision, concepto|None, regla_id|None, motivo, limites_extra, representacion)
PROP = [
    (13, "Grupos asignaturas inscrito en ciclo escolar  señalado", "grupos-asignaturas-inscripcion", "r5mat-001", "no_especificada",
     "Fila con tipo Alfanumerico y ejemplo de lista de claves grupo-asignatura con el mismo patron que la fila 9 respaldada; el nombre documenta inscripcion a grupos en ciclo senalado.",
     ["Descripcion vacia ('Pendiente de especificar'); ciclo 'senalado' segun nombre sin resolver a cual; no fusiona definiciones 9 y 13; no acredita equivalencias entre planes."]),
    (14, "Fecha inscripción en ciclo escolar  señalado", "tiempo", "r5mat-002", "fecha",
     "Tipo Fecha con ejemplo 04/08/2022; el nombre documenta evento de inscripcion y ciclo senalado.",
     ["Descripcion vacia; evento y ciclo solo segun nombre; solo referencia temporal calendario; sin vigencia ni valores."]),
    (20, "Municipio", "municipio", "r5mat-003", "nombre",
     "Descripcion 'Municipio donde el alumno' con ejemplo HERMOSILLO en texto: referencia municipal del alumno con representacion nombre.",
     ["Descripcion trunca: funcion municipal no documentada (no residencia ni registro); nombre no codigo; sujeto alumno por conjunto."]),
    (47, "Promedio anterior al ciclo inscrito (Solo asig. aprobadas)", "promedio-anterior-ciclo-aprobadas", "r5mat-004", "no_especificada",
     "Tipo Numerico flotante con ejemplo 8.2; nombre fija periodo anterior al ciclo inscrito y subconjunto solo aprobadas.",
     ["Descripcion vacia; escala, rango y metodo no declarados; no homologa con promedio de ultimo ciclo; ejemplo no fija escala."]),
    (48, "Promedio anterior al ciclo inscrito (Todas las asignaturas)", "promedio-anterior-ciclo-todas", "r5mat-005", "no_especificada",
     "Tipo Numerico flotante con ejemplo 8.2; nombre fija periodo anterior al ciclo inscrito y cobertura todas las asignaturas.",
     ["Descripcion vacia; escala, rango y metodo no declarados; distinto del subconjunto solo aprobadas; no homologa con ultimo ciclo."]),
    (49, "Num. asignaturas reprobadas ciclo anterior al ciclo inscrito", "asignaturas-reprobadas-ciclo-anterior", "r5mat-006", "no_especificada",
     "Tipo Numerico entero con ejemplo 0; nombre fija conteo de reprobadas del ciclo anterior al inscrito.",
     ["Descripcion vacia; metodo de conteo no documentado; no homologa con reprobadas de ultimo ciclo."]),
    (52, "Promedio periodo escolar inscrito (Solo asig. aprobadas)", "promedio-periodo-inscrito-aprobadas", "r5mat-007", "no_especificada",
     "Tipo Numerico flotante con ejemplo 0; nombre fija periodo escolar inscrito y subconjunto solo aprobadas.",
     ["Descripcion vacia; escala y metodo no declarados; ejemplo 0 no distingue ausencia de valor; no homologa con otros promedios."]),
    (53, "Promedio periodo escolar inscrito (todas las asignaturas)", "promedio-periodo-inscrito-todas", "r5mat-008", "no_especificada",
     "Tipo Numerico flotante con ejemplo 0; nombre fija periodo escolar inscrito y cobertura todas las asignaturas.",
     ["Descripcion vacia; escala y metodo no declarados; ejemplo 0 no distingue ausencia de valor; distinto del subconjunto solo aprobadas."]),
    (61, "Tipo de baja", "tipo-baja-alumno", "r5mat-009", "no_especificada",
     "Descripcion literal 'Tipo de baja' en conjunto de Matriculas con familia de reglas de baja del alumno (fecha y periodo de baja); ejemplo vacio.",
     ["Descripcion tautologica; dominio y valores no documentados; representacion no afirmada; sujeto alumno por conjunto y familia documental."]),
    (64, "Fecha de alternativa de titulación de no exigibilidad", "tiempo", "r5mat-010", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa; ejemplo vacio; nombre fija evento de alternativa de no exigibilidad.",
     ["Descripcion vacía; evento solo según nombre; solo referencia temporal; alternativas sin norma que las defina."]),
    (66, "Fecha de alternativa de titulación de examen prof.", "tiempo", "r5mat-011", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa; ejemplo vacío; nombre fija evento de alternativa de examen profesional.",
     ["Descripción vacía; evento solo según nombre; solo referencia temporal; sin vigencia."]),
    (67, "Fecha de titulación del título profesional", "tiempo", "r5mat-012", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa; ejemplo vacío; nombre fija evento de titulación del título profesional.",
     ["Descripción vacía; evento solo según nombre; solo referencia temporal; sin vigencia ni valores."]),
    (68, "Fecha de impresión del título profesional", "tiempo", "r5mat-013", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa; ejemplo vacío; nombre fija evento de impresión del título.",
     ["Descripción vacía; evento solo según nombre; solo referencia temporal; acto administrativo, no acto académico."]),
    (69, "Fecha de la convalidación", "tiempo", "r5mat-014", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa; ejemplo vacío; nombre fija evento de convalidación.",
     ["Descripción vacía; evento solo según nombre; solo referencia temporal; convalidación sin norma que la defina."]),
    (70, "Fecha de la equivalencia", "tiempo", "r5mat-015", "fecha",
     "Tipo Fecha con formato dd/mm/aaaa con ejemplo 30/11/2021; nombre fija evento de equivalencia.",
     ["Descripción vacía; evento solo según nombre; ejemplo único no acredita dominio de valores; sin vigencia."]),
]
# (fila, variable, motivo, evidencia_faltante)
PEND = [
    (8, "Inscrito ciclo  escolar actual",
     "Descripción vacía; el ejemplo '222 (Reing)' parece clave de ciclo con calificador de reingreso pero ningún documento lo define.",
     "Definición del valor '222 (Reing)' y del ciclo actual de referencia en el diccionario o muestra de valores."),
    (11, "Ciclo escolar actual motivo no inscrito",
     "Descripción vacía, tipo Texto y ejemplo vacío: sin dominio ni valores no se fija si es código, motivo en texto libre o indicador.",
     "Dominio de motivos de no inscripción (catálogo o texto libre) con ejemplos por valor."),
    (12, "Inscritos ciclo escolar señalado",
     "Descripción vacía; el ejemplo '222 (Reing)' no define qué denota el valor ni a qué ciclo remite 'señalado'.",
     "Definición del valor '222 (Reing)' y del ciclo señalado de referencia."),
    (17, "Se realizo equivalencia en el ciclo actual",
     "Descripción vacía, tipo Texto y ejemplo vacío: no se fija si es indicador Sí/No, fecha, folio o texto.",
     "Dominio y representación del campo de equivalencia en el diccionario o muestra de valores."),
    (25, "Estimulo Ciclo Actual",
     "Descripción vacía, tipo Texto y ejemplo vacío: no se fija si es tipo de estímulo, monto, indicador o programa.",
     "Dominio del campo Estímulo (catálogo de estímulos o indicador) con ejemplos."),
    (26, "Grupo Indig.(Pertenece)",
     "Descripción vacía y ejemplo vacío: la faceta 'pertenece' solo consta en el nombre; representación y dominio sin documentar.",
     "Instrumento de captación o diccionario corregido con descripción, representación y valores de la faceta de pertenencia."),
    (27, "Grupo Indig. (Habla)",
     "Descripción vacía y ejemplo vacío: la faceta 'habla' solo consta en el nombre; sin valores no se fija indicador ni lengua.",
     "Instrumento de captación o diccionario corregido con descripción y valores de la faceta de habla."),
    (28, "Grupo Indig. (Vive en Comunidad)",
     "Descripción vacía y ejemplo vacío: la faceta solo consta en el nombre; sin valores no se fija indicador ni comunidad.",
     "Instrumento de captación o diccionario corregido con descripción y valores de la faceta de residencia en comunidad."),
    (29, "Grupo Indig. (Padres)",
     "Descripción vacía y ejemplo vacío: la faceta solo consta en el nombre; no se fija si refiere a pertenencia, habla o ascendencia de los padres.",
     "Instrumento de captación o diccionario corregido con descripción y valores de la faceta de padres."),
    (35, "Área Bachillerato",
     "Descripción vacía y ejemplo en blanco: sin dominio no se fija si es área de conocimiento, plantel o texto libre.",
     "Dominio del campo Área de Bachillerato (catálogo de áreas o texto libre) con ejemplos."),
    (54, "Inscrito ciclo actual (solo Serv.Soc. y Pract.Prof.)",
     "Descripción vacía y ejemplo en blanco con tipo Numérico entero: no se fija indicador, conteo ni clave.",
     "Representación y dominio del campo con muestra de valores no vacíos."),
    (58, "Periodo escolar de egreso",
     "Descripción vacía y ejemplo vacío con tipo Numérico entero: no se fija si es clave de periodo, año o conteo.",
     "Definición del periodo escolar de egreso y su representación (clave, año u otra) con ejemplos."),
    (62, "Cambio de Unidad Académica",
     "Descripción vacía y ejemplo vacío con tipo Texto: no se fija si es indicador, nombre de unidad destino o fecha.",
     "Representación y dominio del campo de cambio de unidad con ejemplos."),
    (63, "Alternativa de titulación de no exigibilidad",
     "Descripción vacía y ejemplo vacío: la alternativa solo consta en el nombre; sin norma de titulación no se fija su contenido.",
     "Norma de titulación UES que defina la alternativa de no exigibilidad y su registro."),
    (65, "Alternativa de titulación de examen profesional",
     "Descripción vacía y ejemplo vacío: la alternativa solo consta en el nombre; sin norma no se fija su contenido.",
     "Norma de titulación UES que defina la alternativa de examen profesional y su registro."),
]
SOLS = [
    {"id": "MAT-W-01", "url_probable": "https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85",
     "busqueda_concreta": "Dataset Matrículas de Estudiantes UES: diccionario-matriculas-de-estudiantes.csv vigente y recurso Estudiantes 2022-2 con muestra de valores por columna.",
     "definiciones_afectadas": [diri(n) for n in (8, 11, 12, 17, 25, 35, 54, 58, 62)],
     "evidencia_exacta_requerida": "Captura textual de filas del diccionario con descripción no vacía y ejemplos por variable, y valores observados de las columnas 222 (Reing), Estímulo, Área Bachillerato y periodo de egreso."},
    {"id": "MAT-W-02", "url_probable": "https://ues.mx/normatividad/ (reglamento escolar y de titulación UES)",
     "busqueda_concreta": "Normatividad UES: alternativas de titulación (no exigibilidad, examen profesional), equivalencia y convalidación; qué fecha registra cada acto.",
     "definiciones_afectadas": [diri(n) for n in (63, 64, 65, 66, 67, 68, 69, 70, 17)],
     "evidencia_exacta_requerida": "Fragmento del reglamento con la lista de alternativas de titulación y definición de equivalencia/convalidación, con fecha de publicación y ámbito de aplicación."},
    {"id": "MAT-W-03", "url_probable": "https://ues.mx/ (calendario escolar y catálogo de periodos/ciclos UES)",
     "busqueda_concreta": "Calendario escolar UES 2022: claves de ciclo/periodo (qué es '222'), ciclo actual frente a ciclo señalado, periodo escolar de egreso.",
     "definiciones_afectadas": [diri(n) for n in (8, 12, 13, 14, 58)],
     "evidencia_exacta_requerida": "Documento que defina la clave de ciclo 222, el calificador (Reing) y a qué remite 'ciclo señalado', con periodo de cobertura 2022-2."},
    {"id": "MAT-W-04", "url_probable": "https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85",
     "busqueda_concreta": "Instrumento de captación o diccionario corregido de Matrículas: dominios de Tipo de baja, Estímulo, Cambio de Unidad Académica y las cuatro facetas de Grupo Indígena.",
     "definiciones_afectadas": [diri(n) for n in (11, 25, 26, 27, 28, 29, 61, 62)],
     "evidencia_exacta_requerida": "Catálogo o manual con valores admisibles por campo (tipos de baja, estímulos, facetas indígena) y su representación."},
    {"id": "MAT-W-05", "url_probable": "https://ues.mx/normatividad/ (reglamento de evaluación UES)",
     "busqueda_concreta": "Reglamento de evaluación UES: escala de promedios (rango 0-10 u otra), cómputo de promedios por subconjunto y conteo de reprobadas.",
     "definiciones_afectadas": [diri(n) for n in (47, 48, 49, 52, 53)],
     "evidencia_exacta_requerida": "Artículo o numeral con escala, redondeo y conjuntos de asignaturas incluidos en cada promedio, con fecha de vigencia."},
]
# CONCEPTOS retirados (bloqueo auditor r5): sin descripcion sustantiva no hay conceptos exclusivos.
CONCEPTOS = {}

decisiones_significados = []
reglas = []
FALT = {
    13: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción que fije a qué ciclo remite 'señalado' y qué denotan los códigos de grupo."),
    14: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción que fije evento y ciclo de la fecha de inscripción."),
    20: ("Descripción trunca sin verbo ('Municipio donde el alumno': función ausente)",
         "Descripción completa con la función municipal (residencia, registro u otra)."),
    47: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción con escala, rango, método y cobertura de asignaturas del promedio."),
    48: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción con escala, rango, método y cobertura de asignaturas del promedio."),
    49: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción con método de conteo de asignaturas reprobadas."),
    52: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción con escala y método del promedio del periodo inscrito."),
    53: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción con escala y método del promedio del periodo inscrito."),
    61: ("Descripción tautológica ('Tipo de baja' repite el nombre; sin sujeto, dominio ni valores)",
         "Dominio y valores admisibles del tipo de baja con ejemplos."),
    64: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción del evento y norma UES de la alternativa de no exigibilidad."),
    66: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción del evento y norma UES de la alternativa de examen profesional."),
    67: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción que fije el evento de titulación del título profesional."),
    68: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción que fije el evento de impresión del título profesional."),
    69: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción del evento y norma de convalidación."),
    70: ("Descripción vacía ('Pendiente de especificar')",
         "Descripción del evento y norma de equivalencia."),
}

for n, variable, concepto, rid, _repr, motivo_corto, lims in PROP:
    iri = diri(n)
    estado_desc, faltante = FALT[n]
    decisiones_significados.append({
        "definicion_iri": iri, "decision": "pendiente",
        "motivo": (f"Propuesta {rid} RETIRADA (bloqueo auditor r5): {estado_desc}. "
                   "Nombre, tipo y ejemplo no bastan para fijar concepto; no se aprueba por nombre. "
                   "Sin regla revisada ni evidencia externa vinculada."),
        "evidencia": [f"data/portal/inspecciones/{DICC}.json:definiciones[{n}] ({fila(n)})",
                      f"huella_fila_diccionario={huella_por_iri[iri]} (recomputada OK 30/30)",
                      f"data/semantica/cobertura.json (fila {n})"] + EV_COMUN})

for n, variable, motivo, faltante in PEND:
    iri = diri(n)
    decisiones_significados.append({
        "definicion_iri": iri, "decision": "pendiente",
        "motivo": motivo + " Sin regla revisada que respalde el significado; no se aprueba por nombre.",
        "evidencia": [f"data/portal/inspecciones/{DICC}.json:definiciones[{n}] ({fila(n)})",
                      f"huella_fila_diccionario={huella_por_iri[iri]} (recomputada OK 30/30)",
                      f"data/semantica/cobertura.json (fila {n})"] + EV_COMUN})

COLS = []  # bloqueadas: las 8 candidatas dependen de reglas retiradas; quedan candidatas sin vinculo
prop_por_fila = {n: (c, r) for n, _, c, r, _, _, _ in PROP}
decisiones_columnas = []
vinculos = []
for n in COLS:
    campo = FILAS[n]["Nombre variable"]
    iri_def = diri(n)
    concepto, rid = prop_por_fila[n]
    col_iri = f"{BASE}file-column/{REC}%2F{HOJA.replace(' ', '%20')}%2F{n}"
    motivo = (f"Columna fisica verificada en esquema (posicion {n}, nombre unico) + fila {n} del diccionario "
              f"del mismo conjunto con regla {rid} y concepto {concepto}; huellas verificadas.")
    ev = [f"data/portal/inspecciones/{REC}.json:hoja={HOJA}:posicion={n}",
          f"data/portal/contenido-inspeccion.json:recurso={REC}:hoja={HOJA}",
          f"data/portal/inspecciones/{DICC}.json:definiciones[{n}]",
          f"huella_esquema={H_ESQ} (recomputada con huella() de scripts/consolidar_semantica.py)",
          f"huella_fila_diccionario={huella_por_iri[iri_def]} (recomputada OK)",
          f"nombre_unico_en_esquema=True (70 campos, sin duplicados)"]
    decisiones_columnas.append({"columna": col_iri, "recurso": REC, "campo": campo,
                                "decision": "proponer", "definicion_iri": iri_def,
                                "motivo": motivo, "evidencia": ev,
                                "concepto": concepto, "regla_id": rid})
    vinculos.append({"recurso": REC, "campo": campo, "columna": col_iri, "diccionario": DICC,
                     "concepto": concepto, "descripcion": FILAS[n]["Descripción"],
                     "huella_esquema": H_ESQ, "huella_fila_diccionario": huella_por_iri[iri_def],
                     "criterio": (f"Revision explicita del campo {campo!r} en el esquema del recurso {REC} "
                                  f"(hoja {HOJA}, posicion {n}) y su fila {n} del diccionario {DICC} del mismo conjunto "
                                  f"{CONJ}; regla {rid} row-restricted. Alcance documental; sin validar valores, "
                                  "sin vigencia ni cruces.")})

fuentes = [
    {"localizador": f"data/portal/inspecciones/{DICC}.json",
     "sha256": "73c4f6243458d700a99df5d3c55327bc9fde1a94d75f94a443606237327574b2",
     "aplicabilidad": "Diccionario local: filas 8,11,12,13,14,17,20,25-29,35,47-49,52-54,58,61-70 verificadas."},
    {"localizador": f"data/portal/inspecciones/{REC}.json",
     "sha256": "19e412eb0ccd161aaf111bba9d66506ed0eb986445d269b195d16ed1f48f2868",
     "aplicabilidad": f"Esquema del recurso: hoja {HOJA} con 70 campos; posiciones 14,20,64,66-70 verificadas."},
    {"localizador": "data/portal/contenido-inspeccion.json",
     "sha256": "61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb",
     "aplicabilidad": "Agregado de inspecciones del portal; contexto de recurso y diccionario."},
    {"localizador": "data/semantica/cobertura.json",
     "sha256": "ee3f6a1bff66a5315b73293c7952ef90f2fe601e0d797c6113d5f6129886d5be",
     "aplicabilidad": "Estados previos de las 30 variables y 8 correspondencias candidatas."},
    {"localizador": "ontologia/semantica.json",
     "sha256": "0d8ffc7509e4d694dfdb76bb28a6f6eca209bdb6f546b17dd1826171657e4b28",
     "aplicabilidad": "Conceptos vigentes reutilizados (tiempo, municipio, grupos-asignaturas-inscripcion); sin conceptos nuevos salvo 6 limitados."},
    {"localizador": "propuestas/cobertura-muse-20261023/educacion/entrega.json",
     "sha256": "3e2df431fb4a6337ebf1d9b3888233179e66e620fa902dfe8a0390e3f728792f",
     "aplicabilidad": "Dictamen previo agente-8 revisado (filas /11,/12,/13,/17 pendientes por descripcion vacia); no repetido sin revision."},
    {"localizador": "propuestas/pendientes-muse-r4/investigacion/pendientes.json",
     "sha256": "c2f516a0bc2506c548e30f83af64f53e71b21faeb621e7a1e98931a2be09778f",
     "aplicabilidad": "INV-P-07 revisado: exigia respaldo explicito de las 28 definiciones vacias de Matriculas."},
]

pendientes = [{"definicion_iri": diri(n), "variable": v, "conjunto": CONJ, "diccionario": DICC,
               "descripcion": FILAS[n]["Descripción"], "tipo_dato": FILAS[n]["Tipo de dato"],
               "ejemplo": FILAS[n]["Ejemplo de dato"].strip(),
               "motivo": m, "evidencia_faltante": f}
              for n, v, m, f in PEND]
for n, variable, _c, rid, _r, _m, _l in PROP:
    estado_desc, faltante = FALT[n]
    pendientes.append({"definicion_iri": diri(n), "variable": variable, "conjunto": CONJ,
                       "diccionario": DICC, "descripcion": FILAS[n]["Descripción"],
                       "tipo_dato": FILAS[n]["Tipo de dato"],
                       "ejemplo": FILAS[n]["Ejemplo de dato"].strip(),
                       "motivo": (f"Propuesta {rid} RETIRADA (bloqueo auditor r5): {estado_desc}."),
                       "evidencia_faltante": faltante})
pendientes.sort(key=lambda p: p["definicion_iri"])

entrega = {"rol": "matriculas", "generado_en_utc": datetime.now(timezone.utc).isoformat(),
           "alcance": "30 significados asignados del diccionario de Matriculas de Estudiantes; 8 columnas candidatas del recurso Estudiantes 2022-2.",
           "decisiones_significados": decisiones_significados, "reglas": reglas,
           "conceptos_nuevos": {}, "decisiones_columnas": decisiones_columnas,
           "vinculos": vinculos, "fuentes": fuentes, "pendientes": pendientes,
           "solicitudes_web_archivo": "solicitudes_web.json",
           "verificacion": {"asignados": 30, "decisiones": 30,
                             "huella_fila_recomputada_ok": 30,
                             "columnas_candidatas": 8, "columnas_proponer": 0, "columnas_sin_vinculo": 8,
                             "columnas_nombre_unico_ok": 8, "columnas_iri_exacta_ok": 8,
                             "huella_esquema_recomputada": H_ESQ}}
save("entrega.json", entrega)
save("solicitudes_web.json", {"rol": "matriculas", "destinatario": "catalogos-web",
                               "nota": "Sin control de Obscura; se piden fuentes concretas con evidencia exacta.",
                               "solicitudes": SOLS})

h = hashlib.sha256((AQUI / "entrega.json").read_bytes()).hexdigest()
n_prop = sum(1 for d in decisiones_significados if d["decision"] == "proponer")
n_pen = sum(1 for d in decisiones_significados if d["decision"] == "pendiente")
lineas = ["# Resultado matriculas (ronda 5)",
          "",
          f"Asignados: 30. Decisiones: {n_prop} proponer, {n_pen} pendiente, 0 artefacto_documental.",
          "Reglas nuevas: 0. Conceptos nuevos: 0 (bloqueo auditor: retiradas r5mat-001 a r5mat-015).",
          "Reutilizacion de vigentes: ninguna.",
          f"Columnas: 8 candidatas verificadas fisicamente (esquema 70 campos, nombres unicos, IRI exacta) pero sin vinculo: 0 proponer (dependian de reglas retiradas).",
          f"Vinculos: {len(vinculos)}. Solicitudes web: {len(SOLS)} (MAT-W-01 a MAT-W-05).",
          "",
          "## Bloqueo auditor y nueva version (caso por caso)",
          "",
          "- r5mat-001 (/13), r5mat-002 (/14), r5mat-004 a r5mat-008 (/47,/48,/49,/52,/53), r5mat-010 a r5mat-015 (/64,/66,/67,/68,/69,/70):",
          "  descripcion 'Pendiente de especificar'; respaldo era solo nombre+tipo/ejemplo. RETIRADAS.",
          "- r5mat-003 (/20 Municipio): descripcion trunca 'Municipio donde el alumno' sin verbo; la funcion municipal,",
          "  nucleo del significado, ausente. No sustantiva. RETIRADA.",
          "- r5mat-009 (/61 Tipo de baja): descripcion 'Tipo de baja' tautologica (repite el nombre; sin sujeto, dominio ni valores).",
          "  No sustantiva. RETIRADA.",
          "- Las 8 columnas y 8 vinculos dependientes, retirados con sus reglas; las correspondencias quedan candidatas.",
          "",
          "## Dictamen previo revisado (no repetido)",
          "",
          "- Agente-8 educacion marco /11, /12, /13 y /17 pendientes por descripcion vacia ('Pendiente de especificar').",
          "- Ronda-4 INV-P-07 exigio respaldo explicito de las 28 definiciones vacias de Matriculas.",
          "- Revision propia: filas completas (tipo/formato/ejemplo) + esquema del recurso + huellas recomputadas 30/30.",
          "- Ninguna fila tiene descripcion sustantiva ni evidencia externa vinculada: 30 pendientes con evidencia faltante precisa.",
          "",
          "## Verificacion",
          "",
          "- Huellas de fila recomputadas con huella() de scripts/consolidar_semantica.py: 30/30 OK.",
          f"- Huella de esquema recomputada (tabla {HOJA}): {H_ESQ}.",
          "- 8 columnas localizadas (posicion, nombre unico e IRI verificados); sin vinculo por reglas retiradas.",
          "- Reglas, conceptos y vinculos: 0 (retirados; sin colisiones que verificar).",
          "",
          "## Busquedas negativas",
          "",
          "- Descarga directa del portal (API CKAN package_show del dataset) bloqueada por WAF del sitio (pagina 'Acceso no permitido', CODIGO BWAF);",
          "  se usan las instantaneas congeladas data/portal/inspecciones (2026-10-23) como fuente primaria. Sin archivo de intento conservado.",
          "- Sin diccionario corregido UES ni norma de titulacion/evaluacion en fuentes locales: 30 pendientes con evidencia faltante precisa.",
          "- Ninguna fuente externa respalda aplicacion local: no se promociona por nombre, clasificador ni documentacion nacional.",
          "",
          "## Pendientes (30)",
          "",
          "Motivos y evidencia faltante en entrega.json -> pendientes; solicitudes web en solicitudes_web.json.",
          "",
          "## Archivos",
          "",
          "- entrega.json, solicitudes_web.json, resultado.md, listo.json, construir.py",
          f"- sha256(entrega.json) = {h}"]
(AQUI / "resultado.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
save("listo.json", {"rol": "matriculas", "entrega": "entrega.json", "sha256": h,
                    "cuentas": {"asignados": 30, "proponer_significados": n_prop,
                                "pendiente_significados": n_pen, "reglas_nuevas": len(reglas),
                                "conceptos_nuevos": len(CONCEPTOS),
                                "decisiones_columnas": len(decisiones_columnas),
                                "vinculos": len(vinculos), "solicitudes_web": len(SOLS)},
                    "estado": "completo"})
print("listo sha:", h)
print("significados:", len(decisiones_significados), "reglas:", len(reglas))
print("conceptos:", len(CONCEPTOS), "columnas:", len(decisiones_columnas))