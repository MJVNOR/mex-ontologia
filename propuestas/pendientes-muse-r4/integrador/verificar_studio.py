"""Oráculos SELECT vivos calculados desde el resultado integrado y evidencia fijada."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from sincronizar_studio_portal import api
from integrar_ronda_4 import validar

def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    rules=read(ROOT/'ontologia/semantica.json')
    config,folder,base,accepted,_=validar(rules)
    report=read(ROOT/'data/semantica/cobertura.json')
    variables=report['resumen']['estados_variables']
    mappings=report['resumen']['estados_correspondencias']
    checks={
      'respaldadas':('?item a mex:VariableDocumentada; mex:estadoSemantico "respaldada_por_definicion" .',variables.get('respaldada_por_definicion',0)),
      'significados_candidatos':('?item a mex:VariableDocumentada; mex:estadoSemantico "candidata_sin_definicion_suficiente" .',variables.get('candidata_sin_definicion_suficiente',0)),
      'conceptos':('?item a mex:ConceptoCompartido .',len(rules['conceptos'])),
      'revisadas':('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "documental_revisada" .',mappings.get('documental_revisada',0)),
      'candidatas':('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "candidata_por_nombre" .',mappings.get('candidata_por_nombre',0)),
      'vinculos_ambiguos':('?item a mex:CorrespondenciaSemantica; mex:estadoCorrespondencia "ambigua_por_nombre" .',mappings.get('ambigua_por_nombre',0)),
      'variables_calificadas':('?item mex:tieneCalificadorDocumentado ?q .',sum(bool(v.get('calificador')) for v in report['variables'])),
      'componentes_calificador':('?v mex:tieneCalificadorDocumentado ?item .',sum(len(v.get('calificador',{})) for v in report['variables'])),
      'fichas_cruce_preservadas':('?item a mex:RevisionCruceRonda3 .',3),
      'comparaciones_2020_preservadas':('?item a mex:ComparacionMunicipal2020 .',72),
      'evidencias_fuente_preservadas':('?item a mex:EvidenciaFuenteComparacion .',144)}
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'consultas':{},'conteos':{},'verificado':False}
    for name,(pattern,expected) in checks.items():
        query='PREFIX mex: <https://example.org/mex-ontologi/vocab/> SELECT (COUNT(DISTINCT ?item) AS ?total) WHERE { '+pattern+' }'
        response=api('/query',{'query':query})
        raw=response['results'][0]['total']
        count=int(re.match(r'^"?(\d+)',str(raw)).group(1))
        if count!=expected:
            raise ValueError(f'{name}: Studio {count} != generado {expected}')
        result['conteos'][name]=count
        result['consultas'][name]=query
    result.update(verificado=True,manifiesto_sha256=config['manifiesto_sha256'],
        semantica_sha256=hashlib.sha256((ROOT/'ontologia/semantica.json').read_bytes()).hexdigest(),
        limite='SELECT valida el grafo vivo; las respuestas del modelo se evalúan por separado.')
    (ROOT/'reports/ronda-4-studio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['conteos'],ensure_ascii=True))

if __name__=='__main__':
    main()
