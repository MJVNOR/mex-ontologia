"""Extrae valores literales (con acentos) de diccionarios y catalogos descargados."""
import json, csv, shutil, os
import openpyxl

def load_xlsx(path):
    tmp = path + '.tmp.xlsx'
    if not os.path.exists(tmp):
        shutil.copyfile(path, tmp)
    return openpyxl.load_workbook(tmp, data_only=True, read_only=True)

out = {'diccionarios': {}, 'catalogos': {}}
B = 'propuestas/agente-1-catalogos/fuentes'

# Diccionarios educativos: fila del Campo de Formación
for cj, dic in [('403912fd-5853-4e18-8256-f77206f855bd', 'ed82f8a6-6414-4ce4-94df-302408eb2f67'),
                ('e5aad52d-5760-481c-ba65-db0ba4a5315e', 'dc87a5be-8ef7-4e90-af72-ea5053423fad'),
                ('e7a3d62f-4ace-479c-aa52-1c9e384dc429', '508da131-e18f-45ac-9ec0-8aac03cea798'),
                ('85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f', '598dbd86-0a0b-42a4-ab3d-6cb656f9b605')]:
    p = f'{B}/{cj}_{dic}_Diccionario.bin'
    wb = load_xlsx(p)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr = [c if c is not None else '' for c in rows[0]]
    icat = next(i for i, h in enumerate(hdr) if 'logo' in str(h))
    for r in rows[1:]:
        vals = [c if c is not None else '' for c in r]
        if 'acad' in str(vals[0]).lower() if vals else False:
            out['diccionarios'][cj] = {'hoja': ws.title, 'encabezado': [str(x) for x in hdr],
                'fila': [str(x) for x in vals], 'indice_catalogo_ref': icat}
            break

# Diccionario hidrico (CSV latin-1/cp1252)
p = f'{B}/ee8f639f-5e89-46ae-93b9-934b05fc6233_ca5574f0-d59d-4fc1-a52f-5c533b2abf82_Diccionario.bin'
with open(p, 'r', encoding='cp1252', newline='') as f:
    rd = list(csv.reader(f))
out['diccionarios']['ee8f639f-5e89-46ae-93b9-934b05fc6233'] = {
    'encabezado': rd[0], 'fila_clave': rd[1]}

# Diccionario fiebre (CSV utf-8)
p = f'{B}/5494daa1-09ca-4750-aeac-2558553700e1_33d0a99e-c721-496f-a05e-07646e9ae42a_Diccionario.bin'
with open(p, 'r', encoding='utf-8-sig', newline='') as f:
    rd = list(csv.reader(f))
hdr, rows = rd[0], rd[1:]
d = {}
for r in rows[:176]:
    if r[0] in ('servic_atencion', 'motiv_rech_ricket_sangre', 'ricket_especie_rtpcr', 'des_mpo_res'):
        if r[0] == 'des_mpo_res' and r[6]:
            continue  # fila 7 no declara catalogo; el ref viene de 177/178
        d[r[0]] = r[:10]
d['linea177'] = rows[176][:10]
d['linea178'] = rows[177][:10]
out['diccionarios']['5494daa1-09ca-4750-aeac-2558553700e1'] = {'encabezado': hdr[:10], 'filas': d}

# Hojas exactas de catalogos (releer del contenido ya volcado para confirmar)
cat = json.load(open('propuestas/agente-1-catalogos/catalogos_contenido.json', encoding='utf-8'))
for k, v in cat.items():
    out['catalogos'][k.split('/')[-1][:17]] = [
        {'hoja': h['hoja'], 'encabezado': h['encabezado'],
         'nfilas_datos': h['nfilas_datos']} for h in v['hojas']]

with open('propuestas/agente-1-catalogos/exactos.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('exactos escritos')
