"""Auditoria B independiente del payload R10 (E/payload/v001).

Solo lectura sobre el material auditado; escribe su resultado en esta carpeta.
No calcula ni escribe dictamenes por unidad/forma: eso lo decide el auditor.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
E = ROOT / "propuestas/ampliacion-post-r9/ejecucion-20261024"
P = E / "payload/v001"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon(value) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


out: dict = {"auditor": "b", "paquete": "payload/v001", "checks": {}}
checks = out["checks"]


def rec(name, ok, detail=None):
    checks[name] = {"ok": bool(ok), "detalle": detail}
    return ok


# ---------------------------------------------------------------- 1. bytes
sello = load(E / "sello-payload-previo.json")
mism = []
for rel, expected in sello["archivos"].items():
    actual = sha(P / rel)
    if actual != expected:
        mism.append({"archivo": rel, "declarado": expected, "real": actual})
rec("sha16_archivos", not mism, {"declarados": len(sello["archivos"]), "discrepancias": mism})

aceptadas_sha = sha(P / "aceptadas.json")
rec(
    "sha_aceptadas",
    aceptadas_sha == "df5705eaf6e0b8d8dcb0257a54a258264cda3e8adfe8655f87dfda90b9c2031c",
    aceptadas_sha,
)

origenes = load(E / "payload-origenes.json")
omism = []
for rel, expected in origenes["origenes"].items():
    actual = sha(ROOT / rel)
    if actual != expected:
        omism.append({"ruta": rel, "declarado": expected, "real": actual})
rec("sha_origenes", not omism, {"declarados": len(origenes["origenes"]), "discrepancias": omism})

# el payload declara consumir el sello S: comprobar que los artefactos que
# realmente importan (shapes.ttl, resultados) siguen siendo los sellados.
sello_s = load(E / "S-shacl/v001/sello.json")
s_art = sello_s["artefactos"]
s_bad = [k for k, v in s_art.items() if sha(E / "S-shacl/v001" / k) != v]
rec("sello_S_artefactos", not s_bad, {"artefactos": len(s_art), "rotos": s_bad})

# ---------------------------------------------------------------- 2. schema
acc = load(P / "aceptadas.json")
schema_errors = []
if acc.get("format_version") != 1:
    schema_errors.append("format_version != 1")
if acc.get("release") != "R10" or acc.get("release_base") != "R9":
    schema_errors.append("release/release_base")
unit_keys = {
    "id", "diccionario", "fila", "conjunto", "nombre", "unidad_literal", "unidad_qudt",
    "normativa_uri", "normativa_sha256", "huella_fila_diccionario", "fuente_url", "sujeto",
    "variable", "definicion_iri", "etiqueta", "comentario", "evidencia_normativa",
}
units = acc.get("unidades", [])
ids = [u.get("id") for u in units]
if ids != ["Q-U02", "Q-U03", "Q-U04", "Q-U05", "Q-U06"]:
    schema_errors.append(f"ids unidades {ids}")
for u in units:
    if set(u) != unit_keys:
        schema_errors.append(f"{u.get('id')}: claves {sorted(set(u) ^ unit_keys)}")
    for k, v in u.items():
        if k == "fila":
            if not isinstance(v, int) or isinstance(v, bool):
                schema_errors.append(f"{u['id']}.fila no entero")
        elif not isinstance(v, str) or not v:
            schema_errors.append(f"{u['id']}.{k} no string no vacio")
    if u["unidad_qudt"] != u["normativa_uri"]:
        schema_errors.append(f"{u['id']}: unidad_qudt != normativa_uri")
    if not u["unidad_qudt"].startswith("http://qudt.org/vocab/unit/"):
        schema_errors.append(f"{u['id']}: IRI QUDT no canonica")
    if not u["sujeto"].startswith("https://example.org/mex-ontologi/declaracion-unidad/r10/"):
        schema_errors.append(f"{u['id']}: sujeto fuera del espacio declarado")
    if u["variable"].rsplit("%2F", 1)[-1] != str(u["fila"]):
        schema_errors.append(f"{u['id']}: variable no termina en la fila")
    if u["definicion_iri"].rsplit("%2F", 1)[-1] != str(u["fila"]):
        schema_errors.append(f"{u['id']}: definicion no termina en la fila")
formas = acc.get("formas", [])
formas_ids = [f.get("id") for f in formas]
inst = acc.get("archivos_instalables", {})
rec("schema_aceptadas", not schema_errors, {"errores": schema_errors, "unidades": len(units), "formas": formas_ids})

# ---------------------------------------------------------------- 3. filas vs cobertura
cob = load(ROOT / "data/semantica/cobertura.json")
byh = {v.get("huella_fila_diccionario"): v for v in cob["variables"] if v.get("huella_fila_diccionario")}
corr = []
for u in units:
    fila = load(P / "filas" / f"{u['id']}.json")
    h = canon(fila)
    v = byh.get(u["huella_fila_diccionario"])
    item = {
        "id": u["id"],
        "huella_recalculada": h,
        "huella_igual": h == u["huella_fila_diccionario"],
        "literal_exacto": fila.get("Unidad de medida") == u["unidad_literal"],
        "nombre_exacto": fila.get("Nombre variable") == u["nombre"],
        "en_cobertura": bool(v),
    }
    if v:
        for campo in ("variable", "conjunto", "diccionario", "definicion_iri", "iri", "estado", "concepto"):
            item[campo + "_igual"] = v.get(campo) == u.get(campo) if campo != "iri" else v.get("iri") == u["variable"]
    corr.append(item)
rec("filas_vs_cobertura", all(
    i["huella_igual"] and i["literal_exacto"] and i["nombre_exacto"] and i["en_cobertura"]
    and all(i.get(k) for k in i if k.endswith("_igual"))
    for i in corr), corr)

# fila del payload == fila declarada por Q/v002 y la copia local existe
q = load(E / "Q-unidades/v002/casos.json")
qcasos = {c["id"]: c for c in q["casos"]}
qerr = []
for u in units:
    qc = qcasos.get(u["id"])
    if not qc:
        qerr.append(f"{u['id']} ausente en Q/v002")
        continue
    if qc["fila"] != load(P / "filas" / f"{u['id']}.json"):
        qerr.append(f"{u['id']}: fila distinta de Q/v002")
    if qc["huella_fila"] != u["huella_fila_diccionario"]:
        qerr.append(f"{u['id']}: huella distinta de Q/v002")
    if sha(ROOT / qc["copia"]["ruta"]) != qc["copia"]["sha256"]:
        qerr.append(f"{u['id']}: copia de fuente alterada")
rec("filas_vs_Q_v002", not qerr, {"errores": qerr})

# ---------------------------------------------------------------- 4. normativa
nerr = []
for u in units:
    n = P / "normativa" / f"{u['id']}.txt"
    h = sha(n)
    text = n.read_text(encoding="utf-8")
    if h != u["normativa_sha256"]:
        nerr.append(f"{u['id']}: sha normativa {h}")
    if "QUDT 3.5.3" not in text:
        nerr.append(f"{u['id']}: sin version QUDT 3.5.3")
    if u["unidad_qudt"] not in text:
        nerr.append(f"{u['id']}: sin IRI exacta")
    if "http://qudt.org/3.5.3/vocab/unit" not in text:
        nerr.append(f"{u['id']}: sin isDefinedBy 3.5.3")
rec("normativa", not nerr, {"errores": nerr})

# cobertura de la evidencia normativa contra W/v002
w = load(E / "W-estandares/v002/entrega.json")
wmap = {r["caso"]: r for r in w["resultados"]}
werr = []
for u in units:
    r = wmap.get(u["id"])
    if not r:
        werr.append(f"{u['id']} sin verificacion W")
    elif r["sujeto_rdf"] != u["unidad_qudt"]:
        werr.append(f"{u['id']}: W verifica {r['sujeto_rdf']} y el payload declara {u['unidad_qudt']}")
    elif r["estado"] != "verificado" or r.get("version") != "3.5.3":
        werr.append(f"{u['id']}: W estado/version {r['estado']} {r.get('version')}")
rec("unidad_qudt_vs_W", not werr, {"errores": werr})

# ---------------------------------------------------------------- 5. datos/unidades.ttl
txt = (P / "datos/unidades.ttl").read_text(encoding="utf-8")
triples = []
for block in re.split(r"\n\s*\n", txt):
    block = block.strip()
    if not block or block.startswith("@"):
        continue
    m = re.match(r"<([^>]+)>\s+a\s+mex:UnidadDeclarada\s*;(.*)", block, re.S)
    if not m:
        continue
    subj = m.group(1)
    for stmt in re.split(r";", m.group(2)):
        stmt = " ".join(stmt.split())
        if not stmt:
            continue
        if stmt.startswith("rdfs:label"):
            triples.append((subj, "rdfs:label", stmt.split('"', 1)[1].rsplit('"', 1)[0]))
        elif stmt.startswith("rdfs:comment"):
            triples.append((subj, "rdfs:comment", stmt.split('"', 1)[1].rsplit('"', 1)[0]))
        elif stmt.startswith("mex:evidenciaNormativa"):
            triples.append((subj, "mex:evidenciaNormativa", stmt.split('"', 1)[1].rsplit('"', 1)[0]))
        elif stmt.startswith("prov:wasDerivedFrom"):
            for o in re.findall(r"<([^>]+)>", stmt):
                triples.append((subj, "prov:wasDerivedFrom", o))
        elif stmt.startswith("mex:"):
            p = stmt.split()[0][4:]
            q = re.search(r'"([^"]*)"|<([^>]+)>', stmt)
            triples.append((subj, "mex:" + p, q.group(1) if q.group(1) is not None else q.group(2)))
        else:
            triples.append((subj, "?", stmt))

derr = []
expected = set()
for u in units:
    s = u["sujeto"]
    expected |= {
        (s, "rdf:type", "mex:UnidadDeclarada"),
        (s, "rdfs:label", u["etiqueta"]),
        (s, "rdfs:comment", u["comentario"]),
        (s, "prov:wasDerivedFrom", u["fuente_url"]),
        (s, "prov:wasDerivedFrom", u["normativa_uri"]),
        (s, "mex:conjuntoFuente", u["conjunto"]),
        (s, "mex:definicionFuente", u["definicion_iri"]),
        (s, "mex:diccionarioFuente", u["diccionario"]),
        (s, "mex:evidenciaNormativa", u["evidencia_normativa"]),
        (s, "mex:unidadLiteral", u["unidad_literal"]),
        (s, "mex:unidadQudt", u["unidad_qudt"]),
        (s, "mex:variableDocumentada", u["variable"]),
    }
actual = set()
for subj, pred, obj in triples:
    actual.add((subj, "rdf:type", "mex:UnidadDeclarada") if pred == "?" else (subj, pred, obj))
if actual != expected:
    derr.append({"extra": sorted(map(str, actual - expected)), "faltan": sorted(map(str, expected - actual))})
subs = {t[0] for t in triples}
if subs != {u["sujeto"] for u in units}:
    derr.append({"sujetos": sorted(subs)})
rec("datos_60_triples", len(actual) == 60 and not derr, {"triples": len(actual), "por_sujeto": {s: sum(1 for t in actual if t[0] == s) for s in subs}, "errores": derr})

# ---------------------------------------------------------------- 6. shapes
shapes_txt = (P / "shapes/adicionales.ttl").read_text(encoding="utf-8")
decl_ids = re.findall(r"^shape:(\w+)\s+a\s+sh:NodeShape", shapes_txt, re.M)
rec("shapes_6_ids", decl_ids == formas_ids,
    {"declaradas": decl_ids, "en_aceptadas": formas_ids,
     "sha": sha(P / "shapes/adicionales.ttl"),
     "sha_sellado_S": s_art["shapes.ttl"],
     "sha_declarado": inst.get("shapes"),
     "igual_a_sellado": sha(P / "shapes/adicionales.ttl") == s_art["shapes.ttl"]})
rec("datos_sha_declarado", sha(P / "datos/unidades.ttl") == inst.get("datos"),
    {"real": sha(P / "datos/unidades.ttl"), "declarado": inst.get("datos")})

# ---------------------------------------------------------------- 7. invariantes
inv = {}
inv["config_sha"] = sha(ROOT / "config.toml")
inv["config_igual_payload"] = inv["config_sha"] == sha(P / "config-iri-base.toml")
inv["config_igual_sello"] = inv["config_sha"] == sello["archivos"]["config-iri-base.toml"]
inv["base_semantica_igual_vivo"] = sha(P / "base-semantica.json") == sha(ROOT / "ontologia/semantica.json")
inv["cobertura_r9_igual_vivo"] = sha(P / "cobertura-r9.json") == sha(ROOT / "data/semantica/cobertura.json")
base = load(E / "base.json")
bad130 = [rel for rel, h in base["sha256"].items() if not (ROOT / rel).exists() or sha(ROOT / rel) != h]
inv["base130_rotos"] = bad130
resumen = load(P / "cobertura-r9.json")["resumen"]
esperado = {
    "definiciones_con_nombre_examinadas": 1563, "filas_sin_nombre": 7,
    "variables_materializadas": 1442, "columnas_totales_examinadas": 5523,
    "columnas_con_correspondencia": 4523, "conceptos_compartidos": 1106,
    "referencias_catalogo_sin_resolver": 1,
    "sistemas_identificadores_recuperados": 1, "condiciones_conexion": 6,
    "referencias_catalogo_con_recurso_identificado": 16,
    "estados_variables": {"respaldada_por_definicion": 1423, "fuera_del_nucleo_actual": 124,
                          "candidata_sin_definicion_suficiente": 16},
    "estados_correspondencias": {"documental_revisada": 4506, "candidata_por_nombre": 17},
}
inv["resumen_r9_exacto"] = resumen == esperado
inv["resumen_vivo_exacto"] = cob["resumen"] == esperado
inv["nucleo_sha_vivo"] = sha(ROOT / "data/semantica/nucleo.ttl")
manifiestos = sorted(rel for rel in base["sha256"] if "manifiesto" in rel)
inv["manifiestos_declarados"] = len(manifiestos)
inv["rondas_1_9_presentes"] = all((ROOT / f"data/integracion-ronda-{n}").exists() for n in range(2, 10))
rec("invariantes", not bad130 and inv["resumen_r9_exacto"] and inv["resumen_vivo_exacto"]
    and inv["base_semantica_igual_vivo"] and inv["cobertura_r9_igual_vivo"]
    and inv["config_igual_payload"] and inv["config_igual_sello"], inv)

# ---------------------------------------------------------------- 8. alcance
alcance = {}
alcance["Q_U01_en_aceptadas"] = any(u["id"] == "Q-U01" for u in units)
alcance["toneladas_en_datos"] = "Toneladas" in txt or "TON_Metric" in txt
alcance["hm3_en_datos"] = "hm3" in txt.lower() or "HectoM3" in txt
alcance["objetos_prohibidos"] = [w for w in ("QuantityValue", "conversionMultiplier", "factorConversion") if w in txt]
alcance["modelo_en_manifiesto"] = "modelo" in inst
alcance["archivos_en_payload"] = sorted(str(p.relative_to(P)).replace("\\", "/") for p in P.rglob("*") if p.is_file())
alcance["fuera_del_manifiesto"] = sorted(set(alcance["archivos_en_payload"]) - set(sello["archivos"]))
alcance["faltan_del_manifiesto"] = sorted(set(sello["archivos"]) - set(alcance["archivos_en_payload"]))
alcance["formas_declaradas_sin_fichero_propio"] = not (P / "shapes/adicionales.ttl").exists()
rec("alcance", not alcance["Q_U01_en_aceptadas"] and not alcance["toneladas_en_datos"]
    and not alcance["hm3_en_datos"] and not alcance["objetos_prohibidos"]
    and not alcance["fuera_del_manifiesto"] and not alcance["faltan_del_manifiesto"], alcance)

# ---------------------------------------------------------------- 9. contrato I (no aprobado)
ic = E / "I-codigo/v001"
contrato = load(ic / "contrato.json")
script = ic / "scripts/integrar_ronda_10.py"
src = script.read_text(encoding="utf-8")
mat = {
    "obligatorios_incluyen_auditorias": "auditorias/a.json" in src and "auditorias/b.json" in src,
    "exige_sha_aceptadas": "audit.get('aceptadas_sha256')" in src,
    "exige_dictamen_por_id": "set(seen) != ids" in src,
    "provgate_presente": "PROV" in src,
    "tests": sorted(str(p.relative_to(ic)).replace("\\", "/") for p in ic.rglob("test*")),
    "produce_cambios": any(k in src for k in ("write_text", "shutil.copy", "open(..., 'w'")),
}
rec("contrato_I_material", True, {"revisado": "no aprobado", **mat, "nota": "PROVgate sin resolver: no se aprueba codigo"})

out["resultado_global"] = "ok" if all(v["ok"] for v in checks.values()) else "hallazgos"
Path(__file__).resolve().parents[1].joinpath("auditoria-raw.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out["resultado_global"]))
for k, v in checks.items():
    print(("OK  " if v["ok"] else "BAD "), k)
