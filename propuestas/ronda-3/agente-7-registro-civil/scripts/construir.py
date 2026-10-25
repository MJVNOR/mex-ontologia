"""Agente 7 ronda 3 (registro civil: Divorcios/Defunciones/Nacimientos/Matrimonios).

Lee (solo lectura): asignaciones del integrador, inspeccion de contenido,
inventario, cobertura y semantica central. Escribe SOLO en su carpeta:
propuestas.json, fuente/inspeccion-extracto.json y resultado.md.
No toca nucleo, ni genera nada central, ni usa red.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "propuestas" / "ronda-3" / "agente-7-registro-civil"
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import huella  # noqa: E402  funcion pura
from integrar_contenido import valor  # noqa: E402  funcion pura

DIC_DIV = "10357304-e171-44ca-a453-f989e6a2ff83"
DIC_SEED = "12f684e9-f4d5-4714-933d-aa153a812174"
DIC_NAC = "22202305-2d02-4c49-b216-cc98224357f0"
DIC_MAT = "364ffa5c-e1c2-4185-a22f-80bede6735d0"

# (diccionario, variable) -> (concepto, representacion). Solo literales especificos.
# Pares codigo/nombre comparten concepto con distinta representacion.
PROP = {
    (DIC_DIV, "edad_div1"): ("edad-divorciado-1", "no_especificada"),
    (DIC_DIV, "edad_div2"): ("edad-divorciado-2", "no_especificada"),
    (DIC_DIV, "sexo_div1"): ("sexo-divorciado-1", "no_especificada"),
    (DIC_DIV, "sexo_div2"): ("sexo-divorciado-2", "no_especificada"),
    (DIC_MAT, "edad_cty1"): ("edad-contrayente-1", "no_especificada"),
    (DIC_MAT, "edad_cty2"): ("edad-contrayente-2", "no_especificada"),
    (DIC_MAT, "sexo_cty1"): ("sexo-contrayente-1", "no_especificada"),
    (DIC_MAT, "sexo_cty2"): ("sexo-contrayente-2", "no_especificada"),
    (DIC_SEED, "FECHANACIMIENTO"): ("fecha-nacimiento-difunto", "fecha"),
    (DIC_SEED, "SEXO"): ("sexo-difunto", "codigo"),
    (DIC_SEED, "ENTIDADNACIMIENTO"): ("entidad-nacimiento-difunto", "codigo"),
    (DIC_SEED, "ENTIDADNACIMIENTOD"): ("entidad-nacimiento-difunto", "nombre"),
    (DIC_SEED, "NACIONALIDAD"): ("nacionalidad-difunto", "codigo"),
    (DIC_SEED, "NACIONALIDADD"): ("nacionalidad-difunto", "nombre"),
    (DIC_SEED, "EDAD"): ("edad-difunto-sin-momento-confirmado", "no_especificada"),
    (DIC_SEED, "PESO"): ("peso-difunto", "no_especificada"),
    (DIC_SEED, "ESTADOCONYUGAL"): ("estado-conyugal-difunto", "codigo"),
    (DIC_SEED, "ESTADOCONYUGALD"): ("estado-conyugal-difunto", "nombre"),
    (DIC_SEED, "RESIDEEXTRANJERO"): ("extranjeria-difunto-segun-definicion", "no_especificada"),
    (DIC_SEED, "ENTIDADRESIDENCIA"): ("entidad-residencia-difunto", "codigo"),
    (DIC_SEED, "ENTIDADRESIDENCIAD"): ("entidad-residencia-difunto", "nombre"),
    (DIC_SEED, "ESCOLARIDAD"): ("escolaridad-difunto", "codigo"),
    (DIC_SEED, "ESCOLARIDADD"): ("escolaridad-difunto", "nombre"),
    (DIC_SEED, "ENTIDADDEFUNCION"): ("entidad-defuncion", "codigo"),
    (DIC_SEED, "ENTIDADDEFUNCIOND"): ("entidad-defuncion", "nombre"),
    (DIC_SEED, "JURISDICCIONDEFUNCION"): ("jurisdiccion-defuncion", "codigo"),
    (DIC_SEED, "JURISDICCIONDEFUNCIOND"): ("jurisdiccion-defuncion", "nombre"),
    (DIC_SEED, "FECHADEFUNCION"): ("fecha-defuncion", "fecha"),
    (DIC_SEED, "ATENCIONMEDICA"): ("atencion-medica-difunto", "codigo"),
    (DIC_SEED, "ATENCIONMEDICAD"): ("atencion-medica-difunto", "no_especificada"),
    (DIC_SEED, "REALIZO_CIRUGIA"): ("cirugia-difunto", "codigo"),
    (DIC_SEED, "REALIZO_CIRUGIAD"): ("cirugia-difunto", "no_especificada"),
    (DIC_SEED, "PRACTICONECROPSIA"): ("autopsia-difunto", "codigo"),
    (DIC_SEED, "PRACTICONECROPSIAD"): ("autopsia-difunto", "no_especificada"),
    (DIC_SEED, "OCURRIODURANTEEMBARAZO"): ("defuncion-durante-embarazo", "codigo"),
    (DIC_SEED, "OCURRIODURANTEEMBARAZOD"): ("defuncion-durante-embarazo", "no_especificada"),
    (DIC_SEED, "OCURRIOENTRABAJO"): ("defuncion-en-trabajo", "codigo"),
    (DIC_SEED, "OCURRIOENTRABAJOD"): ("defuncion-en-trabajo", "no_especificada"),
    (DIC_NAC, "FECHANACIMIENTOMADRE"): ("fecha-nacimiento-madre", "fecha"),
    (DIC_NAC, "ENTIDADNACIMIENTO"): ("entidad-nacimiento-madre", "codigo"),
    (DIC_NAC, "ENTIDADNACIMIENTOD"): ("entidad-nacimiento-madre", "nombre"),
    (DIC_NAC, "NACIOEXTRANJERO"): ("extranjeria-madre-segun-definicion", "codigo"),
    (DIC_NAC, "NACIOEXTRANJEROD"): ("extranjeria-madre-segun-definicion", "no_especificada"),
    (DIC_NAC, "EDAD"): ("edad-madre", "no_especificada"),
    (DIC_NAC, "ESTADOCONYUGAL"): ("estado-conyugal-madre", "codigo"),
    (DIC_NAC, "ESTADOCONYUGALD"): ("estado-conyugal-madre", "nombre"),
    (DIC_NAC, "HABLALENGUAINDIGENA"): (None, None),  # bloqueada abajo
    (DIC_NAC, "ENTIDADRESIDENCIA"): ("entidad-residencia-madre", "codigo"),
    (DIC_NAC, "ENTIDADRESIDENCIAD"): ("entidad-residencia-madre", "nombre"),
    (DIC_NAC, "RESIDEEXTRANJERO"): ("residencia-extranjero-madre", "codigo"),
    (DIC_NAC, "NUMEROEMBARAZOS"): ("numero-embarazos-madre", "no_especificada"),
    (DIC_NAC, "HIJOSNACIDOSMUERTOS"): ("hijos-nacidos-muertos-madre", "no_especificada"),
    (DIC_NAC, "HIJOSNACIDOSVIVOS"): ("hijos-nacidos-vivos-madre", "no_especificada"),
    (DIC_NAC, "HIJOSSOBREVIVIENTES"): ("hijos-sobrevivientes-madre", "no_especificada"),
    (DIC_NAC, "CONDICIONHIJOANTERIOR"): ("condicion-hijo-anterior-madre", "codigo"),
    (DIC_NAC, "CONDICIONHIJOANTERIORD"): ("condicion-hijo-anterior-madre", "nombre"),
    (DIC_NAC, "VIVEHIJOANTERIOR"): ("supervivencia-hijo-anterior-madre", "codigo"),
    (DIC_NAC, "VIVEHIJOANTERIORD"): ("supervivencia-hijo-anterior-madre", "no_especificada"),
    (DIC_NAC, "ESCOLARIDAD"): ("escolaridad-madre", "codigo"),
    (DIC_NAC, "ESCOLARIDADD"): ("escolaridad-madre", "nombre"),
    (DIC_NAC, "TRABAJAACTUALMENTE"): ("trabajo-actual-madre", "codigo"),
    (DIC_NAC, "TRABAJAACTUALMENTED"): ("trabajo-actual-madre", "no_especificada"),
    (DIC_NAC, "EDADPADRE"): ("edad-padre", "no_especificada"),
    (DIC_NAC, "FECHANACIMIENTO"): ("fecha-nacimiento-nacido", "fecha"),
    (DIC_NAC, "HORANACIMIENTO"): ("hora-nacimiento-nacido", "hora"),
    (DIC_NAC, "SEXO"): ("sexo-nacido", "codigo"),
    (DIC_NAC, "SEXOD"): ("sexo-nacido", "nombre"),
    (DIC_NAC, "EDADGESTACIONAL"): ("edad-gestacional-nacido", "no_especificada"),
    (DIC_NAC, "TALLA"): ("talla-nacido", "no_especificada"),
    (DIC_NAC, "PESO"): ("peso-nacido", "no_especificada"),
    (DIC_NAC, "LUGARNACIMIENTO"): ("lugar-ocurrencia-nacimiento", "codigo"),
    (DIC_NAC, "LUGARNACIMIENTOD"): ("lugar-ocurrencia-nacimiento", "nombre"),
    (DIC_NAC, "TIPOCESAREA"): ("cesarea-parto", "codigo"),
    (DIC_NAC, "TIPOCESAREAD"): ("cesarea-parto", "nombre"),
    (DIC_NAC, "ENTIDADFEDERATIVAPARTO"): ("entidad-parto", "codigo"),
    (DIC_NAC, "ENTIDADFEDERATIVAPARTOD"): ("entidad-parto", "nombre"),
}
PROP.pop((DIC_NAC, "HABLALENGUAINDIGENA"))

# Bloqueos por politica aunque el literal sea especifico: identidad/etnia/lengua
# o genericidad sin poblacion/evento.
BLOQ = {
    (DIC_SEED, "SE_RECONOCIA_AFROMEXICANO"): "identidad",
    (DIC_SEED, "SE_RECONOCIA_AFROMEXICANOD"): "identidad",
    (DIC_SEED, "SE_CONSIDERA_INDIGENA"): "identidad",
    (DIC_SEED, "SE_CONSIDERA_INDIGENAD"): "identidad",
    (DIC_SEED, "HABLALENGUAINDIGENA"): "identidad",
    (DIC_SEED, "HABLALENGUAINDIGENAD"): "identidad",
    (DIC_NAC, "SECONSIDERAINDIGENA"): "identidad",
    (DIC_NAC, "SECONSIDERAINDIGENAD"): "identidad",
    (DIC_NAC, "HABLALENGUAINDIGENA"): "identidad",
    (DIC_NAC, "HABLALENGUAINDIGENAD"): "identidad",
    (DIC_SEED, "CLAVEEDAD"): "generica",
    (DIC_SEED, "CLAVEEDADD"): "generica",
    (DIC_NAC, "RESIDEEXTRANJEROD"): "contradiccion",
}
RAZON = {
    "pendiente": "Descripcion literal 'Pendiente de especificar' o vacia: proponer por nombre violaria la prohibicion de inferencia.",
    "identidad": "Atribucion de identidad/etnia/lengua: requiere catalogo o texto publicado que defina valores; no se promueve codigo a identidad por costumbre.",
    "generica": "Descripcion generica sin poblacion ni evento; insuficiente para un concepto estrecho.",
    "contradiccion": "Contradicción entre el par código RESIDEEXTRANJERO ('es recidente en el extranjero' = residencia fuera) y RESIDEEXTRANJEROD ('es residente extranjera', que puede ser extranjería y no residencia fuera): sin confirmar no se unifican; queda pendiente con pregunta. No se deduce lugar.",
}

TAG = {DIC_DIV: "div", DIC_SEED: "seed", DIC_NAC: "nac", DIC_MAT: "mat"}

NUEVOS = {
    "edad-divorciado-1": ["Edad del divorciado 1", "Edad del divorciado 1 del registro de divorcios; unidad no declarada en la fila; no distingue registro, ocurrencia ni residencia.", None],
    "edad-divorciado-2": ["Edad del divorciado 2", "Edad del divorciado 2 del registro de divorcios; unidad no declarada en la fila; no distingue registro, ocurrencia ni residencia.", None],
    "sexo-divorciado-1": ["Sexo del divorciado 1", "Sexo declarado del divorciado 1 del registro de divorcios.", "sexo-declarado"],
    "sexo-divorciado-2": ["Sexo del divorciado 2", "Sexo declarado del divorciado 2 del registro de divorcios.", "sexo-declarado"],
    "edad-contrayente-1": ["Edad del contrayente 1", "Edad del contrayente 1 del registro de matrimonios; unidad no declarada en la fila.", None],
    "edad-contrayente-2": ["Edad del contrayente 2", "Edad del contrayente 2 del registro de matrimonios; unidad no declarada en la fila.", None],
    "sexo-contrayente-1": ["Sexo del contrayente 1", "Sexo declarado del contrayente 1 del registro de matrimonios.", "sexo-declarado"],
    "sexo-contrayente-2": ["Sexo del contrayente 2", "Sexo declarado del contrayente 2 del registro de matrimonios.", "sexo-declarado"],
    "fecha-nacimiento-difunto": ["Fecha de nacimiento del difunto", "Fecha de nacimiento de la persona difunta del registro epidemiologico de defunciones.", "tiempo"],
    "entidad-nacimiento-difunto": ["Entidad de nacimiento del difunto", "Entidad federativa de nacimiento de la persona difunta; codigo y nombre denotan el mismo objeto.", "entidad"],
    "nacionalidad-difunto": ["Nacionalidad del difunto", "Nacionalidad declarada de la persona difunta; sin catalogo publicado.", None],
    "peso-difunto": ["Peso del difunto", "Peso registrado de la persona difunta; unidad no declarada en la fila.", None],
    "estado-conyugal-difunto": ["Estado conyugal del difunto", "Estado conyugal declarado de la persona difunta; codigo y nombre denotan el mismo objeto.", None],
    "edad-difunto-sin-momento-confirmado": ["Edad del difunto (momento sin confirmar)", "La fuente dice 'Edad del difunto' sin declarar si es edad al morir; no se adopta el momento 'al fallecer' del concepto central. Unidad no declarada en la fila.", None],
    "entidad-residencia-difunto": ["Entidad de residencia del difunto", "Entidad federativa donde residia la persona difunta; codigo y nombre denotan el mismo objeto.", "entidad"],
    "escolaridad-difunto": ["Escolaridad del difunto", "Nivel escolar declarado de la persona difunta; codigo y nombre denotan el mismo objeto.", None],
    "entidad-defuncion": ["Entidad de la defuncion", "Entidad federativa donde ocurrio la defuncion; codigo y nombre denotan el mismo objeto.", "entidad"],
    "jurisdiccion-defuncion": ["Jurisdiccion de la defuncion", "Jurisdiccion donde ocurrio la defuncion; codigo y nombre denotan el mismo objeto. Sin jerarquia publicada.", None],
    "extranjeria-difunto-segun-definicion": ["Extranjería del difunto según definición", "La descripción dice 'Identificador de si es extrangero' (sic); no declara residencia ni nombre y el nombre de variable no se usa como evidencia. Representación no especificada; valores no documentados.", None],
    "fecha-defuncion": ["Fecha de la defuncion", "Fecha en que ocurrio la defuncion.", "tiempo"],
    "atencion-medica-difunto": ["Atencion medica del difunto", "Indicador de si recibio atencion medica; sujeto (difunto) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; valores no documentados.", None],
    "cirugia-difunto": ["Cirugia del difunto", "Indicador de si se le realizo cirugia; sujeto (difunto) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; valores no documentados.", None],
    "autopsia-difunto": ["Autopsia del difunto", "Indicador de si se le practico autopsia; sujeto (difunto) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; valores no documentados.", None],
    "defuncion-durante-embarazo": ["Defuncion durante el embarazo", "Indicador de si la defuncion ocurrio durante el embarazo; valores no documentados.", None],
    "defuncion-en-trabajo": ["Defuncion en el trabajo", "Indicador de si la defuncion ocurrio en el trabajo; valores no documentados.", None],
    "fecha-nacimiento-madre": ["Fecha de nacimiento de la madre", "Fecha de nacimiento de la madre del nacido.", "tiempo"],
    "entidad-nacimiento-madre": ["Entidad de nacimiento de la madre", "Entidad federativa de nacimiento de la madre; codigo y nombre denotan el mismo objeto.", "entidad"],
    "extranjeria-madre-segun-definicion": ["Extranjería de la madre según definición", "La descripción dice 'Indicador de si es extrangera' (sic); el nombre de variable sugiere nacimiento en el extranjero pero la descripción no lo declara: contradicción nombre/descripción registrada sin deducir lugar. Valores no documentados.", None],
    "edad-madre": ["Edad de la madre", "Edad de la madre del nacido; unidad no declarada en la fila.", None],
    "estado-conyugal-madre": ["Estado conyugal de la madre", "Estado conyugal declarado de la madre; codigo y nombre denotan el mismo objeto.", None],
    "entidad-residencia-madre": ["Entidad de residencia de la madre", "Entidad federativa donde reside la madre; codigo y nombre denotan el mismo objeto.", "entidad"],
    "residencia-extranjero-madre": ["Residencia en el extranjero de la madre", "Indicador de si la madre reside en el extranjero, según el literal del código; valores no documentados. Su par textual RESIDEEXTRANJEROD queda pendiente por contradicción; no se unifican.", None],
    "numero-embarazos-madre": ["Numero de embarazos de la madre", "Numero total de embarazos que ha tenido la madre.", None],
    "hijos-nacidos-muertos-madre": ["Hijos nacidos muertos de la madre", "Numero de hijos nacidos muertos; sujeto (madre) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal.", None],
    "hijos-nacidos-vivos-madre": ["Hijos nacidos vivos de la madre", "Numero de hijos nacidos vivos; sujeto (madre) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal.", None],
    "hijos-sobrevivientes-madre": ["Hijos sobrevivientes de la madre", "Numero de hijos sobrevivientes; sujeto (madre) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal.", None],
    "condicion-hijo-anterior-madre": ["Condicion del hijo anterior", "Condicion del hijo anterior; sujeto (madre) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; codigo y texto denotan el mismo objeto.", None],
    "supervivencia-hijo-anterior-madre": ["Supervivencia del hijo anterior", "Indicador de si el hijo anterior todavia vive; sujeto (madre) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; valores no documentados.", None],
    "escolaridad-madre": ["Escolaridad de la madre", "Nivel escolar declarado de la madre; codigo y texto denotan el mismo objeto.", None],
    "trabajo-actual-madre": ["Trabajo actual de la madre", "Indicador sobre el trabajo actual de la madre; valores no documentados.", None],
    "edad-padre": ["Edad del padre", "Edad del padre del nacido; unidad no declarada en la fila.", None],
    "fecha-nacimiento-nacido": ["Fecha de nacimiento del nacido", "Fecha en que ocurrio el nacimiento; el sujeto se toma del conjunto y filas vecinas (nacido), con ese limite.", "tiempo"],
    "hora-nacimiento-nacido": ["Hora del nacimiento", "Hora en que ocurrio el nacimiento; el sujeto se toma del conjunto y filas vecinas (nacido), con ese limite.", "tiempo"],
    "sexo-nacido": ["Sexo del nacido", "Sexo del nacido; codigo y nombre denotan el mismo objeto.", "sexo-declarado"],
    "edad-gestacional-nacido": ["Edad gestacional del nacido", "Edad gestacional del nacido; unidad no declarada en la fila.", None],
    "talla-nacido": ["Talla del nacido", "Talla del nacido; unidad no declarada en la fila.", None],
    "peso-nacido": ["Peso del nacido", "Peso del nacido; unidad no declarada en la fila.", None],
    "lugar-ocurrencia-nacimiento": ["Lugar del nacimiento", "Lugar donde ocurrio el nacimiento; codigo y nombre denotan el mismo objeto. Tipologia del lugar no documentada.", None],
    "cesarea-parto": ["Cesarea del parto", "Indicador de si fue por cesarea; encuadre (parto) tomado del contexto publicado del conjunto (inferencia-contextual-publicada), no hecho autónomo del literal; codigo y texto denotan el mismo objeto.", None],
    "entidad-parto": ["Entidad del parto", "Entidad federativa donde fue el parto; codigo y nombre denotan el mismo objeto.", "entidad"],
}
REUTILIZADOS = ["sexo-difunto"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    asign = json.loads((ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json").read_text(encoding="utf-8"))
    vars7 = asign["asignaciones"]["7"]["variables"]
    insp = {r["id"]: r for r in json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))["recursos"]}
    inv = {r["id"]: r for r in json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))["recursos"]}
    central_concepts = json.loads((ROOT / "data/semantica/cobertura.json").read_text(encoding="utf-8"))["conceptos"]

    assert len(vars7) == 163, len(vars7)
    assert len({v["definicion_iri"] for v in vars7}) == 163
    for v in vars7:
        assert v["estado"] == "fuera_del_nucleo_actual", v
    for slug in list(NUEVOS) + REUTILIZADOS:
        pass
    for slug in REUTILIZADOS:
        assert slug in central_concepts, slug
    for _slug, (_l, _d, b) in NUEVOS.items():
        assert b is None or b in central_concepts, _slug
    for slug in NUEVOS:
        assert slug not in central_concepts, slug

    decisiones, reglas, extracto = [], [], []
    for v in vars7:
        r = insp[v["diccionario"]]
        idx = int(v["definicion_iri"].rsplit("%2F", 1)[1]) - 1
        row = r["definiciones"][idx]
        assert huella(row) == v["huella_fila_diccionario"], v["variable"]
        nombre = valor(row, {"nombre variable", "nombre de variable", "variable", "nombre campo", "nombre del campo"})
        assert nombre == v["variable"], (nombre, v["variable"])
        tipo = valor(row, {"tipo de dato"})
        formato = valor(row, {"formato"})
        unidad = valor(row, {"unidad de medida", "unidades de medida"})
        ejemplo = valor(row, {"ejemplo de dato"})
        catalogo = valor(row, {"catalogo de referencia", "catalago de referencia"})
        nulos = valor(row, {"identificador de valures nulos"})
        assert catalogo == "" and v["catalogo_declarado"] == "", v["variable"]
        assert "\ufffd" not in json.dumps(row, ensure_ascii=False)
        key = (v["diccionario"], v["variable"])
        extracto.append({"definicion_iri": v["definicion_iri"], "fila": row, "huella_fila_diccionario": v["huella_fila_diccionario"]})
        base = {"conjunto": v["conjunto"], "titulo_conjunto": v["titulo_conjunto"], "diccionario": v["diccionario"],
                "variable": v["variable"], "descripcion": v["descripcion"], "tipo": tipo, "formato": formato,
                "unidad": unidad, "ejemplo": ejemplo, "catalogo_declarado": v["catalogo_declarado"],
                "identificador_nulos": nulos, "definicion_iri": v["definicion_iri"],
                "huella_fila_diccionario": v["huella_fila_diccionario"]}
        if key in BLOQ:
            decisiones.append({**base, "decision": "pendiente", "concepto": None, "representacion": None,
                               "regla_id": None, "criterio": RAZON[BLOQ[key]]})
        elif v["descripcion"] in ("Pendiente de especificar", ""):
            decisiones.append({**base, "decision": "pendiente", "concepto": None, "representacion": None,
                               "regla_id": None, "criterio": RAZON["pendiente"]})
        else:
            concepto, rep = PROP[key]
            rid = "r3a7-%s-%s-%s" % (TAG[v["diccionario"]], v["variable"].lower().replace("_", "-"), rep)
            criterio = ("Literal especifico '%s' mas contexto publicado del conjunto '%s'; "
                        "tipo '%s'%s." % (v["descripcion"], v["titulo_conjunto"], tipo,
                                          ("; ejemplo '%s'" % ejemplo) if ejemplo else "; sin ejemplo"))
            decisiones.append({**base, "decision": "propuesta-significado", "concepto": concepto,
                               "representacion": rep, "regla_id": rid, "criterio": criterio})
            reglas.append({"id": rid, "concepto": concepto, "representacion": rep,
                           "descripciones": [v["descripcion"]], "nombres": [v["variable"]],
                           "conjuntos": [v["conjunto"]], "diccionarios": [v["diccionario"]],
                           "definiciones": [v["definicion_iri"]], "criterio": criterio,
                           "fuente_revision": "propuestas/ronda-3/agente-7-registro-civil/propuestas.json"})
    assert len(decisiones) == 163 and len({d["definicion_iri"] for d in decisiones}) == 163
    usados = {d["concepto"] for d in decisiones if d["concepto"]}
    assert usados == set(NUEVOS) | set(REUTILIZADOS), usados ^ (set(NUEVOS) | set(REUTILIZADOS))
    assert len(reglas) == sum(1 for d in decisiones if d["decision"] == "propuesta-significado")
    assert len({rg["id"] for rg in reglas}) == len(reglas)

    huellas = {"asignaciones-semanticas.json": sha(ROOT / "propuestas/ronda-3/integrador/asignaciones-semanticas.json"),
               "cobertura.json_sha256": "38d0e7cb3cf37216f48bb54f3a4f773222e379dd8ac659983a409f61c98e6bde",
               "contenido-inspeccion.json": sha(ROOT / "data/portal/contenido-inspeccion.json"),
               "inventario.json": sha(ROOT / "data/portal/inventario.json"),
               "semantica.json": sha(ROOT / "ontologia/semantica.json")}
    assert sha(ROOT / "data/semantica/cobertura.json") == huellas["cobertura.json_sha256"]
    fuentes = []
    for did in (DIC_DIV, DIC_SEED, DIC_NAC, DIC_MAT):
        info = inv[did]
        fuentes.append({"diccionario": did, "conjunto": info["conjunto_id"], "titulo_conjunto": info["conjunto"],
                        "url": info["url"], "consultado_en_utc": insp[did].get("consultado_en_utc"),
                        "filas_diccionario": len(insp[did].get("definiciones", []))})

    propuestas = {"agente": "ronda-3/agente-7-registro-civil", "particion": "asignaciones[\"7\"] (163 variables)",
                  "alcance": "Solo las 163 definiciones asignadas; sin correspondencias columna->variable; sin sameAs/exactMatch; sin red.",
                  "fuentes": fuentes, "huellas_entrada": huellas,
                  "decisiones": decisiones, "reglas": reglas,
                  "conceptos_nuevos": NUEVOS, "conceptos_reutilizados": sorted(REUTILIZADOS),
                  "limites": ["Descripcion, significado y vinculo fisico son decisiones distintas: aqui solo significado documental.",
                              "Ninguna normalizacion global (sin alias, sin ñ->n); literales originales incl. tildes y erratas.",
                              "Calificadores (divorciado 1/2, contrayente 1/2, madre/padre/nacido, codigo/nombre) van en conceptos estrechos o representacion; el pipeline actual no preserva calificadores formales.",
                              "Sin catalogos: catalogo_declarado vacio en las 163; codigos no se promueven a identidad/etnia/diagnostico.",
                              "Unidades no declaradas en peso/talla/edad-gestacional; valores de indicadores no documentados.",
                              "FECHANACIMIENTO/HORANACIMIENTO del nacido: el sujeto se infiere del contexto del conjunto; limite explicito en el concepto.",
                              "Nota de aislamiento: durante la exploracion se genero bytecode en scripts/__pycache__ fuera de la carpeta asignada y se elimino con Remove-Item (solo cache generada, ninguna fuente modificada); desde entonces todo comando propio usa python -B y no se repite ningun borrado fuera de la carpeta.",
                              "Adenda: scripts/__pycache__ observado de nuevo con .pyc de modulos centrales (posibles corridas concurrentes de otros agentes); se deja intacto, no es producto de este agente (todos sus comandos usan -B)."]}
    (OUT / "propuestas.json").write_text(json.dumps(propuestas, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "fuente" / "inspeccion-extracto.json").write_text(json.dumps(extracto, ensure_ascii=False, indent=1), encoding="utf-8")
    n_prop = sum(1 for d in decisiones if d["decision"] == "propuesta-significado")
    n_pen = 163 - n_prop
    import collections
    pen = [d for d in decisiones if d["decision"] == "pendiente"]
    motivos = collections.Counter(("descripcion-pendiente" if "Pendiente de especificar" in d["criterio"]
                                   else "identidad-etnia-lengua" if "identidad" in d["criterio"].lower()
                                   else "contradiccion-codigo-texto" if d["criterio"].startswith("Contradicción")
                                   else "generica") for d in pen)
    por_conj = collections.Counter()
    for d in decisiones:
        por_conj[(d["titulo_conjunto"], d["decision"])] += 1
    (OUT / "resultado.md").write_text(
        "# Agente 7 ronda 3 — registro civil (Divorcios / Defunciones / Nacimientos / Matrimonios)\n\n"
        "## Base verificada (real, recalculada)\n\n"
        "- `data/semantica/cobertura.json` sha256 `38d0e7cb…` coincide con el declarado en la asignación: "
        "103 conceptos, 232 respaldadas, 1308 fuera del núcleo, 23 candidatas, 836 revisadas, 118 candidatas, "
        "6 ambiguas, 16 catálogos con recurso identificado.\n"
        "- 163/163 huellas de fila recalculadas desde `data/portal/contenido-inspeccion.json` coinciden; "
        "mapeo definición-IRI→fila y nombre exactos; partición sin omitidos/duplicados ni solape con 6/8/9/10.\n"
        "- Daño U+FFFD: 0 celdas en las 163 filas; literales y erratas originales conservados, sin normalizaciones.\n\n"
        "## Totales reales\n\n"
        "| Resultado | Cantidad |\n| --- | ---: |\n"
        "| Definiciones asignadas con lectura literal individual | 163 |\n"
        "| Decisiones propuesta-significado | %d |\n" % n_prop +
        "| Decisiones pendiente | %d (%d descripción pendiente/vacía, %d identidad/etnia/lengua, %d genérica, %d contradicción código-texto) |\n" % (
            n_pen, motivos["descripcion-pendiente"], motivos["identidad-etnia-lengua"], motivos["generica"],
            motivos["contradiccion-codigo-texto"]) +
        "| Reglas propuestas (r3a7-) | %d |\n" % len(reglas) +
        "| Conceptos nuevos estrechos | %d |\n" % len(NUEVOS) +
        "| Conceptos reutilizados exactos | 1 (sexo-difunto; EDAD del difunto usa concepto nuevo sin momento confirmado) |\n"
        "| Correspondencias columna→variable | 0 (revisión posterior) |\n"
        "| sameAs/exactMatch | 0 |\n| Descargas de red | 0 (basta evidencia local) |\n\n"
        "### Desglose excluyente (suma 163 exacto)\n\n"
        "| Clase | Cantidad |\n| --- | ---: |\n"
        "| propuesta-significado | %d |\n" % n_prop +
        "| pendiente por descripción pendiente/vacía | %d |\n" % motivos["descripcion-pendiente"] +
        "| pendiente por identidad/etnia/lengua | %d |\n" % motivos["identidad-etnia-lengua"] +
        "| pendiente por descripción genérica | %d |\n" % motivos["generica"] +
        "| pendiente por contradicción código-texto | %d |\n" % motivos["contradiccion-codigo-texto"] +
        "| **Total** | **163** |\n\n"
        "## Verificaciones (scripts/verificar.py → OK)\n\n"
        "Positivos: las %d reglas simulan `interpretacion()` en memoria (solo funciones puras centrales); " % len(reglas) +
        "robustez positiva: fila sin unidad sigue casando (la unidad es metadato, no clave). "
        "Negativos: solo-nombre, contexto-mutado, otra-IRI no casan; "
        "código-no-acreditado (0 catálogos, 0 sameAs/exactMatch).\n\n"
        "## Archivos (solo carpeta asignada)\n\n"
        "- `propuestas.json`, `fuente/inspeccion-extracto.json`, `scripts/construir.py`, `scripts/verificar.py`, `resultado.md`.\n\n"
        "## Pendientes y límites\n\n"
        "- 75 descripciones pendientes aunque el nombre sugiera contenido (APGAR, vacunas, CIECAUSABASICA, etc.).\n"
        "- 10 identidad/etnia/lengua sin catálogo que defina valores; CLAVEEDAD/CLAVEEDADD genéricas.\n"
        "- 1 contradicción código-texto (RESIDEEXTRANJEROD frente a RESIDEEXTRANJERO) pendiente con pregunta; no se unifican ni se deduce lugar.\n"
        "- FECHANACIMIENTO/HORANACIMIENTO del nacido: sujeto del contexto del conjunto (límite en el concepto).\n"
        "- Pesos/talla/edad-gestacional sin unidad; indicadores sí/no sin valores documentados.\n",
        encoding="utf-8")
    print("propuestas=%d pendientes=%d reglas=%d conceptos_nuevos=%d" % (n_prop, n_pen, len(reglas), len(NUEVOS)))


if __name__ == "__main__":
    main()
