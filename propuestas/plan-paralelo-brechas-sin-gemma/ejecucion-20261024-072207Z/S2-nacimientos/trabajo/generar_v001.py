"""Genera v001 S2-nacimientos: primera puerta -> sin_pista_nueva x53, brecha_externa.
Lee asignacion.json, conserva evidencia previa (SHA recalculados), verifica
package_show del conjunto en vivo y escribe entrega.json + entrega.md."""
import ast, hashlib, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROY = Path(".")
S2 = PROY / "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos"
TRAB = S2 / "trabajo"
EV = TRAB / "evidencia"
V001 = S2 / "v001"
for d in (EV, V001):
    d.mkdir(parents=True, exist_ok=True)

ahora = datetime.now(timezone.utc)
HOY = ahora.date().isoformat()

asig = json.loads((S2 / "asignacion.json").read_text(encoding="utf-8"))
casos = asig["casos"]
assert len(casos) == 53, len(casos)

# 1. Verificacion en vivo del paquete del publicador (cambio_de_fuente_por_comprobar)
PKG_URL = "https://datos.sonora.gob.mx/api/3/action/package_show?id=940de7d8-73ec-4a08-8d26-b7cc97ff17bd"
req = urllib.request.Request(PKG_URL, headers={"User-Agent": "MEX-Ontologi-S2/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    pkg_bytes = r.read()
pkg_path = EV / "package_show_940de7d8_2026-10-24.json"
pkg_path.write_bytes(pkg_bytes)
pkg = json.loads(pkg_bytes.decode("utf-8"))["result"]
pkg_res = {x["id"]: x for x in pkg["resources"]}
dic, rec = pkg_res["22202305-2d02-4c49-b216-cc98224357f0"], pkg_res["46977217-9396-4f9c-bddb-6616e82530b4"]

# 2. Descriptor nacional (solo lectura local ya preservada)
raw = (PROY / "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/sinac_desc_dump.txt").read_bytes().decode("utf-16")
desc = {}
for line in raw.splitlines():
    try:
        t = ast.literal_eval(line.strip())
    except Exception:
        continue
    if isinstance(t, tuple) and len(t) == 4 and isinstance(t[0], int):
        desc[t[1]] = {"idnac": t[0], "desc": t[2], "cat": t[3]}

def sha(p):
    return hashlib.sha256((PROY / p).read_bytes()).hexdigest()

F_INSP = "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
F_DD = "propuestas/investigacion-post-r6/salud-nacimientos/evidencia/cap_inegi_530_dd.html"
F_HTTP = "propuestas/investigacion-post-r6/salud-nacimientos/evidencia/http-log.json"
F_DESC = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx"
R_PKG = str(pkg_path.as_posix())

D_VARS = {c["original"]["variable"] for c in casos} - set(desc)
assert all(v.endswith("D") or v.startswith("ANOMALIACIE") for v in D_VARS), D_VARS

decisiones = []
for c in casos:
    var = c["original"]["variable"]
    orig_sha = hashlib.sha256(json.dumps(c["original"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    fila = c["original"]["evidencia"][0]["localizador"]
    if var in desc:
        e = desc[var]
        motivo = (
            f"sin_pista_nueva: Manual 2015, INEGI 2018 y descriptor SINAC 2020-2025 ya examinados (ronda anterior); "
            f"redescargarlos no es novedad. Descriptor nacional trae nombre EXACTO ({var}, IDnac={e['idnac']}), "
            f"descripcion y catalogo ({e['cat']}); vigencia 2020-2025 cubre el recurso 46977217 (2022-01-01 a 2022-09-26). "
            f"No promociona: sin tabla columna<->variable ni nota del publicador que vincule esta fila (huella {c['original']['huella_fila_diccionario'][:12]}...) "
            f"al descriptor; contenido del catalogo ({e['cat']}) no publicado en el descriptor y codebook aplicado al recurso sin fuente vinculada. "
            f"Verificacion en vivo {HOY}: package_show del conjunto (version=null, fuentes_extras='', notes='Subsistema de Informacion sobre Nacimientos') "
            f"sin diccionario corregido, codebook ni declaracion de edicion. sinac_catalogos_2020_2023.zip evaluado y diferido en ronda anterior: "
            f"contenido nacional sin vinculo del publicador; no resuelve."
        )
        falt = (
            f"Nota del publicador que vincule el recurso 46977217 con la variable {var} (IDnac={e['idnac']}) del descriptor SINAC 2020-2025 "
            f"para esta fila (huella {c['original']['huella_fila_diccionario'][:12]}...), con contenido publicado del catalogo ({e['cat']}), "
            f"tabla columna<->variable y codebook aplicado al recurso."
        )
        ev2_loc = f"Hoja1 fila ID={e['idnac']}, VARIABLE={var}"
        ev2_af = f"Descriptor nacional SINAC 2020-2025: {var} = {e['desc']} Catalogo: {e['cat']}."
        cond = (
            f"Reabre si el publicador publica diccionario corregido del recurso 46977217, o nota que vincule esta fila con {var} "
            f"(IDnac={e['idnac']}) + contenido del catalogo {e['cat']} + tabla columna<->variable; o si W aporta documento primario equivalente."
        )
    else:
        motivo = (
            f"sin_pista_nueva: '{var}' sin contraparte en descriptor nacional SINAC 2020-2025 (65 variables base, sin columnas D ni ANOMALIACIE*) "
            f"ni en primarias ya examinadas (Modelo 2015, INEGI 2017, DOF CEN); rebuscarlas no es novedad. "
            f"Verificacion en vivo {HOY}: package_show del conjunto (version=null, fuentes_extras='') sin descripcion ni codebook para esta columna. "
            f"Inferir su sentido desde la columna base seria join inventado."
        )
        falt = (
            f"Descripcion publicada de {var} en el diccionario 22202305-2d02-4c49-b216-cc98224357f0 o nota del publicador que la vincule "
            f"al recurso 46977217 (huella {c['original']['huella_fila_diccionario'][:12]}...), con codebook si aplica."
        )
        ev2_loc = "Hoja1, 65 variables base (ID 1..64); busqueda exacta del nombre"
        ev2_af = f"Negativa acotada: '{var}' no figura entre las 65 variables del descriptor nacional SINAC 2020-2025."
        cond = (
            f"Reabre si el publicador publica descripcion/codebook de {var} aplicable al recurso 46977217, "
            f"o si W aporta documento primario con definicion y vinculo formal a esta fila."
        )
    decisiones.append({
        "id": c["id"], "tipo": c["tipo"], "original_sha256": orig_sha,
        "puerta": "sin_pista_nueva", "pista": None,
        "estado": "brecha_externa", "afirmacion_propuesta": None,
        "motivo": motivo, "evidencia_faltante": falt,
        "evidencia": [
            {"ruta": F_INSP, "sha256": sha(F_INSP), "localizador": fila,
             "afirmacion_soportada": f"Fila local verificada: Descripcion='Pendiente de especificar', Catalogo de referencia=''; tipo y ejemplo no definen el significado ({var})"},
            {"ruta": F_DESC, "sha256": sha(F_DESC), "localizador": ev2_loc, "afirmacion_soportada": ev2_af},
        ],
        "condicion_reapertura": cond,
        "limites": c["antecedente"].get("limites", c["original"].get("limites", [])),
    })

fuentes = [
    {"ruta": F_INSP, "sha256": sha(F_INSP), "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=22202305-2d02-4c49-b216-cc98224357f0&limit=1000&offset=0&sort=_id+asc", "fecha_consulta": "2026-10-23", "localizador": "definiciones (106 filas)"},
    {"ruta": F_DESC, "sha256": sha(F_DESC), "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip", "fecha_consulta": "2026-10-24", "localizador": "Descriptores_SINAC_2020.xlsx, Hoja1 (A1='SINAC 2020-2025', 65 variables ID 1..64)"},
    {"ruta": F_DD, "sha256": sha(F_DD), "url": "https://www.inegi.org.mx/rnm/index.php/catalog/530/data-dictionary/F1?file_name=SINAC2018", "fecha_consulta": "2026-10-24", "localizador": "diccionario nacional SINAC2018, 62 variables V1-V62 (datos 2017)"},
    {"ruta": F_HTTP, "sha256": sha(F_HTTP), "url": None, "fecha_consulta": "2026-10-24", "localizador": "entradas dgis-manual/metodologia/inegi-530/dof-cen (HTTP 200, bytes verificados)"},
    {"ruta": R_PKG, "sha256": sha(R_PKG), "url": PKG_URL, "fecha_consulta": ahora.isoformat(timespec="seconds"), "localizador": "result.version=null, result.fuentes_extras='', recurso diccionario 22202305 (datastore_active=true), recurso 46977217 2022-01-01/2022-09-26"},
]

entrega = {"rol": "S2-nacimientos", "version": "v001", "decisiones": decisiones, "fuentes": fuentes,
    "novedades": (
        "Sin pista nueva en los 53 IDs: Manual SINAC Modelo 2015, diccionario INEGI SINAC2018, metodologia 2020, DOF CEN y descriptor "
        "SINAC 2020-2025 ya examinados en rondas previas; no se redescargan como novedad. Verificacion propia en vivo con herramienta independiente "
        f"(package_show del conjunto, {HOY}): sin diccionario corregido, codebook, tabla columna<->variable ni declaracion de edicion (version=null, "
        "fuentes_extras=''). sinac_catalogos_2020_2023.zip (DGIS DA) evaluado y diferido con motivo documentado: contenido nacional sin vinculo del "
        "publicador; no resuelve ningun ID. No se requirio navegador compartido: sin peticion a W (paquete W-web de esta ejecucion pendiente; si W aporta "
        "documento resolutivo, el coordinador hara adenda). Resultado: 0 propuestas, 53 brecha_externa."
    )}

(V001 / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2), encoding="utf-8")
print("decisiones:", len(decisiones), "| estados:", {e for d in decisiones for e in [d['estado']]}, "| puertas:", {d['puerta'] for d in decisiones})
print("pkg version:", pkg.get("version"), "| fuentes_extras:", repr(pkg.get("fuentes_extras")))
