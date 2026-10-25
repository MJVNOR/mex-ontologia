"""Integración fijada de correspondencias y evidencia de cruces; sin red ni modelos.

Preparada en staging. Se instalará en scripts/ después del relevo semántico.
"""
import hashlib
import json
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

from construir_catalogo import ROOT, PROV


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dentro(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Evidencia de ronda 3 fuera de su carpeta')
    return path


def cargar_evidencia(root=ROOT):
    config_path = root / 'ontologia/revision-ronda-3.json'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    folder = dentro(root, config['evidencia'])
    path = folder / 'manifiesto.json'
    if sha(path) != config['manifiesto_sha256']:
        raise ValueError('Manifiesto de ronda 3 modificado')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    sources = {'revision_ronda_3': config_path, 'manifiesto_ronda_3': path}
    for relative, expected in manifest['archivos'].items():
        source = dentro(folder, relative)
        if sha(source) != expected:
            raise ValueError('Evidencia de ronda 3 modificada: ' + relative)
        sources['ronda_3_' + relative] = source
    for relative, expected in manifest['insumos'].items():
        source = dentro(root, relative)
        if sha(source) != expected:
            raise ValueError('Insumo de ronda 3 modificado: ' + relative)
        sources['ronda_3_insumo_' + relative] = source
    read = lambda name: json.loads((folder / name).read_text(encoding='utf-8'))
    return config, manifest, folder, sources, read


def validar_extension_vinculos(rules, previous, root=ROOT):
    """Permite exclusivamente las 29 adiciones fijadas; conserva el prefijo exacto."""
    config, manifest, folder, sources, read = cargar_evidencia(root)
    baseline = read('vinculos-anteriores.json')
    additions = read('correspondencias-29.json')['entradas']
    if baseline != previous or len(baseline) != 836 or len(additions) != 29:
        raise ValueError('Base o extensión documental distinta de la aprobada')
    links = rules['vinculos_documentales_revisados']
    if links != baseline + additions:
        raise ValueError('La ronda 3 admite exactamente las 836 previas y 29 adiciones')
    keys = [(x['recurso'], x['campo'], x['columna']) for x in links]
    if len(set(keys)) != 865:
        raise ValueError('Correspondencias de ronda 3 duplicadas o solapadas')
    return additions


def construir(report, rules, base):
    config, manifest, folder, sources, read = cargar_evidencia()
    additions = validar_extension_vinculos(rules, read('vinculos-anteriores.json'))
    mex, graph = Namespace(base + 'vocab/'), Graph()
    mappings = {x['columna']: x for x in report['correspondencias']
                if x['estado'] == 'documental_revisada'}
    if len(mappings) != 865:
        raise ValueError('No se materializaron las 865 correspondencias revisadas')
    variables = {v['iri']: v for v in report['variables']}
    origin = folder / 'entregas/agente-2-correspondencias/propuestas.json'
    entity = URIRef(origin.as_uri())
    graph.add((entity, RDF.type, PROV.Entity))
    graph.add((entity, mex.sha256Evidencia, Literal(sha(origin))))
    for entry in additions:
        mapping = mappings.get(entry['columna'])
        if not mapping or mapping['revision'] != entry:
            raise ValueError('Correspondencia aprobada no materializada: ' + entry['columna'])
        variable = variables[mapping['variable']]
        if (variable['diccionario'] != entry['diccionario']
                or variable['huella_fila_diccionario'] != entry['huella_fila_diccionario']
                or variable['concepto'] != entry['concepto']):
            raise ValueError('Respaldo de correspondencia alterado: ' + entry['columna'])
        graph.add((URIRef(mapping['iri']), PROV.wasDerivedFrom, entity))
    from integrar_cruces_r3 import construir as construir_cruces
    crosses, summary, cross_sources = construir_cruces(
        base, carpeta=folder / 'entregas/agente-5-cruces')
    graph += crosses
    sources.update({'cruces_ronda_3_' + key: path for key, path in cross_sources.items()})
    return graph, {'correspondencias_nuevas': len(additions),
                   'correspondencias_revisadas_totales': len(mappings),
                   'cruces': summary, 'manifiesto_sha256': config['manifiesto_sha256']}, sources
