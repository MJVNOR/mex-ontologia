"""Q-unidades v001: inventario reproducible de unidades literales y 6 propuestas cualificadas.

Lee filas originales (data/portal/inspecciones/*.json) + estados
(data/semantica/cobertura.json). Reusa sellos P1 v003 y W v003 sin editarlos.
No instala, no regenera el grafo, no toca Studio ni manifiestos R1-R9.

Escribe: inventario-unidades.json, propuesta-q-unidades.ttl (SOLO
declaracion cualificada: sin unidadQudt, sin QuantityValue, sin
conversiones/factores), consultas, entrega.json/.md,
informe-exclusiones.md, pruebas.json y congelada.json (sin autoinclusion).
"""
import hashlib
import json
import pathlib

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
Q = BASE / "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades"
V = Q / "v001"
(V / "consultas").mkdir(parents=True, exist_ok=True)


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def huella_fila(fila: dict) -> str:
    return hashlib.sha256(
        json.dumps(fila, ensure_ascii=False, sort_keys=True,
                   separators=(",", ":")).encode("utf-8")).hexdigest()


def inspeccion(dic: str) -> dict:
    return json.loads(
        (BASE / f"data/portal/inspecciones/{dic}.json").read_text(encoding="utf-8"))


cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
por_huella = {v["huella_fila_diccionario"]: v for v in cob["variables"]
              if v.get("huella_fila_diccionario")}

# --- 1. Inventario reproducible: todo literal no vacio en "Unidad de medida" ---
distintas: dict = {}
inspecciones = 0
incompletos = 0
for p in sorted((BASE / "data/portal/inspecciones").glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    inspecciones += 1
    if d.get("definiciones") and d.get("completo") is not True:
        incompletos += 1
    for f in d.get("definiciones", []):
        lit = f.get("Unidad de medida", "")
        if not isinstance(lit, str) or not lit.strip():
            continue
        h = huella_fila(f)
        e = distintas.setdefault(lit, {"filas": 0, "ejemplos": []})
        e["filas"] += 1
        if len(e["ejemplos"]) < 3:
            v = por_huella.get(h, {})
            e["ejemplos"].append({
                "diccionario": p.stem,
                "variable": f.get("Nombre variable"),
                "huella": h,
                "estado": v.get("estado", "sin_cobertura"),
                "concepto": v.get("concepto", ""),
            })

# --- 2. Seis propuestas: unidad fisica explicita, respaldada, no R9, no hm3 ---
SPEC = [
    {"id": "Q-U01", "dic": "94215f51-9c89-414d-8c3d-92792e609a2a",
     "literal": "Toneladas", "concepto": "produccion-cultivo-toneladas",
     "slug": "declaracion-produccion-toneladas", "w": "Q-W-01",
     "pista": "tonelada metrica"},
    {"id": "Q-U02", "dic": "a4eb0b8b-d6c6-44b8-b00a-f5f45c1875a5",
     "literal": "Kilogramos", "concepto": "peso-promedio-cabeza-subasta",
     "slug": "declaracion-pesoprom-kilogramos", "w": "Q-W-02",
     "pista": "kilogramo"},
    {"id": "Q-U03", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "MW", "concepto": "unidad-capacidad-planta-electrica",
     "slug": "declaracion-capacidad-mw", "w": "Q-W-03",
     "pista": "megavatio",
     "matiz": " (fila de unidad de Capacidad Autorizada)"},
    {"id": "Q-U04", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "GWh", "concepto": "unidad-generacion-planta-electrica",
     "slug": "declaracion-generacion-gwh", "w": "Q-W-04",
     "pista": "gigavatio-hora",
     "matiz": " (fila de unidad de Generacion Estimada)"},
    {"id": "Q-U05", "dic": "251309e5-0309-46ed-9711-77a1dd408eeb",
     "literal": "Porcentaje", "concepto": "porc-analfabetismo-localidad",
     "slug": "declaracion-analf-porcentaje", "w": "Q-W-05",
     "pista": "porcentaje"},
    {"id": "Q-U06", "dic": "33d0a99e-c721-496f-a05e-07646e9ae42a",
     "literal": "Grados celcius", "concepto": "temperatura-caso",
     "slug": "declaracion-temperatura-grados", "w": "Q-W-06",
     "pista": "grado Celsius"},
]

casos = []
for s in SPEC:
    d = inspeccion(s["dic"])
    hits = [f for f in d["definiciones"]
            if f.get("Unidad de medida") == s["literal"]
            and por_huella.get(huella_fila(f), {}).get("concepto") == s["concepto"]]
    assert len(hits) == 1, (s["id"], len(hits))
    fila = hits[0]
    h = huella_fila(fila)
    v = por_huella[h]
    assert v["estado"] == "respaldada_por_definicion", s["id"]
    assert v["diccionario"] == s["dic"], s["id"]
    var = fila["Nombre variable"]
    idx = v["definicion_iri"].rsplit("%2F", 1)[1]
    casos.append({
        **s, "variable": var, "huella": h,
        "definicion_iri": v["definicion_iri"],
        "documented_iri": v["definicion_iri"].replace(
            "/definition/", "/documented-variable/"),
        "conjunto": v["conjunto"], "descripcion": v["descripcion"],
        "fuente_url": d["fuente"], "fila": fila,
    })
    assert set(casos[-1]) >= {"variable", "huella", "definicion_iri"}

# --- 2b. No duplicar R9 (Milimetros/Hectareas ya vinculadas en P1) ni otra declaracion ---
R9_LITERALES = {"Milímetros", "Hectáreas"}
assert not any(c["literal"] in R9_LITERALES for c in casos)
portal = BASE / "data/portal/ampliacion.ttl"
from rdflib import Graph as _Graph, RDF as _RDF, URIRef as _URIRef  # noqa: E402
_MEX = "https://example.org/mex-ontologi/vocab/"
_pg = _Graph()
_pg.parse(portal, format="turtle")
ya_declaradas = {str(o) for s in _pg.subjects(_RDF.type, _URIRef(_MEX + "UnidadDeclarada"))
                 for o in _pg.objects(s, _URIRef(_MEX + "variableDocumentada"))}
assert len(ya_declaradas) == 2, ya_declaradas  # R9: MilliM + HA
assert not any(c["documented_iri"] in ya_declaradas for c in casos), \
    "una propuesta ya esta declarada en el portal"

# Las peticiones a W deben cubrir exactamente estos seis casos y literales.
pet = json.loads((Q / "peticiones-web.json").read_text(encoding="utf-8"))
assert {p["caso"]: p["id"] for p in pet["solicitudes"]} == {c["id"]: c["w"] for c in casos}
assert all(c["literal"] in next(p["pide"] for p in pet["solicitudes"]
                               if p["caso"] == c["id"]) for c in casos)

# --- 3. TTL: solo declaracion cualificada (sin unidadQudt ni QuantityValue) ---
def bloque(c):
    return (f"<https://example.org/mex-ontologi/propuesta/q-unidades/v001/{c['slug']}>"
            f" a mex:UnidadDeclarada ;\n"
            f"    rdfs:label \"{c['variable']}: unidad {c['literal']}"
            f"{c.get('matiz', '')}\"@es ;\n"
            f"    mex:variableDocumentada <{c['documented_iri']}> ;\n"
            f"    mex:definicionFuente <{c['definicion_iri']}> ;\n"
            f"    mex:conjuntoFuente \"{c['conjunto']}\" ;\n"
            f"    mex:diccionarioFuente \"{c['dic']}\" ;\n"
            f"    mex:unidadLiteral \"{c['literal']}\" ;\n"
            f"    mex:evidenciaNormativa \"{c['w']}: Q-unidades/peticiones-web.json"
            f" (pista: {c['pista']}) ; pendiente de verificacion por W en QUDT 3.5.3,"
            f" sin vinculo hasta su sello\" ;\n"
            f"    prov:wasDerivedFrom <{c['fuente_url']}> ;\n"
            f"    rdfs:comment \"Alcance: SOLO variable {c['variable']} de ESA"
            f" definicion del diccionario {c['dic']}. Sin atribucion global."
            f" Sin valores ni factores.\"@es .\n")


TTL = ("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n"
       "@prefix prov: <http://www.w3.org/ns/prov#> .\n"
       "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
       "# Q-unidades v001 (propuesta, NO instalable): 6 declaraciones cualificadas.\n"
       "# Sin mex:unidadQudt, sin QuantityValue, sin factores. Vinculo solo con sello W.\n\n"
       + "\n".join(bloque(c) for c in casos))
(V / "propuesta-q-unidades.ttl").write_text(TTL, encoding="utf-8")

from rdflib import Graph, URIRef  # noqa: E402

g = Graph()
g.parse(data=TTL, format="turtle")
Q1 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT ?d ?var ?lit WHERE { ?d a mex:UnidadDeclarada ;"
      " mex:variableDocumentada ?var ; mex:unidadLiteral ?lit } ORDER BY ?d")
rows = list(g.query(Q1))
assert len(rows) == 6, len(rows)
terms = set(list(g.subjects()) + list(g.predicates()) + list(g.objects()))
uris = {str(t) for t in terms if isinstance(t, URIRef)}
assert not any("qudt.org/vocab/unit" in u for u in uris), "sin IRIs QUDT sin sello W"
assert "http://qudt.org/vocab/unit/MilliM" not in uris
assert not any("QuantityValue" in u for u in uris)
assert not any("conversion" in u.lower() for u in uris
               if u.startswith("https://example.org")), "sin conversiones"
lits = {str(r[2]) for r in rows}
assert lits == {c["literal"] for c in casos}, lits
(V / "consultas" / "q-unidades-declaradas.rq").write_text(Q1, encoding="utf-8")

# --- 4. Sellos reusados (verificados por codigo, sin edicion) ---
P1E = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/entrega.json"
P1C = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/congelada.json"
W3C = "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v003/congelada.json"
W3E = "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v003/entrega.json"
sellos = {r: sha(BASE / r) for r in (P1E, P1C, W3C, W3E)}
# W v003 no se incluye en su propio sello: hash fijado aqui. P1 se contrasta
# contra SU sello, que es la fuente autoritativa (no un literal duplicado).
assert sellos[W3C] == "6876a312956e110fff535df9aea8eeee27e25ce5a11f58b10c280f52126b3190"
p1c = json.loads((BASE / P1C).read_text(encoding="utf-8"))
assert p1c["archivos"]["v003/entrega.json"] == sellos[P1E]

fuentes = []
for c in casos:
    r = f"data/portal/inspecciones/{c['dic']}.json"
    fuentes.append({"ruta": r, "sha256": sha(BASE / r), "url": c["fuente_url"],
                    "localizador": f"{c['variable']}, Unidad de medida exacta"})
fuentes += [
    {"ruta": "data/semantica/cobertura.json",
     "sha256": sha(BASE / "data/semantica/cobertura.json"),
     "localizador": "estados respaldada_por_definicion"},
    {"ruta": P1E, "sha256": sellos[P1E],
     "localizador": "inventario P1 y 2 unidades R9 (no duplicadas)"},
    {"ruta": P1C, "sha256": sellos[P1C],
     "localizador": "sello P1 (contraste del hash de entrega)"},
    {"ruta": "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/presas_vars.json",
     "sha256": p1c["archivos"]["presas_vars.json"],
     "localizador": "22 filas (hm3 en cap_name, cap_namo, vol_muerto, Almacenamiento; "
                    "Altitud en Grados)"},
    {"ruta": W3C, "sha256": sellos[W3C], "localizador": "sello W v003 (HectoM3 ausente)"},
    {"ruta": W3E, "sha256": sellos[W3E], "localizador": "W v003 entrega"},
    {"ruta": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/peticiones-web.json",
     "sha256": sha(Q / "peticiones-web.json"),
     "localizador": "6 solicitudes Q-W-01..06 a W"},
]

(V / "inventario-unidades.json").write_text(json.dumps(
    {"nota": "Un literal por fila original con Unidad de medida no vacia; "
             "estados segun huella en cobertura.json. Piso, no censo: "
             f"{incompletos} inspecciones con definiciones no marcan completo=true.",
     "inspecciones_totales": inspecciones,
     "inspecciones_con_definiciones_no_completas": incompletos,
     "distintas": len(distintas),
     "filas_con_unidad": sum(e["filas"] for e in distintas.values()),
     "literales": {k: v for k, v in sorted(distintas.items())}},
    ensure_ascii=False, indent=1), encoding="utf-8")

ENTREGA = {
    "rol": "Q-unidades", "version": "v001", "fecha_utc": "2026-10-24",
    "estado": "propuesta_para_auditar_NO_instalable",
    "base": {"informe": "reports/ronda-9.json",
             "estado_r9": "cerrado_integrado_validado_y_sincronizado"},
    "casos": [{**{k: c[k] for k in (
        "id", "variable", "literal", "huella", "definicion_iri",
        "documented_iri", "conjunto", "w", "pista",
        "fuente_url", "descripcion")}, "diccionario": c["dic"]}
        for c in casos],
    "grafo": {"archivo": "v001/propuesta-q-unidades.ttl",
              "declaraciones": 6, "sin_unidadQudt": True,
              "sin_QuantityValue": True, "sin_conversiones": True},
    "inventario": {"archivo": "v001/inventario-unidades.json",
                   "literales_distintos": len(distintas),
                   "filas_con_unidad": sum(e["filas"] for e in distintas.values()),
                   "inspecciones": inspecciones,
                   "con_definiciones_no_completas": incompletos},
    "modelo": "opencode/deepseek-v4.1-flash-free",
    "reproducible_con": "uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/"
                        "Q-unidades/v001/scripts/generar_v001.py (solo lectura local; "
                        "sin red, sin grafo, escribe solo en v001/)",
    "peticiones_w": {"ruta": "Q-unidades/peticiones-web.json",
                     "solicitudes": ["Q-W-01", "Q-W-02", "Q-W-03",
                                     "Q-W-04", "Q-W-05", "Q-W-06"]},
    "fuentes": fuentes,
    "limites": [
        "v001 no instalable: sin vinculo QUDT hasta sello W; solo declaracion cualificada.",
        "No se duplica R9 (Milimetros/Hectareas) ni se repite HectoM3 (sello W v003).",
        "Compuestas (Pesos/kilogramo, Toneladas/hectareas, Pesos por tonelada), moneda, Grados y conteos: en informe-exclusiones.md.",
        "Inventario = piso de literales legibles en data/portal/inspecciones (no censo del portal).",
        "Sin QuantityValue, factores, atribucion global, Gemma ni contactos."],
}
(V / "entrega.json").write_text(json.dumps(ENTREGA, ensure_ascii=False, indent=1),
                                encoding="utf-8")
(V / "entrega.md").write_text(
    "# Q-unidades v001 — 6 declaraciones cualificadas (no instalables)\n\n"
    + "\n".join(f"- {c['id']} `{c['variable']}` literal `{c['literal']}`"
                f" ({c['dic']}, huella `{c['huella'][:12]}…)"
                f" → petición {c['w']} ({c['pista']})" for c in casos)
    + "\n\nGrafo solo cualificado: sin `mex:unidadQudt`, sin QuantityValue,"
      " sin factores. Vínculo solo con sello W en versión nueva.\n"
    + f"\nInventario: {len(distintas)} literales distintos /"
      f" {sum(e['filas'] for e in distintas.values())} filas con unidad"
      f" en {inspecciones} inspecciones ({incompletos} no completas).\n"
      "Reproducir: `uv run python propuestas/ampliacion-post-r9/"
      "ejecucion-20261024/Q-unidades/v001/scripts/generar_v001.py`.\n",
    encoding="utf-8")
(V / "informe-exclusiones.md").write_text(
    "# Q-unidades v001 — exclusiones (no propuestas)\n\n"
    "- **Hectómetros cúbicos** (4 filas: `cap_name`, `cap_namo`, `vol_muerto`,"
    " `Almacenamiento(hm³)`, según el diccionario sellado"
    " `P1-qudt/presas_vars.json`; la inspección local `ca5574f0…` solo expone 3"
    " definiciones): búsqueda agotada; HectoM3 404 + ausente del índice"
    " QUDT 3.5.3 (sello W v003). No se repite sin pista primaria distinta;"
    " nada de M3/factores.\n"
    "- **Hectáreas fuera de R9** (14 filas: SUPSEM ya vinculada en R9;"
    " SUPCOSE, SUPSINI, SHD139…, SUMTOT fuera): mismo"
    " término R9 (HA) ya vinculado en otra definición; no se duplica.\n"
    "- **Compuestas sin término exacto conocido**: `Pesos/kilogramo` (3),"
    " `Toneladas/hectáreas` (1), `Pesos por tonelada` (1). Sin petición:\n"
    "  requieren término precoordinado que Q no puede acreditar localmente.\n"
    "- **Grados** (2 filas visibles: Latitud, Longitud; una tercera, Altitud en"
    " Grados, consta en `P1-qudt/presas_vars.json`): literal ambiguo sin"
    " calificativo (existe también `Grados celcius`) y fila malrotulada;"
    " no se propone en v001.\n"
    "- **Moneda/importe** (`Pesos MXN`, `Miles de pesos MXN`,"
    " `Pesos Mexicanos`, `Miles de litros; Toneladas`): escala o moneda,"
    " no magnitud física con término exacto local.\n"
    "- **Referencia indirecta**: `La unidad de medida que se indica en la"
    " siguiente variable` (3), `Mantiene las unidades indicadas en UMED`,"
    " `Unidad según tipo de metal` (descripción, columna vacía): sin literal"
    " explícito propio.\n"
    "- **Conteo**: `Cabezas` (15): conteo, sin término físico exacto local.\n"
    "- **Códigos, títulos, clasificaciones y N/A** (resto del inventario):"
    " no son unidades (ver `inventario-unidades.json`).\n",
    encoding="utf-8")
(V / "pruebas.json").write_text(json.dumps(
    {"consultas_filas": {"q-unidades-declaradas": 6},
     "literales": sorted(lits),
     "inventario": {"literales_distintos": len(distintas),
                    "filas_con_unidad": sum(e["filas"] for e in distintas.values()),
                    "inspecciones": inspecciones,
                    "con_definiciones_no_completas": incompletos},
     "checks": {"seis_declaraciones": True, "sin_iris_qudt": True,
                "sin_quantityvalue": True, "sin_conversiones": True,
                "sellos_w_p1_verificados": True,
                "sin_duplicar_r9_ni_portal": True,
                "peticiones_w_cubren_los_6_casos": True,
                "literales_exactos_de_fila": True}},
    ensure_ascii=False, indent=1), encoding="utf-8")

alcance = sorted(
    [p for p in V.rglob("*") if p.is_file() and p.name != "congelada.json"
     and "__pycache__" not in p.parts],
    key=lambda p: p.relative_to(V).as_posix())
arch = {p.relative_to(V).as_posix().replace("\\", "/"): sha(p) for p in alcance}
(V / "congelada.json").write_text(json.dumps(
    {"rol": "Q-unidades", "version": "v001", "fecha_utc": "2026-10-24",
     "alcance": "v001/** (excluye este sello)",
     "nota": "Sello sin autoinclusion; hashes finales tras toda escritura.",
     "archivos": arch}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK literales={sorted(lits)} archivos={len(arch)}")
print(f"inventario: {len(distintas)} literales distintos")
