"""Fetch CKAN package metadata for vigencia (solo lectura remota, escritura local en este dir)."""
import json, hashlib, datetime, urllib.request, pathlib
BASE = pathlib.Path(__file__).parent
OUT = BASE / "evidencia" / "ckan"
OUT.mkdir(parents=True, exist_ok=True)
CKAN = "https://datos.sonora.gob.mx"
IDS = [
 "403912fd-5853-4e18-8256-f77206f855bd",
 "e5aad52d-5760-481c-ba65-db0ba4a5315e",
 "e7a3d62f-4ace-479c-aa52-1c9e384dc429",
 "85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f",
 "ee8f639f-5e89-46ae-93b9-934b05fc6233",
 "5494daa1-09ca-4750-aeac-2558553700e1",
 "0b5f5e16-2de3-4be1-811f-4b0976ed82d3",
 "943d0723-afbb-470a-8fe8-d62e8671de84",
 "93ca5e1c-702e-4e62-bc61-638907be184a",
 "caf587a5-23ac-496b-85d4-6ceb1d615d78",
 "960ef0a9-73ed-4191-ae0b-b868d7e48292",
]
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "MEX-Ontologi-agente4-vigencia/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    return body
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = {"fecha_utc": utc, "base": CKAN, "paquetes": {}}
for pid in IDS:
    url = f"{CKAN}/api/3/action/package_show?id={pid}"
    try:
        body = fetch(url)
    except Exception as e:
        manifest["paquetes"][pid] = {"url": url, "error": repr(e), "fecha_utc": utc}
        print(pid, "ERROR", e)
        continue
    sha = hashlib.sha256(body).hexdigest()
    fn = OUT / f"package_{pid}.json"
    fn.write_bytes(body)
    try:
        j = json.loads(body)
        res = j.get("result", {}) if j.get("success") else {}
        resources = res.get("resources", [])
        manifest["paquetes"][pid] = {
            "url": url, "fecha_utc": utc, "sha256": sha,
            "bytes": len(body), "archivo": f"evidencia/ckan/package_{pid}.json",
            "success": j.get("success"),
            "titulo": res.get("title"), "nombre": res.get("name"),
            "metadata_created": res.get("metadata_created"),
            "metadata_modified": res.get("metadata_modified"),
            "notas_len": len(res.get("notes") or ""),
            "num_recursos": len(resources),
            "recursos": [{"id": r.get("id"), "name": r.get("name"),
                          "url": r.get("url"), "created": r.get("created"),
                          "last_modified": r.get("last_modified"),
                          "metadata_modified": r.get("metadata_modified"),
                          "mimetype": r.get("mimetype"), "formato": r.get("format"),
                          "tamano": r.get("size")} for r in resources],
        }
        print(pid, res.get("title"), len(resources), res.get("metadata_created"), res.get("metadata_modified"))
    except Exception as e:
        manifest["paquetes"][pid] = {"url": url, "fecha_utc": utc, "sha256": sha, "error_parse": repr(e)}
        print(pid, "PARSE-ERROR", e)
(BASE / "evidencia" / "ckan_manifiesto.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(manifest["paquetes"]))
