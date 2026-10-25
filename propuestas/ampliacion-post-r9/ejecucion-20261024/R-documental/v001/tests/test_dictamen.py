"""Prueba del dictamen R: sello coherente, checks sin fallas y bytes sellados intactos.

Solo stdlib. Uso: uv run python -m unittest discover -s tests (dentro de v001).
"""
import hashlib
import json
import unittest
from pathlib import Path

V001 = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[6]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class TestDictamen(unittest.TestCase):
    def test_checks_sin_fallas(self):
        d = json.loads((V001 / "dictamen.json").read_text(encoding="utf-8"))
        fallas = [c["id"] for c in d["checks"] if not c["ok"]]
        self.assertEqual(fallas, [], fallas)
        self.assertEqual(d["checks_resumen"]["total"], len(d["checks"]))
        self.assertEqual(d["entregas"]["T-top50/v001"]["veredicto"], "FAVORABLE CON OBSERVACIONES")
        self.assertEqual(d["entregas"]["A2-registro-civil/v001"]["veredicto"], "FAVORABLE CON OBSERVACIONES")

    def test_sello_coincide(self):
        s = json.loads((V001 / "sello.json").read_text(encoding="utf-8"))
        for a in s["archivos"]:
            p = ROOT / a["ruta"]
            self.assertTrue(p.is_file(), a["ruta"])
            self.assertEqual(sha(p), a["sha256"], a["ruta"])
            self.assertEqual(p.stat().st_size, a["bytes"], a["ruta"])
        lado = (V001 / "sello.sha256").read_text(encoding="utf-8").split()
        self.assertEqual(lado, [sha(V001 / "sello.json"), "sello.json"])

    def test_sellos_auditados_coinciden(self):
        s = json.loads((V001 / "sello.json").read_text(encoding="utf-8"))
        rutas = {a["ruta"] for a in s["archivos"]}
        for rel in ("T-top50/v001/congelada.json", "A2-registro-civil/v001/congelada.json"):
            self.assertIn("propuestas/ampliacion-post-r9/ejecucion-20261024/" + rel, rutas)
        self.assertNotIn("sello.json", " ".join(rutas))
        self.assertNotIn("sello.sha256", " ".join(rutas))


if __name__ == "__main__":
    unittest.main()
