import hashlib, pathlib
code = pathlib.Path(
    "propuestas/pendientes-muse-r4/ambiguedades/generar_entrega.py"
).read_text(encoding="utf-8")
target = "propuestas/pendientes-muse-r4/ambiguedades/entrega.json"
tmp = "C:/Users/marti/AppData/Local/Temp/opencode/gen_ambig.json"
assert target in code
code = code.replace(target, tmp)
ns = {
    "__name__": "gen",
    "__file__": str(
        pathlib.Path(
            "propuestas/pendientes-muse-r4/ambiguedades/generar_entrega.py"
        ).resolve()
    ),
}
exec(compile(code, "gen", "exec"), ns)
p = pathlib.Path(tmp)
print("regen:", hashlib.sha256(p.read_bytes()).hexdigest())
print("listo: b72cdcf4e1ae3668e2287e373652b30a93f1cf0c2af3d7d90852cd031b7d1ac")
print("disco: 93e89e136a7e178a6e7e35d95d41cbc3e4788bd25de68180d893b964924e50b3")
