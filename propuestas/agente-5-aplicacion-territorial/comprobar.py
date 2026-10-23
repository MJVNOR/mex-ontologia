"""Comprobacion de codigos territoriales en archivos de datos (agente 5).

Solo lee las columnas necesarias (claves, anio/periodo y nombres para coherencia).
Conserva el codigo original y registra `strip` como transformacion.
No aplica relleno ni prefijos: las ocho referencias usan sus propias claves.
No modifica el grafo central; solo escribe controles y conjuntos de claves.
"""
import csv
import datetime
import hashlib
import io
import json
import pathlib
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
DESC = BASE / "descargas"
CLAV = BASE / "claves"
RAIZ = BASE.parent.parent  # MEX-Ontologi

# Ocho variables documentadas (ontologia/territorio.json). No reidentificar.
VARIABLES = [
    {"id": "V1", "diccionario": "03a33e71-d447-47b1-aa0d-b341996e023c", "variable": "CLAVE",
     "conjunto": "0b5f5e16-2de3-4be1-811f-4b0976ed82d3", "titulo": "Proyecciones de poblacion - Grupos quinquenales de edad",
     "recurso_cat": "de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0", "hoja": "Catalogo_Municipios", "nivel": "municipio",
     "huella": "546de2ebb84dc9256ab486b8cbaeb6ebd3c64c6eb96f5c34078c8357beb555fe"},
    {"id": "V2", "diccionario": "03a33e71-d447-47b1-aa0d-b341996e023c", "variable": "CLAVE_ENT",
     "conjunto": "0b5f5e16-2de3-4be1-811f-4b0976ed82d3", "titulo": "Proyecciones de poblacion - Grupos quinquenales de edad",
     "recurso_cat": "de5c06c7-03d7-4ed4-a9fc-ec7d10b024f0", "hoja": "Catalogo_Estado", "nivel": "entidad",
     "huella": "e4f533916502747d0ffe968a435a120e96d2657aeb21460e22561ee75011d9cf"},
    {"id": "V3", "diccionario": "1b6d0817-66a9-4b25-9468-efca73e3ce20", "variable": "CLAVE",
     "conjunto": "943d0723-afbb-470a-8fe8-d62e8671de84", "titulo": "Proyecciones de poblacion - Grandes grupos de edad",
     "recurso_cat": "d7c4b8b2-568f-4349-a1ed-23fa93189e83", "hoja": "Catalogo_Municipios", "nivel": "municipio",
     "huella": "b732229b908b232ed20c979bd606cfc9bc353021e2ee2d6c4278dbe5ca318b31"},
    {"id": "V4", "diccionario": "1b6d0817-66a9-4b25-9468-efca73e3ce20", "variable": "CLAVE_ENT",
     "conjunto": "943d0723-afbb-470a-8fe8-d62e8671de84", "titulo": "Proyecciones de poblacion - Grandes grupos de edad",
     "recurso_cat": "d7c4b8b2-568f-4349-a1ed-23fa93189e83", "hoja": "Catalogo_Estado", "nivel": "entidad",
     "huella": "e4f533916502747d0ffe968a435a120e96d2657aeb21460e22561ee75011d9cf"},
    {"id": "V5", "diccionario": "5f46e4b8-858d-47dc-a180-125f3cc8727a", "variable": "Cve. Municipio",
     "conjunto": "93ca5e1c-702e-4e62-bc61-638907be184a", "titulo": "Incidencia delictiva municipal",
     "recurso_cat": "36d3ac85-4327-41f5-9259-538a7723a0ae", "hoja": "cat_municipio", "nivel": "municipio",
     "huella": "31c1c6ee9eb1b45f7c46967c1b3d67a486203e40a3b9cee6702465ffa162d448"},
    {"id": "V6", "diccionario": "a8a09044-87db-49a2-82c3-29594ec6ffd5", "variable": "Clave_Ent",
     "conjunto": "caf587a5-23ac-496b-85d4-6ceb1d615d78", "titulo": "Victimas del fuero comun en el estado",
     "recurso_cat": "7f3aca28-4251-48b8-a759-69c992580744", "hoja": "cat_entidad", "nivel": "entidad",
     "huella": "398129adb15dd0d1545e51593fb4fe34d126ea01cc8236896570d967fc094cdc"},
    {"id": "V7", "diccionario": "f1bbd13b-3364-441c-81b4-7b7c548be39f", "variable": "CLAVE",
     "conjunto": "960ef0a9-73ed-4191-ae0b-b868d7e48292", "titulo": "Proyecciones de poblacion - Indicadores demograficos",
     "recurso_cat": "e0d2acc2-9841-4f6d-baea-88ba86710a7d", "hoja": "Catalogo_Municipios", "nivel": "municipio",
     "huella": "b0771af1f718ab544b37a6c285c8aecb115758bdbb5d5cacc36bb84ea6c4e5e5"},
    {"id": "V8", "diccionario": "f1bbd13b-3364-441c-81b4-7b7c548be39f", "variable": "CLAVE_ENT",
     "conjunto": "960ef0a9-73ed-4191-ae0b-b868d7e48292", "titulo": "Proyecciones de poblacion - Indicadores demograficos",
     "recurso_cat": "e0d2acc2-9841-4f6d-baea-88ba86710a7d", "hoja": "Catalogo_Estado", "nivel": "entidad",
     "huella": "e4f533916502747d0ffe968a435a120e96d2657aeb21460e22561ee75011d9cf"},
]

# Recursos de datos a comprobar: (conjunto_id, recurso_id, periodo, formato, columnas fisicas esperadas)
DATOS = [
    ("0b5f5e16-2de3-4be1-811f-4b0976ed82d3", "81513319-6073-4239-84ab-4cfcc660819a", "1990-2040 (columna A\u00d1O)", "XLSX", ["CLAVE", "CLAVE_ENT"]),
    ("943d0723-afbb-470a-8fe8-d62e8671de84", "775d76b5-eabc-4342-9beb-741ec68c42ed", "1990-2040 (columna A\u00d1O)", "XLSX", ["CLAVE", "CLAVE_ENT"]),
    ("960ef0a9-73ed-4191-ae0b-b868d7e48292", "7e590f35-f293-40e3-b3e1-4002f8c3fbfe", "1990-2040 (columna A\u00d1O)", "XLSX", ["CLAVE", "CLAVE_ENT"]),
]
_I = ["2513ec12-4b23-4700-8eeb-9cfb634d5553", "147ead58-f894-4b0d-9881-ab06368e4cc9",
      "4e13a33e-4738-41ac-a0a4-3ac0afab9091", "d18cac7c-60dd-45ce-8cba-d90dc9fb5a18",
      "0794d04e-7779-4fb6-b2ad-94a927e49a64", "70c0bfb7-5378-42db-a20c-95da9ce1a4e4",
      "22d74901-c3ab-4d80-9f4f-b9e7da051ba8", "fc4a46ba-5318-4cc9-aadc-aa578300af15",
      "18b58aaf-e382-478e-86d9-8f50a7b08e12", "fb66e0fa-21e5-4c11-9d9d-7b4f701ee044",
      "befd1c5e-1222-4795-a866-d46cf602637b"]
for i, r in enumerate(_I):
    DATOS.append(("93ca5e1c-702e-4e62-bc61-638907be184a", r, str(2015 + i), "CSV", ["Cve. Municipio"]))
_V = ["4c1f984e-a6be-412b-b274-5af2d4ff55b1", "15650860-3a0b-461f-becb-658422e3a597",
      "c7ab7527-c2f5-44f2-a33e-6a368574f992", "1d7c90a8-d10b-4dbc-a16d-61e57164d80a",
      "e26eafbe-5d74-4882-af64-89e5bddbb46e", "652ca41a-5c9e-4d00-aa9a-f4d006b613fe",
      "1ec37796-0ad6-44b9-ba36-30bd4ae3d526", "8c2618f2-b317-41b0-b0d3-8020e735ffd7",
      "10d7cb8c-4058-4b9c-85f5-c25819d0f66b", "8f959438-7c12-419a-be1b-e0e4a52b0a26",
      "39ff0330-1959-4b92-914e-a48c691aff01"]
for i, r in enumerate(_V):
    col = "Cve. Municipio" if i == 0 else "Clave_Ent"  # 2015 trae columna municipal; resto entidad
    DATOS.append(("caf587a5-23ac-496b-85d4-6ceb1d615d78", r, str(2015 + i), "CSV", [col]))

ESPECIALES_MUN = {"26998", "26999"}  # pertenecen al catalogo y son categorias no municipales


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cargar_catalogos():
    d = json.loads((RAIZ / "data" / "territorio" / "catalogos.json").read_text(encoding="utf-8"))
    out = {}
    for ref in d["referencias"]:
        out[(ref["recurso"], ref["hoja"])] = {
            "codigos": [e["codigo"] for e in ref["entradas"]],
            "sha256": ref["archivo_sha256"],
            "filas": ref["filas_retenidas"],
        }
    return out


def cargar_urls():
    d = json.loads((RAIZ / "data" / "portal" / "inventario.json").read_text(encoding="utf-8"))
    return {r["id"]: r["url"] for r in d["recursos"] if r.get("url")}


def descargar(rid, url):
    dest = DESC / f"{rid}{'.csv' if '/download/' in url and url.rstrip().lower().endswith('.csv') else '.xlsx' if 'resource' in url and '.csv' not in url.lower() else ''}"
    # extension por formato conocido
    if dest.suffix == "":
        dest = DESC / (rid + (".csv" if rid in _I + _V else ".xlsx"))
    if not dest.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "MEX-Ontologi agente-5"})
        with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
            f.write(r.read())
    return dest


def texto_original(v):
    """Conserva el codigo original como texto. Registra conversion numerico->texto."""
    if v is None:
        return None, None
    if isinstance(v, float):
        if v.is_integer():
            return str(int(v)), "numerico_a_texto"
        return repr(v), "numerico_a_texto"
    if isinstance(v, int):
        return str(v), "numerico_a_texto"
    s = str(v)
    if s != s.strip():
        return s, "strip"
    return s, "ninguna"


def norm(s):
    return s.strip() if isinstance(s, str) else s


def composicion_exacta(clave, ent):
    """CLAVE (nnnnn) = CLAVE_ENT (nn) + municipio (3 digitos). Igualdad exacta, sin relleno.

    Documentado por los diccionarios: CLAVE formato nnnnn, CLAVE_ENT formato nn.
    Exige digitos ASCII 0-9 en ambas: rechaza '26ABC' y digitos Unicode
    ('isdigit' acepta p. ej. superindices y digitos de otras escrituras).
    `startswith` aceptaria CLAVE_ENT='2' para CLAVE='26001'; esta comprobacion lo rechaza.
    """
    import re
    c, e = norm(clave), norm(ent)
    if not re.fullmatch(r"[0-9]{5}", c) or not re.fullmatch(r"[0-9]{2}", e):
        return False
    return c[:2] == e


def selftest():
    assert composicion_exacta("26001", "26")
    assert not composicion_exacta("26001", "2")  # ponytail: startswith lo aceptaria
    assert not composicion_exacta("26001", "27")
    assert not composicion_exacta("26001", "260")
    assert not composicion_exacta("2601", "26")
    assert not composicion_exacta("26ABC", "26")  # letras en clave municipal
    assert not composicion_exacta("26A01", "26")
    assert not composicion_exacta("26001", "2A")  # letras en clave de entidad
    assert not composicion_exacta("\u0662\u0666\u0660\u0660\u0661", "26")  # digitos arabigos Unicode
    assert not composicion_exacta("26001", "\u00b2\u2076")  # superindices: isdigit() los acepta
    assert not composicion_exacta("\uff12\uff16\uff10\uff10\uff11", "\uff12\uff16")  # ancho completo
    assert composicion_exacta(" 26001 ", " 26 ")  # strip registrado como transformacion


def _letra(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def variantes(anio):
    return {"A\u00d1O", "A\u00f1o", "A\u00d1o", "A\ufffdO", "A\u00c3\u00d1O"}


def _colnum(ref):
    n = 0
    for ch in ref:
        if ch.isalpha():
            n = n * 26 + (ord(ch.upper()) - 64)
        else:
            break
    return n - 1


def leer_xlsx(path, columnas):
    """Lee la primera hoja por XML (tolerante a <dimension> roto y a drawings ausentes)."""
    import re
    import zipfile
    import xml.etree.ElementTree as ET
    NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    z = zipfile.ZipFile(path)
    ss = []
    try:
        sxml = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in sxml.findall(f"{NS}si"):
            ss.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
    except KeyError:
        pass
    wbxml = ET.fromstring(z.read("xl/workbook.xml"))
    hojas = [s.get("name") for s in wbxml.iter(f"{NS}sheet")]
    sname = next((h for h in hojas if h), hojas[0] if hojas else "Sheet 1")
    # localizar el xml de la primera hoja visible
    hoja_xml = None
    for n in z.namelist():
        if n.startswith("xl/worksheets/sheet") and n.endswith(".xml") and "_rels" not in n:
            hoja_xml = n
            break
    wxml = ET.fromstring(z.read(hoja_xml))
    filas = []
    for row in wxml.iter(f"{NS}row"):
        celdas = {}
        for c in row.findall(f"{NS}c"):
            ref = c.get("r", "A1")
            t = c.get("t")
            v = c.find(f"{NS}v")
            val = v.text if v is not None else None
            if t == "s" and val is not None:
                val = ss[int(val)] if int(val) < len(ss) else val
            elif t == "inlineStr":
                t_el = c.find(f"{NS}is/{NS}t")
                val = t_el.text if t_el is not None else val
            elif t == "b":
                val = val
            elif val is not None and re.fullmatch(r"-?\d+(\.\d+)?", val):
                f = float(val)
                val = int(f) if f.is_integer() else f
            celdas[_colnum(ref)] = val
        if celdas:
            ancho = max(celdas) + 1
            filas.append([celdas.get(i) for i in range(ancho)])
    header = filas[0]
    htxt = [str(c) if c is not None else "" for c in header]
    nombre_hoja = sname
    idx = {}
    for c in columnas + ["NOM_MUN", "NOM_ENT", "A\u00d1O"]:
        for i, h in enumerate(htxt):
            if h == c or (c == "A\u00d1O" and h in variantes(c)):
                idx[c] = i
                idx[c + "__fisica"] = h
                break
    datos = {c: [] for c in columnas}
    anios, nombres_mun, nombres_ent, pares = [], [], [], []
    n = 0
    for r in filas[1:]:
        if all(v is None or (isinstance(v, str) and v.strip() == "") for v in r):
            continue
        n += 1
        for c in columnas:
            datos[c].append(r[idx[c]] if c in idx and idx[c] < len(r) else None)
        if "A\u00d1O" in idx:
            anios.append(r[idx["A\u00d1O"]] if idx["A\u00d1O"] < len(r) else None)
        if "NOM_MUN" in idx:
            nombres_mun.append((r[idx[columnas[0]]] if idx[columnas[0]] < len(r) else None,
                                r[idx["NOM_MUN"]] if idx["NOM_MUN"] < len(r) else None))
        if "NOM_ENT" in idx and len(columnas) > 1:
            nombres_ent.append((r[idx[columnas[1]]] if idx[columnas[1]] < len(r) else None,
                                r[idx["NOM_ENT"]] if idx["NOM_ENT"] < len(r) else None))
        if len(columnas) == 2 and columnas[0] in idx and columnas[1] in idx:
            a = r[idx[columnas[0]]] if idx[columnas[0]] < len(r) else None
            b = r[idx[columnas[1]]] if idx[columnas[1]] < len(r) else None
            pares.append((a, b))
    return {"filas": n, "hoja": nombre_hoja, "header_fisico": htxt, "indices": {k: v for k, v in idx.items() if not k.endswith("__fisica")},
            "fisicas": {k: v for k, v in idx.items() if k.endswith("__fisica")},
            "posiciones": {c: {"hoja": nombre_hoja, "indice_1based": idx[c] + 1, "letra": _letra(idx[c]),
                               "encabezado": htxt[idx[c]]}
                           for c in columnas + ["NOM_MUN", "NOM_ENT", "A\u00d1O"] if c in idx},
            "datos": datos, "anios": anios, "nombres_mun": nombres_mun,
            "nombres_ent": nombres_ent, "pares": pares}


def leer_csv(path, columnas):
    raw = path.read_bytes()
    texto = None
    codif = None
    for enc in ("utf-8-sig", "latin-1"):
        try:
            texto = raw.decode(enc)
            codif = enc
            break
        except UnicodeDecodeError:
            continue
    lector = csv.DictReader(io.StringIO(texto))
    orden = {h: i for i, h in enumerate(lector.fieldnames or [])}
    campo = {c: None for c in columnas}
    for h in lector.fieldnames or []:
        for c in columnas + ["A\u00f1o", "A\u00d1O"]:
            if h == c or h.strip() == c:
                campo[c] = h
    datos = {c: [] for c in columnas}
    anios = []
    n = 0
    for fila in lector:
        if all((fila.get(h) or "").strip() == "" for h in lector.fieldnames or []):
            continue
        n += 1
        for c in columnas:
            datos[c].append(fila.get(campo[c]) if campo[c] else None)
        acol = campo.get("A\u00f1o") or campo.get("A\u00d1O")
        if acol:
            anios.append(fila.get(acol))
    return {"filas": n, "hoja": "CSV (hoja unica)", "header_fisico": lector.fieldnames, "codificacion": codif,
            "fisicas": {c: campo[c] for c in columnas},
            "posiciones": {c: {"hoja": "CSV (hoja unica)", "indice_1based": orden[campo[c]] + 1,
                               "letra": _letra(orden[campo[c]]), "encabezado": campo[c]}
                           for c in columnas + ["A\u00f1o", "A\u00d1O"] if campo.get(c)},
            "datos": datos, "anios": anios, "nombres_mun": [], "nombres_ent": [], "pares": []}


def resumir_columna(vals):
    orig = {}
    nulos = 0
    trans = set()
    for v in vals:
        o, t = texto_original(v)
        if o is None or norm(o) == "":
            nulos += 1
            continue
        trans.add(t)
        n = norm(o)
        orig.setdefault(n, set()).add(o)
    return {"distintos": sorted(orig), "nulos": nulos, "transformaciones": sorted(trans),
            "originales": {k: sorted(x) for k, x in orig.items()}}


def main():
    selftest()
    cats = cargar_catalogos()
    urls = cargar_urls()
    fecha = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    resultados = []
    for conjunto_id, rid, periodo, formato, columnas in DATOS:
        url = urls[rid]
        dest = descargar(rid, url)
        h = sha256(dest)
        lec = leer_xlsx(dest, columnas) if formato == "XLSX" else leer_csv(dest, columnas)
        for v in VARIABLES:
            if v["conjunto"] != conjunto_id:
                continue
            if v["variable"] not in columnas:
                continue
            cat = cats[(v["recurso_cat"], v["hoja"])]
            ref = lec["datos"][v["variable"]]
            res = resumir_columna(ref)
            catset = set(cat["codigos"])
            coins = [c for c in res["distintos"] if c in catset]
            fuera = [c for c in res["distintos"] if c not in catset]
            esp = [c for c in res["distintos"] if c in ESPECIALES_MUN] if v["nivel"] == "municipio" else []
            anios = sorted({norm(texto_original(a)[0]) for a in lec["anios"] if texto_original(a)[0] and norm(texto_original(a)[0]) != ""}) if lec["anios"] else []
            # coherencia compuesta CLAVE<->CLAVE_ENT: composicion exacta documentada
            # CLAVE (nnnnn) = CLAVE_ENT (nn) + municipio (3 digitos); igualdad exacta, sin relleno
            coh = None
            if len(columnas) == 2 and formato == "XLSX":
                mal = set()
                for a, b in lec["pares"]:
                    oa, _ = texto_original(a)
                    ob, _ = texto_original(b)
                    if oa is None or ob is None or norm(oa) == "" or norm(ob) == "":
                        continue
                    if not composicion_exacta(oa, ob):
                        mal.add((norm(oa), norm(ob)))
                coh = {"regla": "CLAVE(5 digitos) == CLAVE_ENT(2 digitos) + municipio(3 digitos); igualdad exacta",
                       "pares_distintos": len({(texto_original(a)[0], texto_original(b)[0]) for a, b in lec["pares"]}),
                       "incoherentes": sorted(mal)}
            # contradicciones de nombre solo si se leyo la columna de nombre
            contra = None
            if lec["nombres_mun"] and v["nivel"] == "municipio":
                por_cod = {}
                for cv, nv in lec["nombres_mun"]:
                    oc, _ = texto_original(cv)
                    if oc is None or norm(oc) == "":
                        continue
                    por_cod.setdefault(norm(oc), set()).add(str(nv).strip() if nv is not None else "")
                contra = {k: sorted(x) for k, x in por_cod.items() if len(x) > 1}
            magdalena = None
            if lec["nombres_mun"] and "26036" in res["distintos"]:
                magdalena = sorted({str(nv) for cv, nv in lec["nombres_mun"]
                                    if texto_original(cv)[0] and norm(texto_original(cv)[0]) == "26036" and nv})
            if fuera:
                estado = "no_compatible"
            elif res["nulos"] or esp or (coh and coh["incoherentes"]) or (contra):
                estado = "compatible_con_excepciones"
            else:
                estado = "compatible"
            resultados.append({
                "variable_id": v["id"], "diccionario": v["diccionario"], "variable": v["variable"],
                "significado": ("municipio" if v["nivel"] == "municipio" else "entidad") + " respaldado por definicion; columna fisica localizada por coincidencia exacta de encabezado",
                "conjunto": conjunto_id, "titulo": next(x["titulo"] for x in VARIABLES if x["conjunto"] == conjunto_id),
                "recurso_datos": rid, "periodo": periodo, "formato": formato,
                "columna_fisica": (lec["fisicas"].get(v["variable"] + "__fisica") if formato == "XLSX" else lec["fisicas"].get(v["variable"])),
                "columna_ubicacion": lec["posiciones"].get(v["variable"]),
                "ubicaciones_leidas": lec["posiciones"],
                "huella_fila_diccionario": v["huella"],
                "referencia": {"recurso": v["recurso_cat"], "hoja": v["hoja"], "sha256": cat["sha256"], "entradas": cat["filas"]},
                "consulta": {"metodo": "descarga publicada, lectura solo de columnas clave+anio+nombre" if formato == "XLSX" else "descarga publicada CSV, lectura solo de columnas clave+anio",
                             "url": url, "fecha_utc": fecha, "sha256_archivo": h, "bytes": dest.stat().st_size,
                             "archivo_local": f"descargas/{dest.name}",
                             "header_fisico": lec["header_fisico"] if formato == "CSV" else lec["header_fisico"]},
                "cobertura": {"tipo": "completa", "filas": lec["filas"], "claves_distintas": len(res["distintos"]),
                              "anios_distintos": anios},
                "coincidencias": {"n": len(coins), "claves": coins},
                "excepciones": {"nulos": res["nulos"], "especiales_no_municipales": esp,
                                "sin_correspondencia": fuera,
                                "transformaciones_observadas": res["transformaciones"]},
                "coherencia_compuesta": coh, "contradicciones_nombre": contra,
                "magdalena_26036_nombres": magdalena,
                "transformacion_propuesta": "strip al comparar; conservar original y ceros; sin relleno ni prefijo",
                "estado_cobertura": "completa", "estado_resultado": estado,
                "limitaciones": ("Compatibilidad de valores no demuestra vigencia historica "
                                 "ni autoriza cruces entre poblaciones, periodos o niveles de agregacion."),
            })
            CLAV.joinpath(f"{rid}_{v['variable'].replace('.', '').replace(' ', '_')}.json").write_text(
                json.dumps({"recurso": rid, "periodo": periodo, "variable": v["variable"],
                            "distintos_normalizados": res["distintos"],
                            "originales_por_clave": res["originales"], "nulos": res["nulos"],
                            "sha256_archivo": h}, ensure_ascii=False, indent=1), encoding="utf-8")
    # caso especial: victimas 2015 no tiene columna fisica Clave_Ent.
    # Encabezado extraido del archivo (no manual); revision de encabezado completa,
    # validacion de valores no aplicable.
    variantes_v6 = [r for r in resultados if r["variable_id"] == "V6"]
    if not any(r["periodo"] == "2015" for r in variantes_v6):
        rid15 = "4c1f984e-a6be-412b-b274-5af2d4ff55b1"
        v6 = next(v for v in VARIABLES if v["id"] == "V6")
        cat = cats[(v6["recurso_cat"], v6["hoja"])]
        url = urls[rid15]
        dest = DESC / (rid15 + ".csv")
        with open(dest, encoding="utf-8-sig", newline="") as f:
            encabezado_archivo = next(csv.reader(f))
        resultados.append({
            "variable_id": "V6", "diccionario": v6["diccionario"], "variable": "Clave_Ent",
            "significado": "entidad-registro respaldada por definicion; SIN columna fisica en el recurso 2015",
            "conjunto": v6["conjunto"], "titulo": v6["titulo"], "recurso_datos": rid15, "periodo": "2015",
            "formato": "CSV", "columna_fisica": None, "columna_ubicacion": None, "ubicaciones_leidas": {},
            "huella_fila_diccionario": v6["huella"],
            "referencia": {"recurso": v6["recurso_cat"], "hoja": v6["hoja"], "sha256": cat["sha256"], "entradas": cat["filas"]},
            "consulta": {"metodo": "descarga publicada; encabezado extraido del archivo, sin lectura de valores",
                         "url": url, "fecha_utc": fecha, "sha256_archivo": sha256(dest), "bytes": dest.stat().st_size,
                         "archivo_local": f"descargas/{dest.name}",
                         "header_fisico": encabezado_archivo},
            "cobertura": {"tipo": "no_aplicable", "revision_encabezado": "completa",
                          "validacion_valores": "no_aplicable",
                          "filas": None, "claves_distintas": None, "anios_distintos": ["2015"]},
            "coincidencias": {"n": 0, "claves": []},
            "excepciones": {"nulos": 0, "especiales_no_municipales": [],
                            "sin_correspondencia": [],
                            "transformaciones_observadas": [],
                            "nota": "El recurso 2015 trae 'Cve. Municipio' (nivel municipal) sin respaldo en el diccionario a8a09044; no se homologa con Clave_Ent."},
            "coherencia_compuesta": None, "contradicciones_nombre": None, "magdalena_26036_nombres": None,
            "transformacion_propuesta": "ninguna; columna fuera del alcance de las ocho variables",
            "estado_cobertura": "encabezado_completo", "estado_resultado": "sin_columna_fisica",
            "limitaciones": "No se comprueba Clave_Ent en 2015 porque la columna no existe en ese recurso. "
                            "Revision de encabezado completa; validacion de valores no aplicable.",
        })
    (BASE / "resultados_intermedios.json").write_text(
        json.dumps({"fecha_utc": fecha, "resultados": resultados}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"recursos: {len(DATOS)}, comprobaciones: {len(resultados)}, fecha: {fecha}")


if __name__ == "__main__":
    main()
