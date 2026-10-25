"""Materializa data/integracion-ronda-9/ + ontologia/revision-ronda-9.json.

SOLO lo ejecuta el coordinador tras la auditoria, en la instalacion real.
Este staging NO lo corre: aqui vive como propuesta para no regenerar nada.

Pasos:
  1. Verifica pins vivos (semantica actual, cobertura R8 1423/1106/4506/17/1442,
     normativa W, bloques P1-Q1/Q3, shape P4 por SHA).
  2. Copia TTLs + aceptadas.json desde este staging a data/integracion-ronda-9/.
  3. Congela base-semantica.json (= ontologia/semantica.json) y
     cobertura-r8.json (= data/semantica/cobertura.json).
  4. Copia auditorias *.TEMPLATE.json -> auditoria-a/b.json (con el SHA aun
     pendiente), escribe manifiesto.json con SHA de cada archivo + insumos W,
     e imprime los 2 SHA que el coordinador fija en auditorias y revision.
  5. El coordinador fija aceptadas_sha256 en A+B, re-calcula el manifiesto
     (el SHA de aceptadas cambia -> re-ejecutar este script), y escribe
     ontologia/revision-ronda-9.json con el manifiesto_sha256 impreso.

Uso: uv run python propuestas/plan-tras-r8/ejecucion-20261024/I-codigo/v001/data-integracion-ronda-9/materializar.py
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
STAGING = REPO / "propuestas/plan-tras-r8/ejecucion-20261024/I-codigo/v001/data-integracion-ronda-9"
DEST = REPO / "data/integracion-ronda-9"

PIN = {"respaldadas": 1423, "conceptos": 1106, "revisadas": 4506,
       "candidatas": 17, "materializadas": 1442}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if DEST.exists():
        sys.exit("REFUSO: data/integracion-ronda-9 ya existe; no regenerar. "
                 "Borrarlo a mano solo si la auditoria lo ordena.")
    sem = json.loads((REPO / "ontologia/semantica.json").read_text(encoding="utf-8"))
    cob = json.loads((REPO / "data/semantica/cobertura.json").read_text(encoding="utf-8"))
    res = cob.get("resumen", {})
    checks = {
        "respaldadas_1423": res.get("estados_variables", {}).get("respaldada_por_definicion") == PIN["respaldadas"],
        "conceptos_1106": res.get("conceptos_compartidos") == PIN["conceptos"],
        "revisadas_4506": res.get("estados_correspondencias", {}).get("documental_revisada") == PIN["revisadas"],
        "candidatas_17": res.get("estados_correspondencias", {}).get("candidata_por_nombre") == PIN["candidatas"],
        "materializadas_1442": res.get("variables_materializadas") == PIN["materializadas"],
    }
    if not all(checks.values()):
        sys.exit("Pin R8 roto en vivo: " + json.dumps(checks))
    for rel, want in {
        "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-MilliM-evidencia.txt":
            "5e63691124e69c162ddfa65bde77fb1ad3e9a2173ffd33b9910100880a9ea9a7",
        "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-HA-evidencia.txt":
            "9095968323f72af577b4a94684a78e2f806595ca118529b5e47cb0b2acd1ee3e",
    }.items():
        if sha(REPO / rel) != want:
            sys.exit("Normativa W distinta al pin: " + rel)
    p1 = (REPO / "propuestas/plan-tras-r8/ejecucion-20261024/P1-qudt/v002/propuesta-qudt.ttl").read_text(encoding="utf-8").replace("\r\n", "\n")
    datos = (STAGING / "datos/propuesta-qudt.ttl").read_text(encoding="utf-8").replace("\r\n", "\n")
    for bloque in [b for b in datos.split("\n\n") if "UnidadDeclarada" in b or "declaracion-" in b]:
        if bloque.strip() and bloque.strip() not in p1:
            sys.exit("Bloque staging ajeno a P1 v002")
    if sha(STAGING / "shapes/shape-exclusion-significado.ttl") != \
            "fc301d854b6c9175be601282ab4073f054a1736103b92ea634003c7bcc2b148d":
        sys.exit("Shape staging distinto a P4 v001")
    (DEST / "datos").mkdir(parents=True)
    (DEST / "modelo").mkdir()
    (DEST / "shapes").mkdir()
    (DEST / "auditorias").mkdir()
    shutil.copyfile(STAGING / "datos/propuesta-qudt.ttl", DEST / "datos/propuesta-qudt.ttl")
    shutil.copyfile(STAGING / "modelo/vocabulario-minimo.ttl", DEST / "modelo/vocabulario-minimo.ttl")
    shutil.copyfile(STAGING / "shapes/shape-exclusion-significado.ttl",
                    DEST / "shapes/shape-exclusion-significado.ttl")
    shutil.copyfile(STAGING / "aceptadas.json", DEST / "aceptadas.json")
    shutil.copyfile(REPO / "ontologia/semantica.json", DEST / "base-semantica.json")
    shutil.copyfile(REPO / "data/semantica/cobertura.json", DEST / "cobertura-r8.json")
    for name in ("auditoria-a", "auditoria-b"):
        shutil.copyfile(STAGING / "auditorias" / (name + ".TEMPLATE.json"),
                        DEST / "auditorias" / (name + ".json"))
    archivos = {rel: sha(DEST / rel) for rel in sorted(
        ["datos/propuesta-qudt.ttl", "modelo/vocabulario-minimo.ttl",
         "shapes/shape-exclusion-significado.ttl", "base-semantica.json",
         "cobertura-r8.json", "aceptadas.json",
         "auditorias/auditoria-a.json", "auditorias/auditoria-b.json"])}
    insumos = {rel: sha(REPO / rel) for rel in sorted([
        "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-MilliM-evidencia.txt",
        "propuestas/plan-tras-r8/ejecucion-20261024/W-estandares/v002/normativa/unit-HA-evidencia.txt"])}
    manifiesto = {"formato": "r9-v001", "format_version": 1, "release_base": "R8",
                  "release_propuesta": "R9", "archivos": archivos, "insumos": insumos,
                  "aceptadas_sha256": archivos["aceptadas.json"]}
    (DEST / "manifiesto.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("aceptadas_sha256=" + archivos["aceptadas.json"])
    print("manifiesto_sha256=" + sha(DEST / "manifiesto.json"))
    print('revision-ronda-9.json: {"evidencia": "data/integracion-ronda-9", '
          '"manifiesto_sha256": "<pegar>", "aceptadas_sha256": "<pegar>", '
          '"alcance": "2 declaraciones P1-Q1/Q3 + shape P4 sh:sparql; 0 nucleo"}')


if __name__ == "__main__":
    main()
