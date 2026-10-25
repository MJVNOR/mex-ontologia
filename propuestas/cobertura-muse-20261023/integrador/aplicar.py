"""Aplica únicamente reglas aceptadas por auditoría de la entrega exacta."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/cobertura-muse-20261023'
TARGET = ROOT / 'data/integracion-cobertura'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import construir, interpretacion, validar_calificador

DOMAINS = ['salud', 'registro-civil', 'educacion', 'gobierno-digital', 'territorio-economia']

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    config_path = ROOT / 'ontologia/revision-cobertura.json'
    if config_path.exists() or TARGET.exists():
        raise ValueError('Ya existe una integración de cobertura: revisar antes de reemplazar')
    manifest0 = read(STAGE / 'fuentes/manifiesto.json')
    for relative, expected in manifest0['insumos_centrales'].items():
        if sha(ROOT / relative) != expected:
            raise ValueError('Insumo central cambió desde la instantánea: ' + relative)
    with ZipFile(STAGE / 'integrador/antes-cobertura.zip') as archive:
        previous = json.loads(archive.read('ontologia/semantica.json'))
    baseline = read(ROOT / 'data/semantica/cobertura.json')
    by_definition = {v['definicion_iri']: v for v in baseline['variables']}
    expected_definitions = {key for key, v in by_definition.items() if v['estado'] == 'fuera_del_nucleo_actual'}
    deliveries = {d: read(STAGE / d / 'entrega.json') for d in DOMAINS}
    reviews, review_paths = {}, {}
    for name, domains in [('auditoria-a', ['gobierno-digital', 'territorio-economia']),
                          ('auditoria-b', ['salud', 'registro-civil', 'educacion'])]:
        audit_path = STAGE / name / 'auditoria.json'
        audit = read(audit_path)
        if {r['dominio'] for r in audit['dictamenes']} != set(domains):
            raise ValueError('Auditoría mezcla dominios históricos: ' + name)
        for domain in domains:
            if audit['sha_entregas'][domain] != sha(STAGE / domain / 'entrega.json'):
                raise ValueError('Auditoría no corresponde a entrega final: ' + domain)
            domain_reviews = [r for r in audit['dictamenes'] if r['dominio'] == domain]
            if len(domain_reviews) != len({r['regla_id'] for r in domain_reviews}):
                raise ValueError('Dictámenes duplicados: ' + domain)
            if {r['regla_id'] for r in domain_reviews} != {r['id'] for r in deliveries[domain]['reglas']}:
                raise ValueError('Auditoría no cubre cada regla actual: ' + domain)
            reviews[domain] = {r['regla_id']: r for r in domain_reviews}
            review_paths[domain] = 'auditorias/' + name + '.json'
    merged = copy.deepcopy(previous)
    all_concepts = dict(previous['conceptos'])
    accepted_rules, decisions, origins = [], [], {}
    used_definitions, all_ids = set(), {r['id'] for r in previous['reglas_descripcion_exacta']}
    domain_counts = {}
    for domain, payload in deliveries.items():
        marker = read(STAGE / domain / 'listo.json')
        if (marker.get('sha256') or marker.get('sha256_entrega_json')) != sha(STAGE / domain / 'entrega.json'):
            raise ValueError('Entrega cambió tras listo: ' + domain)
        for key, concept in payload['conceptos_nuevos'].items():
            if key in all_concepts and all_concepts[key] != concept:
                raise ValueError('Conceptos incompatibles: ' + key)
            all_concepts[key] = concept
        rows = payload['decisiones']
        if len(rows) != len({r['definicion_iri'] for r in rows}):
            raise ValueError('Definiciones repetidas en ' + domain)
        if used_definitions & {r['definicion_iri'] for r in rows}:
            raise ValueError('Solape de dominios: ' + domain)
        used_definitions.update(r['definicion_iri'] for r in rows)
        rule_by_def = {r['definiciones'][0]: r for r in payload['reglas']}
        if len(rule_by_def) != len(payload['reglas']):
            raise ValueError('Más de una regla por definición')
        counts = collections.Counter()
        for item in rows:
            decision = copy.deepcopy(item)
            definition = decision['definicion_iri']
            old = by_definition[definition]
            if old['estado'] != 'fuera_del_nucleo_actual':
                raise ValueError('No se permite alterar un significado previo')
            decision['dominio'] = domain
            proposal = rule_by_def.get(definition)
            if (decision['decision'] == 'proponer') != (proposal is not None):
                raise ValueError('Decisión y regla discrepan: ' + definition)
            if proposal:
                audit = reviews[domain][proposal['id']]
                decision['dictamen_auditoria'] = audit['dictamen']
                decision['motivo_auditoria'] = audit['motivo']
                if audit['dictamen'] not in {'aceptar', 'condicionado', 'rechazar'}:
                    raise ValueError('Dictamen desconocido')
            if proposal and audit['dictamen'] == 'aceptar':
                rule = copy.deepcopy(proposal)
                if rule['id'] in all_ids:
                    raise ValueError('ID de regla repetido: ' + rule['id'])
                all_ids.add(rule['id'])
                for field, key in [('nombres', 'variable'), ('descripciones', 'descripcion'),
                                   ('conjuntos', 'conjunto'), ('diccionarios', 'diccionario'),
                                   ('definiciones', 'definicion_iri')]:
                    if rule[field] != [old[key]]:
                        raise ValueError('Regla sin restricción literal exacta: ' + rule['id'] + '/' + field)
                if rule['huella_fila_diccionario'] != old['huella_fila_diccionario']:
                    raise ValueError('Huella documental distinta: ' + rule['id'])
                if 'calificador' in rule:
                    validar_calificador(rule['calificador'])
                source = 'entregas/' + domain + '/entrega.json'
                rule['fuente_revision'] = 'data/integracion-cobertura/' + source
                accepted_rules.append(rule)
                origins[rule['id']] = {'entrega': source, 'auditoria': review_paths[domain]}
                decision['estado_integracion'] = 'aceptada'
            else:
                decision['estado_integracion'] = 'pendiente'
                if not proposal and not decision.get('motivo'):
                    raise ValueError('Pendiente sin motivo: ' + definition)
            counts[decision['estado_integracion']] += 1
            decisions.append(decision)
        domain_counts[domain] = dict(counts)
    if used_definitions != expected_definitions:
        raise ValueError('La partición no cubre exactamente las definiciones pendientes')
    # Solo conceptos utilizados y sus ancestros; no se cargan conceptos descartados.
    needed = {r['concepto'] for r in accepted_rules}
    stack = list(needed)
    while stack:
        key = stack.pop()
        concept = all_concepts[key]
        if len(concept) != 3:
            raise ValueError('Estructura de concepto inválida: ' + key)
        parent = concept[2]
        if parent and parent not in needed:
            needed.add(parent)
            stack.append(parent)
    new_concepts = {k: all_concepts[k] for k in sorted(needed) if k not in previous['conceptos']}
    for key in needed:
        ancestors = set()
        node = key
        while node is not None:
            if node in ancestors:
                raise ValueError('Ciclo en jerarquía de conceptos: ' + key)
            ancestors.add(node)
            node = all_concepts[node][2]
    merged['conceptos'].update(new_concepts)
    merged['reglas_descripcion_exacta'].extend(accepted_rules)
    for row in baseline['variables']:
        assignment = interpretacion(row['variable'], row['descripcion'], row['conjunto'], merged,
                                    row['diccionario'], row['definicion_iri'])
        if row['estado'] != 'fuera_del_nucleo_actual' and any(
                row.get(k) != assignment.get(k) for k in ('estado', 'concepto', 'regla', 'representacion')):
            raise ValueError('Se alteró una interpretación previa: ' + row['definicion_iri'])
    expected_states = collections.Counter()
    accepted_ids = {r['definiciones'][0] for r in accepted_rules}
    for row in baseline['variables']:
        expected_states['respaldada_por_definicion' if row['definicion_iri'] in accepted_ids else row['estado']] += 1
    # Las nuevas variables también producen nuevas correspondencias candidatas,
    # nunca revisiones automáticas. Fijar expectativas actuales, sin borrar históricas.
    _, _, simulated = construir(read(ROOT / 'data/portal/inventario.json'),
                                read(ROOT / 'data/portal/contenido-inspeccion.json'), merged, None,
                                'https://example.org/mex-ontologi/')
    mapping_states = simulated['resumen']['estados_correspondencias']
    assert mapping_states['documental_revisada'] == len(previous['vinculos_documentales_revisados'])
    summary = {'definiciones_revisadas': len(decisions), 'reglas_aceptadas': len(accepted_rules),
               'pendientes_tras_revision': len(decisions)-len(accepted_rules),
               'conceptos_nuevos': len(new_concepts), 'dominios': domain_counts,
               'estados_variables_esperados': dict(expected_states),
               'estados_correspondencias_esperados': mapping_states,
               'correspondencias_previas_preservadas': len(previous['vinculos_documentales_revisados'])}
    accepted = {'reglas': accepted_rules, 'conceptos': new_concepts,
                'decisiones': decisions, 'origenes': origins, 'resumen': summary}
    # No mutar las entregas: las copias centrales y su manifiesto son evidencia permanente.
    TARGET.mkdir(parents=True)
    for domain in DOMAINS:
        folder = TARGET / 'entregas' / domain
        folder.mkdir(parents=True)
        for filename in ('entrega.json', 'pendientes.json', 'resultado.md', 'listo.json'):
            shutil.copyfile(STAGE / domain / filename, folder / filename)
    (TARGET / 'auditorias').mkdir()
    for name in ('auditoria-a', 'auditoria-b'):
        shutil.copyfile(STAGE / name / 'auditoria.json', TARGET / 'auditorias' / (name + '.json'))
    if (STAGE / 'investigacion/listo.json').exists():
        researcher = read(STAGE / 'investigacion/listo.json')
        expected = researcher.get('sha256') or researcher.get('sha256_evidencia')
        if expected and sha(STAGE / 'investigacion/evidencia.json') != expected:
            raise ValueError('La evidencia Obscura cambió tras listo')
        (TARGET / 'investigacion').mkdir()
        for filename in ('evidencia.json', 'resultado.md', 'listo.json'):
            shutil.copyfile(STAGE / 'investigacion' / filename, TARGET / 'investigacion' / filename)
    write(TARGET / 'base-semantica.json', previous)
    shutil.copyfile(ROOT / 'data/semantica/cobertura.json', TARGET / 'base-cobertura.json')
    write(TARGET / 'aceptadas.json', accepted)
    manifest = {'archivos': {p.relative_to(TARGET).as_posix(): sha(p)
                             for p in sorted(TARGET.rglob('*')) if p.is_file()},
                'insumos': {k: v for k, v in manifest0['insumos_centrales'].items()
                            if k in {'data/portal/contenido-inspeccion.json', 'data/portal/inventario.json'}}}
    write(TARGET / 'manifiesto.json', manifest)
    backup = ROOT / 'data/backups/cobertura-antes-20261023.zip'
    if backup.exists():
        raise ValueError('El respaldo de destino ya existe')
    backup.parent.mkdir(exist_ok=True)
    shutil.copyfile(STAGE / 'integrador/antes-cobertura.zip', backup)
    config = {'version': 1, 'evidencia': 'data/integracion-cobertura',
              'manifiesto_sha256': sha(TARGET / 'manifiesto.json'),
              'respaldo': backup.relative_to(ROOT).as_posix(),
              'sha256_respaldo': sha(backup), 'resumen': summary}
    write(ROOT / 'ontologia/semantica.json', merged)
    round1_path = ROOT / 'ontologia/revision-agentes.json'
    round1 = read(round1_path)
    round1['esperado_actual'] = dict(round1.get('esperado_actual', round1['esperado']),
        conceptos=len(merged['conceptos']), variables_respaldadas=expected_states['respaldada_por_definicion'],
        variables_pendientes=expected_states['candidata_sin_definicion_suficiente'],
        correspondencias_revisadas=mapping_states['documental_revisada'])
    write(round1_path, round1)
    round2_path = ROOT / 'ontologia/revision-ronda-2.json'
    round2 = read(round2_path)
    round2['esperado_actual'] = dict(round2['esperado'],
        conceptos=len(merged['conceptos']), respaldadas=expected_states['respaldada_por_definicion'],
        pendientes_significados=expected_states['candidata_sin_definicion_suficiente'],
        revisadas=mapping_states['documental_revisada'], candidatas=mapping_states.get('candidata_por_nombre', 0),
        ambiguas_vinculos=mapping_states.get('ambigua_por_nombre', 0))
    write(round2_path, round2)
    write(config_path, config)
    print(json.dumps(summary, ensure_ascii=True, indent=2))

if __name__ == '__main__':
    main()
