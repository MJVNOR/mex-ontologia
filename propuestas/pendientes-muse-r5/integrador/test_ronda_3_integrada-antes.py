"""Regresiones de las 29 correspondencias y su evidencia de cruces fijada."""
import copy
import json
import sys
import unittest
import zipfile
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from integrar_ronda_3 import cargar_evidencia, validar_extension_vinculos


@unittest.skipUnless((ROOT / 'ontologia/revision-ronda-3.json').exists(), 'Ronda 3 aún no integrada')
class Ronda3Integrada(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        read = lambda path: json.loads(path.read_text(encoding='utf-8'))
        cls.rules = read(ROOT / 'ontologia/semantica.json')
        cls.config, _, cls.folder, _, frozen = cargar_evidencia()
        cls.previous = frozen('vinculos-anteriores.json')
        cls.additions = frozen('correspondencias-29.json')['entradas']
        cls.report = read(ROOT / 'data/semantica/cobertura.json')
        cls.graph = Graph().parse(ROOT / 'data/semantica/interpretaciones.ttl', format='turtle')
        cls.mex = Namespace('https://example.org/mex-ontologi/vocab/')

    def test_extension_exacta_836_mas_29(self):
        self.assertEqual(validar_extension_vinculos(self.rules, self.previous), self.additions)
        expected = 865 + self.report.get('integracion_ronda_4', {}).get('correspondencias_nuevas', 0)
        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), expected)
        self.assertEqual(self.report['resumen']['estados_correspondencias']['documental_revisada'], expected)

    def test_rechaza_adicion_no_aprobada_y_cambio_previo(self):
        changed = copy.deepcopy(self.rules)
        changed['vinculos_documentales_revisados'].append(self.additions[0])
        with self.assertRaises(ValueError):
            validar_extension_vinculos(changed, self.previous)
        changed = copy.deepcopy(self.rules)
        changed['vinculos_documentales_revisados'][0]['concepto'] = 'alterado'
        with self.assertRaises(ValueError):
            validar_extension_vinculos(changed, self.previous)

    def test_nucleo_semantico_del_relevo_intacto(self):
        with zipfile.ZipFile(ROOT / self.config['respaldo']) as archive:
            before = json.loads(archive.read('ontologia/semantica.json'))
        if (ROOT / 'ontologia/revision-ronda-4.json').exists():
            from integrar_ronda_4 import validar
            _, _, r4_before, _, _ = validar(self.rules)
            after = copy.deepcopy(r4_before)
        else:
            after = copy.deepcopy(self.rules)
        before.pop('vinculos_documentales_revisados')
        after.pop('vinculos_documentales_revisados')
        self.assertEqual(before, after)

    def test_adiciones_con_evidencia_fijada_en_rdf(self):
        prov = Namespace('http://www.w3.org/ns/prov#')
        origin = URIRef((self.folder / 'entregas/agente-2-correspondencias/propuestas.json').as_uri())
        rows = {r['columna']: r for r in self.report['correspondencias'] if r['estado'] == 'documental_revisada'}
        for entry in self.additions:
            row = rows[entry['columna']]
            self.assertEqual(row['revision'], entry)
            self.assertIn((URIRef(row['iri']), prov.wasDerivedFrom, origin), self.graph)

    def test_tres_fichas_y_72_comparaciones_con_144_fuentes(self):
        self.assertEqual(len(set(self.graph.subjects(RDF.type, self.mex.RevisionCruceRonda3))), 3)
        self.assertEqual(len(set(self.graph.subjects(RDF.type, self.mex.ComparacionMunicipal2020))), 72)
        self.assertEqual(len(set(self.graph.subjects(RDF.type, self.mex.EvidenciaFuenteComparacion))), 144)
        query = (ROOT / 'queries/portal/cruces_ronda_3.rq').read_text(encoding='utf-8')
        rows = list(self.graph.query(query))
        self.assertEqual(len(rows), 72)
        for row in rows:
            self.assertEqual(row.val_gg, row.val_ind)
            self.assertNotEqual(row.med_gg, row.med_ind)
            self.assertNotEqual(row.sha_gg, row.sha_ind)

    def test_periodo_y_fuentes_separados_sin_identidad_de_medidas(self):
        for comp in self.graph.subjects(RDF.type, self.mex.ComparacionMunicipal2020):
            self.assertEqual(list(self.graph.objects(comp, self.mex.periodoCruzado)), [Literal('2020')])
            evidences = list(self.graph.subjects(self.mex.evidenciaDeFuente, comp))
            self.assertEqual(len(evidences), 2)
            self.assertEqual({str(self.graph.value(e, self.mex.fuenteRol)) for e in evidences}, {'grandes_grupos', 'indicadores'})
            for evidence in evidences:
                self.assertEqual(len(list(self.graph.objects(evidence, self.mex.fuenteOriginal))), 1)
                self.assertEqual(len(list(self.graph.objects(evidence, self.mex.shaFuente))), 1)
            self.assertFalse(list(self.graph.objects(comp, self.mex.mismaMedida)))

    def test_historia_y_triaje_no_se_promueven_a_cobertura_total(self):
        summary = self.report['integracion_ronda_3']
        self.assertTrue(summary['cruces']['no_habilita_cruces'])
        self.assertEqual(sum(summary['cruces']['triaje_informativo'].values()), 3916)
        types = {str(value) for value in self.graph.objects(None, self.mex.tipoEvidencia)}
        self.assertTrue({'recomputo_agregados_fuente_historico', 'validacion_original_2020', 'union_listas_fuente_historico'} <= types)


if __name__ == '__main__':
    unittest.main()
