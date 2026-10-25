"""Fase adicional lote-1: verifica columnas derivadas de reglas r4 propias."""
import hashlib, json, sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path("C:/Users/marti/Documents/MEX-Ontologi")
STAGE = ROOT / "propuestas/pendientes-muse-r4"
LOTE = STAGE / "lote-1"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(STAGE / "integrador"))
from consolidar_semantica import huella, interpretacion
from integrar_contenido import clave
import comprobar as CTRL

ad = json.loads((LOTE / "asignacion-adicional.json").read_text(encoding="utf-8"))
assert hashlib.sha256((LOTE / "asignacion-adicional.json").read_bytes()).hexdigest() == \
    json.loads((STAGE / "integrador/asignaciones-adicionales.json").read_text(encoding="utf-8"))["columnas_adicionales"]["lote-1"]["sha256"], "SHA adicional"
ent = json.loads((LOTE / "entrega.json").read_text(encoding="utf-8"))
reglas_fijas, conceptos_fijos, sig_fijos = ent["reglas"], ent["conceptos_nuevos"], ent["decisiones_significados"]
prop = json.loads((STAGE / "integrador/semantica-propuesta.json").read_text(encoding="utf-8"))
cob = json.loads((STAGE / "fuentes/data/semantica/cobertura.json").read_text(encoding="utf-8"))
cov = {v["definicion_iri"]: v for v in cob["variables"] if v.get("definicion_iri")}
insp = json.loads((ROOT / "data/portal/contenido-inspeccion.json").read_text(encoding="utf-8"))
ib = {r["id"]: r for r in insp["recursos"]}
names = {}
for vv in cov.values():
    names[(vv["conjunto"], clave(vv["variable"]))] = names.get((vv["conjunto"], clave(vv["variable"])), 0) + 1
mi_meta = {r["definiciones"][0]: (r["concepto"], r["id"]) for r in reglas_fijas}
existentes = {d["columna"] for d in ent["decisiones_columnas"]}
assert not ({c["columna"] for c in ad["columnas"]} & existentes), "solape de IRIs"
assert len({c["columna"] for c in ad["columnas"]}) == len(ad["columnas"]), "duplicadas en adicional"

def tabla_de(col_iri, recurso):
    tail = col_iri.split("/file-column/", 1)[1]
    rid, hoja, pos = unquote(tail).rsplit("/", 2)
    assert rid == recurso
    ri = ib[rid]
    assert ri["ok"]
    ts = [t for t in ri["tablas"] if t["hoja"] == hoja]
    assert len(ts) == 1, hoja
    return ts[0], int(pos)

nuevas_dec, nuevos_vinc, pend_det = [], [], []
for c in ad["columnas"]:
    col_iri, recurso, campo = c["columna"], c["recurso"], c["campo"]
    dest = c["definiciones_por_nombre"][0]
    ev = []
    try:
        assert dest in mi_meta, "destino no es regla propia proponer: " + dest
        concepto, rid = mi_meta[dest]
        v = cov[dest]
        tabla, pos = tabla_de(col_iri, recurso)
        h_esc = huella(tabla)
        ev += ["data/portal/contenido-inspeccion.json recurso %s hoja %s" % (recurso, tabla["hoja"]),
               "huella_esquema=" + h_esc]
        obs = [f for f in tabla["campos"] if f["posicion_original"] == pos]
        assert obs, "posicion ausente"
        assert clave(obs[0]["id"]) == clave(campo), "campo fisico %r != %r" % (obs[0]["id"], campo)
        ev.append("campo fisico pos %d = %r" % (pos, obs[0]["id"]))
        n_ig = sum(1 for f in tabla["campos"] if clave(f["id"]) == clave(campo))
        assert n_ig == 1, "nombre no unico en tabla"
        assert names[(c["conjunto"], clave(v["variable"]))] == 1, "variable no unica en diccionario"
        assert c["conjunto"] == v["conjunto"], "conjunto distinto"
        act = interpretacion(v["variable"], v["descripcion"], v["conjunto"], prop, v["diccionario"], v["definicion_iri"])
        assert act["estado"] == "respaldada_por_definicion" and act["concepto"] == concepto, "destino no respaldado: " + repr(act)
        nuevas_dec.append({"columna": col_iri, "recurso": recurso, "campo": campo, "decision": "proponer",
            "definicion_iri": dest, "motivo": "columna fisica verificada + destino respaldado por regla propia " + rid + "; alcance documental.",
            "evidencia": ev + ["regla " + rid + " concepto " + concepto, "huella_fila=" + v["huella_fila_diccionario"]]})
        nuevos_vinc.append({"recurso": recurso, "campo": campo, "columna": col_iri, "diccionario": v["diccionario"],
            "concepto": concepto, "descripcion": v["descripcion"], "huella_esquema": h_esc,
            "huella_fila_diccionario": v["huella_fila_diccionario"],
            "criterio": "Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo conjunto. Alcance documental; sin sistema verificado ni equivalencias.",
            "dependencia": dest})
    except AssertionError as e:
        nuevas_dec.append({"columna": col_iri, "recurso": recurso, "campo": campo, "decision": "pendiente",
            "motivo": "falta respaldo fisico: " + str(e), "evidencia": ev or ["sin evidencia verificable"]})
        pend_det.append(col_iri)

assert ent["reglas"] == reglas_fijas and ent["conceptos_nuevos"] == conceptos_fijos and ent["decisiones_significados"] == sig_fijos
ent["decisiones_columnas"].extend(nuevas_dec)
ent["vinculos"].extend(nuevos_vinc)
(LOTE / "entrega.json").write_text(json.dumps(ent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

pend_cols = [d for d in ent["decisiones_columnas"] if d["decision"] != "proponer"]
pend_sig = [d for d in sig_fijos if d["decision"] != "proponer"]
(LOTE / "pendientes.json").write_text(json.dumps({"pendientes_columnas": pend_cols,
    "pendientes_significados": pend_sig, "conteo_columnas": len(pend_cols), "conteo_significados": len(pend_sig)},
    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
n_prop = sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "proponer")
(LOTE / "resultado.md").write_text("\n".join([
 "# Resultado lote-1 ronda 4 (fase adicional)", "",
 "Columnas asignadas: %d (originales 702 + adicionales %d)" % (len(ent["decisiones_columnas"]), len(ad["columnas"])),
 "proponer: %d" % n_prop, "pendiente: %d" % len(pend_cols),
 "rechazar: %d" % sum(1 for d in ent["decisiones_columnas"] if d["decision"] == "rechazar"),
 "vinculos: %d (%d con dependencia explicita)" % (len(ent["vinculos"]), sum(1 for x in ent["vinculos"] if "dependencia" in x)),
 "significados: %d (proponer 18, pendientes 2)" % len(sig_fijos),
 "reglas nuevas: %d, conceptos nuevos: %d (inalterados)" % (len(reglas_fijas), len(conceptos_fijos)), "",
 "Criterio adicional: columna fisica (archivo/hoja/posicion) + definicion exacta + huella verificadas; interpretacion contra semantica-propuesta.json; dependencia explicita de regla propia. Sin homologaciones.", ""]), encoding="utf-8")
sha = hashlib.sha256((LOTE / "entrega.json").read_bytes()).hexdigest()
(LOTE / "listo.json").write_text(json.dumps({"sha256": sha, "sha256_entrega": sha, "columnas": len(ent["decisiones_columnas"]),
    "proponer": n_prop, "vinculos": len(ent["vinculos"]), "significados": len(sig_fijos),
    "reglas": len(reglas_fijas), "estado": "completo-fase-adicional"}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("adicionales", len(ad["columnas"]), "proponer", sum(1 for d in nuevas_dec if d["decision"] == "proponer"),
      "pend", len(pend_det), "total_col", len(ent["decisiones_columnas"]), sha)

res = CTRL.check("lote-1")
print("comprobar:", json.dumps(res, ensure_ascii=True)[:600])
assert res["valido"], res["errores"]
