"""Prueba pertinente A2: el analisis separado debe concluir BLOQUEADO con causa
y la congelada debe coincidir con los bytes en disco. Solo stdlib."""
import hashlib
import json
import unittest
from pathlib import Path

V001 = Path(__file__).resolve().parents[1]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


class TestBloqueo(unittest.TestCase):
    def test_veredicto_bloqueado_con_causas(self):
        r = json.loads((V001 / "resultados.json").read_text(encoding="utf-8"))
        self.assertEqual(r["veredicto"], "BLOQUEADO")
        self.assertTrue(r["causas_bloqueo"])
        self.assertIsNone(r["comparacion_volumenes"])
        self.assertIsNone(r["join_grafo"])
        self.assertEqual(len(r["ejes"]), 8)

    def test_congelada_coincide(self):
        c = json.loads((V001 / "congelada.json").read_text(encoding="utf-8"))
        for rel, h in c["archivos"].items():
            self.assertEqual(sha(V001 / rel), h, rel)
        lado = (V001 / "congelada.sha256").read_text(encoding="utf-8").strip()
        self.assertTrue(lado.startswith(sha(V001 / "congelada.json")))


if __name__ == "__main__":
    unittest.main()
