"""Prepara reparacion-test-enie/tests/test_ronda_2.py: copia exacta del central
con SOLO test_enie_no_se_promueve_como_acento corregido. No toca central."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
src = (ROOT / 'tests/test_ronda_2.py').read_text(encoding='utf-8')
old = '''    def test_enie_no_se_promueve_como_acento(self):
        p = json.loads((ROOT / 'data/integracion-ronda-2/entregas/agente-1-correspondencias/propuestas.json').read_text(encoding='utf-8'))
        candidates = [x for x in p['pendientes_clasificados'] if x.get('etapa') == 'vinculo']
        self.assertEqual(len(candidates), 1)
        target = candidates[0]['columna']
        self.assertNotIn(target, {r['columna'] for r in self.rules['vinculos_documentales_revisados']})
'''
new = '''    def test_enie_no_se_promueve_como_acento(self):
        from integrar_contenido import clave
        from consolidar_semantica import huella
        # 1. El normalizador SI confunde e\u00f1e: 'A\u00f1o' y 'ano' colisionan; prohibido aprobar por nombre.
        self.assertNotEqual('A\u00f1o', 'ano')
        self.assertEqual(clave('A\u00f1o'), clave('ano'))
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
                         ('A\u00f1o', 'a95d2d39-12df-4836-9792-1ce52e05db3c', 'anio-registro', 'A\u00f1o del registro'))
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
'''
assert src.count(old) == 1, 'metodo original no hallado exacto 1 vez'
new_src = src.replace(old, new)
root_old = "ROOT = Path(__file__).resolve().parents[1]"
root_new = "ROOT = Path(__file__).resolve().parents[5]  # copia en auditoria-b: mismo repo real, sin tocar central"
assert new_src.count(root_old) == 1
new_src = new_src.replace(root_old, root_new)
out = ROOT / 'propuestas/pendientes-muse-r4/auditoria-b/reparacion-test-enie/tests/test_ronda_2.py'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(new_src, encoding='utf-8')
print('escrito', out)
