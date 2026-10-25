"""Unitarias v002: conteo, denominadores, divergencias, SHA, drift, particion CSV."""
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

STAGING = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING / "scripts"))
import generar_cobertura_operativa as g

ROOT = g.ROOT
V2OUT = ("propuestas/cobertura-operativa-post-r9/ejecucion-20261024/"
         "B-cobertura/v002/salida")


class CoberturaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = g.leer_fuentes(ROOT)

    def generar_tmp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return g.generar(ROOT, Path(tmp.name))

    def leer(self, r):
        return json.loads(Path(r["json"]).read_text(encoding="utf-8"))

    def test_conteo_y_ecuaciones(self):
        i = self.leer(self.generar_tmp())
        self.assertEqual((i["format_version"], i["release"]), (1, "R9"))
        ind = i["indicadores"]
        self.assertEqual((ind["significados_respaldados"], ind["conceptos"],
                          ind["correspondencias_revisadas"], ind["candidatas"],
                          ind["ambiguas"]), (1423, 1106, 4506, 17, 0))
        self.assertEqual(ind["particion_columnas"], g.ESPERADO_ESTADOS)

    def test_resumen_completo_sin_drift(self):
        self.assertEqual(self.f["data/semantica/cobertura.json"]["resumen"],
                         self.f["reports/ronda-9.json"]["resumen_actual"])
        mut = json.loads(json.dumps(self.f["data/semantica/cobertura.json"]))
        mut["resumen"]["conceptos_compartidos"] = 999
        with self.assertRaises(ValueError):
            g.comprobar_resumen(self.f["reports/ronda-9.json"], mut)

    def test_csv_particion_unica(self):
        filas = self.f["csv_filas"]
        self.assertEqual(len(filas), 5523)
        self.assertEqual(len({r["columna_iri"] for r in filas}), 5523)
        self.assertEqual(Counter(r["estado_columna"] for r in filas),
                         Counter(g.ESPERADO_ESTADOS))
        with self.assertRaises(ValueError):  # particion adulterada
            g.comprobar_csv([dict(r, estado_columna="documental_revisada") for r in filas])

    def test_denominadores_138_no_154(self):
        i = self.leer(self.generar_tmp())
        self.assertEqual(i["denominadores"]["significados_reales_pendientes"], 138)
        self.assertEqual(i["denominadores"]["columnas_con_definicion_sin_interpretacion"], 154)
        self.assertEqual(i["denominadores"]["variables_pendientes"], 140)

    def test_frentes_completos_con_condicion_y_referencia(self):
        i = self.leer(self.generar_tmp())
        fr = i["frentes"]
        self.assertEqual(len(fr), 19 + 1 + 1 + 5)  # C4 + 138 + 17 + 5 obs
        for x in fr:
            self.assertTrue(x.get("referencia_exacta"), x["frente"])
            if x["frente"] == "candidatas-17":
                self.assertEqual(len(x["items"]), 17)
                self.assertTrue(all(it.get("condicion_reapertura") for it in x["items"]))
            else:
                self.assertTrue(x.get("condicion_reapertura"), x["frente"])
        self.assertTrue(any(x["frente"] == "significados-138" for x in fr))
        self.assertEqual({x["frente"] for x in fr if x["tipo"] == "observacion_esquema"},
                         set(g.OBS_IDS))

    def test_evidencia_sha_fisico(self):
        self.assertEqual(g.verificar_evidencia(
            self.f["propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/entrega.json"],
            ROOT), 104)
        p = ROOT / "reports/ronda-9.json"
        self.assertEqual(g.sha(p), hashlib.sha256(p.read_bytes()).hexdigest())
        with self.assertRaises((FileNotFoundError, OSError)):
            g.sha(ROOT / "reports/no-existe.json")

    def test_entradas_divergentes_fallan(self):
        mut = json.loads(json.dumps(self.f["reports/ronda-9.json"]))
        mut["release"] = "R8"
        with self.assertRaises(ValueError):
            g.comprobar_resumen(mut, self.f["data/semantica/cobertura.json"])

    def test_tildes_qudt_y_salida_estable(self):
        a, b = self.generar_tmp(), self.generar_tmp()
        ja = json.loads(Path(a["json"]).read_text(encoding="utf-8"))
        self.assertEqual(ja, json.loads(Path(b["json"]).read_text(encoding="utf-8")))
        self.assertIn("Milímetros", ja["notas_cerradas"]["qudt"])
        self.assertIn("Hectáreas", ja["notas_cerradas"]["qudt"])
        self.assertIn("Hectómetros cúbicos", ja["notas_cerradas"]["qudt"])
        self.assertEqual(ja["fecha_base"], "2026-10-24")
        self.assertNotIn("instalacion_futura", ja)

    def test_siete_preguntas_sin_envio(self):
        i = self.leer(self.generar_tmp())
        n = i["necesidades_preguntas_no_enviadas"]
        self.assertEqual((n["contactos_externos"], len(n["items"])), (0, 7))
        self.assertTrue(all(x["estado_envio"] == "no_enviada" for x in n["items"]))
        self.assertIn("matriz-preguntas.json", n["expediente"])


if __name__ == "__main__":
    unittest.main()
