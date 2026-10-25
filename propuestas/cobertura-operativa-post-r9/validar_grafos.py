"""Revalida RDF/SHACL y consulta la copia viva sin modificar Studio."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/cobertura-operativa-post-r9/ejecucion-20261024'
V=E/'validacion';V.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'scripts'))
from construir_catalogo import motor
from sincronizar_studio_portal import api,normalizar_cadenas
from rdflib import Graph
from rdflib.compare import isomorphic
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    dest=V/'grafos.json';assert not dest.exists(),'No sobrescribir validación'
    graph=ROOT/'data/portal/portal-completo.ttl';shapes=ROOT/'data/portal/shapes.ttl'
    store=V/'store-portal'
    portal={'sintaxis':motor(['validate',str(graph)],store),
            'carga':motor(['load',str(graph)],store),
            'stats':motor(['stats'],store),
            'shacl':motor(['shacl',str(shapes)],store),
            'sha256':sha(graph),'shapes_sha256':sha(shapes)}
    assert portal['shacl'].get('conforms') is True
    assert portal['stats']['triples']==322405
    result={'fecha_utc':datetime.now(timezone.utc).isoformat(),'portal':portal,
            'studio':{'verificado':False},'mutaciones_grafo':0,'gemma':'excluido'}
    # Guarda una copia nueva en el expediente; no llama /update ni /load.
    live=V/'studio-observado.ttl'
    try:
        api('/save',{'path':str(live),'format':'turtle'})
        studio_store=V/'store-studio'
        studio={'sintaxis':motor(['validate',str(live)],studio_store),
                'carga':motor(['load',str(live)],studio_store),
                'stats':motor(['stats'],studio_store),
                'shacl':motor(['shacl',str(shapes)],studio_store),
                'snapshot':live.relative_to(ROOT).as_posix(),'snapshot_sha256':sha(live)}
        current=normalizar_cadenas(Graph().parse(live,format='turtle'))
        before=normalizar_cadenas(Graph().parse(ROOT/'data/catalogo/studio-live.ttl',format='turtle'))
        studio['identico_a_snapshot_r9']=isomorphic(current,before)
        studio['verificado']=studio['identico_a_snapshot_r9'] and studio['shacl'].get('conforms') is True
        result['studio']=studio
    except Exception as error:
        result['studio']['error']=str(error)
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'portal_triples':portal['stats']['triples'],'portal_shacl':portal['shacl']['conforms'],
        'studio_verificado':result['studio']['verificado'],'studio_error':result['studio'].get('error')}))
    assert result['studio']['verificado'],'Studio no verificado; consultar el recibo'

if __name__=='__main__':main()
