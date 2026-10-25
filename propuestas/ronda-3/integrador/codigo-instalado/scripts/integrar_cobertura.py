"""Verifica la evidencia fijada de cobertura y conserva su procedencia en RDF."""
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
        raise ValueError('Evidencia de cobertura fuera de su carpeta')
    return path


def cargar_evidencia(rules, root=ROOT):
    config_path = root / 'ontologia/revision-cobertura.json'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    folder = dentro(root, config['evidencia'])
    manifest_path = folder / 'manifiesto.json'
    if sha(manifest_path) != config['manifiesto_sha256']:
        raise ValueError('Manifiesto de cobertura modificado')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    sources = {'revision_cobertura': config_path, 'manifiesto_cobertura': manifest_path}
    for relative, expected in manifest['archivos'].items():
        path = dentro(folder, relative)
        if sha(path) != expected:
            raise ValueError('Evidencia de cobertura modificada: ' + relative)
        sources['cobertura_' + relative] = path
    for relative, expected in manifest['insumos'].items():
        path = dentro(root, relative)
        if sha(path) != expected:
            raise ValueError('Fuente documental de cobertura modificada: ' + relative)
        sources['cobertura_insumo_' + relative] = path
    accepted = json.loads((folder / 'aceptadas.json').read_text(encoding='utf-8'))
    previous = json.loads((folder / 'base-semantica.json').read_text(encoding='utf-8'))
    installed = {r['id']: r for r in rules['reglas_descripcion_exacta']}
    if len(installed) != len(rules['reglas_descripcion_exacta']):
        raise ValueError('Reglas semánticas duplicadas')
    for rule in previous['reglas_descripcion_exacta'] + accepted['reglas']:
        if installed.get(rule['id']) != rule:
            raise ValueError('Regla aceptada o anterior modificada: ' + rule['id'])
    for key, concept in {**previous['conceptos'], **accepted['conceptos']}.items():
        if rules['conceptos'].get(key) != concept:
            raise ValueError('Concepto aceptado o anterior modificado: ' + key)
    for key in ('observaciones_revision', 'condiciones'):
        if rules[key] != previous[key]:
            raise ValueError('La ampliación de cobertura alteró ' + key)
    if (root / 'ontologia/revision-ronda-3.json').exists():
        from integrar_ronda_3 import validar_extension_vinculos
        validar_extension_vinculos(rules, previous['vinculos_documentales_revisados'], root)
    elif rules['vinculos_documentales_revisados'] != previous['vinculos_documentales_revisados']:
        raise ValueError('La ampliación de cobertura alteró vinculos_documentales_revisados')
    return config, accepted, folder, sources


def construir(report, rules, base):
    config, accepted, folder, sources = cargar_evidencia(rules)
    mex, graph = Namespace(base + 'vocab/'), Graph()
    variables = {v['definicion_iri']: v for v in report['variables']}
    for rule in accepted['reglas']:
        definition = rule['definiciones'][0]
        variable = variables[definition]
        if variable['estado'] != 'respaldada_por_definicion' or variable['regla'] != rule['id']:
            raise ValueError('Interpretación aceptada no materializada: ' + rule['id'])
        if variable['huella_fila_diccionario'] != rule['huella_fila_diccionario']:
            raise ValueError('Fila documental cambió: ' + definition)
        origin = accepted['origenes'][rule['id']]
        for relative in (origin['entrega'], origin['auditoria']):
            source = dentro(folder, relative)
            entity = URIRef(source.as_uri())
            graph.add((entity, RDF.type, PROV.Entity))
            graph.add((entity, mex.sha256Evidencia, Literal(sha(source))))
            graph.add((URIRef(variable['iri']), PROV.wasDerivedFrom, entity))
    summary = dict(accepted['resumen'])
    summary['manifiesto_sha256'] = config['manifiesto_sha256']
    return graph, summary, sources
