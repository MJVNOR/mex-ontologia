import pathlib, shutil
p = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat\trabajo\node_modules")
shutil.rmtree(p, ignore_errors=True)
print("cache vitest eliminada, existe:", p.exists())
