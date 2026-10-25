"""Ronda 4 lote-4, segunda revision: reglas nuevas para significados pendientes con respaldo literal."""
import json, hashlib, pathlib
BASE = pathlib.Path("C:/Users/marti/Documents/MEX-Ontologi")
LOTE = BASE/"propuestas/pendientes-muse-r4/lote-4"
cob = json.load(open(BASE/"data/semantica/cobertura.json", encoding="utf-8"))
vidx = {v["definicion_iri"]: v for v in cob["variables"]}
asig = json.load(open(LOTE/"asignacion.json", encoding="utf-8"))
ent = json.load(open(LOTE/"entrega.json", encoding="utf-8"))

CONCEPTOS = {
 "bien-juridico-afectado-delito-municipal": ["Bien juridico afectado por el delito", "Bien juridico afectado declarado en el diccionario municipal de incidencia delictiva; ejemplo literal: la vida y la integridad corporal. Solo texto declarado; sin catalogo resuelto.", None],
 "tipo-delito-registrado": ["Tipo de delito registrado", "Descripcion especifica del tipo de delito que se realizo, segun el diccionario municipal; ejemplo: Homicidio. Solo texto declarado; sin catalogo resuelto.", None],
 "subtipo-delito-registrado": ["Subtipo de delito registrado", "Detalle mas especifico sobre el tipo de delito que se realizo, segun el diccionario municipal; ejemplo: Homicidio doloso. Solo texto declarado; sin catalogo resuelto.", None],
 "modalidad-delito-registrado": ["Modalidad del delito registrado", "Categoria en la que se puede clasificar el delito, segun el diccionario municipal; ejemplo: Con arma de fuego. Solo texto declarado; sin catalogo resuelto.", None],
 "identificador-registro-encuesta-tic": ["Identificador del registro de encuesta TIC", "Identificador unico del registro declarado en el diccionario de la encuesta TIC (tipo Entero, formato XX, ejemplo 10). Solo folio de fila; no acredita sistema de identificadores.", None],
 "sector-dependencia-encuesta-tic": ["Sector de la dependencia encuestada", "Sector declarado por la dependencia encuestada (ejemplo: 04 - SECRETARIA DE HACIENDA). Valor con prefijo numerico segun ejemplo; no se separa codigo de nombre; sin catalogo resuelto.", None],
 "momento-inicio-registro-encuesta": ["Momento de inicio del registro de encuesta", "Hora de inicio declarada en el diccionario de la encuesta TIC; tipo declarado Fecha y Hora, formato DD/MM/AAAA HH:MM. No se reduce a hora del dia.", "tiempo"],
 "momento-fin-registro-encuesta": ["Momento de finalizacion del registro de encuesta", "Hora de finalizacion declarada en el diccionario de la encuesta TIC; tipo declarado Fecha y Hora, formato DD/MM/AAAA HH:MM. No se reduce a hora del dia.", "tiempo"],
 "momento-ultima-modificacion-registro-encuesta": ["Momento de ultima modificacion del registro de encuesta", "Hora de la ultima modificacion declarada en el diccionario de la encuesta TIC; tipo declarado Fecha y Hora, formato DD/MM/AAAA HH:MM. No se reduce a hora del dia.", "tiempo"],
 "metodologia-planeacion-documentacion-software": ["Metodologia de planeacion y documentacion de software", "Metodologia de planeacion que utiliza y documentacion que se realiza en un proyecto de desarrollo de software, segun respuesta declarada a la encuesta. Solo texto declarado.", None],
 "metodologia-desarrollo-utilizada": ["Metodologia de desarrollo utilizada", "Metodologia que se utiliza, segun respuesta declarada a la encuesta de desarrollo de software. Solo texto declarado.", None],
 "tipo-pruebas-software-realizadas": ["Tipo de pruebas de software realizadas", "Tipo de pruebas que realizan, segun respuesta declarada; el ejemplo (Si) no tipifica las pruebas. Solo sentido literal de la pregunta.", None],
 "lugar-almacenamiento-informacion-sistemas": ["Lugar de almacenamiento de la informacion de los sistemas", "Donde se almacena la informacion de los sistemas, segun respuesta declarada (ejemplo: Nube). Solo texto declarado.", None],
 "sistemas-uso-firma-electronica": ["Sistemas donde se usa la firma electronica", "Sistemas donde se hace uso de la firma electronica, segun lista declarada en la respuesta. Solo texto declarado.", None],
 "conteo-proyectos-desarrollo-dependencia": ["Conteo de proyectos de desarrollo de la dependencia", "Cuantos proyectos de desarrollo de software se encuentran en desarrollo actualmente por su dependencia, segun el literal de la pregunta. Tipo declarado Booleano Si/No y ejemplo Si no expresan el conteo; solo sentido literal de la pregunta.", None],
 "atencion-incidencias-reportes-tecnicos": ["Atencion de incidencias y reportes tecnicos", "Como atiende las incidencias, reportes de problemas tecnicos y solucion de dudas, segun respuesta declarada. Tipo declarado Booleano Si/No no describe el procedimiento; solo sentido literal de la pregunta.", None],
 "razon-no-desarrollo-interno-tic": ["Razon de no desarrollo interno TIC", "Razon principal por la que no se desarrollan de forma interna en su dependencia, segun respuesta declarada. Solo texto declarado.", None],
 "procedimiento-identificacion-requerimientos-tic": ["Procedimiento de identificacion de requerimientos TIC", "Procedimiento para identificar requerimientos cuando se requiere adquirir o desarrollar una solucion de TIC, segun respuesta declarada. Solo texto declarado.", None],
 "decision-desarrollo-interno-vs-tercero-tic": ["Decision de desarrollo interno o adquisicion con tercero TIC", "Como se decide si una solucion de TIC debe ser desarrollada internamente o adquirida con un tercero, segun respuesta declarada. Solo texto declarado.", None],
 "autorizacion-asignacion-recursos-proyectos-tic": ["Autorizacion y asignacion de recursos a proyectos TIC", "Como se autorizan y asignan los recursos a los proyectos de TIC, segun respuesta declarada. Solo texto declarado.", None],
 "comentarios-validacion-encuesta": ["Comentarios sobre la validacion de la encuesta", "Comentarios sobre la validacion, campo de texto libre de la encuesta TIC. Solo texto declarado.", None],
 "clave-cie-declarada-salud": ["Clave CIE declarada en salud", "Clave CIE declarada en el diccionario de salud, formato literal CnnX (ejemplos F122, J029). Solo clave declarada; no acredita pertenencia ni version del catalogo CIE.", None],
 "clasificacion-llamada-911": ["Clasificacion de la llamada 911", "Clasificacion de la llamada realizada, segun el diccionario de llamadas procedentes 911 (ejemplo: asistencia). Solo texto declarado; sin catalogo resuelto.", None],
}
# (sufijo definicion, concepto, representacion, limite_extra, positivo, contraejemplo)
PLAN = [
 ("5f46e4b8-858d-47dc-a180-125f3cc8727a%2F3","bien-juridico-afectado-delito-municipal","no_especificada","Descripcion con redaccion defectuosa en fuente (Campo en la que...); ejemplo fija el sentido; sin catalogo resuelto.","Denota el bien juridico afectado declarado.","No aplica a otro delito ni a otra demarcacion."),
 ("5f46e4b8-858d-47dc-a180-125f3cc8727a%2F4","tipo-delito-registrado","no_especificada","Sin catalogo resuelto; ejemplo ilustrativo.","Denota el tipo de delito declarado.","No aplica a otro nivel de clasificacion."),
 ("5f46e4b8-858d-47dc-a180-125f3cc8727a%2F5","subtipo-delito-registrado","no_especificada","Sin catalogo resuelto; ejemplo ilustrativo.","Denota el subtipo de delito declarado.","No aplica al tipo ni a la modalidad."),
 ("5f46e4b8-858d-47dc-a180-125f3cc8727a%2F6","modalidad-delito-registrado","no_especificada","Sin catalogo resuelto; ejemplo ilustrativo.","Denota la modalidad declarada.","No aplica al tipo ni al subtipo."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F1","identificador-registro-encuesta-tic","no_especificada","Tipo Entero, formato XX, ejemplo 10; solo folio de fila.","Denota el folio del registro de encuesta.","No identifica dependencia ni sistema."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F1","identificador-registro-encuesta-tic","no_especificada","Tipo Entero, formato XX, ejemplo 10; solo folio de fila.","Denota el folio del registro de encuesta.","No identifica dependencia ni sistema."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F1","identificador-registro-encuesta-tic","no_especificada","Tipo Entero, formato XX, ejemplo 10; solo folio de fila.","Denota el folio del registro de encuesta.","No identifica dependencia ni sistema."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F2","sector-dependencia-encuesta-tic","no_especificada","Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo.","Denota el sector declarado.","No acredita adscripcion ni vigencia."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F2","sector-dependencia-encuesta-tic","no_especificada","Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo.","Denota el sector declarado.","No acredita adscripcion ni vigencia."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F2","sector-dependencia-encuesta-tic","no_especificada","Ejemplo con prefijo numerico; no se separa codigo de nombre; sin catalogo.","Denota el sector declarado.","No acredita adscripcion ni vigencia."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F3","momento-inicio-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de inicio declarado.","No aplica al fin ni a la modificacion."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F3","momento-inicio-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de inicio declarado.","No aplica al fin ni a la modificacion."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F3","momento-inicio-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de inicio declarado.","No aplica al fin ni a la modificacion."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F4","momento-fin-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de finalizacion declarado.","No aplica al inicio ni a la modificacion."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F4","momento-fin-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de finalizacion declarado.","No aplica al inicio ni a la modificacion."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F4","momento-fin-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de finalizacion declarado.","No aplica al inicio ni a la modificacion."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F5","momento-ultima-modificacion-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de ultima modificacion declarado.","No aplica al inicio ni al fin."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F5","momento-ultima-modificacion-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de ultima modificacion declarado.","No aplica al inicio ni al fin."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F5","momento-ultima-modificacion-registro-encuesta","no_especificada","Tipo Fecha y Hora, formato DD/MM/AAAA HH:MM; no reducir a hora del dia.","Denota el momento de ultima modificacion declarado.","No aplica al inicio ni al fin."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F8","metodologia-planeacion-documentacion-software","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la metodologia y documentacion declaradas.","No acredita metodologia ni documento concreto."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F10","metodologia-desarrollo-utilizada","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la metodologia declarada.","No acredita metodologia concreta."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F13","tipo-pruebas-software-realizadas","no_especificada","Ejemplo (Si) no tipifica las pruebas; solo sentido literal de la pregunta.","Denota el tipo de pruebas declarado.","No acredita prueba concreta."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F21","lugar-almacenamiento-informacion-sistemas","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota el lugar de almacenamiento declarado.","No acredita infraestructura concreta."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F28","sistemas-uso-firma-electronica","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota los sistemas con firma electronica declarados.","No acredita sistema concreto."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F36","conteo-proyectos-desarrollo-dependencia","no_especificada","Tipo Booleano Si/No y ejemplo Si no expresan el conteo; solo sentido literal de la pregunta.","Denota el conteo de proyectos preguntado.","No afirma numero ni existencia."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F39","atencion-incidencias-reportes-tecnicos","no_especificada","Tipo Booleano Si/No no describe el procedimiento; solo sentido literal de la pregunta.","Denota la forma de atencion preguntada.","No afirma procedimiento concreto."),
 ("a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F40","conteo-personas-desarrollo-software","no_especificada","Descripcion literal identica a la regla vigente r3a9-059; tipo Booleano Si/No y ejemplo Si no expresan el conteo.","Denota el conteo de personas preguntado.","No afirma numero ni adscripcion."),
]
PLAN_CORRECTO = list(PLAN)
EXTRA = [
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F8","razon-no-desarrollo-interno-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la razon declarada.","No acredita causa ni situacion."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F8","razon-no-desarrollo-interno-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la razon declarada.","No acredita causa ni situacion."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F9","procedimiento-identificacion-requerimientos-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota el procedimiento declarado.","No acredita procedimiento concreto."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F9","procedimiento-identificacion-requerimientos-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota el procedimiento declarado.","No acredita procedimiento concreto."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F10","decision-desarrollo-interno-vs-tercero-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota el criterio de decision declarado.","No acredita decision concreta."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F10","decision-desarrollo-interno-vs-tercero-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota el criterio de decision declarado.","No acredita decision concreta."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F11","autorizacion-asignacion-recursos-proyectos-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la forma de autorizacion declarada.","No acredita acto concreto."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F11","autorizacion-asignacion-recursos-proyectos-tic","no_especificada","Solo texto declarado; ejemplo ilustrativo.","Denota la forma de autorizacion declarada.","No acredita acto concreto."),
 ("c65eb4e7-a17d-43c7-b08c-05811505edf1%2F13","comentarios-validacion-encuesta","no_especificada","Campo de texto libre; ejemplo generico.","Denota los comentarios declarados.","No afirma contenido."),
 ("f3ecd3d2-2156-4251-82e5-13b079471ee9%2F13","comentarios-validacion-encuesta","no_especificada","Campo de texto libre; ejemplo generico.","Denota los comentarios declarados.","No afirma contenido."),
 ("f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F12","clave-cie-declarada-salud","codigo","Formato literal CnnX; no acredita catalogo CIE ni version.","Denota la clave CIE declarada.","No acredita diagnostico ni catalogo."),
 ("355da8aa-8544-4f32-b942-f54e007dd49b%2F12","clave-cie-declarada-salud","codigo","Formato literal CnnX; no acredita catalogo CIE ni version.","Denota la clave CIE declarada.","No acredita diagnostico ni catalogo."),
 ("7922b8c8-db09-4172-ad7f-31b0ba0c68e3%2F7","clasificacion-llamada-911","no_especificada","Solo texto declarado; ejemplo ilustrativo; sin catalogo.","Denota la clasificacion declarada.","No acredita tipificacion oficial."),
]
FULL = PLAN_CORRECTO + EXTRA
BASE_IRI = "https://example.org/mex-ontologi/definition/"
reglas = []
for i, (suf, concepto, rep, lim, pos, contra) in enumerate(FULL, 1):
    di = BASE_IRI + suf
    v = vidx[di]
    rid = f"r4-lote-4-{i:03d}"
    ins_row = {"variable": v["variable"], "descripcion": v["descripcion"], "definicion_iri": di,
               "diccionario": v["diccionario"], "conjunto": v["conjunto"],
               "unidad_de_medida": v.get("unidad_de_medida", ""), "tipo_de_dato": v.get("tipo_de_dato", ""),
               "ejemplo_de_dato": "", "huella_fila_diccionario": v["huella_fila_diccionario"]}
    reglas.append({"id": rid, "concepto": concepto, "representacion": rep,
        "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
        "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]], "definiciones": [di],
        "criterio": "Segunda revision lote-4; lectura literal de la fila del diccionario y contexto del conjunto; alcance fijado a esta definicion.",
        "fuente_revision": "propuestas/pendientes-muse-r4/lote-4/entrega.json",
        "alcance": "Solo este diccionario, conjunto, definicion, nombre y descripcion.",
        "positivo": pos, "contraejemplo": contra, "limite": lim,
        "evidencia": [ins_row], "huella_fila_diccionario": v["huella_fila_diccionario"]})
print("reglas:", len(reglas))
prop = {BASE_IRI + s for s, *_ in FULL}
print("definiciones con regla:", len(prop))
# variables asignadas
allvars = {vp["definicion_iri"] for vp in asig["variables_pendientes"]}
print("asignadas:", len(allvars), "sin regla:", sorted(allvars - prop))
# validar que FULL cubre 40 y restan 7
