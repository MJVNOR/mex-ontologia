"""R-documental v002: aclaracion del check T-07 y revision de carriles.

No modifica v001 ni ninguna entrega de autores. Solo lee y escribe en
propuestas/ampliacion-post-r9/ejecucion-20261024/R-documental/v002/.

Uso: uv run python propuestas/ampliacion-post-r9/ejecucion-20261024/R-documental/v002/scripts/aclarar_t07.py
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

V002 = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[6]
EJEC = "propuestas/ampliacion-post-r9/ejecucion-20261024"
V001 = EJEC + "/R-documental/v001"
T = EJEC + "/T-top50/v001"
MAPA = "data/portal/oportunidades-cruce.json"
TOP_CSV = "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001/prioridades_top50.csv"
SEGUIM = "reports/seguimiento-operativo-post-r9.json"

PARES = {
    "A1-911": "19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92",
    "A2-matrimonios-nacimientos": "1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5",
    "A3-itama": "27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848",
}
A3_TITULO = "Poblaci\u00f3n ITAMA Internamiento"
A3_TITULO_SIN_DIACRITICO = "Poblacion ITAMA Internamiento"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def main():
    hoy = datetime.now(timezone.utc).isoformat(timespec="seconds")
    mapa = load(MAPA)
    inv = {p["id"]: p for p in mapa["pares"]}
    top = {r["id"]: r for r in csv.DictReader(open(ROOT / TOP_CSV, encoding="utf-8"))}
    staging = load(T + "/top50-oportunidades-r9.json")
    filas = {f["id"]: f for f in staging["filas"]}
    v001 = load(V001 + "/dictamen.json")
    a3 = inv[PARES["A3-itama"]]

    evidencia = {
        "expresion_intermedia": A3_TITULO_SIN_DIACRITICO,
        "resultado_intermedio": a3["titulo_a"] == A3_TITULO_SIN_DIACRITICO,
        "expresion_corregida": A3_TITULO,
        "resultado_corregido": a3["titulo_a"] == A3_TITULO,
        "titulo_real": a3["titulo_a"],
        "diferencia": "literal sin diacritico frente a byte UTF-8 con U+00F3 en el titulo del mapa",
    }

    carriles = []
    for nombre, pid in PARES.items():
        p, r, f = inv[pid], top[pid], filas[pid]
        carriles.append({
            "carril": nombre, "id": pid, "rango": int(r["rango"]), "score": float(r["score"]),
            "rango_staging": f["rango"], "score_staging": f["score"],
            "titulo_a": p["titulo_a"], "titulo_b": p["titulo_b"],
            "carril_analitico_staging": f["carril_analitico"],
            "estado_staging": f["estado"],
        })
    n_con_carril = sum(1 for f in staging["filas"] if f["carril_analitico"])
    t07_v001 = next(c for c in v001["checks"] if c["id"] == "T-07")
    t08_v001 = next(c for c in v001["checks"] if c["id"] == "T-08b")

    doc = {
        "rol": "R-documental",
        "version": "v002",
        "tipo": "aclaracion_de_check_y_revision_de_logica",
        "fecha_utc": hoy,
        "preserva": {
            "v001": "bytes intactos; no se reescribe ni se re-sella lo entregado",
            "dictamen_json_sha256": sha(ROOT / V001 / "dictamen.json"),
            "dictamen_md_sha256": sha(ROOT / V001 / "dictamen.md"),
            "sello_json_sha256": sha(ROOT / V001 / "sello.json"),
            "sello_sha256_sidecar": (ROOT / V001 / "sello.sha256").read_text(encoding="utf-8").split()[0],
            "sidecar_coincide": (ROOT / V001 / "sello.sha256").read_text(encoding="utf-8").split()[0]
                                == sha(ROOT / V001 / "sello.json"),
        },
        "aclaracion_t07": {
            "pregunta": "Por que T-07 aparecio en false si el detalle A1(2,3.0) A2(4,3.0) A3(1,5.0) concuerda?",
            "causa": "Defecto del instrumento de auditoria, no de la entrega: el check comparaba el titulo "
                     "A3 contra un literal sin diacritico ('Poblacion'), mientras el mapa contiene "
                     "'Poblaci\u00f3n'. La igualdad de titulo fallaba aunque ID, rango y score ya coincidieran.",
            "evidencia": evidencia,
            "estado_en_v001_sellado": {
                "T-07_ok": t07_v001["ok"], "T-07_detalle": t07_v001["detalle"],
                "checks_total": v001["checks_resumen"]["total"],
                "checks_ok": v001["checks_resumen"]["ok"],
                "fallas": v001["checks_resumen"]["fallas"],
            },
            "por_que_sin_hallazgo": "Los hallazgos se reservan a defectos de la entrega auditada. Este era un "
                                    "defecto del auditor y se corrigio antes de sellar; no corresponde hallazgo "
                                    "contra T ni contra sus autores.",
            "corridas_intermedias": "La corrida preliminar mostro en false T-07, T-11, T-15, A2-05 y A2-11. "
                                    "T-11 quedo asociado al hallazgo H-01 (huella del plan desactualizada); "
                                    "T-15 y A2-05 eran literales del auditor (punto final y diacritico) y "
                                    "A2-11 usaba claves internas en vez de los nombres de eje de la ficha. "
                                    "Solo los bytes sellados constituyen entrega; las corridas intermedias no.",
            "regla_declarada_en_v001": "Una falla de check solo degrada el veredicto si no esta asociada a un "
                                       "hallazgo documentado; por eso T-11 no lo degrada y una falla sin "
                                       "explicacion si lo haria.",
        },
        "revision_carriles": {
            "metodo": "Identificacion por ID exacto contra el mapa; la etiqueta de carril es solo nominativa.",
            "filas": carriles,
            "cobertura_etiquetas": {"con_carril": n_con_carril, "sin_carril": len(staging["filas"]) - n_con_carril},
            "checks_que_lo_cubren": {
                "T-07": "presencia de los tres IDs, rango y score esperados y titulos del mapa",
                "T-08b": "carril_analitico exacto por ID y fidelidad de la fila (titulos, familias, bloqueadores, conjuntos)",
                "T-10": "estado NO_JOIN_APROBADO en las 50 filas; ningun join ni rate",
            },
            "T-08b_en_v001": {"ok": t08_v001["ok"], "detalle": t08_v001["detalle"]},
            "limites": "El carril no acredita comparabilidad, no autoriza join ni rate y no cambia por ranking.",
        },
        "regla_corregida_para_v002_de_autores": {
            "titulos": "Comparar por ID, rango y score; usar el titulo como contraste normalizado, nunca como "
                       "unica puerta de aceptacion.",
            "carriles": "Mantener el mapeo por ID exacto y exigir que las 47 filas restantes no lleven etiqueta.",
            "literales": "Tomar los literales de la fuente (UTF-8) en lugar de reescribirlos en el check.",
        },
        "no_aceptacion_de_bytes_futuros": {
            "T-top50/v002": "pendiente de sello; no evaluado",
            "A2-registro-civil/v002": "pendiente de sello; no evaluado",
            "A1-911/v002": "pendiente de sello; no evaluado",
            "A3-itama/v002": "pendiente de sello; no evaluado",
            "W/v002": "sellada por su autor con 6 normas oficiales 3.5.3; fuera de este encargo y sin bytes revisados aqui",
            "Q/v002 y S/v001": "en proceso; no evaluadas",
        },
        "siguiente_encargo": "Auditar T-top50/v002 y A2-registro-civil/v002 cuando esten selladas, y despues "
                             "A1-911/v002 y A3-itama/v002; sin editar autores ni produccion.",
        "hashes_fuentes": {r: sha(ROOT / r) for r in (MAPA, TOP_CSV, T + "/top50-oportunidades-r9.json", SEGUIM)},
    }

    (V002 / "aclaracion-t07.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    L = []
    L.append("# R-documental v002 — Aclaracion de T-07 y revision de carriles")
    L.append("")
    L.append(f"Fecha UTC: {hoy}. Preserva v001 byte a byte; no evalua entregas futuras.")
    L.append("")
    L.append("## Que paso con T-07")
    L.append("")
    L.append("T-07 aparecio en `false` en una corrida intermedia por un defecto del check, no de T: "
             "el titulo A3 se comparaba contra `Poblacion` (sin diacritico) y el mapa dice "
             "`Población`. ID, rango y score ya concordaban: A1 rango 2 score 3.0, A2 rango 4 score 3.0, "
             "A3 rango 1 score 5.0.")
    L.append("")
    L.append("En el v001 sellado T-07 esta en `true` (" + t07_v001["detalle"] + ") y el resumen es "
             f"{v001['checks_resumen']['ok']}/{v001['checks_resumen']['total']} sin fallas. "
             "No corresponde hallazgo contra T: el hallazgo H-01 es otro asunto (huella del plan).")
    L.append("")
    L.append("La misma corrida intermedia mostro T-11, T-15, A2-05 y A2-11 en false: T-11 quedo ligado a H-01; "
             "los otros tres eran literales del auditor (punto final, diacritico y nombres de eje). "
             "Solo cuentan los bytes sellados.")
    L.append("")
    L.append("## Carriles")
    L.append("")
    L.append("| Carril | ID | Rango | Score | Etiqueta staging | Estado |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for c in carriles:
        L.append(f"| {c['carril']} | `{c['id'][:8]}…` | {c['rango']} | {c['score']} | "
                 f"{c['carril_analitico_staging']} | {c['estado_staging']} |")
    L.append("")
    L.append(f"Solo {n_con_carril} de 50 filas llevan etiqueta; las otras {50 - n_con_carril} quedan sin carril. "
             "T-07 verifica presencia/rango/score/titulos por ID; T-08b verifica la etiqueta exacta y la fidelidad "
             "de la fila; T-10 mantiene NO_JOIN_APROBADO. El carril no acredita comparabilidad ni autoriza join o rate.")
    L.append("")
    L.append("## Regla corregida y limites")
    L.append("")
    L.append("Para v002 de los autores: comparar por ID, rango y score; usar titulos normalizados solo como "
             "contraste; tomar literales UTF-8 de la fuente; mantener el mapeo de carriles por ID exacto. "
             "Una falla de check solo degrada el veredicto si no esta asociada a un hallazgo documentado.")
    L.append("")
    L.append("No se aceptan bytes futuros: T/A2 v002 y A1/A3 v002 quedan pendientes de sello. W/v002 (6 normas "
             "3.5.3) esta fuera de este encargo y no se reviso aqui; Q/v002 y S/v001 siguen en proceso. "
             "No se editan autores ni produccion.")
    L.append("")
    (V002 / "aclaracion-t07.md").write_text("\n".join(L), encoding="utf-8")

    rutas = [EJEC + "/R-documental/v002/aclaracion-t07.json",
             EJEC + "/R-documental/v002/aclaracion-t07.md",
             EJEC + "/R-documental/v002/scripts/aclarar_t07.py",
             EJEC + "/R-documental/v001/dictamen.json",
             EJEC + "/R-documental/v001/dictamen.md",
             EJEC + "/R-documental/v001/sello.json",
             EJEC + "/R-documental/v001/sello.sha256",
             T + "/top50-oportunidades-r9.json", T + "/congelada.json",
             MAPA, TOP_CSV, SEGUIM]
    sello = {
        "rol": "R-documental", "version": "v002",
        "tipo": "sello_de_aclaracion",
        "fecha_utc": hoy,
        "nota": "SHA256 por codigo sobre bytes en disco. Excluye sello.json y sello.sha256.",
        "v001_preservado": doc["preserva"],
        "no_aceptacion_de_bytes_futuros": doc["no_aceptacion_de_bytes_futuros"],
        "archivos": [{"ruta": r, "sha256": sha(ROOT / r), "bytes": (ROOT / r).stat().st_size}
                     for r in sorted(set(rutas))],
    }
    (V002 / "sello.json").write_text(json.dumps(sello, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (V002 / "sello.sha256").write_text(sha(V002 / "sello.json") + "  sello.json\n", encoding="utf-8")

    print("R-documental v002: aclaracion T-07 + carriles; v001 preservado")
    print("  T-07 v001:", t07_v001["ok"], t07_v001["detalle"], "| checks",
          f"{v001['checks_resumen']['ok']}/{v001['checks_resumen']['total']}")
    print("  carriles:", [(c["carril"], c["rango"], c["score"]) for c in carriles])
    print("  sello:", sha(V002 / "sello.json"))


if __name__ == "__main__":
    main()
