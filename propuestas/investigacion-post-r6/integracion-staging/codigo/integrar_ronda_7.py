"""Extension R7 de evidencia (STAGING, no instalada): exactamente 1 regla + 1 concepto nuevo, 0 vinculos.

Copia minima adaptada de scripts/integrar_ronda_6.py. No se importa ni se usa
hasta que el integrador la instale como scripts/integrar_ronda_7.py junto con
ontologia/revision-ronda-7.json + data/integracion-ronda-7/. El concepto y el
texto de la regla los fija aceptadas.json al integrar (doble auditoria pendiente).
"""
import copy
import hashlib
import json
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from construir_catalogo import ROOT, PROV
from integrar_contenido import clave

PIN_DEFINICION = 'https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5'
PIN_DICCIONARIO = '67156807-2013-4117-9ca9-394aea647127'
PIN_CONJUNTO = 'a3320cad-afd3-4840-8c3b-36236df26099'
PIN_HUELLA = 'c16feb711c8027da46df863668671e9f35e699129da382b494d45039abe1f232'

REGLA_KEYS = {'id', 'concepto', 'representacion', 'nombres', 'descripciones', 'conjuntos',
              'diccionarios', 'definiciones', 'huella_fila_diccionario', 'limites', 'limite',
              'calificador', 'evidencia', 'criterio', 'fuente_revision', 'alcance'}
PROHIBIDOS_EXTRA = ('join', 'vigencia', 'equivalen', 'homolog', 'catalogo', 'catálogo',
                    'sameas', 'exactmatch', 'unifica', 'fusiona')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dentro(root, relative):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError('Evidencia de ronda 7 fuera de carpeta')
    return p


def cargar(root=ROOT):
    cp = root / 'ontologia/revision-ronda-7.json'
    config = json.loads(cp.read_text(encoding='utf-8'))
    folder = dentro(root, config['evidencia'])
    mp = folder / 'manifiesto.json'
    if sha(mp) != config['manifiesto_sha256']:
        raise ValueError('Manifiesto de ronda 7 modificado')
    manifest = json.loads(mp.read_text(encoding='utf-8'))
    sources = {'revision_ronda_7': cp, 'manifiesto_ronda_7': mp}
    required = {'base-semantica.json', 'aceptadas.json', 'auditorias/auditoria-a.json', 'auditorias/auditoria-b.json'}
    if not isinstance(manifest.get('archivos'), dict) or not isinstance(manifest.get('insumos'), dict) or not required.issubset(manifest['archivos']):
        raise ValueError('Manifiesto de ronda 7 incompleto')
    for category, base in [('archivos', folder), ('insumos', root)]:
        for rel, h in manifest[category].items():
            p = dentro(base, rel)
            if sha(p) != h:
                raise ValueError('Evidencia de ronda 7 modificada: ' + rel)
            sources['ronda_7_' + category + '_' + rel] = p
    read = lambda rel: json.loads((folder / rel).read_text(encoding='utf-8'))
    accepted = read('aceptadas.json')
    if len(accepted.get('reglas', [])) != 1:
        raise ValueError('Ronda 7 admite exactamente una regla')
    if accepted.get('vinculos'):
        raise ValueError('Ronda 7 no admite correspondencias nuevas')
    if len(accepted.get('conceptos', {})) != 1:
        raise ValueError('Ronda 7 admite exactamente un concepto nuevo')
    row = accepted['reglas'][0]
    if row.get('definiciones') != [PIN_DEFINICION]:
        raise ValueError('Ronda 7 solo admite la IRI CLASIF asignada')
    if row.get('diccionarios') != [PIN_DICCIONARIO] or row.get('conjuntos') != [PIN_CONJUNTO]:
        raise ValueError('Ronda 7 solo admite el diccionario y conjunto asignados')
    if len(row.get('nombres', [])) != 1 or clave(row['nombres'][0]) != 'clasif':
        raise ValueError('Ronda 7 solo admite el nombre CLASIF')
    if len(row.get('descripciones', [])) != 1 or clave(row['descripciones'][0]) != clave('Clasificación'):
        raise ValueError('Ronda 7 solo admite la descripción asignada')
    if row.get('huella_fila_diccionario') != PIN_HUELLA:
        raise ValueError('Ronda 7 solo admite la huella asignada')
    if not isinstance(row.get('limites'), list) or not row['limites']:
        raise ValueError('Ronda 7 exige límites escritos')
    for extra in row:
        if extra in REGLA_KEYS:
            continue
        if any(p in json.dumps(row[extra], ensure_ascii=False).lower() for p in PROHIBIDOS_EXTRA):
            raise ValueError('Campo extra con alcance no admitido en ronda 7: ' + extra)
    origins = accepted.get('origenes', {}).get(row['id'], [])
    if not origins or any(rel not in manifest['archivos'] for rel in origins):
        raise ValueError('Origen no fijado por manifiesto de ronda 7: ' + row['id'])
    return config, folder, read('base-semantica.json'), accepted, sources


def validar_sobre_base(rules, base_r6, root=ROOT):
    config, folder, baseline, accepted, sources = cargar(root)
    if baseline != base_r6:
        raise ValueError('Base de ronda 7 no coincide con ronda 6 validada')
    expected = copy.deepcopy(baseline)
    expected['reglas_descripcion_exacta'].extend(accepted['reglas'])
    expected['vinculos_documentales_revisados'].extend(accepted['vinculos'])
    for k, v in accepted['conceptos'].items():
        if k in expected['conceptos']:
            raise ValueError('Ronda 7 exige concepto nuevo, clave ya existente: ' + k)
        expected['conceptos'][k] = v
    for field, key in [('reglas_descripcion_exacta', 'id'), ('vinculos_documentales_revisados', 'columna')]:
        ids = [r[key] for r in rules[field]]
        if len(ids) != len(set(ids)):
            raise ValueError('Reglas o columnas duplicadas en ronda 7')
    for audit_name in ('auditoria-a', 'auditoria-b'):
        audit = json.loads((folder / 'auditorias' / f'{audit_name}.json').read_text(encoding='utf-8'))
        approvals = {x['id'] for x in audit['dictamenes'] if x['tipo'] == 'reglas' and x['dictamen'] == 'aceptar'}
        for row in accepted['reglas']:
            if row['id'] not in approvals:
                raise ValueError(f'Ronda 7 sin aprobación independiente en {audit_name}: ' + row['id'])
    if rules != expected:
        raise ValueError('Ronda 7 permite solo la base y la regla auditada exacta')
    return config, folder, baseline, accepted, sources


def construir(report, rules, base):
    from integrar_ronda_4 import validar
    validar(rules)
    config, folder, baseline, accepted, sources = cargar()
    g = Graph()
    mex = Namespace(base + 'vocab/')
    variables = {v['definicion_iri']: v for v in report['variables']}
    for row in accepted['reglas']:
        observed = variables[row['definiciones'][0]]
        if observed.get('regla') != row['id'] or observed.get('concepto') != row['concepto'] or observed.get('huella_fila_diccionario') != row['huella_fila_diccionario']:
            raise ValueError('Regla R7 no materializada fielmente')
        for rel in accepted['origenes'][row['id']]:
            p = dentro(folder, rel)
            entity = URIRef(p.as_uri())
            g.add((entity, RDF.type, PROV.Entity))
            g.add((entity, mex.sha256Evidencia, Literal(sha(p))))
            g.add((URIRef(observed['iri']), PROV.wasDerivedFrom, entity))
    return g, dict(accepted['resumen'], manifiesto_sha256=config['manifiesto_sha256']), sources
