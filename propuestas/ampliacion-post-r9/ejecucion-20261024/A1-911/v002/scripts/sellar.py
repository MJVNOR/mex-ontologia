"""Sella A1-911 v002: SHA-256 de cada archivo entregable, sin autohash.

Escribe sello.json (mapa archivo -> sha256) y sello.sha256 (sha256 de
sello.json). El sello no se incluye a si mismo.

Uso:
    uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A1-911/v002/scripts/sellar.py
"""

import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parents[1]
EXCLUIR = {"sello.json", "sello.sha256"}

archivos = sorted(
    p.relative_to(BASE).as_posix()
    for p in BASE.rglob("*")
    if p.is_file() and p.relative_to(BASE).as_posix() not in EXCLUIR
)
assert "resultados.json" in archivos and "entrega.json" in archivos, archivos

sello = {
    "rol": "A1-911",
    "version": "v002",
    "algoritmo": "sha256",
    "par": "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92",
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
