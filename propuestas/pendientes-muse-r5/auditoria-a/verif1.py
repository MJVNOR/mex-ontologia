import json
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def show(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    row = insp[dic]['definiciones'][idx - 1]
    print('==', dic, idx)
    for k, v in row.items():
        print('  ', k, '=', repr(str(v)[:160]))
# defunciones: surtido (17,38,53,63,70=ENTIDADOCURRENCIA?,76)
for i in [17, 38, 53, 63, 70, 76, 79]:
    show(f'https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F{i}')
    print()
# epidemiologia: 9,11,13,24,36
for i in [9, 11, 13, 24, 36]:
    show(f'https://example.org/mex-ontologi/definition/2334deaa-dd0c-444e-b038-4cc556ad715d%2F{i}')
    print()
