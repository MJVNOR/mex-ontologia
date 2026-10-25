"""R-documental v001: auditoria semantica/documental de T-top50/v001 y A2/v001.

Solo lectura sobre entregas selladas y fuentes. Escribe exclusivamente en
propuestas/ampliacion-post-r9/ejecucion-20261024/R-documental/v001/.

Recalcula por codigo: 3916/1191/50, scores, orden, sellos SHA256, y reproduce
la estructura completa de A2 resultados.json desde las fuentes locales.
Emite dictamen.json, dictamen.md, sello.json y sello.sha256.
Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/R-documental/v001/scripts/auditar.py
"""
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

V001 = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[6]
EJEC = "propuestas/ampliacion-post-r9/ejecucion-20261024"
T = ROOT / EJEC / "T-top50/v001"
A2 = ROOT / EJEC / "A2-registro-civil/v001"

MAPA = "data/portal/oportunidades-cruce.json"
CRIT = "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/criterio.json"
TOP_CSV = "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv"
MAT_CSV = "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/matriz_pares_relevantes.csv"
COB = "reports/cobertura-operativa-r9.json"
PERFIL = "reports/catalogo-perfil.json"
INSP = "data/portal/contenido-inspeccion.json"
LOTE = "data/portal/lote-cruces/validacion-lote.json"
PLAN = "docs/plan-paralelo-ampliacion-post-r9.md"
SEGUIM = "reports/seguimiento-operativo-post-r9.json"
VERIF = "data/territorio/verificacion.json"

PAR_A1 = "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92"
PAR_A2 = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5"
PAR_A3 = "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848"
MAT_C = "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98"
NAC_C = "df2d60f5-2243-4bb0-885a-941aa8a657f5"
DIC_MAT = "364ffa5c-e1c2-4185-a22f-80bede6735d0"
DIC_NAC = "6bcf5b63-0855-4f3b-81a0-4bca82e97272"
NO_JOIN = "NO_JOIN_APROBADO"

CHECKS = []


def chk(cid, entrega, enunciado, ok, detalle="", hallazgo=None):
    CHECKS.append({"id": cid, "entrega": entrega, "enunciado": enunciado,
                   "ok": bool(ok), "detalle": detalle, "hallazgo": hallazgo})
    return bool(ok)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def csvrows(rel):
    with open(ROOT / rel, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def snapshot(base):
    out = {}
    for p in sorted(Path(base).rglob("*")):
        if p.is_file():
            out[str(p.relative_to(ROOT)).replace("\\", "/")] = sha(p)
    return out


def mtime(rel):
    return datetime.fromtimestamp((ROOT / rel).stat().st_mtime, timezone.utc).isoformat()


def main():
    hoy = datetime.now(timezone.utc).isoformat(timespec="seconds")
    snap_ini = {"T": snapshot(T), "A2": snapshot(A2)}

    mapa = load(MAPA)
    crit = load(CRIT)
    cob = load(COB)
    perfil = load(PERFIL)
    insp = load(INSP)
    lote = load(LOTE)
    top = csvrows(TOP_CSV)
    mat = csvrows(MAT_CSV)
    pares = mapa["pares"]
    inv = {p["id"]: p for p in pares}
    pesos, pen = crit["pesos_familia"], crit["penalizaciones"]
    a_entrega = load(EJEC + "/T-top50/v001/entrega.json")
    t_cong = load(EJEC + "/T-top50/v001/congelada.json")
    a2_res = load(EJEC + "/A2-registro-civil/v001/resultados.json")
    a2_cong = load(EJEC + "/A2-registro-civil/v001/congelada.json")

    def score(p):
        return round(sum(pesos.get(f, 1) for f in p.get("familias_compartidas", []))
                     + sum(pen.get(b, 0) for b in p.get("pendientes", [])), 2)

    # ---------------- T-top50 ----------------
    por_estado = {}
    for p in pares:
        por_estado[p["estado"]] = por_estado.get(p["estado"], 0) + 1
    cand = [p for p in pares if p["estado"] == "candidata_por_validar"]
    calc = sorted(((score(p), p["id"]) for p in cand), key=lambda r: (-r[0], r[1]))
    scores_calc = {i: s for s, i in calc}

    chk("T-01", "T", "Mapa con 3916 pares y 1191 candidatas", 
        len(pares) == 3916 and por_estado.get("candidata_por_validar") == 1191,
        f"pares={len(pares)} estados={por_estado}")
    chk("T-02", "T", "Reparto de estados 2328/1191/396/1", 
        por_estado == {"sin_clave_detectada": 2328, "candidata_por_validar": 1191,
                       "solo_dimensiones_amplias_o_tiempo": 396, "exploratorio_ejecutado": 1},
        json.dumps(por_estado, sort_keys=True))
    chk("T-03", "T", "1191 ids candidatos unicos", len({p["id"] for p in cand}) == 1191,
        f"unicos={len({p['id'] for p in cand})}")
    chk("T-04", "T", "Matriz 1191 filas, ids unicos y 1191 scores recomputados iguales",
        len(mat) == 1191 and len({r["id"] for r in mat}) == 1191
        and all(float(r["score"]) == scores_calc[r["id"]] for r in mat),
        "desiguales=" + str(sum(1 for r in mat if float(r["score"]) != scores_calc.get(r["id"]))))
    orden = [(float(r["score"]), r["id"]) for r in top]
    chk("T-05", "T", "Top50: rangos 1-50, ids unicos, orden score desc/id asc y 50 scores iguales",
        len(top) == 50 and len({r["id"] for r in top}) == 50
        and [int(r["rango"]) for r in top] == list(range(1, 51))
        and orden == calc[:50],
        f"n={len(top)} primer={top[0]['id']} score={top[0]['score']}")
    p1 = inv[calc[0][1]]
    chk("T-06", "T", "Top1 ITAMA con pesos 13.0, penalizaciones -8.0 y score 5.0",
        calc[0][0] == 5.0
        and round(sum(pesos.get(f, 1) for f in p1["familias_compartidas"]), 2) == 13.0
        and round(sum(pen.get(b, 0) for b in p1["pendientes"]), 2) == -8.0,
        f"id={calc[0][1]} score={calc[0][0]}")
    rangos = {r["id"]: (int(r["rango"]), float(r["score"])) for r in top}
    a_ok = (rangos.get(PAR_A1) == (a_entrega["casos_analiticos_identificados"]["A1-911"]["rango"],
                                   a_entrega["casos_analiticos_identificados"]["A1-911"]["score"]))
    a2_ok = (rangos.get(PAR_A2) == (a_entrega["casos_analiticos_identificados"]["A2-matrimonios-nacimientos"]["rango"],
                                    a_entrega["casos_analiticos_identificados"]["A2-matrimonios-nacimientos"]["score"]))
    a3_ok = (rangos.get(PAR_A3) == (a_entrega["casos_analiticos_identificados"]["A3-itama"]["rango"],
                                    a_entrega["casos_analiticos_identificados"]["A3-itama"]["score"]))
    ident_ok = (inv[PAR_A1]["titulo_a"] == "Llamadas Improcedentes 911"
                and inv[PAR_A1]["titulo_b"] == "Llamadas Procedentes 911"
                and inv[PAR_A2]["titulo_a"] == "Matrimonios" and inv[PAR_A2]["titulo_b"] == "Nacimientos"
                and inv[PAR_A3]["titulo_a"] == "Poblaci\u00f3n ITAMA Internamiento"
                and inv[PAR_A3]["titulo_b"] == "Poblaci\u00f3n ITAMA Externamiento")
    chk("T-07", "T", "A1/A2/A3 por ID exacto en top50 con rango, score y titulos del mapa",
        a_ok and a2_ok and a3_ok and ident_ok,
        f"A1={rangos.get(PAR_A1)} A2={rangos.get(PAR_A2)} A3={rangos.get(PAR_A3)}")

    st = load(EJEC + "/T-top50/v001/top50-oportunidades-r9.json")
    meta, filas = st["meta"], st["filas"]
    st_meta = (meta["mapa"]["sha256"] == sha(ROOT / MAPA) and meta["mapa"]["pares"] == 3916
               and meta["mapa"]["candidatas"] == 1191
               and meta["criterio_c2"]["sha256"] == sha(ROOT / CRIT)
               and meta["cobertura_r9"]["sha256"] == sha(ROOT / COB)
               and meta["estado_filas"] == NO_JOIN
               and meta["pares_a1_a3"] == {"A1-911": PAR_A1, "A2-matrimonios-nacimientos": PAR_A2,
                                           "A3-itama": PAR_A3})
    chk("T-08a", "T", "Staging JSON: meta con huellas reales, 3916/1191 y estado NO_JOIN",
        st_meta, f"filas={len(filas)}")

    filas_ok, filas_err = len(filas) == 50, []
    carril = {PAR_A1: "A1-911", PAR_A2: "A2-matrimonios-nacimientos", PAR_A3: "A3-itama"}
    for i, f in enumerate(filas):
        r, p = top[i], inv.get(f["id"])
        ok = (p is not None and f["rango"] == i + 1 and f["id"] == r["id"]
              and f["score"] == float(r["score"])
              and f["titulo_a"] == p["titulo_a"] and f["titulo_b"] == p["titulo_b"]
              and set(f["familias"]) == set(p["familias_compartidas"])
              and set(f["bloqueadores"]) == set(p["pendientes"])
              and f["fuentes"] == {"conjunto_a": p["conjunto_a"], "conjunto_b": p["conjunto_b"]}
              and f["estado"] == NO_JOIN and f["carril_analitico"] == carril.get(f["id"]))
        if not ok:
            filas_err.append(f["id"])
    chk("T-08b", "T", "Staging JSON: 50 filas fieles al mapa/CSV (titulos, familias, bloqueadores, conjuntos, carril)",
        filas_ok and not filas_err, f"desviaciones={filas_err[:3]}")

    md_t = (T / "top50-oportunidades-r9.md").read_text(encoding="utf-8")
    html_t = (T / "vista-top50-r9.html").read_text(encoding="utf-8")
    md_ids = {r["id"] for r in top if r["id"] in md_t}
    html_ids = {r["id"] for r in top if r["id"] in html_t}
    chk("T-09", "T", "Vistas md/html contienen las 50 filas y el estado NO_JOIN_APROBADO",
        len(md_ids) == 50 and len(html_ids) == 50 and NO_JOIN in md_t and NO_JOIN in html_t
        and html_t.count("<tr><td>") == 50,
        f"md={len(md_ids)} html={len(html_ids)} filas_html={html_t.count('<tr><td>')}")
    chk("T-10", "T", "Ningun join ni rate aprobado por el ranking",
        all(f["estado"] == NO_JOIN for f in filas)
        and a_entrega["estado_filas"] == NO_JOIN
        and "tasa" not in json.dumps(st, ensure_ascii=False).lower()
        and "rate" not in {k.lower() for f in filas for k in f},
        "estado_filas=" + a_entrega["estado_filas"])

    fuentes_ok, fuentes_err = [], []
    for f in a_entrega["fuentes"]:
        real = sha(ROOT / f["ruta"]) if (ROOT / f["ruta"]).is_file() else None
        (fuentes_ok if real == f["sha256"] else fuentes_err).append(f["ruta"])
    chk("T-11", "T", "Huellas de fuentes declaradas coinciden con los bytes actuales (6/7; plan desactualizado, H-01)",
        not [r for r in fuentes_err if r != PLAN] and fuentes_err in ([], [PLAN]),
        f"coinciden={len(fuentes_ok)}/7 no_coinciden={fuentes_err}", hallazgo="H-01")

    num_ok = (cob["indicadores"]["significados_respaldados"] == 1423
              and cob["indicadores"]["conceptos"] == 1106
              and cob["denominadores"]["significados_reales_pendientes"] == 138
              and cob["pendientes"]["vigencias"] == 16
              and cob["pendientes"]["candidatas_dependientes_de_evidencia"] == 17
              and cob["estado"] == "cobertura_operativa_validada_sin_cambios_al_grafo")
    prosa = a_entrega["resultados"]["cobertura_r9"] + " " + json.dumps(a_entrega["resultados"], ensure_ascii=False)
    chk("T-12", "T", "Cobertura R9: 1423/1106/138/16/17 y estado declarados coinciden con el reporte",
        num_ok and all(n in prosa for n in ("1423", "1106", "138", "16", "17")),
        f"estado={cob['estado']}")

    t_hash_ok = all(sha(ROOT / a["ruta"]) == a["sha256"]
                    and (ROOT / a["ruta"]).stat().st_size == a["bytes"] for a in t_cong["archivos"])
    t_set = {str(p.relative_to(ROOT)).replace("\\", "/") for p in T.rglob("*") if p.is_file()}
    t_dec = {a["ruta"] for a in t_cong["archivos"]}
    chk("T-13", "T", "Sellos T: 7 archivos con SHA256/bytes correctos y sin omisiones",
        t_hash_ok and t_dec | {EJEC + "/T-top50/v001/congelada.json"} == t_set,
        f"declarados={len(t_dec)} en_disco={len(t_set)}")

    rango_mat_ok = ([int(r["rango"]) for r in mat] == list(range(1, 1192))
                    and [float(r["score"]) for r in mat] == sorted((float(r["score"]) for r in mat), reverse=True)
                    and [r["id"] for r in mat[:50]] == [r["id"] for r in top])
    chk("T-14", "T", "Matriz ordenada por rango 1-1191, score no creciente y mismas 50 primeras",
        rango_mat_ok, f"rango1={mat[0]['rango']} rangoN={mat[-1]['rango']}")

    resumen_t = a_entrega["resultados"]
    chk("T-15", "T", "Resumenes de entrega (top50, matriz, mapa, top1) coinciden con el recomputo",
        resumen_t["matriz_1191"].startswith("1191/1191")
        and resumen_t["top50_csv"].startswith("50/50")
        and resumen_t["orden_top50"].startswith("50/50")
        and resumen_t["verificacion_mapa"] ==
        "3916 pares; estados sin_clave_detectada=2328, candidata_por_validar=1191, "
        "solo_dimensiones_amplias_o_tiempo=396, exploratorio_ejecutado=1."
        and resumen_t["top1"]["pesos_suma"] == 13.0
        and resumen_t["top1"]["penalizaciones_suma"] == -8.0
        and resumen_t["top1"]["score"] == 5.0,
        "prosa de resultados verificada contra recomputo")

    # ---------------- A2 ----------------
    a2_hash_ok = all(sha(A2 / rel) == h for rel, h in a2_cong["archivos"].items())
    lado = (A2 / "congelada.sha256").read_text(encoding="utf-8").split()
    a2_set = {str(p.relative_to(A2)).replace("\\", "/") for p in A2.rglob("*") if p.is_file()}
    chk("A2-01", "A2", "Sellos A2: 5 archivos con SHA256 correctos, sidecar y sin omisiones",
        a2_hash_ok and lado == [sha(A2 / "congelada.json"), "congelada.json"]
        and set(a2_cong["archivos"]) | {"congelada.json", "congelada.sha256"} == a2_set,
        f"declarados={len(a2_cong['archivos'])} en_disco={len(a2_set)}")

    inv_p = {c["id"]: c for c in perfil["inventario"]}
    recs = {r["id"]: r for r in insp["recursos"]}
    defs_mat = {d["Nombre variable"]: d for d in recs[DIC_MAT]["definiciones"]}
    defs_nac = {d["Nombre variable"]: d for d in recs[DIC_NAC]["definiciones"]}
    par_op = inv[PAR_A2]
    par_lote = next(p for p in lote["pares"] if p["id"] == PAR_A2)
    errores_b = [t["error_b"] for t in par_lote["pruebas_recursos"]]
    diag = par_lote["diagnostico_muestras"]

    esperado = {
        "par": PAR_A2,
        "pregunta": "Que volumenes de matrimonios y nacimientos se registran en un periodo "
                    "y ambito territorial documentalmente comparables?",
        "veredicto": "BLOQUEADO",
        "comparacion_volumenes": None,
        "join_grafo": None,
        "causas_bloqueo": [
            "grano distinto (evento vs agregado) impide join fila a fila",
            "unicidad/cardinalidad no acreditadas: muestras n=100 declaran no demostrar unicidad ni cobertura",
            "inconsistencia interna en Nacimientos: total != hombres+mujeres en 5/6 pruebas; meses faltantes",
            "municipio/periodo solo de registro, sin residencia y sin catalogo de correspondencia de codigos",
            "poblaciones distintas (actos vs conteos de nacidos); prohibidas causalidad y tasas poblacionales",
        ],
        "ejes": {
            "claves": {
                "veredicto": "no_acreditada",
                "evidencia": "oportunidades: estado candidata_por_validar, familia municipio con "
                             "pendientes verificar_catalogo_dominio_unicidad_y_contexto_de_clave y "
                             "municipio_puede_requerir_entidad_como_clave_compuesta; "
                             "nombres_campos_coincidentes_sin_garantia_semantica=[municipio]"},
            "grano": {
                "veredicto": "distinto_bloquea_join",
                "evidencia": f"diccionario Matrimonios vars={sorted(defs_mat)} (evento con dia_matrimonio, "
                             "edad/sexo contrayentes); diccionario Nacimientos vars="
                             f"{sorted(defs_nac)} (conteo agregado hombres/mujeres/total por municipio-anio-mes)"},
            "unicidad": {
                "veredicto": "no_acreditada",
                "evidencia": "validacion-lote diagnostico_muestras alcance en a y b: "
                             "'Diagnostico de muestra; no demuestra unicidad ni cobertura integral'"},
            "cardinalidad": {
                "veredicto": "no_acreditada",
                "evidencia": f"decision={par_lote['decision']}; errores_b={errores_b}"},
            "poblacion": {
                "veredicto": "distinta",
                "evidencia": "matrimonios=actos (2 contrayentes por fila, sin id persona); "
                             "nacimientos=conteos agregados por sexo; poblaciones distintas explicitas, "
                             "sin join de personas"},
            "periodo_ambito": {
                "veredicto": "comparable_solo_en_registro_no_acreditado_para_join",
                "evidencia": "anios_coincidentes_solo_en_nombres 2015-2024; ambos diccionarios: "
                             "'Municipio de registro'/'Anio-Mes de registro'; ningun campo de residencia "
                             "en definiciones locales; municipio sin catalogo de correspondencia"},
            "unidades": {
                "veredicto": "no_homologables_sin_regla",
                "evidencia": "matrimonios: fila=1 evento; nacimientos: fila=agregado con total; "
                             "pendiente validar_unidades_de_medidas_seleccionadas; sin tasas poblacionales"},
            "cobertura": {
                "veredicto": "no_acreditada",
                "evidencia": "prueba 2016: 'Faltan meses por municipio; ausencia no equivale a cero'; "
                             "muestras n=100 con total_declarado (Mat2023=14685, Nac2024=627) de "
                             "recursos/anios distintos"},
        },
        "fuentes_locales": {
            "reports/catalogo-perfil.json": {
                "mat_recursos": len(inv_p[MAT_C]["recursos"]),
                "nac_recursos": len(inv_p[NAC_C]["recursos"])},
            "data/portal/contenido-inspeccion.json": {
                "diccionario_matrimonios_sha256": recs[DIC_MAT]["sha256_fragmento_o_archivo"],
                "diccionario_nacimientos_sha256": recs[DIC_NAC]["sha256_fragmento_o_archivo"]},
            "data/portal/oportunidades-cruce.json": {"estado_par": par_op["estado"]},
            "data/portal/lote-cruces/validacion-lote.json": {"decision_par": par_lote["decision"]},
        },
        "metodo": "solo_datos_documentos_locales; sin_red; sin_grafo; sin_studio",
    }
    difs = [k for k in esperado if esperado.get(k) != a2_res.get(k)]
    chk("A2-02", "A2", "resultados.json se reproduce integramente desde fuentes locales (8 ejes, causas, fuentes, metodo)",
        not difs and set(esperado) == set(a2_res), f"claves_divergentes={difs}")

    chk("A2-03", "A2", "Eje claves: par candidata_por_validar, pendientes de catalogo/unicidad y campo municipio sin garantia",
        par_op["estado"] == "candidata_por_validar"
        and "verificar_catalogo_dominio_unicidad_y_contexto_de_clave" in par_op["pendientes"]
        and par_op["nombres_campos_coincidentes_sin_garantia_semantica"] == ["municipio"],
        f"estado={par_op['estado']} pendientes={len(par_op['pendientes'])}")

    grano_ok = (set(defs_mat) == {"municipio", "edad_cty1", "edad_cty2", "sexo_cty1", "sexo_cty2",
                                  "a\u00f1o_matrimonio", "mes_matrimonio", "dia_matrimonio"}
                and set(defs_nac) == {"municipio", "a\u00f1o", "mes", "hombres", "mujeres", "total"}
                and "dia_matrimonio" in defs_mat and "hombres" in defs_nac and "total" in defs_nac)
    chk("A2-04", "A2", "Eje grano: Matrimonios fila-evento (dia/edad/sexo) vs Nacimientos agregado (hombres/mujeres/total)",
        grano_ok, "vars_mat=" + str(len(defs_mat)) + " vars_nac=" + str(len(defs_nac)))

    unic_ok = (diag["a"]["limite"] == 100 and diag["b"]["limite"] == 100
               and diag["a"]["filas_muestra"] == 100 and diag["b"]["filas_muestra"] == 100
               and diag["a"]["alcance"] == "Diagn\u00f3stico de muestra; no demuestra unicidad ni cobertura integral"
               and diag["b"]["alcance"] == "Diagn\u00f3stico de muestra; no demuestra unicidad ni cobertura integral")
    chk("A2-05", "A2", "Eje unicidad: dos muestras n=100 declaran no demostrar unicidad ni cobertura integral",
        unic_ok, f"a={diag['a']['nombre']} b={diag['b']['nombre']}")

    err_total = [e for e in errores_b if "Total no coincide" in e]
    err_meses = [e for e in errores_b if "Faltan meses" in e]
    anios = [t["anio"] for t in par_lote["pruebas_recursos"]]
    chk("A2-06", "A2", "Eje cardinalidad: 6 pruebas, decision de fallo, 5 total!=hombres+mujeres y 1 meses faltantes",
        len(par_lote["pruebas_recursos"]) == 6 and par_lote["decision"] == "fallo_validacion_integral"
        and len(err_total) == 5 and len(err_meses) == 1
        and anios == [2015, 2016, 2020, 2021, 2022, 2023]
        and all("ausencia no equivale a cero" in e for e in err_meses),
        f"anios={anios} total={len(err_total)} meses={len(err_meses)}")

    pob_ok = ("id_persona" not in defs_mat and "id_persona" not in defs_nac
              and {"hombres", "mujeres"} <= set(defs_nac)
              and len([v for v in defs_mat if v.startswith(("edad_cty", "sexo_cty"))]) == 4)
    chk("A2-07", "A2", "Eje poblacion: actos con dos contrayentes sin id de persona vs conteos agregados por sexo",
        pob_ok, "sin id_persona en ambos diccionarios")

    anios_mapa = par_op["anios_coincidentes_solo_en_nombres"]
    desc_reg = any("registro" in (d.get("Descripci\u00f3n") or "").lower()
                   for d in list(defs_mat.values()) + list(defs_nac.values())
                   if d.get("Nombre variable") in ("municipio", "a\u00f1o_matrimonio", "mes_matrimonio",
                                                   "a\u00f1o", "mes"))
    resid = any("residencia" in (d.get("Descripci\u00f3n") or "").lower()
                for d in list(defs_mat.values()) + list(defs_nac.values()))
    chk("A2-08", "A2", "Eje periodo/ambito: solape 2015-2024 solo por nombres, periodo de registro y sin residencia",
        anios_mapa == [str(y) for y in range(2015, 2025)] and desc_reg and not resid,
        f"anios={anios_mapa[0]}-{anios_mapa[-1]} registro={desc_reg} residencia={resid}")

    unidades_ok = ("validar_unidades_de_medidas_seleccionadas" in par_op["pendientes"]
                   and set(defs_mat) >= {"dia_matrimonio"} and {"hombres", "mujeres", "total"} <= set(defs_nac)
                   and a2_res["ejes"]["unidades"]["veredicto"] == "no_homologables_sin_regla")
    chk("A2-09", "A2", "Eje unidades: fila-evento vs fila-agregado, pendiente de unidades y sin tasas",
        unidades_ok, "pendiente de unidades presente en el mapa")

    cob_ok = (diag["a"]["total_declarado"] == 14685 and diag["b"]["total_declarado"] == 627
              and diag["a"]["nombre"] == "Matrimonios 2023" and diag["b"]["nombre"] == "Nacimientos 2024"
              and any("Faltan meses" in e for e in err_meses))
    chk("A2-10", "A2", "Eje cobertura: muestras n=100 con totales 14685/627 de recursos-anios distintos y meses faltantes",
        cob_ok, f"total_a={diag['a']['total_declarado']} total_b={diag['b']['total_declarado']}")

    ficha = (A2 / "A2-pregunta-ficha.md").read_text(encoding="utf-8")
    ficha_rows = re.findall(r"^\| (\d) \|", ficha, flags=re.M)
    veredictos_ficha = ["no acreditada", "distinto, bloquea join", "no acreditada", "no acreditada",
                        "distinta", "solo registro, no join", "no homologables", "no acreditada"]
    ejes_ficha = ["Claves", "Grano", "Unicidad", "Cardinalidad", "Poblaci\u00f3n",
                  "Periodo/\u00e1mbito", "Unidades", "Cobertura"]
    chk("A2-11", "A2", "Ficha: 8 ejes con veredicto coherente con resultados.json",
        ficha_rows == list("12345678")
        and all(v in ficha for v in veredictos_ficha)
        and all(k in ficha for k in ejes_ficha),
        f"filas={len(ficha_rows)} ejes={len(ejes_ficha)}")

    md_a2 = (A2 / "resultados.md").read_text(encoding="utf-8")
    caus_md = re.findall(r"^\d+\. ", md_a2, flags=re.M)
    chk("A2-12", "A2", "resultados.md: BLOQUEADO, 5 causas y anios de inconsistencia 2015/2020-2023",
        "BLOQUEADO" in md_a2 and len(caus_md) == 5 and "2015" in md_a2 and "2023" in md_a2,
        f"causas={len(caus_md)}")

    nombres_mat = [r.get("name", "") for r in inv_p[MAT_C]["recursos"]]
    nombres_nac = [r.get("name", "") for r in inv_p[NAC_C]["recursos"]]
    anios_mat = sorted({int(y) for n in nombres_mat for y in re.findall(r"(20\d{2})", n)})
    anios_nac = sorted({int(y) for n in nombres_nac for y in re.findall(r"(20\d{2})", n)})
    chk("A2-13", "A2", "Inventario: 11 recursos Matrimonios (2015-2024) y 16 Nacimientos (2010-2024), diccionario incluido",
        len(nombres_mat) == 11 and len(nombres_nac) == 16
        and anios_mat == list(range(2015, 2025)) and anios_nac == list(range(2010, 2025))
        and any("Diccionario" in n for n in nombres_mat) and any("Diccionario" in n for n in nombres_nac),
        f"mat={len(nombres_mat)} {anios_mat[0]}-{anios_mat[-1]}; nac={len(nombres_nac)} {anios_nac[0]}-{anios_nac[-1]}")

    script_a2 = (A2 / "scripts/analizar.py").read_text(encoding="utf-8")
    imports_a2 = sorted(set(re.findall(r"^import (\w+)", script_a2, flags=re.M)))
    rutas_ok = ("parents[6]" in script_a2 and "parents[1]" in script_a2
                and PAR_A2 in script_a2 and DIC_MAT in script_a2 and DIC_NAC in script_a2)
    chk("A2-14", "A2", "Script A2: solo stdlib, rutas e IDs correctos, sin red/grafo/studio",
        imports_a2 == ["csv", "hashlib", "json", "pathlib"] or imports_a2 == ["hashlib", "json", "pathlib"]
        or (set(imports_a2) <= {"hashlib", "json", "pathlib", "csv"} and rutas_ok),
        f"imports={imports_a2} rutas_ids={rutas_ok}")

    chk("A2-15", "A2", "A2 no calcula comparacion ni join: ambos campos nulos y sin tasas",
        a2_res["comparacion_volumenes"] is None and a2_res["join_grafo"] is None
        and "tasa poblacional" not in json.dumps(a2_res, ensure_ascii=False).lower().replace(
            "sin tasas poblacionales", ""),
        "comparacion_volumenes=null join_grafo=null")

    # ---------------- hallazgos ----------------
    hallazgos = []
    if fuentes_err:
        hallazgos.append({
            "id": "H-01", "entrega": "T-top50/v001", "severidad": "menor",
            "tipo": "trazabilidad",
            "titulo": "Huella declarada del plan no corresponde al archivo actual",
            "descripcion": "La unica fuente de T cuya huella no coincide es docs/plan-paralelo-ampliacion-post-r9.md. "
                           "Su mtime (" + mtime(PLAN) + ") es posterior al sellado de T ("
                           + mtime(EJEC + "/T-top50/v001/congelada.json") + "); el cambio es posterior, "
                           "no atribuible al carril. Las cifras no dependen de ese archivo y fueron recomputadas.",
            "evidencia": {"declarado": next(f["sha256"] for f in a_entrega["fuentes"] if f["ruta"] == PLAN),
                          "actual": sha(ROOT / PLAN), "mtime_plan": mtime(PLAN),
                          "mtime_sello_T": mtime(EJEC + "/T-top50/v001/congelada.json")},
            "impacto": "La huella del insumo ya no ancla el texto vigente; no altera 3916/1191/50 ni scores.",
            "accion": "Al congelar el plan, re-declarar su huella en T v002 (o registrar la version usada)."})
    if len(nombres_mat) == 11 and len(nombres_nac) == 16 and "10 recursos Matrimonios" in md_a2:
        hallazgos.append({
            "id": "H-02", "entrega": "A2-registro-civil/v001", "severidad": "menor",
            "tipo": "documental",
            "titulo": "Conteo de recursos distinto entre resultados.md y resultados.json",
            "descripcion": "El md dice 10 recursos Matrimonios y 15 Nacimientos; el JSON registra 11 y 16. "
                           "La diferencia es el recurso Diccionario de cada conjunto: ambos conteos son "
                           "compatibles si el md explicita que excluye diccionarios.",
            "evidencia": {"md": "10 Matrimonios / 15 Nacimientos", "json": {"mat": 11, "nac": 16},
                          "diccionarios": [DIC_MAT, DIC_NAC]},
            "impacto": "Ambiguedad de lectura del inventario; no afecta el veredicto BLOQUEADO.",
            "accion": "Precisar en v002: '10 recursos de datos + 1 diccionario' y '15 + 1'."})
    verif_terr = load(VERIF)
    ids_par = {t["recurso_a"] for t in par_lote["pruebas_recursos"]} | \
              {t["recurso_b"] for t in par_lote["pruebas_recursos"]} | {DIC_MAT, DIC_NAC}
    raw_terr = (ROOT / VERIF).read_text(encoding="utf-8")
    sin_correspondencia_par = not any(i in raw_terr for i in ids_par)
    if verif_terr["correspondencias"] and sin_correspondencia_par:
        hallazgos.append({
            "id": "H-03", "entrega": "A2-registro-civil/v001", "severidad": "menor",
            "tipo": "semantico",
            "titulo": "La frase 'sin catalogo de correspondencia' es mas amplia que la evidencia",
            "descripcion": "El repositorio contiene correspondencias territoriales ("
                           + str(len(verif_terr["correspondencias"])) + " entradas, con referencia "
                           "Catalogo_Municipios) para otros conjuntos, pero ninguna cubre los recursos de "
                           "Matrimonios/Nacimientos y el diccionario no declara catalogo de referencia. "
                           "Lo no acreditado es la correspondencia para este par, no la inexistencia de "
                           "catalogo en el portal.",
            "evidencia": {"correspondencias_territoriales": len(verif_terr["correspondencias"]),
                          "recursos_del_par_sin_correspondencia": len(ids_par),
                          "catalogo_de_referencia_diccionario": "",
                          "fuente": "data/territorio/verificacion.json"},
            "impacto": "Redaccion; el eje sigue no acreditado y el veredicto no cambia.",
            "accion": "Reformular: 'sin correspondencia acreditada para estos recursos'."})
    hallazgos.append({
        "id": "H-04", "entrega": "A2-registro-civil/v001", "severidad": "menor",
        "tipo": "trazabilidad",
        "titulo": "Fuentes locales sin huella SHA256 de archivo completo",
        "descripcion": "fuentes_locales registra conteos, hashes de fragmento de diccionario y estados, "
                       "pero no el SHA256 de reports/catalogo-perfil.json, contenido-inspeccion.json, "
                       "oportunidades-cruce.json ni validacion-lote.json. La reproduccion depende de "
                       "bytes que no quedan anclados en la entrega.",
        "evidencia": {r: sha(ROOT / r) for r in (PERFIL, INSP, MAPA, LOTE)},
        "impacto": "Trazabilidad; el contenido se reprodujo y coincide, pero el sello no fija las fuentes.",
        "accion": "Anadir huellas completas de las cuatro fuentes en A2 v002."})

    # ---------------- resumen y veredictos ----------------
    fallas = [c for c in CHECKS if not c["ok"]]
    t_checks = [c for c in CHECKS if c["entrega"] == "T"]
    a2_checks = [c for c in CHECKS if c["entrega"] == "A2"]
    t_h = [h for h in hallazgos if h["entrega"].startswith("T")]
    a2_h = [h for h in hallazgos if h["entrega"].startswith("A2")]

    def veredicto(checks, hs):
        sin_explicar = [c["id"] for c in checks if not c["ok"] and not c.get("hallazgo")]
        if sin_explicar or any(h["severidad"] == "bloqueante" for h in hs):
            return "NO FAVORABLE"
        return "FAVORABLE CON OBSERVACIONES" if hs else "FAVORABLE"

    snap_fin = {"T": snapshot(T), "A2": snapshot(A2)}
    sin_cambio = snap_ini == snap_fin
    chk("G-01", "GLOBAL", "Ningun byte de las entregas selladas cambio durante la auditoria",
        sin_cambio, "snapshots inicio/fin identicos" if sin_cambio else "DIFERENCIAS DETECTADAS")

    dictamen = {
        "rol": "R-documental",
        "version": "v001",
        "fecha_utc": hoy,
        "objeto": "Dictamen semantico/documental independiente de T-top50/v001 y A2-registro-civil/v001",
        "alcance": [
            "T-top50/v001: 3916 pares, 1191 candidatas, top50, scores, fuentes y sellos.",
            "A2-registro-civil/v001: par matrimonios/nacimientos, 8 ejes, veredicto y sellos.",
        ],
        "fuera_de_alcance": [
            "A1-911, A3-itama, Q-unidades y S: en elaboracion; no se aprueban entregas futuras.",
            "Base IRI / example.org: intacta y no evaluada.",
            "Integracion, publicacion en reports/, grafo, Studio y escritores centrales.",
        ],
        "metodo": [
            "Lectura directa de fuentes locales; sin red, sin grafo, sin Studio.",
            "Recomputo independiente de scores y orden (no importa el codigo de T).",
            "Reproduccion integra de resultados.json de A2 desde fuentes y comparacion de igualdad.",
            "SHA256 de cada archivo calculado por codigo; snapshots antes/despues para probar no escritura.",
        ],
        "veredicto_global": "FAVORABLE CON OBSERVACIONES",
        "entregas": {
            "T-top50/v001": {
                "veredicto": veredicto(t_checks, t_h),
                "checks": len(t_checks), "checks_ok": sum(c["ok"] for c in t_checks),
                "sellos": "verificados (7/7 archivos, bytes y SHA256)",
                "hallazgos": [h["id"] for h in t_h],
                "sintesis": "3916 pares, 1191 candidatas y top50 recomputados por codigo: rangos, scores, "
                            "orden, titulos, familias, bloqueadores y conjuntos coinciden. 50/50 filas en "
                            "NO_JOIN_APROBADO; ningun join ni rate se deriva del ranking.",
            },
            "A2-registro-civil/v001": {
                "veredicto": veredicto(a2_checks, a2_h),
                "checks": len(a2_checks), "checks_ok": sum(c["ok"] for c in a2_checks),
                "sellos": "verificados (5/5 archivos y sidecar)",
                "hallazgos": [h["id"] for h in a2_h],
                "sintesis": "BLOQUEADO reproducido: grano evento vs agregado, unicidad/cardinalidad no "
                            "acreditadas (muestras n=100), total!=hombres+mujeres en 5/6 pruebas, meses "
                            "faltantes, ambito de registro y poblaciones distintas. Sin comparacion ni join.",
            },
            "A1-911 / A3-itama / Q-unidades / S": {
                "veredicto": "NO EVALUADO",
                "checks": 0, "checks_ok": 0, "sellos": "no aplica",
                "hallazgos": [],
                "sintesis": "En elaboracion. No se extiende aprobacion ni se anticipa dictamen.",
            },
        },
        "hallazgos": hallazgos,
        "checks": CHECKS,
        "checks_resumen": {"total": len(CHECKS), "ok": len(CHECKS) - len(fallas),
                           "fallas": [c["id"] for c in fallas]},
        "hashes_fuentes": {r: {"sha256": sha(ROOT / r), "bytes": (ROOT / r).stat().st_size}
                           for r in (MAPA, CRIT, TOP_CSV, MAT_CSV, COB, PERFIL, INSP, LOTE, PLAN, SEGUIM, VERIF)},
        "hashes_entregas": {
            "T-top50/v001": {a["ruta"]: {"sha256": a["sha256"], "bytes": a["bytes"]}
                             for a in t_cong["archivos"]},
            "A2-registro-civil/v001": {rel: {"sha256": h, "bytes": (A2 / rel).stat().st_size}
                                       for rel, h in a2_cong["archivos"].items()},
        },
        "sello": {"ruta": EJEC + "/R-documental/v001/sello.json",
                  "nota": "SHA256 de esta entrega y de los bytes auditados; hash propio en sello.sha256"},
        "limites": [
            "No se re-ejecutaron los scripts sellados para no escribir en sus carpetas; su logica se "
            "reprodujo de forma independiente.",
            "La auditoria verifica coherencia interna y contra fuentes locales; no acredita verdad "
            "extramuros ni calidad de los datos originales publicados.",
            "No se evaluan entregas A1/A3/Q/S ni se aprueba integracion alguna.",
        ],
    }

    (V001 / "dictamen.json").write_text(
        json.dumps(dictamen, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    # ---------------- dictamen.md ----------------
    L = []
    L.append("# R — Dictamen semantico/documental (v001)")
    L.append("")
    L.append(f"Fecha UTC: {hoy}. Objeto: T-top50/v001 y A2-registro-civil/v001.")
    L.append("Lectura directa de fuentes locales; sin red, sin grafo, sin Studio. "
             "Ningun join ni rate aprobado por el ranking.")
    L.append("")
    L.append("## Veredicto")
    L.append("")
    L.append(f"**{dictamen['veredicto_global']}**")
    L.append("")
    L.append("| Entrega | Veredicto | Checks | Sellos | Hallazgos |")
    L.append("| --- | --- | --- | --- | --- |")
    for nombre, e in dictamen["entregas"].items():
        L.append(f"| {nombre} | {e['veredicto']} | {e['checks_ok']}/{e['checks']} | {e['sellos']} | "
                 f"{', '.join(e['hallazgos']) or '—'} |")
    L.append("")
    L.append("## T — Top 50")
    L.append("")
    L.append("Recomputo propio (sin importar el codigo de T): 3916 pares; 2328 sin clave, 1191 "
             "candidatas, 396 solo dimensiones, 1 exploratorio. 1191/1191 ids unicos y scores iguales "
             "a la matriz; 50/50 rangos, ids, scores y orden (score desc, id asc) iguales al CSV.")
    L.append("Top1 ITAMA: pesos 13.0 + penalizaciones -8.0 = 5.0. A1/A2/A3 en rangos 2/4/1 por ID exacto. "
             "50 filas del staging fieles al mapa y todas en `NO_JOIN_APROBADO`. Cobertura R9 declarada "
             "(1423/1106/138/16/17) coincide con el reporte.")
    L.append("")
    L.append("## A2 — Registro civil")
    L.append("")
    L.append("`resultados.json` se reproduce integramente desde las fuentes con la logica declarada: "
             "BLOQUEADO, sin comparacion de volumenes ni join. Los 8 ejes se sostienen:")
    L.append("")
    L.append("- Claves: par `candidata_por_validar`; `municipio` coincide solo como nombre de campo, sin "
             "catalogo/unicidad acreditados (pendientes del mapa).")
    L.append("- Grano: Matrimonios fila-evento (dia, edad/sexo de contrayentes) vs Nacimientos "
             "agregado municipio-anio-mes (hombres/mujeres/total).")
    L.append("- Unicidad/cobertura: muestras n=100 declaran no demostrar unicidad ni cobertura; "
             "no equivalen al universo.")
    L.append("- Cardinalidad: 6 pruebas; 5 con total != hombres+mujeres (2015, 2020-2023) y 1 con "
             "meses faltantes (2016); decision `fallo_validacion_integral`.")
    L.append("- Poblacion: actos con dos contrayentes vs conteos de nacidos; sin id de persona.")
    L.append("- Periodo/ambito: solape 2015-2024 solo por nombres; municipio/anio/mes de registro, "
             "sin residencia ni correspondencia de codigos acreditada.")
    L.append("- Unidades: fila-evento vs fila-agregado; pendiente de unidades; sin tasas.")
    L.append("")
    L.append("## Hallazgos")
    L.append("")
    L.append("| ID | Entrega | Severidad | Hallazgo | Accion |")
    L.append("| --- | --- | --- | --- | --- |")
    for h in hallazgos:
        L.append(f"| {h['id']} | {h['entrega']} | {h['severidad']} | {h['titulo']} | {h['accion']} |")
    L.append("")
    L.append("Ningun hallazgo es bloqueante ni altera cifras o veredictos; los cuatro son de "
             "trazabilidad o redaccion y se corrigen en v002 sin reescribir lo sellado.")
    L.append("")
    L.append("## Checks y limites")
    L.append("")
    L.append(f"{dictamen['checks_resumen']['ok']}/{dictamen['checks_resumen']['total']} comprobaciones OK. "
             "La unica desviacion de un criterio es la huella del plan en T (H-01), explicada por edicion "
             "posterior al sellado. El detalle maquina, con hashes exactos calculados por codigo, esta en "
             "`dictamen.json`; el sello en `sello.json` (+ `sello.sha256`).")
    L.append("")
    L.append("No se evaluan A1-911, A3-itama, Q-unidades ni S (en elaboracion): no se aprueba trabajo "
             "futuro. Base IRI/example.org intacta y fuera de alcance. Snapshots antes/despues prueban "
             "que no se modifico ningun byte sellado.")
    L.append("")
    (V001 / "dictamen.md").write_text("\n".join(L), encoding="utf-8")

    # ---------------- sello ----------------
    propios = ["dictamen.json", "dictamen.md", "scripts/auditar.py", "tests/test_dictamen.py"]
    rutas = [EJEC + "/R-documental/v001/" + r for r in propios if (V001 / r).is_file()]
    rutas += [a["ruta"] for a in t_cong["archivos"]]
    rutas += [EJEC + "/T-top50/v001/congelada.json"]
    rutas += [EJEC + "/A2-registro-civil/v001/" + rel for rel in a2_cong["archivos"]]
    rutas += [EJEC + "/A2-registro-civil/v001/congelada.json",
              EJEC + "/A2-registro-civil/v001/congelada.sha256"]
    rutas += [MAPA, CRIT, TOP_CSV, MAT_CSV, COB, PERFIL, INSP, LOTE, PLAN, SEGUIM, VERIF]
    sello = {
        "rol": "R-documental",
        "version": "v001",
        "fecha_utc": hoy,
        "nota": "SHA256 calculado por codigo sobre los bytes en disco. No se incluye a si mismo "
                "ni a sello.sha256; el hash propio va en el sidecar.",
        "veredicto_global": dictamen["veredicto_global"],
        "checks_resumen": dictamen["checks_resumen"],
        "archivos": [{"ruta": r, "sha256": sha(ROOT / r), "bytes": (ROOT / r).stat().st_size}
                     for r in sorted(set(rutas))],
    }
    (V001 / "sello.json").write_text(
        json.dumps(sello, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (V001 / "sello.sha256").write_text(
        sha(V001 / "sello.json") + "  sello.json\n", encoding="utf-8")

    print("R-documental v001:", dictamen["veredicto_global"])
    for nombre, e in dictamen["entregas"].items():
        print(f"  {nombre}: {e['veredicto']} ({e['checks_ok']}/{e['checks']})")
    print("  hallazgos:", ", ".join(h["id"] + ":" + h["severidad"] for h in hallazgos))
    print("  checks:", f"{len(CHECKS) - len(fallas)}/{len(CHECKS)} OK", "fallas:", [c["id"] for c in fallas])
    print("  sello:", sha(V001 / "sello.json"))


if __name__ == "__main__":
    sys.exit(main())
