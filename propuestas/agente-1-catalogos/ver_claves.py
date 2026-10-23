import json
d = json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))
recs = d.get('recursos', [])
r = recs[0]
with open('propuestas/agente-1-catalogos/claves_contenido.txt', 'w', encoding='utf-8') as f:
    f.write('keys: ' + ', '.join(sorted(r.keys())) + '\n')
    f.write(json.dumps(r, ensure_ascii=False, indent=2)[:6000])
print('ok', len(recs))
