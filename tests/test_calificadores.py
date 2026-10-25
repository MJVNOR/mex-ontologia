import copy
from pathlib import Path
import sys
import unittest

from rdflib import Literal, Namespace, RDF, XSD

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from consolidar_semantica import construir, interpretacion


class CalificadoresTest(unittest.TestCase):
    def setUp(self):
        self.base = 'https://example.org/test/'
        self.mex = Namespace(self.base + 'vocab/')
        self.rules = {'alcance': 'Prueba de distritos distintos',
                      'conceptos': {'superficie': ['Superficie', 'Superficie por distrito', None]},
                      'condiciones': {'contexto': 'Conservar distrito'}, 'distinciones': [],
                      'reglas_descripcion_exacta': [], 'vinculos_documentales_revisados': [],
                      'observaciones_revision': []}
        for name in ('municipio-registro', 'municipio-residencia', 'municipio-defuncion',
                     'anio-registro', 'anio-defuncion', 'organizacion-publicadora', 'organizacion-capturadora'):
            self.rules['conceptos'][name] = [name, 'Concepto de prueba: ' + name, None]
        self.inventory = {'recursos': [{'id': 'dic', 'conjunto_id': 'd', 'conjunto': 'Trigo', 'clasificacion': 'diccionario'}]}
        self.inspection = {'recursos': [{'id': 'dic', 'ok': True, 'definiciones': []}]}
        for i, district in enumerate(['001', '002'], 1):
            name = 'SHD' + district
            desc = 'Superficie en distrito ' + district
            self.inspection['recursos'][0]['definiciones'].append({'Nombre variable': name, 'Descripción': desc})
            self.rules['reglas_descripcion_exacta'].append({
                'id': 'r' + district, 'concepto': 'superficie', 'representacion': 'no_especificada',
                'nombres': [name], 'descripciones': [desc], 'conjuntos': ['d'], 'diccionarios': ['dic'],
                'definiciones': [self.base + 'definition/dic%2F' + str(i)],
                'calificador': {'distrito': district}, 'limite': 'Sin identidad territorial acreditada'})

    def test_distritos_sobreviven_en_reporte_y_consulta_rdf(self):
        g, model, report = construir(self.inventory, self.inspection, self.rules, None, self.base)
        self.assertEqual([v['calificador']['distrito'] for v in report['variables']], ['001', '002'])
        query = '''SELECT ?nombre ?valor WHERE {
          ?v mex:nombreVariableLocal ?nombre; mex:tieneCalificadorDocumentado ?q.
          ?q mex:dimensionCalificador "distrito"^^xsd:string; mex:valorCalificador ?valor.
        } ORDER BY ?nombre'''
        rows = list(g.query(query, initNs={'mex': self.mex, 'xsd': XSD}))
        self.assertEqual([(str(a), str(b)) for a, b in rows], [('SHD001', '001'), ('SHD002', '002')])
        self.assertEqual(len(set(g.subjects(RDF.type, self.mex.CalificadorDocumental))), 2)
        self.assertEqual(len(list(g.triples((None, self.mex.limiteSemantico, None)))), 2)

    def test_regla_no_alcanza_otro_contexto_y_no_comparte_mutaciones(self):
        rule = self.rules['reglas_descripcion_exacta'][0]
        args = ['SHD001', rule['descripciones'][0], 'd', self.rules, 'dic', rule['definiciones'][0]]
        result = interpretacion(*args)
        result['calificador']['distrito'] = '999'
        self.assertEqual(interpretacion(*args)['calificador']['distrito'], '001')
        for pos in (0, 1, 2, 4, 5):
            changed = args.copy()
            changed[pos] = 'otro'
            self.assertNotEqual(interpretacion(*changed).get('regla'), rule['id'])

    def test_calificadores_invalidos_no_se_ignoran(self):
        for invalid in (None, {}, [], {'distrito': 1}, {'distrito': ''}, {' ': '001'}):
            rules = copy.deepcopy(self.rules)
            rule = rules['reglas_descripcion_exacta'][0]
            rule['calificador'] = invalid
            with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, 'alificador'):
                interpretacion('SHD001', rule['descripciones'][0], 'd', rules, 'dic', rule['definiciones'][0])


if __name__ == '__main__':
    unittest.main()
