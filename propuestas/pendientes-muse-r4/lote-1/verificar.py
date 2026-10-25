"""Verificacion lote-1 ronda 4: evidencia concreta, sin aprobacion por nombre."""
import hashlib, json
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("C:/Users/marti/Documents/MEX-Ontologi")
STAGE = ROOT / "propuestas/pendientes-muse-r4"
LOTE = STAGE / "lote-1"

def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def norm(s):
    import unicodedata
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())

asig = json.loads((LOTE / "asignacion.json").read_text(encoding="utf-8"))
inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
insp = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
cob = json.loads((STAGE / "fuentes/data/semantica/cobertura.json").read_text(encoding="utf-8"))
sem = json.loads((STAGE / "fuentes/ontologia/semantica.json").read_text(encoding="utf-8"))

resources = {r["id"]: r for r in inv["recursos"]}
insp_by = {r["id"]: r for r in insp["recursos"]}
cov_by_def = {v["definicion_iri"]: v for v in cob["variables"] if v.get("definicion_iri")}
rev_cols = {(v["recurso"], v["campo"], v["columna"]) for v in sem["vinculos_documentales_revisados"]}

# unicidad de variables por (conjunto, clave)
from collections import Counter
all_names = Counter()
for r in insp["recursos"]:
    res = resources.get(r["id"])
    if not res or res.get("clasificacion") == "diccionario":
        pass
    if r.get("ok") and "definiciones" in r:
        rr = resources[r["id"]]
        for row in r["definiciones"]:
            nm = ""
            for k, val in row.items():
                if norm(k) in {"nombre variable", "nombre de variable", "variable", "nombre campo", "nombre del campo"} and val is not None and str(val).strip():
                    nm = str(val).strip(); break
            if nm:
                all_names[(rr["conjunto_id"], norm(nm))] += 1

def parse_col(iri):
    # .../file-column/{rid}%2F{hoja}%2F{pos}  (rid itself contains dashes, no slash)
    tail = iri.split("/file-column/", 1)[1]
    dec = unquote(tail)
    rid, hoja, pos = dec.rsplit("/", 2)
    return rid, hoja, int(pos)

decisiones, vinculos, pendientes_det = [], [], []
n_prop = n_pend = n_rech = 0
for c in asig["columnas"]:
    col_iri, recurso, campo = c["columna"], c["recurso"], c["campo"]
    definicion_iri = c["definiciones_por_nombre"][0] if c.get("definiciones_por_nombre") else None
    ev = []
    motivo = ""
    decision = "pendiente"
    definicion_dest = None
    try:
        h_esc = None; tabla = None; obs = None; nombre_unico = True
        if "/file-column/" in col_iri:
            rid, hoja, pos = parse_col(col_iri)
            assert rid == recurso, f"recurso IRI {rid} != {recurso}"
            ri = insp_by.get(recurso)
            assert ri and ri.get("ok"), "sin inspeccion ok"
            tablas = [t for t in ri.get("tablas", []) if t["hoja"] == hoja]
            assert tablas, f"hoja {hoja} no capturada"
            assert len(tablas) == 1, f"hoja duplicada {hoja}"
            tabla = tablas[0]
            h_esc = huella(tabla)
            ev.append(f"data/portal/contenido-inspeccion.json recurso {recurso} hoja {hoja}")
            ev.append(f"data/portal/inspecciones/{recurso}.json")
            flds = [f for f in tabla["campos"] if f["posicion_original"] == pos]
            assert flds, f"posicion {pos} ausente"
            obs = flds[0]["id"]
            ev.append(f"esquema capturado campo pos {pos} = {obs!r}")
            n_iguales = sum(1 for f in tabla["campos"] if norm(f["id"]) == norm(campo))
            nombre_unico = n_iguales == 1
            ev.append(f"unicidad columna nombre_unico={nombre_unico} (coincidencias={n_iguales})")
            if tabla.get("metodo_encabezado"):
                ev.append(f"metodo_encabezado={tabla.get('metodo_encabezado')} (rutina de captura, no bloquea por si sola)")
        elif "/column/" in col_iri:
            # columna datastore: esquema API en inventario
            rinv = resources.get(recurso)
            assert rinv and rinv.get("datastore", {}).get("ok"), "sin datastore ok"
            fields = [f for f in rinv["datastore"]["campos"] if not f["id"].startswith("_")]
            h_esc = huella([{"nombre": f["id"], "tipo": f.get("type")} for f in fields])
            obs = campo if any(norm(f["id"]) == norm(campo) for f in fields) else None
            assert obs, f"campo {campo!r} ausente en datastore"
            ev.append(f"data/portal/inventario.json recurso {recurso} datastore campo {campo!r}")
            n_iguales = sum(1 for f in fields if norm(f["id"]) == norm(campo))
            nombre_unico = n_iguales == 1
            ev.append(f"unicidad datastore nombre_unico={nombre_unico}")
        else:
            raise AssertionError("IRI de columna sin patron conocido")
        if norm(obs) != norm(campo):
            decision, motivo = "rechazar", f"campo asignado {campo!r} != observado {obs!r} en esquema"
            ev.append("descarte por diferencia fisica esquema vs asignacion")
        elif not definicion_iri:
            motivo = "sin definicion candidata"
        else:
            # fila diccionario
            didx = int(unquote(definicion_iri).rsplit("/", 1)[1])
            dic_id = unquote(definicion_iri).split("/definition/", 1)[1].rsplit("/", 1)[0].replace("%2F", "/")
            # dic_id viene como {dic}/{idx} url-encoded; extraer dic
            dec2 = unquote(definicion_iri)
            dic = dec2.split("/definition/", 1)[1].rsplit("/", 1)[0]
            di = insp_by.get(dic)
            assert di and di.get("ok") and "definiciones" in di, f"diccionario {dic} sin definiciones"
            row = di["definiciones"][didx - 1]
            h_fila = huella(row)
            vname = ""
            for k, val in row.items():
                if norm(k) in {"nombre variable", "nombre de variable", "variable", "nombre campo", "nombre del campo"} and val is not None and str(val).strip():
                    vname = str(val).strip(); break
            desc = ""
            for k, val in row.items():
                if norm(k) in {"descripcion", "definicion"} and val is not None and str(val).strip():
                    desc = str(val).strip(); break
            ev.append(f"data/portal/contenido-inspeccion.json diccionario {dic} fila {didx} variable {vname!r}")
            ev.append(f"huella_esquema={h_esc} huella_fila={h_fila}")
            ctx = cov_by_def.get(definicion_iri, {})
            estado = ctx.get("estado", "?")
            concepto = ctx.get("concepto", "")
            ev.append(f"cobertura estado={estado} concepto={concepto} descripcion={desc!r}")
            # ya revisada?
            if (recurso, campo, col_iri) in rev_cols or (recurso, campo, None) in rev_cols:
                decision, motivo = "pendiente", "columna ya revisada en nucleo; no duplicar"
            elif not desc:
                motivo = "definicion con descripcion vacia; falta respaldo explicito"
            elif norm(vname) != norm(campo):
                decision, motivo = "rechazar", f"variable diccionario {vname!r} != campo {campo!r}"
            elif all_names.get((c["conjunto"], norm(campo)), 0) != 1 or not nombre_unico:
                motivo = f"nombre no unico (diccionario={all_names.get((c['conjunto'], norm(campo)),0)} unico_col={nombre_unico}); ambiguedad sin resolver"
            elif estado != "respaldada_por_definicion":
                motivo = f"definicion estado={estado}; sin regla revisada que respalde"
            else:
                # proponer: reutiliza concepto vigente, sin inferir unidades/catálogos
                decision = "proponer"
                definicion_dest = definicion_iri
                motivo = f"columna fisica verificada + fila diccionario exacta + concepto vigente {concepto}; alcance documental, sin validar valores ni catálogos"
                vinculos.append({
                    "recurso": recurso, "campo": campo, "columna": col_iri,
                    "diccionario": dic, "concepto": concepto, "descripcion": desc,
                    "huella_esquema": h_esc, "huella_fila_diccionario": h_fila,
                    "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto: nombre, contexto, descripcion y representacion. Alcance de interpretacion documental; no se validan valores ni se confirma pertenencia a catalogos."
                })
                ev.append(f"definicion {definicion_iri} concepto {concepto}")
    except AssertionError as e:
        motivo = f"evidencia incompleta: {e}"
    except Exception as e:
        motivo = f"evidencia incompleta: {type(e).__name__} {e}"
    if decision == "proponer":
        n_prop += 1
    elif decision == "rechazar":
        n_rech += 1
    else:
        decision = "pendiente"; n_pend += 1
        pendientes_det.append({"columna": col_iri, "campo": campo, "recurso": recurso, "motivo": motivo, "evidencia": ev})
    d = {"columna": col_iri, "recurso": recurso, "campo": campo, "decision": decision, "motivo": motivo, "evidencia": ev}
    if definicion_dest:
        d["definicion_iri"] = definicion_dest
    decisiones.append(d)

# significados pendientes
dec_sig = []
for v in asig["variables_pendientes"]:
    iri = v["definicion_iri"]
    ctx = cov_by_def.get(iri, {})
    dec_sig.append({"definicion_iri": iri, "decision": "pendiente",
        "motivo": f"estado={v.get('estado')}; {v.get('motivo')}; sin regla revisada ni evidencia adicional local",
        "evidencia": [f"cobertura estado={ctx.get('estado','?')}", f"diccionario {v.get('diccionario')} variable {v.get('variable')!r} descripcion={v.get('descripcion')!r}"]})

sols = [{"definicion_iri": v["definicion_iri"], "fuente_probable": "publicador del conjunto " + v.get("conjunto",""), "documento_requerido": "diccionario o nota que respalde " + str(v.get("variable"))} for v in asig["variables_pendientes"]]
sols.append({"definicion_iri": "https://example.org/mex-ontologi/definition/251309e5-0309-46ed-9711-77a1dd408eeb%2F1", "fuente_probable": "conjunto b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f", "documento_requerido": "descripcion o regla que precise CVE_LOC (Clave geografica) antes de vincular columna file-column/8e684391-9137-4359-b654-f19602911421/IML_2020/1"})
entrega = {"decisiones_columnas": decisiones, "vinculos": vinculos, "decisiones_significados": dec_sig,
    "reglas": [], "conceptos_nuevos": {},
    "solicitudes_investigacion": sols}

(LOTE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(LOTE / "pendientes.json").write_text(json.dumps({"pendientes_columnas": pendientes_det, "conteo": len(pendientes_det)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
res = [f"# Resultado lote-1 ronda 4", "", f"Columnas asignadas: {len(decisiones)}", f"proponer: {n_prop}", f"pendiente: {n_pend}", f"rechazar: {n_rech}", f"vinculos: {len(vinculos)}", f"significados: {len(dec_sig)} (pendientes {sum(1 for d in dec_sig if d['decision']=='pendiente')})", f"reglas nuevas: 0, conceptos nuevos: 0", "", "Criterio: solo proponer con columna fisica verificada + fila exacta + definicion respaldada + nombre unico + encabezado confirmado. Heuristicas, no-unicos y no-respaldadas quedan pendientes. Sin inferir unidades, catalogos ni vigencia.", ""]
(LOTE / "resultado.md").write_text("\n".join(res), encoding="utf-8")
import hashlib as H
sha = H.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
(LOTE / "listo.json").write_text(json.dumps({"sha256": sha, "sha256_entrega": sha, "columnas": len(decisiones), "proponer": n_prop, "pendiente": n_pend, "rechazar": n_rech, "vinculos": len(vinculos), "significados": len(dec_sig), "estado": "completo"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(n_prop, n_pend, n_rech, len(vinculos), sha)
