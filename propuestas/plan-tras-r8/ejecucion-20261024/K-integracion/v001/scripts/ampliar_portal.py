"""Amplía el modelo con el inventario existente; no consulta ni descarga filas."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tomllib
from urllib.parse import quote, urlsplit

from rdflib import DCAT, DCTERMS as DCT, FOAF, Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS, URIRef, XSD

from construir_catalogo import ROOT, PROV, motor, url_http
from guardar_rdf import serializar_atomico, escribir_json_atomico


def ampliar(inventario, base):
    mex = Namespace(base + "vocab/")
    g = Graph()
    model = Graph()
    for graph in (g, model):
        for prefix, ns in (("mex", mex), ("dcat", DCAT), ("dct", DCT), ("foaf", FOAF), ("prov", PROV), ("skos", SKOS)):
            graph.bind(prefix, ns)

    def node(kind, id_):
        return URIRef(base + kind + "/" + quote(str(id_), safe=""))

    def webnode(kind, url):
        return node(kind, hashlib.sha256(url.encode("utf-8")).hexdigest())

    snapshot = json.dumps(inventario, ensure_ascii=False, sort_keys=True).encode("utf-8")
    activity = node("inventory", hashlib.sha256(snapshot).hexdigest())
    g.add((activity, RDF.type, PROV.Activity))
    g.add((activity, RDFS.label, Literal("Inventario de cobertura del portal", lang="es")))
    g.add((activity, PROV.endedAtTime, Literal(inventario["generado_en_utc"], datatype=XSD.dateTime)))

    def entity(subject, cls, label, source):
        g.add((subject, RDF.type, cls))
        g.add((subject, RDFS.label, Literal(label, lang="es")))
        g.add((subject, PROV.wasGeneratedBy, activity))
        g.add((subject, PROV.wasDerivedFrom, URIRef(source)))

    classes = {
        mex.PaginaPortal: "Página del portal",
        mex.VisualizacionDeclarada: "Visualización declarada",
        mex.EsquemaObservado: "Esquema observado",
        mex.ColumnaObservada: "Columna observada",
        DCAT.DataService: "Servicio de consulta de datos",
        DCAT.Dataset: "Conjunto de datos", DCAT.Catalog: "Catálogo", DCAT.CatalogRecord: "Registro de metadatos",
        FOAF.Organization: "Dependencia", SKOS.Concept: "Tema", PROV.Activity: "Actividad de extracción",
    }
    for cls, label in classes.items():
        model.add((cls, RDF.type, OWL.Class))
        model.add((cls, RDFS.label, Literal(label, lang="es")))
    properties = {
        "paginaPortal": (OWL.ObjectProperty, "Página del portal", DCAT.Catalog, mex.PaginaPortal),
        "tipoPagina": (OWL.DatatypeProperty, "Tipo de página según navegación", mex.PaginaPortal, XSD.string),
        "visualizacionDeclarada": (OWL.ObjectProperty, "Visualización declarada en la página", mex.PaginaPortal, mex.VisualizacionDeclarada),
        "dominioVisualizacion": (OWL.DatatypeProperty, "Dominio del destino de visualización", mex.VisualizacionDeclarada, XSD.string),
        "esquema": (OWL.ObjectProperty, "Esquema observado del recurso", mex.RecursoCatalogado, mex.EsquemaObservado),
        "columna": (OWL.ObjectProperty, "Columna del esquema", mex.EsquemaObservado, mex.ColumnaObservada),
        "nombreCampo": (OWL.DatatypeProperty, "Nombre original del campo", mex.ColumnaObservada, XSD.string),
        "tipoCampoDeclarado": (OWL.DatatypeProperty, "Tipo declarado por DataStore", mex.ColumnaObservada, XSD.string),
        "posicionCampo": (OWL.DatatypeProperty, "Posición del campo desde uno", mex.ColumnaObservada, XSD.integer),
        "campoInterno": (OWL.DatatypeProperty, "Campo interno de DataStore", mex.ColumnaObservada, XSD.boolean),
        "servicioConsulta": (OWL.ObjectProperty, "Servicio de consulta verificado", mex.RecursoCatalogado, DCAT.DataService),
        "estadoEstructura": (OWL.DatatypeProperty, "Estado de inspección de estructura", mex.RecursoCatalogado, XSD.string),
        "clasificacionPorMetadatos": (OWL.DatatypeProperty, "Clasificación inicial por metadatos", mex.RecursoCatalogado, XSD.string),
        "evidenciaClasificacion": (OWL.DatatypeProperty, "Evidencia de clasificación", mex.RecursoCatalogado, XSD.string),
    }
    for name, (cls, label, domain, range_) in properties.items():
        p = mex[name]
        for pred, value in ((RDF.type, cls), (RDFS.label, Literal(label, lang="es")), (RDFS.domain, domain), (RDFS.range, range_)):
            model.add((p, pred, value))
    ontology = URIRef(base + "portal-model")
    model.add((ontology, RDF.type, OWL.Ontology))
    model.add((ontology, RDFS.label, Literal("mex-ontologi: páginas y estructuras del portal", lang="es")))
    model.add((ontology, RDFS.comment, Literal("Las columnas pertenecen a cada recurso. Nombres iguales no implican equivalencia. Los enlaces de visualización no establecen qué datos alimentan un tablero.", lang="es")))

    catalog = node("catalog", "sonora")
    for key, kind, cls, label_pred in (("organizaciones", "organization", FOAF.Organization, FOAF.name), ("grupos", "theme", SKOS.Concept, SKOS.prefLabel)):
        listado = inventario[key]
        for item in listado.get("items", []):
            if not item.get("id"):
                continue
            subject = node(kind, item["id"])
            label = (item.get("title") or item["name"]).strip()
            # Etiquetas existentes pertenecen al catálogo base; no generar otra versión.
            g.add((subject, RDF.type, cls))
            if not item.get("en_grafo_catalogo"):
                entity(subject, cls, label, listado["url"])
                g.add((subject, label_pred, Literal(label, lang="es")))
                g.add((subject, DCT.identifier, Literal(item["id"])))

    page_entries = list(inventario["paginas"])
    sections = {"/": "Inicio", "/dataset": "Conjuntos de datos", "/organization": "Organizaciones", "/group": "Grupos", "/about": "Acerca del portal"}
    for entry in inventario.get("secciones", []):
        page_entries.append({"url": entry["url"], "nombre": sections.get(urlsplit(entry["url"]).path.rstrip("/") or "/", entry["nombre"]),
                             "tipo": "seccion", "descubierto_en": "https://datos.sonora.gob.mx/"})
    for page in page_entries:
        subject = webnode("page", page["url"])
        entity(subject, mex.PaginaPortal, page["nombre"], page.get("descubierto_en", page["url"]))
        g.add((subject, FOAF.page, URIRef(page["url"])))
        g.add((subject, mex.tipoPagina, Literal(page["tipo"])))
        g.add((catalog, mex.paginaPortal, subject))
        for url in page.get("destinos_visualizacion", []):
            if not url_http(url):
                continue
            view = webnode("visualization", url)
            entity(view, mex.VisualizacionDeclarada, "Visualización — " + page["nombre"], page["url"])
            g.add((view, FOAF.page, URIRef(url)))
            g.add((view, mex.dominioVisualizacion, Literal(urlsplit(url).netloc)))
            g.add((subject, mex.visualizacionDeclarada, view))

    for resource in inventario["recursos"]:
        subject = node("resource", resource["id"])
        source = "https://datos.sonora.gob.mx/api/3/action/resource_show?id=" + quote(resource["id"], safe="")
        g.add((subject, mex.estadoEstructura, Literal(resource["estructura"])))
        g.add((subject, mex.clasificacionPorMetadatos, Literal(resource["clasificacion"])))
        g.add((subject, mex.evidenciaClasificacion, Literal(resource["evidencia_clasificacion"])))
        g.add((subject, PROV.wasGeneratedBy, activity))
        datastore = resource.get("datastore", {})
        if not datastore.get("ok") or not datastore.get("campos"):
            continue
        schema = node("schema", resource["id"])
        entity(schema, mex.EsquemaObservado, f"Esquema — {resource['nombre']} — {resource['conjunto']}", datastore["url"])
        g.add((subject, mex.esquema, schema))
        service = node("service", resource["id"])
        entity(service, DCAT.DataService, f"Consulta DataStore — {resource['nombre']} — {resource['conjunto']}", datastore["url"])
        g.add((service, DCAT.endpointURL, URIRef(datastore["url"])))
        g.add((subject, mex.servicioConsulta, service))
        for position, field in enumerate(datastore["campos"], start=1):
            column = URIRef(base + "column/" + quote(resource["id"], safe="") + "/" + quote(field["id"], safe=""))
            entity(column, mex.ColumnaObservada, f"{field['id']} — {resource['nombre']} — {resource['conjunto']}", datastore["url"])
            g.add((schema, mex.columna, column))
            g.add((column, DCT.isPartOf, schema))
            g.add((column, mex.nombreCampo, Literal(field["id"])))
            if field.get("type"):
                g.add((column, mex.tipoCampoDeclarado, Literal(field["type"])))
            g.add((column, mex.posicionCampo, Literal(position)))
            g.add((column, mex.campoInterno, Literal(field["id"].startswith("_"))))
    return g, model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--load", action="store_true")
    args = parser.parse_args()
    config = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))["catalogo"]
    source = ROOT / "data/portal/inventario.json"
    inventario = json.loads(source.read_text(encoding="utf-8"))
    extra, model = ampliar(inventario, config["base_iri"])
    combined = Graph()
    for file in ("catalogo.ttl", "ontologia.ttl"):
        combined.parse(ROOT / "data/catalogo" / file, format="turtle")
    # No unir inventarios de otra fecha con un catálogo que no contiene sus recursos.
    mex = Namespace(config["base_iri"] + "vocab/")
    ids = {str(id_) for r in combined.objects(None, mex.recurso) for id_ in combined.objects(r, DCT.identifier)}
    if ids != {r["id"] for r in inventario["recursos"]}:
        raise RuntimeError("Los identificadores del inventario y del catálogo no coinciden. Actualiza ambos antes de ampliar.")
    extension = extra + model
    content_file = ROOT / 'data/portal/contenido-inspeccion.json'
    cross_file = ROOT / 'data/portal/cruce-registro-civil.json'
    if content_file.exists() and cross_file.exists():
        from integrar_contenido import integrar, documentar
        inspection = json.loads(content_file.read_text(encoding='utf-8'))
        cross = json.loads(cross_file.read_text(encoding='utf-8'))
        content, content_model, coverage = integrar(inventario, inspection, cross, config['base_iri'])
        extension += content + content_model
        serializar_atomico(content, ROOT / 'data/portal/contenido.ttl')
        documentar(coverage)
    opportunities_file = ROOT / 'data/portal/oportunidades-cruce.json'
    if opportunities_file.exists():
        opportunity_report = json.loads(opportunities_file.read_text(encoding='utf-8'))
        sources = {'inventario': source, 'inspeccion': content_file, 'cruce': cross_file,
                   'catalogo': ROOT / 'data/catalogo/catalogo.ttl'}
        if any(hashlib.sha256(path.read_bytes()).hexdigest() != opportunity_report['huellas_entrada'].get(key)
               for key, path in sources.items()):
            raise RuntimeError('El mapa de cruces está desactualizado: ejecuta scripts/mapear_cruces.py antes de ampliar.')
        from mapear_cruces import rdf_map
        extension += rdf_map(opportunity_report, config['base_iri'])
    batch_file = ROOT / 'data/portal/lote-cruces/validacion-lote.json'
    if batch_file.exists():
        batch_report = json.loads(batch_file.read_text(encoding='utf-8'))
        batch_sources = {'oportunidades': opportunities_file, 'inventario': source, 'inspeccion': content_file}
        if any(hashlib.sha256(path.read_bytes()).hexdigest() != batch_report['huellas_entrada'].get(key)
               for key, path in batch_sources.items()):
            raise RuntimeError('Validación por lote desactualizada: ejecuta scripts/validar_lote_cruces.py antes de ampliar.')
        from validar_lote_cruces import rdf_lote
        extension += rdf_lote(batch_report, config['base_iri'])
    semantic_rules = ROOT / 'ontologia/semantica.json'
    if semantic_rules.exists():
        from consolidar_semantica import generar
        semantic_data, semantic_model, semantic_report = generar()
        extension += semantic_data + semantic_model
    combined += extension
    output = ROOT / "data/portal"
    for name, graph in (("ampliacion.ttl", extension), ("ontologia-portal.ttl", model), ("portal-completo.ttl", combined)):
        serializar_atomico(graph, output / name)
    shapes = Graph().parse(ROOT / "data/catalogo/shapes.ttl", format="turtle")
    portal_shapes = (ROOT / "shapes/portal.ttl").read_text(encoding="utf-8").replace("{{BASE_IRI}}", config["base_iri"])
    shapes.parse(data=portal_shapes, format="turtle")
    if content_file.exists() and cross_file.exists():
        shapes.parse(data=(ROOT / 'shapes/contenido.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
    if opportunities_file.exists():
        shapes.parse(data=(ROOT / 'shapes/oportunidades.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
    if batch_file.exists():
        shapes.parse(data=(ROOT / 'shapes/lote.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
    if semantic_rules.exists():
        shapes.parse(data=(ROOT / 'shapes/semantica.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
        if (ROOT / 'ontologia/territorio.json').exists():
            shapes.parse(data=(ROOT / 'shapes/territorio.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
        if (ROOT / 'ontologia/revision-agentes.json').exists():
            shapes.parse(data=(ROOT / 'shapes/integracion-agentes.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
        if (ROOT / 'ontologia/revision-ronda-2.json').exists():
            shapes.parse(data=(ROOT / 'shapes/ronda-2.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
    if (ROOT / 'ontologia/revision-ronda-3.json').exists():
        shapes.parse(data=(ROOT / 'shapes/ronda-3.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')
    if (ROOT / 'ontologia/revision-ronda-9.json').exists():
        from integrar_ronda_9 import cargar_shapes
        shapes += cargar_shapes(ROOT)
    serializar_atomico(shapes, output / "shapes.ttl")
    report = {"base_iri": config["base_iri"], "generado_en_utc": datetime.now(timezone.utc).isoformat(),
              "inventario_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "triples_extension": len(extension), "triples_combinados": len(combined)}
    if content_file.exists() and cross_file.exists():
        report['contenido_sha256'] = hashlib.sha256(content_file.read_bytes()).hexdigest()
        report['cruce_sha256'] = hashlib.sha256(cross_file.read_bytes()).hexdigest()
    if opportunities_file.exists():
        report['oportunidades_sha256'] = hashlib.sha256(opportunities_file.read_bytes()).hexdigest()
    if batch_file.exists():
        report['lote_sha256'] = hashlib.sha256(batch_file.read_bytes()).hexdigest()
    if semantic_rules.exists():
        report['semantica'] = {'huellas_entrada': semantic_report['huellas_entrada'], 'resumen': semantic_report['resumen']}
    if args.load:
        store = ROOT / "store" / datetime.now(timezone.utc).strftime("portal-%Y%m%dT%H%M%S%fZ")
        report["store_dir"] = str(store.relative_to(ROOT))
        report["sintaxis"] = motor(["validate", str(output / "portal-completo.ttl")], store)
        report["carga"] = motor(["load", str(output / "portal-completo.ttl")], store)
        report["shacl"] = motor(["shacl", str(output / "shapes.ttl")], store)
        if report["shacl"].get("conforms") is not True:
            raise RuntimeError("La ampliación no supera SHACL: " + json.dumps(report["shacl"], ensure_ascii=False))
        for file in sorted((ROOT / "queries/portal").glob("*.rq")):
            query = file.read_text(encoding="utf-8").replace("{{BASE_IRI}}", config["base_iri"])
            report.setdefault("consultas", {})[file.stem] = motor(["query", query], store)
        report["stats"] = motor(["stats"], store)
    escribir_json_atomico(report, ROOT / "reports/portal-carga.json")
    print(json.dumps({k: v for k, v in report.items() if k != "consultas"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
