"""Construye v001/entrega.json + entrega.md + congelada.json para S4-epidemiologia."""
import hashlib
import json
from pathlib import Path

BASE = Path(".")
S4 = BASE / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S4-epidemiologia"
V001 = S4 / "v001"
FECHA = "2026-10-24"

asig = json.loads((S4 / "asignacion.json").read_text(encoding="utf-8"))
assert asig["conteo"] == 25 and len(asig["casos"]) == 25

GATE = (" Puerta primera 2026-10-24: package_show en vivo sin cambios "
        "(metadata_modified 2025-08-19, version null, fuentes_extras vacia); "
        "revision_list API devuelve 400; indice web del CSV reproduce las mismas "
        "descripciones ya documentadas sin instrumento nuevo; Definiciones "
        "Operacionales DGE mar-2021 es referente nacional generico sin vinculo "
        "campo/recurso/edicion y no se descarga como novedad. Sin pista real; "
        "se conserva la evidencia previa con SHAs re-verificados.")

W_LIMITE = ("Peticion WEB-S4-01 a W-web pendiente (trabajo/peticiones-web.json): "
            "activity stream del conjunto y reintento de descarga por navegacion "
            "normal. Si aporta diccionario corregido o nota del publicador, "
            "reapertura por adenda/v002.")

W_REAP = ("; o si W-web (WEB-S4-01) aporta revision del diccionario posterior "
          "a 2024-10-31 o nota del publicador que lo resuelva.")


def reapert(faltante: str) -> str:
    base = "Reabrir si aparece: " + faltante
    return base + W_REAP


def sha_of(path: str) -> str:
    return hashlib.sha256((BASE / path).read_bytes()).hexdigest()


decisiones = []
for caso in asig["casos"]:
    o = caso["original"]
    oh = hashlib.sha256(
        json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    ev = [
        {"ruta": e["ruta"], "sha256": sha_of(e["ruta"]),
         "localizador": e["localizador"],
         "afirmacion_soportada": e["afirmacion_soportada"]}
        for e in o["evidencia"]
    ]
    decisiones.append({
        "id": caso["id"],
        "tipo": caso["tipo"],
        "original_sha256": oh,
        "puerta": "sin_pista_nueva",
        "pista": None,
        "estado": "brecha_externa",
        "afirmacion_propuesta": None,
        "motivo": o["motivo"] + GATE,
        "evidencia_faltante": o["evidencia_faltante"],
        "evidencia": ev,
        "condicion_reapertura": reapert(o["evidencia_faltante"]),
        "limites": o["limites"] + [W_LIMITE],
    })

fuentes = [
    {"ruta": "data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json",
     "sha256": sha_of("data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json"),
     "url": None, "fecha_consulta": None,
     "localizador": "Diccionario del conjunto (59 definiciones); filas citadas por ID."},
    {"ruta": "data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json",
     "sha256": sha_of("data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json"),
     "url": None, "fecha_consulta": None,
     "localizador": "Hoja SUIVE del recurso 1689b19c (esquema de 59 campos)."},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/datastore_diccionario_2026-10-24.json",
     "sha256": sha_of("propuestas/investigacion-post-r6/epidemiologia/evidencia/datastore_diccionario_2026-10-24.json"),
     "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=2334deaa-dd0c-444e-b038-4cc556ad715d&limit=60&offset=0",
     "fecha_consulta": FECHA,
     "localizador": "records[_id=9/11/13/23-44]: descripciones en vivo, catalogo vacio."},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/examen_manual_suive32_paginas.txt",
     "sha256": sha_of("propuestas/investigacion-post-r6/epidemiologia/evidencia/examen_manual_suive32_paginas.txt"),
     "url": "https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf",
     "fecha_consulta": FECHA,
     "localizador": "Paginas p17/p18/p26/p50: referentes nacionales sin vinculo local."},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/http_log.json",
     "sha256": sha_of("propuestas/investigacion-post-r6/epidemiologia/evidencia/http_log.json"),
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=dca16d84-dbf0-4501-b702-dc6372a480ea",
     "fecha_consulta": FECHA,
     "localizador": "Consultas package_show/datastore/manual + 403 xlsx/csv/boletin."},
]

entrega = {
    "rol": "S4-epidemiologia",
    "version": "v001",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades": ("Puerta primera 2026-10-24 sobre 25 IDs: sin pista nueva en "
                  "ninguno; package_show en vivo sin cambios; 0 propuestas, "
                  "25 brechas externas. Peticion WEB-S4-01 a W-web pendiente; "
                  "el trabajo local queda cerrado y solo se reabre por adenda/v002 "
                  "si W aporta evidencia resolutiva."),
}

V001.mkdir(parents=True, exist_ok=True)
(V001 / "entrega.json").write_text(
    json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lineas = ["# S4-epidemiología — entrega v001 (2026-10-24)",
          "",
          "25 IDs, 0 propuestas, 25 brechas externas. Puerta: `sin_pista_nueva` en todos.",
          "Petición WEB-S4-01 a W-web pendiente; cierre local con reapertura condicionada.",
          "",
          "| ID (sufijo) | variable | estado |",
          "| --- | --- | --- |"]
for d in decisiones:
    suf = d["id"].rsplit("%2F", 1)[-1]
    var = next(c["original"]["variable"] for c in asig["casos"] if c["id"] == d["id"])
    lineas.append(f"| ...%2F{suf} | {var} | brecha_externa |")
lineas += ["",
           "Documento exacto faltante por grupo: ver `evidencia_faltante` de cada decisión en `entrega.json` (EPI-R6-01/02/03).",
           "Reapertura: diccionario corregido o nota del publicador con vínculo campo/recurso/edición/periodo; o hallazgo resolutivo de W-web (adenda/v002)."]
(V001 / "entrega.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

# Verificacion + congelada
carg = json.loads((V001 / "entrega.json").read_text(encoding="utf-8"))
assert len(carg["decisiones"]) == 25
assert [d["id"] for d in carg["decisiones"]] == [c["id"] for c in asig["casos"]]
for d in carg["decisiones"]:
    c = next(x for x in asig["casos"] if x["id"] == d["id"])
    oh = hashlib.sha256(
        json.dumps(c["original"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    assert d["original_sha256"] == oh, d["id"]
    for e in d["evidencia"]:
        assert e["sha256"] == sha_of(e["ruta"]), e["ruta"]
for f in carg["fuentes"]:
    assert f["sha256"] == sha_of(f["ruta"]), f["ruta"]

archivos = [{"ruta": "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S4-epidemiologia/v001/entrega.json",
             "sha256": sha_of("propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S4-epidemiologia/v001/entrega.json")},
            {"ruta": "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S4-epidemiologia/v001/entrega.md",
             "sha256": sha_of("propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S4-epidemiologia/v001/entrega.md")}]
congelada = {"rol": "S4-epidemiologia", "version": "v001", "archivos": archivos,
             "conteos": {"decisiones": 25, "brecha_externa": 25,
                         "propuesta_para_auditar": 0, "acceso_no_resuelto": 0}}
(V001 / "congelada.json").write_text(
    json.dumps(congelada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK v001:", len(decisiones), "decisiones verificadas; congelada escrita.")
