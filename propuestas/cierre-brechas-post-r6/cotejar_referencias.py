"""Lista discrepancias de referencias nuevas sin alterar expedientes."""
from consolidar import ROOT,HERE,read,sha
import json

issues=[]
checked={}
for folder in [HERE/r['tarea'] for r in read(HERE/'tareas.json')]:
    def visit(value,origin):
        if isinstance(value,dict):
            if isinstance(value.get('ruta'),str) and value.get('sha256'):
                locator=value['ruta'].removeprefix('local: ')
                path=ROOT/locator
                actual=checked.get(str(path))
                if path.is_file() and actual is None:
                    actual=sha(path)
                    checked[str(path)]=actual
                if actual != value['sha256']:
                    issues.append({'tarea':folder.name,'archivo':origin,'ruta':value['ruta'],'sha_declarado':value['sha256'],'sha_actual':actual})
            for key,item in value.items():
                if key != 'original':
                    visit(item,origin)
        elif isinstance(value,list):
            for item in value:
                visit(item,origin)
    for path in [folder/'entrega.json',*folder.glob('*list*.json')]:
        if path.is_file():
            try:
                visit(read(path),path.name)
            except Exception as exc:
                issues.append({'tarea':folder.name,'archivo':path.name,'error':str(exc)})
unique={json.dumps(item,sort_keys=True):item for item in issues}
(HERE/'discrepancias-referencias.json').write_text(json.dumps(list(unique.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(list(unique.values()),ensure_ascii=True))
