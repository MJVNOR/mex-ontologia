"""Cobertura específica R7 (staging): lote SINAC auditado A+B.

Deriva todo de manifiestos fijados (aceptadas.json, delta.json,
auditorías, reports/ronda-7.json); no hardcodea conteos observados ni
compara el vivo consigo mismo. Solo lectura de producción (más tmp
efímeros en negativas sintéticas): no instala nada.
"""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'ontologia/semantica.json').exists())
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
import integrar_ronda_7 as R7


def _read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


@unittest.skipUnless((ROOT / 'ontologia/revision-ronda-7.json').exists(), 'Ronda 7 aún no integrada')
class Ronda7Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config, cls.folder, cls.baseline, cls.accepted, _ = R7.cargar()
        cls.rules = _read('ontologia/semantica.json')
        cls.report = _read('data/semantica/cobertura.json')
        cls.delta = _read('data/integracion-ronda-7/delta.json')
        cls.r7report = _read('reports/ronda-7.json')
        cls.variables = {v['definicion_iri']: v for v in cls.report['variables']}
        cls.mappings = {v['columna']: v for v in cls.report['correspondencias']
                        if v['estado'] == 'documental_revisada'}

    # --- integridad ---
    def test_manifiesto_coincide_y_evidencia_intacta(self):
        mp = self.folder / 'manifiesto.json'
        self.assertEqual(hashlib.sha256(mp.read_bytes()).hexdigest(),
                         self.config['manifiesto_sha256'])
        # cargar() ya verificó cada SHA; aquí se constata el contenido mínimo.
        manifest = json.loads(mp.read_text(encoding='utf-8'))
        for rel in ('base-semantica.json', 'aceptadas.json',
                    'auditorias/auditoria-a.json', 'auditorias/auditoria-b.json'):
            self.assertIn(rel, manifest['archivos'])
        self.assertIsInstance(manifest['insumos'], dict)

    # --- aprobación SHA ---
    def test_doble_aprobacion_con_sha_pinnado(self):
        sha_aceptadas = hashlib.sha256(
            (self.folder / 'aceptadas.json').read_bytes()).hexdigest()
        self.assertEqual(sha_aceptadas, self.delta['aceptadas_sha256'])
        for name in ('auditoria-a', 'auditoria-b'):
            audit = json.loads((self.folder / 'auditorias' / f'{name}.json').read_text(encoding='utf-8'))
            self.assertEqual(audit.get('aceptadas_sha256'), sha_aceptadas)
            ok_reglas = {x['id'] for x in audit['dictamenes']
                         if x['tipo'] == 'reglas' and x['dictamen'] == 'aceptar'}
            ok_vinc = {x['id'] for x in audit['dictamenes']
                       if x['tipo'] == 'vinculos' and x['dictamen'] == 'aceptar'}
            for row in self.accepted['reglas']:
                self.assertIn(row['id'], ok_reglas)
            for row in self.accepted['vinculos']:
                self.assertIn(row['columna'], ok_vinc)

    # --- base exacta ---
    def test_extension_exacta_sobre_base_r6(self):
        from integrar_ronda_4 import validar
        validar(self.rules)  # cadena histórica R4→R7 intacta
        baseline = _read('data/integracion-ronda-7/base-semantica.json')
        R7.validar_sobre_base(self.rules, baseline)

    # --- deltas cruzados (reglas/vínculos derivados, no literales) ---
    def test_deltas_cruzados_reglas_vinculos_conceptos(self):
        n_reglas = len(self.accepted['reglas'])
        n_vinc = len(self.accepted['vinculos'])
        self.assertEqual(n_reglas, self.delta['reglas_nuevas'])
        self.assertEqual(n_vinc, self.delta['vinculos_nuevos'])
        self.assertEqual(len(self.accepted['conceptos']), self.delta['conceptos_nuevos'])
        # Materialización en cobertura: base R6 esperada + delta aprobado.
        r6 = _read('ontologia/revision-ronda-6.json')
        self.assertEqual(
            self.report['resumen']['estados_variables']['respaldada_por_definicion'],
            r6['estados_variables_esperados']['respaldada_por_definicion'] + n_reglas)
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['documental_revisada'],
            self.delta['estados_correspondencias_esperados']['documental_revisada'])
        # Candidatas: 17 del delta + nuevas listadas en el reporte aprobado.
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['candidata_por_nombre'],
            self.delta['estados_correspondencias_esperados']['candidata_por_nombre']
            + len(self.r7report['candidatas_nuevas']))

    def test_materializacion_fiel_y_procedencia(self):
        from rdflib import Graph, Namespace, URIRef
        from rdflib.namespace import RDF
        prov = Namespace('http://www.w3.org/ns/prov#')
        graph = Graph().parse(ROOT / 'data/semantica/interpretaciones.ttl', format='turtle')
        for row in self.accepted['reglas']:
            observed = self.variables[row['definiciones'][0]]
            self.assertEqual(observed.get('estado'), 'respaldada_por_definicion')
            self.assertEqual(observed.get('regla'), row['id'])
            self.assertEqual(observed.get('concepto'), row['concepto'])
            self.assertEqual(observed.get('huella_fila_diccionario'), row['huella_fila_diccionario'])
            sources = list(graph.objects(URIRef(observed['iri']), prov.wasDerivedFrom))
            self.assertTrue(any('integracion-ronda-7' in str(s) for s in sources))
        for row in self.accepted['vinculos']:
            self.assertEqual(self.mappings[row['columna']]['revision'], row)

    # --- scope ---
    def test_scope_cerrado_sin_vigencias_joins_identidad(self):
        prohibidas = {'vigencia', 'vigencias', 'join', 'joins', 'equivalencia',
                      'identidad_catalogo', 'codigo_nacional', 'edicion_catalogo'}
        self.assertFalse(set(R7.REGLA_KEYS) & prohibidas)
        self.assertFalse(set(R7.VINCULO_KEYS) & prohibidas)
        for row in self.accepted['reglas']:
            self.assertFalse(set(row) - R7.REGLA_KEYS)
        for row in self.accepted['vinculos']:
            self.assertFalse(set(row) - R7.VINCULO_KEYS)
            self.assertIn(row['columna'], R7.PARES_20)
        for row in self.accepted['reglas']:
            self.assertIn(row['definiciones'][0], R7.UNIVERSO_31)

    def test_pendientes_conservados_no_promovidos(self):
        aceptadas_defs = {r['definiciones'][0] for r in self.accepted['reglas']}
        # Filas D103/D105 fuera del lote: siguen sin respaldo en este pase.
        for sufijo in ('%2F103', '%2F105'):
            self.assertFalse([d for d in aceptadas_defs if d.endswith(sufijo)])
        # Las 28 nuevas del reporte siguen candidatas, no revisadas.
        revisadas = {v['columna'] for v in self.report['correspondencias']
                     if v['estado'] == 'documental_revisada'}
        for columna in self.r7report['candidatas_nuevas']:
            self.assertNotIn(columna, revisadas)

    def test_construir_emite_solo_procedencia(self):
        import tomllib
        permitidos = {'wasDerivedFrom', 'sha256Evidencia', 'type'}
        base_iri = tomllib.loads((ROOT / 'config.toml').read_bytes().decode('utf-8'))['catalogo']['base_iri']
        graph, _, _ = R7.construir(self.report, self.rules, base_iri)
        self.assertTrue(len(graph) > 0)
        for _, p, _ in graph:
            self.assertIn(str(p).split('#')[-1].split('/')[-1], permitidos)

    # --- negativas (solo lectura: mutan copias en memoria) ---
    def test_rechaza_regla_intrusa_fuera_del_universo(self):
        rules = copy.deepcopy(self.rules)
        intrusa = copy.deepcopy(self.accepted['reglas'][0])
        intrusa['id'] = 'r7-intrusa'
        intrusa['definiciones'] = ['https://example.org/mex-ontologi/definition/intrusa%2F1']
        rules['reglas_descripcion_exacta'].append(intrusa)
        baseline = _read('data/integracion-ronda-7/base-semantica.json')
        with self.assertRaises(ValueError):
            R7.validar_sobre_base(rules, baseline)

    def test_rechaza_vinculo_fuera_de_allowlist(self):
        rules = copy.deepcopy(self.rules)
        intruso = copy.deepcopy(self.accepted['vinculos'][0])
        intruso['columna'] = 'https://example.org/mex-ontologi/file-column/intrusa%2F1'
        rules['vinculos_documentales_revisados'].append(intruso)
        baseline = _read('data/integracion-ronda-7/base-semantica.json')
        with self.assertRaises(ValueError):
            R7.validar_sobre_base(rules, baseline)

    def test_rechaza_base_alterada(self):
        baseline = _read('data/integracion-ronda-7/base-semantica.json')
        base = copy.deepcopy(baseline)
        base['observaciones_revision'] = []
        with self.assertRaises(ValueError):
            R7.validar_sobre_base(self.rules, base)

    # --- gancho R8 ---
    def test_r8_hook_por_deltas_aprobados(self):
        """Expectativa de revisadas = base + deltas aprobados de manifiestos.

        Hoy suma R6+R7 leídos de sus aceptadas.json validados. Si aterriza
        revision-ronda-8.json, este test exige sumar también su delta
        aprobado (nunca el vivo contra sí mismo); fallará a propósito
        hasta extender el patrón, en vez de fingir cobertura.
        """
        r2 = _read('ontologia/revision-ronda-2.json')
        total = r2['esperado_actual']['revisadas']
        for modulo, nombre in (('integrar_ronda_6', 'revision-ronda-6.json'),
                               ('integrar_ronda_7', 'revision-ronda-7.json')):
            if (ROOT / f'ontologia/{nombre}').exists():
                mod = __import__(modulo, fromlist=['cargar'])
                _, _, _, aceptadas, _ = mod.cargar()
                total += len(aceptadas['vinculos'])
        if (ROOT / 'ontologia/revision-ronda-8.json').exists():
            mod = __import__('integrar_ronda_8', fromlist=['cargar'])
            _, _, _, aceptadas8, _ = mod.cargar()
            total += len(aceptadas8['vinculos'])
        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), total)
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['documental_revisada'], total)


if __name__ == '__main__':
    unittest.main()
