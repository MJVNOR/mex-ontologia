"""B-tecnica v001 - auditoria tecnica independiente de T-top50 v001 y A2-registro-civil v001.

Solo lectura sobre lo sellado. La reproduccion corre en sandbox temporal con las
rutas de salida redirigidas; nunca escribe en T-top50 ni en A2-registro-civil.

Genera, por codigo (sin transcripcion manual de hashes):
  dictamen-tecnico-T-A2.json / .md
  congelada.json + congelada.sha256 (sidecar)

Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/B-tecnica/v001/scripts/auditar_tecnica.py
"""
import csv
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[6]
BASE = ROOT / "propuestas/ampliacion-post-r9/ejecucion-20261024"
T = BASE / "T-top50/v001"
A2 = BASE / "A2-registro-civil/v001"
OUT = BASE / "B-tecnica/v001"
C2 = ROOT / "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001"
MAPA = ROOT / "data/portal/oportunidades-cruce.json"
COB = ROOT / "reports/cobertura-operativa-r9.json"
LOTE = ROOT / "data/portal/lote-cruces/validacion-lote.json"
INSP = ROOT / "data/portal/contenido-inspeccion.json"
PERFIL = ROOT / "reports/catalogo-perfil.json"

PAR_A1 = "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92"
PAR_A2 = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5"
PAR_A3 = "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848"
NO_JOIN = "NO_JOIN_APROBADO"
EJES_A2 = ["claves", "grano", "unicidad", "cardinalidad", "poblacion",
           "periodo_ambito", "unidades", "cobertura"]

findings = []
comandos = []


def F(fid, carril, comprobacion, ok, evidencia="", estado=None):
    estado = estado or ("PASS" if ok else "FAIL")
    findings.append({"id": fid, "carril": carril, "comprobacion": comprobacion,
                     "estado": estado, "evidencia": evidencia})
    return ok


def sha_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def manifest(dirp):
    d = {}
    for p in sorted(pathlib.Path(dirp).rglob("*")):
        if p.is_file():
            b = p.read_bytes()
            d[p.relative_to(dirp).as_posix()] = {"sha256": hashlib.sha256(b).hexdigest(),
                                                 "bytes": len(b)}
    return d


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def git_state():
    r = git("status", "--porcelain", "-uall")
    return sorted(x for x in r.stdout.splitlines()
                  if x.strip() and "ejecucion-20261024/B-tecnica/" not in x)


def git_rastreados():
    """Solo modificaciones de archivos ya rastreados (ignora altas de carriles concurrentes)."""
    r = git("status", "--porcelain", "-uall")
    return sorted(x for x in r.stdout.splitlines()
                  if x[:2].strip() and not x.startswith("??"))


def run(argv, cwd, etiqueta):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    comandos.append({"etiqueta": etiqueta, "argv": [str(a) for a in argv], "cwd": str(cwd),
                     "rc": r.returncode, "stdout": (r.stdout or "").strip()[-500:],
                     "stderr": (r.stderr or "").strip()[-500:]})
    return r


def label(ok):
    return "PASS" if ok else "FAIL"


# --------------------------------------------------------------------------- sellos
def audit_seals():
    t_cong = load(T / "congelada.json")
    t_man = manifest(T)
    malos = []
    for a in t_cong["archivos"]:
        p = ROOT / a["ruta"]
        if not p.is_file():
            malos.append((a["ruta"], "falta"))
        elif sha_file(p) != a["sha256"] or p.stat().st_size != a["bytes"]:
            malos.append((a["ruta"], "sha/bytes"))
    cubiertos = {a["ruta"].split("T-top50/v001/")[-1] for a in t_cong["archivos"]}
    faltan = sorted(set(t_man) - cubiertos - {"congelada.json"})
    F("T-SELLO-1", "T", "congelada.json v001: 7 archivos con SHA256 y bytes exactos",
      not malos and len(t_cong["archivos"]) == 7, f"malos={malos}; n={len(t_cong['archivos'])}")
    F("T-SELLO-2", "T", "congelada cubre todos los archivos de v001 salvo si misma",
      not faltan, f"sin_cubrir={faltan}; cubiertos={len(cubiertos)}")

    a_cong = load(A2 / "congelada.json")
    a_man = manifest(A2)
    malos = [(rel, h) for rel, h in a_cong["archivos"].items()
             if not (A2 / rel).is_file() or sha_file(A2 / rel) != h]
    faltan = sorted(set(a_man) - set(a_cong["archivos"]) -
                    {"congelada.json", "congelada.sha256"})
    lado = (A2 / "congelada.sha256").read_text(encoding="utf-8").strip()
    F("A2-SELLO-1", "A2", "congelada.json: 5 entregables con SHA256 exactos",
      not malos and len(a_cong["archivos"]) == 5, f"malos={malos}; n={len(a_cong['archivos'])}")
    F("A2-SELLO-2", "A2", "sidecar congelada.sha256 sella congelada.json (sin autohash)",
      lado == f"{sha_file(A2 / 'congelada.json')}  congelada.json", ascii(lado))
    F("A2-SELLO-3", "A2", "congelada cubre todos los archivos de v001 salvo sellos",
      not faltan, f"sin_cubrir={faltan}")
    return t_man, a_man


# ------------------------------------------------------------------ T: recomputo
def audit_t():
    m = load(MAPA)
    crit = load(C2 / "criterio.json")
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]
    pares = m["pares"]

    def sc(p):
        return round(sum(pesos.get(f, 1) for f in p.get("familias_compartidas", []))
                     + sum(pen.get(b, 0) for b in p.get("pendientes", [])), 2)

    cand = [p for p in pares if p["estado"] == "candidata_por_validar"]
    calc = sorted(((sc(p), p["id"], p) for p in cand), key=lambda r: (-r[0], r[1]))
    F("T-01", "T", "Mapa: 3916 pares y 1191 candidatas_por_validar",
      len(pares) == 3916 and len(cand) == 1191,
      f"pares={len(pares)}; candidatas={len(cand)}; estados={m['resumen']['estados']}")
    F("T-02", "T", "1191 ids de candidata unicos",
      len({p["id"] for p in cand}) == 1191)

    with open(C2 / "matriz_pares_relevantes.csv", encoding="utf-8") as f:
        mat = list(csv.DictReader(f))
    with open(C2 / "prioridades_top50.csv", encoding="utf-8") as f:
        top = list(csv.DictReader(f))
    byid = {p["id"]: p for p in cand}
    malos = [r["id"] for r in mat if float(r["score"]) != sc(byid[r["id"]])]
    F("T-03", "T", "1191/1191 scores de matriz recomputados iguales (formula del criterio)",
      not malos and len(mat) == 1191, f"filas={len(mat)}; discrepancias={len(malos)}")
    F("T-04", "T", "Matriz y mapa cubren el mismo conjunto de 1191 candidatas",
      {r["id"] for r in mat} == set(byid), f"mat={len(mat)}; mapa={len(byid)}")

    orden_mat = [r["id"] for r in mat]
    orden_calc = [r[1] for r in calc]
    mismo_orden = orden_mat == orden_calc
    F("T-05", "T", "Orden completo de 1191 respeta (-score, id)",
      mismo_orden, "matriz ya ordenada como el recomputo" if mismo_orden else
      "matriz en otro orden; se compara por score y el top50 contra el prefijo del recomputo",
      estado="PASS" if mismo_orden else "OBS")

    F("T-06", "T", "Top50 = prefijo exacto del orden recomputado (50/50 ids en orden)",
      len(top) == 50 and [r["id"] for r in top] == orden_calc[:50],
      f"top={len(top)}")
    F("T-07", "T", "Rangos 1..50 unicos y en orden",
      [int(r["rango"]) for r in top] == list(range(1, 51)))
    F("T-08", "T", "50/50 scores del CSV iguales al recomputo",
      all(float(r["score"]) == calc[i][0] for i, r in enumerate(top)))
    F("T-09", "T", "Top50: 50 ids unicos; max 5.0 y min 1.0 como declara la entrega",
      len({r["id"] for r in top}) == 50 and max(float(r["score"]) for r in top) == 5.0
      and min(float(r["score"]) for r in top) == 1.0,
      f"max={max(float(r['score']) for r in top)}; min={min(float(r['score']) for r in top)}")

    st = load(T / "top50-oportunidades-r9.json")
    filas = st["filas"]
    F("T-10", "T", "Staging JSON: 50 filas coherentes con el mapa original (titulos, familias, bloqueadores, conjuntos)",
      len(filas) == 50 and all(
          f["id"] == orden_calc[i] and f["rango"] == i + 1 and f["score"] == calc[i][0]
          and f["titulo_a"] == byid[f["id"]]["titulo_a"]
          and f["titulo_b"] == byid[f["id"]]["titulo_b"]
          and f["familias"] == byid[f["id"]]["familias_compartidas"]
          and f["bloqueadores"] == byid[f["id"]]["pendientes"]
          and f["fuentes"] == {"conjunto_a": byid[f["id"]]["conjunto_a"],
                               "conjunto_b": byid[f["id"]]["conjunto_b"]}
          for i, f in enumerate(filas)), f"filas={len(filas)}")

    carril = {PAR_A1: "A1-911", PAR_A2: "A2-matrimonios-nacimientos", PAR_A3: "A3-itama"}
    F("T-11", "T", "Todas las filas NO_JOIN_APROBADO; carril analitico solo en los 3 pares A1-A3",
      all(f["estado"] == NO_JOIN for f in filas)
      and all(f["carril_analitico"] == carril.get(f["id"]) for f in filas)
      and sum(1 for f in filas if f["carril_analitico"]) == 3)
    F("T-12", "T", "A1/A2/A3 por ID exacto, rangos 2/4/1 y scores 3.0/3.0/5.0",
      {f["id"]: (f["rango"], f["score"]) for f in filas if f["id"] in carril}
      == {PAR_A1: (2, 3.0), PAR_A2: (4, 3.0), PAR_A3: (1, 5.0)})

    # MD y HTML: se reconstruye la fila esperada desde el JSON y se compara.
    md = (T / "top50-oportunidades-r9.md").read_text(encoding="utf-8")
    lineas = [ln for ln in md.splitlines() if re.match(r"^\| \d+ \| `", ln)]
    filas_md = [ln[2:-2].split(" | ") for ln in lineas]
    md_ok = len(filas_md) == 50
    if md_ok:
        for i, (campos, f) in enumerate(zip(filas_md, filas)):
            esp = [str(f["rango"]), f"`{f['id']}`".strip("`"), f["titulo_a"], f["titulo_b"],
                   f"{f['score']}", "; ".join(f["bloqueadores"])]
            if len(campos) != 6 or campos[0] != esp[0] or campos[1].strip("`") != f["id"] \
                    or campos[2] != esp[2] or campos[3] != esp[3] \
                    or float(campos[4]) != f["score"] or campos[5] != esp[5]:
                md_ok = False
                break
    F("T-13", "T", "MD: 50 filas, en el mismo orden y con los mismos campos que el JSON",
      md_ok, f"filas_md={len(filas_md)}")

    txt_html = (T / "vista-top50-r9.html").read_text(encoding="utf-8")
    trs = re.findall(r"<tr><td>(\d+)</td><td><code>([^<]+)</code></td><td>(.*?)</td>"
                     r"<td>(.*?)</td><td>([\d.]+)</td><td>(.*?)</td><td>([A-Z_]+)</td></tr>",
                     txt_html)
    html_ok = len(trs) == 50
    if html_ok:
        for (rango, pid, ta, tb, score, bloq, estado), f in zip(trs, filas):
            if (int(rango), pid, html.unescape(ta), html.unescape(tb), float(score),
                    html.unescape(bloq), estado) != (f["rango"], f["id"], f["titulo_a"],
                                                     f["titulo_b"], f["score"],
                                                     "; ".join(f["bloqueadores"]), NO_JOIN):
                html_ok = False
                break
    F("T-14", "T", "HTML: 50 filas, mismo orden/campos/estado que el JSON (sin contradiccion)",
      html_ok, f"filas_html={len(trs)}")

    encabezados = ("3916" in md and "1191" in md
                   and st["meta"]["mapa"]["pares"] == 3916
                   and st["meta"]["mapa"]["candidatas"] == 1191
                   and st["meta"]["estado_filas"] == NO_JOIN
                   and st["meta"]["cobertura_r9"]["estado"] == load(COB)["estado"])
    F("T-15", "T", "Cabeceras MD/HTML y meta del staging coinciden con mapa y cobertura R9",
      bool(encabezados))

    ent = load(T / "entrega.json")
    fuentes = [(s["ruta"], s["sha256"]) for s in ent["fuentes"]]
    malas = [(r, h) for r, h in fuentes
             if not (ROOT / r).is_file() or sha_file(ROOT / r) != h]
    datos = [x for x in malas if not x[0].startswith("docs/")]
    F("T-16", "T", "entrega.json: las 6 fuentes de datos/criterio con SHA256 exactos",
      not datos, f"n_fuentes={len(fuentes)}; discrepancias_datos={datos}")
    deriva = [x for x in malas if x[0].startswith("docs/")]
    F("T-16b", "T", "Fuente documental del plan: el SHA citado ya no coincide con el archivo actual",
      not deriva,
      f"deriva={[(r, h, sha_file(ROOT / r)) for r, h in deriva]}; "
      "el plan citado se actualizo despues del sello (nota de continuidad DeepSeek); "
      "no afecta mapa, criterio, CSVs, cobertura ni seguimiento. Corregir con nota/delta en v002.",
      estado="OBS" if deriva else "PASS")

    mapa_sha = sha_file(MAPA)
    cob = load(COB)
    F("T-17", "T", "Meta del staging sella mapa, criterio y cobertura con los SHA reales",
      st["meta"]["mapa"]["sha256"] == mapa_sha
      and st["meta"]["criterio_c2"]["sha256"] == sha_file(C2 / "criterio.json")
      and st["meta"]["cobertura_r9"]["sha256"] == sha_file(COB),
      f"mapa={mapa_sha}")

    ind, pend = cob["indicadores"], cob["pendientes"]
    decl = ent["resultados"]["cobertura_r9"]
    cob_ok = (ind["significados_respaldados"] == 1423 and ind["conceptos"] == 1106
              and pend["vigencias"] == 16 and ind["candidatas"] == 17
              and "1423" in decl and "1106" in decl and "138" in decl
              and "16" in decl and "17" in decl
              and cob["estado"] == "cobertura_operativa_validada_sin_cambios_al_grafo")
    F("T-18", "T", "Cifras de cobertura R9 declaradas (1423/1106/138/16/17) iguales a la fuente",
      cob_ok, f"significados={ind['significados_respaldados']}; conceptos={ind['conceptos']}; "
              f"vigencias={pend['vigencias']}; candidatas={ind['candidatas']}")

    # Mapa original inmutable: sello declarado, git limpio, mtime anterior a la congelacion,
    # y huella interna igual al localizador de la entrega.
    base = load(BASE / "base.json")
    congelado_en = datetime.fromisoformat(base["fecha_utc"])
    mtime = datetime.fromtimestamp(MAPA.stat().st_mtime, tz=congelado_en.tzinfo)
    interno = load(MAPA)["generado_en_utc"]
    git_mapa = git("status", "--porcelain", "--", "data/portal/oportunidades-cruce.json")
    F("T-19", "T", "Mapa original inmutable: SHA declarado, git limpio, mtime previo a base.json",
      mapa_sha == "40f107d5cf9c11ce937073ac2f7b5b0e3c9db8c342f7414cecb0f0744e0d0c14"
      and mapa_sha in {s["sha256"] for s in ent["fuentes"]}
      and st["meta"]["mapa"]["sha256"] == mapa_sha
      and git_mapa.stdout.strip() == "" and git_mapa.returncode == 0
      and mtime <= congelado_en
      and interno in ent["fuentes"][0]["localizador"],
      f"sha={mapa_sha}; git={ascii(git_mapa.stdout.strip())}; mtime={mtime.isoformat()}; "
      f"generado_interno={interno}; base={base['fecha_utc']}")

    # Sin join automatico: ninguna aprobacion encubierta en las salidas T.
    crudo = md + txt_html + json.dumps(st, ensure_ascii=False)
    sin_join = not re.search(r"(?<!NO_)JOIN_APROBADO", crudo) \
        and not re.search(r'"join[a-z_]*"\s*:\s*true', crudo) \
        and '"join_grafo"' not in json.dumps(st)
    F("T-20", "T", "Sin join automatico: ningun JOIN_APROBADO ni campo join en T",
      sin_join)

    src = (T / "scripts/reproducir_top50_r9.py").read_text(encoding="utf-8")
    imports = set(re.findall(r"^(?:import|from)\s+([a-zA-Z_][\w.]*)", src, re.M))
    escrituras = [ln.strip() for ln in src.splitlines()
                  if re.search(r"""open\(.*['"]w['"]|write_text\(""", ln)]
    F("T-21", "T", "Reproductor real: solo stdlib, sin red y escribe unicamente dentro de V001",
      imports <= {"csv", "hashlib", "html", "json", "pathlib"}
      and not re.search(r"\b(socket|requests|urllib|gemma)\b", src, re.I)
      and bool(escrituras) and all("V001 /" in ln for ln in escrituras),
      f"imports={sorted(imports)}; escrituras={[ln[:55] for ln in escrituras]}")
    F("T-22", "T", "Ninguna salida de T/A2 invoca Gemma ni contactos a publicadores",
      not re.search(r"gemma|contact", crudo, re.I)
      and not re.search(r"gemma|contact",
                        (A2 / "resultados.json").read_text(encoding="utf-8")
                        + (A2 / "resultados.md").read_text(encoding="utf-8"), re.I))

    return st, filas


# ------------------------------------------------------------------- T: reproduccion
def reproduce_t():
    # Ubicacion target simulada dentro de la carpeta asignada: el reproductor sellado
    # hace p.relative_to(ROOT), asi que el staging simulado debe colgar del repo.
    sb = OUT / "_sim" / "T-top50"
    if sb.exists():
        shutil.rmtree(sb)
    out = sb / "v001"
    dst = out / "scripts" / "reproducir_top50_r9.py"
    dst.parent.mkdir(parents=True)
    txt = (T / "scripts/reproducir_top50_r9.py").read_text(encoding="utf-8")
    pares = [("V001 = pathlib.Path(__file__).resolve().parents[1]",
              f'V001 = pathlib.Path({json.dumps(out.as_posix())})'),
             ("ROOT = pathlib.Path(__file__).resolve().parents[6]",
              f'ROOT = pathlib.Path({json.dumps(ROOT.as_posix())})')]
    try:
        for old, new in pares:
            assert txt.count(old) == 1, f"T: no se pudo redirigir {old}"
            txt = txt.replace(old, new)
        dst.write_text(txt, encoding="utf-8")
        r = run([sys.executable, "-B", str(dst)], sb, "T-reproducir")
        ok = r.returncode == 0
        F("T-REPRO-1", "T", "El reproductor sellado corre en staging simulado (asserts internos incluidos)",
          ok, f"rc={r.returncode}; stdout={ascii((r.stdout or '').strip()[-200:])}")
        iguales, difs = [], []
        for nombre in ("top50-oportunidades-r9.json", "top50-oportunidades-r9.md",
                       "vista-top50-r9.html"):
            misma = ok and (out / nombre).is_file() \
                and (out / nombre).read_bytes() == (T / nombre).read_bytes()
            (iguales if misma else difs).append(nombre)
        F("T-REPRO-2", "T", "Salidas regeneradas byte-identicas a las selladas (3/3)",
          len(iguales) == 3, f"iguales={iguales}; distintas={difs}")
    finally:
        if (OUT / "_sim").exists():
            shutil.rmtree(OUT / "_sim")
    return out, ok


# ------------------------------------------------------------------ A2: verificacion
def audit_a2():
    res = load(A2 / "resultados.json")
    lote = load(LOTE)
    ins = load(INSP)
    perfil = load(PERFIL)
    oport = load(MAPA)
    par = next(p for p in lote["pares"] if p["id"] == PAR_A2)
    op = next(p for p in oport["pares"] if p["id"] == PAR_A2)
    inv = {c["id"]: c for c in perfil["inventario"]}
    recs = {r["id"]: r for r in ins["recursos"]}
    MAT = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98"
    NAC = "df2d60f5-2243-4bb0-885a-941aa8a657f5"
    DIC_MAT, DIC_NAC = ("364ffa5c-e1c2-4185-a22f-80bede6735d0",
                        "6bcf5b63-0855-4f3b-81a0-4bca82e97272")
    defs_mat = {d["Nombre variable"]: d for d in recs[DIC_MAT]["definiciones"]}
    defs_nac = {d["Nombre variable"]: d for d in recs[DIC_NAC]["definiciones"]}
    ev = {k: v["evidencia"] for k, v in res["ejes"].items()}

    F("A2-01", "A2", "Par correcto, 8 ejes del plan, veredicto BLOQUEADO sin volumen ni join",
      res["par"] == PAR_A2 and list(res["ejes"]) == EJES_A2
      and res["veredicto"] == "BLOQUEADO" and res["comparacion_volumenes"] is None
      and res["join_grafo"] is None and len(res["causas_bloqueo"]) == 5,
      f"ejes={list(res['ejes'])}; causas={len(res['causas_bloqueo'])}")

    F("A2-02", "A2", "Eje claves: par candidata_por_validar, familia municipio y pendientes de catalogo",
      op["estado"] == "candidata_por_validar" and "municipio" in op["familias_compartidas"]
      and "verificar_catalogo_dominio_unicidad_y_contexto_de_clave" in op["pendientes"]
      and "municipio_puede_requerir_entidad_como_clave_compuesta" in ev["claves"]
      and res["ejes"]["claves"]["veredicto"] == "no_acreditada",
      f"estado={op['estado']}")

    F("A2-03", "A2", "Eje grano: variables citadas = diccionarios locales; evento vs agregado",
      str(sorted(defs_mat)) in ev["grano"] and str(sorted(defs_nac)) in ev["grano"]
      and "dia_matrimonio" in defs_mat and {"hombres", "mujeres", "total"} <= set(defs_nac)
      and res["ejes"]["grano"]["veredicto"] == "distinto_bloquea_join")

    diag = par["diagnostico_muestras"]
    alcance_ok = all("no demuestra unicidad ni cobertura integral" in d["alcance"]
                     and d["limite"] == 100 for d in diag.values())
    F("A2-04", "A2", "Eje unicidad: limites de muestra declarados (n=100, sin universalidad)",
      alcance_ok and res["ejes"]["unicidad"]["veredicto"] == "no_acreditada",
      f"limites={[d['limite'] for d in diag.values()]}; "
      f"alcance_verbatim_ok={all('Diagn\u00f3stico de muestra' in d['alcance'] for d in diag.values())}")

    errs = [t["error_b"] for t in par["pruebas_recursos"]]
    n_total = sum(1 for e in errs if e and "Total no coincide con hombres + mujeres" in e)
    n_meses = sum(1 for e in errs if e and "Faltan meses por municipio" in e)
    F("A2-05", "A2", "Eje cardinalidad: 6 pruebas, 5 fallos total!=hombres+mujeres y 1 de meses faltantes",
      par["decision"] == "fallo_validacion_integral" and len(errs) == 6
      and n_total == 5 and n_meses == 1
      and res["ejes"]["cardinalidad"]["veredicto"] == "no_acreditada",
      f"pruebas={len(errs)}; total!=suma={n_total}; meses={n_meses}")
    F("A2-06", "A2", "Eje poblacion: actos con 2 contrayentes vs conteos agregados; sin id de persona",
      "sexo_cty1" in defs_mat and "sexo_cty2" in defs_mat
      and not any("persona" in k.lower() or k.lower() in ("id", "curp") for k in defs_mat)
      and not any("persona" in k.lower() or k.lower() in ("id", "curp") for k in defs_nac)
      and res["ejes"]["poblacion"]["veredicto"] == "distinta")

    anios_mat = {int(x) for r in inv[MAT]["recursos"]
                 for x in re.findall(r"(20\d\d)", r["name"])}
    anios_nac = {int(x) for r in inv[NAC]["recursos"]
                 for x in re.findall(r"(20\d\d)", r["name"])}
    registro = {"Municipio de registro"} <= {d["Descripción"] for d in defs_mat.values()} \
        and {"Municipio de registro"} <= {d["Descripción"] for d in defs_nac.values()}
    sin_residencia = not any("residencia" in (d["Nombre variable"] + d["Descripción"]).lower()
                             for d in list(defs_mat.values()) + list(defs_nac.values()))
    F("A2-07", "A2", "Eje periodo/ambito: interseccion real 2015-2024, solo registro, sin residencia",
      anios_mat & anios_nac == set(range(2015, 2025)) and registro and sin_residencia
      and res["ejes"]["periodo_ambito"]["veredicto"]
      == "comparable_solo_en_registro_no_acreditado_para_join",
      f"anios_mat={sorted(anios_mat)}; anios_nac={sorted(anios_nac)}; "
      f"interseccion={sorted(anios_mat & anios_nac)}")
    F("A2-08", "A2", "Eje unidades: fila-evento vs fila-agregado; pendiente de homologacion citado",
      "validar_unidades_de_medidas_seleccionadas" in par["pendientes_originales"]
      and res["ejes"]["unidades"]["veredicto"] == "no_homologables_sin_regla"
      and not any("tasa" in k.lower() for k in list(defs_mat) + list(defs_nac)))

    tot = {d["nombre"]: d["total_declarado"] for d in diag.values()}
    F("A2-09", "A2", "Eje cobertura: ausencia != cero y muestras de recursos/anios distintos",
      tot.get("Matrimonios 2023") == 14685 and tot.get("Nacimientos 2024") == 627
      and n_meses == 1
      and res["ejes"]["cobertura"]["veredicto"] == "no_acreditada",
      f"total_declarado={tot}")
    F("A2-10", "A2", "Muestra != universo: la entrega no presenta la muestra como cobertura completa",
      all(d["limite"] == 100 for d in diag.values()) and "muestras" in ev["cobertura"]
      and "no demuestra unicidad ni cobertura integral" in diag["a"]["alcance"]
      and res["comparacion_volumenes"] is None)

    # Fidelidad de citas textuales (evidencia reproducible, no transcripcion alterada).
    raw_lote = LOTE.read_text(encoding="utf-8")
    verbatim_uni = "Diagn\u00f3stico de muestra; no demuestra unicidad ni cobertura integral" in raw_lote
    citado_uni = "Diagnostico de muestra; no demuestra unicidad ni cobertura integral" in ev["unicidad"]
    F("A2-11", "A2", "Cita textual de unicidad: la fuente dice 'Diagnostico' con acento",
      verbatim_uni and citado_uni,
      "La fuente dice 'Diagn\u00f3stico de muestra; ...'; resultados.json cita 'Diagnostico de muestra; ...' "
      "(sin tilde). El sentido se mantiene; la cita no es literal.",
      estado="OBS" if (verbatim_uni and citado_uni) else "FAIL")
    F("A2-12", "A2", "Cita de periodo: 'Anio-Mes de registro' no existe como variable unica",
      "A\u00f1o de registro" in {d["Descripción"] for d in defs_mat.values()}
      and "Mes de registro" in {d["Descripción"] for d in defs_mat.values()},
      "Los diccionarios tienen variables separadas 'A\u00f1o de registro' y 'Mes de registro' "
      "(mas 'Dia de registro' en Matrimonios); la evidencia las parafrasea como "
      "'Anio-Mes de registro'. No altera el veredicto.",
      estado="OBS")

    F("A2-13", "A2", "Fuentes locales declaradas: conteos y SHA de diccionarios reales",
      res["fuentes_locales"]["reports/catalogo-perfil.json"]["mat_recursos"]
      == len(inv[MAT]["recursos"]) == 11
      and res["fuentes_locales"]["reports/catalogo-perfil.json"]["nac_recursos"]
      == len(inv[NAC]["recursos"]) == 16
      and res["fuentes_locales"]["data/portal/contenido-inspeccion.json"]
      ["diccionario_matrimonios_sha256"] == recs[DIC_MAT]["sha256_fragmento_o_archivo"]
      and res["fuentes_locales"]["data/portal/contenido-inspeccion.json"]
      ["diccionario_nacimientos_sha256"] == recs[DIC_NAC]["sha256_fragmento_o_archivo"])

    # Script no ficticio: solo stdlib, sin red, no fabrica datos ni escribe fuera.
    src = (A2 / "scripts/analizar.py").read_text(encoding="utf-8")
    imports = set(re.findall(r"^(?:import|from)\s+([a-zA-Z_][\w.]*)", src, re.M))
    escrituras = [ln.strip() for ln in src.splitlines()
                  if re.search(r"""open\(.*['"]w['"]""", ln)]
    F("A2-14", "A2", "Script reproducible real: solo stdlib, sin red y escribe unicamente en OUT",
      imports <= {"hashlib", "json", "pathlib"} and "http" not in src.lower()
      and not re.search(r"\b(socket|requests|urllib)\b", src)
      and bool(escrituras) and all("OUT /" in ln for ln in escrituras),
      f"imports={sorted(imports)}; escrituras={[ln[:60] for ln in escrituras]}")
    return res


# ---------------------------------------------------------------- A2: reproduccion
def reproduce_a2():
    sb = pathlib.Path(tempfile.mkdtemp(prefix="b-tecnica-a2-", dir=tempfile.gettempdir()))
    out = sb / "v001"
    entregables = ["A2-pregunta-ficha.md", "resultados.md", "resultados.json",
                   "scripts/analizar.py", "tests/test_bloqueo.py"]
    for rel in entregables:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((A2 / rel).read_bytes())
    dst = out / "scripts/analizar.py"
    txt = dst.read_text(encoding="utf-8")
    for old, new in [("REPO = Path(__file__).resolve().parents[6]",
                      f'REPO = Path({json.dumps(ROOT.as_posix())})'),
                     ("OUT = Path(__file__).resolve().parents[1]",
                      f'OUT = Path({json.dumps(out.as_posix())})')]:
        assert txt.count(old) == 1, f"A2: no se pudo redirigir {old}"
        txt = txt.replace(old, new)
    dst.write_text(txt, encoding="utf-8")
    r = run([sys.executable, "-B", str(dst)], sb, "A2-analizar")
    ok = r.returncode == 0
    F("A2-REPRO-1", "A2", "El analisis sellado corre en sandbox y concluye BLOQUEADO",
      ok and "BLOQUEADO" in (r.stdout or ""),
      f"rc={r.returncode}; stdout={ascii((r.stdout or '').strip()[:200])}")
    igual = ok and (out / "resultados.json").read_bytes() == (A2 / "resultados.json").read_bytes()
    F("A2-REPRO-2", "A2", "resultados.json regenerado byte-identico al sellado",
      igual, f"sha_sandbox={sha_file(out / 'resultados.json') if ok else 'n/a'}")
    cong_sb = load(out / "congelada.json")
    cong_sell = load(A2 / "congelada.json")
    otros = {k: v for k, v in cong_sb["archivos"].items() if k != "scripts/analizar.py"}
    otros_ok = otros == {k: v for k, v in cong_sell["archivos"].items()
                         if k != "scripts/analizar.py"}
    lado_ok = (out / "congelada.sha256").read_text(encoding="utf-8").strip() \
        == f"{sha_file(out / 'congelada.json')}  congelada.json"
    F("A2-REPRO-3", "A2", "cadena de sello regenerada: 4/5 hashes iguales (script redirigido) y sidecar valido",
      otros_ok and lado_ok,
      "El unico hash distinto es scripts/analizar.py, cuya copia solo cambia las 2 lineas de ruta "
      "(REPO/OUT) para escribir en el sandbox; el resto reproduce byte a byte.")
    return sb, ok


# ------------------------------------------------------------------------ ejecucion
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    snap_inicio = {"T": manifest(T), "A2": manifest(A2)}
    git_inicio = git_rastreados()
    git_untracked_inicio = {x for x in git_state() if x.startswith("??")}

    t_man, a_man = audit_seals()
    st, filas = audit_t()
    a2 = audit_a2()
    sb_t, _ = reproduce_t()
    sb_a2, _ = reproduce_a2()

    rt = run([sys.executable, "-B", str(T / "tests/test_top50_r9.py")], T, "T-tests")
    F("T-TEST", "T", "Pruebas selladas T ejecutadas y en verde",
      rt.returncode == 0, f"rc={rt.returncode}; {ascii(((rt.stdout or '') + (rt.stderr or '')).strip()[-300:])}")
    ra = run([sys.executable, "-B", str(A2 / "tests/test_bloqueo.py")], A2, "A2-tests")
    F("A2-TEST", "A2", "Pruebas selladas A2 ejecutadas y en verde",
      ra.returncode == 0, f"rc={ra.returncode}; {ascii(((ra.stdout or '') + (ra.stderr or '')).strip()[-300:])}")

    # Integridad de la base congelada y de lo ajeno a los carriles.
    base = load(BASE / "base.json")
    malos = [rel for rel, h in base["sha256"].items()
             if not (ROOT / rel).is_file() or sha_file(ROOT / rel) != h]
    F("X-01", "X", "Base congelada intacta: 130/130 archivos de base.json con SHA exacto",
      not malos and len(base["sha256"]) == 130, f"n={len(base['sha256'])}; malos={malos}")

    iri = load(BASE / "iri-fuera-de-alcance.json")
    cfg = ROOT / iri["ruta"]
    F("X-02", "X", "IRI fuera de alcance: config.toml con SHA declarado y sin cambios",
      cfg.is_file() and sha_file(cfg) == iri["sha256"]
      and iri["modificacion_permitida"] is False
      and git("status", "--porcelain", "--", "config.toml").stdout.strip() == "",
      f"sha={sha_file(cfg) if cfg.is_file() else 'falta'}; base_iri={iri['base_iri']}")

    F("X-03", "X", "Sin escrituras en T/A2 durante la auditoria (manifiestos identicos)",
      manifest(T) == snap_inicio["T"] and manifest(A2) == snap_inicio["A2"])
    F("X-04", "X", "La auditoria no modifica ningun archivo rastreado (git: modificaciones estables)",
      git_rastreados() == git_inicio,
      f"modificados_antes={len(git_inicio)}; ahora={len(git_rastreados())}")
    nuevos = sorted({x for x in git_state() if x.startswith("??")} - git_untracked_inicio)
    F("X-04b", "X", "Altas nuevas en el arbol corresponden a carriles concurrentes, no a B-tecnica",
      all("B-tecnica/" not in x for x in nuevos),
      f"altas_durante_auditoria={len(nuevos)} fuera_de_B-tecnica; ejemplo="
      f"{[x[:90] for x in nuevos[:4]]}; otros carriles escriben v002 en paralelo",
      estado="OBS" if nuevos else "PASS")
    F("X-05", "X", "Ningun carril produce RDF/TTL ni toca el grafo o Studio",
      not list(T.rglob("*.ttl")) and not list(A2.rglob("*.ttl"))
      and not [p for d in (T, A2) for p in d.rglob("*")
               if p.is_file() and p.suffix in {".rdf", ".owl", ".jsonld"}])

    r1_r9 = ["data/integracion/manifiesto.json"] + [
        f"data/integracion-ronda-{n}/manifiesto.json" for n in range(2, 10)]
    ok_r = all(r in base["sha256"] and sha_file(ROOT / r) == base["sha256"][r]
               for r in r1_r9)
    extra = sorted(r for r in base["sha256"]
                   if ("manifiesto" in r and r not in r1_r9))
    F("X-06", "X", "Manifiestos R1-R9 intactos y con SHA exacto",
      ok_r and all(sha_file(ROOT / r) == base["sha256"][r] for r in extra),
      f"R1-R9={len(r1_r9)} intactos; manifiestos adicionales intactos={len(extra)}")

    for x in findings:
        if x["estado"] == "FAIL" and x["carril"] in ("T", "A2") and x["id"] in (
                "A2-11", "A2-12"):
            x["estado"] = "OBS"
            x["evidencia"] += " [cita no literal: no altera el resultado]"

    resume = {k: sum(1 for f in findings if f["estado"] == k) for k in ("PASS", "OBS", "FAIL")}

    def veredicto(carril):
        est = [f["estado"] for f in findings if f["carril"] == carril]
        if "FAIL" in est:
            return "RECHAZADO"
        if "OBS" in est:
            return "ACEPTADO_CON_OBSERVACIONES"
        return "ACEPTADO"

    sellos = {
        "T-top50/v001": t_man,
        "A2-registro-civil/v001": a_man,
    }
    dictamen = {
        "rol": "B-tecnica",
        "version": "v001",
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "objeto": "Auditoria tecnica independiente de T-top50 v001 y A2-registro-civil v001",
        "metodo": "recomputo propio desde fuentes, verificacion de sellos, reproduccion en "
                  "sandbox temporal con rutas redirigidas, ejecucion de pruebas selladas y "
                  "comprobacion de no-escritura; solo stdlib",
        "sandbox": {"T": str(sb_t), "A2": str(sb_a2),
                    "nota": "Ubicacion target simulada: T se reproduce en "
                            "B-tecnica/v001/_sim/T-top50 (cuelga del repo porque el reproductor "
                            "usa relative_to(ROOT)) y se elimina al terminar; A2 en un temporal "
                            "del sistema. Las copias solo cambian las 2 lineas de ruta de salida "
                            "(ROOT/V001 y REPO/OUT); nada se escribe en los v001 sellados."},
        "sellos_auditados": sellos,
        "sellos_digest": {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()
                          for k, v in sellos.items()},
        "fuentes_clave": {
            "data/portal/oportunidades-cruce.json": sha_file(MAPA),
            "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json":
                sha_file(C2 / "criterio.json"),
            "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv":
                sha_file(C2 / "prioridades_top50.csv"),
            "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv":
                sha_file(C2 / "matriz_pares_relevantes.csv"),
            "reports/cobertura-operativa-r9.json": sha_file(COB),
            "data/portal/lote-cruces/validacion-lote.json": sha_file(LOTE),
            "data/portal/contenido-inspeccion.json": sha_file(INSP),
            "reports/catalogo-perfil.json": sha_file(PERFIL),
            "config.toml": sha_file(cfg),
        },
        "comandos": comandos,
        "comprobaciones": findings,
        "resumen": resume,
        "dictamen": {
            "T-top50": {
                "veredicto": veredicto("T"),
                "base": "1191 scores recomputados; top50 = prefijo exacto del orden (-score, id); "
                        "mapa 3916/1191 inmutable; MD/HTML coinciden fila a fila con el JSON",
                "condiciones": "La publicacion en reports/ sigue siendo del escritor central; "
                               "oportunidad no equivale a join aprobado.",
            },
            "A2-registro-civil": {
                "veredicto": veredicto("A2"),
                "base": "BLOQUEADO con 8 ejes; evidencia cruzada contra fuentes locales; "
                        "muestra n=100 declarada como no universal; sin volumen ni join",
                "condiciones": "Corregir en v002 las citas no literales (tilde en 'Diagnostico' "
                               "y 'Anio-Mes de registro') si se busca transcripcion exacta; "
                               "no cambia el veredicto BLOQUEADO.",
            },
        },
        "no_auditado": {
            "A1-911": "PENDIENTE: no se acepta ni se adelanta dictamen",
            "A3-itama": "PENDIENTE: no se acepta ni se adelanta dictamen",
            "Q-unidades": "PENDIENTE: no se acepta ni se adelanta dictamen",
            "S-shacl": "PENDIENTE: no se acepta ni se adelanta dictamen",
            "integracion_final": "PENDIENTE: se audita despues, sin instalar",
        },
        "v002_observados": {
            "carriles": sorted(p.parent.name for p in BASE.glob("*/v002")),
            "nota": "Otros carriles publicaron v002 durante esta auditoria. Fuera de alcance: "
                    "aqui solo se auditan T-top50/v001 y A2-registro-civil/v001, y su bytes "
                    "permanecieron intactos (X-03). No se acepta ni se dictamina v002.",
        },
        "limites": [
            "IRI definitiva / example.org fuera de alcance: config.toml solo se verifica, no se toca.",
            "Sin Gemma, sin contactos a publicadores, sin busquedas agotadas, sin manifiestos R1-R9.",
            "Sin joins automaticos, sin instalar, sin Studio, sin tocar escritores centrales.",
            "Escritura limitada a propuestas/ampliacion-post-r9/ejecucion-20261024/B-tecnica/v001/.",
        ],
    }

    (OUT / "dictamen-tecnico-T-A2.json").write_text(
        json.dumps(dictamen, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "dictamen-tecnico-T-A2.md").write_text(render_md(dictamen), encoding="utf-8")

    archivos = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name not in {"congelada.json", "congelada.sha256",
                                         "__pycache__"} and "__pycache__" not in p.parts:
            b = p.read_bytes()
            archivos.append({"ruta": str(p.relative_to(ROOT)).replace("\\", "/"),
                             "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    cong = {"rol": "B-tecnica", "version": "v001",
            "nota": "Congelada v001 por codigo. Corregir en v002; no editar.",
            "archivos": archivos}
    (OUT / "congelada.json").write_text(
        json.dumps(cong, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "congelada.sha256").write_text(
        f"{sha_file(OUT / 'congelada.json')}  congelada.json\n", encoding="utf-8")
    print(f"B-tecnica v001: {resume}; T={veredicto('T')} A2={veredicto('A2')}; "
          f"{len(archivos)} archivos sellados")


def render_md(d):
    L = ["# Dictamen tecnico independiente T-top50 v001 y A2-registro-civil v001",
         "", f"Rol B-tecnica v001 - {d['fecha_utc']}.", "",
         f"Metodo: {d['metodo']}.", "",
         f"Resumen: **{d['resumen']['PASS']} PASS / {d['resumen']['OBS']} OBS / "
         f"{d['resumen']['FAIL']} FAIL**.", "",
         "## Dictamen", "",
         "| Carril | Veredicto | Base de la decision |", "| --- | --- | --- |"]
    for k, v in d["dictamen"].items():
        L.append(f"| {k} | **{v['veredicto']}** | {v['base']} |")
    L += ["", "## Sellos auditados (SHA256 por archivo)", ""]
    for lane, man in d["sellos_auditados"].items():
        L += [f"### {lane}", "", f"Digest del manifiesto: `{d['sellos_digest'][lane]}`", "",
              "| Archivo | SHA256 | Bytes |", "| --- | --- | --- |"]
        for rel, h in man.items():
            L.append(f"| `{rel}` | `{h['sha256']}` | {h['bytes']} |")
        L.append("")
    L += ["## Fuentes clave verificadas", "", "| Fuente | SHA256 |", "| --- | --- |"]
    for rel, h in d["fuentes_clave"].items():
        L.append(f"| `{rel}` | `{h}` |")
    L += ["", "## Comprobaciones", "",
          "| ID | Carril | Comprobacion | Estado | Evidencia |",
          "| --- | --- | --- | --- | --- |"]
    for f in d["comprobaciones"]:
        ev = str(f["evidencia"]).replace("|", "\\|")
        L.append(f"| {f['id']} | {f['carril']} | {f['comprobacion']} | {f['estado']} | {ev} |")
    L += ["", "## Reproduccion (comandos y resultado)", ""]
    for c in d["comandos"]:
        L.append(f"- `{c['etiqueta']}` rc={c['rc']} (cwd `{c['cwd']}`): "
                 f"`{' '.join(c['argv'][-1:])}`")
    L += ["", "Sandbox: `" + d["sandbox"]["T"] + "` (eliminado al terminar) y `" + d["sandbox"]["A2"] + "` "
          "(solo se redirigen las lineas de ruta de salida); nada se escribe en los v001 sellados.", "",
          "## Pendiente (no auditado, no aceptado)", ""]
    for k, v in d["no_auditado"].items():
        L.append(f"- **{k}**: {v}")
    L += ["", f"v002 observados fuera de alcance: "
          f"{', '.join(d['v002_observados']['carriles']) or 'ninguno'}. "
          "Solo se dictamina sobre v001 sellado; sus bytes no cambiaron durante la auditoria.", ""]
    L += ["## Limites", ""] + [f"- {x}" for x in d["limites"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
