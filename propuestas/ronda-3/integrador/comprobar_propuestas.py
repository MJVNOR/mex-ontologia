"""Contraste independiente de propuestas con las filas crudas, sin cambiar el núcleo.

El informe es estructural y de procedencia: no sustituye la auditoría semántica.
"""
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import unquote

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import huella, interpretacion


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    coverage = read(ROOT / 'data/semantica/cobertura.json')
    inspection = read(ROOT / 'data/portal/contenido-inspeccion.json')
    central = read(ROOT / 'ontologia/semantica.json')
    assignment = read(HERE / 'asignaciones-semanticas.json')['asignaciones']
    variables = {v['definicion_iri']: v for v in coverage['variables']}
    documents = {d['id']: d for d in inspection['recursos']}
    errors, agents, all_rules, concepts, owners, definitions = [], [], [], {}, {}, {}
    for number in [3, 6, 7, 8, 9, 10]:
        folders = list(HERE.parent.glob(f'agente-{number}-*'))
        path = folders[0] / 'propuestas.json' if folders else None
        if not path or not path.exists():
            agents.append({'agente': number, 'estado': 'sin_entrega'})
            continue
        data = read(path)
        rules = data['reglas']
        expected = {v['definicion_iri'] for v in assignment[str(number)]['variables']} if number != 3 else None
        if expected is not None:
            actual = [v['definicion_iri'] for v in data['decisiones']]
            if set(actual) != expected or len(actual) != len(set(actual)):
                errors.append([number, 'particion_decisiones'])
        for key, value in data['conceptos_nuevos'].items():
            if key in central['conceptos']:
                errors.append([number, 'concepto_nuevo_existente', key])
            if key in concepts and concepts[key] != value:
                errors.append([number, 'concepto_colision_entre_agentes', key, owners[key]])
            concepts[key] = value
            owners.setdefault(key, []).append(number)
        for rule in rules:
            ids = rule.get('definiciones', [])
            if len(ids) != 1 or any(len(rule.get(k, [])) != 1 for k in ['nombres', 'descripciones', 'conjuntos', 'diccionarios']):
                errors.append([number, 'alcance_no_singular', rule['id']])
                continue
            iri = ids[0]
            if iri in definitions:
                errors.append([number, 'definicion_repetida', iri, definitions[iri]])
            definitions[iri] = number
            v = variables.get(iri)
            if not v or v['estado'] != 'fuera_del_nucleo_actual' or (expected is not None and iri not in expected):
                errors.append([number, 'fuera_de_asignacion', iri])
                continue
            for array, field in [('nombres', 'variable'), ('descripciones', 'descripcion'), ('conjuntos', 'conjunto'), ('diccionarios', 'diccionario')]:
                if rule[array] != [v[field]]:
                    errors.append([number, 'literal_o_identidad', iri, field])
            dictionary, index = unquote(iri.split('/definition/')[1]).rsplit('/', 1)
            raw = documents[dictionary]['definiciones'][int(index) - 1]
            if huella(raw) != v['huella_fila_diccionario']:
                errors.append([number, 'huella_fila', iri])
            result = interpretacion(v['variable'], v['descripcion'], v['conjunto'], {'reglas_descripcion_exacta': [rule]}, dictionary, iri)
            if result.get('concepto') != rule['concepto'] or result.get('estado') != 'respaldada_por_definicion':
                errors.append([number, 'regla_no_dispara', rule['id']])
            # A definition in a different document must not match this rule.
            negative = interpretacion(v['variable'], v['descripcion'], v['conjunto'], {'reglas_descripcion_exacta': [rule]}, 'otro-diccionario', iri)
            if negative.get('estado') == 'respaldada_por_definicion':
                errors.append([number, 'regla_escapa_diccionario', rule['id']])
        all_rules.extend(rules)
        agents.append({'agente': number, 'reglas': len(rules), 'conceptos_nuevos': len(data['conceptos_nuevos']),
                       'calificadores': sum(bool(r.get('calificador')) for r in rules),
                       'sha256_propuestas': hashlib.sha256(path.read_bytes()).hexdigest()})
    ids = [r['id'] for r in all_rules]
    if len(ids) != len(set(ids)):
        errors.append(['ids_regla_duplicados'])
    report = {'alcance': 'Control independiente de identidad, huellas y restricción de reglas; no aprobación semántica',
              'agentes': agents, 'reglas': len(all_rules), 'conceptos_distintos': len(concepts),
              'conceptos_compartidos': {c: ns for c, ns in owners.items() if len(ns) > 1}, 'errores': errors}
    (HERE / 'control-propuestas.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
