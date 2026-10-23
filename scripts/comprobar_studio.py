"""Comprueba el contrato HTTP/MCP que Studio usa con el motor, sin abrir la interfaz."""

import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import time
import tomllib
from urllib.error import URLError
from urllib.request import Request, urlopen
from rdflib.util import from_n3

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8137"


def api(path, payload=None, headers=None):
    request = Request(
        BASE + path,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={"Content-Type": "application/json", **(headers or {})},
    )
    with urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8")
        if body.startswith("event:") or body.startswith("data:"):
            messages = [json.loads(line[5:].strip()) for line in body.splitlines() if line.startswith("data:") and line[5:].strip()]
            result = next((m for m in messages if "id" in m), messages[-1] if messages else {})
        else:
            result = json.loads(body) if body else None
        return result, dict(response.headers)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, default=ROOT / "tools/open-ontologies.exe")
    args = parser.parse_args()
    # No conectar con otro proceso ni terminarlo si el puerto ya está en uso.
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 8137))
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    log_path = reports / "studio-motor.log"
    base_iri = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]["base_iri"]
    cmd = [str(args.engine.resolve()), "--data-dir", str(ROOT / "store/studio-check"),
           "serve-http", "--host", "127.0.0.1", "--port", "8137", "--storage-mode", "memory"]
    env = dict(os.environ)
    env.pop("OPEN_ONTOLOGIES_TOKEN", None)
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(cmd, stdout=log, stderr=log, env=env,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            deadline = time.monotonic() + 20
            while True:
                if process.poll() is not None:
                    raise RuntimeError("El motor terminó. Consulta reports/studio-motor.log")
                try:
                    stats, _ = api("/api/stats")
                    break
                except (URLError, TimeoutError):
                    if time.monotonic() >= deadline:
                        raise RuntimeError("El motor no respondió antes del plazo")
                    time.sleep(0.25)
            result = {"alcance": "Prueba de integración del motor con los endpoints usados por Studio; no prueba de interfaz Tauri", "motor": str(args.engine.resolve()), "url": BASE, "cargas": []}
            for name in ("ontologia.ttl", "catalogo.ttl"):
                loaded, _ = api("/api/load", {"path": str(ROOT / "data/catalogo" / name)})
                if loaded.get("error") or loaded.get("ok") is False:
                    raise RuntimeError(str(loaded))
                result["cargas"].append(loaded)
            result["stats"], _ = api("/api/stats")
            for name, query in {
                "datasets": "SELECT (COUNT(?d) AS ?n) WHERE { ?d a <http://www.w3.org/ns/dcat#Dataset> }",
                "recursos": "SELECT (COUNT(?r) AS ?n) WHERE { ?r a <" + base_iri + "vocab/RecursoCatalogado> }",
                "studio_classes": "PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?c ?l WHERE { { ?c a owl:Class } UNION { ?c rdfs:subClassOf ?x } OPTIONAL { ?c rdfs:label ?l } FILTER(!isBlank(?c)) } LIMIT 300",
                "studio_edges": "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?a ?b WHERE { ?a rdfs:subClassOf ?b . FILTER(!isBlank(?a) && !isBlank(?b)) }",
            }.items():
                result[name], _ = api("/api/query", {"query": query})
            result["studio_sparql_compatible"] = isinstance(result["datasets"].get("results"), dict) and "bindings" in result["datasets"]["results"]
            def bindings(name):
                data = result[name]["results"]
                if isinstance(data, dict):
                    return [{key: value["value"] for key, value in row.items()} for row in data["bindings"]]
                return [{key: from_n3(value).toPython() for key, value in row.items()} for row in data]
            # El frontend de Studio espera JSON SPARQL con results.bindings y value.
            manifest = json.loads((ROOT / "reports/catalogo-carga.json").read_text(encoding="utf-8"))
            for query, count in (("datasets", manifest["conjuntos"]), ("recursos", manifest["recursos"])):
                assert int(bindings(query)[0]["n"]) == count
            init, headers = api("/mcp", {
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "mex-ontologi-check", "version": "0.1.0"}},
            }, {"Accept": "application/json, text/event-stream"})
            if "result" not in init:
                raise RuntimeError("MCP initialize falló: " + str(init))
            result["mcp_initialize"] = init
            session = next((v for k, v in headers.items() if k.lower() == "mcp-session-id"), None)
            session_headers = {"Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2025-03-26"}
            if session:
                session_headers["Mcp-Session-Id"] = session
            api("/mcp", {"jsonrpc": "2.0", "method": "notifications/initialized"}, session_headers)
            tools, _ = api("/mcp", {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session_headers)
            names = [t["name"] for t in tools.get("result", {}).get("tools", [])]
            if "onto_query" not in names:
                raise RuntimeError("No se obtuvo onto_query en MCP tools/list")
            result["mcp_tools_count"] = len(names)
            query_result, _ = api("/mcp", {
                "jsonrpc": "2.0", "id": 3, "method": "tools/call",
                "params": {"name": "onto_query", "arguments": {"query": "SELECT (COUNT(?d) AS ?n) WHERE { ?d a <http://www.w3.org/ns/dcat#Dataset> }"}},
            }, session_headers)
            if query_result.get("error") or query_result.get("result", {}).get("isError"):
                raise RuntimeError("Falló onto_query por MCP: " + str(query_result))
            result["mcp_query"] = query_result
            result["servidor_cerrado_al_final"] = True
            (reports / "studio-conexion.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({"conexion_http": "ok", "conexion_mcp": "ok", "contrato_sparql_studio_compatible": result["studio_sparql_compatible"], "triples": result["stats"].get("triples"), "filas_consulta_clases": len(bindings("studio_classes")), "clases_distintas": len({r['c'] for r in bindings('studio_classes')}), "aristas_consulta_jerarquia": len(bindings("studio_edges")), "herramientas_mcp": len(names)}, ensure_ascii=False, indent=2))
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    main()
