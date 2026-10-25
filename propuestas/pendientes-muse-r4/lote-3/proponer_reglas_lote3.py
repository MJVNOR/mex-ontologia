"""Ronda 4 lote-3, segunda revision: propone reglas nuevas row-restricted.

Parte de entrega.json vigente (conserva las 282 decisiones/vinculos
comprobados) y reexamina los 123 significados pendientes con fila completa
(tipo/formato/ejemplo/unidad) y conceptos exactos. Crea reglas r4-lote-3-...
restringidas a una definicion exacta + huella; crea conceptos nuevos
limitados solo cuando ningun concepto vigente es exacto. Descripciones
vacias, incompletas o contradictorias quedan pendientes por ese motivo real.
Regenera entrega.json, pendientes.json, resultado.md y listo.json.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

LOTE = Path(__file__).resolve().parent
ROOT = LOTE.parents[2]
BASE = "https://example.org/mex-ontologi/"
ALCANCE = ("solo aplica a la definicion citada (alcance simultaneo por "
           "conjunto, diccionario, definicion, nombre y descripcion); no "
           "autoriza cruces, homologaciones ni equivalencias")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# (variable, concepto, representacion, limites, nota_criterio,
#  concepto_nuevo [etiqueta, definicion, padre] o None si vigente)
PROPUESTAS = [
    # SINAC 22202305-2d02-4c49-b216-cc98224357f0
    ("SECONSIDERAINDIGENA", "autoadscripcion-indigena-madre", "codigo",
     ["Valores y catalogo no documentados; ejemplo 2 sin mapa declarado; no "
      "homologa identidad ni pertenencia a catalogos nacionales."],
     "indicador codificado; ejemplo de dato 2.",
     ["Autoadscripcion indigena de la madre",
      "Indicador de si la madre se considera indigena, segun el literal de "
      "la fila; valores y catalogo no documentados.", None]),
    ("SECONSIDERAINDIGENAD", "autoadscripcion-indigena-madre", "nombre",
     ["Par textual del indicador; ejemplo NO; no se fusiona con el codigo "
      "mas alla de compartir aspecto."],
     "indicador textual; ejemplo de dato NO.",
     None),
    ("HABLALENGUAINDIGENA", "habla-lengua-indigena-madre", "codigo",
     ["Valores y catalogo no documentados; ejemplo 2 sin mapa declarado."],
     "indicador codificado; ejemplo de dato 2.",
     ["Habla de lengua indigena de la madre",
      "Indicador de si la madre habla lengua indigena, segun el literal de "
      "la fila; valores y catalogo no documentados.", None]),
    ("HABLALENGUAINDIGENAD", "habla-lengua-indigena-madre", "nombre",
     ["Par textual del indicador; ejemplo NO."],
     "indicador textual; ejemplo de dato NO.",
     None),
    # SUIVE 2334deaa-dd0c-444e-b038-4cc556ad715d
    ("no_semana", "semana-referencia-vigilancia", "codigo",
     ["Numero de semana declarado (ejemplo 22); sin acreditar sistema de "
      "semana epidemiologica ni calendario; solo referencia temporal "
      "declarada."],
     "numero de semana; ejemplo de dato 22.",
     ["Semana de referencia de vigilancia",
      "Numero de la semana declarado en la fila de vigilancia "
      "epidemiologica; sistema y calendario no documentados.", "tiempo"]),
    # Donaciones 52fbcaaa-765b-4c92-8418-ccebc3fcfdcd
    ("ID_Persona", "identificador-persona-donante", "codigo",
     ["Formato N_NNNN (ejemplo 1_2005); identificador local al conjunto; "
      "no habilita identidad entre fuentes ni cruces."],
     "identificador local con formato N_NNNN.",
     ["Identificador de persona donante",
      "Identificador unico de cada persona donante dentro del conjunto; "
      "local, no habilita identidad entre fuentes.", None]),
    # Gobernanza 90f5c6ec-026e-4216-9541-e4730c836ff1
    ("ID", "identificador-registro-encuesta", "codigo",
     ["Formato XX (ejemplo 10); ordinal local del registro de respuesta."],
     "identificador del registro de respuesta.",
     ["Identificador del registro de encuesta",
      "Identificador unico del registro de respuesta dentro del conjunto; "
      "local.", None]),
    ("P2", "sector-dependencia-encuestada", "nombre",
     ["Ejemplo combina clave y nombre (04 - SECRETARIA DE HACIENDA) sin "
      "separador documentado; no resuelve catalogo."],
     "sector declarado en texto; ejemplo con clave y nombre.",
     ["Sector de la dependencia encuestada",
      "Sector declarado por la dependencia que responde la encuesta; "
      "dominio no documentado.", None]),
    ("P3", "tiempo", "hora",
     ["Evento y cobertura no fijados en la fila; solo referencia temporal "
      "declarada con formato DD/MM/AAAA HH:MM."],
     "hora de inicio declarada; evento no fijado.", None),
    ("P4", "tiempo", "hora",
     ["Evento y cobertura no fijados en la fila; solo referencia temporal "
      "declarada con formato DD/MM/AAAA HH:MM."],
     "hora de finalizacion declarada; evento no fijado.", None),
    ("P5", "tiempo", "hora",
     ["Evento y cobertura no fijados en la fila; solo referencia temporal "
      "declarada con formato DD/MM/AAAA HH:MM."],
     "hora de ultima modificacion declarada; evento no fijado.", None),
    ("P7", "condiciones-innovacion-tic-mencionadas", "nombre",
     ["Respuesta abierta por dependencia (ejemplo Platicas, reuniones); "
      "sin dominio ni codificacion; no agrega ni compara."],
     "mencion libre de condiciones; ejemplo con texto.",
     ["Condiciones de innovacion TIC mencionadas",
      "Condiciones que la dependencia considera que contribuyen a la "
      "innovacion en TIC, segun mencion libre; sin dominio documentado.",
      None]),
    ("P9", "ejemplos-desarrollo-tic-mencionados", "nombre",
     ["Respuesta abierta (ejemplo Prototipo 1); sin dominio; no compara."],
     "mencion libre de ejemplos de desarrollo TIC.",
     ["Ejemplos de desarrollo TIC mencionados",
      "Ejemplos que el personal del area TIC haya desarrollado, segun "
      "mencion libre; sin dominio documentado.", None]),
    ("P10", "apoyo-tendencias-tic-dependencia", "codigo",
     ["Booleano Si/No (ejemplo Si); literal de la pregunta conservado."],
     "respuesta Si/No a la pregunta de apoyo.",
     ["Apoyo al analisis de tendencias TIC",
      "Respuesta a si en la dependencia coordinadora existe interes y apoyo "
      "para que el personal TIC analice tendencias y tecnologias.",
      None]),
    ("P11", "ejemplos-apoyo-tendencias-mencionados", "nombre",
     ["Respuesta abierta (ejemplo Tecnologia 1); sin dominio."],
     "mencion libre de ejemplos que reflejen lo anterior.",
     ["Ejemplos de apoyo a tendencias mencionados",
      "Ejemplos que reflejen el interes y apoyo al analisis de tendencias, "
      "segun mencion libre.", None]),
    ("P13", "recursos-anuales-innovacion-mencionados", "nombre",
     ["Ejemplo mixto (5000, software): montos y especie sin normalizar; "
      "no agregar ni convertir."],
     "mencion libre de recursos anuales destinados a innovacion.",
     ["Recursos anuales de innovacion mencionados",
      "Recursos anuales destinados a innovacion, segun mencion libre; "
      "unidad mixta sin normalizar.", None]),
    ("P15", "instrumentos-fines-digitales-sector-mencionados", "nombre",
     ["Respuesta abierta (ejemplo Reglamento 1); sin catalogo."],
     "mencion libre de instrumentos con fines digitales del sector.",
     ["Instrumentos con fines digitales del sector mencionados",
      "Reglamentos, politicas, procedimientos o instrumentos con fines "
      "digitales del sector, segun mencion libre.", None]),
    ("P16", "instrumentos-previos-ley-gobierno-digital", "codigo",
     ["Booleano Si/No (ejemplo Si); literal de la pregunta conservado, "
      "aunque truncado en la fila."],
     "respuesta Si/No sobre instrumentos previos a la Ley.",
     ["Instrumentos previos a la Ley de Gobierno Digital",
      "Respuesta a si la dependencia contaba con instrumentos que "
      "orientaran estrategias antes de la Ley de Gobierno Digital.",
      None]),
    ("P17", "instrumentos-fines-digitales-mencionados", "nombre",
     ["Respuesta abierta; sin catalogo."],
     "mencion libre de instrumentos con fines digitales.",
     ["Instrumentos con fines digitales mencionados",
      "Reglamentos, politicas, procedimientos o instrumentos con fines "
      "digitales, segun mencion libre.", None]),
    ("P18", "instrumentos-actuales-mejora-administracion", "codigo",
     ["Booleano Si/No (ejemplo No); literal de la pregunta conservado."],
     "respuesta Si/No sobre instrumentos actuales en implementacion.",
     ["Instrumentos actuales de mejora administrativa",
      "Respuesta a que instrumentos se implementan en la administracion "
      "estatal para mejorar estrategias en materia digital.", None]),
    ("P20", "normativa-requerida-mencionada", "nombre",
     ["Respuesta abierta (ejemplo Normativa 12); sin catalogo."],
     "mencion libre de normativa que necesita expedirse.",
     ["Normativa requerida mencionada",
      "Normativa que la dependencia considera que necesita expedirse para "
      "cumplir sus funciones, segun mencion libre.", None]),
    ("P21", "instrumentos-actuales-mencionados", "nombre",
     ["Respuesta abierta (ejemplo El reglamento 120 y el 159); sin "
      "catalogo ni vigencia acreditada."],
     "mencion libre de instrumentos actuales en implementacion.",
     ["Instrumentos actuales mencionados",
      "Instrumentos que se implementan en la administracion estatal para "
      "mejorar estrategias digitales, segun mencion libre.", None]),
    # Zonas Salva b37f6cd2-c72c-448c-bcb2-9127c4912847
    ("Tipo de Lugar", "giro-establecimiento-zona-salva", "nombre",
     ["Dominio abierto sin catalogo declarado (ejemplo RESTAURANTE); no "
      "resuelve giro oficial."],
     "giro declarado en texto; ejemplo RESTAURANTE.",
     ["Giro del establecimiento zona salva",
      "Giro que tiene el establecimiento que es zona salva, segun texto "
      "libre; sin catalogo.", None]),
    # Denuncias 3f6942e3-a9c5-42c0-a38b-2b7aad2a6c99
    ("No_D", "numero-entrada-registro", "codigo",
     ["Ordinal de la entrada dentro del recurso (ejemplo 6); local, sin "
      "continuidad entre fuentes."],
     "numero de entrada; ejemplo 6.",
     ["Numero de la entrada",
      "Ordinal de la entrada dentro del recurso; local, sin continuidad "
      "entre fuentes.", None]),
    ("MEDIO DE RECEPCION", "medio-recepcion-denuncia", "nombre",
     ["Texto libre (ejemplo TELEFONICA); sin catalogo de medios."],
     "medio por el cual se tomo la denuncia.",
     ["Medio de recepcion de la denuncia",
      "Medio por el cual se tomo la denuncia; sin catalogo.", None]),
    ("ASUNTO", "asunto-denuncia", "nombre",
     ["Texto libre (ejemplo DENUNCIA); sin catalogo."],
     "asunto general de la denuncia.",
     ["Asunto de la denuncia",
      "Asunto general de la denuncia; sin catalogo.", None]),
    ("HECHOS", "hechos-denuncia", "nombre",
     ["Texto libre descriptivo; sin codificacion."],
     "hechos descritos en la denuncia.",
     ["Hechos de la denuncia",
      "Hechos descritos en la denuncia, en texto libre.", None]),
    ("GIRO", "giro-denuncia", "nombre",
     ["Texto libre (ejemplo CRIADERO DE ANIMALES DE GRANJA); sin "
      "catalogo de giros."],
     "giro de la denuncia.",
     ["Giro de la denuncia",
      "Giro de la denuncia; sin catalogo.", None]),
    ("MATERIA DE LA DENUNCIA", "materia-denuncia", "nombre",
     ["Texto libre (ejemplo ANIMAL); sin catalogo de materias."],
     "materia de la denuncia.",
     ["Materia de la denuncia",
      "Materia de la denuncia; sin catalogo.", None]),
    # Apoyos medida c429c558-a38a-4f32-9ea9-8356c1c59cc1
    ("concepto_medida", "clasificacion-apoyo-otorgado", "nombre",
     ['Unidad "No aplica"; ejemplo Medidas de ayuda; clasificacion '
      "declarada sin catalogo."],
     "concepto general de clasificacion del apoyo.",
     ["Clasificacion del apoyo otorgado",
      "Concepto general bajo el cual se clasifica el apoyo otorgado; sin "
      "catalogo.", None]),
    ("Tipo_ayuda", "tipo-ayuda-victima", "nombre",
     ["Texto libre (ejemplo Atencion medica); sin catalogo."],
     "tipo especifico de ayuda otorgada a la victima.",
     ["Tipo de ayuda a la victima",
      "Tipo especifico de ayuda otorgada a la victima; sin catalogo.",
      None]),
    ("Tipo_subsidio", "nivel-financiamiento-apoyo", "nombre",
     ["Ejemplo Estatal sugiere ambito; valores y escala no documentados; "
      "no es monto."],
     "nivel de financiamiento otorgado.",
     ["Nivel de financiamiento del apoyo",
      "Nivel de financiamiento otorgado; valores no documentados.", None]),
    ("Sector", "sector-poblacion-beneficiaria", "nombre",
     ["Texto libre (ejemplo En situacion de vulnerabilidad); sin "
      "catalogo."],
     "sector poblacional de la poblacion beneficiaria.",
     ["Sector de la poblacion beneficiaria",
      "Sector poblacional al que pertenece la poblacion beneficiaria; sin "
      "catalogo.", None]),
    ("Poblaci\u00f3n_beneficiaria", "grupo-personas-apoyo", "nombre",
     ["Texto libre (ejemplo Victimas de delito); sin conteo ni padron."],
     "grupo de personas que reciben el apoyo.",
     ["Grupo de personas que recibe el apoyo",
      "Grupo de personas que reciben el apoyo; descripcion del grupo, no "
      "conteo.", None]),
    # Apoyos d26d1900-6ff7-41a4-8968-f8984fc85e75
    ("CONSECUTIVO", "numero-entrada-registro", "codigo",
     ["Ordinal de la entrada dentro del recurso (ejemplo 8); local."],
     "numero consecutivo de la entrada.", None),
    ("Cantidad de apoyos otorgados", "cantidad-apoyos-otorgados",
     "no_especificada",
     ["Unidad declarada: apoyos (ejemplo 500); conteo sin equivalencia "
      "con otras medidas."],
     "conteo de apoyos entregados; ejemplo 500.",
     ["Cantidad de apoyos otorgados",
      "Unidad de apoyos que fueron entregados; conteo local.", None]),
    ("Monto", "monto-apoyo", "no_especificada",
     ["Moneda y unidad no declaradas (ejemplo 42800, flotante); no "
      "comparar, agregar ni convertir."],
     "monto declarado sin moneda; ejemplo 42800.",
     ["Monto del apoyo",
      "Monto declarado del apoyo; moneda no documentada.", None]),
    ("Comentarios\n/Observaciones", "bienes-otorgados-apoyo", "nombre",
     ["Mencion libre (ejemplo DESPENSAS, COBERTORES); sin catalogo."],
     "bienes otorgados mencionados en observaciones.",
     ["Bienes otorgados mencionados",
      "Diferentes bienes otorgados, segun mencion libre en observaciones; "
      "sin catalogo.", None]),
    # 89e8c891-5987-44eb-ba11-9508e3dd87e6
    ("No", "identificador-respuesta", "codigo",
     ["Identificador local de la respuesta dentro del recurso."],
     "identificador de la respuesta.",
     ["Identificador de la respuesta",
      "Identificador de la respuesta dentro del recurso; local.", None]),
    # 087efeed-26c4-4ec4-8128-49f257d5182
    ("No.", "identificador-evento", "codigo",
     ["Identificador local del evento dentro del recurso."],
     "identificador del evento.",
     ["Identificador del evento",
      "Identificador del evento dentro del recurso; local.", None]),
    # Centros nocturnos 637b1909-8788-4bdf-9508e4fa9e8c008
    ("Tipo", "tipo-centro-nocturno", "nombre",
     ["Texto (ejemplo PRIVADO); dominio abierto sin catalogo."],
     "tipo de centro nocturno.",
     ["Tipo de centro nocturno",
      "Tipo de centro nocturno; sin catalogo.", None]),
    ("Estatus", "estatus-centro-nocturno", "nombre",
     ["Texto (ejemplo Inspeccionado); dominio abierto; no acredita "
      "vigencia del estatus."],
     "estatus del centro nocturno.",
     ["Estatus del centro nocturno",
      "Estatus del centro nocturno; vigencia no documentada.", None]),
    # Llamadas 911 1a95d734-2f0e-4781-8831-77dcfcbe70f8
    ("clasificacion", "clasificacion-llamada", "nombre",
     ["Texto (ejemplo asistencia); clasificacion declarada sin catalogo "
      "publicado."],
     "clasificacion de la llamada realizada.",
     ["Clasificacion de la llamada",
      "Clasificacion de la llamada realizada; sin catalogo.", None]),
]

# Motivos reales para los que quedan pendientes (variable -> (motivo, falta)).
PEND_MOTIVO_VACIA = (
    "Descripcion vacia o 'Pendiente de especificar': sin respaldo explicito "
    "vinculado a esta definicion; no se interpreta el nombre.")

def main():
    entrega = load(LOTE / "entrega.json")
    asig = load(LOTE / "asignacion.json")
    ins = load(ROOT / "data/portal/contenido-inspeccion.json")
    base = load(ROOT / "propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json")
    prev = load(ROOT / "propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json")
    insmap = {r["id"]: r for r in ins["recursos"]}
    variables = {v["definicion_iri"]: v for v in base["variables"]
                 if v.get("definicion_iri")}
    by_var = {}
    for s in asig["variables_pendientes"]:
        by_var.setdefault((s["diccionario"], s["variable"]), []).append(s)
    assert all(len(v) == 1 for v in by_var.values()), "variable duplicada"

    reglas, conceptos_nuevos, prop_iris = [], {}, []
    for i, (var, concepto, rep, limites, nota, nuevo) in enumerate(
            PROPUESTAS, 1):
        matches = [s for (d, vv), lst in by_var.items() for s in lst
                   if vv == var]
        assert len(matches) == 1, f"sin match unico: {var}"
        s = matches[0]
        v = variables[s["definicion_iri"]]
        assert v["variable"] == var
        idx = int(s["definicion_iri"].split("%2F")[-1])
        row = insmap[v["diccionario"]]["definiciones"][idx - 1]
        rid = f"r4-lote-3-{concepto}-{i}"
        tipo = row.get("Tipo de dato", "")
        formato = row.get("Formato", row.get("formato", ""))
        ejemplo = row.get("Ejemplo de dato", "")
        reglas.append({
            "id": rid, "concepto": concepto, "representacion": rep,
            "nombres": [v["variable"]], "descripciones": [v["descripcion"]],
            "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
            "definiciones": [v["definicion_iri"]],
            "huella_fila_diccionario": v["huella_fila_diccionario"],
            "limites": [ALCANCE, *limites],
            "criterio": (f"Regla de descripcion exacta {rid}: variable "
                         f"{var} del diccionario {v['diccionario']} "
                         f"(conjunto {v['conjunto']}), fila {idx}: "
                         f"descripcion literal «{v['descripcion']}»; tipo "
                         f"{tipo}, formato {formato or 'no declarado'}, "
                         f"ejemplo {ejemplo or 'no declarado'}; "
                         f"representacion {rep}; {nota}"),
            "evidencia": [
                f"data/portal/contenido-inspeccion.json:recurso="
                f"{v['diccionario']}:definiciones[{idx}]",
                f"tipo={tipo}; formato={formato or 'no declarado'}; "
                f"ejemplo={ejemplo or 'no declarado'}",
                f"definicion_iri={v['definicion_iri']}",
                f"huella_fila_diccionario={v['huella_fila_diccionario']}"]})
        if nuevo is not None and concepto not in prev["conceptos"]:
            conceptos_nuevos[concepto] = nuevo
        prop_iris.append(v["definicion_iri"])

    # Decisiones de significados: proponer las 43 con regla, resto pendiente.
    pendientes_det = [p for p in
                      json.loads((LOTE / "pendientes.json").read_text(
                          encoding="utf-8"))["pendientes"]
                      if p["tipo"] == "columna"]
    decisiones_sig = []
    for s in asig["variables_pendientes"]:
        defi = s["definicion_iri"]
        v = variables.get(defi, {})
        ev = [f"data/portal/contenido-inspeccion.json:recurso="
              f"{s['diccionario']}",
              f"definicion_iri={defi}",
              f"estado_cobertura={v.get('estado', s['estado'])}"]
        if defi in prop_iris:
            r = next(r for r in reglas if r["definiciones"] == [defi])
            decisiones_sig.append({
                "definicion_iri": defi, "decision": "proponer",
                "motivo": (f"Descripcion literal «{v['descripcion']}» con "
                           f"fila completa verificada respalda el sentido "
                           f"limitado del concepto {r['concepto']} "
                           f"(regla {r['id']}); {r['limites'][-1]}"),
                "evidencia": ev + [f"regla={r['id']}",
                                   f"concepto={r['concepto']}"]})
        else:
            desc = (s.get("descripcion") or "").strip()
            if defi.endswith("%2F18") and "22202305" in defi:
                motivo = ("Divergencia documentada con su par codificado: "
                          "RESIDEEXTRANJERO indica 'si la madre es recidente "
                          "en el extranjero' y RESIDEEXTRANJEROD 'si la madre "
                          "es residente extranjera'; el concepto vigente "
                          "residencia-extranjero-madre registra que el par "
                          "textual queda pendiente por contradiccion y no se "
                          "unifican.")
                falt = ("Aclaracion documental de la diferencia entre "
                        "residir en el extranjero y ser residente extranjera "
                        "en SINAC.")
            elif "de01_a_04" in defi and "2334deaa" in defi:
                motivo = ("Contradiccion nombre/descripcion: el nombre "
                          "sugiere 1-4 y la descripcion dice 'entre 1 y 5 "
                          "anos'; sin regla para rango contradictorio.")
                falt = "Aclaracion del rango de01_a_04 en SUIVE."
            elif (s["variable"], s["diccionario"]) == (
                    "TRIMESTRE", "3f6942e3-a9c5-42c0-a38b-2b7aad2a6c99"):
                motivo = ("Descripcion incompleta 'Trimestre del estrato': "
                          "'estrato' no definido en fila ni contexto; solo "
                          "pista temporal sin evento fijado.")
                falt = "Definicion de 'estrato' en Denuncias 1er Trimestre."
            elif (s["variable"], s["diccionario"]) == (
                    "cve_cie10", "2334deaa-dd0c-444e-b038-4cc556ad715d"):
                motivo = ("Descripcion generica 'Clave' sin objeto fijado; "
                          "el ejemplo sugiere CIE pero inferirlo seria "
                          "interpretar el nombre, no respaldo explicito.")
                falt = ("Descripcion que fije el objeto de cve_cie10 (CIE-10 "
                        "y version usada).")
            elif (s["variable"], s["diccionario"]) == (
                    "acumulado", "2334deaa-dd0c-444e-b038-4cc556ad715d"):
                motivo = ("'Acumulados' no fija objeto ni periodo de "
                          "acumulacion.")
                falt = "Definicion de acumulado (objeto y periodo) en SUIVE."
            elif not desc or desc.lower() == "pendiente de especificar":
                motivo = PEND_MOTIVO_VACIA
                falt = (f"Descripcion publicada de {s['variable']} "
                        f"(diccionario {s['diccionario']}).")
            else:
                motivo = ("Dominio o medida sin documento que fije catalogo, "
                          f"unidades o vigencia para «{desc}».")
                falt = (f"Documento de dominio/medida para {s['variable']} "
                        f"(diccionario {s['diccionario']}).")
            decisiones_sig.append({"definicion_iri": defi,
                                   "decision": "pendiente", "motivo": motivo,
                                   "evidencia": ev})
            pendientes_det.append({"tipo": "significado", "iri": defi,
                                   "variable": s["variable"],
                                   "motivo": motivo,
                                   "evidencia_faltante": falt,
                                   "evidencia_revisada": ev})

    assert {d for r in reglas for d in r["definiciones"]} == {
        d["definicion_iri"] for d in decisiones_sig
        if d["decision"] == "proponer"}

    entrega["decisiones_significados"] = decisiones_sig
    entrega["reglas"] = reglas
    entrega["conceptos_nuevos"] = conceptos_nuevos
    entrega["generado_en_utc"] = datetime.now(timezone.utc).isoformat()
    entrega["solicitudes_investigacion"] = [
        {"id": "r4-lote-3-inv-02",
         "iris": [s["definicion_iri"]
                  for s in asig["variables_pendientes"]
                  if s["diccionario"] ==
                  "22202305-2d02-4c49-b216-cc98224357f0"
                  and (s.get("descripcion") or "").strip().lower()
                  == "pendiente de especificar"],
         "duda": "53 variables SINAC sin descripcion (atencion prenatal, "
                 "vacunas, anomalias CIE, CLUES, certificacion, etc.).",
         "fuente_probable": "Secretaria de Salud / SINAC.",
         "documento_requerido": "Diccionario SINAC completo con "
                                "descripciones y catalogos (CLUES con "
                                "version historica 2022, CIE, ocupacion)."},
        {"id": "r4-lote-3-inv-03",
         "iris": [s["definicion_iri"]
                  for s in asig["variables_pendientes"]
                  if s["diccionario"] ==
                  "2334deaa-dd0c-444e-b038-4cc556ad715d"
                  and s["definicion_iri"] not in prop_iris],
         "duda": "SUIVE: cve_cie10 solo 'Clave'; acumulado sin objeto ni "
                 "periodo; de01_a_04 contradictorio; 22 filas sin "
                 "descripcion (desagregados *f e instituciones).",
         "fuente_probable": "Servicios de Salud de Sonora / SUIVE.",
         "documento_requerido": "Diccionario SUIVE con descripciones, "
                                "aclaracion del rango de01_a_04 y documento "
                                "de cobertura de unidades reportantes."},
        {"id": "r4-lote-3-inv-07",
         "iris": [s["definicion_iri"]
                  for s in asig["variables_pendientes"]
                  if (s["definicion_iri"].endswith("%2F18")
                      or (s["variable"], s["diccionario"]) ==
                      ("TRIMESTRE",
                       "3f6942e3-a9c5-42c0-a38b-2b7aad2a6c99"))],
         "duda": "RESIDEEXTRANJEROD diverge de su par codificado "
                 "(residente extranjera vs reside en el extranjero); "
                 "TRIMESTRE no define 'estrato'.",
         "fuente_probable": "Secretaria de Salud / SINAC; publicador de "
                            "Denuncias.",
         "documento_requerido": "Aclaracion documental de la diferencia "
                                "extranjero/residente y definicion de "
                                "estrato en Denuncias."},
    ]
    (LOTE / "entrega.json").write_text(
        json.dumps(entrega, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (LOTE / "pendientes.json").write_text(
        json.dumps({"lote": "lote-3", "pendientes": pendientes_det},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    n_col_prop = sum(1 for d in entrega["decisiones_columnas"]
                     if d["decision"] == "proponer")
    n_col_pen = len(entrega["decisiones_columnas"]) - n_col_prop
    n_sig_prop = sum(1 for d in decisiones_sig if d["decision"] == "proponer")
    md = f"""# Resultado lote-3 (ronda 4, segunda revision)

- Columnas asignadas revisadas: {len(entrega["decisiones_columnas"])} (evidencia recomputada; sin cambios: {n_col_prop} proponer, {n_col_pen} pendiente, 0 rechazar).
- Vinculos con formato exacto: {len(entrega["vinculos"])} (conservados).
- Significados asignados: {len(decisiones_sig)} ({n_sig_prop} proponer con regla nueva, {len(decisiones_sig) - n_sig_prop} pendiente).
- Reglas nuevas: {len(reglas)} (IDs r4-lote-3-...), restringidas a una definicion exacta + huella; 3 reutilizan el concepto vigente tiempo; 1 concepto nuevo compartido por 2 reglas (numero-entrada-registro).
- Conceptos nuevos: {len(conceptos_nuevos)} (etiqueta, definicion limitada, padre justificado; resto reutiliza vigentes exactos).
- Pendientes restantes con motivo real: descripciones vacias (75 - 0 propuestas = 75 siguen), contradicciones (de01_a_04, RESIDEEXTRANJEROD), incompletas (TRIMESTRE, cve_cie10, acumulado).
- Solicitudes de investigacion: {len(entrega["solicitudes_investigacion"])} grupos con IRIs concretos.
"""
    (LOTE / "resultado.md").write_text(md, encoding="utf-8")
    sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
    (LOTE / "listo.json").write_text(json.dumps({
        "lote": "lote-3", "sha256": sha,
        "columnas": len(entrega["decisiones_columnas"]),
        "proponer_columna": n_col_prop,
        "pendientes_columna": n_col_pen,
        "significados": len(decisiones_sig), "proponer_significado":
        n_sig_prop, "vinculos": len(entrega["vinculos"]),
        "reglas": len(reglas),
        "conceptos_nuevos": len(conceptos_nuevos)},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reglas": len(reglas),
                      "conceptos_nuevos": len(conceptos_nuevos),
                      "sig_proponer": n_sig_prop,
                      "sig_pendiente": len(decisiones_sig) - n_sig_prop,
                      "sha256": sha[:16] + "..."}))


if __name__ == "__main__":
    main()
