"""Extension R8: solo 28 vinculos SINAC con significado ya respaldado en R7.

Copia en I-codigo/v002 (staging, NO instalada). Al instalar va a
`scripts/integrar_ronda_8.py` con `ontologia/revision-ronda-8.json` y
`data/integracion-ronda-8/`.

Alcance cerrado: 0 reglas, 0 conceptos. Cada vinculo une una columna fisica
del universo pinnado de 28 con una definicion ya respaldada en la cobertura
R7 pinnada, con concepto identico al de su respaldo. Sin joins, vigencias,
equivalencias, codigos ni identidad de catalogos. `construir()` solo emite
PROV.wasDerivedFrom + sha256Evidencia sobre nodos del core.
"""

import copy
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from construir_catalogo import ROOT, PROV

DICCIONARIO_SINAC = "22202305-2d02-4c49-b216-cc98224357f0"
RECURSO_SINAC = "46977217-9396-4f9c-bddb-6616e82530b4"
HUELLA_ESQUEMA_SINAC = "9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95"
PREFIX_DEFINICION = "https://example.org/mex-ontologi/definition/"

# Universo pinnado de 28 columnas fisicas SINAC (aceptadas.json v002).
UNIVERSO_28 = frozenset(
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F" + n
    for n in ("100", "106", "31", "32", "34", "37", "39", "43", "45", "57",
              "58", "59", "61", "63", "65", "67", "69", "71", "72", "74",
              "76", "77", "79", "84", "87", "89", "97", "99")
)

VINCULO_KEYS = {"campo", "columna", "concepto", "criterio", "definicion_iri",
                "descripcion", "diccionario", "huella_esquema",
                "huella_fila_diccionario", "recurso"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dentro(root, relative):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError("Evidencia de ronda 8 fuera de carpeta")
    return p


def cargar(root=ROOT):
    cp = root / "ontologia/revision-ronda-8.json"
    config = json.loads(cp.read_text(encoding="utf-8"))
    folder = dentro(root, config["evidencia"])
    mp = folder / "manifiesto.json"
    if sha(mp) != config["manifiesto_sha256"]:
        raise ValueError("Manifiesto de ronda 8 modificado")
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    sources = {"revision_ronda_8": cp, "manifiesto_ronda_8": mp}
    required = {"base-semantica.json", "aceptadas.json", "cobertura-r7.json",
                "auditorias/auditoria-a.json", "auditorias/auditoria-b.json"}
    if not isinstance(manifest.get("archivos"), dict) \
            or not required.issubset(manifest["archivos"]):
        raise ValueError("Manifiesto de ronda 8 incompleto")
    for rel, h in manifest["archivos"].items():
        p = dentro(folder, rel)
        if sha(p) != h:
            raise ValueError("Evidencia de ronda 8 modificada: " + rel)
        sources["ronda_8_" + rel] = p
    read = lambda rel: json.loads((folder / rel).read_text(encoding="utf-8"))
    accepted = read("aceptadas.json")
    baseline = read("base-semantica.json")
    cob7 = read("cobertura-r7.json")
    # Pin resumen R7: fija candidatas y pre-estados del reporte vivo.
    res7 = cob7.get("resumen", {})
    if res7.get("estados_correspondencias", {}).get("documental_revisada") != 4478 \
            or res7.get("estados_correspondencias", {}).get("candidata_por_nombre") != 45 \
            or res7.get("estados_variables", {}).get("respaldada_por_definicion") != 1423 \
            or res7.get("estados_variables", {}).get("candidata_sin_definicion_suficiente") != 16 \
            or res7.get("estados_variables", {}).get("fuera_del_nucleo_actual") != 124 \
            or res7.get("conceptos_compartidos") != 1106 \
            or res7.get("columnas_con_correspondencia") != 4523:
        raise ValueError("cobertura-r7.json sin pin 4478/45/1423/16/124/1106/4523")
    if {m["columna"] for m in cob7.get("correspondencias", [])
            if m.get("estado") == "candidata_por_nombre"} < UNIVERSO_28:
        raise ValueError("cobertura-r7.json sin el universo de 28 candidatas")
    if accepted.get("reglas") != [] or accepted.get("conceptos") != {} \
            or not isinstance(accepted.get("vinculos"), list):
        raise ValueError("Ronda 8 admite solo vinculos: 0 reglas, 0 conceptos")
    # Respaldo R7 por variable pinnada (estado+concepto+huella, no por reglas).
    resp7 = {v.get("definicion_iri"): v for v in cob7.get("variables", [])
             if v.get("estado") == "respaldada_por_definicion"}
    if len(accepted["vinculos"]) != 28:
        raise ValueError("Ronda 8 exige exactamente 28 vinculos")
    for row in accepted["vinculos"]:
        if set(row) - VINCULO_KEYS:
            raise ValueError("Vinculo R8 con claves no admitidas: " + row.get("columna", "?"))
        if row.get("columna") not in UNIVERSO_28:
            raise ValueError("Vinculo R8 fuera del universo de 28: " + row.get("columna", "?"))
        if not (isinstance(row.get("definicion_iri"), str)
                and row["definicion_iri"].startswith(PREFIX_DEFINICION)):
            raise ValueError("Vinculo R8 sin IRI definition exacta: " + row.get("columna", "?"))
        base = resp7.get(row.get("definicion_iri"))
        if base is None or row.get("concepto") != base.get("concepto"):
            raise ValueError("Vinculo R8 sin respaldo R7 con concepto identico: " + row.get("columna", "?"))
        if row.get("huella_fila_diccionario") != base.get("huella_fila_diccionario"):
            raise ValueError("Vinculo R8 sin huella de fila exacta: " + row.get("columna", "?"))
        if row.get("diccionario") != DICCIONARIO_SINAC \
                or row.get("recurso") != RECURSO_SINAC \
                or row.get("huella_esquema") != HUELLA_ESQUEMA_SINAC:
            raise ValueError("Vinculo R8 fuera de scope SINAC pinnado: " + row.get("columna", "?"))
        for k in ("campo", "descripcion", "criterio"):
            if not row.get(k):
                raise ValueError("Vinculo R8 incompleto (" + k + "): " + row.get("columna", "?"))
        if row.get("concepto") not in baseline.get("conceptos", {}):
            raise ValueError("Vinculo R8 con concepto inexistente en base: " + row.get("columna", "?"))
        origins = accepted.get("origenes", {}).get(row["columna"], [])
        if not origins or any(rel not in manifest["archivos"] for rel in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 8: " + row["columna"])
    return config, folder, baseline, accepted, sources


def validar_sobre_base(rules, base_r7, root=ROOT):
    config, folder, baseline, accepted, sources = cargar(root)
    if baseline != base_r7:
        raise ValueError("Base de ronda 8 no coincide con ronda 7 validada")
    expected = copy.deepcopy(baseline)
    expected["vinculos_documentales_revisados"].extend(accepted["vinculos"])
    cols = [r["columna"] for r in rules["vinculos_documentales_revisados"]]
    if len(cols) != len(set(cols)):
        raise ValueError("Columnas duplicadas en ronda 8")
    # Doble aprobacion por vinculo en A y B, con SHA pinnado en ambas.
    sha_aceptadas = hashlib.sha256((folder / "aceptadas.json").read_bytes()).hexdigest()
    for audit_name in ("auditoria-a", "auditoria-b"):
        audit = json.loads((folder / "auditorias" / f"{audit_name}.json").read_text(encoding="utf-8"))
        if audit.get("aceptadas_sha256") != sha_aceptadas:
            raise ValueError("Ronda 8 exige aceptadas_sha256 pinnado en " + audit_name)
        ok = {x["id"] for x in audit["dictamenes"]
              if x["tipo"] == "vinculos" and x["dictamen"] == "aceptar"}
        for row in accepted["vinculos"]:
            if row["columna"] not in ok:
                raise ValueError("Ronda 8 sin aprobacion en " + audit_name + ": " + row["columna"])
    if rules != expected:
        raise ValueError("Ronda 8 permite solo la base y los 28 vinculos auditados exactos")
    return config, folder, baseline, accepted, sources


def construir(report, rules, base, root=ROOT):
    # Valida ademas la cadena R4->R5->R6->R7->R8 (R7 delega a R8 si existe
    # su config); no se reemplazan manifiestos anteriores.
    from integrar_ronda_4 import validar
    validar(rules, root)
    config, folder, baseline, accepted, sources = cargar(root)
    g = Graph()
    mex = Namespace(base + "vocab/")
    mappings = {v["columna"]: v for v in report["correspondencias"]
                if v["estado"] == "documental_revisada"}
    for row in accepted["vinculos"]:
        observed = mappings[row["columna"]]
        if observed["revision"] != row:
            raise ValueError("Vinculo R8 no materializado fielmente: " + row["columna"])
        for rel in accepted["origenes"][row["columna"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed["iri"]), PROV.wasDerivedFrom, entity))
    return g, dict(accepted.get("resumen", {}), manifiesto_sha256=config["manifiesto_sha256"]), sources
