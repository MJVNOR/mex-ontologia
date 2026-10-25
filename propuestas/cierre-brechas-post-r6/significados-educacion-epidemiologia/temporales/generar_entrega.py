"""Genera entrega.json / entrega.md / cierrelisto.json para significados-educacion-epidemiologia.

Reusa los 55 casos de asignacion.json como `original` literal; no inventa
fuentes: solo re-verifica hashes desde bytes y suma la Guia UES feb2023
(novedad matizada, no resolutoria). Serializa con json.dumps.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(".")
CARP = Path("propuestas/cierre-brechas-post-r6/significados-educacion-epidemiologia")

asig = json.loads((CARP / "asignacion.json").read_text(encoding="utf-8"))
assert asig["tarea"] == "significados-educacion-epidemiologia"
assert asig["clave_id"] == "definicion_iri"
assert len(asig["casos"]) == 55, len(asig["casos"])

# Re-verificacion de hashes desde bytes (2026-10-24).
rutas = {e["ruta"]: e["sha256"] for c in asig["casos"] for e in c["evidencia"]}
for r, esp in sorted(rutas.items()):
    h = hashlib.sha256((BASE / r).read_bytes()).hexdigest()
    assert h == esp, (r, esp, h)

GUIA_PDF = "propuestas/cierre-brechas-post-r6/significados-educacion-epidemiologia/Guia_Opciones_Titulacion_UES_feb2023.pdf"
GUIA_TXT = "propuestas/cierre-brechas-post-r6/significados-educacion-epidemiologia/Guia_Opciones_Titulacion_UES_feb2023.txt"
GUIA_URL = "https://ues.mx/archivos/alumnos/reglamentos/Guia%20de%20Opciones%20de%20Titulacion%20Nivel%20Licenciatura%20feb2023.pdf"

NOVEDAD_GUIA = (
    " Novedad 2026-10-24 (no resolutoria): Guia UES feb2023 examinada por primera vez"
    " (Last-Modified 2023-03-10, posterior al periodo 2022-2): 'Constancia de No Exigibilidad"
    " del Examen Profesional' aparece 4 veces como tramite de Control Escolar, no como"
    " alternativa de titulacion ni vinculada a fila+huella+periodo; no acredita /63 ni /64."
)

decisiones = []
for c in asig["casos"]:
    iri = c["definicion_iri"]
    motivo = c["motivo"] + (
        " Ultima revision 2026-10-24 (cierre-brechas): hashes de evidencia re-verificados"
        " desde bytes; sin fuente primaria nueva con vinculo campo/recurso/edicion/periodo;"
        " peticiones web pendientes en web-obscura (peticiones-web.json)."
    )
    if iri.endswith("%2F63") or iri.endswith("%2F64"):
        motivo += NOVEDAD_GUIA
    decisiones.append({
        "id": iri,
        "estado": "sigue_pendiente",
        "original": c,
        "motivo": motivo,
        "evidencia_faltante": c["evidencia_faltante"],
        "evidencia": [
            {"ruta": e["ruta"], "sha256": e["sha256"],
             "localizador": e["localizador"],
             "afirmacion_soportada": e["afirmacion_soportada"]}
            for e in c["evidencia"]
        ],
        "limites": c["limites"],
    })

ids = [d["id"] for d in decisiones]
assert len(ids) == 55 and len(set(ids)) == 55

fuentes = [
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/package_show_2026-10-24.json",
     "sha256": "0a09e4667f14edee56e8ae5e931d22b7766161621b765ed8f88c295c1f2a68d1",
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=dca16d84-dbf0-4501-b702-dc6372a480ea",
     "fecha_consulta": "2026-10-24",
     "localizador": "result.resources[1] edicion 2022; result.fuentes_extras; result.version"},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/datastore_diccionario_2026-10-24.json",
     "sha256": "dfe6e73b759a22c5b0a2acc5c9b03573b5d1fed39cd088f5b542c907ca91b348",
     "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=2334deaa-dd0c-444e-b038-4cc556ad715d&limit=60&offset=0",
     "fecha_consulta": "2026-10-24",
     "localizador": "records[_id=9..44]"},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/examen_manual_suive32_paginas.txt",
     "sha256": "9c20cd10f4673483d449551e2a48613e5c030d73ad929aa7ff033f06bf7393cc",
     "url": "https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf",
     "fecha_consulta": "2026-10-24",
     "localizador": "pp. 17, 18, 24, 26, 50"},
    {"ruta": "propuestas/investigacion-post-r6/epidemiologia/evidencia/http_log.json",
     "sha256": "0f0c01573fe25b4e1a659fc01154b678b8a8956156787f8099f6af7876e706a0",
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=dca16d84-dbf0-4501-b702-dc6372a480ea",
     "fecha_consulta": "2026-10-24",
     "localizador": "consultas package_show/datastore/manual + 403 xlsx/csv/boletin"},
    {"ruta": "data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json",
     "sha256": "298786f09028a94004420c08eb28120294b130378a0cf12d609a1bffb950288d",
     "url": "", "fecha_consulta": "2026-10-24",
     "localizador": "/definiciones (diccionario epidemiologia, 59 filas)"},
    {"ruta": "data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json",
     "sha256": "31861377197a43619d42bf22a49c3b3f34b122f800f0f29d4d2fdf75a03a4c60",
     "url": "", "fecha_consulta": "2026-10-24",
     "localizador": "hoja=SUIVE, esquema de 59 campos"},
    {"ruta": "data/portal/inspecciones/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d.json",
     "sha256": "73c4f6243458d700a99df5d3c55327bc9fde1a94d75f94a443606237327574b2",
     "url": "", "fecha_consulta": "2026-10-24",
     "localizador": "/definiciones (diccionario matriculas)"},
    {"ruta": "propuestas/investigacion-post-r6/matriculas/evidencia/datastore_diccionario.json",
     "sha256": "c68a276e7aeff4e1d08ecc984ce48f25e34138f751f8d6988f57bdf25041ea0d",
     "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=8c0e76ff-3a86-4b1d-beee-b04bebe7df8d",
     "fecha_consulta": "2026-10-24",
     "localizador": "revalidacion live: 0 cambios en las 30 filas"},
    {"ruta": "propuestas/investigacion-post-r6/matriculas/evidencia/Matriculas-2022-2.xlsx",
     "sha256": "1b68919ce503511a167e2a375a695fee5447787322db2d7dc8132142ff3bdeaf",
     "url": "https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6",
     "fecha_consulta": "2026-10-24",
     "localizador": "hoja 'Estudiantes 2022-2', 15212 filas x 70 cols; distribuciones empiricas"},
    {"ruta": "propuestas/investigacion-post-r6/matriculas/evidencia/package_matriculas.json",
     "sha256": "8752e00e44cdcfd8a7c6bb556b7028754da5a7e2a3387c04182d6435d056d7b7",
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=e819466c-7282-46c5-84e9-65917dd8cc85",
     "fecha_consulta": "2026-10-24",
     "localizador": "recurso 58f2d5a6, periodo 2022-01-01 a 2022-06-01"},
    {"ruta": GUIA_PDF,
     "sha256": hashlib.sha256((BASE / GUIA_PDF).read_bytes()).hexdigest(),
     "url": GUIA_URL, "fecha_consulta": "2026-10-24",
     "localizador": "Last-Modified 2023-03-10; 'Constancia de No Exigibilidad del Examen Profesional' (tramite 2.2/3.2, 4 menciones)"},
    {"ruta": GUIA_TXT,
     "sha256": hashlib.sha256((BASE / GUIA_TXT).read_bytes()).hexdigest(),
     "url": GUIA_URL, "fecha_consulta": "2026-10-24",
     "localizador": "extraccion pypdf 6.21.2, 36 pp / 47033 chars; contexto de 'No Exigibilidad'"},
]

entrega = {
    "tarea": "significados-educacion-epidemiologia",
    "tipo": "significados",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades_frente_a_investigacion_previa": [
        "Guia UES de Opciones de Titulacion feb2023 examinada por primera vez (PDF+TXT preservados con SHA): "
        "'Constancia de No Exigibilidad del Examen Profesional' existe como tramite (4 menciones), no como "
        "alternativa de titulacion; Last-Modified 2023-03-10 posterior al periodo 2022-2 y sin vinculo a "
        "fila+huella: matiza la afirmacion de ausencia pero no resuelve /63 ni /64.",
        "Busquedas nativas 2026-10-24 (websearch): SUIVE solo devuelve el manual 32 ya examinado y un blog "
        "privado (no primario); UES solo devuelve la propia Guia 2023 y normativa ya examinada. Sin pista "
        "primaria nueva con vinculo campo/recurso/edicion/periodo.",
        "Re-verificacion desde bytes de las 8 rutas de evidencia citadas en la asignacion: 8/8 coinciden; "
        "variables/textos/huellas literales preservadas.",
        "Sin resultados web-obscura al cierre: peticiones WEB-EPI-01/02 y WEB-MAT-01/02 registradas en "
        "peticiones-web.json, pendientes del agente web-obscura.",
    ],
    "busquedas_limitadas": [
        {"proveedor_herramienta": "websearch nativa",
         "consulta": "SUIVE manual 2022 DGE vigilancia epidemiologica formato captacion edad sexo institucion",
         "fecha": "2026-10-24",
         "resultado": "Solo manual 32 ya examinado + blog privado saludtotal.mx (no primario). Sin pista nueva.",
         "fuente_primaria": "https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf (ya preservada en investigacion previa)"},
        {"proveedor_herramienta": "websearch nativa",
         "consulta": "UES Sonora Reglamento titulacion 'no exigibilidad' alternativa",
         "fecha": "2026-10-24",
         "resultado": "Guia UES feb2023 (novedad matizada, no resolutoria); resto normativa ya examinada.",
         "fuente_primaria": GUIA_URL},
        {"proveedor_herramienta": "descarga directa + pypdf 6.21.2",
         "consulta": "Guia UES feb2023, texto completo, terminos 'exigibilidad' / 'examen profesional' como alternativa",
         "url": GUIA_URL, "fecha": "2026-10-24",
         "resultado": "'No Exigibilidad' solo como constancia de tramite (4x); ninguna alternativa asi nombrada.",
         "fuente_primaria": GUIA_URL},
        {"proveedor_herramienta": "agente web-obscura (pendiente)",
         "consulta": "peticiones-web.json (WEB-EPI-01/02, WEB-MAT-01/02)",
         "fecha": "2026-10-24",
         "resultado": "Sin resultados en carpeta web-obscura al cierre de esta entrega.",
         "fuente_primaria": ""},
    ],
}

(CARP / "entrega.json").write_text(
    json.dumps(entrega, ensure_ascii=False, indent=2), encoding="utf-8")

lineas = ["# Cierre de brechas — significados educacion/epidemiologia (55 IDs)",
          "",
          "Resultado: **0 propuesta_resolucion, 55 sigue_pendiente**.",
          " Toda promocion exige fuente primaria con vinculo campo/recurso/edicion/periodo;",
          " homonimia, norma general sin vinculo e igualdad de valores no acreditan.",
          "",
          "## Unica novedad frente a investigacion previa (no resolutoria)",
          "",
          "- Guia UES de Opciones de Titulacion feb2023 (preservada con SHA en esta carpeta):",
          " 'Constancia de No Exigibilidad del Examen Profesional' existe como tramite de",
          " Control Escolar (4 menciones), no como alternativa de titulacion; edicion posterior",
          " al periodo 2022-2 y sin vinculo a fila+huella. Matiza la ausencia afirmada en R6,",
          " no resuelve /63 ni /64. Resto de busquedas nativas sin pista primaria nueva;",
          " web-obscura pendiente (peticiones-web.json).",
          "",
          "## Decisiones",
          "",
          "| ID | variable | estado | brecha exacta subsistente |",
          "|---|---|---|---|"]
for d in decisiones:
    frag = d["id"].split("%2F")[1]
    var = d["original"].get("variable")
    falt = d["evidencia_faltante"].replace("\n", " ")
    lineas.append(f"| ...%2F{frag} | {var} | sigue_pendiente | {falt} |")
lineas += ["",
           "Detalle por ID (motivo, evidencia con SHA re-verificado, limites): ver `entrega.json`.",
           "Fuentes: 12 (10 previas re-verificadas + Guia UES PDF/TXT nuevas).",
           "Propuestas revisables: ninguna; la integradora auditara antes de aplicar."]
(CARP / "entrega.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

# Verificacion de entrega.json.
chk = json.loads((CARP / "entrega.json").read_text(encoding="utf-8"))
assert len(chk["decisiones"]) == 55
assert [d["id"] for d in chk["decisiones"]] == [c["definicion_iri"] for c in asig["casos"]]
assert all(d["estado"] == "sigue_pendiente" for d in chk["decisiones"])
assert all("propuesta" not in d for d in chk["decisiones"])

archivos = ["peticiones-web.json", "entrega.json", "entrega.md",
            Path(GUIA_PDF).name, Path(GUIA_TXT).name,
            "temporales/generar_entrega.py"]
cierre = {
    "archivos": [{"ruta": str(CARP / n),
                  "sha256": hashlib.sha256((CARP / n).read_bytes()).hexdigest()}
                 for n in archivos],
    "conteos": {"decisiones": 55, "sigue_pendiente": 55,
                "propuesta_resolucion": 0, "fuentes": len(fuentes)},
}
(CARP / "cierrelisto.json").write_text(
    json.dumps(cierre, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK: 55 decisiones, 12 fuentes, %d archivos en cierrelisto." % len(archivos))
