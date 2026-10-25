"""Prueba A1-911 v002: ejecuta el script, exige bloqueo y comprueba el sello.

- Dos ejecuciones en directorios distintos producen bytes identicos.
- Los ficheros entregados coinciden con la salida regenerada (nada transcrito).
- El sello cubre los entregables y su propio sha256 cuadra.
- No hay proporcion ni join; el duplicado y la ausencia de MUNICIPIO constan.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCRIPT = BASE / "scripts" / "comprobar_a1_911.py"
SELLO = BASE / "sello.json"
SELLO_SHA = BASE / "sello.sha256"


def ejecutar(destino):
    p = subprocess.run([sys.executable, str(SCRIPT), str(destino)],
                       capture_output=True, text=True, encoding="utf-8")
    assert p.returncode == 0, p.stderr[-2000:]
    return {n: (destino / n).read_bytes()
            for n in ("resultados.json", "entrega.json", "entrega.md")}


with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
    uno = ejecutar(Path(t1))
    dos = ejecutar(Path(t2))
    assert uno == dos, "la salida no es determinista"
    for nombre, datos in uno.items():
        assert datos == (BASE / nombre).read_bytes(), f"{nombre} entregado != generado"

r = json.loads((BASE / "resultados.json").read_text(encoding="utf-8"))
e = json.loads((BASE / "entrega.json").read_text(encoding="utf-8"))

assert r["resultado"] == "bloqueado" and e["resultado"] == "bloqueado"
assert r["join"]["ejecutado"] is False
assert r["proporcion"]["estado"] == "bloqueada"
assert "valor" not in r["proporcion"] and "tasa" not in r["proporcion"]
assert set(r["ficha"]) == {"claves", "grano", "unicidad", "cardinalidad",
                           "poblacion", "periodo", "unidades", "cobertura_datos"}
assert all(v["estado"] and v["evidencia"] for v in r["ficha"].values())

d = r["hallazgos"]["duplicado_entre_conjuntos"]
assert d["recursos"] == ["54285a13-3a2a-4e47-b0af-e855861f5347",
                         "6ce17dd1-5716-44e9-bc5f-603c0925afe6"]
assert d["sha256"] == "9d710cb868c3fb6304a4310259bf4c7e64d2af7cdc15cd253bdc8dd86c9c2109"
assert r["hallazgos"]["q2_improcedentes_sin_municipio"]["columnas"] == [
    "FECHA", "HORA", "MOTIVO NO PROCEDENTE"]
assert r["hallazgos"]["muestra_a_desde_duplicado"]["recurso_muestra_a"] == d["recursos"][0]

estados = {c["id"]: c["estado"] for c in r["comprobaciones"]}
assert estados["proporcion"] == "bloqueado" and estados["join"] == "bloqueado"
assert estados["duplicado_entre_conjuntos"] == "ok"
assert estados["q2_improcedentes_sin_municipio"] == "ok"
assert estados["particion_no_declarada"] == "bloqueado"

sello = json.loads(SELLO.read_text(encoding="utf-8"))
for rel, sha in sello["archivos"].items():
    assert hashlib.sha256((BASE / rel).read_bytes()).hexdigest() == sha, rel
for obligatorio in ("entrega.json", "entrega.md", "resultados.json",
                    "scripts/comprobar_a1_911.py", "tests/test_a1_911.py"):
    assert obligatorio in sello["archivos"], obligatorio
assert "sello.json" not in sello["archivos"] and "sello.sha256" not in sello["archivos"]
sha_sello = hashlib.sha256(SELLO.read_bytes()).hexdigest()
assert SELLO_SHA.read_text(encoding="utf-8") == f"{sha_sello}  sello.json\n"

print("test_a1_911 v002 OK")
