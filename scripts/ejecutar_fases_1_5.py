"""Fases 1-5 sobre backend MCP efimero en copia temporal. Prod intacto, sin escritura de agentes."""
import json, os, secrets, socket, subprocess, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EXE = str(ROOT / "tools" / "open-ontologies.exe")
ALLOW = ("onto_query,onto_stats,onto_status,onto_validate,onto_shacl,onto_load,"
         "onto_conservative_check,onto_module_extract,onto_justify,onto_provenance,"
         "onto_support_check,onto_support_report,onto_support_verdict,onto_cq_run,"
         "onto_verify_cq,onto_cq_verdicts_list,onto_pack,onto_lineage")


class Backend:
    def __init__(self, store):
        env = dict(os.environ, OPEN_ONTOLOGIES_STORAGE_MODE="persistent")
        subprocess.run([EXE, "--no-connect", "--data-dir", str(store), "load",
                        str(ROOT / "data" / "portal" / "portal-completo.ttl")],
                       check=True, capture_output=True, env=env)
        self.token = secrets.token_urlsafe(16)
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        self.port = s.getsockname()[1]
        s.close()
        self.url = f"http://127.0.0.1:{self.port}/mcp"
        self.proc = subprocess.Popen(
            [EXE, "serve-http", "--host", "127.0.0.1", "--port", str(self.port),
             "--storage-mode", "persistent", "--data-dir", str(store),
             "--tools-allow", ALLOW],
            env={**env, "OPEN_ONTOLOGIES_TOKEN": self.token},
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.sid = None
        for _ in range(100):
            if self.proc.poll() is not None:
                raise RuntimeError("serve murio")
            try:
                self._rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                         "clientInfo": {"name": "fases", "version": "0"}})
                break
            except OSError:
                time.sleep(0.2)

    def _rpc(self, method, params):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "Authorization": "Bearer " + self.token, "MCP-Protocol-Version": "2025-03-26"}
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        r = urlopen(Request(self.url, data=json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
            headers=h), timeout=300)
        self.sid = r.headers.get("Mcp-Session-Id", self.sid)
        raw = r.read().decode()
        for ln in raw.splitlines():
            if ln.startswith("data:") and ln[5:].strip():
                return json.loads(ln[5:])
        return json.loads(raw)

    def call(self, name, args):
        res = self._rpc("tools/call", {"name": name, "arguments": args})
        if "error" in res:
            return {"_error": res["error"]}
        result = res.get("result", {})
        if result.get("isError"):
            return {"_tool_error": result.get("content")}
        if "structuredContent" in result:
            return result["structuredContent"]
        try:
            return json.loads("\n".join(c["text"] for c in result.get("content", [])
                                        if c.get("type") == "text"))
        except Exception:
            return {"_raw": result.get("content")}

    def close(self):
        self.proc.terminate()


def main():
    tmp = Path(tempfile.mkdtemp(prefix="mex-fases-"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    be = Backend(tmp / "store")
    rep = {}
    try:
        # Fase 1: puente realista variable -> concepto (subClassOf) con significado documentado
        q = ('PREFIX mex: <https://example.org/mex-ontologi/vocab/> '
             'SELECT ?v ?c WHERE { ?v mex:significadoDocumentado ?c . }')
        r = be.call("onto_query", {"query": q + " LIMIT 1"})
        rows = r.get("results", [])
        v = rows[0]["v"].strip("<>") if rows else ""
        c = rows[0]["c"].strip("<>") if rows else ""
        ext = f"<{v}> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <{c}> ."
        out1 = tmp / "cons"
        rep["f1_puente"] = ext
        rep["f1"] = be.call("onto_conservative_check",
                            {"extension_ttl": ext, "out_dir": str(out1), "profile": "rdfs"})
        # Fase 2: justificacion + proveniencia de una conclusion derivada real (rdfs9)
        q2 = ('PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
              'SELECT ?x ?a ?b WHERE { ?x a ?a . ?a rdfs:subClassOf ?b . } LIMIT 5')
        r2 = be.call("onto_query", {"query": q2})
        rows2 = r2.get("results", [])
        if rows2:
            x = rows2[0]["x"]
            concl = f"{x} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> {rows2[0]['b']}"
            rep["f2_conclusion"] = concl
            rep["f2_justify"] = be.call("onto_justify", {"triple": concl, "profile": "rdfs"})
            rep["f2_provenance"] = be.call("onto_provenance",
                                           {"triple": concl, "profile": "rdfs",
                                            "semirings": ["boolean", "lineage"]})
        else:
            rep["f2"] = {"nota": "sin patron x-a-b en el grafo", "query": r2}
        # Fase 3: soporte
        rep["f3_check"] = be.call("onto_support_check", {"limit": 10})
        rep["f3_report"] = be.call("onto_support_report", {})
        # Fase 4: 3 CQs reales
        cqs = json.dumps([
            {"id": "sig-municipio", "question": "Significado documentado de Municipio",
             "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                        "PREFIX skos: <http://www.w3.org/2004/02/skos/core#> "
                        "SELECT ?s WHERE { ?v mex:nombreVariableLocal \"Municipio\" . "
                        "?v mex:significadoDocumentado/skos:prefLabel ?s . } LIMIT 5")},
            {"id": "corr-revisadas", "question": "Correspondencias con revision documental",
             "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                        "SELECT (COUNT(?c) AS ?n) WHERE { ?c mex:estadoCorrespondencia "
                        "\"documental_revisada\" . } LIMIT 1"), "expected_min_rows": 1},
            {"id": "vars-totales", "question": "Cuantas variables documentadas hay",
             "sparql": ("PREFIX mex: <https://example.org/mex-ontologi/vocab/> "
                        "SELECT (COUNT(DISTINCT ?v) AS ?n) WHERE { "
                        "?v a mex:VariableDocumentada . } LIMIT 1"), "expected_min_rows": 1}])
        rep["f4"] = be.call("onto_cq_run", {"cqs_json": cqs})
        # Fase 5: pack + lineage (pack escribe en temporal, no en prod)
        rep["f5_pack"] = be.call("onto_pack", {"path": str(tmp / "pack"), "name": "mex-sonora",
                                              "version": "demo-1"})
        rep["f5_lineage"] = be.call("onto_lineage", {})
    finally:
        be.close()
    (ROOT / "reports" / f"fases-1-5-{stamp}.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    resumen = {}
    for k, v in rep.items():
        s = str(v)
        resumen[k] = s[:300].encode("ascii", "replace").decode("ascii")
    print(json.dumps(resumen, indent=1)[:3000])


if __name__ == "__main__":
    main()
