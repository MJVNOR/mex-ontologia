"""Genera entrega.json + alineacion.json + entrega.md + cierrelisto.json
para correspondencias-b, conforme al dictamen de auditoria
propuestas/cierre-brechas-post-r6/auditoria-correspondencias/dictamen.json
(veredicto: requiere_correccion).

Registro SEPARADO estructural: estado
'par_estructural_revisado_significado_pendiente', sin concepto aprobado,
sin cambio de estatus semantico, sin joins/identidad de catalogos,
sin vigencia del vinculo, sin promocion semantica. NO aplicable a
vinculos_documentales_revisados: el core (scripts/consolidar_semantica.py:271)
exige variable 'respaldada_por_definicion'.

Solo escribe dentro de propuestas/cierre-brechas-post-r6/correspondencias-b/.
Serializado con json.dumps; SHA-256 recomputados desde bytes.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
FECHA = "2026-10-24"
ESTADO = "par_estructural_revisado_significado_pendiente"
DICTAMEN = "propuestas/cierre-brechas-post-r6/auditoria-correspondencias/dictamen.json"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))


asig = load("propuestas/cierre-brechas-post-r6/correspondencias-b/asignacion.json")
casos = {c["columna"]: c for c in asig["casos"]}
assert len(casos) == 10, len(casos)

dic_est = load("data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json")
rec_est = load("data/portal/inspecciones/58f2d5a6-0432-48f1-8a35-a5efcce78bac.json")
dic_seed = load("data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json")
rec_seed = load("data/portal/inspecciones/6f39fc5d-e097-4954-8cd7-10e8f9dea541.json")
dic_egr = load("data/portal/inspecciones/f89137ba-d82e-44fe-80c7-cc355f09f9f5.json")
rec_egr = load("data/portal/inspecciones/ad6f77b8-569d-4826-8ce0-3c6efddcb098.json")
pkg_mat = load("propuestas/investigacion-post-r6/matriculas/evidencia/package_matriculas.json")
pkg_def = load("propuestas/pendientes-muse-r6/salud/evidencia/package_defunciones.json")
pkg_egr = load("propuestas/investigacion-post-r6/diversos/evidencia/ckan-egresos.json")

INS_D_EST = "data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json"
INS_R_EST = "data/portal/inspecciones/58f2d5a6-0432-48f1-8a35-a5efcce78bac.json"
INS_D_SEED = "data/portal/inspecciones/12f684e9-f4d5-4714-933d-aa153a812174.json"
INS_R_SEED = "data/portal/inspecciones/6f39fc5d-e097-4954-8cd7-10e8f9dea541.json"
INS_D_EGR = "data/portal/inspecciones/f89137ba-d82e-44fe-80c7-cc355f09f9f5.json"
INS_R_EGR = "data/portal/inspecciones/ad6f77b8-569d-4826-8ce0-3c6efddcb098.json"
DIST = "propuestas/investigacion-post-r6/matriculas/evidencia/distribuciones.json"
XLSX = "propuestas/investigacion-post-r6/matriculas/evidencia/Matriculas-2022-2.xlsx"
PKG_MAT = "propuestas/investigacion-post-r6/matriculas/evidencia/package_matriculas.json"
PKG_DEF = "propuestas/pendientes-muse-r6/salud/evidencia/package_defunciones.json"
CKAN_EGR = "propuestas/investigacion-post-r6/diversos/evidencia/ckan-egresos.json"
COB = "data/semantica/cobertura.json"
PREV = "reports/investigacion-post-r6.json"


def ev(ruta, localizador, afirmacion):
    return {"ruta": ruta, "sha256": sha(ruta),
            "localizador": localizador, "afirmacion_soportada": afirmacion}


def ctx(ruta, localizador, afirmacion, rol):
    d = ev(ruta, localizador, afirmacion)
    d["rol"] = rol
    return d


F_EST_D = ev(INS_D_EST, "/definiciones (filas 67-70: 0-based 66-69)",
             "Diccionario 8c0e76ff filas 67-70: Tipo Fecha, Formato dd/mm/aaaa, "
             "Descripcion 'Pendiente de especificar' (fila 70 con ejemplo 30/11/2021).")
F_EST_R = ev(INS_R_EST, "tablas[0].hoja='Estudiantes 2022-2', campos pos 67-70",
             "Recurso 58f2d5a6 hoja 'Estudiantes 2022-2' (70 columnas): ids literales "
             "de columnas 67-70 identicos byte a byte a las variables del diccionario.")
F_SEED_D = ev(INS_D_SEED, "/definiciones (0-based 37,71,72,73,74)",
              "Diccionario 12f684e9 filas 38/72/73/74/75: CLUES Alfanumerico ej SRIMS000915; "
              "MUNICIPIOOCURRENCIA Numerico ej 997; MUNICIPIOOCURRENCIAD Texto ej NO APLICA; "
              "LOCALIDADOCURRENCIA Numerico ej 9997; LOCALIDADOCURRENCIAD Texto ej NO APLICA; "
              "todas Descripcion 'Pendiente de especificar'.")
F_SEED_R = ev(INS_R_SEED, "tablas[0].hoja='SEED 20 09 22', campos pos 38/72/73/74/75",
              "Recurso 6f39fc5d hoja 'SEED 20 09 22' (80 columnas): ids literales 38/72-75 "
              "identicos a las variables.")
F_EGR_D = ev(INS_D_EGR, "/definiciones/14",
             "Diccionario f89137ba fila 15: Total_Egresos, Numerico entero, ejemplo 2, "
             "Descripcion 'Total de urgencias atendidas', obligatoriedad Si.")
F_EGR_R = ev(INS_R_EGR, "tablas[0].hoja='Egresos Hospitalarios 2018-2022', campos[14] pos 15",
             "Recurso ad6f77b8 hoja 'Egresos Hospitalarios 2018-2022' (15 columnas): "
             "col 15 Total_Egresos.")
F_XLSX = ev(XLSX, "hoja 'Estudiantes 2022-2', 15212 filas x 70 columnas",
            "Recurso de datos autentico (fuente primaria): cabeceras = variables del "
            "diccionario; base fisica de las distribuciones.")
F_PKG_MAT = ev(PKG_MAT, "result.numero_variables=70; resources[1]: Matriculas - 2022 - 2 "
               "(start_date 2022-01-01, end_date 2022-06-01); resources[0]: diccionario",
               "Mismo conjunto CKAN e819466c: diccionario 8c0e76ff y recurso 58f2d5a6 "
               "co-publicados; conteo declarado 70.")
F_PKG_DEF = ev(PKG_DEF, "result.numero_variables=80; resources[] (Diccionario 12f684e9; "
               "Defunciones 2022 6f39fc5d; periodo 2022-01-01 a 2022-09-22)",
               "Mismo paquete CKAN: diccionario 12f684e9 y recurso 6f39fc5d "
               "co-publicados; conteo declarado 80; XLSX con datastore_active=false.")
F_CKAN_EGR = ev(CKAN_EGR, "result.numero_variables=15; resources[1] ad6f77b8 "
                "(2015-01-01 a 2022-12-31); Fuentes extras vacias",
                "Mismo conjunto CKAN 8993c917: diccionario f89137ba y recurso ad6f77b8 "
                "co-publicados; conteo declarado 15; sin metodologia publicada.")

C_DIST = ctx(DIST, "entradas filas 67/68/69/70 (derivado local del xlsx)",
             "Dominios empiricos: fila 67 (15211 nulos, 1 distinto '08/09/2018'); "
             "fila 69 (1333 no nulos, 354 distintos); fila 70 (239 no nulos, "
             "157 distintos); fila 68 vacia (15212 nulos).",
             "CONTEXTO: derivado local; compatible con Formato dd/mm/aaaa pero NO "
             "prueba directa del par columna-definicion.")
C_PREV = ctx(PREV, "decisiones por definicion_iri (169, 0 promociones)",
             "Investigacion previa: 10/10 significados siguen pendientes (matriculas: "
             "normas UES sin vinculo edicion-recurso-periodo; SEED: manual Modelo 2022 "
             "por ID con ambiguedades; egresos: contradiccion conservada).",
             "CONTEXTO: reporte derivado; registra el ultimo resultado por ID, NO "
             "prueba del par.")
C_COB = ctx(COB, "observaciones_revision id egresos-descripcion-urgencias",
            "Observacion vigente: nombre Total_Egresos vs descripcion 'Total de urgencias "
            "atendidas'; estado pendiente_aclaracion_o_revision; no interpretar como "
            "egresos ni urgencias.",
            "CONTEXTO: artefacto semantico local; fija el pendiente conservado, NO "
            "prueba del par.")

LIM = [
    "Registro separado 'par_estructural_revisado_significado_pendiente': sin concepto "
    "aprobado y sin cambio de estatus semantico (variables siguen "
    "'candidata_sin_definicion_suficiente' / 'candidata_por_nombre'; egresos "
    "'fuera_del_nucleo_actual').",
    "Sin joins, cruces, homologaciones, equivalencias ni identidad de catalogos.",
    "Sin vigencia nueva del vinculo: los periodos citados son metadatos del recurso "
    "CKAN, no del par; no inferir vigencia del nombre del archivo.",
    "Sin promocion semantica: descripciones 'Pendiente de especificar' y pendientes "
    "conservados (EGR 15 pendiente_aclaracion_o_revision; SEED ambiguedad "
    "general-vs-fetal; EST 68 sin muestra de valores).",
    "NO aplicable a vinculos_documentales_revisados: el core "
    "(scripts/consolidar_semantica.py:271) exige variable 'respaldada_por_definicion'.",
]

CRIT_EST = ("Nombre literal byte-identico + ordinal coincidente (pos N <-> fila N) en "
            "diccionario 8c0e76ff + recurso 58f2d5a6 del mismo conjunto CKAN "
            "co-publicado (conteo declarado 70 = conteo real 70; ver alineacion.json; "
            "2 desalineaciones ajenas a estos IDs en pos 21 y 32). Tipo/Formato Fecha "
            "dd/mm/aaaa declarados.")
CRIT_SEED = ("Nombre literal + ordinal coincidente (pos N <-> fila N) en diccionario "
             "12f684e9 + recurso 6f39fc5d del mismo paquete CKAN co-publicado "
             "(conteo declarado 80 = conteo real 80 y secuencia completa identica; ver "
             "alineacion.json). Sin acceso a valores (XLSX, datastore_active=false).")
CRIT_EGR = ("Nombre literal + ordinal coincidente (pos 15 <-> fila 15) en diccionario "
            "f89137ba + recurso ad6f77b8 del mismo conjunto CKAN co-publicado "
            "(conteo declarado 15 = conteo real 15 y secuencia completa identica; ver "
            "alineacion.json). La contradiccion descripcion-vs-titulo no rompe el par "
            "estructural; impide interpretar el sentido (conservado pendiente).")

decisiones = []


def propuesta(col, var, dicc, rec, huella, criterio):
    return {"columna": col, "variable": var,
            "diccionario": dicc, "recurso": rec,
            "huella_fila_diccionario": huella, "criterio": criterio,
            "estado_propuesto": ESTADO,
            "estado_semantico_actual": "candidata_por_nombre",
            "significado": "pendiente"}


def build(col, huella, evid, contexto, crit, faltante, motivo, concepto_anterior):
    c = casos[col]
    decisiones.append({
        "id": col,
        "estado": ESTADO,
        "estado_semantico_actual": "candidata_por_nombre",
        "significado": "pendiente",
        "original": c,
        "motivo": motivo,
        "evidencia_faltante": faltante,
        "evidencia": evid,
        "contexto": contexto,
        "propuesta": propuesta(col, c["variable"],
                               c["variable"].split("%2F")[0].rsplit("/", 1)[-1],
                               c["recurso"], huella, crit),
        "historial_propuesta_rechazada": {
            "estado_anterior": "propuesta_resolucion",
            "estado_propuesto_anterior": "documental_revisada",
            "concepto_propuesto_anterior": concepto_anterior,
            "dictamen": DICTAMEN,
            "veredicto": "requiere_correccion",
            "efecto": "registro inactivo como aprobacion; sustituido por el presente "
                      "registro estructural separado; se conserva solo como historial.",
        },
        "limites": LIM,
    })


EST67 = "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F67"
EST68 = "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F68"
EST69 = "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F69"
EST70 = "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F70"
S38 = "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F38"
S72 = "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F72"
S73 = "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F73"
S74 = "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F74"
S75 = "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F75"
EG15 = "https://example.org/mex-ontologi/file-column/ad6f77b8-569d-4826-8ce0-3c6efddcb098%2FEgresos%20Hospitalarios%202018-2022%2F15"

build(EST67, "de5cd0cf3209d047b3dbc8b3a76992f8a52c6e1f6d5b20ca452b762f6b10e993",
      [F_EST_D, F_EST_R, F_XLSX, F_PKG_MAT], [C_DIST, C_PREV], CRIT_EST,
      "Para el significado (pendiente): definicion del evento de titulacion aplicable "
      "al periodo del recurso + codebook de representacion de vacios.",
      "Estructural: nombre literal identico + pos 67 <-> fila 67, mismo conjunto; "
      "Tipo/Formato Fecha dd/mm/aaaa. Significado pendiente (descripcion 'Pendiente de "
      "especificar'; normas UES sin vinculo edicion-recurso-periodo). Registro separado "
      "condicionado; no aprobacion.", "tiempo")
build(EST68, "0475086a02e3cd9f2d50ded42b978d782edb3e1ea742601c0c0b40fec2e43d58",
      [F_EST_D, F_EST_R, F_XLSX, F_PKG_MAT], [C_DIST, C_PREV], CRIT_EST,
      "Para el significado (pendiente): definicion del evento de impresion aplicable al "
      "periodo + muestra de valores (columna vacia: sin dominio observable).",
      "Estructural: nombre literal identico + pos 68 <-> fila 68, mismo conjunto. "
      "Columna totalmente vacia: representacion no verificable. Significado pendiente. "
      "Registro separado condicionado; no aprobacion.", "tiempo")
build(EST69, "a0792669fb9fb33d8e517cc98ef71161b90ee12f10a620cfa84b647522a5c6c1",
      [F_EST_D, F_EST_R, F_XLSX, F_PKG_MAT], [C_DIST, C_PREV], CRIT_EST,
      "Para el significado (pendiente): definicion del evento de convalidacion aplicable "
      "al periodo (Reglamento 2023 posterior al dato; define proceso, no campo).",
      "Estructural: nombre literal identico + pos 69 <-> fila 69, mismo conjunto. "
      "Significado pendiente. Registro separado condicionado; no aprobacion.", "tiempo")
build(EST70, "1fe84a93ab498ab4d7dc47f0a54b4ad5278e0d9194e5cc00c06c3028927ff3b3",
      [F_EST_D, F_EST_R, F_XLSX, F_PKG_MAT], [C_DIST, C_PREV], CRIT_EST,
      "Para el significado (pendiente): definicion del evento de equivalencia aplicable "
      "al periodo (Reglamento 2023 posterior; Lineamientos abrogados).",
      "Estructural: nombre literal identico + pos 70 <-> fila 70, mismo conjunto. "
      "Significado pendiente. Registro separado condicionado; no aprobacion.", "tiempo")
build(S38, "1b32ad8dbecd8c74b4f0bfd3497c88a32c8b2f8590a4a9f42f2b10717804423b",
      [F_SEED_D, F_SEED_R, F_PKG_DEF], [C_PREV], CRIT_SEED,
      "Para el significado (pendiente): nota del publicador que vincule el recurso "
      "6f39fc5d con preg 19.2 / 9.2 (fetal) del Manual SEED Modelo 2022 "
      "(huella 1b32ad8d...), con tabla pregunta<->columna y formato verificable.",
      "Estructural: CLUES pos 38 <-> fila 38, mismo paquete. Dos preguntas CLUES "
      "candidatas (19.2 defuncion / 9.2 expulsion fetal): ambiguedad de significado "
      "conservada pendiente. Registro separado condicionado; no aprobacion.",
      "unidad-salud")
build(S72, "da9a0fcd2979fbcca215523a090a0332d76bfb531c9f92fecae3bd347819febf",
      [F_SEED_D, F_SEED_R, F_PKG_DEF], [C_PREV], CRIT_SEED,
      "Para el significado (pendiente): codebook con mapa numerico (ejemplo local 997) "
      "y vinculo pregunta<->columna (huella da9a0fcd...).",
      "Estructural: MUNICIPIOOCURRENCIA pos 72 <-> fila 72, mismo paquete. Sin codebook "
      "ni vinculo a pregunta del manual: significado pendiente.", "municipio")
build(S73, "45f58439a5c544c88713e5f5ba62c1a0ddf40f9aa6181a506e30f6d50a6e1b85",
      [F_SEED_D, F_SEED_R, F_PKG_DEF], [C_PREV], CRIT_SEED,
      "Para el significado (pendiente): codebook que defina el literal 'NO APLICA' como "
      "valor valido y su pregunta del manual (huella 45f58439...).",
      "Estructural: MUNICIPIOOCURRENCIAD pos 73 <-> fila 73, mismo paquete "
      "(contigua a /72 por posicion, sin afirmar vinculo semantico). Significado "
      "pendiente.", "municipio")
build(S74, "0485c56408609aa3a1cab7e67e8e7b1f0b4ee7cd6607fbe8c97de194423cac9d",
      [F_SEED_D, F_SEED_R, F_PKG_DEF], [C_PREV], CRIT_SEED,
      "Para el significado (pendiente): codebook con mapa numerico (ejemplo local 9997) "
      "y vinculo pregunta<->columna (huella 0485c564...).",
      "Estructural: LOCALIDADOCURRENCIA pos 74 <-> fila 74, mismo paquete. "
      "Significado pendiente.", "localidad")
build(S75, "6f76513d06bf1de37df4a91e3103ac0e3782913df200633ca0673e907e345bd4",
      [F_SEED_D, F_SEED_R, F_PKG_DEF], [C_PREV], CRIT_SEED,
      "Para el significado (pendiente): codebook que defina 'NO APLICA' y su pregunta "
      "del manual (huella 6f76513d...).",
      "Estructural: LOCALIDADOCURRENCIAD pos 75 <-> fila 75, mismo paquete "
      "(contigua a /74 por posicion, sin afirmar vinculo semantico). Significado "
      "pendiente.", "localidad")
build(EG15, "98c73e56ff407766447b52e08850d0b8669f6979145b4c66fac1f1f83aec9f05",
      [F_EGR_D, F_EGR_R, F_CKAN_EGR], [C_COB, C_PREV], CRIT_EGR,
      "Fe de erratas o diccionario corregido del publicador que fije que cuenta "
      "Total_Egresos (conjunto+diccionario+fila+huella citados); vale cualquier "
      "evidencia primaria inequivoca vinculada a la fila.",
      "Estructural: Total_Egresos pos 15 <-> fila 15, mismo conjunto. Contradiccion "
      "conservada (titulo de hoja 'Egresos Hospitalarios 2018-2022' vs descripcion "
      "'Total de urgencias atendidas'; subsistema GIIS-B014 separado). Sin interpretar "
      "el sentido (pendiente_aclaracion_o_revision vigente).", None)

assert [d["id"] for d in decisiones] == [c["columna"] for c in asig["casos"]]
assert len({d["id"] for d in decisiones}) == 10
for d in decisiones:
    assert "concepto" not in d["propuesta"]
    assert d["original"]["concepto"] == casos[d["id"]]["concepto"]
    assert d["propuesta"]["variable"] == d["original"]["variable"]

fuentes = [
    {"ruta": INS_D_EST, "sha256": sha(INS_D_EST), "url": None,
     "fecha_consulta": FECHA, "localizador": "/definiciones (filas 67-70)"},
    {"ruta": INS_R_EST, "sha256": sha(INS_R_EST), "url": None,
     "fecha_consulta": FECHA, "localizador": "tablas[0] hoja 'Estudiantes 2022-2'"},
    {"ruta": INS_D_SEED, "sha256": sha(INS_D_SEED), "url": None,
     "fecha_consulta": FECHA, "localizador": "/definiciones (filas 38/72-75)"},
    {"ruta": INS_R_SEED, "sha256": sha(INS_R_SEED), "url": None,
     "fecha_consulta": FECHA, "localizador": "tablas[0] hoja 'SEED 20 09 22'"},
    {"ruta": INS_D_EGR, "sha256": sha(INS_D_EGR), "url": None,
     "fecha_consulta": FECHA, "localizador": "/definiciones/14"},
    {"ruta": INS_R_EGR, "sha256": sha(INS_R_EGR), "url": None,
     "fecha_consulta": FECHA,
     "localizador": "tablas[0] hoja 'Egresos Hospitalarios 2018-2022'"},
    {"ruta": DIST, "sha256": sha(DIST), "url": None, "fecha_consulta": FECHA,
     "localizador": "entradas filas 67/68/69/70 (CONTEXTO, derivado local)"},
    {"ruta": XLSX, "sha256": sha(XLSX),
     "url": "https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65717dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx",
     "fecha_consulta": "2026-10-24",
     "localizador": "hoja 'Estudiantes 2022-2', 15212 filas x 70 columnas"},
    {"ruta": PKG_MAT, "sha256": sha(PKG_MAT),
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=e819466c-7282-46c5-84e9-65717dd8cc85",
     "fecha_consulta": "2026-10-24",
     "localizador": "result.numero_variables=70; resources[0..1]"},
    {"ruta": PKG_DEF, "sha256": sha(PKG_DEF), "url": None,
     "fecha_consulta": "2026-10-24",
     "localizador": "result.numero_variables=80; resources[] (dicc+recurso)"},
    {"ruta": CKAN_EGR, "sha256": sha(CKAN_EGR),
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=8993c917-47d8-4304-8141-5f481fe04301",
     "fecha_consulta": "2026-10-24", "localizador": "result.numero_variables=15"},
    {"ruta": COB, "sha256": sha(COB), "url": None, "fecha_consulta": FECHA,
     "localizador": "observaciones_revision id egresos-descripcion-urgencias (CONTEXTO)"},
    {"ruta": PREV, "sha256": sha(PREV), "url": None, "fecha_consulta": FECHA,
     "localizador": "decisiones por definicion_iri (CONTEXTO, 169 sin promocion)"},
]

entrega = {
    "tarea": "correspondencias-b",
    "tipo": "correspondencias",
    "correccion_auditoria": {
        "dictamen": DICTAMEN,
        "veredicto": "requiere_correccion",
        "cambios": "estado 'propuesta_resolucion'->'" + ESTADO + "'; "
                    "estado_propuesto 'documental_revisada'->'" + ESTADO + "'; "
                    "concepto retirado de propuesta (original preserva concepto); "
                    "estado_semantico_actual 'candidata_por_nombre' + significado "
                    "'pendiente' anadidos; distribuciones y reporte previo "
                    "recategorizados a contexto; historial de propuesta rechazada "
                    "guardado por ID; artefacto alineacion.json adjunto.",
        "no_aplica_a": "vinculos_documentales_revisados (core exige "
                       "'respaldada_por_definicion'; invariante no relajado).",
    },
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades_frente_a_investigacion_previa": [
        "Correccion estructural por dictamen de auditoria (requiere_correccion): "
        "ninguna de las 10 decisiones es aprobacion ni cambia estatus semantico; "
        "los 10 significados siguen pendientes como en la investigacion previa.",
        "Separacion de criterios por ID: par estructural (nombre+ordinal, mismo "
        "conjunto co-publicado) vs significado pendiente; sin homonimia entre "
        "catalogos como prueba (CLASIF 2129x28 y manual SEED por ID: lineas agotadas).",
        "Alineacion en secuencia completa verificada en alineacion.json: SEED 80/80 y "
        "Egresos 15/15 identicos; Estudiantes 70/70 con 2 desalineaciones ajenas a los "
        "IDs (pos 21 y 32 por espacios): NO se afirma 1:1 donde hay mismatch.",
        "Distribuciones empiricas y reports/investigacion-post-r6.json recategorizados "
        "a CONTEXTO (rol declarado): no son prueba directa del par.",
    ],
    "busquedas_limitadas": [
        "Sin fetches web nuevos: lineas agotadas en investigacion previa 2026-10-24; "
        "repetirlas presentaria datos conocidos como nuevos.",
        "Verificacion local SHA-256 desde bytes (python hashlib) el 2026-10-24; "
        "proveedor/herramienta por fuente en 'fuentes'.",
        "Peticiones web-obscura en peticiones-web.json; navegador compartido no "
        "manejado desde este agente; web-obscura con pistas que no cierran significado "
        "segun dictamen.",
        "Ningun error HTTP interpretado como inexistencia: no hubo fetches nuevos.",
    ],
}

out = HERE / "entrega.json"
out.write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------- alineacion.json ----------
def secuencia(nombres_dic, ids_rec):
    campos, difs = [], []
    for i, (v, c) in enumerate(zip(nombres_dic, ids_rec), 1):
        ok = (v == c)
        campos.append({"pos": i, "variable": v, "columna": c, "coincide": ok})
        if not ok:
            difs.append({"pos": i, "variable": v, "columna": c})
    return campos, difs


NOM_EST = [x["Nombre variable"] for x in dic_est["definiciones"]]
COL_EST = [x["id"] for x in rec_est["tablas"][0]["campos"]]
NOM_SEED = [x["Nombre variable"] for x in dic_seed["definiciones"]]
COL_SEED = [x["id"] for x in rec_seed["tablas"][0]["campos"]]
NOM_EGR = [x["Nombre variable"] for x in dic_egr["definiciones"]]
COL_EGR = [x["id"] for x in rec_egr["tablas"][0]["campos"]]

pares = []
for etiqueta, dicc_id, rec_id, hoja, noms, cols, pkg, declarado in [
    ("matriculas", "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d",
     "58f2d5a6-0432-48f1-8a35-a5efcce78bac", "Estudiantes 2022-2",
     NOM_EST, COL_EST, pkg_mat, 70),
    ("defunciones-seed", "12f684e9-f4d5-4714-933d-aa153a812174",
     "6f39fc5d-e097-4954-8cd7-10e8f9dea541", "SEED 20 09 22",
     NOM_SEED, COL_SEED, pkg_def, 80),
    ("egresos", "f89137ba-d82e-44fe-80c7-cc355f09f9f5",
     "ad6f77b8-569d-4826-8ce0-3c6efddcb098", "Egresos Hospitalarios 2018-2022",
     NOM_EGR, COL_EGR, pkg_egr, 15),
]:
    campos, difs = secuencia(noms, cols)
    real_dic, real_rec = len(noms), len(cols)
    declarado_raw = pkg.get("result", pkg).get("numero_variables", declarado)
    try:
        declarado_pkg = int(declarado_raw)
    except (TypeError, ValueError):
        declarado_pkg = declarado_raw
    pares.append({
        "conjunto": etiqueta,
        "diccionario": dicc_id,
        "recurso": rec_id,
        "hoja": hoja,
        "n_filas_diccionario_real": real_dic,
        "n_columnas_recurso_real": real_rec,
        "numero_variables_declarado_ckan": declarado_pkg,
        "numero_variables_declarado_literal": declarado_raw,
        "conteos_coherentes": (real_dic == real_rec == declarado_pkg),
        "campos": campos,
        "diferencias": difs,
        "afirmacion_1_1_en_secuencia_completa": (len(difs) == 0 and real_dic == real_rec),
    })

alineacion = {
    "tarea": "correspondencias-b",
    "fecha_utc": FECHA,
    "pares": pares,
    "fuentes_primarias": [
        {"ruta": r, "sha256": sha(r), "origen": o}
        for r, o in [
            (INS_D_EST, "portal CKAN preservado (inspeccion diccionario matriculas)"),
            (INS_R_EST, "portal CKAN preservado (inspeccion recurso matriculas)"),
            (INS_D_SEED, "portal CKAN preservado (inspeccion diccionario SEED)"),
            (INS_R_SEED, "portal CKAN preservado (inspeccion recurso SEED)"),
            (INS_D_EGR, "portal CKAN preservado (inspeccion diccionario egresos)"),
            (INS_R_EGR, "portal CKAN preservado (inspeccion recurso egresos)"),
            (XLSX, "recurso de datos autentico UES (matriculas 2022-2)"),
            (PKG_MAT, "metadatos CKAN conjunto matriculas"),
            (PKG_DEF, "metadatos CKAN conjunto defunciones"),
            (CKAN_EGR, "metadatos CKAN conjunto egresos"),
        ]
    ],
    "verificacion": "conteos reales desde inspecciones preservadas; diferencias "
                    "reportadas sin afirmar 1:1 donde hay mismatch (matriculas pos 21 "
                    "y 32); IDs asignados 67-70/38/72-75/15 exactos en ambos artefactos.",
}
(HERE / "alineacion.json").write_text(
    json.dumps(alineacion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------- verificacion ----------
chk = json.loads((HERE / "entrega.json").read_text(encoding="utf-8"))
assert [d["id"] for d in chk["decisiones"]] == [c["columna"] for c in asig["casos"]]
assert len({d["id"] for d in chk["decisiones"]}) == 10
assert all(d["estado"] == ESTADO for d in chk["decisiones"])
for d in chk["decisiones"]:
    assert set(d) == {"id", "estado", "estado_semantico_actual", "significado",
                      "original", "motivo", "evidencia_faltante", "evidencia",
                      "contexto", "propuesta", "historial_propuesta_rechazada", "limites"}
    assert d["estado_semantico_actual"] == "candidata_por_nombre"
    assert d["significado"] == "pendiente"
    assert d["id"] == d["original"]["columna"] == d["propuesta"]["columna"]
    assert d["propuesta"]["variable"] == d["original"]["variable"]
    assert "concepto" not in d["propuesta"]
    assert d["propuesta"]["estado_propuesto"] == ESTADO
    assert d["propuesta"]["estado_semantico_actual"] == "candidata_por_nombre"
    assert d["propuesta"]["significado"] == "pendiente"
    for e in d["evidencia"] + d["contexto"]:
        assert e["sha256"] == sha(e["ruta"]), e["ruta"]
for f in chk["fuentes"]:
    assert f["sha256"] == sha(f["ruta"]), f["ruta"]
aln = json.loads((HERE / "alineacion.json").read_text(encoding="utf-8"))
for p in aln["pares"]:
    assert p["n_filas_diccionario_real"] == len(p["campos"]) == p["n_columnas_recurso_real"]
    assert p["afirmacion_1_1_en_secuencia_completa"] == (len(p["diferencias"]) == 0)
    for c in p["campos"]:
        assert c["coincide"] == (c["variable"] == c["columna"])
for s in aln["fuentes_primarias"]:
    assert s["sha256"] == sha(s["ruta"]), s["ruta"]

# ---------- entrega.md ----------
L = ["# Correspondencias-b: registro estructural separado (10/10 "
     + ESTADO + ")",
     "",
     "Correccion por dictamen de auditoria (`requiere_correccion`): ningun par es "
     "aprobacion; ningun significado cambia de estatus; sin concepto aprobado "
     "(el `original` preserva el concepto asignado solo como referencia). "
     "NO aplicable a `vinculos_documentales_revisados`: el core exige variable "
     "`respaldada_por_definicion`. Herramienta: lectura local con SHA-256 "
     "(python hashlib), 2026-10-24.",
     "",
     "| # | campo (pos) | concepto original (no aprobado) | estado | significado |",
     "|---|-------------|--------------------------------|--------|-------------|"]
for i, d in enumerate(chk["decisiones"], 1):
    o = d["original"]
    L.append(f"| {i} | `{o['campo']}` ({o['columna'].rsplit('%2F', 1)[-1]}) "
             f"| {o['concepto']} | {d['estado']} | {d['significado']} |")
L += ["",
      "## Alineacion en secuencia completa (`alineacion.json`)",
      "",
      "- defunciones-seed: 80 filas diccionario = 80 columnas recurso = "
      "numero_variables 80; secuencia identica 80/80.",
      "- egresos: 15 = 15 = numero_variables 15; secuencia identica 15/15.",
      "- matriculas: 70 = 70 = numero_variables 70, pero 2 desalineaciones ajenas "
      "a los IDs (pos 21 `'Sexo '` vs `'Sexo'`; pos 32 `' Promedio de bachillerato'` "
      "vs `'Promedio de bachillerato'`): NO se afirma 1:1 en secuencia completa; "
      "los IDs 67-70 son exactos en ambos artefactos.",
      "",
      "## Contexto (no prueba del par)",
      "",
      "- `distribuciones.json` y `reports/investigacion-post-r6.json`: derivados; "
      "informan compatibilidad de formato y ultimo resultado por ID.",
      "- `cobertura.json` (EGR 15): fija el pendiente conservado "
      "`pendiente_aclaracion_o_revision`.",
      "",
      "## Historial",
      "",
      "- Propuesta anterior (`propuesta_resolucion` / `documental_revisada` con "
      "concepto) rechazada por auditoria; guardada por ID en "
      "`historial_propuesta_rechazada`, inactiva como aprobacion.",
      "",
      "## Limites",
      "",
      "- Sin joins/cruces/identidad de catalogos; sin vigencia nueva del vinculo; "
      "sin promocion semantica (EST 68 sin muestra; SEED ambiguedad general-fetal; "
      "EGR 15 sin fe de erratas).",
      ""]
(HERE / "entrega.md").write_text("\n".join(L), encoding="utf-8")

# ---------- cierrelisto.json ----------
archivos = []
for pat in ("*.json", "*.md", "*.py"):
    for p in sorted(HERE.glob(pat)):
        if p.name == "cierrelisto.json":
            continue
        archivos.append({"ruta": "propuestas/cierre-brechas-post-r6/correspondencias-b/" + p.name,
                         "sha256": sha("propuestas/cierre-brechas-post-r6/correspondencias-b/" + p.name)})
congelado = [{"ruta": "propuestas/cierre-brechas-post-r6/correspondencias-b/" + n,
              "sha256": sha("propuestas/cierre-brechas-post-r6/correspondencias-b/" + n)}
             for n in ("entrega.json", "alineacion.json", "entrega.md")]
cierre = {"archivos": archivos,
          "conteos": {"decisiones": len(chk["decisiones"]),
                      ESTADO: sum(1 for d in chk["decisiones"] if d["estado"] == ESTADO),
                      "propuesta_resolucion": 0,
                      "sigue_pendiente": 0,
                      "fuentes": len(chk["fuentes"]),
                      "evidencia_items": sum(len(d["evidencia"]) for d in chk["decisiones"]),
                      "contexto_items": sum(len(d["contexto"]) for d in chk["decisiones"])},
          "congelado_final_3_sha": congelado}
(HERE / "cierrelisto.json").write_text(
    json.dumps(cierre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
chk2 = json.loads((HERE / "cierrelisto.json").read_text(encoding="utf-8"))
for a in chk2["archivos"]:
    assert a["sha256"] == sha(a["ruta"]), a["ruta"]
for c in chk2["congelado_final_3_sha"]:
    assert c["sha256"] == sha(c["ruta"]), c["ruta"]
print("OK", cierre["conteos"])
for c in congelado:
    print("CONGELADO", c["ruta"], c["sha256"])
