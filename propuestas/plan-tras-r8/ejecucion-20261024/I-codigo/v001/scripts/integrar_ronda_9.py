"""Ronda 9 (STAGING en I-codigo/v001, NO instalada).

Solo integra pilotos aceptados post-R8:
- P1-QUDT v002: 2 declaraciones cualificadas de unidad (Q1 MilliM, Q3 HA
  con IRI HTTP canonica verificada por W). Q2 hm3 queda fuera: sin vinculo,
  sin conversiones, sin QuantityValue.
- P4 v002: shape de exclusion significadoDocumentado/significadoCandidato
  via sh:sparql (forma exacta v001) + 4 fixtures re-ejecutadas en store
  temporal (ver P4 v002/entrega.json; aqui se pinnea forma por SHA).
- P2/P3 negativas: 0 intervalos, 0 jerarquias. C1-C4 son vistas derivadas,
  no se materializan.

Al instalar va a `scripts/integrar_ronda_9.py` con
`ontologia/revision-ronda-9.json` y `data/integracion-ronda-9/`.
Nada de este staging toca produccion, manifiestos R1-R8, grafo ni Studio.
"""

import hashlib
import json
import unicodedata
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from construir_catalogo import ROOT, PROV

EVIDENCIA = "data/integracion-ronda-9"

REQUIRED = {"datos/propuesta-qudt.ttl", "modelo/vocabulario-minimo.ttl",
            "shapes/shape-exclusion-significado.ttl", "base-semantica.json",
            "cobertura-r8.json", "aceptadas.json",
            "auditorias/auditoria-a.json", "auditorias/auditoria-b.json"}

# Pin R8: resumen inmutable que R9 no edita (nucleo intacto).
PIN_RESPALADADAS = 1423
PIN_CONCEPTOS = 1106
PIN_REVISADAS = 4506
PIN_CANDIDATAS = 17
PIN_MATERIALIZADAS = 1442

SHAPE_SHA = "fc301d854b6c9175be601282ab4073f054a1736103b92ea634003c7bcc2b148d"

QUDT_OK = {"http://qudt.org/vocab/unit/MilliM", "http://qudt.org/vocab/unit/HA"}

DECL_KEYS = {"id", "sujeto", "variable", "definicion_iri", "unidad_literal",
             "unidad_qudt", "diccionario", "conjunto", "huella_fila_diccionario",
             "normativa"}

# Tabla pinnada: solo estas 2 declaraciones existen. Q2 hm3 NO figura.
DECL_PIN = {
    "P1-Q1": {
        "sujeto": "https://example.org/mex-ontologi/propuesta/p1-qudt/v002/declaracion-precipitacion-mm",
        "variable": "https://example.org/mex-ontologi/documented-variable/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
        "definicion_iri": "https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
        "unidad_literal": "Milimetros",
        "unidad_qudt": "http://qudt.org/vocab/unit/MilliM",
        "diccionario": "6713de4e-1e2b-447d-8000-f6ceaabd8473",
        "conjunto": "8b4edefe-cb1a-401c-90c6-05548779defd",
        "huella_fila_diccionario": "dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f",
        "normativa": {"archivo": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-MilliM-evidencia.txt",
                      "sha256": "5e63691124e69c162ddfa65bde77fb1ad3e9a2173ffd33b9910100880a9ea9a7",
                      "url": "https://qudt.org/vocab/unit/MilliM"},
    },
    "P1-Q3": {
        "sujeto": "https://example.org/mex-ontologi/propuesta/p1-qudt/v002/declaracion-superficie-ha",
        "variable": "https://example.org/mex-ontologi/documented-variable/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
        "definicion_iri": "https://example.org/mex-ontologi/definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
        "unidad_literal": "Hectareas",
        "unidad_qudt": "http://qudt.org/vocab/unit/HA",
        "diccionario": "94215f51-9c89-414d-8c3d-92792e609a2a",
        "conjunto": "3e17a7e8-c8d4-49c4-a426-4dec099cd0cd",
        "huella_fila_diccionario": "208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321",
        "normativa": {"archivo": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-HA-evidencia.txt",
                      "sha256": "9095968323f72af577b4a94684a78e2f806595ca118529b5e47cb0b2acd1ee3e",
                      "url": "https://qudt.org/vocab/unit/HA"},
    },
}

PROHIBIDO = ("QuantityValue", "conversionMultiplier", "conversionFactor",
             "conversionOffset", "qudt:expression", "QuantityKind",
             "hasQuantityKind", "HectoM3", "HectoHA", "https://qudt.org/vocab/unit")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dentro(root, relative):
    p = (Path(root) / relative).resolve()
    if not p.is_relative_to(Path(root).resolve()):
        raise ValueError("Evidencia de ronda 9 fuera de carpeta: " + str(relative))
    return p


def _clave(texto):
    # ponytail: normalizacion local minima (tolerar Milimetros/Milimetros
    # con acento); upgrade path: importar clave() de integrar_contenido.
    nfkd = unicodedata.normalize("NFKD", str(texto or ""))
    return "".join(c for c in nfkd if not unicodedata.combining(c)).casefold().strip()


def cargar(root=ROOT):
    root = Path(root)
    cp = root / "ontologia/revision-ronda-9.json"
    config = json.loads(cp.read_text(encoding="utf-8"))
    if config.get("evidencia") != EVIDENCIA:
        raise ValueError("Ronda 9 exige evidencia " + EVIDENCIA)
    folder = dentro(root, config["evidencia"])
    mp = folder / "manifiesto.json"
    if sha(mp) != config["manifiesto_sha256"]:
        raise ValueError("Manifiesto de ronda 9 modificado")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    if manifest.get("format_version") != 1:
        raise ValueError("Manifiesto R9 exige format_version 1 separado de release")
    if not isinstance(manifest.get("archivos"), dict) \
            or not REQUIRED.issubset(manifest["archivos"]):
        raise ValueError("Manifiesto de ronda 9 incompleto")
    sources = {"revision_ronda_9": cp, "manifiesto_ronda_9": mp}
    for rel, h in manifest["archivos"].items():
        p = dentro(folder, rel)
        if sha(p) != h:
            raise ValueError("Evidencia de ronda 9 modificada: " + rel)
        sources["ronda_9_" + rel] = p
    for rel, h in (manifest.get("insumos") or {}).items():
        p = dentro(root, rel)
        if sha(p) != h:
            raise ValueError("Insumo de ronda 9 modificado: " + rel)
        sources["ronda_9_insumo_" + rel] = p
    read = lambda rel: json.loads((folder / rel).read_text(encoding="utf-8"))
    accepted = read("aceptadas.json")
    baseline = read("base-semantica.json")
    cob8 = read("cobertura-r8.json")
    # Sin edicion del nucleo por esta via: 0 reglas, 0 conceptos, 0 vinculos core.
    if accepted.get("reglas", []) != [] or accepted.get("conceptos", {}) != {} \
            or accepted.get("vinculos", []) != []:
        raise ValueError("Ronda 9 no edita el nucleo: 0 reglas, 0 conceptos, 0 vinculos")
    if accepted.get("format_version") != 1 or accepted.get("release_base") != "R8":
        raise ValueError("aceptadas R9 exige format_version 1 y release_base R8")
    # Pin R8 en snapshot: 1423/1106/4506/17/variables1442.
    res8 = cob8.get("resumen", {})
    if res8.get("estados_variables", {}).get("respaldada_por_definicion") != PIN_RESPALADADAS \
            or res8.get("conceptos_compartidos") != PIN_CONCEPTOS \
            or res8.get("estados_correspondencias", {}).get("documental_revisada") != PIN_REVISADAS \
            or res8.get("estados_correspondencias", {}).get("candidata_por_nombre") != PIN_CANDIDATAS \
            or res8.get("variables_materializadas") != PIN_MATERIALIZADAS:
        raise ValueError("cobertura-r8.json sin pin 1423/1106/4506/17/1442")
    decls = accepted.get("declaraciones")
    if not isinstance(decls, list) or {d.get("id") for d in decls} != set(DECL_PIN):
        raise ValueError("Ronda 9 admite exactamente P1-Q1 y P1-Q3 (Q2 hm3 fuera)")
    cob_vars = {v.get("definicion_iri"): v for v in cob8.get("variables", [])}
    datos_txt = (folder / "datos/propuesta-qudt.ttl").read_text(encoding="utf-8")
    for tok in PROHIBIDO:
        if tok in datos_txt:
            raise ValueError("propuesta-qudt.ttl con token prohibido: " + tok)
    if "file-column" in datos_txt:
        raise ValueError("Unidad solo sobre definicion local: sin columna fisica en TTL")
    for d in decls:
        if set(d) - DECL_KEYS:
            raise ValueError("Declaracion R9 con claves no admitidas: " + d.get("id", "?"))
        pin = DECL_PIN[d["id"]]
        for k in ("sujeto", "variable", "definicion_iri", "unidad_literal",
                  "unidad_qudt", "diccionario", "conjunto", "huella_fila_diccionario"):
            if d.get(k) != pin[k]:
                raise ValueError("Declaracion R9 distinta al pin: " + d["id"] + "/" + k)
        if d.get("normativa") != pin["normativa"]:
            raise ValueError("Declaracion R9 sin normativa pinnada: " + d["id"])
        if d.get("unidad_qudt") not in QUDT_OK:
            raise ValueError("Declaracion R9 sin IRI HTTP canonica: " + d["id"])
        base_var = cob_vars.get(d["definicion_iri"])
        if base_var is None or base_var.get("estado") != "respaldada_por_definicion":
            raise ValueError("Declaracion R9 sin respaldo documental: " + d["id"])
        for k in ("huella_fila_diccionario", "conjunto", "diccionario"):
            if base_var.get(k) != d[k]:
                raise ValueError("Declaracion R9 sin fila local exacta: " + d["id"] + "/" + k)
        if base_var.get("iri") != d["variable"]:
            raise ValueError("Declaracion R9 sin variable local exacta: " + d["id"])
        # Fila local por huella (sin inferir por parecido): unica y con la
        # misma unidad literal (tolerando acentos) y variable que cobertura.
        insp = json.loads((root / "data/portal/inspecciones" / (d["diccionario"] + ".json")).read_text(encoding="utf-8"))
        filas = [r for r in insp.get("definiciones", [])
                 if _huella_fila(r) == d["huella_fila_diccionario"]]
        if len(filas) != 1:
            raise ValueError("Declaracion R9 sin fila local unica: " + d["id"])
        if _clave(filas[0].get("Unidad de medida", "")) != _clave(d["unidad_literal"]):
            raise ValueError("Unidad R9 sin respaldo en inspeccion local: " + d["id"])
        if _clave(filas[0].get("Nombre variable", "")) != _clave(base_var.get("variable", "")):
            raise ValueError("Variable R9 sin nombre local exacto: " + d["id"])
        # Normativa W pinnada (archivo fuera de evidencia, verificado por SHA).
        norm = root / d["normativa"]["archivo"]
        if not str(d["normativa"]["archivo"]).startswith("propuestas/") \
                or sha(norm) != d["normativa"]["sha256"]:
            raise ValueError("Normativa W modificada o fuera de sitio: " + d["id"])
        if d["sujeto"] not in datos_txt or d["definicion_iri"] not in datos_txt \
                or d["unidad_literal"] not in datos_txt or d["unidad_qudt"] not in datos_txt:
            raise ValueError("Declaracion R9 ausente en TTL de datos: " + d["id"])
        origins = (accepted.get("origenes") or {}).get(d["id"], [])
        if not origins or any(o not in manifest["archivos"] for o in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 9: " + d["id"])
    _verificar_grafo_minimo(folder)
    _verificar_shape(folder)
    return config, folder, baseline, accepted, cob8, sources


def _huella_fila(value):
    # Replica exacta de consolidar_semantica.huella (sin importar el core).
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _verificar_grafo_minimo(folder):
    datos = Graph()
    datos.parse(folder / "datos/propuesta-qudt.ttl", format="turtle")
    modelo = Graph()
    modelo.parse(folder / "modelo/vocabulario-minimo.ttl", format="turtle")
    mex = Namespace("https://example.org/mex-ontologi/vocab/")
    sujetos = set(datos.subjects(RDF.type, mex.UnidadDeclarada))
    esperados = {URIRef(DECL_PIN[i]["sujeto"]) for i in DECL_PIN}
    if sujetos != esperados:
        raise ValueError("Grafo R9 exige exactamente 2 declaraciones P1-Q1/Q3")
    for s in esperados:
        if set(datos.objects(s, mex.unidadQudt)) != {URIRef(DECL_PIN[_id_por_sujeto(s)]["unidad_qudt"])}:
            raise ValueError("Vinculo QUDT inexacto: " + str(s))
        if list(datos.objects(URIRef(DECL_PIN[_id_por_sujeto(s)]["variable"]), mex.unidadQudt)):
            raise ValueError("Unidad solo en declaracion, nunca en variable: " + str(s))
    # Vocabulario minimo: terminos nuevos, sin QuantityValue ni conversiones.
    modelo_txt = (folder / "modelo/vocabulario-minimo.ttl").read_text(encoding="utf-8")
    for tok in PROHIBIDO:
        if tok in modelo_txt:
            raise ValueError("vocabulario-minimo con token prohibido: " + tok)
    if "mex:UnidadDeclarada" not in modelo_txt or "mex:unidadQudt" not in modelo_txt:
        raise ValueError("vocabulario-minimo incompleto")


def _id_por_sujeto(sujeto):
    for i, pin in DECL_PIN.items():
        if pin["sujeto"] == str(sujeto):
            return i
    raise ValueError("Sujeto R9 desconocido: " + str(sujeto))


def _verificar_shape(folder):
    p = folder / "shapes/shape-exclusion-significado.ttl"
    if sha(p) != SHAPE_SHA:
        raise ValueError("Shape R9 sin hash pinnado v001")
    txt = p.read_text(encoding="utf-8")
    for frag in ("sh:sparql", "VariableDocumentada", "significadoDocumentado",
                 "significadoCandidato", "sh:select"):
        if frag not in txt:
            raise ValueError("Shape R9 sin estructura esperada: " + frag)
    g = Graph()
    g.parse(p, format="turtle")
    from rdflib.namespace import SH
    if len(list(g.triples((None, SH.sparql, None)))) != 1:
        raise ValueError("Shape R9 exige un unico sh:sparql")


def cargar_shapes(root=ROOT):
    """Devuelve el Graph SHACL de R9 ya verificado (hash + estructura)."""
    _config, folder, _b, _a, _c, _s = cargar(root)
    g = Graph()
    g.parse(folder / "shapes/shape-exclusion-significado.ttl", format="turtle")
    return g


def construir(report, rules, base, root=ROOT):
    # Cadena R4->...->R8 sin tocarla: solo se valida, no se reescribe.
    if (Path(root) / "ontologia/revision-ronda-4.json").exists():
        from integrar_ronda_4 import validar
        validar(rules, Path(root))
    config, folder, baseline, accepted, cob8, sources = cargar(root)
    if baseline != rules:
        raise ValueError("Base de ronda 9 no coincide con semantica actual")
    res = (report.get("resumen") or {})
    if res.get("estados_variables", {}).get("respaldada_por_definicion") != PIN_RESPALADADAS \
            or res.get("conceptos_compartidos") != PIN_CONCEPTOS \
            or res.get("estados_correspondencias", {}).get("documental_revisada") != PIN_REVISADAS \
            or res.get("estados_correspondencias", {}).get("candidata_por_nombre") != PIN_CANDIDATAS \
            or res.get("variables_materializadas") != PIN_MATERIALIZADAS:
        raise ValueError("Reporte vivo sin pin R8 1423/1106/4506/17/1442")
    # Doble aprobacion A+B: global aceptar + SHA exacto + por caso.
    sha_aceptadas = sha(folder / "aceptadas.json")
    for audit_name in ("auditoria-a", "auditoria-b"):
        audit = json.loads((folder / "auditorias" / f"{audit_name}.json").read_text(encoding="utf-8"))
        if audit.get("dictamen") != "aceptar":
            raise ValueError("Ronda 9 sin dictamen global aceptar en " + audit_name)
        if audit.get("aceptadas_sha256") != sha_aceptadas:
            raise ValueError("Ronda 9 exige aceptadas_sha256 pinnado en " + audit_name)
        ok = {x["id"] for x in audit.get("dictamenes", [])
              if x.get("tipo") == "declaraciones" and x.get("dictamen") == "aceptar"}
        for d in accepted["declaraciones"]:
            if d["id"] not in ok:
                raise ValueError("Ronda 9 sin aprobacion en " + audit_name + ": " + d["id"])
    if rules != baseline:
        raise ValueError("Ronda 9 no edita el nucleo")
    # Fidelidad: la declaracion propuesta sigue materializada en el vivo.
    vivas = {v.get("definicion_iri"): v for v in report.get("variables", [])}
    for d in accepted["declaraciones"]:
        obs = vivas.get(d["definicion_iri"])
        if obs is None or obs.get("estado") != "respaldada_por_definicion" \
                or obs.get("iri") != d["variable"] \
                or obs.get("huella_fila_diccionario") != d["huella_fila_diccionario"]:
            raise ValueError("Declaracion R9 no materializada fielmente: " + d["id"])
    g = Graph()
    datos = Graph()
    datos.parse(folder / "datos/propuesta-qudt.ttl", format="turtle")
    g += datos
    modelo = Graph()
    modelo.parse(folder / "modelo/vocabulario-minimo.ttl", format="turtle")
    g += modelo
    mex = Namespace(str(base) + "vocab/")
    for d in accepted["declaraciones"]:
        for rel in accepted["origenes"][d["id"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(d["sujeto"]), PROV.wasDerivedFrom, entity))
    return g, dict(accepted.get("resumen", {}), manifiesto_sha256=config["manifiesto_sha256"],
                   format_version=1, release="R9"), sources
