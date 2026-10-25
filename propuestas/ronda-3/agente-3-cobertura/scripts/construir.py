"""Construye la entrega del agente 3 (ronda 3): inventario de cobertura y
propuestas de significado para 4 familias con lectura completa.

Solo LEE fuera de su carpeta; solo ESCRIBE dentro de ella.
No ejecuta consolidar/ampliar/sincronizar. Sin red. Solo stdlib.

Criterio de correccion del integrador (ronda 3):
- Un concepto estrecho por categoria/estado/poblacion (vacas != toros,
  sembrada != cosechada != siniestrada, bovino != menor).
- Agrupacion solo via broader explicito o calificador formal por regla.
- La unidad se lee fila por fila del diccionario; si falta, no se deduce.
- Los textos de evidencia salen byte-exactos de las fuentes; la prosa
  analitica nunca transcribe literales (solo cita identificadores/IRIs).

Uso desde la raiz del proyecto:
  uv run python propuestas/ronda-3/agente-3-cobertura/scripts/construir.py
"""
import collections
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import validar_propuestas  # noqa: E402

AQUI = Path(__file__).resolve().parent.parent
ROOT = AQUI.parent.parent.parent  # propuestas/ronda-3/agente-3-cobertura -> raiz
PEND = ROOT / "reports" / "pendientes-semanticos.json"
COB = ROOT / "data" / "semantica" / "cobertura.json"
SEM = ROOT / "ontologia" / "semantica.json"
INV = ROOT / "data" / "portal" / "inventario.json"
INSP = ROOT / "data" / "portal" / "contenido-inspeccion.json"

FAMS = {
    "045da7ba-ee72-498a-9b7a-071176e2a4ea": "censo",
    "94215f51-9c89-414d-8c3d-92792e609a2a": "agricultura",
    "863b9cc8-daeb-4430-b835-6a0ced5abd31": "pesca",
    "a7591bc9-f905-45cb-ba6c-ae3588d87594": "trigo",
}

# Claves de fila observadas en los 4 diccionarios leidos.
K_NOMBRE = {"nombre variable"}
K_DESC = {"descripcion", "definicion"}
K_UNIDAD = {"unidad de medida", "unidades de medida"}
K_TIPO = {"tipo de dato"}
K_EJEMPLO = {"ejemplo de dato"}


def _normkey(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s.strip().lower())
                   if unicodedata.category(c) != "Mn")


def valor(row, keys):
    for k, v in row.items():
        if _normkey(k) in keys and isinstance(v, str) and v.strip():
            return v
    return ""


def valor_crudo(row, keys):
    for k, v in row.items():
        if _normkey(k) in keys and isinstance(v, str):
            return v
    return ""


# (familia, variable, concepto, representacion, unidad_esperada|None,
#  calificador|None, alcance, positivo, contraejemplo, limite)
# unidad_esperada=None -> no se exige unidad (se registra la literal, vacia o no).
# Si se fija, la fila debe traerla exacta o la construccion falla.
REGLAS_SPEC = []

# --- Censo Ganadero: una categoria, un concepto; totales con poblacion distinta ---
_CENSO_CATS = [
    ("VACAS", "conteo-vacas-censo", "vacas"),
    ("TOROS", "conteo-toros-censo", "toros"),
    ("VAQUILLAS", "conteo-vaquillas-censo", "vaquillas"),
    ("NOVILLOS", "conteo-novillos-censo", "novillos"),
    ("BECERRAS", "conteo-becerras-censo", "becerras"),
    ("BECERROS", "conteo-becerros-censo", "becerros"),
    ("PORCINOS", "conteo-porcinos-censo", "porcinos"),
    ("EQUINO", "conteo-equinos-censo", "equinos"),
    ("CAPRINO", "conteo-caprinos-censo", "caprinos"),
    ("MULAR", "conteo-mulares-censo", "mulares"),
    ("ASNAL", "conteo-asnos-censo", "asnos"),
    ("OVINOS", "conteo-ovinos-censo", "ovinos"),
]
for _var, _con, _cat in _CENSO_CATS:
    REGLAS_SPEC.append(
        ("censo", _var, _con, "no_especificada", "Cabezas", None,
         "Solo este diccionario, conjunto, definición y nombre.",
         "Denota el conteo de cabezas de la categoría de la evidencia.",
         "No aplica a otra categoría (cada categoría tiene su concepto) ni a "
         "No_PROD_CENSADOS (población productores) ni a totales.",
         "Categoría conservada por concepto; no demuestra exhaustividad de "
         "categorías ni igualdad con totales."))

REGLAS_SPEC += [
    ("censo", "TOTAL_GANADO_BOVINO", "total-ganado-bovino-censo", "no_especificada", "Cabezas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el total de ganado bovino registrado.",
     "No aplica a TOTAL_GANADO_MENOR (población ganado menor, concepto distinto) "
     "ni a categorías individuales.",
     "Población explícita: ganado bovino. No demuestra igualdad con la suma de categorías."),
    ("censo", "TOTAL_GANADO_MENOR", "total-ganado-menor-censo", "no_especificada", "Cabezas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el total de ganado menor registrado.",
     "No aplica a TOTAL_GANADO_BOVINO (población ganado bovino, concepto distinto).",
     "Población explícita: ganado menor. No demuestra igualdad con la suma de categorías."),
    ("censo", "No_PROD_CENSADOS", "productores-ganaderos-censados", "no_especificada", "Productores", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el conteo de productores ganaderos censados.",
     "No aplica a ningún conteo de cabezas (población distinta).",
     "Población productores, no cabezas."),
    ("censo", "DDR", "ddr-registro", "no_especificada", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el distrito de desarrollo rural del registro censal.",
     "La regla ddr-municipio no aplica (función municipio no declarada aquí).",
     "Sin unidad declarada en la fila; ejemplo combina clave y nombre sin separador "
     "documentado; no resuelve catálogo oficial."),
    ("censo", "REGION", "region-geografica-estado", "no_especificada", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la región geográfica del estado declarada para el registro.",
     "La regla region-municipio no aplica (función municipio no declarada aquí).",
     "Sin unidad declarada; no vincula a municipio concreto ni prueba exclusividad."),
    ("censo", "CUENCA", "cuenca-referencia-registro", "no_especificada", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la cuenca hidrológica de referencia del registro.",
     "La regla cuenca-municipio no aplica (función municipio no declarada aquí).",
     "Sin unidad declarada; 'de referencia' limita el alcance al registro; "
     "no prueba correspondencia geoespacial."),
]

# --- Agricultura Sonora ---
REGLAS_SPEC += [
    ("agricultura", "CDDR", "ddr-registro-cultivo", "codigo", "CCC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave del DDR donde se registra el cultivo.",
     "NDDR no aplica a esta regla (es nombre, otra regla).",
     "Clave sin catálogo resuelto."),
    ("agricultura", "NDDR", "descripcion-ddr-registro-cultivo", "no_especificada", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la descripción del DDR del cultivo según la fuente.",
     "CDDR no aplica a esta regla (es código, otra regla).",
     "Sin unidad declarada; la fila declara tipo Numérico con ejemplo vacío, en conflicto "
     "con 'Descripción': registrado sin deducir formato ni catálogo."),
    ("agricultura", "CMUN", "municipio-registro-cultivo", "codigo", "CC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave del municipio donde se registra el cultivo.",
     "La regla municipio-nombre no aplica (texto y función distintos).",
     "No resuelve CVEGEO ni catálogo."),
    ("agricultura", "NMUN", "municipio-registro-cultivo-nombre", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre del municipio en que se registra el cultivo.",
     "La regla municipio-registro-delito no aplica (evento distinto).",
     "Sin unidad declarada; no resuelve identidad municipal entre fuentes."),
    ("agricultura", "CVMES", "mes-registro-cultivo", "codigo", "CC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave del mes en que se registra el cultivo.",
     "La regla mes-registro no aplica (objeto cultivo no declarado allá).",
     "Requiere año como contexto."),
    ("agricultura", "NMES", "mes-registro-cultivo-nombre", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre del mes en que se registra el cultivo.",
     "CVMES no aplica a esta regla (es código, otra regla).",
     "Sin unidad declarada; requiere año como contexto."),
    ("agricultura", "CULTIVO", "cultivo-registrado", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre del cultivo.",
     "DESVAR no aplica (variedad, otra regla).",
     "Sin unidad declarada; un nombre no es identidad global entre fuentes."),
    ("agricultura", "CVECUL", "cultivo-registrado-clave", "codigo", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave identificadora del cultivo.",
     "CVEVAR no aplica (variedad, otra regla).",
     "Sin unidad declarada; clave sin catálogo resuelto."),
    ("agricultura", "DESVAR", "variedad-cultivo", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre de la variedad del cultivo.",
     "CULTIVO no aplica (cultivo, otra regla).",
     "Sin unidad declarada; sin catálogo resuelto."),
    ("agricultura", "CVEVAR", "variedad-cultivo-clave", "codigo", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave identificadora de la variedad del cultivo.",
     "CVECUL no aplica (cultivo, otra regla).",
     "Sin unidad declarada; clave sin catálogo resuelto."),
    ("agricultura", "CIERREYAVAN", "estado-cierre-avance-cultivo", "no_especificada",
     "CIERRE DE PRODUCCION AGRICOLA AAAA ; AVANCE DE PRODUCCION AGRICOLA AAAA", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota si el registro es dato de cierre o de avance de producción.",
     "Un dato de avance no equivale a un dato de cierre.",
     "AAAA es marcador sin año concreto en la unidad literal; avance y cierre no comparables."),
    ("agricultura", "SUPSEM", "superficie-sembrada-cultivo", "no_especificada", "Hectáreas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota superficie sembrada del cultivo.",
     "SUPCOSE y SUPSINI no aplican (estados distintos, conceptos distintos).",
     "Estado sembrada conservado por concepto; no se infiere balance con otros estados."),
    ("agricultura", "SUPCOSE", "superficie-cosechada-cultivo", "no_especificada", "Hectáreas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota superficie cosechada del cultivo.",
     "SUPSEM y SUPSINI no aplican (estados distintos, conceptos distintos).",
     "Estado cosechada conservado por concepto; no se infiere balance con otros estados."),
    ("agricultura", "SUPSINI", "superficie-siniestrada-cultivo", "no_especificada", "Hectáreas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota superficie siniestrada del cultivo.",
     "SUPSEM y SUPCOSE no aplican (estados distintos, conceptos distintos).",
     "Estado siniestrada conservado por concepto; no se infiere balance con otros estados."),
    ("agricultura", "PRODTON", "produccion-cultivo-toneladas", "no_especificada", "Toneladas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota producción total obtenida.",
     "SUPSEM no aplica (superficie, otra regla).",
     "Medida en la unidad literal de la fila."),
    ("agricultura", "RENDMNTO", "rendimiento-cultivo", "no_especificada", "Toneladas/hectáreas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota rendimiento como producción por hectárea sembrada.",
     "PRODTON no aplica (total, no cociente por hectárea).",
     "No verifica el cálculo."),
    ("agricultura", "PMR", "precio-medio-rural-cultivo", "no_especificada", "Pesos por tonelada", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el precio medio del cultivo como cociente valor/producción.",
     "VALPROD no aplica (valor total, otra regla).",
     "No verifica el cálculo del cociente."),
    ("agricultura", "VALPROD", "valor-produccion-cultivo", "no_especificada", "Miles de pesos MXN", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el valor total producido por cultivo.",
     "PMR no aplica (precio por tonelada, otra regla).",
     "Medida en la unidad literal de la fila."),
]

# --- Pesca y Acuacultura ---
REGLAS_SPEC += [
    ("pesca", "CDDR", "ddr-registro-pesquero", "codigo", "CCC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave del DDR donde se registra la producción pesquera.",
     "La regla ddr-registro-cultivo no aplica (otro conjunto y objeto).",
     "Clave sin catálogo resuelto."),
    ("pesca", "NDDR", "descripcion-ddr-registro-pesquero", "no_especificada", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la descripción del DDR de la producción pesquera según la fuente.",
     "CDDR no aplica a esta regla (es código, otra regla).",
     "Sin unidad declarada; tipo Texto con ejemplo vacío: no hay evidencia de nombre puro; "
     "sin deducir formato ni catálogo."),
    ("pesca", "CMUN", "municipio-registro-pesquero", "codigo", "CC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave del municipio donde se registra la producción.",
     "La regla municipio-registro-cultivo no aplica (otro conjunto y objeto).",
     "No resuelve CVEGEO."),
    ("pesca", "CVEOF", "oficina-pesquera-registro", "codigo", "CCCC", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave de la oficina pesquera donde se registra la producción.",
     "NOFICINA no aplica a esta regla (es nombre, otra regla).",
     "No identifica publicadora ni capturadora."),
    ("pesca", "NOFICINA", "oficina-pesquera-registro-nombre", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre de la oficina pesquera donde se registra la producción.",
     "CVEOF no aplica a esta regla (es código, otra regla).",
     "Sin unidad declarada; no identifica publicadora ni capturadora."),
    ("pesca", "ESPECIE", "especie-producida-pesca", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre de la especie producida.",
     "ORIGEN no aplica (origen, otra regla).",
     "Sin unidad declarada; sin catálogo resuelto."),
    ("pesca", "CESPE", "especie-producida-pesca-clave", "codigo", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave numérica de la especie producida.",
     "CVEOF no aplica (oficina, otra regla).",
     "Sin unidad declarada; clave sin catálogo resuelto."),
    ("pesca", "ORIGEN", "origen-produccion-pesquera", "nombre", "Captura; Cosecha; Aguas Continentales", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre del origen de la producción con las etiquetas literales de la fila.",
     "ESPECIE no aplica (especie, otra regla).",
     "El diccionario no publica mapeo código-etiqueta: prohibido mapear 1, 2, 3 por orden."),
    ("pesca", "CVORIGEN", "origen-produccion-pesquera-clave", "codigo", "1, 2, 3", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave numérica del origen de la producción.",
     "Asignar 1=Captura por orden no está documentado y queda prohibido.",
     "Claves literales sin mapeo publicado a etiquetas."),
    ("pesca", "PESODESEMB", "peso-desembarcado-pesca", "no_especificada", "Toneladas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el peso al desembarque con las modalidades literales de la definición.",
     "PVIVO no aplica (peso vivo, otra regla).",
     "Modalidades conservadas sin homologar."),
    ("pesca", "PVIVO", "peso-vivo-pesca", "no_especificada", "Toneladas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el peso total en captura estimado por factores de conversión.",
     "El peso desembarcado no equivale al peso vivo.",
     "Factores FAO/INAPESCA citados sin verificar; no convertir."),
    ("pesca", "VALOR", "valor-produccion-pesquera", "no_especificada", "Pesos MXN", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el valor total producido.",
     "Los pesos físicos no aplican (cantidades, otras reglas).",
     "Medida en la unidad literal de la fila."),
]

# --- Trigo: superficie por DDR con calificador formal; total con concepto propio ---
_TRIGO_SHD = ["SHD139", "SHD140", "SHD141", "SHD142", "SHD143", "SHD144",
              "SHD147", "SHD148", "SHD149", "SHD193"]
for _var in _TRIGO_SHD:
    _ddr = _var[3:]
    REGLAS_SPEC.append(
        ("trigo", _var, "superficie-sembrada-trigo-ddr", "no_especificada", "Hectáreas",
         {"distrito_desarrollo_rural": _ddr},
         "Solo este diccionario, conjunto, definición y nombre.",
         "Denota superficie sembrada de trigo en el DDR del calificador.",
         "Otro SHD no aplica (DDR distinto, calificador distinto); SUMTOT no aplica (total, otra regla).",
         "DDR conservado por calificador formal; sin suma demostrada entre DDR.",
         "REQUISITO DE INTEGRACION: interpretacion()/construir() no propagan calificador a la variable "
         "documentada ni al grafo (verificado: 0 calificadores en resultados). Antes de aplicar, propagar "
         "el calificador y validar DDR distinto por regla; alternativa: 10 conceptos estrechos por DDR."))

REGLAS_SPEC += [
    ("trigo", "SUMTOT", "superficie-total-sembrada-trigo-registro", "no_especificada", "Hectáreas", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la superficie total sembrada por registro.",
     "Ningún SHD aplica (desagregados por DDR); el total no se demuestra suma de las SHD.",
     "Total por registro sin suma demostrada."),
    ("trigo", "CVEV", "variedad-trigo-sembrada-clave", "codigo", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota la clave de la variedad del trigo.",
     "VARIEDAD no aplica a esta regla (es nombre, otra regla).",
     "Sin unidad declarada; clave sin catálogo resuelto."),
    ("trigo", "VARIEDAD", "variedad-trigo-sembrada", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el nombre de la variedad sembrada.",
     "TVAR no aplica (tipo, otra regla).",
     "Sin unidad declarada; un nombre no es identidad global."),
    ("trigo", "TVAR", "variedad-trigo-sembrada-tipo", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre.",
     "Denota el tipo de variedad de trigo.",
     "GRUPO no tiene propuesta (descripción genérica sin leyenda).",
     "Sin unidad declarada; catálogo de tipos no publicado."),
    ("trigo", "FUENTE", "organizacion", "nombre", "", None,
     "Solo este diccionario, conjunto, definición y nombre. Reutiliza el concepto existente organizacion.",
     "Denota la institución generadora del dato con papel generadora.",
     "No identifica a la organización publicadora del catálogo CKAN ni a una capturadora.",
     "Sin unidad declarada; papel generadora conservado por separado."),
]

NUEVOS_CONCEPTOS = {
    "ganado-registrado-censo": ("Ganado registrado en el censo",
        "Ganado registrado en el Censo Ganadero de Sonora. Agrupa conteos por categoría y totales "
        "por agrupación; la categoría o agrupación y su población se conservan por concepto.", None),
    "productores-ganaderos-censados": ("Productores ganaderos censados",
        "Número de productores ganaderos censados en el Censo Ganadero de Sonora. Población: productores, "
        "no cabezas. Unidad literal de la fila: Productores.", None),
    "ddr-registro": ("Distrito de Desarrollo Rural del registro",
        "Distrito de Desarrollo Rural al que pertenece el registro del Censo Ganadero de Sonora según la fuente. "
        "Sin unidad declarada en la fila. No resuelve un catálogo oficial de DDR.", "territorio"),
    "region-geografica-estado": ("Región geográfica del estado declarada",
        "Región geográfica del estado declarada para el registro del Censo Ganadero de Sonora. "
        "Sin unidad declarada. No vincula a municipio concreto ni prueba exclusividad territorial.", "territorio"),
    "cuenca-referencia-registro": ("Cuenca hidrológica de referencia del registro",
        "Cuenca hidrológica de referencia del registro del Censo Ganadero de Sonora. Sin unidad declarada. "
        "El alcance 'de referencia' se limita al registro; no prueba correspondencia geoespacial.", "territorio"),
    "ddr-registro-cultivo": ("Distrito de Desarrollo Rural donde se registra el cultivo",
        "Clave del DDR donde se registra el cultivo en Agricultura Sonora. Sin catálogo resuelto.", "territorio"),
    "descripcion-ddr-registro-cultivo": ("Descripción del DDR donde se registra el cultivo según la fuente",
        "Descripción del Distrito de Desarrollo Rural del cultivo en Agricultura Sonora, según la fuente. "
        "La fila declara tipo Numérico con ejemplo vacío: conflicto registrado sin deducir formato. "
        "Sin unidad declarada; sin catálogo resuelto.", "territorio"),
    "municipio-registro-cultivo": ("Municipio donde se registra el cultivo",
        "Clave del municipio en que se registra el cultivo en Agricultura Sonora. No resuelve CVEGEO "
        "ni identidad municipal entre fuentes.", "municipio-registro"),
    "municipio-registro-cultivo-nombre": ("Nombre del municipio donde se registra el cultivo",
        "Nombre del municipio en que se registra el cultivo en Agricultura Sonora. Sin unidad declarada; "
        "no resuelve identidad municipal entre fuentes.", "municipio-registro"),
    "mes-registro-cultivo": ("Mes en que se registra el cultivo",
        "Clave del mes en que se registra el cultivo en Agricultura Sonora. Requiere año como contexto.",
        "mes-registro"),
    "mes-registro-cultivo-nombre": ("Nombre del mes en que se registra el cultivo",
        "Nombre del mes en que se registra el cultivo en Agricultura Sonora. Sin unidad declarada; "
        "requiere año como contexto.", "mes-registro"),
    "cultivo-registrado": ("Cultivo registrado",
        "Nombre del cultivo registrado en Agricultura Sonora. Sin unidad declarada. Un nombre no es "
        "identidad global entre fuentes.", None),
    "cultivo-registrado-clave": ("Clave del cultivo registrado",
        "Clave identificadora del cultivo en Agricultura Sonora. Sin unidad declarada; sin catálogo resuelto.",
        None),
    "variedad-cultivo": ("Variedad del cultivo",
        "Nombre de la variedad del cultivo en Agricultura Sonora. Sin unidad declarada; sin catálogo resuelto.",
        None),
    "variedad-cultivo-clave": ("Clave de la variedad del cultivo",
        "Clave identificadora de la variedad del cultivo en Agricultura Sonora. Sin unidad declarada; "
        "sin catálogo resuelto.", None),
    "estado-cierre-avance-cultivo": ("Dato de cierre o avance de producción del cultivo",
        "Indica si el registro del cultivo es dato de cierre o de avance de producción. La unidad literal "
        "de la fila usa AAAA como marcador sin año concreto. Avance y cierre no son comparables.", None),
    "superficie-cultivo": ("Superficie del cultivo",
        "Superficie del cultivo en Agricultura Sonora. El estado (sembrada, cosechada, siniestrada) "
        "se conserva por concepto; la unidad literal es Hectáreas.", None),
    "superficie-sembrada-cultivo": ("Superficie sembrada del cultivo",
        "Superficie sembrada del cultivo en Agricultura Sonora. Unidad literal de la fila: Hectáreas. "
        "No se infiere balance con cosechadas ni siniestradas.", "superficie-cultivo"),
    "superficie-cosechada-cultivo": ("Superficie cosechada del cultivo",
        "Superficie cosechada del cultivo en Agricultura Sonora. Unidad literal de la fila: Hectáreas. "
        "No se infiere balance con sembradas ni siniestradas.", "superficie-cultivo"),
    "superficie-siniestrada-cultivo": ("Superficie siniestrada del cultivo",
        "Superficie siniestrada del cultivo en Agricultura Sonora. Unidad literal de la fila: Hectáreas. "
        "No se infiere balance con sembradas ni cosechadas.", "superficie-cultivo"),
    "produccion-cultivo-toneladas": ("Producción total del cultivo en toneladas",
        "Producción total obtenida del cultivo en Agricultura Sonora. Unidad literal de la fila: Toneladas.",
        None),
    "rendimiento-cultivo": ("Rendimiento del cultivo por hectárea sembrada",
        "Rendimiento del cultivo: producción obtenida por hectárea sembrada. Unidad literal de la fila: "
        "Toneladas/hectáreas. No verifica el cálculo.", None),
    "precio-medio-rural-cultivo": ("Precio Medio Rural del cultivo",
        "Precio medio del cultivo (PMR) como cociente entre valor de producción total y producción en "
        "toneladas, según definición. Unidad literal de la fila: Pesos por tonelada. No verifica el cálculo.",
        None),
    "valor-produccion-cultivo": ("Valor total producido por cultivo",
        "Valor Total Producido por cultivo en Agricultura Sonora. Unidad literal de la fila: "
        "Miles de pesos MXN.", None),
    "ddr-registro-pesquero": ("Distrito de Desarrollo Rural donde se registra la producción pesquera",
        "Clave del DDR donde se registra la producción en Pesca y Acuacultura. Sin catálogo resuelto.",
        "territorio"),
    "descripcion-ddr-registro-pesquero": ("Descripción del DDR donde se registra la producción pesquera según la fuente",
        "Descripción del Distrito de Desarrollo Rural de la producción en Pesca y Acuacultura, según la fuente. "
        "Tipo Texto con ejemplo vacío: no hay evidencia de nombre puro. "
        "Sin unidad declarada; sin catálogo resuelto.", "territorio"),
    "municipio-registro-pesquero": ("Municipio donde se registra la producción pesquera",
        "Clave del municipio donde se registra la producción en Pesca y Acuacultura. No resuelve CVEGEO.",
        "municipio-registro"),
    "oficina-pesquera-registro": ("Oficina pesquera donde se registra la producción",
        "Clave de la oficina pesquera donde se registra la producción. No identifica organización "
        "publicadora ni capturadora.", "organizacion"),
    "oficina-pesquera-registro-nombre": ("Nombre de la oficina pesquera donde se registra la producción",
        "Nombre de la oficina pesquera donde se registra la producción. Sin unidad declarada; no identifica "
        "organización publicadora ni capturadora.", "organizacion"),
    "especie-producida-pesca": ("Especie producida en pesca y acuacultura",
        "Nombre de la especie producida. Sin unidad declarada; sin catálogo resuelto.", None),
    "especie-producida-pesca-clave": ("Clave de la especie producida en pesca y acuacultura",
        "Clave numérica de la especie producida. Sin unidad declarada; sin catálogo resuelto.", None),
    "origen-produccion-pesquera": ("Origen de la producción pesquera",
        "Nombre del origen de la producción con las etiquetas literales de la fila. El diccionario no publica "
        "mapeo código-etiqueta: prohibido mapear por orden.", None),
    "origen-produccion-pesquera-clave": ("Clave del origen de la producción pesquera",
        "Clave numérica del origen de la producción con los valores literales de la fila. Sin mapeo publicado "
        "a etiquetas.", None),
    "peso-desembarcado-pesca": ("Peso desembarcado del producto pesquero",
        "Peso que al desembarque conserva el producto en sus modalidades literales. Unidad literal de la fila: "
        "Toneladas. Modalidades sin homologar.", None),
    "peso-vivo-pesca": ("Peso vivo del producto pesquero en captura",
        "Peso total del producto en el momento de su captura, estimado por factores de conversión aplicados "
        "al peso desembarcado (metodología FAO y factores del Instituto Nacional de la Pesca citados sin "
        "verificar). Unidad literal de la fila: Toneladas. No convertir ni equiparar al peso desembarcado.",
        None),
    "valor-produccion-pesquera": ("Valor total de la producción pesquera",
        "Valor total producido en Pesca y Acuacultura. Unidad literal de la fila: Pesos MXN.", None),
    "variedad-trigo-sembrada": ("Variedad de trigo sembrada",
        "Nombre de la variedad de trigo sembrada. Sin unidad declarada. Un nombre no es identidad global.", None),
    "variedad-trigo-sembrada-clave": ("Clave de la variedad de trigo sembrada",
        "Clave de la variedad del trigo. Sin unidad declarada; sin catálogo resuelto.", None),
    "variedad-trigo-sembrada-tipo": ("Tipo de variedad de trigo sembrada",
        "Tipo de variedad de trigo. Sin unidad declarada; catálogo de tipos no publicado.", None),
    "superficie-sembrada-trigo-ddr": ("Superficie sembrada de trigo por DDR",
        "Superficie sembrada de trigo por Distrito de Desarrollo Rural. Unidad literal de la fila: Hectáreas. "
        "El DDR se conserva por calificador formal de la regla, no por el concepto. Sin suma demostrada entre DDR.", None),
    "superficie-total-sembrada-trigo-registro": ("Superficie total sembrada de trigo por registro",
        "Superficie total sembrada por registro. Unidad literal de la fila: Hectáreas. "
        "No se demuestra suma de los desagregados por DDR.", None),
}

_CENSO_CAT_LABELS = {
    "vacas": ("Conteo de vacas registradas en el censo",
              "Número de vacas registradas en el Censo Ganadero de Sonora. Categoría: vacas. "
              "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
              "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "toros": ("Conteo de toros registrados en el censo",
              "Número de toros registrados en el Censo Ganadero de Sonora. Categoría: toros. "
              "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
              "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "vaquillas": ("Conteo de vaquillas registradas en el censo",
                  "Número de vaquillas registradas en el Censo Ganadero de Sonora. Categoría: vaquillas. "
                  "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                  "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "novillos": ("Conteo de novillos registrados en el censo",
                 "Número de novillos registrados en el Censo Ganadero de Sonora. Categoría: novillos. "
                 "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                 "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "becerras": ("Conteo de becerras registradas en el censo",
                 "Número de becerras registradas en el Censo Ganadero de Sonora. Categoría: becerras. "
                 "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                 "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "becerros": ("Conteo de becerros registrados en el censo",
                 "Número de becerros registrados en el Censo Ganadero de Sonora. Categoría: becerros. "
                 "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                 "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "porcinos": ("Conteo de porcinos registrados en el censo",
                 "Número de porcinos registrados en el Censo Ganadero de Sonora. Categoría: porcinos. "
                 "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                 "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "equinos": ("Conteo de equinos registrados en el censo",
                "Número de equinos registrados en el Censo Ganadero de Sonora. Categoría: equinos. "
                "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "caprinos": ("Conteo de caprinos registrados en el censo",
                 "Número de caprinos registrados en el Censo Ganadero de Sonora. Categoría: caprinos. "
                 "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                 "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "mulares": ("Conteo de mulares registrados en el censo",
                "Número de animales mulares registrados en el Censo Ganadero de Sonora. Categoría: mulares. "
                "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
                "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "asnos": ("Conteo de asnos registrados en el censo",
              "Número de asnos registrados en el Censo Ganadero de Sonora. Categoría: asnos. "
              "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
              "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "ovinos": ("Conteo de ovinos registrados en el censo",
               "Número de ovinos registrados en el Censo Ganadero de Sonora. Categoría: ovinos. "
               "Población: cabezas de ganado de la categoría. Unidad literal de la fila: Cabezas. "
               "No demuestra exhaustividad de categorías ni igualdad con totales."),
    "bovino": ("Total de ganado bovino registrado en el censo",
               "Total de ganado bovino registrado en el Censo Ganadero de Sonora. Población explícita: "
               "ganado bovino. Unidad literal de la fila: Cabezas. "
               "No demuestra igualdad con la suma de categorías."),
    "menor": ("Total de ganado menor registrado en el censo",
              "Total de ganado menor registrado en el Censo Ganadero de Sonora. Población explícita: "
              "ganado menor. Unidad literal de la fila: Cabezas. "
              "No demuestra igualdad con la suma de categorías."),
}
for _var, _con, _cat in _CENSO_CATS:
    _label, _def = _CENSO_CAT_LABELS[_cat]
    NUEVOS_CONCEPTOS[_con] = (_label, _def, "ganado-registrado-censo")
NUEVOS_CONCEPTOS["total-ganado-bovino-censo"] = (
    *_CENSO_CAT_LABELS["bovino"], "ganado-registrado-censo")
NUEVOS_CONCEPTOS["total-ganado-menor-censo"] = (
    *_CENSO_CAT_LABELS["menor"], "ganado-registrado-censo")

# Variables fuera del nucleo leidas que quedan SIN propuesta y por que
NO_PROPUESTA = {
    ("863b9cc8-daeb-4430-b835-6a0ced5abd31", "CVOTRAS"): "Descripcion generica sin referente: no defendible.",
    ("863b9cc8-daeb-4430-b835-6a0ced5abd31", "DOTRAS"): "Descripcion generica sin referente: no defendible.",
    ("a7591bc9-f905-45cb-ba6c-ae3588d87594", "GRUPO"): "Descripcion generica sin leyenda publicada: no defendible.",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fila_inspeccion(imap, dic, variable):
    rows = [r for r in imap[dic]["definiciones"]
            if valor(r, K_NOMBRE) == variable]
    assert len(rows) == 1, (dic, variable, len(rows))
    return rows[0]


def main():
    pend = json.loads(PEND.read_text(encoding="utf-8"))
    cob = json.loads(COB.read_text(encoding="utf-8"))
    sem = json.loads(SEM.read_text(encoding="utf-8"))
    inv = json.loads(INV.read_text(encoding="utf-8"))
    insp = json.loads(INSP.read_text(encoding="utf-8"))
    base = None
    for v in cob["variables"]:
        if v["definicion_iri"].startswith("http"):
            base = v["definicion_iri"].split("/definition/")[0] + "/"
            break

    ahora = datetime.now(timezone.utc).isoformat()
    huellas = {k: sha(p) for k, p in
               {"pendientes": PEND, "cobertura": COB, "semantica": SEM,
                "inventario": INV, "inspeccion": INSP}.items()}

    resumen = pend["resumen"]["estados_columnas"]
    assert resumen["definicion_sin_interpretacion_compartida"] == 3720, resumen
    assert resumen["sin_definicion_coincidente"] == 833, resumen
    assert resumen["sin_diccionario_en_conjunto"] == 13, resumen
    assert resumen["documental_revisada"] == 836, resumen
    assert resumen["candidata_por_nombre"] == 118, resumen
    assert resumen["ambigua_por_nombre"] == 3, resumen
    fuera = [v for v in pend["variables_pendientes"] if v["estado"] == "fuera_del_nucleo_actual"]
    cand4 = [v for v in pend["variables_pendientes"] if v["estado"] == "candidata_sin_definicion_suficiente"]
    assert len(fuera) == 1308, len(fuera)
    assert len(cand4) == 23, len(cand4)

    vmap = {(v["diccionario"], v["variable"]): v for v in cob["variables"]}
    imap = {r["id"]: r for r in insp["recursos"]}

    fam_dic = {}
    for v in fuera:
        if v["diccionario"] in FAMS:
            fam_dic.setdefault(FAMS[v["diccionario"]], []).append(v)
    assert sum(len(x) for x in fam_dic.values()) == 66, {k: len(x) for k, x in fam_dic.items()}

    existentes = set(sem["conceptos"])
    for c in NUEVOS_CONCEPTOS:
        assert c not in existentes, c
        broader = NUEVOS_CONCEPTOS[c][2]
        assert broader is None or broader in existentes or broader in NUEVOS_CONCEPTOS, c
    ids_regla = {r["id"] for r in sem["reglas_descripcion_exacta"]}
    usados = set()
    por_concepto = collections.Counter()
    reglas = []
    cubiertas = set()
    for fam, var, concepto, representacion, unidad_esp, calif, alcance, positivo, contraejemplo, limite, *extra in REGLAS_SPEC:
        req = extra[0] if extra else None
        assert concepto in existentes or concepto in NUEVOS_CONCEPTOS, concepto
        dics = {v["diccionario"] for v in fam_dic[fam] if v["variable"] == var}
        assert len(dics) == 1, (fam, var)
        dic = next(iter(dics))
        assert (dic, var) not in NO_PROPUESTA, (dic, var)
        v = vmap[(dic, var)]
        assert v["estado"] == "fuera_del_nucleo_actual", (dic, var, v["estado"])
        # Evidencia exacta desde las fuentes; la unidad se verifica fila por fila.
        fila = fila_inspeccion(imap, dic, var)
        unidad = valor_crudo(fila, K_UNIDAD)
        if unidad_esp is not None:
            assert unidad == unidad_esp, (dic, var, repr(unidad), repr(unidad_esp))
        por_concepto[concepto] += 1
        rid = "r3a3-%s-%d" % (concepto, por_concepto[concepto])
        assert rid not in ids_regla and rid not in usados, rid
        usados.add(rid)
        regla = {
            "id": rid, "concepto": concepto, "representacion": representacion,
            "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
            "conjuntos": [v["conjunto"]], "diccionarios": [dic],
            "definiciones": [v["definicion_iri"]],
            "criterio": "Revision agente 3 ronda 3; lectura completa del diccionario; alcance fijado a definiciones concretas.",
            "fuente_revision": "propuestas/ronda-3/agente-3-cobertura/propuestas.json",
            "alcance": alcance, "positivo": positivo,
            "contraejemplo": contraejemplo, "limite": limite,
            "evidencia": [{
                "variable": v["variable"], "descripcion": v["descripcion"],
                "definicion_iri": v["definicion_iri"], "diccionario": dic,
                "conjunto": v["conjunto"],
                "unidad_de_medida": unidad, "tipo_de_dato": valor_crudo(fila, K_TIPO),
                "ejemplo_de_dato": valor_crudo(fila, K_EJEMPLO),
                "catalogo_de_referencia": valor(fila, {"catalogo de referencia", "catalago de referencia"}),
            }],
        }
        if calif is not None:
            regla["calificador"] = calif
        if req is not None:
            regla["requisito_integracion"] = req
        reglas.append(regla)
        cubiertas.add((dic, var))
    assert cubiertas | set(NO_PROPUESTA) == {(v["diccionario"], v["variable"]) for vs in fam_dic.values() for v in vs}, "cobertura incompleta de lectura"

    conceptos = {k: [label, definicion, broader] for k, (label, definicion, broader) in NUEVOS_CONCEPTOS.items()}
    no_prop = []
    for (dic, var), motivo in sorted(NO_PROPUESTA.items()):
        v = vmap[(dic, var)]
        no_prop.append({"diccionario": dic, "variable": var, "descripcion": v["descripcion"],
                        "definicion_iri": v["definicion_iri"], "conjunto": v["conjunto"], "motivo": motivo})
    familias = []
    for dic, fam in FAMS.items():
        vs = fam_dic[fam]
        familias.append({"familia": fam, "diccionario": dic, "conjunto": vs[0]["conjunto"],
                         "titulo_conjunto": vs[0]["titulo_conjunto"],
                         "variables_leidas": len(vs),
                         "reglas": sum(1 for r in reglas if r["diccionarios"] == [dic]),
                         "documentacion": "Lectura completa fila por fila (literal, tipo, unidad, "
                                          "catalogo, nulos, ejemplo). El resto del inventario no esta leido."})
    # Positivo real por el mismo validador que usan los negativos.
    filas_val = {}
    for rid_, rec in imap.items():
        for row in rec.get("definiciones", []):
            filas_val[(rid_, valor(row, K_NOMBRE))] = {
                "descripcion": valor_crudo(row, K_DESC),
                "unidad": valor_crudo(row, K_UNIDAD), "tipo": valor_crudo(row, K_TIPO),
                "ejemplo": valor_crudo(row, K_EJEMPLO)}
    fuentes_val = {
        "variables_por_iri": {v["definicion_iri"]: v for v in cob["variables"]},
        "ids_reglas": {r["id"] for r in sem["reglas_descripcion_exacta"]},
        "conceptos": set(sem["conceptos"]),
        "representaciones": {r.get("representacion") for r in sem["reglas_descripcion_exacta"]},
        "filas": filas_val,
    }
    inv_fam = {v: k for k, v in FAMS.items()}
    esperadas_val = {(inv_fam[fam], var) for (fam, var, *_r) in REGLAS_SPEC}
    asignacion_val = {"frontera": {v["definicion_iri"] for v in cand4},
                      "cubiertas_esperadas": esperadas_val}
    propuestas = {
        "generado_en_utc": ahora, "agente": "ronda-3/agente-3-cobertura",
        "base_iri": base, "huellas_entrada": huellas,
        "familias_revisadas": familias,
        "conceptos_nuevos": conceptos, "conceptos_reutilizados": ["organizacion"],
        "reglas": reglas, "sin_propuesta_tras_lectura": no_prop,
        "requisitos_integracion": {
            "calificador_shd": "Las 10 reglas SHD comparten concepto con calificador formal por DDR. "
                               "interpretacion()/construir() no propagan calificador a la variable documentada "
                               "ni al grafo (verificado en esta base: 0 calificadores en resultados). "
                               "Requisito antes de aplicar: propagar el calificador y validar DDR distinto "
                               "por regla. Alternativa: 10 conceptos estrechos por DDR. El pipeline NO "
                               "preserva hoy el calificador; no se declara lo contrario.",
            "aritmetica_simulada": {"respaldadas": 295, "fuera_del_nucleo": 1245,
                                    "candidatas_agente4": 23, "conceptos": 158,
                                    "revisadas_intactas": 836,
                                    "candidatas_columna": 827,
                                    "candidatas_nuevas_no_revisadas": 709},
            "advertencia_candidatas": "Las 709 columnas que matchean las 63 definiciones pasarían a "
                                      "candidata_por_nombre al integrar (cómputo propio verificado: 709 "
                                      "columnas físicas, todas definicion_sin_interpretacion_compartida, "
                                      "nombre único y definición única). Candidata no es revisada: requieren "
                                      "revisión documental del agente 2; esta propuesta no crea "
                                      "correspondencias.",
        },
        "nota": "Propuestas de significado separadas del inventario. Ninguna crea correspondencia "
                "columna-variable ni uso automatico en cruces. Los 23 significados candidatos del "
                "agente 4 no se tocan.",
    }
    (AQUI / "propuestas.json").write_text(json.dumps(propuestas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errores_pos = validar_propuestas(propuestas, fuentes_val, asignacion_val)
    assert errores_pos == [], errores_pos[:3]

    # --- inventario total (sin cambios de estructura) ---
    idef = {v["definicion_iri"]: v for v in cob["variables"]}
    g3720 = collections.defaultdict(lambda: {"iris": set(), "campos": set(), "diccionarios": set(), "definiciones": set()})
    for c in pend["columnas"]:
        if c["estado"] != "definicion_sin_interpretacion_compartida":
            continue
        g = g3720[(c["conjunto"], next(
            (v["titulo_conjunto"] for iri in c["definiciones_por_nombre"]
             if (v := idef.get(iri)) is not None), c["titulo_recurso"]))]
        g["iris"].add(c["columna"])
        g["campos"].add(c["campo"])
        for iri in c["definiciones_por_nombre"]:
            v = idef.get(iri)
            if v is None:
                continue
            g["diccionarios"].add(v["diccionario"])
            g["definiciones"].add(iri)
    todas3720 = [i for g in g3720.values() for i in g["iris"]]
    assert len(todas3720) == 3720 and len(set(todas3720)) == 3720, "particion exacta 3720"
    g3720_out = [{"conjunto": k[0], "titulo_conjunto": k[1], "columnas": len(g["iris"]),
                  "columna_iris": sorted(g["iris"]),
                  "campos_distintos": len(g["campos"]), "diccionarios": sorted(g["diccionarios"]),
                  "definiciones_distintas": len(g["definiciones"])}
                 for k, g in sorted(g3720.items(), key=lambda x: -len(x[1]["iris"]))]

    g833 = collections.defaultdict(lambda: {"iris": set(), "campos": set(), "recursos": set()})
    for c in pend["columnas"]:
        if c["estado"] != "sin_definicion_coincidente":
            continue
        g = g833[(c["conjunto"], c["titulo_recurso"])]
        g["iris"].add(c["columna"])
        g["campos"].add(c["campo"])
        g["recursos"].add(c["recurso"])
    todas833 = [i for g in g833.values() for i in g["iris"]]
    assert len(todas833) == 833 and len(set(todas833)) == 833, "particion exacta 833"
    g833_out = [{"conjunto": k[0], "titulo_recurso": k[1], "columnas": len(g["iris"]),
                 "columna_iris": sorted(g["iris"]),
                 "campos": sorted(g["campos"]), "recursos": sorted(g["recursos"])}
                for k, g in sorted(g833.items(), key=lambda x: -len(x[1]["iris"]))]

    sin13 = [c for c in pend["columnas"] if c["estado"] == "sin_diccionario_en_conjunto"]
    assert len(sin13) == 13
    conj13 = sin13[0]["conjunto"]
    dics_en_conj = sorted({r["id"] for r in inv["recursos"]
                           if r["conjunto_id"] == conj13 and r["clasificacion"] == "diccionario"})

    gfuera = collections.defaultdict(list)
    for v in fuera:
        gfuera[(v["conjunto"], v["titulo_conjunto"])].append(v)
    gruops = []
    todas1308 = []
    for (conj, tit), vs in sorted(gfuera.items(), key=lambda x: -len(x[1])):
        dics = sorted({v["diccionario"] for v in vs})
        leido = conj in {v["conjunto"] for vs2 in fam_dic.values() for v in vs2}
        descs = collections.Counter(v["descripcion"] for v in vs)
        iris = sorted({v["definicion_iri"] for v in vs})
        todas1308.extend(iris)
        gruops.append({
            "conjunto": conj, "titulo_conjunto": tit, "variables": len(vs),
            "definicion_iris": iris,
            "diccionarios": dics, "lectura": "completa" if leido else "pendiente",
            "motivos": dict(collections.Counter(v["motivo"] for v in vs)),
            "descripciones_distintas": len(descs),
            "top_descripciones": [{"descripcion": d, "n": n} for d, n in descs.most_common(8)],
        })
    assert len(todas1308) == 1308 and len(set(todas1308)) == 1308, "particion exacta 1308"
    assert sum(g["variables"] for g in gruops) == 1308

    vacias = collections.Counter(v["descripcion"] for v in fuera
                                 if v["motivo"] == "descripcion_vacia_o_pendiente").most_common(10)

    prio = []
    for g in gruops:
        if g["lectura"] == "completa":
            continue
        col = next((x["columnas"] for x in g3720_out if x["conjunto"] == g["conjunto"]), 0)
        prio.append({"conjunto": g["conjunto"], "titulo_conjunto": g["titulo_conjunto"],
                     "columnas_3720": col, "variables_fuera": g["variables"],
                     "puntaje": col + 5 * g["variables"]})
    prio.sort(key=lambda x: -x["puntaje"])

    inventario = {
        "generado_en_utc": ahora, "agente": "ronda-3/agente-3-cobertura",
        "base_iri": base, "huellas_entrada": huellas,
        "conteos_verificados": {"columnas": dict(pend["resumen"]["estados_columnas"]),
                                "variables_fuera_del_nucleo": 1308,
                                "candidatos_agente4_intactos": 23,
                                "motivos_fuera": dict(collections.Counter(v["motivo"] for v in fuera))},
        "columnas_3720_por_conjunto": g3720_out,
        "columnas_833_por_conjunto": g833_out,
        "columnas_13_sin_diccionario": {
            "columnas": [{"columna": c["columna"], "recurso": c["recurso"],
                          "titulo_recurso": c["titulo_recurso"], "campo": c["campo"],
                          "fuente_esquema": c["fuente_esquema"]} for c in sin13],
            "conjunto": conj13,
            "diccionarios_en_conjunto": dics_en_conj,
            "decision": "Clasificadas. Sin vinculo propuesto: sin diccionario no hay definicion "
                        "documental y no se usa el nombre como evidencia.",
        },
        "fuera_1308_por_conjunto": gruops,
        "vacias_genericas_top": [{"descripcion": d, "n": n} for d, n in vacias],
        "prioridades_pendientes": prio[:15],
        "aritmetica_post_integracion": {"fuera_del_nucleo": 1245, "calculo": "1308 - 63",
                                        "sin_lectura": 1242, "calculo_sin_lectura": "1308 - 66",
                                        "leidas_sin_propuesta": 3,
                                        "nota": "1245 pendientes tras integrar ≠ 1242 sin leer: 3 fueron leídas "
                                                "y quedaron clasificadas sin propuesta (CVOTRAS, DOTRAS, GRUPO)."},
        "limite_revision": "Lectura completa: 4 diccionarios (censo, agricultura, pesca, trigo), 66 variables. "
                           "El resto del inventario esta agrupado pero NO leido fila por fila; sus prioridades "
                           "son conteo y especificidad literal, sin simular revision.",
    }
    (AQUI / "inventario-cobertura.json").write_text(json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fuentes = {
        "generado_en_utc": ahora,
        "insumos": [{"ruta": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": huellas[k]}
                    for k, p in [("pendientes", PEND), ("cobertura", COB), ("semantica", SEM),
                                 ("inventario", INV), ("inspeccion", INSP)]],
        "base_iri": base,
        "descargas": "Ninguna. No se descargo fuente externa alguna; no se propone ningun vinculo "
                     "para columnas sin definicion/diccionario. Clasificacion local con fuentes fijadas.",
        "nota_codificacion": "Los literales de evidencia se copian byte-exactos desde las fuentes "
                             "(incluyen U+FFFD de origen). La prosa analitica (alcance, positivo, "
                             "contraejemplo, limite, definiciones de conceptos nuevos) es redaccion propia "
                             "y nunca transcribe literales: solo cita identificadores e IRIs exactos. "
                             "Ninguna normalizacion aplicada a entregas; sin conversion n->n.",
    }
    (AQUI / "fuente" / "huellas.json").parent.mkdir(exist_ok=True)
    (AQUI / "fuente" / "huellas.json").write_text(json.dumps(fuentes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reglas": len(reglas), "conceptos_nuevos": len(conceptos),
                      "grupos_3720": len(g3720_out), "grupos_833": len(g833_out),
                      "grupos_fuera": len(gruops)}, indent=1))


if __name__ == "__main__":
    main()
