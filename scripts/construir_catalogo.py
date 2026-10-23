"""Genera el catálogo RDF desde CKAN y opcionalmente lo carga en Open Ontologies."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib
from urllib.parse import quote, urlencode, urlsplit

from rdflib import DCAT, DCTERMS as DCT, FOAF, Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS, URIRef, XSD

from explorar_catalogo import consultar_catalogo, presente

ROOT = Path(__file__).resolve().parents[1]
PROV = Namespace("http://www.w3.org/ns/prov#")


def url_http(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    parsed = urlsplit(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc) and not any(c in value for c in '<>"{}|\\^`')


def construir(registros, base, portal, instante):
    if not url_http(base) or not base.endswith("/") or "?" in base or "#" in base:
        raise ValueError("base_iri debe ser una URL HTTP(S) terminada en /, sin consulta ni fragmento")
    if not url_http(portal) or not portal.endswith("/"):
        raise ValueError("portal debe ser una URL HTTP(S) terminada en /")
    mex = Namespace(base + "vocab/")
    g = Graph()
    esquema = Graph()
    for grafo in (g, esquema):
        for prefix, ns in (("mex", mex), ("dcat", DCAT), ("dct", DCT), ("foaf", FOAF), ("skos", SKOS), ("prov", PROV)):
            grafo.bind(prefix, ns)
    def entidad(tipo, identificador):
        return URIRef(base + tipo + "/" + quote(str(identificador), safe=""))
    def texto(s, p, v, idioma=False):
        if presente(v):
            if not isinstance(v, (str, int, float, bool)):
                v = json.dumps(v, ensure_ascii=False, sort_keys=True)
            g.add((s, p, Literal(v, lang="es" if idioma else None)))

    ontology = URIRef(base + "ontology")
    esquema.add((ontology, RDF.type, OWL.Ontology))
    esquema.add((ontology, RDFS.label, Literal("mex-ontologi: catálogo de Sonora", lang="es")))
    esquema.add((ontology, RDFS.comment, Literal("Modelo local provisional. No es un vocabulario oficial del Gobierno de Sonora.", lang="es")))
    esquema.add((mex.RecursoCatalogado, RDF.type, OWL.Class))
    esquema.add((mex.RecursoCatalogado, RDFS.label, Literal("Recurso registrado en CKAN", lang="es")))
    esquema.add((mex.RecursoCatalogado, RDFS.subClassOf, RDFS.Resource))
    propiedades = {
        "recurso": (OWL.ObjectProperty, "Recurso del conjunto", DCAT.Dataset, mex.RecursoCatalogado),
        "urlDeclarada": (OWL.ObjectProperty, "URL declarada sin comprobar descarga", mex.RecursoCatalogado, RDFS.Resource),
        "regionDeclarada": (OWL.DatatypeProperty, "Región declarada", mex.RecursoCatalogado, XSD.string),
        "inicioDeclarado": (OWL.DatatypeProperty, "Inicio declarado sin interpretar cobertura", mex.RecursoCatalogado, XSD.string),
        "finDeclarado": (OWL.DatatypeProperty, "Fin declarado sin interpretar cobertura", mex.RecursoCatalogado, XSD.string),
        "datastoreActivo": (OWL.DatatypeProperty, "DataStore declarado activo por CKAN", mex.RecursoCatalogado, XSD.boolean),
        "frecuenciaDeclarada": (OWL.DatatypeProperty, "Frecuencia declarada", DCAT.Dataset, XSD.string),
        "jurisdiccionDeclarada": (OWL.DatatypeProperty, "Jurisdicción declarada", DCAT.Dataset, XSD.string),
        "granularidadDeclarada": (OWL.DatatypeProperty, "Granularidad declarada", DCAT.Dataset, XSD.string),
        "origenDeclarado": (OWL.DatatypeProperty, "Categoría de origen declarada", DCAT.Dataset, XSD.string),
        "fuentesExtrasDeclaradas": (OWL.DatatypeProperty, "Fuentes extras declaradas", DCAT.Dataset, XSD.string),
    }
    for nombre, (tipo, etiqueta, dominio, rango) in propiedades.items():
        prop = mex[nombre]
        for p, v in ((RDF.type, tipo), (RDFS.label, Literal(etiqueta, lang="es")), (RDFS.domain, dominio), (RDFS.range, rango)):
            esquema.add((prop, p, v))

    catalogo = entidad("catalog", "sonora")
    extraccion = entidad("extraction", instante)
    g.add((catalogo, RDF.type, DCAT.Catalog))
    texto(catalogo, DCT.title, "Catálogo de datos abiertos de Sonora", True)
    g.add((catalogo, FOAF.homepage, URIRef(portal)))
    g.add((catalogo, PROV.wasGeneratedBy, extraccion))
    g.add((extraccion, RDF.type, PROV.Activity))
    g.add((extraccion, PROV.endedAtTime, Literal(instante, datatype=XSD.dateTime)))
    g.add((extraccion, PROV.used, URIRef(portal + "api/3/action/package_search")))
    alertas = []
    for d in registros:
        ds = entidad("dataset", d["id"])
        record = entidad("record", d["id"])
        source = URIRef(portal + "api/3/action/package_show?" + urlencode({"id": d["id"]}))
        g.add((catalogo, DCAT.dataset, ds))
        g.add((catalogo, DCAT.record, record))
        g.add((ds, RDF.type, DCAT.Dataset))
        g.add((record, RDF.type, DCAT.CatalogRecord))
        g.add((record, FOAF.primaryTopic, ds))
        for node in (ds, record):
            g.add((node, DCT.identifier, Literal(d["id"])))
            g.add((node, PROV.wasDerivedFrom, source))
            g.add((node, PROV.wasGeneratedBy, extraccion))
        texto(ds, DCT.title, d.get("title"), True)
        texto(ds, DCT.description, d.get("notes"), True)
        if d.get("name"):
            g.add((ds, DCAT.landingPage, URIRef(portal + "dataset/" + quote(d["name"], safe=""))))
        for campo, predicado in (("metadata_created", DCT.issued), ("metadata_modified", DCT.modified)):
            if d.get(campo):
                try:
                    fecha = datetime.fromisoformat(d[campo]).isoformat()
                    g.add((record, predicado, Literal(fecha, datatype=XSD.dateTime)))
                except ValueError:
                    alertas.append({"id": d["id"], "campo": campo, "problema": "Fecha inválida", "valor": d[campo]})
        org = d.get("organization")
        if org:
            node = entidad("organization", org["id"])
            g.add((ds, DCT.publisher, node))
            g.add((node, RDF.type, FOAF.Organization))
            texto(node, DCT.identifier, org["id"])
            texto(node, FOAF.name, org.get("title") or org.get("name"), True)
        for group in d.get("groups", []):
            node = entidad("theme", group["id"])
            g.add((ds, DCAT.theme, node))
            g.add((node, RDF.type, SKOS.Concept))
            texto(node, SKOS.prefLabel, (group.get("title") or group["name"]).strip(), True)
        if not d.get("groups"):
            alertas.append({"id": d["id"], "problema": "Sin grupo temático"})
        for tag in d.get("tags", []):
            texto(ds, DCAT.keyword, tag["name"], True)
        if url_http(d.get("license_url")):
            g.add((ds, DCT.license, URIRef(d["license_url"])))
        for campo, predicado in (("frequency", mex.frecuenciaDeclarada), ("jurisdiccion", mex.jurisdiccionDeclarada), ("granularidad_datos", mex.granularidadDeclarada), ("data_source", mex.origenDeclarado), ("fuentes_extras", mex.fuentesExtrasDeclaradas)):
            texto(ds, predicado, d.get(campo))
        for r in d.get("resources", []):
            node = entidad("resource", r["id"])
            g.add((ds, mex.recurso, node))
            g.add((node, RDF.type, mex.RecursoCatalogado))
            g.add((node, PROV.wasDerivedFrom, source))
            g.add((node, PROV.wasGeneratedBy, extraccion))
            texto(node, DCT.identifier, r["id"])
            texto(node, DCT.title, r.get("name"), True)
            texto(node, DCT.format, str(r.get("format") or "").strip().upper())
            if url_http(r.get("url")):
                g.add((node, mex.urlDeclarada, URIRef(r["url"])))
            else:
                alertas.append({"id": r["id"], "problema": "URL ausente o inválida", "valor": r.get("url")})
            for campo, predicado in (("region", mex.regionDeclarada), ("start_date", mex.inicioDeclarado), ("end_date", mex.finDeclarado)):
                texto(node, predicado, r.get(campo))
            if isinstance(r.get("datastore_active"), bool):
                g.add((node, mex.datastoreActivo, Literal(r["datastore_active"])))
            if r.get("region") == "-":
                alertas.append({"id": r["id"], "problema": "Región sin identificar"})
            if r.get("start_date") == r.get("end_date") == "1989-06-04":
                alertas.append({"id": r["id"], "problema": "Intervalo repetido 1989-06-04 pendiente de revisión"})
    return g, esquema, alertas


def motor(argumentos, store=None):
    exe = ROOT / "tools" / "open-ontologies.exe"
    env = dict(os.environ, OPEN_ONTOLOGIES_STORAGE_MODE="persistent")
    cmd = [str(exe), "--no-connect"]
    if store:
        cmd += ["--data-dir", str(store)]
    result = subprocess.run(cmd + argumentos, check=True, capture_output=True, encoding="utf-8", env=env)
    payload = json.loads(result.stdout)
    if payload.get("ok") is False:
        raise RuntimeError(result.stdout)
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--load", action="store_true", help="Cargar una nueva instantánea persistente sin borrar almacenes previos")
    args = parser.parse_args()
    config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]
    registros = consultar_catalogo()
    instante = datetime.now(timezone.utc).isoformat()
    g, esquema, alertas = construir(registros, config["base_iri"], config["portal"], instante)
    output = ROOT / "data" / "catalogo"
    output.mkdir(parents=True, exist_ok=True)
    for nombre, grafo in (("catalogo.ttl", g), ("ontologia.ttl", esquema)):
        grafo.serialize(output / nombre, format="turtle", encoding="utf-8")
    shapes = (ROOT / "shapes/catalogo.ttl").read_text(encoding="utf-8").replace("{{BASE_IRI}}", config["base_iri"])
    (output / "shapes.ttl").write_text(shapes, encoding="utf-8")
    # Conservamos solo los campos usados por la conversión; no contactos personales.
    conjuntos_campos = ("id", "name", "title", "notes", "metadata_created", "metadata_modified", "license_url", "frequency", "jurisdiccion", "granularidad_datos", "data_source", "fuentes_extras")
    recursos_campos = ("id", "name", "format", "url", "region", "start_date", "end_date", "datastore_active")
    snapshot = []
    for d in registros:
        entry = {k: d.get(k) for k in conjuntos_campos}
        org = d.get("organization")
        entry["organization"] = {k: org.get(k) for k in ("id", "name", "title")} if org else None
        entry["groups"] = [{k: group.get(k) for k in ("id", "name", "title")} for group in d.get("groups", [])]
        entry["tags"] = [{"name": tag["name"]} for tag in d.get("tags", [])]
        entry["resources"] = [{k: r.get(k) for k in recursos_campos} for r in d.get("resources", [])]
        snapshot.append(entry)
    (output / "metadatos.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "consultado_en_utc": instante, "base_iri": config["base_iri"],
        "conjuntos": len(registros), "recursos": sum(len(d["resources"]) for d in registros),
        "triples_datos": len(g), "triples_modelo": len(esquema),
        "sha256_rdf": hashlib.sha256((output / "catalogo.ttl").read_bytes()).hexdigest(),
        "alertas": alertas,
    }
    if args.load:
        store = ROOT / "store" / datetime.now(timezone.utc).strftime("catalogo-%Y%m%dT%H%M%S%fZ")
        for nombre in ("ontologia.ttl", "catalogo.ttl"):
            motor(["validate", str(output / nombre)], store)
            motor(["load", str(output / nombre)], store)
        manifest["store_dir"] = str(store.relative_to(ROOT))
        manifest["stats"] = motor(["stats"], store)
        manifest["shacl"] = motor(["shacl", str(output / "shapes.ttl")], store)
        if manifest["shacl"].get("conforms") is not True:
            raise RuntimeError("La validación SHACL no confirmó conformidad: " + json.dumps(manifest["shacl"], ensure_ascii=False))
        for query in sorted((ROOT / "queries").glob("*.rq")):
            # El marcador permite usar las consultas con cualquier base_iri configurada.
            sparql = query.read_text(encoding="utf-8").replace("{{BASE_IRI}}", config["base_iri"])
            manifest.setdefault("consultas", {})[query.stem] = motor(["query", sparql], store)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "catalogo-carga.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k not in ("alertas", "consultas")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
