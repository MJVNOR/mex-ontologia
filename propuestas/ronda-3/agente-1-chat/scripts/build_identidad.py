import hashlib, pathlib, shutil, subprocess

SRC = pathlib.Path(r"C:\Users\marti\Documents\open-ontologies\studio\src-tauri\sidecars\agent")
STAGE = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\propuestas\ronda-3\agente-1-chat\evidencia\build-identidad")
ESBUILD = SRC / "node_modules" / "esbuild" / "bin" / "esbuild"
INST = pathlib.Path(r"C:\Users\marti\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\open-ontologies-studio\sidecars\agent\dist\index.js")

if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)
for name in ["index.ts", "graphrag.ts", "mcp.ts", "cache-key.ts", "tokenise.ts",
             "workflows.ts", "baseline.ts", "graphrag.test.ts", "package.json"]:
    shutil.copy2(SRC / name, STAGE / name)
shutil.copytree(SRC / "providers", STAGE / "providers")
subprocess.run(["cmd", "/c", "mklink", "/J", str(STAGE / "node_modules"),
                str(SRC / "node_modules")], capture_output=True)

r = subprocess.run(
    ["node", str(ESBUILD), "index.ts", "--bundle", "--platform=node",
     "--format=esm", "--target=node20", "--outfile=dist/index.js"],
    cwd=STAGE, capture_output=True, text=True, timeout=300)
print("esbuild rc:", r.returncode)
print((r.stdout + r.stderr)[:2000])
built = STAGE / "dist" / "index.js"
if built.exists():
    hb = hashlib.sha256(built.read_bytes()).hexdigest()
    hi = hashlib.sha256(INST.read_bytes()).hexdigest()
    print("rebuild bytes:", built.stat().st_size, "sha256:", hb)
    print("instalado bytes:", INST.stat().st_size, "sha256:", hi)
    print("IDENTICOS:" , hb == hi)
