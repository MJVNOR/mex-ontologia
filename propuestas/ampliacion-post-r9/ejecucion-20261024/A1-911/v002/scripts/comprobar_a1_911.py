"""A1-911 v002: comprobaciones reproducibles del par 911 (solo lectura local).

Genera resultados.json, entrega.json y entrega.md a partir de las fuentes
locales, sin descargas, sin contactos, sin tocar el grafo ni Studio.

Uso:
    uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/comprobar_a1_911.py [SALIDA]

Sin argumento escribe en la carpeta v002. Con argumento escribe alli (lo usa
el test para comprobar determinismo sin pisar la entrega).

Los numeros y SHA salen de estos archivos; ninguno se transcribe a mano:
data/portal/inventario.json, data/portal/inspecciones/*.json,
data/portal/contenido-inspeccion.json, data/portal/oportunidades-cruce.json,
data/portal/lote-cruces/validacion-lote.json, ontologia/semantica.json,
reports/pendientes-semanticos.json,
docs/plan-paralelo-ampliacion-post-r9.md.
"""

import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parents[6]
assert (RAIZ / "data/portal/inventario.json").exists(), f"raiz inesperada: {RAIZ}"

A = "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f"
B = "923b485b-515e-4fb9-a4ac-cccbeb88cc92"
PID = A + "--" + B

IMPRO_Q2 = "0df8592f-bb3d-466c-aec3-6cbc91253be0"
IMPRO_Q1_FALSO = "54285a13-3a2a-4e47-b0af-e855861f5347"
DICC_A = "1a95d734-2f0e-4781-8831-77dcfcbe70f8"
PROC_Q1 = "6ce17dd1-5716-44e9-bc5f-603c0925afe6"
PROC_Q2 = "943e2919-6a8b-4776-ac4f-c3d6b02bb94e"
DICC_B = "7922b8c8-db09-4172-ad7f-31b0ba0c68e3"

RIDS = [IMPRO_Q2, IMPRO_Q1_FALSO, DICC_A, PROC_Q1, PROC_Q2, DICC_B]

FUENTES = [
    "data/portal/inventario.json",
    "data/portal/contenido-inspeccion.json",
    "data/portal/oportunidades-cruce.json",
    "data/portal/lote-cruces/validacion-lote.json",
    "ontologia/semantica.json",
    "reports/pendientes-semanticos.json",
    "docs/plan-paralelo-ampliacion-post-r9.md",
] + [f"data/portal/inspecciones/{rid}.json" for rid in RIDS]

PREGUNTA = (
    "¿Se pueden comparar los volumenes clasificados como procedentes e improcedentes "
    "por municipio y mes? Solo calcular una proporcion si consta que las categorias "
    "forman una particion del mismo universo."
)


def cargar(rel):
    return json.loads((RAIZ / rel.replace("/", "\\")).read_text(encoding="utf-8"))


def sha_archivo(rel):
    return hashlib.sha256((RAIZ / rel.replace("/", "\\")).read_bytes()).hexdigest()


def trimestre(nombre, url):
    t = (nombre + " " + url).lower()
    q = "Q1" if "primer trimestre" in t else "Q2" if "segundo trimestre" in t else None
    anio = re.search(r"20\d{2}", t)
    return q, anio.group(0) if anio else None


# ---------------------------------------------------------------- fuentes
fuentes_sha = {
    rel: {"sha256": sha_archivo(rel), "bytes": (RAIZ / rel.replace("/", "\\")).stat().st_size}
    for rel in FUENTES
}

inv = cargar("data/portal/inventario.json")
oc = cargar("data/portal/oportunidades-cruce.json")
vl = cargar("data/portal/lote-cruces/validacion-lote.json")
sem = cargar("ontologia/semantica.json")
pend = cargar("reports/pendientes-semanticos.json")

inspecciones = {rid: cargar(f"data/portal/inspecciones/{rid}.json") for rid in RIDS}

recursos = {}
for r in inv["recursos"]:
    if r.get("conjunto_id") not in (A, B):
        continue
    d = inspecciones[r["id"]]
    tabla = d["tablas"][0]
    recursos[r["id"]] = {
        "conjunto": r["conjunto"],
        "conjunto_id": r["conjunto_id"],
        "nombre": r["nombre"],
        "formato": r["formato"],
        "url": r["url"],
        "descripcion": r.get("descripcion"),
        "ok": d["ok"],
        "http": d["http"],
        "completo": d["completo"],
        "bytes_leidos": d["bytes_leidos"],
        "sha256": d["sha256_fragmento_o_archivo"],
        "hoja": tabla["hoja"],
        "columnas": [c["id"] for c in tabla["campos"]],
        "metodo_encabezado": tabla["metodo_encabezado"],
        "consultado_en_utc": d["consultado_en_utc"],
        "vars": len(d["definiciones"]) if "definiciones" in d else None,
    }

assert len(recursos) == 6, sorted(recursos)
assert set(recursos) == set(RIDS), sorted(recursos)
for rid, r in recursos.items():
    assert r["ok"] and r["completo"] and r["http"] == 200, rid
    assert r["bytes_leidos"] > 0 and len(r["sha256"]) == 64, rid

grupo = {"a": [r for r in RIDS if recursos[r]["conjunto_id"] == A],
         "b": [r for r in RIDS if recursos[r]["conjunto_id"] == B]}
assert len(grupo["a"]) == 3 and len(grupo["b"]) == 3
assert set(grupo["a"]) == {IMPRO_Q2, IMPRO_Q1_FALSO, DICC_A}
assert set(grupo["b"]) == {PROC_Q1, PROC_Q2, DICC_B}

xlsx = [rid for rid in RIDS if recursos[rid]["formato"] == "XLSX"]
assert len(xlsx) == 4

# ------------------------------------------------- duplicado entre conjuntos
dup = [(x, y) for x in grupo["a"] for y in grupo["b"]
       if recursos[x]["formato"] == "XLSX" and recursos[y]["formato"] == "XLSX"
       and recursos[x]["sha256"] == recursos[y]["sha256"]]
assert dup == [(IMPRO_Q1_FALSO, PROC_Q1)], dup
dup_sha = recursos[IMPRO_Q1_FALSO]["sha256"]
assert recursos[IMPRO_Q1_FALSO]["bytes_leidos"] == recursos[PROC_Q1]["bytes_leidos"]
assert recursos[IMPRO_Q1_FALSO]["hoja"] == recursos[PROC_Q1]["hoja"] == "LLAMADAS PROCEDENTES 911"
assert "procedentes" in recursos[IMPRO_Q1_FALSO]["url"].lower()
assert "improcedentes" in recursos[IMPRO_Q1_FALSO]["nombre"].lower()  # el nombre dice Improcedentes

# el mismo SHA no aparece en un tercer recurso del corpus inspeccionado
ocurrencias = []
for f in (RAIZ / "data/portal/inspecciones").glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    if d.get("sha256_fragmento_o_archivo") == dup_sha:
        ocurrencias.append(d["id"])
assert sorted(ocurrencias) == sorted([IMPRO_Q1_FALSO, PROC_Q1]), ocurrencias

# ------------------------------------------------------------- diccionarios
assert recursos[DICC_A]["sha256"] == recursos[DICC_B]["sha256"]
dic = inspecciones[DICC_A]["definiciones"]
assert len(dic) == 7 and len(inspecciones[DICC_B]["definiciones"]) == 7
vars_dicc = [d["Nombre variable"] for d in dic]
unidades = sorted({d["Unidad de medida"] for d in dic})
assert unidades == [""], unidades
identificadores = {d["Nombre variable"]: d["Identificadores"] for d in dic}
assert sorted(v for v, x in identificadores.items() if x.strip()) == ["hora"], identificadores
assert "y asi sucesivamente" in identificadores["hora"]  # texto residual, no una clave
assert "motivo no procedente" not in [v.lower() for v in vars_dicc]
cols_q2_impro = [c.lower() for c in recursos[IMPRO_Q2]["columnas"]]
sin_diccionario = [c for c in cols_q2_impro if c not in [v.lower() for v in vars_dicc]]

# ------------------------------------------------- Q2 improcedentes sin corte
assert recursos[IMPRO_Q2]["columnas"] == ["FECHA", "HORA", "MOTIVO NO PROCEDENTE"]
assert "MUNICIPIO" not in recursos[IMPRO_Q2]["columnas"]
assert recursos[IMPRO_Q2]["hoja"] == "LLAMADA IMPROCEDENTES 911"
improcedentes_reales = [rid for rid in xlsx
                        if recursos[rid]["hoja"].upper().startswith("LLAMADA IMPROCEDENTES")]
assert improcedentes_reales == [IMPRO_Q2], improcedentes_reales
assert all("MUNICIPIO" not in recursos[rid]["columnas"] for rid in improcedentes_reales)

# ------------------------------------------------------------ periodo nominal
periodos = {rid: trimestre(recursos[rid]["nombre"], recursos[rid]["url"]) for rid in xlsx}
assert periodos == {
    IMPRO_Q1_FALSO: ("Q1", "2026"),
    IMPRO_Q2: ("Q2", "2026"),
    PROC_Q1: ("Q1", "2026"),
    PROC_Q2: ("Q2", "2026"),
}, periodos

# --------------------------------------------- oportunidad y lote (cruce R9)
par = next(p for p in oc["pares"] if p["id"] == PID)
assert par["estado"] == "candidata_por_validar" and par["alcance_ejecucion"] == "No ejecutado"
assert par["anios_coincidentes_solo_en_nombres"] == ["2026"]

familias = {e["familia"]: e for e in par["evaluacion_claves"]}
assert set(familias) >= {"municipio", "localidad", "periodo"}


def recursos_a(familia):
    return sorted({c.split("/file-column/")[1].split("%2F")[0]
                   for c in familias[familia]["columnas_a"]})


territoriales = ["municipio", "localidad", "division_territorial_declarada"]
assert all(recursos_a(f) == [IMPRO_Q1_FALSO] for f in territoriales), \
    {f: recursos_a(f) for f in territoriales}
assert recursos_a("periodo") == [IMPRO_Q2, IMPRO_Q1_FALSO]

ple = next(p for p in vl["pares"] if p.get("id") == PID)
assert ple["decision"] == "requiere_revision" and ple["ejecuciones"] == []
muestras = ple["diagnostico_muestras"]
assert muestras["a"]["recurso_id"] == IMPRO_Q1_FALSO  # muestra tomada del duplicado
assert muestras["b"]["recurso_id"] == PROC_Q2
assert IMPRO_Q2 not in json.dumps(muestras)
assert muestras["a"]["filas_muestra"] == 29 and muestras["b"]["filas_muestra"] == 29
assert all("FECHA" not in m["campos_solicitados"] for m in muestras.values())
assert all("no demuestra unicidad" in m["alcance"] for m in muestras.values())

cmp_municipio = next(c for c in ple["comparacion_muestras"] if c["familia"] == "municipio")
assert "sin equivalencia" in cmp_municipio["interpretacion"]

# ------------------------------------------------------------ semantica local
vinculos = [v for v in sem["vinculos_documentales_revisados"] if v.get("recurso") in RIDS]
mun = [v for v in vinculos if v.get("campo") == "MUNICIPIO"]
recursos_con_municipio = sorted({v["recurso"] for v in mun})
assert IMPRO_Q2 not in recursos_con_municipio
assert IMPRO_Q1_FALSO in recursos_con_municipio
hora_dup = [v for v in vinculos if v["recurso"] == IMPRO_Q1_FALSO and v.get("campo") == "HORA"]
assert hora_dup and "improcedente" in hora_dup[0]["concepto"]
motivo = next(c for c in pend["columnas"]
              if c["recurso"] == IMPRO_Q2 and c["campo"] == "MOTIVO NO PROCEDENTE")
assert motivo["estado"] == "sin_definicion_coincidente"

# ------------------------------------- no hay copias locales de filas (911)
copias = []
for p in RAIZ.rglob("*"):
    if any(x in p.parts for x in ("node_modules", ".git")):
        continue
    if p.is_file() and p.suffix.lower() in {".xlsx", ".xls", ".csv"}:
        n = p.name.lower()
        if "llamada" in n and ("911" in n or "procedente" in n or "improcedente" in n):
            copias.append(str(p.relative_to(RAIZ)).replace("\\", "/"))
assert copias == [], copias

# --------------------------------------------------- sin documento de particion
assert all(recursos[rid]["descripcion"] is None for rid in RIDS)
assert all(recursos[rid]["formato"] in {"XLSX", "CSV"} for rid in RIDS)

# -------------------------------------------------------------- ficha 8 ejes
n_heur = sum(1 for rid in RIDS if recursos[rid]["metodo_encabezado"] == "heuristica_requiere_revision")
reps_a = {k: v["repeticiones_muestra"] for k, v in muestras["a"]["campos"].items()}
reps_b = {k: v["repeticiones_muestra"] for k, v in muestras["b"]["campos"].items()}
nulos_a = {k: v["nulos"] for k, v in muestras["a"]["campos"].items()}
nulos_b = {k: v["nulos"] for k, v in muestras["b"]["campos"].items()}
sha_dicc = recursos[DICC_A]["sha256"]

ficha = {
    "claves": {
        "estado": "no_acreditada",
        "evidencia": (
            f"Ninguno de los 6 recursos declara columna identificadora: las 7 variables del "
            f"diccionario {DICC_A[:8]} (sha {sha_dicc[:12]}, identico en ambos conjuntos) no "
            f"aportan identificador (6 con 'Identificadores' vacio y 'hora' solo con texto "
            f"residual). {n_heur} de 6 esquemas usan "
            "metodo_encabezado=heuristica_requiere_revision. El cruce R9 exige clave compuesta "
            "entidad+municipio y entidad+municipio+localidad."
        ),
        "comprobado": ["esquemas", "diccionario.Identificadores", "oportunidad.pendientes"],
        "pendiente": ["catalogo de municipios con unicidad", "contexto de clave documentado"],
    },
    "grano": {
        "estado": "fila_evento_llamada_sin_agregacion_validada",
        "evidencia": (
            "Los cuatro XLSX tienen grano de llamada individual (FECHA/HORA + atributos), "
            "sin columnas de total ni de resumen. El lote de cruces rechaza ejecutar por "
            f"falta de estrategia de agregacion: {ple['motivos'][0]}."
        ),
        "comprobado": ["esquemas", "lote.decision", "lote.ejecuciones"],
        "pendiente": ["regla de agregacion por municipio y mes"],
    },
    "unicidad": {
        "estado": "no_acreditada",
        "evidencia": (
            "Solo hay diagnosticos de muestra n=29 con alcance literal "
            "'no demuestra unicidad ni cobertura integral'. Repeticiones en la muestra: "
            f"MUNICIPIO {reps_a['MUNICIPIO']}/29 (Q1) y {reps_b['MUNICIPIO']}/29 (Q2); "
            f"LOCALIDAD {reps_a['LOCALIDAD']}/29 y {reps_b['LOCALIDAD']}/29; "
            f"COLONIA {reps_a['COLONIA']}/29 y {reps_b['COLONIA']}/29. "
            "Una muestra no acredita unicidad del recurso completo."
        ),
        "comprobado": ["lote.diagnostico_muestras", "lote.alcance"],
        "pendiente": ["copia local de filas y conteo de duplicados por clave"],
    },
    "cardinalidad": {
        "estado": "no_acreditada",
        "evidencia": (
            "Sin clave primaria declarada no hay cardinalidad 1:1 ni N:M demostrable. "
            f"El lote queda en '{ple['decision']}' con ejecuciones={ple['ejecuciones']} y "
            "pendiente 'comprobar_cardinalidad_y_evitar_multiplicacion_de_filas'. "
            "Ademas el recurso etiquetado como improcedentes Q1 comparte SHA con procedentes Q1, "
            "de modo que una union ingenua duplicaria filas y ningun total es fiable."
        ),
        "comprobado": ["lote", "duplicado entre conjuntos"],
        "pendiente": ["conteo de filas por recurso", "clave y cardinalidad declaradas"],
    },
    "poblacion": {
        "estado": "sin_particion_acreditada",
        "evidencia": (
            "Procedentes e improcedentes viven en conjuntos separados y ningun recurso del par "
            "es un documento de particion: los 6 son XLSX/CSV de datos o diccionario, sin "
            "descripcion, y no aportan total del universo. El recurso de improcedentes Q1 "
            f"({IMPRO_Q1_FALSO[:8]}) contiene en realidad la hoja LLAMADAS PROCEDENTES 911 con "
            f"sha {dup_sha[:12]}, identico a procedentes Q1 ({PROC_Q1[:8]}). Sin particion "
            "declarada no se calcula proporcion."
        ),
        "comprobado": ["inventario", "esquemas", "duplicado"],
        "pendiente": ["fe de erratas o diccionario que declare la particion y su total"],
    },
    "periodo": {
        "estado": "nominal_2026_sin_verificar_contenido",
        "evidencia": (
            "Trimestres solo en nombres/URL: Q1 y Q2 de 2026 en los cuatro XLSX; el cruce solo "
            "coincide en el anio y 'solo en nombres'. Las muestras n=29 pidieron "
            f"{sorted(muestras['a']['campos_solicitados'])} y no FECHA, asi que no hay ningun "
            "valor de fecha leido localmente. Un recurso de improcedentes Q1 no existe: ese "
            "lugar lo ocupa el duplicado de procedentes Q1."
        ),
        "comprobado": ["nombres/URL", "lote.campos_solicitados"],
        "pendiente": ["copias locales para verificar FECHA y cobertura mensual"],
    },
    "unidades": {
        "estado": "conteo_de_llamadas_sin_unidad_fisica",
        "evidencia": (
            "Las 7 variables del diccionario tienen 'Unidad de medida' vacia. La medida "
            "implicita es conteo de filas (llamadas), no una magnitud con unidad; no hay "
            "termino QUDT aplicable ni peticion a W que hacer por este par."
        ),
        "comprobado": ["diccionario.Unidad de medida"],
        "pendiente": [],
    },
    "cobertura_datos": {
        "estado": "parcial_y_asimetrica",
        "evidencia": (
            "Improcedentes reales: solo Q2 (0df8592f, 3 columnas FECHA/HORA/MOTIVO, "
            "sin MUNICIPIO). Procedentes: Q1 (6ce17dd1) y Q2 (943e2919), 7 columnas. "
            "El Q1 de improcedentes es un duplicado byte a byte de procedentes Q1. "
            "No hay conteos de filas: solo bytes leidos. Las dos muestras n=29 son de "
            "archivos procedentes (incluido el duplicado); no hay muestra de 0df8592f."
        ),
        "comprobado": ["inventario", "esquemas", "duplicado", "lote.diagnostico_muestras"],
        "pendiente": ["copia local de improcedentes Q2 con MUNICIPIO", "conteos por municipio y mes"],
    },
}

comprobaciones = [
    {"id": "recursos_del_par", "estado": "ok",
     "detalle": f"6 recursos en inventario (3 por conjunto): {sorted(recursos)}"},
    {"id": "duplicado_entre_conjuntos", "estado": "ok",
     "detalle": f"{IMPRO_Q1_FALSO} (conjunto A) == {PROC_Q1} (conjunto B), sha {dup_sha}, bytes {recursos[PROC_Q1]['bytes_leidos']}, hoja LLAMADAS PROCEDENTES 911"},
    {"id": "duplicado_no_se_repite_en_corpus", "estado": "ok",
     "detalle": f"el sha aparece exactamente en {len(ocurrencias)} inspecciones: {sorted(ocurrencias)}"},
    {"id": "diccionarios_identicos", "estado": "ok",
     "detalle": f"diccionarios de A y B con sha {sha_dicc}; 7 variables; unidades vacias; sin variable 'motivo no procedente'"},
    {"id": "columnas_sin_diccionario", "estado": "no_acreditado",
     "detalle": f"columnas de improcedentes Q2 sin definicion en el diccionario: {sin_diccionario}"},
    {"id": "q2_improcedentes_sin_municipio", "estado": "ok",
     "detalle": "0df8592f solo tiene FECHA, HORA y MOTIVO NO PROCEDENTE; no permite corte por municipio"},
    {"id": "improcedentes_reales_solo_q2", "estado": "ok",
     "detalle": f"unico XLSX con hoja de improcedentes: {improcedentes_reales}; el Q1 del conjunto A es el duplicado de procedentes"},
    {"id": "muestra_a_desde_duplicado", "estado": "ok",
     "detalle": f"la muestra A del lote se tomo de {IMPRO_Q1_FALSO} (procedentes Q1), no de 0df8592f; la comparacion muestral es procedentes Q1 vs procedentes Q2"},
    {"id": "familias_territoriales_solo_por_duplicado", "estado": "ok",
     "detalle": f"en el cruce, municipio/localidad/division_territorial_declarada solo enlazan columnas de {IMPRO_Q1_FALSO}; sin el duplicado no hay familia territorial compartida"},
    {"id": "periodo_compartido_real", "estado": "ok",
     "detalle": "FECHA existe en 0df8592f y en los procedentes; el periodo es la unica familia compartida con columna propia de improcedentes"},
    {"id": "coincidencias_municipio_muestrales", "estado": "no_acreditado",
     "detalle": f"{cmp_municipio['coincidencias_exactas_muestra']} coincidencias textuales en muestra n=29 ({', '.join(cmp_municipio['ejemplos_coincidentes'])}); interpretacion del lote: {cmp_municipio['interpretacion']}"},
    {"id": "particion_no_declarada", "estado": "bloqueado",
     "detalle": "ningun recurso del par declara particion del universo ni total; descripcion nula en los 6"},
    {"id": "proporcion", "estado": "bloqueado",
     "detalle": "no calculada: falta particion acreditada y, para improcedentes, falta MUNICIPIO"},
    {"id": "join", "estado": "bloqueado",
     "detalle": "no ejecutado: lote requiere_revision, ejecuciones vacias, sin grano/clave/cardinalidad validados"},
    {"id": "filas_locales", "estado": "no_acreditado",
     "detalle": "0 copias locales de filas 911 (xlsx/xls/csv); solo bytes y SHA de inspeccion"},
    {"id": "concepto_municipio_improcedentes", "estado": "no_acreditado",
     "detalle": f"vinculos semanticos de MUNICIPIO solo en {recursos_con_municipio}; 0df8592f no tiene"},
    {"id": "conflicto_semantico_duplicado", "estado": "ok",
     "detalle": f"el vinculo HORA de {IMPRO_Q1_FALSO} usa concepto '{hora_dup[0]['concepto']}' aunque el archivo es procedentes: la etiqueta improcedente del conjunto se propago al contenido"},
    {"id": "motivo_sin_definicion", "estado": "no_acreditado",
     "detalle": "MOTIVO NO PROCEDENTE figura como 'sin_definicion_coincidente' en pendientes semanticos"},
]

resultados = {
    "rol": "A1-911",
    "version": "v002",
    "par": {
        "id": PID,
        "conjunto_a": A, "titulo_a": "Llamadas Improcedentes 911",
        "conjunto_b": B, "titulo_b": "Llamadas Procedentes 911",
    },
    "pregunta": PREGUNTA,
    "resultado": "bloqueado",
    "proporcion": {
        "estado": "bloqueada",
        "motivo": "No consta que procedentes e improcedentes particionen el mismo universo: no hay documento, total ni fe de erratas. Ademas el unico recurso real de improcedentes (Q2) no tiene MUNICIPIO.",
        "requisito": "particion_acreditada_del_mismo_universo",
    },
    "join": {
        "ejecutado": False,
        "motivo": "lote requiere_revision sin ejecuciones; sin clave, grano ni cardinalidad validados; sin MUNICIPIO en improcedentes Q2.",
    },
    "recursos": recursos,
    "conjuntos": {
        "a": {"titulo": "Llamadas Improcedentes 911", "recursos": grupo["a"]},
        "b": {"titulo": "Llamadas Procedentes 911", "recursos": grupo["b"]},
    },
    "hallazgos": {
        "duplicado_entre_conjuntos": {
            "recursos": [IMPRO_Q1_FALSO, PROC_Q1],
            "sha256": dup_sha,
            "bytes": recursos[PROC_Q1]["bytes_leidos"],
            "hoja": recursos[PROC_Q1]["hoja"],
            "detalle": "El recurso de improcedentes Q1 es byte a byte el de procedentes Q1; su URL tambien apunta al archivo de procedentes.",
        },
        "diccionarios_identicos": {
            "recursos": [DICC_A, DICC_B],
            "sha256": sha_dicc,
            "variables": vars_dicc,
            "detalle": "Mismo diccionario en ambos conjuntos; no define MOTIVO NO PROCEDENTE.",
        },
        "columnas_sin_diccionario": sin_diccionario,
        "q2_improcedentes_sin_municipio": {
            "recurso": IMPRO_Q2,
            "columnas": recursos[IMPRO_Q2]["columnas"],
            "detalle": "Sin MUNICIPIO ni LOCALIDAD; el corte territorial y la comparacion por municipio son imposibles para improcedentes.",
        },
        "muestra_a_desde_duplicado": {
            "recurso_muestra_a": IMPRO_Q1_FALSO,
            "recurso_muestra_b": PROC_Q2,
            "detalle": "La comparacion muestral del lote nunca observa improcedentes: compara procedentes Q1 (duplicado) con procedentes Q2.",
        },
        "familias_territoriales_solo_por_duplicado": {
            "familias": territoriales,
            "recurso_unico": IMPRO_Q1_FALSO,
            "detalle": "El 'municipio compartido' del cruce depende del duplicado; al excluirlo no hay clave territorial comun.",
        },
        "coincidencias_municipio_muestrales": {
            "n": cmp_municipio["coincidencias_exactas_muestra"],
            "ejemplos": cmp_municipio["ejemplos_coincidentes"],
            "interpretacion": cmp_municipio["interpretacion"],
        },
        "sin_copias_locales_de_filas": {"archivos": copias},
        "sin_documento_de_particion": True,
    },
    "ficha": ficha,
    "comprobaciones": comprobaciones,
    "verificacion": {
        "fuentes_sha256": fuentes_sha,
        "datos_consultados_entre_utc": [
            min(r["consultado_en_utc"] for r in recursos.values()),
            max(r["consultado_en_utc"] for r in recursos.values()),
        ],
        "reproducir": "uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/comprobar_a1_911.py",
    },
    "reapertura": [
        "Fe de erratas o diccionario del publicador que declare la particion procedentes/improcedentes del mismo universo con su total.",
        "Correccion del recurso 54285a13 (hoy duplicado de procedentes Q1) o sustituto real de improcedentes Q1.",
        "Esquema con MUNICIPIO para improcedentes Q2 (0df8592f) y catalogo de municipios con unicidad.",
        "Copias locales de filas para verificar periodo, conteos por municipio y mes, y unicidad.",
    ],
    "limites": [
        "No se calculo ninguna proporcion ni tasa; no se ejecuto join.",
        "No se infiere unicidad ni cardinalidad del universo a partir de muestras n=29.",
        "Las coincidencias textuales de MUNICIPIO en la muestra no acreditan equivalencia entre conjuntos.",
        "El duplicado Q1 se reporta como hallazgo; no se usa para agregar ni para sumar universos.",
        "No se toco v001, el grafo, la configuracion IRI ni Studio.",
    ],
}

archivos = [
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/entrega.json",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/entrega.md",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/resultados.json",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/comprobar_a1_911.py",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/sellar.py",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/tests/test_a1_911.py",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/sello.json",
    "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/sello.sha256",
]

entrega = {
    "rol": "A1-911",
    "version": "v002",
    "modelo": "opencode/deepseek-v4.1-flash-free",
    "par": resultados["par"],
    "pregunta": PREGUNTA,
    "resultado": "bloqueado",
    "alcance": "Analisis separado del par; sin grafo, sin promociones, sin descargas, sin contactos, sin Studio. Base IRI intacta.",
    "proporcion": resultados["proporcion"],
    "join": resultados["join"],
    "ficha": ficha,
    "hallazgos_clave": [
        f"Duplicado entre conjuntos: {IMPRO_Q1_FALSO} == {PROC_Q1} (sha {dup_sha}); el Q1 de improcedentes es procedentes Q1.",
        f"Diccionarios identicos (sha {sha_dicc}); no definen MOTIVO NO PROCEDENTE.",
        "Improcedentes Q2 (0df8592f) solo trae FECHA/HORA/MOTIVO: sin MUNICIPIO no hay corte territorial.",
        "La muestra A del lote sale del duplicado: la comparacion muestral es procedentes Q1 vs Q2, no improcedentes vs procedentes.",
        "Municipio/localidad/colonia del cruce solo existen por el duplicado; periodo (FECHA) es la unica familia compartida real, con valores sin verificar.",
    ],
    "archivos": archivos,
    "sello": {
        "archivo": "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/sello.sha256",
        "generado_por": "propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/sellar.py",
    },
    "verificacion": resultados["verificacion"],
    "reapertura": resultados["reapertura"],
    "limites": resultados["limites"],
}

# ---------------------------------------------------------------------- md
filas_md = "\n".join(
    f"| {k} | {v['estado']} | {v['evidencia']} |" for k, v in ficha.items()
)
fuentes_md = "\n".join(
    f"| {rel} | {v['sha256']} | {v['bytes']} |" for rel, v in fuentes_sha.items()
)
comprob_md = "\n".join(
    f"| {c['id']} | {c['estado']} | {c['detalle']} |" for c in comprobaciones
)

md = f"""# A1-911 v002 — Llamadas Improcedentes <> Procedentes 911: BLOQUEADO

Par `{PID}`.

Pregunta: {PREGUNTA}

Resultado: **bloqueado**. No se calculo proporcion ni se ejecuto join. Todo lo
de abajo lo produce `scripts/comprobar_a1_911.py` leyendo las fuentes locales.

## Ficha de ocho comprobaciones

| Eje | Estado | Evidencia |
| --- | --- | --- |
{filas_md}

## Hallazgos verificados

- **Duplicado entre conjuntos.** `{IMPRO_Q1_FALSO}` (conjunto A) es byte a byte
  `{PROC_Q1}` (conjunto B): sha `{dup_sha}`, {recursos[PROC_Q1]['bytes_leidos']} bytes, hoja
  `LLAMADAS PROCEDENTES 911`. El "Q1 de improcedentes" del conjunto A es en
  realidad procedentes Q1; su URL tambien apunta al archivo de procedentes.
- **Diccionarios identicos** (`{sha_dicc}`): 7 variables, `Unidad de medida` vacia en todas,
  sin identificador declarado (6 con `Identificadores` vacio; `hora` solo con texto residual),
  sin variable `motivo no procedente` (columna de improcedentes Q2 sin definicion).
- **Q2 improcedentes sin MUNICIPIO.** `{IMPRO_Q2}` tiene solo
  {', '.join(recursos[IMPRO_Q2]['columnas'])}; no admite corte por municipio.
- **La muestra A del lote sale del duplicado.** `{IMPRO_Q1_FALSO}` vs `{PROC_Q2}`:
  la comparacion muestral es procedentes Q1 contra procedentes Q2; no hay ninguna
  observacion de improcedentes.
- **Familias territoriales solo por el duplicado.** En el cruce, municipio, localidad y
  division territorial enlazan unicamente columnas de `{IMPRO_Q1_FALSO}`. Al excluir el
  duplicado, la unica familia compartida real es periodo (FECHA), con valores sin verificar.
- **Coincidencias muestrales de MUNICIPIO: {cmp_municipio['coincidencias_exactas_muestra']}** en n=29
  ({', '.join(cmp_municipio['ejemplos_coincidentes'])}). El lote las califica:
  "{cmp_municipio['interpretacion']}".
- **Sin particion del universo.** Ningun recurso del par declara total ni particion; los 6
  son XLSX/CSV de datos o diccionario, sin descripcion documental.
- **Sin copias locales de filas 911:** 0 archivos xlsx/xls/csv. Solo bytes y SHA de
  inspeccion, por lo que no hay numeradores ni denominadores.

## Comprobaciones

| Comprobacion | Estado | Detalle |
| --- | --- | --- |
{comprob_md}

## Verificacion reproducible

```
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/comprobar_a1_911.py
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/tests/test_a1_911.py
uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/sellar.py
```

Sin marcas de tiempo en la salida: dos ejecuciones producen bytes identicos.
`tests/test_a1_911.py` lo comprueba y ademas coteja los ficheros entregados con
la salida del script y el sello.

## Fuentes (SHA calculado al ejecutar)

| Fuente | sha256 | bytes |
| --- | --- | --- |
{fuentes_md}

## Reapertura

{chr(10).join('- ' + x for x in resultados['reapertura'])}

## Limites

{chr(10).join('- ' + x for x in resultados['limites'])}
"""


def volcar(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


salida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
salida.mkdir(parents=True, exist_ok=True)
(salida / "resultados.json").write_bytes(volcar(resultados).encode("utf-8"))
(salida / "entrega.json").write_bytes(volcar(entrega).encode("utf-8"))
(salida / "entrega.md").write_bytes(md.encode("utf-8"))

print(f"recursos={len(recursos)} duplicado={dup_sha[:12]} proporcion=bloqueada join=false")
print(f"escrito en {salida}")
print("A1-911 v002: comprobaciones OK (bloqueo documentado, sin join).")
