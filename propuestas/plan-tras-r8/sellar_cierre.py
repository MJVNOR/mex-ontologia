"""Conserva recibos finales; los informes históricos no se reescriben."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=read(ROOT/'reports/ronda-9.json');assert report['estado']=='cerrado_integrado_validado_y_sincronizado'
dest=E/'cierre.json';assert not dest.exists()
rec=E/'recibos';rec.mkdir()
for src in ('portal-carga.json','studio-portal-sync.json'):shutil.copyfile(ROOT/'reports'/src,rec/src)
tracking=read(E/'seguimiento.json')
tracking.update(estado=report['estado'],release='R9',pruebas=204,
    portal_triples=322405,studio_triples=323014,
    nucleo={'significados':1423,'conceptos':1106,'revisadas':4506,'candidatas':17,'ambiguas':0},
    observaciones=['Plan recibido tras R8 ejecutado; material K v001 aprobado por A+B e instalado.',
                   'Primer integrador I descartado; correcciones de propuestas preservadas.',
                   'P1: dos declaraciones de unidad; P4: exclusión SHACL; P2/P3: negativos sin instancias.',
                   'Núcleo R8 y manifiestos R1–R8 conservados; 138 significados y 16 vigencias siguen pendientes.',
                   '204 pruebas antes y después de generar; Studio verificado, 62 inserciones y cero retiros.',
                   'Chat revisor informado de R9 y revisando el plan final por solicitud del usuario.'])
(E/'seguimiento.json').write_text(json.dumps(tracking,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
paths=[ROOT/'reports/ronda-9.json',ROOT/'reports/ronda-9.md',ROOT/'ontologia/revision-ronda-9.json',
       ROOT/'data/integracion-ronda-9/manifiesto.json',ROOT/'ontologia/semantica.json',
       E/'aplicacion.json',E/'seleccion-final.json',E/'documentacion-actualizada.json',
       E/'validacion/suite-r9.log',E/'validacion/suite-r9-postgeneracion.log',
       E/'validacion/consultas-r9.json',E/'recibos/portal-carga.json',E/'recibos/studio-portal-sync.json']
paths += [ROOT/p for p in read(E/'documentacion-actualizada.json')]
result={'format_version':1,'release':'R9','estado':report['estado'],
        'fecha_utc':datetime.now(timezone.utc).isoformat(),
        'archivos':{p.relative_to(ROOT).as_posix():sha(p) for p in paths},
        'gemma':'excluido','contactos_externos':0}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cierre':str(dest),'sha256':sha(dest),'archivos':len(result['archivos'])}))
