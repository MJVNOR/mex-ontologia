"""Descarga binaria CKAN con User-Agent (el portal responde 403 sin cabecera).

Reusa el patrón UA de scripts/inventariar_portal.py y scripts/explorar_catalogo.py.
Uso:
  uv run python scripts/descargar_ckan.py --help
  uv run python scripts/descargar_ckan.py --dataset ef7dfb43-a80f-43b6-96c3-e067b8bf7ad1 --salida data/hermosillo-educacion
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PORTAL = "https://datos.sonora.gob.mx/"
UA = "MEX-Ontologi/0.1 (resource download; contact via portal metadata)"

def _get(url, timeout=60):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as r:
        return r.read(), r.url

def api(action, **params):
    url = PORTAL + "api/3/action/" + action + ("?" + urlencode(params) if params else "")
    raw, _ = _get(url, timeout=30)
    payload = json.loads(raw.decode("utf-8", errors="replace"))
    if not payload.get("success"):
        raise RuntimeError(f"CKAN {action}: {payload.get('error')}")
    return payload["result"]

def descargar(url, destino: Path):
    raw, final = _get(url)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(raw)
    return {"url": url, "final": final, "bytes": len(raw), "destino": str(destino)}

def recursos_dataset(dataset_id):
    pkg = api("package_show", id=dataset_id)
    return [{"id": r["id"], "name": r.get("name"), "format": r.get("format"),
             "url": r.get("url"), "datastore_active": r.get("datastore_active")}
            for r in pkg.get("resources", [])]

HERMOSILLO_EDU = {
    "ef7dfb43-a80f-43b6-96c3-e067b8bf7ad1": ["e6ba941d-c8b9-4392-8725-65e913bf2f22"],
    "85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f": ["7422760b-8f99-4774-a436-c7d1f49c2cc0",
        "3e3bed3e-db98-45a0-89b3-d07fb57cafe6", "ae39974c-131d-48f1-bd25-b368d59db4b6",
        "ad71c81a-01ac-40f2-821d-0b1efd06b487"],
}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", default="")
    p.add_argument("--salida", type=Path, default=Path("data/hermosillo-educacion"))
    args = p.parse_args()
    targets = {args.dataset: None} if args.dataset else HERMOSILLO_EDU
    for ds in targets:
        for r in recursos_dataset(ds):
            if ds in HERMOSILLO_EDU and r["id"] not in HERMOSILLO_EDU[ds]:
                continue
            suf = "." + (r["format"] or "bin").lower()
            dest = args.salida / (r["id"][:8] + "-" + (r["name"] or r["id"]).lower().replace(" ", "-") + suf)
            # nombres estables para el lote Hermosillo ya descargado
            info = descargar(r["url"], dest)
            print(json.dumps({**r, **info}, ensure_ascii=False))

if __name__ == "__main__":
    main()
