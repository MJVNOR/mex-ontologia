"""Contrasta la ampliación contra el motor HTTP vivo, solo con SELECT."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from sincronizar_studio_portal import api
from integrar_cobertura import cargar_evidencia

rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
config, _, _, _ = cargar_evidencia(rules)
assert hashlib.sha256((ROOT / config['respaldo']).read_bytes()).hexdigest() == config['sha256_respaldo']
checks = {
    'variables_respaldadas': ('?item a mex:VariableDocumentada; mex:estadoSemantico "respaldada_por_definicion" .', 1212),
    'significados_candidatos': ('?item a mex:VariableDocumentada; mex:estadoSemantico "candidata_sin_definicion_suficiente" .', 23),
    'conceptos': ('?item a mex:ConceptoCompartido .', 940),
    'correspondencias_revisadas': ('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "documental_revisada" .', 836),
    'correspondencias_candidatas': ('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "candidata_por_nombre" .', 3312),
    'vinculos_ambiguos': ('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "ambigua_por_nombre" .', 12),
    'variables_calificadas': ('?item mex:tieneCalificadorDocumentado ?q .', 149),
    'componentes_calificador': ('?v mex:tieneCalificadorDocumentado ?item .', 195),
}
counts, queries = {}, {}
for name, (pattern, expected) in checks.items():
    query = ('PREFIX mex: <https://example.org/mex-ontologi/vocab/> '
             'SELECT (COUNT(DISTINCT ?item) AS ?total) WHERE { ' + pattern + ' }')
    response = api('/query', {'query': query})
    raw = response['results'][0]['total']
    match = re.match(r'^"?(\d+)', str(raw))
    if not match:
        raise ValueError('Conteo HTTP no interpretable: ' + str(raw))
    count = int(match.group(1))
    if count != expected:
        raise ValueError(f'Conteo vivo distinto para {name}: {count} != {expected}')
    counts[name], queries[name] = count, query
result = {'fecha_utc': datetime.now(timezone.utc).isoformat(), 'verificado': True,
          'canal': 'SELECT sobre http://127.0.0.1:8137/api/query',
          'conteos': counts, 'consultas': queries,
          'semantica_sha256': hashlib.sha256((ROOT / 'ontologia/semantica.json').read_bytes()).hexdigest(),
          'manifiesto_sha256': config['manifiesto_sha256'],
          'respaldo_verificado': True,
          'limite': 'No evalúa respuestas del chat ni habilita cruces entre fuentes.'}
(ROOT / 'reports/cobertura-muse-studio.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(counts, ensure_ascii=True, indent=2))
