"""Verificador independiente de la entrega agente-2 ronda 3.

Recalcula huellas desde el estado central (sin reutilizar revisar.py),
comprueba particion 118 sin solapes, 836 revisadas intactas, conceptos y
reglas vigentes, formato listo para integrador y pruebas negativas
(solo-nombre, perdida de enie, contexto insuficiente, filas degeneradas).

Uso: uv run python propuestas/ronda-3/agente-2-correspondencias/verificar.py
Sale con codigo != 0 si alguna comprobacion falla.
"""
import hashlib
import json
import unicodedata
import unittest
from pathlib import Path
from urllib.parse import quote, unquote

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]


def sha256_archivo(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def cargar(nombre):
    with open(AQUI / nombre, encoding="utf-8") as f:
        return json.load(f)


def cargar_central(rel):
    with open(ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


PROP = cargar("propuestas.json")
SEM = cargar_central("ontologia/semantica.json")
COB = cargar_central("data/semantica/cobertura.json")
PEND = cargar_central("reports/pendientes-semanticos.json")
INV = cargar_central("data/portal/inventario.json")
INS = cargar_central("data/portal/contenido-inspeccion.json")


def esquema_hash_por_columna(columna_iri, recurso_id):
    """Recalcula la huella del esquema sin usar revisar.py ni columnas()."""
    recursos = {r["id"]: r for r in INV["recursos"]}
    insp = {r["id"]: r for r in INS["recursos"]}
    r = recursos[recurso_id]
    res = insp[recurso_id]
    if r.get("datastore", {}).get("ok"):
        campos = [f for f in r["datastore"]["campos"] if not f["id"].startswith("_")]
        return huella([{"nombre": f["id"], "tipo": f.get("type")} for f in campos])
    hoja = ""
    if "/file-column/" in columna_iri:
        segs = unquote(columna_iri.split("/file-column/")[1]).split("/")
        if len(segs) >= 3:
            hoja = segs[1]
    tablas = res.get("tablas", [])
    if hoja:
        for tabla in tablas:
            if tabla.get("hoja") == hoja:
                return huella(tabla)
        raise AssertionError(f"hoja {hoja} no encontrada en {recurso_id}")
    assert len(tablas) == 1, f"varias tablas sin hoja en {recurso_id}"
    return huella(tablas[0])


def fila_hash(definicion_iri):
    """Recalcula la huella de la fila del diccionario desde la inspeccion."""
    mitad = definicion_iri.split("/definition/")[1]
    dic_id, pos = unquote(mitad).split("/")
    insp = {r["id"]: r for r in INS["recursos"]}
    fila = insp[dic_id]["definiciones"][int(pos) - 1]
    return huella(fila)


class TestBase(unittest.TestCase):
    def test_huellas_entrada(self):
        esperadas = {"semantica": "ontologia/semantica.json",
                     "cobertura": "data/semantica/cobertura.json",
                     "pendientes": "reports/pendientes-semanticos.json",
                     "inventario": "data/portal/inventario.json",
                     "inspeccion": "data/portal/contenido-inspeccion.json",
                     "config": "config.toml"}
        for clave, rel in esperadas.items():
            self.assertEqual(PROP["huellas_entrada"][clave],
                             sha256_archivo(ROOT / rel), f"huella {clave}")

    def test_conteos_base_actuales(self):
        self.assertEqual(len(SEM["conceptos"]), 103)
        self.assertEqual(len(SEM["vinculos_documentales_revisados"]), 836)
        self.assertEqual(sum(1 for v in COB["variables"]
                             if v.get("estado") == "respaldada_por_definicion"), 232)
        cols = PEND["columnas"]
        self.assertEqual(sum(1 for c in cols if c["estado"] == "documental_revisada"), 836)
        self.assertEqual(sum(1 for c in cols if c["estado"] == "candidata_por_nombre"), 118)
        amb = [c for c in cols if c["estado"] == "ambigua_por_nombre"]
        self.assertEqual(len(amb), 3)
        self.assertEqual(sum(len(c["correspondencias"]) for c in amb), 6)

    def test_revisadas_intactas(self):
        conservadas = set(PROP["conservadas_existentes_iris"])
        self.assertEqual(len(conservadas), 836)
        pend_rev = {c["correspondencias"][0] for c in PEND["columnas"]
                    if c["estado"] == "documental_revisada"}
        self.assertEqual(conservadas, pend_rev)
        cob_rev = {c["columna"] for c in COB["correspondencias"]
                   if c["estado"] == "documental_revisada"}
        sem_rev = {v["columna"] for v in SEM["vinculos_documentales_revisados"]}
        self.assertEqual(cob_rev, sem_rev)
        self.assertEqual(len(sem_rev), 836)


class TestParticion(unittest.TestCase):
    def test_particion_118_sin_solapes(self):
        props = [p["columna"] for p in PROP["propuestas_revisadas"]]
        pends = [p["columna"] for p in PROP["pendientes_clasificados"]]
        self.assertEqual(len(props), 29)
        self.assertEqual(len(pends), 89)
        self.assertEqual(len(set(props + pends)), 118)
        self.assertEqual(set(props) & set(pends), set())
        candidatas = {c["columna"] for c in PEND["columnas"]
                      if c["estado"] == "candidata_por_nombre"}
        self.assertEqual(set(props + pends), candidatas)
        revisadas = {c["columna"] for c in PEND["columnas"]
                     if c["estado"] == "documental_revisada"}
        self.assertEqual(set(props) & revisadas, set())

    def test_correspondencias_trazables(self):
        corr_cand = {c["iri"] for c in COB["correspondencias"]
                     if c["estado"] == "candidata_por_nombre"}
        for p in PROP["propuestas_revisadas"]:
            self.assertIn(p["correspondencia_iri"], corr_cand)
        for p in PROP["pendientes_clasificados"]:
            if "correspondencia_iri" in p:
                self.assertIn(p["correspondencia_iri"], corr_cand)

    def test_conteos_coherentes(self):
        c = PROP["conteos"]
        self.assertEqual(c["candidatas_examinadas"], 118)
        self.assertEqual(c["propuestas_finales"] + c["pendientes_clasificados"], 118)
        self.assertEqual(c["conservadas_existentes"], 836)
        self.assertEqual(c["columnas_ambiguas"], 3)
        self.assertEqual(c["vinculos_ambiguos"], 6)


class TestHuellas(unittest.TestCase):
    def test_huella_esquema_recalculada(self):
        for p in PROP["propuestas_revisadas"]:
            with self.subTest(columna=p["columna"]):
                self.assertEqual(p["huellas"]["huella_esquema"],
                                 esquema_hash_por_columna(p["columna"], p["recurso"]))

    def test_huella_fila_recalculada(self):
        for p in PROP["propuestas_revisadas"]:
            with self.subTest(definicion=p["definicion_iri"]):
                self.assertEqual(p["huellas"]["huella_fila_diccionario"],
                                 fila_hash(p["definicion_iri"]))

    def test_huellas_coinciden_con_central(self):
        var_por_def = {v["definicion_iri"]: v for v in COB["variables"]}
        for p in PROP["propuestas_revisadas"]:
            with self.subTest(definicion=p["definicion_iri"]):
                v = var_por_def[p["definicion_iri"]]
                self.assertEqual(p["huellas"]["huella_fila_diccionario"],
                                 v["huella_fila_diccionario"])
                self.assertEqual(p["definicion"], v["descripcion"])
                self.assertEqual(p["concepto"], v["concepto"])
                self.assertEqual(p["regla"], v["regla"])


class TestVigenciaYFormato(unittest.TestCase):
    def test_conceptos_reglas_vigentes_sin_nuevos(self):
        conceptos = set(SEM["conceptos"].keys())
        reglas = {r["id"] for r in SEM["reglas_descripcion_exacta"]}
        usados_c = {p["concepto"] for p in PROP["propuestas_revisadas"]}
        usados_r = {p["regla"] for p in PROP["propuestas_revisadas"]}
        self.assertTrue(usados_c <= conceptos, usados_c - conceptos)
        self.assertTrue(usados_r <= reglas, usados_r - reglas)

    def test_formato_listo_para_integrador(self):
        obligatorias = ["columna", "campo", "recurso", "conjunto", "diccionario",
                        "variable_iri", "definicion_iri", "concepto", "definicion",
                        "descripcion", "huellas", "criterio", "fuente_esquema",
                        "limitaciones", "correspondencia_iri", "grupo_vinculo",
                        "evidencia_significado", "evidencia_vinculo", "alias_limitado"]
        for p in PROP["propuestas_revisadas"]:
            with self.subTest(columna=p["columna"]):
                for k in obligatorias:
                    self.assertIn(k, p)
                self.assertIn("huella_esquema", p["huellas"])
                self.assertIn("huella_fila_diccionario", p["huellas"])
                self.assertIn("alcance", p["evidencia_vinculo"])
                self.assertTrue(p["fuente_esquema"].startswith("https://"))
                self.assertIsNone(p["alias_limitado"])
                # Traduccion explicita al formato integrador: 'descripcion'
                # es la descripcion literal original (= 'definicion').
                self.assertIn("descripcion", p)
                self.assertEqual(p["descripcion"], p["definicion"])
                self.assertTrue(p["definicion_iri"].startswith(
                    "https://example.org/mex-ontologi/definition/"))
                self.assertTrue(p["columna"].startswith(
                    "https://example.org/mex-ontologi/"))

    def test_sin_alias_y_nombres_exactos(self):
        for p in PROP["propuestas_revisadas"]:
            with self.subTest(columna=p["columna"]):
                self.assertEqual(p["evidencia_vinculo"]["relacion_nombre"], "exacta")
                self.assertEqual(p["campo"], p["variable"])

    def test_grupos_unicos_y_alcance(self):
        ndict = {}
        for r in INV["recursos"]:
            if r["clasificacion"] == "diccionario":
                ndict[r["conjunto_id"]] = ndict.get(r["conjunto_id"], 0) + 1
        for g in PROP["grupos_vinculo"]:
            self.assertEqual(ndict.get(g["conjunto"]["id"]), 1, g["id"])
        vistos = [m["columna"] for g in PROP["grupos_vinculo"] for m in g["miembros"]]
        self.assertEqual(len(vistos), len(set(vistos)))
        self.assertEqual(len(vistos), 30)
        self.assertEqual(sum(g["promovidos"] for g in PROP["grupos_vinculo"]), 29)
        self.assertEqual(sum(g["pendientes"] for g in PROP["grupos_vinculo"]), 1)

    def test_pendientes_con_motivo(self):
        for p in PROP["pendientes_clasificados"]:
            with self.subTest(columna=p["columna"]):
                self.assertIn("motivo", p)
                self.assertIn("etapa", p)
                self.assertTrue(p["motivo"])


class TestNegativas(unittest.TestCase):
    def test_solo_nombre_no_promociona(self):
        # Casos reales: descripcion == nombre -> pendientes.
        solo = {p["columna"]: p for p in PROP["pendientes_clasificados"]
                if p["motivo"] == "descripcion_solo_reconfirma_nombre"}
        self.assertEqual(len(solo), 3)
        for p in PROP["propuestas_revisadas"]:
            import sys
            sys.path.insert(0, str(ROOT / "scripts"))
            from integrar_contenido import clave
            self.assertNotEqual(clave(p["definicion"]), clave(p["variable"]),
                                p["columna"])

    def test_enie_no_equivale(self):
        def sin_agudos(s):
            return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                           if c not in {"\u0300", "\u0301", "\u0302", "\u0308"})

        def relacion(campo, variable):
            if campo == variable:
                return "exacta"
            if (campo or "").lower() == (variable or "").lower():
                return "caja"
            if sin_agudos(campo).lower() == sin_agudos(variable).lower():
                return "acentos"
            return "diferente"

        self.assertEqual(relacion("Año", "ano"), "diferente")
        self.assertEqual(relacion("AÑO", "AÑO"), "exacta")
        self.assertEqual(relacion("Institucion", "Institución"), "acentos")
        real = [p for p in PROP["pendientes_clasificados"]
                if p["motivo"].startswith("nombre_difiere")]
        self.assertEqual(len(real), 1)
        self.assertIn("ano", real[0]["detalle"] + real[0].get("variable_iri", ""))

    def test_filas_degeneradas_no_promocionadas(self):
        for p in PROP["propuestas_revisadas"]:
            self.assertNotRegex(p["definicion_iri"], r"%2F177$|%2F178$")
            self.assertNotRegex(p.get("variable_iri", ""), r"%2F177$|%2F178$")
            self.assertNotEqual(p["definicion"].strip(), "ide_col")
        self.assertEqual(len(PROP["ambiguos"]), 3)
        for a in PROP["ambiguos"]:
            self.assertEqual(len(a["vinculos"]), 2)
            self.assertTrue(a["pregunta_publicador"])
            self.assertIn("177", a["definiciones_por_nombre"][1])
            self.assertIn("178", a["definiciones_por_nombre"][2])

    def test_contexto_insuficiente_no_promociona(self):
        # Un conjunto con >1 diccionario no asigna alcance: puerta sintetica.
        self.assertTrue(all(
            sum(1 for r in INV["recursos"]
                if r["clasificacion"] == "diccionario"
                and r["conjunto_id"] == p["conjunto"]) == 1
            for p in PROP["propuestas_revisadas"]))
        # Ninguna propuesta depende solo de contexto: todas traen descripcion
        # con aporte y huellas verificadas (comprobado en TestHuellas).
        for p in PROP["propuestas_revisadas"]:
            self.assertTrue(p["evidencia_significado"]["verificacion_por_calificador"])

    def test_catalogo_no_es_observacion(self):
        # Caso real: Clave_Ent en hoja cat_entidad del recurso "Catalogo".
        reales = [p for p in PROP["pendientes_clasificados"]
                  if p["motivo"].startswith("catalogo_no_observacion")]
        self.assertEqual(len(reales), 1)
        self.assertEqual(reales[0]["recurso"], "7f3aca28-4251-48b8-a759-69c992580744")
        # Puerta sintetica: recurso/hoja de catalogo nunca promociona
        # (los acentos se ignoran; la enie se preserva: sin_agudos no toca U+0303).
        def sin_agudos(s):
            return "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                           if c not in {"\u0300", "\u0301", "\u0302", "\u0308"})

        def es_catalogo(nombre_recurso, hoja):
            return ("catalogo" in sin_agudos(nombre_recurso).lower()
                    or (hoja or "").lower().startswith("cat_"))
        self.assertTrue(es_catalogo("Catalogo", "cat_entidad"))
        self.assertTrue(es_catalogo("Catálogo estatal", "Hoja1"))
        self.assertFalse(es_catalogo("Divorcios 2020", "CSV"))
        self.assertFalse(es_catalogo("Fiebre manchada 2023", "Hoja1"))
        # Ninguna propuesta vive en recurso/hoja de catalogo.
        for p in PROP["propuestas_revisadas"]:
            self.assertFalse(es_catalogo(
                p["evidencia_vinculo"]["recurso"]["titulo"],
                p["evidencia_vinculo"]["hoja"]))

    def test_sin_normalizacion_enie(self):
        for n in PROP["normalizaciones_ortograficas"]:
            self.assertNotIn("enie", n.get("detalle", "").lower())
        # Todas las propuestas son exacta: cero normalizaciones.
        self.assertEqual(PROP["conteos"]["normalizaciones_ortograficas"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
