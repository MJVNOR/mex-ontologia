"""Modulo RDF de evidencia calificada de cruces ronda 3 (staging, sin activar cruces).

API sencilla: construir(base, carpeta=None, fijas=None) -> (Graph, summary, sources).
No ejecuta nada al importar. TTL solo dentro de staging/ via main().
Lee SOLO la entrega aprobada y verifica SHAs CONGELADOS de los 6 insumos
(cualquier mutacion, aun internamente consistente, se rechaza); verifica SHAs
de los xlsx originales fijados; no red, no modelos.
F1/F3 historicos (recomputo desde agregados / union de listas) diferenciados de
F2 original 2020 (validacion sobre xlsx fijados). Asociacion POR FUENTE: cada
comparacion tiene 2 nodos de evidencia (grandes_grupos, indicadores) con sus
valores, medidas, nombres, filas y SHA propios; igualdad aritmetica, no identidad.
Sin sameAs/exactMatch, sin codigos INEGI inferidos, sin vigencia, sin convertir
el triaje 3916 en cruces.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef

STAGING = Path(__file__).resolve().parent
try:
    from construir_catalogo import PROV, ROOT
    AG = ROOT / "propuestas" / "ronda-3" / "agente-5-cruces"
except ImportError:  # uso standalone desde la carpeta del agente
    PROV = Namespace("http://www.w3.org/ns/prov#")
    AG = STAGING.parent
    ROOT = AG.parents[2]
BASE_DEF = "https://example.org/mex-ontologi/"

ENTREGA_SHA = "cd77771d358cd7720710fee44ff70a6e6b184f56c95289160a706794e1d382e9"

INSUMOS_SHA = {
    "propuestas.json": "cd77771d358cd7720710fee44ff70a6e6b184f56c95289160a706794e1d382e9",
    "fichas/F1.json": "d6fadb3dc36f610e457b6001d76ba9d7f6f7ebb3945f4696987462f67202d63b",
    "fichas/F2.json": "e90b571504b2e7ed499389825c49644f94b1abf1b85db995e6ba21aff126fcd5",
    "fichas/F3.json": "0daca260983253019fffc9d961c8ac5a50e7115ba0d1c18fe35e214deb80f829",
    "fichas/claves-2020.json": "49089f244747e5aa1203163ce9255f33cb6883ec0a8c527e99836086fd3219b0",
    "matriz-cruces.json": "1197d2f4e9cc0b8f90a5e6ac542553b9771f44fa717b18ee0b0851905ea3106c",
}
GG_SHA = "24301617b6a5d89cf99b34ed4d512324cedde52e0c625de9457238e3d8fa340c"
IND_SHA = "e0e21aad3a84b4059efaf7525233ac05b08ced300f0f851fbadaab94057c027a"

CODIGO_RE = re.compile(r"[0-9]{5}", re.ASCII)
ESPECIALES = {"26998", "26999"}
GG_FILAS = (2, 7345)
IND_FILAS = (2, 3673)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def leer(carpeta, rel):
    """Lee un insumo aprobado y exige su SHA congelado (rechaza toda mutacion)."""
    p = carpeta / rel
    if sha(p) != INSUMOS_SHA[rel]:
        raise ValueError("Insumo aprobado modificado: " + rel)
    return p, json.loads(p.read_text(encoding="utf-8"))


def verificar_originales(fijas=None):
    """Verifica SHAs de los xlsx originales fijados en ronda 1."""
    fijas = fijas or {}
    ok = {}
    for sha_esperado in (GG_SHA, IND_SHA):
        p = Path(fijas[sha_esperado]) if sha_esperado in fijas else (
            ROOT / "data" / "integracion" / "fuentes" / (sha_esperado + ".xlsx"))
        if sha(p) != sha_esperado:
            raise ValueError("Original fijado modificado: " + sha_esperado)
        ok[sha_esperado] = p
    return ok


def codigo_textual(code):
    """Codigo municipal textual de 5 digitos ASCII; rechaza int, no digitos y especiales."""
    if not isinstance(code, str):
        raise ValueError("Codigo no textual (int no aceptado): " + repr(code))
    if CODIGO_RE.fullmatch(code) is None:
        raise ValueError("Codigo no ASCII de 5 digitos: " + repr(code))
    if code in ESPECIALES:
        raise ValueError("Categoria especial no municipal: " + code)
    return code  # literal, sin padding ni equivalencia INEGI


def construir(base=BASE_DEF, carpeta=None, fijas=None):
    carpeta = Path(carpeta) if carpeta else AG
    leidos = {}
    for rel in INSUMOS_SHA:
        leidos[rel] = leer(carpeta, rel)
    propuestas = leidos["propuestas.json"][1]
    f1 = leidos["fichas/F1.json"][1]
    f2 = leidos["fichas/F2.json"][1]
    f3 = leidos["fichas/F3.json"][1]
    c20 = leidos["fichas/claves-2020.json"][1]
    matriz = leidos["matriz-cruces.json"][1]
    _propuestas = propuestas
    originales = verificar_originales(fijas)
    gg_sha = f2["fuentes"]["grandes_grupos"]["sha256"]
    ind_sha = f2["fuentes"]["indicadores"]["sha256"]
    if set(originales) != {gg_sha, ind_sha}:
        raise ValueError("SHAs F2 no coinciden con originales fijados")

    mex = Namespace(base + "vocab/")
    g = Graph()
    for prefix, ns in [("mex", mex), ("prov", PROV)]:
        g.bind(prefix, ns)

    def node(kind, key):
        return URIRef(base + kind + "/" + quote(str(key), safe=""))

    def lit(s, key, value):
        if value is not None:
            g.add((s, mex[key], Literal(value)))

    clases = {"RevisionCruceRonda3": "Evidencia calificada de cruce, ronda 3",
              "ComparacionMunicipal2020": "Yuxtaposicion municipal 2020 por clave textual",
              "EvidenciaFuenteComparacion": "Evidencia de una fuente en una comparacion",
              "EvidenciaGrandesGrupos2020": "Evidencia de grandes grupos en 2020",
              "EvidenciaIndicadores2020": "Evidencia de indicadores en 2020"}
    props_o = {"comparacionDe": "Comparacion de la revision",
               "evidenciaDeFuente": "Evidencia aportada por la fuente en la comparacion",
               "fuenteOriginal": "Archivo original fijado"}
    props_d = {"estadoDecision": "Decision de triaje de la ficha",
               "tipoEvidencia": "Alcance probatorio (historico vs original)",
               "alcanceVerificacion": "Alcance expreso de lo verificado",
               "condicionVerificada": "Condicion ya verificada",
               "condicionPendiente": "Bloqueo de uso interpretativo",
               "fuenteRol": "Fuente de la evidencia (grandes_grupos o indicadores)",
               "medidaOrigen": "Medida publicada por la fuente",
               "periodoCruzado": "Periodo cruzado",
               "transformacionPrevia": "Agregacion previa al join",
               "codigoTextual": "Codigo literal sin equivalencia INEGI",
               "nombreOrigen": "Nombre literal de la fuente",
               "valorOrigen": "Valor agregado publicado por la fuente",
               "igualdadValores": "Coherencia aritmetica, no identidad de medida",
               "filaOrigen": "Fila unica de la hoja original",
               "filaOrigenHombres": "Fila de HOMBRES en la hoja original",
               "filaOrigenMujeres": "Fila de MUJERES en la hoja original",
               "shaFuente": "SHA-256 unico del archivo original",
               "hojaFuente": "Hoja del archivo original",
               "limiteInterpretativo": "Limite de interpretacion"}
    for k, label in clases.items():
        g.add((mex[k], RDF.type, OWL.Class))
        g.add((mex[k], RDFS.label, Literal(label, lang="es")))
    for k, label in {**props_o}.items():
        g.add((mex[k], RDF.type, OWL.ObjectProperty))
        g.add((mex[k], RDFS.label, Literal(label, lang="es")))
    for k, label in props_d.items():
        g.add((mex[k], RDF.type, OWL.DatatypeProperty))
        g.add((mex[k], RDFS.label, Literal(label, lang="es")))

    triaje = matriz["resumen"]["decisiones"]
    if sum(triaje.values()) != matriz["resumen"]["total"]:
        raise ValueError("Resumen de triaje inconsistente")

    fichas = {"F1": (f1, "recomputo_agregados_fuente_historico"),
              "F2": (f2, "validacion_original_2020"),
              "F3": (f3, "union_listas_fuente_historico")}
    pares_aprobados = {f["caso"]: f["par"] for f in propuestas["fichas"]}
    reviews = {}
    for caso, (ficha, tipo) in fichas.items():
        for req in ("decision", "alcance", "condiciones_verificadas",
                    "condiciones_que_impiden_uso_interpretativo"):
            if req not in ficha:
                raise ValueError(ficha.get("caso", caso) + " sin " + req)
        r = node("cruce-r3", caso)
        reviews[caso] = r
        g.add((r, RDF.type, mex.RevisionCruceRonda3))
        g.add((r, RDFS.label,
               Literal(caso + " — " + ficha.get("par", pares_aprobados.get(caso, caso)), lang="es")))
        lit(r, "estadoDecision", ficha["decision"])
        lit(r, "tipoEvidencia", tipo)
        lit(r, "alcanceVerificacion", ficha["alcance"])
        for c in ficha["condiciones_verificadas"]:
            lit(r, "condicionVerificada", c)
        for c in ficha["condiciones_que_impiden_uso_interpretativo"]:
            lit(r, "condicionPendiente", c)
        for nc in ficha.get("no_concluye", []):
            lit(r, "limiteInterpretativo", nc)
        g.add((r, PROV.wasDerivedFrom, URIRef((carpeta / ("fichas/" + caso + ".json")).as_uri())))

    # F2: 72 comparaciones 2020; evidencia SEPARADA por fuente (2 nodos por comparacion)
    if c20["anos_cruzados"] != ["2020"] or c20["anos_observados_ambos"] != "1990-2040":
        raise ValueError("Alcance F2 alterado")
    filas = c20["filas"]
    if len(filas) != 72:
        raise ValueError("Comparaciones 2020 != 72")
    vistos = set()
    for f in filas:
        if f["anio"] != "2020" or not f["igualdad"]:
            raise ValueError("Fila 2020 alterada: " + f["codigo_origen"])
        cod = codigo_textual(f["codigo_origen"])
        if cod in vistos:
            raise ValueError("Codigo duplicado: " + cod)
        vistos.add(cod)
        fh, fm = f["fuente_grandes_grupos"]["fila_hombres"], f["fuente_grandes_grupos"]["fila_mujeres"]
        fi = f["fuente_indicadores"]["fila"]
        if not (GG_FILAS[0] <= fh <= GG_FILAS[1] and GG_FILAS[0] <= fm <= GG_FILAS[1]
                and IND_FILAS[0] <= fi <= IND_FILAS[1]):
            raise ValueError("Coordenada fuera de rango: " + cod)
        if f["fuente_grandes_grupos"]["sha256"] != gg_sha or f["fuente_indicadores"]["sha256"] != ind_sha:
            raise ValueError("SHA de fuente 2020 alterado: " + cod)
        if int(f["pob_total_h_m"]) != int(f["pob_mit_mun"]):
            raise ValueError("Coherencia POB rota: " + cod)
        c = node("cruce-r3-2020", cod)
        g.add((c, RDF.type, mex.ComparacionMunicipal2020))
        g.add((c, RDFS.label, Literal(cod + " — 2020", lang="es")))
        g.add((c, mex.comparacionDe, reviews["F2"]))
        lit(c, "codigoTextual", cod)
        lit(c, "periodoCruzado", "2020")
        lit(c, "igualdadValores", True)
        lit(c, "transformacionPrevia", "suma H+M por (CLAVE,ANO) antes del join")
        lit(c, "limiteInterpretativo", "igualdad aritmetica 2020, no identidad de medida")
        ev_g = node("cruce-r3-2020-evidencia", cod + "/grandes_grupos")
        g.add((ev_g, RDF.type, mex.EvidenciaFuenteComparacion))
        g.add((ev_g, RDF.type, mex.EvidenciaGrandesGrupos2020))
        g.add((ev_g, mex.evidenciaDeFuente, c))
        lit(ev_g, "fuenteRol", "grandes_grupos")
        lit(ev_g, "codigoTextual", cod)
        lit(ev_g, "nombreOrigen", f["nombre_grandes_grupos"])
        lit(ev_g, "valorOrigen", int(f["pob_total_h_m"]))
        lit(ev_g, "medidaOrigen", "suma_grupos_edad_H_M")
        lit(ev_g, "filaOrigenHombres", fh)
        lit(ev_g, "filaOrigenMujeres", fm)
        lit(ev_g, "shaFuente", gg_sha)
        lit(ev_g, "hojaFuente", "Sheet 1")
        g.add((ev_g, mex.fuenteOriginal, URIRef(originales[gg_sha].as_uri())))
        ev_i = node("cruce-r3-2020-evidencia", cod + "/indicadores")
        g.add((ev_i, RDF.type, mex.EvidenciaFuenteComparacion))
        g.add((ev_i, RDF.type, mex.EvidenciaIndicadores2020))
        g.add((ev_i, mex.evidenciaDeFuente, c))
        lit(ev_i, "fuenteRol", "indicadores")
        lit(ev_i, "codigoTextual", cod)
        lit(ev_i, "nombreOrigen", f["nombre_indicadores"])
        lit(ev_i, "valorOrigen", int(f["pob_mit_mun"]))
        lit(ev_i, "medidaOrigen", "poblacion_mitad_ano")
        lit(ev_i, "filaOrigen", fi)
        lit(ev_i, "shaFuente", ind_sha)
        lit(ev_i, "hojaFuente", "Sheet 1")
        g.add((ev_i, mex.fuenteOriginal, URIRef(originales[ind_sha].as_uri())))

    for s, _p, o in g:
        if "sameAs" in str(_p) or "exactMatch" in str(_p):
            raise ValueError("Equivalencia prohibida en el modulo")
        if "inegi" in str(o).lower() and isinstance(o, URIRef):
            raise ValueError("Codigo INEGI inferido: " + str(o))

    summary = {"fichas": len(reviews), "comparaciones_2020": len(filas),
               "evidencias_fuente": 2 * len(filas),
               "triaje_informativo": dict(triaje), "no_habilita_cruces": True,
               "entrega_aprobada_sha256": ENTREGA_SHA,
               "sha_insumos": dict(INSUMOS_SHA),
               "sha_originales": {s: sha(p) for s, p in originales.items()}}
    sources = {"propuestas": carpeta / "propuestas.json",
               "ficha_f1": carpeta / "fichas/F1.json",
               "ficha_f2": carpeta / "fichas/F2.json",
               "ficha_f3": carpeta / "fichas/F3.json",
               "claves_2020": carpeta / "fichas/claves-2020.json",
               "matriz_triaje": carpeta / "matriz-cruces.json",
               "original_grandes_grupos": originales[gg_sha],
               "original_indicadores": originales[ind_sha]}
    return g, summary, sources


def main():
    g, summary, _sources = construir()
    (STAGING / "cruces-r3.ttl").write_text(g.serialize(format="turtle"), encoding="utf-8")
    (STAGING / "resumen-cruces-r3.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("cruces-r3:", summary["fichas"], "fichas,",
          summary["comparaciones_2020"], "comparaciones,", summary["evidencias_fuente"], "evidencias")


if __name__ == "__main__":
    main()
