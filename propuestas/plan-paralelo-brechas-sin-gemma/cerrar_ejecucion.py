"""Cierra un lote auditado, conservando versiones y dependencias semánticas."""
from comprobar_ejecucion import ROOT,read,sha,inspect
from pathlib import Path
from datetime import datetime,timezone,timedelta
from collections import Counter
import sys,json

folder=(ROOT/sys.argv[1]).resolve()
selection=read(folder/'seleccion.json')
checked=inspect(folder,selection['versiones'])
if checked['faltantes'] or checked['discrepancias']:
    raise ValueError('No se puede cerrar: faltantes o discrepancias en versiones seleccionadas')
rows=checked['decisiones']
if len(rows)!=188 or len({r['id'] for r in rows})!=188:
    raise ValueError('Se requieren 188 casos primarios únicos')
audits=[]
for role in ('A-documental','B-tecnica'):
    ap=folder/role/'dictamen.json'
    audit=read(ap)
    if audit.get('dictamen')!='aceptar':
        raise ValueError('Auditoría no aceptada: '+role)
    if audit.get('seleccion_sha256')!=sha(folder/'seleccion.json'):
        raise ValueError('La auditoría no corresponde a la selección final: '+role)
    for ref in audit.get('referencias',[]):
        if not isinstance(ref.get('ruta'),str) or not (ROOT/ref['ruta']).is_file() or sha(ROOT/ref['ruta'])!=ref['sha256']:
            raise ValueError('Referencia de auditoría no coincide: '+str(ref.get('ruta')))
    audits.append({'rol':role,'ruta':ap.relative_to(ROOT).as_posix(),'sha256':sha(ap),'dictamen':audit})
proposals=[r for r in rows if r['estado']=='propuesta_para_auditar']
if proposals:
    raise ValueError('Hay propuestas que requieren resolución e integración antes del cierre documental')
web_markers=selection.get('paquetes_web',[{'ruta':(folder/'W-web/paquete/congelada.json').relative_to(ROOT).as_posix(),'sha256':sha(folder/'W-web/paquete/congelada.json')}])
for marker in web_markers:
    if sha(ROOT/marker['ruta'])!=marker['sha256']:
        raise ValueError('Marcador web modificado')
    web=read(ROOT/marker['ruta'])
    for ref in web['archivos']:
        if sha(ROOT/ref['ruta'])!=ref['sha256']:
            raise ValueError('Paquete web alterado: '+ref['ruta'])
deps=read(folder/'dependencias-correspondencias.json')
byid={r['id']:r for r in rows}
for row in deps:
    decision=byid[row['definicion_iri']]
    row['decision_significado']=decision['estado']
    row['condicion_promocion']=decision['condicion_reapertura']
    row['estado_semantico_final']='candidata_por_nombre'
now=datetime.now(timezone.utc)
bytype={kind:dict(Counter(r['estado'] for r in rows if r['tipo']==kind)) for kind in ('significados','vigencias','anomalias')}
byrole={role['rol']:{'casos':role['conteo'],'estados':dict(Counter(r['estado'] for r in rows if r['rol']==role['rol']))} for role in read(folder/'roles.json')}
report={'cerrado_en_utc':now.isoformat(),'cerrado_en_hermosillo':now.astimezone(timezone(timedelta(hours=-7))).isoformat(),'expediente':folder.relative_to(ROOT).as_posix(),'estado':'ejecucion_completa_sin_promociones_documentalmente_acreditadas','conteos':{'casos_primarios':188,'dependencias_correspondencias':20,'por_tipo':bytype,'puertas':checked['puertas'],'promociones_semanticas':0,'pares_estructurales_nuevos':0},'por_rol':byrole,'decisiones':rows,'dependencias_correspondencias':deps,'auditorias':audits,'seleccion':{'ruta':(folder/'seleccion.json').relative_to(ROOT).as_posix(),'sha256':sha(folder/'seleccion.json')},'web':web_markers,'fuentes_cotejadas':checked['fuentes_cotejadas'],'fuentes_base_preservadas':len(read(folder/'base.json')['fuentes_sha256']),'conteos_semanticos_preservados':read(folder/'base.json')['conteos_semanticos'],'chat_gemma':'excluido_sin_cambios','contactos_externos':0,'grafo_modificado':False,'limite':'Brecha externa significa documento o vínculo aún no localizado en lo examinado; no inexistencia universal ni posesión exclusiva del publicador.'}
lines=['# Ejecución del plan paralelo sin Gemma','','Plan ejecutado con diez frentes temáticos, un investigador web y dos auditorías independientes. Las entregas se conservaron por versión y se cotejaron contra las asignaciones y fuentes fijadas.','','## Resultado','','- 169 significados examinados; no hubo promociones acreditadas.','- 16 vigencias y tres registros de anomalía/encabezados conservan su evidencia faltante y condición de reapertura.','- Las 20 correspondencias semánticas siguen candidatas: dependen de las definiciones aún pendientes. Los 20 pares estructurales anteriores se conservan, sin contarlos como avances nuevos.','- Gemma quedó excluido; no hubo contactos externos ni cambios del grafo.','','## Puerta de investigación','',f'Clasificación de los 188 casos: {checked["puertas"]}. Estas cifras son por caso; una misma pista documental puede atender varios casos. Pista nueva no equivale a resolución.','','| Frente | Casos | Entrega final |','| --- | ---: | --- |']
for version in selection['versiones']:
    role=version['rol']
    md=(ROOT/version['entrega']).with_suffix('.md')
    lines.append(f'| {role} | {byrole[role]["casos"]} | [Versión {version["version"]}](../{md.relative_to(ROOT).as_posix()}) |')
lines += ['','## Dependencias para reabrir','','Cada decisión del JSON identifica el documento o dato formal que permitiría reabrir el caso. No se debe lanzar otra ronda de búsquedas genéricas sobre los mismos materiales sin una pista nueva o una revisión formal justificada. Una fuente inaccesible queda diferenciada de una fuente examinada sin contenido resolutivo.','','## Integridad','',f'Se preservaron {report["fuentes_base_preservadas"]} archivos base y se cotejaron {len(checked["fuentes_cotejadas"])} referencias locales de las entregas seleccionadas. Ambas auditorías corresponden al mismo SHA-256 de la selección final.','','Se mantienen 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y cero ambiguas. No se aplicó el staging R7 de CLASIF ni se modificaron manifiestos anteriores.','','[Detalle completo de casos, fuentes, versiones y auditorías](ejecucion-plan-sin-gemma.json).','']
(ROOT/'reports/ejecucion-plan-sin-gemma.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'reports/ejecucion-plan-sin-gemma.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'estado':report['estado'],'conteos':report['conteos'],'fuentes_cotejadas':len(checked['fuentes_cotejadas'])},ensure_ascii=True))
