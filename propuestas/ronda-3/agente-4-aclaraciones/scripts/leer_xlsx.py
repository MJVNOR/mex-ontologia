"""Lee filas de un xlsx con stdlib (sharedStrings + sheet1)."""
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def filas(path, hoja=1):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall(f"{NS}si"):
            ss.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
    sheets = ET.fromstring(z.read("xl/workbook.xml"))
    ids = [s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
           for s in sheets.find(f"{NS}sheets")]
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = None
    for r in rels:
        if r.get("Id") == ids[hoja - 1]:
            target = r.get("Target")
    data = z.read("xl/" + target)
    root = ET.fromstring(data)
    out = []
    for row in root.iter(f"{NS}row"):
        vals = []
        for c in row.findall(f"{NS}c"):
            t = c.get("t")
            v = c.find(f"{NS}v")
            is_ = c.find(f"{NS}is")
            if t == "s" and v is not None:
                vals.append(ss[int(v.text)])
            elif v is not None:
                vals.append(v.text)
            elif is_ is not None:
                vals.append("".join(x.text or "" for x in is_.iter(f"{NS}t")))
            else:
                vals.append("")
        out.append(vals)
    return out


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        print("=" * 20, arg)
        for i, f in enumerate(filas(arg), 1):
            if any("CVE_MUN" in c or "26048" in c or c.strip() == "nnn" for c in f):
                print(i, f)
