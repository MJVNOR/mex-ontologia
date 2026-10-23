import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from rdflib import Graph, Namespace, Literal, URIRef, RDF, OWL

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from inspeccionar_contenido import encabezado, tablas
from integrar_contenido import integrar, valor
from cruzar_registro_civil import entero, agregar


class ContenidoTest(unittest.TestCase):
    def test_codigos_no_pierden_precision_ni_aceptan_fracciones(self):
        self.assertEqual(entero('036'), 36)
        self.assertEqual(entero('36.0'), 36)
        for value in ('3.6', '', None, True, 'NaN'):
            with self.assertRaises(ValueError):
                entero(value)

    def test_encabezado_diccionario_supera_titulo_y_filas(self):
        start, fields = encabezado([['Diccionario'], ['Nombre variable', 'Descripción'], ['x', 'Municipio']])
        self.assertEqual(start, 1)
        self.assertEqual(fields[0]['id'], 'Nombre variable')

    def test_csv_parcial_descarta_ultima_fila_incompleta(self):
        self.assertEqual(tablas(b'a,b\n1,2\n3,', 'CSV', False)[0][1], [['a', 'b'], ['1', '2']])

    def test_etiquetas_diccionario_aceptan_coma_y_variantes(self):
        self.assertEqual(valor({'Nombre variable,': ' municipio '}, {'nombre variable'}), 'municipio')

    def test_paginacion_duplicada_falla(self):
        responses = [{'ok': True, 'url': 'https://example.org/api', 'result': {'total': 2, 'records': [{'_id': 1, 'municipio': 1, 'año': 2022}]}},
                     {'ok': True, 'url': 'https://example.org/api', 'result': {'total': 2, 'records': [{'_id': 1, 'municipio': 1, 'año': 2022}]}}]
        with patch('cruzar_registro_civil.api', side_effect=responses):
            with self.assertRaisesRegex(RuntimeError, 'duplicado'):
                agregar({'id': 'r'}, 'año')

    def test_campos_repetidos_y_valor_ausente_no_se_inventan(self):
        base = 'https://example.org/'
        mex = Namespace(base + 'vocab/')
        resource = {'id': 'r', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'nombre': 'Datos', 'clasificacion': 'datos_estructurados'}
        inventory = {'recursos': [resource]}
        inspection = {'generado_en_utc': '2026-10-23T00:00:00Z', 'recursos': [
            {'id': 'r', 'ok': True, 'fuente': 'https://example.org/datos', 'consultado_en_utc': '2026-10-23T00:00:00Z',
             'tablas': [{'hoja': 'Hoja1', 'fila_encabezado': 1, 'metodo_encabezado': 'heuristica',
                         'campos': [{'id': 'municipio', 'posicion_original': 1}, {'id': 'municipio', 'posicion_original': 2}]}]}]}
        cross = {'fuentes': [{'consultas': ['https://example.org/api'], 'recurso_id': 'r', 'diccionario_id': 'dic'}],
                 'alcance': 'Exploratorio', 'metodo': 'Unión externa', 'limites': ['Sin equivalencias oficiales'],
                 'filas': [{'codigo_municipio_fuente': 1, 'anio_registro': 2022, 'presente_en_ambas': False,
                            'registros_matrimonios': 2, 'registros_divorcios': None}]}
        graph, _, report = integrar(inventory, inspection, cross, base)
        self.assertEqual(len(set(graph.subjects(RDF.type, mex.ColumnaObservada))), 2)
        self.assertFalse(list(graph.triples((None, mex.conteoDivorcios, None))))
        self.assertFalse(list(graph.triples((None, OWL.sameAs, None))))
        self.assertEqual(report['cruce']['codigos_en_ambas'], 0)


if __name__ == '__main__':
    unittest.main()
