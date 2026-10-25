"""Instala la extensión exacta tras controles; conserva las evidencias históricas."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[3]
STAGE=ROOT/'propuestas/pendientes-muse-r4'
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(STAGE/'integrador/codigo/scripts'))
from consolidar_semantica import construir

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p,obj):
    temp=p.with_suffix(p.suffix+'.r4-temporal')
    temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temp.replace(p)

def main():
    if (ROOT/'ontologia/revision-ronda-4.json').exists():
        raise ValueError('Ronda 4 ya instalada; no repetir')
    manifest=read(STAGE/'fuentes/manifiesto.json')
    for p,expected in manifest['insumos_centrales'].items():
        if sha(ROOT/p)!=expected:
            raise ValueError('Base central cambió: '+p)
    folder=ROOT/'data/integracion-ronda-4'
    accepted=read(folder/'aceptadas.json')
    before=read(folder/'base-semantica.json')
    merged=copy.deepcopy(before)
    merged['reglas_descripcion_exacta'].extend(accepted['reglas'])
    merged['vinculos_documentales_revisados'].extend(accepted['vinculos'])
    merged['conceptos'].update(accepted['conceptos'])
    inventory=read(ROOT/'data/portal/inventario.json')
    inspection=read(ROOT/'data/portal/contenido-inspeccion.json')
    reference=read(ROOT/'data/portal/lote-cruces/catalogo-municipal-portal.json')
    graph,model,report=construir(inventory,inspection,merged,reference,'https://example.org/mex-ontologi/')
    baseline=read(folder/'base-cobertura.json')
    current_vars={v['definicion_iri']:v for v in report['variables']}
    for v in baseline['variables']:
        if v['estado']=='respaldada_por_definicion' and current_vars[v['definicion_iri']]!=v:
            raise ValueError('Significado respaldado cambió: '+v['definicion_iri'])
    actual={v['columna']:v for v in report['correspondencias'] if v['estado']=='documental_revisada'}
    for row in baseline['correspondencias']:
        if row['estado']=='documental_revisada' and actual.get(row['columna'])!=row:
            raise ValueError('Correspondencia anterior cambió: '+row['columna'])
    config=read(STAGE/'integrador/config-propuesta.json')
    config['estados_variables_esperados']=report['resumen']['estados_variables']
    config['estados_correspondencias_esperados']=report['resumen']['estados_correspondencias']
    # Actualizar expectativas vigentes; los conteos históricos y sus manifiestos siguen intactos.
    agents=read(ROOT/'ontologia/revision-agentes.json')
    agents['esperado_actual'].update({
        'conceptos':len(merged['conceptos']),
        'variables_respaldadas':report['resumen']['estados_variables'].get('respaldada_por_definicion',0),
        'variables_pendientes':report['resumen']['estados_variables'].get('candidata_sin_definicion_suficiente',0),
        'correspondencias_revisadas':len(actual)})
    round2=read(ROOT/'ontologia/revision-ronda-2.json')
    round2['esperado_actual'].update({'revisadas':len(actual),
        'candidatas':report['resumen']['estados_correspondencias'].get('candidata_por_nombre',0)})
    write(STAGE/'integrador/simulacion.json',{'resumen':report['resumen'],'base_preservada':True,
        'reglas_nuevas':len(accepted['reglas']),'vinculos_nuevos':len(accepted['vinculos'])})
    for p in (STAGE/'integrador/codigo').rglob('*.py'):
        destination=ROOT/p.relative_to(STAGE/'integrador/codigo')
        destination.parent.mkdir(parents=True,exist_ok=True)
        temp=destination.with_suffix('.py.r4-temporal')
        shutil.copy2(p,temp)
        temp.replace(destination)
    write(ROOT/'ontologia/revision-agentes.json',agents)
    write(ROOT/'ontologia/revision-ronda-2.json',round2)
    write(ROOT/'ontologia/semantica.json',merged)
    write(ROOT/'ontologia/revision-ronda-4.json',config)
    # Validación independiente de la evidencia y del objeto instalado exacto.
    sys.path.insert(0,str(STAGE/'integrador/codigo/scripts'))
    from integrar_ronda_4 import validar
    validar(merged,ROOT)
    write(STAGE/'integrador/instalacion.json',{'instalado':True,'resumen':report['resumen'],
        'semantica_sha256':sha(ROOT/'ontologia/semantica.json'),
        'config_sha256':sha(ROOT/'ontologia/revision-ronda-4.json')})
    print(json.dumps(report['resumen'],ensure_ascii=True))

if __name__=='__main__':
    main()
