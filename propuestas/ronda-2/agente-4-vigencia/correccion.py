"""Correccion integrador: fechas reales/microsegundos, redaccion F3/F4, evidencia primaria CMPE."""
import json, datetime, pathlib
BASE = pathlib.Path(__file__).parent
CK = BASE / "evidencia" / "ckan"
mat = json.loads((BASE / "matriz-vigencia.json").read_text(encoding="utf-8"))
ckman = json.loads((BASE / "evidencia" / "ckan_manifiesto.json").read_text(encoding="utf-8"))
citas = json.loads((BASE / "evidencia" / "extractos" / "cmpe2016_citas.json").read_text(encoding="utf-8"))
pkgs = {}
for pid in ckman["paquetes"]:
    pkgs[pid] = json.loads((CK / f"package_{pid}.json").read_text(encoding="utf-8"))["result"]

gen = datetime.datetime.now(datetime.timezone.utc).isoformat()
mat["fecha_consulta_ckan_utc"] = ckman["fecha_utc"]
mat["fecha_generacion_utc"] = gen
mat.pop("fecha_utc", None)
mat["evidencia_ckan"]["fecha_utc"] = ckman["fecha_utc"]
mat["evidencia_externa_cmpe2016"] = {
    "archivo": "evidencia/externa/cmpe2016_inegi.pdf",
    "urls": citas["urls"], "bytes": citas["bytes"], "sha256": citas["sha256"],
    "fecha_descarga_utc": "2026-10-23T09:55:04.085665+00:00",
    "paginas": 202, "citas": "evidencia/extractos/cmpe2016_citas.json"}

SIN_ED = ("Archivo publicado en el conjunto, sin declaracion de edicion/version/fecha "
          "localizada en el alcance descrito (notas y extras CKAN + interior del xlsx)")
F4_BASE = "Recurso de catalogo registrado en CKAN el {c}; modificado {m}. Fecha de edicion y aplicacion historica no documentadas."

def f1(conjunto, recurso):
    p = pkgs[conjunto]
    r = next(x for x in p["resources"] if x["id"] == recurso)
    return {"paquete_created": p["metadata_created"], "paquete_modified": p["metadata_modified"],
            "catalogo_created": r["created"], "catalogo_last_modified": r["last_modified"],
            "catalogo_metadata_modified": r["metadata_modified"]}

P = {
 "V01": ("403912fd-5853-4e18-8256-f77206f855bd", "6d561451-ff08-45d6-b1af-285ff5f417b1"),
 "V02": ("e5aad52d-5760-481c-ba65-db0ba4a5315e", "aaf0c6c1-76a7-40ac-b542-1319d1bb2a5a"),
 "V03": ("e7a3d62f-4ace-479c-aa52-1c9e384dc429", "0e69d911-6ed3-4268-841b-0c4989e7cb45"),
 "V04": ("85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f", "af7a9aba-5a0e-4cf0-9b7d-5a3550e7907e"),
 "V05": ("ee8f639f-5e89-46ae-93b9-934b05fc6233", "f5060479-ee16-49b5-99d4-09aabef8042e"),
 "V06": ("5494daa1-09ca-4750-aeac-2558553700e1", "08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8"),
 "V07": ("5494daa1-09ca-4750-aeac-2558553700e1", "08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8"),
 "V08": ("5494daa1-09ca-4750-aeac-2558553700e1", "08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8"),
 "V09": ("0b5f5e16-2de3-4be1-811f-4b0976ed82d3", "de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0"),
 "V10": ("0b5f5e16-2de3-4be1-811f-4b0976ed82d3", "de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0"),
 "V11": ("943d0723-afbb-470a-8fe8-d62e8671de84", "d7c4b8b2-568f-4349-a1ed-23fa93189e83"),
 "V12": ("943d0723-afbb-470a-8fe8-d62e8671de84", "d7c4b8b2-568f-4349-a1ed-23fa93189e83"),
 "V13": ("93ca5e1c-702e-4e62-bc61-638907be184a", "36d3ac85-4327-41f5-9259-538a7723a0ae"),
 "V14": ("caf587a5-23ac-496b-85d4-6ceb1d615d78", "7f3aca28-4251-48b8-a759-69c992580744"),
 "V15": ("960ef0a9-73ed-4191-ae0b-b868d7e48292", "e0d2acc2-9841-4f6d-baea-88ba86710a7d"),
 "V16": ("960ef0a9-73ed-4191-ae0b-b868d7e48292", "e0d2acc2-9841-4f6d-baea-88ba86710a7d"),
}
CMPE_F3 = {
 "declaracion_interna": "Ninguna en Hoja1 (10 entradas 01-10, sin fecha ni version) ni en notas/extras CKAN",
 "edicion": "CMPE 2016 (Clasificacion mexicana de planes de estudio por campos de formacion academica 2016, educacion superior y media superior)",
 "edicion_acreditada_externa": True,
 "evidencia_primaria": {"archivo": "evidencia/externa/cmpe2016_inegi.pdf",
   "sha256": "66ba2fd24aa01d82684df52677b792e17fe55d38273d6325ff4f6f66a3ef714b",
   "localizadores": ["p.2: catalogacion (titulo, INEGI c2016, vii+206 p., ISBN 978-607-739-984-1)",
                     "p.8: segunda edicion, estructura de 8 a 10 campos"]},
 "nota": "La evidencia primaria acredita la edicion (F3). No acredita aplicabilidad a los periodos de estos conjuntos (F4), ni adopcion u obligatoriedad para UTH: sin evidencia directa."}

for r in mat["referencias"]:
    rid = r["id"]
    conj, rec = P[rid]
    resto = {k: v for k, v in r["f1_ckan"].items() if k not in
             ("paquete_created", "paquete_modified", "catalogo_created", "catalogo_last_modified")}
    r["f1_ckan"] = {**f1(conj, rec), **resto}
    c, m = r["f1_ckan"]["catalogo_created"], r["f1_ckan"]["catalogo_last_modified"]
    if rid in ("V01", "V02", "V03", "V04"):
        r["f3_edicion"] = dict(CMPE_F3)
        r["f4_aplicabilidad"] = (F4_BASE.format(c=c, m=m) +
            " Ninguna fuente (diccionario, nota CKAN, recurso) vincula CMPE 2016 con los periodos de este conjunto.")
        r["justificacion"] = "Edicion documentada con evidencia primaria (F3) pero sin vinculo temporal aplicable (F4 ausente)."
    else:
        r["f3_edicion"] = {"declaracion_interna": "Ninguna localizada en el alcance descrito" if rid not in ("V05",) else
            "Ninguna (hoja Catalogo_estatal: 10 presas, sin fecha ni version; hojas Municipios/Regiones no referenciadas)",
            "edicion": "No determinada; " + SIN_ED[0:1].lower() + SIN_ED[1:],
            "edicion_acreditada_externa": False}
        r["f4_aplicabilidad"] = F4_BASE.format(c=c, m=m)
        if rid == "V05":
            r["f4_aplicabilidad"] += (" Incluye 1 presa de Chihuahua (AGZCH): no es catalogo exclusivo de Sonora. "
                "Recurso 1960-1969 con URL vacia en CKAN: ese periodo declarado carece de evidencia descargable.")
        r["justificacion"] = "Sin edicion determinada (F3) ni vinculo a periodos (F4)."

(BASE / "matriz-vigencia.json").write_text(json.dumps(mat, ensure_ascii=False, indent=1), encoding="utf-8")
print("generacion:", gen, "| refs:", len(mat["referencias"]))
