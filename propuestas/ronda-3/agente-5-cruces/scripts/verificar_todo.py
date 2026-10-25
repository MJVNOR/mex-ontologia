"""Verificador integral de la entrega. Ejecuta todo en orden y comprueba negativos.
Uso: uv run python propuestas/ronda-3/agente-5-cruces/scripts/verificar_todo.py
Solo lee fuera de la carpeta del agente; solo escribe dentro de ella.
"""
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
BASE = RAIZ / "propuestas" / "ronda-3" / "agente-5-cruces"
SCRIPTS = ["verificar_base.py", "construir_matriz.py", "ficha_f1_registro_civil.py",
           "ficha_f2_proyecciones.py", "ficha_f3_educativos.py", "consultas_sparql.py"]


def main():
    for s in SCRIPTS:
        r = subprocess.run([sys.executable, str(BASE / "scripts" / s)],
                           capture_output=True, text=True, cwd=str(RAIZ))
        print(f"--- {s}: exit {r.returncode} ---")
        print((r.stdout or "")[-400:])
        if r.returncode != 0:
            print(r.stderr[-3000:])
            sys.exit(1)
    m = json.loads((BASE / "matriz-cruces.json").read_text(encoding="utf-8"))
    assert m["resumen"]["total"] == 3916
    assert sum(m["resumen"]["decisiones"].values()) == 3916
    # Consistencia F2: cobertura observada vs solo-2020 cruzado + claves entregadas
    c20 = json.loads((BASE / "fichas" / "claves-2020.json").read_text(encoding="utf-8"))
    assert c20["anos_observados_ambos"] == "1990-2040" and c20["anos_cruzados"] == ["2020"]
    assert len(c20["filas"]) == 72 and all(f["igualdad"] and f["anio"] == "2020" for f in c20["filas"])
    # Negativos de integridad de la entrega: equivalencias solo como negacion explicita
    prop = json.loads((BASE / "propuestas.json").read_text(encoding="utf-8"))
    assert "owl:sameAs" in prop["no_propone"] and "skos:exactMatch" in prop["no_propone"]
    cuerpo = json.dumps({k: v for k, v in prop.items() if k != "no_propone"}, ensure_ascii=False)
    assert "sameAs" not in cuerpo and "exactMatch" not in cuerpo, "no se proponen equivalencias"
    for f in ["resultado.md", "propuestas.json", "matriz-cruces.json", "fichas/F1.json",
              "fichas/F2.json", "fichas/F3.json", "fichas/claves-2020.json", "fuente/huellas.json"]:
        assert (BASE / f).exists(), f
    print("TODO OK")


if __name__ == "__main__":
    main()
