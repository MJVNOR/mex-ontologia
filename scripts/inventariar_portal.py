"""Inventario de cobertura: CKAN, recursos y páginas de datos enlazadas en la portada."""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tomllib
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from rdflib import DCTERMS as DCT, Graph, Namespace, URIRef

from explorar_catalogo import consultar_catalogo

ROOT = Path(__file__).resolve().parents[1]
PORTAL = "https://datos.sonora.gob.mx/"
MAX_BYTES = 2_000_000


def leer(url):
    try:
        request = Request(url, headers={"User-Agent": "MEX-Ontologi/0.1 (public portal metadata inventory)"})
        with urlopen(request, timeout=20) as response:
            content = response.read(MAX_BYTES + 1)
            if len(content) > MAX_BYTES:
                return {"ok": False, "url": url, "error": "Respuesta superior al límite de 2 MB"}
            return {"ok": True, "url": response.url, "status": response.status,
                    "content_type": response.headers.get("Content-Type", ""),
                    "body": content.decode(response.headers.get_content_charset() or "utf-8", errors="replace")}
    except HTTPError as error:
        return {"ok": False, "url": url, "status": error.code, "error": str(error)}
    except (URLError, TimeoutError, OSError) as error:
        return {"ok": False, "url": url, "error": str(error)}


def api(action, **params):
    url = PORTAL + "api/3/action/" + action + ("?" + urlencode(params) if params else "")
    result = leer(url)
    if not result["ok"]:
        return result
    try:
        payload = json.loads(result.pop("body"))
        if not payload.get("success"):
            return {"ok": False, "url": url, "error": payload.get("error")}
        return {"ok": True, "url": url, "result": payload["result"]}
    except (ValueError, KeyError) as error:
        return {"ok": False, "url": url, "error": str(error)}


def normalizar(texto):
    return "".join(c for c in unicodedata.normalize("NFD", str(texto).lower()) if unicodedata.category(c) != "Mn")


def canonica(url):
    parsed = urlsplit(url)
    return urlunsplit((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/") or "/", parsed.query, ""))


def tipo_pagina(url, enlaces):
    if re.fullmatch(r"/datos/equipo\d+dataton", urlsplit(url).path):
        return "analisis_dataton"
    textos = {normalizar(link["text"].strip()) for link in enlaces if canonica(link["url"]) == url}
    if "ir a herramienta" in textos:
        return "herramienta"
    if "ir a historia" in textos:
        return "historia"
    if "ver resultados" in textos:
        return "diagnostico"
    return "pagina_de_datos"


class Enlaces(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.links = []
        self.frames = []
        self.title = []
        self.in_title = False
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "a" and attrs.get("href"):
            self.anchor = {"url": urljoin(self.base, attrs["href"]), "text": ""}
        if tag == "iframe" and attrs.get("src"):
            self.frames.append(urljoin(self.base, attrs["src"]))

    def handle_data(self, value):
        if self.in_title:
            self.title.append(value)
        if self.anchor is not None:
            self.anchor["text"] += value

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.anchor is not None:
            self.anchor["text"] = " ".join(self.anchor["text"].split())
            self.links.append(self.anchor)
            self.anchor = None


def inspeccionar_pagina(entry):
    response = leer(entry["url"])
    result = {**entry, "http": {k: v for k, v in response.items() if k != "body"}}
    if response["ok"] and "html" in response["content_type"]:
        parser = Enlaces(response["url"])
        parser.feed(response["body"])
        result.update(titulo=" ".join(parser.title).strip(), iframes=parser.frames,
                      enlaces=parser.links, metodo_inspeccion="http_html")
        # Joomla asigna el src del iframe desde literales por dispositivo.
        # Se leen esos literales sin ejecutar el JavaScript de la página.
        embeds = []
        for block in re.findall(r"window\.powerbiPaths\s*=\s*\{([^}]+)\}", response["body"]):
            for device, url in re.findall(r"(desktop|tablet|mobile)\s*:\s*['\"]([^'\"]+)['\"]", block):
                if urlsplit(url).scheme in ("http", "https") and urlsplit(url).netloc:
                    embeds.append({"url": url, "dispositivo": device, "evidencia": "literal_window.powerbiPaths"})
        result["visualizaciones_declaradas"] = embeds
        result["destinos_visualizacion"] = sorted(set(parser.frames + [e["url"] for e in embeds]))
    return result


def clasificar(recurso, conjunto=""):
    name = normalizar(recurso.get("name", ""))
    formato = str(recurso.get("format") or "").strip().upper()
    if "diccionario" in name or "dictionary" in name:
        return "diccionario", "Nombre del recurso declara diccionario; contenido pendiente de revisión"
    if formato in {"GEOJSON", "SHP", "KML", "KMZ", "GPKG"} or "geometr" in name or "geometr" in normalizar(conjunto):
        return "candidato_geoespacial", "Formato o nombre geoespacial; esquema pendiente de confirmación"
    if formato in {"CSV", "XLSX", "XLS", "JSON", "PARQUET"}:
        return "datos_estructurados", "Formato declarado; estructura del archivo aún no inspeccionada"
    if formato in {"PDF", "DOC", "DOCX", "TXT"}:
        return "documento", "Formato declarado"
    if formato in {"API", "WMS", "WFS", "SPARQL"}:
        return "servicio_declarado", "Formato de servicio declarado; funcionamiento pendiente"
    return "sin_clasificar", "Metadatos insuficientes"


def comprobar_datastore(resource_id):
    result = api("datastore_search", resource_id=resource_id, limit=0)
    if not result["ok"]:
        return {"resource_id": resource_id, "ok": False, "url": result["url"], "error": result.get("error")}
    body = result["result"]
    return {"resource_id": resource_id, "ok": True, "url": result["url"],
            "total_declarado": body.get("total"),
            "campos": [{"id": f.get("id"), "type": f.get("type"), "info": f.get("info")} for f in body.get("fields", [])],
            "registros_recibidos_descartados": len(body.get("records", []))}


def listar_entidades(tipo):
    nombres = api(tipo + "_list")
    detalles = api(tipo + "_list", all_fields="true", include_dataset_count="true")
    if not nombres["ok"]:
        return nombres
    by_name = {item["name"]: item for item in detalles.get("result", [])} if detalles["ok"] else {}
    for nombre in nombres["result"]:
        if nombre not in by_name:
            detail = api(tipo + "_show", id=nombre, include_datasets="false")
            by_name[nombre] = detail["result"] if detail["ok"] else {"name": nombre, "detalle_pendiente": detail.get("error")}
    return {"ok": True, "url": nombres["url"], "result": [by_name[n] for n in nombres["result"]]}


def escribir_reporte(inventario, path):
    c = inventario["cobertura"]
    lines = ["# Cobertura del portal de datos abiertos de Sonora", "",
             f"Inventario generado en UTC: {inventario['generado_en_utc']}", "",
             "## Alcance", "",
             "Inventario de metadatos públicos CKAN y páginas enlazadas desde la portada. No es un inventario de todo el dominio del Gobierno de Sonora ni una copia de todas las filas de sus archivos.", "",
             "## Cobertura por capa", "", "| Capa | Inventariado | Estado |", "| --- | ---: | --- |",
             f"| Conjuntos CKAN | {c['conjuntos']} | Metadatos consultados por API |",
             f"| Recursos CKAN | {c['recursos']} | Clasificados por metadatos |",
             f"| Organizaciones registradas | {c['organizaciones_registradas']} | Listado simple y detalles de API |",
             f"| Grupos registrados | {c['grupos_registrados']} | Listado de API |",
             f"| Páginas en sonora.gob.mx/datos/ | {c['paginas_datos_descubiertas']} | Enlaces únicos de la portada |",
             f"| DataStore declarado activo | {c['datastore_declarado']} | Se intentó consulta de esquema sin filas |",
             f"| DataStore verificado | {c['datastore_verificado']} | API respondió y devolvió esquema |", "",
             "## Clasificación de recursos", "", "Clasificación inicial por nombre y formato, no por inspección completa del contenido.", "",
             "| Tipo | Recursos |", "| --- | ---: |"]
    lines += [f"| {k} | {v} |" for k, v in inventario["clasificacion_recursos"].items()]
    lines += ["", "## Estado del mapeo del catálogo base", "",
              f"{c['recursos_en_grafo']} recursos coinciden por identificador con catalogo.ttl. Quedan {c['estructuras_pendientes']} recursos sin esquema inspeccionado. Este inventario compara el archivo base y no evalúa ampliaciones posteriores; para el grafo ampliado consultar docs/modelo-portal.md y reports/portal-carga.json.", "",
              f"Organizaciones representadas en el grafo: {sum(x['en_grafo_catalogo'] for x in inventario['organizaciones'].get('items', []))} de {c['organizaciones_registradas']}. Grupos representados: {sum(x['en_grafo_catalogo'] for x in inventario['grupos'].get('items', []))} de {c['grupos_registrados']}. El grafo inicial solo incluía organizaciones y temas usados por los conjuntos.", "",
              "## Columnas observadas por API", "",
              "Frecuencia entre recursos de datos con esquema verificado; se excluyen diccionarios y campos internos que empiezan con guion bajo. Compartir un nombre de columna no demuestra equivalencia de significado, unidad o clave.", "",
              "| Campo | Recursos de datos |", "| --- | ---: |"]
    lines += [f"| `{k}` | {v} |" for k, v in list(inventario["campos_observados"].items())[:25]]
    lines += ["", "## Páginas fuera del catálogo", "",
              "Herramientas, historias y análisis del Datatón se inventarían como páginas; una coincidencia temática con un conjunto no demuestra que ese conjunto alimente el tablero.", "",
              "| Página | Tipo inicial | Inspección | Destinos visualización |", "| --- | --- | --- | ---: |"]
    for p in inventario["paginas"]:
        estado = p.get("metodo_inspeccion") or f"Pendiente: HTTP {p['http'].get('status', p['http'].get('error'))}"
        lines.append(f"| [{p['nombre']}]({p['url']}) | {p['tipo']} | {estado} | {len(p.get('destinos_visualizacion', []))} |")
    lines += ["", "Los destinos declarados se extraen de iframes y configuraciones literales para escritorio/tableta/móvil. No se consultaron las APIs internas de las visualizaciones ni se verificaron todas las vistas dentro de cada tablero.", "",
              "## Secciones del portal", "", "| Sección | URL |", "| --- | --- |"]
    lines += [f"| {s['nombre']} | {s['url']} |" for s in inventario["secciones"]]
    lines += ["", "## Destinos de visualización por proveedor", "", "| Dominio | URLs únicas declaradas |", "| --- | ---: |"]
    lines += [f"| {k} | {v} |" for k, v in inventario["proveedores_visualizacion"].items()]
    lines += ["", "## Pendientes y límites", "",
              "- Identificar columnas y claves de recursos sin DataStore mediante diccionarios, muestras o acceso específico a los archivos.",
              "- Confirmar clasificación geoespacial y distinguir archivos de datos de diccionarios.",
              "- Identificar los datos que alimentan cada tablero; los iframes identifican destinos de visualización, no necesariamente APIs ni fuentes de datos.",
              "- Resolver coberturas temporales y territoriales ambiguas antes de crear equivalencias entre fuentes.",
              "- Páginas inaccesibles, enlaces no rastreados y datos generados dinámicamente permanecen pendientes; inventariar una URL no equivale a mapear su contenido.",
              "- Los enlaces de navegación institucional, redes sociales, acceso de usuarios y trámites se registran como referencias, sin rastrear esas plataformas.",
              "- Los informes nuevos no modifican la copia editable abierta en Studio ni incorporan automáticamente contenido al grafo.", "",
              "## Evidencia reproducible", "",
              "`data/portal/inventario.json` contiene URLs, procedencia, estados de acceso, recursos y esquemas recuperados. `data/portal/portada-enlaces.json` conserva la evidencia de la portada. Los metadatos CKAN completos usados se guardan de forma seleccionada, sin campos de contacto personal, en el inventario.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.workers <= 4:
        parser.error("--workers debe estar entre 1 y 4")
    output = ROOT / "data/portal"
    output.mkdir(parents=True, exist_ok=True)
    portada = leer(PORTAL)
    if portada["ok"]:
        parsed = Enlaces(portada["url"])
        parsed.feed(portada["body"])
        evidencia = {"source": PORTAL, "method": "http_html", "captured_at": datetime.now(timezone.utc).isoformat(),
                     "title": " ".join(parsed.title), "links": parsed.links, "frames": parsed.frames}
        (output / "portada-enlaces.json").write_text(json.dumps(evidencia, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        evidencia = json.loads((output / "portada-enlaces.json").read_text(encoding="utf-8"))
        print("Portada HTTP no disponible; usando evidencia DOM guardada con fecha explícita.")
    conjuntos = consultar_catalogo()
    orgs = listar_entidades("organization")
    grupos = listar_entidades("group")
    descubrimientos = {}
    for link in evidencia["links"]:
        url = canonica(link["url"])
        parts = urlsplit(url)
        if parts.netloc == "www.sonora.gob.mx" and parts.path.startswith("/datos/"):
            nombre = link["text"].strip()
            if not nombre or normalizar(nombre).startswith(("ir a ", "ver ")):
                nombre = parts.path.rsplit("/", 1)[-1]
            tipo = tipo_pagina(url, evidencia["links"])
            if url not in descubrimientos or descubrimientos[url]["nombre"] == parts.path.rsplit("/", 1)[-1]:
                descubrimientos[url] = {"url": url, "nombre": nombre, "tipo": tipo, "descubierto_en": PORTAL}
    recursos = []
    for d in conjuntos:
        for r in d.get("resources", []):
            tipo, motivo = clasificar(r, d["title"])
            recursos.append({"id": r["id"], "conjunto_id": d["id"], "conjunto": d["title"], "nombre": r.get("name"),
                             "url": r.get("url"), "formato": r.get("format"), "clasificacion": tipo, "evidencia_clasificacion": motivo,
                             "datastore_declarado": r.get("datastore_active") is True,
                             "estructura": "pendiente", "contenido": "no_integrado"})
    print(f"Inspeccionando {len(descubrimientos)} páginas enlazadas...")
    with ThreadPoolExecutor(args.workers) as pool:
        paginas = list(pool.map(inspeccionar_pagina, descubrimientos.values()))
    activos = [r["id"] for r in recursos if r["datastore_declarado"]]
    print(f"Consultando esquemas DataStore de {len(activos)} recursos, sin filas...")
    with ThreadPoolExecutor(args.workers) as pool:
        schemas = {r["resource_id"]: r for r in pool.map(comprobar_datastore, activos)}
    for r in recursos:
        if r["id"] in schemas:
            r["datastore"] = schemas[r["id"]]
            if r["datastore"]["ok"] and r["datastore"]["campos"]:
                r["estructura"] = "esquema_datastore_verificado"
        r["acceso"] = (["api_datastore_verificada"] if r.get("datastore", {}).get("ok") else []) + (["url_archivo_declarada_sin_comprobar"] if r.get("url") else ["sin_url_archivo"])
    config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]
    grafo = Graph().parse(ROOT / "data/catalogo/catalogo.ttl", format="turtle")
    mex = Namespace(config["base_iri"] + "vocab/")
    ids_grafo = {str(id_) for recurso in grafo.objects(None, mex.recurso) for id_ in grafo.objects(recurso, DCT.identifier)}
    for recurso in recursos:
        recurso["en_grafo_catalogo"] = recurso["id"] in ids_grafo
    campos = Counter(f["id"] for r in recursos if r.get("datastore", {}).get("ok") and r["clasificacion"] != "diccionario"
                     for f in r["datastore"]["campos"] if f.get("id") and not f["id"].startswith("_"))
    destinos = {url for p in paginas for url in p.get("destinos_visualizacion", [])}
    autodiscovery = []
    for url in (PORTAL + "robots.txt", PORTAL + "sitemap.xml"):
        response = leer(url)
        autodiscovery.append({k: v for k, v in response.items() if k != "body"})
    # Los listados pueden incluir contactos: conservar solo identidad y conteo.
    def listado(response, tipo):
        if not response["ok"]:
            return response
        return {"ok": True, "url": response["url"], "items": [
            {**{k: item.get(k) for k in ("id", "name", "title", "package_count", "detalle_pendiente")},
             "en_grafo_catalogo": bool(item.get("id") and any(grafo.triples((URIRef(config["base_iri"] + tipo + "/" + item["id"]), None, None))))}
            for item in response["result"]]}
    inventario = {
        "generado_en_utc": datetime.now(timezone.utc).isoformat(),
        "portada": {"evidencia": {k: v for k, v in evidencia.items() if k not in ("links", "frames")},
                    "consulta_http": {k: v for k, v in portada.items() if k != "body"}},
        "organizaciones": listado(orgs, "organization"), "grupos": listado(grupos, "theme"),
        "descubrimiento_automatico": autodiscovery,
        "campos_observados": dict(campos.most_common()),
        "proveedores_visualizacion": dict(Counter(urlsplit(url).netloc for url in destinos)),
        "secciones": list({canonica(link["url"]): {"nombre": link["text"], "url": canonica(link["url"]), "evidencia": "enlace_en_portada"}
                           for link in evidencia["links"] if urlsplit(link["url"]).netloc == "datos.sonora.gob.mx"
                           and urlsplit(link["url"]).path.rstrip("/") in ("", "/dataset", "/organization", "/group", "/about")}.values()),
        "cobertura": {"conjuntos": len(conjuntos), "recursos": len(recursos),
                      "organizaciones_registradas": len(orgs["result"]) if orgs["ok"] else None,
                      "grupos_registrados": len(grupos["result"]) if grupos["ok"] else None,
                      "paginas_datos_descubiertas": len(paginas), "datastore_declarado": len(activos),
                      "datastore_verificado": sum(r["estructura"] == "esquema_datastore_verificado" for r in recursos),
                      "estructuras_pendientes": sum(r["estructura"] == "pendiente" for r in recursos),
                      "recursos_en_grafo": sum(r["en_grafo_catalogo"] for r in recursos),
                      "destinos_visualizacion_declarados": len(destinos)},
        "clasificacion_recursos": dict(Counter(r["clasificacion"] for r in recursos)),
        "paginas": paginas, "recursos": recursos,
        "navegacion": [{**link, "alcance": "referencia_no_rastreada"} for link in evidencia["links"]
                       if canonica(link["url"]) not in descubrimientos],
    }
    (output / "inventario.json").write_text(json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "reports").mkdir(exist_ok=True)
    escribir_reporte(inventario, ROOT / "reports/cobertura-portal.md")
    print(json.dumps(inventario["cobertura"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
