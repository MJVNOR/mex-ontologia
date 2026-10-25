import pathlib, os

home = pathlib.Path.home()
local = pathlib.Path(os.environ.get("LOCALAPPDATA", ""))
cands = [
    home / ".open-ontologies",
    local / "open-ontologies-studio",
    local / "Packages",
]
for c in cands:
    print("==", c, "existe:", c.exists())
    if c.exists() and c.name == "Packages":
        for child in sorted(c.iterdir()):
            if "codex" in child.name.lower() or "open" in child.name.lower():
                print("  sub:", child)
                sib = child / "LocalCache" / "Local" / "open-ontologies-studio" / "sidecars" / "agent" / "dist" / "index.js"
                print("   bundle:", sib.exists(), sib)
                envf = child / "LocalCache" / "Local" / "open-ontologies-studio" / "agent-env-path.txt"
                print("   envpath:", envf.exists(), envf)
    elif c.exists():
        print("  contenido:", [x.name for x in list(c.iterdir())[:20]])
