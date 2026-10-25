"""Fase adicional lote-6: integra 85 columnas con dependencia explicita de regla nueva.
Conserva EXACTAMENTE reglas, conceptos_nuevos y decisiones_significados de entrega.json."""
import hashlib, json, sys, unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("C:/Users/marti/Documents/MEX-Ontologi")
sys.path.insert(0, str(ROOT / "scripts"))
import consolidar_semantica as CS
STAGE = ROOT / "propuestas/pendientes-muse-r4"
LOTE = STAGE / "lote-6"

def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def norm(s):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())

entrega = json.loads((LOTE / "entrega.json").read_text(encoding="utf-8"))
asig = json.loads((LOTE / "asignacion.json").read_text(encoding="utf-8"))
adic = json.loads((LOTE / "asignacion-adicional.json").read_text(encoding="utf-8"))
assert len(adic["columnas"]) == 85, len(adic["columnas"])
inv = json.loads((ROOT / "data/portal/inventario.json").read_text(encoding="utf-8"))
insp = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
cob = json.loads((STAGE / "fuentes/data/semantica/cobertura.json").read_text(encoding="utf-8"))
sem_live = json.loads((ROOT / "ontologia/semantica.json").read_text(encoding="utf-8"))

orig_ids = [c["columna"] for c in asig["columnas"]]
new_ids = [c["columna"] for c in adic["columnas"]]
assert len(set(orig_ids)) == 519 and len(set(new_ids)) == 85 and not (set(orig_ids) & set(new_ids)), "IRIs no unicos entre fases"
assert {d["columna"] for d in entrega["decisiones_columnas"]} == set(orig_ids), "entrega original alterada"

# reglas y significados intactos: mapa definicion -> (concepto, regla)
rule_by_def = {}
for r in entrega["reglas"]:
    assert len(r["definiciones"]) == 1
    rule_by_def[r["definiciones"][0]] = (r["concepto"], r["id"])
sig_by_def = {d["definicion_iri"]: d for d in entrega["decisiones_significados"]}
assert len(entrega["reglas"]) == 30 and len(entrega["conceptos_nuevos"]) == 27 and len(sig_by_def) == 66

resources = {r["id"]: r for r in inv["recursos"]}
insp_by = {r["id"]: r for r in insp["recursos"]}
dcs = {d["definicion_iri"]: d for d in asig["definiciones_contexto"]}
cov_by_def = {v["definicion_iri"]: v for v in cob["variables"] if v.get("definicion_iri")}
rev_cols = {(v["recurso"], v["campo"], v["columna"]) for v in sem_live["vinculos_documentales_revisados"]}
obs = CS.columnas(inv, insp, "https://example.org/mex-ontologi/")
obs_by = {(o["recurso"], o["campo"], o["iri"]): o for o in obs}
NAME_KEYS = {"nombre variable", "nombre de variable", "variable", "nombre campo", "nombre del campo"}
DESC_KEYS = {"descripcion", "definicion"}

def parse_col(iri):
    if "/file-column/" in iri:
        dec = unquote(iri.split("/file-column/", 1)[1])
        rid, hoja, pos = dec.rsplit("/", 2)
        return ("file", rid, hoja, int(pos))
    dec = unquote(iri.split("/column/", 1)[1])
    rid, campo = dec.rsplit("/", 1)
    return ("datastore", rid, campo, None)

dec_ad, vinc_ad, pend_ad = [], [], []
for c in adic["columnas"]:
    col_iri, recurso, campo = c["columna"], c["recurso"], c["campo"]
    definicion_iri = c["definiciones_por_nombre"][0]
    ev, motivo, decision = [], "", "pendiente"
    vinc = None
    try:
        assert definicion_iri in rule_by_def, f"definicion {definicion_iri} sin regla nueva propia"
        concepto, regla_id = rule_by_def[definicion_iri]
        drow = dcs.get(definicion_iri) or cov_by_def.get(definicion_iri)
        assert drow, "sin contexto documental"
        dec = unquote(definicion_iri)
        dic = dec.split("/definition/", 1)[1].rsplit("/", 1)[0]
        didx = int(dec.rsplit("/", 1)[1])
        di = insp_by.get(dic)
        assert di and di.get("ok") and "definiciones" in di
        row = di["definiciones"][didx - 1]
        vname = next((str(v).strip() for k, v in row.items() if norm(k) in NAME_KEYS and v is not None and str(v).strip()), "")
        desc = next((str(v).strip() for k, v in row.items() if norm(k) in DESC_KEYS and v is not None and str(v).strip()), "")
        h_fila = huella(row)
        assert h_fila == cov_by_def[definicion_iri]["huella_fila_diccionario"], "huella fila distinta de cobertura"
        ev.append(f"data/portal/contenido-inspeccion.json diccionario {dic} fila {didx} variable {vname!r} huella_fila={h_fila}")
        kind, rid, hoja, pos = parse_col(col_iri)
        assert rid == recurso
        if kind == "file":
            ri = insp_by.get(recurso)
            assert ri and ri.get("ok")
            tablas = [t for t in ri.get("tablas", []) if t["hoja"] == hoja]
            assert len(tablas) == 1, f"hoja {hoja} no unica"
            tabla = tablas[0]
            h_esc = huella(tabla)
            flds = [f for f in tabla["campos"] if f["posicion_original"] == pos]
            assert flds, f"posicion {pos} ausente"
            assert norm(flds[0]["id"]) == norm(campo), f"campo {campo!r} != observado {flds[0]['id']!r}"
            assert norm(vname) == norm(campo), f"variable {vname!r} != campo {campo!r}"
            assert sum(1 for f in tabla["campos"] if norm(f["id"]) == norm(campo)) == 1, "nombre no unico en tabla"
            ev.append(f"esquema recurso {recurso} hoja {hoja} pos {pos} = {flds[0]['id']!r} fila_encabezado={tabla.get('fila_encabezado')}")
        else:
            rinv = resources.get(recurso)
            assert rinv and rinv.get("datastore", {}).get("ok")
            flds = [f for f in rinv["datastore"]["campos"] if not f["id"].startswith("_")]
            h_esc = huella([{"nombre": f["id"], "tipo": f.get("type")} for f in flds])
            assert any(norm(f["id"]) == norm(campo) for f in flds), "campo ausente en datastore"
            assert norm(vname) == norm(campo), f"variable {vname!r} != campo {campo!r}"
            assert sum(1 for f in flds if norm(f["id"]) == norm(campo)) == 1, "nombre no unico en datastore"
            ev.append(f"datastore recurso {recurso} campo {campo!r} verificado")
        o = obs_by.get((recurso, campo, col_iri))
        assert o is not None and o["huella_esquema"] == h_esc, "consolidar_semantica.columnas no reproduce columna/huella"
        ev.append(f"consolidar_semantica.columnas verifica huella_esquema={h_esc} nombre_unico={o['nombre_unico']}")
        assert o["nombre_unico"], "nombre no unico segun consolidar_semantica.columnas"
        assert (recurso, campo, col_iri) not in rev_cols, "ya revisada"
        assert desc.strip() and "pendiente de especificar" not in norm(desc), "descripcion sin respaldo"
        assert cov_by_def[definicion_iri]["conjunto"] == c["conjunto"], "conjunto distinto"
        decision = "proponer"
        motivo = f"columna fisica verificada + fila exacta + regla nueva {regla_id} con literal {desc!r}; dependencia explicita"
        vinc = {"recurso": recurso, "campo": campo, "columna": col_iri, "diccionario": dic,
                "concepto": concepto, "descripcion": desc, "huella_esquema": h_esc,
                "huella_fila_diccionario": h_fila,
                "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto: nombre, contexto, descripcion literal y representacion. Alcance de interpretacion documental; no se validan valores ni se confirma pertenencia a catalogos.",
                "dependencia": f"significado nuevo {definicion_iri} (regla {regla_id})"}
    except AssertionError as e:
        motivo = f"evidencia incompleta: {e}"
    except Exception as e:
        motivo = f"evidencia incompleta: {type(e).__name__} {e}"
    d = {"columna": col_iri, "recurso": recurso, "campo": campo, "decision": decision, "motivo": motivo, "evidencia": ev}
    if decision == "proponer":
        d["definicion_iri"] = definicion_iri
        vinc_ad.append(vinc)
    else:
        pend_ad.append({"columna": col_iri, "campo": campo, "recurso": recurso, "motivo": motivo, "evidencia": ev})
    dec_ad.append(d)

entrega["decisiones_columnas"].extend(dec_ad)
entrega["vinculos"].extend(vinc_ad)
# reglas, conceptos_nuevos y decisiones_significados intactos por construccion
(LOTE / "entrega.json").write_text(json.dumps(entrega, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

pend = json.loads((LOTE / "pendientes.json").read_text(encoding="utf-8"))
pend["pendientes_columnas"].extend(pend_ad)
pend["conteo_columnas"] = len(pend["pendientes_columnas"])
(LOTE / "pendientes.json").write_text(json.dumps(pend, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

n_prop = sum(1 for d in entrega["decisiones_columnas"] if d["decision"] == "proponer")
n_pend = sum(1 for d in entrega["decisiones_columnas"] if d["decision"] == "pendiente")
n_rech = sum(1 for d in entrega["decisiones_columnas"] if d["decision"] == "rechazar")
n_sig_prop = sum(1 for d in entrega["decisiones_significados"] if d["decision"] == "proponer")
res = ["# Resultado lote-6 ronda 4", "", f"Columnas asignadas: {len(entrega['decisiones_columnas'])} (base 519 + adicionales 85)",
 f"proponer: {n_prop}", f"pendiente: {n_pend}", f"rechazar: {n_rech}", f"vinculos: {len(entrega['vinculos'])}",
 f"significados: {len(entrega['decisiones_significados'])} (proponer {n_sig_prop}, pendientes {len(entrega['decisiones_significados']) - n_sig_prop})",
 f"reglas nuevas: {len(entrega['reglas'])}, conceptos nuevos: {len(entrega['conceptos_nuevos'])}", "",
 "Criterio: proponer con columna fisica verificada (consolidar_semantica.columnas + huella) + fila exacta + literal especifico. Respaldadas reutilizan concepto vigente; adicionales dependen explicitamente de las 30 reglas nuevas. Descripciones vacias/Pendiente de especificar quedan pendientes. Sin inferir unidades, catalogos ni vigencia.", ""]
(LOTE / "resultado.md").write_text("\n".join(res), encoding="utf-8")
sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
(LOTE / "listo.json").write_text(json.dumps({"sha256_entrega": sha, "columnas": len(entrega["decisiones_columnas"]),
 "proponer": n_prop, "pendiente": n_pend, "rechazar": n_rech, "vinculos": len(entrega["vinculos"]),
 "significados": len(entrega["decisiones_significados"]), "estado": "completo"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(n_prop, n_pend, n_rech, len(entrega["vinculos"]), sha)
