import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from mcp_compartido import Cliente, verificar_consulta


class Compartido(unittest.TestCase):
    def test_ignora_evento_sse_vacio_y_conserva_sesion(self):
        class Response:
            headers = {'Mcp-Session-Id': 'sesion-prueba'}
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self):
                return b'data: \nid: 0\nretry: 3000\n\ndata: {"jsonrpc":"2.0","id":1,"result":{"ok":true}}\n\n'
        client = Cliente('http://127.0.0.1:1/mcp', 'solo-prueba')
        with patch('mcp_compartido.urlopen', return_value=Response()):
            self.assertEqual(client.rpc('ping', {}), {'ok': True})
        self.assertEqual(client.headers['Mcp-Session-Id'], 'sesion-prueba')

    def test_limite_real_no_comentario_ni_literal(self):
        for q in ('SELECT * WHERE {?s ?p ?o} # LIMIT 1',
                  'SELECT * WHERE {?s ?p "LIMIT 1"}',
                  'SELECT * WHERE {{SELECT * WHERE {?s ?p ?o} LIMIT 1}}',
                  'SELECT * WHERE {?s ?p ?o} LIMIT 2001',
                  'DELETE WHERE {?s ?p ?o}',
                  'SELECT * WHERE {SERVICE <https://example.org> {?s ?p ?o}} LIMIT 1'):
            with self.assertRaises(ValueError):
                verificar_consulta(q)
        verificar_consulta('PREFIX x: <https://example.org/> SELECT * WHERE {?s ?p ?o} LIMIT 2000')


if __name__ == '__main__':
    unittest.main()
