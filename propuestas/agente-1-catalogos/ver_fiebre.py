"""Lista variables del diccionario Fiebre manchada alrededor de 129/162/168/177/178 y vuelca conjuntos implicados."""
import json
cob = json.load(open('data/semantica/cobertura.json', encoding='utf-8'))
d = '33d0a99e-c721-496f-a05e-07646e9ae42a'
vs = [v for v in cob['variables'] if v.get('diccionario') == d]
print('total vars en diccionario fiebre:', len(vs))
def num(defiri):
    return defiri.rsplit('%2F', 1)[-1]
vs_sorted = sorted(vs, key=lambda v: int(num(v['definicion_iri'])) if num(v['definicion_iri']).isdigit() else 9999)
for v in vs_sorted:
    n = num(v['definicion_iri'])
    if n in ('129', '162', '168', '177', '178'):
        tag = ' <- ref'
    else:
        tag = ''
    print(n, '|', v.get('variable'), '|', (v.get('descripcion') or '')[:80], '| cat_decl:', repr(v.get('catalogo_declarado')), '| estado:', v.get('estado'), tag)
