import csv, shutil, openpyxl
from collections import Counter
# hidrico diccionario fila Clave
p = 'propuestas/agente-1-catalogos/fuentes/ee8f639f-5e89-46ae-93b9-934b05fc6233_ca5574f0-d59d-4fc1-a52f-5c533b2abf82_Diccionario.bin'
for enc in ('utf-8-sig', 'latin-1'):
    try:
        with open(p, 'r', encoding=enc, newline='') as f:
            rd = list(csv.reader(f))
        print('leido con', enc)
        break
    except Exception as e:
        print(enc, 'fallo', e)
hdr = rd[0]
print('hidrico dicc hdr:', hdr)
for r in rd[1:]:
    if r[0] == 'Clave':
        print('fila Clave:', r[:10])
# fiebre muestra: columnas motiv/especie/des_mpo
src = 'propuestas/agente-1-catalogos/fuentes/muestra_5494daa1-09ca-4750-aeac-2558553700e1_4121cf57-1e4a-4fb0-b175-3805edffca2c.bin'
shutil.copyfile(src, src + '.xlsx')
wb = openpyxl.load_workbook(src + '.xlsx', data_only=True, read_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
hdr = [str(c) for c in rows[0]]
for col in ['motiv_rech_ricket_sangre', 'ricket_especie_rtpcr', 'des_mpo_res', 'servic_atencion']:
    i = hdr.index(col)
    vals = [str(r[i]) if r[i] is not None else '' for r in rows[1:51]]
    print(col, 'n=50:', dict(Counter(vals)))
# catalogo especie/motivos completos ya volcados; verifica unicidad y cobertura catalogos
import json
cat = json.load(open('propuestas/agente-1-catalogos/catalogos_contenido.json', encoding='utf-8'))
for k, v in cat.items():
    if '5494daa1' in k:
        for h in v['hojas']:
            codigos = [r[0] for r in h['filas']]
            print(h['hoja'], 'codigos:', codigos, 'unicos:', len(set(codigos)) == len(codigos))
    if 'f5060479' in k:
        for h in v['hojas']:
            if 'logo' in h['hoja']:
                codigos = [r[0] for r in h['filas']]
                print(h['hoja'], 'n=', len(codigos), 'unicos:', len(set(codigos)) == len(codigos), 'codigos:', codigos)
print('ok')
