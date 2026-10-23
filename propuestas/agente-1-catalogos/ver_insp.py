import json
d = json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))
recs = {r['id']: r for r in d.get('recursos', [])}
ids = ['6d561451-ff08-45d6-b1af-285ff5f417b1','ed82f8a6-6414-4ce4-94df-302408eb2f67',
 'aaf0c6c1-76a7-40ac-b542-1319d1bb2a5a','dc87a5be-8ef7-4e90-af72-ea5053423fad',
 '0e69d911-6ed3-4268-841b-0c4989e7cb45','508da131-e18f-45ac-9ec0-8aac03cea798',
 'af7a9aba-5a0e-4cf0-9b7d-5a3550e7907e','598dbd86-0a0b-42a4-ab3d-6cb656f9b605',
 'f5060479-ee16-49b5-99d4-09aabef8042e','ca5574f0-d59d-4fc1-a52f-5c533b2abf82',
 '08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8','33d0a99e-c721-496f-a05e-07646e9ae42a']
with open('propuestas/agente-1-catalogos/inspecciones_objetivo.txt', 'w', encoding='utf-8') as f:
    for i in ids:
        r = recs.get(i)
        if not r:
            f.write(f'{i}: NO ENCONTRADO en contenido-inspeccion\n')
            continue
        f.write(f"===== {i} | ok={r.get('ok')} | fuente={r.get('fuente')} | sha={r.get('sha256_fragmento_o_archivo')} | bytes={r.get('bytes_leidos')} | metodo={r.get('metodo')}\n")
        for t in r.get('tablas', [])[:12]:
            campos = [c.get('id') for c in t.get('campos', [])]
            f.write(f"  hoja={t.get('hoja')!r} fila_enc={t.get('fila_encabezado')} metodo={t.get('metodo_encabezado')} ncampos={len(campos)}\n")
            f.write(f"    campos: {campos[:40]}\n")
print('ok')
