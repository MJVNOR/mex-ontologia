import json
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
for defiri in ['https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F15',
'https://example.org/mex-ontologi/definition/063058e6-aed3-4a60-b944-5e653c77b14d%2F17',
'https://example.org/mex-ontologi/definition/1a95d734-2f0e-4781-8831-77dcfcbe70f8%2F7',
'https://example.org/mex-ontologi/definition/7922b8c8-db09-4172-ad7f-31b0ba0c68e3%2F7',
'https://example.org/mex-ontologi/definition/bdbf043f-5d12-4362-bce0-bd4c8ab1e2a1%2F2']:
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    row = insp[dic]['definiciones'][idx-1]
    print('==', dic, idx)
    for k, v in row.items():
        print(f'  {k}: {str(v)[:160]!r}')
    print()
