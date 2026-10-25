import pathlib, collections
import openpyxl
base = pathlib.Path(r"C:\Users\marti\Documents\MEX-Ontologi\data\hermosillo-educacion-uth")
def rows(fn, sheet=0):
    wb = openpyxl.load_workbook(base/fn, data_only=True, read_only=True)
    ws = wb.worksheets[sheet] if isinstance(sheet,int) else wb[sheet]
    rr = list(ws.iter_rows(values_only=True))
    hdr = [str(c).strip() if c is not None else "" for c in rr[0]]
    return hdr, [r for r in rr[1:] if any(v is not None and str(v).strip()!="" for v in r)]

# matricula detalle
hdr, d = rows("matricula-sep-dic-2025.xlsx")
iS, iN, iP, iE = hdr.index("Sexo"), hdr.index("Nivel"), hdr.index("Programa educativo"), hdr.index("Edad")
print("MATRICULA", len(d), "registros")
print(" sexo:", dict(collections.Counter(r[iS] for r in d)))
print(" nivel:", dict(collections.Counter(r[iN] for r in d)))
print(" edad media:", round(sum(r[iE] for r in d if isinstance(r[iE],(int,float)))/len(d),2), "min", min(r[iE] for r in d if isinstance(r[iE],(int,float))), "max", max(r[iE] for r in d if isinstance(r[iE],(int,float))))
top = collections.Counter(str(r[iP]).strip() for r in d).most_common(8)
print(" top programas:", top)
# nuevo ingreso / reingreso / titulados / egresados totales y %M
for fn, hm, mm in [("nuevo-ingreso-sep-dic-2025.xlsx","Hombres Nuevo Ingreso","Mujeres Nuevo Ingreso"),
 ("reingreso-sep-dic-2025.xlsx","Hombres - Reingreso","Mujeres - Reingreso"),
 ("titulados-2025.xlsx","Hombres Titulados","Mujeres Tituladas"),
 ("egresados-2025-uth.xlsx","Hombres Egresados","Mujeres Egresadas")]:
    h, dd = rows(fn)
    ih, im = h.index(hm), h.index(mm)
    th = sum(r[ih] or 0 for r in dd); tm = sum(r[im] or 0 for r in dd)
    print(fn, f"H={th} M={tm} T={th+tm} %M={tm/(th+tm)*100:.1f}% filas={len(dd)}")
# promedios
h, dd = rows("promedio-sep-dic-2025.xlsx")
iw = h.index("PROMEDIO DE APROVECHAMIENTO MUJER"); imn = h.index("PROMEDIO DE APROVECHAMIENTO HOMBRE")
valsM = [r[iw] for r in dd if isinstance(r[iw],(int,float))]; valsH = [r[imn] for r in dd if isinstance(r[imn],(int,float))]
print(f"PROMEDIO nM={len(valsM)} mediaM={sum(valsM)/len(valsM):.2f} nH={len(valsH)} mediaH={sum(valsH)/len(valsH):.2f}")
# discapacidad
h, dd = rows("discapacidad-may-ago-2025.xlsx")
print("DISCAPACIDAD header:", h)
tot = [0]*6
for r in dd:
    for k in range(6):
        v = r[k+2]
        if isinstance(v,(int,float)): tot[k]+=v
print(" totales etniaH,etniaM,lengH,lengM,discH,discM:", tot, "programas con algun caso:", sum(1 for r in dd if any(isinstance(r[k+2],(int,float)) and r[k+2]>0 for k in range(6))))
