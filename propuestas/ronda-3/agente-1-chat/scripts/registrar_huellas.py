import hashlib, json, pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
UPSTREAM = pathlib.Path(r"C:\Users\marti\Documents\open-ontologies\studio\src-tauri\sidecars\agent")
INST = pathlib.Path(r"C:\Users\marti\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\open-ontologies-studio\sidecars\agent\dist\index.js")

huellas = {}
for copia in sorted((BASE / "fuente").rglob("*")):
    if copia.is_file() and copia.name != "huellas.json":
        rel = copia.relative_to(BASE / "fuente").as_posix()
        origen = UPSTREAM / rel
        huellas[rel] = {
            "origen": str(origen),
            "bytes_origen": origen.stat().st_size,
            "sha256": hashlib.sha256(origen.read_bytes()).hexdigest(),
            "copia_bytes": copia.stat().st_size,
        }
        assert copia.read_bytes() == origen.read_bytes(), rel

huellas["_instalado"] = {
    "ruta": str(INST),
    "bytes": INST.stat().st_size,
    "sha256": hashlib.sha256(INST.read_bytes()).hexdigest(),
}
huellas["_toolchain_upstream"] = {
    "node": "v22.23.2",
    "npm": "10.2.3",
    "esbuild": "0.28.2",
    "typescript": "5.9.3",
    "vitest": "4.1.11",
    "@anthropic-ai/sdk": "0.116.0",
}
(BASE / "fuente" / "huellas.json").write_text(
    json.dumps(huellas, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: v.get("sha256", "")[:16] for k, v in huellas.items()}, indent=2))
