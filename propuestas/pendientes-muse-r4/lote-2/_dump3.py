"""Paso 4 lote-2: vuelca filas completas de diccionario para las 28 pendientes."""
import io
import json

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'
LOTE = 'propuestas/pendientes-muse-r4/lote-2/'


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


asig = load(LOTE + 'asignacion.json')
pend = asig['variables_pendientes']
print('pendientes:', len(pend))
insp_cache = {}


def inspeccion(rid):
    if rid not in insp_cache:
        try:
            insp_cache[rid] = load('data/portal/inspecciones/%s.json' % rid)
        except OSError:
            insp_cache[rid] = None
    return insp_cache[rid]


out = []
for s in pend:
    di = s['definicion_iri']
    idx = int(di.rsplit('%2F', 1)[1])
    dinsp = inspeccion(s['diccionario'])
    rows = (dinsp or {}).get('definiciones', [])
    row = rows[idx - 1] if 1 <= idx <= len(rows) else None
    out.append({'conjunto': s['conjunto'], 'titulo_conjunto': s['titulo_conjunto'],
                'diccionario': s['diccionario'], 'definicion_iri': di, 'indice': idx,
                'variable': s['variable'], 'descripcion': s['descripcion'],
                'motivo': s['motivo'], 'fila_completa': row,
                'n_filas_diccionario': len(rows)})

with io.open(ROOT + LOTE + '_pend28.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
print('volcado ok')
