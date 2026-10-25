"""Extensión R7: adiciones exactas auditadas (lote SINAC + vínculos con significado respaldado).

Copia preparada en staging, NO instalada. Al instalar va a
`scripts/integrar_ronda_7.py` junto con `ontologia/revision-ronda-7.json` y
`data/integracion-ronda-7/`. No reutiliza el staging viejo hardcoded CLASIF.

Reglas:
- Solo reglas cuyo `definiciones == [una IRI del universo de 31 SINAC]` y con
  diccionario/conjunto/huella fijados; el subconjunto aprobado (parcial o
  vacío) lo fija `aceptadas.json` del manifiesto nuevo. Nada se asume aprobado.
- Solo vínculos del allowlist de 20 pares estructurales cuya `definicion_iri`
  quede respaldada por una regla del mismo lote (las `...D` siguen pendientes).
- Conceptos estrictamente nuevos (clave inexistente en base; reutilizar en su
  lugar si un concepto existente representa exactamente el sentido).
- Cada regla y cada vínculo exige aprobación `aceptar` en AMBAS auditorías.
- Sin códigos equivalentes, identidad de catálogos ni vigencias (barrido de
  alcance); límites escritos obligatorios; base R6 exacta congelada.
- No altera el contrato de estados del núcleo ni relaja
  `respaldada_por_definicion` (lo verifica `construir` y el core).
"""

import copy
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from construir_catalogo import ROOT, PROV

DICCIONARIO_SINAC = "22202305-2d02-4c49-b216-cc98224357f0"
CONJUNTO_SINAC = "940de7d8-73ec-4a08-8d26-b7cc97ff17bd"
RECURSO_SINAC = "46977217-9396-4f9c-bddb-6616e82530b4"

# Universo máximo de 31 definiciones SINAC propuestas en
# S2-nacimientos/v002/entrega.json (pendientes de auditoría A/B).
UNIVERSO_31 = frozenset(
    "https://example.org/mex-ontologi/definition/"
    "22202305-2d02-4c49-b216-cc98224357f0%2F" + fila
    for fila in (
        "31", "32", "34", "37", "39", "43", "45", "57", "58", "59", "61",
        "63", "65", "67", "69", "71", "72", "74", "76", "77", "79", "83",
        "84", "87", "89", "97", "99", "100", "102", "104", "106",
    )
)

# Allowlist de 20 pares estructurales (columna física exacta).
PARES_20 = frozenset([
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F102",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F103",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F104",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F105",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F83",
    "https://example.org/mex-ontologi/file-column/5772b8ec-e272-4265-a757-f7ddd179fe04%2F2020%2F2",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F14",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F20",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F64",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F66",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F67",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F68",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F69",
    "https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F70",
    "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F38",
    "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F72",
    "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F73",
    "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F74",
    "https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F75",
    "https://example.org/mex-ontologi/file-column/ad6f77b8-569d-4826-8ce0-3c6efddcb098%2FEgresos%20Hospitalarios%202018-2022%2F15",
])

REGLA_KEYS = {"id", "concepto", "representacion", "nombres", "descripciones",
              "conjuntos", "diccionarios", "definiciones",
              "huella_fila_diccionario", "limites", "limite", "calificador",
              "evidencia", "criterio", "fuente_revision", "alcance"}
VINCULO_KEYS = {"campo", "columna", "concepto", "criterio", "definicion_iri",
                "descripcion", "diccionario", "huella_esquema",
                "huella_fila_diccionario", "recurso"}
# Alcance no admitido en R7: equivalencias, homologaciones, fusiones y
# vigencias nuevas. Son subcadenas de afirmación (no menciones sueltas):
# los límites pueden decir "sin acta de vigencia", "cubre el recurso 2022"
# o "ni identidad de catálogos" en descargo, pero nunca declarar una
# vigencia nueva, equivalencia u homologación. La identidad de catálogos
# queda excluida por el pin de diccionario/conjunto, el respaldo en el mismo
# lote y el barrido equivalen/homolog/sameas/exactmatch.
PROHIBIDOS_ALCANCE = ("sameas", "exactmatch", "equivalen", "homolog",
                      "unifica", "fusiona", "nueva vigencia",
                      "vigencia nueva", "nueva_vigencia", "identity")


def _prohibido(obj):
    blob = json.dumps(obj, ensure_ascii=False).lower()
    return next((p for p in PROHIBIDOS_ALCANCE if p in blob), None)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dentro(root, relative):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError("Evidencia de ronda 7 fuera de carpeta")
    return p


def cargar(root=ROOT):
    cp = root / "ontologia/revision-ronda-7.json"
    config = json.loads(cp.read_text(encoding="utf-8"))
    folder = dentro(root, config["evidencia"])
    mp = folder / "manifiesto.json"
    if sha(mp) != config["manifiesto_sha256"]:
        raise ValueError("Manifiesto de ronda 7 modificado")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    sources = {"revision_ronda_7": cp, "manifiesto_ronda_7": mp}
    required = {"base-semantica.json", "aceptadas.json",
                "auditorias/auditoria-a.json", "auditorias/auditoria-b.json"}
    if (not isinstance(manifest.get("archivos"), dict)
            or not isinstance(manifest.get("insumos"), dict)
            or not required.issubset(manifest["archivos"])):
        raise ValueError("Manifiesto de ronda 7 incompleto")
    for category, base in [("archivos", folder), ("insumos", root)]:
        for rel, h in manifest[category].items():
            p = dentro(base, rel)
            if sha(p) != h:
                raise ValueError("Evidencia de ronda 7 modificada: " + rel)
            sources["ronda_7_" + category + "_" + rel] = p
    read = lambda rel: json.loads((folder / rel).read_text(encoding="utf-8"))
    accepted = read("aceptadas.json")
    if not isinstance(accepted.get("reglas"), list) \
            or not isinstance(accepted.get("vinculos"), list) \
            or not isinstance(accepted.get("conceptos"), dict):
        raise ValueError("aceptadas.json de ronda 7 con forma inválida")
    for row in accepted["reglas"]:
        if set(row) - REGLA_KEYS:
            raise ValueError("Regla R7 con claves no admitidas: " + row.get("id", "?"))
        if not (isinstance(row.get("definiciones"), list)
                and len(row["definiciones"]) == 1
                and row["definiciones"][0] in UNIVERSO_31):
            raise ValueError("Regla R7 fuera del universo de 31 SINAC: " + row.get("id", "?"))
        if row.get("diccionarios") != [DICCIONARIO_SINAC] \
                or row.get("conjuntos") != [CONJUNTO_SINAC]:
            raise ValueError("Regla R7 fuera de diccionario/conjunto SINAC: " + row.get("id", "?"))
        if not row.get("nombres") or not row.get("descripciones") \
                or not row.get("huella_fila_diccionario") \
                or not row.get("representacion") or not row.get("concepto"):
            raise ValueError("Regla R7 incompleta: " + row.get("id", "?"))
        if not isinstance(row.get("limites"), list) or not row["limites"]:
            raise ValueError("Regla R7 exige límites escritos: " + row.get("id", "?"))
        # El barrido cubre equivalencias/identidad/vigencias nuevas aunque vengan
        # en texto libre de criterio, alcance o límites.
        hallazgo = _prohibido(row)
        if hallazgo:
            raise ValueError("Regla R7 con alcance no admitido (" + hallazgo + "): " + row.get("id", "?"))
        origins = accepted.get("origenes", {}).get(row["id"], [])
        if not origins or any(rel not in manifest["archivos"] for rel in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 7: " + row["id"])
    respaldadas = {r["definiciones"][0] for r in accepted["reglas"]}
    for row in accepted["vinculos"]:
        if set(row) - VINCULO_KEYS:
            raise ValueError("Vínculo R7 con claves no admitidas: " + row.get("columna", "?"))
        if row.get("columna") not in PARES_20:
            raise ValueError("Vínculo R7 fuera de los 20 pares: " + row.get("columna", "?"))
        # Solo correspondencias cuyo significado queda respaldado en este lote;
        # las ...D y los pares de otros frentes siguen pendientes.
        if row.get("definicion_iri") not in respaldadas:
            raise ValueError("Vínculo R7 sin significado respaldado en el lote: " + row.get("columna", "?"))
        for k in ("huella_esquema", "huella_fila_diccionario", "descripcion",
                  "criterio", "concepto", "diccionario", "recurso", "campo"):
            if not row.get(k):
                raise ValueError("Vínculo R7 incompleto (" + k + "): " + row.get("columna", "?"))
        if _prohibido(row):
            raise ValueError("Vínculo R7 con alcance no admitido: " + row.get("columna", "?"))
        origins = accepted.get("origenes", {}).get(row["columna"], [])
        if not origins or any(rel not in manifest["archivos"] for rel in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 7: " + row["columna"])
    for k, v in accepted["conceptos"].items():
        if not isinstance(v, list) or len(v) != 3 or not v[0] or not v[1]:
            raise ValueError("Concepto R7 con forma inválida: " + k)
        if v[2] is not None and not isinstance(v[2], str):
            raise ValueError("Concepto R7 con broader inválido: " + k)
        if _prohibido(v):
            raise ValueError("Concepto R7 con alcance no admitido: " + k)
    return config, folder, read("base-semantica.json"), accepted, sources


def validar_sobre_base(rules, base_r6, root=ROOT):
    config, folder, baseline, accepted, sources = cargar(root)
    if baseline != base_r6:
        raise ValueError("Base de ronda 7 no coincide con ronda 6 validada")
    expected = copy.deepcopy(baseline)
    expected["reglas_descripcion_exacta"].extend(accepted["reglas"])
    expected["vinculos_documentales_revisados"].extend(accepted["vinculos"])
    for k, v in accepted["conceptos"].items():
        # Nada de deduplicar/sobrescribir conceptos previos silenciosamente:
        # si la clave existe, la regla debe reutilizarla en vez de redefinirla.
        if k in expected["conceptos"]:
            raise ValueError("Ronda 7 exige concepto nuevo, clave ya existente: " + k)
        expected["conceptos"][k] = v
    for field, key in [("reglas_descripcion_exacta", "id"),
                       ("vinculos_documentales_revisados", "columna")]:
        ids = [r[key] for r in rules[field]]
        if len(ids) != len(set(ids)):
            raise ValueError("Reglas o columnas duplicadas en ronda 7")
    defs = [d for r in rules["reglas_descripcion_exacta"] for d in r.get("definiciones", [])]
    if len(defs) != len(set(defs)):
        raise ValueError("Definiciones duplicadas en ronda 7")
    # Doble aprobación por regla y por vínculo: aceptar en A y en B.
    for audit_name in ("auditoria-a", "auditoria-b"):
        audit = json.loads((folder / "auditorias" / f"{audit_name}.json").read_text(encoding="utf-8"))
        ok_reglas = {x["id"] for x in audit["dictamenes"]
                     if x["tipo"] == "reglas" and x["dictamen"] == "aceptar"}
        ok_vinc = {x["id"] for x in audit["dictamenes"]
                   if x["tipo"] == "vinculos" and x["dictamen"] == "aceptar"}
        for row in accepted["reglas"]:
            if row["id"] not in ok_reglas:
                raise ValueError("Ronda 7 sin aprobación en " + audit_name + ": " + row["id"])
        for row in accepted["vinculos"]:
            if row["columna"] not in ok_vinc:
                raise ValueError("Ronda 7 sin aprobación en " + audit_name + ": " + row["columna"])
    if rules != expected:
        raise ValueError("Ronda 7 permite solo la base y las adiciones auditadas exactas")
    return config, folder, baseline, accepted, sources


def construir(report, rules, base):
    # Valida además toda la cadena histórica R4→R5→R6→R7. R4 invoca
    # validar_sobre_base (R5 delega a R6; R6 delega a R7 si existe su config);
    # no se reemplazan manifiestos anteriores.
    from integrar_ronda_4 import validar
    validar(rules)
    config, folder, baseline, accepted, sources = cargar()
    g = Graph()
    mex = Namespace(base + "vocab/")
    variables = {v["definicion_iri"]: v for v in report["variables"]}
    mappings = {v["columna"]: v for v in report["correspondencias"]
                if v["estado"] == "documental_revisada"}
    for row in accepted["reglas"]:
        observed = variables[row["definiciones"][0]]
        if observed.get("estado") != "respaldada_por_definicion" \
                or observed.get("regla") != row["id"] \
                or observed.get("concepto") != row["concepto"] \
                or observed.get("huella_fila_diccionario") != row["huella_fila_diccionario"]:
            raise ValueError("Regla R7 no materializada fielmente: " + row["id"])
        for rel in accepted["origenes"][row["id"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed["iri"]), PROV.wasDerivedFrom, entity))
    for row in accepted["vinculos"]:
        observed = mappings[row["columna"]]
        if observed["revision"] != row:
            raise ValueError("Vínculo R7 no materializado fielmente: " + row["columna"])
        for rel in accepted["origenes"][row["columna"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed["iri"]), PROV.wasDerivedFrom, entity))
    return g, dict(accepted["resumen"], manifiesto_sha256=config["manifiesto_sha256"]), sources
