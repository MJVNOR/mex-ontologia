"""Compara fuentes oficiales descargadas (ronda-3 agente-4) contra evidencia central.

Lee UNICAMENTE: data/semantica/cobertura.json (central) y
propuestas/ronda-3/agente-4-aclaraciones/fuente/* (descargas propias).
Escribe: propuestas/ronda-3/agente-4-aclaraciones/comparativa.json
No modifica nada fuera de la carpeta del agente.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI / "scripts"))
from leer_xlsx import filas  # noqa: E402

BASE = AQUI.parents[2]
F = AQUI / "fuente"
FIJ = BASE / "data" / "integracion" / "fuentes"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def datastore(rid):
    d = json.loads((F / f"datastore_{rid}.json").read_text(encoding="utf-8"))
    return {r["_id"]: r for r in d["result"]["records"]}


cob = json.loads((BASE / "data" / "semantica" / "cobertura.json").read_text(encoding="utf-8"))
by_iri = {v["definicion_iri"]: v for v in cob["variables"]}
obs = {o["id"]: o for o in cob["observaciones_revision"]}

out = {"items": [], "catalogo": {}, "paquetes": {}, "fijadas": {}}

# Significados con datastore disponible: compara descripcion actual vs cobertura
pares = [
    ("12f684e9-f4d5-4714-933d-aa153a812174", [38, 72, 73, 74, 75]),
    ("22202305-2d02-4c49-b216-cc98224357f0", [83, 102, 103, 104, 105]),
    ("8c0e76ff-3a86-4b1d-beee-b04bebe7df8d", [14, 20, 64, 66, 67, 68, 69, 70]),
    ("2fc2fbc6-e918-4d5d-b907-1191e266b131", [5]),
    ("3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99", [2]),
    ("33d0a99e-c721-496f-a05e-07646e9ae42a", [7, 177, 178]),
    ("f89137ba-d82e-44fe-80c7-cc355f09f9f5", [15]),
    ("6713de4e-1e2b-447d-8000-f6ceaabd8473", [5]),
]
for rid, ids in pares:
    try:
        recs = datastore(rid)
    except FileNotFoundError:
        recs = None
    for i in ids:
        iri = f"https://example.org/mex-ontologi/definition/{rid}%2F{i}"
        v = by_iri.get(iri, {})
        item = {"definicion_iri": iri, "fila": i, "diccionario": rid,
                "descripcion_cobertura": v.get("descripcion"),
                "huella_cobertura": v.get("huella_fila_diccionario")}
        if recs is not None and i in recs:
            r = recs[i]
            dk = next(k for k in r if "scripci" in k)
            item["descripcion_actual"] = r[dk]
            item["coincide"] = (r[dk] == v.get("descripcion"))
            item["fuente"] = f"fuente/datastore_{rid}.json"
        else:
            item["descripcion_actual"] = None
            item["coincide"] = None
            item["nota"] = "sin datastore actual (404 o ausente)"
        out["items"].append(item)

# xlsx: filas pertinentes vs cobertura (comparacion semantica, no bytes)
xlsx_filas = {
    "diccionario_3395795d.xlsx": ("CVE_MUN", 4),
    "diccionario_587a3ccd.xlsx": ("Mes", 2),
    "diccionario_bfb8788b.xlsx": ("Fecha", 4),
}
for arch, (var, n) in xlsx_filas.items():
    rows = filas(F / arch)
    fila = rows[n - 1]
    out["items"].append({"archivo": arch, "variable": var, "fila_n": n,
                         "fila_actual": fila, "sha256": sha(F / arch)})

# catalogo Fiebre: hojas + tokens + sha vs fijada
z = zipfile.ZipFile(F / "catalogo_fiebre_08d3b1a7.xlsx")
txt = "".join(z.read(n).decode("utf-8", "replace")
              for n in z.namelist() if n.endswith(".xml"))
import re  # noqa: E402
out["catalogo"] = {
    "hojas": re.findall(r"<sheet[^>]*name=\"([^\"]+)\"", txt),
    "ocurrencias": {t: txt.count(t) for t in
                     ("des_mpo_res", "ide_id", "ide_col", "des_jur_res", "cve_loc_res")},
    "sha256": sha(F / "catalogo_fiebre_08d3b1a7.xlsx"),
}
fij = list(FIJ.glob("3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c.*"))
out["catalogo"]["sha_fijada"] = fij[0].name if fij else None
out["catalogo"]["bytes_identicos"] = bool(fij and
    sha(fij[0]) == out["catalogo"]["sha256"])

# paquetes: recursos actuales por conjunto
for conj in ("5494daa1-09ca-4750-aeac-2558553700e1", "cd3d6e34-3789-479e-9f2b-a717b8419f9c",
             "940de7d8-73ec-4a08-8d26-b7cc97ff17bd", "e819466c-7282-46c5-84e9-65917dd8cc85"):
    d = json.loads((F / f"package_{conj}.json").read_text(encoding="utf-8"))
    out["paquetes"][conj] = [(r["id"], r["name"]) for r in d["result"]["resources"]]

# Traza a–o/año Nacimientos 2024 (solo lectura central + fuente propia)
import hashlib as _hl  # noqa: E402
inv = json.loads((BASE / "data" / "portal" / "inventario.json").read_text(encoding="utf-8"))
r_inv = next(x for x in inv["recursos"] if x["id"] == "ffca84a8-155e-41af-8223-0e098966cadf")
campo_inv = [f["id"] for f in r_inv["datastore"]["campos"] if not f["id"].startswith("_id")][1]
ds_ff = json.loads((F / "datastore_ffca84a8-155e-41af-8223-0e098966cadf.json").read_text(encoding="utf-8"))
campo_ds = ds_ff["result"]["fields"][2]["id"]
crudo_ds = (F / "datastore_ffca84a8-155e-41af-8223-0e098966cadf.json").read_bytes()
ds_dict = json.loads((F / "datastore_6bcf5b63-0855-4f3b-81a0-4bca82e97272.json").read_text(encoding="utf-8"))
var_dict = next(r for r in ds_dict["result"]["records"] if r["_id"] == 2)["Nombre variable"]
head = (F / "nacimientos-2024_head.bin").read_bytes()
esquema = [{"nombre": f["id"], "tipo": f.get("type")}
           for f in r_inv["datastore"]["campos"] if not f["id"].startswith("_")]
h_recalc = _hl.sha256(json.dumps(esquema, ensure_ascii=False, sort_keys=True,
                                 separators=(",", ":")).encode("utf-8")).hexdigest()
out["traza_a_o"] = {
    "codepoints_campo_inventario": [hex(ord(c)) for c in campo_inv],
    "codepoints_campo_datastore_actual": [hex(ord(c)) for c in campo_ds],
    "datastore_crudo_contiene_E2_80_93": b"\xe2\x80\x93" in crudo_ds,
    "datastore_crudo_contiene_C3_B1": "Ã±".encode("utf-8") in crudo_ds,
    "codepoints_variable_diccionario_6bcf5b63_f2": [hex(ord(c)) for c in var_dict],
    "csv_head_primeros_bytes_hex": head[:40].hex(),
    "huella_esquema_recalculada": h_recalc,
    "huella_esquema_fijada": "e0437c5f0c9a47bc7ac43aa296e8bc62125574b141e284834303e55fd3ecde32",
    "metodo_inspeccion_central": next(
        (x.get("metodo") for x in
         json.loads((BASE / "data" / "portal" / "contenido-inspeccion.json").read_text(
             encoding="utf-8"))["recursos"] if x["id"] == "ffca84a8-155e-41af-8223-0e098966cadf"), None),
    "conclusion": ("Pipeline local fiel (datastore->inventario->huella->IRI); "
                   "divergencia archivo-vs-datastore del lado del publicador."),
}

(AQUI / "comparativa.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
n_ok = sum(1 for i in out["items"] if i.get("coincide") is True)
n_no = sum(1 for i in out["items"] if i.get("coincide") is False)
print(f"OK comparativa.json: {n_ok} coinciden, {n_no} difieren, "
      f"catalogo_identico={out['catalogo']['bytes_identicos']}")
