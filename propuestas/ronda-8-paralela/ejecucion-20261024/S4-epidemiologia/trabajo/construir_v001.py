# -*- coding: utf-8 -*-
"""Construye v001/entrega.json + entrega.md + congelada.json para S4-epidemiologia (ronda-8-paralela/ejecucion-20261024)."""
import hashlib
import io
import json
import re
from pathlib import Path

BASE = Path(".")
S4 = BASE / "propuestas/ronda-8-paralela/ejecucion-20261024/S4-epidemiologia"
V001 = S4 / "v001"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


asig = json.loads((S4 / "asignacion.json").read_bytes().decode("utf-8"))
assert len(asig["casos"]) == 25

dic = json.loads(io.open(
    "data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json",
    encoding="utf-8").read())
defs = dic["definiciones"]
rec = json.loads(io.open(
    "data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json",
    encoding="utf-8").read())
pos = {c["id"]: c["posicion_original"] for c in rec["tablas"][0]["campos"]}

MAN = {
    "/9": ("p18", "Manual p18: cada enfermedad incluye codigo CIE 10 (generico nacional, sin version/edicion); ejemplo local A04/A08-A09 no aparece en el manual."),
    "/11": ("p26", "Manual p26: acumulado = total de casos acumulados hasta la semana epidemiologica del ano actual (concepto analitico nacional, no regla de computo de la columna local pos 11)."),
    "/13": ("p18", "Manual p18: formato nacional de 30 columnas con tabulacion por edad (layout distinto de las 59 locales); no fija intervalo 01-04 ni resuelve contradiccion nombre/descripcion ni solape edad 5."),
    "/23": ("p50", "Manual p50: recuadro Ign. = casos de edad ignorada en pantalla SUAVE nacional; no es definicion de la columna local pos 23 ni vinculo edicion-recurso-periodo."),
}
FALTA = {
    "/9": "EPI-R6-01 + EPI-R6-03: instrumento SUIVE edicion aplicable 2022 que fije objeto de cve_cie10 y version de catalogo CIE vinculada al recurso 1689b19c; o diccionario corregido/nota del publicador.",
    "/11": "EPI-R6-01 + EPI-R6-02: documento del publicador que fije objeto y periodo/regla de acumulacion de la columna pos 11; o diccionario corregido con regla de computo (totalm/totalf no la definen).",
    "/13": "EPI-R6-01 + EPI-R6-03: nota del publicador que fije el intervalo real (nombre 01-04 vs descripcion entre 1 y 5) y el tratamiento de la edad 5 frente a de05_a_09.",
}


def grupo(suf):
    if suf in MAN:
        return MAN[suf]
    n = int(suf[1:])
    if 24 <= n <= 35:
        return ("p18", "Manual p18: subdivision por sexo del formato nacional; no define la convencion de sufijo f local. Inferir f=femenino por totalf esta prohibido sin respaldo explicito.")
    return ("p17", "Manual p17: instituciones nacionales SSA, IMSS, ISSSTE, Otras, IMSS-Prospera, DIF, PEMEX, SEDENA, SEMAR; conjunto DISTINTO de las 9 columnas locales (imss_ord/imss_sol/d_if/sedemar vs IMSS-Prospera/DIF/SEMAR). Sin equivalencia autorizada.")


def faltante(suf, var, pp):
    if suf in FALTA:
        return FALTA[suf]
    return ("EPI-R6-01 + EPI-R6-02: diccionario corregido con descripcion para la columna "
            "%s pos %s, o nota del publicador que fije su sentido literal citando "
            "conjunto+diccionario+fila+huella y vincule edicion-recurso-periodo." % (var, pp))


E1 = "data/portal/inspecciones/2334deaa-dd0c-444e-b038-4cc556ad715d.json"
E2 = "data/portal/inspecciones/1689b19c-b0dc-4e39-bf07-e3a2e684ef1a.json"
E3 = "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/W-web/paquete-v002/diccionario-vigilancia-epidemiologica_2026-10-24.csv"
E4 = "propuestas/investigacion-post-r6/epidemiologia/evidencia/examen_manual_suive32_paginas.txt"
E5 = "propuestas/investigacion-post-r6/epidemiologia/evidencia/http_log.json"
H = {e: sha(e) for e in [E1, E2, E3, E4, E5]}

GATE = (" Puerta primera 2026-10-24: package_show en vivo sin cambios "
        "(metadata_modified 2025-08-19, version null, fuentes_extras vacia); "
        "revision_list API devuelve 400; indice web del CSV reproduce las mismas "
        "descripciones ya documentadas sin instrumento nuevo; Definiciones "
        "Operacionales DGE mar-2021 es referente nacional generico sin vinculo "
        "campo/recurso/edicion y no se descarga como novedad. Correccion de revision "
        "local: el cuerpo guardado de datastore_search 2026-10-24 es pagina de bloqueo "
        "WAF (BWAF Acceso no permitido), no filas; la confirmacion en vivo de "
        "descripciones la aporta la re-descarga W-v002 (F-V002-04-EPI-DICC, CSV "
        "identico, sin revision posterior a 2024-10-31). Sin pista nueva concreta; "
        "no se re-emite peticion a W (prohibido repetir busquedas agotadas). "
        "Se conserva la evidencia previa con SHAs re-verificados por codigo.")
WREAP = ("; o si W-web aporta revision del diccionario posterior a 2024-10-31 o nota "
         "del publicador que lo resuelva (WEB-S4-01 ya atendida en ejecucion previa "
         "sin hallazgo resolutivo: F-V002-04-EPI-DICC).")
WLIM = ("Peticion WEB-S4-01 atendida en ejecucion previa (W-v002 F-V002-04-EPI-DICC): "
        "sin revision del diccionario posterior a 2024-10-31; CSV re-descargado identico. "
        "No se re-emite peticion en esta ejecucion (sin pista primaria nueva concreta; "
        "prohibido repetir busquedas agotadas y re-presentar material conocido como novedad).")

decisiones = []
for c in asig["casos"]:
    suf = "/" + c["id"].rsplit("%2F", 1)[-1]
    m = re.match(r"/definiciones/(\d+) \(Nombre variable=([^)]+)\)",
                 c["evidencia"][0]["localizador"])
    di = int(m.group(1))
    vname = m.group(2)
    x = defs[di]
    dk = [k for k in x if "escrip" in k.lower()][0]
    ck = [k for k in x if "logo" in k.lower()][0]
    ek = [k for k in x if "jemplo" in k.lower()][0]
    assert x["Nombre variable"] == vname, (di, vname)
    assert x[ck] == "", (di, vname)
    pp = pos[vname]
    desc = x[dk]
    ej = x[ek]
    pg, man_txt = grupo(suf)
    motivo = (man_txt + " Sin respaldo explicito vinculado a esta definicion; no se aprueba "
              "por nombre, ejemplo aislado ni catalogo nacional generico sin vinculo local. "
              "Criterio R6 conservado." + GATE)
    falt = faltante(suf, vname, pp)
    ev = [
        {"ruta": E1, "sha256": H[E1],
         "localizador": "/definiciones/%d (Nombre variable=%s)" % (di, vname),
         "afirmacion_soportada": "Descripcion='%s', catalogo de referencia vacio, ejemplo registrado '%s'." % (desc, ej)},
        {"ruta": E2, "sha256": H[E2],
         "localizador": "hoja=SUIVE posicion_original=%d (id=%s)" % (pp, vname),
         "afirmacion_soportada": "Columna fisica %s observada en pos %d del esquema de 59 campos; sin documentar su computo." % (vname, pp)},
        {"ruta": E3, "sha256": H[E3],
         "localizador": "fila Nombre variable=%s (re-descarga W-v002 2026-10-24, 59 filas)" % vname,
         "afirmacion_soportada": "Diccionario vigente re-descargado en vivo 2026-10-24 identico: Descripcion='%s', catalogo vacio." % desc},
        {"ruta": E4, "sha256": H[E4],
         "localizador": "paginas del manual: " + pg,
         "afirmacion_soportada": man_txt},
        {"ruta": E5, "sha256": H[E5],
         "localizador": "consultas package_show/datastore/manual + 403 xlsx/csv/boletin",
         "afirmacion_soportada": "Package sin cambios (fuentes_extras vacio, version null); manual fresco byte-identico Last-Modified 2021-08-10 < periodo 2022; descargas bloqueadas 403 sin evadir; cuerpo datastore guardado = bloqueo WAF."},
    ]
    decisiones.append({
        "id": c["id"], "tipo": c["tipo"], "original_sha256": c["original_sha256"],
        "puerta": "sin_pista_nueva", "pista": None, "estado": "brecha_externa",
        "afirmacion_propuesta": None, "motivo": motivo,
        "evidencia_faltante": falt, "evidencia": ev,
        "condicion_reapertura": "Reabrir si aparece: " + falt + WREAP,
        "limites": ["Alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion; no autoriza cruces, homologaciones ni equivalencias.",
                    "Evidencia negativa acotada a las busquedas 2026-10-24 documentadas en http_log.json, no ausencia universal.",
                    WLIM],
    })

fuentes = [
    {"ruta": E1, "sha256": H[E1], "url": None, "fecha_consulta": None,
     "localizador": "Diccionario del conjunto (59 definiciones); filas citadas por ID."},
    {"ruta": E2, "sha256": H[E2], "url": None, "fecha_consulta": None,
     "localizador": "Hoja SUIVE del recurso 1689b19c (esquema de 59 campos)."},
    {"ruta": E3, "sha256": H[E3],
     "url": "https://datos.sonora.gob.mx/dataset/dca16d84-dbf0-4501-b702-dc6372a480ea",
     "fecha_consulta": "2026-10-24",
     "localizador": "Diccionario vigente re-descargado en vivo por W-v002 (F-V002-04-EPI-DICC): 59 filas, descripciones identicas."},
    {"ruta": E4, "sha256": H[E4],
     "url": "https://epidemiologia.salud.gob.mx/gobmx/salud/documentos/manuales/32_ManualSuive.pdf",
     "fecha_consulta": "2026-10-24",
     "localizador": "Paginas p17/p18/p26/p50: referentes nacionales sin vinculo local."},
    {"ruta": E5, "sha256": H[E5],
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=dca16d84-dbf0-4501-b702-dc6372a480ea",
     "fecha_consulta": "2026-10-24",
     "localizador": "Consultas package_show/datastore/manual + 403 xlsx/csv/boletin."},
]

entrega = {
    "rol": "S4-epidemiologia",
    "version": "v001",
    "decisiones": decisiones,
    "fuentes": fuentes,
    "novedades": ("Puerta primera 2026-10-24 sobre 25 IDs: sin pista nueva concreta en ninguno; "
                  "0 propuestas, 25 brechas externas. WEB-S4-01 ya atendida en ejecucion previa "
                  "(W-v002 F-V002-04-EPI-DICC) sin hallazgo resolutivo; no se re-emite peticion. "
                  "Correccion de revision local: el cuerpo datastore 2026-10-24 guardado es bloqueo "
                  "WAF, no filas; la confirmacion en vivo la da el CSV W-v002 identico. El trabajo "
                  "local queda cerrado y solo se reabre por adenda/v002 si aparece instrumento del publicador."),
}

V001.mkdir(parents=True, exist_ok=True)
(V001 / "entrega.json").write_text(
    json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lineas = ["# S4-epidemiología — entrega v001 (2026-10-24)",
          "",
          "25 IDs, 0 propuestas, 25 brechas externas. Puerta: `sin_pista_nueva` en todos.",
          "WEB-S4-01 ya atendida en ejecución previa sin hallazgo resolutivo; sin re-emisión (sin pista nueva concreta).",
          "",
          "| ID (sufijo) | variable | estado |",
          "| --- | --- | --- |"]
for d in decisiones:
    suf2 = d["id"].rsplit("%2F", 1)[-1]
    var2 = re.match(r"/definiciones/\d+ \(Nombre variable=([^)]+)\)",
                    d["evidencia"][0]["localizador"]).group(1)
    lineas.append("| ...%%2F%s | %s | brecha_externa |" % (suf2, var2))
lineas += ["",
           "Documento exacto faltante por grupo: ver `evidencia_faltante` de cada decisión en `entrega.json` (EPI-R6-01/02/03).",
           "Reapertura: diccionario corregido o nota del publicador con vínculo campo/recurso/edición/periodo; o hallazgo resolutivo de W-web (adenda/v002)."]
(V001 / "entrega.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

# Verificacion + congelada (todo hash recalculado, nada a mano)
carg = json.loads((V001 / "entrega.json").read_text(encoding="utf-8"))
assert len(carg["decisiones"]) == 25
assert [d["id"] for d in carg["decisiones"]] == [c["id"] for c in asig["casos"]]
for d in carg["decisiones"]:
    assert d["estado"] == "brecha_externa"
    assert d["afirmacion_propuesta"] is None
    assert len(d["evidencia"]) == 5
    for e in d["evidencia"]:
        assert e["sha256"] == sha(e["ruta"]), e["ruta"]
    assert d["evidencia_faltante"] and d["condicion_reapertura"]
for f in carg["fuentes"]:
    assert f["sha256"] == sha(f["ruta"]), f["ruta"]

archivos = [{"ruta": "propuestas/ronda-8-paralela/ejecucion-20261024/S4-epidemiologia/v001/entrega.json",
             "sha256": sha("propuestas/ronda-8-paralela/ejecucion-20261024/S4-epidemiologia/v001/entrega.json")},
            {"ruta": "propuestas/ronda-8-paralela/ejecucion-20261024/S4-epidemiologia/v001/entrega.md",
             "sha256": sha("propuestas/ronda-8-paralela/ejecucion-20261024/S4-epidemiologia/v001/entrega.md")}]
congelada = {"rol": "S4-epidemiologia", "version": "v001", "archivos": archivos,
             "conteos": {"decisiones": 25, "brecha_externa": 25,
                         "propuesta_para_auditar": 0, "acceso_no_resuelto": 0}}
(V001 / "congelada.json").write_text(
    json.dumps(congelada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK v001: 25 decisiones verificadas; congelada escrita.")
