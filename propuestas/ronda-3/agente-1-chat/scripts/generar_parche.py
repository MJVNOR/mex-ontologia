import difflib, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
for name in ["graphrag.ts", "index.ts"]:
    original = (BASE / "fuente" / name).read_text(encoding="utf-8").splitlines()
    modificado = (BASE / "trabajo" / name).read_text(encoding="utf-8").splitlines()
    diff = difflib.unified_diff(
        original, modificado,
        fromfile=f"studio/src-tauri/sidecars/agent/{name} (original)",
        tofile=f"studio/src-tauri/sidecars/agent/{name} (parchado)",
        lineterm="")
    out = BASE / "parche" / f"{name}.patch"
    texto = "\n".join(diff) + "\n"
    out.write_text(texto, encoding="utf-8")
    anadidas = sum(1 for l in texto.splitlines() if l.startswith("+") and not l.startswith("+++"))
    quitadas = sum(1 for l in texto.splitlines() if l.startswith("-") and not l.startswith("---"))
    print(name, "lineas +:", anadidas, "-:", quitadas, "->", out)
