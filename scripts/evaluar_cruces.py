"""Item 2: conservative_check sameAs sobre los 98 pares revisar_primero. Guarda incremental."""
import json, os, secrets, socket, subprocess, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EXE = str(ROOT / "tools" / "open-ontologies.exe")
ALLOW = ("onto_query,onto_stats,onto_status,onto_conservative_check,"
         "onto_cq_run,onto_verify_cq,onto_cq_verdicts_list")


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
        for _ in range(120):
            if self.proc.poll() is not None:
                raise RuntimeError("serve murio")
            try:
                self._rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                         "clientInfo": {"name": "cruces", "version": "0"}})
                return
            except OSError:
                time.sleep(0.5)

    def _rpc(self, method, params):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "Authorization": "Bearer " + self.token, "MCP-Protocol-Version": "2025-03-26"}
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        r = urlopen(Request(self.url, data=json.dumps(
            {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
            headers=h), timeout=600)
        self.sid = r.headers.get("Mcp-Session-Id", self.sid)
        raw = r.read().decode()
        for ln in raw.splitlines():
            if ln.startswith("data:") and ln[5:].strip():
                return json.loads(ln[5:])
        return json.loads(raw)

    def call(self, name, args):
        res = self._rpc("tools/call", {"name": name, "arguments": args})
        if "error" in res:
            return {"_error": str(res["error"])[:300]}
        result = res.get("result", {})
        if result.get("isError"):
            return {"_tool_error": str(result.get("content"))[:500]}
        sc = result.get("structuredContent")
        if sc is not None:
            return sc
        try:
            return json.loads("\n".join(c["text"] for c in result.get("content", [])
                                        if c.get("type") == "text"))
        except Exception:
            return {"_raw": str(result.get("content"))[:500]}

    def close(self):
        self.proc.terminate()


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / "reports" / f"cruces-conserv-{stamp}.jsonl"
    tmp = Path(tempfile.mkdtemp(prefix="mex-cruces-"))
    d = json.load(open(ROOT / "data" / "portal" / "oportunidades-cruce.json", encoding="utf-8"))
    pares = [p for p in d["pares"] if p.get("prioridad_revision") == "revisar_primero"
             and p.get("evaluacion_claves")]
    print(f"pares: {len(pares)}", flush=True)
    be = Backend(tmp / "store")
    try:
        for i, p in enumerate(pares):
            ev = p["evaluacion_claves"][0]
            try:
                ca, cb = ev["columnas_a"][0], ev["columnas_b"][0]
                ext = f"<{ca}> <http://www.w3.org/2002/07/owl#sameAs> <{cb}> ."
                r = be.call("onto_conservative_check",
                            {"extension_ttl": ext, "out_dir": str(tmp / f"c{i}"), "profile": "rdfs"})
                row = {"id": p["id"], "a": p["titulo_a"], "b": p["titulo_b"],
                       "familia": ev.get("familia"), "columnas": [ca, cb],
                       "verdict": r.get("conservativity_verdict"), "new": r.get("new_consequences"),
                       "err": r.get("_error") or r.get("_tool_error")}
            except Exception as e:
                row = {"id": p["id"], "err": str(e)[:200]}
            with open(out, "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            if (i + 1) % 10 == 0:
                print(f"{i + 1}/{len(pares)}", flush=True)
    finally:
        be.close()
    print("OK " + str(out))


if __name__ == "__main__":
    main()
