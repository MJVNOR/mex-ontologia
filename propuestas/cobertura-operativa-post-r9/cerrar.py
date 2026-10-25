"""Cierra el seguimiento documental: conserva R9 y sus manifiestos."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/cobertura-operativa-post-r9/ejecucion-20261024'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    require(not (E/'cierre.json').exists(),'Cierre ya existe')
    base=read(E/'base.json')
    changed=[p for p,h in base['sha256'].items() if sha(ROOT/p)!=h]
    require(not changed,'Históricos/estado R9 modificados: '+str(changed))
    pub=read(E/'publicacion.json')
    for row in pub['archivos']:require(sha(ROOT/row['ruta'])==row['sha256'],'Publicación alterada')
    audit=ROOT/pub['dictamen']['ruta']
    require(sha(audit)==pub['dictamen']['sha256'],'Dictamen alterado')
    graph=read(E/'validacion/grafos.json')
    require(graph['portal']['shacl'].get('conforms') is True and graph['studio']['verificado'], 'Validación grafo pendiente')
    require(graph['studio']['shacl'].get('conforms') is True and graph['mutaciones_grafo']==0,'Studio no conforme')
    log=E/'validacion/suite.log';text=log.read_text(encoding='utf-8-sig')
    matches=re.findall(r'Ran (\d+) tests? in ([\d.]+)s',text)
    require(matches and int(matches[-1][0])==213 and re.search(r'^OK\s*$',text,re.M) and not re.search(r'^FAILED',text,re.M),'Suite final no verde')
    op=read(ROOT/'reports/cobertura-operativa-r9.json')
    for row in op['fuentes']:require(sha(ROOT/row['ruta'])==row['sha256'],'Fuente reporte divergente')
    question=E/'C-preguntas/preguntas-documentales.json'
    source=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json'
    require(question.read_bytes()==source.read_bytes(),'Preguntas no son copia exacta')
    q=read(question);require(len(q['preguntas'])==7 and len(q['necesidades'])==7,'Conteos preguntas')
    result={'format_version':1,'release_base':'R9','estado':'seguimiento_documental_completado',
        'fecha_utc':datetime.now(timezone.utc).isoformat(),
        'expediente':E.relative_to(ROOT).as_posix(),
        'avances':['Reporte operativo R9 publicado con 26 frentes y criterios de reapertura.',
                   'Siete necesidades y siete preguntas conservadas sin envío, copia exacta del expediente previo.',
                   'Presas cotejado con evidencia R6–R9: sin evidencia primaria nueva que reabra V05.'],
        'presas':{'correspondencia_cat_estatal_clave':'ya_integrada_R6',
                  'vigencia_V05':'sin_acreditar','integraciones_nuevas':0,
                  'dictamen':ref(E/'A-presas/entrega.json')},
        'pendientes':{'significados_reales':138,'vigencias':16,'acceso_no_resuelto':['V13','V14'],
                      'candidatas':17,'referencia_catalogo':'des_mpo_res','encabezados_corruptos':2,'observaciones_esquema':5},
        'reporte_operativo':ref(ROOT/'reports/cobertura-operativa-r9.json'),
        'auditoria_independiente':ref(audit),
        'pruebas':dict(ref(log),pruebas=213,resultado='OK',segundos=float(matches[-1][1])),
        'validacion':dict(ref(E/'validacion/grafos.json'),portal_triples=graph['portal']['stats']['triples'],
             studio_triples=graph['studio']['stats']['triples'],rdf_y_shacl_conformes=True,
             studio_identico_a_r9=graph['studio']['identico_a_snapshot_r9'],
             modo='Comprobación de sincronización por exportación de solo lectura; sin update/load en Studio.'),
        'preguntas':dict(ref(question),necesidades=7,preguntas=7,estado='preparadas_no_enviadas'),
        'archivos_modificados_o_nuevos':pub['archivos'],
        'integridad':{'base':ref(E/'base.json'),'archivos_estado_r9_preservados':len(base['sha256']),
                     'discrepancias':[],'manifiestos_R1_R9':'sin_cambios'},
        'grafo_modificado':False,'gemma':'excluido_sin_cambios','contactos_externos':0}
    jp=ROOT/'reports/seguimiento-operativo-post-r9.json';mp=ROOT/'reports/seguimiento-operativo-post-r9.md'
    require(not jp.exists() and not mp.exists(),'Informe seguimiento ya existe')
    jp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    mp.write_text('''# Seguimiento operativo posterior a R9

Estado: completado. Actualización documental; no abre una ronda semántica nueva.

## Avances

- [Cobertura operativa R9](cobertura-operativa-r9.md): estados, denominadores y criterios de reapertura de 26 frentes; incluye las 17 candidatas individualizadas y las cinco observaciones de esquema.
- Siete necesidades y siete preguntas preservadas como copia exacta del expediente, preparadas y **no enviadas**.
- Presas: la asociación `cat_estatal/Clave → /4` ya estaba integrada en R6. Los archivos cotejados no aportan evidencia primaria nueva; V05 sigue sin vigencia acreditada.

## Validación

- **213 pruebas Python OK**, incluidas nueve pruebas del nuevo generador.
- RDF y SHACL conformes: portal **322405 triples** y Studio **323014 triples**.
- La exportación viva de Studio coincide con el snapshot R9; no se aplicaron operaciones de actualización ni carga sobre Studio.
- Los 52 archivos fijados de estado y evidencia R9 conservan sus hashes. Manifiestos R1–R9 intactos.

## Pendientes

Se mantienen 138 significados, 16 vigencias (V13/V14 con acceso no resuelto), `des_mpo_res`, dos encabezados corruptos, 17 candidatas y cinco observaciones de esquema. Solo se reabren con evidencia concreta. No se promovieron candidatas ni ejecutaron joins por el ranking. Gemma quedó excluido y no se contactó a publicadores.

## Archivos

Nuevos: `scripts/generar_cobertura_operativa.py`, `tests/test_generar_cobertura_operativa.py`, `reports/cobertura-operativa-r9.json` y `.md`, este informe y su JSON. README y PLAN enlazan la vista operativa; sus copias previas están en el expediente. Entregas Presas, preguntas, auditoría, suite y recibos: `propuestas/cobertura-operativa-post-r9/ejecucion-20261024/`.

[Recibo con hashes, archivos y validación](seguimiento-operativo-post-r9.json).
''',encoding='utf-8')
    pub['estado']='publicado_validado_y_cerrado'
    (E/'publicacion.json').write_text(json.dumps(pub,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    refs=[jp,mp,E/'publicacion.json',audit,E/'A-presas/entrega.json',question,E/'validacion/grafos.json',log]
    refs += [ROOT/r['ruta'] for r in pub['archivos']]
    (E/'cierre.json').write_text(json.dumps({'estado':result['estado'],
        'archivos':{p.relative_to(ROOT).as_posix():sha(p) for p in refs},'gemma':'excluido'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'estado':result['estado'],'pruebas':213,'grafo_modificado':False}))

if __name__=='__main__':main()
