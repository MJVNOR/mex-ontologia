from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from mapear_cruces import clasificar, evaluar, generar


def perfil(id_, fields, years=()):
    columns = []
    for name, description in fields:
        role = clasificar(name, description)
        if role:
            columns.append({'columna': 'urn:' + id_ + ':' + name, 'origen': 'DataStore', **role})
    return {'id': id_, 'titulo': id_, 'columnas_clave': columns, 'familias': sorted({c['familia'] for c in columns}),
            'anios_en_nombres': list(years), 'publicadores': ['urn:publicador']}


class OportunidadesTest(unittest.TestCase):
    def test_medidas_y_preguntas_no_son_identificadores(self):
        for name in ('POB_TOT', 'total_municipios', 'poblacion_municipio', 'municipios_atendidos', 'localidades_atendidas', 'P6'):
            self.assertIsNone(clasificar(name, 'Total de habitantes en el municipio o dependencia'))

    def test_residencia_y_registro_no_se_homologan(self):
        a = perfil('a', [('municipio', 'Municipio de registro')])
        b = perfil('b', [('MUNICIPIORESIDENCIA', 'Clave del municipio de residencia')])
        result = evaluar(a, b, frozenset())
        self.assertIn('sentidos_distintos_requieren_pregunta_y_agregacion_explicitas', result['pendientes'])
        self.assertEqual(result['estado'], 'candidata_por_validar')

    def test_codigo_y_nombre_requieren_catalogo(self):
        a, b = perfil('a', [('CVE_MUN', 'Clave de municipio')]), perfil('b', [('NOM_MUN', 'Nombre de municipio')])
        self.assertIn('requiere_correspondencia_codigo_nombre', evaluar(a, b, frozenset())['pendientes'])

    def test_compartir_anio_no_valida_un_join(self):
        a, b = perfil('a', [('año', 'Año')]), perfil('b', [('año', 'Año')])
        self.assertEqual(evaluar(a, b, frozenset())['estado'], 'solo_dimensiones_amplias_o_tiempo')

    def test_todos_los_pares_sin_autopares_ni_duplicados(self):
        ps = {i: perfil(i, [('municipio', 'Municipio de registro')]) for i in ('a', 'b', 'c', 'd')}
        pairs = generar(ps, {'fuentes': [{'conjunto_id': 'a'}, {'conjunto_id': 'b'}]})
        self.assertEqual(len(pairs), 6)
        self.assertEqual(len({p['id'] for p in pairs}), 6)
        self.assertTrue(all(p['conjunto_a'] != p['conjunto_b'] for p in pairs))
        self.assertEqual(sum(p['estado'] == 'exploratorio_ejecutado' for p in pairs), 1)
        self.assertTrue(all('Solo los dos recursos' in p['alcance_ejecucion'] for p in pairs if p['estado'] == 'exploratorio_ejecutado'))

    def test_ausencia_de_anios_no_afirma_solapamiento(self):
        a, b = perfil('a', [('municipio', '')]), perfil('b', [('municipio', '')])
        result = evaluar(a, b, frozenset())
        self.assertEqual(result['anios_coincidentes_solo_en_nombres'], [])
        self.assertIn('verificar_periodos_y_cobertura_real', result['pendientes'])

    def test_localidad_necesita_contexto(self):
        a, b = perfil('a', [('CVE_LOC', 'Clave de la localidad')]), perfil('b', [('LOC', 'Clave de localidad')])
        self.assertIn('localidad_puede_requerir_entidad_y_municipio_como_clave_compuesta', evaluar(a, b, frozenset())['pendientes'])

    def test_programa_educativo_no_equivale_sin_institucion(self):
        a, b = perfil('a', [('Programa Educativo', 'Nombre del programa educativo')]), perfil('b', [('Programa Educativo', 'Nombre del programa educativo')])
        self.assertIn('programa_requiere_institucion_plan_y_homologacion_de_nombres', evaluar(a, b, frozenset())['pendientes'])

    def test_clues_detectado_sin_inventar_vigencia(self):
        self.assertEqual(clasificar('CLUES', 'Clave de la unidad de salud')['familia'], 'unidad_salud_clues')
        a, b = perfil('a', [('CLUES', '')]), perfil('b', [('CLUES', '')])
        self.assertIn('comprobar_catalogo_clues_y_vigencia_de_unidades', evaluar(a, b, frozenset())['pendientes'])

    def test_estrato_sexo_no_identifica_registros(self):
        a, b = perfil('a', [('Sexo', '')]), perfil('b', [('Sexo', '')])
        self.assertEqual(evaluar(a, b, frozenset())['estado'], 'solo_dimensiones_amplias_o_tiempo')


if __name__ == '__main__':
    unittest.main()
