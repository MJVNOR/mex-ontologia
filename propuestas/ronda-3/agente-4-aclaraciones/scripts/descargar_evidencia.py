"""Descarga evidencia oficial publicada para ronda-3 agente-4 (solo lectura del nucleo).

Fuentes: CKAN datos.sonora.gob.mx (API datastore_search / package_show y
descarga de catalogo.xlsx de Fiebre manchada). Todo se guarda UNICAMENTE en
propuestas/ronda-3/agente-4-aclaraciones/fuente/ con manifiesto URL+fecha+SHA.
No modifica el nucleo ni las copias fijadas; solo compara y reporta.
"""
import datetime
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "fuente"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MEX-Ontologi-ronda3-agente4"}
BASE = "https://datos.sonora.gob.mx"

# Diccionarios pertinentes (datastore_search, fuente oficial publicada).
DICCIONARIOS = {
    "12f684e9-f4d5-4714-933d-aa153a812174": "cd3d6e34-3789-479e-9f2b-a717b8419f9c",
    "22202305-2d02-4c49-b216-cc98224357f0": "940de7d8-73ec-4a08-8d26-b7cc97ff17bd",
    "8c0e76ff-3a86-4b1d-beee-b04bebe7df8d": "e819466c-7282-46c5-84e9-65917dd8cc85",
    "251309e5-0309-46ed-9711-77a1dd408eeb": "b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f",
    "2fc2fbc6-e918-4d5d-b907-1191e266b131": "5f2e31dd-83e8-4445-b132-cd0925045941",
    "3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99": "c589afac-79f1-4aac-9ade-e949301bcca3",
    "587a3ccd-a814-4190-8e6f-dfb20ccf44c4": "7e97d026-d773-47b1-a0ec-078cce93fd13",
    "bfb8788b-8ce3-475e-8bbd-dd1c5154c877": "8c1f452e-7967-4c6b-a7b5-f2279360ad6c",
    "33d0a99e-c721-496f-a05e-07646e9ae42a": "5494daa1-09ca-4750-aeac-2558553700e1",
    # Diccionarios de observaciones (Egresos, IMM, Lluvias).
    "f89137ba-d82e-44fe-80c7-cc355f09f9f5": "8993c917-47d8-4304-8141-5f481fe04301",
    "3395795d-b152-4706-b81e-2b562f86a207": "e262a488-69e5-4064-bd2b-191c5c8fc9f9",
    "6713de4e-1e2b-447d-8000-f6ceaabd8473": "8b4edefe-cb1a-401c-90c6-05548779defd",
}

CONJUNTOS = sorted(set(DICCIONARIOS.values()) | {
    "df2d60f5-2243-4bb0-885a-941aa8a657f5",  # Nacimientos 2024 (esquema a-o)
    "c6140d53-1f16-4dd8-8ab3-d2b47f03a921",  # Divorcios 2023 (resuelto, testigo)
})

# Diccionarios xlsx sin datastore (descarga directa oficial) + diccionario
# Nacimientos-2024 del conjunto df2d60f5 (datastore aparte, abajo).
XLSX = {
    "diccionario_251309e5.xlsx":
        "https://datos.sonora.gob.mx/dataset/b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f"
        "/resource/251309e5-0309-46ed-9711-77a1dd408eeb/download/diccionario.xlsx",
    "diccionario_587a3ccd.xlsx":
        "https://datos.sonora.gob.mx/dataset/7e97d026-d773-47b1-a0ec-078cce93fd13"
        "/resource/587a3ccd-a814-4190-8e6f-dfb20ccf44c4/download/diccionario_produccion-minera.xlsx",
    "diccionario_bfb8788b.xlsx":
        "https://datos.sonora.gob.mx/dataset/8c1f452e-7967-4c6b-a7b5-f2279360ad6c"
        "/resource/bfb8788b-8ce3-475e-8bbd-dd1c5154c877/download/diccionario.xlsx",
    "diccionario_3395795d.xlsx":
        "https://datos.sonora.gob.mx/dataset/e262a488-69e5-4064-bd2b-191c5c8fc9f9"
        "/resource/3395795d-b152-4706-b81e-2b562f86a207/download/diccionario.xlsx",
}

# Datastore del recurso de datos Nac2024 + su diccionario 6bcf5b63, y cabecera
# cruda del CSV (primeros 601 bytes) para la cuestion de codificacion a–o/año.
EXTRA_DATASTORE = {
    "datastore_ffca84a8-155e-41af-8223-0e098966cadf.json":
        f"{BASE}/api/3/action/datastore_search?resource_id=ffca84a8-155e-41af-8223-0e098966cadf&limit=1&offset=0",
    "datastore_6bcf5b63-0855-4f3b-81a0-4bca82e97272.json":
        f"{BASE}/api/3/action/datastore_search?resource_id=6bcf5b63-0855-4f3b-81a0-4bca82e97272&limit=50&offset=0&sort=_id+asc",
}
CSV_HEAD_URL = ("https://datos.sonora.gob.mx/dataset/df2d60f5-2243-4bb0-885a-941aa8a657f5"
                "/resource/ffca84a8-155e-41af-8223-0e098966cadf/download/nacimientos-2024.csv")

CATALOGO_FIEBRE = (
    "https://datos.sonora.gob.mx/dataset/5494daa1-09ca-4750-aeac-2558553700e1"
    "/resource/08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8/download/catalogo.xlsx"
)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ahora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifiesto = {"generado_en_utc": ahora, "archivos": {}}

    def guardar(nombre, url, datos: bytes):
        p = OUT / nombre
        p.write_bytes(datos)
        sha = hashlib.sha256(datos).hexdigest()
        manifiesto["archivos"][nombre] = {
            "url": url, "fecha_utc": ahora,
            "sha256": sha, "bytes": len(datos),
        }
        print(f"{nombre}: {len(datos)} bytes sha256={sha[:16]}...")
        return sha

    for rid, conj in DICCIONARIOS.items():
        url = (f"{BASE}/api/3/action/datastore_search?resource_id={rid}"
               f"&limit=1000&offset=0&sort=_id+asc")
        try:
            raw = get(url)
            payload = json.loads(raw.decode("utf-8"))
            assert payload.get("success") is True, "success!=True"
            guardar(f"datastore_{rid}.json", url, raw)
        except Exception as e:  # noqa: BLE001 - se registra y se sigue
            print(f"AVISO {rid}: {type(e).__name__}: {e}")
            manifiesto["archivos"][f"datastore_{rid}.json"] = {
                "url": url, "fecha_utc": ahora, "error": f"{type(e).__name__}: {e}",
            }

    for conj in CONJUNTOS:
        url = f"{BASE}/api/3/action/package_show?id={conj}"
        try:
            raw = get(url)
            payload = json.loads(raw.decode("utf-8"))
            assert payload.get("success") is True, "success!=True"
            guardar(f"package_{conj}.json", url, raw)
        except Exception as e:  # noqa: BLE001
            print(f"AVISO package {conj}: {type(e).__name__}: {e}")
            manifiesto["archivos"][f"package_{conj}.json"] = {
                "url": url, "fecha_utc": ahora, "error": f"{type(e).__name__}: {e}",
            }

    try:
        raw = get(CATALOGO_FIEBRE)
        guardar("catalogo_fiebre_08d3b1a7.xlsx", CATALOGO_FIEBRE, raw)
    except Exception as e:  # noqa: BLE001
        print(f"AVISO catalogo fiebre: {type(e).__name__}: {e}")
        manifiesto["archivos"]["catalogo_fiebre_08d3b1a7.xlsx"] = {
            "url": CATALOGO_FIEBRE, "fecha_utc": ahora,
            "error": f"{type(e).__name__}: {e}",
        }

    for nombre, url in XLSX.items():
        try:
            guardar(nombre, url, get(url))
        except Exception as e:  # noqa: BLE001
            print(f"AVISO {nombre}: {type(e).__name__}: {e}")
            manifiesto["archivos"][nombre] = {
                "url": url, "fecha_utc": ahora, "error": f"{type(e).__name__}: {e}",
            }

    for nombre, url in EXTRA_DATASTORE.items():
        try:
            guardar(nombre, url, get(url))
        except Exception as e:  # noqa: BLE001
            print(f"AVISO {nombre}: {type(e).__name__}: {e}")
            manifiesto["archivos"][nombre] = {
                "url": url, "fecha_utc": ahora, "error": f"{type(e).__name__}: {e}",
            }

    try:
        req = urllib.request.Request(CSV_HEAD_URL, headers={**UA, "Range": "bytes=0-600"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
        guardar("nacimientos-2024_head.bin",
                CSV_HEAD_URL + " (primeros 601 bytes, encabezado)", raw)
    except Exception as e:  # noqa: BLE001
        print(f"AVISO nac2024 head: {type(e).__name__}: {e}")
        manifiesto["archivos"]["nacimientos-2024_head.bin"] = {
            "url": CSV_HEAD_URL, "fecha_utc": ahora, "error": f"{type(e).__name__}: {e}",
        }

    (OUT / "manifiesto-fuentes.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK manifiesto-fuentes.json")


if __name__ == "__main__":
    main()
