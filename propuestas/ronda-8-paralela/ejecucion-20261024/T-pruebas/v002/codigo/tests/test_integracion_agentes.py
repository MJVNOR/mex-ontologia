import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from openpyxl import Workbook

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'ontologia/semantica.json').exists())
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import interpretacion
from integrar_entregas import composicion_exacta, construir, leer_tabla


def _aceptadas_ronda(n):
    """Delta aprobado R{n} validado por cadena de SHAs, sin importar integradores.

    Lee ontologia/revision-ronda-{n}.json → verifica manifiesto_sha256 contra
    el manifiesto real → verifica cada SHA de archivos → devuelve aceptadas.json.
    Sin config → None (ronda ausente; delta cero). Solo lectura; nunca compara
    el vivo consigo mismo. (v002: vía R8 sin diseñar integrador.)
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


class IntegracionAgentesTest(unittest.TestCase):
    def test_composicion_no_acepta_prefijo_corto_letras_ni_digitos_unicode(self):
        self.assertTrue(composicion_exacta('26001', '26'))
        for municipal, entidad in [('26001', '2'), ('26ABC', '26'), ('２６００１', '２６'),
                                    ('٢٦٠٠١', '٢٦'), ('26¹23', '26'), ('26001', '27'), (None, '26')]:
            self.assertFalse(composicion_exacta(municipal, entidad))

    def test_las_20_reglas_no_alcanzan_otro_diccionario_conjunto_o_definicion(self):
        rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        proposals = json.loads((ROOT / 'data/integracion/entregas/agente-3-significados/propuestas.json').read_text(encoding='utf-8'))
        for v in proposals['variables']:
            if v['decision'] != 'proponer':
                continue
            args = [v['variable'], v['descripcion_literal'], v['conjunto'], rules, v['diccionario'], v['definicion_iri']]
            expected = v['regla_propuesta']['id']
            self.assertEqual(interpretacion(*args)['regla'], expected)
            for pos in [2, 4, 5]:
                other = args.copy(); other[pos] = 'otra-fuente'
                self.assertNotEqual(interpretacion(*other).get('regla'), expected)

    def test_62_revisiones_previas_se_conservan_integramente(self):
        manifest = json.loads((ROOT / 'data/integracion/manifiesto.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(ROOT / manifest['respaldo']) as z:
            before = json.loads(z.read('ontologia/semantica.json'))
        after = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
        self.assertEqual(len(before['vinculos_documentales_revisados']), 62)
        config = json.loads((ROOT / 'ontologia/revision-agentes.json').read_text(encoding='utf-8'))
        r6n = 0
        if (ROOT / 'ontologia/revision-ronda-6.json').exists():
            from integrar_ronda_6 import cargar as cargar_r6
            _, _, _, accepted_r6, _ = cargar_r6()
            r6n = len(accepted_r6['vinculos'])
        r7n = 0
        if (ROOT / 'ontologia/revision-ronda-7.json').exists():
            # Delta R7 derivado del manifiesto fijado (3.º sumando); sin
            # hardcodear el conteo observado. R8 extenderá este patrón.
            from integrar_ronda_7 import cargar as cargar_r7
            _, _, _, accepted_r7, _ = cargar_r7()
            r7n = len(accepted_r7['vinculos'])
        r8 = _aceptadas_ronda(8)
        r8n = len(r8['vinculos']) if r8 is not None else 0
        self.assertEqual(len(after['vinculos_documentales_revisados']),
                         config.get('esperado_actual', config['esperado'])['correspondencias_revisadas'] + r6n + r7n + r8n)
        for item in before['vinculos_documentales_revisados']:
            self.assertIn(item, after['vinculos_documentales_revisados'])

    def test_un_manifiesto_modificado_impide_generar(self):
        with patch('integrar_entregas.sha', return_value='0' * 64):
            with self.assertRaisesRegex(ValueError, 'Manifiesto'):
                construir(None, None, None, None, 'https://example.org/test/')

    def test_lector_conserva_ceros_texto_y_rechaza_formulas(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'referencia.xlsx'
            wb = Workbook(); sh = wb.active; sh.append(['Clave', 'Nombre']); sh.append(['001', 'Educación']); wb.save(path)
            self.assertEqual(leer_tabla(path)[1], ['001', 'Educación'])
            sh['A2'] = '=1+1'; wb.save(path); wb.close()
            with self.assertRaisesRegex(ValueError, 'Fórmula'):
                leer_tabla(path)


if __name__ == '__main__':
    unittest.main()
