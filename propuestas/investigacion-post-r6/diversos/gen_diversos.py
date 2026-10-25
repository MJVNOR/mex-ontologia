"""Generador/verificador de la entrega diversos (investigacion-post-r6).

Uso:
  uv run python propuestas/investigacion-post-r6/diversos/gen_diversos.py inspeccionar
  uv run python propuestas/investigacion-post-r6/diversos/gen_diversos.py hashes
Solo lee/escribe dentro de propuestas/investigacion-post-r6/diversos/.
"""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path("propuestas/investigacion-post-r6/diversos")
EV = BASE / "evidencia"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inspeccionar() -> None:
    p = EV / "dgis-ehosp-descripcion-intento.html"
    txt = p.read_bytes().decode("iso-8859-1", errors="replace")
    print("bytes:", len(txt))
    print("tiene_iframe:", "iframe" in txt.lower())
    import re
    print("menciones_variable:", len(re.findall(r"(?i)variable", txt)))
    print("links_dat_ehosp:", sorted(set(re.findall(r"Dat-Ehosp-[A-Za-z_]+\.html", txt)))[:12])
    print("iframes:", re.findall(r'iframe[^>]*src="([^"]+)"', txt))
    c = EV / "conapo-im2020.html"
    print("conapo_bytes:", c.stat().st_size, "es_reto:", "Challenge Validation" in c.read_text(errors="replace"))


def hashes() -> None:
    files = sorted(BASE.rglob("*"))
    out = []
    for f in files:
        if f.is_file() and f.name != "listo.json":
            out.append({"ruta": f.as_posix(), "sha256": sha256(f), "bytes": f.stat().st_size})
    for e in out:
        print(e["ruta"], e["bytes"], e["sha256"][:16])


def descargar(url: str, nombre: str, timeout: int = 300) -> dict:
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "MEX-Ontologi-investigacion-post-r6/diversos"})
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        data = r.read()
        p = EV / nombre
        p.write_bytes(data)
        return {"archivo": nombre, "url": url, "http": r.status,
                "bytes": len(data), "sha256": sha256(p),
                "fecha_consulta_utc": "2026-10-24",
                "content_type": r.headers.get("Content-Type")}
    except Exception as ex:  # noqa: BLE001
        return {"archivo": nombre, "url": url, "http": None, "bytes": 0,
                "sha256": None, "fecha_consulta_utc": "2026-10-24",
                "error": repr(ex)[:300]}


def ronda2() -> None:
    import json as _json
    log = []
    log.append(descargar(
        "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/IMC_2020.zip",
        "conapo-IMC_2020.zip"))
    print(log[-1].get("http"), log[-1].get("bytes"), (log[-1].get("sha256") or "")[:16])
    log.append(descargar(
        "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/imc2020_shp.zip",
        "conapo-imc2020_shp.zip"))
    print(log[-1].get("http"), log[-1].get("bytes"), (log[-1].get("sha256") or "")[:16])
    log.append(descargar(
        "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Marginacion/Indice_de_marginacion_urbana_por_colonia_2020.rar",
        "conapo-calculo-colonia-2020.rar"))
    print(log[-1].get("http"), log[-1].get("bytes"), (log[-1].get("sha256") or "")[:16])
    for u, n in [
        ("http://sinba08.salud.gob.mx/cubos/Metadatos/fuentes/Dat-Ehosp-Descripcion_de_variables.html",
         "dgis-ehosp-descripcion-fuentespath.html"),
        ("http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html",
         "dgis-ehosp-descripcion-minusculas.html"),
        ("https://sinba08.salud.gob.mx/cubos/Metadatos/Dat-Ehosp-Descripcion_de_variables.html",
         "dgis-ehosp-descripcion-https.html"),
    ]:
        log.append(descargar(u, n))
        print(n, log[-1].get("http"), log[-1].get("bytes"),
              (log[-1].get("sha256") or "")[:16],
              (log[-1].get("error") or "")[:120])
    _json.dump(log, (EV / "http-log-ronda2.json").open("w", encoding="utf-8"),
               indent=1, ensure_ascii=False)
    print("ronda2 log guardado")


def verificar() -> None:
    import json as _json
    ent = _json.loads((BASE / "entrega.json").read_text(encoding="utf-8"))
    assert ent["grupo_fuente"] == "diversos", "grupo"
    ids = set(ent["ids_asignados"])
    decs = ent["decisiones"]
    assert len(decs) == 5, f"decisiones={len(decs)}"
    assert {d["definicion_iri"] for d in decs} == ids, "iris"
    for d in decs:
        assert d["estado"] in ("propuesta_respaldada", "sigue_pendiente"), d
        assert d["huella_fila_diccionario"] and d["variable"], d
        for e in d["evidencia"]:
            p = Path(e["ruta"])
            assert p.is_file(), f"falta {e['ruta']}"
            assert sha256(p) == e["sha256"], f"sha {e['ruta']}"
        if d["estado"] == "propuesta_respaldada":
            assert d.get("significado_propuesto"), d
    for f in ent["fuentes"]:
        p = Path(f["ruta"])
        if (BASE / "evidencia").as_posix() in f["ruta"] or f["ruta"].startswith("propuestas/investigacion-post-r6/diversos"):
            assert p.is_file(), f"falta {f['ruta']}"
            assert sha256(p) == f["sha256"], f"sha {f['ruta']}"
    print("verificacion OK: 5 decisiones, fuentes y evidencias con SHA correspondiente")


def examinar() -> None:
    import zipfile
    for n in ["conapo-IMC_2020.zip", "conapo-imc2020_shp.zip"]:
        p = EV / n
        print("=" * 20, n, p.stat().st_size)
        try:
            z = zipfile.ZipFile(p)
            for i in z.infolist():
                print(f"  {i.file_size:>12}  {i.filename}")
        except Exception as ex:  # noqa: BLE001
            print("  ERROR:", repr(ex)[:200])
    r = EV / "conapo-calculo-colonia-2020.rar"
    b = r.read_bytes()
    print("=" * 20, "rar", len(b), "magia:", b[:16])


def dbf_campos() -> None:
    import struct
    import zipfile
    z = zipfile.ZipFile(EV / "conapo-imc2020_shp.zip")
    raw = z.read("colonias_imc2020.dbf")
    print("dbf bytes:", len(raw))
    nreg, hlen, rlen = struct.unpack("<IHH", raw[4:12])
    print("registros:", nreg, "header_len:", hlen, "record_len:", rlen)
    off = 32
    while raw[off] != 0x0D:
        name = raw[off:off + 11].split(b"\x00")[0].decode("latin-1")
        typ = chr(raw[off + 11])
        ln = raw[off + 16]
        print(f"  campo={name} tipo={typ} long={ln}")
        off += 32


def dbf_clasif() -> None:
    import struct
    import zipfile
    from collections import Counter
    z = zipfile.ZipFile(EV / "conapo-imc2020_shp.zip")
    raw = z.read("colonias_imc2020.dbf")
    nreg, hlen, rlen = struct.unpack("<IHH", raw[4:12])
    fields = []
    off = 32
    while raw[off] != 0x0D:
        name = raw[off:off + 11].split(b"\x00")[0].decode("latin-1")
        ln = raw[off + 16]
        fields.append((name, ln))
        off += 32
    pos = 1
    target = None
    for name, ln in fields:
        if name == "CLASIF":
            target = (pos, ln)
            break
        pos += ln
    assert target, "sin CLASIF"
    p, ln = target
    c = Counter()
    for i in range(nreg):
        base = hlen + i * rlen
        val = raw[base + p:base + p + ln].decode("latin-1").strip()
        c[val] += 1
    print("distintos:", len(c))
    for v, n in c.most_common():
        print(f"  {n:>7}  {v!r}")


def dbf_sonora() -> None:
    import struct
    import zipfile
    from collections import Counter
    z = zipfile.ZipFile(EV / "conapo-imc2020_shp.zip")
    raw = z.read("colonias_imc2020.dbf")
    nreg, hlen, rlen = struct.unpack("<IHH", raw[4:12])
    fields = []
    off = 32
    while raw[off] != 0x0D:
        name = raw[off:off + 11].split(b"\x00")[0].decode("latin-1")
        ln = raw[off + 16]
        fields.append((name, ln))
        off += 32
    pos = {}
    p = 1
    for name, ln in fields:
        pos[name] = (p, ln)
        p += ln
    pe, le = pos["CVE_ENT"]
    pc, lc = pos["CLASIF"]
    c = Counter()
    nson = 0
    ej = []
    for i in range(nreg):
        base = hlen + i * rlen
        if raw[base + pe:base + pe + le].decode("latin-1").strip() == "26":
            nson += 1
            v = raw[base + pc:base + pc + lc].decode("latin-1").strip()
            c[v] += 1
            if len(ej) < 3:
                pv, lv = pos["CVE_COL"]
                ej.append((raw[base + pv:base + pv + lv].decode("latin-1").strip(), v))
    print("registros_sonora:", nson)
    print("distintos_sonora:", len(c))
    for v, n in c.most_common():
        print(f"  {n:>6}  {v!r}")
    print("ejemplos:", ej)


def xlsx_nacional() -> None:
    from openpyxl import load_workbook
    tmp = EV / "_tmp_IMUC_2020.xlsx"
    wb = load_workbook(tmp, read_only=True, data_only=True)
    print("hojas:", wb.sheetnames)
    ws = wb["Diccionario"]
    for r in ws.iter_rows(values_only=True):
        print(" | ".join("" if v is None else str(v)[:60] for v in r))


def xlsx_sonora() -> None:
    from collections import Counter
    from openpyxl import load_workbook
    tmp = EV / "_tmp_IMUC_2020.xlsx"
    wb = load_workbook(tmp, read_only=True, data_only=True)
    c = Counter()
    n = 0
    ncol = None
    for ws in (wb["IMUC_2020_AGS-MOR"], wb["IMUC_2020_NAY-ZAC"]):
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                head = ["" if v is None else str(v) for v in r]
                try:
                    ice, icl = head.index("CVE_ENT"), head.index("CLASIF")
                except ValueError:
                    print("hoja sin encabezado:", ws.title, head[:6])
                    break
                ncol = len(head)
                continue
            n += 1
            if str(r[ice]).strip() == "26":
                c[str(r[icl])] += 1
    print("filas_totales:", n, "columnas:", ncol)
    print("sonora_distintos:", len(c))
    for v, k in c.most_common():
        print(f"  {k:>6}  {v!r}")


def ronda2b() -> None:
    import json as _json
    import shutil
    log = []
    log.append(descargar(
        "https://datos.sonora.gob.mx/dataset/a3320cad-afd3-4840-8c3b-36236df26099/resource/09ef2342-fd9f-4334-bcd5-9c969baca32f/download/indice-de-marginacion-colonias-2020.xlsx",
        "sonora-imc2020-local.xlsx"))
    print(log[-1].get("http"), log[-1].get("bytes"), (log[-1].get("sha256") or "")[:16])
    print("extractor_rar:", shutil.which("unrar"), shutil.which("7z"), shutil.which("bsdtar"))
    _json.dump(log, (EV / "http-log-ronda2b.json").open("w", encoding="utf-8"),
               indent=1, ensure_ascii=False)


def xlsx_local() -> None:
    from collections import Counter
    from openpyxl import load_workbook
    wb = load_workbook(EV / "sonora-imc2020-local.xlsx", read_only=True, data_only=True)
    print("hojas:", wb.sheetnames)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    head = ["" if v is None else str(v) for v in next(rows)]
    print("columnas:", len(head))
    print("encabezado:", head)
    icl = head.index("CLASIF")
    c = Counter()
    n = 0
    for r in rows:
        n += 1
        c[str(r[icl])] += 1
    print("filas_datos:", n, "distintos:", len(c))
    for v, k in c.most_common():
        print(f"  {k:>6}  {v!r}")


def ronda2c() -> None:
    import json as _json
    log = []
    for u, n in [
        ("http://sinba08.salud.gob.mx/cubos/Metadatos/stmenu.js", "dgis-stmenu.js"),
        ("http://sinba08.salud.gob.mx/cubos/Metadatos/fuentes/", "dgis-fuentes-dir.html"),
        ("http://sinba08.salud.gob.mx/cubos/cuboSectorialEgresos1822.html",
         "dgis-cubo-sectorial-1822.html"),
    ]:
        log.append(descargar(u, n))
        print(n, log[-1].get("http"), log[-1].get("bytes"),
              (log[-1].get("sha256") or "")[:16],
              (log[-1].get("error") or "")[:100])
    _json.dump(log, (EV / "http-log-ronda2c.json").open("w", encoding="utf-8"),
               indent=1, ensure_ascii=False)


def ronda2fin() -> None:
    import json as _json
    p = BASE / "entrega.json"
    ent = _json.loads(p.read_text(encoding="utf-8"))
    dec = {d["definicion_iri"]: d for d in ent["decisiones"]}
    claus = " En manos del publicador según R6; la búsqueda negativa acotada no prueba exclusividad: vale cualquier evidencia primaria inequívoca vinculada a la fila, venga de la fuente que venga."

    cl = dec["https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5"]
    cl["estado"] = "propuesta_respaldada"
    cl["significado_propuesto"] = ("Clasificación del tipo de asentamiento de la colonia: atributo CLASIF del producto "
        "CONAPO Índice de marginación urbana por colonia 2020 (IMC_2020), a nivel colonia, estimado con base en el "
        "Censo de Población y Vivienda 2020. Dominio de referencia nacional: 38 valores observados; en Sonora se "
        "observan 7 (Barrio, Colonia, Ejido, Fraccionamiento, Privada, Residencial, Unidad habitacional) más '-' "
        "como marcador de nulo declarado en el diccionario local.")
    cl["evidencia"] += [
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/sonora-imc2020-local.xlsx",
         "sha256": "14a741bb438adbf82aa535baaf87abe0fab94fd23c8df86b84fa98d1904b5224",
         "localizador": "hoja IMC_2020, 28 columnas, 2129 filas de datos; conteo CLASIF idéntico al nacional-Sonora",
         "afirmacion_soportada": "Archivo local auténtico (sha idéntico a la inspección preservada): el extracto Sonora del producto nacional, con nulo '-' declarado."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-IMC_2020.zip",
         "sha256": "5d93b314428f88008ba380bac56b587169cfefd3acaf4659857a07874822b8bb",
         "localizador": "IMUC_2020.xlsx: hojas IMUC_2020_* (74227 filas) + Diccionario (CLASIF='Clasificación', Fuente CONAPO/INEGI Censo 2020)",
         "afirmacion_soportada": "El producto nacional a nivel colonia trae diccionario espejo del local (28 variables) y datos Sonora (2129 filas) idénticos al archivo local."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-imc2020_shp.zip",
         "sha256": "69d73b5bb0127df6c81701684eb28cd6bd666d9319a1ffb45da76446ae278426",
         "localizador": "colonias_imc2020.dbf: campo CLASIF C(25); subset CVE_ENT=26 → 2129 registros, 8 valores, conteos idénticos",
         "afirmacion_soportada": "La cartografía nacional a nivel colonia confirma variable, nivel y dominio con la misma distribución exacta."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-imc-diccionario-nota.md",
         "sha256": "97ac6f973389087eac54346b1893dd7cacaa8fba443b21bc14e2d7980f374ccd",
         "localizador": "tabla Variable|Descripción + pie de fuente + encabezado IMUC_2020_NAY-ZAC",
         "afirmacion_soportada": "Transcripción citable del diccionario nacional y del esquema de datos a nivel colonia."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-clasif-comparativa-nota.md",
         "sha256": "e0f3d75a58418b3a7118b94027d1e2425c398b8b75702a5e9d019ce84a0352c4",
         "localizador": "tablas de conteos local/nacional-xlsx/nacional-shp + dominio nacional de 38 valores",
         "afirmacion_soportada": "Identidad de valores local↔Sonora-nacional; dominio nacional 38 valores; códigos INEGI no adoptados."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-calculo-colonia-2020.rar",
         "sha256": "27ade0e655d49570cafcfe5d13540430bbc13891ac5a8129c3f41a9195a59ee0",
         "localizador": "magia Rar! (verificada), 3193 bytes; sin extractor (unrar/7z/bsdtar ausentes)",
         "afirmacion_soportada": "El programa de cálculo existe y es un RAR genuino, pero su contenido no pudo examinarse (NEG-DIV-06)."},
    ]
    cl["vinculo_fuente_local"] += (" Archivo local 09ef2342 (hoja IMC_2020, 2129 filas) idéntico en valores, "
        "distribución, esquema (28 columnas) y formato de clave (nnnnn_nnnn) al extracto Sonora (CVE_ENT=26) del "
        "producto nacional IMC_2020, ed. 2020, enlazado por el publicador en Fuentes extras.")
    cl["evidencia_faltante"] = ("Ninguna bloqueante. Residual: la declaración del publicador (Fuentes extras) es a "
        "nivel de conjunto, no cita conjunto+diccionario+fila+huella; ver límites.")
    cl["motivo"] = ("Propuesta respaldada bajo el criterio, opción (3): el publicador declara en CKAN base censal "
        "INEGI y Fuentes extras = página CONAPO índices-2020 (evidencia primaria del propio publicador vinculada al "
        "conjunto); el producto enlazado (IMC_2020, ed. 2020, a nivel colonia, sin equiparar localidad/AGEB) trae "
        "diccionario espejo con CLASIF y datos cuyo extracto Sonora es idéntico al archivo local (2129 filas, "
        "distribución exacta 1050/854/119/89/7/7/2/1, clave nnnnn_nnnn, 28 columnas); el '-' es nulo declarado "
        "(obligatoriedad: No). Cadena recurso/campo/versión vinculada sin definiciones inventadas.")
    cl["limites"] = [
        "La declaración del publicador es a nivel de conjunto (Fuentes extras), no cita fila+huella: la promoción queda condicionada a que el rol integrador acepte esta cadena como 'explícita' bajo la opción (3).",
        "No se adoptan los códigos numéricos INEGI 1-43; el dominio acreditable es el textual del producto CONAPO (38 valores nacionales; 7+'-' en Sonora).",
        "'-' = nulo declarado (obligatoriedad: No), no un tipo de asentamiento.",
        "No se equipara localidad/AGEB con colonia: toda la evidencia es de producto a nivel colonia (IMUC_2020).",
        "El RAR del programa de cálculo no fue examinado (sin extractor): no aporta ni resta.",
    ]

    te = dec["https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15"]
    te["evidencia"] += [
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/dgis-ehosp-descripcion-minusculas.html",
         "sha256": "a7840926d6f4f4fcf8bedc3875a3ec22763c06129e1628ff2e8ec38fc56a8b0e",
         "localizador": "sha idéntico al intento con mayúsculas: mismo marco sin tabla",
         "afirmacion_soportada": "El contenido no depende de la capitalización de la URL: ambas variantes sirven el mismo marco."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/dgis-cubo-sectorial-1822.html",
         "sha256": "1c445b46eff1132922e9ffab2bd77f54690fda07bcdc07b64ae082a90ecdf17f",
         "localizador": "contenedor JS de 5625 bytes, solo título; sin tabla de variables extraíble",
         "afirmacion_soportada": "El cubo sectorial 2018-2022 (época del recurso local) tampoco expone su diccionario de variables por estas vías."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/http-log-ronda2c.json",
         "sha256": "3069bfbe53bb9b643a1e89ef6a8ff47f586432f059068ff4a33868d4738d0b4c",
         "localizador": "entradas stmenu.js (404), fuentes/ (403), sectorial (200), https (timeout)",
         "afirmacion_soportada": "Registro de la ronda 2c: el archivo de variables no existe en fuentes/ (404), el menú JS no se sirve (404) y no hay listado (403)."},
    ]
    te["motivo"] += (" Ronda 2 (2026-10-24): agotadas las rutas efectivas del marco (variante en minúsculas con "
        "bytes idénticos, ruta fuentes/ 404, stmenu.js 404, listado de directorio 403, https con timeout, cubo "
        "sectorial 2018-2022 sin tabla): la tabla de variables DGIS no es recuperable por estas vías.")

    for iri in [
        "https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2",
        "https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7",
        "https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8",
    ]:
        dec[iri]["evidencia_faltante"] = dec[iri]["evidencia_faltante"].rstrip() + claus
    te["evidencia_faltante"] = te["evidencia_faltante"].rstrip() + claus

    for n in ent["busquedas_negativas_limitadas"]:
        if n["id"] == "NEG-DIV-01":
            n["alcance"] = ("SUPERADA 2026-10-24: IMC_2020.zip (43 MB, sha 5d93b314…) e imc2020_shp.zip (38 MB, sha "
                "69d73b5b…) descargados de conapo.segob.gob.mx (HTTP 200); RAR del programa de cálculo descargado "
                "(3193 bytes, RAR genuino) pero no examinado por falta de extractor (NEG-DIV-06).")
        if n["id"] == "NEG-DIV-02":
            n["alcance"] += (" Ronda 2c: variante en minúsculas idéntica, fuentes/Dat-Ehosp-… 404, stmenu.js 404, "
                "listado 403, https con timeout, cubo sectorial sin tabla (NEG-DIV-05).")
        if n["id"] == "NEG-DIV-04":
            n["alcance"] = ("Metodología/cuestionario PROAES, diccionario corregido de pesca SAGARHPA y aclaración "
                "de Servicios de Salud de Sonora: sin documento público localizado en portal CKAN (Fuentes extras "
                "vacías en los tres conjuntos) ni en DGIS/CONAPO/INEGI revisados. En manos del publicador según R6; "
                "esta búsqueda negativa acotada no prueba exclusividad: vale cualquier evidencia primaria "
                "inequívoca vinculada a la fila, venga de la fuente que venga. No se contacta.")
    ent["busquedas_negativas_limitadas"] += [
        {"id": "NEG-DIV-05", "fecha_utc": "2026-10-24",
         "alcance": "Tabla de variables del cubo DGIS agotada por las vías accesibles: marco con/sin mayúsculas (mismo sha), ruta en fuentes/ 404, stmenu.js 404, listado de directorio 403, https con timeout, cubo sectorial 2018-2022 contenedor JS sin tabla. Acotado a lo revisado."},
        {"id": "NEG-DIV-06", "fecha_utc": "2026-10-24",
         "alcance": "Programa de cálculo CONAPO a nivel colonia (.rar, 3193 bytes, magia Rar! verificada): sin extractor disponible (unrar/7z/bsdtar ausentes); contenido no examinado. Acotado a esta limitación técnica."},
    ]
    ent["fuentes"] += [
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-IMC_2020.zip",
         "url": "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/IMC_2020.zip",
         "sha256": "5d93b314428f88008ba380bac56b587169cfefd3acaf4659857a07874822b8bb",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web",
         "contenido": "Base nacional IMC_2020 (IMUC_2020.xlsx: hojas IMUC_2020_* a nivel colonia, 74227 filas, + Diccionario con CLASIF).",
         "localizador": "IMUC_2020.xlsx: Diccionario (CLASIF='Clasificación') + IMUC_2020_NAY-ZAC (encabezado 28 col, subset Sonora 2129 filas)"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-imc2020_shp.zip",
         "url": "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Colonia/imc2020_shp.zip",
         "sha256": "69d73b5bb0127df6c81701684eb28cd6bd666d9319a1ffb45da76446ae278426",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web",
         "contenido": "Cartografía nacional a nivel colonia (74226 registros): campo CLASIF C(25), 38 valores; Sonora 8 valores idénticos al local.",
         "localizador": "colonias_imc2020.dbf: campos (OBJECTID…CLASIF) + subset CVE_ENT=26"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-calculo-colonia-2020.rar",
         "url": "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Marginacion/Indice_de_marginacion_urbana_por_colonia_2020.rar",
         "sha256": "27ade0e655d49570cafcfe5d13540430bbc13891ac5a8129c3f41a9195a59ee0",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web_intento_limitado",
         "contenido": "Programa de cálculo a nivel colonia (RAR genuino, 3193 bytes; contenido no examinado, NEG-DIV-06).",
         "localizador": "magia Rar! verificada; sin extractor disponible"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/sonora-imc2020-local.xlsx",
         "url": "https://datos.sonora.gob.mx/dataset/a3320cad-afd3-4840-8c3b-36236df26099/resource/09ef2342-fd9f-4334-bcd5-9c969baca32f/download/indice-de-marginacion-colonias-2020.xlsx",
         "sha256": "14a741bb438adbf82aa535baaf87abe0fab94fd23c8df86b84fa98d1904b5224",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web",
         "contenido": "Archivo local auténtico (sha idéntico a la inspección preservada): hoja IMC_2020, 2129 filas, CLASIF con 7 valores + '-' nulo.",
         "localizador": "hoja IMC_2020, encabezado 28 col; conteo CLASIF 1050/854/119/89/7/7/2/1"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-imc-diccionario-nota.md",
         "sha256": "97ac6f973389087eac54346b1893dd7cacaa8fba443b21bc14e2d7980f374ccd",
         "fecha_consulta": "2026-10-24", "tipo": "nota_analisis",
         "contenido": "Transcripción del Diccionario nacional IMUC_2020 y del encabezado de datos a nivel colonia.",
         "localizador": "tabla Variable|Descripción + pie de fuente"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-clasif-comparativa-nota.md",
         "sha256": "e0f3d75a58418b3a7118b94027d1e2425c398b8b75702a5e9d019ce84a0352c4",
         "fecha_consulta": "2026-10-24", "tipo": "nota_analisis",
         "contenido": "Comparativa de dominios CLASIF local/nacional-xlsx/nacional-shp + dominio nacional de 38 valores.",
         "localizador": "tablas de conteos + lista de 38 valores"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/dgis-ehosp-descripcion-minusculas.html",
         "url": "http://sinba08.salud.gob.mx/cubos/Metadatos/Dat-ehosp-Descripcion_de_variables.html",
         "sha256": "a7840926d6f4f4fcf8bedc3875a3ec22763c06129e1628ff2e8ec38fc56a8b0e",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web_intento_limitado",
         "contenido": "Variante en minúsculas: bytes idénticos al intento con mayúsculas (mismo marco sin tabla).",
         "localizador": "sha idéntico a dgis-ehosp-descripcion-intento.html"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/dgis-cubo-sectorial-1822.html",
         "url": "http://sinba08.salud.gob.mx/cubos/cuboSectorialEgresos1822.html",
         "sha256": "1c445b46eff1132922e9ffab2bd77f54690fda07bcdc07b64ae082a90ecdf17f",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web_intento_limitado",
         "contenido": "Cubo sectorial 2018-2022: contenedor JS sin tabla de variables extraíble.",
         "localizador": "solo título del cubo; 5625 bytes"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/http-log-ronda2.json",
         "sha256": "69bb03d12964cdf2f301fcae348c30c8a6f3671cb443b67f18202a0ac4ee421a",
         "fecha_consulta": "2026-10-24", "tipo": "log_generado",
         "contenido": "Registro de descargas ronda 2 (CONAPO zips/rar + 3 variantes DGIS).",
         "localizador": "entradas por archivo"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/http-log-ronda2b.json",
         "sha256": "e5f290b816b79fbcab1fe6b79398c87d31af9513d1d55c747a39608804801025",
         "fecha_consulta": "2026-10-24", "tipo": "log_generado",
         "contenido": "Registro de descarga del xlsx local + verificación de extractores RAR ausentes.",
         "localizador": "entradas por archivo"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/http-log-ronda2c.json",
         "sha256": "3069bfbe53bb9b643a1e89ef6a8ff47f586432f059068ff4a33868d4738d0b4c",
         "fecha_consulta": "2026-10-24", "tipo": "log_generado",
         "contenido": "Registro ronda 2c (stmenu.js 404, fuentes/ 403, sectorial 200, https timeout).",
         "localizador": "entradas por archivo"},
    ]
    ent["resumen_investigacion"] += (" Ronda 2 (2026-10-24): descargados y examinados IMC_2020.zip (base nacional "
        "a nivel colonia, 74227 filas + Diccionario con CLASIF) e imc2020_shp.zip (74226 registros, campo CLASIF): "
        "el archivo local (2129 filas) es idéntico en valores al extracto Sonora del producto nacional y el "
        "diccionario local es espejo del nacional; CLASIF pasa a propuesta_respaldada (opción 3) con insumos en "
        "staging/clasif.json. Pista DGIS agotada por las vías accesibles (NEG-DIV-05); RAR de cálculo sin extractor "
        "(NEG-DIV-06). Se corrige el lenguaje de exclusividad: las búsquedas negativas acotadas no prueban que solo "
        "el publicador posea los documentos faltantes.")
    ent["propuestas_respaldadas"] = 1
    ent["siguen_pendientes"] = 4
    p.write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
    print("entrega.json actualizada")


def cotejar() -> None:
    import json as _json
    dep = _json.loads(Path("reports/pendientes-depurados.json").read_text(encoding="utf-8"))
    ent = _json.loads((BASE / "entrega.json").read_text(encoding="utf-8"))
    src = {s["definicion_iri"]: s for s in dep["significados"] if s.get("grupo_fuente") == "diversos"}
    print("diversos en depurados:", len(src))
    cambios = 0
    for d in ent["decisiones"]:
        iri = d["definicion_iri"]
        s = src.get(iri)
        assert s is not None, f"IRI sin fuente: {iri}"
        for campo in ("variable", "descripcion_original", "huella_fila_diccionario"):
            if d.get(campo) != s[campo]:
                print(f"MISMATCH {d.get('variable')}/{campo}: entrega={d.get(campo)!r} depurados={s[campo]!r}")
                d[campo] = s[campo]
                cambios += 1
    print("fuente depurados:", dep["generado_en_utc"], "| cambios aplicados:", cambios)
    if cambios:
        (BASE / "entrega.json").write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
        print("entrega.json reescrita (solo campos originales)")


def defectos() -> None:
    import json as _json
    p = BASE / "entrega.json"
    ent = _json.loads(p.read_text(encoding="utf-8"))
    dec = {d["definicion_iri"]: d for d in ent["decisiones"]}
    base = (" No localizado en fuentes examinadas (portal CKAN, DGIS/CONAPO/INEGI revisados; R6). "
        "En manos del publicador según R6; la búsqueda negativa acotada no prueba exclusividad ni "
        "capacidad única: vale cualquier evidencia primaria inequívoca vinculada a la fila, venga de "
        "la fuente que venga.")
    dec["https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2"]["evidencia_faltante"] = (
        "Metodología o cuestionario PROAES de Denuncias Ambientales que defina 'estrato' y a qué "
        "trimestre refiere TRIMESTRE (calendario de denuncia vs estrato operativo/muestral)." + base)
    dec["https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15"]["evidencia_faltante"] = (
        "Documento que fije qué cuenta Total_Egresos (egresos vs urgencias): aclaración aplicable a la fila "
        "o diccionario corregido / fe de erratas (conjunto+diccionario+fila+huella citados)." + base)
    dec["https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F7"]["evidencia_faltante"] = (
        "Diccionario corregido o metodología que complete 'Clave de otras' (objeto: otras oficinas, especies, "
        "orígenes u otro) y su catálogo, con edición y periodo; o evidencia primaria inequívoca vinculada a la fila." + base)
    dec["https://example.org/mex-ontologi/definition/863b9cc8-daeb-4430-b835-6a0ced5abd31%2F8"]["evidencia_faltante"] = (
        "Diccionario corregido o metodología que complete 'Clave/Nombre de otras' y su catálogo; o evidencia "
        "primaria inequívoca vinculada a la fila." + base)
    for iri, d in dec.items():
        assert "Solo el publicador" not in d.get("evidencia_faltante", ""), iri
        assert "Solo publicador" not in d.get("evidencia_faltante", ""), iri
    p.write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
    print("defecto 2 aplicado: 4 evidencia_faltante sin exclusividad")


def xlsx_conteo() -> None:
    from openpyxl import load_workbook
    import zipfile
    z = zipfile.ZipFile(EV / "conapo-IMC_2020.zip")
    tmp = EV / "_tmp_IMUC_2020.xlsx"
    if not tmp.exists():
        with z.open("IMUC_2020.xlsx") as f, tmp.open("wb") as o:
            o.write(f.read())
    wb = load_workbook(tmp, read_only=True, data_only=True)
    for name in ("IMUC_2020_AGS-MOR", "IMUC_2020_NAY-ZAC"):
        ws = wb[name]
        n = 0
        nv = 0
        vacias = 0
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                continue
            n += 1
            if r[0] is None or str(r[0]).strip() == "":
                vacias += 1
            else:
                nv += 1
        print(f"{name}: filas_datos={n} con_clave={nv} vacias={vacias}")
    wb.close()
    tmp.unlink()


def integrador() -> None:
    import json as _json
    p = BASE / "entrega.json"
    ent = _json.loads(p.read_text(encoding="utf-8"))
    dec = {d["definicion_iri"]: d for d in ent["decisiones"]}
    cl = dec["https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5"]
    prop = cl.pop("significado_propuesto", None)
    assert prop, "sin propuesta activa que historiar"
    cl["estado"] = "sigue_pendiente"
    cl["historial_propuesta_rechazada"] = {
        "significado_propuesto_original": prop,
        "fecha_propuesta": "2026-10-24",
        "decision": "NO promover (integrador tras 2 auditorías)",
        "fecha_decision": "2026-10-24",
        "motivos": [
            "Ambas auditorías coinciden: 'tipo de asentamiento' carece de fuente explícita.",
            "La lectura mínima genérica ('Clasificación', atributo CLASIF del producto 2020) acredita procedencia/contexto pero no resuelve el objeto clasificado exigido por el criterio.",
            "No crear concepto tautológico para bajar el conteo de pendientes.",
        ],
        "refs_auditorias": [
            "cotejo coordinador: mismatch descripcion_original CLASIF ('Clasificación' con tilde)",
            "dictamen auditor-otros: 3 defectos (tilde; exclusividad incl. TRIMESTRE; listo SHA)",
            "decisión integrador: NO promover CLASIF",
        ],
    }
    cl["evidencia_faltante"] = ("Documento del publicador que fije el objeto clasificado por CLASIF "
        "(qué clasifica: tipo de asentamiento u otro) y su lista cerrada de valores, aplicable a la fila "
        "(conjunto+diccionario+fila+huella citados); o diccionario corregido / fe de erratas; o evidencia "
        "primaria inequívoca vinculada explícitamente a la definición. No localizado en fuentes examinadas "
        "(portal CKAN con Fuentes extras a nivel de conjunto; diccionarios nacional y local describen CLASIF solo "
        "como 'Clasificación'/'Clasificacion'; R6). En manos del publicador según R6; la búsqueda negativa "
        "acotada no prueba exclusividad ni capacidad única: vale cualquier evidencia primaria inequívoca "
        "vinculada a la fila, venga de la fuente que venga.")
    cl["limites"] = [
        "C1 (objeto sin resolver): ninguna fuente examinada declara qué clasifica CLASIF; 'tipo de asentamiento' no tiene fuente explícita y no se adopta.",
        "C2 (valores observados, sin catálogo): los 38 valores nacionales y los 7+'-' de Sonora son conteos observados en datos, no un catálogo publicado; no se adoptan códigos INEGI 1-43; '-' = nulo declarado (obligatoriedad: No), no un tipo.",
        "C3 (sin joins ni identidad de catálogos): la identidad de valores del subset Sonora (2129 filas) es compatibilidad documental, no autoriza joins por CLASIF ni fusión/identidad entre el recurso local y el producto nacional.",
        "C4 (vínculo a nivel conjunto): la declaración del publicador (Fuentes extras CKAN) no cita fila+huella; no suple el documento exacto faltante.",
        "No se equipara localidad/AGEB con colonia: toda la evidencia es de producto a nivel colonia (IMUC_2020).",
        "El RAR del programa de cálculo no fue examinado (sin extractor): no aporta ni resta.",
    ]
    ent["propuestas_respaldadas"] = 0
    ent["siguen_pendientes"] = 5
    ent["resumen_investigacion"] += (" Decisión integrador tras 2 auditorías (2026-10-24): CLASIF NO se promueve "
        "y vuelve a sigue_pendiente; la propuesta original se conserva íntegra en historial_propuesta_rechazada con "
        "motivos y refs. Se conserva todo el avance documental (identidad 2129x28 del subset Sonora, 38 valores "
        "como OBSERVADOS sin catálogo) y se corrige el conteo nacional (74226 válidas + 1 fila vacía). "
        "0 propuestas / 5 pendientes.")
    p.write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
    print("integrador aplicado: CLASIF sigue_pendiente, 0/5")


def nota_tecnica() -> None:
    import json as _json
    pdf = EV / "conapo-nota-tecnica-IMUC_2020.pdf"
    if pdf.exists() and pdf.stat().st_size > 100000:
        e = {"archivo": pdf.name, "url": "https://www.gob.mx/cms/uploads/attachment/file/714573/Nota_t_cnica_IMUC_2020.pdf",
             "http": 200, "bytes": pdf.stat().st_size, "sha256": sha256(pdf),
             "fecha_consulta_utc": "2026-10-24", "nota": "descarga previa misma ronda"}
    else:
        e = descargar("https://www.gob.mx/cms/uploads/attachment/file/714573/Nota_t_cnica_IMUC_2020.pdf",
                      "conapo-nota-tecnica-IMUC_2020.pdf")
    safe = lambda s: str(s).encode("ascii", "replace").decode()
    print(safe(f'{e.get("http")} {e.get("bytes")} {(e.get("sha256") or "")[:16]}'))
    raw = pdf.read_bytes()
    print("magia:", raw[:8])
    from pypdf import PdfReader
    r = PdfReader(pdf)
    print("paginas:", len(r.pages))
    full = []
    for i, pg in enumerate(r.pages):
        full.append((i + 1, pg.extract_text() or ""))
    hits = []
    for num, t in full:
        for kw in ("CLASIF", "clasificaci", "asentamiento"):
            if kw.lower() in t.lower():
                for ln in t.splitlines():
                    if kw.lower() in ln.lower():
                        hits.append({"pag": num, "kw": kw, "linea": ln.strip()[:200]})
                        break
    print("hits:", len(hits))
    for h in hits:
        print(safe(f'  p{h["pag"]} [{h["kw"]}] {h["linea"][:120]}'))
    _json.dump(hits, (EV / "nota-tecnica-hits.json").open("w", encoding="utf-8"),
               indent=1, ensure_ascii=False)
    _json.dump([e], (EV / "http-log-ronda2d.json").open("w", encoding="utf-8"),
               indent=1, ensure_ascii=False)
    pag4 = [t for n, t in full if n == 4][0]
    (EV / "nota-tecnica-p4.txt").write_text(pag4, encoding="utf-8")
    print("p4 guardada, caracteres:", len(pag4))


def cierre() -> None:
    import json as _json
    p = BASE / "entrega.json"
    ent = _json.loads(p.read_text(encoding="utf-8"))
    dec = {d["definicion_iri"]: d for d in ent["decisiones"]}
    cl = dec["https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5"]
    cl["evidencia"] += [
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/calculo-extraido/Indice_de_marginacion_urbana_por_colonia_2020.txt",
         "sha256": sha256(EV / "calculo-extraido/Indice_de_marginacion_urbana_por_colonia_2020.txt"),
         "localizador": "líneas 42-43 (lectura IMUC_2020 + rbind), 59-69 (DP2 sobre columnas 15:25), 104 (enlace nota metodológica); sin mención a CLASIF",
         "afirmacion_soportada": "El programa oficial lee las hojas IMUC_2020, calcula el índice solo con columnas 15:25 y arrastra CLASIF (1:25) sin definirla; remite a la nota metodológica."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-nota-tecnica-IMUC_2020.pdf",
         "sha256": "7143fe571176450ff839af719e2b6a6354f5f6f11bd296841e5d9f05ce3f8a26",
         "localizador": "p4, nota 10 al pie: 'Los atributos seleccionados para generar una capa simplificada de colonias fueron: clave y nombre de municipio, clasificación de la colonia y código postal'",
         "afirmacion_soportada": "Única mención (1 en 18 pp.): 'clasificación de la colonia' como atributo de la capa simplificada; el token CLASIF aparece 0 veces y 'tipo de asentamiento' 0 veces: sin definición explícita del objeto."},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/nota-tecnica-p4.txt",
         "sha256": sha256(EV / "nota-tecnica-p4.txt"),
         "localizador": "p4 íntegra (nota 10)",
         "afirmacion_soportada": "Transcripción citable del contexto: capa simplificada de colonias por disolución de polígonos; atributo listado sin definición."},
    ]
    for n in ent["busquedas_negativas_limitadas"]:
        if n["id"] == "NEG-DIV-06":
            n["alcance"] = ("SUPERADA 2026-10-24 con tar.exe de Windows (libarchive; sin instalar nada): el RAR "
                "lista 1 entrada 'Indice_de_marginacion_urbana_por_colonia_2020.txt' (nombre seguro, sin rutas); "
                "extraído en evidencia/calculo-extraido/ (9031 bytes). Sin puentes ni instalaciones.")
    ent["busquedas_negativas_limitadas"] += [
        {"id": "NEG-DIV-07", "fecha_utc": "2026-10-24",
         "alcance": "Nota técnica IMUC 2020 (18 pp., sha 7143fe57…): 1 mención a 'clasificación de la colonia' (atributo de capa, nota 10, p4); 0 menciones al token CLASIF y 0 a 'tipo de asentamiento'. Acredita procedencia del atributo, no su objeto: insuficiente para promover (decisión integrador firme). Acotado a este documento."},
    ]
    ent["fuentes"] += [
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/calculo-extraido/Indice_de_marginacion_urbana_por_colonia_2020.txt",
         "sha256": sha256(EV / "calculo-extraido/Indice_de_marginacion_urbana_por_colonia_2020.txt"),
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web_extraida",
         "contenido": "Script R oficial del cálculo IMUC 2020 (extraído del RAR con tar.exe; 9031 bytes).",
         "localizador": "ver evidencia CLASIF"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/conapo-nota-tecnica-IMUC_2020.pdf",
         "url": "https://www.gob.mx/cms/uploads/attachment/file/714573/Nota_t_cnica_IMUC_2020.pdf",
         "sha256": "7143fe571176450ff839af719e2b6a6354f5f6f11bd296841e5d9f05ce3f8a26",
         "fecha_consulta": "2026-10-24", "tipo": "nueva_web",
         "contenido": "Nota técnica IMUC 2020 (18 pp., %PDF-1.5): 1 mención a 'clasificación de la colonia', sin definición del objeto.",
         "localizador": "p4 nota 10; conteos 0/0 de CLASIF/'tipo de asentamiento'"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/nota-tecnica-p4.txt",
         "sha256": sha256(EV / "nota-tecnica-p4.txt"),
         "fecha_consulta": "2026-10-24", "tipo": "nota_analisis",
         "contenido": "Transcripción de p4 de la nota técnica (contexto de la capa simplificada).",
         "localizador": "p4 íntegra"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/nota-tecnica-hits.json",
         "sha256": sha256(EV / "nota-tecnica-hits.json"),
         "fecha_consulta": "2026-10-24", "tipo": "log_generado",
         "contenido": "Líneas con CLASIF/clasificaci/asentamiento por página (6 hits).",
         "localizador": "entradas por hit"},
        {"ruta": "propuestas/investigacion-post-r6/diversos/evidencia/http-log-ronda2d.json",
         "sha256": sha256(EV / "http-log-ronda2d.json"),
         "fecha_consulta": "2026-10-24", "tipo": "log_generado",
         "contenido": "Registro de descarga de la nota técnica.",
         "localizador": "entrada única"},
    ]
    ent["resumen_investigacion"] += (" Cierre RAR/nota (2026-10-24): tar.exe listó y extrajo el RAR (1 entrada segura) "
        "en evidencia/calculo-extraido/; el script arrastra CLASIF sin definirla y remite a la nota técnica IMUC 2020, "
        "que solo menciona 'clasificación de la colonia' como atributo de capa (0 menciones a CLASIF/'tipo de "
        "asentamiento'): sin definición explícita, la decisión de NO promover queda firme; 0/5.")
    p.write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
    print("cierre aplicado")


def congelar() -> None:
    import json as _json
    p = BASE / "entrega.json"
    ent = _json.loads(p.read_text(encoding="utf-8"))
    dec = {d["definicion_iri"]: d for d in ent["decisiones"]}
    cl = dec["https://example.org/mex-ontologi/definition/67156807-2013-4117-9ca9-394aea647127%2F5"]
    assert cl["estado"] == "sigue_pendiente", cl["estado"]
    assert "significado_propuesto" not in cl, "significado activo residual"
    viejo = cl["motivo"]
    assert viejo.startswith("Propuesta respaldada"), "motivo ya corregido?"
    cl.setdefault("historial_propuesta_rechazada", {})["motivo_propuesta_original"] = viejo
    cl["motivo"] = ("Sigue pendiente: identidad documental confirmada pero brecha de significado abierta. "
        "Confirmado: el archivo local (hoja IMC_2020, 2129 filas, 28 columnas) coincide en valores con el subset "
        "Sonora del producto nacional IMC_2020 ed. 2020; el diccionario local es espejo del nacional (28 variables, "
        "CLASIF='Clasificación' en ambos); el script oficial arrastra CLASIF sin definirla; la nota técnica solo "
        "lista 'clasificación de la colonia' como atributo de capa (0 menciones a CLASIF/'tipo de asentamiento'). "
        "Brecha: ninguna fuente declara el objeto clasificado; 'tipo de asentamiento' carece de fuente explícita. "
        "Falta el documento exacto citado en evidencia_faltante; límites C1-C4 vigentes.")
    ent["resumen_investigacion"] = ent["resumen_investigacion"].replace(
        "CLASIF pasa a propuesta_respaldada (opción 3) con insumos en staging/clasif.json.",
        "CLASIF llegó a propuesta_respaldada (opción 3) en ronda 2 y fue REVERTIDA por el integrador tras 2 auditorías (ver historial_propuesta_rechazada); staging/clasif.json = rechazada/no_integrar.")
    assert "pasa a propuesta_respaldada" not in ent["resumen_investigacion"]
    p.write_text(_json.dumps(ent, indent=1, ensure_ascii=False), encoding="utf-8")
    print("congelado: motivo activo coherente con sigue_pendiente")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "hashes"
    if mode == "inspeccionar":
        inspeccionar()
    elif mode == "verificar":
        verificar()
    elif mode == "ronda2":
        ronda2()
    elif mode == "examinar":
        examinar()
    elif mode == "dbf":
        dbf_campos()
    elif mode == "dbfval":
        dbf_clasif()
    elif mode == "dbfson":
        dbf_sonora()
    elif mode == "xlsxnac":
        xlsx_nacional()
    elif mode == "xlsxson":
        xlsx_sonora()
    elif mode == "ronda2b":
        ronda2b()
    elif mode == "xlsxloc":
        xlsx_local()
    elif mode == "ronda2c":
        ronda2c()
    elif mode == "ronda2fin":
        ronda2fin()
    elif mode == "cotejar":
        cotejar()
    elif mode == "defectos":
        defectos()
    elif mode == "conteo":
        xlsx_conteo()
    elif mode == "integrador":
        integrador()
    elif mode == "nota":
        nota_tecnica()
    elif mode == "cierre":
        cierre()
    elif mode == "congelar":
        congelar()
    else:
        hashes()
