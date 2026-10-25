"""Coteja las entregas congeladas y sus fuentes; no integra cambios semánticos."""
from pathlib import Path
import sys,json,hashlib
from collections import Counter
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def original_sha(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

def inspect(folder,versions=None):
    issues=[]
    missing=[]
    checked={}
    selected=[]
    decisions=[]
    base=read(folder/'base.json')
    for path,fingerprint in base['fuentes_sha256'].items():
        if sha(ROOT/path)!=fingerprint:
            issues.append({'tipo':'fuente_base_alterada','ruta':path})
    def refs(value,context):
        if isinstance(value,dict):
            if isinstance(value.get('ruta'),str) and value.get('sha256'):
                path=(ROOT/value['ruta']).resolve()
                if not path.is_relative_to(ROOT) or not path.is_file():
                    issues.append({'tipo':'ruta_ausente','contexto':context,'ruta':value['ruta']})
                else:
                    actual=checked.setdefault(path.relative_to(ROOT).as_posix(),sha(path))
                    if actual!=value['sha256']:
                        issues.append({'tipo':'sha_no_coincide','contexto':context,'ruta':value['ruta'],'declarado':value['sha256'],'actual':actual})
            for child in value.values():
                refs(child,context)
        elif isinstance(value,list):
            for child in value:
                refs(child,context)
    for role in read(folder/'roles.json'):
        name=role['rol']
        ap=ROOT/role['asignacion']
        if sha(ap)!=role['sha256']:
            issues.append({'tipo':'asignacion_alterada','rol':name})
        assignment=read(ap)
        frozen=sorted((folder/name).glob('v[0-9][0-9][0-9]/congelada.json'))
        if versions:
            version=next((r for r in versions if r['rol']==name),None)
            marker=ROOT/version['marcador'] if version else None
        else:
            marker=frozen[-1] if frozen else None
        if not marker or not marker.is_file():
            missing.append(name)
            continue
        vfolder=marker.parent
        try:
            doc=read(vfolder/'entrega.json')
            seal=read(marker)
            if not (vfolder/'entrega.md').is_file():
                issues.append({'tipo':'informe_ausente','rol':name})
            refs(doc,name+'/'+vfolder.name)
            refs(seal,name+'/'+vfolder.name+'/congelada')
            pinned={r['ruta'] for r in seal.get('archivos',[]) if isinstance(r,dict) and r.get('ruta')}
            for required in ('entrega.json','entrega.md'):
                if (vfolder/required).relative_to(ROOT).as_posix() not in pinned:
                    issues.append({'tipo':'entrega_no_fijada','rol':name,'archivo':required})
            indexed={r['id']:r for r in assignment['casos']}
            ids=[r['id'] for r in doc['decisiones']]
            if len(ids)!=len(set(ids)) or set(ids)!=set(indexed):
                issues.append({'tipo':'ids_incompletos','rol':name,'esperados':len(indexed),'recibidos':len(ids)})
            for row in doc['decisiones']:
                source=indexed.get(row['id'])
                if source is None:
                    continue
                if row.get('original_sha256')!=original_sha(source['original']):
                    issues.append({'tipo':'original_sha_incorrecto','rol':name,'id':row['id']})
                if row.get('tipo')!=source['tipo']:
                    issues.append({'tipo':'tipo_incorrecto','rol':name,'id':row['id']})
                if row.get('puerta') not in {'pista_nueva','cambio_de_fuente_por_comprobar','sin_pista_nueva'}:
                    issues.append({'tipo':'puerta_incorrecta','rol':name,'id':row['id']})
                state=row.get('estado')
                if state not in {'propuesta_para_auditar','brecha_externa','acceso_no_resuelto'}:
                    issues.append({'tipo':'estado_incorrecto','rol':name,'id':row['id']})
                if not row.get('motivo') or not row.get('evidencia'):
                    issues.append({'tipo':'motivo_o_evidencia_ausente','rol':name,'id':row['id']})
                if state=='propuesta_para_auditar':
                    if not row.get('afirmacion_propuesta'):
                        issues.append({'tipo':'propuesta_vacia','rol':name,'id':row['id']})
                elif not row.get('evidencia_faltante') or not row.get('condicion_reapertura'):
                    issues.append({'tipo':'brecha_sin_condicion','rol':name,'id':row['id']})
                decisions.append(dict(row,rol=name,version=vfolder.name))
            entry={'rol':name,'version':vfolder.name,'marcador':marker.relative_to(ROOT).as_posix(),'sha256_marcador':sha(marker),'entrega':(vfolder/'entrega.json').relative_to(ROOT).as_posix(),'sha256_entrega':sha(vfolder/'entrega.json')}
            if versions:
                for field in ('sha256_marcador','sha256_entrega'):
                    if entry[field]!=version[field]:
                        issues.append({'tipo':'version_congelada_modificada','rol':name,'campo':field})
            selected.append(entry)
        except Exception as exc:
            issues.append({'tipo':'error_lectura','rol':name,'detalle':str(exc)})
    return {'fecha_utc':datetime.now(timezone.utc).isoformat(),'carpeta':folder.relative_to(ROOT).as_posix(),'faltantes':missing,'discrepancias':issues,'seleccion':selected,'conteo_decisiones':len(decisions),'estados':dict(Counter(r['estado'] for r in decisions)),'puertas':dict(Counter(r['puerta'] for r in decisions)),'fuentes_cotejadas':checked,'decisiones':decisions}

if __name__=='__main__':
    folder=(ROOT/sys.argv[1]).resolve()
    selection_path=folder/sys.argv[2] if len(sys.argv)>2 else folder/'seleccion.json'
    versions=read(selection_path)['versiones'] if selection_path.is_file() else None
    result=inspect(folder,versions)
    (folder/'comprobacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('decisiones','fuentes_cotejadas','seleccion')},ensure_ascii=True))
