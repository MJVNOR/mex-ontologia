#!/usr/bin/env python3
"""Auditoria R-documental v003: reproduccion independiente de entregas selladas.

Lee bytes de las carpetas auditadas y de las fuentes locales. No escribe en
ellas. Genera verificacion.json con comprobaciones, hallazgos y huellas.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[6]
BASE = ROOT / "propuestas" / "ampliacion-post-r9" / "ejecucion-20261024"
OUT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_sellos import sha256_file, verify_abs_seal, verify_list_seal, verify_map_seal  # noqa: E402


def load(rel: str | Path) -> Any:
    p = ROOT / rel
    return json.loads(p.read_text(encoding="utf-8"))


def sha(rel: str | Path) -> str:
    return sha256_file(ROOT / rel)


def bytes_(rel: str | Path) -> int:
    return (ROOT / rel).stat().st_size


def check(checks: list[dict], cid: str, ok: bool, detalle: str, **extra: Any) -> None:
    checks.append({"id": cid, "ok": bool(ok), "detalle": detalle, **extra})


def norm(s: str) -> str:
    return " ".join(s.split())


def audit_t() -> dict[str, Any]:
    d = BASE / "T-top50" / "v002"
    checks: list[dict] = []
    seal = verify_list_seal("T-top50/v002", d)
    check(checks, "sello", seal["sello_valido"],
          f"{seal['archivos_ok']}/{seal['entradas']} archivos; sello canónico {'OK' if seal['sello_canonico_ok'] else 'DISCREPA'}; extras={seal['extras_no_sellados']}")

    plan_hash = sha("docs/plan-paralelo-ampliacion-post-r9.md")
    ent = load(d.relative_to(ROOT) / "entrega.json")
    check(checks, "h01_plan_actual", plan_hash == ent["hallazgo_h01"]["actual"] == "f43214a0d38ff2cb1fcdfb213d9aa0fba67415dc21b2033ac305a3a70eda0ce8",
          f"plan actual {plan_hash[:16]}… == declarado {ent['hallazgo_h01']['actual'][:16]}…; bytes {bytes_('docs/plan-paralelo-ampliacion-post-r9.md')}")

    mapa = load("data/portal/oportunidades-cruce.json")
    pares = mapa["pares"]
    cand = [p for p in pares if p["estado"] == "candidata_por_validar"]
    check(checks, "universo_3916_1191", len(pares) == 3916 and len(cand) == 1191,
          f"{len(pares)} pares, {len(cand)} candidatas")
    check(checks, "ids_unicos", len({p["id"] for p in pares}) == len(pares) == 3916,
          f"{len({p['id'] for p in pares})} ids únicos de {len(pares)}")

    crit = load("propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json")
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]

    def score(p: dict) -> float:
        return round(sum(pesos.get(f, 1) for f in p["familias_compartidas"]) + sum(pen.get(b, 0) for b in p["pendientes"]), 2)

    calc = sorted(((score(p), p["id"], p) for p in cand), key=lambda r: (-r[0], r[1]))
    check(checks, "scores_1191", len({r[1] for r in calc}) == 1191,
          f"{len(calc)} scores recomputados; cola {calc[-1][0]}")

    with open(ROOT / "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv", encoding="utf-8") as fh:
        import csv
        top_csv = list(csv.DictReader(fh))
    with open(ROOT / "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv", encoding="utf-8") as fh:
        matriz = list(csv.DictReader(fh))
    check(checks, "csv_50_1191", len(top_csv) == 50 and len(matriz) == 1191,
          f"top50={len(top_csv)}, matriz={len(matriz)}")
    byid = {i: s for s, i, _ in calc}
    check(checks, "matriz_scores", all(float(r["score"]) == byid[r["id"]] for r in matriz),
          "1191 scores de matriz == recomputo")
    check(checks, "top50_orden", all(top_csv[n]["id"] == calc[n][1] and float(top_csv[n]["score"]) == calc[n][0] and int(top_csv[n]["rango"]) == n + 1 for n in range(50)),
          "50 rangos/ids/scores y orden desc,id asc")

    pub = load(d.relative_to(ROOT) / "top50-oportunidades-r9.json")
    filas = pub["filas"]
    check(checks, "json_50", len(filas) == 50 and [f["rango"] for f in filas] == list(range(1, 51)),
          f"{len(filas)} filas, rangos 1..{filas[-1]['rango']}")
    check(checks, "json_filas_coinciden_csv", all(f["id"] == top_csv[n]["id"] and f["score"] == float(top_csv[n]["score"]) for n, f in enumerate(filas)),
          "ids/scores de las 50 filas == CSV")
    check(checks, "no_join", all(f["estado"] == "NO_JOIN_APROBADO" for f in filas) and pub["meta"]["estado_filas"] == "NO_JOIN_APROBADO",
          f"{sum(1 for f in filas if f['estado']=='NO_JOIN_APROBADO')}/50 filas NO_JOIN_APROBADO")

    carriles = {f["carril_analitico"]: f for f in filas if f.get("carril_analitico")}
    esperado = {"A1-911": (2, 3.0), "A2-matrimonios-nacimientos": (4, 3.0), "A3-itama": (1, 5.0)}
    ok_c = all(k in carriles and (carriles[k]["rango"], carriles[k]["score"]) == v for k, v in esperado.items()) and len(carriles) == 3
    check(checks, "carriles_3", ok_c,
          "; ".join(f"{k}: rango {carriles[k]['rango']} score {carriles[k]['score']}" for k in carriles) + f"; etiquetadas {len(carriles)}/50")
    carr = ent["resultados"]["carriles"]
    check(checks, "pares_a1_a3", all(carr[k]["id"] == pub["meta"]["pares_a1_a3"][k] for k in carr)
          and all((carr[k]["rango"], carr[k]["score"]) == esperado[k] for k in carr),
          "los 3 pares identificados por ID exacto, rangos 2/4/1, sin join")

    fuentes_ok = []
    for f in pub["meta"]["fuentes"]:
        fuentes_ok.append({"ruta": f["ruta"], "sha_ok": sha(f["ruta"]) == f["sha256"], "bytes_ok": bytes_(f["ruta"]) == f["bytes"]})
    check(checks, "fuentes_meta", all(x["sha_ok"] and x["bytes_ok"] for x in fuentes_ok),
          f"{sum(1 for x in fuentes_ok if x['sha_ok'] and x['bytes_ok'])}/{len(fuentes_ok)} fuentes con hash/bytes vigentes")

    # Reproduccion del script publicable en directorio temporal.
    tmp = Path(tempfile.mkdtemp(prefix="r_t_"))
    art = {}
    try:
        spec = importlib.util.spec_from_file_location("pub_t", d / "scripts" / "publicar_top50_r9.py")
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        mod.generar(ROOT, tmp)
        for name in ("top50-oportunidades-r9.json", "top50-oportunidades-r9.md", "top50-oportunidades-r9.html"):
            a = sha256_file(tmp / name)
            b = sha256_file(d / name)
            art[name] = {"reproducido": a, "sellado": b, "igual": a == b}
    except Exception as exc:  # noqa: BLE001
        art = {"error": f"{type(exc).__name__}: {exc}"}
    check(checks, "script_reproduce", bool(art) and "error" not in art and all(v["igual"] for v in art.values()),
          "3/3 artefactos idénticos" if "error" not in art else art["error"])

    guard = "destino prohibido" in (d / "scripts" / "publicar_top50_r9.py").read_text(encoding="utf-8") and "congelada.json" in (d / "scripts" / "publicar_top50_r9.py").read_text(encoding="utf-8")
    check(checks, "script_guardas", guard,
          "el script rechaza escribir en fuentes y en carpetas con congelada.json; excepción explícita para su propia carpeta de versión")

    return {"entrega": "T-top50/v002", "sello": seal, "checks": checks, "reproduccion": art,
            "total_ok": sum(c["ok"] for c in checks), "total": len(checks)}


def audit_a1() -> dict[str, Any]:
    d = BASE / "A1-911" / "v002"
    checks: list[dict] = []
    seal = verify_map_seal("A1-911/v002", d)
    check(checks, "sello", seal["sello_valido"],
          f"{seal['archivos_ok']}/{seal['entradas']} archivos; sidecar {'OK' if seal['sidecar_hash_ok'] else 'DISCREPA'}; extras={seal['extras_no_sellados']}")

    ent = load(d.relative_to(ROOT) / "entrega.json")
    res = load(d.relative_to(ROOT) / "resultados.json")
    src_ok = []
    for rel, meta in ent["verificacion"]["fuentes_sha256"].items():
        src_ok.append({"ruta": rel, "sha_ok": sha(rel) == meta["sha256"], "bytes_ok": bytes_(rel) == meta["bytes"]})
    check(checks, "fuentes", all(x["sha_ok"] and x["bytes_ok"] for x in src_ok),
          f"{sum(1 for x in src_ok if x['sha_ok'] and x['bytes_ok'])}/{len(src_ok)} fuentes vigentes")

    perfil = load("reports/catalogo-perfil.json")
    inv = {c["id"]: c for c in perfil["inventario"]}
    par = res["par"]
    ids_a = {r["id"] for r in inv[par["conjunto_a"]]["recursos"]}
    ids_b = {r["id"] for r in inv[par["conjunto_b"]]["recursos"]}
    ids = ids_a | ids_b
    check(checks, "recursos_par", len(ids_a) == 3 and len(ids_b) == 3 and ids == set(res["recursos"]),
          f"A={len(ids_a)}, B={len(ids_b)}; {len(res['recursos'])} recursos con ficha")

    insp = {r["id"]: r for r in load("data/portal/contenido-inspeccion.json")["recursos"]}
    d1, d2 = "54285a13-3a2a-4e47-b0af-e855861f5347", "6ce17dd1-5716-44e9-bc5f-603c0925afe6"
    s1, s2 = insp[d1]["sha256_fragmento_o_archivo"], insp[d2]["sha256_fragmento_o_archivo"]
    same = s1 == s2 == "9d710cb868c3fb6304a4310259bf4c7e64d2af7cdc15cd253bdc8dd86c9c2109"
    n_shas = sum(1 for r in insp.values() if r.get("sha256_fragmento_o_archivo") == s1)
    check(checks, "duplicado_q1", same and n_shas == 2,
          f"54285a13 == 6ce17dd1 (sha {s1[:16]}…, {insp[d1]['bytes_leidos']} bytes); el sha aparece en {n_shas} inspecciones")

    hojas = {rid: (r.get("tablas") or [{}])[0].get("hoja", "") for rid, r in insp.items() if rid in ids}
    improc = [rid for rid, h in hojas.items() if "IMPROCEDENTE" in h.upper()]
    check(checks, "improcedentes_solo_q2", improc == ["0df8592f-bb3d-466c-aec3-6cbc91253be0"] and hojas[d1] == "LLAMADAS PROCEDENTES 911",
          f"hoja improcedentes en {improc}; Q1 improcedentes contiene hoja '{hojas[d1]}'")

    dic = insp["1a95d734-2f0e-4781-8831-77dcfcbe70f8"]
    defs = dic["definiciones"]
    vars_ = [x["Nombre variable"] for x in defs]
    units_empty = all(x["Unidad de medida"].strip() == "" for x in defs)
    ident_nonempty = [x["Nombre variable"] for x in defs if x["Identificadores"].strip()]
    check(checks, "diccionario", dic["sha256_fragmento_o_archivo"] == "fcd73b159fdf46ce33a5d9c43f227b7a7b5e296cb197399a8eac6c6be57c5140"
          and insp["7922b8c8-db09-4172-ad7f-31b0ba0c68e3"]["sha256_fragmento_o_archivo"] == dic["sha256_fragmento_o_archivo"]
          and len(vars_) == 7 and units_empty and ident_nonempty == ["hora"]
          and not any("motivo" in v.lower() for v in vars_),
          f"sha idéntico A/B; {len(vars_)} variables; unidades vacías={units_empty}; Identificadores no vacío solo en {ident_nonempty}; sin variable motivo")

    heuristic = all((r.get("tablas") or [{}])[0].get("metodo_encabezado") == "heuristica_requiere_revision" for rid, r in insp.items() if rid in ids)
    check(checks, "esquemas_heuristica", heuristic, "6/6 esquemas con metodo_encabezado=heuristica_requiere_revision")

    cols_q2 = [c["id"] for c in insp["0df8592f-bb3d-466c-aec3-6cbc91253be0"]["tablas"][0]["campos"]]
    check(checks, "q2_sin_municipio", cols_q2 == ["FECHA", "HORA", "MOTIVO NO PROCEDENTE"],
          f"columnas Q2: {cols_q2}")

    lote = load("data/portal/lote-cruces/validacion-lote.json")
    lp = next(p for p in lote["pares"] if p["id"] == par["id"])
    da, db = lp["diagnostico_muestras"]["a"], lp["diagnostico_muestras"]["b"]
    check(checks, "muestra_a", da["recurso_id"] == d1 and db["recurso_id"] == "943e2919-6a8b-4776-ac4f-c3d6b02bb94e",
          f"muestra A={da['recurso_id'][:8]}… ({da['nombre']}); B={db['recurso_id'][:8]}… ({db['nombre']})")
    check(checks, "muestra_n29", da["limite"] == db["limite"] == 29 and da["filas_muestra"] == db["filas_muestra"] == 29,
          f"límite {da['limite']}; filas {da['filas_muestra']}/{db['filas_muestra']}; campos {da['campos_solicitados']}")
    reps = {k: (da["campos"][k]["repeticiones_muestra"], db["campos"][k]["repeticiones_muestra"]) for k in ("MUNICIPIO", "LOCALIDAD", "COLONIA")}
    check(checks, "repeticiones_muestra", reps == {"MUNICIPIO": (20, 20), "LOCALIDAD": (18, 10), "COLONIA": (1, 4)},
          f"repeticiones (A,B): {reps}")

    comp = lp.get("comparacion_muestras") or {}
    coinc = comp.get("coincidencias") if isinstance(comp, dict) else None
    if isinstance(coinc, dict):
        vals = coinc.get("MUNICIPIO") or coinc.get("municipio") or []
    else:
        vals = coinc or []
    check(checks, "coincidencias_6", len(vals) == 6,
          f"coincidencias muestrales MUNICIPIO={len(vals)}: {vals}")

    # Copias locales de filas 911: hashes exactos en xlsx/xls/csv del repo.
    target = {insp[d1]["sha256_fragmento_o_archivo"], insp["0df8592f-bb3d-466c-aec3-6cbc91253be0"]["sha256_fragmento_o_archivo"], insp["943e2919-6a8b-4776-ac4f-c3d6b02bb94e"]["sha256_fragmento_o_archivo"]}
    matches = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix.lower() not in {".xlsx", ".xls", ".csv"}:
            continue
        if sha256_file(p) in target:
            matches.append(str(p.relative_to(ROOT)))
    check(checks, "sin_copias_locales", matches == [], f"copias exactas xlsx/xls/csv de los 3 archivos 911: {len(matches)} {matches[:5]}")

    check(checks, "sin_join_ni_tasa", res["join"]["ejecutado"] is False and res["proporcion"]["estado"] == "bloqueada" and res["resultado"] == "bloqueado" and ent["resultado"] == "bloqueado",
          "join=false; proporción=bloqueada; resultado=bloqueado")
    check(checks, "ficha_8_ejes", set(res["ficha"]) == {"claves", "grano", "unicidad", "cardinalidad", "poblacion", "periodo", "unidades", "cobertura_datos"},
          f"ejes: {sorted(res['ficha'])}")
    check(checks, "duplicado_no_usado_para_sumar", "no se usa para agregar ni para sumar universos" in " ".join(res["limites"]),
          "límite declarado: el duplicado no se usa para agregar/sumar")

    return {"entrega": "A1-911/v002", "sello": seal, "checks": checks,
            "total_ok": sum(c["ok"] for c in checks), "total": len(checks),
            "coincidencias_muestra": vals}


def audit_a2() -> dict[str, Any]:
    d = BASE / "A2-registro-civil" / "v002"
    checks: list[dict] = []
    seal = verify_map_seal("A2-registro-civil/v002", d)
    check(checks, "sello", seal["sello_valido"],
          f"{seal['archivos_ok']}/{seal['entradas']} archivos; sidecar {'OK' if seal['sidecar_hash_ok'] else 'DISCREPA'}; extras={seal['extras_no_sellados']}")

    ent = load(d.relative_to(ROOT) / "entrega.json")
    res = load(d.relative_to(ROOT) / "resultados.json")
    for rel, meta in ent["verificacion"]["fuentes_sha256"].items():
        check(checks, f"fuente:{rel}", sha(rel) == meta["sha256"] and bytes_(rel) == meta["bytes"],
              f"sha/bytes {'OK' if sha(rel) == meta['sha256'] and bytes_(rel) == meta['bytes'] else 'DISCREPA'}")

    perfil = load("reports/catalogo-perfil.json")
    inv = {c["id"]: c for c in perfil["inventario"]}
    mat, nac = inv["1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98"], inv["df2d60f5-2243-4bb0-885a-941aa8a657f5"]
    DIC_MAT, DIC_NAC = "364ffa5c-e1c2-4185-a22f-80bede6735d0", "6bcf5b63-0855-4f3b-81a0-4bca82e97272"
    m_data = sum(1 for r in mat["recursos"] if r["id"] != DIC_MAT)
    n_data = sum(1 for r in nac["recursos"] if r["id"] != DIC_NAC)
    fl = res["fuentes_locales"]["reports/catalogo-perfil.json"]
    check(checks, "h02_conteos", len(mat["recursos"]) == 11 and m_data == 10 and len(nac["recursos"]) == 16 and n_data == 15
          and (fl["mat_recursos"], fl["mat_recursos_datos"], fl["mat_diccionarios"]) == (11, 10, 1)
          and (fl["nac_recursos"], fl["nac_recursos_datos"], fl["nac_diccionarios"]) == (16, 15, 1),
          f"Matrimonios {len(mat['recursos'])}={m_data}+1; Nacimientos {len(nac['recursos'])}={n_data}+1")

    insp = {r["id"]: r for r in load("data/portal/contenido-inspeccion.json")["recursos"]}
    vars_mat = sorted(x["Nombre variable"] for x in insp[DIC_MAT]["definiciones"])
    vars_nac = sorted(x["Nombre variable"] for x in insp[DIC_NAC]["definiciones"])
    check(checks, "grano_diccionarios", "dia_matrimonio" in vars_mat and "total" in vars_nac and "hombres" in vars_nac and "mujeres" in vars_nac,
          f"Matrimonios={vars_mat}; Nacimientos={vars_nac}")

    lote = load("data/portal/lote-cruces/validacion-lote.json")
    lp = next(p for p in lote["pares"] if p["id"] == res["par"])
    pruebas = lp["pruebas_recursos"]
    errs = [t.get("error_b") for t in pruebas]
    total_err = sum(1 for e in errs if e and "Total no coincide" in e)
    mes_err = sum(1 for e in errs if e and "Faltan meses" in e)
    check(checks, "cardinalidad_6_pruebas", len(pruebas) == 6 and total_err == 5 and mes_err == 1 and lp["decision"] == "fallo_validacion_integral",
          f"6 pruebas: {total_err} total≠hombres+mujeres, {mes_err} meses faltantes; decision={lp['decision']}")

    da, db = lp["diagnostico_muestras"]["a"], lp["diagnostico_muestras"]["b"]
    quote_ok = all("Diagnóstico de muestra; no demuestra unicidad ni cobertura integral" in (da["alcance"], db["alcance"]) for _ in [0])
    check(checks, "unicidad_cita", quote_ok and da["limite"] == db["limite"] == 100,
          f"cita literal con tilde en A/B; muestras n={da['limite']}/{db['limite']}")
    check(checks, "muestras_totales", (da["recurso_id"], da["total_declarado"]) != (db["recurso_id"], db["total_declarado"])
          and da["total_declarado"] == 14685 and db["total_declarado"] == 627,
          f"A={da['nombre']} total {da['total_declarado']}; B={db['nombre']} total {db['total_declarado']} (recursos/años distintos)")

    ev = res["ejes"]["periodo_ambito"]["evidencia"]
    check(checks, "periodo_variables", all(v in ev for v in ("Municipio de registro", "Año de registro", "Mes de registro", "Dia de registro"))
          and "Anio-Mes de registro" not in ev,
          "variables separadas y cita textual; sin 'Anio-Mes de registro'")

    # Reproduccion del script en directorio temporal (monkeypatch OUT).
    tmp = Path(tempfile.mkdtemp(prefix="r_a2_"))
    try:
        spec = importlib.util.spec_from_file_location("a2", d / "scripts" / "analizar.py")
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        mod.OUT = tmp
        mod.main()
        got = json.loads((tmp / "resultados.json").read_text(encoding="utf-8"))
        same = got == res
        err = None
    except Exception as exc:  # noqa: BLE001
        same = False
        err = f"{type(exc).__name__}: {exc}"
    check(checks, "script_reproduce", same, "resultados.json idéntico al sellado" if same else f"no reproduce: {err}")

    md = (d / "entrega.md").read_text(encoding="utf-8")
    rmd = (d / "resultados.md").read_text(encoding="utf-8")
    check(checks, "md_json_coherentes", "10 recursos de datos + 1 diccionario = 11" in md and "15 recursos de datos + 1 diccionario = 16" in md
          and "10 recursos de datos + 1 diccionario = 11" in rmd and "15 recursos de datos + 1 diccionario = 16" in rmd,
          "md de entrega y resultados declaran 10+1 / 15+1")
    check(checks, "sin_join_ni_tasa", res["comparacion_volumenes"] is None and res["join_grafo"] is None and res["veredicto"] == "BLOQUEADO",
          "comparación y join nulos; BLOQUEADO")

    # Razonamiento: no atribuir el bloqueo a grano/población como imposibilidad absoluta.
    sobre = []
    if "bloquean cualquier comparación" in rmd:
        sobre.append("resultados.md: 'Causas (bloquean cualquier comparación/join)'")
    if "impide join fila a fila" in " ".join(res["causas_bloqueo"]):
        sobre.append("resultados.json: 'grano distinto ... impide join fila a fila' como causa de bloqueo")
    if "poblaciones distintas (actos vs conteos de nacidos)" in " ".join(res["causas_bloqueo"]):
        sobre.append("resultados.json: poblaciones distintas listada entre las causas que bloquean")
    check(checks, "bloqueo_por_cobertura_no_solo_grano", not sobre,
          "sin sobreafirmación: el bloqueo se atribuye a cobertura/cardinalidad/catálogo" if not sobre else "; ".join(sobre))

    return {"entrega": "A2-registro-civil/v002", "sello": seal, "checks": checks,
            "total_ok": sum(c["ok"] for c in checks), "total": len(checks),
            "sobreafirmaciones": sobre}


def audit_a3() -> dict[str, Any]:
    d = BASE / "A3-itama" / "v002"
    checks: list[dict] = []
    seal = verify_list_seal("A3-itama/v002", d)
    check(checks, "sello", seal["sello_valido"],
          f"{seal['archivos_ok']}/{seal['entradas']} archivos; discrepancias={[c['ruta'] for c in seal['archivos_discrepantes']]}; extras={seal['extras_no_sellados']}")

    seal_mtime = (d / "congelada.json").stat().st_mtime
    posteriores = sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and p.name != "congelada.json" and p.stat().st_mtime > seal_mtime)
    check(checks, "sin_escrituras_post_sello", posteriores == [],
          f"archivos con mtime posterior al sello ({len(posteriores)}): {posteriores}")

    inv_json = load(d.relative_to(ROOT) / "resultados" / "inventario-archivos-repo.json")
    counts = {".xlsx": 0, ".csv": 0}
    seen = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        ext = p.suffix.lower()
        if ext in counts:
            counts[ext] += 1
            seen.append(p)
    check(checks, "conteo_repo", counts[".xlsx"] == inv_json["xlsx_total"] and counts[".csv"] == inv_json["csv_total"],
          f"barrido independiente: {counts['.xlsx']} xlsx, {counts['.csv']} csv; inventario declara {inv_json['xlsx_total']}/{inv_json['csv_total']}")

    perfil = load("reports/catalogo-perfil.json")
    inv = {c["id"]: c for c in perfil["inventario"]}
    itama_ids = [r["id"] for r in inv["27a5c80c-514a-4170-a2e5-7ef40d818641"]["recursos"]] + [r["id"] for r in inv["4d27a1c4-381d-4ce0-a663-0d3e23a93848"]["recursos"]]
    insp = {r["id"]: r for r in load("data/portal/contenido-inspeccion.json")["recursos"]}
    itama_hashes = {insp[i]["sha256_fragmento_o_archivo"] for i in itama_ids}
    exact = [str(p.relative_to(ROOT)) for p in seen if sha256_file(p) in itama_hashes]
    check(checks, "itama_8_y_cero_copias", len(itama_ids) == 8 and len(itama_hashes) == 8 and exact == [],
          f"{len(itama_ids)} recursos ITAMA ({sum(1 for i in itama_ids if insp[i]['fuente'].lower().endswith('.xlsx'))} xlsx); copias exactas en repo: {len(exact)}")

    # Muestras y escolaridad del par en el lote.
    lote = load("data/portal/lote-cruces/validacion-lote.json")
    lp = next(p for p in lote["pares"] if p["id"] == "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848")
    da, db = lp["diagnostico_muestras"]["a"], lp["diagnostico_muestras"]["b"]
    check(checks, "muestras_29_16", da["filas_muestra"] == 29 and db["filas_muestra"] == 16,
          f"muestras A={da['filas_muestra']} B={db['filas_muestra']}; límites {da['limite']}/{db['limite']}")
    esc = da["campos"].get("escolaridad") or da["campos"].get("ESCOLARIDAD")
    check(checks, "escolaridad_ausente", esc is None or esc.get("nulos") == 29,
          f"escolaridad en muestra A: {esc}")

    dic_fields = []
    for i in ("07781b38-8a53-42eb-b3b7-3c1ebc6a4415", "a7ee5717-b14d-439b-9508-bada58d0d185"):
        dic_fields.append(len(insp[i]["definiciones"]))
    check(checks, "diccionarios_11", dic_fields == [11, 11] and all(x["Unidad de medida"].strip() == "" for i in ("07781b38-8a53-42eb-b3b7-3c1ebc6a4415", "a7ee5717-b14d-439b-9508-bada58d0d185") for x in insp[i]["definiciones"]),
          f"campos por diccionario={dic_fields}; unidades vacías")

    return {"entrega": "A3-itama/v002", "sello": seal, "checks": checks,
            "total_ok": sum(c["ok"] for c in checks), "total": len(checks),
            "posteriores_al_sello": posteriores}


def audit_w() -> dict[str, Any]:
    d = BASE / "W-estandares" / "v002"
    checks: list[dict] = []
    seal = verify_abs_seal("W-estandares/v002", d)
    check(checks, "sello", seal["sello_valido"],
          f"{seal['archivos_ok']}/{seal['entradas']} archivos; extras={seal['extras_no_sellados']}")

    ent = load(d.relative_to(ROOT) / "entrega.json")
    check(checks, "base_r9", sha(ent["base"]["congelada"]) == ent["base"]["sha256"],
          f"base.json {ent['base']['sha256'][:16]}…")
    pet = load("propuestas/ampliacion-post-r9/ejecucion-20261024/Q-unidades/peticiones-web.json")
    check(checks, "peticiones_6", sha(ent["solicitud"]["ruta"]) == ent["solicitud"]["sha256"] and len(pet["solicitudes"]) == 6,
          f"peticiones {len(pet['solicitudes'])}; sha de solicitud vigente")

    casos = {s["caso"]: s["id"] for s in pet["solicitudes"]}
    res = {r["id"]: r for r in ent["resultados"]}
    check(checks, "casos_qw", len(res) == 6 and all(casos.get(r["caso"]) == rid for rid, r in res.items()),
          f"casos {sorted('Q-U0'+str(i) for i in range(1,7))} -> {sorted(res)}")

    expected = {
        "Q-W-01": ("TON_Metric", "t", None, "Metric Ton"),
        "Q-W-02": ("KiloGM", "kg", "Kilogramo", "Kilogram"),
        "Q-W-03": ("MegaW", "MW", "Megavatio", "Megawatt"),
        "Q-W-04": ("GigaW-HR", "GW·h", None, "Gigawatt Hour"),
        "Q-W-05": ("PERCENT", "%", None, "Percent"),
        "Q-W-06": ("DEG_C", "°C", "Grado Celsius", "Degree Celsius"),
    }
    malos = []
    for rid, r in res.items():
        term, sym, es, en = expected[rid]
        evp = ROOT / r["evidencia"]["ruta"]
        txt = evp.read_text(encoding="utf-8")
        ok = (r["sujeto_rdf"] == f"http://qudt.org/vocab/unit/{term}" and r["simbolo"] == sym
              and r["etiqueta_es"] == es and r["etiqueta_en"] == en
              and sha256_file(evp) == r["evidencia"]["sha256"] and evp.stat().st_size == r["evidencia"]["bytes"]
              and f"http://qudt.org/vocab/unit/{term}" in txt and "QUDT 3.5.3" in txt
              and "http://qudt.org/3.5.3/vocab/unit" in txt and "2026-10-20T17:45:20.378+00:00" in txt
              and (f'"{es}"@es' in txt if es else "@es" not in txt)
              and (f'"{sym}"' in txt))
        if not ok:
            malos.append({"id": rid, "falta": [k for k, v in {
                "sujeto": r["sujeto_rdf"] == f"http://qudt.org/vocab/unit/{term}",
                "simbolo": r["simbolo"] == sym,
                "etiqueta": (r["etiqueta_es"] == es and r["etiqueta_en"] == en),
                "hash": sha256_file(evp) == r["evidencia"]["sha256"],
                "texto": f"http://qudt.org/vocab/unit/{term}" in txt,
                "version": "QUDT 3.5.3" in txt,
                "generado": "2026-10-20T17:45:20.378+00:00" in txt,
                "etiqueta_texto": (f'"{es}"@es' in txt if es else "@es" not in txt),
                "simbolo_texto": f'"{sym}"' in txt,
            }.items() if not v]})
    check(checks, "terminos_6", not malos, "6/6 sujetos, símbolos, etiquetas @es/@en, versión, generado y hash de evidencia" if not malos else malos)

    g = (d / "normativa" / "unit-GigaW-HR-evidencia.txt").read_text(encoding="utf-8")
    check(checks, "gigaw_simbolo", '"GW·h"' in g and "GW.h" in g and "GWH" in g and "GWh" not in g,
          "evidencia: GW·h; ucumCode GW.h; uneceCommonCode GWH; sin 'GWh'")
    pc = (d / "normativa" / "unit-PERCENT-evidencia.txt").read_text(encoding="utf-8")
    check(checks, "percent_factor", "0.01" in pc and "conversionMultiplier" in pc,
          "PERCENT: conversionMultiplier 0.01 en el término normativo")

    capas = load(d.relative_to(ROOT) / "normativa" / "capas-normativas.json")
    check(checks, "capas_6", len(capas["capas_por_termino"]) == 6 and len({c["sujeto_rdf"] for c in capas["capas_por_termino"]}) == 6,
          f"{len(capas['capas_por_termino'])} capas, sujetos únicos")
    check(checks, "sin_alias_ni_factores", ent["resumen"]["alias_inventados"] == 0 and ent["resumen"]["casos_locales_promovidos"] == 0
          and "no se aplican" in " ".join(ent["condiciones_de_aceptacion"]).lower() or "no se aplica" in " ".join(ent["condiciones_de_aceptacion"]).lower(),
          "0 alias, 0 casos locales promovidos; sin factores aplicados")
    check(checks, "fuente_local_distinta", "Fuente normativa != evidencia local" in " ".join(ent["limites"]),
          "se declara que la fuente normativa no acredita el uso local")

    return {"entrega": "W-estandares/v002", "sello": seal, "checks": checks,
            "total_ok": sum(c["ok"] for c in checks), "total": len(checks)}


def main() -> int:
    out = {
        "generado_en_utc": "2026-10-24",
        "metodo": "reproduccion_independiente_solo_lectura",
        "entregas": {
            "T-top50/v002": audit_t(),
            "A1-911/v002": audit_a1(),
            "A2-registro-civil/v002": audit_a2(),
            "A3-itama/v002": audit_a3(),
            "W-estandares/v002": audit_w(),
        },
        "pendientes_no_auditados": {
            "Q-unidades/v003": "sin sello al cierre de esta verificacion",
            "S-shacl/v001": "en prueba; sin sello",
        },
    }
    payload = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)
    (OUT / "verificacion.json").write_text(payload + "\n", encoding="utf-8")
    print(payload[:1200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
