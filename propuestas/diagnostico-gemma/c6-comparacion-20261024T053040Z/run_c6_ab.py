"""C6 comparacion controlada: A exacto bundle, B = A + thinking minimal. 2 intentos, 0 retry."""
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
GAP_S = 70  # >=65s entre inicios

SAFE_HEADERS = {
    "content-type", "retry-after", "x-request-id", "x-google-request-id",
    "x-cloud-trace-context", "date", "server", "via",
    "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
}

env = {}
for line in (REPO / ".env").read_text().splitlines():
    if line.strip() and not line.strip().startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
key = env["ONTO_LLM_API_KEY"]
assert env["ONTO_LLM_MODEL"] == MODEL

ict = json.loads((REPO / "propuestas/diagnostico-gemma/c6-captura-20261024T052828Z/payload-intercept.json").read_bytes())
URL = ict["url_sin_query"]
assert ict["method"] == "POST"
BODY_A = ict["body"]  # orden de claves preservado del archivo
assert list(BODY_A.keys()) == ["model", "messages", "temperature", "top_p", "max_tokens"]
assert BODY_A["model"] == MODEL and BODY_A["max_tokens"] == 4096
BODY_B = dict(BODY_A)
BODY_B["extra_body"] = {"google": {"thinking_config": {"thinking_level": "minimal", "include_thoughts": False}}}

msgs_json = json.dumps(BODY_A["messages"], ensure_ascii=False)
sha_msgs = hashlib.sha256(msgs_json.encode("utf-8")).hexdigest()
sys_c, user_c = BODY_A["messages"][0]["content"], BODY_A["messages"][1]["content"]


def one_shot(body):
    raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(URL, data=raw,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key}, method="POST")
    t0 = time.monotonic()
    inicio = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            resp = r.read().decode("utf-8", "replace")
            status, err = r.status, None
            hdrs = {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        resp = e.read().decode("utf-8", "replace")
        status, err = e.code, f"HTTPError {e.code}"
        hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
    except Exception as e:
        resp, status, err, hdrs = "", None, f"{type(e).__name__}: {str(e)[:200]}", {}
    dur = round(time.monotonic() - t0, 2)
    try:
        parsed = json.loads(resp)
    except Exception:
        parsed = None
    ch = ((parsed.get("choices") or [{}])[0]) if isinstance(parsed, dict) else {}
    return {
        "inicio_utc": inicio, "url": URL, "body_enviado": body,
        "sha256_messages": sha_msgs,
        "input_system_chars": len(sys_c), "input_user_chars": len(user_c),
        "input_total_chars": len(sys_c) + len(user_c),
        "input_total_utf8_bytes": len((sys_c + user_c).encode("utf-8")),
        "status": status, "duracion_s": dur, "error": err,
        "headers_diagnostico": {k: v for k, v in hdrs.items() if k in SAFE_HEADERS},
        "usage": (parsed.get("usage") if isinstance(parsed, dict) else None),
        "finish_reason": ch.get("finish_reason"),
        "respuesta_completa": parsed if parsed is not None else resp,
    }, t0


a, tA = one_shot(BODY_A)
(HERE / "a-exacto-bundle.json").write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

queda = GAP_S - (time.monotonic() - tA)
if queda > 0:
    time.sleep(queda)

b, _ = one_shot(BODY_B)
(HERE / "b-thinking-minimal.json").write_text(json.dumps(b, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

resumen = {
    "fecha_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "modelo": MODEL, "caso": "C6-clave-26001",
    "gap_inicios_s": round((datetime.datetime.fromisoformat(b["inicio_utc"].replace("Z", "+00:00")) - datetime.datetime.fromisoformat(a["inicio_utc"].replace("Z", "+00:00"))).total_seconds(), 1),
    "A": {k: a[k] for k in ("inicio_utc", "status", "duracion_s", "error", "usage", "finish_reason")},
    "B": {k: b[k] for k in ("inicio_utc", "status", "duracion_s", "error", "usage", "finish_reason")},
    "requests_reales": 2, "retries": 0,
}
(HERE / "resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(resumen, indent=2, ensure_ascii=False))
