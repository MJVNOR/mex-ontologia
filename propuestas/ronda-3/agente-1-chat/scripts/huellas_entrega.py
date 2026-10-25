import hashlib, json, pathlib
BASE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat")
for p in ["parche/graphrag.ts", "parche/index.ts", "parche/graphrag.ts.patch",
          "parche/index.ts.patch", "trabajo/recuperacion-r3.test.ts",
          "evidencia/evaluacion_C05_C06.json"]:
    b = (BASE / p).read_bytes()
    print(p, len(b), hashlib.sha256(b).hexdigest())
