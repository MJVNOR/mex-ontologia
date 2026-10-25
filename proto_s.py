import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, 'scripts')
from construir_catalogo import motor
d = Path(tempfile.mkdtemp(prefix='sproto-'))
shape = d / 's.ttl'
shape.write_text('''@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix shape: <https://example.org/mex-ontologi/shapes/> .
shape:T a sh:NodeShape ; sh:targetClass mex:VariableDocumentada ;
 sh:sparql [ a sh:SPARQLConstraint ; sh:message "falta doc"@es ;
  sh:select """SELECT $this WHERE { $this <https://example.org/mex-ontologi/vocab/estadoSemantico> "respaldada_por_definicion" . FILTER NOT EXISTS { $this <https://example.org/mex-ontologi/vocab/significadoDocumentado> ?d } }""" ] .
''', encoding='utf-8')
data = d / 'd.ttl'
data.write_text('''@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix ex: <https://example.org/mex-ontologi/test/> .
ex:v1 a mex:VariableDocumentada ; mex:estadoSemantico "respaldada_por_definicion" .
''', encoding='utf-8')
store = Path(tempfile.mkdtemp(prefix='sstore-'))
print(motor(['validate', str(data)], store))
print(motor(['load', str(data)], store))
r = motor(['shacl', str(shape)], store)
print(json.dumps(r, ensure_ascii=False)[:1000])
