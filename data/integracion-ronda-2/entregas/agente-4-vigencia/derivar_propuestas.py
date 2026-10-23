"""Deriva propuestas.json desde matriz-vigencia.json (sin duplicar a mano)."""
import json, pathlib
BASE = pathlib.Path(__file__).parent
mat = json.loads((BASE / "matriz-vigencia.json").read_text(encoding="utf-8"))
props = []
for r in mat["referencias"]:
    props.append({
        "id_propuesta": r["id"],
        "referencia_iri": r["referencia_iri"],
        "conjunto": r["conjunto"],
        "titulo_conjunto": r["titulo_conjunto"],
        "hoja_campo": r["hoja_campo"],
        "clasificacion": "vigencia_" + r["vigencia"],
        "facetas": {"f1_ckan": r["f1_ckan"], "f2_periodos_declarados": r["f2_periodos_declarados"],
                    "f3_edicion": r["f3_edicion"], "f4_aplicabilidad": r["f4_aplicabilidad"]},
        "justificacion": r["justificacion"],
        "limitaciones": r.get("limitaciones", []),
        "cambios_sugeridos_integrador": {
            "accion": "Registrar por referencia {vigencia: no_acreditada} con facetas F1-F4 y localizadores; no afirmar vigencia historica ni extender a otros conjuntos/periodos.",
        },
        "no_aplicado": True,
    })
out = {"generado_en_utc": mat["fecha_generacion_utc"],
       "fecha_consulta_ckan_utc": mat["fecha_consulta_ckan_utc"],
       "nota": "Propuestas, no aplicadas al grafo. Solo vigencia documental por periodo; no repiten comprobaciones de valores (agente 3) ni cotejo de localidades.",
       "total": len(props), "propuestas": props,
       "fuera_de_matriz": mat["fuera_de_matriz"]}
(BASE / "propuestas.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("propuestas:", len(props))
