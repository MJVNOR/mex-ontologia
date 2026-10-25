"""Verificacion lote-2: evidencia concreta por columna (esquema + diccionario)."""
import hashlib
import io
import json
from urllib.parse import unquote

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'
LOTE = 'propuestas/pendientes-muse-r4/lote-2/'
FUENTES = 'propuestas/pendientes-muse-r4/fuentes/'


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


asig = load(LOTE + 'asignacion.json')
cob = load(FUENTES + 'data/semantica/cobertura.json')
sem = load(FUENTES + 'ontologia/semantica.json')
inv = load('data/portal/inventario.json')

cov_by_def = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}
resources = {r['id']: r for r in inv['recursos']}
revisados = {(v['recurso'], v['campo'], v.get('columna')) for v in sem['vinculos_documentales_revisados']}

insp_cache = {}


def inspeccion(rid):
    if rid not in insp_cache:
        try:
            insp_cache[rid] = load('data/portal/inspecciones/%s.json' % rid)
        except OSError:
            insp_cache[rid] = None
    return insp_cache[rid]


def clave(t):
    import unicodedata
    t = unicodedata.normalize('NFKD', str(t or ''))
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return ' '.join(t.lower().split())


results = []
for col in asig['columnas']:
    iri = col['columna']
    rid = col['recurso']
    campo = col['campo']
    dis = col['definiciones_por_nombre']
    rec = {'columna': iri, 'recurso': rid, 'campo': campo, 'definiciones': dis}
    insp = inspeccion(rid)
    if insp is None:
        rec.update(ok_esquema=False, detalle='sin inspeccion local del recurso')
        results.append(rec)
        continue
    if '/file-column/' in iri:
        tail = unquote(iri.split('/file-column/', 1)[1])
        parts = tail.split('/')
        # parts: [recurso, hoja, posicion]
        if len(parts) == 3 and parts[0] == rid:
            hoja, pos = parts[1], parts[2]
            tablas = [t for t in insp.get('tablas', []) if t.get('hoja') == hoja]
            if not tablas:
                rec.update(ok_esquema=False, detalle='hoja no encontrada: %s' % hoja)
            else:
                tabla = tablas[0]
                campos = tabla.get('campos', [])
                try:
                    idx = int(pos)
                    f = next((c for c in campos if c.get('posicion_original') == idx), None)
                except ValueError:
                    f = None
                if f is None:
                    rec.update(ok_esquema=False, detalle='posicion fuera de rango: %s' % pos)
                else:
                    rec['campo_en_posicion'] = f.get('id')
                    rec['nombre_unico'] = sum(clave(c.get('id')) == clave(campo) for c in campos) == 1
                    rec['n_campos'] = len(campos)
                    rec['huella_esquema'] = huella(tabla)
                    rec['ok_esquema'] = (f.get('id') == campo)
                    rec['detalle'] = 'campo coincide en posicion' if rec['ok_esquema'] else \
                        'mismatch: esquema=%r' % f.get('id')
                    rec['evidencia_esquema'] = 'data/portal/inspecciones/%s.json#tablas/%s' % (rid, hoja)
        else:
            rec.update(ok_esquema=False, detalle='IRI file-column no parseable')
    elif '/column/' in iri:
        tail = unquote(iri.split('/column/', 1)[1])
        parts = tail.split('/')
        r = resources.get(rid, {})
        ds = (r.get('datastore') or {})
        fields = [f for f in ds.get('campos', []) if not f['id'].startswith('_')] if ds.get('ok') else []
        rec['n_campos'] = len(fields)
        match = [f for f in fields if f['id'] == campo]
        rec['nombre_unico'] = sum(clave(f['id']) == clave(campo) for f in fields) == 1
        rec['huella_esquema'] = huella([{'nombre': f['id'], 'tipo': f.get('type')} for f in fields]) if fields else None
        rec['ok_esquema'] = len(match) == 1
        rec['detalle'] = 'campo datastore unico' if rec['ok_esquema'] else 'datastore: %d campos, %d matches' % (len(fields), len(match))
        rec['evidencia_esquema'] = 'data/portal/inventario.json#recursos/%s/datastore' % rid
    else:
        rec.update(ok_esquema=False, detalle='IRI sin patron conocido')
    # definicion
    if len(dis) == 1 and dis[0] in cov_by_def:
        v = cov_by_def[dis[0]]
        rec['definicion_ok'] = (clave(v['variable']) == clave(campo))
        rec['variable_dic'] = v['variable']
        rec['descripcion'] = v['descripcion']
        rec['estado_def'] = v['estado']
        rec['concepto'] = v.get('concepto')
        rec['regla'] = v.get('regla')
        rec['representacion'] = v.get('representacion')
        rec['huella_fila'] = v.get('huella_fila_diccionario')
        rec['diccionario'] = v.get('diccionario')
        # recomputar huella fila desde inspeccion del diccionario
        try:
            idxd = int(dis[0].rsplit('%2F', 1)[1])
        except ValueError:
            idxd = None
        rec['huella_recomputada'] = None
        if idxd:
            dinsp = inspeccion(v['diccionario'])
            rows = (dinsp or {}).get('definiciones', [])
            if 1 <= idxd <= len(rows):
                rec['huella_recomputada'] = huella(rows[idxd - 1])
                rec['huella_coincide'] = (rec['huella_recomputada'] == v.get('huella_fila_diccionario'))
            else:
                rec['huella_coincide'] = False
        # conflicto con revision existente?
        rec['ya_revisado'] = (rid, campo, iri) in revisados or (rid, campo, None) in revisados
    else:
        rec['definicion_ok'] = False
        rec['detalle_def'] = 'defs: %d, en cobertura: %s' % (len(dis), all(d in cov_by_def for d in dis))
    results.append(rec)

with io.open(ROOT + LOTE + '_verificacion.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

# resumen ascii-safe
from collections import Counter
print('total:', len(results))
print(Counter((r.get('ok_esquema'), r.get('definicion_ok')) for r in results))
print('huella_coincide False:', sum(1 for r in results if r.get('huella_coincide') is False))
print('ya_revisado:', sum(1 for r in results if r.get('ya_revisado')))
print('nombre_unico False:', sum(1 for r in results if r.get('nombre_unico') is False))
for r in results:
    if not r.get('ok_esquema') or not r.get('definicion_ok') or r.get('huella_coincide') is False or r.get('ya_revisado') or r.get('nombre_unico') is False:
        print('PROBLEMA:', r['recurso'], '|', r['campo'], '|', r['columna'][-40:], '|',
              r.get('detalle'), '| def_ok=', r.get('definicion_ok'), '| huella=', r.get('huella_coincide'),
              '| unico=', r.get('nombre_unico'), '| yarev=', r.get('ya_revisado'),
              '| var=', r.get('variable_dic'))
