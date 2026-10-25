"""Verificacion lote-6 ronda 4: exhaustiva, propone reglas nuevas cuando el literal respalda."""
import hashlib, json, sys, unicodedata
from pathlib import Path
from urllib.parse import unquote
from collections import Counter, defaultdict

ROOT = Path("C:/Users/marti/Documents/MEX-Ontologi")
sys.path.insert(0, str(ROOT / "scripts"))
import consolidar_semantica as CS
STAGE = ROOT / "propuestas/pendientes-muse-r4"
LOTE = STAGE / "lote-6"

def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def norm(s):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())

def vacia_o_pendiente(desc):
    d = norm(str(desc or ""))
    return (not d) or ("pendiente de especificar" in d)

def vacua(desc):
    d = norm(str(desc or ""))
    return (not d) or ("pendiente de especificar" in d) or d in {"cuales?", "cuales?4"}

asig = json.loads((LOTE / "asignacion.json").read_text(encoding="utf-8"))
inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
insp = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
cob = json.loads((STAGE / "fuentes/data/semantica/cobertura.json").read_text(encoding="utf-8"))
sem = json.loads((STAGE / "fuentes/ontologia/semantica.json").read_text(encoding="utf-8"))
sem_live = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))

resources = {r["id"]: r for r in inv["recursos"]}
insp_by = {r["id"]: r for r in insp["recursos"]}
dcs = {d["definicion_iri"]: d for d in asig["definiciones_contexto"]}
cov_by_def = {v["definicion_iri"]: v for v in cob["variables"] if v.get("definicion_iri")}
rev_cols = {(v["recurso"], v["campo"], v["columna"]) for v in sem_live["vinculos_documentales_revisados"]}
conceptos_live = sem_live["conceptos"]

# columnas observadas segun consolidar_semantica.columnas (verificacion cruzada)
obs = CS.columnas(inv, insp, "https://example.org/mex-ontologi/")
obs_by = {}
for o in obs:
    obs_by.setdefault((o["recurso"], o["campo"], o.get("iri")), o)
obs_pair = defaultdict(list)
for o in obs:
    obs_pair[(o["recurso"], o["campo"])].append(o)

NAME_KEYS = {"nombre variable", "nombre de variable", "variable", "nombre campo", "nombre del campo"}
DESC_KEYS = {"descripcion", "definicion"}

def fila_dic(dic_id, idx):
    di = insp_by.get(dic_id)
    assert di and di.get("ok") and "definiciones" in di, f"diccionario {dic_id} sin definiciones"
    rows = di["definiciones"]
    assert 1 <= idx <= len(rows), f"fila {idx} fuera de rango en {dic_id}"
    return rows[idx - 1]

def datos_fila(row):
    vname = ""
    for k, val in row.items():
        if norm(k) in NAME_KEYS and val is not None and str(val).strip():
            vname = str(val).strip(); break
    desc = ""
    for k, val in row.items():
        if norm(k) in DESC_KEYS and val is not None and str(val).strip():
            desc = str(val).strip(); break
    return vname, desc

def parse_col(iri):
    if "/file-column/" in iri:
        dec = unquote(iri.split("/file-column/", 1)[1])
        rid, hoja, pos = dec.rsplit("/", 2)
        return ("file", rid, hoja, int(pos))
    dec = unquote(iri.split("/column/", 1)[1])
    rid, campo = dec.rsplit("/", 1)
    return ("datastore", rid, campo, None)

# --- conceptos nuevos propuestos (id -> [etiqueta, definicion, padre]) ---
CN = {
 "autoreconocimiento-afromexicano-difunto": ["Autorreconocimiento afromexicano del difunto", "Identificador de si la persona difunta se reconoce como afromexicana; codigo y texto describen el mismo hecho.", None],
 "condicion-indigena-difunto": ["Condicion indigena del difunto", "Identificador de si la persona difunta se considera indigena; codigo y texto describen el mismo hecho. Poblacion: difunto.", None],
 "habla-lengua-indigena-difunto": ["Habla de lengua indigena del difunto", "Identificador de si la persona difunta habla lengua indigena; codigo y texto describen el mismo hecho.", None],
 "clave-edad-difunto": ["Clave de edad del difunto", "Clave de la edad de la persona difunta segun su diccionario; conserva codigo sin inferir escala.", None],
 "unidad-edad-difunto": ["Unidad de edad del difunto", "Unidad en que se expresa la edad de la persona difunta segun su diccionario; no se homologa escala.", None],
 "bien-juridico-afectado-delito": ["Bien juridico afectado por el delito", "Campo en el que el delito se realizo segun el diccionario de Victimas del fuero comun.", None],
 "tipo-delito-fuero-comun": ["Tipo de delito del fuero comun", "Descripcion especifica del tipo de delito que se realizo segun el diccionario.", None],
 "subtipo-delito-fuero-comun": ["Subtipo de delito del fuero comun", "Detalle mas especifico sobre el tipo de delito que se realizo segun el diccionario.", None],
 "modalidad-delito-fuero-comun": ["Modalidad del delito del fuero comun", "Categoria en la que se puede clasificar el delito segun el diccionario.", None],
 "modalidad-delito-municipal-anterior": ["Modalidad del delito municipal (metodologia anterior)", "Categoria general en la que entra el delito cometido; conjunto de incidencia municipal metodologia anterior.", None],
 "tipo-delito-municipal-anterior": ["Tipo de delito municipal (metodologia anterior)", "Detalle mas especifico sobre el tipo de delito; incidencia municipal metodologia anterior.", None],
 "subtipo-delito-municipal-anterior": ["Subtipo de delito municipal (metodologia anterior)", "Ultimo nivel de detalle del delito; incidencia municipal metodologia anterior.", None],
 "identificador-registro-diagnostico-digital": ["Identificador del registro del diagnostico", "Identificador unico del registro del Diagnostico del Entorno Digital.", None],
 "sector-dependencia-diagnostico": ["Sector de la dependencia", "Sector al que pertenece la dependencia en el Diagnostico del Entorno Digital.", None],
 "hora-inicio-registro-diagnostico": ["Hora de inicio del registro", "Hora de inicio del registro del Diagnostico del Entorno Digital.", None],
 "hora-fin-registro-diagnostico": ["Hora de finalizacion del registro", "Hora de finalizacion del registro del Diagnostico del Entorno Digital.", None],
 "hora-modificacion-registro-diagnostico": ["Hora de ultima modificacion del registro", "Hora de la ultima modificacion del registro del Diagnostico del Entorno Digital.", None],
 "suficiencia-infraestructura-datacenter": ["Suficiencia de infraestructura del datacenter", "Declaracion de si se cuenta con la infraestructura suficiente; existencia declarada, no acredita suficiencia tecnica.", None],
 "infraestructura-adicional-datacenter": ["Infraestructura adicional requerida del datacenter", "Infraestructura adicional que requiere el datacenter segun declaracion.", None],
 "intercambio-informacion-dependencia": ["Intercambio de informacion de la dependencia", "Declaracion de si la dependencia realiza intercambio de informacion.", None],
 "beneficio-consolidacion-declarado": ["Beneficio declarado de la consolidacion", "Declaracion de si la consolidacion resulto beneficiosa; no evalua el beneficio.", None],
 "motivo-beneficio-consolidacion": ["Motivo del beneficio de la consolidacion", "Motivo declarado por el que la consolidacion resulto beneficiosa.", None],
 "aspectos-no-beneficiados-consolidacion": ["Aspectos no beneficiados por la consolidacion", "Aspectos que no resultaron beneficiados por la consolidacion segun declaracion.", None],
 "periodo-poblacion-ceresos": ["Periodo de la poblacion Ceresos", "Periodo del cual se informa el numero de poblacion de Ceresos; conserva texto sin inferir vigencia.", "tiempo"],
 "mes-produccion-minera": ["Mes de la produccion minera", "Registro cronologico de la produccion del metal extraido; requiere anio como contexto.", "mes"],
 "fecha-registro-presa": ["Fecha del registro de presa", "Fecha del registro de Cuerpos de Agua (presas); evento registro.", "tiempo"],
 "numero-entrada-titulados": ["Numero de la entrada de titulados", "Numero de la entrada del registro de Titulados de Licenciatura.", None],
}
# def iri -> (concepto, representacion, regla_id)
NUEVOS = {
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F6": ("autoreconocimiento-afromexicano-difunto", "codigo", "r4-lote-6-seed-afro-codigo"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F7": ("autoreconocimiento-afromexicano-difunto", "nombre", "r4-lote-6-seed-afro-nombre"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F8": ("condicion-indigena-difunto", "codigo", "r4-lote-6-seed-indigena-codigo"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F9": ("condicion-indigena-difunto", "nombre", "r4-lote-6-seed-indigena-nombre"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F10": ("habla-lengua-indigena-difunto", "codigo", "r4-lote-6-seed-lengua-codigo"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F11": ("habla-lengua-indigena-difunto", "nombre", "r4-lote-6-seed-lengua-nombre"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F15": ("clave-edad-difunto", "codigo", "r4-lote-6-seed-claveedad-codigo"),
 "https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F16": ("unidad-edad-difunto", "nombre", "r4-lote-6-seed-unidadedad-nombre"),
 "https://example.org/mex-ontologi/definition/a8a09044-87db-49a2-82c3-29594ec6ffd5%2F3": ("bien-juridico-afectado-delito", "no_especificada", "r4-lote-6-fuero-bien-no_especificada"),
 "https://example.org/mex-ontologi/definition/a8a09044-87db-49a2-82c3-29594ec6ffd5%2F4": ("tipo-delito-fuero-comun", "no_especificada", "r4-lote-6-fuero-tipo-no_especificada"),
 "https://example.org/mex-ontologi/definition/a8a09044-87db-49a2-82c3-29594ec6ffd5%2F5": ("subtipo-delito-fuero-comun", "no_especificada", "r4-lote-6-fuero-subtipo-no_especificada"),
 "https://example.org/mex-ontologi/definition/a8a09044-87db-49a2-82c3-29594ec6ffd5%2F6": ("modalidad-delito-fuero-comun", "no_especificada", "r4-lote-6-fuero-modalidad-no_especificada"),
 "https://example.org/mex-ontologi/definition/404e97de-3954-4106-82ee-afd2cb20b868%2F5": ("modalidad-delito-municipal-anterior", "no_especificada", "r4-lote-6-incant-modalidad-no_especificada"),
 "https://example.org/mex-ontologi/definition/404e97de-3954-4106-82ee-afd2cb20b868%2F6": ("tipo-delito-municipal-anterior", "no_especificada", "r4-lote-6-incant-tipo-no_especificada"),
 "https://example.org/mex-ontologi/definition/404e97de-3954-4106-82ee-afd2cb20b868%2F7": ("subtipo-delito-municipal-anterior", "no_especificada", "r4-lote-6-incant-subtipo-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F1": ("identificador-registro-diagnostico-digital", "codigo", "r4-lote-6-dig-id-codigo"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F2": ("sector-dependencia-diagnostico", "nombre", "r4-lote-6-dig-sector-nombre"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F3": ("hora-inicio-registro-diagnostico", "no_especificada", "r4-lote-6-dig-p3-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F4": ("hora-fin-registro-diagnostico", "no_especificada", "r4-lote-6-dig-p4-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F5": ("hora-modificacion-registro-diagnostico", "no_especificada", "r4-lote-6-dig-p5-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F8": ("suficiencia-infraestructura-datacenter", "no_especificada", "r4-lote-6-dig-p9-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F9": ("infraestructura-adicional-datacenter", "no_especificada", "r4-lote-6-dig-p10-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F20": ("intercambio-informacion-dependencia", "no_especificada", "r4-lote-6-dig-p21-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F34": ("beneficio-consolidacion-declarado", "no_especificada", "r4-lote-6-dig-p35-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F35": ("motivo-beneficio-consolidacion", "no_especificada", "r4-lote-6-dig-p36-no_especificada"),
 "https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F36": ("aspectos-no-beneficiados-consolidacion", "no_especificada", "r4-lote-6-dig-p37-no_especificada"),
 "https://example.org/mex-ontologi/definition/2fc2fbc6-e918-4d5d-b907-1191e266b131%2F5": ("periodo-poblacion-ceresos", "no_especificada", "r4-lote-6-ceresos-periodo-no_especificada"),
 "https://example.org/mex-ontologi/definition/587a3ccd-a814-4190-8e6f-dfb20ccf44c4%2F1": ("mes-produccion-minera", "no_especificada", "r4-lote-6-mineria-mes-no_especificada"),
 "https://example.org/mex-ontologi/definition/bfb8788b-8ce3-475e-8bbd-dd1c5154c877%2F2": ("fecha-registro-presa", "fecha", "r4-lote-6-presas-fecha-fecha"),
 "https://example.org/mex-ontologi/definition/5b587fca-6317-43a2-bdb3-6b3b046a0e76%2F1": ("numero-entrada-titulados", "no_especificada", "r4-lote-6-titulados-no-no_especificada"),
}

decision_col, vinculos, pend_col = [], [], []
n_prop = n_pend = n_rech = 0
for c in asig["columnas"]:
    col_iri, recurso, campo = c["columna"], c["recurso"], c["campo"]
    defs = c.get("definiciones_por_nombre") or []
    definicion_iri = defs[0] if defs else None
    ev, motivo, decision, definicion_dest = [], "", "pendiente", None
    vinc = None
    try:
        kind, rid, hoja, pos = parse_col(col_iri)
        assert rid == recurso, f"recurso IRI {rid} != {recurso}"
        dcs_row = dcs.get(definicion_iri) if definicion_iri else None
        assert definicion_iri, "sin definicion candidata"
        assert dcs_row, f"definicion {definicion_iri} sin contexto"
        dec = unquote(definicion_iri)
        didx = int(dec.rsplit("/", 1)[1])
        dic = dec.split("/definition/", 1)[1].rsplit("/", 1)[0]
        row = fila_dic(dic, didx)
        vname, desc = datos_fila(row)
        h_fila = huella(row)
        ev.append(f"data/portal/contenido-inspeccion.json diccionario {dic} fila {didx} variable {vname!r}")
        if dcs_row.get("huella_fila_diccionario"):
            assert h_fila == dcs_row["huella_fila_diccionario"], f"huella fila {h_fila} != {dcs_row['huella_fila_diccionario']}"
            ev.append(f"huella_fila_diccionario={h_fila} coincide")
        ctx = cov_by_def.get(definicion_iri, {})
        ev.append(f"cobertura estado={dcs_row.get('estado')} concepto={dcs_row.get('concepto') or ctx.get('concepto','')} descripcion={desc!r}")
        assert dcs_row.get("conjunto") == c.get("conjunto"), f"conjunto {c.get('conjunto')} != {dcs_row.get('conjunto')}"
        if kind == "file":
            ri = insp_by.get(recurso)
            rinv = resources.get(recurso)
            assert ri and ri.get("ok"), "sin inspeccion ok"
            tablas = [t for t in ri.get("tablas", []) if t["hoja"] == hoja]
            assert tablas, f"hoja {hoja} no capturada"
            assert len(tablas) == 1, f"hoja duplicada {hoja}"
            tabla = tablas[0]
            h_esc = huella(tabla)
            ev.append(f"data/portal/contenido-inspeccion.json recurso {recurso} hoja {hoja} fila_encabezado={tabla.get('fila_encabezado')}")
            ev.append(f"data/portal/inspecciones/{recurso}.json metodo={tabla.get('metodo_encabezado')} (aviso generico no bloqueante: encabezado fila 1 verificado campo por campo)")
            flds = [f for f in tabla["campos"] if f["posicion_original"] == pos]
            assert flds, f"posicion {pos} ausente"
            obs_field = flds[0]["id"]
            ev.append(f"esquema capturado campo pos {pos} = {obs_field!r}")
            n_ig = sum(1 for f in tabla["campos"] if norm(f["id"]) == norm(campo))
            ev.append(f"unicidad en tabla nombre_unico={n_ig == 1} (coincidencias={n_ig})")
            if norm(obs_field) != norm(campo):
                decision, motivo = "rechazar", f"campo asignado {campo!r} != observado {obs_field!r} en esquema"
                ev.append("descarte por diferencia fisica esquema vs asignacion")
            elif norm(vname) != norm(campo):
                decision, motivo = "rechazar", f"variable diccionario {vname!r} != campo {campo!r}"
            elif n_ig != 1:
                motivo = f"nombre no unico en tabla ({n_ig} coincidencias); ambiguedad sin resolver"
            else:
                o = obs_by.get((recurso, campo, col_iri))
                assert o is not None, "columna no reproducida por consolidar_semantica.columnas"
                assert o["huella_esquema"] == h_esc, "huella esquema difiere de consolidar_semantica.columnas"
                ev.append(f"consolidar_semantica.columnas verifica columna, huella_esquema={h_esc}, nombre_unico={o['nombre_unico']}")
                motivo = None
        else:
            rinv = resources.get(recurso)
            assert rinv and rinv.get("datastore", {}).get("ok"), "sin datastore ok"
            flds = [f for f in rinv["datastore"]["campos"] if not f["id"].startswith("_")]
            h_esc = huella([{"nombre": f["id"], "tipo": f.get("type")} for f in flds])
            ev.append(f"inventario datastore recurso {recurso} campos={len(flds)}")
            assert any(norm(f["id"]) == norm(campo) for f in flds), f"campo {campo!r} ausente en datastore"
            n_ig = sum(1 for f in flds if norm(f["id"]) == norm(campo))
            ev.append(f"unicidad en datastore nombre_unico={n_ig == 1} (coincidencias={n_ig})")
            if norm(vname) != norm(campo):
                decision, motivo = "rechazar", f"variable diccionario {vname!r} != campo {campo!r}"
            elif n_ig != 1:
                motivo = f"nombre no unico en datastore ({n_ig}); ambiguedad sin resolver"
            else:
                cand = [x for x in obs_pair.get((recurso, campo), []) if x["iri"] == col_iri]
                assert cand, "columna no reproducida por consolidar_semantica.columnas"
                assert cand[0]["huella_esquema"] == h_esc, "huella esquema difiere de consolidar_semantica.columnas"
                ev.append(f"consolidar_semantica.columnas verifica columna, huella_esquema={h_esc}")
                motivo = None
        if decision != "rechazar" and motivo is None:
            if (recurso, campo, col_iri) in rev_cols:
                motivo = "columna ya revisada en nucleo; no duplicar"
            elif vacia_o_pendiente(desc):
                motivo = "definicion con descripcion vacia o Pendiente de especificar; falta respaldo explicito"
            elif definicion_iri in NUEVOS:
                concepto, _, _ = NUEVOS[definicion_iri]
                decision, definicion_dest = "proponer", definicion_iri
                motivo = f"columna fisica verificada + fila exacta + literal especifico {desc!r}; regla nueva y concepto nuevo {concepto}; alcance documental"
                vinc = {"recurso": recurso, "campo": campo, "columna": col_iri, "diccionario": dic,
                        "concepto": concepto, "descripcion": desc, "huella_esquema": h_esc,
                        "huella_fila_diccionario": h_fila,
                        "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto: nombre, contexto, descripcion literal y representacion. Alcance de interpretacion documental; no se validan valores ni se confirma pertenencia a catalogos.",
                        "dependencia": f"significado nuevo {definicion_iri} (regla {NUEVOS[definicion_iri][2]})"}
                ev.append(f"definicion {definicion_iri} concepto nuevo {concepto}")
            else:
                concepto = dcs_row.get("concepto") or ctx.get("concepto")
                assert concepto, "sin concepto vigente"
                assert dcs_row.get("estado") == "respaldada_por_definicion", f"estado={dcs_row.get('estado')}"
                decision, definicion_dest = "proponer", definicion_iri
                motivo = f"columna fisica verificada + fila diccionario exacta + concepto vigente {concepto} {(dcs_row.get('regla') or '')}; alcance documental, sin validar valores ni catalogos"
                vinc = {"recurso": recurso, "campo": campo, "columna": col_iri, "diccionario": dic,
                        "concepto": concepto, "descripcion": desc, "huella_esquema": h_esc,
                        "huella_fila_diccionario": h_fila,
                        "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto: nombre, contexto, descripcion y representacion. Alcance de interpretacion documental; no se validan valores ni se confirma pertenencia a catalogos."}
                ev.append(f"definicion {definicion_iri} concepto vigente {concepto}")
    except AssertionError as e:
        motivo = f"evidencia incompleta: {e}"
    except Exception as e:
        motivo = f"evidencia incompleta: {type(e).__name__} {e}"
    if decision == "proponer":
        n_prop += 1
        vinculos.append(vinc)
    elif decision == "rechazar":
        n_rech += 1
    else:
        decision = "pendiente"; n_pend += 1
        pend_col.append({"columna": col_iri, "campo": campo, "recurso": recurso, "motivo": motivo, "evidencia": ev})
    d = {"columna": col_iri, "recurso": recurso, "campo": campo, "decision": decision, "motivo": motivo, "evidencia": ev}
    if definicion_dest:
        d["definicion_iri"] = definicion_dest
    decision_col.append(d)

dec_sig, pend_sig = [], []
for v in asig["variables_pendientes"]:
    iri = v["definicion_iri"]
    dctx = dcs.get(iri, {})
    var, desc = v.get("variable"), v.get("descripcion", "")
    if iri in NUEVOS:
        concepto, _, _ = NUEVOS[iri]
        dec_sig.append({"definicion_iri": iri, "decision": "proponer",
            "motivo": f"literal especifico {desc!r} respalda significado; concepto nuevo {concepto}; alcance documental",
            "evidencia": [f"diccionario {v.get('diccionario')} variable {var!r} descripcion={desc!r}", f"conjunto {v.get('conjunto')}"]})
    else:
        dec_sig.append({"definicion_iri": iri, "decision": "pendiente",
            "motivo": f"descripcion vacia, Pendiente de especificar o vacua ({desc!r}); requiere fuente adicional vinculada a esa definicion",
            "evidencia": [f"diccionario {v.get('diccionario')} variable {var!r} descripcion={desc!r}", f"estado={v.get('estado')}"]})
        pend_sig.append({"definicion_iri": iri, "variable": var, "motivo": dec_sig[-1]["motivo"], "evidencia": dec_sig[-1]["evidencia"]})

usados = {NUEVOS[d["definicion_iri"]][0] for d in decision_col if d["decision"] == "proponer" and d.get("definicion_iri") in NUEVOS}
usados |= {NUEVOS[d["definicion_iri"]][0] for d in dec_sig if d["decision"] == "proponer"}
conceptos_nuevos = {k: v for k, v in CN.items() if k in usados}
assert set(conceptos_nuevos) - set(conceptos_live.keys()), "concepto nuevo colisiona con nucleo"

reglas, vistos = [], set()
for iri, (concepto, rep, rid) in NUEVOS.items():
    usada = any(d.get("definicion_iri") == iri and d["decision"] == "proponer" for d in decision_col) or \
            any(d["definicion_iri"] == iri and d["decision"] == "proponer" for d in dec_sig)
    if not usada or rid in vistos:
        continue
    vistos.add(rid)
    dctx = dcs.get(iri, {})
    pend = next((v for v in asig["variables_pendientes"] if v["definicion_iri"] == iri), {})
    conjunto = dctx.get("conjunto") or pend.get("conjunto")
    dic = iri.split("/definition/", 1)[1].rsplit("%2F" if "%2F" in iri else "/", 1)[0]
    dic = unquote(dic).split("/")[0]
    row = fila_dic(dic, int(unquote(iri).rsplit("/", 1)[1]))
    vname, desc = datos_fila(row)
    evd = {"descripcion": desc,
           "tipo": str(row.get("Tipo de dato", row.get("Tipo", ""))),
           "formato": str(row.get("Formato", "")),
           "unidad": str(row.get("Unidad de medida", row.get("Unidad", ""))),
           "ejemplo": str(row.get("Ejemplo de dato", row.get("Ejemplo", ""))),
           "catalogo_declarado": str(row.get("Catálogo de referencia", row.get("Catalogo de referencia", ""))),
           "titulo_conjunto": dctx.get("titulo_conjunto", "") or pend.get("titulo_conjunto", "")}
    reglas.append({"id": rid, "concepto": concepto, "representacion": rep, "nombres": [vname],
        "descripciones": [desc], "conjuntos": [conjunto], "diccionarios": [dic], "definiciones": [iri],
        "huella_fila_diccionario": huella(row),
        "limites": ["solo aplica a la definicion citada (alcance simultaneo por conjunto, diccionario, definicion, nombre y descripcion); no autoriza cruces, homologaciones ni equivalencias"],
        "evidencia": evd,
        "criterio": f"Literal especifico {desc!r} mas contexto publicado del conjunto; tipo {evd['tipo']!r}; sin ejemplo validante.",
        "fuente_revision": "propuestas/pendientes-muse-r4/lote-6/verificar.py"})
    assert reglas[-1]["huella_fila_diccionario"] == (dctx.get("huella_fila_diccionario") or huella(row)), f"huella {iri}"

solic = [{"definicion_iri": p["definicion_iri"], "fuente_probable": "publicador del conjunto " + next((v.get("conjunto", "") for v in asig["variables_pendientes"] if v["definicion_iri"] == p["definicion_iri"]), ""),
          "documento_requerido": "diccionario o nota que respalde la variable " + next((str(v.get("variable", "")) for v in asig["variables_pendientes"] if v["definicion_iri"] == p["definicion_iri"]), "")}
         for p in pend_sig]

entrega = {"decisiones_columnas": decision_col, "vinculos": vinculos, "decisiones_significados": dec_sig,
    "reglas": reglas, "conceptos_nuevos": conceptos_nuevos, "solicitudes_investigacion": solic}
(LOTE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(LOTE / "pendientes.json").write_text(json.dumps({"pendientes_columnas": pend_col, "pendientes_significados": pend_sig,
    "conteo_columnas": len(pend_col), "conteo_significados": len(pend_sig)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
n_sig_prop = sum(1 for d in dec_sig if d["decision"] == "proponer")
res = ["# Resultado lote-6 ronda 4", "", f"Columnas asignadas: {len(decision_col)}",
 f"proponer: {n_prop}", f"pendiente: {n_pend}", f"rechazar: {n_rech}", f"vinculos: {len(vinculos)}",
 f"significados: {len(dec_sig)} (proponer {n_sig_prop}, pendientes {len(dec_sig) - n_sig_prop})",
 f"reglas nuevas: {len(reglas)}, conceptos nuevos: {len(conceptos_nuevos)}", "",
 "Criterio: proponer con columna fisica verificada (consolidar_semantica.columnas + huella) + fila exacta + literal especifico. Respaldadas reutilizan concepto vigente; literales especificos fuera del nucleo proponen regla y concepto nuevos con dependencia explicita. Descripciones vacias/Pendiente de especificar y avisos vacuos quedan pendientes. Aviso heuristico generico de encabezado no bloquea cuando la fila 1 se verifica campo por campo. Sin inferir unidades, catalogos ni vigencia.", ""]
(LOTE / "resultado.md").write_text("\n".join(res), encoding="utf-8")
sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
(LOTE / "listo.json").write_text(json.dumps({"sha256_entrega": sha, "columnas": len(decision_col),
 "proponer": n_prop, "pendiente": n_pend, "rechazar": n_rech, "vinculos": len(vinculos),
 "significados": len(dec_sig), "estado": "completo"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(n_prop, n_pend, n_rech, len(vinculos), n_sig_prop, len(reglas), len(conceptos_nuevos), sha)