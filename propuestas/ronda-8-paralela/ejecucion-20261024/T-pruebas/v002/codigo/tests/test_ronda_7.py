"""Cobertura específica R7 (staging v002, compatible R8).

Deriva todo de manifiestos fijados (aceptadas.json, delta.json,
auditorías, reports/ronda-7.json, baseline R7 pinnada); no hardcodea
conteos observados (ni 4506) ni compara el vivo consigo mismo. Solo
lectura de producción: no instala nada.

R8 (esta ejecución: solo vínculos M1/M2, 0 reglas, 0 conceptos) se lee
por deltas aceptados validados (cadena de SHAs), sin importar ni diseñar
integrador. Con config R8 ausente, los bloques R8 son no-op y todo vale
en era R7; con config R8, las expectativas descuentan/aplican su delta.
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


def _aceptadas_ronda(n):
    """Delta aprobado R{n} validado por cadena de SHAs, sin importar integradores.

    Lee ontologia/revision-ronda-{n}.json → verifica manifiesto_sha256 contra
    el manifiesto real → verifica cada SHA de archivos → devuelve aceptadas.json.
    Sin config → None (ronda ausente; delta cero). Solo lectura.
    """
    cfg_path = ROOT / f'ontologia/revision-ronda-{n}.json'
    if not cfg_path.exists():
        return None
    config = json.loads(cfg_path.read_text(encoding='utf-8'))
    folder = (ROOT / config['evidencia']).resolve()
    if not folder.is_relative_to(ROOT.resolve()):
        raise ValueError(f'Manifiesto de ronda {n} fuera de carpeta')
    mp = folder / 'manifiesto.json'
    if hashlib.sha256(mp.read_bytes()).hexdigest() != config['manifiesto_sha256']:
        raise ValueError(f'Manifiesto de ronda {n} modificado')
    manifest = json.loads(mp.read_text(encoding='utf-8'))
    for rel, h in manifest.get('archivos', {}).items():
        p = (folder / rel).resolve()
        if not p.is_relative_to(folder):
            raise ValueError(f'Evidencia de ronda {n} fuera de carpeta')
        if hashlib.sha256(p.read_bytes()).hexdigest() != h:
            raise ValueError(f'Evidencia de ronda {n} modificada: ' + rel)
    return json.loads((folder / 'aceptadas.json').read_text(encoding='utf-8'))


def _base_r7_pinnada():
    """Baseline R7 pinnada: base-semantica.json con SHA fijado en delta.json."""
    raw = (ROOT / 'data/integracion-ronda-7/base-semantica.json').read_bytes()
    delta = _read('data/integracion-ronda-7/delta.json')
    if hashlib.sha256(raw).hexdigest() != delta['base_sha256']:
        raise ValueError('Baseline R7 pinnada modificada')
    return json.loads(raw.decode('utf-8'))


def _reglas_era_r7(rules_live):
    """Vivo menos delta R8 validado = era R7 (si hay config R8; si no, el vivo)."""
    r8 = _aceptadas_ronda(8)
    if r8 is None:
        return rules_live
    era = copy.deepcopy(rules_live)
    cols8 = {v['columna'] for v in r8.get('vinculos', [])}
    ids8 = {r['id'] for r in r8.get('reglas', [])}
    era['vinculos_documentales_revisados'] = [
        v for v in era['vinculos_documentales_revisados'] if v['columna'] not in cols8]
    era['reglas_descripcion_exacta'] = [
        r for r in era['reglas_descripcion_exacta'] if r['id'] not in ids8]
    return era


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
        cls.r8 = _aceptadas_ronda(8)
        cls.r8_cols = {v['columna'] for v in cls.r8.get('vinculos', [])} if cls.r8 else set()

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

    # --- base exacta por aritmética pinnada (válida en era R7 y tras R8) ---
    def test_extension_exacta_base_pinnada_mas_deltas(self):
        # La cadena R4→R7 no conoce R8 (igualdad exacta sobre el vivo
        # fallaría tras instalarlo sin un integrador nuevo, que no se
        # diseña aquí): se sustituye por baseline pinnada + deltas
        # aceptados validados. Nada compara el vivo consigo mismo.
        base = _base_r7_pinnada()
        expected = copy.deepcopy(base)
        expected['reglas_descripcion_exacta'].extend(self.accepted['reglas'])
        expected['vinculos_documentales_revisados'].extend(self.accepted['vinculos'])
        for k, v in self.accepted['conceptos'].items():
            if k in expected['conceptos']:
                raise ValueError('Ronda 7 exige concepto nuevo, clave ya existente: ' + k)
            expected['conceptos'][k] = v
        if self.r8 is not None:
            for row in self.r8.get('reglas', []):
                expected['reglas_descripcion_exacta'].append(row)
            for row in self.r8.get('vinculos', []):
                expected['vinculos_documentales_revisados'].append(row)
            for k, v in self.r8.get('conceptos', {}).items():
                if k in expected['conceptos'] and expected['conceptos'][k] != v:
                    raise ValueError('Ronda 8 sustituyó concepto previo: ' + k)
                expected['conceptos'][k] = v
        for field, key in [('reglas_descripcion_exacta', 'id'),
                           ('vinculos_documentales_revisados', 'columna')]:
            ids = [r[key] for r in expected[field]]
            self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.rules, expected)

    # --- deltas cruzados (derivados, no literales; R8 descuenta) ---
    def test_deltas_cruzados_reglas_vinculos_conceptos(self):
        n_reglas = len(self.accepted['reglas'])
        n_vinc = len(self.accepted['vinculos'])
        self.assertEqual(n_reglas, self.delta['reglas_nuevas'])
        self.assertEqual(n_vinc, self.delta['vinculos_nuevos'])
        self.assertEqual(len(self.accepted['conceptos']), self.delta['conceptos_nuevos'])
        # Materialización en cobertura: base R6 esperada + delta aprobado R7.
        # R8 no trae reglas: las respaldadas no se mueven con su instalación.
        r6 = _read('ontologia/revision-ronda-6.json')
        self.assertEqual(
            self.report['resumen']['estados_variables']['respaldada_por_definicion'],
            r6['estados_variables_esperados']['respaldada_por_definicion'] + n_reglas)
        # Revisadas: delta R7 + delta R8 validado (sin hardcodear 4506).
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['documental_revisada'],
            self.delta['estados_correspondencias_esperados']['documental_revisada'] + len(self.r8_cols))
        # Candidatas: 17 del delta + 28 nuevas del reporte − promovidas por R8.
        nuevas = self.r7report['candidatas_nuevas']
        self.assertTrue(self.r8_cols <= set(nuevas),
                        'R8 fuera de M1/M2: columnas no previstas en esta ejecución')
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['candidata_por_nombre'],
            self.delta['estados_correspondencias_esperados']['candidata_por_nombre']
            + len(nuevas) - len(self.r8_cols & set(nuevas)))

    def test_materializacion_fiel_y_procedencia(self):
        from rdflib import Graph, Namespace, URIRef
        from rdflib.namespace import RDF  # noqa: F401 (reserva de integridad del grafo)
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
        if self.r8 is not None:
            # Tras instalar R8, sus vínculos aceptados materializan fielmente.
            rows = {r['columna']: r for r in self.r8.get('vinculos', [])}
            for columna, row in rows.items():
                self.assertEqual(self.mappings[columna]['revision'], row)

    # --- scope (R7 + R8 solo-vínculos) ---
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
        if self.r8 is not None:
            # Scope R8 de esta ejecución: SOLO vínculos, sin reglas ni
            # conceptos; columnas dentro de M1/M2 (las 28 nuevas).
            self.assertEqual(list(self.r8.get('reglas', [])), [])
            self.assertEqual(dict(self.r8.get('conceptos', {})), {})
            self.assertTrue(self.r8_cols <= set(self.r7report['candidatas_nuevas']))

    def test_pendientes_conservados_no_promovidos(self):
        aceptadas_defs = {r['definiciones'][0] for r in self.accepted['reglas']}
        # Filas D103/D105 fuera del lote: siguen sin respaldo en este pase.
        for sufijo in ('%2F103', '%2F105'):
            self.assertFalse([d for d in aceptadas_defs if d.endswith(sufijo)])
        # Las 28 nuevas: candidatas en era R7; revisadas si R8 las instaló.
        revisadas = {v['columna'] for v in self.report['correspondencias']
                     if v['estado'] == 'documental_revisada'}
        for columna in self.r7report['candidatas_nuevas']:
            if columna in self.r8_cols:
                self.assertIn(columna, revisadas)
            else:
                self.assertNotIn(columna, revisadas)

    def test_construir_emite_solo_procedencia(self):
        import tomllib
        permitidos = {'wasDerivedFrom', 'sha256Evidencia', 'type'}
        base_iri = tomllib.loads((ROOT / 'config.toml').read_bytes().decode('utf-8'))['catalogo']['base_iri']
        # Sobre la era R7 (el constructor R7 no conoce R8 por diseño).
        graph, _, _ = R7.construir(self.report, _reglas_era_r7(self.rules), base_iri)
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

    # --- total por deltas aprobados (válido en era R7 y tras instalar R8) ---
    def test_revisadas_totales_por_deltas_aprobados(self):
        """Expectativa de revisadas = baseline R7 pinnada + deltas validados.

        Nunca el vivo contra sí mismo y sin hardcodear 4506: la base sale
        del pin SHA y cada delta de su aceptadas.json validado. Si R8 existe
        en config, su delta suma; si no, el total es el de era R7.
        """
        base = _base_r7_pinnada()
        total = len(base['vinculos_documentales_revisados']) + len(self.accepted['vinculos'])
        if self.r8 is not None:
            total += len(self.r8.get('vinculos', []))
        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), total)
        self.assertEqual(
            self.report['resumen']['estados_correspondencias']['documental_revisada'], total)


if __name__ == '__main__':
    unittest.main()
