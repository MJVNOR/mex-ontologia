"""Pruebas de publicar_top50_r9 v002: instalacion, destino temporal, no escritura
en fuentes ni versiones selladas, 50 filas identicas, carriles y sello.

Solo stdlib. No escribe fuera de directorios temporales.
"""
import csv
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
V2 = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(V2 / "scripts"))
import publicar_top50_r9 as pub  # noqa: E402

ROOT = pub.raiz(V2)
V001 = ROOT / "propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v001"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def foto(paths):
    return {str(p): (sha(p), p.stat().st_mtime_ns) for p in paths}


class TestPublicarTop50R9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapa = json.loads((ROOT / pub.FUENTES["mapa"]).read_text(encoding="utf-8"))
        cls.crit = json.loads((ROOT / pub.FUENTES["criterio"]).read_text(encoding="utf-8"))
        cls.pesos, cls.pen = cls.crit["pesos_familia"], cls.crit["penalizaciones"]
        with open(ROOT / pub.FUENTES["top50_csv"], encoding="utf-8") as f:
            cls.top = list(csv.DictReader(f))
        with open(ROOT / pub.FUENTES["matriz_csv"], encoding="utf-8") as f:
            cls.mat = list(csv.DictReader(f))
        cls.publicado = json.loads((V2 / f"{pub.NOMBRE}.json").read_text(encoding="utf-8"))

    def calc(self):
        return sorted(((pub.score(p, self.pesos, self.pen), p["id"]) for p in self.mapa["pares"]
                       if p["estado"] == "candidata_por_validar"), key=lambda r: (-r[0], r[1]))

    def test_mapa_3916_y_reparto_estados(self):
        estados = {}
        for p in self.mapa["pares"]:
            estados[p["estado"]] = estados.get(p["estado"], 0) + 1
        self.assertEqual(len(self.mapa["pares"]), 3916)
        self.assertEqual(estados, {
            "sin_clave_detectada": 2328,
            "candidata_por_validar": 1191,
            "solo_dimensiones_amplias_o_tiempo": 396,
            "exploratorio_ejecutado": 1,
        })

    def test_matriz_1191_scores_recomputados(self):
        self.assertEqual(len(self.mat), 1191)
        self.assertEqual(len({r["id"] for r in self.mat}), 1191)
        byid = {i: s for s, i in self.calc()}
        self.assertEqual(len(byid), 1191)
        for r in self.mat:
            self.assertEqual(float(r["score"]), byid[r["id"]], r["id"])

    def test_publicado_50_ids_orden_rangos_scores(self):
        filas = self.publicado["filas"]
        self.assertEqual(len(filas), 50)
        self.assertEqual(len({f["id"] for f in filas}), 50)
        calc = self.calc()
        for n, (f, r) in enumerate(zip(filas, self.top)):
            self.assertEqual(f["rango"], n + 1)
            self.assertEqual(f["id"], r["id"])
            self.assertEqual(f["id"], calc[n][1])
            self.assertEqual(f["score"], float(r["score"]))
            self.assertEqual(f["score"], calc[n][0])
            self.assertEqual(f["estado"], pub.NO_JOIN)

    def test_carriles_a1_a2_a3_por_rango(self):
        carriles = {f["carril_analitico"]: f["rango"] for f in self.publicado["filas"]
                    if f["carril_analitico"]}
        self.assertEqual(carriles, {"A1-911": 2, "A2-matrimonios-nacimientos": 4, "A3-itama": 1})
        self.assertEqual(sum(1 for f in self.publicado["filas"] if f["carril_analitico"]), 3)
        porid = {f["id"]: f["rango"] for f in self.publicado["filas"]}
        for tag, pid in pub.A_PARES.items():
            self.assertEqual(porid[pid], carriles[tag], tag)

    def test_destino_instalado_y_explicito(self):
        instalado = ROOT / "scripts/publicar_top50_r9.py"
        self.assertEqual(pub.destino_publicacion(ROOT, None, instalado).resolve(),
                         (ROOT / "reports").resolve())
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(pub.destino_publicacion(ROOT, td).resolve(), pathlib.Path(td).resolve())
        with self.assertRaises(SystemExit):  # carpeta de version sin --out-dir
            pub.destino_publicacion(ROOT, None, V2 / "scripts/publicar_top50_r9.py")

    def test_generar_en_outdir_temporal_reproduce_publicado(self):
        with tempfile.TemporaryDirectory() as td:
            res = pub.generar(ROOT, td)
            self.assertEqual(res["filas"], 50)
            self.assertEqual(res["estado_filas"], pub.NO_JOIN)
            for nombre in (f"{pub.NOMBRE}.json", f"{pub.NOMBRE}.md", f"{pub.NOMBRE}.html"):
                self.assertTrue((pathlib.Path(td) / nombre).is_file(), nombre)
            nuevo = json.loads((pathlib.Path(td) / f"{pub.NOMBRE}.json").read_text(encoding="utf-8"))
            self.assertEqual(nuevo["filas"], self.publicado["filas"])
            self.assertEqual(nuevo["meta"], self.publicado["meta"])
            vista = (pathlib.Path(td) / f"{pub.NOMBRE}.html").read_text(encoding="utf-8")
            md = (pathlib.Path(td) / f"{pub.NOMBRE}.md").read_text(encoding="utf-8")
            for f in self.publicado["filas"]:
                self.assertIn(f["id"], vista)
                self.assertIn(f["id"], md)

    def test_no_escribe_fuentes_ni_versiones_selladas(self):
        fuentes = [ROOT / r for r in pub.FUENTES.values()]
        previo = foto(fuentes + sorted(p for p in V001.rglob("*") if p.is_file()))
        with tempfile.TemporaryDirectory() as td:
            pub.generar(ROOT, td)
        self.assertEqual(foto(fuentes + sorted(p for p in V001.rglob("*") if p.is_file())), previo)
        for prohibido in (V001, ROOT / "data/portal", ROOT / pub.FUENTES["criterio"].rsplit("/", 1)[0]):
            with self.assertRaises(SystemExit, msg=str(prohibido)):
                pub.generar(ROOT, prohibido)

    def test_contenido_publicado_y_fuentes_completas(self):
        textos = {n: (V2 / f"{pub.NOMBRE}{n}").read_text(encoding="utf-8")
                  for n in (".json", ".md", ".html")}
        for nombre, texto in textos.items():
            self.assertNotIn("staging", texto.lower(), nombre)
            self.assertNotIn("T-top50/v001", texto, nombre)
        self.assertEqual(len(self.publicado["filas"]), 50)
        self.assertTrue(all(f["estado"] == pub.NO_JOIN for f in self.publicado["filas"]))
        self.assertTrue(all(isinstance(f["bloqueadores"], list) for f in self.publicado["filas"]))
        self.assertEqual(self.publicado["meta"]["estado_filas"], pub.NO_JOIN)
        fuentes = self.publicado["meta"]["fuentes"]
        self.assertEqual(len(fuentes), len(pub.FUENTES))
        for f in fuentes:
            self.assertRegex(f["sha256"], r"^[0-9a-f]{64}$")
            ruta = ROOT / f["ruta"]
            self.assertEqual(f["sha256"], sha(ruta), f["ruta"])
            self.assertEqual(f["bytes"], ruta.stat().st_size)
        self.assertIn(pub.NO_JOIN, textos[".md"])
        self.assertIn(pub.NO_JOIN, textos[".html"])
        self.assertNotIn("<script", textos[".html"].lower())

    def test_cli_explicito_temporal_y_rechazo_sin_outdir(self):
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
        script = V2 / "scripts/publicar_top50_r9.py"
        with tempfile.TemporaryDirectory() as td:
            ok = subprocess.run([sys.executable, str(script), "--root", str(ROOT), "--out-dir", td],
                                capture_output=True, text=True, env=env)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertTrue((pathlib.Path(td) / f"{pub.NOMBRE}.html").is_file())
        sin = subprocess.run([sys.executable, str(script), "--root", str(ROOT)],
                             capture_output=True, text=True, env=env)
        self.assertNotEqual(sin.returncode, 0)  # version: exige --out-dir

    def test_congelada_generada_por_codigo(self):
        sello = V2 / "congelada.json"
        if not sello.is_file():  # durante la primera corrida el sello aun no existe
            return
        cong = json.loads(sello.read_text(encoding="utf-8"))
        self.assertEqual(cong["alcance"], "propuestas/ampliacion-post-r9/ejecucion-20261024/T-top50/v002/")
        self.assertGreaterEqual(len(cong["archivos"]), 9)
        for a in cong["archivos"]:
            p = V2 / a["ruta"]
            self.assertTrue(p.is_file(), a["ruta"])
            self.assertNotIn("__pycache__", a["ruta"])
            self.assertFalse(a["ruta"].endswith(".pyc"), a["ruta"])
            self.assertEqual(sha(p), a["sha256"], a["ruta"])
            self.assertEqual(p.stat().st_size, a["bytes"], a["ruta"])
        canon = json.dumps(cong["archivos"], ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
        self.assertEqual(hashlib.sha256(canon).hexdigest(), cong["sello_sha256"])
        self.assertTrue(all(e["exit_code"] == 0 for e in cong["ejecuciones"]))


if __name__ == "__main__":
    unittest.main()
