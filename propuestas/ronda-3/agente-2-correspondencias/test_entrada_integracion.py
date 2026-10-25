"""Prueba de la entrada de integracion (29 correspondencias).

Verifica SHA congelado, formato compatible con vinculos_documentales_revisados,
revalidacion contra el estado central, simulacion 836 -> 865 sin solapes y
rechazo de huella/campo/columna/concepto alterados.

Uso: uv run python propuestas/ronda-3/agente-2-correspondencias/test_entrada_integracion.py
"""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
from preparar_integracion import (CONGELADO_SHA, cargar_central, hoja_de,  # noqa: E402
                                  validar_entradas)


def sha256_archivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


PROP = json.loads((AQUI / "propuestas.json").read_text(encoding="utf-8"))
ENT = json.loads((AQUI / "entrada_integracion_29.json").read_text(encoding="utf-8"))
SEM, COB, INV, INS, BASE = cargar_central()
sys.path.insert(0, str(ROOT / "scripts"))
from consolidar_semantica import columnas  # noqa: E402

COLS = {c["iri"]: c for c in columnas(INV, INS, BASE)}
VAR_POR_DEF = {v["definicion_iri"]: v for v in COB["variables"]}
REC = {r["id"]: r for r in INV["recursos"]}
PREVIAS = {(r["recurso"], r["campo"], r["columna"]) for r in SEM["vinculos_documentales_revisados"]}


class TestEntrada(unittest.TestCase):
    def test_congelado_y_conteos(self):
        self.assertEqual(sha256_archivo(AQUI / "propuestas.json"), CONGELADO_SHA)
        self.assertEqual(ENT["sha_propuestas_congelada"], CONGELADO_SHA)
        self.assertEqual(len(ENT["entradas"]), 29)
        self.assertEqual(ENT["conteos"], {"previas_exactas": 836, "nuevas": 29, "total_simulado": 865})

    def test_formato_compatible(self):
        esperadas = {"recurso", "campo", "columna", "diccionario", "concepto",
                     "descripcion", "huella_esquema", "huella_fila_diccionario", "criterio"}
        for e in ENT["entradas"]:
            with self.subTest(columna=e["columna"]):
                self.assertEqual(set(e.keys()), esperadas)
                self.assertTrue(e["columna"].startswith("https://example.org/mex-ontologi/"))

    def test_revalidacion_central(self):
        vistas = validar_entradas(ENT["entradas"], SEM, COLS, VAR_POR_DEF, REC, PREVIAS)
        self.assertEqual(len(vistas), 29)

    def test_simulacion_865_sin_solapes(self):
        self.assertEqual(len(SEM["vinculos_documentales_revisados"]), 836)
        self.assertEqual(len(PREVIAS), 836)
        nuevas = {(e["recurso"], e["campo"], e["columna"]) for e in ENT["entradas"]}
        self.assertEqual(len(nuevas), 29)
        self.assertEqual(nuevas & PREVIAS, set())
        self.assertEqual(len(PREVIAS | nuevas), 865)
        cob_rev = {c["columna"] for c in COB["correspondencias"] if c["estado"] == "documental_revisada"}
        sem_cols = {r["columna"] for r in SEM["vinculos_documentales_revisados"]}
        self.assertEqual(cob_rev, sem_cols)

    def test_sin_catalogos(self):
        import unicodedata

        def sa(s):
            return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                           if c not in {"\u0300", "\u0301", "\u0302", "\u0308"})
        for e in ENT["entradas"]:
            with self.subTest(columna=e["columna"]):
                self.assertNotIn("catalogo", sa(REC[e["recurso"]].get("nombre")).lower())
                self.assertFalse(hoja_de(e["columna"]).lower().startswith("cat_"))

    def test_conceptos_vigentes(self):
        conceptos = set(SEM["conceptos"].keys())
        for e in ENT["entradas"]:
            self.assertIn(e["concepto"], conceptos)


class TestMutaciones(unittest.TestCase):
    def mutar(self, idx, clave, valor):
        copia = copy.deepcopy(ENT["entradas"])
        copia[idx][clave] = valor
        return copia

    def test_rechaza_huella_esquema(self):
        with self.assertRaises(ValueError):
            validar_entradas(self.mutar(0, "huella_esquema", "0" * 64), SEM, COLS, VAR_POR_DEF, REC, PREVIAS)

    def test_rechaza_huella_fila(self):
        with self.assertRaises(ValueError):
            validar_entradas(self.mutar(1, "huella_fila_diccionario", "0" * 64), SEM, COLS, VAR_POR_DEF, REC, PREVIAS)

    def test_rechaza_campo(self):
        with self.assertRaises(ValueError):
            validar_entradas(self.mutar(2, "campo", "campo_inexistente"), SEM, COLS, VAR_POR_DEF, REC, PREVIAS)

    def test_rechaza_columna(self):
        with self.assertRaises(ValueError):
            validar_entradas(self.mutar(3, "columna", ENT["entradas"][3]["columna"] + "_x"), SEM, COLS, VAR_POR_DEF, REC, PREVIAS)

    def test_rechaza_concepto(self):
        with self.assertRaises(ValueError):
            validar_entradas(self.mutar(4, "concepto", "municipio"), SEM, COLS, VAR_POR_DEF, REC, PREVIAS)

    def test_rechaza_solape_con_previa(self):
        copia = copy.deepcopy(ENT["entradas"])
        previa = SEM["vinculos_documentales_revisados"][0]
        copia[5] = dict(copia[5], recurso=previa["recurso"], campo=previa["campo"], columna=previa["columna"])
        with self.assertRaises(ValueError):
            validar_entradas(copia, SEM, COLS, VAR_POR_DEF, REC, PREVIAS)


if __name__ == "__main__":
    unittest.main(verbosity=1)
