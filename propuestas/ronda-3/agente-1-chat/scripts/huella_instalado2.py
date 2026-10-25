import hashlib, pathlib
p = pathlib.Path(r"C:\Users\marti\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\open-ontologies-studio\sidecars\agent\dist\index.js")
b = p.read_bytes()
print("bytes:", len(b))
print("sha256:", hashlib.sha256(b).hexdigest())
e = pathlib.Path(str(p.parent.parent / "agent-env-path.txt"))
print("envpath existe:", e.exists())
if e.exists():
    print("envpath contenido (solo ruta, sin secretos):", e.read_text(encoding="utf-8", errors="replace")[:300])
