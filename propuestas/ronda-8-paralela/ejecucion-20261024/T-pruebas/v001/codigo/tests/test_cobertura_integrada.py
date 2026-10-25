import json
from pathlib import Path
import sys
import unittest

from rdflib import Graph, Literal, Namespace, URIRef, XSD

# Corrección R7 (staging): localizar la raíz por marcador en vez de
# parents[1], porque esta copia vive en v001/codigo/tests/.
def _root():
    for p in Path(__file__).resolve().parents:
        if (p / 'ontologia/semantica.json').exists():
            return p
    raise RuntimeError('Raíz del proyecto no localizada')

ROOT = _root()
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
        promoted_ids = set()
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
                promoted_ids.update(rule['definiciones'])
            expected = {k:v for k,v in expected.items() if v}
        if (ROOT / 'ontologia/revision-ronda-5.json').exists():
            from integrar_ronda_5 import cargar
            _, folder, _, r5, _ = cargar()
            before = {v['definicion_iri']: v for v in json.loads((folder / 'base-cobertura.json').read_text(encoding='utf-8'))['variables']}
            for rule in r5['reglas']:
                state = before[rule['definiciones'][0]]['estado']
                expected[state] -= 1
                expected['respaldada_por_definicion'] += 1
                promoted_ids.update(rule['definiciones'])
            expected = {k:v for k,v in expected.items() if v}
        if (ROOT / 'ontologia/revision-ronda-6.json').exists():
            # R6 no admite reglas nuevas (su propia guardia lo impone);
            # se verifica en vez de suponerse. Sin delta de variables.
            from integrar_ronda_6 import cargar as cargar_r6
            _, _, _, r6, _ = cargar_r6()
            self.assertEqual(list(r6.get('reglas', [])), [])
        if (ROOT / 'ontologia/revision-ronda-7.json').exists():
            # Delta R7 derivado del manifiesto fijado, sin hardcodear
            # conteos observados: cada regla mueve su estado previo a
            # respaldada. Estado previo = base post-R4 salvo promoción
            # R4/R5 ya contabilizada (red neutra en ese caso).
            from integrar_ronda_5 import cargar as cargar_r5
            from integrar_ronda_7 import cargar as cargar_r7
            _, folder5, _, _, _ = cargar_r5()
            base5 = {v['definicion_iri']: v['estado'] for v in
                     json.loads((folder5 / 'base-cobertura.json').read_text(encoding='utf-8'))['variables']}
            _, _, _, r7, _ = cargar_r7()
            for rule in r7['reglas']:
                d = rule['definiciones'][0]
                state = 'respaldada_por_definicion' if d in promoted_ids else base5[d]
                expected[state] -= 1
                expected['respaldada_por_definicion'] += 1
            expected = {k:v for k,v in expected.items() if v}
        # R8 (28 vínculos previstos): los vínculos no mueven estados de
        # variables; si R8 aportara reglas se extiende este patrón con su
        # manifiesto (ver test_ronda_7.test_r8_hook_documentado).
        self.assertEqual(dict(Counter(v['estado'] for v in self.variables.values())), expected)

    def test_significados_y_vinculos_anteriores_preservados(self):
        promoted = {}
        if (ROOT / 'ontologia/revision-ronda-4.json').exists():
            from integrar_ronda_4 import validar
            _, _, _, r4, _ = validar(self.rules)
            promoted = {d: rule for rule in r4['reglas'] for d in rule['definiciones']}
        r4_ids = set(promoted)
        if (ROOT / 'ontologia/revision-ronda-5.json').exists():
            from integrar_ronda_5 import cargar
            _, _, _, r5, _ = cargar()
            promoted.update({d: rule for rule in r5['reglas'] for d in rule['definiciones']})
        if (ROOT / 'ontologia/revision-ronda-6.json').exists():
            from integrar_ronda_6 import cargar as cargar_r6
            _, _, _, r6, _ = cargar_r6()
            self.assertEqual(list(r6.get('reglas', [])), [])
        if (ROOT / 'ontologia/revision-ronda-7.json').exists():
            from integrar_ronda_7 import cargar as cargar_r7
            _, _, _, r7, _ = cargar_r7()
            promoted.update({d: rule for rule in r7['reglas'] for d in rule['definiciones']})
        for row in self.previous['variables']:
            if row['definicion_iri'] in r4_ids:
                # Ruta histórica R4 intacta (incluye su salto de fuera).
                if row['estado'] == 'fuera_del_nucleo_actual':
                    continue
                current = self.variables[row['definicion_iri']]
                self.assertEqual(row['estado'], 'candidata_sin_definicion_suficiente')
                self.assertEqual(current['estado'], 'respaldada_por_definicion')
                self.assertEqual(current['regla'], promoted[row['definicion_iri']]['id'])
                continue
            if row['definicion_iri'] in promoted:
                # Promoción R5/R7 derivada de manifiesto: el estado previo
                # es el de la base (fuera o candidata) y el actual queda
                # respaldado con regla y huella del lote aprobado.
                current = self.variables[row['definicion_iri']]
                self.assertIn(row['estado'], ('fuera_del_nucleo_actual', 'candidata_sin_definicion_suficiente'))
                self.assertEqual(current['estado'], 'respaldada_por_definicion')
                self.assertEqual(current['regla'], promoted[row['definicion_iri']]['id'])
                self.assertEqual(current['huella_fila_diccionario'],
                                 promoted[row['definicion_iri']]['huella_fila_diccionario'])
                continue
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
        promoted = {}
        if (ROOT / 'ontologia/revision-ronda-4.json').exists():
            from integrar_ronda_4 import validar
            _, _, _, r4, _ = validar(self.rules)
            promoted = {d: r for r in r4['reglas'] for d in r['definiciones']}
        if (ROOT / 'ontologia/revision-ronda-5.json').exists():
            from integrar_ronda_5 import cargar
            _, _, _, r5, _ = cargar()
            promoted.update({d: r for r in r5['reglas'] for d in r['definiciones']})
        if (ROOT / 'ontologia/revision-ronda-6.json').exists():
            # R6 sin reglas: nada que promover en variables.
            from integrar_ronda_6 import cargar as cargar_r6
            _, _, _, r6, _ = cargar_r6()
            self.assertEqual(list(r6.get('reglas', [])), [])
        if (ROOT / 'ontologia/revision-ronda-7.json').exists():
            # Promociones R7 (lote SINAC auditado A+B) derivadas del
            # manifiesto; sin hardcodear sus conteos.
            from integrar_ronda_7 import cargar as cargar_r7
            _, _, _, r7, _ = cargar_r7()
            promoted.update({d: r for r in r7['reglas'] for d in r['definiciones']})
        for decision in self.accepted['decisiones']:
            variable = self.variables[decision['definicion_iri']]
            if decision['estado_integracion'] == 'pendiente':
                if decision['definicion_iri'] in promoted:
                    self.assertEqual(variable['estado'], 'respaldada_por_definicion')
                    approved = promoted[decision['definicion_iri']]
                    self.assertEqual(variable['regla'], approved['id'])
                    self.assertEqual(variable['huella_fila_diccionario'], approved['huella_fila_diccionario'])
                else:
                    self.assertEqual(variable['estado'], 'fuera_del_nucleo_actual')
            else:
                self.assertEqual(decision['dictamen_auditoria'], 'aceptar')
                self.assertEqual(variable['estado'], 'respaldada_por_definicion')


if __name__ == '__main__':
    unittest.main()
