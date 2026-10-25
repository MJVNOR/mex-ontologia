"""Q-unidades v003: TTL integrable de 5 declaraciones con vinculo QUDT.

Parte de W-estandares v002 YA SELLADO (validado por codigo, sin navegar) y de
Q-unidades v002 sellado. Escribe EXCLUSIVAMENTE bajo Q-unidades/v003/.

- Valida SHA del sello W v002 (12 archivos), los 6 sujetos Q-W-01..06 y que
  cada evidencia normativa declare el mismo sujeto http.
- Aplica vinculo QUDT SOLO a Q-U02..Q-U06, con base documentada por caso.
- Q-U01 'Toneladas' queda excluida: W acredita TON_Metric pero declara que el
  literal local no elige variante; la variante exige evidencia local.
- hm3/HectoM3 sigue excluida (agotada). Sin M3, sin factores, sin QuantityValue.
- Copias locales y normativas por caso, con SHA exactos.
- evidenciaNormativa con el mismo patron que R9 (P1-qudt/v003): ruta + sha256 de
  la evidencia y del sello. Nada inventado.
"""
import hashlib
import json
import pathlib
import shutil

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
EJ = BASE / "propuestas/ampliacion-post-r9/ejecucion-20261024"
Q = EJ / "Q-unidades"
V = Q / "v003"
W = EJ / "W-estandares/v002"
FECHA = "2026-10-24"

RUTA_W_ENTREGA = W.relative_to(BASE).as_posix() + "/entrega.json"
RUTA_W_SELLO = W.relative_to(BASE).as_posix() + "/congelada.json"
RUTA_V002_SELLO = Q.relative_to(BASE).as_posix() + "/v002/congelada.json"
RUTA_CANAL = Q.relative_to(BASE).as_posix() + "/peticiones-web.json"
RUTA_COB = "data/semantica/cobertura.json"
RUTA_R9 = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/entrega.json"
RUTA_R9_TTL = "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v003/propuesta-qudt.ttl"

SHA_V002 = "e103701ebd1614d6b323fcb293705c9960fa0637732914370f9a2737d1c9be30"
SHA_COB = "1486fcae52a210c803e1173aa0ecbfddd40d1e66a3147aebb1c64fdfa39dfb31"
SHA_R9 = "7a5c7441465d00611475a2b32b3e8faa396a22ee1dfb0886de297031028330c8"
SHA_CANAL = "00921b383e537dda8cbbeea1d31aef9bb2ff6d3ab0e57ab644536bfb17643452"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def huella_fila(fila):
    return hashlib.sha256(json.dumps(fila, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def escribir(ruta, texto):
    ruta = pathlib.Path(ruta)
    assert V in ruta.parents, f"escritura fuera de v003: {ruta}"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


def json_txt(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1)


# --- 0. base sellada ------------------------------------------------------
assert sha(BASE / RUTA_V002_SELLO) == SHA_V002, "v002 no es el sello esperado"
assert sha(BASE / RUTA_COB) == SHA_COB
assert sha(BASE / RUTA_R9) == SHA_R9
assert sha(BASE / RUTA_CANAL) == SHA_CANAL
v002 = json.loads((BASE / RUTA_V002_SELLO).read_text(encoding="utf-8"))
assert v002["rol"] == "Q-unidades" and v002["version"] == "v002"

# --- 1. validacion del sello W v002 --------------------------------------
w_sello = json.loads((BASE / RUTA_W_SELLO).read_text(encoding="utf-8"))
assert w_sello["rol"] == "W-estandares" and w_sello["version"] == "v002"
validacion_archivos = []
for a in w_sello["archivos"]:
    p = BASE / a["ruta"]
    assert p.is_file(), a["ruta"]
    real = sha(p)
    assert real == a["sha256"], f"hash distinto: {a['ruta']}"
    assert p.stat().st_size == a["bytes"], f"bytes distintos: {a['ruta']}"
    validacion_archivos.append({"ruta": a["ruta"], "sha256": real,
                                "bytes": a["bytes"], "coincide": True})
assert len(validacion_archivos) == 12, len(validacion_archivos)

w = json.loads((BASE / RUTA_W_ENTREGA).read_text(encoding="utf-8"))
assert sha(BASE / RUTA_W_ENTREGA) == next(
    a["sha256"] for a in w_sello["archivos"] if a["ruta"] == RUTA_W_ENTREGA)
assert w["norma"]["version"] == "3.5.3"
assert len(w["resultados"]) == 6

ESPERADO = {
    "Q-W-01": ("Q-U01", "http://qudt.org/vocab/unit/TON_Metric"),
    "Q-W-02": ("Q-U02", "http://qudt.org/vocab/unit/KiloGM"),
    "Q-W-03": ("Q-U03", "http://qudt.org/vocab/unit/MegaW"),
    "Q-W-04": ("Q-U04", "http://qudt.org/vocab/unit/GigaW-HR"),
    "Q-W-05": ("Q-U05", "http://qudt.org/vocab/unit/PERCENT"),
    "Q-W-06": ("Q-U06", "http://qudt.org/vocab/unit/DEG_C"),
}
sujetos = {}
for r in w["resultados"]:
    pid = r["id"]
    assert pid in ESPERADO, pid
    caso, sujeto = ESPERADO[pid]
    assert r["caso"] == caso, (pid, r["caso"])
    assert r["estado"] == "verificado", pid
    assert r["sujeto_rdf"] == sujeto, (pid, r["sujeto_rdf"])
    assert r["sujeto_rdf"].startswith("http://qudt.org/vocab/unit/"), pid
    assert r["url"] == r["sujeto_rdf"].replace("http://", "https://"), pid
    assert r["version"] == "3.5.3", pid
    ev = BASE / r["evidencia"]["ruta"]
    assert sha(ev) == r["evidencia"]["sha256"], pid
    assert ev.stat().st_size == r["evidencia"]["bytes"], pid
    assert any(a["ruta"] == r["evidencia"]["ruta"]
               and a["sha256"] == r["evidencia"]["sha256"]
               for a in w_sello["archivos"]), f"evidencia no sellada: {pid}"
    texto = ev.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    assert lineas[1] == f"IRI canonica del sujeto RDF: {sujeto}", (pid, lineas[1])
    assert "Version normativa: QUDT 3.5.3" in texto, pid
    assert r["simbolo"] in texto, (pid, r["simbolo"])
    assert "isDefinedBy" in texto and "3.5.3" in texto, pid
    sujetos[pid] = {"caso": caso, "sujeto": sujeto, "version": r["version"],
                    "simbolo": r["simbolo"], "etiqueta_es": r["etiqueta_es"],
                    "etiqueta_en": r["etiqueta_en"],
                    "evidencia": r["evidencia"]["ruta"],
                    "sha256_evidencia": r["evidencia"]["sha256"],
                    "nota_w": r["nota"]}
assert len({s["sujeto"] for s in sujetos.values()}) == 6

# --- 2. casos: vinculo aplicado solo a Q-U02..Q-U06 ----------------------
cob = json.loads((BASE / RUTA_COB).read_text(encoding="utf-8"))
por_huella = {v["huella_fila_diccionario"]: v for v in cob["variables"]
              if v.get("huella_fila_diccionario")}

SPEC = [
    {"id": "Q-U02", "dic": "a4eb0b8b-d6c6-44b8-b00a-f5f45c1875a5",
     "literal": "Kilogramos", "concepto": "peso-promedio-cabeza-subasta",
     "slug": "declaracion-pesoprom-kilogramos", "w": "Q-W-02",
     "base": "simbolo kg + etiqueta @es 'Kilogramo' en QUDT 3.5.3",
     "transferencia": "sin transferencia: la fila es la variable medida"},
    {"id": "Q-U03", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "MW", "concepto": "unidad-capacidad-planta-electrica",
     "slug": "declaracion-capacidad-mw", "w": "Q-W-03",
     "base": "simbolo MW + etiqueta @es 'Megavatio' en QUDT 3.5.3",
     "transferencia": "NO se transfiere a 'Capacidad Autorizada' ni a otras "
                      "filas del diccionario: solo la fila 'Unidad de Medida'"},
    {"id": "Q-U04", "dic": "a6cdb7ad-ec32-44aa-851d-684947df4243",
     "literal": "GWh", "concepto": "unidad-generacion-planta-electrica",
     "slug": "declaracion-generacion-gwh", "w": "Q-W-04",
     "base": "uneceCommonCode GWH + ucumCode GW.h + FactorUnit GigaW x HR; el "
             "simbolo QUDT es GW\u00b7h y NO 'GWh': la diferencia se conserva, "
             "no se declara alias",
     "transferencia": "NO se transfiere a 'Generacion Estimada' ni a otras "
                      "filas del diccionario: solo la fila 'Unidad de Medida'"},
    {"id": "Q-U05", "dic": "251309e5-0309-46ed-9711-77a1dd408eeb",
     "literal": "Porcentaje", "concepto": "porc-analfabetismo-localidad",
     "slug": "declaracion-analf-porcentaje", "w": "Q-W-05",
     "base": "simbolo % + etiqueta @en 'Percent'; QUDT no publica @es (documentado "
             "por W); conversionMultiplier 0.01 pertenece al termino y no se "
             "aplica a datos locales",
     "transferencia": "sin transferencia: la fila es la variable medida"},
    {"id": "Q-U06", "dic": "33d0a99e-c721-496f-a05e-07646e9ae42a",
     "literal": "Grados celcius", "concepto": "temperatura-caso",
     "slug": "declaracion-temperatura-grados", "w": "Q-W-06",
     "base": "simbolo \u00b0C + etiqueta @es 'Grado Celsius'; el literal local "
             "conserva su error ortografico, no se normaliza",
     "transferencia": "sin transferencia: la fila es la variable medida"},
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
    assert v["diccionario"] == s["dic"] and v["variable"] == fila["Nombre variable"]
    assert v["definicion_iri"].endswith(f"%2F{idx}"), s["id"]
    suj = sujetos[s["w"]]
    assert suj["caso"] == s["id"]

    copia_local = V / "fuentes" / s["id"] / f"{s['dic']}.json"
    copia_local.parent.mkdir(parents=True, exist_ok=True)
    origen = BASE / f"data/portal/inspecciones/{s['dic']}.json"
    shutil.copy2(origen, copia_local)
    assert sha(copia_local) == sha(origen)

    copia_norm = V / "normativa" / s["id"] / pathlib.Path(suj["evidencia"]).name
    copia_norm.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE / suj["evidencia"], copia_norm)
    assert sha(copia_norm) == suj["sha256_evidencia"]

    casos.append({
        "id": s["id"], "literal": s["literal"], "huella_fila": h,
        "variable": fila["Nombre variable"], "diccionario": s["dic"],
        "conjunto": v["conjunto"], "definicion_iri": v["definicion_iri"],
        "variable_documentada_iri": v["iri"], "concepto": v["concepto"],
        "regla": v["regla"], "indice_definicion": idx,
        "estado_cobertura": v["estado"], "estado": "integrable",
        "peticion_w": s["w"], "slug": s["slug"],
        "sujeto_qudt": suj["sujeto"], "version_qudt": suj["version"],
        "simbolo_qudt": suj["simbolo"], "etiqueta_es_qudt": suj["etiqueta_es"],
        "etiqueta_en_qudt": suj["etiqueta_en"],
        "base_del_vinculo": s["base"], "transferencia": s["transferencia"],
        "evidencia_normativa": {
            "ruta": suj["evidencia"], "sha256": suj["sha256_evidencia"],
            "sello": RUTA_W_SELLO, "sha256_sello": sha(BASE / RUTA_W_SELLO),
        },
        "fuente_local": {
            "ruta": origen.relative_to(BASE).as_posix(), "sha256": sha(origen),
            "url": d["fuente"],
            "localizador": f"{fila['Nombre variable']}, 'Unidad de medida' = "
                           f"'{s['literal']}', definiciones[{idx}], huella {h}",
        },
        "copias": {
            "local": {"ruta": copia_local.relative_to(BASE).as_posix(),
                      "sha256": sha(copia_local), "bytes": copia_local.stat().st_size},
            "normativa": {"ruta": copia_norm.relative_to(BASE).as_posix(),
                          "sha256": sha(copia_norm), "bytes": copia_norm.stat().st_size},
        },
        "fila": fila,
    })

# --- 3. TTL integrable: 5 declaraciones con unidadQudt -------------------
def bloque(c):
    return (
        f"<https://example.org/mex-ontologi/propuesta/q-unidades/v003/{c['slug']}>"
        f" a mex:UnidadDeclarada ;\n"
        f"    rdfs:label \"{c['variable']}: unidad {c['literal']}\"@es ;\n"
        f"    mex:variableDocumentada <{c['variable_documentada_iri']}> ;\n"
        f"    mex:definicionFuente <{c['definicion_iri']}> ;\n"
        f"    mex:conjuntoFuente \"{c['conjunto']}\" ;\n"
        f"    mex:diccionarioFuente \"{c['diccionario']}\" ;\n"
        f"    mex:unidadLiteral \"{c['literal']}\" ;\n"
        f"    mex:unidadQudt <{c['sujeto_qudt']}> ;\n"
        f"    mex:evidenciaNormativa \"{c['peticion_w']}: "
        f"{c['evidencia_normativa']['ruta']} "
        f"sha256={c['evidencia_normativa']['sha256']} ; "
        f"sello W v002 {RUTA_W_SELLO} "
        f"sha256={c['evidencia_normativa']['sha256_sello']}\" ;\n"
        f"    prov:wasDerivedFrom <{c['fuente_local']['url']}> , "
        f"<{c['sujeto_qudt']}> ;\n"
        f"    rdfs:comment \"Alcance: SOLO variable {c['variable']} de ESA "
        f"definicion del diccionario {c['diccionario']}. {c['transferencia']}. "
        f"Sin atribucion global, sin valores, sin factores ni conversiones.\"@es .\n")


TTL = ("@prefix mex: <https://example.org/mex-ontologi/vocab/> .\n"
       "@prefix prov: <http://www.w3.org/ns/prov#> .\n"
       "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n"
       "# Q-unidades v003 (INTEGRABLE): 5 declaraciones con vinculo QUDT\n"
       "# verificado en el sello W-estandares v002.\n"
       "# Sin QuantityValue, sin factores, sin conversiones, sin alias.\n"
       "# EXCLUIDAS (sin triple): Q-U01 'Toneladas' (W acredita TON_Metric pero\n"
       "#   el literal local no elige variante; requiere evidencia local) y\n"
       "#   hm3/Hectometros cubicos (busqueda agotada; sin M3 ni factor).\n\n"
       + "\n".join(bloque(c) for c in casos))
escribir(V / "propuesta-q-unidades.ttl", TTL)

from rdflib import Graph, URIRef  # noqa: E402

g = Graph()
g.parse(data=TTL, format="turtle")
Q1 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT ?d ?var ?lit ?u ?def WHERE { ?d a mex:UnidadDeclarada ;\n"
      "  mex:variableDocumentada ?var ; mex:unidadLiteral ?lit ;\n"
      "  mex:definicionFuente ?def ; mex:unidadQudt ?u } ORDER BY ?d")
rows = list(g.query(Q1))
assert len(rows) == 5, len(rows)
assert {str(r[2]) for r in rows} == {c["literal"] for c in casos}
assert {str(r[3]) for r in rows} == {c["sujeto_qudt"] for c in casos}
assert all(str(r[3]).startswith("http://qudt.org/vocab/unit/") for r in rows)
Q2 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT (COUNT(?d) AS ?n) WHERE { ?d a mex:UnidadDeclarada .\n"
      "  FILTER NOT EXISTS { ?d mex:unidadQudt ?u } }")
assert int(list(g.query(Q2))[0][0]) == 0
Q3 = ("PREFIX mex: <https://example.org/mex-ontologi/vocab/>\n"
      "SELECT ?d ?ev WHERE { ?d a mex:UnidadDeclarada ; mex:evidenciaNormativa ?ev }"
      " ORDER BY ?d")
assert len(list(g.query(Q3))) == 5
terminos = set(g.subjects()) | set(g.predicates()) | set(g.objects())
uris = {str(t) for t in terminos if isinstance(t, URIRef)}
assert not any("https://qudt.org" in u for u in uris), "sujetos deben ser http"
assert not any("QuantityValue" in u for u in uris)
assert not any("unit/M3" in u for u in uris)
assert not any("TON_Metric" in u for u in uris), "Q-U01 no se vincula"
assert not any("conversion" in u.lower() for u in uris)
escribir(V / "consultas/q1-declaraciones-integradas.rq", Q1)
escribir(V / "consultas/q2-sin-unidad-qudt.rq", Q2)
escribir(V / "consultas/q3-evidencia-normativa.rq", Q3)

# --- 4. validacion y exclusiones -----------------------------------------
escribir(V / "validacion-w.json", json_txt({
    "nota": "Validacion por codigo del sello W-estandares v002: hashes de los 12 "
            "archivos, sujetos http, version 3.5.3 y evidencia por termino. "
            "Sin navegacion (Q no navega).",
    "sello_w": {"ruta": RUTA_W_SELLO, "sha256": sha(BASE / RUTA_W_SELLO),
                "entrega": {"ruta": RUTA_W_ENTREGA,
                            "sha256": sha(BASE / RUTA_W_ENTREGA)}},
    "archivos_verificados": validacion_archivos,
    "sujetos": sujetos,
    "resultado": {"archivos": len(validacion_archivos), "coinciden": 12,
                  "sujetos_http": 6, "version": "3.5.3",
                  "sujetos_distintos": 6},
}))

escribir(V / "exclusiones.md", "\n".join([
    "# Q-unidades v003 â€” exclusiones (sin triple en el TTL)", "",
    "## Q-U01 `Toneladas` (PRODTON, 94215f51) â€” variante local no acreditada", "",
    "W v002 verifico `http://qudt.org/vocab/unit/TON_Metric` y dejo constancia de "
    "que el literal local no elige variante. El corpus usa `Toneladas` sin "
    "calificativo en 3 definiciones de 2 diccionarios (agricultura y pesca). "
    "Asignar TON_Metric seria decidir la unidad local desde la norma: no se hace.",
    "",
    "Reapertura: evidencia local (documentacion del recurso o del publicador) que "
    "declare tonelada metrica para esa definicion.",
    "",
    "## hm3 / `HectÃ³metros cÃºbicos` (1 fila) â€” busqueda agotada", "",
    "HectoM3: 404 + ausente del indice QUDT 3.5.3 (sello W v003 de la ronda "
    "anterior). No se repite la busqueda y no se sustituye por M3 ni por factor "
    "alguno.",
    "",
    "## Fuera de alcance de v003", "",
    "- Los otros 49 filas con literal `Porcentaje` y las otras 2 con `Toneladas`: "
    "v003 solo publica los 5 casos con vinculo verificado; el inventario completo "
    "esta en `v002/inventario-unidades.json` (sellado).",
    "- Compuestas, moneda, conteos, codigos y referencias indirectas: ver "
    "`v002/informe-exclusiones.md`.",
    "",
]))

# --- 5. entrega ----------------------------------------------------------
ENTREGA = {
    "rol": "Q-unidades", "version": "v003", "fecha_utc": FECHA,
    "estado": "integrable_para_auditar",
    "continua_a": ["v001", "v002"],
    "predecesoras": {
        "q_v002": {"sello": RUTA_V002_SELLO, "sha256": SHA_V002,
                   "nota": "v002 sellado intacto; v003 no lo edita"},
        "w_v002": {"sello": RUTA_W_SELLO, "sha256": sha(BASE / RUTA_W_SELLO),
                   "entrega": RUTA_W_ENTREGA,
                   "sha256_entrega": sha(BASE / RUTA_W_ENTREGA),
                   "validacion": "Q-unidades/v003/validacion-w.json"},
    },
    "base": {"release": "R9", "sha256_cobertura": SHA_COB,
             "informe": "reports/ronda-9.json",
             "sha256_informe": sha(BASE / "reports/ronda-9.json")},
    "resumen": {"declaraciones": 5, "con_unidad_qudt": 5,
                "excluidas": ["Q-U01", "hm3"],
                "sujetos_http_verificados": 6, "verificadas_no_aplicadas": 1},
    "casos": casos,
    "grafo": {"archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/"
                         "Q-unidades/v003/propuesta-q-unidades.ttl",
              "sha256": sha(V / "propuesta-q-unidades.ttl"),
              "declaraciones": 5, "con_unidadQudt": 5,
              "sin_QuantityValue": True, "sin_conversiones": True,
              "sin_alias": True,
              "excluidas_sin_triple": ["Q-U01 Toneladas", "hm3"]},
    "fuentes": {"indice": "propuestas/ampliacion-post-r9/ejecucion-20261024/"
                          "Q-unidades/v003/fuentes/indice-copias.json",
                "sha256_indice": None},
    "integracion": {"destino": "carril I (escritor central unico)",
                    "guia": "propuestas/ampliacion-post-r9/ejecucion-20261024/"
                            "Q-unidades/v003/integracion.md",
                    "requiere_cambios_de_vocabulario": False,
                    "requiere_cambios_de_shapes": False,
                    "triples_nuevos": 5,
                    "predicados": ["mex:UnidadDeclarada (rdf:type)",
                                   "mex:variableDocumentada", "mex:definicionFuente",
                                   "mex:conjuntoFuente", "mex:diccionarioFuente",
                                   "mex:unidadLiteral", "mex:unidadQudt",
                                   "mex:evidenciaNormativa", "prov:wasDerivedFrom",
                                   "rdfs:label", "rdfs:comment"]},
    "limites": [
        "v003 solo escribe en Q-unidades/v003/; no edita v001, v002 ni W v002.",
        "Q-U01 y hm3 quedan sin triple: la norma no decide la unidad local.",
        "Sin QuantityValue, sin factores, sin conversiones, sin alias por parecido.",
        "Sin navegacion: la validacion normativa usa el sello W v002 en disco.",
        "No se tocan R1-R9, manifiestos, config.toml, ontologia, shapes, grafo ni Studio.",
    ],
    "condiciones_aceptacion": [
        "Auditor replica los sha256 de congelada.json y de las 10 copias.",
        "Auditor confirma 5 declaraciones, todas con sujeto http y evidencia sellada.",
        "Auditor confirma que Q-U01 y hm3 no aparecen en el TTL.",
        "I integra el TTL tal cual; sin cambios de vocabulario ni de shapes.",
    ],
}
indice = {
    "nota": "Copias byte a byte por caso: fuente local (inspeccion) y evidencia "
            "normativa sellada por W. sha256(copia) == sha256(origen).",
    "locales": [{"caso": c["id"], "origen": c["fuente_local"]["ruta"],
                 "sha256_origen": c["fuente_local"]["sha256"],
                 "copia": c["copias"]["local"]["ruta"],
                 "sha256_copia": c["copias"]["local"]["sha256"],
                 "bytes": c["copias"]["local"]["bytes"], "iguales": True}
                for c in casos],
    "normativas": [{"caso": c["id"],
                    "origen": c["evidencia_normativa"]["ruta"],
                    "sha256_origen": c["evidencia_normativa"]["sha256"],
                    "copia": c["copias"]["normativa"]["ruta"],
                    "sha256_copia": c["copias"]["normativa"]["sha256"],
                    "bytes": c["copias"]["normativa"]["bytes"], "iguales": True}
                   for c in casos],
    "sello_w": {"ruta": RUTA_W_SELLO, "sha256": sha(BASE / RUTA_W_SELLO),
                "archivos_verificados": 12},
}
escribir(V / "fuentes/indice-copias.json", json_txt(indice))
ENTREGA["fuentes"]["sha256_indice"] = sha(V / "fuentes/indice-copias.json")
escribir(V / "entrega.json", json_txt(ENTREGA))

escribir(V / "integracion.md", "\n".join([
    "# Q-unidades v003 â€” integracion (carril I)", "",
    "## Payload", "",
    "`propuesta-q-unidades.ttl`: 5 `mex:UnidadDeclarada` con `mex:unidadQudt` y "
    "`mex:evidenciaNormativa`. Es el TTL integrable; no requiere cambios de "
    "vocabulario ni de shapes (todos los predicados ya existen en "
    "`data/portal/ampliacion.ttl`).", "",
    "| caso | variable | literal | sujeto QUDT |", "| --- | --- | --- | --- |",
    *[f"| {c['id']} | `{c['variable']}` | `{c['literal']}` | "
      f"`{c['sujeto_qudt']}` |" for c in casos], "",
    "## Pasos", "",
    "1. Dos auditorias independientes sobre los bytes de v003 y del sello W v002 "
    "(`validacion-w.json` ya replica sus 12 hashes).",
    "2. Integrar el TTL tal cual en el grafo del portal; una sola sincronizacion.",
    "3. Ejecutar `consultas/q1..q3` y el SHACL del portal; comprobar que no se "
    "altera nada ajeno.",
    "4. Respaldar Studio antes de sincronizar, como en R9.", "",
    "## Prohibiciones", "",
    "- No agregar Q-U01 (`Toneladas`) ni hm3: no estan en el TTL y no deben "
    "aparecer por convencion.",
    "- No completar unidades de filas vecinas: cada declaracion alcanza solo su "
    "definicion. En U03/U04, solo la fila `Unidad de Medida`; no se transfiere a "
    "`Capacidad Autorizada` ni a `Generacion Estimada`.",
    "- Sin `QuantityValue`, sin factores, sin conversiones, sin alias "
    "(`GWh` != simbolo QUDT `GW\u00b7h`; la diferencia se conserva).",
    "",
]))

escribir(V / "entrega.md", "\n".join([
    "# Q-unidades v003 â€” 5 declaraciones integrables con vinculo QUDT", "",
    "Valida el sello W v002 (12 archivos, 6 sujetos http, QUDT 3.5.3) y aplica "
    "vinculo solo donde las fuentes lo avalan.", "",
    "| caso | variable | literal | sujeto QUDT | evidencia |",
    "| --- | --- | --- | --- | --- |",
    *[f"| {c['id']} | `{c['variable']}` | `{c['literal']}` | "
      f"`{c['sujeto_qudt']}` | `{c['peticion_w']}` |" for c in casos], "",
    "**Excluidas:** Q-U01 `Toneladas` (W acredita TON_Metric pero el literal local "
    "no elige variante: requiere evidencia local) y hm3/Hectometros cubicos "
    "(busqueda agotada; sin M3 ni factor).", "",
    "Integracion: `integracion.md`. Copias y hashes: `fuentes/indice-copias.json` "
    "y `validacion-w.json`.", "",
]))

# --- 6. pruebas ----------------------------------------------------------
escribir(V / "pruebas.json", json_txt({
    "generado_por": "v003/scripts/generar_v003.py",
    "w_v002": {"sello_sha256": sha(BASE / RUTA_W_SELLO),
               "archivos_replicados": 12, "sujetos_http": 6,
               "version": "3.5.3", "evidencias_por_sujeto": 6},
    "grafo": {"turtle_parse_ok": True, "declaraciones": 5,
              "con_unidad_qudt": 5, "sin_unidad_qudt": 0,
              "con_evidencia_normativa": 5},
    "consultas": {"q1-declaraciones-integradas": 5,
                  "q2-sin-unidad-qudt": 0,
                  "q3-evidencia-normativa": 5},
    "copias": {"locales": 5, "normativas": 5, "sha_iguales": 10},
    "checks": {
        "sello_w_v002_replicado": True,
        "seis_sujetos_http_verificados": True,
        "cinco_vinculos_aplicados": True,
        "toneladas_excluida": True,
        "hm3_excluida": True,
        "sin_quantityvalue": True,
        "sin_factores_ni_conversiones": True,
        "sin_alias": True,
        "u03_u04_solo_fila_unidad_de_medida": True,
        "evidencia_normativa_con_ruta_y_sha": True,
        "v002_intacto": True,
    },
}))

# --- 7. sello ------------------------------------------------------------
alcance = sorted([p for p in V.rglob("*") if p.is_file()
                  and p.name not in ("congelada.json", "congelada.sha256")],
                 key=lambda p: p.relative_to(V).as_posix())
archivos = [{"ruta": p.relative_to(BASE).as_posix(), "sha256": sha(p),
             "bytes": p.stat().st_size} for p in alcance]
assert len(archivos) == len(alcance) >= 12
escribir(V / "congelada.json", json_txt({
    "rol": "Q-unidades", "version": "v003", "fecha_utc": FECHA,
    "alcance": V.relative_to(BASE).as_posix() +
               "/** (excluye congelada.json y congelada.sha256)",
    "nota": "Sello por codigo sobre bytes escritos (CRLF en Windows). No se "
            "incluye a si mismo. No editar tras congelar: corregir en v004.",
    "base_verificada": {RUTA_COB: SHA_COB, RUTA_R9: SHA_R9,
                        RUTA_CANAL: SHA_CANAL, RUTA_V002_SELLO: SHA_V002},
    "predecesora_w_observada": {
        RUTA_W_SELLO: sha(BASE / RUTA_W_SELLO),
        RUTA_W_ENTREGA: sha(BASE / RUTA_W_ENTREGA),
        "nota": "W v002 sellado; sus 12 hashes se replican en validacion-w.json",
    },
    "archivos": archivos,
}))
(V / "congelada.sha256").write_text(
    f"{sha(V / 'congelada.json')}  congelada.json\n", encoding="utf-8")

print(f"OK v003: {len(archivos)} archivos, 5 declaraciones, "
      f"W v002 {sha(BASE / RUTA_W_SELLO)[:12]}")
print(f"sello congelada.json = {sha(V / 'congelada.json')}")
