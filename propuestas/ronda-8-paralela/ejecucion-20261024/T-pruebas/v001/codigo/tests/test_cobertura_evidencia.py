import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists()) / 'scripts'))
from integrar_cobertura import cargar_evidencia


class EvidenciaCoberturaTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'data/integracion-cobertura'
        self.folder.mkdir(parents=True)
        (self.root / 'ontologia').mkdir()
        self.before = {'conceptos': {'anterior': ['Anterior', 'Definición previa', None]},
                       'reglas_descripcion_exacta': [{'id': 'previa', 'concepto': 'anterior'}],
                       'vinculos_documentales_revisados': [{'columna': 'preservar'}],
                       'observaciones_revision': [], 'condiciones': {'contexto': 'Preservar'}}
        self.accepted = {'conceptos': {'nuevo': ['Nuevo', 'Nueva definición', None]},
                         'reglas': [{'id': 'nueva', 'concepto': 'nuevo'}]}
        self.rules = copy.deepcopy(self.before)
        self.rules['conceptos'].update(self.accepted['conceptos'])
        self.rules['reglas_descripcion_exacta'] += self.accepted['reglas']
        self.write(self.folder / 'base-semantica.json', self.before)
        self.write(self.folder / 'aceptadas.json', self.accepted)
        self.source = self.root / 'data/fuente.json'
        self.write(self.source, {'descripcion': 'Literal documentado'})
        self.manifest = {'archivos': {name: self.sha(self.folder / name) for name in
                                    ('base-semantica.json', 'aceptadas.json')},
                         'insumos': {'data/fuente.json': self.sha(self.source)}}
        self.save_manifest()

    def sha(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def save_manifest(self):
        self.write(self.folder / 'manifiesto.json', self.manifest)
        self.write(self.root / 'ontologia/revision-cobertura.json', {
            'evidencia': 'data/integracion-cobertura',
            'manifiesto_sha256': self.sha(self.folder / 'manifiesto.json')})

    def test_evidencia_fijada_y_reglas_anteriores_se_validan(self):
        _, accepted, _, sources = cargar_evidencia(self.rules, self.root)
        self.assertEqual(accepted, self.accepted)
        self.assertIn(self.source, sources.values())

    def test_cambio_de_documento_impide_regenerar(self):
        self.write(self.source, {'descripcion': 'Descripción nueva sin revisar'})
        with self.assertRaisesRegex(ValueError, 'Fuente documental'):
            cargar_evidencia(self.rules, self.root)

    def test_alteracion_de_entrega_o_manifiesto_es_rechazada(self):
        (self.folder / 'aceptadas.json').write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Evidencia de cobertura'):
            cargar_evidencia(self.rules, self.root)
        self.write(self.folder / 'manifiesto.json', {})
        with self.assertRaisesRegex(ValueError, 'Manifiesto'):
            cargar_evidencia(self.rules, self.root)

    def test_no_permite_cambiar_una_regla_previa_o_un_vinculo(self):
        rules = copy.deepcopy(self.rules)
        rules['reglas_descripcion_exacta'][0]['concepto'] = 'nuevo'
        with self.assertRaisesRegex(ValueError, 'Regla aceptada o anterior'):
            cargar_evidencia(rules, self.root)
        rules = copy.deepcopy(self.rules)
        rules['vinculos_documentales_revisados'] = []
        with self.assertRaisesRegex(ValueError, 'vinculos_documentales'):
            cargar_evidencia(rules, self.root)

    def test_manifiesto_no_puede_salir_de_su_carpeta(self):
        self.manifest['archivos']['../../escape.json'] = '0' * 64
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'fuera de su carpeta'):
            cargar_evidencia(self.rules, self.root)


if __name__ == '__main__':
    unittest.main()
