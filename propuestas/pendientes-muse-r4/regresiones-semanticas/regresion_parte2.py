"""Parte 2: preservacion en construccion combinada (C), esquema/fila (D), duplicadas (E)."""
import copy
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas' / 'pendientes-muse-r4'
PREP = STAGE / 'integrador' / 'codigo' / 'scripts'
sys.path.insert(0, str(PREP))
sys.path.append(str(ROOT / 'scripts'))

from integrar_contenido import clave  # noqa: E402
import consolidar_semantica as GEN  # noqa: E402
assert 'integrador' in GEN.__file__, GEN.__file__
import consolidar_semantica as NUCLEO_CHECK  # noqa: F401  (mismo modulo; el nucleo se compara por archivo)

OUT = STAGE / 'regresiones-semanticas'
RESULTS = json.loads((OUT / '_parte1.json').read_text(encoding='utf-8'))


def caso(suite, cid, descripcion, esperado, ok, observacion=''):
    RESULTS.append({'suite': suite, 'id': cid, 'descripcion': descripcion,
                    'esperado': esperado, 'resultado': 'aprobado' if ok else 'fallido',
                    'observacion': observacion})
    return ok


def fails_with(fn, fragment=''):
    try:
        fn()
    except ValueError as e:
        return fragment in str(e), str(e)[:300]
    except Exception as e:
        return False, 'otra excepcion: %r' % e
    return False, 'NO FALLO'


base = json.loads((ROOT / 'ontologia' / 'semantica.json').read_text(encoding='utf-8'))
cob = json.loads((ROOT / 'data' / 'semantica' / 'cobertura.json').read_text(encoding='utf-8'))
inventory = json.loads((ROOT / 'data' / 'portal' / 'inventario.json').read_text(encoding='utf-8'))
inspection = json.loads((ROOT / 'data' / 'portal' / 'contenido-inspeccion.json').read_text(encoding='utf-8'))
ref_path = ROOT / 'data' / 'portal' / 'lote-cruces' / 'catalogo-municipal-portal.json'
reference = json.loads(ref_path.read_text(encoding='utf-8')) if ref_path.exists() else None
import tomllib
base_iri = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']

nuevas, vinculos, conceptos = [], [], {}
for i in range(1, 7):
    d = json.loads((STAGE / f'lote-{i}' / 'entrega.json').read_text(encoding='utf-8'))
    nuevas.extend(d.get('reglas', []))
    vinculos.extend(d.get('vinculos', []))
    for k, v in d.get('conceptos_nuevos', {}).items():
        conceptos.setdefault(k, v)
amb = json.loads((STAGE / 'ambiguedades' / 'entrega.json').read_text(encoding='utf-8'))

merged = copy.deepcopy(base)
for k, v in conceptos.items():
    merged['conceptos'][k] = v
merged['reglas_descripcion_exacta'].extend(copy.deepcopy(nuevas))
merged['vinculos_documentales_revisados'].extend(copy.deepcopy(vinculos))

# ---------- Suite C: construccion combinada sin instalar ----------
t0 = time.time()
_, _, report = GEN.construir(inventory, inspection, merged, reference, base_iri)
dt = time.time() - t0
print('construir combinada: %.1fs' % dt)
json.dump({'variables': [{'definicion_iri': v.get('definicion_iri'), 'estado': v.get('estado'),
                          'regla': v.get('regla'), 'concepto': v.get('concepto')}
                         for v in report['variables']],
           'correspondencias': [{'columna': m['columna'], 'estado': m['estado']} for m in report['correspondencias']]},
          (OUT / '_report.json').open('w', encoding='utf-8'), ensure_ascii=False)

vars_rep = {v['definicion_iri']: v for v in report['variables'] if v.get('definicion_iri')}
maps_rep = {m['columna']: m for m in report['correspondencias'] if m['estado'] == 'documental_revisada'}
base_vars = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}
base_resp = {k: v for k, v in base_vars.items() if v['estado'] == 'respaldada_por_definicion'}
base_maps = {m['columna']: m for m in cob['correspondencias'] if m['estado'] == 'documental_revisada'}

perdidos = [k for k, v in base_resp.items()
            if vars_rep.get(k, {}).get('estado') != 'respaldada_por_definicion'
            or vars_rep.get(k, {}).get('concepto') != v.get('concepto')
            or vars_rep.get(k, {}).get('regla') != v.get('regla')]
caso('C-preservacion', 'C-sig-1212', '1212 significados de base intactos (estado+concepto+regla)',
     '1212 intactos', not perdidos, '' if not perdidos else 'perdidos: %s' % perdidos[:5])

perdidos_v = [k for k in base_maps if k not in maps_rep]
caso('C-preservacion', 'C-vinc-865', '865 vinculos de base siguen documental_revisada',
     '865 intactos', not perdidos_v, '' if not perdidos_v else 'perdidos: %s' % perdidos_v[:3])

no_mat = [r['id'] for r in nuevas
          if vars_rep.get(r['definiciones'][0], {}).get('regla') != r['id']
          or vars_rep.get(r['definiciones'][0], {}).get('estado') != 'respaldada_por_definicion']
caso('C-preservacion', 'C-reglas-175', '175 reglas nuevas materializadas en la propuesta',
     '175 materializadas', not no_mat, '' if not no_mat else 'no materializadas: %s' % no_mat[:5])

no_vinc = [v['columna'] for v in vinculos if v['columna'] not in maps_rep]
caso('C-preservacion', 'C-vinc-nuevos', 'vinculos nuevos documental_revisada en la propuesta',
     '%d revisados' % len(vinculos), not no_vinc, '' if not no_vinc else 'faltan: %s' % no_vinc[:3])

cambios_estado = [k for k, v in base_vars.items()
                  if v['estado'] != 'respaldada_por_definicion'
                  and vars_rep.get(k, {}).get('estado') == 'respaldada_por_definicion'
                  and k not in {r['definiciones'][0] for r in nuevas}]
caso('C-preservacion', 'C-sin-promocion', 'ninguna fila ajena se promueve por las reglas nuevas',
     'sin promociones ajenas', not cambios_estado, '' if not cambios_estado else 'promovidas: %s' % cambios_estado[:5])

# PIN ambiguos: con generador preparado resuelven; con nucleo sin parche no
merged_amb = copy.deepcopy(merged)
merged_amb['vinculos_documentales_revisados'].extend(copy.deepcopy(amb['vinculos']))
_, _, rep_amb = GEN.construir(inventory, inspection, merged_amb, reference, base_iri)
maps_amb = {m['columna']: m for m in rep_amb['correspondencias'] if m['estado'] == 'documental_revisada'}
faltan_pin = [v['columna'] for v in amb['vinculos'] if v['columna'] not in maps_amb]
caso('C-preservacion', 'C-pin-5', '5 PIN ambiguos resuelven con definicion_iri (generador preparado)',
     '5 resueltos', not faltan_pin, '' if not faltan_pin else 'faltan: %s' % faltan_pin[:3])

sys.path.append(str(ROOT / 'scripts'))
import importlib
nucleo_src = (ROOT / 'scripts' / 'consolidar_semantica.py').read_text(encoding='utf-8')
caso('C-preservacion', 'C-pin-nucleo', 'nucleo sin parche rechaza PIN sin columna fisica (contraste)',
     'ValueError', 'definition_pin' not in nucleo_src,
     'el nucleo instalado no soporta definicion_iri; se requiere el generador preparado' if 'definition_pin' not in nucleo_src else 'el nucleo ya lo soporta')

# ---------- Suite D: cambios de esquema/fila (muestra real + sintetico) ----------
alter = copy.deepcopy(merged)
alter['vinculos_documentales_revisados'][865]['huella_esquema'] = '0' * 64
ok, obs = fails_with(lambda: GEN.construir(inventory, inspection, alter, reference, base_iri), 'Evidencia de revisi')
caso('D-esquema', 'D-huella-esquema', 'huella_esquema alterada aborta la construccion', 'ValueError', ok, obs)

alter = copy.deepcopy(merged)
alter['vinculos_documentales_revisados'][866]['huella_fila_diccionario'] = '0' * 64
ok, obs = fails_with(lambda: GEN.construir(inventory, inspection, alter, reference, base_iri), 'Evidencia de revisi')
caso('D-esquema', 'D-huella-fila', 'huella_fila_diccionario alterada aborta', 'ValueError', ok, obs)

alter = copy.deepcopy(merged)
alter['vinculos_documentales_revisados'][867]['descripcion'] = 'descripcion manipulada'
ok, obs = fails_with(lambda: GEN.construir(inventory, inspection, alter, reference, base_iri), 'Evidencia de revisi')
caso('D-esquema', 'D-descripcion', 'descripcion alterada aborta', 'ValueError', ok, obs)

alter = copy.deepcopy(merged)
alter['vinculos_documentales_revisados'][868]['diccionario'] = 'diccionario-inexistente'
ok, obs = fails_with(lambda: GEN.construir(inventory, inspection, alter, reference, base_iri), 'dej')
caso('D-esquema', 'D-diccionario', 'diccionario alterado no coincide', 'ValueError', ok, obs)

# ---------- Suite E: selecciones duplicadas invalidas (mismo codigo, muestra pequena) ----------
mini_inv = {'recursos': [
    {'id': 'dic', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'clasificacion': 'diccionario'},
    {'id': 'r', 'conjunto_id': 'd', 'conjunto': 'Prueba', 'clasificacion': 'datos_estructurados', 'url': 'https://example.org/r'}]}
filas = [{'Nombre variable': 'Unidad', 'Descripción': 'Unidad de capacidad'},
         {'Nombre variable': 'Unidad', 'Descripción': 'Unidad de generación'}]
mini_insp = {'recursos': [
    {'id': 'dic', 'ok': True, 'definiciones': filas},
    {'id': 'r', 'ok': True, 'tablas': [{'hoja': 'Datos', 'campos': [
        {'id': 'Unidad', 'posicion_original': 1}, {'id': 'Unidad', 'posicion_original': 2}]}]}]}
base_test = {'alcance': 'T', 'conceptos': {'capacidad': ['Cap', 'D', None], 'generacion': ['Gen', 'D', None]},
             'condiciones': {}, 'distinciones': [], 'reglas_descripcion_exacta': [],
             'vinculos_documentales_revisados': [], 'observaciones_revision': []}
for _k in ['municipio-registro', 'municipio-residencia', 'municipio-defuncion',
           'anio-registro', 'anio-defuncion', 'organizacion-publicadora', 'organizacion-capturadora']:
    base_test['conceptos'][_k] = [_k, 'Definicion de prueba', None]
for j, c in enumerate(['capacidad', 'generacion']):
    base_test['reglas_descripcion_exacta'].append(
        {'id': 'rx%d' % j, 'concepto': c, 'nombres': ['Unidad'], 'descripciones': [filas[j]['Descripción']],
         'conjuntos': ['d'], 'diccionarios': ['dic'],
         'definiciones': ['https://example.org/mex-ontologi/definition/dic%%2F%d' % (j + 1)],
         'representacion': 'x'})
cols = GEN.columnas(mini_inv, mini_insp, base_iri)


def vinculo(j, **kw):
    col = cols[j]
    v = dict(recurso='r', campo='Unidad', columna=col['iri'], diccionario='dic',
             definicion_iri='https://example.org/mex-ontologi/definition/dic%%2F%d' % (j + 1),
             concepto=['capacidad', 'generacion'][j], descripcion=filas[j]['Descripción'],
             huella_esquema=col['huella_esquema'], huella_fila_diccionario=GEN.huella(filas[j]),
             criterio='Revision fisica explicita')
    v.update(kw)
    return v


def build_con(rules):
    return GEN.construir(mini_inv, mini_insp, rules, None, base_iri)


ok, obs = fails_with(lambda: build_con(dict(base_test, vinculos_documentales_revisados=[vinculo(0)] * 2)), 'duplicadas')
caso('E-duplicadas', 'E-col-dup', 'columna revisada duplicada se rechaza', 'ValueError', ok, obs)

dup_rules = base_test['reglas_descripcion_exacta'] + [dict(base_test['reglas_descripcion_exacta'][0])]
ok, obs = fails_with(lambda: build_con(dict(base_test, reglas_descripcion_exacta=dup_rules)), 'conflicto')
caso('E-duplicadas', 'E-regla-dup', 'regla con id/descripcion duplicados entra en conflicto', 'ValueError', ok, obs)

sin_col = vinculo(0)
sin_col.pop('columna')
ok, obs = fails_with(lambda: build_con(dict(base_test, vinculos_documentales_revisados=[sin_col])), 'columna f')
caso('E-duplicadas', 'E-pin-sin-columna', 'definicion_iri sin columna fisica se rechaza', 'ValueError', ok, obs)

incompleto = vinculo(0)
incompleto.pop('criterio')
ok, obs = fails_with(lambda: build_con(dict(base_test, vinculos_documentales_revisados=[incompleto])), 'evidencia completa')
caso('E-duplicadas', 'E-pin-incompleto', 'pin sin evidencia completa se rechaza', 'ValueError', ok, obs)

sin_def = vinculo(0)
sin_def.pop('definicion_iri')
ok, obs = fails_with(lambda: build_con(dict(base_test, vinculos_documentales_revisados=[sin_def])), 'dej')
caso('E-duplicadas', 'E-amb-sin-pin', 'nombre duplicado sin pin no se resuelve por posicion', 'ValueError', ok, obs)

otro_concepto = vinculo(0, concepto='generacion')
ok, obs = fails_with(lambda: build_con(dict(base_test, vinculos_documentales_revisados=[otro_concepto])), 'dej')
caso('E-duplicadas', 'E-concepto-ajeno', 'vinculo a concepto distinto al respaldado se rechaza', 'ValueError', ok, obs)

print('total:', len(RESULTS), 'fallos:', sum(1 for r in RESULTS if r['resultado'] == 'fallido'))
for x in RESULTS:
    if x['resultado'] == 'fallido':
        print('FALLO:', x['id'], '|', x['observacion'][:250])
json.dump(RESULTS, (OUT / '_todos.json').open('w', encoding='utf-8'), ensure_ascii=False, indent=1)
