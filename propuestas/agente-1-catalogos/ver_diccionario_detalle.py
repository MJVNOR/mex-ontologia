"""Vuelca filas relevantes de diccionarios (columna Catalogo de referencia y detalle) + busca des_mpo en catalogo fiebre."""
import json, glob, shutil, os
import openpyxl

def load(path):
    tmp = path + '.xlsx'
    if not os.path.exists(tmp):
        shutil.copyfile(path, tmp)
    return openpyxl.load_workbook(tmp, data_only=True, read_only=True)

# 1) diccionarios educativos: fila Campo de Formación
for p in sorted(glob.glob('propuestas/agente-1-catalogos/fuentes/*_Diccionario.bin')):
    if '5494daa1' in p or 'ee8f639f' in p:
        continue
    wb = load(p)
    print('=====', p.split('/')[-1][:70])
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        hdr = [str(c) if c is not None else '' for c in rows[0]]
        print(' hoja:', ws.title, '| hdr:', hdr)
        try:
            icat = next(i for i, h in enumerate(hdr) if 'talogo' in h)
        except StopIteration:
            icat = None
        for r in rows[1:]:
            vals = [('' if v is None else str(v)) for v in r]
            if any('Formaci' in v or 'formaci' in v for v in vals):
                print('  fila:', vals[:9] if len(vals) > 9 else vals)
                if icat is not None:
                    print('   -> col catalogo ref:', vals[icat] if icat < len(vals) else '')
                print('   -> ncols:', len(vals))

# 2) catalogo fiebre: buscar des_mpo / ide_ en todo el libro
p = 'propuestas/agente-1-catalogos/fuentes/5494daa1-09ca-4750-aeac-2558553700e1_08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8_Catalogo.bin'
wb = load(p)
print('===== busqueda des_mpo/ide en catalogo fiebre')
for ws in wb.worksheets:
    for row in ws.iter_rows(values_only=True):
        vals = [('' if v is None else str(v)) for v in row]
        if any('des_mpo' in v or 'ide_id' in v or 'ide_col' in v for v in vals):
            print(' hoja', ws.title, ':', vals)
print('fin busqueda (si no hay lineas, no existe)')

# 3) diccionario fiebre CSV: filas 7,129,162,168,177,178 crudas
import csv
pcsv = 'propuestas/agente-1-catalogos/fuentes/5494daa1-09ca-4750-aeac-2558553700e1_33d0a99e-c721-496f-a05e-07646e9ae42a_Diccionario.bin'
with open(pcsv, 'r', encoding='utf-8-sig', newline='') as f:
    rd = csv.reader(f)
    hdr = next(rd)
    print('dicc fiebre hdr:', hdr)
    rows = list(rd)
    print('nfilas dicc fiebre:', len(rows))
    # localiza columnas
    try:
        iv = hdr.index('Nombre variable')
    except ValueError:
        iv = 0
    wanted = {'des_mpo_res', 'servic_atencion', 'motiv_rech_ricket_sangre', 'ricket_especie_rtpcr', 'ide_id'}
    for r in rows:
        if r[iv] in wanted:
            print(' ', r)
