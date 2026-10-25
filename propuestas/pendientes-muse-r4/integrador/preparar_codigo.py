"""Prepara cambios centrales revisables sin instalarlos."""
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[3]
STAGE=ROOT/'propuestas/pendientes-muse-r4'
OUT=STAGE/'integrador/codigo'

def edit(relative, replacements):
    value=(ROOT/relative).read_text(encoding='utf-8')
    for old,new in replacements:
        if value.count(old)!=1:
            raise ValueError('Fragmento no único: '+relative+' / '+old[:60])
        value=value.replace(old,new)
    path=OUT/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(value,encoding='utf-8')

def main():
    edit('scripts/integrar_ronda_3.py',[
        ("    links = rules['vinculos_documentales_revisados']\n", "    if (root / 'ontologia/revision-ronda-4.json').exists():\n        from integrar_ronda_4 import validar\n        _, _, base_r4, _, _ = validar(rules, root)\n        links = base_r4['vinculos_documentales_revisados']\n    else:\n        links = rules['vinculos_documentales_revisados']\n"),
        ("    if len(mappings) != 865:\n", "    if not {r['columna'] for r in rules['vinculos_documentales_revisados'][:865]}.issubset(mappings):\n"),
        ("                   'correspondencias_revisadas_totales': len(mappings),", "                   'correspondencias_revisadas_totales': len(mappings),\n                   'correspondencias_historicas_ronda_3': 865,")])
    edit('scripts/consolidar_semantica.py',[
        ("        matches = lookup.get((col['conjunto'], clave(variable_name)), [])\n", "        matches = lookup.get((col['conjunto'], clave(variable_name)), [])\n        definition_pin = revision.get('definicion_iri') if revision else None\n        if definition_pin:\n            if not revision.get('columna') or not all(revision.get(k) for k in ('huella_esquema', 'huella_fila_diccionario', 'descripcion', 'criterio')):\n                raise ValueError('Selección de definición requiere columna física y evidencia completa')\n            matches = [v for v in matches if v['definicion_iri'] == definition_pin]\n"),
        ("            if len(matches) != 1 or all_names[(col['conjunto'], clave(variable_name))] != 1 or not col['nombre_unico'] or matches[0]['diccionario'] != revision['diccionario'] or matches[0].get('concepto') != revision['concepto'] or matches[0]['estado'] != 'respaldada_por_definicion':", "            name_ambiguous = (all_names[(col['conjunto'], clave(variable_name))] != 1 or not col['nombre_unico']) and not definition_pin\n            if len(matches) != 1 or name_ambiguous or matches[0]['diccionario'] != revision['diccionario'] or matches[0].get('concepto') != revision['concepto'] or matches[0]['estado'] != 'respaldada_por_definicion':"),
        ("    report['huellas_entrada'] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}",
         "    if (ROOT / 'ontologia/revision-ronda-4.json').exists():\n        from integrar_ronda_4 import construir as integrar_ronda_4\n        r4_data, r4_report, r4_sources = integrar_ronda_4(report, rules, base)\n        data += r4_data\n        report['integracion_ronda_4'] = r4_report\n        sources.update(r4_sources)\n    report['huellas_entrada'] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}")])
    edit('tests/test_ronda_3_integrada.py',[
        ("        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), 865)\n        self.assertEqual(self.report['resumen']['estados_correspondencias']['documental_revisada'], 865)",
         "        expected = 865 + self.report.get('integracion_ronda_4', {}).get('correspondencias_nuevas', 0)\n        self.assertEqual(len(self.rules['vinculos_documentales_revisados']), expected)\n        self.assertEqual(self.report['resumen']['estados_correspondencias']['documental_revisada'], expected)"),
        ("        after = copy.deepcopy(self.rules)\n", "        if (ROOT / 'ontologia/revision-ronda-4.json').exists():\n            from integrar_ronda_4 import validar\n            _, _, r4_before, _, _ = validar(self.rules)\n            after = copy.deepcopy(r4_before)\n        else:\n            after = copy.deepcopy(self.rules)\n")])
    edit('tests/test_cobertura_integrada.py',[
        ("        self.assertEqual(dict(Counter(v['estado'] for v in self.variables.values())),\n                         self.accepted['resumen']['estados_variables_esperados'])",
         "        expected = dict(self.accepted['resumen']['estados_variables_esperados'])\n        if (ROOT / 'ontologia/revision-ronda-4.json').exists():\n            from integrar_ronda_4 import validar\n            _, _, _, r4, _ = validar(self.rules)\n            old = {v['definicion_iri']: v for v in self.variables.values()}\n            base = json.loads((ROOT / 'data/integracion-ronda-4/base-cobertura.json').read_text(encoding='utf-8'))\n            before = {v['definicion_iri']: v for v in base['variables']}\n            for rule in r4['reglas']:\n                state = before[rule['definiciones'][0]]['estado']\n                expected[state] -= 1\n                expected['respaldada_por_definicion'] += 1\n            expected = {k:v for k,v in expected.items() if v}\n        self.assertEqual(dict(Counter(v['estado'] for v in self.variables.values())), expected)"),
        ("    def test_condicionados_y_pendientes_no_se_promueven(self):\n        for decision", "    def test_condicionados_y_pendientes_no_se_promueven(self):\n        promoted = set()\n        if (ROOT / 'ontologia/revision-ronda-4.json').exists():\n            from integrar_ronda_4 import validar\n            _, _, _, r4, _ = validar(self.rules)\n            promoted = {d for r in r4['reglas'] for d in r['definiciones']}\n        for decision"),
        ("            if decision['estado_integracion'] == 'pendiente':\n                self.assertEqual(variable['estado'], 'fuera_del_nucleo_actual')",
         "            if decision['estado_integracion'] == 'pendiente':\n                if decision['definicion_iri'] in promoted:\n                    self.assertEqual(variable['estado'], 'respaldada_por_definicion')\n                else:\n                    self.assertEqual(variable['estado'], 'fuera_del_nucleo_actual')")])
    destination=OUT/'scripts/integrar_ronda_4.py'
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(STAGE/'integrador/integrar_ronda_4.py',destination)
    print('Cambios preparados; núcleo sin instalar')

if __name__=='__main__':
    main()
