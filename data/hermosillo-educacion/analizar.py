import pathlib, openpyxl
base = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\data\hermosillo-educacion")
def load(fn):
    wb = openpyxl.load_workbook(base/fn, data_only=True, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c).strip() if c is not None else "" for c in rows[0]]
    data = [r for r in rows[1:] if any(v is not None for v in r)]
    return hdr, data
# 2020-2021 detalle Hermosillo
hdr, data = load("total-egresados-2020-2021.xlsx")
ih = hdr.index("Hermosillo")
detalle = sorted([(r[0], r[ih] or 0) for r in data], key=lambda x: x[1], reverse=True)
print("2020-2021 Hermosillo total:", sum(v for _,v in detalle), "programas con dato:", len([v for _,v in detalle if v]))
for prog, v in detalle[:10]: print(f"  {v:3d} {prog}")
print("  ... ceros/vacíos:", [p for p,v in detalle if not v][:5])
print()
for fn in ["egresados-2022.xlsx","egresados-2023.xlsx","egresados-2024.xlsx","egresados-2025.xlsx"]:
    hdr, data = load(fn)
    ih = hdr.index("Hombres Egresados"); im = hdr.index("Mujeres Egresadas"); ip = hdr.index("Programa Educativo")
    th = sum((r[ih] or 0) for r in data); tm = sum((r[im] or 0) for r in data)
    tot = th+tm
    print(f"{fn}: filas={len(data)} H={th} M={tm} Total={tot} %M={tm/tot*100:.1f}%")
    top = sorted(data, key=lambda r: ((r[ih] or 0)+(r[im] or 0)), reverse=True)[:5]
    for r in top:
        print(f"   {(r[ih] or 0)+(r[im] or 0):3d} (H{r[ih]} M{r[im]}) {r[ip]}")
    print()
