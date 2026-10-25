"""Detecta columnas que pasan a candidatas por los significados propuestos."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
STAGE=ROOT/'propuestas/pendientes-muse-r4'
sys.path.insert(0,str(ROOT/'scripts'))
from consolidar_semantica import construir

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    base=read(STAGE/'fuentes/ontologia/semantica.json')
    pending=read(STAGE/'fuentes/reports/pendientes-semanticos.json')
    columns={c['columna']:c for c in pending['columnas']}
    merged=copy.deepcopy(base)
    owners={}
    initial=set()
    inputs={}
    for name in [f'lote-{i}' for i in range(1,7)]:
        folder=STAGE/name
        assignment=read(folder/'asignacion.json')
        for row in assignment['columnas']+assignment['variables_pendientes']:
            owners[row['conjunto']]=name
        initial.update(c['columna'] for c in assignment['columnas'])
        delivery=read(folder/'entrega.json')
        inputs[name]=sha(folder/'entrega.json')
        for k,v in delivery.get('conceptos_nuevos',{}).items():
            if k in merged['conceptos'] and merged['conceptos'][k]!=v:
                raise ValueError('Concepto incompatible: '+k+' / '+name)
            merged['conceptos'][k]=v
        merged['reglas_descripcion_exacta'].extend(delivery.get('reglas',[]))
    _,_,report=construir(read(ROOT/'data/portal/inventario.json'),read(ROOT/'data/portal/contenido-inspeccion.json'),
        merged,read(ROOT/'data/portal/lote-cruces/catalogo-municipal-portal.json'),'https://example.org/mex-ontologi/')
    variables={v['iri']:v for v in report['variables'] if v.get('iri')}
    additional=collections.defaultdict(list)
    for mapping in report['correspondencias']:
        if mapping['estado']!='candidata_por_nombre' or mapping['columna'] in initial:
            continue
        row=copy.deepcopy(columns[mapping['columna']])
        v=variables[mapping['variable']]
        row.update(estado=mapping['estado'],correspondencias=[mapping['iri']],definiciones_por_nombre=[v['definicion_iri']])
        additional[owners[row['conjunto']]].append(row)
    output={'sha_entregas_semanticas':inputs,'columnas_adicionales':{}}
    for name in [f'lote-{i}' for i in range(1,7)]:
        path=STAGE/name/'asignacion-adicional.json'
        if path.exists():
            raise ValueError('Asignación adicional ya fijada: '+name)
        payload={'columnas':additional[name], 'motivo':'Nuevas candidatas derivadas de significados propuestos en esta ronda; aprobación semántica independiente todavía requerida.',
            'sha_entregas_semanticas':inputs}
        write(path,payload)
        output['columnas_adicionales'][name]={'cantidad':len(additional[name]),'sha256':sha(path)}
    write(STAGE/'integrador/asignaciones-adicionales.json',output)
    print(json.dumps(output['columnas_adicionales'],ensure_ascii=True))

if __name__=='__main__':
    main()
