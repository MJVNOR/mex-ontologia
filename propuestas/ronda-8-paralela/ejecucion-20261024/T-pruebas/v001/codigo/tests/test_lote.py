from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists()) / 'scripts'))
from validar_lote_cruces import normalizar_clave, unir, unir_educacion, diagnosticar_valores, agregar_validado


class LoteTest(unittest.TestCase):
    def test_normalizacion_no_homologa_codigos_ni_acentos(self):
        self.assertEqual(normalizar_clave('  001 '), '001')
        self.assertNotEqual(normalizar_clave('001'), normalizar_clave('1'))
        self.assertNotEqual(normalizar_clave('Alamos'), normalizar_clave('Álamos'))

    def test_nulos_y_cardinalidad_solo_muestral(self):
        x = diagnosticar_valores([{'m': '1'}, {'m': '1'}, {'m': None}], ['m'])['m']
        self.assertEqual((x['nulos'], x['repeticiones_muestra'], x['distintos_muestra']), (1, 1, 1))

    def test_union_no_rellena_ceros(self):
        a = {'ok': True, 'agregados': [{'municipio_local': 1, 'anio_registro': 2022, 'valor': 4}]}
        b = {'ok': True, 'agregados': [{'municipio_local': 2, 'anio_registro': 2022, 'valor': 5}]}
        rows = unir(a, b)
        self.assertIsNone(rows[0]['valor_b'])
        self.assertEqual(len(rows), 2)

    def test_no_une_resultado_fallido(self):
        with self.assertRaises(ValueError):
            unir({'ok': False}, {'ok': True})

    def test_grano_repetido_no_multiplica_filas(self):
        row = {'municipio_local': 1, 'anio_registro': 2022, 'valor': 4}
        with self.assertRaisesRegex(ValueError, 'único'):
            unir({'ok': True, 'agregados': [row, row]}, {'ok': True, 'agregados': []})

    def run_births(self, rows):
        strategy = {'campos': ['_id', 'municipio', 'año', 'mes', 'hombres', 'mujeres', 'total'],
                    'campo_anio': 'año', 'anio': 2022, 'grano_origen': 'municipio_mes'}
        source = {'id': 'prueba', 'conjunto_id': 'd', 'nombre': 'Nacimientos 2022'}
        responses = [{'ok': True, 'url': 'https://example.org/api', 'result': {'total': len(rows), 'records': rows}},
                     {'ok': True, 'result': {'total': len(rows)}}]
        with tempfile.TemporaryDirectory() as folder, patch('validar_lote_cruces.OUT', Path(folder)), patch('validar_lote_cruces.api', side_effect=responses):
            return agregar_validado(source, strategy)

    def rows(self):
        return [{'_id': m, 'municipio': 1, 'año': 2022, 'mes': m, 'hombres': 1, 'mujeres': 1, 'total': 2} for m in range(1, 13)]

    def test_nacimientos_suma_medida_y_no_filas(self):
        result = self.run_births(self.rows())
        self.assertTrue(result['ok'])
        self.assertEqual((result['total_filas'], result['valor_total']), (12, 24))

    def test_totales_inconsistentes_no_producen_agregado(self):
        rows = self.rows()
        rows[0]['total'] = 3
        result = self.run_births(rows)
        self.assertFalse(result['ok'])
        self.assertIn('Total no coincide', result['error'])
        self.assertNotIn('agregados', result)

    def test_ausencia_de_mes_no_se_interpreta_como_cero(self):
        result = self.run_births(self.rows()[:-1])
        self.assertFalse(result['ok'])
        self.assertIn('Faltan meses', result['error'])

    def test_celdas_educativas_vacias_se_conservan(self):
        a = {'ok': True, 'periodo_declarado': '2020-2021', 'valores': [{'programa_clave_local': 'a', 'programa_declarado': 'A', 'sede_declarada': 'H', 'valor': None}]}
        b = {'ok': True, 'periodo_declarado': '2020-2021', 'valores': [{'programa_clave_local': 'a', 'programa_declarado': 'A', 'sede_declarada': 'H', 'valor': 0}]}
        row = unir_educacion(a, b)[0]
        self.assertIsNone(row['valor_a'])
        self.assertEqual(row['valor_b'], 0)
        self.assertTrue(row['presente_en_ambas'])

    def test_periodos_educativos_no_se_mezclan(self):
        with self.assertRaises(ValueError):
            unir_educacion({'ok': True, 'periodo_declarado': '2020-2021'}, {'ok': True, 'periodo_declarado': '2021-2022'})


if __name__ == '__main__':
    unittest.main()
