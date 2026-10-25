"""Genera v001 P4-shacl-versionado (plan-tras-r8/ejecucion-20261024).
Solo escribe dentro de P4-shacl-versionado/v001/.
Todos los SHA-256 se calculan por codigo; nada se tipea a mano.
Validacion SHACL con motor real open-ontologies en STORES AISLADOS
(tempstore por fixture, via scripts/construir_catalogo.motor, sin Studio).
"""
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:\Users\marti\Documents\MEX-Ontologi")
P4 = REPO / "propuestas/plan-tras-r8/ejecucion-20261024/P4-shacl-versionado"
OUT = P4 / "v001"
PROP = OUT / "propuesta"
FIX = OUT / "fixtures"
CON = OUT / "consultas"
for d in (PROP, FIX, CON):
    d.mkdir(parents=True, exist_ok=True)

import sys
sys.path.insert(0, str(REPO / "scripts"))
from construir_catalogo import motor


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- 1. TTL separado (staging, no toca shapes/semantica.ttl) ---
# sh:not / sh:xone NO implementados en el motor por defecto (conforms null,
# skipped_constraints); ademas xone prohibiria NEITHER. Se usa sh:sparql,
# soportado por el motor, que permite ninguno/uno y prohibe ambos.
SHAPE = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix shape: <https://example.org/mex-ontologi/shapes/> .

# Propuesta P4 v001 (staging): exclusion mutua entre significadoDocumentado y
# significadoCandidato para mex:VariableDocumentada. Permite NEITHER (variable
# pendiente), permite DOC-solo o CAND-solo, prohibe BOTH. No declara ni repite
# prov:wasDerivedFrom (regla minCount 2 de correspondencias queda intacta).
# Integracion R9: anadir este sh:sparql al shape:VariableDocumentada central.
shape:VariableDocumentadaExclusion a sh:NodeShape ;
    sh:targetClass mex:VariableDocumentada ;
    sh:sparql [
        a sh:SPARQLConstraint ;
        sh:message "mex:significadoDocumentado y mex:significadoCandidato son mutuamente excluyentes; se permite ninguno o uno solo"@es ;
        sh:select \"\"\"SELECT $this WHERE { $this <https://example.org/mex-ontologi/vocab/significadoDocumentado> ?d . $this <https://example.org/mex-ontologi/vocab/significadoCandidato> ?c . }\"\"\" ;
    ] .
"""
(PROP / "shape-exclusion-significado.ttl").write_text(SHAPE, encoding="utf-8")

PREFIX = "@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n@prefix ex: <https://example.org/mex-ontologi/test/> .\n@prefix concepto: <https://example.org/mex-ontologi/concept/> .\n"
FIXTURES = {
    "fixture-neither.ttl": "ex:v-pendiente a mex:VariableDocumentada .\n",
    "fixture-doc.ttl": "ex:v-doc a mex:VariableDocumentada ;\n    mex:significadoDocumentado concepto:anio-defuncion .\n",
    "fixture-cand.ttl": "ex:v-cand a mex:VariableDocumentada ;\n    mex:significadoCandidato concepto:anio-defuncion .\n",
    "fixture-both.ttl": "ex:v-ambos a mex:VariableDocumentada ;\n    mex:significadoDocumentado concepto:anio-defuncion ;\n    mex:significadoCandidato concepto:anio-registro .\n",
}
for name, body in FIXTURES.items():
    (FIX / name).write_text(PREFIX + body, encoding="utf-8")

QUERY = """# P4 v001: variables con AMBOS significados (debe dar vacio tras integrar).
PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?v ?d ?c WHERE {
  ?v a mex:VariableDocumentada ;
     mex:significadoDocumentado ?d ;
     mex:significadoCandidato ?c .
} ORDER BY ?v
"""
(CON / "variables-con-ambos-significados.rq").write_text(QUERY, encoding="utf-8")

METADATA = {
    "formato_entrega": "p4-v001",
    "format_version": "1",
    "release": "R8",
    "nota": "format_version describe el esquema de esta entrega; release nombra la ronda aprobada. No migrar el nucleo: este archivo es descriptivo y vive en staging.",
}
(PROP / "metadata-formato.json").write_text(json.dumps(METADATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

CHANGELOG = """# Propuesta de changelog (staging, no aplicar a docs/ sin aprobacion R9)

## Formato
- `format_version`: version del esquema de entrega (este piloto: `p4-v001` = formato 1).
- `release`: ronda aprobada (R8 vigente; R9 cuando se integre lo aprobado).

## Entrada propuesta (no integrada)
- `P4 v001`: regla de exclusion documentado/candidato (TTL separado) + 4 fixtures
  validados con motor real en stores aislados (3 conformes, 1 no conforme).
- Manifiestos R1-R8 intactos; el siguiente manifiesto se ANEXA (append/snapshot),
  no se reescribe historia.

## Regla
- No mutar manifiestos ni rondas aprobadas. Cada integracion anexa un manifiesto
  nuevo y, si el motor lo soporta, un snapshot (`version`/`history`).
"""
(PROP / "changelog-R9-propuesto.md").write_text(CHANGELOG, encoding="utf-8")

NOTA_R9 = """# Interfaces minimas de integracion futura (R9, solo si la forma se aprueba)

1. `shapes/semantica.ttl`, `shape:VariableDocumentada`: anadir UNICAMENTE el
   bloque `sh:sparql` de `propuesta/shape-exclusion-significado.ttl`.
   No tocar `maxCount 1` de cada significado ni los `minCount` de PROV.
2. Versionado: subir `format_version` solo si cambia el esquema de entrega;
   `release` cambia solo con ronda aprobada. Anexar manifiesto nuevo; jamas
   reescribir manifiestos R1-R8.
3. Validacion: suite Python completa + SHACL central con alcance declarado
   (triples de carga vs total Studio) + replicas de estas 4 fixtures.
4. Esta entrega no integra nada: no modifica semantica, shapes centrales,
   manifiestos previos, grafo ni Studio.
"""
(PROP / "nota-integracion-R9.md").write_text(NOTA_R9, encoding="utf-8")

# --- 2. Validacion con motor real en STORES AISLADOS ---
shape_path = PROP / "shape-exclusion-significado.ttl"
ESPERADO = {"fixture-neither.ttl": True, "fixture-doc.ttl": True, "fixture-cand.ttl": True, "fixture-both.ttl": False}
resultados = []
for name, esperado in ESPERADO.items():
    data_path = FIX / name
    store = Path(tempfile.mkdtemp(prefix="p4store-"))
    v = motor(["validate", str(data_path)], store)
    assert v.get("ok") is True, v
    motor(["load", str(data_path)], store)
    r = motor(["shacl", str(shape_path)], store)
    assert not r.get("skipped_constraints"), r
    conforms = r.get("conforms")
    assert conforms is esperado, (name, r)
    # La consulta de ambos debe coincidir con el veredicto: vacia salvo both.
    qtexto = (CON / "variables-con-ambos-significados.rq").read_text(encoding="utf-8")
    q = motor(["query", qtexto], store)
    filas = q.get("rows", q.get("results", q))
    n = len(filas) if isinstance(filas, list) else filas
    resultados.append({
        "fixture": f"fixtures/{name}",
        "esperado_conforms": esperado,
        "conforms": conforms,
        "violation_count": r.get("violation_count"),
        "filas_con_ambos": n,
        "store_aislado": "tempstore (sin Studio)",
    })

# Operador declarado no disponible: verificador --verified ausente en el exe distribuido.
verdad = Path(tempfile.mkdtemp(prefix="p4v-"))
try:
    motor(["shacl", "--verified", str(shape_path)], verdad)
    verified = "disponible"
except RuntimeError as e:
    verified = "no disponible en el exe distribuido (bloqueo honesto; no se simula)"
    assert "oo-shacl" in str(e) or "verified" in str(e).lower(), str(e)[:300]

# --- 3. Fuentes primarias (hashes por codigo) ---
F_SHAPES = REPO / "shapes/semantica.ttl"
F_R8 = REPO / "reports/ronda-8.json"
F_PLAN = REPO / "docs/plan-actualizado-tras-r8.md"
F_PLANJ = REPO / "docs/plan-actualizado-tras-r8.json"
F_ASIG = P4 / "asignacion.json"
H = {p: sha256(p) for p in (F_SHAPES, F_R8, F_PLAN, F_PLANJ, F_ASIG)}
# Fijos R8: la forma central permite hoy ambos (maxCount 1 por propiedad, sin exclusion).
central = F_SHAPES.read_text(encoding="utf-8")
assert "mex:significadoDocumentado" in central and "mex:significadoCandidato" in central
assert "sh:not" not in central and "VariableDocumentadaExclusion" not in central
r8 = json.loads(F_R8.read_text(encoding="utf-8"))
assert r8["estado"] == "cerrado_integrado_validado_y_sincronizado"
assert r8["resumen_actual"]["estados_correspondencias"]["candidata_por_nombre"] == 17

entrega = {
    "rol": "P4-shacl-versionado",
    "version": "v001",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "base": "reports/ronda-8.json",
    "asignacion_sha256": H[F_ASIG],
    "estado": "propuesta_para_auditar",
    "casos": [],
    "resultados": resultados,
    "motor": {
        "exe": "tools/open-ontologies.exe",
        "operador": "sh:sparql (soportado; veredicto determinado, sin skipped_constraints)",
        "operadores_evitados": "sh:not y sh:xone: no implementados en el evaluador por defecto (conforms null/indeterminado); xone ademas prohibiria NEITHER. Verificador --verified: " + verified,
        "stores": "aislados por fixture (tempstore); sin Studio; sin tocar produccion",
    },
    "fuentes": [
        {"ruta": "shapes/semantica.ttl", "sha256": H[F_SHAPES], "localizador": "shape:VariableDocumentada (maxCount 1 por significado, sin exclusion; sin sh:not ni Exclusion)",
         "afirmacion_soportada": "La forma central vigente permite hoy ambos significados; la exclusion solo existe en el TTL separado propuesto"},
        {"ruta": "reports/ronda-8.json", "sha256": H[F_R8], "localizador": "estado + resumen_actual.estados_correspondencias",
         "afirmacion_soportada": "R8 cerrado/integrado/validado; 17 candidatas por nombre; base congelada del plan"},
        {"ruta": "docs/plan-actualizado-tras-r8.md", "sha256": H[F_PLAN], "localizador": "seccion 3, fila P4",
         "afirmacion_soportada": "P4: exclusion documentado/candidato + versionado/changelog; preservar PROV min2; separar formato de release"},
        {"ruta": "docs/plan-actualizado-tras-r8.json", "sha256": H[F_PLANJ], "localizador": "piloto P4",
         "afirmacion_soportada": "Condicion de aceptacion: permite ninguno, impide ambos, preserva rondas; no duplicar PROV"},
    ],
    "propuestos_staging": [
        "propuesta/shape-exclusion-significado.ttl",
        "propuesta/metadata-formato.json",
        "propuesta/changelog-R9-propuesto.md",
        "propuesta/nota-integracion-R9.md",
        "fixtures/fixture-neither.ttl",
        "fixtures/fixture-doc.ttl",
        "fixtures/fixture-cand.ttl",
        "fixtures/fixture-both.ttl",
        "consultas/variables-con-ambos-significados.rq",
    ],
    "limites": [
        "Escritura exclusiva en P4-shacl-versionado/v001; no se modifica produccion, ontologia/semantica.json, shapes centrales, manifiestos previos, grafo ni Studio.",
        "Gemma excluido; sin contactos externos; sin navegador (reservado a W): ninguna URL primaria concreta requerida; sin peticiones-web.json.",
        "No se repite investigacion R8; sin inventar unidades, fechas ni jerarquias; C1/C4/P3 cubren sus casos (17/19/101), P4 tiene 0 casos asignados.",
        "No se duplica prov:wasDerivedFrom minCount 2; el TTL propuesto no declara PROV.",
        "Manifiestos R1-R8 intactos: solo append/snapshots futuros; format_version != release; metadata descriptiva sin migrar el nucleo.",
        "Verificador --verified no disponible en el exe distribuido; no se simula su veredicto.",
    ],
    "condiciones_de_aceptacion": [
        "La forma permite variables pendientes sin ninguno de los dos vinculos.",
        "La forma impide que una variable tenga ambos (fixture-both conforms=false; otros tres conforms=true con motor real).",
        "Se preservan las rondas aprobadas y los manifiestos R1-R8.",
        "PROV minCount 2 de correspondencias intacto y no duplicado.",
        "Version de formato JSON separada de version de release; changelog descriptivo.",
        "Integracion R9 solo por las interfaces minimas de nota-integracion-R9.md, con suite + SHACL central conformes.",
    ],
    "navegador": "no usado (reservado a W); sin peticiones-web.json: diseno y validacion 100% locales con motor real",
}
p_json = OUT / "entrega.json"
p_json.write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lineas = ["# P4-shacl-versionado v001", "",
    "Piloto de diseno (0 casos asignados): exclusion documentado/candidato + versionado. Estado: propuesta_para_auditar.",
    "Motor real open-ontologies en stores aislados (sin Studio), via scripts/construir_catalogo.motor:",
    "| fixture | esperado | conforms | violaciones | filas con ambos |",
    "| --- | --- | --- | --- | --- |"]
for r in resultados:
    lineas.append(f"| {r['fixture']} | {r['esperado_conforms']} | {r['conforms']} | {r['violation_count']} | {r['filas_con_ambos']} |")
lineas += ["",
    "Operador: sh:sparql (determinado). Evitados sh:not/sh:xone (no implementados en el evaluador por defecto; xone ademas prohibiria NEITHER).",
    "--verified no disponible en el exe distribuido (bloqueo honesto, no simulado).",
    "No se toca produccion/shapes centrales/manifiestos/grafo/Studio. Versionado: format_version (esquema entrega) separado de release (ronda).",
    "Navegador no usado; sin peticiones-web.json."]
p_md = OUT / "entrega.md"
p_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

archivos = []
for p in sorted(OUT.rglob("*")):
    if p.is_file() and p.name != "congelada.json":
        archivos.append({"ruta": str(p.relative_to(REPO)).replace(chr(92), "/"), "sha256": sha256(p)})
congelada = {"rol": "P4-shacl-versionado", "version": "v001",
             "archivos": archivos,
             "conteos": {"fixtures_conforms_true": 3, "fixtures_conforms_false": 1, "fuentes": 4,
                         "casos_asignados": 0, "propuestos_staging": 9}}
(OUT / "congelada.json").write_text(json.dumps(congelada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK v001 P4:", len(resultados), "fixtures;", len(archivos), "archivos congelados")
