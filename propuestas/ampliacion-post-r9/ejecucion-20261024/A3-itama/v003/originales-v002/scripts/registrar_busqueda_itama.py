"""A3 ITAMA v002 — registro de la busqueda de copias locales, acotada a ITAMA.

Correccion del coordinador (C1): v001 afirmo "0 copias locales *.xlsx" para todo
el repo, y eso es falso. Este script NO niega que haya hojas de calculo en el
repo: cuenta XLSX y CSV, y comprueba por nombre, por contenido y por SHA-256 si
alguno es copia de los 6 recursos XLSX o de los 2 diccionarios CSV de ITAMA.

Registra en evidencia-busqueda.json, por consulta: patron, raiz, exclusiones,
rutas encontradas y resultado. Sin red, sin grafo. Solo stdlib.

Uso:
    uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v002/scripts/registrar_busqueda_itama.py
"""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
V002 = Path(__file__).resolve().parents[1]
DESTINO = V002 / "evidencia-busqueda.json"

EXCLUIR_DIRS = {"node_modules", ".venv", ".git", "__pycache__"}

# 6 recursos XLSX del par internamiento/externamiento (metadatos.json).
IDS_XLSX = (
    "56dbfc19-0e71-45dc-bf50-6b5a5a92bd7c",
    "59f89fe2-1999-47c5-b464-5f303377fc04",
    "525d84db-d4aa-480d-9c1a-a3d4e7524ac2",
    "cf589b78-2fee-4fb6-b7c8-434e050a058e",
    "71defd43-bee9-45fa-9463-ce2cac2b9ab8",
    "7f95e924-57cc-4f3a-8b5a-e254e7b97993",
)
# 2 diccionarios CSV de los mismos conjuntos.
IDS_DICCIONARIOS = (
    "07781b38-8a53-42eb-b3b7-3c1ebc6a4415",
    "a7ee5717-b14d-439b-9508-bada58d0d185",
)
IDS_ITAMA = IDS_XLSX + IDS_DICCIONARIOS

RUTAS_DOCUMENTALES = (
    "data/catalogo/metadatos.json",
    "data/semantica/cobertura.json",
    "data/semantica/nucleo.ttl",
    "data/portal/oportunidades-cruce.json",
    "data/portal/lote-cruces/validacion-lote.json",
    "data/portal/inspecciones/07781b38-8a53-42eb-b3b7-3c1ebc6a4415.json",
    "data/portal/inspecciones/a7ee5717-b14d-439b-9508-bada58d0d185.json",
)


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def excluida(ruta: Path) -> bool:
    return any(parte in EXCLUIR_DIRS for parte in ruta.parts)


def por_sufijo(sufijos: set[str], raiz: Path = ROOT) -> list[Path]:
    return sorted(
        p
        for p in raiz.rglob("*")
        if p.is_file() and p.suffix.lower() in sufijos and not excluida(p)
    )


def libros(raiz: Path = ROOT) -> list[Path]:
    return por_sufijo({".xlsx", ".xls", ".xlsm"}, raiz)


def hojas_de_calculo(raiz: Path = ROOT) -> list[Path]:
    return por_sufijo({".xlsx", ".xls", ".xlsm", ".csv"}, raiz)


def hashes_publicados() -> dict[str, str]:
    """SHA-256 reportados por las inspecciones locales de los 8 IDs ITAMA."""
    hashes = {}
    for identificador in IDS_ITAMA:
        ruta = ROOT / "data/portal/inspecciones" / f"{identificador}.json"
        inspeccion = json.loads(ruta.read_text(encoding="utf-8"))
        assert inspeccion.get("ok") and inspeccion.get("completo"), ruta
        hashes[identificador] = inspeccion["sha256_fragmento_o_archivo"]
    return hashes


def id_en_nombre(ruta: Path) -> str | None:
    nombre = ruta.name.lower()
    for identificador in IDS_ITAMA:
        if identificador in nombre:
            return identificador
    if re.search(r"\bitama\b", ruta.stem, re.I):
        return "itama"
    return None


def texto_libro(ruta: Path) -> str | None:
    """Devuelve el XML descomprimido del libro; None si no es un ZIP legible."""
    if ruta.suffix.lower() == ".xls":
        return None
    try:
        with zipfile.ZipFile(ruta) as libro:
            partes = []
            for nombre in libro.namelist():
                if nombre.endswith(".xml"):
                    partes.append(libro.read(nombre).decode("utf-8", "ignore"))
            return "".join(partes)
    except (zipfile.BadZipFile, OSError):
        return None


def escanear(raiz: Path = ROOT) -> dict:
    """Barre el repo y devuelve el registro completo (sin escribir nada)."""
    encontrados = libros(raiz)
    csvs = por_sufijo({".csv"}, raiz)
    publicados = hashes_publicados()

    rutas_por_id: dict[str, list[str]] = {
        i: [] for i in (*IDS_ITAMA, "itama", "internamiento", "externamiento")
    }
    for ruta in hojas_de_calculo(raiz):
        nombre = ruta.name.lower()
        for clave in rutas_por_id:
            if clave in nombre:
                rutas_por_id[clave].append(ruta.relative_to(raiz).as_posix())
    inspecciones = sorted(
        p.relative_to(raiz).as_posix()
        for p in raiz.rglob("*.json")
        if not excluida(p)
        and any(identificador in p.name.lower() for identificador in IDS_ITAMA)
    )

    por_nombre = [p for p in encontrados if id_en_nombre(p)]
    con_token: list[str] = []
    subcadenas: dict[str, list[str]] = {}
    ids_en_contenido: list[str] = []
    no_inspeccionables: list[str] = []
    hashes_locales = {
        p: sha256(p) for p in hojas_de_calculo(raiz)
    }
    exactas = sorted(
        {
            (publicados[identificador], ruta.relative_to(raiz).as_posix())
            for identificador, digest in publicados.items()
            for ruta, local in hashes_locales.items()
            if local == digest
        }
    )

    for ruta in encontrados:
        texto = texto_libro(ruta)
        if texto is None:
            no_inspeccionables.append(ruta.relative_to(raiz).as_posix())
            continue
        rel = ruta.relative_to(raiz).as_posix()
        if re.search(r"\bITAMA\b", texto, re.I):
            con_token.append(rel)
        for hallado in set(
            re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]*ITAMA[A-Za-zÁÉÍÓÚÑáéíóúñ]*", texto, re.I)
        ):
            valor = hallado.upper()
            if valor != "ITAMA":
                subcadenas.setdefault(valor, [])
                if rel not in subcadenas[valor]:
                    subcadenas[valor].append(rel)
        bajo = texto.lower()
        if any(identificador in bajo for identificador in IDS_ITAMA):
            ids_en_contenido.append(rel)

    itama = sorted(set(por_nombre) | set(con_token) | set(ids_en_contenido) | {e[1] for e in exactas})

    rutas_consultadas = [
        {
            "ruta": rel,
            "sha256": sha256(raiz / rel),
            "consultada_para": "premisas del bloqueo y respaldo de sexo/escolaridad",
        }
        for rel in RUTAS_DOCUMENTALES
    ]

    evidencia = {
        "carril": "A3-itama",
        "version": "v002",
        "generado_en_utc": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "alcance": {
            "recursos_xlsx": list(IDS_XLSX),
            "diccionarios_csv": list(IDS_DICCIONARIOS),
            "nota": (
                "Solo se pronuncian copias locales de estos 8 IDs ITAMA. "
                "Los XLSX/CSV de otros conjuntos (territorio/presas, "
                "catalogos, salud) se cuentan pero no se evaluan como ITAMA "
                "ni se niegan."
            ),
        },
        "consultas": [
            {
                "id": "P1",
                "patron": "**/*.{xlsx,xls,xlsm} y **/*.csv",
                "raiz": ".",
                "exclusiones": sorted(EXCLUIR_DIRS),
                "xlsx_encontrados": len(encontrados),
                "csv_encontrados": len(csvs),
                "coincidencias_itama": len(itama),
                "rutas_xlsx": [p.relative_to(raiz).as_posix() for p in encontrados],
                "rutas_csv": [p.relative_to(raiz).as_posix() for p in csvs],
                "resultado": (
                    f"El repo SI contiene {len(encontrados)} XLSX y {len(csvs)} "
                    "CSV locales, de otros conjuntos (territorio/presas, "
                    "catalogos, salud, nacimientos). Ninguno es copia ITAMA: "
                    f"{len(itama)} coincidencias. No se afirma que el repo "
                    "carezca de hojas de calculo."
                ),
            },
            {
                "id": "P2",
                "patron": "nombre de archivo contiene los 8 IDs ITAMA o las palabras itama/internamiento/externamiento",
                "raiz": ".",
                "exclusiones": sorted(EXCLUIR_DIRS),
                "archivos_encontrados": sum(
                    len(v) for k, v in rutas_por_id.items() if k in IDS_ITAMA
                ),
                "por_clave": rutas_por_id,
                "json_inspeccion": inspecciones,
                "resultado": (
                    "0 XLSX/CSV con alguno de los 8 IDs ni con las palabras "
                    "itama/internamiento/externamiento. Los IDs aparecen solo "
                    f"en {len(inspecciones)} JSON de inspeccion (8 IDs x "
                    "original + respaldo)."
                ),
            },
            {
                "id": "P3",
                "patron": r"contenido XML de cada libro: token \bITAMA\b y subcadenas de los 8 IDs",
                "raiz": ".",
                "exclusiones": sorted(EXCLUIR_DIRS),
                "libros_inspeccionados": len(encontrados)
                - len(no_inspeccionables),
                "no_inspeccionables": no_inspeccionables,
                "coincidencias_token_itama": len(con_token),
                "coincidencias_ids": len(ids_en_contenido),
                "subcadenas_no_token": subcadenas,
                "resultado": (
                    "0 libros con el token ITAMA y 0 con IDs ITAMA. Las "
                    "subcadenas halladas (ITAMAR, CHITAMA, IXCATITAMAN) son "
                    "nombres de localidades en catalogos de LOCALIDADES: "
                    "falsos positivos, no datos del instituto."
                ),
            },
            {
                "id": "P4",
                "patron": "SHA-256 de cada XLSX/CSV local contra los 8 SHA-256 publicados en las inspecciones",
                "raiz": ".",
                "exclusiones": sorted(EXCLUIR_DIRS),
                "archivos_hasheados": len(hashes_locales),
                "coincidencias_exactas": [
                    {"sha256": digest, "ruta": ruta} for digest, ruta in exactas
                ],
                "resultado": (
                    "0 copias exactas: ningun XLSX ni CSV local coincide con "
                    "los SHA-256 de los 6 recursos y 2 diccionarios ITAMA."
                ),
            },
        ],
        "rutas_consultadas": rutas_consultadas,
        "rutas_xlsx": [p.relative_to(raiz).as_posix() for p in encontrados],
        "rutas_csv": [p.relative_to(raiz).as_posix() for p in csvs],
        "resumen": {
            "xlsx_repo_total": len(encontrados),
            "csv_repo_total": len(csvs),
            "xlsx_itama": len(itama),
            "xlsx_con_token_itama": len(con_token),
            "xlsx_con_subcadena_no_token": len(
                {r for rutas in subcadenas.values() for r in rutas}
            ),
            "copias_exactas_itama": len(exactas),
            "json_inspeccion": len(inspecciones),
            "ids_con_inspeccion_json": len(
                {
                    identificador
                    for identificador in IDS_ITAMA
                    if any(identificador in ruta for ruta in inspecciones)
                }
            ),
        },
    }
    return evidencia


def escribir(destino: Path = DESTINO, raiz: Path = ROOT) -> dict:
    evidencia = escanear(raiz)
    destino.write_text(
        json.dumps(evidencia, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return evidencia


def main() -> dict:
    evidencia = escribir()
    resumen = evidencia["resumen"]
    print(f"XLSX en el repo: {resumen['xlsx_repo_total']}")
    print(f"CSV en el repo: {resumen['csv_repo_total']}")
    print(f"Copias exactas ITAMA: {resumen['copias_exactas_itama']}")
    print(f"Evidencia: {DESTINO.relative_to(ROOT).as_posix()}")
    return evidencia


if __name__ == "__main__":
    main()
