"""Cierra R10 con recibos reales y conserva los cierres anteriores."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ampliacion-post-r9/ejecucion-20261024'
M=E/'reanudacion-muse'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(p,value):
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    assert not (ROOT/'reports/ronda-10.json').exists(), 'Cierre ya existente'
    portal=read(ROOT/'reports/portal-carga.json')
    sync=read(ROOT/'reports/studio-portal-sync.json')
    coverage=read(ROOT/'data/semantica/cobertura.json')
    accepted=read(ROOT/'data/integracion-ronda-10/aceptadas.json')
    delta=read(M/'delta-rdf.json')
    publication=read(M/'publicacion.json')
    suite=(M/'suite-r10.log').read_text(encoding='utf-8')
    match=re.search(r'Ran (\d+) tests in ([\d.]+)s',suite)
    assert match and int(match[1])==233 and suite.strip().endswith('OK')
    assert portal['triples_combinados']==322495 and portal['sintaxis']['ok'] and portal['shacl']['conforms']
    assert portal['shacl']['violation_count']==0 and len(portal['consultas'])==30
    assert sync['verificado'] and sync['shacl']['conforms'] and sync['shacl']['violation_count']==0
    assert (sync['triples_insertados'],sync['triples_retirados_gestionados'],sync['triples_totales_studio'])==(90,0,323104)
    assert delta['delta_exacto_integrador_r10'] and delta['triples_retirados']==0
    assert read(M/'D-analisis/v004/dictamen-a3-consolidado.json')['veredicto']=='CONSOLIDADO_APTO_CIERRE_FORMAL'
    base=read(E/'base.json')['sha256']
    historical={rel:h for rel,h in base.items() if 'manifiesto' in Path(rel).name
                or rel.startswith('reports/ronda-') or rel.startswith('ontologia/')}
    assert all(sha(ROOT/rel)==h for rel,h in historical.items()),'Se alteró una base o cierre anterior'
    assert (ROOT/'config.toml').read_bytes()==(E/'config-iri-base.toml').read_bytes()
    assert coverage['resumen']==read(ROOT/'data/integracion-ronda-10/cobertura-r9.json')['resumen']
    backup=ROOT/sync['respaldo']
    assert backup.is_file()
    backup_rel=backup.relative_to(ROOT).as_posix()
    base_backup=read(E/'respaldo-previo.json')
    assert sha(ROOT/base_backup['zip'])==base_backup['sha256']
    for name in ('portal-carga.json','studio-portal-sync.json'):
        shutil.copyfile(ROOT/'reports'/name,M/('cierre-'+name))
    now=datetime.now(timezone.utc)
    evidence=[p for sub in ('A-auditoria','B-auditoria','D-analisis','V-pruebas')
              for p in (M/sub).rglob('*.json') if p.name not in {'check.json'}]
    evidence += [M/name for name in ('preflight.json','instalacion.json','delta-rdf.json',
        'publicacion.json','adenda-trazabilidad.json','cierre-portal-carga.json','cierre-studio-portal-sync.json')]
    report={'format_version':1,'release':'R10','release_base':'R9',
        'fecha_utc':now.isoformat(),'fecha_cliente':now.astimezone(timezone(timedelta(hours=-7))).isoformat(),
        'zona_cliente':'America/Hermosillo','estado':'cerrado_integrado_validado_y_sincronizado',
        'expediente':E.relative_to(ROOT).as_posix(),
        'modelo_reanudacion':'opencode-go/muse-spark-1.3-contributor','mcp':'nativo OpenCode',
        'base_iri':'https://example.org/mex-ontologi/','config_toml_sin_cambios':True,
        'delta':{'significados':0,'conceptos':0,'correspondencias_revisadas':0,'joins':0,
                 'declaraciones_unidad':5,'formas_shacl':6,'triples_agregados':90,'triples_retirados':0},
        'resumen_actual':coverage['resumen'],
        'unidades':[{'id':u['id'],'variable':u['nombre'],'literal':u['unidad_literal'],
                     'unidad_qudt':u['unidad_qudt'],'definicion_iri':u['definicion_iri']} for u in accepted['unidades']],
        'declaraciones_unidad_total':7,
        'analisis':{'top50_filas':50,'candidatas_estructurales':1191,'pares_mapa':3916,
                    'pares_analizados':3,'ejes_por_par':8,'estado':'tres_bloqueados_con_evidencia',
                    'publicaciones':['reports/top50-oportunidades-r9.html','reports/top50-oportunidades-r9.json',
                        'reports/top50-oportunidades-r9.md','reports/analisis-pares-post-r9.md','reports/analisis-pares-post-r9.json'],
                    'itama_consolidado':'propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v003'},
        'pruebas':{'suite_python':233,'segundos':float(match[2]),'resultado':'OK','omitidas':0,
                   'nuevas_integracion':18,'nuevas_cli_publicador':2,'log':str((M/'suite-r10.log').relative_to(ROOT)).replace('\\','/')},
        'validacion':{'portal_triples':322495,'studio_triples':323104,'sintaxis_rdf':True,
                      'portal_shacl':True,'studio_shacl':True,'violaciones':0,'consultas_portal_ejecutadas':30,
                      'delta_exacto_integrador':True,'fixtures_nuevas_formas':'15 infracciones negativas detectadas; controles positivos conformes; motor real',
                      'formas_sin_instancias_portal':portal['shacl'].get('unmatched_shapes',[])},
        'sincronizacion':sync,
        'respaldos':{'base':base_backup,'studio':backup_rel,'studio_sha256':sha(backup)},
        'pendientes':{'significados_reales':138,'vigencias':16,'candidatas_semanticas':17,
                     'referencia_catalogo':'des_mpo_res','encabezados_corruptos':2,'acceso_vigencias':['V13','V14'],
                     'unidades_no_promovidas':['Toneladas: variante local sin acreditar','hm³: término exacto no verificado en la versión respaldada'],
                     'analisis':'Se requiere documentación/cobertura adicional antes de calcular comparaciones.'},
        'fuera_de_alcance':['Gemma','cambiar la base IRI','contactar publicadores','promover significados o candidatas sin respaldo'],
        'trazabilidad':{'historicos_inmutables_comprobados':len(historical),
                       'historicos_sha256':historical,'core_sha256':sha(ROOT/'ontologia/semantica.json'),
                       'config_sha256':sha(ROOT/'config.toml'),
                       'manifiesto_r10_sha256':sha(ROOT/'data/integracion-ronda-10/manifiesto.json'),
                       'evidencia_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(evidence))}},
        'observaciones_resueltas':['Guarda del publicador corregida y probada con CLI instalado en raíz temporal.',
            'ITAMA v003 conserva el resultado y corrige el expediente/sello; duplicado de pruebas obsoleto excluido.',
            'Deriva del wrapper S documentada sin cambio de shapes; adenda-trazabilidad.json.',
            'Fecha errónea del dictamen D/v003 corregida mediante adenda D/v004, sin modificar el dictamen anterior.']}
    summary=('R10 incorpora **cinco declaraciones de unidad cualificadas** y **seis formas SHACL**. '
        'Conserva **1423 significados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas**. '
        '**233 pruebas pasan**; RDF y SHACL conformes. Portal: **322495 triples**. Studio: **323104**, '
        'con respaldo, 90 inserciones y cero retiradas. [Informe R10](reports/ronda-10.md).')
    for name,marker,new_title,old_title in [
        ('README.md','## Estado vigente: ronda 9','## Estado vigente: ronda 10','## Antecedente: ronda 9'),
        ('PLAN.md','## Estado vigente y siguiente trabajo documental','## Estado vigente: R10 y siguiente trabajo documental','## Antecedente R9')]:
        p=ROOT/name;text=p.read_text(encoding='utf-8')
        assert marker in text
        intro=(new_title+'\n\n'+summary+'\n\n'+
            'Se publicaron el [top 50 de oportunidades](reports/top50-oportunidades-r9.html) y '
            '[tres análisis de pares](reports/analisis-pares-post-r9.md), bloqueados con evidencia. '
            'El ranking no autoriza joins. Quedan 138 significados reales, 16 vigencias, 17 candidatas, '
            '`des_mpo_res` y dos encabezados corruptos; requieren evidencia adicional. '
            'Toneladas y hm³ mantienen sus límites. Gemma y la decisión de IRI siguen fuera de alcance.\n\n'+old_title)
        p.write_text(text.replace(marker,intro,1),encoding='utf-8')
    md=['# Ronda 10 — cierre de ampliación posterior a R9','',
        'Fecha del cliente: **2026-10-24, America/Hermosillo**. Ejecución retomada con Muse 1.3 por el MCP nativo de OpenCode.','',summary.split(' [Informe R10]')[0],'',
        '## Integrado','', '| Variable en su definición local | Literal conservado | Término QUDT 3.5.3 |','| --- | --- | --- |']
    md += [f"| {u['variable']} | {u['literal']} | `{u['unidad_qudt']}` |" for u in report['unidades']]
    md += ['', 'MW y GWh califican exclusivamente sus filas «Unidad de Medida». No se transfieren a otras columnas ni a valores observados; no hay factores ni conversiones. Hay siete declaraciones de unidad en total, incluidas las dos de R9.','',
        'Las seis formas controlan coherencia de estados/significados, correspondencias revisadas y el contrato de UnidadDeclarada. Admiten propiedades adicionales válidas; no hay `sh:closed` global.','',
        '## Análisis publicados','',
        '- [Top 50 legible](top50-oportunidades-r9.html): 50 filas reconciliadas sobre 1191 candidatas y 3916 pares; todas `NO_JOIN_APROBADO`.',
        '- [Tres fichas, ocho comprobaciones por par](analisis-pares-post-r9.md): 911, Registro Civil e ITAMA. No se calcularon proporciones, comparaciones de volúmenes ni distribuciones.',
        '- 911: Q1 mal etiquetado/duplicado y Q2 improcedentes sin MUNICIPIO.',
        '- Registro Civil: agregación pendiente de validar, totales incompatibles y meses ausentes.',
        '- ITAMA: faltan archivos completos y respaldo de periodo/escolaridad; expediente consolidado y sellado en [v003](../propuestas/ampliacion-post-r9/ejecucion-20261024/A3-itama/v003/entrega.md).','',
        '## Comprobaciones y respaldo','',
        '- Dos auditorías independientes aceptaron los once casos y los bytes exactos; integrador y pruebas revisados.',
        '- 233 pruebas Python, cero omitidas; 30 consultas del portal ejecutadas.',
        '- RDF: 322405 → 322495; delta exacto del integrador: +90/−0. SHACL conforme en portal y Studio, cero infracciones.',
        '- Una forma histórica carece de instancias: ResultadoMunicipalLote; se registra sin fingir una comprobación con instancias.',
        '- Studio: 323014 → 323104; sincronización única con respaldo y conservación de datos ajenos.',
        f"- [Respaldo de Studio](../{backup_rel}); archivo base de 130 entradas en el expediente.",
        f"- {len(historical)} archivos históricos/configuraciones contrastados por SHA; semántica e IRI intactas.",
        '- Recibos, dictámenes, huellas y detalle de las adendas en [ronda-10.json](ronda-10.json).','',
        '## Brechas externas conservadas','',
        '138 significados reales, 16 vigencias, 17 correspondencias candidatas, `des_mpo_res` y dos encabezados corruptos. V13/V14 mantienen el problema de acceso. Toneladas requiere acreditar la variante local; hm³ sigue sin un término exacto verificado. No se inventan definiciones, vigencias, equivalencias ni unidades. Gemma y la decisión de IRI quedaron fuera de alcance; no se contactó a publicadores.','']
    if sync.get('archivo_canonico_pendiente'):
        md += ['## Copia canónica de Studio','',
               'El grafo fue verificado; Windows impidió reemplazar la copia canónica. La copia viva recuperada y su SHA constan en el recibo de sincronización.','']
    dump(ROOT/'reports/ronda-10.json',report)
    (ROOT/'reports/ronda-10.md').write_text('\n'.join(md),encoding='utf-8')
    files=[ROOT/'reports/ronda-10.json',ROOT/'reports/ronda-10.md',ROOT/'README.md',ROOT/'PLAN.md',ROOT/'AGENTS.md',
           *[ROOT/'scripts'/s for s in ('integrar_ronda_10.py','ampliar_portal.py','consolidar_semantica.py','publicar_top50_r9.py')],
           ROOT/'tests/test_ronda_10.py',ROOT/'tests/test_publicar_top50_instalado.py']
    dump(M/'cierre-final.json',{'estado':report['estado'],'archivos_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in files}})
    print(json.dumps({'estado':report['estado'],'suite':233,'portal':322495,'studio':323104,
                      'historicos_intactos':len(historical)},ensure_ascii=False))

if __name__=='__main__':
    main()
