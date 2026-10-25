import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import zipfile

from rdflib import Graph, Literal, Namespace, RDF, OWL, SKOS

ROOT = Path(__file__).resolve().parents[5]  # copia en auditoria-b: mismo repo real, sin tocar central
sys.path.insert(0, str(ROOT / 'scripts'))
from integrar_ronda_2 import cargar_evidencia, validar_codigo


class Ronda2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / 'ontologia/revision-ronda-2.json').read_text(encoding='utf-8'))
        cls.rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        cls.graph = Graph().parse(ROOT / 'data/integracion-ronda-2/ronda-2.ttl', format='turtle')
        cls.mex = Namespace('https://example.org/mex-ontologi/vocab/')

    def test_162_revisiones_anteriores_se_conservan_exactamente(self):
        with zipfile.ZipFile(ROOT / self.config['respaldo']) as z:
            previous = json.loads(z.read('ontologia/semantica.json'))
        self.assertEqual(len(previous['vinculos_documentales_revisados']), 162)
        self.assertEqual(self.config['esperado']['revisadas'], 836)
        expected = self.config.get('esperado_actual', self.config['esperado'])
        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), expected['revisadas'])
        for revision in previous['vinculos_documentales_revisados']:
            self.assertIn(revision, self.rules['vinculos_documentales_revisados'])

    def test_enie_no_se_promueve_como_acento(self):
        from integrar_contenido import clave
        from consolidar_semantica import huella
        # 1. El normalizador SI confunde eñe: 'Año' y 'ano' colisionan; prohibido aprobar por nombre.
        self.assertNotEqual('Año', 'ano')
        self.assertEqual(clave('Año'), clave('ano'))
        # 2. El pendiente historico de ronda 2 sigue registrado como tal (historia intacta).
        p = json.loads((ROOT / 'data/integracion-ronda-2/entregas/agente-1-correspondencias/propuestas.json').read_text(encoding='utf-8'))
        candidates = [x for x in p['pendientes_clasificados'] if x.get('etapa') == 'vinculo']
        self.assertEqual(len(candidates), 1)
        target = candidates[0]['columna']
        self.assertEqual(target, 'https://example.org/mex-ontologi/file-column/e52ec9d3-2242-4928-b2a3-06b95800c229%2FHoja1%2F1')
        # 3. Solo vale el recibo R4 explicito: un unico vinculo con evidencia exacta vigente.
        receipts = [r for r in self.rules['vinculos_documentales_revisados'] if r['columna'] == target]
        self.assertEqual(len(receipts), 1)
        r = receipts[0]
        self.assertEqual((r['campo'], r['diccionario'], r['concepto'], r['descripcion']),
                         ('Año', 'a95d2d39-12df-4836-9792-1ce52e05db3c', 'anio-registro', 'Año del registro'))
        # 4. Hashes recomputados desde fuentes, no copiados a ciegas.
        inspection = json.loads((ROOT / 'data/portal/contenido-inspeccion.json').read_text(encoding='utf-8'))
        tables = [t for res in inspection['recursos'] if res['id'] == r['recurso'] for t in res.get('tablas', [])]
        self.assertEqual(len(tables), 1)
        self.assertEqual(r['huella_esquema'], huella(tables[0]))
        raw = json.loads((ROOT / 'data/portal/inspecciones/a95d2d39-12df-4836-9792-1ce52e05db3c.json').read_text(encoding='utf-8'))
        self.assertEqual(r['huella_fila_diccionario'], huella(raw['definiciones'][0]))
        # 5. Revision explicita con criterio (no mera existencia en la lista).
        self.assertTrue(r.get('criterio'))
        # 6. Recibo firmado R4: el mismo vinculo esta en aceptadas.json fijadas.
        accepted = json.loads((ROOT / 'data/integracion-ronda-4/aceptadas.json').read_text(encoding='utf-8'))
        fixed = [e for e in accepted['vinculos'] if e['columna'] == target]
        self.assertEqual(len(fixed), 1)
        self.assertEqual(fixed[0], r)

    def test_codigo_rechaza_conversiones_implicitas(self):
        self.assertEqual(validar_codigo('260010001', 9), '260010001')
        for code in ['26001001', '２６００１０００１', '26001ABCD', 260010001, '260010001.0']:
            with self.assertRaises(ValueError):
                validar_codigo(code, 9)

    def test_fuente_modificada_impide_generar(self):
        with patch('integrar_ronda_2.sha', return_value='0' * 64):
            with self.assertRaisesRegex(ValueError, 'Manifiesto'):
                cargar_evidencia()

    def test_localidades_son_comprobaciones_sin_identidad_oficial(self):
        g, m = self.graph, self.mex
        checks = set(g.subjects(RDF.type, m.ComprobacionLocalidadCensal))
        self.assertEqual(len(checks), 1850)
        self.assertEqual(len(set(g.objects(None, m.claveCensalOriginal))), 1850)
        self.assertFalse(list(g.triples((None, OWL.sameAs, None))))
        self.assertFalse(list(g.triples((None, SKOS.exactMatch, None))))
        self.assertFalse(list(g.triples((None, m.usaSistemaIdentificadores, None))))

    def test_evaluacion_no_certifica_ui_ni_inventa_respuestas(self):
        g, m = self.graph, self.mex
        cases = set(g.subjects(RDF.type, m.ResultadoCasoEvaluacion))
        self.assertEqual(len(cases), 20)
        no_response = set(g.subjects(m.estadoCasoEvaluacion, Literal('no_ejecutado_cuota_modelo')))
        self.assertEqual(len(no_response), 16)
        self.assertTrue(all(not list(g.objects(c, m.respuestaObtenida)) for c in no_response))
        evaluation = next(g.subjects(RDF.type, m.EvaluacionPipelineConsulta))
        self.assertEqual(g.value(evaluation, m.estadoEvaluacionUI), Literal('no_ejecutada'))
        self.assertEqual(g.value(evaluation, m.respuestasModelo), Literal(4))

    def test_dictamenes_no_promueven_significados_y_vigencia_sigue_pendiente(self):
        g, m = self.graph, self.mex
        self.assertEqual(len(set(g.subjects(RDF.type, m.DictamenPendienteSemantico))), 32)
        self.assertEqual(len(set(g.subjects(m.estadoVigenciaRevisada, Literal('no_acreditada')))), 16)
        self.assertFalse(list(g.triples((None, m.significadoDocumentado, None))))


if __name__ == '__main__':
    unittest.main()
