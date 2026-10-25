"""Paso 6 lote-2: huellas de las 28 desde cobertura + recomputo, precedentes representacion."""
import hashlib
import io
import json

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


cob = load('propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json')
cov = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}
asig = load('propuestas/pendientes-muse-r4/lote-2/asignacion.json')
pend = load('propuestas/pendientes-muse-r4/lote-2/_pend28.json')
sem = load('propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json')
rules = {r['id']: r for r in sem['reglas_descripcion_exacta']}
# precedentes de representacion
for rid in ['r3a9-085', 'r3a10-0252', 'r3a9-061', 'r3a8-068', 'r3a10-0114', 'r3a3-precio-medio-rural-cultivo-1']:
    r = rules.get(rid, {})
    print(rid, '->', r.get('representacion'), '|', r.get('concepto'))
# huellas: cobertura vs recomputo
insp_cache = {}


def inspeccion(rid):
    if rid not in insp_cache:
        insp_cache[rid] = load('data/portal/inspecciones/%s.json' % rid)
    return insp_cache[rid]


print('--- huellas 28:')
for s in pend:
    di = s['definicion_iri']
    v = cov.get(di)
    hc = v['huella_fila_diccionario'] if v else None
    dinsp = inspeccion(s['diccionario'])
    rows = dinsp.get('definiciones', [])
    hr = huella(rows[s['indice'] - 1]) if 1 <= s['indice'] <= len(rows) else None
    print('OK ' if hc == hr else 'MISMATCH ', s['variable'], '|', s['diccionario'], '|', hc)
