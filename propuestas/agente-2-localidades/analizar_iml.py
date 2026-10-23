"""Analiza IML_2020 como referencia *derivada* de localidades (no catalogo oficial).
Solo lee archivos en propuestas/agente-2-localidades/fuentes/ y escribe en esa misma carpeta.
Preserva codigos originales; cualquier normalizacion se registra por separado.
"""
import json, hashlib, os
from collections import Counter, defaultdict
from openpyxl import load_workbook

BASE = os.path.join("propuestas", "agente-2-localidades")
F = os.path.join(BASE, "fuentes")
IML = os.path.join(F, "IML_2020_datos.xlsx")
CAT = os.path.join(F, "catalogo_mun_ent_solo.xlsx")
DIC = os.path.join(F, "diccionario_localidad.xlsx")

def sha(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def sheet_headers_vals(path, sheet):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=False))
    hdr = [(c.value, c.column_letter, c.row) for c in rows[0]]
    wb.close()
    return hdr, len(rows) - 1

def analyze_iml():
    wb = load_workbook(IML, read_only=True, data_only=True)
    ws = wb["IML_2020"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(v).strip() if v is not None else "" for v in rows[0]]
    idx = {h: i for i, h in enumerate(hdr)}
    need = ["CVE_LOC", "ENT", "NOM_ENT", "MUN", "NOM_MUN", "LOC", "NOM_LOC"]
    assert all(c in idx for c in need), f"faltan columnas: {hdr[:10]}"
    data = rows[1:]
    # originales como texto crudo (str de lo que openpyxl devuelve; numericos llegan como int/float)
    recs = []
    for r in data:
        recs.append({c: r[idx[c]] for c in need})
    # composicion con padding explicito SEPARADO (propuesta, no dato original)
    def pad(v, n):
        if v is None or (isinstance(v, str) and v.strip() == ""):
            return None
        s = str(v).strip()
        # si viene como '260010001.0' por float, recortar
        if s.endswith(".0"):
            s = s[:-2]
        try:
            # solo digitos? si no, devolver None para no inventar
            if "." in s:
                s = str(int(float(s)))
            else:
                s = str(int(s))
        except ValueError:
            return None
        return s.zfill(n)
    comp_ok = comp_fail = 0
    fails = []
    seen_cve = {}
    dup_cve_diff = []
    name_to_cves = defaultdict(set)
    cve_to_names = defaultdict(set)
    ents, muns = Counter(), Counter()
    loc_vals_raw = Counter()
    for rec in recs:
        ent_p, mun_p, loc_p = pad(rec["ENT"], 2), pad(rec["MUN"], 3), pad(rec["LOC"], 4)
        cve_p = pad(rec["CVE_LOC"], 9)
        raw_cve = rec["CVE_LOC"]
        ents[str(rec["ENT"])] += 1
        muns[f"{rec['ENT']}|{rec['MUN']}"] += 1
        loc_vals_raw[str(rec["LOC"])] += 1
        comp = (ent_p or "") + (mun_p or "") + (loc_p or "")
        if cve_p is not None and comp == cve_p:
            comp_ok += 1
        else:
            comp_fail += 1
            if len(fails) < 20:
                fails.append({"CVE_LOC": raw_cve, "ENT": rec["ENT"], "MUN": rec["MUN"],
                              "LOC": rec["LOC"], "comp_padding": comp or None, "cve_padding": cve_p})
        key = cve_p if cve_p is not None else f"RAW:{raw_cve!r}"
        nm = (str(rec["NOM_MUN"] or "").strip(), str(rec["NOM_LOC"] or "").strip())
        if key in seen_cve and seen_cve[key] != nm:
            dup_cve_diff.append({"cve_padding": key, "nombres": sorted({str(seen_cve[key]), str(nm)})})
        seen_cve.setdefault(key, nm)
        name_to_cves[f"{nm[0]}||{nm[1]}"].add(key)
        cve_to_names[key].add(f"{nm[0]}||{nm[1]}")
    # nombres identicos con >1 CVE (homonimia, NO identidad)
    homonimos = {k: sorted(v) for k, v in name_to_cves.items() if len(v) > 1}
    multi_nombre = {k: sorted(v) for k, v in cve_to_names.items() if len(v) > 1}
    # categorias especiales: buscar LOC 9999/9998/0000, CVE terminaciones sospechosas
    especiales = [r for r in recs if str(r["LOC"]).strip().lstrip("0") in ("9999", "9998", "999", "99", "9", "") or str(r["CVE_LOC"])[-4:] in ("9999", "9998")]
    resumen = {
        "archivo": os.path.basename(IML),
        "sha256": sha(IML),
        "hoja": "IML_2020",
        "fila_encabezado": 1,
        "columnas": hdr,
        "filas_datos": len(recs),
        "ents_distintos_raw": sorted(ents),
        "n_municipios_distintos_par_ent_mun": len(muns),
        "cve_loc_unicos_padding9": len(seen_cve),
        "composicion_padding_ENT2_MUN3_LOC4_vs_CVELOC9": {"ok": comp_ok, "falla": comp_fail},
        "ejemplos_falla": fails,
        "cve_con_mas_de_un_par_nombres": multi_nombre,
        "pares_mun_loc_homonimos_solo_conteo": len(homonimos),
        "ejemplos_homonimos_max5": dict(list(homonimos.items())[:5]),
        "candidatos_categoria_especial": len(especiales),
        "ejemplos_especiales_max10": [{"CVE_LOC": r["CVE_LOC"], "ENT": r["ENT"], "MUN": r["MUN"], "LOC": r["LOC"], "NOM_MUN": r["NOM_MUN"], "NOM_LOC": r["NOM_LOC"]} for r in especiales[:10]],
        "nota_ceros": "Los valores numericos de Excel pierden ceros a la izquierda al leerse como numero; el padding 2/3/4/9 es TRANSFORMACION propuesta y separada, no dato original.",
    }
    wb.close()
    return resumen

def describe_workbook(path):
    wb = load_workbook(path, read_only=True, data_only=True)
    out = {"archivo": os.path.basename(path), "sha256": sha(path), "hojas": wb.sheetnames, "detalle": {}}
    for s in wb.sheetnames:
        ws = wb[s]
        rows = list(ws.iter_rows(values_only=True))
        out["detalle"][s] = {"filas_totales": len(rows), "encabezado": [str(v) for v in rows[0]] if rows else []}
    wb.close()
    return out

if __name__ == "__main__":
    cat = describe_workbook(CAT)
    dic = describe_workbook(DIC)
    iml = analyze_iml()
    with open(os.path.join(BASE, "iml2020-verificacion.json"), "w", encoding="utf-8") as f:
        json.dump({"catalogo_publicado_0c1554d8": cat, "diccionario_251309e5": dic, "derivada_IML_2020": iml}, f, indent=2, ensure_ascii=False)
    print(json.dumps({"catalogo_hojas": cat["hojas"], "dic_hojas": dic["hojas"],
                      "iml_filas": iml["filas_datos"], "iml_comp_ok": iml["composicion_padding_ENT2_MUN3_LOC4_vs_CVELOC9"],
                      "iml_cve_unicos": iml["cve_loc_unicos_padding9"], "iml_ents": iml["ents_distintos_raw"]}, indent=2, ensure_ascii=False))
