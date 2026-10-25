"""Comprueba el generador real con las entregas completas, sin simular sus triples."""
import json
import hashlib
from pathlib import Path
import sys
from zipfile import ZipFile

from rdflib import URIRef, Namespace, XSD

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/cobertura-muse-20261023'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import construir

with ZipFile(STAGE / 'integrador/antes-cobertura.zip') as archive:
    rules = json.loads(archive.read('ontologia/semantica.json'))
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
all_rules, hashes = [], {}
for domain in ('salud', 'registro-civil', 'educacion', 'gobierno-digital', 'territorio-economia'):
    payload = read(STAGE / domain / 'entrega.json')
    hashes[domain] = hashlib.sha256((STAGE / domain / 'entrega.json').read_bytes()).hexdigest()
    rules['conceptos'].update(payload['conceptos_nuevos'])
    rules['reglas_descripcion_exacta'].extend(payload['reglas'])
    all_rules.extend(payload['reglas'])
base = 'https://example.org/mex-ontologi/'
data, _, report = construir(read(ROOT / 'data/portal/inventario.json'),
                            read(ROOT / 'data/portal/contenido-inspeccion.json'), rules, None, base)
variables = {v['definicion_iri']: v for v in report['variables']}
mex = Namespace(base + 'vocab/')
qualified = 0
for rule in all_rules:
    if 'calificador' not in rule:
        continue
    qualified += 1
    variable = variables[rule['definiciones'][0]]
    assert variable['calificador'] == rule['calificador'], rule['id']
    subject = URIRef(variable['iri'])
    actual = {}
    for node in data.objects(subject, mex.tieneCalificadorDocumentado):
        dimension = data.value(node, mex.dimensionCalificador)
        value = data.value(node, mex.valorCalificador)
        assert value.datatype == XSD.string
        actual[str(dimension)] = str(value)
    assert actual == rule['calificador'], rule['id']
    for limit in variable.get('limites', []):
        assert any(str(v) == limit for v in data.objects(subject, mex.limiteSemantico)), rule['id']
result = {'motor': 'consolidar_semantica.construir real', 'variables_evaluadas': len(variables),
          'reglas_nuevas_simuladas': len(all_rules), 'reglas_calificadas_verificadas': qualified,
          'triples_generados': len(data), 'limites_preservados': True, 'sha_entregas': hashes}
(STAGE / 'integrador/verificacion-generador.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=True))
