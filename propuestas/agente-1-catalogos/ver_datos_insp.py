import json
d = json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))
recs = {r['id']: r for r in d.get('recursos', [])}
ids = ['05bf66fb-6539-43ef-ae23-9369b678abac',  # matriculas dato
 'd62602e7-a059-4c34-a300-057ec4eb98f0',  # promedio dato
 '79362ac6-c6ad-4231-aa41-f23ab92d1ae1',  # titulados dato
 '7422760b-8f99-4774-a436-c7d1f49c2cc0',  # egresados dato
 'ffe3c845-1fc7-4a6c-ab21-3a1db1740fdd',  # hidrico 1980-89
 '4121cf57-1e4a-4fb0-b175-3805edffca2c',  # fiebre 2022
 'f2333c5e-26ea-47c8-93ee-fda5e9106672']
with open('propuestas/agente-1-catalogos/inspecciones_datos.txt', 'w', encoding='utf-8') as f:
    for i in ids:
        r = recs.get(i)
        if not r:
            f.write(f'{i}: NO ENCONTRADO\n'); continue
        f.write(f"===== {i} | fuente={r.get('fuente')} | sha={r.get('sha256_fragmento_o_archivo')}\n")
        for t in r.get('tablas', [])[:6]:
            campos = [c.get('id') for c in t.get('campos', [])]
            f.write(f"  hoja={t.get('hoja')!r} fila_enc={t.get('fila_encabezado')} ncampos={len(campos)}\n")
            f.write(f"    campos: {campos[:50]}\n")
print('ok')
