"""M2-sinac v003: corrige defecto de v002 (descripcion adoptaba el descriptor
nacional; en 74/76 introducia CIE-10/0000 no aprobados en R7). v001/v002
preservadas e intactas. Descripcion = literal local exacto de cada fila
('Pendiente de especificar'); evidencia/criterio solo vinculo fisico +
significado minimo R7 ya aprobado. Modelo: M1-sinac v001."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
M2 = ROOT / "propuestas/ronda-8-paralela/ejecucion-20261024/M2-sinac"
V = M2 / "v003"
INSP = ROOT / "data/portal/contenido-inspeccion.json"
COB = ROOT / "propuestas/ronda-8-paralela/ejecucion-20261024/cobertura-r7.json"
S2 = ROOT / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/v002/entrega.json"
R7 = ROOT / "reports/ronda-7.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def huella(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


asig = json.loads((M2 / "asignacion.json").read_text(encoding="utf-8"))
insp = json.loads(INSP.read_text(encoding="utf-8"))
cob = json.loads(COB.read_text(encoding="utf-8"))
recs = {r["id"]: r for r in insp["recursos"]}
REC = recs["46977217-9396-4f9c-bddb-6616e82530b4"]
DICC = recs["22202305-2d02-4c49-b216-cc98224357f0"]
campos = REC["tablas"][0]["campos"]
defs = DICC["definiciones"]
var_by_iri = {v["iri"]: v for v in cob["variables"] if "iri" in v}
corr_by_col = {x["columna"]: x for x in cob["correspondencias"]}

SHA_INSP = sha(INSP)
SHA_COB = sha(COB)
SHA_S2 = sha(S2)

# unicidad de nombres (M1: pruebas por caso)
nombres_campos = [c["id"] for c in campos]
nombres_defs = [d["Nombre variable"] for d in defs]
assert len(set(nombres_campos)) == len(nombres_campos) == 106
assert len(set(nombres_defs)) == len(nombres_defs) == 106
assert huella(REC["tablas"][0]) == "9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95"

RUTAS = ["data/portal/contenido-inspeccion.json",
         "propuestas/ronda-8-paralela/ejecucion-20261024/cobertura-r7.json",
         "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/v002/entrega.json"]

decisiones = []
vinculos = []
origenes = {}
for caso in asig["casos"]:
    n = int(caso["variable"].split("%2F")[1])
    campo, concepto = caso["campo"], caso["concepto"]
    regla = caso["definicion"]["regla"]
    idef = caso["definicion"]["definicion_iri"]
    # fisico
    assert campos[n - 1]["id"] == campo and campos[n - 1]["posicion_original"] == n
    assert defs[n - 1]["Nombre variable"] == campo
    hfila = huella(defs[n - 1])
    assert hfila == caso["definicion"]["huella_fila_diccionario"]
    desc_local = defs[n - 1]["Descripción"]
    assert desc_local == "Pendiente de especificar" == caso["definicion"]["descripcion"]
    # payload cobertura R7 exacto
    v = var_by_iri[caso["variable"]]
    assert v["definicion_iri"] == idef, campo
    assert v["concepto"] == concepto, campo
    assert v["diccionario"] == "22202305-2d02-4c49-b216-cc98224357f0", campo
    assert v["descripcion"] == "Pendiente de especificar", campo
    assert v["huella_fila_diccionario"] == hfila, campo
    assert v["estado"] == "respaldada_por_definicion", campo
    mc = corr_by_col[caso["columna"]]
    assert mc["estado"] == "candidata_por_nombre", campo
    assert mc["variable"] == caso["variable"], campo

    ev = [
        {"ruta": RUTAS[0], "sha256": SHA_INSP,
         "localizador": (f"recurso 46977217 tablas[0]: hoja SINAC 2022 26-09-22, fila_encabezado 1, 106 campos; "
                         f"campos[posicion_original={n}].id={campo} (unico)"),
         "afirmacion_soportada": f"La columna fisica existe en el esquema del recurso con nombre exacto {campo} en ordinal {n}, sin duplicados."},
        {"ruta": RUTAS[0], "sha256": SHA_INSP,
         "localizador": (f"recurso 22202305 definiciones[{n - 1}] (fila {n}): Nombre variable={campo}; "
                         f"huella_fila={hfila}"),
         "afirmacion_soportada": f"La fila del diccionario existe con nombre exacto {campo} en ordinal {n} y huella coincidente con R7."},
        {"ruta": RUTAS[1], "sha256": SHA_COB,
         "localizador": (f"variables {caso['variable']}: estado=respaldada_por_definicion, concepto={concepto}, regla={regla}; "
                         f"correspondencias {caso['columna']}: estado=candidata_por_nombre, variable={caso['variable']}"),
         "afirmacion_soportada": "El significado esta respaldado en R7 y la correspondencia es candidata sin revision previa; variable y definicion_iri coinciden exactos."},
        {"ruta": RUTAS[2], "sha256": SHA_S2,
         "localizador": f"decision {regla}: estado propuesta_para_auditar; fuente_revision de la definicion local",
         "afirmacion_soportada": "El significado del caso esta fijado por S2-nacimientos v002 (auditoria A/B pendiente); este vinculo no crea regla ni concepto nuevo."},
    ]
    vinculo = {
        "campo": campo,
        "columna": caso["columna"],
        "concepto": concepto,
        "criterio": (f"Revision explicita de la columna fisica pos {n} ({campo}) de la hoja SINAC 2022 26-09-22 del recurso "
                     f"46977217-9396-4f9c-bddb-6616e82530b4 y de su fila {n} del diccionario 22202305-2d02-4c49-b216-cc98224357f0 "
                     f"en el mismo conjunto 940de7d8-73ec-4a08-8d26-b7cc97ff17bd: nombre exacto, ordinal coincidente, "
                     f"descripcion Pendiente de especificar y huella de fila {hfila}."),
        "definicion_iri": idef,
        "descripcion": "Pendiente de especificar",
        "diccionario": "22202305-2d02-4c49-b216-cc98224357f0",
        "huella_esquema": huella(REC["tablas"][0]),
        "huella_fila_diccionario": hfila,
        "recurso": caso["recurso"],
    }
    vinculos.append(vinculo)
    origenes[caso["columna"]] = list(RUTAS)
    decisiones.append({
        "id": caso["iri"],
        "tipo": "correspondencias",
        "estado": "propuesta_para_auditar",
        "afirmacion_propuesta": (f"La columna fisica pos {n} ({campo}) de la hoja SINAC 2022 26-09-22 del recurso "
                                 f"46977217-9396-4f9c-bddb-6616e82530b4 corresponde a la variable documentada fila {n} ({campo}) "
                                 f"del diccionario 22202305-2d02-4c49-b216-cc98224357f0 (definicion {idef}), mismo conjunto 940de7d8, "
                                 f"descripcion Pendiente de especificar, concepto {concepto} ({regla}). Alcance: solo este recurso y esta "
                                 f"definicion local; no autoriza otra edicion, adopcion global, totalidad de catalogos, equivalencias, joins ni vigencias."),
        "motivo": (f"Correspondencia formal suficiente verificada en inspecciones originales: 1) sistema: recurso y diccionario en el mismo "
                   f"conjunto 940de7d8 del portal; 2) recurso: hoja SINAC 2022 26-09-22 con 106 campos, columna de nombre exacto en ordinal {n} "
                   f"sin duplicados; 3) fila {n} del diccionario con nombre exacto y huella {hfila} coincidente con R7; 4) significado ya respaldado "
                   f"({regla}, {concepto}) con descripcion Pendiente de especificar; no se aprueba por nombre solo sino por esquema+fila+huella+significado. "
                   f"Expediente R7 (cierre, paquetes W v001-v004, S2 v002) revisado; sin busquedas genericas repetidas y sin pista web nueva: no se escribe peticiones-web.json."),
        "evidencia": ev,
        "evidencia_faltante": None,
        "condicion_reapertura": ("Si la auditoria rechaza el vinculo, revierte a brecha_externa con el motivo del dictamen; "
                                 "reapertura con fe de erratas del publicador o instrumento que corrija ordinal/nombre."),
        "limites": caso["definicion"]["limites"],
        "vinculo_propuesto": vinculo,
        "origenes": list(RUTAS),
    })

print("verificacion fisica + cobertura R7 OK: 14/14")
entrega = {
    "rol": "M2-sinac",
    "version": "v003",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "modelo": "opencode-go/muse-spark-1.3-contributor",
    "base": {"asignacion_sha256": sha(M2 / "asignacion.json"), "ronda7_sha256": sha(R7),
             "cobertura_r7_sha256": SHA_COB, "inspeccion_sha256": SHA_INSP, "s2_v002_sha256": SHA_S2},
    "resumen": {"casos_asignados": 14, "propuestas_para_auditar": 14, "brechas_externas": 0,
                "accesos_no_resueltos": 0, "peticiones_web": 0},
    "decisiones": decisiones,
    "vinculos_propuestos": vinculos,
    "origenes": origenes,
    "origenes_sha256": {r: sha(ROOT / r) for r in RUTAS},
    "pruebas_verificables": ("Para cada caso: unicidad del nombre en los 106 campos del recurso y en las 106 filas del diccionario; "
                             "igualdad de ordinales columna-posicion_original y fila-indice; huella_esquema=9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95 "
                             "y huella_fila recomputadas por codigo (hashlib.sha256, json sort_keys) coincidentes con R7; estado respaldada_por_definicion "
                             "con mismo concepto, regla, definicion_iri, descripcion y huella en cobertura-r7.json; correspondencia candidata_por_nombre con variable exacta. "
                             "Descriptor y catalogos nacionales no se invocan como vinculo fisico."),
}
V.mkdir(parents=True, exist_ok=True)
(V / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1), encoding="utf-8")

filas = "\n".join(f"| {i + 1} | {d['vinculo_propuesto']['campo']} ({d['vinculo_propuesto']['columna'].split('%2F')[-1]}) "
                  f"| {d['vinculo_propuesto']['columna'].split('%2F')[-1]} | {d['vinculo_propuesto']['concepto']} / {asig['casos'][i]['definicion']['regla']} | {d['estado']} |"
                  for i, d in enumerate(decisiones))
md = "\n".join([
    "# M2-sinac v003 — 14 correspondencias nuevas SINAC (propuestas para auditar)",
    "",
    "Corrige v002 (descripcion adoptaba el descriptor nacional; v001/v002 intactas). Descripcion = literal local exacto.",
    "Rol M2-sinac: ultimas 14 correspondencias nuevas SINAC; evidencia fisica y significado R7 exactos. Modelo opencode-go/muse-spark-1.3-contributor.",
    "",
    "## Resultado",
    "",
    "- 14/14 casos verificados como correspondencia formal suficiente: propuesta_para_auditar. 0 brechas, 0 accesos no resueltos.",
    "- Vinculos propuestos con formato ontologia/semantica.json.vinculos_documentales_revisados (columna, campo, recurso, diccionario, definicion_iri, concepto, descripcion, huella_esquema, huella_fila_diccionario, criterio). Sin reglas ni conceptos nuevos.",
    "- Significado ya respaldado en R7 (S2-nacimientos v002, auditoria A/B pendiente); aqui solo se acredita el alcance fisico columna<->fila.",
    "- Expediente R7 revisado (cierre, paquetes W-web v001-v004, S2 v002, reports/ronda-7.json/md): sin busquedas genericas repetidas. Sin pista primaria nueva: no se escribe peticiones-web.json (solo W usa Obscura).",
    "",
    "## Pruebas verificables (por caso)",
    "",
    "1. Nombre unico en los 106 campos de la hoja SINAC 2022 26-09-22 y en las 106 filas del diccionario; ordinal columna = posicion_original y fila = indice; nombre exacto en ambos.",
    "2. huella_esquema = 9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95 y huella_fila recomputadas por codigo coinciden con R7.",
    "3. cobertura-r7.json: variable en estado respaldada_por_definicion con mismo concepto, regla, definicion_iri, descripcion y huella; correspondencia en estado candidata_por_nombre con variable exacta, sin revision previa.",
    "",
    "## Decisiones",
    "",
    "| # | Campo (pos) | Variable (fila) | Concepto / regla | Estado |",
    "| --- | --- | --- | --- | --- |",
    filas,
    "",
    "## Evidencia y SHA-256 (calculados por codigo)",
    "",
    "| Archivo | SHA-256 |",
    "| --- | --- |",
    *[f"| {r} | {sha(ROOT / r)} |" for r in RUTAS],
    f"| asignacion.json | {sha(M2 / 'asignacion.json')} |",
    f"| reports/ronda-7.json | {sha(R7)} |",
    "",
    "## Alcance y limites",
    "",
    "- Cada afirmacion vale solo para el recurso 46977217-9396-4f9c-bddb-6616e82530b4 (hoja SINAC 2022 26-09-22) y la definicion local fijada; no autoriza otra edicion, adopcion global, totalidad de catalogos, equivalencias, joins ni vigencias.",
    "- Descriptor y catalogos nacionales DGIS pertenecen al registro nacional, no al extracto Sonora; no se invocan como vinculo fisico.",
    "- Congelada: correcciones solo en v004, sin editar v003.",
    ""]) + "\n"
(V / "entrega.md").write_text(md, encoding="utf-8")
print("v003 entrega.json + entrega.md escritos")
