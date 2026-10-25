import hashlib, pathlib, sys

candidatos = [
    pathlib.Path(r"C:\Users\marti\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g\LocalCache\Local\open-ontologies-studio\sidecars\agent\dist\index.js"),
]
for p in candidatos:
    print("existe:", p.exists(), p)
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print("bytes:", p.stat().st_size, "sha256:", h)

# buscar otros dist/index.js instalados sin recorrer todo el disco: variables de entorno habituales
import os
for base in [os.environ.get("LOCALAPPDATA", ""), os.environ.get("APPDATA", "")]:
    print("base:", base)
