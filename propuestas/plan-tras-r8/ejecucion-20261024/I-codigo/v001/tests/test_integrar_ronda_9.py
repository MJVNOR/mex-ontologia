"""Regresion R9 (staging I-codigo/v001): solo Q1/Q3 + shape P4, nada de nucleo.

Todo el arbol de evidencia es sintetico bajo tmp: no toca produccion ni lo
congelado. Las auditorias fake solo existen en tmp. Importa el integrador
desde el staging (scripts/integrar_ronda_9.py), no desde scripts/.
"""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve()
STAGING = _HERE.parents[1]
REPO = next(p for p in _HERE.parents if (p / "scripts" / "construir_catalogo.py").exists())
sys.path.insert(0, str(STAGING / "scripts"))
sys.path.insert(0, str(REPO / "scripts"))

import integrar_ronda_9 as r9

BASE_IRI = "https://example.org/mex-ontologi/"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


DATOS_TTL = """@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
<{s1}> a mex:UnidadDeclarada ;
    mex:variableDocumentada <{v1}> ;
    mex:definicionFuente <{d1}> ;
    mex:unidadLiteral "{u1}" ;
    mex:unidadQudt <{q1}> ;
    mex:estadoPropuesta "propuesta_para_auditar" ;
    prov:wasDerivedFrom <{q1}> .
<{s2}> a mex:UnidadDeclarada ;
    mex:variableDocumentada <{v2}> ;
    mex:definicionFuente <{d2}> ;
    mex:unidadLiteral "{u2}" ;
    mex:unidadQudt <{q2}> ;
    mex:estadoPropuesta "propuesta_para_auditar" ;
    prov:wasDerivedFrom <{q2}> .
"""

MODELO_TTL = """@prefix mex: <https://example.org/mex-ontologi/vocab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
mex:UnidadDeclarada a rdfs:Class .
mex:unidadQudt a rdfs:Property .
mex:variableDocumentada a rdfs:Property .
"""

Q1 = r9.DECL_PIN["P1-Q1"]
Q3 = r9.DECL_PIN["P1-Q3"]

COB_VARS = [
    {"definicion_iri": Q1["definicion_iri"], "iri": Q1["variable"], "variable": "Precipitacion_mm",
     "descripcion": "Cantidad de lluvia registrada en el dia por municipio",
     "estado": "respaldada_por_definicion", "concepto": "precipitacion-diaria",
     "conjunto": Q1["conjunto"], "diccionario": Q1["diccionario"],
     "huella_fila_diccionario": Q1["huella_fila_diccionario"]},
    {"definicion_iri": Q3["definicion_iri"], "iri": Q3["variable"], "variable": "SUPSEM",
     "descripcion": "Cantidad de hectareas sembradas.",
     "estado": "respaldada_por_definicion", "concepto": "superficie-sembrada-cultivo",
     "conjunto": Q3["conjunto"], "diccionario": Q3["diccionario"],
     "huella_fila_diccionario": Q3["huella_fila_diccionario"]},
    {"definicion_iri": "https://example.org/mex-ontologi/definition/xxxx%2F1", "iri": "https://example.org/mex-ontologi/documented-variable/xxxx%2F1",
     "variable": "OTRA", "descripcion": "Otra", "estado": "candidata_sin_definicion_suficiente",
     "concepto": "tiempo", "conjunto": "c", "diccionario": "d", "huella_fila_diccionario": "00"},
]

RESUMEN_R8 = {"estados_variables": {"respaldada_por_definicion": 1423},
              "conceptos_compartidos": 1106,
              "estados_correspondencias": {"documental_revisada": 4506, "candidata_por_nombre": 17},
              "variables_materializadas": 1442}


def _decl_row(pin):
    return {"id": None, "sujeto": pin["sujeto"], "variable": pin["variable"],
            "definicion_iri": pin["definicion_iri"], "unidad_literal": pin["unidad_literal"],
            "unidad_qudt": pin["unidad_qudt"], "diccionario": pin["diccionario"],
            "conjunto": pin["conjunto"],
            "huella_fila_diccionario": pin["huella_fila_diccionario"],
            "normativa": dict(pin["normativa"])}


def make_root(tmp):
    tmp = Path(tmp)
    folder = tmp / "data/integracion-ronda-9"
    (folder / "datos").mkdir(parents=True)
    (folder / "modelo").mkdir()
    (folder / "shapes").mkdir()
    (folder / "auditorias").mkdir()
    (folder / "datos/propuesta-qudt.ttl").write_text(DATOS_TTL.format(
        s1=Q1["sujeto"], v1=Q1["variable"], d1=Q1["definicion_iri"], u1=Q1["unidad_literal"], q1=Q1["unidad_qudt"],
        s2=Q3["sujeto"], v2=Q3["variable"], d2=Q3["definicion_iri"], u2=Q3["unidad_literal"], q2=Q3["unidad_qudt"]), encoding="utf-8")
    (folder / "modelo/vocabulario-minimo.ttl").write_text(MODELO_TTL, encoding="utf-8")
    shutil.copyfile(STAGING / "data-integracion-ronda-9/shapes/shape-exclusion-significado.ttl",
                    folder / "shapes/shape-exclusion-significado.ttl")
    base = {"conceptos": {"c": ["C", "D", None]}, "reglas_descripcion_exacta": [],
            "vinculos_documentales_revisados": []}
    (folder / "base-semantica.json").write_text(json.dumps(base), encoding="utf-8")
    (folder / "cobertura-r8.json").write_text(json.dumps(
        {"resumen": copy.deepcopy(RESUMEN_R8), "variables": copy.deepcopy(COB_VARS)}), encoding="utf-8")
    rows = []
    for pid, pin in (("P1-Q1", Q1), ("P1-Q3", Q3)):
        row = _decl_row(pin)
        row["id"] = pid
        rows.append(row)
    accepted = {"format_version": 1, "release_base": "R8", "release_propuesta": "R9",
                "reglas": [], "conceptos": {}, "vinculos": [], "declaraciones": rows,
                "origenes": {"P1-Q1": ["datos/propuesta-qudt.ttl"],
                             "P1-Q3": ["datos/propuesta-qudt.ttl"]},
                "resumen": {"declaraciones_unidad_nuevas": 2}}
    (folder / "aceptadas.json").write_text(json.dumps(accepted, ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp / "ontologia").mkdir(parents=True, exist_ok=True)
    # Insumos vivos espejados (solo lectura): inspecciones + normativa W.
    for dic in (Q1["diccionario"], Q3["diccionario"]):
        dest = tmp / "data/portal/inspecciones" / (dic + ".json")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / "data/portal/inspecciones" / (dic + ".json"), dest)
    for pid in ("P1-Q1", "P1-Q3"):
        rel = r9.DECL_PIN[pid]["normativa"]["archivo"]
        dest = tmp / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / rel, dest)
    sha_acep = _sha(folder / "aceptadas.json")
    for name in ("auditoria-a", "auditoria-b"):
        (folder / "auditorias" / (name + ".json")).write_text(json.dumps(
            {"dictamen": "aceptar", "aceptadas_sha256": sha_acep,
             "dictamenes": [{"tipo": "declaraciones", "id": "P1-Q1", "dictamen": "aceptar"},
                            {"tipo": "declaraciones", "id": "P1-Q3", "dictamen": "aceptar"}]}), encoding="utf-8")
    repin(tmp, folder)
    return tmp, folder, base, accepted


def repin(tmp, folder):
    tmp, folder = Path(tmp), Path(folder)
    manifest = {"formato": "r9-v001", "format_version": 1, "release_base": "R8",
                "archivos": {p.relative_to(folder).as_posix(): _sha(p)
                             for p in sorted(folder.rglob("*")) if p.is_file() and p.name != "manifiesto.json"},
                "insumos": {r9.DECL_PIN[pid]["normativa"]["archivo"]: _sha(tmp / r9.DECL_PIN[pid]["normativa"]["archivo"])
                            for pid in ("P1-Q1", "P1-Q3")}}
    (folder / "manifiesto.json").write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    (tmp / "ontologia/revision-ronda-9.json").write_text(json.dumps(
        {"evidencia": "data/integracion-ronda-9",
         "manifiesto_sha256": _sha(folder / "manifiesto.json")}), encoding="utf-8")


def _report(extra_vars=True):
    return {"resumen": copy.deepcopy(RESUMEN_R8),
            "variables": copy.deepcopy(COB_VARS),
            "correspondencias": []}


class TestRonda9(unittest.TestCase):
    def test_valido(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            config, f2, baseline, acc, cob8, sources = r9.cargar(Path(root))
            self.assertEqual({d["id"] for d in acc["declaraciones"]}, {"P1-Q1", "P1-Q3"})
            g, rep, src = r9.construir(_report(), copy.deepcopy(base), BASE_IRI, Path(root))
            self.assertEqual(rep["release"], "R9")
            mex = "https://example.org/mex-ontologi/vocab/"
            sujetos = {str(s) for s in g.subjects(
                __import__("rdflib").URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                __import__("rdflib").URIRef(mex + "UnidadDeclarada"))}
            self.assertEqual(sujetos, {Q1["sujeto"], Q3["sujeto"]})
            shapes = r9.cargar_shapes(Path(root))
            self.assertGreater(len(shapes), 0)

    def test_manifiesto_modificado_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            (folder / "manifiesto.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_unidad_literal_distinta_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            a = json.loads((folder / "aceptadas.json").read_text(encoding="utf-8"))
            a["declaraciones"][0]["unidad_literal"] = "Metros"
            (folder / "aceptadas.json").write_text(json.dumps(a), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_q2_colado_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            a = json.loads((folder / "aceptadas.json").read_text(encoding="utf-8"))
            q2 = _decl_row(Q1)
            q2.update(id="P1-Q2", unidad_qudt="http://qudt.org/vocab/unit/M3")
            a["declaraciones"].append(q2)
            (folder / "aceptadas.json").write_text(json.dumps(a), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_origen_fuera_de_manifiesto_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            a = json.loads((folder / "aceptadas.json").read_text(encoding="utf-8"))
            a["origenes"]["P1-Q1"] = ["datos/inexistente.ttl"]
            (folder / "aceptadas.json").write_text(json.dumps(a), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_normativa_modificada_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            (Path(root) / Q1["normativa"]["archivo"]).write_text("TAMPERED", encoding="utf-8")
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_auditoria_global_no_aceptar_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            for name in ("auditoria-a", "auditoria-b"):
                p = folder / "auditorias" / (name + ".json")
                au = json.loads(p.read_text(encoding="utf-8"))
                au["dictamen"] = "observar"
                p.write_text(json.dumps(au), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.construir(_report(), copy.deepcopy(base), BASE_IRI, Path(root))

    def test_auditoria_sin_caso_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            p = folder / "auditorias" / "auditoria-b.json"
            au = json.loads(p.read_text(encoding="utf-8"))
            au["dictamenes"] = [d for d in au["dictamenes"] if d["id"] != "P1-Q3"]
            p.write_text(json.dumps(au), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.construir(_report(), copy.deepcopy(base), BASE_IRI, Path(root))

    def test_aceptadas_remendada_tras_pin_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            a = json.loads((folder / "aceptadas.json").read_text(encoding="utf-8"))
            a["declaraciones"][0]["unidad_literal"] = "Milimetros "
            (folder / "aceptadas.json").write_text(json.dumps(a), encoding="utf-8")
            repin(root, folder)  # repin NO toca auditorias: pin viejo
            with self.assertRaises(ValueError):
                r9.construir(_report(), copy.deepcopy(base), BASE_IRI, Path(root))

    def test_shape_modificado_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            p = folder / "shapes/shape-exclusion-significado.ttl"
            p.write_text(p.read_text(encoding="utf-8").replace("sh:sparql", "sh:property"), encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_shape_sin_estructura_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            p = folder / "shapes/shape-exclusion-significado.ttl"
            txt = p.read_text(encoding="utf-8").replace("sh:sparql", "sh:property")
            p.write_text(txt, encoding="utf-8")
            viejo = r9.SHAPE_SHA
            r9.SHAPE_SHA = _sha(p)
            try:
                repin(root, folder)
                with self.assertRaisesRegex(ValueError, "estructura"):
                    r9.cargar(Path(root))
            finally:
                r9.SHAPE_SHA = viejo

    def test_ruta_escape_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            (Path(root) / "escape.json").write_text("{}", encoding="utf-8")
            m = json.loads((folder / "manifiesto.json").read_text(encoding="utf-8"))
            m["archivos"]["../escape.json"] = _sha(Path(root) / "escape.json")
            (folder / "manifiesto.json").write_text(json.dumps(m, sort_keys=True), encoding="utf-8")
            (Path(root) / "ontologia/revision-ronda-9.json").write_text(json.dumps(
                {"evidencia": "data/integracion-ronda-9",
                 "manifiesto_sha256": _sha(folder / "manifiesto.json")}), encoding="utf-8")
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_nucleo_editado_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            rules = copy.deepcopy(base)
            rules["conceptos"]["nuevo"] = ["N", "D", None]
            with self.assertRaises(ValueError):
                r9.construir(_report(), rules, BASE_IRI, Path(root))

    def test_conversion_colada_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            p = folder / "datos/propuesta-qudt.ttl"
            p.write_text(p.read_text(encoding="utf-8") + "\n# QuantityValue\n", encoding="utf-8")
            repin(root, folder)
            with self.assertRaises(ValueError):
                r9.cargar(Path(root))

    def test_pin_reporte_vivo_roto_se_rechaza(self):
        with tempfile.TemporaryDirectory() as t:
            root, folder, base, accepted = make_root(t)
            rep = _report()
            rep["resumen"]["estados_variables"]["respaldada_por_definicion"] = 1424
            with self.assertRaises(ValueError):
                r9.construir(rep, copy.deepcopy(base), BASE_IRI, Path(root))

    def test_staging_ttl_son_exactamente_q1_q3(self):
        from rdflib import URIRef
        g = __import__("rdflib").Graph()
        g.parse(STAGING / "data-integracion-ronda-9/datos/propuesta-qudt.ttl", format="turtle")
        mex = "https://example.org/mex-ontologi/vocab/"
        sujetos = {str(s) for s in g.subjects(
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(mex + "UnidadDeclarada"))}
        self.assertEqual(sujetos, {Q1["sujeto"], Q3["sujeto"]})
        for s, q in ((Q1["sujeto"], Q1["unidad_qudt"]), (Q3["sujeto"], Q3["unidad_qudt"])):
            self.assertEqual({str(o) for o in g.objects(URIRef(s), URIRef(mex + "unidadQudt"))}, {q})

    def test_shape_staging_es_p4_v001(self):
        self.assertEqual(_sha(STAGING / "data-integracion-ronda-9/shapes/shape-exclusion-significado.ttl"),
                         r9.SHAPE_SHA)
        self.assertEqual(_sha(REPO / "propuestas/plan-tras-r8/ejecucion-20261024/P4-shacl-versionado/v001/propuesta/shape-exclusion-significado.ttl"),
                         r9.SHAPE_SHA)


if __name__ == "__main__":
    unittest.main()
