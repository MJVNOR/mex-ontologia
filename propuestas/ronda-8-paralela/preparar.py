"""Fija el punto de partida R7 y reparte exclusivamente los pendientes solicitados."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
assert not E.exists() or not any(E.iterdir())
E.mkdir(parents=True,exist_ok=True)
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r7=read(ROOT/'reports/ronda-7.json')
cov=read(ROOT/'data/semantica/cobertura.json')
rules=read(ROOT/'ontologia/semantica.json')
variables={v['iri']:v for v in cov['variables'] if v.get('iri')}
newcols=set(r7['candidatas_nuevas'])
maps=[dict(m,definicion=variables[m['variable']]) for m in cov['correspondencias'] if m['estado']=='candidata_por_nombre']
new=sorted([m for m in maps if m['columna'] in newcols],key=lambda x:x['columna'])
old=sorted([m for m in maps if m['columna'] not in newcols],key=lambda x:x['columna'])
assert len(new)==28 and len(old)==17
cases=[r for r in r7['decisiones'] if r['estado_final']!='integrado_r7']
assert len(cases)==157
roles=[]
def role(name,scope,items):
    folder=E/name
    folder.mkdir()
    assignment={'rol':name,'alcance':scope,'casos':items,'base':'reports/ronda-7.json','salida':'entrega.json/md + congelada.json; versiones nuevas para correcciones; no editar tras congelar','modelo':'opencode-go/muse-spark-1.3-contributor'}
    p=folder/'asignacion.json'
    write(p,assignment)
    roles.append({'rol':name,'casos':len(items),'alcance':scope,'asignacion':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
role('M1-sinac','Primeras 14 correspondencias nuevas SINAC; verificar evidencia física y significado R7 exactos.',new[:14])
role('M2-sinac','Últimas 14 correspondencias nuevas SINAC; verificar evidencia física y significado R7 exactos.',new[14:])
role('M3-anteriores','17 candidatas previas; identidad física ya revisada, dependencia semántica pendiente; no promover sin significado.',old)
for name in ('S1-defunciones','S2-nacimientos','S3-matriculas','S4-epidemiologia','S5-tic','S6-diversos'):
    role(name,'Revisión por caso de significado pendiente; nuevas pistas primarias o cierre motivado sin repetir búsquedas agotadas.',[r for r in cases if r['tipo']=='significados' and r['rol']==name])
for name in ('V1-uth-presas','V2-salud-anomalias','V3-coespo','V4-seguridad'):
    role(name,'Vigencias: distinguir publicación, periodo de datos, edición y aplicabilidad; sólo casos de vigencia.',[r for r in cases if r['tipo']=='vigencias' and r['rol']==name])
role('X-anomalias','Aclarar des_mpo_res y dos encabezados corruptos; conservar original, no inventar catálogo ni significados.',[r for r in cases if r['tipo']=='anomalias'])
role('T-pruebas','Suite Python R7: corregir fallos preservando invariantes históricos, ampliar cobertura específica R7 y proponer adaptación futura R8.',[])
role('W-web','Único navegador Obscura compartido. Atender peticiones por archivo; fuentes primarias y evidencia real, sin repetir consultas agotadas.',[])
write(E/'roles.json',roles)
pins={}
for rel in ('ontologia/semantica.json','data/semantica/cobertura.json','data/portal/portal-completo.ttl','data/catalogo/studio-live.ttl','reports/ronda-7.json','reports/ronda-7.md','reports/studio-portal-sync.json'):
    pins[rel]=sha(ROOT/rel)
for p in (ROOT/'ontologia').glob('revision*.json'):
    pins[p.relative_to(ROOT).as_posix()]=sha(p)
for p in (ROOT/'data').glob('integracion*/manifiesto.json'):
    pins[p.relative_to(ROOT).as_posix()]=sha(p)
for p in (ROOT/'scripts').glob('integrar*.py'):
    pins[p.relative_to(ROOT).as_posix()]=sha(p)
write(E/'base.json',{'fecha_utc':datetime.now(timezone.utc).isoformat(),'resumen':cov['resumen'],'sha256':pins,'gemma':'excluido','contactos_externos':0})
write(E/'base-semantica.json',rules)
write(E/'cobertura-r7.json',cov)
write(E/'pendientes-iniciales.json',cases)
plan=['# Plan y ejecución paralela R8 — sin Gemma','','Inicio: '+datetime.now(timezone.utc).isoformat(),'','## Reparto','','| Agente | Casos | Trabajo |','| --- | ---: | --- |']
plan += [f"| {r['rol']} | {r['casos']} | {r['alcance']} |" for r in roles]
plan += ['','## Secuencia','','1. Revisar en paralelo las 45 correspondencias, 138 significados, 16 vigencias y tres registros de anomalía; ejecutar suite R7.','2. Congelar cada entrega y sus fuentes. Investigación web centralizada por MCP Obscura, sólo pistas nuevas o cambios comprobables.','3. Auditar propuestas con dos revisores independientes; auditar código y pruebas.','4. Respaldar y crear nueva evidencia/manifiesto R8. Integrar sólo decisiones acreditadas, preservando rondas anteriores.','5. Regenerar, ejecutar suite completa, validar RDF/SHACL y sincronizar Studio con respaldo.','6. Cerrar con resultados y condiciones concretas para reabrir brechas externas.','','Modelo de agentes: `opencode-go/muse-spark-1.3-contributor`, MCP nativo OpenCode. Sin Gemma, mensajes externos, definiciones o vigencias inventadas.','']
(ROOT/'docs/plan-paralelo-ronda-8-sin-gemma.md').write_text('\n'.join(plan),encoding='utf-8')
print(json.dumps({'expediente':E.relative_to(ROOT).as_posix(),'roles':roles},ensure_ascii=False))
