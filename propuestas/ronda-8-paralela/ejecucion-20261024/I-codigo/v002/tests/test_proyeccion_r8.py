"""Puerta de proyeccion R8: 28 revisadas -> candidatas y viceversa (sintetico)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from r8_proyeccion import preparar_proyeccion_r7, proyectar_semantica_r7


def _col(i):
    return f"https://example.org/mex-ontologi/file-column/xx%2F{i}"


def _fx(n=28):
    cols = [_col(i) for i in range(n)]
    semantic = {
        "correspondencias": [{"columna": c, "estado": "documental_revisada",
                              "revision": {"columna": c}} for c in cols]
        + [{"columna": _col("otro"), "estado": "candidata_por_nombre", "revision": None}],
        "variables": [{"definicion_iri": "d"}],
        "resumen": {"estados_correspondencias": {"documental_revisada": n, "candidata_por_nombre": 1}},
    }
    accepted = {"vinculos": [{"columna": c} for c in cols]}
    base = {"reglas_descripcion_exacta": [], "vinculos_documentales_revisados": [],
            "conceptos": {}}
    return semantic, accepted, base


class TestProyeccion(unittest.TestCase):
    def test_valid(self):
        semantic, accepted, base = _fx()
        proj, delta = preparar_proyeccion_r7(semantic, base,
                                             {"reglas": [], "vinculos": [], "conceptos": {}},
                                             base, accepted)
        self.assertEqual(delta, {"n_reglas": 0, "n_vinculos": 28, "n_conceptos": 0})
        self.assertEqual(proj["resumen"]["estados_correspondencias"],
                         {"documental_revisada": 0, "candidata_por_nombre": 29})
        self.assertTrue(all(m["revision"] is None for m in proj["correspondencias"][:28]))
        # El vivo queda intacto.
        self.assertEqual(semantic["resumen"]["estados_correspondencias"]["documental_revisada"], 28)

    def test_invalid_sin_revisar(self):
        semantic, accepted, base = _fx()
        semantic["correspondencias"][0]["estado"] = "candidata_por_nombre"
        with self.assertRaises(ValueError):
            proyectar_semantica_r7(semantic, accepted)

    def test_invalid_otro_n(self):
        semantic, accepted, base = _fx(n=27)
        with self.assertRaises(ValueError):
            proyectar_semantica_r7(semantic, accepted)

    def test_invalid_base_discontinua(self):
        semantic, accepted, base = _fx()
        otra = {"reglas_descripcion_exacta": [{"id": "x"}], "vinculos_documentales_revisados": [],
                "conceptos": {}}
        with self.assertRaises(ValueError):
            preparar_proyeccion_r7(semantic, base,
                                   {"reglas": [], "vinculos": [], "conceptos": {}},
                                   otra, accepted)


if __name__ == "__main__":
    unittest.main()
