"""Publica el recibo R9 tras comprobar material, suite y sincronización reales."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
E = ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
sys.path.insert(0, str(ROOT/'scripts'))
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return {'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def require(ok,msg):
    if not ok: raise ValueError(msg)

def main():
    require(not (ROOT/'reports/ronda-9.json').exists(), 'R9 ya existe')
    from integrar_ronda_9 import cargar
    cargar(ROOT)  # Verifica manifiesto, material y auditorías antes de cerrar.
    base = read(E/'base.json')
    require(sha(ROOT/'ontologia/semantica.json') == base['sha256']['ontologia/semantica.json'], 'Núcleo R8 cambió')
    for rel,h in base['sha256'].items():
        if ('manifiesto' in rel or rel.startswith('ontologia/revision-')
                or re.match(r'reports/ronda-[1-8]\.',rel)):
            require(sha(ROOT/rel)==h,'Histórico alterado: '+rel)
    cov = read(ROOT/'data/semantica/cobertura.json')
    require(cov['resumen']==base['resumen'],'R9 alteró los conteos semánticos')
    load = read(ROOT/'reports/portal-carga.json')
    sync = read(ROOT/'reports/studio-portal-sync.json')
    require(load['shacl'].get('conforms') is True,'SHACL portal')
    require(sync.get('verificado') is True and sync['shacl'].get('conforms') is True,'Studio sin verificar')
    require(load['semantica']['huellas_entrada']['reglas']==sha(ROOT/'ontologia/semantica.json'),'Carga semántica vieja')
    suite = E/'validacion/suite-r9-postgeneracion.log'
    log = suite.read_text(encoding='utf-8-sig')
    matches = re.findall(r'Ran (\d+) tests? in ([\d.]+)s',log)
    require(matches and int(matches[-1][0])>181 and re.search(r'^OK\s*$',log,re.M)
            and not re.search(r'^FAILED',log,re.M), 'Suite R9 no verde')
    seleccion = read(E/'seleccion-final.json')
    for item in seleccion['archivos']:
        require(sha(ROOT/item['ruta'])==item['sha256'],'Selección alterada: '+item['ruta'])
    cfg=read(ROOT/'ontologia/revision-ronda-9.json')
    evidence=ROOT/cfg['evidencia']
    require(load['semantica']['huellas_entrada'].get('revision_ronda_9')==sha(ROOT/'ontologia/revision-ronda-9.json'), 'Carga sin R9 actual')
    require(load['semantica']['huellas_entrada'].get('manifiesto_ronda_9')==sha(evidence/'manifiesto.json'), 'Carga sin manifiesto R9 actual')
    queries=read(E/'validacion/consultas-r9.json')
    require(queries['declaraciones']==2 and queries['variables_con_ambos']==0, 'Consultas R9 no conformes')
    result={
        'format_version':1, 'release':'R9',
        'fecha_utc':datetime.now(timezone.utc).isoformat(),
        'estado':'cerrado_integrado_validado_y_sincronizado',
        'expediente':E.relative_to(ROOT).as_posix(),
        'delta':{'significados':0,'conceptos':0,'correspondencias_revisadas':0,
                 'declaraciones_unidad':2,'formas_shacl_exclusion':1,
                 'intervalos':0,'jerarquias_clinicas':0},
        'resumen_actual':cov['resumen'],
        'pendientes':{'significados_reales':138,'vigencias':16,'candidatas_semanticas':17,
                      'referencia_catalogo':'des_mpo_res','encabezados_corruptos':2,
                      'vigencias_acceso_no_resuelto':['V13','V14']},
        'pilotos':{'P1':'2 declaraciones cualificadas sobre definiciones; hm3 sin vínculo QUDT',
                   'P2':'negativo: no hay bordes temporales documentados',
                   'P3':'negativo: 101 conceptos sin jerarquía documental justificable',
                   'P4':'exclusión documentado/candidato; permite ninguno'},
        'vistas_derivadas':seleccion,
        'pruebas':dict(ref(suite),pruebas=int(matches[-1][0]),segundos=float(matches[-1][1]),resultado='OK'),
        'consultas_afectadas':dict(ref(E/'validacion/consultas-r9.json'),resultado=queries),
        'portal':{'triples_combinados':load['triples_combinados'],'sintaxis':load.get('sintaxis'),'shacl':load['shacl']},
        'studio':sync,
        'integridad':{'base':ref(E/'base.json'),'respaldo':ref(E/'respaldo-previo.json'),
                      'manifiesto_r9':ref(evidence/'manifiesto.json'),
                      'aplicacion':ref(E/'aplicacion.json')},
        'plan_revisado_por_chat':'docs/plan-actualizado-tras-r8.md',
        'gemma':'excluido_sin_cambios','contactos_externos':0,
        'limites':['Una unidad declarada por una definición no se atribuye globalmente a otros recursos o periodos.',
                   'No se materializan valores, conversiones, intervalos ni jerarquías sin respaldo.',
                   'Las 1191 oportunidades priorizadas siguen sin autorizar joins.',
                   'Los 138 significados y las 16 vigencias requieren evidencia primaria nueva; no se repiten búsquedas agotadas sin una pista concreta.']}
    (ROOT/'reports/ronda-9.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=f'''# Ronda 9 — plan posterior a R8

Estado: cerrado, integrado, validado y sincronizado.

## Resultado

- Dos declaraciones de unidad cualificadas: milímetros y hectáreas, con términos QUDT verificados y literales de fuente conservados.
- Una regla SHACL impide que una variable tenga significado documentado y candidato simultáneamente; admite variables pendientes sin ninguno.
- Pilotos negativos de periodos e intervalos y de jerarquía clínica: no se incorporaron fechas ni relaciones por suposición. El hm³ permanece sin vínculo QUDT.
- **1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas.**
- **{result['pruebas']['pruebas']} pruebas Python OK**, RDF y SHACL conformes.
- Portal: **{load['triples_combinados']} triples**. Studio: **{sync['triples_totales_studio']} triples**, verificado y con ediciones ajenas preservadas.

## Auditorías y vistas de trabajo

Se trazaron las 17 candidatas y los 19 casos de vigencia/anomalía; se reconciliaron las 5523 columnas. La nueva prioridad de revisión cubre 1191 pares estructurales y presenta 50 primeros candidatos; no autoriza joins.

Las correcciones de propuestas anteriores —IRIs tentativas, sello autorreferente, hashes truncados, literales sin tildes y etiquetas de organismo— se conservan como antecedentes. Solo se instaló el material final aceptado.

## Pendientes externos

Quedan **138 significados, 16 vigencias y 17 candidatas** dependientes del respaldo documental faltante. V13/V14 mantienen acceso no resuelto; `des_mpo_res` no tiene catálogo aplicable identificado. Las dos filas corruptas de encabezado siguen conservadas, fuera del conteo de significados reales.

El chat solicitado revisó R8 y devolvió el plan que originó esta ejecución. Gemma quedó excluido y no se contactó a publicadores.

Detalle, hashes, pruebas, auditorías y recibos: [ronda-9.json](ronda-9.json).
'''
    (ROOT/'reports/ronda-9.md').write_text(md,encoding='utf-8')
    print(json.dumps({'estado':result['estado'],'pruebas':result['pruebas']['pruebas'],'portal':load['triples_combinados'],'studio':sync['triples_totales_studio']}))

if __name__=='__main__': main()
