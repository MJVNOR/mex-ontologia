"""Construye P1-QUDT v003. Preserva v001/ y v002/. Solo escribe v003/ y raiz P1.
Corrige defecto v002: literales exactos (con tilde) desde inspecciones. Grafo instalable: Q1+Q3.
Q2 negativo en informe aparte."""
import json, hashlib, pathlib, shutil

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"
V = MIO / "v003"
(V / "consultas").mkdir(parents=True, exist_ok=True)
(V / "fixtures").mkdir(parents=True, exist_ok=True)

MILIM = "http://qudt.org/vocab/unit/MilliM"
HA = "http://qudt.org/vocab/unit/HA"

def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def insp(dic):
    return json.loads((BASE / f"data/portal/inspecciones/{dic}.json").read_text(encoding="utf-8"))

cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
estado_por_def = {r["definicion_iri"]: r["estado"] for r in cob["variables"]}

W3 = "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v003"
w_sello = {"ruta": f"{W3}/congelada.json", "sha256": sha(BASE / f"{W3}/congelada.json")}
w_ent = {"ruta": f"{W3}/entrega.json", "sha256": sha(BASE / f"{W3}/entrega.json")}
w_ver = {"ruta": f"{W3}/verificacion-hashes.json", "sha256": sha(BASE / f"{W3}/verificacion-hashes.json")}

CASOS = [
    {"id": "P1-Q1", "concepto": "precipitacion-diaria", "variable": "Precipitacion_mm",
     "dataset": "8b4edefe-cb1a-401c-90c6-05548779defd", "resource": "6713de4e-1e2b-447d-8000-f6ceaabd8473",
     "definicion_iri": "https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "huella": "dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f8",
     "qudt": MILIM, "w_ref": "P1-W-01",
     "w_file": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-MilliM-evidencia.txt",
     "fuente_url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=6713de4e-1e2b-447d-8000-f6ceaabd8473&limit=1000&offset=0&sort=_id+asc"},
    {"id": "P1-Q3", "concepto": "superficie-sembrada-cultivo", "variable": "SUPSEM",
     "dataset": "3e17a7e8-c8d4-49c4-a426-4dec099cd0cd", "resource": "94215f51-9c89-414d-8c3d-92792e609a2a",
     "definicion_iri": "https://example.org/mex-ontologi/definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "huella": "208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321",
     "qudt": HA, "w_ref": "P1-W-03",
     "w_file": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-HA-evidencia.txt",
     "fuente_url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=94215f51-9c89-414d-8c3d-92792e609a2a&limit=1000&offset=0&sort=_id+asc"},
]

for c in CASOS:
    d = insp(c["resource"])
    assert d.get("fuente", "") == c["fuente_url"], c["id"]
    assert estado_por_def[c["definicion_iri"]] == "respaldada_por_definicion", c["id"]
    hit = [x for x in d["definiciones"] if x.get("Nombre variable") == c["variable"]]
    assert len(hit) == 1, c["id"]
    # literal EXACTO de la fila, sin normalizar
    c["unidad_literal"] = hit[0]["Unidad de medida"]
    assert c["unidad_literal"] and c["unidad_literal"] != c["unidad_literal"].encode("ascii", "ignore").decode(), c["id"]
    c["fila"] = hit[0]
    # fixture v003 = copia exacta de la fila (lectura de inspeccion; v002 no se toca)
    (V / "fixtures" / f"{c['id']}-{c['variable']}.json").write_text(
        json.dumps(hit[0], ensure_ascii=False, indent=1), encoding="utf-8")
    # igualdad byte-exacta con fixture v002 preservado
    f2 = MIO / "v002/fixtures" / f"{c['id']}-{c['variable']}.json"
    assert json.loads(f2.read_text(encoding="utf-8")) == hit[0], f"fixture v002 difiere en {c['id']}"

shutil.copyfile(MIO / "v002/vocabulario.ttl", V / "vocabulario.ttl")

def bloque(c):
    slug = {"P1-Q1": "declaracion-precipitacion-mm", "P1-Q3": "declaracion-superficie-ha"}[c["id"]]
    wsha = sha(BASE / c["w_file"]); c["w_sha"] = wsha
    L = c["unidad_literal"]
    return f"""<https://example.org/mex-ontologi/propuesta/p1-qudt/v003/{slug}> a mex:UnidadDeclarada ;
    rdfs:label "{c['variable']}: unidad {L}"@es ;
    mex:variableDocumentada <{c['documented_iri']}> ;
    mex:definicionFuente <{c['definicion_iri']}> ;
    mex:conjuntoFuente "{c['dataset']}" ;
    mex:diccionarioFuente "{c['resource']}" ;
    mex:unidadLiteral "{L}" ;
    mex:unidadQudt <{c['qudt']}> ;
    mex:evidenciaNormativa "{c['w_ref']}: {c['w_file']} sha256={wsha} ; sello W v003 {W3}/congelada.json sha256={w_sello['sha256']}" ;
    prov:wasDerivedFrom <{c['fuente_url']}> , <{c['qudt']}> ;
    rdfs:comment "Alcance: SOLO variable {c['variable']} de ESA definicion del diccionario {c['resource']}. Sin atribucion global. Sin valores, sin conversiones."@es .
"""

TTL = ("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n@prefix prov: <http://www.w3.org/ns/prov#> .\n"
       "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
       "# P1-QUDT v003 instalable (Q1+Q3). Literales exactos de fila. Q2 en informe aparte.\n\n"
       + "\n".join(bloque(c) for c in CASOS))
(V / "propuesta-qudt.ttl").write_text(TTL, encoding="utf-8")

from rdflib import Graph, URIRef
g = Graph(); g.parse(data=TTL, format="turtle")
gv = Graph(); gv.parse(data=(V / "vocabulario.ttl").read_text(encoding="utf-8"), format="turtle")

Q = {
 "q1-vinculos-verificados.rq": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
   "SELECT ?d ?var ?u WHERE { ?d a mex:UnidadDeclarada ; mex:variableDocumentada ?var ; mex:unidadQudt ?u } ORDER BY ?d", 2),
 "q3-trazabilidad.rq": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\nPREFIX prov: <http://www.w3.org/ns/prov#>\n"
   "SELECT ?d ?lit ?src WHERE { ?d a mex:UnidadDeclarada ; mex:unidadLiteral ?lit ; prov:wasDerivedFrom ?src } ORDER BY ?d ?src", 4),
}
res = {}
for f, (qq, n) in Q.items():
    (V / "consultas" / f).write_text(qq, encoding="utf-8")
    rows = list(g.query(qq))
    assert len(rows) == n, f"{f}: {len(rows)} != {n}"
    res[f] = len(rows)

lits = {str(r[1]) for r in g.query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?d ?lit WHERE { ?d mex:unidadLiteral ?lit }")}
U = {str(r[0]) for r in g.query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?u WHERE { ?s mex:unidadQudt ?u }")}
terms = set(list(g.subjects()) + list(g.predicates()) + list(g.objects()))
uris_qudt = {str(t) for t in terms if isinstance(t, URIRef) and "qudt.org/vocab/unit" in str(t)}
checks = {
 "literales_exactos_fila": lits == {c["unidad_literal"] for c in CASOS},
 "literales_con_tilde": all(c["unidad_literal"] != c["unidad_literal"].encode("ascii", "ignore").decode() for c in CASOS),
 "sujetos_http_exactos": U == {MILIM, HA},
 "solo_iris_qudt_http": uris_qudt == {MILIM, HA},
 "solo_q1q3_en_grafo": len(list(g.query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?d WHERE { ?d a mex:UnidadDeclarada }"))) == 2,
 "sin_aprobacion_en_grafo": "estadoPropuesta" not in TTL and "propuesta_para_auditar" not in TTL and "sin_evidencia_para_integrar" not in TTL,
 "sin_quantityvalue": not any("QuantityValue" in str(t) for t in terms if isinstance(t, URIRef)),
 "sin_conversion": not any("conversion" in str(t).lower() for t in list(g.predicates()) + list(g.objects()) if isinstance(t, URIRef)),
 "dataset_distinto_resource": all(c["dataset"] != c["resource"] for c in CASOS),
}
assert all(checks.values()), checks
(V / "pruebas.json").write_text(json.dumps(
    {"consultas_filas": res, "literales": sorted(lits), "checks": checks}, ensure_ascii=False, indent=1), encoding="utf-8")

(V / "informe-negativo-Q2.md").write_text(
 "# Q2 negativo (informe aparte, fuera del grafo instalable)\n\n"
 "Variable Almacenamiento(hm3), diccionario ca5574f0-d59d-4fc1-a52f-5c533b2abf82: literal local "
 f"\"{(json.loads((BASE / 'data/portal/inspecciones/ca5574f0-d59d-4fc1-a52f-5c533b2abf82.json').read_text(encoding='utf-8'))['definiciones'][2].get('Unidad de medida'))}\" "
 "conservado sin reinterpretar.\n"
 "W P1-W-02: HectoM3 404 + ausente del indice QUDT 3.5.3; HectoHA 404. Sin vinculo QUDT, sin M3, sin factor "
 "(M3 solo acredita su propia IRI). Sello W v003: "
 f"{W3}/congelada.json sha256={w_sello['sha256']}.\n", encoding="utf-8")

fuentes = [
 {"ruta": "data/portal/inspecciones/6713de4e-1e2b-447d-8000-f6ceaabd8473.json", "sha256": sha(BASE / "data/portal/inspecciones/6713de4e-1e2b-447d-8000-f6ceaabd8473.json"),
  "url": CASOS[0]["fuente_url"], "localizador": "Precipitacion_mm, Unidad de medida exacta de fila, Ejemplo=12.5"},
 {"ruta": "data/portal/inspecciones/94215f51-9c89-414d-8c3d-92792e609a2a.json", "sha256": sha(BASE / "data/portal/inspecciones/94215f51-9c89-414d-8c3d-92792e609a2a.json"),
  "url": CASOS[1]["fuente_url"], "localizador": "SUPSEM, Unidad de medida exacta de fila"},
 {"ruta": "data/semantica/cobertura.json", "sha256": sha(BASE / "data/semantica/cobertura.json"), "localizador": "estados respaldada_por_definicion"},
 {"ruta": "reports/ronda-8.json", "sha256": sha(BASE / "reports/ronda-8.json"), "localizador": "base cerrada R8"},
 {"ruta": CASOS[0]["w_file"], "sha256": CASOS[0]["w_sha"], "url": "https://qudt.org/vocab/unit/MilliM", "localizador": "W P1-W-01 VERIFICADO, sujeto http"},
 {"ruta": CASOS[1]["w_file"], "sha256": CASOS[1]["w_sha"], "url": "https://qudt.org/vocab/unit/HA", "localizador": "W P1-W-03 VERIFICADO, sujeto http; HectoHA 404"},
 {"ruta": w_sello["ruta"], "sha256": w_sello["sha256"], "localizador": "sello final W v003 existente"},
 {"ruta": w_ent["ruta"], "sha256": w_ent["sha256"], "localizador": "W v003 entrega (M3 no autoriza sustituciones ni factores)"},
 {"ruta": w_ver["ruta"], "sha256": w_ver["sha256"], "localizador": "verificacion de hashes por codigo W"},
]
ENTREGA = {
 "rol": "P1-qudt", "version": "v003", "fecha_utc": "2026-10-24", "estado": "propuesta_para_auditar",
 "corrige_a": "v002", "defecto_corregido": "unidadLiteral normalizado sin tilde; v003 usa literales exactos de fila",
 "base": {"informe": "reports/ronda-8.json", "estado_r8": "cerrado_integrado_validado_y_sincronizado"},
 "casos": [
  {"id": "P1-Q1", "variable": "Precipitacion_mm", "dataset_uuid": CASOS[0]["dataset"], "resource_uuid": CASOS[0]["resource"],
   "definicion_iri": CASOS[0]["definicion_iri"], "huella": CASOS[0]["huella"], "unidad_literal": CASOS[0]["unidad_literal"],
   "unidad_qudt": MILIM, "resultado": "propuesta_para_auditar"},
  {"id": "P1-Q3", "variable": "SUPSEM", "dataset_uuid": CASOS[1]["dataset"], "resource_uuid": CASOS[1]["resource"],
   "definicion_iri": CASOS[1]["definicion_iri"], "huella": CASOS[1]["huella"], "unidad_literal": CASOS[1]["unidad_literal"],
   "unidad_qudt": HA, "resultado": "propuesta_para_auditar"},
  {"id": "P1-Q2", "resultado": "sin_evidencia_para_integrar", "informe": "v003/informe-negativo-Q2.md",
   "nota": "Fuera del grafo instalable; sin vinculo, sin M3, sin factor."}],
 "archivos_instalables": ["v003/vocabulario.ttl", "v003/propuesta-qudt.ttl"],
 "validacion_local": {"turtle_parse_ok": True, **{k.replace(".rq", ""): v for k, v in res.items()}, "checks": checks},
 "fuentes": fuentes,
 "sello_w_v003": {"ruta": w_sello["ruta"], "sha256": w_sello["sha256"], "estado": "existente_verificado_por_codigo"},
 "limites": ["v001/v002 preservadas sin edicion; v003 no las modifica.",
  "Literales exactos de fila, sin normalizar; semantica conceptual sin cambios.",
  "Grafo instalable: solo Q1+Q3; Q2 en informe aparte.",
  "Sin QuantityValue, conversiones, factores, alias, atribucion global, produccion, Gemma."],
 "condiciones_aceptacion": ["Auditor replica SHAs y Q1=2/Q3=4 filas.",
  "Sello W v003 citado coincide por codigo.", "Q2 permanece fuera."],
}
(V / "entrega.json").write_text(json.dumps(ENTREGA, ensure_ascii=False, indent=1), encoding="utf-8")
(V / "entrega.md").write_text(
 "# P1-QUDT v003 — instalable Q1+Q3 (literales exactos)\n\n"
 f"Q1 `{CASOS[0]['unidad_literal']}`→`{MILIM}`, Q3 `{CASOS[1]['unidad_literal']}`→`{HA}` (HTTP canonico, W v003 sellado). "
 "Q2 negativo en `informe-negativo-Q2.md`, fuera del grafo. v001/v002 preservadas.\n", encoding="utf-8")

alcance = sorted([p for p in MIO.rglob("*") if p.is_file()
                  and "v001" not in p.relative_to(MIO).parts and "v002" not in p.relative_to(MIO).parts
                  and p.name != "congelada.json"], key=lambda p: p.relative_to(MIO).as_posix())
arch = {p.relative_to(MIO).as_posix().replace("\\", "/"): sha(p) for p in alcance}
(V / "congelada.json").write_text(json.dumps({"rol": "P1-qudt", "version": "v003", "fecha_utc": "2026-10-24",
  "alcance": "v003/** + raiz P1 (excluye v001/v002 historicas y excluye este sello)",
  "nota": "Sello sin autoinclusion; hashes finales tras toda escritura.",
  "archivos": arch}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK literales={[c['unidad_literal'] for c in CASOS]} archivos={len(arch)}")
