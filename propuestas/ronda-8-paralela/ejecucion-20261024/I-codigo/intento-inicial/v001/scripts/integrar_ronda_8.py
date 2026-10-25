"""Extension R8: solo vinculos sobre el universo de 45 candidatas R7 con respaldo previo.

Copia preparada en staging (I-codigo/v001), NO instalada. Al instalar va a
`scripts/integrar_ronda_8.py` junto con `ontologia/revision-ronda-8.json` y
`data/integracion-ronda-8/`.

Controles (estructurales; sin filtro textual de contenido, sin NLP):
- Esquema cerrado de claves (REGLA_KEYS/VINCULO_KEYS): sin campos para
  equivalencias, vigencias, joins ni identidad de catalogos. `construir()`
  emite solo PROV.wasDerivedFrom + sha256Evidencia sobre nodos del core.
- Cada regla: una unica IRI de definicion no respaldada antes, un unico
  `nombres` y una unica `descripciones` exactos, huella de fila,
  evidencia/criterio/alcance no vacios, limites escritos. El subconjunto
  aprobado (parcial o vacio) lo fija `aceptadas.json`; nada se asume aprobado.
  R8 probablemente trae 0 reglas: el codigo lo admite sin asumirlo.
- Cada vinculo: columna del universo pinnado de 45 candidatas R7,
  `definicion_iri` respaldada por una regla R8 del mismo lote o ya respaldada
  en la base R7, y `concepto` identico al de su regla de respaldo.
- Conceptos: referenciados existen en base o lote; sin conceptos nuevos
  sobrantes (todo nuevo lo usa >=1 regla); broader existe; clave nueva
  obligatoria (reutilizar si un concepto existente representa el sentido).
- Procedencia y aprobacion: manifiesto nuevo con SHA de cada archivo e
  insumo, origenes pinnados, doble `aceptar` A+B por regla y por vinculo con
  `aceptadas_sha256` pinnado en AMBAS auditorias, base R7 exacta
  (R7base+R7aceptadas), unicidad de ids/definiciones/columnas, exactitud final.
- No altera el contrato de estados del nucleo ni relaja
  `respaldada_por_definicion` (lo verifica `construir` y el core).
"""

import copy
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from construir_catalogo import ROOT, PROV

# Universo maximo de 45 candidatas R7: 28 nuevas SINAC (M1+M2) + 17 anteriores
# (M3). Fijado desde reports/ronda-7.json + asignacion M3; solo el subconjunto
# aprobado por A/B se promueve.
UNIVERSO_45 = frozenset([
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F100",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F103",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F105",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F106",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F31",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F32",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F34",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F37",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F39",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F43",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F45",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F57",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F58",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F59",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F61",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F63",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F65",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F67",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F69",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F71",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F72",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F74",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F76",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F77",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F79",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F84",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F87",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F89",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F97",
    "https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F99",
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


def _texto_unico(valor):
    return isinstance(valor, list) and len(valor) == 1 \
        and isinstance(valor[0], str) and valor[0].strip()


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
    if (not isinstance(manifest.get("archivos"), dict)
            or not isinstance(manifest.get("insumos"), dict)
            or not required.issubset(manifest["archivos"])):
        raise ValueError("Manifiesto de ronda 8 incompleto")
    for category, base in [("archivos", folder), ("insumos", root)]:
        for rel, h in manifest[category].items():
            p = dentro(base, rel)
            if sha(p) != h:
                raise ValueError("Evidencia de ronda 8 modificada: " + rel)
            sources["ronda_8_" + category + "_" + rel] = p
    read = lambda rel: json.loads((folder / rel).read_text(encoding="utf-8"))
    accepted = read("aceptadas.json")
    baseline = read("base-semantica.json")
    # Cobertura R7 congelada: fija el universo de 45 candidatas y los
    # pre-estados de cada variable (el reporte vivo ya trae el delta).
    cob7 = read("cobertura-r7.json")
    res7 = cob7.get("resumen", {})
    if res7.get("estados_correspondencias", {}).get("documental_revisada") != 4478 \
            or res7.get("estados_correspondencias", {}).get("candidata_por_nombre") != 45 \
            or res7.get("estados_variables", {}).get("respaldada_por_definicion") != 1423 \
            or res7.get("estados_variables", {}).get("candidata_sin_definicion_suficiente") != 16 \
            or res7.get("estados_variables", {}).get("fuera_del_nucleo_actual") != 124 \
            or res7.get("conceptos_compartidos") != 1106 \
            or res7.get("columnas_con_correspondencia") != 4523:
        raise ValueError("cobertura-r7.json no fija el pin R7 4478/45/1423/16/124/1106/4523")
    pre_est = {v.get("definicion_iri"): v.get("estado")
               for v in cob7.get("variables", []) if v.get("definicion_iri")}
    if {m["columna"] for m in cob7.get("correspondencias", [])
            if m.get("estado") == "candidata_por_nombre"} != UNIVERSO_45:
        raise ValueError("cobertura-r7.json sin el universo de 45 candidatas exacto")
    if not isinstance(accepted.get("reglas"), list) \
            or not isinstance(accepted.get("vinculos"), list) \
            or not isinstance(accepted.get("conceptos"), dict):
        raise ValueError("aceptadas.json de ronda 8 con forma inválida")
    # Respaldo previo R7: definiciones ya respaldadas en la base R8 (= R7
    # validada). Un vínculo nuevo exige variable ya respaldada R7 o regla R8.
    respaldadas_r7 = {d for r in baseline.get("reglas_descripcion_exacta", [])
                      for d in r.get("definiciones", [])}
    respaldadas_r8 = set()
    conceptos_base = set(baseline.get("conceptos", {}))
    for row in accepted["reglas"]:
        if set(row) - REGLA_KEYS:
            raise ValueError("Regla R8 con claves no admitidas: " + row.get("id", "?"))
        if not (isinstance(row.get("definiciones"), list)
                and len(row["definiciones"]) == 1
                and isinstance(row["definiciones"][0], str)):
            raise ValueError("Regla R8 exige una única definición: " + row.get("id", "?"))
        if row["definiciones"][0] in respaldadas_r7:
            raise ValueError("Regla R8 re-respalda definición R7: " + row.get("id", "?"))
        # Nuevo vínculo o regla solo desde pendientes R7 (candidatas o fuera);
        # el reparto candidata/fuera de cada regla lo fija cobertura-r7 y la
        # auditoría A/B, no el nombre.
        if pre_est.get(row["definiciones"][0], "respaldada_por_definicion") == "respaldada_por_definicion":
            raise ValueError("Regla R8 fuera de pendientes R7: " + row.get("id", "?"))
        if not _texto_unico(row.get("nombres")) \
                or not _texto_unico(row.get("descripciones")):
            raise ValueError("Regla R8 exige un único nombre y descripción exactos: " + row.get("id", "?"))
        if not row.get("huella_fila_diccionario") \
                or not row.get("representacion") or not row.get("concepto"):
            raise ValueError("Regla R8 incompleta: " + row.get("id", "?"))
        if not isinstance(row.get("limites"), list) or not row["limites"] \
                or not row.get("criterio") or not row.get("alcance") \
                or not row.get("evidencia"):
            raise ValueError("Regla R8 sin evidencia/criterio/alcance/límites fijados: " + row.get("id", "?"))
        if row["concepto"] not in conceptos_base \
                and row["concepto"] not in accepted["conceptos"]:
            raise ValueError("Regla R8 con concepto inexistente en base y lote: " + row.get("id", "?"))
        origins = accepted.get("origenes", {}).get(row["id"], [])
        if not origins or any(rel not in manifest["archivos"] for rel in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 8: " + row["id"])
        respaldadas_r8.add(row["definiciones"][0])
    conceptos_reglas = {r["concepto"] for r in accepted["reglas"]}
    for row in accepted["vinculos"]:
        if set(row) - VINCULO_KEYS:
            raise ValueError("Vínculo R8 con claves no admitidas: " + row.get("columna", "?"))
        if row.get("columna") not in UNIVERSO_45:
            raise ValueError("Vínculo R8 fuera del universo de 45: " + row.get("columna", "?"))
        respaldo = [r for r in accepted["reglas"]
                    if r["definiciones"][0] == row.get("definicion_iri")]
        if respaldo:
            if len(respaldo) != 1 or row.get("concepto") != respaldo[0]["concepto"]:
                raise ValueError("Vínculo R8 sin significado respaldado del lote: " + row.get("columna", "?"))
        elif row.get("definicion_iri") not in respaldadas_r7:
            raise ValueError("Vínculo R8 sin variable respaldada R7 ni regla R8: " + row.get("columna", "?"))
        else:
            # Respaldo R7: el concepto debe coincidir con la regla que lo
            # respalda en la base (misma definición).
            base_reglas = [r for r in baseline.get("reglas_descripcion_exacta", [])
                           if row.get("definicion_iri") in r.get("definiciones", [])]
            if len(base_reglas) != 1 or row.get("concepto") != base_reglas[0]["concepto"]:
                raise ValueError("Vínculo R8 con concepto distinto a su respaldo R7: " + row.get("columna", "?"))
        for k in ("huella_esquema", "huella_fila_diccionario", "descripcion",
                  "criterio", "diccionario", "recurso", "campo"):
            if not row.get(k):
                raise ValueError("Vínculo R8 incompleto (" + k + "): " + row.get("columna", "?"))
        if row["concepto"] not in conceptos_base \
                and row["concepto"] not in accepted["conceptos"]:
            raise ValueError("Vínculo R8 con concepto inexistente en base y lote: " + row.get("columna", "?"))
        origins = accepted.get("origenes", {}).get(row["columna"], [])
        if not origins or any(rel not in manifest["archivos"] for rel in origins):
            raise ValueError("Origen no fijado por manifiesto de ronda 8: " + row["columna"])
    for k, v in accepted["conceptos"].items():
        if not isinstance(v, list) or len(v) != 3 or not v[0] or not v[1]:
            raise ValueError("Concepto R8 con forma inválida: " + k)
        if v[2] is not None and v[2] not in conceptos_base \
                and v[2] not in accepted["conceptos"]:
            raise ValueError("Concepto R8 con broader inexistente: " + k)
    # Sin conceptos nuevos sobrantes: todo concepto del lote lo usa >=1 regla.
    sobrantes = set(accepted["conceptos"]) - conceptos_reglas
    if sobrantes:
        raise ValueError("Conceptos R8 sin regla que los use: " + sorted(sobrantes)[0])
    return config, folder, baseline, accepted, sources


def validar_sobre_base(rules, base_r7, root=ROOT):
    config, folder, baseline, accepted, sources = cargar(root)
    if baseline != base_r7:
        raise ValueError("Base de ronda 8 no coincide con ronda 7 validada")
    expected = copy.deepcopy(baseline)
    expected["reglas_descripcion_exacta"].extend(accepted["reglas"])
    expected["vinculos_documentales_revisados"].extend(accepted["vinculos"])
    for k, v in accepted["conceptos"].items():
        # Nada de deduplicar/sobrescribir conceptos previos silenciosamente.
        if k in expected["conceptos"]:
            raise ValueError("Ronda 8 exige concepto nuevo, clave ya existente: " + k)
        expected["conceptos"][k] = v
    for field, key in [("reglas_descripcion_exacta", "id"),
                       ("vinculos_documentales_revisados", "columna")]:
        ids = [r[key] for r in rules[field]]
        if len(ids) != len(set(ids)):
            raise ValueError("Reglas o columnas duplicadas en ronda 8")
    defs = [d for r in rules["reglas_descripcion_exacta"] for d in r.get("definiciones", [])]
    if len(defs) != len(set(defs)):
        raise ValueError("Definiciones duplicadas en ronda 8")
    # Doble aprobación por regla y por vínculo: aceptar en A y en B, con el
    # SHA del aceptadas.json revisado pinnado en ambas auditorías.
    sha_aceptadas = hashlib.sha256((folder / "aceptadas.json").read_bytes()).hexdigest()
    for audit_name in ("auditoria-a", "auditoria-b"):
        audit = json.loads((folder / "auditorias" / f"{audit_name}.json").read_text(encoding="utf-8"))
        if audit.get("aceptadas_sha256") != sha_aceptadas:
            raise ValueError("Ronda 8 exige aceptadas_sha256 pinnado en " + audit_name + " antes de aceptar IDs")
        ok_reglas = {x["id"] for x in audit["dictamenes"]
                     if x["tipo"] == "reglas" and x["dictamen"] == "aceptar"}
        ok_vinc = {x["id"] for x in audit["dictamenes"]
                   if x["tipo"] == "vinculos" and x["dictamen"] == "aceptar"}
        for row in accepted["reglas"]:
            if row["id"] not in ok_reglas:
                raise ValueError("Ronda 8 sin aprobación en " + audit_name + ": " + row["id"])
        for row in accepted["vinculos"]:
            if row["columna"] not in ok_vinc:
                raise ValueError("Ronda 8 sin aprobación en " + audit_name + ": " + row["columna"])
    if rules != expected:
        raise ValueError("Ronda 8 permite solo la base y las adiciones auditadas exactas")
    return config, folder, baseline, accepted, sources


def verificar_continuidad_r7_r8(r7base, r7accepted, r8base, r8accepted):
    """Continuidad R7->R8: la base R8 es exactamente R7base+R7aceptadas.

    Devuelve (n_reglas, n_vinculos, n_conceptos) del delta R8 aprobado, sin
    hardcodear totales: los adaptadores derivan el expected de aquí.
    """
    if r8base["reglas_descripcion_exacta"] != r7base["reglas_descripcion_exacta"] + r7accepted["reglas"] \
            or r8base["vinculos_documentales_revisados"] != r7base["vinculos_documentales_revisados"] + r7accepted["vinculos"]:
        raise ValueError("Base R8 discontinua respecto a cadena R7")
    for k, v in r7base["conceptos"].items():
        if r8base["conceptos"].get(k) != v:
            raise ValueError("Concepto base alterado en cadena R8: " + k)
    for k, v in r7accepted["conceptos"].items():
        if r8base["conceptos"].get(k) != v:
            raise ValueError("Concepto R7 ausente en base R8: " + k)
    return (len(r8accepted["reglas"]), len(r8accepted["vinculos"]),
            len(r8accepted["conceptos"]))


def _pre_estados(r8folder):
    """Pre-estados R7 por definición desde cobertura-r7.json (ya pinnada)."""
    cob7 = json.loads((r8folder / "cobertura-r7.json").read_text(encoding="utf-8"))
    return {v.get("definicion_iri"): v.get("estado")
            for v in cob7.get("variables", []) if v.get("definicion_iri")}


def proyectar_semantica_r7(semantic, accepted, pre_est):
    """Proyecta el reporte vivo R8 a su equivalente R7 para asserts históricos.

    Revierte el delta aprobado (vínculos promovidos -> candidatas con
    revision None, reglas -> su pre-estado R7 real, conceptos restados) sin
    tocar el reporte vivo. Los adaptadores R1/R2 conservan así todas sus
    validaciones R7 intactas y aplican después el delta R8 real. No usa
    observados como expected: todo sale del delta aprobado por A/B más los
    pre-estados pinnados.
    """
    proj = copy.deepcopy(semantic)
    vinc_cols = {v["columna"] for v in accepted.get("vinculos", [])}
    regla_defs = {r["definiciones"][0]: r for r in accepted.get("reglas", [])}
    for m in proj.get("correspondencias", []):
        if m["columna"] in vinc_cols:
            m["estado"] = "candidata_por_nombre"
            m["revision"] = None
    for v in proj.get("variables", []):
        # ponytail: la demotion restaura el pre-estado pinnado exacto; si una
        # regla R8 viniera de fuera_del_nucleo, su bucket se restaura igual.
        if v.get("definicion_iri") in regla_defs:
            v["estado"] = pre_est.get(v["definicion_iri"],
                                      "candidata_sin_definicion_suficiente")
            v.pop("regla", None)
            v.pop("concepto", None)
    res = proj.get("resumen", {})
    est_var = res.get("estados_variables", {})
    est_cor = res.get("estados_correspondencias", {})
    n_vinc, n_reg = len(vinc_cols), len(regla_defs)
    n_con = len(accepted.get("conceptos", {}))
    if "documental_revisada" in est_cor:
        est_cor["documental_revisada"] -= n_vinc
    est_cor["candidata_por_nombre"] = est_cor.get("candidata_por_nombre", 0) + n_vinc
    if n_reg:
        de_cand = sum(1 for d in regla_defs
                      if pre_est.get(d) == "candidata_sin_definicion_suficiente")
        est_var["respaldada_por_definicion"] = est_var.get("respaldada_por_definicion", 0) - n_reg
        est_var["candidata_sin_definicion_suficiente"] = \
            est_var.get("candidata_sin_definicion_suficiente", 0) + de_cand
        est_var["fuera_del_nucleo_actual"] = \
            est_var.get("fuera_del_nucleo_actual", 0) + (n_reg - de_cand)
    if "conceptos_compartidos" in res:
        res["conceptos_compartidos"] -= n_con
    return proj


def preparar_proyeccion_r7(semantic, r7base, r7accepted, r8base, r8accepted,
                           r8folder):
    """Continuidad R7->R8 + proyección del reporte vivo a equivalente R7.

    Uso en adaptadores R1/R2 (una sola llamada, sin duplicar bloques R7):
        semantic_vivo = semantic
        semantic, delta8 = preparar_proyeccion_r7(...)
        ... bloque histórico R7 intacto sobre `semantic` ...
        ... delta R8 derivado sobre `semantic_vivo` con delta8 ...
    `delta8` trae n_reglas/n_vinculos/n_conceptos/de_candidatas, todo derivado
    del lote aprobado por A/B (nada observado, nada hardcodeado).
    """
    counts = verificar_continuidad_r7_r8(r7base, r7accepted, r8base, r8accepted)
    pre_est = _pre_estados(r8folder)
    proj = proyectar_semantica_r7(semantic, r8accepted, pre_est)
    n_reglas, n_vinculos, n_conceptos = counts
    delta = {"n_reglas": n_reglas, "n_vinculos": n_vinculos,
             "n_conceptos": n_conceptos,
             "de_candidatas": sum(1 for r in r8accepted.get("reglas", [])
                                  if pre_est.get(r["definiciones"][0])
                                  == "candidata_sin_definicion_suficiente")}
    return proj, delta


def construir(report, rules, base, root=ROOT):
    # Valida además toda la cadena histórica R4→R5→R6→R7→R8. R4 invoca
    # validar_sobre_base (R5 delega a R6; R6 delega a R7; R7 delega a R8 si
    # existe su config); no se reemplazan manifiestos anteriores.
    from integrar_ronda_4 import validar
    validar(rules, root)
    config, folder, baseline, accepted, sources = cargar(root)
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
            raise ValueError("Regla R8 no materializada fielmente: " + row["id"])
        for rel in accepted["origenes"][row["id"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed["iri"]), PROV.wasDerivedFrom, entity))
    for row in accepted["vinculos"]:
        observed = mappings[row["columna"]]
        if observed["revision"] != row:
            raise ValueError("Vínculo R8 no materializado fielmente: " + row["columna"])
        for rel in accepted["origenes"][row["columna"]]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed["iri"]), PROV.wasDerivedFrom, entity))
    return g, dict(accepted["resumen"], manifiesto_sha256=config["manifiesto_sha256"]), sources
