import json, io
cob = json.load(open('data/semantica/cobertura.json', encoding='utf-8'))
def num(defiri):
    return defiri.rsplit('%2F', 1)[-1]
for d in ['33d0a99e-c721-496f-a05e-07646e9ae42a', 'ca5574f0-d59d-4fc1-a52f-5c533b2abf82',
          'ed82f8a6-6414-4ce4-94df-302408eb2f67', 'dc87a5be-8ef7-4e90-af72-ea5053423fad',
          '508da131-e18f-45ac-9ec0-8aac03cea798', '598dbd86-0a0b-42a4-ab3d-6cb656f9b605']:
    vs = [v for v in cob['variables'] if v.get('diccionario') == d]
    vs_sorted = sorted(vs, key=lambda v: int(num(v['definicion_iri'])) if num(v['definicion_iri']).isdigit() else 9999)
    with io.open(f'propuestas/agente-1-catalogos/vars_{d[:8]}.txt', 'w', encoding='utf-8') as f:
        f.write(f"diccionario {d} total={len(vs)}\n")
        for v in vs_sorted:
            f.write(f"{num(v['definicion_iri'])} | {v.get('variable')} | {(v.get('descripcion') or '')[:120]} | cat={v.get('catalogo_declarado')!r} | huella={v.get('huella_fila_diccionario')}\n")
print('ok')
