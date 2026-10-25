"""Pruebas A2 v002: bloqueo reproducido, fuentes ancladas y sello coherente.

Reproduce las pruebas de v001 (veredicto BLOQUEADO, 8 ejes, sin comparacion
ni join) y anade las correcciones H-02 (datos vs diccionario) y H-04
(SHA256 completo de las cuatro fuentes). Solo stdlib.
"""
import hashlib
import json
import unittest
from pathlib import Path

V002 = Path(__file__).resolve().parents[1]
REPO = V002.parents[4]
FUENTES = [
    "reports/catalogo-perfil.json",
    "data/portal/contenido-inspeccion.json",
    "data/portal/oportunidades-cruce.json",
    "data/portal/lote-cruces/validacion-lote.json",
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


class TestBloqueo(unittest.TestCase):
    def setUp(self):
        self.r = json.loads((V002 / "resultados.json").read_text(encoding="utf-8"))

    def test_veredicto_bloqueado_con_causas(self):
        r = self.r
        self.assertEqual(r["veredicto"], "BLOQUEADO")
        self.assertTrue(r["causas_bloqueo"])
        self.assertIsNone(r["comparacion_volumenes"])
        self.assertIsNone(r["join_grafo"])
        self.assertEqual(len(r["ejes"]), 8)

    def test_citas_literales_b_tecnica(self):
        u = self.r["ejes"]["unicidad"]["evidencia"]
        self.assertIn("Diagnóstico de muestra", u)
        p = self.r["ejes"]["periodo_ambito"]["evidencia"]
        self.assertIn("'Año de registro'", p)
        self.assertIn("'Mes de registro'", p)
        self.assertNotIn("Anio-Mes", p)

    def test_h02_recursos_datos_y_diccionario(self):
        f = self.r["fuentes_locales"]["reports/catalogo-perfil.json"]
        self.assertEqual(f["mat_recursos"], 11)
        self.assertEqual(f["mat_recursos_datos"], 10)
        self.assertEqual(f["mat_diccionarios"], 1)
        self.assertEqual(f["nac_recursos"], 16)
        self.assertEqual(f["nac_recursos_datos"], 15)
        self.assertEqual(f["nac_diccionarios"], 1)
        self.assertEqual(f["mat_recursos"], f["mat_recursos_datos"] + f["mat_diccionarios"])
        self.assertEqual(f["nac_recursos"], f["nac_recursos_datos"] + f["nac_diccionarios"])

    def test_h04_sha256_completo_de_fuentes(self):
        for rel in FUENTES:
            with self.subTest(fuente=rel):
                decl = self.r["fuentes_locales"][rel]
                p = REPO / rel
                self.assertEqual(decl["sha256"], sha(p))
                self.assertEqual(decl["bytes"], p.stat().st_size)

    def test_sello_coincide(self):
        s = json.loads((V002 / "sello.json").read_text(encoding="utf-8"))
        self.assertNotIn("sello.json", s["archivos"])
        for rel, h in s["archivos"].items():
            self.assertEqual(sha(V002 / rel), h, rel)
        lado = (V002 / "sello.sha256").read_text(encoding="utf-8").strip()
        self.assertTrue(lado.startswith(sha(V002 / "sello.json")))


if __name__ == "__main__":
    unittest.main()
