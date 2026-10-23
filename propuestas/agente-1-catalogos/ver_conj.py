import json
m = json.load(open('data/catalogo/metadatos.json', encoding='utf-8'))
targets = {'403912fd-5853-4e18-8256-f77206f855bd','e5aad52d-5760-481c-ba65-db0ba4a5315e',
 'e7a3d62f-4ace-479c-aa52-1c9e384dc429','85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f',
 'ee8f639f-5e89-46ae-93b9-934b05fc6233','5494daa1-09ca-4750-aeac-2558553700e1'}
out = []
for ds in m:
    if ds.get('id') in targets:
        out.append(ds)
with open('propuestas/agente-1-catalogos/conjuntos_objetivo.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
for ds in out:
    print('======', ds['id'], '|', ds.get('title'))
    print('  org:', (ds.get('organization') or {}).get('title'))
    for r in ds.get('resources', []):
        print('  -', r.get('id'), '|', r.get('name'), '|', r.get('format'), '|', (r.get('url') or '')[:130], '| datastore:', r.get('datastore_active'))
