"""Copia únicamente propuestas aprobadas; no instala ni modifica el núcleo."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import shutil
from comprobar import check

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r4'
TARGET = ROOT / 'data/integracion-ronda-4'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if TARGET.exists():
        raise ValueError('Evidencia de ronda 4 ya fijada')
    base = read(STAGE/'fuentes/ontologia/semantica.json')
    baseline = read(STAGE/'fuentes/data/semantica/cobertura.json')
    audit_a = read(STAGE/'auditoria-a/entrega.json')
    audit_b = read(STAGE/'auditoria-b/entrega.json')
    if any(h.get('bloquea') for h in audit_b.get('hallazgos_codigo',[])):
        raise ValueError('Auditoría de código contiene bloqueos sin resolver')
    required_code={p.relative_to(STAGE/'integrador').as_posix() for p in (STAGE/'integrador/codigo').rglob('*.py')}
    required_code.update(['comprobar.py','fijar_aceptaciones.py','instalar.py','verificar_studio.py'])
    if not required_code.issubset(audit_b['sha_codigo']):
        raise ValueError('Código de instalación sin auditoría exacta completa')
    for relative,expected in audit_b['sha_codigo'].items():
        if sha(STAGE/'integrador'/relative)!=expected:
            raise ValueError('Código cambió tras auditoría: '+relative)
    deliveries={}
    for name in [f'lote-{i}' for i in range(1,7)]+['ambiguedades']:
        control=check(name)
        if not control['valido']:
            raise ValueError('Entrega inválida: '+str(control))
        for audit in [audit_a,audit_b]:
            if audit['sha_entregas'][name]!=control['sha256']:
                raise ValueError('Auditoría desactualizada: '+name)
        deliveries[name]=read(STAGE/name/'entrega.json')
    def approvals(audit,category):
        rows=[r for r in audit['dictamenes'] if r['tipo']==category]
        if len(rows)!=len({r['id'] for r in rows}):
            raise ValueError('Auditoría con IDs duplicados')
        entries=[r for d in deliveries.values() for r in d[category]]
        key='id' if category=='reglas' else 'columna'
        if {r['id'] for r in rows}!={r[key] for r in entries}:
            raise ValueError('Auditoría no cubre cada propuesta exacta: '+category)
        return {r['id']:r for r in rows if r['dictamen']=='aceptar'}
    ar, av=approvals(audit_a,'reglas'),approvals(audit_b,'vinculos')
    accepted={'reglas':[],'vinculos':[],'conceptos':{},'origenes':{},'resumen':{}}
    concepts=copy.deepcopy(base['conceptos'])
    for name,delivery in deliveries.items():
        for key,value in delivery['conceptos_nuevos'].items():
            if key in concepts and concepts[key]!=value:
                raise ValueError('Conceptos incompatibles: '+key)
            concepts[key]=value
        for entry in delivery['reglas']:
            if entry['id'] in ar:
                rule=copy.deepcopy(entry)
                rule['fuente_revision']='data/integracion-ronda-4/entregas/'+name+'/entrega.json'
                accepted['reglas'].append(rule)
                accepted['origenes'][rule['id']]=['entregas/'+name+'/entrega.json','auditorias/auditoria-a.json']
    supported={v['definicion_iri'] for v in baseline['variables'] if v['estado']=='respaldada_por_definicion'}
    supported.update(d for r in accepted['reglas'] for d in r['definiciones'])
    for name,delivery in deliveries.items():
        decisions={d['columna']:d for d in delivery['decisiones_columnas']}
        for entry in delivery['vinculos']:
            if entry['columna'] in av and decisions[entry['columna']]['definicion_iri'] in supported:
                accepted['vinculos'].append(entry)
                accepted['origenes'][entry['columna']]=['entregas/'+name+'/entrega.json','auditorias/auditoria-b.json']
    needed={r['concepto'] for r in accepted['reglas']}
    stack=list(needed)
    while stack:
        key=stack.pop()
        parent=concepts[key][2]
        if parent and parent not in needed:
            needed.add(parent)
            stack.append(parent)
    accepted['conceptos']={k:concepts[k] for k in sorted(needed) if k not in base['conceptos']}
    accepted['resumen']={'significados_nuevos':len(accepted['reglas']), 'correspondencias_nuevas':len(accepted['vinculos']),
        'significados_respaldados_totales':1212+len(accepted['reglas']),
        'correspondencias_revisadas_totales':865+len(accepted['vinculos']),
        'columnas_revisadas_en_ronda':sum(len(d['decisiones_columnas']) for d in deliveries.values()),
        'significados_revisados_en_ronda':sum(len(d['decisiones_significados']) for n,d in deliveries.items() if n!='ambiguedades')}
    for role in list(deliveries)+['investigacion','catalogos']:
        shutil.copytree(STAGE/role,TARGET/'entregas'/role)
    # Los respaldos de configuración pueden contener credenciales: no son evidencia del grafo.
    public_chat={'entrega.json','pendientes.json','resultado.md','listo.json','evaluacion.json',
        'respuestas-saneadas.json','adenda-ui.json','corpus.json','cambio-modelo.json',
        'reinicio-requerido.json','ejecutar_chat.mjs','oraculo.py','oraculo2.py','oraculo3.py',
        'antes-cambio-modelo','ensayo-gemma4','ensayo-gemini31'}
    shutil.copytree(STAGE/'chat',TARGET/'entregas/chat',
        ignore=lambda directory,names:[n for n in names if n not in public_chat])
    for name in ['auditoria-a','auditoria-b']:
        write(TARGET/'auditorias'/f'{name}.json',read(STAGE/name/'entrega.json'))
    write(TARGET/'base-semantica.json',base)
    write(TARGET/'base-cobertura.json',baseline)
    write(TARGET/'aceptadas.json',accepted)
    shutil.copytree(STAGE/'integrador/codigo',TARGET/'codigo')
    for name in ['comprobar.py','fijar_aceptaciones.py','instalar.py','verificar_studio.py']:
        shutil.copy2(STAGE/'integrador'/name,TARGET/'codigo'/name)
    manifest={'ronda':4,'archivos':{p.relative_to(TARGET).as_posix():sha(p) for p in TARGET.rglob('*') if p.is_file()},
        'insumos':{p:sha(ROOT/p) for p in ['data/portal/inventario.json','data/portal/contenido-inspeccion.json']}}
    write(TARGET/'manifiesto.json',manifest)
    write(STAGE/'integrador/config-propuesta.json',{'version':1,'evidencia':'data/integracion-ronda-4',
        'manifiesto_sha256':sha(TARGET/'manifiesto.json'),'esperado':accepted['resumen'],
        'respaldo':'propuestas/pendientes-muse-r4/integrador/antes-r4.zip','respaldo_sha256':sha(STAGE/'integrador/antes-r4.zip')})
    print(json.dumps(accepted['resumen'],ensure_ascii=True))

if __name__=='__main__':
    main()
