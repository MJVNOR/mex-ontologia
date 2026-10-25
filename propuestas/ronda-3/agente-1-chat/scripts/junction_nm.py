import pathlib, subprocess
STAGE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat\evidencia\build-identidad")
SRC = pathlib.Path(r"C:\Users\marti\Documents\open-ontologies\studio\src-tauri\sidecars\agent\node_modules")
link = STAGE / "node_modules"
if not link.exists():
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(SRC)],
                       capture_output=True, text=True)
    print(r.stdout, r.stderr, r.returncode)
print("link existe:", link.exists())
