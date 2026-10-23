"""Descarga evidencia primaria CMPE 2016 (INEGI). Escribe solo en evidencia/externa/."""
import urllib.request, hashlib, datetime, pathlib, json
BASE = pathlib.Path(__file__).parent
OUT = BASE / "evidencia" / "externa"
OUT.mkdir(parents=True, exist_ok=True)
URLS = [
 "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825086664.pdf",
 "https://snieg.mx/SNIEG_Canal/Material2021/docs/clasificador_cmpe.pdf",
]
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
man = {"fecha_utc": utc, "intentos": []}
for u in URLS:
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "MEX-Ontologi-agente4-vigencia/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
        sha = hashlib.sha256(body).hexdigest()
        fn = OUT / ("cmpe2016_inegi.pdf" if "702825086664" in u else "cmpe2016_snieg.pdf")
        fn.write_bytes(body)
        man["intentos"].append({"url": u, "ok": True, "archivo": f"evidencia/externa/{fn.name}",
                                "bytes": len(body), "sha256": sha, "fecha_utc": utc})
        print("OK", u, len(body), sha[:16])
    except Exception as e:
        man["intentos"].append({"url": u, "ok": False, "error": repr(e), "fecha_utc": utc})
        print("FALLO", u, repr(e)[:200])
(OUT / "manifiesto_externa.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
