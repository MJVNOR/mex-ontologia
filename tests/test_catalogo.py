import copy
from pathlib import Path
import sys
import unittest

from rdflib import DCAT, DCTERMS as DCT, Graph, RDF, URIRef
from rdflib.compare import isomorphic

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from construir_catalogo import construir


class CatalogoTest(unittest.TestCase):
    def setUp(self):
        self.base = "https://example.org/mex-ontologi/"
        self.portal = "https://datos.sonora.gob.mx/"
        self.time = "2026-10-23T00:00:00+00:00"
        self.registros = [{
            "id": "uuid-1", "name": "nombre con espacios", "title": 'Título "con comillas" y á',
            "notes": "Primera línea\nSegunda línea", "metadata_modified": "2026-10-01T12:00:00",
            "organization": {"id": "org-1", "title": "Organización"},
            "resources": [{"id": "r-1", "name": "Archivo", "url": "", "format": "csv",
                           "start_date": "1989-06-04", "end_date": "1989-06-04", "region": "-", "datastore_active": False}],
        }]

    def build(self, registros=None, base=None):
        return construir(registros or self.registros, base or self.base, self.portal, self.time)

    def test_identidad_no_depende_del_titulo(self):
        g, _, _ = self.build()
        changed = copy.deepcopy(self.registros)
        changed[0]["title"] = "Otro título"
        other, _, _ = self.build(changed)
        self.assertEqual(set(g.subjects(RDF.type, DCAT.Dataset)), set(other.subjects(RDF.type, DCAT.Dataset)))

    def test_campos_ambiguos_no_se_convierten_en_hechos(self):
        g, _, alertas = self.build()
        self.assertFalse(list(g.triples((None, DCT.spatial, None))))
        self.assertFalse(list(g.triples((None, DCT.temporal, None))))
        self.assertFalse(list(g.subjects(RDF.type, DCAT.Distribution)))
        self.assertEqual(len(alertas), 4)
        self.assertIn((URIRef(self.base + "resource/r-1"), URIRef(self.base + "vocab/regionDeclarada"), None), g)

    def test_fechas_de_metadatos_solo_en_registro(self):
        g, _, _ = self.build()
        self.assertFalse(list(g.objects(URIRef(self.base + "dataset/uuid-1"), DCT.modified)))
        self.assertEqual(len(list(g.objects(URIRef(self.base + "record/uuid-1"), DCT.modified))), 1)

    def test_serializacion_preserva_texto_y_grafo(self):
        g, _, _ = self.build()
        restored = Graph().parse(data=g.serialize(format="turtle"), format="turtle")
        self.assertTrue(isomorphic(g, restored))

    def test_base_configurable(self):
        g, schema, _ = self.build(base="https://example.net/nuevo/")
        self.assertFalse(any(str(term).startswith(self.base) for triple in g + schema for term in triple if isinstance(term, URIRef)))


if __name__ == "__main__":
    unittest.main()
