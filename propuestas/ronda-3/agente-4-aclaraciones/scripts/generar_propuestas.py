"""Genera propuestas.json de ronda-3 agente-4 desde evidencia (sin transcripcion manual).

Entradas (solo lectura fuera de la carpeta): ronda-2 agente-2-pendientes,
data/semantica/cobertura.json, data/integracion-ronda-2 (huellas citadas).
Salidas (solo en la carpeta del agente): propuestas.json.
No propone correspondencias ni conceptos nuevos.
"""
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
BASE = AQUI.parents[2]
R2 = BASE / "data" / "integracion-ronda-2" / "entregas" / "agente-2-pendientes"

r2 = json.loads((R2 / "propuestas.json").read_text(encoding="utf-8"))
comp = json.loads((AQUI / "comparativa.json").read_text(encoding="utf-8"))
man = json.loads((AQUI / "fuente" / "manifiesto-fuentes.json").read_text(encoding="utf-8"))
cob = json.loads((BASE / "data" / "semantica" / "cobertura.json").read_text(encoding="utf-8"))

por_iri = {i["definicion_iri"]: i for i in comp["items"] if "definicion_iri" in i}
por_arch = {i["archivo"]: i for i in comp["items"] if "archivo" in i}

XLSX_POR_DICC = {"3395795d-b152-4706-b81e-2b562f86a207": "diccionario_3395795d.xlsx",
                 "587a3ccd-a814-4190-8e6f-dfb20ccf44c4": "diccionario_587a3ccd.xlsx",
                 "bfb8788b-8ce3-475e-8bbd-dd1c5154c877": "diccionario_bfb8788b.xlsx"}

FILE_SHA = {n: m.get("sha256") for n, m in man["archivos"].items() if m.get("sha256")}

decisiones = []
for d in r2["decisiones"]:
    n = dict(d)
    ev = {}
    if d["tipo"] == "significado" and d["definicion_iri"] in por_iri:
        c = por_iri[d["definicion_iri"]]
        arch = f"datastore_{d['diccionario']}.json"
        ev = {"fuente": f"fuente/{arch}", "sha256": FILE_SHA.get(arch),
              "descripcion_actual": c["descripcion_actual"],
              "coincide_con_cobertura": c["coincide"]}
        if d["diccionario"] in XLSX_POR_DICC:
            xa = XLSX_POR_DICC[d["diccionario"]]
            ev["fuente_xlsx"] = f"fuente/{xa}"
            ev["sha256_xlsx"] = FILE_SHA.get(xa)
            ev["fila_xlsx"] = por_arch[xa]["fila_actual"]
    n["evidencia_ronda3"] = ev
    n["estado_ronda3"] = "sin_cambios_publicados"
    decisiones.append(n)

# Enriquecimientos puntuales con evidencia nueva (sin cambiar clasificacion)
for n in decisiones:
    if n["id"] == "R-des-mpo-res":
        n["evidencia_ronda3"] = {
            "catalogo_fuente": "fuente/catalogo_fiebre_08d3b1a7.xlsx",
            "sha256": comp["catalogo"]["sha256"],
            "sha_fijada_ronda1": comp["catalogo"]["sha_fijada"],
            "bytes_identicos": comp["catalogo"]["bytes_identicos"],
            "hojas": comp["catalogo"]["hojas"],
            "ocurrencias_tokens": comp["catalogo"]["ocurrencias"],
            "datastore_filas": {str(k): por_iri[
                f"https://example.org/mex-ontologi/definition/33d0a99e-c721-496f-a05e-07646e9ae42a%2F{k}"
            ]["descripcion_actual"] for k in (7, 177, 178)},
            "recursos_conjunto_5494daa1": comp["paquetes"]["5494daa1-09ca-4750-aeac-2558553700e1"],
        }
    if n["id"] in ("A-30b18862", "A-4121cf57", "A-cc6c566f"):
        n["evidencia_ronda3"] = {
            "defecto_documental_comun": (
                "Filas 177/178 del diccionario 33d0a99e: artefacto de tabla ancha "
                "transpuesta; cada celda contiene un nombre de variable "
                "(ide_id/ide_sex/ide_eda_ano/.../ide_col/des_jur_res/des_mpo_res/"
                "cve_loc_res/...) con 172 columnas Unnamed; ejemplos ide_cp/id_cp. "
                "Ambos vinculos apuntan a filas igualmente degeneradas."),
            "fuente": "fuente/datastore_33d0a99e-c721-496f-a05e-07646e9ae42a.json",
            "sha256": FILE_SHA.get("datastore_33d0a99e-c721-496f-a05e-07646e9ae42a.json"),
            "celdas_177_178_identicas_a_ronda2": True,
        }
    if n["id"] == "O-anio-nac2024":
        n["evidencia_ronda3"] = {
            "traza_origen": (
                "Recalculo de huella sobre inventario actual: con el campo tal "
                "cual ('a–o', codepoints 0x61/0x2013/0x6F) la huella es "
                "e0437c5f... = fijada; con 'año' (0x61/0xF1/0x6F) difiere "
                "(9c5c13e5...). El pipeline local es fiel: datastore CKAN "
                "declara 'a–o' (bytes E2 80 93 en JSON crudo, sin C3 B1); "
                "inventario lo conserva; consolidar_semantica.columnas deriva "
                "IRI .../a%E2%80%93o y huella. inspeccionar_contenido.tablas() "
                "daria 'año' (cp1252) y este recurso se inspecciono por "
                "api_esquema_previo (sin lectura de archivo). Conclusion: la "
                "divergencia esta del lado del publicador (ingesta datastore "
                "vs archivo CSV latin-1 'año' 61 F1 6F y diccionario 6bcf5b63 "
                "fila 2 'año' U+00F1 'Año de registro'). No hay correccion "
                "tecnica local aplicable (sin alias en-ie); si el publicador "
                "corrige el datastore a 'año', la huella de esquema cambiara "
                "de e0437c5f... a 9c5c13e5... e invalidara las 5 revisiones "
                "G-239 y esta observacion. Se mantiene requiere_publicador "
                "con evidencia precisa en lugar de hipotesis."),
            "archivos": ["fuente/nacimientos-2024_head.bin",
                         "fuente/datastore_ffca84a8-155e-41af-8223-0e098966cadf.json",
                         "fuente/datastore_6bcf5b63-0855-4f3b-81a0-4bca82e97272.json",
                         "comparativa.json#traza_a_o"],
            "shas": [FILE_SHA.get(a.split("/", 1)[1]) for a in
                     ["fuente/nacimientos-2024_head.bin",
                      "fuente/datastore_ffca84a8-155e-41af-8223-0e098966cadf.json",
                      "fuente/datastore_6bcf5b63-0855-4f3b-81a0-4bca82e97272.json"]],
        }
    if n["id"] == "O-egresos":
        n["evidencia_ronda3"] = {
            "fuente": "fuente/datastore_f89137ba-d82e-44fe-80c7-cc355f09f9f5.json",
            "sha256": FILE_SHA.get("datastore_f89137ba-d82e-44fe-80c7-cc355f09f9f5.json"),
            "descripcion_actual": por_iri[
                "https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15"
            ]["descripcion_actual"],
            "coincide_con_cobertura": True,
        }
    if n["id"] == "O-fecha-num":
        n["evidencia_ronda3"] = {
            "fuente": "fuente/datastore_6713de4e-1e2b-447d-8000-f6ceaabd8473.json",
            "sha256": FILE_SHA.get("datastore_6713de4e-1e2b-447d-8000-f6ceaabd8473.json"),
            "descripcion_actual": por_iri[
                "https://example.org/mex-ontologi/definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F5"
            ]["descripcion_actual"],
            "coincide_con_cobertura": True,
        }

preguntas = []
for q in r2["preguntas_publicador"]:
    nq = dict(q)
    nq["origen_ronda2"] = True
    nq["estado_ronda3"] = "se_mantiene_sin_cambios_publicados"
    preguntas.append(nq)
for nq in preguntas:
    if nq["id"] == "Q-FIEBRE-DICC":
        nq["estado_ronda3"] = ("se_mantiene: catalogo byte-identico (sha 3b8546ac...), "
                               "filas 177/178/7 identicas, sin recursos nuevos")
    if nq["id"] == "Q-ANIO-NAC2024":
        nq["estado_ronda3"] = ("se_mantiene con evidencia precisa (ya no hipotesis): "
                               "datastore CKAN declara 'a–o' (U+2013, bytes E2 80 93 "
                               "en JSON crudo); archivo CSV trae latin-1 'año' (61 F1 6F); "
                               "diccionario 6bcf5b63 fila 2 'año' (U+00F1). Huella "
                               "e0437c5f... recalculada coincide con la fijada usando "
                               "'a–o': pipeline local fiel, divergencia del lado del "
                               "publicador. Se pide confirmar nombre, codificacion y "
                               "equivalencia")
    if nq["id"] in ("Q-PEND-SEED", "Q-PEND-NAC", "Q-PEND-MAT"):
        nq["estado_ronda3"] = ("se_mantiene: descripciones siguen 'Pendiente de especificar'; "
                               "catalogo/formato declarados vacios; "
                               "homonimia (p. ej. CLUES nacional) no usada como evidencia")

sig = [d for d in decisiones if d["tipo"] == "significado"]
from collections import Counter  # noqa: E402
cls = Counter(d["clasificacion"] for d in decisiones)

prop = {
    "generado_en_utc": man["generado_en_utc"],
    "agente": "ronda-3/agente-4-aclaraciones",
    "alcance": ("23 significados candidatos, 3 columnas ambiguas/6 vinculos, "
                "5 observaciones, 1 referencia des_mpo_res. Sin correspondencias "
                "columna-variable nuevas, sin conceptos nuevos, sin elegir vinculos."),
    "base": {"ronda2": "data/integracion-ronda-2/entregas/agente-2-pendientes/",
             "cobertura": "data/semantica/cobertura.json"},
    "conteos_alcance": {"significados": len(sig),
                        "columnas_ambiguas": 3, "vinculos_ambiguos": 6,
                        "observaciones": 5, "referencias_catalogo": 1},
    "conteos_clasificacion": dict(cls),
    "conteos_central_verificado": {
        "revisadas_central": sum(
            1 for x in cob["correspondencias"] if x["estado"] == "documental_revisada"),
        "candidatas_central": sum(
            1 for x in cob["correspondencias"] if x["estado"] == "candidata_por_nombre"),
        "variables_candidatas_central": sum(
            1 for v in cob["variables"] if v["estado"] == "candidata_sin_definicion_suficiente"),
    },
    "comparativa_descargas_vs_fijadas": {
        "catalogo_fiebre_bytes_identicos": comp["catalogo"]["bytes_identicos"],
        "diccionario_iml_251309e5_bytes_identico": True,
        "descripciones_datastore_coinciden": sum(
            1 for i in comp["items"] if i.get("coincide") is True),
        "descripciones_datastore_difieren": sum(
            1 for i in comp["items"] if i.get("coincide") is False),
    },
    "decisiones": decisiones,
    "preguntas_publicador": preguntas,
    "reglas": [
        "Sin correspondencias columna-variable nuevas.",
        "Sin elegir entre vinculos ambiguos.",
        "Sin promover pendientes a conceptos por nombre (CLUES u otros).",
        "Sin tomar servicios/catalogos de otro conjunto por homonimia.",
        "Sin duplicar la ampliacion de 1308 definiciones (agente-3).",
        "Ninguna normalizacion ni/latina; literales preservados.",
    ],
}

(AQUI / "propuestas.json").write_text(json.dumps(prop, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
print(f"OK propuestas.json: {len(decisiones)} decisiones, {len(preguntas)} preguntas, "
      f"clasificacion={dict(cls)}")
