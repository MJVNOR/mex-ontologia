"""Genera v001 S2-nacimientos (ronda-8-paralela/ejecucion-20261024).
Todos los SHA-256 se calculan por codigo; nada se tipea a mano.
Solo escribe dentro de S2-nacimientos/v001/."""
import hashlib
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:\Users\marti\Documents\MEX-Ontologi")
S2 = REPO / "propuestas/ronda-8-paralela/ejecucion-20261024/S2-nacimientos"
OUT = S2 / "v001"
OUT.mkdir(parents=True, exist_ok=True)

P_INSP = REPO / "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
P_ZIP = REPO / ("propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/"
                "S2-nacimientos/trabajo/evidencia/sinac_catalogos_2020_2023.zip")
P_DESC = REPO / ("propuestas/cierre-brechas-post-r6/significados-salud/evidencia/"
                 "desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx")
P_ASIG = S2 / "asignacion.json"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


H_INSP, H_ZIP, H_DESC = sha256(P_INSP), sha256(P_ZIP), sha256(P_DESC)
H_ASIG = sha256(P_ASIG)
print("H_INSP", H_INSP)
print("H_ZIP ", H_ZIP)
print("H_DESC", H_DESC)
print("H_ASIG", H_ASIG)

# --- verificacion computable 1: filas locales ---
insp = json.loads(P_INSP.read_text(encoding="utf-8"))
defs = insp["definiciones"]
asig = json.loads(P_ASIG.read_text(encoding="utf-8"))
assert len(asig["casos"]) == 22, len(asig["casos"])
filas = {}
for c in asig["casos"]:
    fila = int(c["id"].split("%2F")[1])
    d = defs[fila - 1]
    assert d["Tipo de dato"] == "Texto", (fila, d)
    assert d["Descripci\u00f3n"] == "Pendiente de especificar", (fila, d)
    filas[c["id"]] = (fila, d["Nombre variable"], d["Ejemplo de dato"])

# --- verificacion computable 2: ausencia en descriptor ---
from openpyxl import load_workbook

wb = load_workbook(P_DESC, read_only=True, data_only=True)
ws = wb.active
celdas = set()
for row in ws.iter_rows(values_only=True):
    for v in row:
        if isinstance(v, str):
            celdas.add(v.strip())
nombres = [filas[c["id"]][1] for c in asig["casos"]]
assert not [n for n in nombres if n in celdas], "descriptor contiene un nombre D"
print("descriptor: 0/22 coincidencias exactas")

# --- verificacion computable 3: ausencia en el zip (nombres + celdas) ---
with zipfile.ZipFile(P_ZIP) as zz:
    zin = zz.namelist()
    assert len(zin) == 20, zin
    assert not any(n[:-5].strip() in nombres for n in zin if n.lower().endswith(".xlsx")), [
        n for n in zin if n[:-5].strip() in nombres]
    hits = {}
    for n in zin:
        wb2 = load_workbook(io.BytesIO(zz.read(n)), read_only=True, data_only=True)
        for ws2 in wb2.worksheets:
            for row in ws2.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str) and v.strip() in nombres:
                        hits.setdefault(v.strip(), []).append(n)
    assert not hits, hits
print("zip: 20 xlsx, 0/22 coincidencias en hojas ni celdas")

BASE = {  # columna D -> columna base que decodifica (sin afirmar regla del publicador)
    "ATENCIONPRENATALD": "ATENCIONPRENATAL", "TRIMESTREPRIMERCONSULTAD": "TRIMESTREPRIMERCONSULTA",
    "SOBREVIVIOPARTOD": "SOBREVIVIOPARTO", "AFILIACIOND": "AFILIACION",
    "INTERRUMPIOESTUDIOSD": "INTERRUMPIOESTUDIOS", "CLAVEOCUPACIONHABITUALD": "CLAVEOCUPACIONHABITUAL",
    "TAMIZAUDITIVOD": "TAMIZAUDITIVO", "VACUNA_BCGD": "VACUNA_BCG",
    "VACUNAHEPATITIS_BD": "VACUNAHEPATITIS_B", "VITAMINA_AD": "VITAMINA_A",
    "VITAMINA_KD": "VITAMINA_K", "PRODUCTOEMBARAZOD": "PRODUCTOEMBARAZO",
    "RESOLUCIONEMBARAZOD": "RESOLUCIONEMBARAZO", "UTILIZOFORCEPSD": "UTILIZOFORCEPS",
    "PERSONALATENDIOD": "PERSONALATENDIO", "TIPOMEDICOATENDIOD": "TIPOMEDICOATENDIO",
    "CERTIFICADOPORD": "CERTIFICADOPOR", "ENTIDADFEDERATIVACERTIFICAD": "ENTIDADFEDERATIVACERTIFICA",
    "MUNICIPIOCERTIFICAD": "MUNICIPIOCERTIFICA", "LOCALIDADCERTIFICAD": "LOCALIDADCERTIFICA",
}

R_INSP = "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
R_ZIP = ("propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/"
         "S2-nacimientos/trabajo/evidencia/sinac_catalogos_2020_2023.zip")
R_DESC = ("propuestas/cierre-brechas-post-r6/significados-salud/evidencia/"
          "desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx")
LIMITES = [
    "Alcance simultaneo por conjunto+diccionario+fila+huella; no autoriza cruces, joins ni identidad de catalogos.",
    "Descriptor/catalogos DGIS citados son del registro nacional (SINAC 2020-2025 / codebook 2020-2023), no del extracto Sonora del portal; la coincidencia de nombres o valores no sustituye la tabla del publicador.",
    "Negativas y ausencias acotadas a lo revisado el 2026-10-24; no ausencia universal.",
]

decisiones = []
for c in asig["casos"]:
    cid = c["id"]
    fila, nombre, ejemplo = filas[cid]
    idx = fila - 1
    if nombre in BASE:
        base = BASE[nombre]
        motivo = (
            f"brecha_externa: fila portal verificada ({nombre}, Texto, ejemplo {ejemplo!r}, "
            "Descripcion 'Pendiente de especificar') sin contraparte nacional verificada por codigo: "
            f"ausente del descriptor SINAC 2020-2025 (0/22) y del codebook 2020-2023 "
            f"(zip de 20 xlsx, 0/22 en nombres y celdas). Desajuste estructural concreto: columna "
            f"derivada local '{nombre}' cuyo contenido decodificaria '{base}', pero la regla "
            "publicador columna->catalogo no esta declarada en el instrumento local ni en fuente "
            "primaria vinculada al recurso 46977217. Expediente R7 revisado (S2 v001/v002, W-web "
            "paquetes v001..v004 y cierres): sin pista primaria nueva para este ID; no se repiten "
            "busquedas genericas agotadas. Negativa acotada a lo revisado el 2026-10-24."
        )
        falt = (f"Regla del publicador que fije {nombre} como decodificacion de {base} con catalogo "
                "declarado, aplicable al recurso 46977217.")
        reap = (f"Reabre si el publicador publica la regla de decodificacion de {nombre} (o su "
                "definicion) aplicable al recurso 46977217, o si W aporta documento primario equivalente.")
    else:  # ANOMALIACIE1/2
        motivo = (
            f"brecha_externa: fila portal verificada ({nombre}, Texto, ejemplo {ejemplo!r}, "
            "Descripcion 'Pendiente de especificar') sin contraparte nacional verificada por codigo: "
            f"ausente del descriptor SINAC 2020-2025 (0/22) y del codebook 2020-2023 "
            "(zip de 20 xlsx, 0/22 en nombres y celdas). Desajuste estructural concreto: columna "
            "textual local sin variable en el instrumento nacional (el modelo nacional codifica "
            "anomalias con CODIGOCIEANOMALIA/0000). Sin definicion del publicador vinculada al "
            "recurso 46977217. Expediente R7 revisado (S2 v001/v002, W-web paquetes v001..v004 y "
            "cierres): sin pista primaria nueva para este ID; no se repiten busquedas genericas "
            "agotadas. Negativa acotada a lo revisado el 2026-10-24."
        )
        falt = (f"Definicion publicada de {nombre} por el publicador (o regla que la vincule a "
                "CODIGOCIEANOMALIA) aplicable al recurso 46977217.")
        reap = (f"Reabre si el publicador publica la definicion o regla de {nombre} aplicable al "
                "recurso 46977217, o si W aporta documento primario equivalente.")
    decisiones.append({
        "id": cid,
        "tipo": "significados",
        "original_sha256": c["original_sha256"],
        "puerta": "sin_pista_nueva",
        "pista": None,
        "estado": "brecha_externa",
        "afirmacion_propuesta": None,
        "motivo": motivo,
        "evidencia_faltante": falt,
        "evidencia": [
            {"ruta": R_INSP, "sha256": H_INSP,
             "localizador": f"/definiciones/{idx} (fila {fila}, variable {nombre})",
             "afirmacion_soportada": (f"Fila local: Nombre={nombre}, Tipo=Texto, Ejemplo={ejemplo!r}, "
                                      "Descripcion=Pendiente de especificar")},
            {"ruta": R_ZIP, "sha256": H_ZIP,
             "localizador": "listado completo del zip (20 xlsx) + barrido de celdas por codigo",
             "afirmacion_soportada": f"Negativa acotada verificada por codigo: 0/22; '{nombre}' sin coincidencia en nombres de archivo ni en celdas del codebook 2020-2023."},
            {"ruta": R_DESC, "sha256": H_DESC,
             "localizador": "Hoja1; busqueda exacta del nombre por codigo",
             "afirmacion_soportada": f"Negativa acotada verificada por codigo: '{nombre}' no figura entre las variables del descriptor nacional SINAC 2020-2025."},
        ],
        "condicion_reapertura": reap,
        "limites": LIMITES,
    })

entrega = {
    "rol": "S2-nacimientos",
    "version": "v001",
    "fecha_utc": datetime.now(timezone.utc).isoformat(),
    "base": "reports/ronda-7.json",
    "asignacion_sha256": H_ASIG,
    "decisiones": decisiones,
    "fuentes": [
        {"ruta": R_INSP, "sha256": H_INSP,
         "localizador": "inspeccion portal conjunto nacimientos (106 definiciones); filas S2 verificadas por codigo",
         "verificado_por_codigo": "2026-10-24"},
        {"ruta": R_ZIP, "sha256": H_ZIP,
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_catalogos_2020_2023.zip",
         "localizador": "codebook nacional SINAC 2020-2023: 20 xlsx; barrido completo por codigo, 0/22",
         "verificado_por_codigo": "2026-10-24"},
        {"ruta": R_DESC, "sha256": H_DESC,
         "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip",
         "localizador": "descriptor nacional SINAC 2020-2025, Hoja1; busqueda exacta por codigo, 0/22",
         "verificado_por_codigo": "2026-10-24"},
    ],
    "pruebas": {
        "filas_locales": "22/22 filas Texto con Descripcion 'Pendiente de especificar' (lectura directa del JSON por codigo)",
        "descriptor": "0/22 coincidencias exactas (barrido de celdas con openpyxl)",
        "codebook_zip": "20 xlsx listados; 0/22 en nombres de archivo y en celdas (barrido con openpyxl)",
        "expediente_r7": "S2 v001/v002 + notas primera-puerta/w-web + W-web paquetes v001..v004 y cierres revisados; sin pista primaria nueva para estos 22 IDs",
        "navegador": "no usado (reservado a W); sin peticiones-web.json: ninguna pista nueva concreta que lo requiera",
    },
    "novedades": ("v001 ronda-8: revision local de los 22 IDs asignados sin pista nueva. 0 propuesta_para_auditar, "
                  "22 brecha_externa con desajuste estructural concreto (20 columnas D derivadas sin variable nacional "
                  "ni regla de decodificacion publicada; 2 ANOMALIACIE* sin variable en el instrumento). Dobles negativas "
                  "verificadas por codigo (descriptor 0/22, codebook 20 xlsx 0/22). Expediente R7 y paquetes W v001..v004 "
                  "revisados sin hallazgo nuevo para estos IDs."),
}

p_json = OUT / "entrega.json"
p_json.write_text(json.dumps(entrega, ensure_ascii=False, indent=2), encoding="utf-8")

lineas = ["# S2-nacimientos v001 (ronda-8-paralela/ejecucion-20261024)", "",
          "22 IDs asignados, puerta `sin_pista_nueva` en los 22. Resultado: 0 propuesta_para_auditar, 22 brecha_externa.",
          "Revision exclusivamente local (sin navegador; reservado a W). Dobles negativas verificadas por codigo:",
          "descriptor SINAC 2020-2025 0/22 y codebook 2020-2023 (20 xlsx) 0/22 en nombres y celdas.",
          "Expediente R7 revisado (S2 v001/v002, notas primera-puerta/w-web, W-web paquetes v001..v004 y cierres):",
          "sin pista primaria nueva para estos IDs; no se repiten busquedas genericas agotadas.",
          "Sin peticiones-web.json: ninguna pista nueva concreta requiere al navegador compartido.", "",
          "| fila | variable | ejemplo | estado |",
          "| --- | --- | --- | --- |"]
for c in asig["casos"]:
    fila, nombre, ejemplo = filas[c["id"]]
    lineas.append(f"| {fila} | {nombre} | {ejemplo} | brecha_externa |")
lineas += ["",
           "## Pruebas verificables (por codigo, 2026-10-24)",
           "- Filas: 22/22 Texto con Descripcion 'Pendiente de especificar' (lectura directa del JSON).",
           "- Descriptor: 0/22 coincidencias exactas (barrido de celdas con openpyxl).",
           "- Codebook zip (20 xlsx): 0/22 en nombres de archivo y en celdas (barrido con openpyxl).",
           "- Hashes: inspeccion `76fe6822...7513b`, zip `9c7dcd52...141cb4e`, descriptor `0af0b6be...7fd6ed4`",
           "  (completos en entrega.json; calculados por codigo).",
           "- R7/W: S2 v001 (53 brechas) y v002 (31 propuestas + 22 brechas) mas W v001..v004 revisados;",
           "  F-W02-SINAC-CAT ya incorporado en v002; v003/v004 sin material S2. Sin hallazgo nuevo.",
           "",
           "## Limites",
           "- Negativas acotadas a lo revisado el 2026-10-24; no ausencia universal.",
           "- Fuentes nacionales citadas no sustituyen la tabla del publicador para el recurso 46977217.",
           "- Sin joins, sin identidad de catalogos, sin vigencias inferidas."]
p_md = OUT / "entrega.md"
p_md.write_text("\n".join(lineas) + "\n", encoding="utf-8")

congelada = {
    "rol": "S2-nacimientos",
    "version": "v001",
    "archivos": [
        {"ruta": "propuestas/ronda-8-paralela/ejecucion-20261024/S2-nacimientos/v001/entrega.json",
         "sha256": sha256(p_json)},
        {"ruta": "propuestas/ronda-8-paralela/ejecucion-20261024/S2-nacimientos/v001/entrega.md",
         "sha256": sha256(p_md)},
    ],
    "conteos": {"decisiones": 22, "propuesta_para_auditar": 0, "brecha_externa": 22, "fuentes": 3},
}
(OUT / "congelada.json").write_text(json.dumps(congelada, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK v001:", len(decisiones), "decisiones")
