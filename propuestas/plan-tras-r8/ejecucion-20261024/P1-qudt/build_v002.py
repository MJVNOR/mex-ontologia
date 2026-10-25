"""Construye entrega P1-QUDT v002. No modifica v001/. Solo escribe v002/ y raiz P1."""
import json, hashlib, pathlib

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"
V1 = MIO / "v001"
V = MIO / "v002"
(V / "consultas").mkdir(parents=True, exist_ok=True)
(V / "fixtures").mkdir(parents=True, exist_ok=True)

MILIM = "http://qudt.org/vocab/unit/MilliM"
HA = "http://qudt.org/vocab/unit/HA"

def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
estado_por_def = {r["definicion_iri"]: r["estado"] for r in cob["variables"]}

CASOS = [
    {"id": "P1-Q1", "concepto": "precipitacion-diaria", "variable": "Precipitacion_mm",
     "dataset": "8b4edefe-cb1a-401c-90c6-05548779defd", "resource": "6713de4e-1e2b-447d-8000-f6ceaabd8473",
     "definicion_iri": "https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "huella": "dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f",
     "unidad_literal": "Milimetros", "qudt": MILIM, "w_ref": "P1-W-01",
     "w_file": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-MilliM-evidencia.txt",
     "w_url": "https://qudt.org/vocab/unit/MilliM",
     "localizador": "inspeccion definiciones[5]: Precipitacion_mm, Unidad de medida=Milimetros, Ejemplo=12.5",
     "fuente_url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=6713de4e-1e2b-447d-8000-f6ceaabd8473&limit=1000&offset=0&sort=_id+asc"},
    {"id": "P1-Q2", "concepto": "volumen-agua-presas", "variable": "Almacenamiento(hm3)",
     "dataset": "ee8f639f-5e89-46ae-93b9-934b05fc6233", "resource": "ca5574f0-d59d-4fc1-a52f-5c533b2abf82",
     "definicion_iri": "https://example.org/mex-ontologi/definition/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3",
     "huella": "7f846ce0b9f83f30c32ea09ab7b09ba328ea4826b1c5ec2b3dede27003aaac3b",
     "unidad_literal": "Hectometros cubicos", "qudt": None, "w_ref": "P1-W-02",
     "w_file": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/P1-W-02-negativo-HectoM3.txt",
     "w_url": "https://qudt.org/vocab/unit/HectoM3",
     "localizador": "inspeccion: Almacenamiento(hm3), Unidad de medida=Hectometros cubicos, Ejemplo=738.54",
     "fuente_url": "https://datos.sonora.gob.mx/dataset/ee8f639f-5e89-46ae-93b9-934b05fc6233/resource/ca5574f0-d59d-4fc1-a52f-5c533b2abf82/download/diccionario_recursos_hidricos.csv"},
    {"id": "P1-Q3", "concepto": "superficie-sembrada-cultivo", "variable": "SUPSEM",
     "dataset": "3e17a7e8-c8d4-49c4-a426-4dec099cd0cd", "resource": "94215f51-9c89-414d-8c3d-92792e609a2a",
     "definicion_iri": "https://example.org/mex-ontologi/definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "huella": "208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321",
     "unidad_literal": "Hectareas", "qudt": HA, "w_ref": "P1-W-03",
     "w_file": "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-HA-evidencia.txt",
     "w_url": "https://qudt.org/vocab/unit/HA",
     "localizador": "inspeccion: SUPSEM, Unidad de medida=Hectareas, Descripcion=Cantidad de hectareas sembradas",
     "fuente_url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=94215f51-9c89-414d-8c3d-92792e609a2a&limit=1000&offset=0&sort=_id+asc"},
]

# 1. literal local + estado respaldado coinciden (Q1/Q3 vinculables; Q2 literal ok pero sin QUDT)
for c in CASOS:
    d = json.loads((BASE / f"data/portal/inspecciones/{c['resource']}.json").read_text(encoding="utf-8"))
    assert d.get("fuente", "") == c["fuente_url"], f"fuente URL distinta en {c['id']}"
    assert estado_por_def[c["definicion_iri"]] == "respaldada_por_definicion", c["id"]

VOC = """@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Vocabulario minimo P1-QUDT v002 (propuesta, no nucleo: terminos nuevos, sin rename).
mex:UnidadDeclarada a rdfs:Class ;
    rdfs:label "Unidad declarada"@es ;
    rdfs:comment "Declara la unidad de UNA variable documentada segun ESA definicion del diccionario. Sin valores, sin conversiones."@es .
mex:variableDocumentada a rdfs:Property ;
    rdfs:label "variable documentada"@es ;
    rdfs:comment "IRI mex:documented-variable de R8. No se imputa dominio qudt:QuantityValue."@es .
mex:definicionFuente a rdfs:Property ;
    rdfs:label "definicion fuente"@es ;
    rdfs:comment "IRI mex:definition de R8 que respalda la variable."@es .
mex:conjuntoFuente a rdfs:Property ;
    rdfs:label "conjunto fuente (dataset UUID)"@es ;
    rdfs:comment "UUID del conjunto CKAN (dataset). Distinto del UUID del recurso/diccionario."@es .
mex:diccionarioFuente a rdfs:Property ;
    rdfs:label "diccionario fuente (resource UUID)"@es ;
    rdfs:comment "UUID del recurso CKAN que porta el diccionario. Distinto del UUID del conjunto."@es .
mex:unidadLiteral a rdfs:Property ;
    rdfs:label "unidad literal"@es ;
    rdfs:comment "Texto tal cual en la columna Unidad de medida de la fila."@es .
mex:unidadQudt a rdfs:Property ;
    rdfs:label "unidad QUDT"@es ;
    rdfs:comment "IRI HTTP canonica verificada por W. Solo si existe precoordinada; sin conversiones ni factores."@es .
# Nota: el estado de aprobacion vive en entrega.json (paquete); el grafo solo declara y evidencia.
mex:motivoNegativo a rdfs:Property ;
    rdfs:label "motivo negativo"@es .
mex:evidenciaNormativa a rdfs:Property ;
    rdfs:label "evidencia normativa"@es ;
    rdfs:comment "Ruta + SHA + URL + localizador del archivo W que verifica (o niega) el IRI."@es .
"""
(V / "vocabulario.ttl").write_text(VOC, encoding="utf-8")

def bloque(c):
    slug = {"P1-Q1": "declaracion-precipitacion-mm", "P1-Q2": "declaracion-volumen-agua-hm3-negativa",
            "P1-Q3": "declaracion-superficie-ha"}[c["id"]]
    wsha = sha(BASE / c["w_file"])
    c["w_sha"] = wsha
    if c["qudt"]:
        extra = f'    mex:unidadQudt <{c["qudt"]}> ;\n'
        comment = (f"Alcance: SOLO variable {c['variable']} de ESA definicion del diccionario {c['resource']}. "
                   "Sin atribucion global a recurso/periodos. Sin valores, sin conversiones.")
    else:
        extra = ""
        comment = ("NEGATIVO: HectoM3 dio 404 y esta ausente del indice QUDT 3.5.3 (W P1-W-02). Sin vinculo QUDT; "
                   "no se inventa conversion a M3 ni factor. Solo se conserva el literal local cualificado.")
    motivo = "" if c["qudt"] else '    mex:motivoNegativo "HectoM3 404 + ausente en indice QUDT 3.5.3 (P1-W-02); sin M3 ni factor inventados" ;\n'
    der = f"    prov:wasDerivedFrom <{c['fuente_url']}> ;" if not c["qudt"] else \
        f"    prov:wasDerivedFrom <{c['fuente_url']}> , <{c['w_url'].replace('https://qudt.org', 'http://qudt.org')}> ;"
    return f"""<https://example.org/mex-ontologi/propuesta/p1-qudt/v002/{slug}> a mex:UnidadDeclarada ;
    rdfs:label "{c['variable']}: unidad {c['unidad_literal']} (declaracion cualificada)"@es ;
    mex:variableDocumentada <{c['documented_iri']}> ;
    mex:definicionFuente <{c['definicion_iri']}> ;
    mex:conjuntoFuente "{c['dataset']}" ;
    mex:diccionarioFuente "{c['resource']}" ;
    mex:unidadLiteral "{c['unidad_literal']}" ;
{extra}{motivo}    mex:evidenciaNormativa "{c['w_ref']}: {c['w_file']} sha256={wsha} url={c['w_url']}" ;
{der}
    rdfs:comment "{comment}"@es .
"""

TTL = ("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n@prefix prov: <http://www.w3.org/ns/prov#> .\n"
       "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
       "# P1-QUDT v002. Q1/Q3 con IRI HTTP canonica verificada por W; Q2 negativa sin vinculo.\n"
       "# Sin QuantityValue, sin conversiones, sin factores, sin alias por parecido.\n\n"
       + "\n".join(bloque(c) for c in CASOS))
(V / "propuesta-qudt.ttl").write_text(TTL, encoding="utf-8")

from rdflib import Graph
g = Graph(); g.parse(data=TTL, format="turtle")
gv = Graph(); gv.parse(data=VOC, format="turtle")

Q = {
 "q1-vinculos-verificados.rq": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
   "SELECT ?d ?var ?u WHERE { ?d a mex:UnidadDeclarada ; mex:variableDocumentada ?var ; mex:unidadQudt ?u } ORDER BY ?d", 2),
 "q2-negativos-sin-vinculo.rq": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
   "SELECT ?d ?var ?m WHERE { ?d a mex:UnidadDeclarada ; mex:variableDocumentada ?var ; mex:motivoNegativo ?m . "
   "FILTER NOT EXISTS { ?d mex:unidadQudt ?u } }", 1),
 "q3-trazabilidad.rq": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\nPREFIX prov: <http://www.w3.org/ns/prov#>\n"
   "SELECT ?d ?lit ?src WHERE { ?d a mex:UnidadDeclarada ; mex:unidadLiteral ?lit ; prov:wasDerivedFrom ?src } ORDER BY ?d ?src", 5),
}
res = {}
for f, (qq, n) in Q.items():
    (V / "consultas" / f).write_text(qq, encoding="utf-8")
    rows = list(g.query(qq))
    assert len(rows) == n, f"{f}: {len(rows)} != {n}"
    res[f] = len(rows)

# pruebas estrictas
U = {str(r[0]) for r in g.query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?u WHERE { ?s mex:unidadQudt ?u }")}
from rdflib import URIRef
uris_qudt = {str(t) for t in set(list(g.subjects()) + list(g.predicates()) + list(g.objects()))
             if isinstance(t, URIRef) and "qudt.org/vocab/unit" in str(t)}
checks = {
 "sujetos_http_exactos": U == {MILIM, HA},
 "solo_iris_qudt_http": uris_qudt == {MILIM, HA},
 "sin_hecto_alias": not any("Hecto" in u for u in uris_qudt),
 "sin_quantityvalue": not any("QuantityValue" in str(t) for t in
      set(list(g.subjects()) + list(g.predicates()) + list(g.objects()) + list(gv.subjects()) + list(gv.predicates()) + list(gv.objects()))
      if isinstance(t, URIRef)),
 "sin_conversion": not any("conversion" in str(t).lower() for t in
      list(g.predicates()) + list(g.objects()) if isinstance(t, URIRef)),
 "sin_aprobacion_en_grafo": "estadoPropuesta" not in TTL and "propuesta_para_auditar" not in TTL,
 "dataset_distinto_resource": all(c["dataset"] != c["resource"] for c in CASOS),
 "uuid_con_formato": all(len(c["dataset"]) == 36 and len(c["resource"]) == 36 for c in CASOS),
}
# q2 check riguroso por conteo
n_q2link = len(list(g.query("PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT ?u WHERE { <https://example.org/mex-ontologi/propuesta/p1-qudt/v002/declaracion-volumen-agua-hm3-negativa> mex:unidadQudt ?u }")))
checks["q2_sin_vinculo"] = (n_q2link == 0)
assert all(checks.values()), checks
(V / "pruebas.json").write_text(json.dumps({"consultas_filas": res, "checks": checks}, ensure_ascii=False, indent=1), encoding="utf-8")

# fixtures: copiar v001 (lectura, sin modificar v001)
import shutil
for f in (V1 / "fixtures").glob("*.json"):
    shutil.copyfile(f, V / "fixtures" / f.name)

fuente_rutas = [
    ("data/portal/inspecciones/6713de4e-1e2b-447d-8000-f6ceaabd8473.json", CASOS[0]["fuente_url"], "definiciones[5] Precipitacion_mm/Milimetros/12.5"),
    ("data/portal/inspecciones/ca5574f0-d59d-4fc1-a52f-5c533b2abf82.json", CASOS[1]["fuente_url"], "Almacenamiento(hm3)/Hectometros cubicos/738.54"),
    ("data/portal/inspecciones/94215f51-9c89-414d-8c3d-92792e609a2a.json", CASOS[2]["fuente_url"], "SUPSEM/Hectareas/Cantidad de hectareas sembradas"),
    ("data/semantica/cobertura.json", None, "estados respaldada_por_definicion de las 3 definiciones"),
    ("reports/ronda-8.json", None, "base cerrada R8"),
    (CASOS[0]["w_file"], CASOS[0]["w_url"], "W P1-W-01 VERIFICADO MilliM http canonico; vocab 2026-10-20"),
    (CASOS[2]["w_file"], CASOS[2]["w_url"], "W P1-W-03 VERIFICADO HA http canonico; HectoHA 404 rechazado"),
    (CASOS[1]["w_file"], CASOS[1]["w_url"], "W P1-W-02 NEGATIVO: HectoM3 404 + ausente indice 3.5.3"),
    ("propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-M3-evidencia.txt",
     "https://qudt.org/vocab/unit/M3", "W alternativa M3 verificada: NO usada por P1 (requeriria factor no declarado)"),
]
fuentes = [{"ruta": r, "sha256": sha(BASE / r), **({"url": u} if u else {}), "localizador": loc} for r, u, loc in fuente_rutas]

ENTREGA = {
 "rol": "P1-qudt", "version": "v002", "fecha_utc": "2026-10-24", "estado": "propuesta_para_auditar",
 "base": {"informe": "reports/ronda-8.json", "estado_r8": "cerrado_integrado_validado_y_sincronizado"},
 "casos": [
   {"id": "P1-Q1", "variable": "Precipitacion_mm", "dataset_uuid": CASOS[0]["dataset"], "resource_uuid": CASOS[0]["resource"],
    "definicion_iri": CASOS[0]["definicion_iri"], "huella": CASOS[0]["huella"], "unidad_literal": "Milimetros",
    "unidad_qudt": MILIM, "normativa": "W P1-W-01 VERIFICADO", "resultado": "propuesta_para_auditar"},
   {"id": "P1-Q2", "variable": "Almacenamiento(hm3)", "dataset_uuid": CASOS[1]["dataset"], "resource_uuid": CASOS[1]["resource"],
    "definicion_iri": CASOS[1]["definicion_iri"], "huella": CASOS[1]["huella"], "unidad_literal": "Hectometros cubicos",
    "unidad_qudt": None, "normativa": "W P1-W-02 NEGATIVO (HectoM3 404/ausente); sin M3 ni factor inventados",
    "resultado": "sin_evidencia_para_integrar"},
   {"id": "P1-Q3", "variable": "SUPSEM", "dataset_uuid": CASOS[2]["dataset"], "resource_uuid": CASOS[2]["resource"],
    "definicion_iri": CASOS[2]["definicion_iri"], "huella": CASOS[2]["huella"], "unidad_literal": "Hectareas",
    "unidad_qudt": HA, "normativa": "W P1-W-03 VERIFICADO", "resultado": "propuesta_para_auditar"}],
 "archivos_propuestos": ["v002/vocabulario.ttl", "v002/propuesta-qudt.ttl",
   "v002/consultas/q1-vinculos-verificados.rq", "v002/consultas/q2-negativos-sin-vinculo.rq",
   "v002/consultas/q3-trazabilidad.rq", "v002/fixtures/P1-Q1-Precipitacion_mm.json",
   "v002/fixtures/P1-Q2-Almacenamiento(hm3).json", "v002/fixtures/P1-Q3-SUPSEM.json", "v002/pruebas.json"],
 "validacion_local": {"turtle_parse_ok": True, "vocabulario_parse_ok": True, **{k.replace(".rq", ""): v for k, v in res.items()}, "checks": checks},
 "fuentes": fuentes,
 "sello_w_v002": "PENDIENTE: W v002/normativa sin congelada a esta fecha; SHAs de archivos W registrados como observados. Hash final P1 se fija contra sello W cuando exista; si difiere, v003.",
 "limites": [
   "v001 preservada e intacta; v002 no la modifica.",
   "Declaracion cualificada estrictamente sobre ESA definicion del diccionario; ninguna atribucion global a recurso/periodos.",
   "Q2 sin vinculo QUDT; sin conversion a M3 ni factor; sin alias por parecido.",
   "Sujetos RDF exactos en http (no https); verificado por codigo, sin re-navegar (rol W).",
   "datasetUUID (conjunto) distinguido de resourceUUID (diccionario) en modelo, consultas y pruebas.",
   "Sin QuantityValue observado, sin conversiones, sin cambios de conceptos, sin produccion, sin Gemma."],
 "condiciones_aceptacion": [
   "Auditor replica SHAs y localizadores; Q1=2, Q2=1, Q3=5 filas.",
   "Sello W v002 confirma SHAs normativos; si difieren, v003.",
   "Q1/Q3 integrables con IRI http verificado; Q2 permanece fuera."],
}
(V / "entrega.json").write_text(json.dumps(ENTREGA, ensure_ascii=False, indent=1), encoding="utf-8")
(V / "entrega.md").write_text(
 "# P1-QUDT v002 — propuesta_para_auditar (Q1/Q3) + Q2 negativa\n\n"
 "v001 preservada. Q1→`http://qudt.org/vocab/unit/MilliM`, Q3→`http://qudt.org/vocab/unit/HA` "
 "(HTTP canónico verificado por W v002). Q2 sin vínculo (HectoM3 404/ausente índice; sin M3 ni factor).\n\n"
 "Modelo mínimo en `vocabulario.ttl` (términos nuevos, sin rename): UnidadDeclarada, "
 "variableDocumentada, definicionFuente, conjuntoFuente=datasetUUID, diccionarioFuente=resourceUUID, "
 "unidadLiteral, unidadQudt, estadoPropuesta, motivoNegativo, evidenciaNormativa.\n\n"
 "Consultas: Q1=2, Q2=1, Q3=5 filas (rdflib existente). Sello W v002 pendiente: SHAs normativos "
 "registrados como observados; hash final se fija contra sello W.\n", encoding="utf-8")

# sello v002: NO se incluye a si mismo; hashes de archivos finales tras toda escritura.
alcance = sorted([p for p in MIO.rglob("*") if p.is_file()
                  and "v001" not in p.relative_to(MIO).parts
                  and p.name != "congelada.json"], key=lambda p: p.relative_to(MIO).as_posix())
arch = {p.relative_to(MIO).as_posix().replace("\\", "/"): sha(p) for p in alcance}
congel = {"rol": "P1-qudt", "version": "v002", "fecha_utc": "2026-10-24",
  "alcance": "v002/** + raiz P1 (excluye v001 historica y excluye este sello)",
  "nota": "Este sello no contiene su propio hash; cubre archivos finales tras toda escritura.",
  "archivos": arch}
(V / "congelada.json").write_text(json.dumps(congel, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK q={[f'{k}={v}' for k, v in res.items()]} archivos={len(congel['archivos'])}")
