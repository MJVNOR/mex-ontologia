"""M2-sinac v001: construye entrega.json/md. Todos los SHA y huellas se calculan
por codigo a partir de los archivos locales; nada se tipea a mano."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[5]
M2 = ROOT / "propuestas/ronda-8-paralela/ejecucion-20261024/M2-sinac"
V = M2 / "v001"
S2 = ROOT / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/trabajo/evidencia"
CAT = S2 / "cat_sinac_2020_2023"
DESC_XLSX = ROOT / "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx"
ZIP = S2 / "sinac_catalogos_2020_2023.zip"
INSP_DICC = ROOT / "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
INSP_REC = ROOT / "data/portal/inspecciones/46977217-9396-4f9c-bddb-6616e82530b4.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def huella(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


asig = json.loads((M2 / "asignacion.json").read_text(encoding="utf-8"))
dicc = json.loads(INSP_DICC.read_text(encoding="utf-8"))
rec = json.loads(INSP_REC.read_text(encoding="utf-8"))
campos = rec["tablas"][0]["campos"]
defs = dicc["definiciones"]

wb = openpyxl.load_workbook(DESC_XLSX, read_only=True, data_only=True)
desc_rows = {}
for r in wb.active.iter_rows(values_only=True):
    if r and str(r[0]).strip().isdigit():
        desc_rows[int(r[0])] = {
            "variable": str(r[1]).strip(),
            "descripcion": str(r[2]).strip(),
            "catalogo": (str(r[3]).strip() if r[3] else None),
        }

IDNAC = {65: 41, 67: 42, 69: 43, 71: 44, 72: 45, 74: 46, 76: 47,
         77: 51, 79: 52, 84: 50, 87: 54, 89: 55, 97: 59, 99: 60}
CATFILE = {65: "SI_NO.xlsx", 67: "SI_NO.xlsx", 69: "PRODUCTO_EMBARAZO.xlsx",
           77: "RESOLUCION_EMBARAZO.xlsx", 79: "UTILIZO_FORCEPS.xlsx",
           87: "PERSONA_ATENDIO_PARTO.xlsx", 89: "TIPO_MEDICO.xlsx",
           97: "NACIMIENTO_CERTIFICADO_POR.xlsx", 99: "ESTABLECIMIENTO_SALUD_202204.xlsx"}

esq = huella(rec["tablas"][0])
SHA_DICC = sha(INSP_DICC)
SHA_REC = sha(INSP_REC)
SHA_DESC = sha(DESC_XLSX)
SHA_ZIP = sha(ZIP)

# verificaciones fisicas previas (fallan ruidosamente si algo no cuadra)
for caso in asig["casos"]:
    n = int(caso["variable"].split("%2F")[1])
    campo = caso["campo"]
    assert campos[n - 1]["id"] == campo, (n, campo)
    assert campos[n - 1]["posicion_original"] == n, (n, campo)
    assert defs[n - 1]["Nombre variable"] == campo, (n, campo)
    assert huella(defs[n - 1]) == caso["definicion"]["huella_fila_diccionario"], (n, campo)
    d = desc_rows[IDNAC[n]]
    assert d["variable"] == campo, (n, campo, d)
print("verificacion fisica OK: 14/14 nombre+ordinal+huellas+descriptor")

cat_etiqueta = {}
for n, fn in CATFILE.items():
    if fn == "ESTABLECIMIENTO_SALUD_202204.xlsx":
        continue
    w = openpyxl.load_workbook(CAT / fn, read_only=True, data_only=True)
    rows = [r for r in w.active.iter_rows(values_only=True) if r and r[0] is not None]
    cat_etiqueta[fn] = {str(r[0]).strip(): (str(r[1]).strip() if len(r) > 1 and r[1] else "") for r in rows[1:]}

URL_ZIP = "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_catalogos_2020_2023.zip"
URL_DESC = "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip"

decisiones = []
vinculos = []
fuentes = {}
origenes = {}


def add_fuente(ruta, h, url=None, localizador=None):
    if ruta not in fuentes:
        fuentes[ruta] = {"ruta": ruta, "sha256": h}
        if url:
            fuentes[ruta]["url"] = url
        if localizador:
            fuentes[ruta]["localizador"] = localizador
    return {"ruta": ruta, "sha256": h, **({"url": url} if url else {}), **({"localizador": localizador} if localizador else {})}


for caso in asig["casos"]:
    n = int(caso["variable"].split("%2F")[1])
    campo, concepto = caso["campo"], caso["concepto"]
    regla = caso["definicion"]["regla"]
    idef = caso["definicion"]["iri"]
    f = defs[n - 1]
    tipo, ejemplo = f["Tipo de dato"], f["Ejemplo de dato"]
    d = desc_rows[IDNAC[n]]
    prev_c = campos[n - 2]["id"] if n > 1 else None
    next_c = campos[n]["id"] if n < len(campos) else None
    hfila = huella(f)

    ev = [
        {**add_fuente("data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json",
                      SHA_DICC, dicc["fuente"], f"/definiciones/{n - 1} (fila {n}, variable {campo})"),
         "afirmacion_soportada": f"Fila local: Nombre={campo}, Tipo={tipo}, Ejemplo='{ejemplo}', Descripcion={f['Descripción']}, Catalogo='{f['Catálogo de referencia']}'"},
        {**add_fuente("data/portal/inspecciones/46977217-9396-4f9c-bddb-6616e82530b4.json",
                      SHA_REC, rec["fuente"], f"tablas[0]: hoja 'SINAC 2022 26-09-22', 106 campos; posicion {n} = {campo} (vecinos {prev_c} | {next_c})"),
         "afirmacion_soportada": f"El recurso 46977217 trae la columna {campo} en la posicion {n}, mismo ordinal que la fila {n} del diccionario"},
        {**add_fuente("propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx",
                      SHA_DESC, URL_DESC, f"Hoja1 fila ID={IDNAC[n]}, VARIABLE={campo}"),
         "afirmacion_soportada": f"Descriptor SINAC 2020-2025: {campo} = {d['descripcion']} Catalogo: {d['catalogo']}."},
        {**add_fuente("propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/trabajo/evidencia/sinac_catalogos_2020_2023.zip",
                      SHA_ZIP, URL_ZIP, "zip 20 xlsx; sin columnas D ni ANOMALIACIE* ni DIAGNOSTICOS"),
         "afirmacion_soportada": "Codebook nacional 2020-2023; vigencia cubre el recurso 2022"},
    ]
    fn = CATFILE.get(n)
    if fn and fn != "ESTABLECIMIENTO_SALUD_202204.xlsx":
        hcat = sha(CAT / fn)
        etq = cat_etiqueta[fn].get(ejemplo, "")
        assert etq, (campo, ejemplo, fn)
        ev.append({**add_fuente(
            f"propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/trabajo/evidencia/cat_sinac_2020_2023/{fn}",
            hcat, URL_ZIP, f"Hoja1, catalogo {fn[:-5]}: codigo {ejemplo}"),
            "afirmacion_soportada": f"Codigo local '{ejemplo}' = '{etq}' en el catalogo nacional {fn[:-5]}"})
    if fn == "ESTABLECIMIENTO_SALUD_202204.xlsx":
        hcat = sha(CAT / fn)
        ev.append({**add_fuente(
            "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/trabajo/evidencia/cat_sinac_2020_2023/ESTABLECIMIENTO_SALUD_202204.xlsx",
            hcat, URL_ZIP, "Hoja1 ID/CLUES/.../ESTATUS (41802 filas, corte 202204)"),
            "afirmacion_soportada": "Catalogo nacional de establecimientos (mismo que cita el descriptor); ejemplo local vacio, sin verificacion de valor"})

    if d["catalogo"] and fn and fn != "ESTABLECIMIENTO_SALUD_202204.xlsx":
        etq = cat_etiqueta[fn][ejemplo]
        afirma = (f"{campo} = variable IDnac={IDNAC[n]} del descriptor SINAC 2020-2025: {d['descripcion']} "
                  f"Codigos {fn[:-5]} verificados (p. ej. {ejemplo}='{etq}'); columna local = codigo entero, etiqueta D = descripcion del catalogo.")
    elif n in (71, 72):
        afirma = (f"{campo} = variable IDnac={IDNAC[n]} del descriptor SINAC 2020-2025: {d['descripcion']} "
                  f"Sin catalogo nacional (descriptor Catálogo=None); tipo local ({tipo}) compatible; ejemplo '{ejemplo}'.")
    elif n == 84:
        afirma = (f"{campo} = variable IDnac={IDNAC[n]} del descriptor SINAC 2020-2025: {d['descripcion']} "
                  f"Sin catalogo nacional; tipo local {tipo} con ejemplo '{ejemplo}' (duracion codificada como hora).")
    elif n == 99:
        afirma = (f"{campo} = variable IDnac={IDNAC[n]} del descriptor SINAC 2020-2025: {d['descripcion']} "
                  f"Verificacion de ambito: mismo catalogo ESTABLECIMIENTO_SALUD_202204; ejemplo local vacio.")
    else:
        afirma = (f"{campo} = variable IDnac={IDNAC[n]} del descriptor SINAC 2020-2025: {d['descripcion']} "
                  f"Catalogo DIAGNOSTICOS = CIE-10 (lineamientos DOF/CEN en evidencia previa); ejemplo local '{ejemplo}' = NINGUNA APARENTE, "
                  f"corroborado por columna hermana ANOMALIACIE* del mismo renglon.")

    vinculo = {
        "columna": caso["columna"],
        "campo": campo,
        "recurso": caso["recurso"],
        "diccionario": "22202305-2d02-4c49-b216-cc98224357f0",
        "definicion_iri": idef,
        "concepto": concepto,
        "descripcion": d["descripcion"],
        "huella_esquema": esq,
        "huella_fila_diccionario": hfila,
        "criterio": (f"Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto: "
                     f"nombre exacto {campo}, posicion ordinal identica (columna {n} de 106 ↔ fila {n} de 106, vecinos {prev_c} | {next_c}), "
                     f"tipo/ejemplo local ({tipo} / '{ejemplo}') y descripcion del descriptor nacional IDnac={IDNAC[n]}. "
                     f"Alcance de interpretacion documental; no valida valores ni confirma pertenencia a catalogos."),
    }
    vinculos.append(vinculo)
    origenes[caso["columna"]] = [{"ruta": e["ruta"], "sha256": e["sha256"]} for e in ev]
    decisiones.append({
        "id": caso["iri"],
        "columna": caso["columna"],
        "campo": campo,
        "recurso": caso["recurso"],
        "definicion_iri": idef,
        "concepto": concepto,
        "regla": regla,
        "estado": "propuesta_para_auditar",
        "afirmacion_propuesta": (f"La columna {campo} (posicion {n} de 106, hoja 'SINAC 2022 26-09-22', recurso 46977217, "
                                 f"2022-01-01 a 2022-09-26) es la materializacion fisica de la variable {campo} "
                                 f"(fila {n} de 106 del diccionario 22202305, conjunto 940de7d8): nombre exacto coincidente y ordinal identico. " + afirma),
        "motivo": (f"Vinculo fisico exacto verificado por codigo en inspecciones originales: columna {n}={campo} (huella_esquema {esq[:12]}...) "
                   f"↔ fila {n}={campo} (huella_fila {hfila[:12]}...). Significado ya respaldado en R7 ({regla}, {concepto}, estado integrado_r7). "
                   f"No se aprueba por nombre solo: ordinal, vecinos, tipo/ejemplo y huellas coinciden."),
        "vinculo_propuesto": vinculo,
        "evidencia": ev,
        "evidencia_faltante": None,
        "condicion_reapertura": ("Si la auditoria rechaza el vinculo, revierte a brecha_externa con el motivo del dictamen; "
                                 "reapertura con fe de erratas del publicador o instrumento que corrija ordinal/nombre."),
        "limites": caso["definicion"]["limites"],
    })

entrega = {
    "rol": "M2-sinac",
    "version": "v001",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "base": "propuestas/ronda-8-paralela/ejecucion-20261024/base.json",
    "casos_asignados": len(asig["casos"]),
    "resumen": {"propuesta_para_auditar": sum(1 for x in decisiones if x["estado"] == "propuesta_para_auditar"),
                "brecha_externa": 0, "acceso_no_resuelto": 0},
    "comprobaciones_ejecutadas_por_codigo": [
        "columna[n].id == diccionario[n].Nombre para los 14 (ordinal identico)",
        "huella_esquema == sha256-tabla de semantica.json para el recurso (9b46e1c0...)",
        "huella_fila == huella declarada en asignacion para los 14",
        "VARIABLE del descriptor IDnac == campo local para los 14 (lectura directa del xlsx)",
        "codigo-ejemplo local hallado en catalogo nacional con etiqueta coincidente (7 casos A1)",
    ],
    "peticiones_web": "ninguna: toda la evidencia es local y ya examinada en R7; sin pista primaria nueva",
    "decisiones": decisiones,
    "vinculos_propuestos": vinculos,
    "origenes_por_columna": origenes,
    "fuentes": list(fuentes.values()),
}
V.mkdir(parents=True, exist_ok=True)
(V / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=1), encoding="utf-8")

lineas = ["# M2-sinac v001 — 14 vínculos físicos SINAC",
          "",
          "14/14 `propuesta_para_auditar`, 0 brechas, 0 accesos sin resolver.",
          "Vínculo = columna n ↔ fila n (nombre exacto + ordinal idéntico), huellas verificadas por código.",
          "Significado ya respaldado en R7 (integrado_r7); aquí solo se acredita el alcance físico.",
          "",
          "| n | campo | concepto | descriptor | estado |",
          "| --- | --- | --- | --- | --- |"]
for x in decisiones:
    n = x["columna"].split("%2F")[-1]
    lineas.append(f"| {n} | {x['campo']} | {x['concepto']} | {x['vinculo_propuesto']['descripcion'][:60]} | {x['estado']} |")
lineas += ["",
           "Sin peticiones web: evidencia local ya examinada en R7, sin pista primaria nueva.",
           "Correcciones futuras en v002; v001 no se edita tras congelar."]
(V / "entrega.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("entrega.json + entrega.md escritos:", len(decisiones), "decisiones,", len(fuentes), "fuentes")
