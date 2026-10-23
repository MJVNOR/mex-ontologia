"""Consulta metadatos CKAN; no descarga los archivos de los recursos."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API = "https://datos.sonora.gob.mx/api/3/action/package_search"


def consultar_catalogo(page_size=25):
    registros = {}
    inicio = 0
    total_inicial = None
    while True:
        url = f"{API}?{urlencode({'rows': page_size, 'start': inicio, 'sort': 'id asc'})}"
        request = Request(url, headers={"User-Agent": "MEX-Ontologi/0.1 (catalog metadata exploration)"})
        with urlopen(request, timeout=60) as response:
            payload = json.load(response)
        if not payload.get("success"):
            raise RuntimeError(f"CKAN rechazó la consulta: {payload.get('error')}")
        resultado = payload["result"]
        total = resultado["count"]
        if total_inicial is None:
            total_inicial = total
        if total != total_inicial:
            raise RuntimeError("El tamaño del catálogo cambió durante la consulta; vuelve a ejecutar.")
        pagina = resultado["results"]
        if not pagina and inicio < total:
            raise RuntimeError("La API devolvió una página vacía antes de completar el catálogo.")
        for registro in pagina:
            if registro["id"] in registros:
                raise RuntimeError("Se repitió un identificador durante la paginación; vuelve a ejecutar.")
            registros[registro["id"]] = registro
        inicio += len(pagina)
        print(f"Metadatos consultados: {inicio}/{total}")
        if inicio >= total:
            break
    if len(registros) != total_inicial:
        raise RuntimeError("El número de registros no coincide con el total declarado.")
    return list(registros.values())


def presente(valor):
    return valor is not None and valor != "" and valor != [] and valor != {}


def inventario_campos(registros):
    campos = sorted({campo for registro in registros for campo in registro})
    return {
        campo: {
            "presente": sum(campo in registro for registro in registros),
            "con_valor": sum(presente(registro.get(campo)) for registro in registros),
            "tipos": sorted({type(registro[campo]).__name__ for registro in registros if campo in registro}),
        }
        for campo in campos
    }


def resumir(registros):
    recursos = [recurso for registro in registros for recurso in registro.get("resources", [])]
    organizaciones = {}
    grupos = Counter()
    formatos = Counter()
    for registro in registros:
        org = registro.get("organization")
        if org:
            organizaciones[org["id"]] = org.get("title") or org.get("name")
        grupos.update(grupo.get("title") or grupo.get("name") for grupo in registro.get("groups", []))
    formatos.update(str(recurso.get("format") or "SIN FORMATO").upper() for recurso in recursos)
    campos = inventario_campos(registros)
    return {
        "fuente": API,
        "consultado_en_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": "Metadatos de conjuntos públicos devueltos por package_search; sin descargar recursos.",
        "conjuntos": len(registros),
        "recursos": len(recursos),
        "organizaciones_con_conjuntos": len(organizaciones),
        "organizaciones": organizaciones,
        "grupos": dict(grupos.most_common()),
        "formatos": dict(formatos.most_common()),
        "campos_conjuntos": campos,
        "campos_recursos": inventario_campos(recursos),
        "valores_campos_recursos": {
            campo: dict(Counter(str(recurso.get(campo)) for recurso in recursos if presente(recurso.get(campo))).most_common())
            for campo in ("start_date", "end_date", "region", "datastore_active")
        },
        "alertas": {
            "recursos_sin_url": sum(not presente(r.get("url")) for r in recursos),
            "recursos_region_guion": sum(r.get("region") == "-" for r in recursos),
            "recursos_intervalo_1989_06_04": sum(r.get("start_date") == r.get("end_date") == "1989-06-04" for r in recursos),
            "conjuntos_sin_grupo": sum(not d.get("groups") for d in registros),
        },
        "valores_campos_especiales": {
            campo: dict(Counter(str(registro.get(campo)) for registro in registros if presente(registro.get(campo))).most_common())
            for campo in ("frequency", "granularidad_datos", "jurisdiccion", "license_id")
        },
        "inventario": [
            {
                "id": registro["id"],
                "titulo": registro.get("title"),
                "organizacion_id": (registro.get("organization") or {}).get("id"),
                "grupos": [grupo.get("name") for grupo in registro.get("groups", [])],
                "etiquetas": [tag.get("name") for tag in registro.get("tags", [])],
                "recursos": [
                    {campo: recurso.get(campo) for campo in ("id", "name", "format", "url", "datastore_active")}
                    for recurso in registro.get("resources", [])
                ],
            }
            for registro in registros
        ],
    }


def markdown(resumen):
    lineas = [
        "# Diagnóstico del catálogo de Sonora", "",
        f"Consulta UTC: {resumen['consultado_en_utc']}", "",
        f"Fuente: {API}", "",
        resumen["alcance"], "",
        f"- Conjuntos: {resumen['conjuntos']}",
        f"- Recursos referenciados: {resumen['recursos']}",
        f"- Organizaciones con conjuntos: {resumen['organizaciones_con_conjuntos']}", "",
        "Los conteos describen esta consulta; no prueban la disponibilidad de las descargas ni la calidad del contenido.", "",
        "## Formatos declarados", "", "| Formato | Recursos |", "| --- | ---: |",
    ]
    lineas.extend(f"| {formato} | {cantidad} |" for formato, cantidad in resumen["formatos"].items())
    alertas = resumen["alertas"]
    lineas.extend(["", "## Hallazgos para el modelo", "",
                   f"- {alertas['conjuntos_sin_grupo']} conjuntos sin grupo temático.",
                   f"- {alertas['recursos_sin_url']} recursos sin URL.",
                   f"- {alertas['recursos_region_guion']} recursos con región declarada como guion; no tratarlo como un lugar.",
                   f"- {alertas['recursos_intervalo_1989_06_04']} recursos declaran inicio y fin iguales a 1989-06-04. Es un patrón que requiere revisión; no se ha confirmado si es un valor por defecto o una cobertura real.",
                   "- datastore_active indica una posible vía para consultar filas; todavía no se verificaron esas consultas.",
                   "- Se cuentan organizaciones presentes en conjuntos, no todas las organizaciones registradas en el portal."])
    for titulo, clave, total in (
        ("Campos de los conjuntos", "campos_conjuntos", resumen["conjuntos"]),
        ("Campos de los recursos", "campos_recursos", resumen["recursos"]),
    ):
        lineas.extend(["", f"## {titulo}", "", "| Campo | Presente | Con valor | Sin valor o ausente |", "| --- | ---: | ---: | ---: |"])
        for campo, perfil in resumen[clave].items():
            lineas.append(f"| `{campo}` | {perfil['presente']} | {perfil['con_valor']} | {total - perfil['con_valor']} |")
    lineas.extend(["", "## Alcance de los indicadores", "",
                   "‘Con valor’ excluye null, cadenas vacías, listas vacías y objetos vacíos. No verifica significado, vigencia ni validez de URLs.", "",
                   "Las fechas metadata_created y metadata_modified describen el registro del catálogo; no deben asumirse como fechas de los datos.", "",
                   "Los valores de campos especiales y el inventario de conjuntos están en catalogo-perfil.json.", ""])
    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page-size", type=int, default=25)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "reports")
    args = parser.parse_args()
    if not 1 <= args.page_size <= 1000:
        parser.error("--page-size debe estar entre 1 y 1000")
    resumen = resumir(consultar_catalogo(args.page_size))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "catalogo-perfil.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "catalogo-diagnostico.md").write_text(markdown(resumen), encoding="utf-8")
    print(f"Diagnóstico guardado en {args.output}")


if __name__ == "__main__":
    main()
