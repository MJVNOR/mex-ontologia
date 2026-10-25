"""Req3 diagnostico: OpenAI-compatible + thinking minimal. UN solo intento, sin retry."""
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = "gemma-4-31b-it"
TIMEOUT = 90

# Ultimo inicio conocido req2: 2026-10-24T05:26:02Z. Dormir 25s garantiza >=65s.
time.sleep(25)

env = {}
for line in (HERE.parents[2] / ".env").read_text().splitlines():
    if line.strip() and not line.strip().startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
base = env["ONTO_LLM_BASE_URL"].rstrip("/")
assert env["ONTO_LLM_MODEL"] == MODEL
key = env["ONTO_LLM_API_KEY"]

url = f"{base}/chat/completions"
body = {
    "model": MODEL,
    "messages": [{"role": "user", "content": "Responde solamente OK"}],
    "max_tokens": 256,
    "extra_body": {"google": {"thinking_config": {"thinking_level": "minimal", "include_thoughts": False}}},
}
req = urllib.request.Request(
    url, data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
    method="POST",
)
import datetime
t0 = time.monotonic()
inicio = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
try:
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        resp_body = r.read().decode("utf-8", "replace")
        status, err = r.status, None
except urllib.error.HTTPError as e:
    resp_body = e.read().decode("utf-8", "replace")
    status, err = e.code, f"HTTPError {e.code}"
dur = round(time.monotonic() - t0, 2)
parsed = json.loads(resp_body)
choice = (parsed.get("choices") or [{}])[0]
out = {
    "inicio_utc": inicio,
    "url": url,
    "body_enviado": body,
    "status": status,
    "duracion_s": dur,
    "error": err,
    "usage": parsed.get("usage"),
    "finish_reason": choice.get("finish_reason"),
    "texto_visible": ((choice.get("message") or {}).get("content")),
    "respuesta_completa": parsed,
}
(HERE / "req3-minimal-thinking.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({k: out[k] for k in ("inicio_utc", "status", "duracion_s", "error", "usage", "finish_reason", "texto_visible")}, indent=2, ensure_ascii=False))
