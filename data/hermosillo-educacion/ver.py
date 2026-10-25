import pathlib, openpyxl
base = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\data\hermosillo-educacion")
for fn in sorted(base.glob("*.xlsx")):
    print("="*80); print(fn.name)
    wb = openpyxl.load_workbook(fn, data_only=True, read_only=True)
    print(" hojas:", wb.sheetnames)
    for ws in wb.worksheets:
        print(f" -- hoja {ws.title} max_row={ws.max_row} max_col={ws.max_column}")
        rows = list(ws.iter_rows(values_only=True))
        # imprime primeras 8 filas
        for r in rows[:8]:
            print("   ", r)
        # si hay columna Hermosillo, cuenta
        if rows:
            hdr = [str(c).strip() if c is not None else "" for c in rows[0]]
            print("   header:", hdr)
            # busca indice hermosillo
            idx = [i for i,h in enumerate(hdr) if "hermos" in h.lower()]
            print("   idx_hermosillo:", idx)
            # totales: suma columna hermosillo excluyendo header
            for i in idx:
                vals = [r[i] for r in rows[1:] if r[i] is not None]
                nums = [v for v in vals if isinstance(v,(int,float))]
                print(f"   col {hdr[i]}: n_filas_con_dato={len(vals)} suma={sum(nums)} primeros={vals[:10]}")
        print()
