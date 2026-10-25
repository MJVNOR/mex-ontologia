"""A1-911: comprobaciones reproducibles del par 911 (solo lectura local).
Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v001/scripts/comprobar_a1_911.py
No descarga, no regenera grafo, no toca Studio. Todo numero sale de estos archivos:
data/portal/inventario.json, data/portal/inspecciones/*.json,
data/portal/contenido-inspeccion.json, data/portal/oportunidades-cruce.json,
data/portal/lote-cruces/validacion-lote.json, ontologia/semantica.json.
"""
import json

RAIZ = r"C:\Users\marti\Documents\MEX-Ontologi"
A = "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f"
B = "923b485b-515e-4fb9-a4ac-cccbeb88cc92"
PID = A + "--" + B
RIDS = ["0df8592f-bb3d-466c-aec3-6cbc91253be0", "54285a13-3a2a-4e47-b0af-e855861f5347",
        "1a95d734-2f0e-4781-8831-77dcfcbe70f8", "6ce17dd1-5716-44e9-bc5f-603c0925afe6",
        "943e2919-6a8b-4776-ac4f-c3d6b02bb94e", "7922b8c8-db09-4172-ad7f-31b0ba0c68e3"]


def j(rel):
    with open(RAIZ + "\\" + rel.replace("/", "\\"), encoding="utf-8") as f:
        return json.load(f)


out = {"par": PID}
inv = j("data/portal/inventario.json")
recs = [r for r in inv["recursos"] if r.get("conjunto_id") in (A, B)]
out["recursos_inventario"] = len(recs)
out["recursos"] = {r["id"]: {"conjunto": r["conjunto"], "nombre": r["nombre"],
                             "formato": r["formato"]} for r in recs}
assert len(recs) == 6, len(recs)

esq = {}
for rid in RIDS:
    d = j("data/portal/inspecciones/%s.json" % rid)
    hojas = [(t.get("hoja"), [c["id"] for c in t["campos"]]) for t in d["tablas"]]
    esq[rid] = {"hoja": hojas[0][0], "columnas": hojas[0][1],
                "sha": d["sha256_fragmento_o_archivo"], "bytes": d["bytes_leidos"],
                "metodo": d["tablas"][0]["metodo_encabezado"]}
out["esquemas"] = esq
assert esq[RIDS[0]]["columnas"] == ["FECHA", "HORA", "MOTIVO NO PROCEDENTE"]
assert esq[RIDS[1]]["columnas"] == ["FECHA", "HORA", "MUNICIPIO", "LOCALIDAD",
                                    "COLONIA", "SEXO REPORTANTE", "CLASIFICACION"]
assert esq[RIDS[1]]["sha"] == esq[RIDS[3]]["sha"]  # duplicado byte-identico Q1
assert esq[RIDS[1]]["hoja"] == "LLAMADAS PROCEDENTES 911"
assert esq[RIDS[0]]["hoja"] == "LLAMADA IMPROCEDENTES 911"
out["duplicado_q1_mismo_sha"] = esq[RIDS[1]]["sha"]

dic_a = j("data/portal/inspecciones/1a95d734-2f0e-4781-8831-77dcfcbe70f8.json")
dic_b = j("data/portal/inspecciones/7922b8c8-db09-4172-ad7f-31b0ba0c68e3.json")
assert dic_a["sha256_fragmento_o_archivo"] == dic_b["sha256_fragmento_o_archivo"]
out["diccionarios_mismo_sha"] = dic_a["sha256_fragmento_o_archivo"]
out["diccionario_vars"] = [d["Nombre variable"] for d in dic_a["definiciones"]]
assert len(dic_a["definiciones"]) == 7
assert "motivo no procedente" not in [v.lower() for v in out["diccionario_vars"]]
out["diccionario_unidades"] = list({d["Unidad de medida"] for d in dic_a["definiciones"]})

oc = j("data/portal/oportunidades-cruce.json")
par = next(p for p in oc["pares"] if p["id"] == PID)
out["oportunidad"] = {"estado": par["estado"], "alcance_ejecucion": par["alcance_ejecucion"],
                      "familias": par["familias_compartidas"], "pendientes": par["pendientes"],
                      "anios_nombres": par["anios_coincidentes_solo_en_nombres"]}
assert par["estado"] == "candidata_por_validar" and par["alcance_ejecucion"] == "No ejecutado"

vl = j("data/portal/lote-cruces/validacion-lote.json")
pvl = next(p for p in vl["pares"] if p.get("id") == PID)
out["lote_decision"] = pvl["decision"]
assert pvl["decision"] == "requiere_revision" and pvl["ejecuciones"] == []
for lado in ("a", "b"):
    m = pvl["diagnostico_muestras"][lado]
    out["muestra_" + lado] = {"recurso": m["recurso_id"], "filas": m["filas_muestra"],
                              "hoja": m["hoja"], "alcance": m["alcance"],
                              "sha": m["evidencia_archivo"]["sha256_fragmento_o_archivo"]}
assert out["muestra_a"]["filas"] == 29 and out["muestra_b"]["filas"] == 29
assert "0df8592f" not in json.dumps(pvl["diagnostico_muestras"])  # improcedentes Q2 sin muestra
out["comparacion_muestral"] = [
    {"familia": c["familia"], "distintos_a": c["valores_distintos_a"],
     "distintos_b": c["valores_distintos_b"],
     "coincidencias_exactas_muestra": c["coincidencias_exactas_muestra"],
     "interpretacion": c["interpretacion"]} for c in pvl["comparacion_muestras"]]

sem = j("ontologia/semantica.json")
vinc = [v for v in sem["vinculos_documentales_revisados"]
        if v.get("recurso") in RIDS]
out["vinculos_semanticos_locales"] = len(vinc)
mun = [v for v in vinc if v.get("campo") == "MUNICIPIO"]
out["municipio_concepto"] = list({v["concepto"] for v in mun})
out["municipio_recursos_con_vinculo"] = sorted({v["recurso"] for v in mun})
assert "0df8592f-bb3d-466c-aec3-6cbc91253be0" not in out["municipio_recursos_con_vinculo"]

print(json.dumps(out, ensure_ascii=False, indent=1))
print("A1-911: comprobaciones OK (bloqueo documentado, sin join).")
