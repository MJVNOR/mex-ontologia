"""Gates de carga R8: fila exacta + auditoria fail-closed (fixtures en staging).

Todo el arbol de evidencia es sintetico bajo tmp (staging): no se toca el
material congelado ni la produccion. Las auditorias fake solo existen en
tmp; una fila incorrecta nunca se aprueba para que la prueba pase.
"""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO = next(p for p in _HERE.parents if (p / "scripts" / "construir_catalogo.py").exists())
sys.path.insert(0, str(_HERE.parents[1] / "scripts"))
sys.path.insert(0, str(_REPO / "scripts"))

import integrar_ronda_8 as r8

COLS = sorted(r8.UNIVERSO_28)
DICC = r8.DICCIONARIO_SINAC
RECURSO = r8.RECURSO_SINAC
ESQ = r8.HUELLA_ESQUEMA_SINAC


def _defiri(col):
    return r8.PREFIX_DEFINICION + DICC + "%2F" + col.rsplit("%2F", 1)[1]


def _variri(col):
    return "https://example.org/mex-ontologi/documented-variable/" + DICC + "%2F" + col.rsplit("%2F", 1)[1]


def make_root(tmp, mutate=None, audit_global="aceptar", drop_approval=None,
              drop_candidata=None, tamper_after_pin=False):
    """Arma evidencia fake completa; mutate(row, base_var, mapping) la corrompe."""
    tmp = Path(tmp)
    ev = tmp / "ev"
    (ev / "auditorias").mkdir(parents=True)
    variables, mappings, vinculos, conceptos = [], [], [], {}
    for i, col in enumerate(COLS):
        n = col.rsplit("%2F", 1)[1]
        var = {"definicion_iri": _defiri(col), "iri": _variri(col),
               "descripcion": "D-" + n, "concepto": "C-" + n,
               "estado": "respaldada_por_definicion",
               "huella_fila_diccionario": "H-" + n}
        mp = {"columna": col, "campo": "F-" + n, "variable": _variri(col),
              "estado": "candidata_por_nombre", "revision": None}
        row = {"campo": "F-" + n, "columna": col, "concepto": "C-" + n,
               "criterio": "K-" + n, "definicion_iri": _defiri(col),
               "descripcion": "D-" + n, "diccionario": DICC,
               "huella_esquema": ESQ, "huella_fila_diccionario": "H-" + n,
               "recurso": RECURSO}
        if mutate is not None:
            mutate(row, var, mp, n)
        variables.append(var)
        mappings.append(mp)
        vinculos.append(row)
        conceptos["C-" + n] = ["C " + n, "Concepto " + n, None]
    if drop_candidata is not None:
        mappings = [m for m in mappings if m["columna"] != drop_candidata]
    cobertura = {"resumen": {
        "estados_correspondencias": {"documental_revisada": 4478, "candidata_por_nombre": 45},
        "estados_variables": {"respaldada_por_definicion": 1423,
                              "candidata_sin_definicion_suficiente": 16,
                              "fuera_del_nucleo_actual": 124},
        "conceptos_compartidos": 1106, "columnas_con_correspondencia": 4523},
        "variables": variables, "correspondencias": mappings}
    base = {"conceptos": conceptos, "reglas_descripcion_exacta": [],
            "vinculos_documentales_revisados": []}
    accepted = {"reglas": [], "conceptos": {}, "vinculos": vinculos,
                "origenes": {v["columna"]: ["f1.json"] for v in vinculos},
                "resumen": {}, "alcance": "fake"}
    (ev / "f1.json").write_text("{}", encoding="utf-8")
    (ev / "aceptadas.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    (ev / "base-semantica.json").write_text(json.dumps(base, ensure_ascii=False, indent=2), encoding="utf-8")
    (ev / "cobertura-r7.json").write_text(json.dumps(cobertura, ensure_ascii=False, indent=2), encoding="utf-8")
    sha_acep = hashlib.sha256((ev / "aceptadas.json").read_bytes()).hexdigest()
    ok_ids = {v["columna"] for v in vinculos}
    if drop_approval is not None:
        ok_ids.discard(drop_approval)
    for name in ("auditoria-a", "auditoria-b"):
        audit = {"dictamen": audit_global, "aceptadas_sha256": sha_acep,
                 "dictamenes": [{"tipo": "vinculos", "id": c, "dictamen": "aceptar"} for c in sorted(ok_ids)]}
        (ev / "auditorias" / (name + ".json")).write_text(json.dumps(audit, ensure_ascii=False), encoding="utf-8")
    if tamper_after_pin:
        vinculos[0]["descripcion"] = "TAMPERED"
        (ev / "aceptadas.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    archivos = {}
    for p in sorted(ev.rglob("*.json")):
        archivos[p.relative_to(ev).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    (ev / "manifiesto.json").write_text(json.dumps({"archivos": archivos, "insumos": {}}),
                                         encoding="utf-8")
    cfg = {"evidencia": "ev", "manifiesto_sha256": hashlib.sha256((ev / "manifiesto.json").read_bytes()).hexdigest()}
    (tmp / "ontologia").mkdir(exist_ok=True)
    (tmp / "ontologia/revision-ronda-8.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp, base, accepted


def _rules(base, accepted):
    rules = copy.deepcopy(base)
    rules["vinculos_documentales_revisados"].extend(copy.deepcopy(accepted["vinculos"]))
    return rules


class TestCargar(unittest.TestCase):
    def test_valid(self):
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t)
            cfg, folder, baseline, acc, sources = r8.cargar(Path(root))
            self.assertEqual(len(acc["vinculos"]), 28)
            r8.validar_sobre_base(_rules(base, accepted), base, Path(root))

    def test_invalid_falta_candidata(self):
        # 27 del universo + resto: el `<` estricto lo dejaba pasar.
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, drop_candidata=COLS[0])
            with self.assertRaises(ValueError):
                r8.cargar(Path(root))

    def test_invalid_descripcion(self):
        def mut(row, var, mp, n):
            if n == COLS[0].rsplit("%2F", 1)[1]:
                row["descripcion"] = "descriptor amplio"
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, mutate=mut)
            with self.assertRaises(ValueError):
                r8.cargar(Path(root))

    def test_invalid_campo(self):
        def mut(row, var, mp, n):
            if n == COLS[0].rsplit("%2F", 1)[1]:
                row["campo"] = "OTRO"
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, mutate=mut)
            with self.assertRaises(ValueError):
                r8.cargar(Path(root))

    def test_invalid_variable_mapping(self):
        def mut(row, var, mp, n):
            if n == COLS[0].rsplit("%2F", 1)[1]:
                mp["variable"] = mp["variable"] + "-x"
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, mutate=mut)
            with self.assertRaises(ValueError):
                r8.cargar(Path(root))

    def test_invalid_definicion_sin_respaldo(self):
        def mut(row, var, mp, n):
            if n == COLS[0].rsplit("%2F", 1)[1]:
                row["definicion_iri"] = row["definicion_iri"] + "-x"
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, mutate=mut)
            with self.assertRaises(ValueError):
                r8.cargar(Path(root))

    def test_invalid_audit_global(self):
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, audit_global="observar")
            with self.assertRaises(ValueError):
                r8.validar_sobre_base(_rules(base, accepted), base, Path(root))

    def test_invalid_audit_falta_aprobacion(self):
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, drop_approval=COLS[0])
            with self.assertRaises(ValueError):
                r8.validar_sobre_base(_rules(base, accepted), base, Path(root))

    def test_invalid_audit_sha(self):
        with tempfile.TemporaryDirectory() as t:
            root, base, accepted = make_root(t, tamper_after_pin=True)
            with self.assertRaises(ValueError):
                r8.validar_sobre_base(_rules(base, accepted), base, Path(root))


if __name__ == "__main__":
    unittest.main()
