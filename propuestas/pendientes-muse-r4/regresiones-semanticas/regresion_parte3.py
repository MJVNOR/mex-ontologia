"""Parte 3: suite G — las 3 reglas retiradas de lote-4 NO materializan."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas' / 'pendientes-muse-r4'
OUT = STAGE / 'regresiones-semanticas'

RESULTS = json.loads((OUT / '_todos.json').read_text(encoding='utf-8'))


def caso(suite, cid, descripcion, esperado, ok, observacion=''):
    RESULTS.append({'suite': suite, 'id': cid, 'descripcion': descripcion,
                    'esperado': esperado, 'resultado': 'aprobado' if ok else 'fallido',
                    'observacion': observacion})


RETIRADAS = {
    'r4-lote-4-025': 'https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F36',
    'r4-lote-4-026': 'https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F39',
    'r4-lote-4-027': 'https://example.org/mex-ontologi/definition/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2F40',
}
COLS_DEP = {
    'r4-lote-4-025': 'https://example.org/mex-ontologi/file-column/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2FHoja1%2F36',
    'r4-lote-4-026': 'https://example.org/mex-ontologi/file-column/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2FHoja1%2F39',
    'r4-lote-4-027': 'https://example.org/mex-ontologi/file-column/a4e8bee0-5493-4dec-bbce-0ba1e2fd4c2d%2FHoja1%2F40',
}

rep = json.loads((OUT / '_report.json').read_text(encoding='utf-8'))
vars_rep = {v['definicion_iri']: v for v in rep['variables'] if v.get('definicion_iri')}
col_estado = {}
for m in rep['correspondencias']:
    col_estado.setdefault(m['columna'], set()).add(m['estado'])

for rid, defi in RETIRADAS.items():
    v = vars_rep.get(defi, {})
    ok = v.get('estado') != 'respaldada_por_definicion' and v.get('regla') != rid
    caso('G-retiradas', f'G-def-{rid}',
         'definicion retirada no queda respaldada por ninguna regla',
         'no respaldada', ok, 'estado=%s regla=%s' % (v.get('estado'), v.get('regla')))
    est = col_estado.get(COLS_DEP[rid], set())
    ok = 'documental_revisada' not in est
    caso('G-retiradas', f'G-col-{rid}',
         'columna dependiente no queda como revisada',
         'no revisada', ok, 'estados=%s' % sorted(est))

# control: 4a columna pendiente de lote-4 (observacion vigente, ajena al retiro)
egresos = 'https://example.org/mex-ontologi/file-column/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2FEgresos%20Hospitalarios%202018-2022%2F15'
est = col_estado.get(egresos, set())
caso('G-retiradas', 'G-col-control',
     'columna pendiente por observacion vigente tampoco queda revisada',
     'no revisada', 'documental_revisada' not in est, 'estados=%s' % sorted(est))

print('suite G lista. total:', len(RESULTS),
      'fallos:', sum(1 for r in RESULTS if r['resultado'] == 'fallido'))
for x in RESULTS:
    if x['resultado'] == 'fallido' and x['suite'] == 'G-retiradas':
        print('FALLO:', x['id'], '|', x['observacion'][:250])
json.dump(RESULTS, (OUT / '_todos.json').open('w', encoding='utf-8'), ensure_ascii=False, indent=1)
