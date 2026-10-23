import json
d = json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))
recs = d.get('recursos', [])
print('total recursos inspeccionados:', len(recs))
targets = {'403912fd-5853-4e18-8256-f77206f855bd','e5aad52d-5760-481c-ba65-db0ba4a5315e',
 'e7a3d62f-4ace-479c-aa52-1c9e384dc429','85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f',
 'ee8f639f-5e89-46ae-93b9-934b05fc6233','5494daa1-09ca-4750-aeac-2558553700e1'}
for r in recs:
    cj = r.get('conjunto') or r.get('package_id') or r.get('dataset')
    if cj in targets:
        print('---')
        print(json.dumps(r, ensure_ascii=False)[:3000])
