"""Pruebas T-top50: recomputan 50/1191 unicos, score y orden. Solo stdlib."""
import csv
import hashlib
import json
import pathlib
import unittest

V001 = pathlib.Path(__file__).resolve().parents[1]
ROOT = pathlib.Path(__file__).resolve().parents[6]
C2 = ROOT / "propuestas/plan-tras-r8/ejecucion-20261024/C2-oportunidades/v001"


class TestTop50R9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapa = json.loads((ROOT / "data/portal/oportunidades-cruce.json").read_text(encoding="utf-8"))
        crit = json.loads((C2 / "criterio.json").read_text(encoding="utf-8"))
        cls.pesos, cls.pen = crit["pesos_familia"], crit["penalizaciones"]
        with open(C2 / "prioridades_top50.csv", encoding="utf-8") as f:
            cls.top = list(csv.DictReader(f))
        with open(C2 / "matriz_pares_relevantes.csv", encoding="utf-8") as f:
            cls.mat = list(csv.DictReader(f))

    def sc(self, p):
        return round(sum(self.pesos.get(f, 1) for f in p.get("familias_compartidas", []))
                     + sum(self.pen.get(b, 0) for b in p.get("pendientes", [])), 2)

    def test_mapa_3916_y_1191_candidatas(self):
        self.assertEqual(len(self.mapa["pares"]), 3916)
        self.assertEqual(sum(1 for p in self.mapa["pares"] if p["estado"] == "candidata_por_validar"), 1191)

    def test_matriz_1191_unicos_y_scores(self):
        self.assertEqual(len(self.mat), 1191)
        self.assertEqual(len({r["id"] for r in self.mat}), 1191)
        byid = {p["id"]: p for p in self.mapa["pares"]}
        for r in self.mat:
            self.assertEqual(float(r["score"]), self.sc(byid[r["id"]]), r["id"])

    def test_top50_unicos_orden_y_scores(self):
        self.assertEqual(len(self.top), 50)
        self.assertEqual(len({r["id"] for r in self.top}), 50)
        calc = sorted(((self.sc(p), p["id"]) for p in self.mapa["pares"]
                       if p["estado"] == "candidata_por_validar"), key=lambda r: (-r[0], r[1]))
        for n, r in enumerate(self.top):
            self.assertEqual(int(r["rango"]), n + 1)
            self.assertEqual((float(r["score"]), r["id"]), (calc[n][0], calc[n][1]))

    def test_pares_a1_a3_por_id_exacto(self):
        ids = {r["id"] for r in self.top}
        self.assertIn("19e5036d-dbe3-4e1d-b021-df5d47b6fb1f--923b485b-515e-4fb9-a4ac-cccbeb88cc92", ids)  # A1 911
        self.assertIn("1cf9c8e2-e7e4-43d8-a9fd-6da790e64c98--df2d60f5-2243-4bb0-885a-941aa8a657f5", ids)  # A2
        self.assertIn("27a5c80c-514a-4170-a2e5-7ef40d818641--4d27a1c4-381d-4ce0-a663-0d3e23a93848", ids)  # A3

    def test_salidas_staging_y_congelada(self):
        ent = json.loads((V001 / "top50-oportunidades-r9.json").read_text(encoding="utf-8"))
        self.assertEqual(len(ent["filas"]), 50)
        self.assertTrue(all(f["estado"] == "NO_JOIN_APROBADO" for f in ent["filas"]))
        vista = (V001 / "vista-top50-r9.html").read_text(encoding="utf-8")
        for r in self.top:
            self.assertIn(r["id"], vista)
        cong = json.loads((V001 / "congelada.json").read_text(encoding="utf-8"))
        for a in cong["archivos"]:
            p = ROOT / a["ruta"]
            self.assertTrue(p.is_file(), a["ruta"])
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), a["sha256"])
            self.assertEqual(len(p.read_bytes()), a["bytes"])


if __name__ == "__main__":
    unittest.main()
