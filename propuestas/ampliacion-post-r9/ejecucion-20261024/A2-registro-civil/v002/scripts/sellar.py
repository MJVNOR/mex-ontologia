"""Sella A2-registro-civil v002: SHA-256 de cada archivo entregable, sin autohash.

Escribe sello.json (mapa archivo -> sha256) y sello.sha256 (sha256 de
sello.json). El sello no se incluye a si mismo ni hashea cache de Python.

Uso:
    .venv/Scripts/python.exe propuestas/ampliacion-post-r9/ejecucion-20261024/A2-registro-civil/v002/scripts/sellar.py
"""

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[1]
EXCLUIR = {"sello.json", "sello.sha256"}


def entregable(p):
    rel = p.relative_to(BASE).as_posix()
    return rel not in EXCLUIR and "__pycache__" not in p.parts and p.suffix != ".pyc"


archivos = sorted(
    p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p.is_file() and entregable(p)
)
assert "resultados.json" in archivos and "entrega.json" in archivos, archivos

sello = {
    "rol": "A2-registro-civil",
    "version": "v002",
    "algoritmo": "sha256",
    "par": "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5",
    "resultado": "bloqueado",
    "archivos": {
        rel: hashlib.sha256((BASE / rel).read_bytes()).hexdigest() for rel in archivos
    },
}

texto = json.dumps(sello, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
(BASE / "sello.json").write_bytes(texto.encode("utf-8"))
digest = hashlib.sha256(texto.encode("utf-8")).hexdigest()
(BASE / "sello.sha256").write_bytes(f"{digest}  sello.json\n".encode("utf-8"))

print(f"{len(archivos)} archivos sellados")
print(f"sello.json sha256={digest}")
