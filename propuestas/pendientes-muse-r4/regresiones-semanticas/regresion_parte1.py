"""Regresiones adversariales r4: alcance exacto de 175 reglas, preservacion de base,
PIN ambiguos, cambios de esquema/fila y selecciones duplicadas invalidas.

Usa codigo real (scripts/ y generador preparado en integrador/codigo/scripts)
y fuentes locales. No instala nada.
"""
import copy
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas' / 'pendientes-muse-r4'
PREP = STAGE / 'integrador' / 'codigo' / 'scripts'
sys.path.insert(0, str(PREP))
sys.path.append(str(ROOT / 'scripts'))

from integrar_contenido import clave  # noqa: E402
import consolidar_semantica as GEN  # noqa: E402
assert 'integrador' in GEN.__file__, GEN.__file__  # generador preparado, no el nucleo

OUT = STAGE / 'regresiones-semanticas'
RESULTS = []


def caso(suite, cid, descripcion, esperado, ok, observacion=''):
    RESULTS.append({'suite': suite, 'id': cid, 'descripcion': descripcion,
                    'esperado': esperado, 'resultado': 'aprobado' if ok else 'fallido',
                    'observacion': observacion})
    return ok


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


# ---------- entradas ----------
base = json.loads((ROOT / 'ontologia' / 'semantica.json').read_text(encoding='utf-8'))
cob = json.loads((ROOT / 'data' / 'semantica' / 'cobertura.json').read_text(encoding='utf-8'))
inventory = json.loads((ROOT / 'data' / 'portal' / 'inventario.json').read_text(encoding='utf-8'))
inspection = json.loads((ROOT / 'data' / 'portal' / 'contenido-inspeccion.json').read_text(encoding='utf-8'))
ref_path = ROOT / 'data' / 'portal' / 'lote-cruces' / 'catalogo-municipal-portal.json'
reference = json.loads(ref_path.read_text(encoding='utf-8')) if ref_path.exists() else None
import tomllib
base_iri = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']

lotes = {}
nuevas, vinculos, conceptos = [], [], {}
for i in range(1, 7):
    d = json.loads((STAGE / f'lote-{i}' / 'entrega.json').read_text(encoding='utf-8'))
    lotes[f'lote-{i}'] = d
    nuevas.extend(d.get('reglas', []))
    vinculos.extend(d.get('vinculos', []))
    for k, v in d.get('conceptos_nuevos', {}).items():
        if k in conceptos:
            assert conceptos[k] == v, 'concepto incompatible entre lotes: ' + k
        conceptos[k] = v
amb = json.loads((STAGE / 'ambiguedades' / 'entrega.json').read_text(encoding='utf-8'))
assert len(nuevas) == 172, len(nuevas)

merged = copy.deepcopy(base)
for k, v in conceptos.items():
    assert k not in merged['conceptos'] or merged['conceptos'][k] == v
    merged['conceptos'][k] = v
merged['reglas_descripcion_exacta'].extend(copy.deepcopy(nuevas))
merged['vinculos_documentales_revisados'].extend(copy.deepcopy(vinculos))

variables = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}
regla_de = {r['id']: r for r in nuevas}


def donante_distinto(r, campo):
    for c in nuevas:
        if campo == 'clave-nombre' and clave(c['nombres'][0]) != clave(r['nombres'][0]):
            return c['nombres'][0] + '/zz'
        if campo == 'clave-descripcion' and clave(c['descripciones'][0]) != clave(r['descripciones'][0]):
            return c['descripciones'][0] + ' zz'
        if campo in ('conjuntos', 'diccionarios', 'definiciones') and c[campo][0] != r[campo][0]:
            return c[campo][0]
    return 'zz-inexistente-' + campo

# ---------- Suite A: alcance exacto ----------
for r in nuevas:
    rid = r['id']
    v = variables[r['definiciones'][0]]
    try:
        m = GEN.interpretacion(v['variable'], v['descripcion'], v['conjunto'],
                               merged, v['diccionario'], v['definicion_iri'])
        ok = m.get('regla') == rid and m.get('estado') == 'respaldada_por_definicion'
        obs = '' if ok else 'obtuvo %s/%s' % (m.get('regla'), m.get('estado'))
    except ValueError as e:
        ok, obs = False, 'excepcion: ' + str(e)[:200]
    caso('A-alcance', f'A-pos-{rid}', f'la regla aplica a su fila exacta', rid, ok, obs)

    muts = [
        ('conjunto', v['variable'], v['descripcion'], donante_distinto(r, 'conjuntos'), v['diccionario'], v['definicion_iri']),
        ('diccionario', v['variable'], v['descripcion'], v['conjunto'], donante_distinto(r, 'diccionarios'), v['definicion_iri']),
        ('definicion', v['variable'], v['descripcion'], v['conjunto'], v['diccionario'], donante_distinto(r, 'definiciones')),
        ('nombre', donante_distinto(r, 'clave-nombre'), v['descripcion'], v['conjunto'], v['diccionario'], v['definicion_iri']),
        ('descripcion', v['variable'], donante_distinto(r, 'clave-descripcion'), v['conjunto'], v['diccionario'], v['definicion_iri']),
    ]
    for axis, nm, ds, cj, dc, df in muts:
        try:
            m = GEN.interpretacion(nm, ds, cj, merged, dc, df)
            ok = m.get('regla') != rid
            obs = '' if ok else 'ALCANZA fila distinta por %s' % axis
            if not ok:
                obs += ' regla=%s' % m.get('regla')
        except ValueError as e:
            # conflicto: verificar si esta regla esta entre las coincidentes
            msg = str(e)
            ok = rid not in msg
            obs = ('conflicto sin esta regla' if ok else 'CONFLICTO INCLUYE LA REGLA') + ': ' + msg[:200]
        caso('A-alcance', f'A-neg-{axis}-{rid}', f'no alcanza otro {axis} distinto', 'sin coincidencia', ok, obs)

# ---------- Suite B: normalizacion intencional vs cambio de sentido ----------
for r in nuevas:
    rid = r['id']
    v = variables[r['definiciones'][0]]
    nm = strip_accents(v['variable']).upper()
    ds = strip_accents(v['descripcion']).upper()
    if clave(nm) == clave(v['variable']) and (not v['descripcion'] or clave(ds) == clave(v['descripcion'])):
        try:
            m = GEN.interpretacion(nm, ds or v['descripcion'], v['conjunto'], merged, v['diccionario'], v['definicion_iri'])
            ok = m.get('regla') == rid
            obs = '' if ok else 'obtuvo %s' % m.get('regla')
        except ValueError as e:
            ok, obs = False, 'excepcion: ' + str(e)[:200]
        caso('B-normalizacion', f'B-norm-{rid}', 'mayusculas/sin acentos conservan la regla', rid, ok, obs)

# pares confundibles: mismo nombre normalizado, distinta descripcion
por_nombre, por_desc = {}, {}
for r in nuevas:
    por_nombre.setdefault(clave(r['nombres'][0]), []).append(r)
    por_desc.setdefault(clave(r['descripciones'][0]), []).append(r)
for k, grupo in list(por_nombre.items()) + list(por_desc.items()):
    if len(grupo) < 2:
        continue
    for r in grupo:
        v = variables[r['definiciones'][0]]
        try:
            m = GEN.interpretacion(v['variable'], v['descripcion'], v['conjunto'],
                                   merged, v['diccionario'], v['definicion_iri'])
            ok = m.get('regla') == r['id']
            obs = '' if ok else 'cruce de sentido: obtuvo %s' % m.get('regla')
        except ValueError as e:
            ok, obs = False, 'conflicto de sentido: ' + str(e)[:200]
        caso('B-normalizacion', 'B-disc-%s' % r['id'],
             'discrimina sentidos con nombre/descripcion compartidos', r['id'], ok, obs)

print('suites A/B listas:', len(RESULTS), 'fallos:', sum(1 for r in RESULTS if r['resultado'] == 'fallido'))
json.dump(RESULTS, (OUT / '_parte1.json').open('w', encoding='utf-8'), ensure_ascii=False, indent=1)
