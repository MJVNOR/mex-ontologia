"""Inspeccion completa de los 6 catalogos descargados + columna 'Catalogo de referencia' de diccionarios."""
import json, glob, shutil, os
import openpyxl

def dump_xlsx(path, max_rows=500):
    tmp = path + '.xlsx'
    if not os.path.exists(tmp):
        shutil.copyfile(path, tmp)
    wb = openpyxl.load_workbook(tmp, data_only=True, read_only=True)
    out = {'archivo': path, 'hojas': []}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        # quita filas totalmente vacias al final
        while rows and all(v is None or str(v).strip() == '' for v in rows[-1]):
            rows.pop()
        hdr = [str(c).strip() if c is not None else '' for c in (rows[0] if rows else [])]
        body = rows[1:]
        out['hojas'].append({'hoja': ws.title, 'nfilas_total': len(rows),
                             'nfilas_datos': len(body), 'encabezado': hdr,
                             'filas': [[('' if v is None else str(v)) for v in r] for r in body[:max_rows]]})
    return out

res = {}
for p in sorted(glob.glob('propuestas/agente-1-catalogos/fuentes/*_Catalogo.bin')):
    res[p] = dump_xlsx(p)
with open('propuestas/agente-1-catalogos/catalogos_contenido.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
for p, d in res.items():
    print('=====', p.split('/')[-1][:60])
    for h in d['hojas']:
        print(f"  hoja={h['hoja']!r} filas_datos={h['nfilas_datos']} encabezado={h['encabezado']}")
        for r in h['filas'][:12]:
            print('   ', r)
