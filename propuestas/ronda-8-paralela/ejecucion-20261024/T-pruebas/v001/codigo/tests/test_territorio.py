import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from rdflib import Namespace, RDF, OWL, SKOS

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists()) / 'scripts'))
from integrar_territorio import comparar, reparar_comparacion, construir, aplicar_alias
from extraer_catalogos_territoriales import codigo, extraer
import openpyxl


class TerritorioTest(unittest.TestCase):
    def setUp(self):
        self.base = 'https://example.org/test/'
        self.mex = Namespace(self.base + 'vocab/')
        self.reference = {'recurso_id': 'geo', 'fuente': 'https://example.org/map', 'municipios': [
            {'cvegeo': '26' + str(i).zfill(3), 'nombre': 'Municipio ' + str(i)} for i in range(1, 73)]}
        self.ref = {'recurso': 'r', 'conjunto': 'd', 'titulo_conjunto': 'Sonora', 'fuente': 'https://example.org/catalog.xlsx',
                    'archivo_sha256': 'a' * 64, 'hoja': 'Municipios', 'nivel': 'municipio_local', 'campo_codigo': 'MUNI',
                    'posicion_codigo': 1, 'alcance': 'Sonora', 'entradas': [
                        {'codigo': '1', 'nombre': 'Municipio 1', 'celda_codigo': 'A2', 'celda_nombre': 'B2'}]}
        self.inventory = {'recursos': [{'id': 'r', 'conjunto_id': 'd', 'url': self.ref['fuente']}]}

    def build(self, refs=None, rules=None, semantic=None):
        return construir({'referencias': refs or [self.ref]}, rules or {'limite': 'Instantánea, sin vigencia histórica', 'resoluciones': []},
                         self.inventory, semantic or {'variables': []}, self.reference, self.base)

    def test_conserva_ceros_y_rechaza_codigos_fraccionarios(self):
        self.assertEqual(codigo('001'), '001')
        self.assertEqual(codigo(1.0), '1')
        for value in [1.5, float('nan'), True, '1.0', ' 01', None]:
            with self.assertRaises(ValueError):
                codigo(value)

    def test_codigo_coincidente_no_basta_con_nombre_distinto(self):
        result = comparar({'codigo': '1', 'nombre': 'Otro municipio'}, 'municipio_local', {'26001': {'nombre': 'Aconchi'}})
        self.assertEqual(result['estado'], 'pendiente_nombre_distinto')

    def test_alias_usuario_se_limita_a_sus_entradas_y_conserva_nombres(self):
        self.ref['entradas'][0]['nombre'] = 'Magdalena de Kino'
        self.reference['municipios'][0]['nombre'] = 'Magdalena'
        alias = {'id': 'magdalena-test', 'archivo_sha256': self.ref['archivo_sha256'], 'hoja': 'Municipios',
                 'codigo_origen': '1', 'nombre_origen': 'Magdalena de Kino', 'recurso_destino': 'geo',
                 'codigo_destino': '26001', 'nombre_destino_original': 'Magdalena', 'criterio': 'Aclaración del usuario',
                 'evidencia_usuario': 'Es el mismo municipio', 'fecha_revision': '2026-10-23'}
        data, _, report = self.build(rules={'limite': 'Instantánea', 'resoluciones': [], 'aliases_revisados': [alias]})
        self.assertEqual(report['resumen']['estados_correspondencias'], {'codigo_y_alias_revisado': 1})
        self.assertEqual(len(list(data.triples((None, self.mex.entradaTerritorialDestino, None)))), 1)
        self.assertEqual(report['correspondencias'][0]['nombre_origen'], 'Magdalena de Kino')
        self.assertEqual(report['correspondencias'][0]['nombre_destino_original'], 'Magdalena')
        other = {**self.ref, 'archivo_sha256': 'b' * 64}
        assessment = comparar(self.ref['entradas'][0], 'municipio_local', {'26001': {'nombre': 'Magdalena'}})
        self.assertEqual(aplicar_alias(other, self.ref['entradas'][0], assessment, self.reference, [alias])['estado'], 'pendiente_nombre_distinto')
        alias['nombre_destino_original'] = 'Un nombre distinto'
        with self.assertRaisesRegex(ValueError, 'Evidencia de alias cambió'):
            self.build(rules={'limite': 'Instantánea', 'resoluciones': [], 'aliases_revisados': [alias]})

    def test_reparacion_es_derivada_y_conserva_el_texto_original(self):
        raw = 'Peñasco'.encode('utf-8').decode('latin1')
        row = {'codigo': '26048', 'nombre': 'PEÑASCO'}
        result = comparar(row, 'municipio_compuesto', {'26048': {'nombre': raw}})
        self.assertEqual(result['nombre_destino_original'], raw)
        self.assertEqual(result['nombre_destino_para_comparar'], 'Peñasco')
        self.assertEqual(result['estado'], 'codigo_y_nombre_con_reparacion_codificacion')
        self.assertEqual(reparar_comparacion('Peñasco'), ('Peñasco', False))
        self.assertEqual(reparar_comparacion('Ónavas'.encode('utf-8').decode('cp1252')), ('Ónavas', True))

    def test_categorias_especiales_no_tienen_destino_municipal(self):
        ref = copy.deepcopy(self.ref)
        ref['nivel'] = 'municipio_compuesto'
        ref['entradas'] = [{'codigo': '26998', 'nombre': 'No Especificado', 'celda_codigo': 'A2', 'celda_nombre': 'B2'},
                           {'codigo': '26999', 'nombre': 'Otros Municipios', 'celda_codigo': 'A3', 'celda_nombre': 'B3'}]
        data, _, report = self.build([ref])
        self.assertEqual(report['resumen']['estados_correspondencias'], {'categoria_no_municipal': 2})
        self.assertFalse(list(data.triples((None, self.mex.entradaTerritorialDestino, None))))

    def test_copias_identicas_comparten_entradas_y_conservan_fuentes(self):
        ref = copy.deepcopy(self.ref)
        ref.update(recurso='r2', fuente='https://example.org/catalog2.xlsx')
        self.inventory['recursos'].append({'id': 'r2', 'conjunto_id': 'd', 'url': ref['fuente']})
        data, _, report = self.build([self.ref, ref])
        self.assertEqual(report['resumen']['referencias_distintas_por_archivo_hoja'], 1)
        self.assertEqual(report['resumen']['entradas_distintas'], 1)
        self.assertEqual(sum(report['resumen']['estados_correspondencias'].values()), 1)
        self.assertFalse(list(data.triples((None, OWL.sameAs, None))))
        self.assertFalse(list(data.triples((None, SKOS.exactMatch, None))))
        self.assertFalse(list(data.triples((None, self.mex.usaSistemaIdentificadores, None))))

    def test_clave_duplicada_se_rechaza(self):
        self.ref['entradas'] *= 2
        with self.assertRaisesRegex(ValueError, 'Código repetido'):
            self.build()

    def test_cambio_de_catalogo_invalida_resolucion(self):
        rule = {'recurso': 'r', 'hoja': 'Municipios', 'diccionario': 'dic', 'variable': 'MUNI',
                'archivo_sha256': 'b' * 64, 'huella_fila_diccionario': 'c' * 64, 'criterio': 'Revisado'}
        variable = {'diccionario': 'dic', 'variable': 'MUNI', 'huella_fila_diccionario': 'c' * 64, 'conjunto': 'd',
                    'catalogo_declarado': 'Municipios', 'iri': self.base + 'variable', 'definicion_iri': self.base + 'definition'}
        with self.assertRaisesRegex(ValueError, 'Evidencia de catálogo cambió'):
            self.build(rules={'limite': 'Sin vigencia', 'resoluciones': [rule]}, semantic={'variables': [variable]})

    def test_fuente_de_otro_conjunto_no_se_acepta(self):
        self.ref['conjunto'] = 'otro'
        with self.assertRaisesRegex(ValueError, 'no coincide'):
            self.build()

    def test_extraccion_no_descarta_errores_despues_de_la_muestra(self):
        with tempfile.TemporaryDirectory(dir=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())) as folder:
            path = Path(folder) / 'catalog.xlsx'
            book = openpyxl.Workbook()
            sheet = book.active
            sheet.title = 'Municipios'
            sheet.append(['MUNI', 'MUNICIPIOS'])
            for i in range(1, 73):
                sheet.append([i, 'Municipio ' + str(i)])
            sheet.append([72, 'Repetido al final'])
            book.save(path)
            book.close()
            resource = {'id': 'r', 'conjunto_id': 'd', 'conjunto': 'Sonora', 'url': 'https://example.org/catalog.xlsx'}
            with self.assertRaisesRegex(ValueError, 'Clave repetida'):
                extraer(path, resource, ['Municipios'])


if __name__ == '__main__':
    unittest.main()
