"""Paso 5 lote-2: conceptos existentes, fila P7 y texto completo P22."""
import io
import json

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


sem = load('propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json')
con = sem['conceptos']
print('n conceptos:', len(con))
keys = sorted(con.keys())
with io.open(ROOT + 'propuestas/pendientes-muse-r4/lote-2/_conceptos.txt', 'w', encoding='utf-8') as f:
    for k in keys:
        v = con[k]
        f.write('%s || %s\n' % (k, json.dumps(v, ensure_ascii=False)[:220]))
print('volcado conceptos ok')
# fila P7 del diccionario mejora (respaldada r3a9-085) para comparar tipo con P40
insp = load('data/portal/inspecciones/af14d207-7697-4d52-b99b-46a35a1b76ac.json')
rows = insp.get('definiciones', [])
for i, r in enumerate(rows, 1):
    name = r.get('Nombre variable')
    if name in ('P7', 'P6', 'P9', 'P36', 'P39', 'P40', 'P22'):
        print(i, json.dumps(r, ensure_ascii=False)[:600])
