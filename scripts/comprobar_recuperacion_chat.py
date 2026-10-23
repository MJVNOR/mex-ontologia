"""Prueba la pregunta del diccionario con un motor aislado y sin modificar el grafo."""

import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUESTION = "¿Qué significa la variable año_matrimonio según su diccionario? Consulta el grafo y muestra la evidencia."


def main():
    config = json.loads((ROOT / "scripts/studio-gemini.json").read_text(encoding="utf-8"))
    installed = Path(config["executable"]).parent
    env = dict(os.environ)
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip().startswith("ONTO_"):
            env[key.strip()] = value.strip().strip('"').strip("'")
    secret = env.get("ONTO_LLM_API_KEY", "")
    env.pop("OPEN_ONTOLOGIES_TOKEN", None)
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    base = f"http://127.0.0.1:{port}"

    def api(path, payload=None):
        req = Request(base + "/api" + path,
                      data=json.dumps(payload).encode() if payload is not None else None,
                      headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=30) as response:
            result = json.load(response)
        if isinstance(result, dict) and (result.get("error") or result.get("ok") is False):
            raise RuntimeError(str(result))
        return result

    with tempfile.TemporaryDirectory(prefix="mex-chat-check-") as temp:
        temp_path = Path(temp)
        env["ONTO_ENGINE_URL"] = base + "/mcp"
        env["OPEN_ONTOLOGIES_STUDIO_PORT"] = str(port)
        env["ONTO_CHAT_CACHE"] = str(temp_path / "answers.json")
        with (temp_path / "engine.log").open("w", encoding="utf-8") as log:
            engine = subprocess.Popen(
                [str(installed / "open-ontologies.exe"), "--data-dir", str(temp_path / "store"),
                 "serve-http", "--host", "127.0.0.1", "--port", str(port), "--storage-mode", "memory"],
                stdout=log, stderr=log, env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
            try:
                deadline = time.monotonic() + 20
                while True:
                    if engine.poll() is not None:
                        raise RuntimeError("El motor de prueba terminó antes de iniciar.")
                    try:
                        api("/stats")
                        break
                    except (URLError, TimeoutError):
                        if time.monotonic() > deadline:
                            raise RuntimeError("El motor de prueba no respondió.")
                        time.sleep(0.2)
                api("/load", {"path": str(ROOT / "data/catalogo/studio-live.ttl")})
                before = api("/stats")["triples"]
                message = json.dumps({"type": "chat", "message": QUESTION, "mode": "sketch"}, ensure_ascii=False)
                run = subprocess.run(
                    [config["node"], str(installed / "sidecars/agent/dist/index.js")],
                    input=message + "\n", text=True, encoding="utf-8", capture_output=True,
                    env=env, timeout=120,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
                output = run.stdout.replace(secret, "[clave omitida]") if secret else run.stdout
                events = [json.loads(line) for line in output.splitlines() if line.strip()]
                errors = [event.get("error") for event in events if event.get("type") == "error"]
                if run.returncode or errors:
                    raise RuntimeError("El agente falló: " + str(errors or run.returncode))
                retrieval = next((e for e in events if e.get("type") == "retrieval"), {})
                answer = "\n".join(e.get("content", "") for e in events if e.get("type") == "text")
                after = api("/stats")["triples"]
                checks = {
                    "recupera_relaciones": retrieval.get("facts", 0) > 0,
                    "incluye_definicion": "año de registro" in answer.lower(),
                    "cita_diccionario": "364ffa5c-e1c2-4185-a22f-80bede6735d0" in answer and "diccionario.csv" in answer,
                    "grafo_sin_cambios": before == after and any(e.get("type") == "done" and e.get("mutated") is False for e in events),
                }
                report = {"pregunta": QUESTION, "modelo": env.get("ONTO_LLM_MODEL"), "triples": before,
                          "recuperacion": retrieval, "comprobaciones": checks, "eventos": events}
                report_path = ROOT / "reports/chat-recuperacion.json"
                report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(json.dumps({"informe": str(report_path), "recuperacion": retrieval, "comprobaciones": checks}, ensure_ascii=False))
                if not all(checks.values()):
                    raise RuntimeError("La respuesta no supera todas las comprobaciones; consulta el informe.")
            finally:
                engine.terminate()
                try:
                    engine.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    engine.kill()
                    engine.wait()


if __name__ == "__main__":
    main()
