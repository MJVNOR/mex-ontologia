import json
m = json.load(open('data/catalogo/metadatos.json', encoding='utf-8'))
print(type(m))
if isinstance(m, dict):
    print(list(m.keys())[:20])
    for k in list(m.keys())[:5]:
        v = m[k]
        print(k, type(v))
        if isinstance(v, dict):
            print('  subkeys:', list(v.keys())[:20])
        elif isinstance(v, list) and v:
            print('  first:', str(v[0])[:500])
elif isinstance(m, list):
    print(len(m))
    print(json.dumps(m[0], ensure_ascii=False)[:2000])
