import pathlib, shutil
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat\trabajo")
for nombre in ["node_modules", ".npm-cache", "package-lock.json"]:
    p = BASE / nombre
    if p.is_dir() and not p.is_symlink():
        shutil.rmtree(p, ignore_errors=True)
        print("eliminado:", p, "existe:", p.exists())
    elif p.exists():
        print("se conserva (no es residuo de instalacion fallida):", p)
