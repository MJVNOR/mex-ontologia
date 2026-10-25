import hashlib, pathlib, shutil, sys

SRC = pathlib.Path(r"C:\Users\marti\Documents\open-ontologies\studio\src-tauri\sidecars\agent")
DST = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat\fuente")
FILES = ["graphrag.ts", "graphrag.test.ts", "index.ts", "package.json",
         "vitest.config.ts", "cache-key.ts", "mcp.ts", "tokenise.ts", "providers/types.ts"]

DST.mkdir(parents=True, exist_ok=True)
manifest = []
for name in FILES:
    src = SRC / name
    if not src.exists():
        print("FALTA:", src)
        continue
    dst = DST / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    h = hashlib.sha256(src.read_bytes()).hexdigest()
    manifest.append({"archivo": name, "origen": str(src),
                     "bytes": src.stat().st_size, "sha256": h})
    print(name, src.stat().st_size, h)
print("copiados:", len(manifest))
