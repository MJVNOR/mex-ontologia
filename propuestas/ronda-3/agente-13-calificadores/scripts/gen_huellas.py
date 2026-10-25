import datetime
import hashlib
import json
from pathlib import Path

A13 = Path("propuestas/ronda-3/agente-13-calificadores")
ROOT = Path(".")
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def size(p):
    return Path(p).stat().st_size

entradas = {
    "scripts/consolidar_semantica.py": "original central, solo lectura; copiado a staging/",
    "shapes/semantica.ttl": "original central, solo lectura; copiado a staging/",
    "tests/test_semantica.py": "original central, solo lectura; base de patch/test_semantica.patch",
    "ontologia/semantica.json": "reglas vigentes, solo lectura en memoria",
    "data/portal/inventario.json": "inventario actual, solo lectura en memoria",
    "data/portal/contenido-inspeccion.json": "inspección actual, solo lectura en memoria",
    "data/portal/lote-cruces/catalogo-municipal-portal.json": "referencia municipal, solo lectura en memoria",
    "scripts/ampliar_portal.py": "loader SHACL, solo lectura (ya carga shapes/semantica.ttl)",
    "propuestas/ronda-3/agente-3-cobertura/propuestas.json": "fixture 10 reglas DDR con calificador, solo lectura",
    "propuestas/ronda-3/agente-8-educacion/propuestas.json": "fixture 20 reglas sede con calificador, solo lectura",
}
huellas = {"generado_en_utc": utc, "agente": "ronda-3/agente-13-calificadores",
           "nota": "Sin descargas externas: todas las fuentes son archivos locales del proyecto leídos sin modificar. Sin secretos.",
           "nota_fixtures": "fixture_sha256 es el SHA del snapshot propio (30 reglas verbatim); propuestas_sha256 es el SHA del archivo upstream completo de cada agente. No confundirlos: el snapshot no cambia aunque el upstream evolucione en reglas no calificadas.",
           "fixtures": {"reglas_calificadas_snapshot_sha256": sha(A13 / "fixture/reglas_calificadas.json"),
                        "agente3_propuestas_sha256": sha("propuestas/ronda-3/agente-3-cobertura/propuestas.json"),
                        "agente8_propuestas_sha256": sha("propuestas/ronda-3/agente-8-educacion/propuestas.json"),
                        "reglas_snapshot": 30,
                        "cambios_upstream_no_afectan_snapshot": "agente 3 modificó 2 reglas NDDR no calificadas (SHA 29f1dadf.. -> 92a7dcdd..); agente 8 Nacionalidad no calificada; las 30 reglas con calificador siguen verbatim (0 faltan, 0 difieren)"},
           "entradas": {}}
for p, uso in entradas.items():
    huellas["entradas"][p] = {"sha256": sha(p), "bytes": size(p), "uso": uso}
propios = ["fixture/reglas_calificadas.json", "staging/consolidar_semantica.py",
           "staging/consolidar_semantica_ORIG.py",
           "staging/semantica.ttl", "staging/test_semantica.py",
           "patch/consolidar_semantica.patch", "patch/semantica_ttl.patch",
           "patch/test_semantica.patch", "shape/calificador.ttl",
           "scripts/verificar.py", "scripts/correr_tests_staging.py",
           "scripts/gen_huellas.py", "fuente/verificacion-13.json",
           "docs/como_aplicar.md", "docs/revertir.md",
           "propuestas.json", "resultado.md"]
huellas["propios"] = {}
for rel in propios:
    p = A13 / rel
    huellas["propios"][rel] = {"sha256": sha(p), "bytes": size(p)}
(A13 / "fuente/huellas.json").write_text(json.dumps(huellas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("huellas escritas", utc)
