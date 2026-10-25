import json
from pathlib import Path
import sys
import unittest

from rdflib import Graph, Literal, Namespace, URIRef, XSD

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from integrar_cobertura import cargar_evidencia


@unittest.skipUnless((ROOT / 'ontologia/revision-cobertura.json').exists(), 'Cobertura aún no integrada')
class CoberturaIntegradaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        read = lambda path: json.loads(path.read_text(encoding='utf-8'))
        cls.rules = read(ROOT / 'ontologia/semantica.json')
        _, cls.accepted, folder, _ = cargar_evidencia(cls.rules)
        cls.previous = read(folder / 'base-cobertura.json')
        cls.current = read(ROOT / 'data/semantica/cobertura.json')
        cls.variables = {v['definicion_iri']: v for v in cls.current['variables']}
        cls.graph = Graph().parse(ROOT / 'data/semantica/interpretaciones.ttl', format='turtle')
        cls.mex = Namespace('https://example.org/mex-ontologi/vocab/')

    def test_conteos_y_particion_completa_sin_doble_conteo(self):
        from collections import Counter
        decisions = self.accepted['decisiones']
        self.assertEqual(len(decisions), 1308)
        self.assertEqual(len({d['definicion_iri'] for d in decisions}), 1308)
        self.assertEqual(len(self.variables), 1563)
        expected = dict(self.accepted['resumen']['estados_variables_esperados'])
        if (ROOT / 'ontologia/revision-ronda-4.json').exists():
            from integrar_ronda_4 import validar
            _, _, _, r4, _ = validar(self.rules)
            old = {v['definicion_iri']: v for v in self.variables.values()}
            base = json.loads((ROOT / 'data/integracion-ronda-4/base-cobertura.json').read_text(encoding='utf-8'))
            before = {v['definicion_iri']: v for v in base['variables']}
            for rule in r4['reglas']:
                state = before[rule['definiciones'][0]]['estado']
                expected[state] -= 1
                expected['respaldada_por_definicion'] += 1
            expected = {k:v for k,v in expected.items() if v}
        self.assertEqual(dict(Counter(v['estado'] for v in self.variables.values())), expected)

    def test_significados_y_vinculos_anteriores_preservados(self):
        for row in self.previous['variables']:
            if row['estado'] == 'fuera_del_nucleo_actual':
                continue
            current = self.variables[row['definicion_iri']]
            for key in ('estado', 'concepto', 'regla', 'representacion'):
                self.assertEqual(row.get(key), current.get(key))
        old = [v for v in self.previous['correspondencias'] if v['estado'] == 'documental_revisada']
        new = [v for v in self.current['correspondencias'] if v['estado'] == 'documental_revisada']
        self.assertEqual(len(old), 836)
        for row in old:
            self.assertIn(row, new)

    def test_calificadores_literales_y_procedencia_de_auditoria_llegan_a_rdf(self):
        prov = Namespace('http://www.w3.org/ns/prov#')
        for rule in self.accepted['reglas']:
            variable = self.variables[rule['definiciones'][0]]
            self.assertEqual(variable['regla'], rule['id'])
            subject = URIRef(variable['iri'])
            sources = list(self.graph.objects(subject, prov.wasDerivedFrom))
            self.assertTrue(any('integracion-cobertura/auditorias/' in str(s) for s in sources))
            actual = {}
            for q in self.graph.objects(subject, self.mex.tieneCalificadorDocumentado):
                dimension = self.graph.value(q, self.mex.dimensionCalificador)
                value = self.graph.value(q, self.mex.valorCalificador)
                self.assertEqual(value.datatype, XSD.string)
                actual[str(dimension)] = str(value)
            self.assertEqual(actual, rule.get('calificador', {}))

    def test_condicionados_y_pendientes_no_se_promueven(self):
        promoted = set()
        if (ROOT / 'ontologia/revision-ronda-4.json').exists():
            from integrar_ronda_4 import validar
            _, _, _, r4, _ = validar(self.rules)
            promoted = {d for r in r4['reglas'] for d in r['definiciones']}
        for decision in self.accepted['decisiones']:
            variable = self.variables[decision['definicion_iri']]
            if decision['estado_integracion'] == 'pendiente':
                if decision['definicion_iri'] in promoted:
                    self.assertEqual(variable['estado'], 'respaldada_por_definicion')
                else:
                    self.assertEqual(variable['estado'], 'fuera_del_nucleo_actual')
            else:
                self.assertEqual(decision['dictamen_auditoria'], 'aceptar')
                self.assertEqual(variable['estado'], 'respaldada_por_definicion')


if __name__ == '__main__':
    unittest.main()
