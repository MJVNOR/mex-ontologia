"""Lista modelos disponibles con la credencial existente. No imprime secretos."""
import json
import urllib.request
from pathlib import Path

POINTER = Path("C:/Users/marti/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/open-ontologies-studio/agent-env-path.txt")


def settings():
    target = Path(POINTER.read_text(encoding="utf-8-sig").strip())
    out = {}
    for line in target.read_text(encoding="utf-8-sig").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip().startswith("ONTO_"):
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


if __name__ == "__main__":
    s = settings()
    print("base:", s.get("ONTO_LLM_BASE_URL"))
    print("modelo_actual:", s.get("ONTO_LLM_MODEL"))
    req = urllib.request.Request(
        s["ONTO_LLM_BASE_URL"].rstrip("/") + "/models",
        headers={"Authorization": "Bearer " + s["ONTO_LLM_API_KEY"]},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    for m in data.get("data", []):
        mid = str(m.get("id", "")).replace("models/", "")
        print("-", mid)
