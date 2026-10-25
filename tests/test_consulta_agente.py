import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from consultar_ontologia import verificar


class ConsultaAgenteTest(unittest.TestCase):
    def test_bloquea_escritura(self):
        for q in ("INSERT DATA { <a> <b> <c> }", "DELETE WHERE { ?s ?p ?o }", "LOAD <x>"):
            with self.assertRaises(ValueError, msg=q):
                verificar(q)

    def test_exige_limit_en_select(self):
        with self.assertRaises(ValueError):
            verificar("SELECT ?s WHERE { ?s ?p ?o }")
        verificar("SELECT ?s WHERE { ?s ?p ?o } LIMIT 10")
        verificar("SELECT (COUNT(?s) AS ?n) WHERE { ?s ?p ?o } LIMIT 10")

    def test_manifiesto_y_store_existen(self):
        import json
        m = json.loads((Path(__file__).resolve().parents[1] / "reports/portal-carga.json").read_text(encoding="utf-8"))
        self.assertIn("store_dir", m)
        self.assertTrue((Path(__file__).resolve().parents[1] / m["store_dir"]).is_dir())


if __name__ == "__main__":
    unittest.main()
