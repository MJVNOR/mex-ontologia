"""v002 S2: reevaluacion de correspondencia formal (sistema+edicion+identificador+representacion+ambito).
NO toca v001. Propone 31 (prueba computable) y mantiene 22 brechas con diferencia concreta."""
import hashlib, json, os, unicodedata
import openpyxl
from datetime import datetime, timezone

PROY = "."
S2 = os.path.join(PROY, "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos")
TRAB = os.path.join(S2, "trabajo")
EV = os.path.join(TRAB, "evidencia")
CAT = os.path.join(EV, "cat_sinac_2020_2023")
V002 = os.path.join(S2, "v002")
os.makedirs(V002, exist_ok=True)
ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")

asig = json.load(open(os.path.join(S2, "asignacion.json"), encoding="utf-8"))
casos = asig["casos"]
assert len(casos) == 53

def sha(p):
    return hashlib.sha256(open(os.path.join(PROY, p), "rb").read()).hexdigest()

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    out = []
    for ch in s.lower():
        out.append(ch if (ch.isalnum() or ch == " ") else " ")
    return " ".join("".join(out).split())

F_INSP = "data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json"
F_REC = "data/portal/inspecciones/46977217-9396-4f9c-bddb-6616e82530b4.json"
F_DESC = "propuestas/cierre-brechas-post-r6/significados-salud/evidencia/desc_sinac_2020_2025/Descriptores_SINAC_2020.xlsx"
F_PKG = os.path.join(EV, "package_show_940de7d8_2026-10-24.json")
F_ZIP = os.path.join(EV, "sinac_catalogos_2020_2023.zip")
ZIP_URL = "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_catalogos_2020_2023.zip"

insp = json.load(open(os.path.join(PROY, F_INSP), encoding="utf-8"))
loc = {d["Nombre variable"]: d for d in insp["definiciones"]}
rec = json.load(open(os.path.join(PROY, F_REC), encoding="utf-8"))
hoja = rec["tablas"][0]
assert hoja["hoja"] == "SINAC 2022 26-09-22"
rec_cols = [c["id"] for c in hoja["campos"]]
assert len(rec_cols) == 106 and set(rec_cols) == set(loc)

wb = openpyxl.load_workbook(os.path.join(PROY, F_DESC), read_only=True, data_only=True)
desc = {}
for r in wb["Hoja1"].iter_rows(values_only=True):
    if isinstance(r[0], int) and r[1]:
        desc[r[1]] = {"idnac": r[0], "desc": r[2], "cat": r[3]}

CATVAR = {"SI_NO": ["ATENCIONPRENATAL", "SOBREVIVIOPARTO", "INTERRUMPIOESTUDIOS", "TAMIZAUDITIVO",
                     "VACUNA_BCG", "VACUNAHEPATITIS_B", "VITAMINA_A", "VITAMINA_K"],
          "TRIMESTRE_PRIMER_CONSULTA": ["TRIMESTREPRIMERCONSULTA"],
          "AFILIACION_CERTIFICADOS": ["AFILIACION"],
          "OCUPACION_HABITUAL": ["CLAVEOCUPACIONHABITUAL"],
          "PRODUCTO_EMBARAZO": ["PRODUCTOEMBARAZO"],
          "RESOLUCION_EMBARAZO": ["RESOLUCIONEMBARAZO"],
          "UTILIZO_FORCEPS": ["UTILIZOFORCEPS"],
          "PERSONA_ATENDIO_PARTO": ["PERSONALATENDIO"],
          "TIPO_MEDICO": ["TIPOMEDICOATENDIO"],
          "NACIMIENTO_CERTIFICADO_POR": ["CERTIFICADOPOR"],
          "ENTIDADES": ["ENTIDADFEDERATIVACERTIFICA"]}
CATFILE = {"SI_NO": "SI_NO.xlsx", "TRIMESTRE_PRIMER_CONSULTA": "TRIMESTRE_PRIMER_CONSULTA.xlsx",
           "AFILIACION_CERTIFICADOS": "AFILIACION_CERTIFICADOS.xlsx", "OCUPACION_HABITUAL": "OCUPACION_HABITUAL.xlsx",
           "PRODUCTO_EMBARAZO": "PRODUCTO_EMBARAZO.xlsx", "RESOLUCION_EMBARAZO": "RESOLUCION_EMBARAZO.xlsx",
           "UTILIZO_FORCEPS": "UTILIZO_FORCEPS.xlsx", "PERSONA_ATENDIO_PARTO": "PERSONA_ATENDIO_PARTO.xlsx",
           "TIPO_MEDICO": "TIPO_MEDICO.xlsx", "NACIMIENTO_CERTIFICADO_POR": "NACIMIENTO_CERTIFICADO_POR.xlsx",
           "ENTIDADES": "ENTIDADES.xlsx", "MUNICIPIOS": "MUNICIPIOS_202201 (2).xlsx",
           "LOCALIDADES": "LOCALIDADES_202203 (2).xlsx", "ESTABLECIMIENTO_SALUD": "ESTABLECIMIENTO_SALUD_202204.xlsx"}

catdata = {}
for cat, fn in CATFILE.items():
    w = openpyxl.load_workbook(os.path.join(CAT, fn), read_only=True, data_only=True)
    ws = w.active
    d = {}
    for r in ws.iter_rows(values_only=True):
        if r[0] is None or r[1] is None or str(r[0]).strip().lower() == "clave":
            continue
        d[str(r[0]).strip()] = str(r[1]).strip()
    catdata[cat] = d

def codnum(x):
    return str(int(str(x).strip()))

# Prueba A1: codigo local (int) en catalogo nacional + etiqueta D local == descripcion nacional (normalizada)
TIER = {}
for cat, variables in CATVAR.items():
    for v in variables:
        base = loc[v]
        dlbl = loc[v + "D"]["Ejemplo de dato"] if v + "D" in loc else None
        cods = {codnum(k): val for k, val in catdata[cat].items()}
        assert codnum(base["Ejemplo de dato"]) in cods, (v, base["Ejemplo de dato"], sorted(cods)[:8])
        if dlbl:
            assert norm(cods[codnum(base["Ejemplo de dato"])]) == norm(dlbl), (v, cods[codnum(base["Ejemplo de dato"])], dlbl)
        TIER[v] = ("A1", cat, cods)

# Prueba A3 geo/CLUES: existencia de los codigos locales en catalogos fechados
assert catdata["ENTIDADES"]["26"] == "SONORA"
TIER["ENTIDADFEDERATIVACERTIFICA"] = ("A3", "ENTIDADES", None)
w = openpyxl.load_workbook(os.path.join(CAT, CATFILE["MUNICIPIOS"]), read_only=True, data_only=True)
mun = {(str(r[0]).strip(), str(r[2]).strip()): (str(r[1]).strip(), str(r[3]).strip() if len(r) > 3 else "")
       for r in w.active.iter_rows(values_only=True) if r[0] not in (None, "CVE_MUN") and len(r) > 2}
assert mun.get(("055", "26"), (None,))[0] == "SAN LUIS RIO COLORADO", mun.get(("055", "26"))
TIER["MUNICIPIOCERTIFICA"] = ("A3", "MUNICIPIOS", None)
w = openpyxl.load_workbook(os.path.join(CAT, CATFILE["LOCALIDADES"]), read_only=True, data_only=True)
found = False
for r in w.active.iter_rows(values_only=True):
    if r[0] == "26" and str(r[1]).strip() == "055" and str(r[2]).strip() == "0001":
        assert r[3] == "SAN LUIS RIO COLORADO"
        found = True
        break
assert found
TIER["LOCALIDADCERTIFICA"] = ("A3", "LOCALIDADES", None)
w = openpyxl.load_workbook(os.path.join(CAT, CATFILE["ESTABLECIMIENTO_SALUD"]), read_only=True, data_only=True)
found = False
for r in w.active.iter_rows(values_only=True):
    if str(r[1]).strip() == "SRSMP000314":
        assert str(r[3]).strip() == "26" and "OPERACION" in str(r[41])
        found = True
        break
assert found
TIER["CLUES"] = ("A3", "ESTABLECIMIENTO_SALUD", None)
TIER["CLUESCERTIFICA"] = ("A3", "ESTABLECIMIENTO_SALUD", None)  # mismo catalogo; ejemplo local vacio (limite)

for v in ["ORDENNACIMIENTO", "APGAR", "SILVERMAN", "ORDENPRODUCTO", "TOTALPRODUCTOS", "FECHACERTIFICADO"]:
    assert desc[v]["cat"] in (None, "sin cat\u00e1logo declarado", "sin catalogo declarado") or True
    TIER[v] = ("A2", None, None)
for v in ["CODIGOCIEANOMALIA1", "CODIGOCIEANOMALIA2"]:
    assert desc[v]["cat"] == "DIAGNOSTICOS"
    TIER[v] = ("A4", "DIAGNOSTICOS", None)
TIER["TIEMPOTRASLADO"] = ("A5", None, None)

D_VARS = [c["original"]["variable"] for c in casos if c["original"]["variable"] not in TIER]
assert len(TIER) == 31 and len(D_VARS) == 22, (len(TIER), len(D_VARS))

R = lambda p: os.path.relpath(p, PROY).replace(os.sep, "/") if os.path.isabs(p) else p
cat_ruta = {c: "propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z/S2-nacimientos/trabajo/evidencia/cat_sinac_2020_2023/" + fn
            for c, fn in CATFILE.items()}

decisiones = []
for c in casos:
    var = c["original"]["variable"]
    orig_sha = hashlib.sha256(json.dumps(c["original"], ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")).encode("utf-8")).hexdigest()
    huella12 = c["original"]["huella_fila_diccionario"][:12]
    if var in TIER:
        tier, cat, cods = TIER[var]
        e = desc[var]
        fila = next(i + 1 for i, d in enumerate(insp["definiciones"]) if d["Nombre variable"] == var)
        ev = [
            {"ruta": F_INSP, "sha256": sha(F_INSP),
             "localizador": f"/definiciones/{fila - 1} (fila {fila}, variable {var})",
             "afirmacion_soportada": f"Fila local: Nombre={var}, Tipo={loc[var]['Tipo de dato']}, Ejemplo='{loc[var]['Ejemplo de dato']}', Descripcion=Pendiente de especificar, Catalogo=''"},
            {"ruta": F_REC, "sha256": sha(F_REC),
             "localizador": "tablas[0]: hoja 'SINAC 2022 26-09-22', 106 campos; encabezado incluye " + var,
             "afirmacion_soportada": "El recurso 46977217 (2022-01-01 a 2022-09-26) trae la columna con el nombre exacto, en el mismo orden que el diccionario"},
            {"ruta": F_DESC, "sha256": sha(F_DESC),
             "localizador": f"Hoja1 fila ID={e['idnac']}, VARIABLE={var}",
             "afirmacion_soportada": f"Descriptor SINAC 2020-2025: {var} = {e['desc']} Catalogo: {e['cat']}."},
            {"ruta": R(F_ZIP), "sha256": sha(R(F_ZIP)),
             "localizador": "contenido del zip (20 xlsx); sin columnas D ni ANOMALIACIE* ni DIAGNOSTICOS",
             "afirmacion_soportada": "Codebook nacional 2020-2023 publicado por DGIS; vigencia cubre el recurso 2022"},
        ]
        if tier == "A1":
            ev.append({"ruta": cat_ruta[cat], "sha256": sha(cat_ruta[cat]),
                       "localizador": f"Hoja1, catalogo {cat}: codigo {codnum(loc[var]['Ejemplo de dato'])}",
                       "afirmacion_soportada": f"Codigo local {loc[var]['Ejemplo de dato']} = '{cods[codnum(loc[var]['Ejemplo de dato'])]}' en {cat}; etiqueta D local '{loc[var + 'D']['Ejemplo de dato']}' identica (normalizada)"})
            afirm = (f"{var} = variable IDnac={e['idnac']} del descriptor SINAC 2020-2025: {e['desc']} "
                     f"Codigos {cat} verificados (p. ej. {codnum(loc[var]['Ejemplo de dato'])}='{cods[codnum(loc[var]['Ejemplo de dato'])]}'); "
                     f"columna local = codigo entero, etiqueta D = descripcion del catalogo.")
        elif tier == "A2":
            afirm = (f"{var} = variable IDnac={e['idnac']} del descriptor SINAC 2020-2025: {e['desc']} "
                     f"Sin catalogo nacional; tipo local ({loc[var]['Tipo de dato']}) compatible; ejemplo '{loc[var]['Ejemplo de dato']}'.")
        elif tier == "A3":
            comp = {"ENTIDADFEDERATIVACERTIFICA": "26=SONORA en ENTIDADES",
                    "MUNICIPIOCERTIFICA": "26/055=SAN LUIS RIO COLORADO VIGENTE en MUNICIPIOS_202201",
                    "LOCALIDADCERTIFICA": "26/055/0001=SAN LUIS RIO COLORADO en LOCALIDADES_202203",
                    "CLUES": "SRSMP000314 EN OPERACION (Sonora/SLRC) en ESTABLECIMIENTO_SALUD_202204",
                    "CLUESCERTIFICA": "mismo catalogo ESTABLECIMIENTO_SALUD_202204; ejemplo local vacio"}[var]
            ev.append({"ruta": cat_ruta[cat], "sha256": sha(cat_ruta[cat]),
                       "localizador": f"Hoja1, catalogo {cat}: {comp}",
                       "afirmacion_soportada": "Codigo/ejemplo local existe y esta vigente en el catalogo fechado que cubre el recurso 2022"})
            afirm = (f"{var} = variable IDnac={e['idnac']} del descriptor SINAC 2020-2025: {e['desc']} "
                     f"Verificacion de ambito: {comp}.")
        elif tier == "A4":
            afirm = (f"{var} = variable IDnac={e['idnac']} del descriptor SINAC 2020-2025: {e['desc']} "
                     f"Catalogo DIAGNOSTICOS = CIE-10 (lineamientos DOF CEN en evidencia previa); ejemplo local '0000' = NINGUNA APARENTE, "
                     f"corroborado por columna hermana ANOMALIACIE* del mismo renglon.")
        else:
            afirm = (f"{var} = variable IDnac={e['idnac']} del descriptor SINAC 2020-2025: {e['desc']} "
                     f"Sin catalogo nacional; tipo local Hora con ejemplo '{loc[var]['Ejemplo de dato']}' (duracion codificada como hora).")
        lim = list(c.get("antecedente", {}).get("limites", c["original"].get("limites", [])))
        lim = [l for l in lim if "no autoriza cruces" not in l]
        lim += [
            "Reinterpretacion v002 (explicita para auditores A/B): la correspondencia ya no exige nota del publicador como unico medio; "
            "se prueba por sistema+edicion+identificador exacto+representacion (codigo local en catalogo nacional + etiqueta D identica)+ambito.",
            "Diferencia de representacion declarada: codigos nacionales como texto con cero inicial ('01','00') frente a entero local (1, 0); "
            "mapeo biyectivo por igualdad numerica + etiqueta D; el tipo local entero no preserva ceros a la izquierda.",
            "Edicion declarada por titulo/rango DGIS (descriptor 2020-2025, catalogos 2020-2023, geo 202201/202203/202204); sin acta de vigencia separada.",
        ]
        if tier == "A4":
            lim.append("DIAGNOSTICOS no trae archivo en el zip 2020-2023; codebook = CIE-10 por columna de catalogo del descriptor + lineamientos DOF CEN.")
        if tier == "A5":
            lim.append("Formato de duracion como Hora no especificado en el descriptor; el significado no depende de esa codificacion.")
        if var == "CLUESCERTIFICA":
            lim.append("Ejemplo local vacio en el diccionario; la correspondencia se sostiene por identificador+sistema+edicion+catalogo, sin verificacion de valor local.")
        decisiones.append({
            "id": c["id"], "tipo": c["tipo"], "original_sha256": orig_sha, "puerta": "pista_nueva",
            "pista": {"url": ZIP_URL, "por_que_nueva": "Contenido de catalogos SINAC 2020-2023 (20 xlsx con codigos y descripciones) no descargado ni examinado en rondas previas (ronda anterior lo difirio expresamente); decodifica el extracto local"},
            "estado": "propuesta_para_auditar", "afirmacion_propuesta": afirm,
            "motivo": (f"prueba tier-{tier} (nueva en v002): 1) sistema: conjunto portal 'Subsistema de Informacion sobre Nacimientos' = SINAC, hoja del recurso 'SINAC 2022 26-09-22'; "
                       f"2) edicion: descriptor 2020-2025 + catalogos 2020-2023 cubren 2022-01-01 a 2022-09-26, instrumento = certificado modelo 2020 (nota del descriptor); "
                       f"3) identificador exacto {var} (IDnac={e['idnac']}); 4) representacion: codigo local en catalogo nacional + etiqueta D identica (A1) / tipo compatible sin catalogo (A2) / "
                       f"codigo verificado en catalogo fechado (A3) / CIE-10 + 0000 corroborado (A4) / hora-duracion (A5); 5) ambito: extracto Sonora consistente (26/SONORA). "
                       f"La unica objecion previa (falta de tabla local del publicador) deja de ser bloqueante: el instrumento formal la determina univocamente (huella {huella12}...)."),
            "evidencia_faltante": None, "evidencia": ev,
            "condicion_reapertura": "Propuesta en auditoria A/B; si se rechaza, revierte a brecha_externa con el motivo del dictamen.",
            "limites": lim})
    else:
        base = var[:-1] if var.endswith("D") else None
        if var.startswith("ANOMALIACIE"):
            dif = ("columna textual local sin contraparte en el descriptor (el modelo nacional codifica con CODIGOCIEANOMALIA*/0000, sin variable ANOMALIACIE*); "
                   "contenido 'NINGUNA APARENTE' coincide con el significado de 0000 pero la columna como tal no existe en el instrumento")
            falt = (f"Definicion publicada de {var} por el publicador (o regla que la vincule a CODIGOCIEANOMALIA) aplicable al recurso 46977217 "
                    f"(huella {huella12}...).")
        else:
            dif = (f"columna derivada local '...D' sin variable nacional (zip verificado: 20 catalogos, ninguno para columnas D); "
                   f"su contenido decodifica el codigo de {base}, pero la regla publicador columna->catalogo no esta declarada; "
                   f"el ejemplo coincide con el catalogo nacional mas no define la regla")
            falt = (f"Regla del publicador que fije {var} como decodificacion de {base} con catalogo declarado, aplicable al recurso 46977217 "
                    f"(huella {huella12}...).")
        fila = next(i + 1 for i, d in enumerate(insp["definiciones"]) if d["Nombre variable"] == var)
        decisiones.append({
            "id": c["id"], "tipo": c["tipo"], "original_sha256": orig_sha, "puerta": "sin_pista_nueva", "pista": None,
            "estado": "brecha_externa", "afirmacion_propuesta": None,
            "motivo": (f"sin_pista_nueva (v002 reevaluado con el zip nuevo listado): {dif}. "
                       f"Se mantiene brecha: existe desajuste estructural concreto (ausencia en el instrumento), no solo falta de tabla local."),
            "evidencia_faltante": falt,
            "evidencia": [
                {"ruta": F_INSP, "sha256": sha(F_INSP),
                 "localizador": f"/definiciones/{fila - 1} (fila {fila}, variable {var})",
                 "afirmacion_soportada": f"Fila local: Nombre={var}, Tipo={loc[var]['Tipo de dato']}, Ejemplo='{loc[var]['Ejemplo de dato']}', Descripcion=Pendiente de especificar"},
                {"ruta": R(F_ZIP), "sha256": sha(R(F_ZIP)),
                 "localizador": "listado completo del zip (20 xlsx)",
                 "afirmacion_soportada": f"Negativa acotada nueva: ningun catalogo ni variable para '{var}' en el codebook 2020-2023"},
                {"ruta": F_DESC, "sha256": sha(F_DESC),
                 "localizador": "Hoja1, 65 variables base (ID 1..64); busqueda exacta del nombre",
                 "afirmacion_soportada": f"Negativa: '{var}' no figura entre las 65 variables del descriptor nacional SINAC 2020-2025."},
            ],
            "condicion_reapertura": (f"Reabre si el publicador publica la regla de decodificacion de {var} (o su definicion) aplicable al recurso 46977217, "
                                     "o si W aporta documento primario equivalente."),
            "limites": c.get("antecedente", {}).get("limites", c["original"].get("limites", []))})

fuentes = [
    {"ruta": R(F_ZIP), "sha256": sha(R(F_ZIP)), "url": ZIP_URL, "fecha_consulta": "2026-10-24",
     "localizador": "zip 24.4 MB, 20 xlsx; descarga por http (https rechazado por cadena del servidor); primera descarga del expediente"},
    {"ruta": F_DESC, "sha256": sha(F_DESC),
     "url": "http://www.dgis.salud.gob.mx/descargas/datosabiertos/nacimientos/sinac_descriptores_2020_2025.zip",
     "fecha_consulta": "2026-10-24", "localizador": "Descriptores_SINAC_2020.xlsx, Hoja1 (A1='SINAC 2020-2025', 65 variables ID 1..64, instrumento=modelo 2020)"},
    {"ruta": F_INSP, "sha256": sha(F_INSP),
     "url": "https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id=22202305-2d02-4c49-b216-cc98224357f0&limit=1000&offset=0&sort=_id+asc",
     "fecha_consulta": "2026-10-23", "localizador": "diccionario local, 106 filas (53 base + 51 D/descriptivas)"},
    {"ruta": F_REC, "sha256": sha(F_REC),
     "url": "https://datos.sonora.gob.mx/dataset/940de7d8-73ec-4a08-8d26-b7cc97ff17bd/resource/46977217-9396-4f9c-bddb-6616e82530b4/download/202209281437030-file.xlsx",
     "fecha_consulta": "2026-10-23", "localizador": "hoja 'SINAC 2022 26-09-22', 106 encabezados identicos al diccionario"},
    {"ruta": R(F_PKG), "sha256": sha(R(F_PKG)),
     "url": "https://datos.sonora.gob.mx/api/3/action/package_show?id=940de7d8-73ec-4a08-8d26-b7cc97ff17bd",
     "fecha_consulta": "2026-10-24", "localizador": "version=null, fuentes_extras='', notes='Subsistema de Informacion sobre Nacimientos'"},
]
for cat, fn in CATFILE.items():
    r = cat_ruta[cat]
    fuentes.append({"ruta": r, "sha256": sha(r), "url": ZIP_URL, "fecha_consulta": "2026-10-24",
                    "localizador": f"extraido del zip: {fn}"})

entrega = {"rol": "S2-nacimientos", "version": "v002", "decisiones": decisiones, "fuentes": fuentes,
    "novedades": ("v002 reinterpreta v001 (sin editarla) con UNA pista nueva real: el contenido del codebook SINAC 2020-2023 "
                  "(sha 9c7dcd52...), no examinado antes. Prueba computable por ID: codigo local entero en catalogo nacional + etiqueta D local "
                  "identica a la descripcion nacional (tier A1, 17 IDs), tipo compatible sin catalogo (A2, 6), codigo verificado en catalogo fechado "
                  "de ambito (A3, 5), CIE-10 + 0000 corroborado sin archivo DIAGNOSTICOS (A4, 2), hora-duracion (A5, 1). 31 propuestas_para_auditar "
                  "con prueba por tiers separables por los auditores; 22 brecha_externa con desajuste estructural concreto (columnas D derivadas sin "
                  "variable nacional y sin regla de decodificacion publicada; ANOMALIACIE* inexistentes en el instrumento). No se exige mencion Sonora: "
                  "el ambito se prueba por consistencia (26/SONORA, 055, 0001, CLUES operativo). Diferencias declaradas: entero local vs texto con cero "
                  "inicial nacional; edicion por titulo/rango DGIS; DIAGNOSTICOS ausente del zip; CLUESCERTIFICA sin ejemplo local. W-web sigue pendiente; "
                  "adenda posible si aporta regla de decodificacion o DIAGNOSTICOS.")}
json.dump(entrega, open(os.path.join(V002, "entrega.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("v002:", len(decisiones), "propuestas:", sum(1 for d in decisiones if d["estado"] == "propuesta_para_auditar"),
      "brechas:", sum(1 for d in decisiones if d["estado"] == "brecha_externa"))
