import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, 'scripts')
from construir_catalogo import motor
store = Path(tempfile.mkdtemp(prefix='sq-'))
data = Path(tempfile.mkdtemp(prefix='sqd-')) / 'd.ttl'
data.write_text('''@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix ex: <https://example.org/mex-ontologi/test/> .
ex:v1 a mex:VariableDocumentada ; mex:estadoSemantico "respaldada_por_definicion" .
ex:v2 a mex:VariableDocumentada ; mex:estadoSemantico "candidata_sin_definicion_suficiente" .
''', encoding='utf-8')
motor(['load', str(data)], store)
q = 'SELECT ?e (COUNT(?v) AS ?n) WHERE { ?v <https://example.org/mex-ontologi/vocab/estadoSemantico> ?e } GROUP BY ?e ORDER BY ?e'
r = motor(['query', q], store)
print(json.dumps(r, ensure_ascii=False)[:1000])
s = motor(['stats'], store)
print(json.dumps(s, ensure_ascii=False)[:500])
