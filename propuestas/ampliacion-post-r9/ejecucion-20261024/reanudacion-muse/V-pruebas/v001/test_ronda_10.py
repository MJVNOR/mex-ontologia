"""Ronda 10: pruebas sobre material candidato congelado (E/payload/v001).

Solo lee centrales/payload/codigo; no instala ni modifica nada fuera de este
directorio. Localiza ROOT buscando config.toml+scripts en ancestros, por lo
que es instalable luego en tests/ sin cambios. unittest de stdlib, como el
resto de tests/ del repo.
"""
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF

_p = Path(__file__).resolve()
ROOT = next(c for c in (_p, *_p.parents)
            if (c / "config.toml").is_file() and (c / "scripts").is_dir())
E = ROOT / "propuestas" / "ampliacion-post-r9" / "ejecucion-20261024"
sys.path.insert(0, str(ROOT / "scripts"))

_inst = ROOT / "scripts" / "integrar_ronda_10.py"
_kpath = _inst if _inst.is_file() else E / "K-codigo" / "v001" / "scripts" / "integrar_ronda_10.py"
_spec = importlib.util.spec_from_file_location("integrar_ronda_10", _kpath)
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)

_inst_mat = ROOT / "data" / "integracion-ronda-10"
MAT = _inst_mat if (_inst_mat / "aceptadas.json").is_file() else E / "payload" / "v001"

AUD_A = E / "reanudacion-muse" / "A-auditoria" / "v001" / "auditoria-a.json"
AUD_B = E / "reanudacion-muse" / "B-auditoria" / "v001" / "auditoria-b.json"
AUDITS = AUD_A.is_file() and AUD_B.is_file()

ACEPTADAS_SHA = "df5705eaf6e0b8d8dcb0257a54a258264cda3e8adfe8655f87dfda90b9c2031c"
PIN_REGLAS = "dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd"
BASE_IRI = "https://example.org/mex-ontologi/"
IDS = ["Q-U02", "Q-U03", "Q-U04", "Q-U05", "Q-U06"]
FORMAS = sorted([
    "CorrespondenciaRevisadaVariableRespaldada", "UnidadDeclaradaContrato",
    "VariableCandidataConSignificadoCandidato",
    "VariableCandidataSinSignificadoDocumentado",
    "VariableRespaldadaConSignificadoDocumentado",
    "VariableRespaldadaSinSignificadoCandidato"])
SH = Namespace("http://www.w3.org/ns/shacl#")
SUJ02 = "https://example.org/mex-ontologi/declaracion-unidad/r10/Q-U02"

PAYLOAD_16 = (["aceptadas.json", "base-semantica.json", "cobertura-r9.json",
               "config-iri-base.toml", "datos/unidades.ttl",
               "shapes/adicionales.ttl"]
              + [f"filas/{u}.json" for u in IDS]
              + [f"normativa/{u}.txt" for u in IDS])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def aceptadas():
    return json.loads((MAT / "aceptadas.json").read_text(encoding="utf-8"))


def carpeta_mutada(base, cual, agregado, acept=None):
    dest = Path(base) / "m"
    (dest / "datos").mkdir(parents=True)
    (dest / "shapes").mkdir(parents=True)
    shutil.copy(MAT / "datos" / "unidades.ttl", dest / "datos" / "unidades.ttl")
    shutil.copy(MAT / "shapes" / "adicionales.ttl", dest / "shapes" / "adicionales.ttl")
    with open(dest / cual, "a", encoding="utf-8") as fh:
        fh.write("\n" + agregado + "\n")
    return dest, acept if acept is not None else aceptadas()


def construir_raiz(base, auditorias=True, hook=None):
    root = Path(base) / "root"
    (root / "ontologia").mkdir(parents=True)
    folder = root / "data" / "integracion-ronda-10"
    (folder / "auditorias").mkdir(parents=True)
    shutil.copy(ROOT / "config.toml", root / "config.toml")
    shutil.copy(ROOT / "ontologia" / "semantica.json",
                root / "ontologia" / "semantica.json")
    for rel in PAYLOAD_16:
        dest = folder / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(MAT / rel, dest)
    if auditorias:
        shutil.copy(AUD_A, folder / "auditorias" / "a.json")
        shutil.copy(AUD_B, folder / "auditorias" / "b.json")
    files = {rel: sha(folder / rel) for rel in PAYLOAD_16}
    for n in ("a", "b"):
        q = folder / "auditorias" / f"{n}.json"
        if q.is_file():
            files[f"auditorias/{n}.json"] = sha(q)
    (folder / "manifiesto.json").write_text(json.dumps(
        {"format_version": 1, "release": "R10", "archivos": files},
        ensure_ascii=False, sort_keys=True), encoding="utf-8")
    rev = {"format_version": 1, "release": "R10",
           "evidencia": "data/integracion-ronda-10",
           "manifiesto_sha256": sha(folder / "manifiesto.json")}
    (root / "ontologia" / "revision-ronda-10.json").write_text(
        json.dumps(rev, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    if hook:
        hook(root, folder)
    return root


class MaterialCongeladoTest(unittest.TestCase):
    def test_aceptadas_sha_y_cabecera(self):
        self.assertEqual(sha(MAT / "aceptadas.json"), ACEPTADAS_SHA)
        acc = aceptadas()
        self.assertEqual((acc["format_version"], acc["release"], acc["release_base"]),
                         (1, "R10", "R9"))
        self.assertEqual([u["id"] for u in acc["unidades"]], IDS)
        self.assertEqual(sorted(f["id"] for f in acc["formas"]), FORMAS)
        self.assertTrue({"datos", "shapes"} <= set(acc["archivos_instalables"]))

    def test_sello_previo_cubre_payload(self):
        sello = json.loads((E / "sello-payload-previo.json").read_text(encoding="utf-8"))
        self.assertEqual(sello["archivos"]["aceptadas.json"], ACEPTADAS_SHA)
        for rel, digest in sello["archivos"].items():
            with self.subTest(archivo=rel):
                self.assertEqual(sha(MAT / rel), digest)

    def test_unidad_fila_contexto_normativa(self):
        acc = aceptadas()
        qent = json.loads((E / "Q-unidades" / "v003" / "entrega.json")
                          .read_text(encoding="utf-8"))
        for uid in IDS:
            with self.subTest(unidad=uid):
                unit = next(u for u in acc["unidades"] if u["id"] == uid)
                self.assertGreaterEqual(unit["fila"], 1)  # indice 1-based
                fila = json.loads((MAT / f"filas/{uid}.json").read_text(encoding="utf-8"))
                self.assertEqual(K.canon(fila), unit["huella_fila_diccionario"])
                self.assertEqual(fila["Unidad de medida"], unit["unidad_literal"])
                self.assertEqual(fila["Nombre variable"], unit["nombre"])
                caso = next(c for c in qent["casos"] if c["id"] == uid)
                self.assertEqual(caso["indice_definicion"], unit["fila"])
                self.assertEqual(caso["definicion_iri"], unit["definicion_iri"])
                self.assertEqual(caso["diccionario"], unit["diccionario"])
                self.assertEqual(caso["conjunto"], unit["conjunto"])
                fdir = E / "Q-unidades" / "v003" / "fuentes" / uid
                fsrc = json.loads(next(fdir.iterdir()).read_text(encoding="utf-8"))
                reg = fsrc["definiciones"][unit["fila"] - 1]
                self.assertEqual(reg["Nombre variable"], unit["nombre"])
                self.assertEqual(reg["Unidad de medida"], unit["unidad_literal"])
                norm = MAT / f"normativa/{uid}.txt"
                self.assertEqual(sha(norm), unit["normativa_sha256"])
                texto = norm.read_text(encoding="utf-8")
                self.assertIn("3.5.3", texto)
                self.assertIn(unit["normativa_uri"], texto)
                self.assertEqual(unit["normativa_uri"], unit["unidad_qudt"])

    def test_q_u06_datastore_sin_campos_de_fichero(self):
        fdir = E / "Q-unidades" / "v003" / "fuentes" / "Q-U06"
        fsrc = json.loads(next(fdir.iterdir()).read_text(encoding="utf-8"))
        self.assertEqual(fsrc.get("metodo"), "api_diccionario")
        self.assertIsNone(fsrc.get("http"))
        self.assertIsNone(fsrc.get("completo"))
        unit = next(u for u in aceptadas()["unidades"] if u["id"] == "Q-U06")
        self.assertTrue(unit["fuente_url"].startswith(
            "https://datos.sonora.gob.mx/api/3/action/datastore_search?"))

    def test_datos_60_exactos(self):
        g = Graph().parse(MAT / "datos" / "unidades.ttl", format="turtle")
        self.assertEqual(len(g), 60)
        sujetos = {u["sujeto"] for u in aceptadas()["unidades"]}
        self.assertEqual({str(s) for s in g.subjects()}, sujetos)
        K._datos(MAT, aceptadas())  # whitelist estructural completa

    def test_formas_6_ids_y_prov(self):
        g = Graph().parse(MAT / "shapes" / "adicionales.ttl", format="turtle")
        reales = sorted(str(s).rsplit("/", 1)[-1]
                        for s in g.subjects(RDF.type, SH.NodeShape))
        self.assertEqual(reales, FORMAS)
        prov = [o for _, _, o in g
                if str(o).startswith("http://www.w3.org/ns/prov#")]
        self.assertTrue(prov, "sin objetos PROV en shapes")
        K._shapes(MAT, aceptadas())

    def test_snapshot_inmutable(self):
        cob = json.loads((MAT / "cobertura-r9.json").read_text(encoding="utf-8"))
        K.comprobar_resumen(cob["resumen"])  # 1423/1106/4506/17/1442 y resto
        self.assertEqual(sha(MAT / "base-semantica.json"), PIN_REGLAS)
        live = json.loads((ROOT / "ontologia" / "semantica.json")
                          .read_text(encoding="utf-8"))
        base = json.loads((MAT / "base-semantica.json").read_text(encoding="utf-8"))
        self.assertEqual(live, base)
        self.assertEqual((MAT / "config-iri-base.toml").read_bytes(),
                         (ROOT / "config.toml").read_bytes())


class MutacionesRechazoTest(unittest.TestCase):
    def test_rechazo_triple_extra(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest, acc = carpeta_mutada(
                tmp, "datos/unidades.ttl",
                f'<{SUJ02}> <http://example.org/extra> "x" .')
            with self.assertRaises(ValueError):
                K._datos(dest, acc)

    def test_rechazo_objeto_prohibido_m3(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest, acc = carpeta_mutada(
                tmp, "datos/unidades.ttl",
                f'<{SUJ02}> <https://example.org/mex-ontologi/vocab/unidadQudt> '
                '<http://qudt.org/vocab/unit/M3> .')
            with self.assertRaises(ValueError):
                K._datos(dest, acc)

    def test_rechazo_factor_conversion(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest, acc = carpeta_mutada(
                tmp, "datos/unidades.ttl",
                f'<{SUJ02}> <http://qudt.org/schema/qudt/conversionMultiplier> "1.0" .')
            with self.assertRaises(ValueError):
                K._datos(dest, acc)

    def test_rechazo_literal_no_xsd_en_shapes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest, acc = carpeta_mutada(
                tmp, "shapes/adicionales.ttl",
                '<https://example.org/mex-ontologi/shapes/X> '
                '<http://www.w3.org/2000/01/rdf-schema#label> '
                '"x"^^<http://example.org/t> .')
            with self.assertRaises(ValueError):
                K._shapes(dest, acc)

    def test_rechazo_unidad_m3_forma_falsa_y_duplicada(self):
        acc = aceptadas()
        mala = json.loads(json.dumps(acc))
        mala["unidades"][0]["unidad_qudt"] = "http://qudt.org/vocab/unit/M3"
        with self.assertRaises(ValueError):
            K._validar_aceptadas(mala)
        fantasma = json.loads(json.dumps(acc))
        fantasma["formas"].append({"id": "FormaFantasma"})
        with self.assertRaises(ValueError):
            K._shapes(MAT, fantasma)
        duplicada = json.loads(json.dumps(acc))
        duplicada["unidades"].append(dict(duplicada["unidades"][0]))
        with self.assertRaises(ValueError):
            K._validar_aceptadas(duplicada)


class ContratoTemporalTest(unittest.TestCase):
    """cargar/construir/cargar_shapes sobre raiz TEMP con copias exactas.

    Solo genera manifiesto/config temporales de esas copias. Sin auditorias
    reales A/B el contrato positivo queda PENDIENTE declarado (skip
    explicito); los rechazos si se ejecutan con andamio invalido, que nunca
    puede producir aceptacion.
    """

    def test_estado_auditorias_declarado(self):
        if AUDITS:
            for aud in (AUD_A, AUD_B):
                self.assertEqual(
                    json.loads(aud.read_text(encoding="utf-8"))["dictamen"], "aceptar")
        else:
            self.assertFalse((MAT / "auditorias").exists(),
                             "material congelado no finge auditorias")
            self.assertFalse(AUD_A.exists() or AUD_B.exists())

    def test_cargar_contrato(self):
        if not AUDITS:
            self.skipTest("PENDIENTE: sin auditorias reales A/B; re-ejecutable al llegar")
        with tempfile.TemporaryDirectory() as tmp:
            config, _, _, acc, _, _ = K.cargar(construir_raiz(tmp))
            self.assertEqual(config["release"], "R10")
            self.assertEqual(len(acc["unidades"]), 5)

    def test_construir_contrato(self):
        if not AUDITS:
            self.skipTest("PENDIENTE: sin auditorias reales A/B; re-ejecutable al llegar")
        with tempfile.TemporaryDirectory() as tmp:
            root = construir_raiz(tmp)
            folder = root / "data" / "integracion-ronda-10"
            cob = json.loads((folder / "cobertura-r9.json").read_text(encoding="utf-8"))
            base = json.loads((folder / "base-semantica.json").read_text(encoding="utf-8"))
            graph, receipt, _ = K.construir(cob, base, BASE_IRI, root)
            self.assertEqual(receipt["declaraciones_unidad"], 5)
            self.assertEqual(receipt["formas_shacl"], 6)
            self.assertGreater(len(graph), 60)  # 60 datos + trazas PROV

    def test_cargar_shapes_contrato(self):
        if not AUDITS:
            self.skipTest("PENDIENTE: sin auditorias reales A/B; re-ejecutable al llegar")
        with tempfile.TemporaryDirectory() as tmp:
            g = K.cargar_shapes(construir_raiz(tmp))
            self.assertEqual(len(list(g.subjects(RDF.type, SH.NodeShape))), 6)

    def _raiz_con_auditoria_mutada(self, tmp, cual, cambio):
        def hook(root, folder):
            p = folder / "auditorias" / f"{cual}.json"
            if cambio == "retirar":
                if p.is_file():
                    p.unlink()
            else:
                audit = (json.loads(p.read_text(encoding="utf-8")) if p.is_file()
                         else {"auditor": cual, "dictamen": "aceptar",
                               "aceptadas_sha256": "0" * 64, "dictamenes": []})
                if cambio == "sha":
                    audit["aceptadas_sha256"] = "0" * 64
                elif cambio == "casos":
                    audit["dictamenes"] = audit.get("dictamenes", [])[:-1] or []
                elif cambio == "rechazar":
                    audit["dictamen"] = "rechazar"
                elif cambio == "auditor":
                    audit["auditor"] = "otro"
                p.write_text(json.dumps(audit), encoding="utf-8")
            files = {rel: sha(folder / rel) for rel in PAYLOAD_16}
            for n in ("a", "b"):
                q = folder / "auditorias" / f"{n}.json"
                if q.is_file():
                    files[f"auditorias/{n}.json"] = sha(q)
            (folder / "manifiesto.json").write_text(json.dumps(
                {"format_version": 1, "release": "R10", "archivos": files},
                ensure_ascii=False, sort_keys=True), encoding="utf-8")
            rev = {"format_version": 1, "release": "R10",
                   "evidencia": "data/integracion-ronda-10",
                   "manifiesto_sha256": sha(folder / "manifiesto.json")}
            (root / "ontologia" / "revision-ronda-10.json").write_text(
                json.dumps(rev, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        return construir_raiz(tmp, auditorias=AUDITS, hook=hook)

    def test_rechazo_auditoria_retirada_o_cambiada(self):
        for cual in ("a", "b"):
            for cambio in ("retirar", "sha", "casos", "rechazar", "auditor"):
                with self.subTest(auditoria=cual, cambio=cambio):
                    with tempfile.TemporaryDirectory() as tmp:
                        with self.assertRaises(ValueError):
                            K.cargar(self._raiz_con_auditoria_mutada(tmp, cual, cambio))

    def test_rechazo_nucleo_o_iri_cambiados(self):
        def hook_nucleo(root, folder):
            sem = json.loads((root / "ontologia" / "semantica.json")
                             .read_text(encoding="utf-8"))
            sem["cambio_falso_r10"] = True
            (root / "ontologia" / "semantica.json").write_text(
                json.dumps(sem), encoding="utf-8")

        def hook_iri(root, folder):
            txt = (root / "config.toml").read_text(encoding="utf-8")
            (root / "config.toml").write_text(
                txt.replace(BASE_IRI, "https://example.org/otra/"), encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                K.cargar(construir_raiz(tmp, auditorias=AUDITS, hook=hook_nucleo))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                K.cargar(construir_raiz(tmp, auditorias=AUDITS, hook=hook_iri))


if __name__ == "__main__":
    unittest.main()
