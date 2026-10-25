"""Recuperacion SOLO-B: 1 request, 0 retry. Guardado a prueba de encoding."""
import datetime
import hashlib
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
MODEL = "gemma-4-31b-it"
TIMEOUT = 90

# 1) Verificacion offline: round-trip UTF-8 con coreano/acentos ANTES de la llamada.
probe = "한글 테스트ბ — café, niño, München, 日本語, pensamiento \ub098"
rt = (HERE / "_probe-roundtrip.tmp").write_text(probe, encoding="utf-8")
assert (HERE / "_probe-roundtrip.tmp").read_text(encoding="utf-8") == probe
(HERE / "_probe-roundtrip.tmp").unlink()
(HERE / "_probe-raw.tmp").write_bytes(probe.encode("utf-8"))
assert (HERE / "_probe-raw.tmp").read_bytes().decode("utf-8") == probe
(HERE / "_probe-raw.tmp").unlink()
print("roundtrip-utf8-ok")

# 2) Espera >=65s desde ultimo inicio (B original ~05:32:22Z; ancla conservadora).
ancla = datetime.datetime(2026, 10, 24, 5, 32, 30, tzinfo=datetime.timezone.utc)
queda = 70 - (datetime.datetime.now(datetime.timezone.utc) - ancla).total_seconds()
if queda > 0:
    time.sleep(queda)

env = {}
for line in (REPO / ".env").read_text(encoding="utf-8").splitlines():
    if line.strip() and not line.strip().startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
key = env["ONTO_LLM_API_KEY"]
assert env["ONTO_LLM_MODEL"] == MODEL

ict = json.loads((REPO / "propuestas/diagnostico-gemma/c6-captura-20261024T052828Z/payload-intercept.json").read_bytes())
URL = ict["url_sin_query"]
body = dict(ict["body"])
body["extra_body"] = {"google": {"thinking_config": {"thinking_level": "minimal", "include_thoughts": False}}}

msgs_json = json.dumps(body["messages"], ensure_ascii=False)
sha_msgs = hashlib.sha256(msgs_json.encode("utf-8")).hexdigest()
sys_c, user_c = body["messages"][0]["content"], body["messages"][1]["content"]

raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=raw,
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + key}, method="POST")
t0 = time.monotonic()
inicio = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
try:
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        crudo = r.read()
        status, err = r.status, None
        hdrs = {k.lower(): v for k, v in r.headers.items()}
except urllib.error.HTTPError as e:
    crudo = e.read()
    status, err = e.code, f"HTTPError {e.code}"
    hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
except Exception as e:
    crudo, status, err, hdrs = b"", None, f"{type(e).__name__}: {str(e)[:200]}", {}
dur = round(time.monotonic() - t0, 2)

# 3) PRIMERO el cuerpo crudo, bytes intactos.
(HERE / "b-recuperacion-response.bin").write_bytes(crudo)
try:
    parsed = json.loads(crudo)
except Exception:
    parsed = None
ch = ((parsed.get("choices") or [{}])[0]) if isinstance(parsed, dict) else {}
out = {
    "inicio_utc": inicio, "url": URL, "body_enviado": body,
    "sha256_messages": sha_msgs,
    "input_total_chars": len(sys_c) + len(user_c),
    "input_total_utf8_bytes": len((sys_c + user_c).encode("utf-8")),
    "status": status, "duracion_s": dur, "error": err,
    "headers_diagnostico": {k: v for k, v in hdrs.items() if k in {
        "content-type", "retry-after", "x-request-id", "x-google-request-id",
        "x-cloud-trace-context", "date", "server", "via"}},
    "usage": (parsed.get("usage") if isinstance(parsed, dict) else None),
    "finish_reason": ch.get("finish_reason"),
    "texto_visible": ((ch.get("message") or {}).get("content")),
    "respuesta_parseada": parsed if parsed is not None else None,
    "cuerpo_crudo_bytes": len(crudo),
}
(HERE / "b-recuperacion.json").write_text(json.dumps(out, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: out[k] for k in ("inicio_utc", "status", "duracion_s", "error", "usage", "finish_reason", "cuerpo_crudo_bytes")}, ensure_ascii=True, indent=2))
