"""Construye entrega P1-QUDT v001. Solo escribe bajo P1-qudt/."""
import json, hashlib, pathlib, datetime

BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi")
MIO = BASE / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt"
V = MIO / "v001"
(V / "consultas").mkdir(parents=True, exist_ok=True)
(V / "fixtures").mkdir(parents=True, exist_ok=True)

def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def insp(dic):
    return json.loads((BASE / f"data/portal/inspecciones/{dic}.json").read_text(encoding="utf-8"))

CASOS = [
    {"id": "P1-Q1", "concepto": "precipitacion-diaria", "variable": "Precipitacion_mm",
     "diccionario": "6713de4e-1e2b-447d-8000-f6ceaabd8473",
     "conjunto": "8b4edefe-cb1a-401c-90c6-05548779defd", "titulo": "Registro de Precipitaciones Municipales",
     "definicion_iri": "https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6",
     "huella": "dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f",
     "unidad_literal": "Milimetros", "qudt_candidata": "unit:MilliM (millimetre)",
     "localizador": "definiciones[5]: Nombre variable=Precipitacion_mm, Unidad de medida=Milimetros, Ejemplo=12.5"},
    {"id": "P1-Q2", "concepto": "volumen-agua-presas", "variable": "Almacenamiento(hm3)",
     "diccionario": "ca5574f0-d59d-4fc1-a52f-5c533b2abf82",
     "conjunto": "ee8f639f-5e89-46ae-93b9-934b05fc6233", "titulo": "Recursos Hidricos",
     "definicion_iri": "https://example.org/mex-ontologi/definition/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3",
     "huella": "7f846ce0b9f83f30c32ea09ab7b09ba328ea4826b1c5ec2b3dede27003aaac3b",
     "unidad_literal": "Hectometros cubicos", "qudt_candidata": "unit:HectoM3 (cubic hectometre)",
     "localizador": "definiciones: Nombre variable=Almacenamiento(hm3), Unidad de medida=Hectometros cubicos, Ejemplo=738.54"},
    {"id": "P1-Q3", "concepto": "superficie-sembrada-cultivo", "variable": "SUPSEM",
     "diccionario": "94215f51-9c89-414d-8c3d-92792e609a2a",
     "conjunto": "3e17a7e8-c8d4-49c4-a426-4dec099cd0cd", "titulo": "Agricultura Sonora",
     "definicion_iri": "https://example.org/mex-ontologi/definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "documented_iri": "https://example.org/mex-ontologi/documented-variable/94215f51-9c89-414d-8c3d-92792e609a2a%2F14",
     "huella": "208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321",
     "unidad_literal": "Hectareas", "qudt_candidata": "unit:HectoHA (hectare)",
     "localizador": "definiciones: Nombre variable=SUPSEM, Unidad de medida=Hectareas, Descripcion=Cantidad de hectareas sembradas"},
]

# verificar filas contra inspecciones locales + tomar URL fuente primaria
for c in CASOS:
    d = insp(c["diccionario"])
    c["fuente_url"] = d.get("fuente", "")
    defs = d.get("definiciones", [])
    hit = [x for x in defs if x.get("Nombre variable") == c["variable"]
           or (c["id"] == "P1-Q2" and "Almacenamiento" in (x.get("Nombre variable") or ""))]
    assert hit, f"sin fila para {c['id']}"
    c["fila_diccionario"] = {k: hit[0].get(k) for k in hit[0].keys()}
    (V / "fixtures" / f"{c['id']}-{c['variable']}.json".replace("/", "_")).write_text(
        json.dumps(hit[0], ensure_ascii=False, indent=1), encoding="utf-8")

TTL = """@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# P1-QUDT v001 (propuesta_para_auditar, NO integrada).
# Solo declara la unidad de la variable por recurso, cualificada por fuente.
# Sin valores observados, sin conversiones, sin qudt:QuantityValue.
# mex:unidadQudt se omite hasta que W verifique el URI exacto (peticiones P1-W-01..03).
# Propiedades mex:* nuevas son locales a la propuesta; no renombran el nucleo.

<https://example.org/mex-ontologi/propuesta/p1-qudt/v001/declaracion-precipitacion-mm> a mex:UnidadDeclarada ;
    rdfs:label "Precipitacion diaria: unidad Milimetros (declaracion cualificada)"@es ;
    mex:variableDocumentada <https://example.org/mex-ontologi/documented-variable/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6> ;
    mex:definicionFuente <https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6> ;
    mex:conjuntoFuente "8b4edefe-cb1a-401c-90c6-05548779defd" ;
    mex:unidadLiteral "Milimetros" ;
    mex:unidadQudtCandidata "unit:MilliM (millimetre) - SIN VERIFICAR, peticion P1-W-01" ;
    mex:estadoPropuesta "propuesta_para_auditar" ;
    prov:wasDerivedFrom <https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=6713de4e-1e2b-447d-8000-f6ceaabd8473&limit=1000&offset=0&sort=_id+asc> ;
    rdfs:comment "Alcance: solo variable Precipitacion_mm del diccionario 6713de4e. No afirma valores observados ni conversiones."@es .

<https://example.org/mex-ontologi/propuesta/p1-qudt/v001/declaracion-volumen-agua-hm3> a mex:UnidadDeclarada ;
    rdfs:label "Volumen de agua en presas: unidad Hectometros cubicos (declaracion cualificada)"@es ;
    mex:variableDocumentada <https://example.org/mex-ontologi/documented-variable/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3> ;
    mex:definicionFuente <https://example.org/mex-ontologi/definition/ca5574f0-d59d-4fc1-a52f-5c533b2abf82%2F3> ;
    mex:conjuntoFuente "ee8f639f-5e89-46ae-93b9-934b05fc6233" ;
    mex:unidadLiteral "Hectometros cubicos" ;
    mex:unidadQudtCandidata "unit:HectoM3 (cubic hectometre) - SIN VERIFICAR, peticion P1-W-02" ;
    mex:estadoPropuesta "propuesta_para_auditar" ;
    prov:wasDerivedFrom <https://datos.sonora.gob.mx/dataset/ee8f639f-5e89-46ae-93b9-934b05fc6233/resource/ca5574f0-d59d-4fc1-a52f-5c533b2abf82/download/diccionario_recursos_hidricos.csv> ;
    rdfs:comment "Alcance: solo variable Almacenamiento(hm3) del diccionario ca5574f0. No afirma valores observados ni conversiones."@es .

<https://example.org/mex-ontologi/propuesta/p1-qudt/v001/declaracion-superficie-ha> a mex:UnidadDeclarada ;
    rdfs:label "Superficie sembrada: unidad Hectareas (declaracion cualificada)"@es ;
    mex:variableDocumentada <https://example.org/mex-ontologi/documented-variable/94215f51-9c89-414d-8c3d-92792e609a2a%2F14> ;
    mex:definicionFuente <https://example.org/mex-ontologi/definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14> ;
    mex:conjuntoFuente "3e17a7e8-c8d4-49c4-a426-4dec099cd0cd" ;
    mex:unidadLiteral "Hectareas" ;
    mex:unidadQudtCandidata "unit:HectoHA (hectare) - SIN VERIFICAR, peticion P1-W-03" ;
    mex:estadoPropuesta "propuesta_para_auditar" ;
    prov:wasDerivedFrom <https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=94215f51-9c89-414d-8c3d-92792e609a2a&limit=1000&offset=0&sort=_id+asc> ;
    rdfs:comment "Alcance: solo variable SUPSEM del diccionario 94215f51. No afirma valores observados ni conversiones."@es .
"""
(V / "propuesta-qudt.ttl").write_text(TTL, encoding="utf-8")

# validar Turtle + probar consultas con rdflib (dependencia ya instalada del proyecto)
from rdflib import Graph
g = Graph()
g.parse(data=TTL, format="turtle")
q1 = """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?d ?var ?lit WHERE { ?d a mex:UnidadDeclarada ; mex:variableDocumentada ?var ; mex:unidadLiteral ?lit } ORDER BY ?d"""
r1 = list(g.query(q1))
assert len(r1) == 3, f"Q1 esperaba 3, dio {len(r1)}"
q2 = """PREFIX mex: <https://example.org/mex-ontologi/vocab/>
SELECT ?d ?cj WHERE { ?d a mex:UnidadDeclarada ; mex:conjuntoFuente ?cj } ORDER BY ?d"""
r2 = list(g.query(q2))
assert len(r2) == 3
(V / "consultas" / "q1-declaraciones-por-variable.rq").write_text(q1, encoding="utf-8")
(V / "consultas" / "q2-declaraciones-por-conjunto.rq").write_text(q2, encoding="utf-8")

PETICIONES = {"rol_destino": "W-estandares", "solicitudes": [
    {"id": "P1-W-01", "caso": "P1-Q1", "pide": "URI QUDT normativo exacto para milimetro y documento normativo (URL + localizador). No usar el URI candidato sin verificacion.",
     "url_primaria_concreta": "https://qudt.org/vocab/unit/"},
    {"id": "P1-W-02", "caso": "P1-Q2", "pide": "URI QUDT normativo exacto para hectometro cubico y documento normativo (URL + localizador).",
     "url_primaria_concreta": "https://qudt.org/vocab/unit/"},
    {"id": "P1-W-03", "caso": "P1-Q3", "pide": "URI QUDT normativo exacto para hectarea y documento normativo (URL + localizador).",
     "url_primaria_concreta": "https://qudt.org/vocab/unit/"}]}
(MIO / "peticiones-web.json").write_text(json.dumps(PETICIONES, ensure_ascii=False, indent=1), encoding="utf-8")

fuente_rutas = [
    "data/portal/inspecciones/6713de4e-1e2b-447d-8000-f6ceaabd8473.json",
    "data/portal/inspecciones/ca5574f0-d59d-4fc1-a52f-5c533b2abf82.json",
    "data/portal/inspecciones/94215f51-9c89-414d-8c3d-92792e609a2a.json",
    "data/portal/inspecciones/bfb8788b-8ce3-475e-8bbd-dd1c5154c877.json",
    "data/portal/inspecciones/a6cdb7ad-ec32-44aa-851d-684947df4243.json",
    "data/integracion-cobertura/entregas/territorio-economia/entrega.json",
    "data/semantica/cobertura.json",
    "reports/ronda-8.json",
    "docs/plan-actualizado-tras-r8.md",
    "docs/plan-actualizado-tras-r8.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/base.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/base-semantica.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/asignacion.json",
]
fuentes = []
for r in fuente_rutas:
    e = {"ruta": r, "sha256": sha(BASE / r)}
    for c in CASOS:
        if c["diccionario"] in r:
            e["url"] = c["fuente_url"]
    fuentes.append(e)

INVENTARIO = {
    "nota_metodo": "Unidad EXPLICITA = columna 'Unidad de medida'/'Unidades de medida' no vacia en la inspeccion local del diccionario, o unidad en nombre/descripcion de la fila. Conteos y codigos no son unidades.",
    "unidades_explicitas_verificadas": [
        {"variable": "Precipitacion_mm", "unidad": "Milimetros", "diccionario": "6713de4e-1e2b-447d-8000-f6ceaabd8473"},
        {"variable": "Almacenamiento(hm3)", "unidad": "Hectometros cubicos", "diccionario": "ca5574f0-d59d-4fc1-a52f-5c533b2abf82"},
        {"variable": "cap_name/cap_namo/vol_muerto", "unidad": "Hectometros cubicos", "diccionario": "bfb8788b-8ce3-475e-8bbd-dd1c5154c877"},
        {"variable": "SUPSEM/SUPCOSE/SUPSINI + 11 trigo (ha)", "unidad": "Hectareas", "diccionario": "94215f51-9c89-414d-8c3d-92792e609a2a + a7591bc9 (trigo)"},
        {"variable": "PRODTON/PESODESEMB/PVIVO", "unidad": "Toneladas", "diccionario": "94215f51 / 863b9cc8"},
        {"variable": "RENDMNTO", "unidad": "Toneladas/hectareas (compuesta, sin proponer)", "diccionario": "94215f51-9c89-414d-8c3d-92792e609a2a"},
        {"variable": "premin/premax/preprom", "unidad": "Pesos/kilogramo", "diccionario": "a4eb0b8b-d6c6-44b8-b00a-f5f45c1875a5"},
        {"variable": "pesoprom", "unidad": "Kilogramos", "diccionario": "a4eb0b8b-d6c6-44b8-b00a-f5f45c1875a5"},
        {"variable": "VALOR/VALPROD", "unidad": "Pesos MXN / Miles de pesos MXN", "diccionario": "863b9cc8 / 94215f51 / 53b157b9"},
        {"variable": "Unidad de Medida (plantas)", "unidad": "MW / GWh segun fila", "diccionario": "a6cdb7ad-ec32-44aa-851d-684947df4243"},
        {"variable": "Latitud/Longitud", "unidad": "Grados (angular, sin proponer aun)", "diccionario": "bfb8788b / a6cdb7ad / 2154135f / b37f6cd2"},
        {"variable": "P11/P13 gobierno-digital", "unidad": "GB (encuesta, ejemplo no numerico: no proponer valor)", "diccionario": "bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1"},
    ],
    "excluidas_con_motivo": [
        {"variable": "Altitud (presas, bfb8788b)", "motivo": "Unidad literal 'Grados' fisicamente inverosimil para altitud; se conserva literal sin reinterpretar ni proponer. Posible error de captura: no integrar."},
        {"variable": "temperatura (Rickettsia)", "motivo": "Sin unidad declarada en la fila (solo 'Temperatura del paciente'): no proponer."},
        {"variable": "TALLA/PESO (nacimientos), PESO (difunto)", "motivo": "Sin unidad declarada en la fila: no proponer."},
        {"variable": "CLAVEEDADD 'Unidad de edad'", "motivo": "Es descriptor de codificacion (clave), no unidad fisica: no proponer como QUDT."},
        {"variable": "CIERREYAVAN/CICLO/CDDR/CMUN/CVMES (agricultura)", "motivo": "Columna 'Unidad de medida' usada para listas de codigos, no unidades: no proponer."},
        {"variable": "RENDMNTO Toneladas/hectareas", "motivo": "Unidad compuesta: solo proponer cuando W verifique modelado (fuera de v001)."},
    ],
    "descriptores_nacionales_no_codificacion_adoptada": {
        "nota": "En la base R8 no existe ninguna agrupacion verificable de exactamente 31 descriptores nacionales; no se inventa el conteo. Se separan los descriptores de metodologia nacional encontrados (73 variables / 72 conceptos porc-*/indice-*/grado-marginacion en 8 conjuntos CONAPO/educacion, mas 13 menciones INEGI/FAO/INAPESCA/CONAGUA/SUN): son descriptores, no unidades; no se adopta codificacion ni se propone QUDT para ellos.",
        "conjuntos": ["Indice de marginacion por localidad", "Indice de marginacion urbana en AGEB", "Indice de marginacion urbana por colonia", "Indice de marginacion por municipio", "Indices de marginacion por Entidad Federativa", "Proyecciones de poblacion - Indicadores demograficos", "Indices de Reprobacion", "Indices de Reprobacion Modalidad Remota"],
        "variables_ejemplo": ["GM_2020", "ANALF/SBASC/OVSDE/OVSEE/OVSAE/OVPT/OVSREF/OVHAC", "posicion-nacional-marginacion-municipio/entidad", "clave-ciudad-sun-2018"],
    },
}
(V / "inventario-unidades.json").write_text(json.dumps(INVENTARIO, ensure_ascii=False, indent=1), encoding="utf-8")

ENTREGA = {
    "rol": "P1-qudt", "version": "v001", "fecha_utc": "2026-10-24",
    "estado": "propuesta_para_auditar",
    "base": {"informe": "reports/ronda-8.json", "estado_r8": "cerrado_integrado_validado_y_sincronizado"},
    "casos": [{"id": c["id"], "concepto": c["concepto"], "variable": c["variable"],
               "recurso_conjunto": c["conjunto"], "diccionario": c["diccionario"],
               "unidad_literal": c["unidad_literal"], "unidad_qudt_candidata_sin_verificar": c["qudt_candidata"],
               "definicion_iri": c["definicion_iri"], "huella_fila_diccionario": c["huella"],
               "localizador": c["localizador"], "resultado": "declaracion_cualificada_propuesta"} for c in CASOS],
    "archivos_propuestos": ["v001/propuesta-qudt.ttl", "v001/consultas/q1-declaraciones-por-variable.rq",
                            "v001/consultas/q2-declaraciones-por-conjunto.rq", "v001/fixtures/P1-Q1-Precipitacion_mm.json",
                            "v001/fixtures/P1-Q2-Almacenamiento(hm3).json", "v001/fixtures/P1-Q3-SUPSEM.json",
                            "v001/inventario-unidades.json"],
    "validacion_local": {"turtle_parse_ok": True, "q1_filas": 3, "q2_filas": 3, "validador": "rdflib del proyecto (sin instalar nada)"},
    "fuentes": fuentes,
    "limites": [
        "Gemma excluido; sin contactos externos; sin promocion por nombre.",
        "Sin cambios a nucleo, shapes, manifiestos previos, grafo ni Studio.",
        "Solo se declara la unidad de la variable por recurso; no se afirman valores observados (ejemplos 12.5/738.54 son ilustrativos de la fila, no hechos).",
        "Sin conversiones y sin qudt:QuantityValue.",
        "URIs QUDT candidatos SIN VERIFICAR: mex:unidadQudt omitida hasta respuesta de W (peticiones-web.json P1-W-01..03).",
        "Altitud-Grados y descriptores/codigos excluidos con motivo (ver inventario).",
        "Familia de marginacion/metodologia nacional separada como descriptores, sin adoptar codificacion.",
    ],
    "condiciones_aceptacion": [
        "W verifica URI QUDT exacto + documento normativo para P1-W-01..03.",
        "Auditor replica SHA256 de fuentes y localizadores de fila.",
        "Q1/Q2 devuelven 3 filas sobre propuesta-qudt.ttl.",
        "Sin esta verificacion, la propuesta NO se integra (v001 queda como propuesta_para_auditar).",
    ],
}
(V / "entrega.json").write_text(json.dumps(ENTREGA, ensure_ascii=False, indent=1), encoding="utf-8")

MD = """# P1-QUDT v001 — propuesta_para_auditar (NO integrada)

Inventario de unidades explícitas + propuesta mínima QUDT cualificada (3 casos).

## Casos propuestos (declaración de unidad por variable/recurso)

| Caso | Variable | Unidad literal (fuente) | Diccionario | QUDT |
| --- | --- | --- | --- | --- |
| P1-Q1 | Precipitacion_mm | Milimetros | 6713de4e | unit:MilliM SIN VERIFICAR (P1-W-01) |
| P1-Q2 | Almacenamiento(hm3) | Hectometros cubicos | ca5574f0 | unit:HectoM3 SIN VERIFICAR (P1-W-02) |
| P1-Q3 | SUPSEM | Hectareas | 94215f51 | unit:HectoHA SIN VERIFICAR (P1-W-03) |

## Lo que NO se hace

Valores observados, conversiones, `qudt:QuantityValue`, dominio QuantityValue
sobre VariableDocumentada, Altitud-Grados (literal inverosímil, excluida),
temperatura/TALLA/PESO sin unidad declarada, claves/códigos como unidades,
familia de marginación nacional como codificación adoptada.

## Verificación

- `propuesta-qudt.ttl` parsea (rdflib del proyecto); Q1/Q2 → 3 filas.
- `peticiones-web.json` pide a W los 3 URIs exactos + documento normativo.
- `congelada.json`: SHA256 por código. Autohash de congelada.json =
  sha256 del JSON canónico (sort_keys) sin su propia entrada; reproducir con
  `build_v001.py` / script de verificación del auditor.
- Condición de integración: verificación W + réplica de hashes. Sin eso, no integrar.
"""
(V / "entrega.md").write_text(MD, encoding="utf-8")

# congelada.json: sha de TODOS los archivos bajo P1-qudt (bytes), salvo autoconsumo
todos = sorted([p for p in MIO.rglob("*") if p.is_file() and p.name != "congelada.json"],
               key=lambda p: p.relative_to(MIO).as_posix())
arch = {p.relative_to(MIO).as_posix().replace("\\", "/"): sha(p) for p in todos}
congel = {"rol": "P1-qudt", "version": "v001", "fecha_utc": "2026-10-24",
          "nota_autohash": "archivos['v001/congelada.json'] = sha256(json.dumps(congelada_sin_esa_entrada, sort_keys=True, ensure_ascii=False))",
          "archivos": {**arch, "v001/congelada.json": ""}}
canon = json.dumps({k: v for k, v in congel.items() if k != "archivos"} | {"archivos": {k: v for k, v in arch.items()}}, sort_keys=True, ensure_ascii=False)
congel["archivos"]["v001/congelada.json"] = hashlib.sha256(canon.encode("utf-8")).hexdigest()
(MIO / "v001" / "congelada.json").write_text(json.dumps(congel, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK casos={len(CASOS)} q1={len(r1)} q2={len(r2)} archivos_congelados={len(congel['archivos'])}")
