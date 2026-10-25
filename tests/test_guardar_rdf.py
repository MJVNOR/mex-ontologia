import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from rdflib import Graph, Literal, URIRef

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from guardar_rdf import serializar_atomico


class GuardarRDFTest(unittest.TestCase):
    def test_publica_archivo_completo_con_lexico_intacto(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'grafo.ttl'
            path.write_text('anterior', encoding='utf-8')
            graph = Graph()
            graph.add((URIRef('urn:origen'), URIRef('urn:codigo'), Literal(' 0001 á ')))
            serializar_atomico(graph, path)
            actual = Graph().parse(path, format='turtle')
            self.assertEqual(set(graph), set(actual))
            self.assertEqual(list(Path(directory).iterdir()), [path])

    def test_fallo_serializacion_conserva_archivo_previo(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'grafo.ttl'
            path.write_bytes(b'anterior')
            graph = Mock()
            graph.serialize.side_effect = RuntimeError('fallo de serializacion')
            with self.assertRaises(RuntimeError):
                serializar_atomico(graph, path)
            self.assertEqual(path.read_bytes(), b'anterior')
            self.assertEqual(list(Path(directory).iterdir()), [path])
