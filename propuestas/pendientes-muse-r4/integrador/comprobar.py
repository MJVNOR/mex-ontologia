"""Control independiente de cobertura, huellas y alcance de las propuestas."""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r4'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import columnas, huella, interpretacion, validar_calificador
from integrar_contenido import clave

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(name):
    folder = STAGE / name
    source_manifest = read(STAGE / 'fuentes/manifiesto.json')
    if name != 'ambiguedades':
        assert sha(folder / 'asignacion.json') == source_manifest['lotes'][name]['sha256'], 'Asignación inicial modificada'
    assignment = read(folder / 'asignacion.json')
    if name == 'ambiguedades':
        original = read(STAGE / 'fuentes/reports/pendientes-semanticos.json')
        assert assignment['columnas'] == [c for c in original['columnas'] if c['estado']=='ambigua_por_nombre'], 'Asignación ambigua modificada'
        assignment['variables_pendientes'] = []
    if (folder / 'asignacion-adicional.json').exists():
        additional_manifest = read(STAGE / 'integrador/asignaciones-adicionales.json')
        assert sha(folder / 'asignacion-adicional.json') == additional_manifest['columnas_adicionales'][name]['sha256'], 'Asignación adicional modificada'
        assignment['columnas'].extend(read(folder / 'asignacion-adicional.json')['columnas'])
    delivery = read(folder / 'entrega.json')
    if name == 'ambiguedades':
        assert not delivery.get('reglas') and not delivery.get('conceptos_nuevos'), 'Rol ambiguo no puede modificar significados'
    marker = read(folder / 'listo.json')
    assert (marker.get('sha256') or marker.get('sha256_entrega')) == sha(folder / 'entrega.json'), 'Marcador SHA no coincide'
    inventory = read(ROOT / 'data/portal/inventario.json')
    inspection = read(ROOT / 'data/portal/contenido-inspeccion.json')
    baseline = read(STAGE / 'fuentes/data/semantica/cobertura.json')
    previous = read(STAGE / 'fuentes/ontologia/semantica.json')
    cols = {c['iri']: c for c in columnas(inventory, inspection, 'https://example.org/mex-ontologi/')}
    variables = {v['definicion_iri']: v for v in baseline['variables'] if v.get('definicion_iri')}
    names = collections.Counter((v['conjunto'], clave(v['variable'])) for v in variables.values())
    errors = []
    def require(ok, why):
        if not ok:
            errors.append(why)
    for key, assigned, identifier in [('decisiones_columnas', 'columnas', 'columna'),
                                       ('decisiones_significados', 'variables_pendientes', 'definicion_iri')]:
        if name == 'ambiguedades' and key == 'decisiones_significados':
            continue  # Contexto diagnóstico; las definiciones tienen propietario en los seis lotes.
        rows = delivery.get(key, [])
        ids = [r[identifier] for r in rows]
        require(len(ids)==len(set(ids)), 'Decisiones duplicadas: '+key)
        require(set(ids)=={r[identifier] for r in assignment[assigned]}, 'Partición incompleta: '+key)
        for row in rows:
            require(bool(row.get('motivo')), 'Decisión sin motivo: '+row[identifier])
            if row.get('decision')=='proponer':
                require(bool(row.get('evidencia')), 'Propuesta sin evidencia: '+row[identifier])
    props = {r['columna']: r for r in delivery.get('decisiones_columnas',[]) if r.get('decision')=='proponer'}
    links = delivery.get('vinculos', [])
    require(len(links)==len({r['columna'] for r in links}), 'Vínculos repetidos')
    require(set(props)=={r['columna'] for r in links}, 'Decisiones y vínculos discrepan')
    rules = delivery.get('reglas', [])
    semantic_props = {r['definicion_iri'] for r in delivery.get('decisiones_significados',[]) if r.get('decision')=='proponer'}
    require(semantic_props=={d for r in rules for d in r['definiciones']}, 'Decisiones y reglas discrepan')
    merged = json.loads(json.dumps(previous))
    for key, value in delivery.get('conceptos_nuevos',{}).items():
        require(key not in merged['conceptos'] or merged['conceptos'][key]==value, 'Concepto previo alterado: '+key)
        merged['conceptos'][key]=value
    merged['reglas_descripcion_exacta'].extend(rules)
    if name == 'ambiguedades':
        # Sus vínculos pueden depender de significados propuestos por el propietario de la definición.
        for other in [f'lote-{i}' for i in range(1,7)]:
            proposals = read(STAGE / other / 'entrega.json')
            for key,value in proposals.get('conceptos_nuevos',{}).items():
                require(key not in merged['conceptos'] or merged['conceptos'][key]==value, 'Concepto incompatible: '+key)
                merged['conceptos'][key]=value
            merged['reglas_descripcion_exacta'].extend(proposals.get('reglas',[]))
    for key,value in merged['conceptos'].items():
        require(isinstance(value,list) and len(value)==3, 'Formato de concepto inválido: '+key)
        visited=set()
        node=key
        while node is not None:
            if node in visited or node not in merged['conceptos']:
                errors.append('Ciclo o padre ausente: '+key)
                break
            visited.add(node)
            node=merged['conceptos'][node][2]
    for r in rules:
        require(len(r.get('definiciones',[]))==1, 'Regla no restringida a fila: '+r['id'])
        v = variables[r['definiciones'][0]]
        for field, key in [('nombres','variable'),('descripciones','descripcion'),('conjuntos','conjunto'),('diccionarios','diccionario')]:
            require(r.get(field)==[v[key]], 'Restricción literal distinta: '+r['id']+'/'+field)
        require(r.get('huella_fila_diccionario')==v['huella_fila_diccionario'], 'Huella fila distinta: '+r['id'])
        require(r.get('concepto') in merged['conceptos'], 'Concepto ausente: '+r['id'])
        if r.get('calificador'):
            validar_calificador(r['calificador'])
        try:
            match = interpretacion(v['variable'],v['descripcion'],v['conjunto'],merged,v['diccionario'],v['definicion_iri'])
            require(match.get('regla')==r['id'], 'Regla no aplicada: '+r['id'])
        except ValueError as exc:
            errors.append(str(exc))
    for r in links:
        col = cols[r['columna']]
        prop = props.get(r['columna'],{})
        v = variables.get(prop.get('definicion_iri'))
        require(v is not None, 'Destino sin definición exacta: '+r['columna'])
        if v is None:
            continue
        for key in ['recurso','campo','huella_esquema']:
            require(r.get(key)==col[key], 'Evidencia de esquema distinta: '+r['columna']+'/'+key)
        for key in ['diccionario','descripcion','huella_fila_diccionario']:
            require(r.get(key)==v[key], 'Evidencia documental distinta: '+r['columna']+'/'+key)
        require(col['conjunto']==v['conjunto'], 'Conjunto distinto: '+r['columna'])
        if r.get('definicion_iri'):
            require(name=='ambiguedades' and r['definicion_iri']==v['definicion_iri'], 'Selección de definición fuera de alcance: '+r['columna'])
        else:
            require(col['nombre_unico'] and names[(v['conjunto'],clave(v['variable']))]==1, 'Nombre ambiguo: '+r['columna'])
        actual = interpretacion(v['variable'],v['descripcion'],v['conjunto'],merged,v['diccionario'],v['definicion_iri'])
        require(actual['estado']=='respaldada_por_definicion' and actual.get('concepto')==r.get('concepto'), 'Destino no respaldado: '+r['columna'])
        require(bool(r.get('criterio')), 'Sin criterio: '+r['columna'])
    return {'lote':name,'sha256':sha(folder/'entrega.json'),'columnas':len(delivery.get('decisiones_columnas',[])),
            'significados':len(delivery.get('decisiones_significados',[])), 'vinculos':len(links),'reglas':len(rules),
            'errores':errors,'valido':not errors}

if __name__ == '__main__':
    result=[]
    for name in (sys.argv[1:] or [f'lote-{i}' for i in range(1,7)]):
        try:
            result.append(check(name))
        except Exception as exc:
            result.append({'lote':name,'valido':False,'error':repr(exc)})
    (STAGE/'integrador/control-entregas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True))
