"""Verificador reproducible de la entrega (sin modelos, sin red externa).

Solo lectura fuera de esta carpeta, salvo el motor HTTP local 8137 con --live
(consultas SELECT/CONSTRUCT/ASK, nunca UPDATE). No toca nucleo, ni Studio vivo,
ni la ubicacion upstream (usa su binario vitest existente sin mutarla).
"""
import hashlib
import json
import pathlib
import subprocess
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
TRABAJO = BASE / "trabajo"
PARCHE = BASE / "parche"
UPSTREAM = pathlib.Path(r"C:\Users\marti\Documents\open-ontologies\studio\src-tauri\sidecars\agent")
VITEST = UPSTREAM / "node_modules" / "vitest" / "vitest.mjs"
TSC = UPSTREAM / "node_modules" / "typescript" / "bin" / "tsc"
TYPES = UPSTREAM / "node_modules" / "@types"
FALLOS = []


def comprobar(nombre, condicion, detalle=""):
    print(("OK  " if condicion else "FALLO ") + nombre + (f" ({detalle})" if detalle else ""))
    if not condicion:
        FALLOS.append(nombre)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    live = "--live" in sys.argv[1:]

    # 1. Pruebas offline (reales, con negativos) sobre la fuente copiada.
    r = subprocess.run(
        ["node", str(VITEST), "run", "--root", ".",
         "recuperacion-r3.test.ts", "graphrag.test.ts", "recuperacion-e2e.test.ts"],
        cwd=TRABAJO, capture_output=True, text=True, timeout=300)
    print(r.stdout[-3000:])
    print(r.stderr[-1500:])
    texto = r.stdout + r.stderr
    comprobar("offline sin fallos (incluye e2e omitida sin live)", r.returncode == 0
              and "failed" not in texto.lower() and "passed" in texto,
              f"rc={r.returncode}")

    # 2. Tipos estrictos del modulo parchado.
    r = subprocess.run(
        ["node", str(TSC), "--noEmit", "--strict", "--skipLibCheck",
         "--target", "es2022", "--module", "nodenext",
         "--moduleResolution", "nodenext", "--typeRoots", str(TYPES),
         "graphrag.ts"],
        cwd=TRABAJO, capture_output=True, text=True, timeout=300)
    comprobar("tsc sin errores", r.returncode == 0, (r.stdout + r.stderr)[:500])

    # 3. El parche regenerado coincide con el entregado (aplicabilidad exacta).
    for nombre in ["graphrag.ts", "index.ts"]:
        original = (BASE / "fuente" / nombre).read_text(encoding="utf-8").splitlines()
        modificado = (TRABAJO / nombre).read_text(encoding="utf-8").splitlines()
        import difflib
        regenerado = "\n".join(difflib.unified_diff(
            original, modificado,
            fromfile=f"studio/src-tauri/sidecars/agent/{nombre} (original)",
            tofile=f"studio/src-tauri/sidecars/agent/{nombre} (parchado)",
            lineterm="")) + "\n"
        entregado = (PARCHE / f"{nombre}.patch").read_text(encoding="utf-8")
        comprobar(f"parche {nombre} reproducible", regenerado == entregado,
                  f"{len(entregado)} bytes")
        comprobar(f"parche {nombre} no vacio",
                  len([l for l in entregado.splitlines()
                       if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]) > 0)
        comprobar(f"modificado {nombre} difiere del original",
                  sha(TRABAJO / nombre) != sha(BASE / "fuente" / nombre))
        comprobar(f"original {nombre} intacto",
                  sha(BASE / "fuente" / nombre) ==
                  json.loads((BASE / "fuente" / "huellas.json").read_text(encoding="utf-8"))[nombre]["sha256"])

    # 4. Casos C05/C06 deterministas contra el motor vivo (solo con --live).
    if live:
        r = subprocess.run(
            ["uv", "run", "python", "scripts/evaluar_C05_C06.py"],
            cwd=BASE, capture_output=True, text=True, timeout=300)
        print(r.stdout[-2500:])
        print(r.stderr[-1000:])
        comprobar("C05/C06 deterministas en motor vivo", r.returncode == 0,
                  f"rc={r.returncode}")

    # 5. E2E con el retrieve()/asContext() reales parchados (solo con --live).
    if live:
        import os
        entorno = dict(os.environ, MEX_E2E_LIVE="1")
        r = subprocess.run(
            ["node", str(VITEST), "run", "--root", ".", "recuperacion-e2e.test.ts"],
            cwd=TRABAJO, capture_output=True, text=True, timeout=600,
            env=entorno)
        print(r.stdout[-2500:])
        print(r.stderr[-1000:])
        comprobar("e2e retrieve() real sobre motor vivo", r.returncode == 0,
                  f"rc={r.returncode}")
        try:
            e2e = json.loads((BASE / "evidencia" / "e2e_recuperacion.json").read_text(encoding="utf-8"))
            casos = e2e.get("casos", [])
            comprobar("e2e guardo 6 casos con pregunta+contexto+resumen",
                      len(casos) == 6 and all({"pregunta", "contexto", "resumen"} <= set(c) for c in casos),
                      f"casos={len(casos)}")
            textos = " ".join(c["contexto"] + " " + c["resumen"] for c in casos)
            comprobar("e2e contiene COMPLETE global y de recurso",
                      "GLOBAL CORRESPONDENCE COUNTS (COMPLETE)" in textos
                      and "COMPLETE correspondence counts for resolved resource" in textos)
            comprobar("e2e C05 trae el mapeo revisado esperado",
                      "semantic-mapping/c92aecbb076e2efd7d2dc0f31c469576a9b3ef32fce50445035ee34758bc973a" in textos)
        except Exception as e:  # noqa: BLE001
            comprobar(f"e2e evidencia legible ({e})", False)
    else:
        print("INFO  motor vivo omitido (usa --live para las comprobaciones C05/C06)")

    print(f"\n{len(FALLOS)} fallos: {FALLOS}" if FALLOS else "\nverificacion superada")
    raise SystemExit(1 if FALLOS else 0)


if __name__ == "__main__":
    main()
