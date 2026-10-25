"""Verificacion local X-anomalias R8 (solo lectura fuera de este directorio).
Recomputa SHA256 reales y revalida por codigo cada afirmacion acotada.
Uso: uv run python propuestas/ronda-8-paralela/ejecucion-20261024/X-anomalias/v001/verifica.py
"""
import csv
import hashlib
import json
import os
import re
import zipfile

RAIZ = r"C:\Users\marti\Documents\MEX-Ontologi"


def sha(ruta):
    with open(os.path.join(RAIZ, ruta), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


ESPERADOS = {
    "propuestas/cierre-brechas-post-r6/anomalias/evidencia/diccionario_ricket_1_2026-10-24.csv":
        "2c8ce131bf0e71fe812605f0f95381acaec9c5534e1bed8f05ff1895bf2fcd1c",
    "propuestas/cierre-brechas-post-r6/anomalias/evidencia/ckan-package_5494daa1_2026-10-24.json":
        "e751fe481af047f3ffa6facc57c9d04952e5f874186be2d2fb4a6ae20f9a0154",
    "data/portal/contenido-inspeccion.json":
        "61861aab5bc2b334699c4d78f611a0e2d650c4649bd791927f9095c2ac785efb",
    "propuestas/cierre-brechas-post-r6/anomalias/evidencia/busquedas_2026-10-24.json":
        "62a94db34f34f5d47f39a385352060deeae3fd90aa74883617407f3f3009fa6d",
    "data/integracion/fuentes/3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c.xlsx":
        "3b8546acad7482825755e46a1a619a4838721f8480b94baaef3c755ba293db9c",
}

fallos = []
for ruta, esp in ESPERADOS.items():
    real = sha(ruta)
    estado = "OK " if real == esp else "FALLO"
    print(estado, real, ruta)
    if real != esp:
        fallos.append(ruta)

with open(os.path.join(RAIZ, ESPERADOS and list(ESPERADOS)[0]), encoding="utf-8") as f:
    filas = list(csv.reader(f))
assert len(filas) - 1 == 178, len(filas)
f7 = filas[7]
assert f7[0] == "des_mpo_res" and f7[1] == "Texto" and f7[6] == "" and f7[9] == "Hermosillo", f7[:10]
f177, f178 = filas[177], filas[178]
assert f177[0] == "ide_id" and f177[5] == "des_jur_res" and f177[6] == "des_mpo_res", f177[:10]
assert f178[0] == "ide_id" and f178[6] == "des_mpo_res", f178[:10]
assert f177[9] == "ide_cp" and f178[9] == "id_cp", (f177[9], f178[9])
print("OK  csv: 178 filas; fila7 texto libre sin catalogo; 177/178 corruptas (ide_cp/id_cp)")

with open(os.path.join(RAIZ, "data/portal/contenido-inspeccion.json"), encoding="utf-8") as f:
    ci = json.load(f)
rec = next(r for r in ci["recursos"] if "33d0a99e" in str(r.get("id", "")))
defs = rec["definiciones"]
assert len(defs) == 178, len(defs)
assert defs[6]["Nombre variable"] == "des_mpo_res", defs[6]
assert defs[176]["Nombre variable"] == "ide_id" and defs[176]["Ejemplo de dato"] == "ide_cp", defs[176]
assert defs[177]["Nombre variable"] == "ide_id" and defs[177]["Ejemplo de dato"] == "id_cp", defs[177]
print("OK  inspeccion: 178 definiciones; [6] genuina; [176]/[177] corruptas")

with open(os.path.join(RAIZ, list(ESPERADOS)[1]), encoding="utf-8") as f:
    pkg = json.load(f)
res = pkg.get("result", pkg)
assert res.get("version") is None, res.get("version")
assert len(res["resources"]) == 5, len(res["resources"])
por_id = {x["id"]: x for x in res["resources"]}
assert por_id["33d0a99e-c721-496f-a05e-07646e9ae42a"]["size"] == 51040
assert por_id["08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8"]["size"] == 12702
assert not any("municipio" in (x.get("name", "") or "").lower() for x in res["resources"])
print("OK  ckan: version null, 5 recursos, sizes 51040/12702, sin recurso municipios")

px = os.path.join(RAIZ, list(ESPERADOS)[4])
assert os.path.getsize(px) == 12702, os.path.getsize(px)
z = zipfile.ZipFile(px)
hojas = re.findall(r'name="([^"]+)"', z.read("xl/workbook.xml").decode("utf-8"))
assert len(hojas) == 3, hojas
ss = z.read("xl/sharedStrings.xml").decode("utf-8").lower()
assert "des_mpo_res" not in ss, "des_mpo_res en catalogo"
print("OK  xlsx: 12702 B, 3 hojas", hojas, ", sin des_mpo_res")

if fallos:
    raise SystemExit("FALLOS: %s" % fallos)
print("X-anomalias R8 v001: todas las comprobaciones locales pasan.")
