"""Lanza el MCP stdio de Open Ontologies sobre el almacén vigente del portal.

Resuelve store_dir desde reports/portal-carga.json para no hardcodear
la instantánea en opencode.json. Fija modo persistente.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "reports" / "portal-carga.json").read_text(encoding="utf-8"))
    store = manifest.get("store_dir")
    if not store:
        sys.exit("Genera y carga el portal primero con ampliar_portal.py --load")
    exe = ROOT / "tools" / "open-ontologies.exe"
    # ponytail: subprocess con stdio heredado; os.execve cae con 0xC0000005 en este Windows
    proc = subprocess.run([str(exe), "serve", "--storage-mode", "persistent",
                           "--data-dir", str(ROOT / store),
                           "--tools-allow", "onto_query,onto_stats,onto_status,onto_validate,onto_shacl"])
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
