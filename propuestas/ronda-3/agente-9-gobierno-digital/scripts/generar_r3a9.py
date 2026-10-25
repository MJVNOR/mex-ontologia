"""Genera propuestas ronda-3 agente-9 (gobierno digital) solo dentro de su carpeta.

Lee evidencia central (read-only) y escribe unicamente en
propuestas/ronda-3/agente-9-gobierno-digital/.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
R3A9 = ROOT / "propuestas" / "ronda-3" / "agente-9-gobierno-digital"
assert str(R3A9) in str(Path(__file__).resolve()), "script fuera de carpeta asignada"

sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella  # noqa: E402
from integrar_contenido import valor  # noqa: E402

BASE = "https://example.org/mex-ontologi/"

# Conjuntos asignados al agente 9 (encuesta Diagnostico del Entorno Digital, APE Sonora)
CONJUNTOS = {
    "c9a63b8b-4d70-47db-bfc7-cf86a10b0514": "Desarrollo de Software en la Administracion Publica Estatal",
    "d175b134-77f4-4201-9409-08b05c1d5ffa": "Mejora Regulatoria para el Entorno Digital de la Administracion Publica Estatal",
    "37ab8134-d376-4ebd-94cc-f48bcc7eacd6": "Infraestructura Tecnologica y Ciberseguridad en la Administracion Publica Estatal",
    "a3ea3c02-2e31-40b6-a90b-c12be719f9da": "Gobernanza Tecnologica en la Administracion Publica Estatal",
    "7c6183e5-5903-47c6-9fce-34f018bbdb6a": "Fortalezas y Debilidades del Entorno Digital de la Administracion Publica Estatal",
    "0e085b37-916a-4ef1-b949-c6e8b974f126": "Gobernanza de Datos en la Administracion Publica Estatal",
    "0ec245ba-6941-4995-a564-52e0a4f3999f": "Informacion General del Entorno Digital en la Administracion Publica Estatal",
    "aa353273-7ef0-4279-987a-40fc49b3d712": "Politica Digital en la Administracion Publica Estatal",
    "9208a313-553c-4308-8d58-506e037060b1": "Presupuesto para las TIC en la Administracion Publica Estatal",
    "d227c85d-0609-4ab4-9c4f-22aef39b670f": "Planeacion TIC en la Administracion Publica Estatal",
}

D_DES = "a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d"
D_MEJ = "af14d207-7697-4d52-b99b-46a35a1b76ac"
D_INF = "bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1"
D_GOB = "c65eb4e7-a17d-43c7-b08c-05811505edf1"
D_FOR = "f3ecd3d2-2156-4251-82e5-13b079471ee9"
D_IGEN = "3851f1c3-5045-4703-ba88-93b3d39e0b70"
D_POL = "063058e6-aed3-4a60-b944-5e653c77b14d"
D_GOBD = "90f5c6ec-026e-4216-9541-e4730c836ff1"
D_PRE = "8f8e3cfb-e551-4a95-b382-4999351c5f29"
D_PLA = "3b314916-24f7-4c48-bcb5-c5fe112a9123"

# Variables pendientes por politica explicita (motivo, razon corta).
# Todo lo no listado aqui y no metadato => propuesta.
PENDIENTES = {}
for _d in [D_DES, D_MEJ, D_INF, D_GOB, D_FOR, D_IGEN, D_POL, D_GOBD, D_PRE, D_PLA]:
    PENDIENTES[(_d, "ID")] = ("metadato-captura", "Identificador de fila de captura; no denota objeto de dominio.")
    PENDIENTES[(_d, "P2")] = ("generica-fragmento", "Fragmento de una palabra sin referente explicito; no se infiere sector por el ejemplo.")
    PENDIENTES[(_d, "P3")] = ("metadato-captura", "Hora de captura del cuestionario; metadato operativo, no objeto de dominio.")
    PENDIENTES[(_d, "P4")] = ("metadato-captura", "Hora de captura del cuestionario; metadato operativo, no objeto de dominio.")
    PENDIENTES[(_d, "P5")] = ("metadato-captura", "Hora de captura del cuestionario; metadato operativo, no objeto de dominio.")

_ABIERTA = "respuesta-abierta"
_ABIERTA_R = "Pregunta de texto libre sin referente cerrado ni dominio publicado; no defendible como significado compartido."
for _d in [D_DES, D_MEJ]:
    PENDIENTES[(_d, "P8")] = (_ABIERTA, "Pregunta compuesta y abierta (metodologia y documentacion); respuesta libre.")
    PENDIENTES[(_d, "P10")] = (_ABIERTA, _ABIERTA_R)
    PENDIENTES[(_d, "P13")] = (_ABIERTA, "Pregunta abierta de tipos de prueba; el ejemplo ('Si') ni siquiera es un tipo.")
    PENDIENTES[(_d, "P21")] = (_ABIERTA, "Pregunta abierta de lugar sin catalogo de ubicaciones publicado.")
    PENDIENTES[(_d, "P22")] = ("truncada-en-fuente", "Descripcion cortada a 199 caracteres con '...' en el diccionario publicado; objeto incompleto.")
    PENDIENTES[(_d, "P28")] = (_ABIERTA, _ABIERTA_R)
    PENDIENTES[(_d, "P36")] = ("contradiccion-tipo-descripcion", "El literal pide conteo ('Cuantos proyectos') pero el tipo declarado es Booleano con ejemplo 'Si'; no interpretable sin aclaracion.")
    PENDIENTES[(_d, "P39")] = ("contradiccion-tipo-descripcion", "El literal pregunta 'Como' (abierto, con errata 'atiene') pero el tipo declarado es Booleano; no interpretable sin aclaracion.")
    PENDIENTES[(_d, "P40")] = ("contradiccion-tipo-descripcion", "El literal pide conteo ('Cuantas personas', identico a P7) pero el tipo declarado es Booleano; solo P7 (Numerico) propone.")
for _v in ["P10", "P27", "P29", "P31", "P36", "P37"]:
    PENDIENTES[(D_INF, _v)] = (_ABIERTA, _ABIERTA_R)
PENDIENTES[(D_INF, "P9")] = ("contexto-dependiente-pregunta-previa", "El literal usa deictico 'este' (el datacenter de P6); aislado no nombra su objeto.")
PENDIENTES[(D_INF, "P21")] = ("generica-fragmento", "Literal generico ('el intercambio de informacion') sin objeto ni contraparte en el propio literal.")
PENDIENTES[(D_INF, "P33")] = ("generica-fragmento", "Literal de una palabra con errata ('Cuales?4'); sin referente.")
PENDIENTES[(D_INF, "P35")] = ("contexto-dependiente-pregunta-previa", "El literal remite a 'la consolidacion' de P34; aislado no nombra su objeto.")
for _d in [D_GOB, D_FOR]:
    for _v in ["P7", "P8", "P9", "P10", "P11", "P13"]:
        PENDIENTES[(_d, _v)] = (_ABIERTA, _ABIERTA_R)
for _v in ["P10", "P11", "P15", "P18", "P19", "P21", "P22", "P25"]:
    PENDIENTES[(D_IGEN, _v)] = (_ABIERTA, _ABIERTA_R)
PENDIENTES[(D_IGEN, "P10")] = ("generica-fragmento", "Fragmento sin predicado ('Actividades principales:'); no denota atributo determinable.")
PENDIENTES[(D_IGEN, "P11")] = ("contexto-dependiente-pregunta-previa", "El literal no nombra quien depende (remite a la unidad de P9); aislado insuficiente.")
PENDIENTES[(D_IGEN, "P15")] = ("contexto-dependiente-pregunta-previa", "El literal no nombra que perfil (remite al perfil tecnico de P14); aislado insuficiente.")
for _v in ["P7", "P9", "P11", "P13", "P15", "P17", "P20"]:
    for _d in [D_POL, D_GOBD]:
        PENDIENTES[(_d, _v)] = (_ABIERTA, _ABIERTA_R)
for _v in ["P10", "P16", "P18", "P21"]:
    for _d in [D_POL, D_GOBD]:
        PENDIENTES[(_d, _v)] = ("truncada-en-fuente", "Descripcion cortada en el diccionario publicado (199 caracteres con '...' o corte a media palabra); objeto incompleto.")
PENDIENTES[(D_PRE, "P11")] = ("contexto-dependiente-pregunta-previa", "El literal condiciona a 'la pregunta anterior' (P10); aislado no nombra su objeto.")
PENDIENTES[(D_PLA, "P9")] = (_ABIERTA, "Pide detalle libre sobre el plan; respuesta abierta sin referente cerrado.")

# Conceptos nuevos: slug -> [label, definicion, broader, representacion].
# Poblacion comun: dependencias/areas TIC de la APE Sonora encuestadas en el
# Diagnostico del Entorno Digital. Medida/objeto por concepto; distinciones explicitas.
NUEVOS = [
 ("dependencia-con-desarrolladores-software", "Dependencia con desarrolladores de software",
  "La dependencia declara contar con desarrolladores de software (respuesta Si/No del Diagnostico del Entorno Digital, APE Sonora). Poblacion: dependencias encuestadas; objeto: personal de desarrollo. No acredita numero, perfil ni adscripcion.", None, "no_especificada"),
 ("conteo-personas-desarrollo-software", "Personas dedicadas a desarrollo de software",
  "Numero de personas dedicadas a labores de desarrollo de software en la dependencia (respuesta entera del Diagnostico del Entorno Digital, APE Sonora). Poblacion: personal de la dependencia; medida: conteo de personas. Se distingue de P40 (misma pregunta con tipo Booleano, pendiente por contradiccion).", None, "no_especificada"),
 ("uso-metodologia-desarrollo-tradicional-agil", "Uso de metodologia de desarrollo tradicional o agil",
  "La dependencia declara usar alguna metodologia de desarrollo tradicional o agil (respuesta Si/No del Diagnostico del Entorno Digital, APE Sonora). No acredita cual metodologia (P10 queda pendiente por respuesta abierta).", None, "no_especificada"),
 ("formato-documento-levantamiento-requerimientos", "Formato para levantamiento de requerimientos de software",
  "La dependencia declara contar con formato o documento establecido para el levantamiento de requerimientos del software a desarrollar (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita el contenido del formato.", None, "no_especificada"),
 ("pruebas-automatizadas-ciclo-desarrollo", "Pruebas automatizadas en el ciclo de desarrollo",
  "La dependencia declara implementar pruebas automatizadas en el ciclo de desarrollo de software (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita tipos de prueba (P13 pendiente).", None, "no_especificada"),
 ("plan-recuperacion-perdida-software", "Plan de recuperacion ante perdida de software",
  "La dependencia declara contar con plan de recuperacion ante la perdida de software (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita contenido ni vigencia del plan.", None, "no_especificada"),
 ("repositorio-control-versiones", "Repositorio de control de versiones",
  "La dependencia declara contar con repositorio de control de versiones (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no verificada.", None, "no_especificada"),
 ("servicio-mesa-ayuda-incidencias", "Servicio de mesa de ayuda para incidencias",
  "La dependencia declara contar con servicio de mesa de ayuda para incidencias, reportes tecnicos y dudas (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del canal concreto de atencion (P39 pendiente).", None, "no_especificada"),
 ("conteo-proyectos-desarrollo-area", "Proyectos en desarrollo en el area",
  "Numero de proyectos en desarrollo actualmente por el area (respuesta entera del Diagnostico del Entorno Digital, APE Sonora). Poblacion: proyectos del area; medida: conteo. Se distingue de P36 (por dependencia, con tipo Booleano, pendiente).", None, "no_especificada"),
 ("cronograma-tiempos-proyectos-desarrollo", "Cronograma con tiempos de proyectos de desarrollo",
  "La dependencia declara contar con cronograma o documento con los tiempos requeridos para el desarrollo de los proyectos (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("paquetes-programas-informatica-adquiridos", "Paquetes y programas de informatica adquiridos con derecho de uso",
  "La dependencia declara contar con paquetes y programas de informatica adquiridos para los sistemas administrativos y operativos computarizados, con derecho de uso (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("codigo-fuente-disponible", "Codigo fuente disponible",
  "La dependencia declara contar con codigo fuente (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada; no acredita de que sistemas.", None, "no_especificada"),
 ("proceso-aprobaciones-actualizaciones", "Proceso de aprobaciones para actualizaciones",
  "Ante actualizaciones, la dependencia declara tener definido el proceso de aprobaciones (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("personas-designadas-valorar-peticiones", "Personas designadas para valorar peticiones",
  "La dependencia declara tener personas designadas para valorar y aprobar la procedencia de las peticiones (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia de designacion, no numero ni identidad.", None, "no_especificada"),
 ("criterios-aprobacion-peticiones", "Criterios para aprobar o rechazar peticiones",
  "La dependencia declara contar con criterios para determinar si la peticion se aprueba o no (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita el contenido de los criterios.", None, "no_especificada"),
 ("proceso-desarrollo-proyecto", "Proceso para desarrollar un proyecto",
  "La dependencia declara contar con algun proceso para llevar a cabo el desarrollo de un proyecto (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita el contenido del proceso.", None, "no_especificada"),
 ("uso-firma-electronica", "Uso de firma electronica",
  "La dependencia declara usar algun tipo de firma electronica (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita en que sistemas (P28 pendiente).", None, "no_especificada"),
 ("normativa-medios-identificacion-digitales", "Normativa de medios de identificacion digitales y firma",
  "La dependencia declara contar con normativa que regule medios de identificacion digitales, certificados electronicos y firma (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no texto normativo.", None, "no_especificada"),
 ("politica-gestion-documentos-electronicos", "Politica de gestion de documentos o expedientes electronicos",
  "La dependencia declara contar con politica de gestion de documentos y/o expedientes electronicos (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del sistema archivistico (concepto separado).", None, "no_especificada"),
 ("sistema-gestion-archivistica-electronica", "Sistema de gestion archivistica de documentos electronicos",
  "La dependencia declara contar con sistema de gestion archivistica de documentos electronicos (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de la politica de gestion (concepto separado): sistema vs norma.", None, "no_especificada"),
 ("procesos-calidad-seguridad-software", "Procesos de calidad y seguridad del software",
  "La dependencia declara contar con procesos que aseguren la calidad y seguridad del software (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("renovacion-tecnologica-anual-sistemas", "Necesidad anual de renovacion o solucion tecnologica",
  "La dependencia declara si sus sistemas requieren alguna renovacion o solucion tecnologica anualmente (Si/No, Diagnostico del Entorno Digital, APE Sonora). Percepcion declarada, no dictamen tecnico.", None, "no_especificada"),
 ("manual-identidad-institucion", "Manual de identidad de la institucion",
  "La dependencia declara contar con manual de identidad de la institucion (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("proyectos-desarrollo-software-curso", "Proyectos de desarrollo de software en curso",
  "La dependencia declara tener proyectos de desarrollo de software actualmente en curso (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no numero (el conteo por dependencia, P36, queda pendiente por contradiccion de tipo).", None, "no_especificada"),
 ("software-desarrollado-propio", "Software desarrollado propio",
  "La dependencia declara contar con software desarrollado (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no inventario.", None, "no_especificada"),
 ("proceso-gestion-peticiones-transformacion-digital", "Proceso para gestionar peticiones de transformacion digital",
  "La dependencia declara tener un proceso definido y conocido para gestionar nuevas peticiones de proyectos de transformacion digital (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("dependencia-con-datacenter", "Dependencia con centro de datos",
  "La dependencia declara contar con un datacenter (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada; no acredita suficiencia (P9 pendiente).", None, "no_especificada"),
 ("equipos-con-garantia-soporte", "Equipos con garantia y soporte",
  "La dependencia declara que sus equipos cuentan con garantia y soporte (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("volumen-almacenamiento-neto-gb", "Volumen de almacenamiento neto en GB",
  "Volumen de almacenamiento neto del datacenter en gigabytes (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: gigabytes. Limite: el ejemplo del diccionario ('No') no es numerico; el tipo declarado es Numerico.", None, "no_especificada"),
 ("volumen-procesamiento-neto-cpus", "Volumen de procesamiento neto en CPUs",
  "Volumen de procesamiento neto en cantidad de CPUs (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: numero de CPUs. Limite: el ejemplo del diccionario ('Si') no es numerico; el tipo declarado es Numerico.", None, "no_especificada"),
 ("volumen-memoria-ram-neto-gb", "Volumen de memoria RAM neto en GB",
  "Volumen de memoria RAM neto en gigabytes (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: gigabytes.", None, "no_especificada"),
 ("anio-adquisicion-equipos-infraestructura", "Anio de adquisicion de equipos de infraestructura",
  "Anio en que se realizo la adquisicion de los equipos de infraestructura tecnologica (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: anio calendario. Se distingue de anios censales o de registro del nucleo: es anio de compra de equipo. No se reutiliza el concepto generico 'anio'.", None, "no_especificada"),
 ("licenciamiento-vigente-servidores-equipos", "Licenciamiento vigente de servidores y equipos",
  "La dependencia declara que sus servidores y equipos de computo cuentan con licenciamiento vigente (Si/No, Diagnostico del Entorno Digital, APE Sonora). Declaracion, no auditoria de licencias.", None, "no_especificada"),
 ("servicio-nube-disponible", "Servicio en la nube disponible",
  "La dependencia declara disponer de algun servicio en la nube (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de la plataforma como servicio (concepto separado).", None, "no_especificada"),
 ("plataforma-servicios-nube-dependencia", "Plataforma como servicio en la nube",
  "La dependencia declara contar con una plataforma como servicio en la nube para su dependencia coordinadora (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del servicio en la nube generico (concepto separado).", None, "no_especificada"),
 ("planeacion-investigacion-ciberseguridad", "Planeacion e investigacion de ciberseguridad de largo plazo",
  "La dependencia declara realizar planeacion e investigacion de asuntos de ciberseguridad de largo plazo (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("monitoreo-activos-digitales", "Monitoreo de activos digitales",
  "La dependencia declara monitorear los activos digitales (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("ciberinteligencia-busqueda-amenazas", "Ciberinteligencia y busqueda de amenazas",
  "La dependencia declara realizar ciberinteligencia y busqueda de amenazas (Si/No, Diagnostico del Entorno Digital, APE Sonora). Practica declarada, no incidentes.", None, "no_especificada"),
 ("procedimientos-respuesta-recuperacion-incidentes", "Procedimientos de respuesta y recuperacion ante incidentes ciberneticos",
  "La dependencia declara tener procedimientos especificos para la respuesta y recuperacion ante incidentes ciberneticos (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no texto del procedimiento.", None, "no_especificada"),
 ("programas-concientizacion-riesgos-ciberneticos", "Programas de concientizacion sobre riesgos ciberneticos",
  "La dependencia declara haber implementado programas o acciones de concientizacion sobre riesgos y medidas preventivas de incidentes ciberneticos (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("cooperacion-operativa-local-incidentes", "Cooperacion operativa local ante incidentes ciberneticos",
  "La dependencia declara haber establecido alguna forma de cooperacion operativa a nivel local para enfrentar incidentes ciberneticos (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("ejercicios-simulacros-crisis-ciberneticas", "Ejercicios y simulacros ante incidentes ciberneticos",
  "La dependencia declara realizar ejercicios y simulacros de crisis y emergencias para prepararse ante incidentes ciberneticos (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("normativa-ciberseguridad", "Normativa de ciberseguridad",
  "La dependencia declara contar con alguna normativa de ciberseguridad (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada; el cuales (P27) queda pendiente por respuesta abierta.", None, "no_especificada"),
 ("normas-respuesta-crisis-resiliencia", "Normas de respuesta a incidentes, gestion de crisis y resiliencia digital",
  "La dependencia declara contar con normas especificas de respuesta a incidentes, gestion de crisis y resiliencia digital (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de las normas solo de respuesta a incidentes (concepto separado).", None, "no_especificada"),
 ("normas-respuesta-incidentes", "Normas de respuesta a incidentes",
  "La dependencia declara contar con normas especificas de respuesta a incidentes (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de las normas que anaden gestion de crisis y resiliencia (concepto separado).", None, "no_especificada"),
 ("normas-proteccion-infraestructuras-criticas", "Normas de proteccion de infraestructuras criticas",
  "Existencia declarada de normas especificas de proteccion de infraestructuras criticas (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("participacion-consolidacion-internet-2023", "Participacion en la consolidacion de servicios de internet de 2023",
  "La dependencia declara haber participado en la consolidacion de servicios de internet del 2023 (Si/No, Diagnostico del Entorno Digital, APE Sonora). Evento anual explicito en el literal; no se evalua el beneficio (P35-P37 pendientes).", None, "no_especificada"),
 ("equipos-computo-ofimatica-vigente", "Software de ofimatica vigente en equipos de computo",
  "La dependencia declara que sus equipos de computo cuentan con software de ofimatica vigente (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("equipos-computo-antivirus-vigente", "Software antivirus vigente en equipos de computo",
  "La dependencia declara que sus equipos de computo cuentan con software antivirus vigente (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de la ofimatica (concepto separado).", None, "no_especificada"),
 ("promocion-software-licenciado-politica", "Promocion del software licenciado como politica",
  "La dependencia declara promover el uso de software licenciado como politica para evitar incidentes operativos y financieros (Si/No, Diagnostico del Entorno Digital, APE Sonora). Politica declarada, no auditoria.", None, "no_especificada"),
 ("manual-uso-infraestructura-tecnologica", "Manual de uso de la infraestructura tecnologica",
  "La dependencia declara contar con manual de uso de la infraestructura tecnologica (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("politicas-segmentacion-red-vlans", "Politicas de segmentacion de red y VLANs",
  "El sector declara contar con politicas de segmentacion de red y VLANs para mitigar riesgos informaticos (Si/No, Diagnostico del Entorno Digital, APE Sonora). Poblacion: sector administrativo.", None, "no_especificada"),
 ("politicas-respaldo-datos-informacion", "Politicas de respaldo de datos e informacion",
  "El sector declara contar con politicas de respaldo de datos e informacion para usuarios y centros de datos (Si/No, Diagnostico del Entorno Digital, APE Sonora). Poblacion: sector administrativo.", None, "no_especificada"),
 ("proyectos-tic-uso-adquisicion-arrendamiento", "Generacion de proyectos TIC de uso, adquisicion o arrendamiento",
  "La dependencia coordinadora declara generar proyectos para uso, adquisicion y arrendamiento de bienes o contratacion y renovacion de servicios en materia de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). El como (P7) queda pendiente.", None, "no_especificada"),
 ("adquisiciones-tic-validadas-area-central", "Validacion central de adquisiciones TIC de las areas",
  "Adquisiciones de TIC de las areas validadas previamente por el area central de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Los comentarios (P13) quedan pendientes.", None, "no_especificada"),
 ("utics-solicitan-validacion-adquisiciones", "UTICs que solicitan validacion de adquisiciones TIC",
  "Las UTICs de las entidades del sector administrativo solicitan validacion de sus adquisiciones en materia TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Poblacion: UTICs de entidades del sector.", None, "no_especificada"),
 ("servicios-contratados-tic-hardware", "Servicios contratados de TIC con mantenimiento a hardware",
  "La dependencia declara contar con servicios contratados para uso de TIC que incluyen mantenimiento a hardware (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("unidad-coordinadora-tic", "Unidad coordinadora de TIC",
  "La dependencia coordinadora cuenta con una unidad coordinadora de TIC: existencia declarada (Si/No) y nombre indicado (texto) del Diagnostico del Entorno Digital, APE Sonora. Existencia y nombre son dos representaciones del mismo objeto en dos reglas separadas (criterio codigo/nombre); no se afirma organigrama ni adscripcion.", None, "no_especificada"),
 ("conteo-personas-area-tic", "Personas que integran el area de TIC",
  "Numero de personas que integran el area de TIC en la dependencia, entidad u organismo (respuesta entera del Diagnostico del Entorno Digital, APE Sonora). Medida: conteo de personas.", None, "no_especificada"),
 ("nivel-jerarquico-encargado-utic", "Nivel jerarquico de la persona encargada de la UTIC",
  "Nivel jerarquico declarado de la persona encargada de la UTIC coordinadora (texto del Diagnostico del Entorno Digital, APE Sonora). Atributo del puesto, no identidad de la persona.", None, "no_especificada"),
 ("perfil-tecnico-persona-a-cargo", "Perfil tecnico de la persona a cargo",
  "La dependencia declara si la persona a cargo tiene un perfil tecnico (Si/No, Diagnostico del Entorno Digital, APE Sonora). No acredita cual perfil (P15 pendiente por contexto-dependiente).", None, "no_especificada"),
 ("anio-inicio-a-cargo-utic", "Anio de inicio a cargo de la UTIC coordinadora",
  "Anio desde el que la persona esta a cargo de la UTIC coordinadora (respuesta entera del Diagnostico del Entorno Digital, APE Sonora). Medida: anio calendario de inicio de encargo. No se reutiliza el concepto generico 'anio' del nucleo (rol temporal distinto).", None, "no_especificada"),
 ("mejora-competencias-tecnicas-necesaria", "Necesidad de mejorar competencias tecnicas del personal",
  "La dependencia declara si cree que hace falta algo para mejorar las competencias tecnicas del personal (Si/No, Diagnostico del Entorno Digital, APE Sonora). Percepcion declarada; el que (P18) queda pendiente.", None, "no_especificada"),
 ("acciones-mejora-competencias-humanas", "Acciones de mejora continua de competencias humanas",
  "La dependencia declara llevar a cabo acciones o estrategias para la mejora continua de competencias humanas del personal de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue de las competencias tecnicas (concepto separado).", None, "no_especificada"),
 ("comunicacion-area-tic-titular", "Comunicacion del area de TIC con el titular",
  "El area de TIC declara mantener comunicacion constante y directa con el titular de su dependencia (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("comite-colegiado-decisiones-tic", "Comite o cuerpo colegiado de decisiones TIC",
  "La dependencia coordinadora declara contar con comite o cuerpo colegiado en funciones que participa en decisiones de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Los comentarios (P25) quedan pendientes.", None, "no_especificada"),
 ("condiciones-innovacion-tic-dependencia", "Condiciones para la innovacion en TIC",
  "La dependencia coordinadora declara tener las condiciones para la innovacion en TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). El cuales (P7) queda pendiente.", None, "no_especificada"),
 ("personal-tic-investiga-prototipos", "Personal de TIC que investiga y desarrolla prototipos",
  "El personal del area de TIC declara investigar y desarrollar prototipos con nuevas tecnologias por iniciativa propia (Si/No, Diagnostico del Entorno Digital, APE Sonora). Los ejemplos (P9) quedan pendientes.", None, "no_especificada"),
 ("recursos-destinados-innovacion", "Recursos destinados a la innovacion",
  "La dependencia coordinadora declara destinar recursos para la innovacion (Si/No, Diagnostico del Entorno Digital, APE Sonora). El detalle (P13) queda pendiente.", None, "no_especificada"),
 ("sector-con-reglamentos-antes-ley-digital", "Reglamentos del sector antes de la Ley de Gobierno Digital",
  "El sector declara que contaba con reglamentos, politicas, procedimientos o instrumentos de TIC antes de la publicacion de la Ley de Gobierno Digital (Si/No, Diagnostico del Entorno Digital, APE Sonora). Alcance temporal explicito en el literal. Se distingue de la dependencia coordinadora (P16 truncada, pendiente).", None, "no_especificada"),
 ("necesidad-expedicion-norma-funciones", "Necesidad de expedir norma para cumplir funciones",
  "La dependencia declara considerar necesaria la expedicion de alguna norma para cumplir con sus funciones (Si/No, Diagnostico del Entorno Digital, APE Sonora). Percepcion declarada; el cual (P20) queda pendiente.", None, "no_especificada"),
 ("planeacion-presupuestal-tic-sector", "Planeacion presupuestal TIC del sector",
  "El sector administrativo declara contar con planeacion presupuestal en materia de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Poblacion: sector; se distingue de la dependencia coordinadora (concepto separado).", None, "no_especificada"),
 ("presupuesto-anual-tic-sector-sin-rh", "Presupuesto anual TIC del sector sin recursos humanos",
  "Presupuesto anual asignado del sector en materia TIC, excluyendo recursos humanos (respuesta entera del Diagnostico del Entorno Digital, APE Sonora). Medida: monto anual. Limite: el ejemplo del diccionario no es numerico; el tipo declarado es Entero.", None, "no_especificada"),
 ("planeacion-presupuestal-tic-dependencia", "Planeacion presupuestal TIC de la dependencia",
  "La dependencia coordinadora declara contar con planeacion presupuestal en materia de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del sector (concepto separado).", None, "no_especificada"),
 ("presupuesto-anual-tic-dependencia-sin-rh", "Presupuesto anual TIC de la dependencia sin recursos humanos",
  "Presupuesto anual asignado de la dependencia coordinadora en materia TIC, excluyendo recursos humanos (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: monto anual. Se distingue del sector (concepto separado).", None, "no_especificada"),
 ("requerimiento-presupuesto-extra-tic", "Requerimiento de presupuesto extra en TIC",
  "El area declara requerir presupuesto extra en materia de TIC adicional al asignado (Si/No, Diagnostico del Entorno Digital, APE Sonora). La planeacion de ese requerimiento (P11) queda pendiente por contexto-dependiente.", None, "no_especificada"),
 ("presupuesto-adicional-anual-requerido", "Presupuesto adicional anual requerido",
  "Monto de presupuesto adicional anual que requiere el area en TIC (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: monto anual.", None, "no_especificada"),
 ("vehiculos-a-cargo-area-tic", "Vehiculos a cargo del area de TIC",
  "El area de TIC declara tener vehiculos a su cargo (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del conteo (concepto separado).", None, "no_especificada"),
 ("conteo-vehiculos-area-tic", "Vehiculos a cargo del area de TIC",
  "Numero de vehiculos a cargo del area de TIC (respuesta numerica del Diagnostico del Entorno Digital, APE Sonora). Medida: conteo de vehiculos. Se distingue de la existencia (concepto separado).", None, "no_especificada"),
 ("area-responsable-plan-desarrollo", "Area responsable del plan de desarrollo, trabajo o estrategico",
  "Area declarada responsable de formular el plan de desarrollo, de trabajo o estrategico en la dependencia (texto del Diagnostico del Entorno Digital, APE Sonora). Representacion nombre.", None, "nombre"),
 ("plan-desarrollo-trabajo-estrategico-existente", "Plan de desarrollo, trabajo o estrategico existente",
  "La dependencia declara conocer o contar con un plan de desarrollo, de trabajo o estrategico (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no contenido (P9 pendiente).", None, "no_especificada"),
 ("plan-incluye-seccion-tic", "Plan con seccion de uso de TIC",
  "El plan de desarrollo, trabajo o estrategico declara incluir una seccion especifica sobre el uso y aprovechamiento de las TIC en el sector administrativo (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
 ("plan-tic-sector", "Plan en materia de TIC del sector",
  "El sector declara contar con un plan en materia de TIC (Si/No, Diagnostico del Entorno Digital, APE Sonora). Se distingue del plan general de desarrollo (concepto separado).", None, "no_especificada"),
 ("metas-tic-sector", "Metas en materia TIC del sector",
  "Existencia declarada de metas en materia TIC en el sector (Si/No, Diagnostico del Entorno Digital, APE Sonora). Existencia declarada, no cuales metas.", None, "no_especificada"),
 ("plan-incluye-secciones-entidades-coordinadas", "Plan con secciones de entidades coordinadas",
  "El plan de desarrollo, trabajo o estrategico declara incluir secciones especificas sobre las entidades que coordina el sector (Si/No, Diagnostico del Entorno Digital, APE Sonora).", None, "no_especificada"),
]

_DES = ["P6:dependencia-con-desarrolladores-software", "P7:conteo-personas-desarrollo-software",
        "P9:uso-metodologia-desarrollo-tradicional-agil", "P11:formato-documento-levantamiento-requerimientos",
        "P12:pruebas-automatizadas-ciclo-desarrollo", "P14:plan-recuperacion-perdida-software",
        "P15:repositorio-control-versiones", "P16:servicio-mesa-ayuda-incidencias",
        "P17:conteo-proyectos-desarrollo-area", "P18:cronograma-tiempos-proyectos-desarrollo",
        "P19:paquetes-programas-informatica-adquiridos", "P20:codigo-fuente-disponible",
        "P23:proceso-aprobaciones-actualizaciones", "P24:personas-designadas-valorar-peticiones",
        "P25:criterios-aprobacion-peticiones", "P26:proceso-desarrollo-proyecto",
        "P27:uso-firma-electronica", "P29:normativa-medios-identificacion-digitales",
        "P30:politica-gestion-documentos-electronicos", "P31:sistema-gestion-archivistica-electronica",
        "P32:procesos-calidad-seguridad-software", "P33:renovacion-tecnologica-anual-sistemas",
        "P34:manual-identidad-institucion", "P35:proyectos-desarrollo-software-curso",
        "P37:software-desarrollado-propio", "P38:proceso-gestion-peticiones-transformacion-digital"]
SLUG_POR_VAR = {}
for _d in [D_DES, D_MEJ]:
    for _e in _DES:
        _v, _s = _e.split(":")
        SLUG_POR_VAR[(_d, _v)] = _s
_INF = ["P6:dependencia-con-datacenter", "P7:equipos-con-garantia-soporte",
        "P11:volumen-almacenamiento-neto-gb", "P12:volumen-procesamiento-neto-cpus",
        "P13:volumen-memoria-ram-neto-gb", "P14:anio-adquisicion-equipos-infraestructura",
        "P15:licenciamiento-vigente-servidores-equipos", "P16:servicio-nube-disponible",
        "P17:plataforma-servicios-nube-dependencia", "P18:planeacion-investigacion-ciberseguridad",
        "P19:monitoreo-activos-digitales", "P20:ciberinteligencia-busqueda-amenazas",
        "P22:procedimientos-respuesta-recuperacion-incidentes", "P23:programas-concientizacion-riesgos-ciberneticos",
        "P24:cooperacion-operativa-local-incidentes", "P25:ejercicios-simulacros-crisis-ciberneticas",
        "P26:normativa-ciberseguridad", "P28:normas-respuesta-crisis-resiliencia",
        "P30:normas-respuesta-incidentes", "P32:normas-proteccion-infraestructuras-criticas",
        "P34:participacion-consolidacion-internet-2023", "P38:equipos-computo-ofimatica-vigente",
        "P39:equipos-computo-antivirus-vigente", "P40:promocion-software-licenciado-politica",
        "P41:manual-uso-infraestructura-tecnologica", "P42:politicas-segmentacion-red-vlans",
        "P43:politicas-respaldo-datos-informacion"]
for _e in _INF:
    _v, _s = _e.split(":")
    SLUG_POR_VAR[(D_INF, _v)] = _s
_GF = ["P6:proyectos-tic-uso-adquisicion-arrendamiento", "P12:adquisiciones-tic-validadas-area-central",
       "P14:utics-solicitan-validacion-adquisiciones", "P15:servicios-contratados-tic-hardware"]
for _d in [D_GOB, D_FOR]:
    for _e in _GF:
        _v, _s = _e.split(":")
        SLUG_POR_VAR[(_d, _v)] = _s
_IG = ["P8:unidad-coordinadora-tic", "P9:unidad-coordinadora-tic",
       "P12:conteo-personas-area-tic", "P13:nivel-jerarquico-encargado-utic",
       "P14:perfil-tecnico-persona-a-cargo", "P16:anio-inicio-a-cargo-utic",
       "P17:mejora-competencias-tecnicas-necesaria", "P20:acciones-mejora-competencias-humanas",
       "P23:comunicacion-area-tic-titular", "P24:comite-colegiado-decisiones-tic"]
for _e in _IG:
    _v, _s = _e.split(":")
    SLUG_POR_VAR[(D_IGEN, _v)] = _s
_PO = ["P6:condiciones-innovacion-tic-dependencia", "P8:personal-tic-investiga-prototipos",
       "P12:recursos-destinados-innovacion", "P14:sector-con-reglamentos-antes-ley-digital",
       "P19:necesidad-expedicion-norma-funciones"]
for _d in [D_POL, D_GOBD]:
    for _e in _PO:
        _v, _s = _e.split(":")
        SLUG_POR_VAR[(_d, _v)] = _s
_PR = ["P6:planeacion-presupuestal-tic-sector", "P7:presupuesto-anual-tic-sector-sin-rh",
       "P8:planeacion-presupuestal-tic-dependencia", "P9:presupuesto-anual-tic-dependencia-sin-rh",
       "P10:requerimiento-presupuesto-extra-tic", "P12:presupuesto-adicional-anual-requerido",
       "P13:vehiculos-a-cargo-area-tic", "P14:conteo-vehiculos-area-tic"]
for _e in _PR:
    _v, _s = _e.split(":")
    SLUG_POR_VAR[(D_PRE, _v)] = _s
_PL = ["P6:area-responsable-plan-desarrollo", "P7:plan-desarrollo-trabajo-estrategico-existente",
       "P8:plan-incluye-seccion-tic", "P10:plan-tic-sector", "P11:metas-tic-sector",
       "P12:plan-incluye-secciones-entidades-coordinadas"]
for _e in _PL:
    _v, _s = _e.split(":")
    SLUG_POR_VAR[(D_PLA, _v)] = _s
del _DES, _INF, _GF, _IG, _PO, _PR, _PL, _d, _e, _v, _s
REP_POR_VAR = {(D_IGEN, "P9"): "nombre", (D_PLA, "P6"): "nombre"}

def main():
    asig = json.load(open(ROOT / "propuestas" / "ronda-3" / "integrador" / "asignaciones-semanticas.json", encoding="utf-8"))
    vars9 = asig["asignaciones"]["9"]["variables"]
    assert len(vars9) == 243, len(vars9)
    assert all(v["estado"] == "fuera_del_nucleo_actual" for v in vars9)
    iris = [v["definicion_iri"] for v in vars9]
    assert len(set(iris)) == 243, "IRIs duplicadas en asignacion"

    insp = {}
    for d in {v["diccionario"] for v in vars9}:
        insp[d] = json.load(open(ROOT / "data" / "portal" / "inspecciones" / (d + ".json"), encoding="utf-8"))
    assert set(insp) == {D_DES, D_MEJ, D_INF, D_GOB, D_FOR, D_IGEN, D_POL, D_GOBD, D_PRE, D_PLA}

    sem = json.load(open(ROOT / "ontologia" / "semantica.json", encoding="utf-8"))
    assert len(sem["conceptos"]) == 103
    cob = json.load(open(ROOT / "data" / "semantica" / "cobertura.json", encoding="utf-8"))

    mapa = {}
    for slug, label, definicion, broader, rep in NUEVOS:
        mapa[slug] = {"label": label, "definicion": definicion, "broader": broader, "rep": rep}
    assert set(mapa) == set(SLUG_POR_VAR.values()), "slugs sin uso o sin definir"
    prop_keys = set()
    for v in vars9:
        key = (v["diccionario"], v["variable"])
        if key not in PENDIENTES:
            prop_keys.add(key)
    assert prop_keys == set(SLUG_POR_VAR), (prop_keys ^ set(SLUG_POR_VAR))
    lit_por_slug = {}
    for v in vars9:
        key = (v["diccionario"], v["variable"])
        if key in SLUG_POR_VAR:
            lit_por_slug.setdefault(SLUG_POR_VAR[key], set()).add(v["descripcion"])
    for slug, lits in lit_por_slug.items():
        if slug == "unidad-coordinadora-tic":
            assert len(lits) == 2, (slug, lits)
        else:
            assert len(lits) == 1, (slug, lits)
    inv = {}
    for slug, lits in lit_por_slug.items():
        inv.setdefault(next(iter(lits)), []).append(slug)
    for lit, slugs in inv.items():
        assert len(slugs) == 1, (lit, slugs)

    decisiones, reglas = [], []
    n = 0
    for v in sorted(vars9, key=lambda x: (x["diccionario"], x["variable"])):
        d = insp[v["diccionario"]]
        rows = [r for r in d["definiciones"] if str(r.get("Nombre variable")) == v["variable"]]
        assert len(rows) == 1
        row = rows[0]
        h = huella(row)
        assert h == v["huella_fila_diccionario"], (v["diccionario"], v["variable"])
        idx = d["definiciones"].index(row) + 1
        assert v["definicion_iri"] == BASE + "definition/" + v["diccionario"] + "%2F" + str(idx), v["definicion_iri"]
        tipo = str(row.get("Tipo de dato", ""))
        unidad = str(row.get("Unidad de medida", "") or "")
        ejemplo = row.get("Ejemplo de dato", "")
        ejemplo = "" if ejemplo is None else str(ejemplo)
        catalogo = str(row.get("Cat\u00e1logo de referencia", "") or "")
        key = (v["diccionario"], v["variable"])
        base_dec = {"definicion_iri": v["definicion_iri"], "conjunto": v["conjunto"],
                    "titulo_conjunto": v.get("titulo_conjunto", ""), "diccionario": v["diccionario"],
                    "variable": v["variable"], "descripcion": v["descripcion"], "tipo_de_dato": tipo,
                    "unidad_de_medida": unidad, "ejemplo_de_dato": ejemplo,
                    "catalogo_de_referencia": catalogo, "huella_fila_diccionario": h}
        if key in PENDIENTES:
            motivo, razon = PENDIENTES[key]
            decisiones.append({**base_dec, "veredicto": "pendiente", "motivo": motivo, "razon": razon,
                               "criterio": "Lectura literal individual + contexto publicado (tema Diagnostico del Entorno Digital, APE Sonora; tipo/ejemplo del diccionario). Sin significado documental."})
        else:
            slug = SLUG_POR_VAR[key]
            n += 1
            rid = "r3a9-%03d" % n
            rep = REP_POR_VAR.get(key, "no_especificada")
            decisiones.append({**base_dec, "veredicto": "propuesta", "regla": rid, "concepto": slug,
                               "criterio": "Descripcion literal especifica (poblacion/objeto/medida en el propio literal) + contexto publicado del conjunto + tipo coherente. Alcance fijado a esta definicion."})
            reglas.append({"id": rid, "concepto": slug, "representacion": rep,
                           "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
                           "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
                           "definiciones": [v["definicion_iri"]],
                           "criterio": "Revision agente 9 ronda 3; lectura literal individual; alcance fijado a esta definicion.",
                           "fuente_revision": "propuestas/ronda-3/agente-9-gobierno-digital/propuestas.json",
                           "alcance": "Solo este conjunto, diccionario, definicion y nombre.",
                           "positivo": "Denota exactamente el atributo del literal en la unidad encuestada.",
                           "contraejemplo": "No aplica a otra definicion, variable, conjunto o instrumento aunque el texto parezca similar; cada regla exige su definicion IRI.",
                           "limite": "Respuesta declarada en encuesta (Si/No, conteo o texto); no verifica hechos ni acredita vigencia, identidad o catalogos.",
                           "evidencia": [{"variable": v["variable"], "descripcion": v["descripcion"],
                                          "definicion_iri": v["definicion_iri"], "diccionario": v["diccionario"],
                                          "conjunto": v["conjunto"], "unidad_de_medida": unidad,
                                          "tipo_de_dato": tipo, "ejemplo_de_dato": ejemplo,
                                          "catalogo_de_referencia": catalogo}]})
    conceptos_nuevos = {slug: [mapa[slug]["label"], mapa[slug]["definicion"], mapa[slug]["broader"]] for slug in sorted(mapa)}
    usados = {r["concepto"] for r in reglas}
    assert usados == set(conceptos_nuevos), (usados ^ set(conceptos_nuevos))

    def sha(p):
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    huellas = {"asignaciones_semanticas": sha(ROOT / "propuestas" / "ronda-3" / "integrador" / "asignaciones-semanticas.json"),
               "cobertura_sha": asig.get("sha256_cobertura", ""),
               "reglas": cob["huellas_entrada"]["reglas"],
               "inventario": cob["huellas_entrada"]["inventario"],
               "inspeccion": cob["huellas_entrada"]["inspeccion"]}
    for dd in sorted(insp):
        huellas["inspeccion_" + dd] = sha(ROOT / "data" / "portal" / "inspecciones" / (dd + ".json"))

    propuestas = {"generado_en_utc": datetime.now(timezone.utc).isoformat(),
                  "agente": "agente-9-gobierno-digital",
                  "base_iri": BASE,
                  "huellas_entrada": huellas,
                  "alcance": "Particion exclusiva del agente 9: 243 definiciones fuera_del_nucleo_actual de 10 diccionarios del Diagnostico del Entorno Digital (APE Sonora). Sin nuevas correspondencias columna->variable; sin sameAs/exactMatch.",
                  "decisiones": decisiones,
                  "reglas": reglas,
                  "conceptos_nuevos": conceptos_nuevos,
                  "conceptos_reutilizados": [],
                  "nota_reutilizacion": "Ninguno de los 103 conceptos vigentes es exacto: 'anio' generico no cubre anios de compra/encargo con rol distinto; 'organizacion' no cubre el fragmento generico 'Sector'; no se promueve ningun codigo a catalogo, identidad, etnia ni diagnostico.",
                  "limites": ["Sin U+FFFD en la particion (verificado en las 243 filas): acentos, apertura de interrogacion, NBSP y elipsis preservados byte a byte; tampoco ene-tilde->n en entregas.",
                              "Descripciones truncadas a 199 caracteres o cortadas a media palabra quedan pendientes.",
                              "Conceptos compartidos entre instrumentos pares (desarrollo/mejora, gobtec/fortalezas, politica/gobdatos) denotan la misma pregunta; no se afirma equivalencia de instrumentos.",
                              "Respuestas Si/No = existencia declarada, no verificacion; conteos = declarados, sin unidad publicada salvo GB/CPUs en el literal.",
                              "catalogo_de_referencia vacio en las 243: ninguna regla promueve catalogos.",
                              "Sin red, sin microdatos, sin contacto con publicadores; pendiente no es promocion."],
                  "conteos": {"decisiones": len(decisiones),
                              "propuestas": sum(1 for x in decisiones if x["veredicto"] == "propuesta"),
                              "pendientes": sum(1 for x in decisiones if x["veredicto"] == "pendiente"),
                              "reglas": len(reglas), "conceptos_nuevos": len(conceptos_nuevos)}}
    out = R3A9 / "propuestas.json"
    with io.open(str(out), "w", encoding="utf-8") as f:
        json.dump(propuestas, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps(propuestas["conteos"], indent=1))
    print("pendientes por motivo:", json.dumps(
        {m: sum(1 for x in decisiones if x.get("motivo") == m) for m in sorted({x.get("motivo", "") for x in decisiones if x["veredicto"] == "pendiente"})},
        indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
