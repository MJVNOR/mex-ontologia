import copy
import json
from pathlib import Path
import sys
import unittest

from rdflib import Namespace, URIRef, Literal, RDF, OWL, SKOS

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists()) / 'scripts'))
from consolidar_semantica import construir, interpretacion, columnas, huella


class SemanticaTest(unittest.TestCase):
    def setUp(self):
        self.rules = json.loads((next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists()) / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        self.rules['vinculos_documentales_revisados'] = []
        self.rules['observaciones_revision'] = []
        self.base = 'https://example.org/test/'
        self.mex = Namespace(self.base + 'vocab/')
        self.inventory = {'recursos': [
            {'id': 'dic', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'clasificacion': 'diccionario'},
            {'id': 'r', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'clasificacion': 'datos_estructurados',
             'datastore': {'ok': True, 'url': 'https://example.org/api', 'campos': [{'id': 'municipio'}, {'id': 'CLUES'}]}}]}
        self.inspection = {'recursos': [
            {'id': 'dic', 'ok': True, 'definiciones': [{'Nombre variable': 'municipio', 'Descripción': 'Municipio de registro'},
                                                     {'Nombre variable': 'CLUES', 'Descripción': 'Pendiente de especificar'}]},
            {'id': 'r', 'ok': True}]}

    def build(self):
        return construir(self.inventory, self.inspection, self.rules, None, self.base)

    def test_anio_del_nombre_no_suplanta_el_evento_documentado(self):
        a = interpretacion('año_matrimonio', 'Año de registro', 'd', self.rules)
        b = interpretacion('año_defuncion', 'Año en el que fallecio', 'd', self.rules)
        self.assertEqual(a['concepto'], 'anio-registro')
        self.assertEqual(b['concepto'], 'anio-defuncion')
        self.assertNotEqual(a['concepto'], b['concepto'])

    def test_anio_y_mes_genericos_no_se_promueven_a_registro(self):
        self.assertEqual(interpretacion('Year', 'Año', 'd', self.rules)['concepto'], 'anio')
        self.assertEqual(interpretacion('Mes', 'Mes', 'd', self.rules)['concepto'], 'mes')
        self.assertEqual(interpretacion('Año', 'Año de captura', 'd', self.rules)['concepto'], 'anio-captura')

    def test_eventos_y_poblaciones_se_conservan(self):
        self.assertEqual(interpretacion('fecha_hechos', 'Fecha del reporte de la víctima', 'd', self.rules)['concepto'], 'fecha-reporte-victima')
        self.assertNotEqual(interpretacion('x', 'Nombre del localidad donde recide la madre', 'd', self.rules)['concepto'],
                            interpretacion('x', 'Nombre de la localidad donde fue el parto', 'd', self.rules)['concepto'])

    def test_egresos_no_se_interpretan_como_urgencias_por_nombre(self):
        self.assertEqual(interpretacion('Total_Egresos', 'Total de urgencias atendidas', 'd', self.rules)['estado'], 'fuera_del_nucleo_actual')
        self.assertNotEqual(interpretacion('Municipio', 'Municipio donde el alumno', 'd', self.rules)['estado'], 'respaldada_por_definicion')

    def pinned_revision(self):
        col = next(c for c in columnas(self.inventory, self.inspection, self.base) if c['campo'] == 'municipio')
        row = self.inspection['recursos'][0]['definiciones'][0]
        return {'recurso': 'r', 'campo': 'municipio', 'columna': col['iri'], 'diccionario': 'dic', 'concepto': 'municipio-registro',
                'huella_esquema': col['huella_esquema'], 'huella_fila_diccionario': huella(row), 'descripcion': row['Descripción']}

    def test_revision_caduca_al_cambiar_otro_campo_del_esquema(self):
        self.rules['vinculos_documentales_revisados'] = [self.pinned_revision()]
        self.inventory['recursos'][1]['datastore']['campos'].append({'id': 'nuevo'})
        with self.assertRaisesRegex(ValueError, 'huella_esquema'):
            self.build()

    def test_revision_caduca_al_cambiar_formato_del_diccionario(self):
        self.rules['vinculos_documentales_revisados'] = [self.pinned_revision()]
        self.inspection['recursos'][0]['definiciones'][0]['Formato'] = 'Cambio de formato'
        with self.assertRaisesRegex(ValueError, 'huella_fila_diccionario'):
            self.build()

    def test_alias_revisado_solo_se_aplica_a_la_columna_fisica(self):
        revision = self.pinned_revision()
        self.inventory['recursos'][1]['datastore']['campos'][0]['id'] = 'municipio_alias'
        col = next(c for c in columnas(self.inventory, self.inspection, self.base) if c['campo'] == 'municipio_alias')
        revision.update(campo='municipio_alias', columna=col['iri'], variable='municipio', huella_esquema=col['huella_esquema'])
        self.rules['vinculos_documentales_revisados'] = [revision]
        self.inventory['recursos'].append({'id': 'otro', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'clasificacion': 'datos_estructurados',
            'datastore': {'ok': True, 'url': 'https://example.org/otro', 'campos': [{'id': 'municipio_alias'}]}})
        self.inspection['recursos'].append({'id': 'otro', 'ok': True})
        data, _, report = self.build()
        self.assertEqual(sum(m['estado'] == 'documental_revisada' for m in report['correspondencias']), 1)
        self.assertTrue(list(data.objects(URIRef(col['iri']), self.mex.significadoDocumentado)))
        self.assertFalse(list(data.objects(URIRef(self.base + 'column/otro/municipio_alias'), self.mex.significadoDocumentado)))

    def test_alias_sin_columna_fisica_es_rechazado(self):
        revision = self.pinned_revision()
        revision.update(campo='municipio_alias', variable='municipio')
        del revision['columna']
        self.inventory['recursos'][1]['datastore']['campos'][0]['id'] = 'municipio_alias'
        self.rules['vinculos_documentales_revisados'] = [revision]
        with self.assertRaisesRegex(ValueError, 'IRI de la columna'):
            self.build()

    def test_observacion_conserva_literal_y_no_confirma_significado(self):
        row = self.inspection['recursos'][0]['definiciones'][1]
        self.rules['observaciones_revision'] = [{'id': 'pendiente', 'recurso': 'r', 'campo': 'CLUES', 'diccionario': 'dic',
            'variable': 'CLUES', 'huella_fila_diccionario': huella(row), 'observacion': 'La fuente debe precisar esta definición.'}]
        data, _, report = self.build()
        var = next(data.subjects(self.mex.nombreVariableLocal, Literal('CLUES')))
        self.assertTrue(list(data.objects(var, self.mex.limiteSemantico)))
        self.assertFalse(list(data.objects(var, self.mex.significadoDocumentado)))
        self.assertEqual(next(v for v in report['variables'] if v['variable'] == 'CLUES')['descripcion'], 'Pendiente de especificar')

    def test_observacion_se_detiene_si_su_evidencia_cambia(self):
        self.rules['observaciones_revision'] = [{'id': 'pendiente', 'recurso': 'r', 'campo': 'CLUES', 'diccionario': 'dic',
            'variable': 'CLUES', 'huella_fila_diccionario': '0' * 64, 'observacion': 'Revisar'}]
        with self.assertRaisesRegex(ValueError, 'Evidencia de observación cambió'):
            self.build()

    def test_madre_no_se_confunde_con_recien_nacido(self):
        x = interpretacion('MUNICIPIONACIMIENTO', 'Clave del municipio donde nacio la madre', 'd', self.rules)
        self.assertEqual(x['concepto'], 'municipio-nacimiento-madre')

    def test_clues_pendiente_no_confirma_significado_o_catalogo(self):
        data, _, _ = self.build()
        variables = set(data.subjects(self.mex.nombreVariableLocal, Literal('CLUES')))
        self.assertEqual(len(variables), 1)
        var = next(iter(variables))
        self.assertFalse(list(data.objects(var, self.mex.significadoDocumentado)))
        self.assertTrue(list(data.objects(var, self.mex.significadoCandidato)))
        self.assertFalse(list(data.triples((None, self.mex.usaSistemaIdentificadores, None))))

    def test_clave_unidad_generica_exige_contexto_salud(self):
        x = interpretacion('CLUES', 'Clave de la Unidad', 'd', self.rules)
        self.assertEqual(x['estado'], 'candidata_sin_definicion_suficiente')
        y = interpretacion('CLUES', 'Clave de la Unidad', '318b9551-47a1-4e6b-a194-232ea5a08d43', self.rules)
        self.assertEqual(y['estado'], 'respaldada_por_definicion')

    def test_nombre_coincidente_no_confirma_columna(self):
        data, _, report = self.build()
        col = URIRef(self.base + 'column/r/municipio')
        self.assertFalse(list(data.objects(col, self.mex.significadoDocumentado)))
        self.assertTrue(any(m['estado'] == 'candidata_por_nombre' for m in report['correspondencias']))
        self.assertFalse(list(data.triples((None, OWL.sameAs, None))))
        self.assertFalse(list(data.triples((None, SKOS.exactMatch, None))))

    def test_revision_explicita_habilita_solo_la_columna_revisada(self):
        self.rules['vinculos_documentales_revisados'] = [{'recurso': 'r', 'campo': 'municipio', 'diccionario': 'dic', 'concepto': 'municipio-registro'}]
        data, _, _ = self.build()
        self.assertEqual(list(data.objects(URIRef(self.base + 'column/r/municipio'), self.mex.significadoDocumentado)), [URIRef(self.base + 'concept/municipio-registro')])
        self.assertFalse(list(data.objects(URIRef(self.base + 'column/r/CLUES'), self.mex.significadoDocumentado)))

    def test_revision_se_detiene_si_cambia_la_definicion(self):
        self.rules['vinculos_documentales_revisados'] = [{'recurso': 'r', 'campo': 'municipio', 'diccionario': 'dic', 'concepto': 'municipio-registro'}]
        self.inspection['recursos'][0]['definiciones'][0]['Descripción'] = 'Nombre del municipio'
        with self.assertRaisesRegex(ValueError, 'dejó de coincidir'):
            self.build()

    def test_otra_definicion_fuera_del_nucleo_sigue_creando_ambiguedad(self):
        self.inspection['recursos'][0]['definiciones'].append({'Nombre variable': 'municipio', 'Descripción': 'Indicador sin descripción útil'})
        _, _, report = self.build()
        links = [r for r in report['correspondencias'] if r['campo'] == 'municipio']
        self.assertTrue(links)
        self.assertTrue(all(r['estado'] == 'ambigua_por_nombre' for r in links))

    def test_catalogo_solo_declarado_no_se_resuelve_por_nombre(self):
        self.inspection['recursos'][0]['definiciones'][0]['Catálogo de referencia'] = 'Municipios'
        data, _, _ = self.build()
        refs = list(data.subjects(RDF.type, self.mex.ReferenciaCatalogoDeclarada))
        self.assertEqual(len(refs), 1)
        self.assertIn(Literal('solo_referencia_declarada_sin_resolver'), data.objects(refs[0], self.mex.estadoReferenciaCatalogo))
        self.assertFalse(list(data.subjects(RDF.type, self.mex.SistemaIdentificadores)))

    def test_reglas_contradictorias_no_eligen_una_en_silencio(self):
        self.rules['reglas_descripcion_exacta'].append({'id': 'conflicto', 'concepto': 'anio', 'descripciones': ['Municipio de registro'], 'representacion': 'anio'})
        with self.assertRaisesRegex(ValueError, 'conflicto'):
            self.build()

    def test_codigo_geografico_solo_se_asocia_a_su_recurso_original(self):
        self.inventory['recursos'].append({'id': 'geo', 'conjunto_id': 'g', 'conjunto': 'Geometrías', 'clasificacion': 'candidato_geoespacial', 'url': 'https://example.org/map'})
        self.inspection['recursos'].append({'id': 'geo', 'ok': True, 'fuente': 'https://example.org/map', 'tablas': [
            {'hoja': 'GeoJSON:properties', 'campos': [{'id': 'CVEGEO', 'posicion_original': 1}]}]})
        ref = {'ok': True, 'recurso_id': 'geo', 'fuente': 'https://example.org/map', 'municipios': [
            {'cvegeo': '26' + str(i).zfill(3), 'cve_ent': '26', 'cve_mun': str(i).zfill(3), 'nombre': 'Municipio ' + str(i)} for i in range(1, 73)]}
        data, _, _ = construir(self.inventory, self.inspection, self.rules, ref, self.base)
        subjects = set(data.subjects(self.mex.usaSistemaIdentificadores, None))
        self.assertEqual(subjects, {URIRef(self.base + 'file-column/geo%2FGeoJSON%3Aproperties%2F1')})
        self.assertEqual(len(set(data.subjects(RDF.type, self.mex.EntradaCatalogo))), 72)
        self.assertIn(Literal('26001'), set(data.objects(None, SKOS.notation)))


if __name__ == '__main__':
    unittest.main()
