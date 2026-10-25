"""Cobertura operativa post-R9: reporte reproducible en staging.

Solo lee produccion/expediente (nunca escribe fuera de la salida indicada).
Valida totales y estados contra la evidencia y falla si hay discrepancias.

Interfaces testeables:
  ROOT: raiz del proyecto (detectada por ontologia/semantica.json).
  SALIDA_FUTURA: scripts/generar_cobertura_operativa.py -> reports/cobertura-operativa-r9.json/md.
  generar(root=ROOT, out_dir=...) -> dict con rutas de salida (usado por tests).
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "ontologia" / "semantica.json").exists())
# Nombre de instalacion posterior (NO instalar ahora): scripts/generar_cobertura_operativa.py
# Salida futura: reports/cobertura-operativa-r9.json y reports/cobertura-operativa-r9.md
FECHA_BASE = "2026-10-24"  # estable; sin hora volatil

FUENTES = [
    "reports/ronda-9.json",
    "data/semantica/cobertura.json",
    "docs/plan-actualizado-tras-r9.json",
    "docs/plan-actualizado-tras-r9.md",
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


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leer_json(root, rel):
    return json.loads((Path(root) / rel).read_text(encoding="utf-8"))


def exigir(cond, msg):
    if not cond:
        raise ValueError("cobertura-operativa: " + msg)


def comprobar(r9, cob, plan, c3tot, c3ent, c4mat, c4ent, n_csv):
    ra = r9["resumen_actual"]
    exigir(r9.get("format_version") == 1 and r9.get("release") == "R9",
            "formato/release distintos de 1/R9")
    exigir(ra["estados_variables"]["respaldada_por_definicion"] == 1423, "significados != 1423")
    exigir(ra["conceptos_compartidos"] == 1106, "conceptos != 1106")
    exigir(ra["estados_correspondencias"] == {"documental_revisada": 4506,
            "candidata_por_nombre": 17}, "correspondencias != 4506/17")
    exigir(r9["pendientes"]["significados_reales"] == 138, "pendientes != 138")
    exigir(r9["pendientes"]["vigencias"] == 16, "vigencias != 16")
    exigir(r9["pendientes"]["vigencias_acceso_no_resuelto"] == ["V13", "V14"],
            "V13/V14 no figuran como acceso no resuelto")
    exigir(r9["pendientes"]["referencia_catalogo"] == "des_mpo_res", "des_mpo_res ausente")
    exigir(r9["pendientes"]["encabezados_corruptos"] == 2, "headers != 2")
    exigir(r9.get("contactos_externos") == 0, "contactos externos != 0")
    col = c3tot["columnas"]
    exigir(col["total"] == 5523 and col["documental_revisada"] == 4506
            and col["candidata_por_nombre"] == 17 and col["sin_definicion_coincidente"] == 833
            and col["definicion_sin_interpretacion_compartida"] == 154
            and col["sin_diccionario_en_conjunto"] == 13, "ecuacion 5523 rota en C3")
    exigir(4506 + 17 + 833 + 154 + 13 == 5523, "5523 != 4506+17+833+154+13")
    exigir(col["con_correspondencia"] == 4523 == 4506 + 17, "con_correspondencia != 4523")
    exigir(n_csv == 5523, "CSV != 5523 filas")
    exigir(c3ent["resultados"]["reconciliacion_columnas"]["verificado"] is True,
            "C3 no marca reconciliacion verificada")
    d = c3tot["definiciones"]
    exigir((d["con_nombre_examinadas"], d["respaldada_por_definicion"],
             d["fuera_del_nucleo_actual"], d["candidata_sin_definicion_suficiente"])
            == (1563, 1423, 124, 16), "ecuacion 1563 rota")
    exigir(1423 + 124 + 16 == 1563, "1563 != 1423+124+16")
    vp = c3tot["variables_pendientes"]
    exigir(vp["total"] == 140, "variables pendientes != 140")
    exigir("138" in vp["equivale_a"] and "2 filas corruptas" in vp["equivale_a"],
            "140 != 138+2 sin marcar")
    exigir(vp["motivos"] == {"dominio_o_medida_sin_regla_revisada": 34,
            "descripcion_vacia_o_pendiente": 104, "pista_sin_interpretacion_revisada": 2},
            "motivos 104+34+2 rotos")
    exigir(c3tot["conceptos_compartidos"] == 1106, "conceptos C3 != 1106")
    exigir([o["id"] for o in c3tot["observaciones"]] == OBS_IDS, "5 observaciones inexactas")
    exigir([o["id"] for o in cob["observaciones_revision"]] == OBS_IDS,
            "observaciones cobertura.json inexactas")
    exigir(cob["resumen"]["columnas_totales_examinadas"] == 5523, "cobertura.json total != 5523")
    exigir(cob["auditoria_cobertura"]["estados_columnas"]["definicion_sin_interpretacion_compartida"]
            == 154, "154 columnas mal contadas")
    # 154 es nivel columna; 138 es nivel definicion: denominadores distintos, no se suman.
    exigir(cob["auditoria_cobertura"]["variables_pendientes"] == 140, "140 != 138+2 en auditoria")
    exigir(plan["base_actual"]["columnas"]["total"] == 5523, "plan R9 total != 5523")
    exigir(plan["pendientes_condicionados"]["vigencias_acceso_no_resuelto"] == ["V13", "V14"],
            "plan sin V13/V14")
    casos = c4ent["casos"]
    exigir(len(casos) == 19, "casos C4 != 19")
    exigir(sum(1 for c in casos if c["tipo"] == "vigencias") == 16, "vigencias C4 != 16")
    exigir(sum(1 for c in casos if c["tipo"] == "anomalias") == 3, "anomalias C4 != 3")
    exigir(sum(len(c.get("evidencia_cotejada", [])) for c in casos) == 104,
            "evidencias C4 != 104")
    exigir(c4ent["resumen"]["propuestas_para_integrar"] == 0, "C4 propone integrar != 0")
    exigir([n["id"] for n in c4mat["necesidades"]]
            == ["ND-01", "ND-02", "ND-03", "ND-04", "ND-05", "ND-06", "ND-07"],
            "necesidades != 7")
    exigir([p["id"] for p in c4mat["preguntas"]]
            == ["PQ-01", "PQ-02", "PQ-03", "PQ-04", "PQ-05", "PQ-06", "PQ-07"],
            "preguntas != 7")
    exigir(all(c.get("afirmacion_propuesta") is None for c in casos),
            "hay afirmacion propuesta donde debe haber brecha externa")
    exigir("negativo" in r9["pilotos"]["P2"] and "negativo" in r9["pilotos"]["P3"],
            "P2/P3 no negativos")
    exigir(r9["consultas_afectadas"]["resultado"]["declaraciones"] == 2,
            "declaraciones QUDT != 2")


def frente_c4(c4ent, c4mat):
    mat = {n["id"]: n for n in c4mat["necesidades"]}
    pq = {}
    for p in c4mat["preguntas"]:
        pq.setdefault(p["necesidad"], []).append(p["id"])
    frentes = []
    for c in c4ent["casos"]:
        nd = next((n for n in c4mat["necesidades"] if c["id"] in n.get("casos", [])), None)
        frentes.append({
            "caso": c["id"], "tipo": c["tipo"], "estado": c["estado"],
            "necesidad": nd["id"] if nd else None,
            "organismo": (nd["organismo"]["nombre"] if nd else None),
            "condicion_reapertura": c.get("condicion_reapertura"),
            "evidencia": [{"ruta": e["ruta"], "sha256": e.get("sha256"),
                           "localizador": e.get("localizador")}
                          for e in c.get("evidencia_cotejada", [])],
        })
    return frentes, [{"id": n["id"], "organismo": n["organismo"]["nombre"],
                       "casos": n["casos"], "preguntas": pq.get(n["id"], []),
                       "documento_pedido": n["documento_pedido"], "estado_envio": "no_enviada"}
                      for n in c4mat["necesidades"]]


def generar(root=ROOT, out_dir=None):
    root = Path(root)
    r9 = leer_json(root, "reports/ronda-9.json")
    cob = leer_json(root, "data/semantica/cobertura.json")
    plan = leer_json(root, "docs/plan-actualizado-tras-r9.json")
    c3tot = leer_json(root, "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/totales-cruces-observaciones.json")
    c3ent = leer_json(root, "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/entrega.json")
    c4mat = leer_json(root, "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json")
    c4ent = leer_json(root, "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/entrega.json")
    with open(root / "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/matriz-columnas-5523.csv",
              encoding="utf-8", newline="") as f:
        n_csv = sum(1 for _ in csv.reader(f)) - 1  # csv.reader: hay saltos embebidos
    comprobar(r9, cob, plan, c3tot, c3ent, c4mat, c4ent, n_csv)
    frentes, necesidades = frente_c4(c4ent, c4mat)
    fuentes = [{"ruta": rel, "sha256": sha(root / rel)} for rel in FUENTES]
    informe = {
        "format_version": 1,
        "release": "R9",
        "fecha_base": FECHA_BASE,
        "estado": "cobertura_operativa_validada_sin_cambios_al_grafo",
        "indicadores": {
            "significados_respaldados": 1423, "conceptos": 1106,
            "correspondencias_revisadas": 4506, "candidatas": 17, "ambiguas": 0,
            "columnas_totales": 5523,
            "ecuacion_columnas": "5523=4506+17+833+154+13",
            "columnas_con_correspondencia": 4523,
            "definiciones_con_nombre": 1563,
            "ecuacion_definiciones": "1563=1423+124+16",
        },
        "denominadores": {
            "significados_reales_pendientes": 138,
            "columnas_con_definicion_sin_interpretacion": 154,
            "advertencia": "138 es nivel definicion; 154 es nivel columna. No sumar ni restar columnas como definiciones. 140 variables pendientes = 138+2 headers.",
            "variables_pendientes": 140, "motivos": {"104": "descripcion_vacia_o_pendiente",
             "34": "dominio_o_medida_sin_regla_revisada", "2": "pista_sin_interpretacion_revisada"},
            "encabezados_corruptos_fuera_del_conteo": {
                "filas": [177, 178], "huellas": ["4b17625c", "b5dbcdf5"],
                "recurso_diccionario": "33d0a99e-c721-496f-a05e-07646e9ae42a"},
        },
        "pendientes": {
            "vigencias": 16, "acceso_no_resuelto": ["V13", "V14"],
            "referencia_catalogo": "des_mpo_res", "candidatas_dependientes_de_evidencia": 17,
            "observaciones_esquema": [
                {"id": o["id"], "recurso": o["recurso"], "campo": o["campo"],
                 "observacion": next(x["observacion"] for x in cob["observaciones_revision"]
                                     if x["id"] == o["id"]),
                 "fuente_esquema": o["fuente_esquema"], "localizador": o["localizador"]}
                for o in c3tot["observaciones"]],
        },
        "frentes": frentes,
        "necesidades_preguntas_no_enviadas": {
            "expediente": "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json",
            "contactos_externos": 0, "items": necesidades},
        "notas_cerradas": {
            "presas_cat_estatal": "Resuelta en R6 (cat_estatal/Clave -> definicion /4 Catalogo_estatal); no es vigencia. Evidencia: reports/ronda-6.md.",
            "qudt": "2 declaraciones locales de unidad (Milimetros->MilliM, Hectareas->HA, mex:unidadQudt, alcance por definicion). Sin QuantityValue, valores, conversiones ni unidad global. hm3 (Hectometros cubicos) sin termino precoordinado verificado en QUDT 3.5.3, fuera del grafo.",
            "p2_owl_time": "Negativo: 0 intervalos; faltan limites y referencia temporal.",
            "p3_jerarquia_clinica": "Negativo: 101 conceptos caso-con-* sin respaldo para broader; 0 jerarquias.",
            "p4_shacl": "Exclusion significado documentado/candidato; admite ninguno.",
        },
        "fuentes": fuentes,
        "instalacion_futura": {
            "script": "scripts/generar_cobertura_operativa.py",
            "salida": ["reports/cobertura-operativa-r9.json", "reports/cobertura-operativa-r9.md"],
            "nota": "No instalado; este staging solo escribe su salida propia."},
    }
    out = Path(out_dir) if out_dir else root / "propuestas/cobertura-operativa-post-r9/ejecucion-20261024/B-cobertura/salida"
    out.mkdir(parents=True, exist_ok=True)
    pj, pm = out / "cobertura-operativa-r9.json", out / "cobertura-operativa-r9.md"
    pj.write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pm.write_text(md(informe), encoding="utf-8")
    (out / "sello-archivos.json").write_text(json.dumps(
        {"fecha_base": FECHA_BASE, "archivos": {
            pj.name: sha(pj), pm.name: sha(pm)}}, indent=2) + "\n", encoding="utf-8")
    return {"json": str(pj), "md": str(pm)}


def md(i):
    L = ["# Cobertura operativa R9", "",
         "Release R9, formato 1. Estado validado contra evidencia; sin cambios al grafo.",
         f"Fecha base: {i['fecha_base']}.", "",
         "## Indicadores",
         f"- Significados respaldados: **1423**; conceptos: **1106**.",
         f"- Correspondencias revisadas: **4506**; candidatas: **17**; ambiguas: **0**.",
         f"- Columnas: **5523=4506+17+833+154+13**; con correspondencia 4523=4506+17.",
         f"- Definiciones con nombre: 1563=1423+124+16.", "",
         "## Denominadores (no mezclar)",
         "- **138 significados reales** pendientes (nivel definicion).",
         "- 154 columnas con definicion sin interpretacion (nivel columna): no son 154 definiciones.",
         "- 140 variables pendientes = 138+2 headers corruptos (filas 177/178, huellas 4b17625c/b5dbcdf5).", "",
         "## Vigencias y anomalias (16+3, 104 evidencias, 0 propuestas para integrar)",
         "- Acceso no resuelto: **V13, V14** (no reintentar descarga/token por vias agotadas; W-v003 definitivo).",
         "- `des_mpo_res`: catalogo aplicable sin identificar.",
         "- 7 necesidades (ND-01..ND-07) y 7 preguntas (PQ-01..PQ-07) preparadas y **no enviadas**;",
         "  expediente: `propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json`.",
         "- Contactos externos: 0.", ""]
    for f in i["frentes"]:
        L += [f"### {f['caso']} ({f['tipo']}, {f['estado']})",
              f"- Necesidad: {f['necesidad']}; organismo: {f['organismo']}.",
              f"- Reapertura: {f['condicion_reapertura']}"]
        for e in f["evidencia"]:
            L.append(f"  - `{e['ruta']}` sha `{e['sha256']}` — {e['localizador']}")
        L.append("")
    L += ["## Observaciones de esquema (5, pendientes de aclaracion)"]
    for o in i["pendientes"]["observaciones_esquema"]:
        L += [f"### {o['id']}",
              f"- Recurso `{o['recurso']}`, campo `{o['campo']}`.",
              f"- {o['observacion']}",
              f"- Esquema: {o['fuente_esquema']}", f"- {o['localizador']}", ""]
    L += ["## Notas cerradas",
          f"- Presas: {i['notas_cerradas']['presas_cat_estatal']}",
          f"- QUDT: {i['notas_cerradas']['qudt']}",
          f"- P2: {i['notas_cerradas']['p2_owl_time']}",
          f"- P3: {i['notas_cerradas']['p3_jerarquia_clinica']}",
          f"- P4: {i['notas_cerradas']['p4_shacl']}", "",
          "## Fuentes (SHA-256)"]
    for s in i["fuentes"]:
        L.append(f"- `{s['ruta']}` `{s['sha256']}`")
    L += ["", "Instalacion futura: `scripts/generar_cobertura_operativa.py` -> "
          "`reports/cobertura-operativa-r9.json/md`. No instalado."]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    import sys
    r = generar(sys.argv[1] if len(sys.argv) > 1 else ROOT,
                sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps(r, indent=2))
