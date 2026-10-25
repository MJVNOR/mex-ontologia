"""Cotejo de entregas y sus huellas, sin instalar ni resolver brechas por inferencia."""
from pathlib import Path
from collections import Counter
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect():
    issues=[];missing=[];selected=[];rows=[];refs={}
    def check(value,context):
        if isinstance(value,dict):
            if isinstance(value.get('ruta'),str) and value.get('sha256'):
                p=(ROOT/value['ruta']).resolve()
                if not p.is_relative_to(ROOT) or not p.is_file():
                    issues.append({'tipo':'ruta_ausente','ruta':value['ruta'],'contexto':context})
                else:
                    actual=refs.setdefault(p.relative_to(ROOT).as_posix(),sha(p))
                    if actual!=value['sha256']:
                        issues.append({'tipo':'sha_no_coincide','ruta':value['ruta'],'contexto':context,'declarado':value['sha256'],'actual':actual})
            for x in value.values(): check(x,context)
        elif isinstance(value,list):
            for x in value: check(x,context)
    for role in read(E/'roles.json'):
        if sha(ROOT/role['asignacion'])!=role['sha256']:
            issues.append({'tipo':'asignacion_alterada','rol':role['rol']})
        markers=sorted((E/role['rol']).glob('v[0-9][0-9][0-9]/congelada.json'))
        if not markers:
            missing.append(role['rol']);continue
        marker=markers[-1];folder=marker.parent
        p=folder/'entrega.json'
        if not p.exists():
            missing.append(role['rol']);continue
        assignment=read(ROOT/role['asignacion']);delivery=read(p)
        seal=read(marker)
        check(seal,role['rol']+'/congelada')
        for key,name in [('entrega_sha256','entrega.json'),('entrega_json_sha256','entrega.json'),('entrega_md_sha256','entrega.md')]:
            if seal.get(key) and sha(folder/name)!=seal[key]:
                issues.append({'tipo':'entrega_congelada_alterada','rol':role['rol'],'archivo':name})
        for rel,h in seal.get('fuentes',{}).items() if isinstance(seal.get('fuentes'),dict) else []:
            if isinstance(h,str): check({'ruta':rel,'sha256':h},role['rol']+'/fuentes_congeladas')
        check(delivery,role['rol']+'/entrega')
        expected={r.get('id',r.get('columna')) for r in assignment['casos']}
        decisions=delivery.get('decisiones',[])
        aliases={r['iri']:r['columna'] for r in assignment['casos'] if r.get('iri') and r.get('columna')}
        ids=[aliases.get(r.get('id',r.get('columna')),r.get('id',r.get('columna'))) for r in decisions]
        if set(ids)!=expected or len(ids)!=len(expected):
            issues.append({'tipo':'ids_incorrectos','rol':role['rol'],'esperados':len(expected),'obtenidos':len(ids)})
        for row in decisions:
            if row.get('estado') not in {'brecha_externa','acceso_no_resuelto','propuesta_para_auditar'}:
                issues.append({'tipo':'estado_incorrecto','rol':role['rol'],'id':row.get('id'),'estado':row.get('estado')})
            if row.get('estado')!='propuesta_para_auditar' and (not row.get('evidencia_faltante') or not row.get('condicion_reapertura')):
                issues.append({'tipo':'brecha_sin_condicion','rol':role['rol'],'id':row.get('id')})
            canonical=aliases.get(row.get('id',row.get('columna')),row.get('id',row.get('columna')))
            rows.append(dict(row,id_entrega=row.get('id'),id=canonical,rol=role['rol'],version=folder.name))
        selected.append({'rol':role['rol'],'version':folder.name,'entrega':p.relative_to(ROOT).as_posix(),'sha256_entrega':sha(p),'marcador':marker.relative_to(ROOT).as_posix(),'sha256_marcador':sha(marker)})
    return {'faltantes':missing,'discrepancias':issues,'seleccion':selected,'conteos':dict(Counter(r.get('estado') for r in rows)),'decisiones':rows,'fuentes_cotejadas':refs}
if __name__=='__main__':
    r=inspect()
    print(json.dumps({k:v for k,v in r.items() if k not in ('decisiones','fuentes_cotejadas')},ensure_ascii=False))
    if '--guardar' in sys.argv:
        out=E/'comprobacion-preintegracion.json'
        assert not out.exists()
        out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
