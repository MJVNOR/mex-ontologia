"""Genera entrega.json + entrega.md + listo.json para significados-salud (85 IDs).

Solo escribe dentro de propuestas/cierre-brechas-post-r6/significados-salud/.
Cita evidencia preservada sin modificarla. SHAs calculados sobre bytes en cada corrida.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parents[1]  # significados-salud/
EV = HERE / "evidencia"

FECHA = "2026-10-24"


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def ev_rel(p):
    return str(p.relative_to(ROOT)).replace("\\", "/")


ASIG = json.loads((HERE / "asignacion.json").read_text(encoding="utf-8-sig"))
LOC_DEF = json.loads((ROOT / "data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json").read_text(encoding="utf-8"))
LOC_NAC = json.loads((ROOT / "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json").read_text(encoding="utf-8"))

MANUAL = "propuestas/pendientes-muse-r6/salud/evidencia/Manual_Llenado_CD_CMF_2022_20220930.pdf"
INS_DEF = "data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json"
INS_NAC = "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
DESC_DEF = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_defun_2022/diccionario_datos_defunciones_registradas_2022.xlsx"
CATZIP_DEF = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/CATALOGOS_DEFUN_2022.zip"
DESCZIP_DEF = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/DESCRIPTOR_CAMPOS_DEFUN_2022.zip"
DESC_SINAC = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx"
DESCZIP_SINAC = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/sinac_descriptores_2020_2025.zip"
IDX_DEF = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/dgis_da_defunciones_2026-10-24.html"
IDX_NAC = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/dgis_da_nacimientos_2026-10-24.html"
CAT = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/cat_defun_2022/catalogos/"


def cat_csv(name):
    rows = list(csv.reader((ROOT / (CAT + name)).read_text(encoding="utf-8").splitlines()))
    return rows


# Verificacion de coherencia citada (solo lectura; no acredita identidad)
OCUP = cat_csv("ocupacion.csv")
OCUP_LITS = {r[1] for r in OCUP[1:] if len(r) > 1}
CAUSA = cat_csv("causa_defuncion.csv")
U071 = [r for r in CAUSA if r and r[0].strip().upper() == "U071"]

LIM_BASE = [
    "Alcance simultaneo por conjunto+diccionario+fila+huella; no autoriza cruces, joins ni identidad de catalogos.",
    "Descriptor/catalogos DGIS citados son del registro nacional (DEFUN 2022 / SINAC 2020-2025), no del extracto Sonora del portal; la coincidencia de nombres o valores no sustituye la tabla del publicador.",
    "Negativas y ausencias acotadas a lo revisado el 2026-10-24; no ausencia universal.",
]

# variable defunciones -> (mnemonico_nacional, rango/catalogo, hallazgo_nuevo)
DEF_NEW = {
    "EDADGESTACIONAL": ("sem_gest", "22..42,88,99 + edadgest.csv (22..42 semanas, 88 No aplica, 99 No especificadas)",
        "Nuevo 2026-10-24: codebook nacional 2022 documenta sentinelas 88/99; ejemplo local vacio no contrasta. Resta: unidad de la columna portal + tabla publicador columna<->campo."),
    "CLAVEOCUPACIONHABITUAL": ("ocupacion", "011..100,110,997,998,999 (3 digitos) + ocupacion.csv",
        "Nuevo 2026-10-24: ejemplo local '4' (1 digito) NO encaja en el patron nacional de 3 digitos; indicio de recodificacion local. Resta: codebook del publicador + tabla columna<->campo."),
    "CLAVEOCUPACIONHABITUALD": ("ocupacion", "ocupacion.csv completo (011..110,997,998,999)",
        "Nuevo 2026-10-24: literal 'NO OCUPADO, JUBILADO O PENSIONADO' ausente en ocupacion.csv nacional. Resta: codebook del publicador + tabla columna<->campo."),
    "TRABAJAACTUALMENTE": ("cond_act / ocurr_trab", "condicion_actividad 1,2,8,9 (2=No) y ocurrio_trabajo 1,2,8,9 (2=No)",
        "Nuevo 2026-10-24: ambiguedad de dos campos candidatos confirmada tambien a nivel nacional (actividad vs ocurrio en trabajo). Ejemplo '2'=No en ambos. Resta: fijar campo + tabla del publicador."),
    "TRABAJAACTUALMENTED": ("cond_act / ocurr_trab", "2=No en ambos catalogos nacionales",
        "Nuevo 2026-10-24: 'NO' coherente con 2=No nacional, pero sin fijar campo. Resta: tabla del publicador."),
    "AFILIACION": ("derechohab", "1..9,99 + derechohabiencia.csv (2=IMSS)",
        "Nuevo 2026-10-24: ejemplo '2' coherente con 2=IMSS nacional y con AFILIACIOND='IMSS'. Resta: tabla del publicador columna<->campo."),
    "AFILIACIOND": ("derechohab", "derechohabiencia.csv (2=IMSS)",
        "Nuevo 2026-10-24: 'IMSS' = CVE 2 nacional; coherencia par numerico/D verificada. Resta: tabla del publicador."),
    "SITIODEFUNCION": ("sitio_ocur", "1..12,99 + sitio_ocurrencia.csv (1-9 institucion, 10 via publica, 11 hogar, 12 otro, 99 no especificado)",
        "Nuevo 2026-10-24: el catalogo nacional mezcla institucion (1-9) y sitio (10-12); ejemplo '3'=IMSS explica la confusion sitio-vs-institucion del manual (preg 19 cita 10/11/12/99). Resta: tabla del publicador."),
    "SITIODEFUNCIOND": ("sitio_ocur", "sitio_ocurrencia.csv (3=IMSS)",
        "Nuevo 2026-10-24: 'IMSS' = CVE 3 nacional dentro del campo sitio; confirma el diagnostico de captura cruzada pero no lo acredita. Resta: tabla del publicador."),
    "CLUES": (None, "descriptor nacional 2022: 73 campos, ninguno de clave de establecimiento",
        "Nuevo 2026-10-24 (negativo): el descriptor nacional DEFUN 2022 tampoco documenta CLUES; sin contraparte nacional. Resta: definicion + tabla del publicador."),
    "MUERTEACCIDENTALVIOLENTA": ("natviole", "1,2,8 + accidental_violenta.csv (2=No)",
        "Nuevo 2026-10-24: ejemplo '2'=No coherente nacional. Resta: tabla del publicador."),
    "MUERTEACCIDENTALVIOLENTAD": ("natviole", "accidental_violenta.csv (2=No)",
        "Nuevo 2026-10-24: 'NO' coherente con 2=No nacional. Resta: tabla del publicador."),
    "INTENCIONEVENTO": ("presunto", "1..5,8 + presunta_defuncion_violenta.csv (8=No aplica para muerte natural)",
        "Nuevo 2026-10-24: ejemplo '8' SI es mapeable a nivel nacional (8=No aplica para muerte natural); antes sin mapa. Resta: fijar que 8 local = 8 nacional via tabla del publicador."),
    "INTENCIONEVENTOD": ("presunto", "presunta_defuncion_violenta.csv (8=No aplica para muerte natural)",
        "Nuevo 2026-10-24: 'NO APLICA' coherente con CVE 8 nacional; cuadra mejor con el catalogo que con el manual (que no trae ese literal). Resta: tabla del publicador."),
    "CIECAUSABASICA": ("causa_def", "A000..Y899 + causa_defuncion.csv (U071='COVID-19, virus identificado')",
        "Nuevo 2026-10-24: U071 presente en el catalogo nacional 2022 con formato admitido; edicion CIE del recurso sigue sin declarar. Resta: edicion aplicable + tabla del publicador."),
    "CIECAUSABASICAD": ("causa_def", "causa_defuncion.csv (U071='COVID-19, virus identificado')",
        "Nuevo 2026-10-24: literal local 'COVID-19, VIRUS IDENTIFICADO' coincide (modulo mayusculas) con la entrada U071 nacional 2022. Resta: edicion aplicable + tabla del publicador."),
    "CAUSAPROPIAEMBARAZO": ("complicaro", "1,2,8,9 + complicaron_embarazo.csv (8=No aplica)",
        "Nuevo 2026-10-24: ejemplo '8' mapeable nacional (8=No aplica). Resta: tabla del publicador."),
    "CAUSAPROPIAEMBARAZOD": ("complicaro", "complicaron_embarazo.csv (8=No aplica)",
        "Nuevo 2026-10-24: 'NO APLICA' coherente con CVE 8 nacional. Resta: tabla del publicador."),
    "SITIOOCURRENCIALESION": ("lugar_ocur", "0..9,88 + lugar_ocurrencia.csv (88=No aplica para muerte natural)",
        "Nuevo 2026-10-24: ejemplo '88' SI es mapeable nacional (88=No aplica para muerte natural); antes sin mapa. Resta: tabla del publicador."),
    "SITIOOCURRENCIALESIOND": ("lugar_ocur", "lugar_ocurrencia.csv (88=No aplica para muerte natural)",
        "Nuevo 2026-10-24: 'NO APLICA' coherente con CVE 88 nacional. Resta: tabla del publicador."),
    "PARENTESCOAGRESORD": ("par_agre", "1..72,88,99 + parentesco_agresor.csv (71=Sin parentesco, 72=Ninguno, 88=No aplica, 99=No especificado)",
        "Nuevo 2026-10-24: 'NO APLICA' cuadra con CVE 88 nacional; el catalogo trae mas opciones que el manual ('ninguno'/'Se ignora'). Resta: tabla del publicador."),
    "ENTIDADOCURRENCIA": ("ent_ocurr / ent_ocules", "ent_ocurr 01..32,99 (sin 88) vs ent_ocules 01..35,88,99 (con 88)",
        "Nuevo 2026-10-24: ejemplo local '88' solo existe en el ambito lesion (ent_ocules), no en ocurrencia; ambiguedad de ambito confirmada a nivel nacional. Resta: fijar ambito + tabla del publicador."),
    "ENTIDADOCURRENCIAD": ("ent_ocurr / ent_ocules", "88 solo en ent_ocules (lesion)",
        "Nuevo 2026-10-24: 'NO APLICA' no fija ambito (ocurrencia vs lesion). Resta: fijar ambito + tabla del publicador."),
    "MUNICIPIOOCURRENCIA": ("mun_ocurr / mun_ocules", "mun_ocurr 001..570,999; mun_ocules 001..570,888,999",
        "Nuevo 2026-10-24: ejemplo local '997' fuera de AMBOS rangos nacionales; indicio de recodificacion local. Resta: codebook del publicador + tabla columna<->campo."),
    "MUNICIPIOOCURRENCIAD": ("mun_ocurr / mun_ocules", "rangos nacionales sin 997",
        "Nuevo 2026-10-24: par 997/'NO APLICA' sin contraparte nacional. Resta: codebook + tabla del publicador."),
    "LOCALIDADOCURRENCIA": ("loc_ocurr / loc_ocules", "loc_ocurr 0001..6999,777,9999; loc_ocules 0001..6999,777,8888,9999",
        "Nuevo 2026-10-24: ejemplo local '9997' fuera de AMBOS rangos nacionales; indicio de recodificacion local. Resta: codebook del publicador + tabla columna<->campo."),
    "LOCALIDADOCURRENCIAD": ("loc_ocurr / loc_ocules", "rangos nacionales sin 9997",
        "Nuevo 2026-10-24: par 9997/'NO APLICA' sin contraparte nacional. Resta: codebook + tabla del publicador."),
    "CERTIFICADOPOR": ("cond_cert", "1..5,8,9 + certificante.csv (3=Otro medico)",
        "Nuevo 2026-10-24: ejemplo '3' coherente con 3=Otro medico nacional y con CERTIFICADOPORD='OTRO MEDICO'. Resta: tabla del publicador."),
    "CERTIFICADOPORD": ("cond_cert", "certificante.csv (3=Otro medico)",
        "Nuevo 2026-10-24: literal coherente con CVE 3 nacional (modulo mayusculas). Resta: tabla del publicador."),
    "FECHACERTIFICACION": ("dia_cert/mes_cert/anio_cert", "dia 1..31,99; mes 1..12,99; anio (anio de estadistica)",
        "Nuevo 2026-10-24: campos de fecha de certificacion existen a nivel nacional (separados); formato local 'Fecha' distinto. Resta: formato + tabla del publicador."),
    "JURISDICCION_CLUES": (None, "descriptor nacional 2022 sin campo de jurisdiccion; manual SEED sin pregunta",
        "Nuevo 2026-10-24 (negativo doble): sin contraparte nacional ni pregunta en el manual; ejemplo local '6'. Resta: definicion + tabla del publicador."),
    "JURISDICCION_CLUESD": (None, "sin contraparte nacional ni pregunta en el manual",
        "Nuevo 2026-10-24 (negativo doble): 'SAN LUIS RIO COLORADO' sin fuente que lo defina como jurisdiccion de CLUES. Resta: definicion + tabla del publicador."),
}

SINAC_DESC = {
    "ORDENNACIMIENTO": (19, "Orden de nacimiento del reci\u00e9n nacido vivo. El valor 99 corresponde a No Especificado.", None),
    "ATENCIONPRENATAL": (20, "La madre recibi\u00f3 atenci\u00f3n prenatal.", "SI_NO"),
    "TRIMESTREPRIMERCONSULTA": (21, "Trimestre en el que la madre recibi\u00f3 la primer consulta prenatal.", "TRIMESTRE_PRIMER_CONSULTA"),
    "SOBREVIVIOPARTO": (23, "La madre sobrevivi\u00f3 al parto.", "SI_NO"),
    "AFILIACION": (24, "C\u00f3digo y descripci\u00f3n de Afiliaci\u00f3n a los Servicios de Salud (derechohabiencia).", "AFILIACION_CERTIFICADOS"),
    "INTERRUMPIOESTUDIOS": (26, "Interrumpi\u00f3 estudios por motivo del embarazo.", "SI_NO"),
    "CLAVEOCUPACIONHABITUAL": (27, "C\u00f3digo de la ocupaci\u00f3n habitual de la madre.", "OCUPACION_HABITUAL"),
    "APGAR": (36, "Calificaci\u00f3n obtenida del nacido vivo a los cinco minutos del nacimiento. El valor 99 corresponde a No Especificado.", None),
    "SILVERMAN": (37, "Calificaci\u00f3n obtenida del nacido a los diez minutos del nacimiento. El valor 99 corresponde a No Especificado.", None),
    "TAMIZAUDITIVO": (38, "Se le realiz\u00f3 el tamiz auditivo.", "SI_NO"),
    "VACUNA_BCG": (39, "Se le aplic\u00f3 la vacuna BCG.", "SI_NO"),
    "VACUNAHEPATITIS_B": (40, "Se le aplic\u00f3 la vacuna Hepatitis B.", "SI_NO"),
    "VITAMINA_A": (41, "Se le aplic\u00f3 la vitamina A.", "SI_NO"),
    "VITAMINA_K": (42, "Se le aplic\u00f3 la vitamina K.", "SI_NO"),
    "PRODUCTOEMBARAZO": (43, "Identificaci\u00f3n del tipo de productos extra\u00eddos.", "PRODUCTO_EMBARAZO"),
    "ORDENPRODUCTO": (44, "N\u00famero de producto de acuerdo al orden de extracci\u00f3n del evento actual.", None),
    "TOTALPRODUCTOS": (45, "Total de productos extra\u00eddos del evento actual.", None),
    "CODIGOCIEANOMALIA1": (46, "C\u00f3digo de la CIE10 que corresponde a la anomal\u00eda cong\u00e9nita, enfermedad o lesi\u00f3n del nacido vivo. El valor 0000 corresponde a no especificado.", "DIAGNOSTICOS"),
    "CODIGOCIEANOMALIA2": (47, "Segundo c\u00f3digo de la CIE10 que corresponde a la anomal\u00eda cong\u00e9nita, enfermedad o lesi\u00f3n del nacido vivo.", "DIAGNOSTICOS"),
    "RESOLUCIONEMBARAZO": (51, "Procedimiento utilizado en el nacimiento.", "RESOLUCION_EMBARAZO"),
    "UTILIZOFORCEPS": (52, "Se utilizaron f\u00f3rceps durante el procedimiento.", "UTILIZO_FORCEPS"),
    "CLUES": (49, "Clave \u00danica de Establecimientos en Salud del sitio de atenci\u00f3n del parto descrita por el prestador de servicio.", "ESTABLECIMIENTOS_SALUD"),
    "TIEMPOTRASLADO": (50, "Tiempo de traslado desde su hogar hasta el sitio de atenci\u00f3n del parto.", None),
    "PERSONALATENDIO": (54, "Persona que atendi\u00f3 el parto.", "PERSONA_ATENDIO_PARTO"),
    "TIPOMEDICOATENDIO": (55, "Tipo de m\u00e9dico que atendi\u00f3 el parto.", "TIPO_MEDICO"),
    "CERTIFICADOPOR": (59, "Tipo de profesional de la salud que certifica el nacimiento.", "NACIMIENTO_CERTIFICADO_POR"),
    "CLUESCERTIFICA": (60, "Clave \u00danica de Establecimiento en Salud que certifica el parto.", "ESTABLECIMIENTOS_SALUD"),
    "ENTIDADFEDERATIVACERTIFICA": (61, "Entidad federativa del establecimiento de salud que certifica el parto.", "ENTIDADES"),
    "MUNICIPIOCERTIFICA": (62, "Municipio o delegaci\u00f3n del establecimiento de salud que certifica el parto.", "MUNICIPIOS"),
    "LOCALIDADCERTIFICA": (63, "Localidad del establecimiento de salud que certifica el parto.", "LOCALIDADES"),
    "FECHACERTIFICADO": (64, "Fecha de la certificaci\u00f3n.", None),
}

MANUAL_LOC = {}
for c in ASIG["casos"]:
    for e in c.get("evidencia", []):
        if e["ruta"] == MANUAL:
            MANUAL_LOC[c["definicion_iri"]] = (e["localizador"], e["afirmacion_soportada"])
            break


def build():
    decisiones = []
    for c in ASIG["casos"]:
        iri = c["definicion_iri"]
        var = c["variable"]
        is_def = "12f684e9" in iri
        n = int(iri.split("%2F")[1])
        loc = LOC_DEF if is_def else LOC_NAC
        d = loc["definiciones"][n - 1]
        loc_idx = f"/definiciones/{n - 1}"
        fila = (f"Fila local: Nombre={d.get('Nombre variable')}, Tipo={d.get('Tipo de dato')}, "
                f"Ejemplo={d.get('Ejemplo de dato')!r}, Descripcion={d.get('Descripci\u00f3n')}, Catalogo={d.get('Cat\u00e1logo de referencia')!r}")
        ins = INS_DEF if is_def else INS_NAC
        ev = [{"ruta": ins, "sha256": sha(ins), "localizador": loc_idx, "afirmacion_soportada": fila}]
        if is_def:
            mnem, rango, hallazgo = DEF_NEW[var]
            ev.append({"ruta": DESC_DEF, "sha256": sha(DESC_DEF),
                       "localizador": f"campo {mnem}" if mnem else "73 campos (NOMBRE_CAMPO/NEM\u00d3NICO/RANGO_CLAVES)",
                       "afirmacion_soportada": f"Diccionario nacional DEFUN 2022: {mnem or 'sin campo'}; rango {rango}."})
            csvs = {"EDADGESTACIONAL": "edadgest.csv", "CLAVEOCUPACIONHABITUAL": "ocupacion.csv",
                    "CLAVEOCUPACIONHABITUALD": "ocupacion.csv", "AFILIACION": "derechohabiencia.csv",
                    "AFILIACIOND": "derechohabiencia.csv", "SITIODEFUNCION": "sitio_ocurrencia.csv",
                    "SITIODEFUNCIOND": "sitio_ocurrencia.csv", "MUERTEACCIDENTALVIOLENTA": "accidental_violenta.csv",
                    "MUERTEACCIDENTALVIOLENTAD": "accidental_violenta.csv", "INTENCIONEVENTO": "presunta_defuncion_violenta.csv",
                    "INTENCIONEVENTOD": "presunta_defuncion_violenta.csv", "CIECAUSABASICA": "causa_defuncion.csv",
                    "CIECAUSABASICAD": "causa_defuncion.csv", "CAUSAPROPIAEMBARAZO": "complicaron_embarazo.csv",
                    "CAUSAPROPIAEMBARAZOD": "complicaron_embarazo.csv", "SITIOOCURRENCIALESION": "lugar_ocurrencia.csv",
                    "SITIOOCURRENCIALESIOND": "lugar_ocurrencia.csv", "PARENTESCOAGRESORD": "parentesco_agresor.csv",
                    "CERTIFICADOPOR": "certificante.csv", "CERTIFICADOPORD": "certificante.csv",
                    "TRABAJAACTUALMENTE": "condicion_actividad.csv", "TRABAJAACTUALMENTED": "condicion_actividad.csv"}.get(var)
            if csvs:
                ev.append({"ruta": CAT + csvs, "sha256": sha(CAT + csvs),
                           "localizador": f"columna CVE/DESCRIP de {csvs}",
                           "afirmacion_soportada": f"Catalogo nacional DEFUN 2022 {csvs}: valores CVE citados en el motivo."})
            if iri in MANUAL_LOC:
                locm, afirm = MANUAL_LOC[iri]
                ev.append({"ruta": MANUAL, "sha256": sha(MANUAL), "localizador": locm,
                           "afirmacion_soportada": f"Veredicto previo por ID (R6/post-R6, sin re-examen): {afirm[:280]}"})
            motivo = (f"sigue_pendiente: {hallazgo} Fuente primaria nacional nueva (DGIS Datos Abiertos DEFUN 2022) "
                      f"contrastada contra la fila (huella {c['huella_fila_diccionario'][:12]}...): los nombres de campo nacionales "
                      f"difieren de la columna portal y no hay tabla del publicador que los vincule al recurso 6f39fc5d.")
            falt = (f"Nota del publicador que vincule el recurso 6f39fc5d (2022-01-01 a 2022-09-22) con el campo {mnem if mnem else '(sin campo nacional identificado)'} del "
                    f"registro nacional DEFUN 2022 para esta fila (huella {c['huella_fila_diccionario'][:12]}...), con tabla "
                    f"columna<->campo y codebook aplicable.")
        else:
            if var in SINAC_DESC:
                nid, desc, catal = SINAC_DESC[var]
                cat_txt = catal if catal else "sin cat\u00e1logo declarado"
                ev.append({"ruta": DESC_SINAC, "sha256": sha(DESC_SINAC),
                           "localizador": f"Hoja1 fila ID={nid}, VARIABLE={var}",
                           "afirmacion_soportada": f"Descriptor nacional SINAC 2020-2025 (A1='SINAC 2020-2025', cubre el periodo del recurso): {var} = {desc} Catalogo: {cat_txt}."})
                motivo = (f"sigue_pendiente: Nuevo 2026-10-24: el descriptor nacional SINAC 2020-2025 trae la variable con nombre "
                          f"EXACTO ({var}, IDnac={nid}), descripcion y catalogo ({cat_txt}); vigencia 2020-2025 cubre el recurso 46977217 "
                          f"(2022-01-01 a 2022-09-26). No promociona: el descriptor solo nombra el catalogo (contenido no publicado ahi) y el "
                          f"publicador del extracto Sonora no publica tabla columna<->variable; los valores D y el codebook aplicado al "
                          f"recurso siguen sin fuente vinculada (huella {c['huella_fila_diccionario'][:12]}...).")
                falt = (f"Nota del publicador que vincule el recurso 46977217 con la variable {var} (IDnac={nid}) del descriptor SINAC "
                        f"2020-2025 para esta fila (huella {c['huella_fila_diccionario'][:12]}...), con contenido publicado del catalogo "
                        f"({cat_txt}) y tabla columna<->variable.")
            else:
                ev.append({"ruta": DESC_SINAC, "sha256": sha(DESC_SINAC),
                           "localizador": "Hoja1, 65 variables base (ID 1..64); busqueda exacta del nombre",
                           "afirmacion_soportada": f"Negativa acotada: '{var}' no figura entre las 65 variables del descriptor nacional SINAC 2020-2025."})
                motivo = (f"sigue_pendiente: Nuevo 2026-10-24 (negativo): '{var}' no tiene contraparte ni en el descriptor nacional SINAC "
                          f"2020-2025 (65 variables, ID 1..64, sin columnas D ni ANOMALIACIE*) ni en las primarias ya examinadas "
                          f"(Modelo 2015, INEGI 2017, DOF CEN). Resta la descripcion publicada de la columna en el diccionario 22202305 o "
                          f"nota equivalente del publicador (huella {c['huella_fila_diccionario'][:12]}...).")
                falt = (f"Descripcion publicada de {var} en el diccionario 22202305 o nota del publicador que la vincule al recurso "
                        f"46977217 (huella {c['huella_fila_diccionario'][:12]}...), con codebook si aplica.")
        decisiones.append({"id": iri, "estado": "sigue_pendiente", "original": c, "motivo": motivo,
                           "evidencia_faltante": falt, "evidencia": ev, "limites": LIM_BASE})
    return decisiones


def main():
    decisiones = build()
    ids = [d["id"] for d in decisiones]
    assert len(decisiones) == 85 and len(set(ids)) == 85
    assert set(ids) == {c["definicion_iri"] for c in ASIG["casos"]}
    for d in decisiones:
        for e in d["evidencia"]:
            assert e["sha256"] == sha(e["ruta"]), e["ruta"]

    fuentes = [
        {"ruta": INS_DEF, "sha256": sha(INS_DEF), "url": None, "fecha_consulta": FECHA,
         "localizador": "/definiciones (80 filas; /definiciones/<fila-1> por ID)",
         "aplicabilidad": "Fila local verificada: tipo/ejemplo/descripcion por ID (defunciones)."},
        {"ruta": INS_NAC, "sha256": sha(INS_NAC), "url": None, "fecha_consulta": FECHA,
         "localizador": "/definiciones (106 filas; /definiciones/<fila-1> por ID)",
         "aplicabilidad": "Fila local verificada: tipo/ejemplo/descripcion por ID (nacimientos)."},
        {"ruta": MANUAL, "sha256": sha(MANUAL), "url": "http://www.dgis.salud.gob.mx/descargas/seed/pdf/Manual_Llenado_CD_CMF_2022_20220930.pdf",
         "fecha_consulta": FECHA, "localizador": "portada p1 (Modelo 2022); preguntas por ID citadas en decisiones",
         "aplicabilidad": "Veredictos previos por ID reutilizados como referencia, sin re-examen."},
        {"ruta": DESC_DEF, "sha256": sha(DESC_DEF),
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/defunciones/descriptores/DESCRIPTOR_CAMPOS_DEFUN_2022.zip?v=2023.11.10",
         "fecha_consulta": FECHA, "localizador": "NOMBRE_CAMPO/NEM\u00d3NICO/CAT\u00c1LOGO/RANGO_CLAVES (73 campos)",
         "aplicabilidad": "Diccionario nacional DEFUN 2022 nuevo frente a post-R6; rangos por campo."},
        {"ruta": CATZIP_DEF, "sha256": sha(CATZIP_DEF),
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/defunciones/catalogos/CATALOGOS_DEFUN_2022.zip?v=2023.11.10",
         "fecha_consulta": FECHA, "localizador": "catalogos/*.csv (CVE/DESCRIP) + modelo ER",
         "aplicabilidad": "Codebooks nacionales DEFUN 2022 nuevos frente a post-R6; contraste por ID."},
        {"ruta": DESC_SINAC, "sha256": sha(DESC_SINAC),
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip?V=2026.07.09",
         "fecha_consulta": FECHA, "localizador": "Hoja1 A1='SINAC 2020-2025'; filas ID 1..64 (ID/VARIABLE/DESCRIPCI\u00d3N/Cat\u00e1logo)",
         "aplicabilidad": "Descriptor nacional SINAC 2020-2025 nuevo frente a post-R6; vigencia explicita que cubre el recurso 2022."},
        {"ruta": DESCZIP_SINAC, "sha256": sha(DESCZIP_SINAC),
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip?V=2026.07.09",
         "fecha_consulta": FECHA, "localizador": "Descriptores/sinac_descriptores_2020_2025.zip (contenedor del xlsx)",
         "aplicabilidad": "Paquete original descargado; preserva cadena de custodia del xlsx."},
        {"ruta": IDX_DEF, "sha256": sha(IDX_DEF),
         "url": "http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_defunciones_gobmx.html",
         "fecha_consulta": FECHA, "localizador": "tablas Catalogos/Descriptores/Registros 1998-2024; fila 2022",
         "aplicabilidad": "Pagina DGIS que publica los descriptores/catalogos 2022 (ult. mod. 2025-12-22)."},
        {"ruta": IDX_NAC, "sha256": sha(IDX_NAC),
         "url": "http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_nacimientos_gobmx.html",
         "fecha_consulta": FECHA, "localizador": "filas 18-20: descriptores 2020-2025, catalogos 2020-2023, registros 2022",
         "aplicabilidad": "Pagina DGIS que publica descriptores SINAC 2020-2025 (ult. mod. 2026-07-09)."},
    ]
    entrega = {"tarea": "significados-salud", "tipo": "significados", "decisiones": decisiones, "fuentes": fuentes,
               "novedades_frente_a_investigacion_previa": [
                   "DGIS Datos Abiertos DEFUN 2022 (descriptor 73 campos + 45 catalogos CSV): no examinado en R6/post-R6; contrastado por ID contra las 32 columnas de defunciones.",
                   "Coherencias nuevas defunciones: 2=IMSS (AFILIACION), 3=Otro medico (CERTIFICADOPOR), 8/88 sentinelas mapeables (INTENCIONEVENTO, CAUSAPROPIAEMBARAZO, SITIOOCURRENCIALESION), U071 en causa_defuncion.csv, sitio_ocur 1..12 que explica confusion sitio-vs-institucion.",
                   "Incoherencias nuevas defunciones: CLAVEOCUPACIONHABITUAL '4' fuera del patron nacional 011..110; MUNICIPIOOCURRENCIA '997' y LOCALIDADOCURRENCIA '9997' fuera de ambos rangos nacionales; CLUES y JURISDICCION_CLUES sin campo nacional.",
                   "Descriptor nacional SINAC 2020-2025 (65 variables, ID 1..64, vigencia explicita): no examinado en R6/post-R6; 31/53 variables con nombre exacto, descripcion y nombre de catalogo; 22/53 sin contraparte (20 D + ANOMALIACIE1/2).",
                   "Ningun ID promociona: los codebooks citados son nacionales y el publicador del extracto Sonora no publica tabla columna<->campo ni codebook del recurso; criterio de aceptacion intacto.",
               ],
               "busquedas_limitadas": [
                   "websearch 2026-10-24 (herramienta web nativa): DGIS SEED codebook -> pagina Datos Abiertos Defunciones con catalogos/descriptores 2022 (nuevo); SINAC codebook -> solo clinica (Apgar/Silverman) sin valor de publicador.",
                   "websearch 2026-10-24: datos.gob.mx Informacion Sobre Nacimientos Sonora -> sin diccionario publicado (negativa acotada al buscador).",
                   "webfetch 2026-10-24: da_defunciones_gobmx.html y da_nacimientos_gobmx.html (HTTP 200, copias locales con SHA); Datos_Abiertos indice (terminos de uso).",
                   "Descargas HTTP 200 2026-10-24: CATALOGOS_DEFUN_2022.zip (468325 B), DESCRIPTOR_CAMPOS_DEFUN_2022.zip (13051 B), sinac_descriptores_2020_2025.zip (13347 B); SHAs verificados contra bytes.",
                   "peticiones-web.json escrita 2026-10-24 para el agente web-obscura (navegacion compartida no manejada desde este agente); carpeta web-obscura sin resultados al momento de generar.",
                   "No se descargo sinac_catalogos_2020_2023.zip (23.2 Mb): contenido de catalogos SINAC sin tabla del publicador que lo vincule al recurso; descarga diferida hasta que web-obscura o el publicador aporte el vinculo.",
               ]}
    (HERE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = ["# Cierre de brechas — significados-salud (85 IDs)", "",
          "Tarea `significados-salud`. Fecha: 2026-10-24. 0 propuestas / 85 siguen pendientes.",
          "Ningun cambio al nucleo; solo propuestas revisables en esta carpeta.", "",
          "## Novedad real frente a post-R6 (no repetida)", "",
          "1. DGIS Datos Abiertos DEFUN 2022: descriptor de 73 campos + 45 catalogos CSV,",
          "   contrastados por ID contra las 32 columnas de defunciones.",
          "2. Descriptor nacional SINAC 2020-2025 (vigencia explicita, 65 variables ID 1..64):",
          "   31/53 variables de nacimientos con nombre exacto + descripcion + catalogo;",
          "   22/53 sin contraparte (20 columnas D + ANOMALIACIE1/2).",
          "3. Resultado: coherencias nuevas (2=IMSS, 3=Otro medico, 8/88 sentinelas, U071,",
          "   sitio_ocur 1..12) e incoherencias nuevas ('4' fuera de 011..110, '997'/'9997'",
          "   fuera de rangos, CLUES/JURISDICCION sin campo nacional). Nada promociona:",

          "   falta la tabla del publicador columna<->campo y el codebook del recurso.", "",
          "## Brecha exacta que subsiste (por grupo)", "",
          "- Defunciones (32): nota del publicador que vincule el recurso 6f39fc5d con el",
          "  campo nacional DEFUN 2022 citado por ID (tabla columna<->campo + codebook).",
          "- Nacimientos con nombre exacto (31): nota del publicador que vincule el recurso",
          "  46977217 con la variable IDnac citada (contenido del catalogo + tabla).",
          "- Nacimientos sin contraparte (22): descripcion publicada de la columna D o nota",
          "  equivalente del publicador.", "",
          "## Archivos", "",
          "- `entrega.json` — 85 decisiones + 9 fuentes con SHA verificado contra bytes.",
          "- `evidencia/` — zips descargados, descriptores xlsx, catalogos csv, paginas DGIS,",
          "  `peticiones-web.json` (al inicio) y este generador en `temporales/`.",
          "- `listo.json` — conteos y SHAs.", ""]
    (HERE / "entrega.md").write_text("\n".join(md), encoding="utf-8")

    archivos = [{"ruta": ev_rel(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in sorted((HERE).rglob("*")) if p.is_file() and p.name != "listo.json"]
    listo = {"tarea": "significados-salud", "archivos": archivos,
             "conteos": {"decisiones": len(decisiones), "propuesta_resolucion": sum(1 for d in decisiones if d["estado"] == "propuesta_resolucion"),
                         "sigue_pendiente": sum(1 for d in decisiones if d["estado"] == "sigue_pendiente")}}
    (HERE / "listo.json").write_text(json.dumps(listo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Verificacion final
    e2 = json.loads((HERE / "entrega.json").read_text(encoding="utf-8"))
    assert len(e2["decisiones"]) == 85 and len({d["id"] for d in e2["decisiones"]}) == 85
    assert set(e2["decisiones"][0].keys()) == {"id", "estado", "original", "motivo", "evidencia_faltante", "evidencia", "limites"}
    l2 = json.loads((HERE / "listo.json").read_text(encoding="utf-8"))
    for a in l2["archivos"]:
        assert a["sha256"] == hashlib.sha256((ROOT / a["ruta"]).read_bytes()).hexdigest(), a["ruta"]
    print(f"OK: {len(e2['decisiones'])} decisiones, {len(l2['archivos'])} archivos, SHAs verificados.")


if __name__ == "__main__":
    main()
