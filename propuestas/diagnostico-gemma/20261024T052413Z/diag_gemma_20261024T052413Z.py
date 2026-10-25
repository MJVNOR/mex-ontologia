"""Diagnostico minimo gemma-4-31b-it: EXACTAMENTE 2 requests, sin retries.
(1) OpenAI-compatible: POST {BASE}/chat/completions
(2) Nativo Google: POST .../v1beta/models/gemma-4-31b-it:generateContent
65s+ entre inicios, timeout 90s c/u, un solo intento c/u. Sin system/tools/historial.
Lee clave de .env en memoria; nunca la imprime ni la guarda.
"""
import datetime
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = "gemma-4-31b-it"
TEXT = "Responde solamente OK"
TIMEOUT = 90
GAP_S = 67  # >=65s entre inicios

SAFE_HEADERS = {
    "content-type", "retry-after", "x-request-id", "x-google-request-id",
    "x-cloud-trace-context", "date", "server", "via",
    "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
}


def load_env():
    d = {}
    for line in (HERE.parents[2] / ".env").read_text().splitlines():
        if line.strip() and not line.strip().startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def one_shot(url, headers, body_dict):
    """Un solo intento HTTP. Cero retries. Devuelve dict de evidencia saneada."""
    raw = json.dumps(body_dict).encode()
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    t0 = time.monotonic()
    inicio = utcnow()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read().decode("utf-8", "replace")
            dt = time.monotonic() - t0
            hdrs = {k.lower(): v for k, v in r.headers.items()}
            return {
                "inicio_utc": inicio,
                "url": url,  # ya sin secretos (auth por header)
                "body_enviado": body_dict,
                "status": r.status,
                "duracion_s": round(dt, 2),
                "headers_diagnostico": {k: v for k, v in hdrs.items() if k in SAFE_HEADERS},
                "cuerpo": body[:4000],
                "error": None,
            }
    except urllib.error.HTTPError as e:
        dt = time.monotonic() - t0
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = "<ilegible>"
        hdrs = {k.lower(): v for k, v in (e.headers.items() if e.headers else [])}
        return {
            "inicio_utc": inicio,
            "url": url,
            "body_enviado": body_dict,
            "status": e.code,
            "duracion_s": round(dt, 2),
            "headers_diagnostico": {k: v for k, v in hdrs.items() if k in SAFE_HEADERS},
            "cuerpo": body[:4000],
            "error": f"HTTPError {e.code}",
        }
    except Exception as e:
        dt = time.monotonic() - t0
        return {
            "inicio_utc": inicio,
            "url": url,
            "body_enviado": body_dict,
            "status": None,
            "duracion_s": round(dt, 2),
            "headers_diagnostico": {},
            "cuerpo": "",
            "error": f"{type(e).__name__}: {str(e)[:300]}",
        }


env = load_env()
base = env["ONTO_LLM_BASE_URL"].rstrip("/")
assert env["ONTO_LLM_MODEL"] == MODEL, "modelo .env distinto del autorizado"
key = env["ONTO_LLM_API_KEY"]
assert len(key) > 20, "sin credencial"

# (1) OpenAI-compatible actual de Studio
r1 = one_shot(
    f"{base}/chat/completions",
    {"Content-Type": "application/json", "Authorization": "Bearer " + key},
    {"model": MODEL, "messages": [{"role": "user", "content": TEXT}], "max_tokens": 8},
)
(HERE / "req1-openai-compatible.json").write_text(json.dumps(r1, indent=2, ensure_ascii=False) + "\n")

# Espera minima entre inicios (medida desde inicio de r1 no disponible aqui;
# se duerme GAP_S completo tras r1 para garantizar >=65s entre inicios)
time.sleep(GAP_S)

# (2) Nativo Google generateContent, mismo modelo y contenido
r2 = one_shot(
    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
    {"Content-Type": "application/json", "x-goog-api-key": key},
    {"contents": [{"parts": [{"text": TEXT}]}], "generationConfig": {"maxOutputTokens": 8}},
)
(HERE / "req2-nativo-generateContent.json").write_text(json.dumps(r2, indent=2, ensure_ascii=False) + "\n")


def usage_of(r):
    try:
        b = json.loads(r["cuerpo"])
    except Exception:
        return None
    return b.get("usage") or b.get("usageMetadata")


resumen = {
    "fecha_utc": utcnow(),
    "modelo": MODEL,
    "endpoint_openai_compatible": f"{base}/chat/completions",
    "endpoint_nativo": f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
    "r1": {k: r1[k] for k in ("inicio_utc", "status", "duracion_s", "error")} | {"usage": usage_of(r1)},
    "r2": {k: r2[k] for k in ("inicio_utc", "status", "duracion_s", "error")} | {"usage": usage_of(r2)},
    "requests_reales": 2,
    "retries": 0,
}
(HERE / "resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(resumen, indent=2, ensure_ascii=False))
