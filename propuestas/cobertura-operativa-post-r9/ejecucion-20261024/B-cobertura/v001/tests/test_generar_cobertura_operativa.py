"""Unitarias de cobertura operativa: conteo, denominadores, divergencias y SHA."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

STAGING = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGING / "scripts"))
import generar_cobertura_operativa as g

ROOT = g.ROOT


class CoberturaTest(unittest.TestCase):
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
        self.assertEqual(ind["columnas_totales"], 5523)
        self.assertEqual(4506 + 17 + 833 + 154 + 13, 5523)
        self.assertEqual(ind["columnas_con_correspondencia"], 4523)

    def test_denominadores_138_no_154(self):
        i = self.leer(self.generar_tmp())
        d = i["denominadores"]
        self.assertEqual(d["significados_reales_pendientes"], 138)
        self.assertEqual(d["columnas_con_definicion_sin_interpretacion"], 154)
        self.assertEqual(d["variables_pendientes"], 140)  # 138+2, no 154
        self.assertEqual(len(i["frentes"]), 19)
        self.assertEqual(sum(1 for f in i["frentes"] if f["tipo"] == "vigencias"), 16)
        self.assertEqual([o["id"] for o in i["pendientes"]["observaciones_esquema"]],
                         g.OBS_IDS)

    def test_entradas_divergentes_fallan(self):
        r = self.generar_tmp()
        i = self.leer(r)
        with self.assertRaises(ValueError):  # total adulterado
            g.comprobar({"format_version": 1, "release": "R9",
                         "resumen_actual": {"estados_variables":
                          {"respaldada_por_definicion": 999},
                          "conceptos_compartidos": 1106,
                          "estados_correspondencias": {"documental_revisada": 4506,
                           "candidata_por_nombre": 17},
                          "columnas_totales_examinadas": 5523,
                          "columnas_con_correspondencia": 4523},
                         "pendientes": {"significados_reales": 138, "vigencias": 16,
                          "vigencias_acceso_no_resuelto": ["V13", "V14"],
                          "referencia_catalogo": "des_mpo_res",
                          "encabezados_corruptos": 2},
                         "pilotos": {"P2": "negativo", "P3": "negativo"},
                         "consultas_afectadas": {"resultado": {"declaraciones": 2}},
                         "contactos_externos": 0},
                        *self.evidencia())
        with self.assertRaises(ValueError):  # release distinto
            g.comprobar(dict(self.r9(), release="R8"), *self.evidencia())

    def r9(self):
        return g.leer_json(ROOT, "reports/ronda-9.json")

    def evidencia(self):
        return (g.leer_json(ROOT, "data/semantica/cobertura.json"),
                g.leer_json(ROOT, "docs/plan-actualizado-tras-r9.json"),
                g.leer_json(ROOT, "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/totales-cruces-observaciones.json"),
                g.leer_json(ROOT, "propuestas/plan-tras-r8/ejecucion-20261024/C3-cobertura/v001/entrega.json"),
                g.leer_json(ROOT, "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/matriz-preguntas.json"),
                g.leer_json(ROOT, "propuestas/plan-tras-r8/ejecucion-20261024/C4-referencias/v002/entrega.json"),
                5523)

    def test_fuente_sha_y_faltante(self):
        p = ROOT / "reports/ronda-9.json"
        self.assertEqual(g.sha(p), hashlib.sha256(p.read_bytes()).hexdigest())
        with self.assertRaises((FileNotFoundError, OSError)):
            g.sha(ROOT / "reports/no-existe.json")
        with self.assertRaises((FileNotFoundError, OSError)):
            g.leer_json(ROOT, "reports/no-existe.json")

    def test_salida_estable_sin_hora(self):
        a, b = self.generar_tmp(), self.generar_tmp()
        ja = json.loads(Path(a["json"]).read_text(encoding="utf-8"))
        jb = json.loads(Path(b["json"]).read_text(encoding="utf-8"))
        self.assertNotIn("hora", json.dumps(ja).lower()[:200])
        self.assertEqual(ja, jb)
        self.assertEqual(ja["fecha_base"], "2026-10-24")

    def test_siete_preguntas_sin_envio_remiten_expediente(self):
        i = self.leer(self.generar_tmp())
        n = i["necesidades_preguntas_no_enviadas"]
        self.assertEqual(n["contactos_externos"], 0)
        self.assertEqual(len(n["items"]), 7)
        self.assertTrue(all(x["estado_envio"] == "no_enviada" for x in n["items"]))
        self.assertIn("matriz-preguntas.json", n["expediente"])


if __name__ == "__main__":
    unittest.main()
