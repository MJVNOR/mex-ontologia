#!/usr/bin/env python3
"""Verificacion independiente de sellos de la ejecucion 20261024.

No escribe en las carpetas auditadas. Solo lee bytes y calcula SHA-256.
Salida: JSON por stdout (o --out).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[6]
BASE = ROOT / "propuestas" / "ampliacion-post-r9" / "ejecucion-20261024"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def rel_files(base: Path, exclude: set[str]) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in sorted(base.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(base).as_posix()
        if rel in exclude:
            continue
        if "__pycache__/" in rel or rel.endswith(".pyc"):
            continue
        out[rel] = p
    return out


def verify_list_seal(name: str, base: Path, seal_name: str = "congelada.json") -> dict[str, Any]:
    seal_path = base / seal_name
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    entries = seal["archivos"]
    listed = {e["ruta"]: e for e in entries}
    actual = rel_files(base, {seal_name})
    checks = []
    for rel, entry in listed.items():
        p = base / rel
        if not p.is_file():
            checks.append({"ruta": rel, "estado": "falta"})
            continue
        data = p.read_bytes()
        got = sha256_bytes(data)
        checks.append({
            "ruta": rel,
            "estado": "ok" if (got == entry["sha256"] and len(data) == entry["bytes"]) else "discrepa",
            "sha256_esperado": entry["sha256"],
            "sha256_actual": got,
            "bytes_esperado": entry["bytes"],
            "bytes_actual": len(data),
        })
    extras = sorted(set(actual) - set(listed))
    expected_canon = canon([{"ruta": e["ruta"], "bytes": e["bytes"], "sha256": e["sha256"]} for e in entries])
    recomputed = sha256_bytes(expected_canon)
    declared = seal.get("sello_sha256")
    return {
        "entrega": name,
        "ruta_sello": str(seal_path.relative_to(ROOT)),
        "sha256_sello_archivo": sha256_file(seal_path),
        "tipo": "lista_relativa",
        "entradas": len(entries),
        "total_bytes_declarado": seal.get("total_bytes"),
        "archivos_ok": sum(1 for c in checks if c["estado"] == "ok"),
        "archivos_discrepantes": [c for c in checks if c["estado"] != "ok"],
        "extras_no_sellados": extras,
        "sello_sha256_declarado": declared,
        "sello_sha256_recalculado": recomputed,
        "sello_canonico_ok": declared == recomputed,
        "sello_valido": all(c["estado"] == "ok" for c in checks) and declared == recomputed and not extras,
        "generado_en_utc": seal.get("generado_en_utc"),
        "excluido": seal.get("excluido_del_manifiesto"),
        "ejecuciones": seal.get("ejecuciones"),
    }


def verify_map_seal(name: str, base: Path) -> dict[str, Any]:
    seal_path = base / "sello.json"
    sidecar_path = base / "sello.sha256"
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    entries = seal["archivos"]
    actual = rel_files(base, {"sello.json", "sello.sha256"})
    checks = []
    for rel, expected in entries.items():
        p = base / rel
        if not p.is_file():
            checks.append({"ruta": rel, "estado": "falta"})
            continue
        got = sha256_file(p)
        checks.append({
            "ruta": rel,
            "estado": "ok" if got == expected else "discrepa",
            "sha256_esperado": expected,
            "sha256_actual": got,
            "bytes_actual": p.stat().st_size,
        })
    extras = sorted(set(actual) - set(entries))
    sidecar = sidecar_path.read_text(encoding="utf-8").strip() if sidecar_path.is_file() else ""
    sidecar_hash = sidecar.split()[0] if sidecar else None
    sidecar_name = sidecar.split()[-1] if sidecar else None
    actual_seal_hash = sha256_file(seal_path)
    return {
        "entrega": name,
        "ruta_sello": str(seal_path.relative_to(ROOT)),
        "sha256_sello_archivo": actual_seal_hash,
        "tipo": "mapa_relativo",
        "entradas": len(entries),
        "archivos_ok": sum(1 for c in checks if c["estado"] == "ok"),
        "archivos_discrepantes": [c for c in checks if c["estado"] != "ok"],
        "extras_no_sellados": extras,
        "sidecar": sidecar,
        "sidecar_declara_sello_json": sidecar_name == "sello.json",
        "sidecar_hash_ok": sidecar_hash == actual_seal_hash,
        "sello_valido": all(c["estado"] == "ok" for c in checks) and not extras
        and sidecar_hash == actual_seal_hash and sidecar_name == "sello.json",
        "par": seal.get("par"),
        "resultado": seal.get("resultado"),
    }


def verify_abs_seal(name: str, base: Path) -> dict[str, Any]:
    seal_path = base / "congelada.json"
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    entries = seal["archivos"]
    checks = []
    for e in entries:
        p = ROOT / e["ruta"]
        if not p.is_file():
            checks.append({"ruta": e["ruta"], "estado": "falta"})
            continue
        data = p.read_bytes()
        got = sha256_bytes(data)
        checks.append({
            "ruta": e["ruta"],
            "estado": "ok" if (got == e["sha256"] and len(data) == e["bytes"]) else "discrepa",
            "sha256_esperado": e["sha256"],
            "sha256_actual": got,
            "bytes_esperado": e["bytes"],
            "bytes_actual": len(data),
        })
    listed_rel = {str(Path(e["ruta"]).relative_to(base.relative_to(ROOT))).replace("\\", "/") for e in entries}
    actual = rel_files(base, {"congelada.json"})
    extras = sorted(set(actual) - listed_rel)
    return {
        "entrega": name,
        "ruta_sello": str(seal_path.relative_to(ROOT)),
        "sha256_sello_archivo": sha256_file(seal_path),
        "tipo": "lista_absoluta",
        "entradas": len(entries),
        "archivos_ok": sum(1 for c in checks if c["estado"] == "ok"),
        "archivos_discrepantes": [c for c in checks if c["estado"] != "ok"],
        "extras_no_sellados": extras,
        "sello_valido": all(c["estado"] == "ok" for c in checks) and not extras,
        "fecha_utc": seal.get("fecha_utc"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    results = {
        "T-top50/v002": verify_list_seal("T-top50/v002", BASE / "T-top50" / "v002"),
        "A1-911/v002": verify_map_seal("A1-911/v002", BASE / "A1-911" / "v002"),
        "A2-registro-civil/v002": verify_map_seal("A2-registro-civil/v002", BASE / "A2-registro-civil" / "v002"),
        "A3-itama/v002": verify_list_seal("A3-itama/v002", BASE / "A3-itama" / "v002"),
        "W-estandares/v002": verify_abs_seal("W-estandares/v002", BASE / "W-estandares" / "v002"),
    }
    payload = json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True)
    if args.out:
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        sys.stdout.write(payload + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
