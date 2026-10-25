"""Genera v002 P4-shacl-versionado (plan-tras-r8/ejecucion-20261024).
v001 queda sellada: solo se LEE (forma y fixtures exactos, SHA por codigo).
Valida la forma propuesta exacta de v001 contra el snapshot completo R8
data/catalogo/studio-live.ttl en almacen TEMPORAL AISLADO (sin mutar Studio),
mas re-ejecucion de las 4 fixtures. Solo escribe en P4-shacl-versionado/v002/.
"""
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:\Users\marti\Documents\MEX-Ontologi")
P4 = REPO / "propuestas/plan-tras-r8/ejecucion-20261024/P4-shacl-versionado"
V1 = P4 / "v001"
OUT = P4 / "v002"
OUT.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(REPO / "scripts"))
from construir_catalogo import motor


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


VOC = "https://example.org/mex-ontologi/vocab/"
SHAPE_V1 = V1 / "propuesta/shape-exclusion-significado.ttl"
SNAP = REPO / "data/catalogo/studio-live.ttl"
EXE = REPO / "tools/open-ontologies.exe"
H_SHAPE = sha256(SHAPE_V1)
H_SNAP = sha256(SNAP)
H_EXE = sha256(EXE)
print("H_SHAPE", H_SHAPE)
print("H_SNAP ", H_SNAP)

FIXTURES = ["fixture-neither.ttl", "fixture-doc.ttl", "fixture-cand.ttl", "fixture-both.ttl"]
H_FIX = {n: sha256(V1 / "fixtures" / n) for n in FIXTURES}
ESPERADO = {"fixture-neither.ttl": True, "fixture-doc.ttl": True,
            "fixture-cand.ttl": True, "fixture-both.ttl": False}

# --- 1. Snapshot R8 en store temporal aislado ---
store = Path(tempfile.mkdtemp(prefix="p4v002-snap-"))
cmds = []
r = motor(["validate", str(SNAP)], store); cmds.append(["validate", str(SNAP)])
assert r.get("ok") is True, r
r = motor(["load", str(SNAP)], store); cmds.append(["load", str(SNAP)])
stats = motor(["stats"], store); cmds.append(["stats"])
r = motor(["shacl", str(SHAPE_V1)], store); cmds.append(["shacl", str(SHAPE_V1)])
assert not r.get("skipped_constraints"), r
shacl_snapshot = {"conforms": r.get("conforms"), "violation_count": r.get("violation_count"),
                  "focus_nodes": r.get("focus_nodes"), "violations": r.get("violations", [])}


def q(sparql):
    cmds.append(["query", sparql[:80] + "..."])
    return motor(["query", sparql], store)


def count(sparql):
    out = q(sparql)
    rows = out.get("rows", out.get("results", []))
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        for k in ("n", "c", "count"):
            if k in rows[0]:
                return int(str(rows[0][k]).split("^^")[0].strip().strip('"'))
    return out


Q_VAR = f"SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE {{ ?v a <{VOC}VariableDocumentada> }}"
Q_DOC = f"SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE {{ ?v a <{VOC}VariableDocumentada> ; <{VOC}significadoDocumentado> ?d }}"
Q_CAND = f"SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE {{ ?v a <{VOC}VariableDocumentada> ; <{VOC}significadoCandidato> ?c }}"
Q_BOTH = f"SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE {{ ?v a <{VOC}VariableDocumentada> ; <{VOC}significadoDocumentado> ?d ; <{VOC}significadoCandidato> ?c }}"
Q_NEITHER = f"SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE {{ ?v a <{VOC}VariableDocumentada> . FILTER NOT EXISTS {{ ?v <{VOC}significadoDocumentado>|<{VOC}significadoCandidato> ?x }} }}"
n_var, n_doc, n_cand, n_both, n_neither = (count(x) for x in (Q_VAR, Q_DOC, Q_CAND, Q_BOTH, Q_NEITHER))

Q_LIST = f"SELECT ?v ?d ?c WHERE {{ ?v a <{VOC}VariableDocumentada> ; <{VOC}significadoDocumentado> ?d ; <{VOC}significadoCandidato> ?c }} ORDER BY ?v LIMIT 50"
lst = q(Q_LIST)
ambos = lst.get("rows", lst.get("results", []))
# Tipos/alcance: sujetos con candidato que NO son VariableDocumentada (fuera de alcance de la forma)
Q_FUERA = f"SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE {{ ?s <{VOC}significadoCandidato> ?c . FILTER NOT EXISTS {{ ?s a <{VOC}VariableDocumentada> }} }}"
n_cand_fuera = count(Q_FUERA)

# --- 2. Fixtures exactas de v001, re-ejecutadas en stores aislados ---
res_fixtures = []
for n in FIXTURES:
    fp = V1 / "fixtures" / n
    st = Path(tempfile.mkdtemp(prefix="p4v002-fix-"))
    motor(["validate", str(fp)], st)
    motor(["load", str(fp)], st)
    rr = motor(["shacl", str(SHAPE_V1)], st)
    assert not rr.get("skipped_constraints"), rr
    assert rr.get("conforms") is ESPERADO[n], (n, rr)
    res_fixtures.append({"fixture": f"v001/fixtures/{n}", "sha256": H_FIX[n],
                         "esperado_conforms": ESPERADO[n], "conforms": rr.get("conforms"),
                         "violation_count": rr.get("violation_count")})

entrega = {
    "rol": "P4-shacl-versionado",
    "version": "v002",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "base": "reports/ronda-8.json",
    "estado": "propuesta_para_auditar",
    "casos": [],
    "forma_exacta_v001": {"ruta": "propuestas/plan-tras-r8/ejecucion-20261024/P4-shacl-versionado/v001/propuesta/shape-exclusion-significado.ttl",
                          "sha256": H_SHAPE},
    "snapshot": {"ruta": "data/catalogo/studio-live.ttl", "sha256": H_SNAP,
                 "store": "temporal aislado (sin mutar Studio)", "stats": stats},
    "motor": {"exe": "tools/open-ontologies.exe", "exe_sha256": H_EXE,
              "version_flag": "el exe no acepta --version (error 'unexpected argument'); version registrada por SHA-256 del binario",
              "operador": "sh:sparql (determinado en la instalacion probada)",
              "nota_operadores": "sh:not/xone no detectaron evaluacion en la instalacion probada (conforms null + skipped_constraints); no se afirma soporte universal, solo lo observado con este binario",
              "comandos": cmds},
    "resultado_snapshot": dict(shacl_snapshot, variables={
        "VariableDocumentada_total": n_var, "con_documentado": n_doc,
        "con_candidato": n_cand, "con_ambos": n_both, "sin_ninguno": n_neither,
        "candidato_fuera_de_alcance": n_cand_fuera},
        sujetos_con_ambos=ambos if isinstance(ambos, list) else ambos),
    "conflictos_extras_manuales": ("NINGUNO: 0 variables con ambos; se informa sin eliminar nada"
                                   if n_both == 0 else f"{n_both} variables con ambos (listadas, NO eliminadas)"),
    "fixtures": res_fixtures,
    "versionado": {"format_version": "1 (esquema de esta entrega; sube solo si cambia el esquema)",
                   "release": "R8 vigente (cambia solo con ronda aprobada; R9 cuando se integre lo aprobado)",
                   "regla": "manifiestos R1-R8 intactos; solo append/snapshots futuros; sin migraciones historicas"},
    "limites": [
        "v001 sellada: solo lectura; esta entrega vive en v002 y no modifica produccion, shapes centrales, manifiestos, grafo ni Studio.",
        "Gemma excluido; sin contactos externos; sin navegador (reservado a W); sin peticiones-web.json.",
        "sh:not/xone: afirmacion acotada a la instalacion probada, no universal.",
        "Conflictos, si los hubiera, se informan y no se eliminan.",
    ],
    "condiciones_de_aceptacion": [
        "La forma exacta de v001 (mismo SHA) conforma sobre el snapshot R8.",
        "Ninguna VariableDocumentada tiene ambos significados; se permite ninguna.",
        "Fixtures: 3x true + 1x false con motor real.",
        "Versionado formato vs release sin migraciones historicas.",
    ],
}
p_json = OUT / "entrega.json"
p_json.write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lineas = ["# P4-shacl-versionado v002", "",
    f"Forma exacta de v001 (SHA {H_SHAPE[:16]}...) contra snapshot R8 `{H_SNAP[:16]}...` en store temporal aislado.",
    f"SHACL snapshot: conforms={shacl_snapshot['conforms']}, violaciones={shacl_snapshot['violation_count']}.",
    f"Variables: total={n_var}, doc={n_doc}, cand={n_cand}, ambos={n_both}, ninguno={n_neither}.",
    "Conflictos de extras manuales: " + ("ninguno (nada que eliminar)." if n_both == 0 else f"{n_both} (informados, NO eliminados)."),
    "Fixtures v001 re-ejecutadas: 3x true + 1x false. sh:not/xone sin evaluacion en la instalacion probada (no universal).",
    "Formato (v1) vs release (R8): sin migraciones historicas; v001 sellada intacta."]
p_md = OUT / "entrega.md"
p_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

archivos = [{"ruta": str(p.relative_to(REPO)).replace(chr(92), "/"), "sha256": sha256(p)}
            for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "congelada.json"]
(OUT / "congelada.json").write_text(json.dumps(
    {"rol": "P4-shacl-versionado", "version": "v002", "archivos": archivos,
     "conteos": {"ambos_en_snapshot": n_both, "fixtures_true": 3, "fixtures_false": 1}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK v002: conforms=", shacl_snapshot["conforms"], "ambos=", n_both, "archivos=", len(archivos))
