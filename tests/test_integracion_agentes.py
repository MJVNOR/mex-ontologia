import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import interpretacion
from integrar_entregas import composicion_exacta, construir, leer_tabla


class IntegracionAgentesTest(unittest.TestCase):
    def test_composicion_no_acepta_prefijo_corto_letras_ni_digitos_unicode(self):
        self.assertTrue(composicion_exacta('26001', '26'))
        for municipal, entidad in [('26001', '2'), ('26ABC', '26'), ('２６００１', '２６'),
                                    ('٢٦٠٠١', '٢٦'), ('26¹23', '26'), ('26001', '27'), (None, '26')]:
            self.assertFalse(composicion_exacta(municipal, entidad))

    def test_las_20_reglas_no_alcanzan_otro_diccionario_conjunto_o_definicion(self):
        rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        proposals = json.loads((ROOT / 'data/integracion/entregas/agente-3-significados/propuestas.json').read_text(encoding='utf-8'))
        for v in proposals['variables']:
            if v['decision'] != 'proponer':
                continue
            args = [v['variable'], v['descripcion_literal'], v['conjunto'], rules, v['diccionario'], v['definicion_iri']]
            expected = v['regla_propuesta']['id']
            self.assertEqual(interpretacion(*args)['regla'], expected)
            for pos in [2, 4, 5]:
                other = args.copy(); other[pos] = 'otra-fuente'
                self.assertNotEqual(interpretacion(*other).get('regla'), expected)

    def test_62_revisiones_previas_se_conservan_integramente(self):
        manifest = json.loads((ROOT / 'data/integracion/manifiesto.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(ROOT / manifest['respaldo']) as z:
            before = json.loads(z.read('ontologia/semantica.json'))
        after = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        self.assertEqual(len(before['vinculos_documentales_revisados']), 62)
        config = json.loads((ROOT / 'ontologia/revision-agentes.json').read_text(encoding='utf-8'))
        self.assertEqual(len(after['vinculos_documentales_revisados']),
                         config.get('esperado_actual', config['esperado'])['correspondencias_revisadas'])
        for item in before['vinculos_documentales_revisados']:
            self.assertIn(item, after['vinculos_documentales_revisados'])

    def test_un_manifiesto_modificado_impide_generar(self):
        with patch('integrar_entregas.sha', return_value='0' * 64):
            with self.assertRaisesRegex(ValueError, 'Manifiesto'):
                construir(None, None, None, None, 'https://example.org/test/')

    def test_lector_conserva_ceros_texto_y_rechaza_formulas(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'referencia.xlsx'
            wb = Workbook(); sh = wb.active; sh.append(['Clave', 'Nombre']); sh.append(['001', 'Educación']); wb.save(path)
            self.assertEqual(leer_tabla(path)[1], ['001', 'Educación'])
            sh['A2'] = '=1+1'; wb.save(path); wb.close()
            with self.assertRaisesRegex(ValueError, 'Fórmula'):
                leer_tabla(path)


if __name__ == '__main__':
    unittest.main()
