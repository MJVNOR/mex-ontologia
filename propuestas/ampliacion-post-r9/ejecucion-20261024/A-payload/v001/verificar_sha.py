"""Verifica SHA-256 de payload/v001 y de sus origenes declarados. Solo lectura."""
import hashlib
import json
import pathlib

E = pathlib.Path(__file__).resolve().parents[2]  # .../ejecucion-20261024


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


sello = json.loads((E / "sello-payload-previo.json").read_text(encoding="utf-8"))
origenes = json.loads((E / "payload-origenes.json").read_text(encoding="utf-8"))

ok = True
print("== payload/v001 contra sello-payload-previo.json ==")
for rel, esperado in sello["archivos"].items():
    p = E / "payload" / "v001" / rel
    if not p.exists():
        print(f"FALTA  {rel}")
        ok = False
        continue
    real = sha(p)
    estado = "OK" if real == esperado else "MISMATCH"
    if real != esperado:
        ok = False
    print(f"{estado:8} {rel}  {real[:16]} esperado {esperado[:16]}")

print(f"\narchivos listados en sello: {len(sello['archivos'])}")
reales = sorted(
    str(p.relative_to(E / "payload" / "v001")).replace("\\", "/")
    for p in (E / "payload" / "v001").rglob("*")
    if p.is_file()
)
declarados = sorted(sello["archivos"])
print(f"archivos reales en payload/v001: {len(reales)}")
print("no declarados:", [r for r in reales if r not in declarados])
print("declarados ausentes:", [d for d in declarados if d not in reales])

print("\n== origenes declarados ==")
repo = E.parents[2]
for rel, esperado in origenes["origenes"].items():
    p = repo / rel
    if not p.exists():
        print(f"FALTA  {rel}")
        ok = False
        continue
    real = sha(p)
    if real != esperado:
        ok = False
    print(f"{'OK' if real == esperado else 'MISMATCH':8} {rel}")

aceptadas = E / "payload" / "v001" / "aceptadas.json"
print("\n== aceptadas.json ==")
print("declarado en payload-origenes:", origenes["aceptadas_sha256"])
print("declarado en sello            :", sello["archivos"]["aceptadas.json"])
print("real                          :", sha(aceptadas))
print("coincide con ambos            :",
      sha(aceptadas) == origenes["aceptadas_sha256"] == sello["archivos"]["aceptadas.json"])

print("\nRESULTADO:", "TODO OK" if ok else "HAY DISCREPANCIAS")
