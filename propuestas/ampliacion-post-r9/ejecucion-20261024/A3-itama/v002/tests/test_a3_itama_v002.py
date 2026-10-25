"""Pruebas A3-ITAMA v002 (solo stdlib).

Cubren: la busqueda esta acotada a ITAMA y no niega los XLSX del repo; la
evidencia registrada coincide con un barrido fresco; el nucleo conserva la
distincion sexo (IRIs) vs escolaridad (0 conceptos ITAMA); v001 sigue intacta;
y la congelada coincide con los bytes en disco.
"""

import hashlib
import json
import sys
import unittest
from pathlib import Path

V002 = Path(__file__).resolve().parents[1]
V001 = V002.parent / "v001"
ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(V002 / "scripts"))

import analisis_a3_itama_v002 as analisis  # noqa: E402
import registrar_busqueda_itama as busqueda  # noqa: E402


def sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


class TestBusquedaAcotada(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidencia = busqueda.escanear()
        cls.registrada = json.loads(
            (V002 / "evidencia-busqueda.json").read_text(encoding="utf-8")
        )

    def test_hay_xlsx_pero_ninguno_itama(self):
        resumen = self.evidencia["resumen"]
        self.assertGreater(resumen["xlsx_repo_total"], 0)
        self.assertEqual(resumen["xlsx_itama"], 0)
        self.assertEqual(
            resumen["xlsx_repo_total"], len(self.evidencia["rutas_xlsx"])
        )
        self.assertEqual(len(self.evidencia["consultas"]), 3)

    def test_afirmacion_no_global(self):
        p1 = self.evidencia["consultas"][0]
        self.assertIn("No se afirma que el repo carezca de XLSX", p1["resultado"])
        self.assertGreaterEqual(p1["archivos_encontrados"], 1)
        self.assertIn("rutas_xlsx", self.evidencia)

    def test_registro_coincide_con_barrido_actual(self):
        self.assertEqual(
            self.registrada["resumen"], self.evidencia["resumen"]
        )
        consultadas = self.registrada["rutas_consultadas"]
        self.assertEqual(len(consultadas), 7)
        for item in consultadas:
            self.assertEqual(sha(ROOT / item["ruta"]), item["sha256"], item["ruta"])


class TestNucleo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texto = (V002 / "nucleo.ttl").read_text(encoding="utf-8")

    def test_conserva_seis_conceptos_itama(self):
        iries = analisis.iries_concepto(self.texto)
        self.assertEqual(iries, set(analisis.CONCEPTOS_ITAMA))
        self.assertEqual(len(iries), 6)

    def test_sexo_con_iri_y_escolaridad_sin_iri(self):
        iries = analisis.iries_concepto(self.texto)
        self.assertEqual(
            {i for i in iries if i.startswith("sexo-")}, set(analisis.SEXO_ITAMA)
        )
        self.assertFalse(any("escolaridad" in i for i in iries))
        self.assertIn("Escolaridad ITAMA: 0 conceptos", self.texto)

    def test_fuente_del_extracto_sin_cambios(self):
        fuente = ROOT / "data/semantica/nucleo.ttl"
        self.assertIn(f"SHA256 fuente: {sha(fuente)}", self.texto)


class TestEntrega(unittest.TestCase):
    def test_decision_y_alcance(self):
        entrega = json.loads(
            (V002 / "entrega.json").read_text(encoding="utf-8")
        )
        self.assertEqual(entrega["decision"], "BLOQUEADO")
        self.assertEqual(len(entrega["ficha_8_ejes"]), 8)
        self.assertEqual(
            entrega["busqueda_copias_itama"]["resumen"]["xlsx_itama"], 0
        )
        self.assertGreater(
            entrega["busqueda_copias_itama"]["resumen"]["xlsx_repo_total"], 0
        )
        self.assertNotIn("copias_locales_xlsx", entrega["evidencia"])

    def test_v001_intacta(self):
        entrega = json.loads(
            (V002 / "entrega.json").read_text(encoding="utf-8")
        )
        for rel, esperado in entrega["v001_intacta"].items():
            if rel == "nota":
                continue
            self.assertEqual(sha(V001 / rel), esperado, rel)


class TestSello(unittest.TestCase):
    def test_congelada_coincide(self):
        congelada = V002 / "congelada.json"
        if not congelada.exists():
            self.skipTest("congelada aun no generada")
        sello = json.loads(congelada.read_text(encoding="utf-8"))
        for rel, esperado in sello["archivos"].items():
            self.assertEqual(sha(V002 / rel), esperado, rel)
        sidecar = (V002 / "congelada.sha256").read_text(encoding="utf-8")
        self.assertTrue(sidecar.startswith(sha(congelada)))


if __name__ == "__main__":
    unittest.main()
