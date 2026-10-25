"""Controles de la extensión exacta de vínculos y su manifiesto fijado."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(HERE))
from integrar_ronda_3 import validar_extension_vinculos


def guardar(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class ExtensionFijada(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.previous = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))['vinculos_documentales_revisados'][:836]
        self.additions = json.loads((ROOT / 'propuestas/ronda-3/agente-2-correspondencias/entrada_integracion_29.json').read_text(encoding='utf-8'))['entradas']
        folder = self.root / 'data/integracion-ronda-3'
        guardar(folder / 'vinculos-anteriores.json', self.previous)
        guardar(folder / 'correspondencias-29.json', {'entradas': self.additions})
        manifest = {'archivos': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in folder.iterdir()}, 'insumos': {}}
        guardar(folder / 'manifiesto.json', manifest)
        guardar(self.root / 'ontologia/revision-ronda-3.json', {
            'evidencia': 'data/integracion-ronda-3',
            'manifiesto_sha256': hashlib.sha256((folder / 'manifiesto.json').read_bytes()).hexdigest()})
        self.rules = {'vinculos_documentales_revisados': copy.deepcopy(self.previous + self.additions)}

    def check(self):
        return validar_extension_vinculos(self.rules, self.previous, self.root)

    def test_extension_exacta(self):
        self.assertEqual(self.check(), self.additions)

    def test_rechaza_previa_modificada(self):
        self.rules['vinculos_documentales_revisados'][0]['concepto'] = 'alterado'
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_adicion_modificada(self):
        self.rules['vinculos_documentales_revisados'][-1]['huella_esquema'] = '0' * 64
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_adicion_extra(self):
        self.rules['vinculos_documentales_revisados'].append(self.additions[0])
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_previa_omitida(self):
        del self.rules['vinculos_documentales_revisados'][0]
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_reordenacion(self):
        self.rules['vinculos_documentales_revisados'].reverse()
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_manifiesto_modificado(self):
        (self.root / 'data/integracion-ronda-3/manifiesto.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_evidencia_modificada(self):
        (self.root / 'data/integracion-ronda-3/correspondencias-29.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.check()

    def test_rechaza_ruta_fuera_de_carpeta(self):
        guardar(self.root / 'ontologia/revision-ronda-3.json', {'evidencia': '../fuera'})
        with self.assertRaises(ValueError):
            self.check()


if __name__ == '__main__':
    unittest.main()
