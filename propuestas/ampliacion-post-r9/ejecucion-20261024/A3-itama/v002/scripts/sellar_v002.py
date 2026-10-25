"""Sella A3-ITAMA v002: SHA-256 de cada archivo entregable, sin autohash.

Escribe congelada.json (mapa archivo -> sha256) y congelada.sha256 (sha256 de
congelada.json). El sello no se incluye a si mismo ni a su sidecar.

Uso:
    uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/scripts/sellar_v002.py
"""

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
EXCLUIR = {"congelada.json", "congelada.sha256"}
PAR = (
    "27a5c80c-514a-4170-a2e5-7ef40d818641"
    "--4d27a1c4-381d-4ce0-a663-0d3e23a93848"
)

archivos = sorted(
    p.relative_to(BASE).as_posix()
    for p in BASE.rglob("*")
    if p.is_file() and p.relative_to(BASE).as_posix() not in EXCLUIR
)
for obligatorio in ("entrega.json", "nucleo.ttl", "evidencia-busqueda.json"):
    assert obligatorio in archivos, f"falta {obligatorio}"

sello = {
    "rol": "A3-itama",
    "version": "v002",
    "algoritmo": "sha256",
    "par": PAR,
    "decision": "BLOQUEADO",
    "archivos": {
        rel: hashlib.sha256((BASE / rel).read_bytes()).hexdigest()
        for rel in archivos
    },
}

texto = json.dumps(sello, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
(BASE / "congelada.json").write_bytes(texto.encode("utf-8"))
digest = hashlib.sha256(texto.encode("utf-8")).hexdigest()
(BASE / "congelada.sha256").write_bytes(
    f"{digest}  congelada.json\n".encode("utf-8")
)

print(f"{len(archivos)} archivos sellados")
print(f"congelada.json sha256={digest}")
