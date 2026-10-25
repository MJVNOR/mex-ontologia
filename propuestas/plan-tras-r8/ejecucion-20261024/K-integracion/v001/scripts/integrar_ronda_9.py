"""R9: unidades declaradas por dos definiciones y exclusión SHACL.

No extiende reglas, conceptos ni correspondencias del núcleo R8.
"""
import hashlib
import json
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from construir_catalogo import ROOT, PROV

EVIDENCIA = 'data/integracion-ronda-9'
MEX = Namespace('https://example.org/mex-ontologi/vocab/')
BASE = 'https://example.org/mex-ontologi/'
PIN_REGLAS = 'dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd'
SHAPE_SHA = 'fc301d854b6c9175be601282ab4073f054a1736103b92ea634003c7bcc2b148d'
ARCHIVOS = {'datos':'datos/unidades.ttl', 'modelo':'modelo/unidades.ttl',
            'shapes':'shapes/exclusion-significado.ttl'}
PIN = {
 'P1-Q1': {'diccionario':'6713de4e-1e2b-447d-8000-f6ceaabd8473', 'fila':6,
  'conjunto':'8b4edefe-cb1a-401c-90c6-05548779defd',
  'nombre':'Precipitacion_mm', 'unidad_literal':'Milímetros',
  'unidad_qudt':'http://qudt.org/vocab/unit/MilliM',
  'huella_fila_diccionario':'dec3bb83da6fe2209575146e9775fc615c0473c13209cb9a05f16b492e28bb9f',
  'normativa_sha256':'5e63691124e69c162ddfa65bde77fb1ad3e9a2173ffd33b9910100880a9ea9a7',
  'sujeto':BASE+'propuesta/p1-qudt/v003/declaracion-precipitacion-mm'},
 'P1-Q3': {'diccionario':'94215f51-9c89-414d-8c3d-92792e609a2a', 'fila':14,
  'conjunto':'3e17a7e8-c8d4-49c4-a426-4dec099cd0cd',
  'nombre':'SUPSEM', 'unidad_literal':'Hectáreas',
  'unidad_qudt':'http://qudt.org/vocab/unit/HA',
  'huella_fila_diccionario':'208a95e2c54e495723b39a3b528deb22f6147dfd3bd080f867e6bea2c191f321',
  'normativa_sha256':'9095968323f72af577b4a94684a78e2f806595ca118529b5e47cb0b2acd1ee3e',
  'sujeto':BASE+'propuesta/p1-qudt/v003/declaracion-superficie-ha'}
}
for _p in PIN.values():
    _suffix = _p['diccionario']+'%2F'+str(_p['fila'])
    _p['variable'] = BASE+'documented-variable/'+_suffix
    _p['definicion_iri'] = BASE+'definition/'+_suffix

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dentro(root, rel):
    if not isinstance(rel,str) or Path(rel).is_absolute():
        raise ValueError('Ruta de evidencia no relativa')
    p=(Path(root)/rel).resolve()
    if not p.is_relative_to(Path(root).resolve()):
        raise ValueError('Evidencia fuera de carpeta')
    return p

def comprobar_resumen(summary):
    if (summary.get('estados_variables') != {
        'respaldada_por_definicion':1423,'fuera_del_nucleo_actual':124,
        'candidata_sin_definicion_suficiente':16}
        or summary.get('estados_correspondencias') != {
        'documental_revisada':4506,'candidata_por_nombre':17}
        or summary.get('conceptos_compartidos')!=1106
        or summary.get('variables_materializadas')!=1442
        or summary.get('columnas_totales_examinadas')!=5523):
        raise ValueError('Base R8 sin conteos exactos')

def _auditorias(folder, accepted):
    cases={'P1-Q1','P1-Q3','P4-exclusion'}
    for name in ('a','b'):
        audit=read(folder/f'auditorias/auditoria-{name}.json')
        rows=audit.get('dictamenes',[])
        if (audit.get('auditor')!=name or audit.get('dictamen')!='aceptar'
            or audit.get('aceptadas_sha256')!=sha(folder/'aceptadas.json')
            or len(rows)!=3 or {r.get('id') for r in rows}!=cases
            or any(r.get('dictamen')!='aceptar' for r in rows)):
            raise ValueError('Doble aprobación exacta R9 ausente: '+name)

def _datos(folder, accepted, cob8):
    decls=accepted.get('declaraciones',[])
    if len(decls)!=2 or {d.get('id') for d in decls}!=set(PIN):
        raise ValueError('R9 admite exactamente Q1 y Q3')
    graph=Graph().parse(folder/ARCHIVOS['datos'],format='turtle')
    subjects={URIRef(p['sujeto']) for p in PIN.values()}
    if set(graph.subjects())!=subjects:
        raise ValueError('Grafo R9 con sujetos adicionales o ausentes')
    variables={v.get('definicion_iri'):v for v in cob8['variables']}
    allowed={RDF.type,RDFS.label,RDFS.comment,PROV.wasDerivedFrom,
             MEX.variableDocumentada,MEX.definicionFuente,MEX.conjuntoFuente,
             MEX.diccionarioFuente,MEX.unidadLiteral,MEX.unidadQudt,MEX.evidenciaNormativa}
    if not set(graph.predicates())<=allowed:
        raise ValueError('Grafo R9 con predicado ajeno')
    for d in decls:
        p=PIN[d['id']]
        if d!={'id':d['id'],**p}:
            raise ValueError('Declaración R9 distinta del pin')
        v=variables.get(p['definicion_iri'],{})
        if v.get('estado')!='respaldada_por_definicion':
            raise ValueError('Unidad sin significado respaldado')
        for k,vk in [('variable','iri'),('conjunto','conjunto'),('diccionario','diccionario'),
                     ('nombre','variable'),('huella_fila_diccionario','huella_fila_diccionario')]:
            if p[k]!=v.get(vk): raise ValueError('Variable/fuente R8 inexacta')
        row=read(folder/f'filas/{d["id"]}.json')
        h=hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if (h!=p['huella_fila_diccionario'] or row.get('Unidad de medida')!=p['unidad_literal']
            or row.get('Nombre variable')!=p['nombre']):
            raise ValueError('Fila/unidad literal original alterada')
        if sha(folder/f'normativa/{d["id"]}.txt')!=p['normativa_sha256']:
            raise ValueError('Normativa QUDT no verificada')
        s=URIRef(p['sujeto'])
        expected={RDF.type:MEX.UnidadDeclarada,MEX.variableDocumentada:URIRef(p['variable']),
            MEX.definicionFuente:URIRef(p['definicion_iri']),MEX.conjuntoFuente:Literal(p['conjunto']),
            MEX.diccionarioFuente:Literal(p['diccionario']),MEX.unidadLiteral:Literal(p['unidad_literal']),
            MEX.unidadQudt:URIRef(p['unidad_qudt'])}
        for pred,obj in expected.items():
            if set(graph.objects(s,pred))!={obj}:
                raise ValueError('Triple cualificado R9 inexacto: '+str(pred))
        source=('https://datos.sonora.gob.mx/api/3/action/datastore_search?resource_id='
                +p['diccionario']+'&limit=1000&offset=0&sort=_id+asc')
        if set(graph.objects(s,PROV.wasDerivedFrom))!={URIRef(source),URIRef(p['unidad_qudt'])}:
            raise ValueError('Procedencia R9 incompleta o adicional')
        for pred in (RDFS.label,RDFS.comment,MEX.evidenciaNormativa):
            objects=list(graph.objects(s,pred))
            if len(objects)!=1 or not isinstance(objects[0],Literal):
                raise ValueError('Anotación documental R9 inexacta')
        ev=str(next(graph.objects(s,MEX.evidenciaNormativa)))
        if p['normativa_sha256'] not in ev:
            raise ValueError('Anotación normativa R9 sin hash')
    return graph

def _modelo(folder):
    graph=Graph().parse(folder/ARCHIVOS['modelo'],format='turtle')
    terms={'UnidadDeclarada','variableDocumentada','definicionFuente','conjuntoFuente',
           'diccionarioFuente','unidadLiteral','unidadQudt','motivoNegativo','evidenciaNormativa'}
    if set(graph.subjects())!={MEX[t] for t in terms}:
        raise ValueError('Modelo R9 fuera del vocabulario mínimo')
    for s,p,o in graph:
        if p not in {RDF.type,RDFS.label,RDFS.comment}:
            raise ValueError('Modelo R9 con inferencias adicionales')
        if p==RDF.type and o!=(RDFS.Class if s==MEX.UnidadDeclarada else RDF.Property):
            raise ValueError('Tipo de vocabulario R9 no permitido')
        if p!=RDF.type and not isinstance(o,Literal):
            raise ValueError('Modelo R9 con anotación no literal')
    for t in terms:
        if (MEX[t],RDF.type,RDFS.Class if t=='UnidadDeclarada' else RDF.Property) not in graph:
            raise ValueError('Tipo de vocabulario R9 ausente')
    return graph

def cargar(root=ROOT):
    root=Path(root)
    cp=root/'ontologia/revision-ronda-9.json'; config=read(cp)
    if config.get('evidencia')!=EVIDENCIA or config.get('format_version')!=1 or config.get('release')!='R9':
        raise ValueError('Configuración R9 inexacta')
    folder=dentro(root,EVIDENCIA); mp=folder/'manifiesto.json'
    if sha(mp)!=config.get('manifiesto_sha256'): raise ValueError('Manifiesto R9 alterado')
    manifest=read(mp)
    required=set(ARCHIVOS.values())|{'aceptadas.json','base-semantica.json','cobertura-r8.json',
        'auditorias/auditoria-a.json','auditorias/auditoria-b.json'}
    required|={f'{kind}/{case}.{ext}' for case in PIN for kind,ext in [('filas','json'),('normativa','txt')]}
    files=manifest.get('archivos',{})
    if manifest.get('format_version')!=1 or manifest.get('release')!='R9' or not required<=set(files):
        raise ValueError('Manifiesto R9 incompleto')
    sources={'revision_ronda_9':cp,'manifiesto_ronda_9':mp}
    for rel,h in files.items():
        path=dentro(folder,rel)
        if sha(path)!=h: raise ValueError('Evidencia R9 alterada: '+rel)
        sources['ronda_9_'+rel]=path
    baseline=read(folder/'base-semantica.json'); cob8=read(folder/'cobertura-r8.json')
    if sha(folder/'base-semantica.json')!=PIN_REGLAS or read(root/'ontologia/semantica.json')!=baseline:
        raise ValueError('R9 no puede modificar el núcleo R8')
    comprobar_resumen(cob8['resumen'])
    accepted=read(folder/'aceptadas.json')
    if set(accepted)!={'format_version','release','release_base','declaraciones','archivos_instalables'}:
        raise ValueError('Esquema de aceptadas R9 inexacto')
    if accepted['format_version']!=1 or accepted['release']!='R9' or accepted['release_base']!='R8':
        raise ValueError('Formato/lanzamiento R9 incorrectos')
    if accepted['archivos_instalables']!={k:sha(folder/v) for k,v in ARCHIVOS.items()}:
        raise ValueError('Payload R9 no cubre datos/modelo/shapes exactos')
    _auditorias(folder,accepted)
    _datos(folder,accepted,cob8); _modelo(folder)
    if sha(folder/ARCHIVOS['shapes'])!=SHAPE_SHA: raise ValueError('Forma R9 alterada')
    return config,folder,baseline,accepted,cob8,sources

def cargar_shapes(root=ROOT):
    _,folder,*_=cargar(root)
    return Graph().parse(folder/ARCHIVOS['shapes'],format='turtle')

def construir(report,rules,base,root=ROOT):
    config,folder,baseline,accepted,cob8,sources=cargar(root)
    if str(base)!=BASE or rules!=baseline or report['resumen']!=cob8['resumen']:
        raise ValueError('R9 requiere la misma base semántica R8')
    bydef={v.get('definicion_iri'):v for v in report['variables']}
    old={v.get('definicion_iri'):v for v in cob8['variables']}
    for p in PIN.values():
        if bydef.get(p['definicion_iri'])!=old[p['definicion_iri']]:
            raise ValueError('Variable R9 cambió de contexto en reporte vivo')
    graph=_datos(folder,accepted,cob8)+_modelo(folder)
    for case,p in PIN.items():
        for rel in (f'filas/{case}.json',f'normativa/{case}.txt'):
            file=folder/rel; entity=URIRef(file.as_uri())
            graph.add((entity,RDF.type,PROV.Entity))
            graph.add((entity,MEX.sha256Evidencia,Literal(sha(file))))
            graph.add((URIRef(p['sujeto']),PROV.wasDerivedFrom,entity))
    return graph,{'format_version':1,'release':'R9','declaraciones_unidad':2,
                  'formas_exclusion':1,'manifiesto_sha256':config['manifiesto_sha256']},sources
