"""Sondas dirigidas: la prueba corregida debe FALLAR sin recibo explicito o con hash alterado."""
import sys
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'propuestas/pendientes-muse-r4/auditoria-b/reparacion-test-enie/tests')
import copy
import unittest
import test_ronda_2 as t

t.Ronda2Test.setUpClass()
TARGET = 'https://example.org/mex-ontologi/file-column/e52ec9d3-2242-4928-b2a3-06b95800c229%2FHoja1%2F1'


def run_with(rules):
    inst = t.Ronda2Test('test_enie_no_se_promueve_como_acento')
    inst.rules = rules
    inst.test_enie_no_se_promueve_como_acento()


base = t.Ronda2Test.rules
results = {}

# 1. Sin recibo (solo normalizador): debe FALLAR (prohibe aprobar por nombre).
try:
    run_with({**base, 'vinculos_documentales_revisados':
              [r for r in base['vinculos_documentales_revisados'] if r['columna'] != TARGET]})
    results['sin-recibo-debe-fallar'] = 'NO FALLO (MAL)'
except AssertionError:
    results['sin-recibo-debe-fallar'] = 'falla OK'

# 2. Hash de fila alterado: debe FALLAR.
alt = copy.deepcopy(base['vinculos_documentales_revisados'])
for r in alt:
    if r['columna'] == TARGET:
        r['huella_fila_diccionario'] = '0' * 64
try:
    run_with({**base, 'vinculos_documentales_revisados': alt})
    results['hash-alterado-debe-fallar'] = 'NO FALLO (MAL)'
except AssertionError:
    results['hash-alterado-debe-fallar'] = 'falla OK'

# 3. Concepto distinto al vigente: debe FALLAR.
alt2 = copy.deepcopy(base['vinculos_documentales_revisados'])
for r in alt2:
    if r['columna'] == TARGET:
        r['concepto'] = 'otro-concepto'
try:
    run_with({**base, 'vinculos_documentales_revisados': alt2})
    results['concepto-distinto-debe-fallar'] = 'NO FALLO (MAL)'
except AssertionError:
    results['concepto-distinto-debe-fallar'] = 'falla OK'

# 4. Recibo intacto: debe PASAR.
try:
    run_with(base)
    results['recibo-intacto-debe-pasar'] = 'pasa OK'
except AssertionError as e:
    results['recibo-intacto-debe-pasar'] = f'FALLO INESPERADO: {e}'

print(results)
assert all(v.endswith('OK') for v in results.values()), results
print('SONDAS DIRIGIDAS OK')
