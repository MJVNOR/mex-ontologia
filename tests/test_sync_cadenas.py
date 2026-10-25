from pathlib import Path
import sys
import unittest

from rdflib import Graph, Literal, Namespace, XSD
from rdflib.compare import isomorphic

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from sincronizar_studio_portal import cambios, normalizar_cadenas


class CadenasSyncTest(unittest.TestCase):
    def test_xsd_string_y_literal_simple_no_producen_cambios_ni_pierden_propiedad(self):
        ns = Namespace('https://example.org/')
        desired = Graph().add((ns.variable, ns.codigo, Literal(' 001 ', datatype=XSD.string)))
        actual = Graph().add((ns.variable, ns.codigo, Literal(' 001 ')))
        normalized = normalizar_cadenas(desired)
        self.assertTrue(isomorphic(normalized, normalizar_cadenas(actual)))
        remove, add, owned = cambios(normalizar_cadenas(actual), normalized, normalized)
        self.assertEqual((len(remove), len(add), len(owned)), (0, 0, 1))
        self.assertEqual(str(normalized.value(ns.variable, ns.codigo)), ' 001 ')

    def test_idiomas_y_tipos_distintos_se_preservan(self):
        ns = Namespace('https://example.org/')
        graph = Graph().add((ns.a, ns.p, Literal('uno', lang='es')))
        graph.add((ns.b, ns.p, Literal(1, datatype=XSD.integer)))
        graph.add((ns.c, ns.p, Literal('001')))
        normalized = normalizar_cadenas(graph)
        self.assertEqual(normalized.value(ns.a, ns.p).language, 'es')
        self.assertEqual(normalized.value(ns.b, ns.p).datatype, XSD.integer)
        self.assertNotEqual(normalized.value(ns.b, ns.p), normalized.value(ns.c, ns.p))


if __name__ == '__main__':
    unittest.main()
