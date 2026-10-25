"""Completa el recibo tras error Windows 1224 al guardar el archivo abierto."""
from pathlib import Path
import sys,json,hashlib
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(R/'scripts'))
from sincronizar_studio_portal import api,normalizar_cadenas,cambios
from rdflib import Graph
from rdflib.compare import isomorphic
def main():
 folder=R/'data/portal'
 backup=R/'data/backups/studio-antes-portal-20261023T175938824705Z.ttl'
 desired=normalizar_cadenas(Graph().parse(folder/'ampliacion.ttl',format='turtle'))
 before=normalizar_cadenas(Graph().parse(backup,format='turtle'))
 previous=normalizar_cadenas(Graph().parse(folder/'studio-managed.ttl',format='turtle'))
 remove,add,owned=cambios(before,desired,previous)
 expected=(before-remove)+add
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 fresh=R/'data/backups'/('studio-r4-sincronizado-'+stamp+'.ttl')
 api('/save',{'path':str(fresh),'format':'turtle'})
 actual=normalizar_cadenas(Graph().parse(fresh,format='turtle'))
 if not isomorphic(actual,expected):raise ValueError('Grafo vivo distinto al estado previsto: no actualizar propiedad ni repetir cambios')
 # La sincronización original pasó SHACL y verificó igualdad antes de fallar
 # únicamente al guardar el archivo canónico abierto. No repetir DELETE/LOAD.
 owned.serialize(folder/'studio-managed.ttl',format='turtle',encoding='utf-8')
 report={'respaldo':str(backup.relative_to(R)),'triples_insertados':len(add),'triples_retirados_gestionados':len(remove),'triples_totales_studio':len(actual),'triples_gestionados':len(owned),'verificado':True,'estado':'grafo y propiedad sincronizados; copia canónica requiere cerrar archivo mapeado','copia_viva_recuperacion':str(fresh.relative_to(R)),'copia_sha256':hashlib.sha256(fresh.read_bytes()).hexdigest(),'error_original':'Windows 1224 en /save data/catalogo/studio-live.ttl; la escritura del grafo y comprobación ya habían terminado','fecha_utc':datetime.now(timezone.utc).isoformat()}
 (R/'reports/studio-portal-sync.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
