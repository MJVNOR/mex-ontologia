"""Control independiente de particiones, evidencia, reglas y auditorías finales."""
import collections
import hashlib
import json
from pathlib import Path
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/cobertura-muse-20261023'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import interpretacion, validar_calificador

DOMAINS = ['salud', 'registro-civil', 'educacion', 'gobierno-digital', 'territorio-economia']

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    with ZipFile(STAGE / 'integrador/antes-cobertura.zip') as archive:
        before = json.loads(archive.read('ontologia/semantica.json'))
    baseline = read(ROOT / 'data/semantica/cobertura.json')
    variables = {v['definicion_iri']: v for v in baseline['variables']}
    expected = {v['definicion_iri'] for v in variables.values() if v['estado'] == 'fuera_del_nucleo_actual'}
    errors, pending, parts, deliveries = [], [], {}, {}
    rules, concepts = [], dict(before['conceptos'])
    ids = set(r['id'] for r in before['reglas_descripcion_exacta'])
    for domain in DOMAINS:
        folder = STAGE / domain
        if not (folder / 'listo.json').exists():
            pending.append(domain)
            continue
        marker = read(folder / 'listo.json')
        if (marker.get('sha256') or marker.get('sha256_entrega_json')) != sha(folder / 'entrega.json'):
            pending.append(domain + ': entrega en revisión, SHA aún no fijada')
            continue
        payload = read(folder / 'entrega.json')
        deliveries[domain] = payload
        parts[domain] = [d['definicion_iri'] for d in payload['decisiones']]
        if len(parts[domain]) != len(set(parts[domain])) or not set(parts[domain]) <= expected:
            errors.append(domain + ': decisiones duplicadas o fuera de partición')
        for key, concept in payload['conceptos_nuevos'].items():
            if key in concepts and concepts[key] != concept:
                errors.append(domain + ': concepto en conflicto: ' + key)
            else:
                concepts[key] = concept
        decisions = {d['definicion_iri']: d for d in payload['decisiones']}
        for rule in payload['reglas']:
            if rule['id'] in ids:
                errors.append(domain + ': id de regla repetida: ' + rule['id'])
            ids.add(rule['id'])
            for key in ('nombres', 'descripciones', 'conjuntos', 'diccionarios', 'definiciones'):
                if not isinstance(rule.get(key), list) or len(rule[key]) != 1:
                    errors.append(domain + ': alcance no unitario: ' + rule['id'] + '/' + key)
            definition = rule['definiciones'][0]
            if definition not in decisions:
                errors.append(domain + ': regla fuera de sus decisiones: ' + rule['id'])
                continue
            row = variables[definition]
            for key, field in [('nombres', 'variable'), ('descripciones', 'descripcion'),
                               ('conjuntos', 'conjunto'), ('diccionarios', 'diccionario')]:
                if rule[key][0] != row[field]:
                    errors.append(domain + ': literal distinto: ' + rule['id'] + '/' + key)
            if rule.get('huella_fila_diccionario') != row['huella_fila_diccionario']:
                errors.append(domain + ': huella incorrecta: ' + rule['id'])
            if rule.get('concepto') not in concepts:
                errors.append(domain + ': concepto no definido: ' + rule['id'])
            if 'calificador' in rule:
                try:
                    validar_calificador(rule['calificador'])
                except ValueError as error:
                    errors.append(domain + ': ' + rule['id'] + ': ' + str(error))
            if decisions[definition]['decision'] != 'proponer':
                errors.append(domain + ': regla sobre decisión pendiente: ' + rule['id'])
            rules.append(rule)
        rule_definitions = [r['definiciones'][0] for r in payload['reglas']]
        proposed = {d['definicion_iri'] for d in payload['decisiones'] if d['decision'] == 'proponer'}
        if len(rule_definitions) != len(set(rule_definitions)) or set(rule_definitions) != proposed:
            errors.append(domain + ': proponer y reglas no son 1:1')
    merged_parts = [item for part in parts.values() for item in part]
    if len(merged_parts) != len(set(merged_parts)):
        errors.append('Solape de particiones')
    if not pending and set(merged_parts) != expected:
        errors.append('La partición completa no coincide con las 1308 definiciones')
    for key, concept in concepts.items():
        if len(concept) != 3 or (concept[2] is not None and concept[2] not in concepts):
            errors.append('Padre inexistente o estructura inválida: ' + key)
    combined = dict(before, conceptos=concepts,
                    reglas_descripcion_exacta=before['reglas_descripcion_exacta'] + rules)
    if not errors:
        for row in variables.values():
            result = interpretacion(row['variable'], row['descripcion'], row['conjunto'], combined,
                                    row['diccionario'], row['definicion_iri'])
            if row['estado'] != 'fuera_del_nucleo_actual' and any(
                    row.get(k) != result.get(k) for k in ('estado', 'concepto', 'regla', 'representacion')):
                errors.append('Se alteró una interpretación anterior: ' + row['definicion_iri'])
        for rule in rules:
            args = [rule['nombres'][0], rule['descripciones'][0], rule['conjuntos'][0], combined,
                    rule['diccionarios'][0], rule['definiciones'][0]]
            if interpretacion(*args).get('regla') != rule['id']:
                errors.append('Regla no dispara: ' + rule['id'])
            for pos in (0, 1, 2, 4, 5):
                other = args.copy()
                other[pos] = 'CONTROL_NEGATIVO_OTRA_FUENTE'
                if interpretacion(*other).get('regla') == rule['id']:
                    errors.append('Regla alcanza otro contexto: ' + rule['id'])
    audits = {}
    for auditor, domains in [('auditoria-a', ['gobierno-digital', 'territorio-economia']),
                             ('auditoria-b', ['salud', 'registro-civil', 'educacion'])]:
        path = STAGE / auditor / 'auditoria.json'
        if not path.exists():
            pending.append(auditor)
            continue
        payload = read(path)
        audits[auditor] = {'claves': list(payload), 'sha256': sha(path)}
        targets = {(domain, rule['id']) for domain in domains if domain in deliveries
                   for rule in deliveries[domain]['reglas']}
        actual_reviews = [(r['dominio'], r['regla_id']) for r in payload.get('dictamenes', [])]
        if len(actual_reviews) != len(set(actual_reviews)) or set(actual_reviews) != targets:
            pending.append(auditor + ': dictámenes no corresponden exactamente a su alcance final')
        hashes = payload.get('sha_entregas', {})
        for domain in domains:
            if domain not in deliveries:
                continue
            # The final audit must name the exact delivery hash (not its legacy source).
            recorded = hashes.get(domain)
            if isinstance(recorded, dict):
                recorded = recorded.get('sha256')
            if recorded != sha(STAGE / domain / 'entrega.json'):
                pending.append(auditor + ': auditoría no fijada a ' + domain)
    result = {'dominios_listos': list(deliveries), 'pendientes': pending, 'errores': errors,
              'conteos': {k: {'decisiones': len(v['decisiones']), 'reglas': len(v['reglas']),
                              'pendientes': sum(d['decision'] == 'pendiente' for d in v['decisiones'])}
                         for k, v in deliveries.items()},
              'total_decisiones': len(merged_parts), 'total_reglas_propuestas': len(rules), 'auditorias': audits}
    (STAGE / 'integrador/control.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if errors:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
