"""Comprueba consultas afectadas sobre el almacén R9 ya cargado."""
from pathlib import Path
import sys,json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
sys.path.insert(0,str(ROOT/'scripts'))
from construir_catalogo import motor
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
load=read(ROOT/'reports/portal-carga.json');store=ROOT/load['store_dir']
queries={
 'declaraciones':'SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a <https://example.org/mex-ontologi/vocab/UnidadDeclarada> }',
 'variables_con_ambos':'SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a <https://example.org/mex-ontologi/vocab/VariableDocumentada> ; <https://example.org/mex-ontologi/vocab/significadoDocumentado> ?d ; <https://example.org/mex-ontologi/vocab/significadoCandidato> ?c }'}
result={'store_dir':load['store_dir'],'portal_triples':load['triples_combinados'],'consultas':{}}
for name,q in queries.items():
    raw=motor(['query',q],store)
    n=raw['results'][0]['n']
    match=re.fullmatch(r'"(\d+)"\^\^<http://www.w3.org/2001/XMLSchema#integer>',n)
    assert match,raw
    result[name]=int(match.group(1));result['consultas'][name]={'sparql':q,'resultado':raw}
for name in ('q1-vinculos-verificados','q3-trazabilidad'):
    p=E/f'P1-qudt/v003/consultas/{name}.rq'
    raw=motor(['query',p.read_text(encoding='utf-8')],store)
    result['consultas'][name]={'ruta':p.relative_to(ROOT).as_posix(),
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'filas':len(raw['results']),'resultado':raw}
assert result['declaraciones']==2 and result['variables_con_ambos']==0
assert result['consultas']['q1-vinculos-verificados']['filas']==2
out=E/'validacion/consultas-r9.json';assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'declaraciones':result['declaraciones'],'variables_con_ambos':result['variables_con_ambos'],
                  'filas_trazabilidad':result['consultas']['q3-trazabilidad']['filas']}))
