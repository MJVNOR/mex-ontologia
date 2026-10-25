"""Cobertura operativa post-R9 v002: reporte reproducible en staging.

Solo lee produccion/expediente (nunca escribe fuera de la salida indicada).
Valida totales y estados contra la evidencia y falla si hay discrepancias.

Interfaces testeables:
  ROOT: raiz del proyecto (detectada por ontologia/semantica.json).
  leer_fuentes(root) -> dict con los 14 documentos fuente.
  comprobar_resumen(r9, cob): igualdad completa cobertura.resumen == R9.resumen_actual.
  comprobar_csv(filas): 5523 filas DictReader, IRIs unicas, Counter exacto.
  verificar_evidencia(c4ent, root) -> 104 (SHA fisico de cada evidencia_cotejada).
  construir_informe(f) -> dict (esquema operativo estable, sin metadatos de instalacion).
  generar(root, out_dir) -> dict con rutas de salida.

Uso staging (SIEMPRE con --out-dir explicito, nunca produccion):
  uv run python <este-archivo> --out-dir propuestas/cobertura-operativa-post-r9/ejecucion-20261024/B-cobertura/v002/salida
Instalado genera en reports/ por defecto; tambien acepta --out-dir y --root.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "ontologia" / "semantica.json").exists())
FECHA_BASE = "2026-10-24"  # estable; sin hora volatil

FUENTES = [
    "reports/ronda-9.json",
    "data/semantica/cobertura.json",
    "docs/plan-actualizado-tras-r9.json",
    "docs/plan-actualizado-tras-r9.md",
    "propuestas/plan-tras-r8/ejecucion-20261024/C1-candidatas/v001/entrega.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/totales-cruces-observaciones.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/entrega.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/matriz-columnas-5523.csv",
    "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/entrega.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/recibos/portal-carga.json",
    "propuestas/plan-tras-r8/ejecucion-20261024/recibos/studio-portal-sync.json",
    "reports/ronda-6.json",
    "reports/ronda-6.md",
]

OBS_IDS = ["egresos-descripcion-urgencias", "municipio-formato-ejemplo",
           "fecha-ejemplo-numerico", "anio-nacimientos-2024", "anio-divorcios-2023"]
ESPERADO_ESTADOS = {"documental_revisada": 4506, "candidata_por_nombre": 17,
                    "sin_definicion_coincidente": 833,
                    "definicion_sin_interpretacion_compartida": 154,
                    "sin_diccionario_en_conjunto": 13}

COND_138 = ("Diccionario corregido, codebook, instrumento o respuesta del publicador "
            "que vincule pregunta/campo, codificación, recurso y edición local.")
REF_138 = ("docs/plan-actualizado-tras-r9.md §Pendientes documentales (fila 138 significados); "
           "revisión individual R8 en reports/investigacion-post-r6.md; "
           "motivos 104+34+2 en C3 totales-cruces-observaciones.json:variables_pendientes.")
COND_OBS = ("Evidencia del publicador o diccionario corregido para el conflicto de "
            "urgencias/egresos, formato CVE_MUN, fecha numérica, encabezado a–o y alias "
            "de año de Divorcios 2023.")
REF_OBS = ("docs/plan-actualizado-tras-r9.md §Pendientes documentales (fila cinco observaciones); "
           "localizador por observación en C3 totales-cruces-observaciones.json:observaciones.")
REF_C1 = ("propuestas/plan-tras-r8/ejecucion-20261024/C1-candidatas/v001/entrega.json:"
          "casos[].condicion_reapertura + resultado_global (0 promociones).")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leer_json(root, rel):
    return json.loads((Path(root) / rel).read_text(encoding="utf-8"))


def exigir(cond, msg):
    if not cond:
        raise ValueError("cobertura-operativa: " + msg)


def leer_fuentes(root):
    root = Path(root)
    d = {rel: leer_json(root, rel) for rel in FUENTES if rel.endswith(".json")}
    with open(root / FUENTES[7], encoding="utf-8", newline="") as f:
        d["csv_filas"] = list(csv.DictReader(f))  # DictReader: hay saltos embebidos
    return d


def comprobar_resumen(r9, cob):
    exigir(r9.get("format_version") == 1 and r9.get("release") == "R9",
            "formato/release distintos de 1/R9")
    exigir(cob["resumen"] == r9["resumen_actual"],
            "drift: cobertura.resumen != R9.resumen_actual")
    ra = r9["resumen_actual"]
    exigir(ra["estados_variables"]["respaldada_por_definicion"] == 1423, "significados != 1423")
    exigir(ra["conceptos_compartidos"] == 1106, "conceptos != 1106")
    exigir(ra["estados_correspondencias"] == {"documental_revisada": 4506,
            "candidata_por_nombre": 17}, "correspondencias != 4506/17")
    exigir(ra["columnas_totales_examinadas"] == 5523, "columnas != 5523")


def comprobar_csv(filas):
    exigir(len(filas) == 5523, f"CSV != 5523 filas ({len(filas)})")
    iris = [r["columna_iri"] for r in filas]
    exigir(len(set(iris)) == 5523, "columna_iri no unicas")
    exigir(Counter(r["estado_columna"] for r in filas) == Counter(ESPERADO_ESTADOS),
            "particion de estados distinta de 4506/17/833/154/13")


def verificar_evidencia(c4ent, root):
    n = 0
    for c in c4ent["casos"]:
        for ev in c.get("evidencia_cotejada", []):
            p = Path(root) / ev["ruta"]
            exigir(p.is_file(), f"evidencia ausente: {ev['ruta']}")
            exigir(sha(p) == ev.get("sha256"), f"SHA fisico distinto: {ev['ruta']}")
            n += 1
    exigir(n == 104, f"evidencias != 104 ({n})")
    return n


def comprobar(r9, cob, plan, c1ent, c3tot, c3ent, c4mat, c4ent, filas):
    comprobar_resumen(r9, cob)
    comprobar_csv(filas)
    exigir(r9["pendientes"]["significados_reales"] == 138, "pendientes != 138")
    exigir(r9["pendientes"]["vigencias"] == 16, "vigencias != 16")
    exigir(r9["pendientes"]["vigencias_acceso_no_resuelto"] == ["V13", "V14"],
            "V13/V14 no figuran como acceso no resuelto")
    exigir(r9["pendientes"]["referencia_catalogo"] == "des_mpo_res", "des_mpo_res ausente")
    exigir(r9["pendientes"]["encabezados_corruptos"] == 2, "headers != 2")
    exigir(r9.get("contactos_externos") == 0, "contactos externos != 0")
    col = c3tot["columnas"]
    exigir(col["con_correspondencia"] == 4523 == 4506 + 17, "con_correspondencia != 4523")
    exigir(c3ent["resultados"]["reconciliacion_columnas"]["verificado"] is True,
            "C3 no marca reconciliacion verificada")
    d = c3tot["definiciones"]
    exigir((d["con_nombre_examinadas"], d["respaldada_por_definicion"],
             d["fuera_del_nucleo_actual"], d["candidata_sin_definicion_suficiente"])
            == (1563, 1423, 124, 16), "ecuacion 1563 rota")
    vp = c3tot["variables_pendientes"]
    exigir(vp["total"] == 140 and "138" in vp["equivale_a"], "140 != 138+2")
    exigir(vp["motivos"] == {"dominio_o_medida_sin_regla_revisada": 34,
            "descripcion_vacia_o_pendiente": 104, "pista_sin_interpretacion_revisada": 2},
            "motivos 104+34+2 rotos")
    exigir([o["id"] for o in c3tot["observaciones"]] == OBS_IDS, "5 observaciones inexactas")
    exigir([o["id"] for o in cob["observaciones_revision"]] == OBS_IDS,
            "observaciones cobertura.json inexactas")
    exigir(plan["base_actual"]["columnas"]["total"] == 5523, "plan R9 total != 5523")
    exigir(plan["pendientes_condicionados"]["vigencias_acceso_no_resuelto"] == ["V13", "V14"],
            "plan sin V13/V14")
    casos = c4ent["casos"]
    exigir(len(casos) == 19, "casos C4 != 19")
    exigir(sum(1 for c in casos if c["tipo"] == "vigencias") == 16, "vigencias C4 != 16")
    exigir(sum(1 for c in casos if c["tipo"] == "anomalias") == 3, "anomalias C4 != 3")
    exigir(c4ent["resumen"]["propuestas_para_integrar"] == 0, "C4 propone integrar != 0")
    exigir([n["id"] for n in c4mat["necesidades"]]
            == ["ND-01", "ND-02", "ND-03", "ND-04", "ND-05", "ND-06", "ND-07"],
            "necesidades != 7")
    exigir([p["id"] for p in c4mat["preguntas"]]
            == ["PQ-01", "PQ-02", "PQ-03", "PQ-04", "PQ-05", "PQ-06", "PQ-07"],
            "preguntas != 7")
    exigir(all(c.get("afirmacion_propuesta") is None for c in casos),
            "hay afirmacion propuesta donde debe haber brecha externa")
    exigir(c1ent["resumen"]["casos_cubiertos"] == 17, "C1 casos != 17")
    exigir(c1ent["resumen"]["promociones_propuestas"] == 0, "C1 propone promociones")
    exigir(all(c.get("condicion_reapertura") for c in c1ent["casos"]),
            "candidata sin condicion de reapertura")
    exigir("negativo" in r9["pilotos"]["P2"] and "negativo" in r9["pilotos"]["P3"],
            "P2/P3 no negativos")
    exigir(r9["consultas_afectadas"]["resultado"]["declaraciones"] == 2,
            "declaraciones QUDT != 2")


def frentes(c4ent, c4mat, c1ent, c3tot, cob):
    mat = {n["id"]: n for n in c4mat["necesidades"]}
    pq = {}
    for p in c4mat["preguntas"]:
        pq.setdefault(p["necesidad"], []).append(p["id"])
    out = []
    for c in c4ent["casos"]:
        nd = next((n for n in c4mat["necesidades"] if c["id"] in n.get("casos", [])), None)
        out.append({
            "frente": c["id"], "tipo": c["tipo"], "estado": c["estado"],
            "necesidad": nd["id"] if nd else None,
            "organismo": nd["organismo"]["nombre"] if nd else None,
            "condicion_reapertura": c.get("condicion_reapertura"),
            "referencia_exacta": (f"C4 entrega.json:casos[id={c['id']}]"
                                  + (f" + matriz-preguntas.json:{nd['id']}" if nd else "")),
            "evidencia": [{"ruta": e["ruta"], "sha256": e.get("sha256"),
                           "localizador": e.get("localizador")}
                          for e in c.get("evidencia_cotejada", [])]})
    out.append({"frente": "significados-138", "tipo": "significados", "estado": "pendientes",
                "condicion_reapertura": COND_138, "referencia_exacta": REF_138,
                "evidencia": [], "motivos": {"104": "descripcion_vacia_o_pendiente",
                 "34": "dominio_o_medida_sin_regla_revisada",
                 "2": "pista_sin_interpretacion_revisada"}})
    out.append({"frente": "candidatas-17", "tipo": "candidatas", "estado": "candidatas",
                "condicion_reapertura": None,  # por item abajo; frente agrupa
                "referencia_exacta": REF_C1,
                "evidencia": [],
                "items": [{"columna": c["id"], "campo": c["campo"], "recurso": c["recurso"],
                           "condicion_reapertura": c["condicion_reapertura"]}
                          for c in c1ent["casos"]]})
    obs_txt = {o["id"]: o["observacion"] for o in cob["observaciones_revision"]}
    for o in c3tot["observaciones"]:
        out.append({"frente": o["id"], "tipo": "observacion_esquema",
                    "estado": o["estado"], "recurso": o["recurso"], "campo": o["campo"],
                    "observacion": obs_txt[o["id"]],
                    "condicion_reapertura": COND_OBS, "referencia_exacta": REF_OBS,
                    "evidencia": [{"ruta": o["fuente_esquema"], "localizador": o["localizador"]}]})
    return out, [{"id": n["id"], "organismo": n["organismo"]["nombre"],
                  "casos": n["casos"], "preguntas": pq.get(n["id"], []),
                  "documento_pedido": n["documento_pedido"], "estado_envio": "no_enviada"}
                 for n in c4mat["necesidades"]]


def construir_informe(f, root):
    r9, cob, plan = f["reports/ronda-9.json"], f["data/semantica/cobertura.json"], \
        f["docs/plan-actualizado-tras-r9.json"]
    c1ent = f["propuestas/plan-tras-r8/ejecucion-20261024/C1-candidatas/v001/entrega.json"]
    c3tot = f["propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/totales-cruces-observaciones.json"]
    c3ent = f["propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/entrega.json"]
    c4mat = f["propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json"]
    c4ent = f["propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/entrega.json"]
    comprobar(r9, cob, plan, c1ent, c3tot, c3ent, c4mat, c4ent, f["csv_filas"])
    n_ev = verificar_evidencia(c4ent, root)
    fr, necesidades = frentes(c4ent, c4mat, c1ent, c3tot, cob)
    exigir(all(x.get("condicion_reapertura") or
                (x["frente"] == "candidatas-17" and
                 all(i.get("condicion_reapertura") for i in x["items"]))
                for x in fr), "frente sin condicion de reapertura")
    exigir(all(x.get("referencia_exacta") for x in fr), "frente sin referencia exacta")
    return {
        "format_version": 1,
        "release": "R9",
        "fecha_base": FECHA_BASE,
        "estado": "cobertura_operativa_validada_sin_cambios_al_grafo",
        "indicadores": {
            "significados_respaldados": 1423, "conceptos": 1106,
            "correspondencias_revisadas": 4506, "candidatas": 17, "ambiguas": 0,
            "columnas_totales": 5523,
            "ecuacion_columnas": "5523=4506+17+833+154+13",
            "particion_columnas": dict(sorted(Counter(
                r["estado_columna"] for r in f["csv_filas"]).items())),
            "columnas_con_correspondencia": 4523,
            "definiciones_con_nombre": 1563,
            "ecuacion_definiciones": "1563=1423+124+16",
        },
        "denominadores": {
            "significados_reales_pendientes": 138,
            "columnas_con_definicion_sin_interpretacion": 154,
            "advertencia": ("138 es nivel definición; 154 es nivel columna. "
                            "No sumar ni restar columnas como definiciones. "
                            "140 variables pendientes = 138+2 encabezados."),
            "variables_pendientes": 140,
            "encabezados_corruptos_fuera_del_conteo": {
                "filas": [177, 178], "huellas": ["4b17625c", "b5dbcdf5"],
                "recurso_diccionario": "33d0a99e-c721-496f-a05e-07646e9ae42a"},
        },
        "pendientes": {
            "vigencias": 16, "acceso_no_resuelto": ["V13", "V14"],
            "referencia_catalogo": "des_mpo_res",
            "candidatas_dependientes_de_evidencia": 17,
            "evidencias_c4_verificadas_sha_fisico": n_ev,
        },
        "frentes": fr,
        "necesidades_preguntas_no_enviadas": {
            "expediente": ("propuestas/plan-tras-r8/ejecucion-20261024/"
                           "C4-referencias/v002/matriz-preguntas.json"),
            "contactos_externos": 0, "items": necesidades},
        "notas_cerradas": {
            "presas_cat_estatal": ("Resuelta en R6 (cat_estatal/Clave → definición /4 "
                                   "Catalogo_estatal); no es vigencia. "
                                   "Evidencia: reports/ronda-6.md."),
            "qudt": ("2 declaraciones locales de unidad (Milímetros→MilliM, "
                     "Hectáreas→HA, mex:unidadQudt, alcance por definición). Sin "
                     "QuantityValue, valores, conversiones ni unidad global. hm³ "
                     "(Hectómetros cúbicos) sin término precoordinado verificado en "
                     "QUDT 3.5.3, fuera del grafo."),
            "p2_owl_time": "Negativo: 0 intervalos; faltan límites y referencia temporal.",
            "p3_jerarquia_clinica": ("Negativo: 101 conceptos caso-con-* sin respaldo "
                                     "para broader; 0 jerarquías."),
            "p4_shacl": "Exclusión significado documentado/candidato; admite ninguno.",
        },
        "fuentes": [{"ruta": rel, "sha256": (sha(Path(root) / rel)
                    if not rel.endswith(".csv") else sha(Path(root) / rel))}
                    for rel in FUENTES],
    }


def md(i):
    L = ["# Cobertura operativa R9", "",
         "Release R9, formato 1. Estado validado contra evidencia; sin cambios al grafo.",
         f"Fecha base: {i['fecha_base']}.", "",
         "## Indicadores",
         "- Significados respaldados: **1423**; conceptos: **1106**.",
         "- Correspondencias revisadas: **4506**; candidatas: **17**; ambiguas: **0**.",
         "- Columnas: **5523=4506+17+833+154+13** (IRIs únicas, partición verificada en CSV);",
         "  con correspondencia 4523=4506+17.",
         "- Definiciones con nombre: 1563=1423+124+16.",
         "- `cobertura.resumen == ronda-9.resumen_actual` verificado íntegro (sin drift).", "",
         "## Denominadores (no mezclar)",
         "- **138 significados reales** pendientes (nivel definición).",
         "- 154 columnas con definición sin interpretación (nivel columna).",
         "- 140 variables pendientes = 138+2 encabezados corruptos (filas 177/178).", "",
         "## Frentes con condición de reapertura y referencia exacta"]
    for x in i["frentes"]:
        L += [f"### {x['frente']} ({x['tipo']}, {x['estado']})",
              f"- Referencia: {x['referencia_exacta']}"]
        if x["frente"] == "candidatas-17":
            grupos = {}
            for it in x["items"]:
                grupos.setdefault(it["condicion_reapertura"], []).append(it)
            for cond, items in grupos.items():
                L.append(f"- Reapertura ({len(items)}): {cond}")
                for it in items:
                    L.append(f"  - `{it['columna'].split('%2F')[-1]}` campo `{it['campo']}` recurso `{it['recurso']}`")
        else:
            L.append(f"- Reapertura: {x['condicion_reapertura']}")
            if x.get("observacion"):
                L.append(f"- {x['observacion']}")
            for e in x.get("evidencia", []):
                L.append(f"  - `{e.get('ruta')}`"
                         + (f" sha `{e['sha256']}`" if e.get("sha256") else "")
                         + (f" — {e['localizador']}" if e.get("localizador") else ""))
        L.append("")
    L += ["## Necesidades y preguntas (7+7, no enviadas)",
          f"- Expediente: `{i['necesidades_preguntas_no_enviadas']['expediente']}`.",
          "- Contactos externos: 0. Remitir al expediente; no inventar."]
    for n in i["necesidades_preguntas_no_enviadas"]["items"]:
        L.append(f"- {n['id']} ({n['organismo']}, casos {', '.join(n['casos'])}): "
                 f"{n['documento_pedido']}")
    L += ["", "## Notas cerradas",
          f"- Presas: {i['notas_cerradas']['presas_cat_estatal']}",
          f"- QUDT: {i['notas_cerradas']['qudt']}",
          f"- P2: {i['notas_cerradas']['p2_owl_time']}",
          f"- P3: {i['notas_cerradas']['p3_jerarquia_clinica']}",
          f"- P4: {i['notas_cerradas']['p4_shacl']}", "",
          "## Fuentes (SHA-256)"]
    for s in i["fuentes"]:
        L.append(f"- `{s['ruta']}` `{s['sha256']}`")
    return "\n".join(L) + "\n"


def generar(root=ROOT, out_dir=None):
    root = Path(root)
    out = Path(out_dir) if out_dir else root / "reports"
    informe = construir_informe(leer_fuentes(root), root)
    out.mkdir(parents=True, exist_ok=True)
    pj, pm = out / "cobertura-operativa-r9.json", out / "cobertura-operativa-r9.md"
    pj.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pm.write_text(md(informe), encoding="utf-8")
    return {"json": str(pj), "md": str(pm)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args(argv)
    print(json.dumps(generar(a.root, a.out_dir), indent=2))


if __name__ == "__main__":
    main()
