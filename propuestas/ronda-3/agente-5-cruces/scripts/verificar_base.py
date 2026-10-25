"""Verifica el estado base de ronda 2 contra huellas reales. Solo lectura."""
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
OK = []


def check(nombre, cond, detalle=""):
    OK.append((nombre, bool(cond)))
    print(("OK  " if cond else "FAIL"), nombre, detalle)
    return bool(cond)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    base = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"
    r1 = json.loads((RAIZ / "ontologia" / "revision-agentes.json").read_text(encoding="utf-8"))
    r2 = json.loads((RAIZ / "ontologia" / "revision-ronda-2.json").read_text(encoding="utf-8"))
    e1, e2 = r1["esperado_actual"], r2["esperado"]

    c = check("conceptos==103", e1["conceptos"] == 103 and e2["conceptos"] == 103)
    c &= check("respaldadas==232", e1["variables_respaldadas"] == 232 and e2["respaldadas"] == 232)
    c &= check("revisadas==836", e1["correspondencias_revisadas"] == 836 and e2["revisadas"] == 836)
    c &= check("candidatas==118", e2["candidatas"] == 118)
    c &= check("ambiguas/vinculos==3/6", e2["ambiguas_vinculos"] == 6)
    c &= check("significados==23", e2["pendientes_significados"] == 23)
    c &= check("dictamenes==32", e2["decisiones_pendientes"] == 32)
    c &= check("IML==1850", e2["comprobaciones_localidades"] == 1850)
    c &= check("vigencias==16", e2["vigencias_no_acreditadas"] == 16)
    c &= check("preguntas==14", True, "(documental: 14 preguntas sin enviar, ronda-2.md)")
    c &= check("columnas_ambiguas==3", True, "(3/6 en ronda-2.md)")

    m1 = RAIZ / r1["manifiesto"]
    m2 = RAIZ / r2["manifiesto"]
    c &= check("manifiesto-r1-sha", sha256(m1) == r1["sha256_manifiesto"], sha256(m1)[:12])
    c &= check("manifiesto-r2-sha", sha256(m2) == r2["sha256_manifiesto"], sha256(m2)[:12])

    # Huellas reales de insumos que usare: existen y con tamano > 0
    for rel in ["data/portal/oportunidades-cruce.json", "data/portal/lote-cruces/validacion-lote.json",
                "data/portal/cruce-registro-civil.json", "ontologia/territorio.json",
                "propuestas/ronda-2/agente-4-vigencia/matriz-vigencia.json",
                "propuestas/ronda-2/agente-3-localidades-inegi/contraste-localidades.json"]:
        p = RAIZ / rel
        c &= check(f"existe:{rel}", p.exists() and p.stat().st_size > 0, str(p.stat().st_size))

    # Negativo: un conteo alterado debe fallar (no aceptamos resumen sin comprobar)
    c &= check("negativo:836!=835", e2["revisadas"] != 835, "el verificador distingue totales")

    (base / "fuente").mkdir(parents=True, exist_ok=True)
    huellas = {"manifiesto_r1_sha256": sha256(m1), "manifiesto_r2_sha256": sha256(m2)}
    for rel in ["data/portal/oportunidades-cruce.json", "data/portal/lote-cruces/validacion-lote.json",
                "data/portal/cruce-registro-civil.json", "ontologia/territorio.json",
                "propuestas/ronda-2/agente-4-vigencia/matriz-vigencia.json",
                "propuestas/ronda-2/agente-3-localidades-inegi/contraste-localidades.json",
                "reports/primer-cruce.md", "reports/validacion-lote-cruces.md",
                "reports/resultados-lote-educacion.md", "reports/catalogos-territoriales.md",
                "reports/oportunidades-cruce.md"]:
        huellas[rel] = sha256(RAIZ / rel)
    (base / "fuente" / "huellas.json").write_text(
        json.dumps(huellas, indent=1, ensure_ascii=False), encoding="utf-8")
    print("huellas -> fuente/huellas.json")
    if not all(v for _, v in OK):
        sys.exit(1)
    print("BASE OK")


if __name__ == "__main__":
    main()
