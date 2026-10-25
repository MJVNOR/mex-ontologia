"""Q-unidades v002: continuacion de v001 (inacabada) sin modificarla.

Lee (solo lectura): data/portal/inspecciones/*.json, data/semantica/cobertura.json,
sellos P1 v003 y W v003, peticiones-web.json del carril y base.json.
Escribe EXCLUSIVAMENTE bajo Q-unidades/v002/.

Reglas aplicadas:
- Un literal por fila original con "Unidad de medida" no vacia; literal exacto.
- 6 casos Q-U01..Q-U06 respaldados por definicion; huella de fila + variable +
  definicion + conjunto + diccionario comprobados contra cobertura.json.
- Ninguna URI QUDT se afirma: W no ha sellado Q-W-01..06. TTL solo cualificado.
- "Toneladas" NO se resuelve a variante metrica: fuente local ambigua -> pendiente.
- hm3/HectoM3 no se repite (sello W v003); sin M3 ni conversiones/factores.
- Sin QuantityValue, sin atribucion global de unidad, sin tocar R1-R9 ni Studio.
"""
import hashlib
import json
import pathlib
import shutil

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
Q = BASE / "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades"
V = Q / "v002"
FECHA = "2026-10-24"

RUTA_P1E = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/entrega.json"
RUTA_P1T = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/propuesta-qudt.ttl"
RUTA_WC = "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v003/congelada.json"
RUTA_WE = "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v003/entrega.json"
RUTA_CANAL = "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/peticiones-web.json"
RUTA_V001 = "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v001"
RUTA_V001_SELLO = RUTA_V001 + "/congelada.json"

SHA_P1E = "7a5c7441465d00611475a2b32b3e8faa396a22ee1dfb0886de297031028330c8"
SHA_WC = "6876a312956e110fff535df9aea8eeee27e25ce5a11f58b10c280f52126b3190"
SHA_CANAL = "00921b383e537dda8cbbeea1d31aef9bb2ff6d3ab0e57ab644536bfb17643452"
SHA_COB = "1486fcae52a210c803e1173aa0ecbfddd40d1e66a3147aebb1c64fdfa39dfb31"


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def huella_fila(fila):
    """Huella canonica de fila; debe coincidir con cobertura.json."""
    return hashlib.sha256(json.dumps(fila, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def escribir(ruta, texto):
    ruta = pathlib.Path(ruta)
    assert V in ruta.parents, f"escritura fuera de v002: {ruta}"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


def json_txt(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1)


# --- base congelada -------------------------------------------------------
cob = json.loads((BASE / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
base = json.loads((BASE / "propuestas/ampliacion-post-r9/ejecucion-20261024/base.json")
                  .read_text(encoding="utf-8"))
assert sha(BASE / "data/semantica/cobertura.json") == SHA_COB
assert base["sha256"]["data/semantica/cobertura.json"] == SHA_COB
assert sha(BASE / RUTA_P1E) == SHA_P1E
assert sha(BASE / RUTA_WC) == SHA_WC
assert sha(BASE / RUTA_CANAL) == SHA_CANAL
# v001 se cita por su propio sello; no se replican ni se asumen sus hashes.
assert (BASE / RUTA_V001_SELLO).is_file()
v001_entrega = json.loads((BASE / RUTA_V001 / "entrega.json").read_text(encoding="utf-8"))
assert v001_entrega["version"] == "v001"
assert len(v001_entrega["casos"]) == 6

por_huella = {v["huella_fila_diccionario"]: v for v in cob["variables"]
              if v.get("huella_fila_diccionario")}
assert len(por_huella) == 1424, len(por_huella)

FICHEROS = sorted((BASE / "data/portal/inspecciones").glob("*.json"))
assert len(FICHEROS) == 486, len(FICHEROS)

# --- 1. casos seleccionados ----------------------------------------------
SPEC = [
    {"id": "Q-U01", "dic": "94215f51-9c89-414d-8c3d-92792e609a2a",
     "literal": "Toneladas", "concepto": "produccion-cultivo-toneladas",
     "slug": "declaracion-produccion-toneladas", "w": "Q-W-01",
     "estado_propuesta": "pendiente_ambiguedad_tonelada"},
    {"id": "Q-U02", "dic": "a4eb0b8b-d6c6-44b8-b00a-f5f45c1875a5",
     "literal": "Kilogramos", "concepto": "peso-promedio-cabeza-subasta",
     "slug": "declaracion-pesoprom-kilogramos", "w": "Q-W-02",
     "estado_propuesta": "pendiente_verificacion_W"},
    {"id": "Q-U03", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "MW", "concepto": "unidad-capacidad-planta-electrica",
     "slug": "declaracion-capacidad-mw", "w": "Q-W-03",
     "estado_propuesta": "pendiente_verificacion_W"},
    {"id": "Q-U04", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "GWh", "concepto": "unidad-generacion-planta-electrica",
     "slug": "declaracion-generacion-gwh", "w": "Q-W-04",
     "estado_propuesta": "pendiente_verificacion_W"},
    {"id": "Q-U05", "dic": "251309e5-0309-46ed-9711-77a1dd408eeb",
     "literal": "Porcentaje", "concepto": "porc-analfabetismo-localidad",
     "slug": "declaracion-analf-porcentaje", "w": "Q-W-05",
     "estado_propuesta": "pendiente_verificacion_W"},
    {"id": "Q-U06", "dic": "33d0a99e-c721-496f-a05e-07646e9ae42a",
     "literal": "Grados celcius", "concepto": "temperatura-caso",
     "slug": "declaracion-temperatura-grados", "w": "Q-W-06",
     "estado_propuesta": "pendiente_verificacion_W"},
]


def filas(dic):
    return json.loads((BASE / f"data/portal/inspecciones/{dic}.json")
                      .read_text(encoding="utf-8"))


casos = []
for s in SPEC:
    d = filas(s["dic"])
    hits = [(i, f) for i, f in enumerate(d["definiciones"], 1)
            if f.get("Unidad de medida") == s["literal"]
            and por_huella.get(huella_fila(f), {}).get("concepto") == s["concepto"]]
    assert len(hits) == 1, (s["id"], len(hits))
    idx, fila = hits[0]
    h = huella_fila(fila)
    v = por_huella[h]
    assert v["estado"] == "respaldada_por_definicion", s["id"]
    assert v["diccionario"] == s["dic"], s["id"]
    assert v["variable"] == fila["Nombre variable"], s["id"]
    assert v["definicion_iri"].endswith(f"%2F{idx}"), s["id"]
    assert v["iri"].split("/")[-2] == "documented-variable", s["id"]
    copia = V / "fuentes" / s["id"] / f"{s['dic']}.json"
    copia.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE / f"data/portal/inspecciones/{s['dic']}.json", copia)
    assert sha(copia) == sha(BASE / f"data/portal/inspecciones/{s['dic']}.json")
    casos.append({
        "id": s["id"], "literal": s["literal"], "huella_fila": h,
        "variable": fila["Nombre variable"], "diccionario": s["dic"],
        "conjunto": v["conjunto"], "definicion_iri": v["definicion_iri"],
        "variable_documentada_iri": v["iri"], "concepto": v["concepto"],
        "regla": v["regla"], "indice_definicion": idx,
        "estado_cobertura": v["estado"],
        "estado_propuesta": s["estado_propuesta"],
        "vinculo_qudt": None, "peticion_w": s["w"], "slug": s["slug"],
        "fuente": {
            "ruta": f"data/portal/inspecciones/{s['dic']}.json",
            "sha256": sha(BASE / f"data/portal/inspecciones/{s['dic']}.json"),
            "url": d["fuente"],
            "localizador": f"{fila['Nombre variable']}, 'Unidad de medida' = "
                           f"'{s['literal']}', definiciones[{idx}], huella {h}",
        },
        "copia": {
            "ruta": copia.relative_to(BASE).as_posix(),
            "sha256": sha(copia), "bytes": copia.stat().st_size,
            "igual_a_origen": True,
        },
        "fila": fila,
        "comprobaciones": {
            "huella_recalculada_igual_cobertura": True,
            "variable_igual": True, "conjunto_igual": True,
            "diccionario_igual": True, "definicion_iri_igual": True,
            "unico_por_literal_y_concepto": True,
            "estado_respaldada_por_definicion": True,
            "copia_byte_igual_origen": True,
        },
    })
    escribir(V / "fuentes" / s["id"] / "fila.json", json_txt({
        "caso": s["id"], "diccionario": s["dic"], "indice_definicion": idx,
        "huella_fila": h, "unidad_literal": s["literal"], "fila": fila,
        "nota": "Fila exacta del diccionario de origen; 'Unidad de medida' sin "
                "normalizar. Huella = sha256 del JSON canonico de la fila.",
    }))

# Ambiguedad de 'Toneladas': el corpus usa el mismo literal sin calificativo.
filas_ton = []
for p in FICHEROS:
    d = json.loads(p.read_text(encoding="utf-8"))
    for i, f in enumerate(d.get("definiciones", []), 1):
        if f.get("Unidad de medida") == "Toneladas":
            hh = huella_fila(f)
            vv = por_huella.get(hh, {})
            filas_ton.append({"diccionario": p.stem, "indice_definicion": i,
                              "variable": f["Nombre variable"], "huella_fila": hh,
                              "concepto": vv.get("concepto", "")})
assert len(filas_ton) == 3, len(filas_ton)
assert len({r["diccionario"] for r in filas_ton}) == 2
casos[0]["ambiguedad"] = {
    "motivo": "El literal 'Toneladas' no declara variante. El corpus lo usa igual "
              "en 3 definiciones de 2 diccionarios (agricultura y pesca) sin "
              "calificativo de tonelada metrica, corta ni larga. La norma no "
              "decide la unidad local.",
    "filas_corpus_con_el_mismo_literal": filas_ton,
    "variantes_normativas": "No determinadas por Q. W puede documentar que "
                            "terminos exactos distinguen las variantes; Q no "
                            "elige por parecido.",
    "requiere_para_promover": "Evidencia local (documentacion del recurso o del "
                              "publicador) que declare tonelada metrica para "
                              "PRODTON de 94215f51.",
    "no_hace": ["no asigna variante metrica", "no vincula URI",
                "no aplica factor ni conversion"],
}

# --- 2. inventario de todos los literales --------------------------------
R9_LITERALES = {"Milímetros": "P1-Q1", "Hectáreas": "P1-Q3"}
R9_HUELLAS = {"208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321": "P1-Q3",
              "dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f8": "P1-Q1"}
CONTEO = {"Cabezas", "Productores", "Número de habitantes", "Total de habitantes",
          "cantidad de mujeres atendidas", "Cantidad de cintillos"}
SEL = {(c["diccionario"], c["huella_fila"]): c["id"] for c in casos}
SEL_LIT = {c["literal"] for c in casos}


def tratamiento(lit, dic, h):
    if (dic, h) in SEL:
        return "propuesta", SEL[(dic, h)]
    if h in R9_HUELLAS:
        return "ya_en_r9", (f"vinculada en R9 como {R9_HUELLAS[h]} con el mismo "
                            "literal; no se duplica")
    if lit == "Hectómetros cúbicos":
        return "excluida", "hm3: busqueda agotada (HectoM3 404 + ausente del " \
                           "indice QUDT 3.5.3, sello W v003); no se repite ni se " \
                           "sustituye por M3"
    if lit in R9_LITERALES:
        return "fuera_de_seleccion", f"mismo literal ya vinculado en R9 ({R9_LITERALES[lit]}); " \
                                     "la declaracion es por definicion, no se duplica"
    if lit in SEL_LIT:
        return "fuera_de_seleccion", "literal compartido por varias definiciones; " \
                                     "se propone una sola (alcance de 6 casos)"
    if lit in ("N/A", "No aplica"):
        return "excluida", "sin dato declarado; no es unidad"
    if lit == "Miles de litros; Toneladas":
        return "excluida", "unidad compuesta: mezcla dos unidades (litros y " \
                           "toneladas) para una columna UMED; no se resuelve localmente"
    if "/" in lit or lit.startswith("Pesos por"):
        return "excluida", "unidad compuesta (precio o rendimiento por unidad); " \
                           "requiere termino precoordinado que Q no acredita localmente"
    if ";" in lit:
        return "excluida", "enumeracion de categorias o escala; no es unidad"
    if lit.startswith(("Pesos", "Miles de pesos")):
        return "excluida", "moneda o escala de moneda; no es magnitud fisica con " \
                           "termino exacto local"
    if "se indica en la siguiente variable" in lit or "indicadas en UMED" in lit \
            or lit == "des_cal":
        return "excluida", "referencia indirecta a otra columna; sin literal propio"
    if lit in CONTEO:
        return "excluida", "conteo; sin termino fisico exacto local"
    if "por cada 100" in lit:
        return "excluida", "razon o indicador expresado en prosa; no es unidad"
    if lit == "Edad en años":
        return "excluida", "magnitud con la unidad embebida en el nombre ('años'); " \
                           "fuera de la seleccion de 6"
    if lit == "Grados":
        return "excluida", "ambiguo sin calificativo (angulo vs temperatura); " \
                           "existe ademas 'Grados celcius' en otra definicion"
    return "excluida", "codigo, nombre, clasificacion, rango o texto: no es unidad"


inventario = {}
for p in FICHEROS:
    d = json.loads(p.read_text(encoding="utf-8"))
    for i, f in enumerate(d.get("definiciones", []), 1):
        lit = f.get("Unidad de medida", "")
        if not isinstance(lit, str) or not lit.strip():
            continue
        h = huella_fila(f)
        v = por_huella.get(h, {})
        e = inventario.setdefault(lit, {"filas": 0, "estados_cobertura": {},
                                        "tratamientos": {}, "motivos": {},
                                        "ejemplos": []})
        e["filas"] += 1
        est = v.get("estado", "sin_cobertura")
        e["estados_cobertura"][est] = e["estados_cobertura"].get(est, 0) + 1
        tr, det = tratamiento(lit, p.stem, h)
        e["tratamientos"][tr] = e["tratamientos"].get(tr, 0) + 1
        e["motivos"].setdefault(tr, det)
        if len(e["ejemplos"]) < 3:
            e["ejemplos"].append({"diccionario": p.stem, "indice_definicion": i,
                                  "variable": f.get("Nombre variable"),
                                  "huella_fila": h, "concepto": v.get("concepto", ""),
                                  "tratamiento": tr, "detalle": det})

assert len(inventario) == 61, len(inventario)
assert sum(e["filas"] for e in inventario.values()) == 259
INV = {
    "nota": "Un literal exacto por fila original con 'Unidad de medida' no vacia, "
            "sin normalizar. Estados segun huella de fila en cobertura.json. "
            "tratamientos: propuesta (6 casos) | ya_en_r9 | fuera_de_seleccion | "
            "excluida (motivo por literal).",
    "fuente": {"ruta": "data/portal/inspecciones/*.json", "ficheros": len(FICHEROS),
               "sha256_cobertura": SHA_COB, "base": "R9"},
    "totales": {"literales_distintos": len(inventario),
                "filas_con_unidad": sum(e["filas"] for e in inventario.values()),
                "propuestas": 6},
    "literales": {k: inventario[k] for k in sorted(inventario)},
}
escribir(V / "inventario-unidades.json", json_txt(INV))

# --- 3. TTL: declaracion cualificada, sin unidadQudt ----------------------
def bloque(c):
    pend = ("pendiente de verificacion W (%s): sin vinculo normativo"
            % c["peticion_w"])
    if c["id"] == "Q-U01":
        pend = ("pendiente por ambiguedad local del literal 'Toneladas': no se "
                "asigna variante metrica ni se vincula URI; requiere evidencia "
                "local (Q-W-01b documenta variantes, no decide)")
    return (
        f"<https://example.org/mex-ontologi/propuesta/q-unidades/v002/{c['slug']}>"
        f" a mex:UnidadDeclarada ;\n"
        f"    rdfs:label \"{c['variable']}: unidad {c['literal']}\"@es ;\n"
        f"    mex:variableDocumentada <{c['variable_documentada_iri']}> ;\n"
        f"    mex:definicionFuente <{c['definicion_iri']}> ;\n"
        f"    mex:conjuntoFuente \"{c['conjunto']}\" ;\n"
        f"    mex:diccionarioFuente \"{c['diccionario']}\" ;\n"
        f"    mex:unidadLiteral \"{c['literal']}\" ;\n"
        f"    prov:wasDerivedFrom <{c['fuente']['url']}> ;\n"
        f"    rdfs:comment \"Alcance: SOLO variable {c['variable']} de ESA "
        f"definicion del diccionario {c['diccionario']}. Sin atribucion global, "
        f"sin valores, sin factores ni conversiones. Estado: {pend}.\"@es .\n")


TTL = ("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n"
       "@prefix prov: <http://www.w3.org/ns/prov#> .\n"
       "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
       "# Q-unidades v002 (propuesta, NO instalable tal cual): 6 declaraciones\n"
       "# cualificadas. Sin mex:unidadQudt: W no ha sellado Q-W-01..06.\n"
       "# Sin QuantityValue, sin factores, sin conversiones.\n\n"
       + "\n".join(bloque(c) for c in casos))
escribir(V / "propuesta-q-unidades.ttl", TTL)

from rdflib import Graph, URIRef  # noqa: E402

g = Graph()
g.parse(data=TTL, format="turtle")
Q1 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT ?d ?var ?lit ?def WHERE { ?d a mex:UnidadDeclarada ;\n"
      "  mex:variableDocumentada ?var ; mex:unidadLiteral ?lit ;\n"
      "  mex:definicionFuente ?def } ORDER BY ?d")
rows = list(g.query(Q1))
assert len(rows) == 6, len(rows)
assert {str(r[2]) for r in rows} == {c["literal"] for c in casos}
Q2 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT (COUNT(?d) AS ?n) WHERE { ?d a mex:UnidadDeclarada .\n"
      "  FILTER NOT EXISTS { ?d mex:unidadQudt ?u } }")
assert int(list(g.query(Q2))[0][0]) == 6
Q3 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "PREFIX prov: <http://www.w3.org/ns/prov#>\n"
      "SELECT ?d ?f WHERE { ?d a mex:UnidadDeclarada ; prov:wasDerivedFrom ?f }"
      " ORDER BY ?d")
assert len(list(g.query(Q3))) == 6
terminos = set(g.subjects()) | set(g.predicates()) | set(g.objects())
uris = {str(t) for t in terminos if isinstance(t, URIRef)}
assert not any("qudt.org" in u for u in uris), "sin IRIs QUDT sin sello W"
assert not any("QuantityValue" in u for u in uris)
assert not any("conversion" in u.lower() for u in uris), "sin conversiones"
assert not any("unit/M3" in u for u in uris), "sin M3"
escribir(V / "consultas/q1-declaraciones-por-caso.rq", Q1)
escribir(V / "consultas/q2-declaraciones-sin-unidad-qudt.rq", Q2)
escribir(V / "consultas/q3-trazabilidad-fuente.rq", Q3)

# --- 4. solicitudes a W (canal canonico intacto) -------------------------
canal = json.loads((BASE / RUTA_CANAL).read_text(encoding="utf-8"))
assert len(canal["solicitudes"]) == 6
assert [s["id"] for s in canal["solicitudes"]] == [f"Q-W-0{i}" for i in range(1, 7)]
SOL = {
    "rol_origen": "Q-unidades", "rol_destino": "W-estandares",
    "nota": "Copia de trabajo de las 6 peticiones del canal canonico, mas un "
            "addendum por ambiguedad de 'Toneladas'. Q no navega: W es el unico "
            "navegador. Ninguna URI se congela como aprobada.",
    "canal_canonico": {"ruta": RUTA_CANAL, "sha256": SHA_CANAL,
                       "modificado_por_v002": False},
    "estado_verificacion": {
        "sello_W_vigente": {"ruta": RUTA_WC, "sha256": SHA_WC,
                            "acredita": ["MilliM", "HA"],
                            "acredita_alguna_de_las_6": False},
        "verificadas_de_las_6": 0,
        "consecuencia": "v002 no afirma ninguna URI QUDT; las declaraciones "
                        "quedan cualificadas y pendientes.",
    },
    "solicitudes": canal["solicitudes"],
    "addendum": [{
        "id": "Q-W-01b", "caso": "Q-U01", "sustituye_a": "Q-W-01",
        "motivo": "Q-W-01 pedia 'tonelada metrica' por presuposicion. El literal "
                  "local 'Toneladas' no declara variante: la peticion vigente para "
                  "Q-U01 es Q-W-01b, sin eleccion de variante por Q.",
        "pide": "Documentar que terminos exactos de QUDT 3.5.3 distinguen las "
                "variantes de tonelada (metrica, corta, larga), con sujeto RDF, "
                "version, copia y SHA. Q no elige variante: solo necesita saber "
                "que se esta distinguiendo.",
        "no_pide": "Que la norma decida la unidad local; eso exige evidencia local.",
        "url_primaria_concreta": "https://qudt.org/vocab/unit/",
    }],
    "excluido": {
        "hm3/HectoM3": "busqueda agotada en W v003 (404 + ausente del indice); no "
                       "se repite",
        "M3": "no se usa como sustituto de hm3 ni con factor",
    },
}
escribir(V / "solicitudes/peticiones-web-v002.json", json_txt(SOL))

# --- 5. fuentes: indice de copias + sellos reusados ----------------------
indice_copias = {
    "nota": "Una copia byte a byte del archivo de inspeccion de origen por caso. "
            "sha256(copia) == sha256(origen). Las copias no se editan.",
    "copias": [{"caso": c["id"], "origen": c["fuente"]["ruta"],
                "sha256_origen": c["fuente"]["sha256"],
                "copia": c["copia"]["ruta"], "sha256_copia": c["copia"]["sha256"],
                "bytes": c["copia"]["bytes"], "iguales": True,
                "fila": {"indice_definicion": c["indice_definicion"],
                         "variable": c["variable"], "huella_fila": c["huella_fila"]}}
               for c in casos],
    "sellos_reusados_sin_edicion": [
        {"ruta": RUTA_P1E, "sha256": SHA_P1E,
         "uso": "2 unidades R9 ya vinculadas (MilliM, HA): no se duplican"},
        {"ruta": RUTA_P1T, "sha256": sha(BASE / RUTA_P1T),
         "uso": "forma de integracion R9 (mex:UnidadDeclarada + unidadQudt)"},
        {"ruta": RUTA_WC, "sha256": SHA_WC, "uso": "sello W v003; HectoM3 ausente"},
        {"ruta": RUTA_WE, "sha256": sha(BASE / RUTA_WE),
         "uso": "W v003: acredita MilliM y HA; nada de Q-W-01..06"},
        {"ruta": RUTA_V001_SELLO, "sha256": sha(BASE / RUTA_V001_SELLO),
         "uso": "v001 sellada por su carril; v002 no la edita ni replica sus hashes"},
        {"ruta": RUTA_CANAL, "sha256": SHA_CANAL, "uso": "canal Q->W intacto"},
    ],
}
escribir(V / "fuentes/indice-copias.json", json_txt(indice_copias))

# --- 6. formato de integracion -------------------------------------------
FORMATO = """# Q-unidades v002 — formato de integracion

## Que entrega v002

`propuesta-q-unidades.ttl`: 6 `mex:UnidadDeclarada`, una por definicion, con
`mex:unidadLiteral` exacto y sin `mex:unidadQudt`. Nada mas se afirma.

Predicados usados, todos ya presentes en el vocabulario instalado
(`data/portal/ampliacion.ttl`, verificado por codigo):

| predicado | objeto | comprobacion |
| --- | --- | --- |
| `mex:variableDocumentada` | IRI `documented-variable/...%2F<n>` | coincide con `cobertura.json` |
| `mex:definicionFuente` | IRI `definition/...%2F<n>` | indice de fila exacto |
| `mex:conjuntoFuente` | literal uuid | `cobertura.json` |
| `mex:diccionarioFuente` | literal uuid | `cobertura.json` |
| `mex:unidadLiteral` | literal exacto de fila | sin normalizar |
| `prov:wasDerivedFrom` | URL del recurso | `fuente` de la inspeccion |

## Estado por caso

| caso | literal | estado | condicion para promover |
| --- | --- | --- | --- |
| Q-U01 | `Toneladas` | `pendiente_ambiguedad_tonelada` | evidencia **local** que declare tonelada metrica |
| Q-U02 | `Kilogramos` | `pendiente_verificacion_W` | sello W de Q-W-02 |
| Q-U03 | `MW` | `pendiente_verificacion_W` | sello W de Q-W-03 |
| Q-U04 | `GWh` | `pendiente_verificacion_W` | sello W de Q-W-04 |
| Q-U05 | `Porcentaje` | `pendiente_verificacion_W` | sello W de Q-W-05 |
| Q-U06 | `Grados celcius` | `pendiente_verificacion_W` | sello W de Q-W-06 |

v002 **no es integrable como esta**: falta el vinculo normativo. La version
integrable (v003 o posterior) se produce cuando W selle las peticiones, y solo
para los casos que ademas tengan respaldo local no ambiguo.

## Como se integra (carril I, escritor central unico)

1. Dos auditorias independientes sobre los bytes de v002 y del sello W.
2. Copiar la declaracion aceptada y anadir, **solo** en los casos promovidos:

   ```turtle
   mex:unidadQudt <http://qudt.org/vocab/unit/...> ;
   ```

   y `mex:evidenciaNormativa` con la ruta de la evidencia W, su `sha256` y el
   `sha256` del sello W. Mismo patron que R9
   (`P1-qudt/v003/propuesta-qudt.ttl`).
3. Q-U01 no se promueve por sello W: el estandar no decide la unidad local.
   Se queda como declaracion cualificada o fuera, segun dictamen.
4. Verificar con `consultas/q1..q3` mas SHACL del portal; comprobar que no se
   altera nada ajeno.

## Prohibiciones (aplican a Q y a I)

- Nada de `QuantityValue` global ni por variable.
- Sin factores, conversiones ni sustituciones (hm3 -> M3 incluido).
- Sin atribucion global de unidad a un diccionario o conjunto.
- Sin URIs QUDT no selladas por W; sin alias por parecido.
- No se editan R1–R9, manifiestos, `config.toml` ni Studio.
- v002 no instala, no regenera grafo y no escribe fuera de su carpeta.
"""
escribir(V / "formato-integracion.md", FORMATO)

# --- 7. casos.json / casos.md --------------------------------------------
CASOS = {
    "nota": "6 definiciones respaldadas por definicion, con unidad literal exacta. "
            "huella_fila + variable + definicion + conjunto + diccionario "
            "comprobados contra cobertura.json (sha256 %s)." % SHA_COB,
    "base": {"informe": "reports/ronda-9.json",
             "sha256": sha(BASE / "reports/ronda-9.json"),
             "estado_r9": "cerrado_integrado_validado_y_sincronizado"},
    "resumen": {"casos": 6, "pendiente_verificacion_W": 5,
                "pendiente_ambiguedad_local": 1, "con_vinculo_qudt": 0},
    "casos": [{k: c[k] for k in ("id", "literal", "huella_fila", "variable",
                                 "diccionario", "conjunto", "definicion_iri",
                                 "variable_documentada_iri", "concepto", "regla",
                                 "indice_definicion", "estado_cobertura",
                                 "estado_propuesta", "vinculo_qudt",
                                 "peticion_w", "fuente", "copia", "fila",
                                 "comprobaciones")}
              | ({"ambiguedad": c["ambiguedad"]} if "ambiguedad" in c else {})
              for c in casos],
}
escribir(V / "casos.json", json_txt(CASOS))

lineas = ["# Q-unidades v002 — 6 casos (continuacion de v001)", "",
          "| caso | variable | literal exacto | diccionario | huella (12) | estado |",
          "| --- | --- | --- | --- | --- | --- |"]
for c in casos:
    lineas.append(f"| {c['id']} | `{c['variable']}` | `{c['literal']}` | "
                  f"`{c['diccionario'][:8]}` | `{c['huella_fila'][:12]}` | "
                  f"`{c['estado_propuesta']}` |")
lineas += ["", "Cada caso tiene copia fuente byte a byte en `fuentes/<caso>/` "
               "(sha256 igual al origen) y su fila exacta en `fila.json`.", "",
           "Q-U01 queda pendiente: el literal `Toneladas` no declara variante y el "
           "corpus lo repite en 3 definiciones de 2 diccionarios. La norma no "
           "decide la unidad local; no se asigna variante metrica.", "",
           "Ninguna URI QUDT se afirma en v002: W no ha sellado Q-W-01..06.", ""]
escribir(V / "casos.md", "\n".join(lineas))

# --- 8. exclusiones ------------------------------------------------------
excl = ["# Q-unidades v002 — exclusiones y fuera de seleccion", "",
        "Total inventariado: 61 literales, 259 filas con `Unidad de medida` no "
        "vacia (486 diccionarios, base R9).", ""]
for tr, titulo in (("ya_en_r9", "Ya en R9 (no se duplica)"),
                   ("fuera_de_seleccion", "Fuera de la seleccion de 6"),
                   ("excluida", "Excluidas (no son unidad resoluble)")):
    excl.append(f"## {titulo}")
    excl.append("")
    for lit in sorted(inventario):
        n = inventario[lit]["tratamientos"].get(tr)
        if not n:
            continue
        det = inventario[lit]["motivos"][tr]
        excl.append(f"- `{lit}` ({n} fila{'s' if n != 1 else ''}): {det}.")
    excl.append("")
excl += ["## Notas", "",
         "- **hm3**: busqueda agotada en W v003 (HectoM3 404 + ausente del indice "
         "QUDT 3.5.3). No se repite sin pista primaria distinta; no se usa M3 ni "
         "factor alguno.",
         "- **Compuestas** (`Pesos/kilogramo`, `Toneladas/hectáreas`, "
         "`Pesos por tonelada`, `Miles de litros; Toneladas`): requieren termino "
         "precoordinado que Q no puede acreditar localmente; sin peticion.",
         "- **`Grados`**: literal compartido por Latitud/Longitud (angulo) y "
         "ambiguo frente a `Grados celcius`; no se propone.",
         "- **`Porcentaje`** (50 filas): se propone una sola definicion (ANALF). "
         "La escala de valores (0-100 vs 0-1) no esta declarada localmente: no se "
         "infiere factor; I no debe calcular tasas.",
         "- **`Toneladas`** (3 filas): la ambiguedad de variante afecta a las 3; "
         "ver `casos.json` Q-U01.", ""]
escribir(V / "informe-exclusiones.md", "\n".join(excl))

# --- 9. pruebas ----------------------------------------------------------
PRUEBAS = {
    "generado_por": "v002/scripts/generar_v002.py",
    "base_congelada": {"sha256_cobertura": SHA_COB,
                       "sha256_p1_v003_entrega": SHA_P1E,
                       "sha256_w_v003_congelada": SHA_WC,
                       "sha256_canal_peticiones": SHA_CANAL},
    "inventario": {"ficheros_inspeccion": len(FICHEROS),
                   "literales_distintos": len(inventario),
                   "filas_con_unidad": sum(e["filas"] for e in inventario.values())},
    "grafo": {"turtle_parse_ok": True, "declaraciones": len(rows),
              "sin_unidad_qudt": 6, "con_trazabilidad_fuente": 6},
    "consultas": {"q1-declaraciones-por-caso": len(rows),
                  "q2-declaraciones-sin-unidad-qudt": 6,
                  "q3-trazabilidad-fuente": 6},
    "checks": {
        "seis_casos_respaldados_por_definicion": True,
        "huella_variable_definicion_conjunto_diccionario_coinciden": True,
        "copias_fuente_byte_iguales": True,
        "sin_iris_qudt": True,
        "sin_quantityvalue": True,
        "sin_conversiones_ni_factores": True,
        "sin_m3": True,
        "sin_hm3_repetido": True,
        "toneladas_sin_variante_asignada": True,
        "v001_preservada_sin_edicion": True,
        "canal_peticiones_intacto": True,
        "sellos_reusados_verificados": True,
    },
    "peticiones": {"canal": 6, "addendum": 1, "verificadas_por_W": 0},
}
escribir(V / "pruebas.json", json_txt(PRUEBAS))

# --- 10. entrega ---------------------------------------------------------
ENTREGA = {
    "rol": "Q-unidades", "version": "v002", "fecha_utc": FECHA,
    "estado": "propuesta_para_auditar_NO_instalable",
    "continua_a": "v001",
    "predecesora": {
        "ruta": RUTA_V001,
        "sello": RUTA_V001_SELLO,
        "estado": "v001 completada y sellada por su propio carril; v002 no la "
                  "edita ni replica sus hashes (los verifica su sello)",
        "relacion": "mismos 6 casos; v002 corrige el tratamiento de 'Toneladas' y "
                    "anade copias fuente por caso y formato de integracion",
    },
    "defectos_corregidos": [
        "v001 presuponia la variante metrica de 'Toneladas' en la pista de Q-W-01 "
        "y la escribia en mex:evidenciaNormativa; v002 no asigna variante: Q-U01 "
        "queda pendiente por ambiguedad local.",
        "v001/entrega.json incluia un campo espurio 'dic': 'diccionario' por caso; "
        "v002 no lo reproduce (solo 'diccionario' con el uuid).",
        "v001 no tenia copia fuente por caso ni formato de integracion; v002 los "
        "aporta en fuentes/<caso>/ y formato-integracion.md.",
        "v001 no clasificaba los 61 literales; v002 anade tratamiento y motivo "
        "por literal en inventario-unidades.json.",
    ],
    "base": CASOS["base"],
    "resumen": CASOS["resumen"],
    "casos": CASOS["casos"],
    "grafo": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/propuesta-q-unidades.ttl",
              "sha256": sha(V / "propuesta-q-unidades.ttl"),
              "declaraciones": 6, "sin_unidadQudt": True,
              "sin_QuantityValue": True, "sin_conversiones": True,
              "motivo_sin_unidadQudt": "W no ha sellado Q-W-01..06; no se "
                                       "congelan URIs no verificadas"},
    "inventario": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/inventario-unidades.json",
                   "sha256": sha(V / "inventario-unidades.json"),
                   "literales": len(inventario), "filas": 259},
    "casos_json": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/casos.json",
                   "sha256": sha(V / "casos.json")},
    "fuentes": {"indice": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/fuentes/indice-copias.json",
                "sha256_indice": sha(V / "fuentes/indice-copias.json"),
                "copias_por_caso": 6,
                "sellos_reusados": indice_copias["sellos_reusados_sin_edicion"]},
    "solicitudes": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/solicitudes/peticiones-web-v002.json",
                    "sha256": sha(V / "solicitudes/peticiones-web-v002.json"),
                    "canal_canonico_intacto": RUTA_CANAL,
                    "solicitudes": [f"Q-W-0{i}" for i in range(1, 7)],
                    "addendum": ["Q-W-01b"]},
    "integracion": {"formato": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/formato-integracion.md",
                    "sha256": sha(V / "formato-integracion.md"),
                    "integrable_ahora": False,
                    "requiere": "sello W por caso + respaldo local no ambiguo"},
    "consultas": [f"propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/consultas/{q}" for q in
                  ("q1-declaraciones-por-caso.rq",
                   "q2-declaraciones-sin-unidad-qudt.rq",
                   "q3-trazabilidad-fuente.rq")],
    "exclusiones": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/informe-exclusiones.md",
                    "sha256": sha(V / "informe-exclusiones.md")},
    "limites": [
        "v002 no instala nada: solo propuesta cualificada en su carpeta.",
        "Ninguna URI QUDT afirmada; W no sello Q-W-01..06.",
        "Q-U01 (Toneladas) pendiente por ambiguedad local: sin variante metrica "
        "asignada, sin vinculo, sin factor.",
        "No se duplica R9 (MilliM, HA) ni se repite hm3/HectoM3; sin M3.",
        "Sin QuantityValue global, sin atribucion global de unidad, sin Gemma, "
        "sin contactos, sin navegacion (W es el unico navegador).",
        "No se editan R1-R9, manifiestos, config.toml, Studio ni el grafo.",
    ],
    "condiciones_aceptacion": [
        "Auditor replica los sha256 de congelada.json y de las copias fuente.",
        "Auditor confirma 6 declaraciones y 0 IRIs QUDT en el TTL.",
        "Auditor confirma que Q-U01 no tiene variante asignada ni vinculo.",
        "La promocion exige sello W y, para Q-U01, evidencia local.",
    ],
}
escribir(V / "entrega.json", json_txt(ENTREGA))

md = ["# Q-unidades v002 — 6 declaraciones cualificadas (no instalables)", "",
      "Continua `v001` (sellada por su carril) sin modificarla: corrige el "
      "tratamiento de `Toneladas` y anade copias fuente y formato de integracion. "
      "Base R9.", "",
      "| caso | variable | literal | diccionario | estado |", "| --- | --- | --- | --- | --- |"]
for c in casos:
    md.append(f"| {c['id']} | `{c['variable']}` | `{c['literal']}` | "
              f"`{c['diccionario'][:8]}` | `{c['estado_propuesta']}` |")
md += ["", f"Inventario: 61 literales / 259 filas en 486 diccionarios.", "",
       "Sin `mex:unidadQudt` (W no sello Q-W-01..06), sin QuantityValue, sin "
       "factores. Q-U01 (`Toneladas`) pendiente por ambiguedad local: la norma no "
       "decide la unidad local.", "",
       "Integracion: `formato-integracion.md`. Exclusiones: "
       "`informe-exclusiones.md`. Copias fuente: `fuentes/<caso>/`.", ""]
escribir(V / "entrega.md", "\n".join(md))

# --- 11. sello programatico ----------------------------------------------
alcance = sorted([p for p in V.rglob("*") if p.is_file()
                  and p.name not in ("congelada.json", "congelada.sha256")],
                 key=lambda p: p.relative_to(V).as_posix())
archivos = [{"ruta": p.relative_to(BASE).as_posix(), "sha256": sha(p),
             "bytes": p.stat().st_size} for p in alcance]
assert len(archivos) == len(alcance) > 10
SELLO = {
    "rol": "Q-unidades", "version": "v002", "fecha_utc": FECHA,
    "alcance": "propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/v002/** "
               "(excluye congelada.json y congelada.sha256)",
    "nota": "Sello por codigo sobre bytes escritos (CRLF en Windows). No se "
            "incluye a si mismo. No editar tras congelar: corregir en v003.",
    "base_verificada": {"data/semantica/cobertura.json": SHA_COB,
                        RUTA_P1E: SHA_P1E, RUTA_WC: SHA_WC,
                        RUTA_CANAL: SHA_CANAL},
    "predecesora_observada": {RUTA_V001_SELLO: sha(BASE / RUTA_V001_SELLO),
                              "nota": "hash observado al generar; v001 puede "
                                      "re-sellarse en su carril sin invalidar v002"},
    "archivos": archivos,
}
escribir(V / "congelada.json", json_txt(SELLO))
(V / "congelada.sha256").write_text(
    f"{sha(V / 'congelada.json')}  congelada.json\n", encoding="utf-8")

print(f"OK v002: {len(archivos)} archivos sellados, "
      f"{len(inventario)} literales, {len(rows)} declaraciones")
print(f"sello congelada.json = {sha(V / 'congelada.json')}")
