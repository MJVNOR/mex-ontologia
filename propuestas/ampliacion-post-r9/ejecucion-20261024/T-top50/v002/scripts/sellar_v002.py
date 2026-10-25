"""Sella T-top50 v002: publica, ejecuta pruebas y hashea los bytes reales.

El sello no se transcribe: se calcula sobre esta carpeta. Excluye el propio
``congelada.json``, ``__pycache__`` y ``*.pyc`` (sin autohash ni caches).
Uso: uv run python propuestas/.../T-top50/v002/scripts/sellar_v002.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

V2 = Path(__file__).resolve().parent.parent
ROOT = next(p for p in (V2, *V2.parents)
            if (p / "pyproject.toml").is_file() and (p / "data/portal/oportunidades-cruce.json").is_file())
SELLO = V2 / "congelada.json"
ALCANCE = "propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v002/"
EJECUCIONES = [
    ("publicacion", "propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v002/scripts/publicar_top50_r9.py",
     ["--out-dir", ALCANCE.rstrip("/")]),
    ("pruebas", "propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v002/tests/test_publicar_top50_r9.py", []),
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def correr(nombre: str, relativo: str, extra: list[str]) -> dict:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run([sys.executable, str(ROOT / relativo), *extra], cwd=ROOT,
                          capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    texto = (proc.stdout or "") + (("\n[stderr]\n" + proc.stderr) if proc.stderr else "")
    texto = re.sub(r"in \d+\.\d+s", "in Xs", texto.replace("\r\n", "\n"))
    destino = V2 / "resultados" / f"{nombre}.out"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(texto, encoding="utf-8", newline="\n")
    print(f"[{nombre}] exit={proc.returncode} -> resultados/{nombre}.out")
    return {
        "ejecucion": nombre,
        "comando": f"uv run python {relativo}" + (" " + " ".join(extra) if extra else ""),
        "exit_code": proc.returncode,
        "salida_capturada": f"resultados/{nombre}.out",
        "salida_sha256": sha256(destino),
    }


def manifiesto() -> list[dict]:
    return [
        {"ruta": p.relative_to(V2).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p)}
        for p in sorted(V2.rglob("*"))
        if p.is_file()
        and p.resolve() != SELLO
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
    ]


def main() -> int:
    ejecuciones = [correr(*e) for e in EJECUCIONES]
    if any(e["exit_code"] != 0 for e in ejecuciones):
        print("No se sella: hubo ejecuciones con codigo distinto de 0")
        return 1

    archivos = manifiesto()
    sello = hashlib.sha256(json.dumps(archivos, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    doc = {
        "rol": "T-top50",
        "version": "v002",
        "generado_en_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "modelo": "opencode/deepseek-v4.1-flash-free",
        "alcance": ALCANCE,
        "excluido_del_manifiesto": ["congelada.json (el propio sello)", "__pycache__/", "*.pyc"],
        "ejecuciones": ejecuciones,
        "total_archivos": len(archivos),
        "total_bytes": sum(a["bytes"] for a in archivos),
        "archivos": archivos,
        "sello_sha256": sello,
        "metodo_sello": "sha256 sobre JSON canonico (sort_keys, separadores ',', ':') de la "
                        "lista archivos (ruta, bytes, sha256), sin autohash ni caches",
        "verificacion": "reejecutar este script: sello_sha256 se mantiene porque los artefactos "
                        "no llevan reloj (fecha_corte fija) y las salidas de pruebas normalizan "
                        "duraciones; solo cambia generado_en_utc, excluido del manifiesto",
        "nota": "Cada hash se recalcula de los bytes de esta carpeta; ningun valor se transcribe.",
    }
    SELLO.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for a in archivos:  # verificacion inmediata contra disco
        assert sha256(V2 / a["ruta"]) == a["sha256"], a["ruta"]
    print(json.dumps({"archivos": len(archivos), "bytes": doc["total_bytes"], "sello_sha256": sello}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
