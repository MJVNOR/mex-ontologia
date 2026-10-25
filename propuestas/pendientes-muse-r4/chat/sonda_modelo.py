"""Sonda corta de disponibilidad de un modelo candidato. No imprime secretos."""
import json
import sys
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
    modelo = sys.argv[1]
    s = settings()
    body = json.dumps({
        "model": modelo,
        "messages": [{"role": "user", "content": "Responde solo con la palabra: ok"}],
        "max_tokens": 8,
    }).encode()
    req = urllib.request.Request(
        s["ONTO_LLM_BASE_URL"].rstrip("/") + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + s["ONTO_LLM_API_KEY"], "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.load(r)
        texto = (data.get("choices", [{}])[0].get("message", {}).get("content", ""))[:200]
        print(json.dumps({"modelo": modelo, "http": 200, "respuesta": texto}, ensure_ascii=False))
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"modelo": modelo, "error": str(exc)[:400]}, ensure_ascii=False))
