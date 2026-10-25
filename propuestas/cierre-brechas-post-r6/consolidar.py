"""Consolida revisión por caso y comprueba la integridad de la evidencia local."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:
        raise ValueError(message)

def main():
    base=read(HERE/'base.json')['fuentes_sha256']
    for path,fingerprint in base.items():
        require(sha(ROOT/path)==fingerprint,'Fuente base alterada: '+path)
    tasks=read(HERE/'tareas.json')
    coverage=read(ROOT/'data/semantica/cobertura.json')
    gap_rows=read(ROOT/'propuestas/depuracion-post-r6/catalogos/brechas.json')['brechas']
    excluded=read(ROOT/'propuestas/depuracion-post-r6/encabezados/exclusiones.json')['exclusiones']
    canonical={
        'correspondencias':{r['columna']:r for r in coverage['correspondencias'] if r['estado']=='candidata_por_nombre'},
        'vigencias':{r['id']:r for r in gap_rows if r['id']!='des_mpo_res'},
        'anomalias':{**{r['definicion_iri']:dict(r,id=r['definicion_iri']) for r in excluded},**{r['id']:r for r in gap_rows if r['id']=='des_mpo_res'}},
        'significados':{r['definicion_iri']:r for r in read(ROOT/'reports/investigacion-post-r6.json')['decisiones']},
    }
    checked={}
    def references(value):
        if isinstance(value,dict):
            if isinstance(value.get('ruta'),str) and value.get('sha256'):
                locator=value['ruta']
                # Algunas referencias heredadas anotan el soporte como «local: ruta».
                # Se conserva el original y se cotejan los bytes de su ruta efectiva.
                if locator.startswith('local: '):
                    locator=locator[len('local: '):]
                path=(ROOT/locator).resolve()
                require(path.is_relative_to(ROOT),'Referencia fuera del proyecto: '+str(path))
                require(path.is_file(),'Evidencia ausente: '+str(path))
                require(sha(path)==value['sha256'],'Hash obsoleto: '+str(path))
                checked[path.relative_to(ROOT).as_posix()]=value['sha256']
            for key,entry in value.items():
                # El expediente heredado contiene localizadores descriptivos además
                # de rutas. Su copia íntegra se coteja contra la asignación fijada.
                if key != 'original':
                    references(entry)
        elif isinstance(value,list):
            for entry in value:
                references(entry)
    decisions=[]
    deliveries=[]
    for task in tasks:
        folder=HERE/task['tarea']
        assignment=read(folder/'asignacion.json')
        doc=read(folder/'entrega.json')
        marker_path=next((folder/name for name in ('cierrelisto.json','cierre-listos.json','cierre-listo.json','listo.json') if (folder/name).is_file()),folder/'listo.json')
        marker=read(marker_path)
        originals={r[assignment['clave_id']]:r for r in assignment['casos']}
        rows=doc['decisiones']
        ids=[r['id'] for r in rows]
        require(len(ids)==len(set(ids))==assignment['conteo'] and set(ids)==set(originals),'IDs incompletos o duplicados: '+task['tarea'])
        for row in rows:
            require(row['original']==originals[row['id']],'Original alterado: '+row['id'])
            require(row['original']==canonical[task['tipo']][row['id']],'Asignación difiere de la fuente fijada: '+row['id'])
            require(row['estado'] in {'sigue_pendiente','propuesta_resolucion','par_estructural_revisado_significado_pendiente'},'Estado inesperado: '+row['id'])
            require(row.get('motivo') and row.get('evidencia'),'Falta motivación/evidencia: '+row['id'])
            if row['estado']=='sigue_pendiente':
                require(row.get('evidencia_faltante'),'Falta brecha: '+row['id'])
            if row['estado']=='par_estructural_revisado_significado_pendiente':
                require(task['tipo']=='correspondencias','Estado estructural fuera de correspondencias')
                require(not row.get('propuesta',{}).get('concepto'),'No aprobar concepto por evidencia estructural')
                require(row['propuesta']['estado_propuesto']==row['estado'],'Estado propuesto estructural incoherente')
            elif row['estado']=='propuesta_resolucion':
                require(row.get('propuesta'),'Propuesta vacía: '+row['id'])
            decisions.append(dict(row,tarea=task['tarea'],tipo=task['tipo']))
        references(doc)
        references(marker)
        md=folder/'entrega.md' if (folder/'entrega.md').is_file() else folder/'resultado.md'
        require(md.is_file(),'Falta informe legible: '+task['tarea'])
        deliveries.append({'tarea':task['tarea'],'tipo':task['tipo'],'casos':len(rows),'estados':dict(Counter(r['estado'] for r in rows)),'ruta':(folder/'entrega.json').relative_to(ROOT).as_posix(),'sha256':sha(folder/'entrega.json'),'informe':md.relative_to(ROOT).as_posix()})
    bytype={kind:dict(Counter(r['estado'] for r in decisions if r['tipo']==kind)) for kind in ('significados','correspondencias','vigencias','anomalias')}
    require(len(decisions)==208,'Se requieren 169+20+16+3 casos')
    audits=[]
    for name in ('auditoria-correspondencias','auditoria-vigencias','auditoria-significados-anomalias'):
        path=HERE/name/'dictamen.json'
        doc=read(path)
        references(doc)
        require(doc.get('dictamen')=='aceptar','Auditoría sin cierre: '+name)
        audits.append({'ruta':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'dictamen':doc})
    web=read(HERE/'web-obscura/disponibilidad.json')
    structural=[r for r in decisions if r['estado']=='par_estructural_revisado_significado_pendiente']
    approved={r['id'] for r in audits[0]['dictamen'].get('resoluciones_estructurales_aprobadas',[])}
    require({r['id'] for r in structural}==approved,'Falta aprobación estructural explícita por ID')
    variables={r['iri']:r for r in coverage['variables'] if r.get('iri')}
    ledger={'estado':'registro_documental_estructural','alcance':'Asocia columna y fila de diccionario sin aprobar significado, concepto, códigos, vigencias ni cruces. No modifica vinculos_documentales_revisados ni es consumido por la generación semántica.','auditoria':{'ruta':audits[0]['ruta'],'sha256':audits[0]['sha256']},'pares':[{'columna':r['id'],'variable_documentada':r['original']['variable'],'definicion_iri':variables[r['original']['variable']]['definicion_iri'],'recurso':r['original']['recurso'],'estado':r['estado'],'estado_semantico_actual':'candidata_por_nombre','significado':'pendiente','evidencia_faltante_semantica':canonical['significados'][variables[r['original']['variable']]['definicion_iri']]['evidencia_faltante'],'evidencia':r['evidencia'],'limites':r['limites']} for r in structural]}
    ledger_path=ROOT/'data/revision-estructural-post-r6/revisiones.json'
    ledger_path.parent.mkdir(parents=True,exist_ok=True)
    ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'generado_en_utc':datetime.now(timezone.utc).isoformat(),'alcance':'Revisión de todas las brechas excepto chat Gemma. Las clasificaciones históricas confirmadas no cuentan como nuevas resoluciones.','resumen_por_tipo':bytype,'pares_estructurales_documentados':len(structural),'registro_estructural':{'ruta':ledger_path.relative_to(ROOT).as_posix(),'sha256':sha(ledger_path)},'decisiones':decisions,'entregas':deliveries,'auditorias':audits,'obscura':web,'fuentes_cotejadas':checked,'fuentes_base_preservadas':base,'contactos_externos':0,'promociones_semanticas_integradas':0,'grafo_modificado':False,'chat_gemma':'excluido por el usuario'}
    lines=['# Revisión de brechas posterior a R6','','Se revisaron en paralelo 169 significados, 20 correspondencias candidatas, 16 vigencias y la anomalía `des_mpo_res` con los dos encabezados corruptos. Gemma quedó excluido. No se cuentan las clasificaciones históricas de encabezados como resoluciones nuevas.','','| Área | Pendientes | Pares estructurales documentados | Propuestas semánticas |','| --- | ---: | ---: | ---: |']
    lines += [f'| {kind} | {states.get("sigue_pendiente",0)+states.get("par_estructural_revisado_significado_pendiente",0)} | {states.get("par_estructural_revisado_significado_pendiente",0)} | {states.get("propuesta_resolucion",0)} |' for kind,states in bytype.items()]
    lines += ['',f'**Avance estructural: {len(structural)} pares columna–fila de diccionario documentados**, en [el registro separado](../data/revision-estructural-post-r6/revisiones.json). Su significado sigue pendiente. El estado semántico mantiene 4475 correspondencias revisadas y 20 candidatas: `documental_revisada` exige además una definición respaldada. No se relajó esa validación ni se añadieron conceptos o cruces.','','Los 169 significados, las 16 vigencias y la anomalía con los dos encabezados siguen sin la evidencia necesaria para su resolución. Cada caso detalla el documento o vínculo que falta.']
    lines += ['','## Expedientes por agente','']
    lines += [f'- [{r["tarea"]}](../{r["informe"]}): {r["casos"]} casos.' for r in deliveries]
    lines += ['','## Integridad y alcance','',f'Se cotejaron {len(checked)} referencias locales por SHA-256 y {len(base)} archivos base. Los casos conservan sus originales y evidencia faltante. Una búsqueda negativa o un fallo HTTP no acredita inexistencia; una coincidencia nominal no acredita identidad ni una vigencia histórica.','', '[Uso de Obscura en OpenCode](../docs/investigacion-opencode-obscura.md). La disponibilidad comprobada y el método realmente usado están registrados en el JSON del informe.','', '[Detalle de decisiones, fuentes y auditorías](cierre-brechas-post-r6.json).','']
    (ROOT/'reports/cierre-brechas-post-r6.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'reports/cierre-brechas-post-r6.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'resumen':bytype,'fuentes':len(checked),'base_intacta':len(base)},ensure_ascii=True))

if __name__=='__main__':
    main()
