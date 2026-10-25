"""Ampliación explícita de ronda 4, fijada por manifiesto y auditorías independientes."""
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
        raise ValueError('Evidencia de ronda 4 fuera de su carpeta')
    return path

def cargar(root=ROOT):
    config_path = root / 'ontologia/revision-ronda-4.json'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    folder = dentro(root, config['evidencia'])
    manifest_path = folder / 'manifiesto.json'
    if sha(manifest_path) != config['manifiesto_sha256']:
        raise ValueError('Manifiesto de ronda 4 modificado')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    sources = {'revision_ronda_4': config_path, 'manifiesto_ronda_4': manifest_path}
    for relative, expected in manifest['archivos'].items():
        path = dentro(folder, relative)
        if sha(path) != expected:
            raise ValueError('Evidencia de ronda 4 modificada: '+relative)
        sources['ronda_4_'+relative] = path
    for relative, expected in manifest['insumos'].items():
        path = dentro(root, relative)
        if sha(path) != expected:
            raise ValueError('Insumo de ronda 4 modificado: '+relative)
        sources['ronda_4_insumo_'+relative] = path
    read = lambda p: json.loads((folder / p).read_text(encoding='utf-8'))
    return config, folder, read('base-semantica.json'), read('aceptadas.json'), sources

def validar(rules, root=ROOT):
    config, folder, baseline, accepted, sources = cargar(root)
    expected = json.loads(json.dumps(baseline))
    expected['reglas_descripcion_exacta'].extend(accepted['reglas'])
    expected['vinculos_documentales_revisados'].extend(accepted['vinculos'])
    for key, value in accepted['conceptos'].items():
        if key in expected['conceptos'] and expected['conceptos'][key]!=value:
            raise ValueError('Concepto de base sustituido: '+key)
        expected['conceptos'][key] = value
    if rules != expected:
        raise ValueError('Ronda 4 admite exclusivamente la base exacta y las adiciones auditadas')
    ids = [r['id'] for r in rules['reglas_descripcion_exacta']]
    columns = [r['columna'] for r in rules['vinculos_documentales_revisados']]
    if len(ids)!=len(set(ids)) or len(columns)!=len(set(columns)):
        raise ValueError('Reglas o columnas duplicadas en ronda 4')
    # Las auditorías aprobadas forman parte de evidencia inmutable, por cada ID exacto.
    for category, audit_name, entries, key in [
        ('reglas','auditoria-a',accepted['reglas'],'id'),
        ('vinculos','auditoria-b',accepted['vinculos'],'columna')]:
        audit = json.loads((folder/'auditorias'/f'{audit_name}.json').read_text(encoding='utf-8'))
        approvals = {r['id']:r for r in audit['dictamenes'] if r['tipo']==category and r['dictamen']=='aceptar'}
        for entry in entries:
            if entry[key] not in approvals:
                raise ValueError('Adición sin aprobación independiente: '+entry[key])
    return config, folder, baseline, accepted, sources

def construir(report, rules, base):
    config, folder, baseline, accepted, sources = validar(rules)
    graph, mex = Graph(), Namespace(base+'vocab/')
    variables = {r['definicion_iri']:r for r in report['variables'] if r.get('definicion_iri')}
    mappings = {r['columna']:r for r in report['correspondencias'] if r['estado']=='documental_revisada'}
    for category, entries, key in [('reglas',accepted['reglas'],'id'),('vinculos',accepted['vinculos'],'columna')]:
        for entry in entries:
            if category=='reglas':
                observed = variables[entry['definiciones'][0]]
                if observed.get('regla')!=entry['id'] or observed['estado']!='respaldada_por_definicion':
                    raise ValueError('Significado de ronda 4 no materializado: '+entry['id'])
            else:
                observed = mappings[entry['columna']]
                if observed['revision']!=entry:
                    raise ValueError('Vínculo de ronda 4 no materializado: '+entry['columna'])
            for relative in accepted['origenes'][entry[key]]:
                path = dentro(folder,relative)
                entity = URIRef(path.as_uri())
                graph.add((entity,RDF.type,PROV.Entity))
                graph.add((entity,mex.sha256Evidencia,Literal(sha(path))))
                graph.add((URIRef(observed['iri']),PROV.wasDerivedFrom,entity))
    return graph, dict(accepted['resumen'],manifiesto_sha256=config['manifiesto_sha256']), sources
