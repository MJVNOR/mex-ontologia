"""Paso 8 lote-2: verifica 41 columnas adicionales y amplia entrega (vinculos intactos + nuevos)."""
import collections
import hashlib
import io
import json
import sys
from urllib.parse import unquote

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'
LOTE = 'propuestas/pendientes-muse-r4/lote-2/'
sys.path.insert(0, ROOT + 'scripts')
from consolidar_semantica import huella, interpretacion
from integrar_contenido import clave


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


def save(rel, obj):
    with io.open(ROOT + rel, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


asig = load(LOTE + 'asignacion.json')
adic = load(LOTE + 'asignacion-adicional.json')
assert len(adic['columnas']) == 41, len(adic['columnas'])
orig_iris = {c['columna'] for c in asig['columnas']}
adic_iris = [c['columna'] for c in adic['columnas']]
assert len(set(adic_iris)) == 41 and not (set(adic_iris) & orig_iris), 'traslape de IRIs'

entrega = load(LOTE + 'entrega.json')
snap_reglas = json.dumps(entrega['reglas'], sort_keys=True)
snap_conc = json.dumps(entrega['conceptos_nuevos'], sort_keys=True)
snap_sig = json.dumps(entrega['decisiones_significados'], sort_keys=True)
snap_dec = json.dumps(entrega['decisiones_columnas'], sort_keys=True)
snap_vinc = json.dumps(entrega['vinculos'], sort_keys=True)
rule_by_def = {}
for r in entrega['reglas']:
    for d in r['definiciones']:
        rule_by_def[d] = r

prop = load('propuestas/pendientes-muse-r4/integrador/semantica-propuesta.json')
merged_prop = {'reglas_descripcion_exacta': prop['reglas_descripcion_exacta'], 'conceptos': prop['conceptos']}
base_cov = load('propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json')
variables = {v['definicion_iri']: v for v in base_cov['variables'] if v.get('definicion_iri')}
names = collections.Counter((v['conjunto'], clave(v['variable'])) for v in variables.values())

inv = load('data/portal/inventario.json')
resources = {r['id']: r for r in inv['recursos']}
insp_cache = {}


def inspeccion(rid):
    if rid not in insp_cache:
        try:
            insp_cache[rid] = load('data/portal/inspecciones/%s.json' % rid)
        except OSError:
            insp_cache[rid] = None
    return insp_cache[rid]


print('=== verificacion fisica + interpretacion (semantica-propuesta) ===')
nuevas_dec, nuevos_vinc = [], []
for col in adic['columnas']:
    iri, rid, campo = col['columna'], col['recurso'], col['campo']
    dis = col['definiciones_por_nombre']
    insp = inspeccion(rid)
    if '/file-column/' in iri:
        tail = unquote(iri.split('/file-column/', 1)[1])
        parts = tail.split('/')
        assert len(parts) == 3 and parts[0] == rid, iri
        hoja, pos = parts[1], int(parts[2])
        tabla = next(t for t in insp['tablas'] if t['hoja'] == hoja)
        f = next(c for c in tabla['campos'] if c.get('posicion_original') == pos)
        ok_esc = (f['id'] == campo)
        unico = sum(clave(c['id']) == clave(campo) for c in tabla['campos']) == 1
        h_esc = huella(tabla)
        hoja_txt = 'hoja %s, posicion %d' % (hoja, pos)
    elif '/column/' in iri:
        r = resources[rid]
        ds = (r.get('datastore') or {})
        fields = [x for x in ds.get('campos', []) if not x['id'].startswith('_')] if ds.get('ok') else []
        ok_esc = any(x['id'] == campo for x in fields)
        unico = sum(clave(x['id']) == clave(campo) for x in fields) == 1
        h_esc = huella([{'nombre': x['id'], 'tipo': x.get('type')} for x in fields])
        hoja_txt = 'datastore'
        hoja, pos = '-', 0
    else:
        raise AssertionError('IRI desconocida: ' + iri)
    di = dis[0] if len(dis) == 1 else None
    v = variables.get(di) if di else None
    ok_def = bool(v) and clave(v['variable']) == clave(campo)
    h_fila = v['huella_fila_diccionario'] if v else None
    # recomputo huella fila
    idx = int(di.rsplit('%2F', 1)[1]) if di else None
    dinsp = inspeccion(v['diccionario']) if v else None
    rows = (dinsp or {}).get('definiciones', [])
    h_rec = huella(rows[idx - 1]) if idx and 1 <= idx <= len(rows) else None
    regla = rule_by_def.get(di)
    interp = None
    if v:
        interp = interpretacion(v['variable'], v['descripcion'], v['conjunto'], merged_prop,
                                v['diccionario'], v['definicion_iri'])
    dest_ok = bool(regla) and interp is not None and interp.get('estado') == 'respaldada_por_definicion' \
        and interp.get('regla') == regla['id'] and interp.get('concepto') == regla['concepto']
    uniq_ok = unico and names[(v['conjunto'], clave(v['variable']))] == 1 if v else False
    print('%s | %s | esc=%s unico=%s huellaF=%s regla=%s interp=%s uniq=%s' % (
        rid[:8], campo, ok_esc, unico, h_rec == h_fila,
        regla['id'] if regla else None,
        (interp.get('regla'), interp.get('estado')) if interp else None, uniq_ok))
    assert ok_esc and ok_def and h_rec == h_fila and dest_ok and uniq_ok, 'FALLO: ' + iri
    dep = ('dependencia explicita: regla propuesta %s (pendiente de auditoria); interpretacion comprobada '
           'contra integrador/semantica-propuesta.json.' % regla['id'])
    nuevas_dec.append({
        'columna': iri, 'recurso': rid, 'campo': campo, 'decision': 'proponer',
        'definicion_iri': di,
        'motivo': ('proponer: campo verificado en esquema capturado del recurso (%s, huella_esquema %s) '
                    'y fila de diccionario del mismo conjunto con descripcion literal (huella %s recomputada); %s'
                    % (hoja_txt, h_esc, h_fila, dep)),
        'evidencia': [
            'data/portal/inspecciones/%s.json (%s, campo %s; huella_esquema %s)' % (rid, hoja_txt, campo, h_esc),
            'data/semantica/cobertura.json (definicion %s; huella_fila_diccionario %s recomputada)' % (di, h_fila),
            'propuestas/pendientes-muse-r4/lote-2/entrega.json (regla %s; %s)' % (regla['id'], dep),
            'propuestas/pendientes-muse-r4/lote-2/asignacion-adicional.json (columna candidata_por_nombre)',
        ],
    })
    nuevos_vinc.append({
        'recurso': rid, 'campo': campo, 'columna': iri, 'diccionario': v['diccionario'],
        'concepto': regla['concepto'], 'descripcion': v['descripcion'],
        'huella_esquema': h_esc, 'huella_fila_diccionario': h_fila,
        'criterio': ('Revision explicita del campo en el esquema de este recurso y su fila de diccionario en el mismo '
                     'conjunto: nombre, contexto, descripcion y representacion verificados, huellas recomputadas. '
                     'Reutilizacion de regla propuesta %s y concepto %s para la misma definicion; %s Alcance de '
                     'interpretacion documental; no se validan valores ni se habilitan cruces.'
                     % (regla['id'], regla['concepto'], dep)),
    })

entrega['decisiones_columnas'].extend(nuevas_dec)
entrega['vinculos'].extend(nuevos_vinc)
assert json.dumps(entrega['reglas'], sort_keys=True) == snap_reglas
assert json.dumps(entrega['conceptos_nuevos'], sort_keys=True) == snap_conc
assert json.dumps(entrega['decisiones_significados'], sort_keys=True) == snap_sig
assert json.dumps(entrega['decisiones_columnas'][:667], sort_keys=True) == snap_dec
assert json.dumps(entrega['vinculos'][:667], sort_keys=True) == snap_vinc
save(LOTE + 'entrega.json', entrega)
print('decisiones:', len(entrega['decisiones_columnas']), 'vinculos:', len(entrega['vinculos']))

# pendientes.json y resultado.md
p = load(LOTE + 'pendientes.json')
p['columnas_pendientes'] = []
p['nota'] = ('708 columnas decididas (667 originales + 41 adicionales, todas proponer con evidencia verificada; '
             '0 pendientes). 21 de 28 significados propuestos con reglas r4-lote-2-001 a 021; 7 pendientes '
             '(P2 ambiguo x2, P8 doble, P13/P36/P39/P40 tipo-vs-pregunta). Reglas nuevas: 21. Conceptos nuevos: 16.')
save(LOTE + 'pendientes.json', p)

rd = io.open(ROOT + LOTE + 'resultado.md', encoding='utf-8').read()
rd = rd.replace('Columnas asignadas: 667.', 'Columnas asignadas: 667 + 41 adicionales = 708.')
rd = rd.replace('Decisiones: 667 proponer, 0 pendiente, 0 rechazar (sin cambios; vinculos intactos).',
                'Decisiones: 708 proponer, 0 pendiente, 0 rechazar.')
rd = rd.replace('Vinculos propuestos: 667.', 'Vinculos propuestos: 708 (667 intactos + 41 nuevos con dependencia explicita de su regla propuesta).')
rd += ('\n## Columnas adicionales (41)\n\nTodas proponer con dependencia explicita de su regla propuesta '
       '(pendiente de auditoria), interpretacion comprobada contra integrador/semantica-propuesta.json: '
       'Inspeccion y Vigilancia 2do Trim 2022 ACTIVIDAD x4 / MOTIVO x4 (4 hojas); Matriculas Estudiante x14; '
       'Planeacion TIC ID/P3/P4/P5/P9; Becas Convocatoria x5; Victimas DELITO/MODALIDAD; Mejora ID/P3/P4/P5/P10; '
       'Matriculas Semestre que cursa; Titulados No. Huellas de esquema y fila recomputadas en los 41 casos; '
       'nombres unicos; sin traslape con las 667 originales.\n')
io.open(ROOT + LOTE + 'resultado.md', 'w', encoding='utf-8').write(rd)

h = hashlib.sha256(io.open(ROOT + LOTE + 'entrega.json', 'rb').read()).hexdigest()
save(LOTE + 'listo.json', {'lote': 'lote-2', 'sha256_entrega': h,
    'cuentas': {'decisiones_columnas': 708, 'proponer': 708, 'pendiente_columna': 0, 'rechazar': 0,
                'vinculos': 708, 'decisiones_significados': 28, 'significados_proponer': 21,
                'significados_pendiente': 7, 'reglas_nuevas': 21, 'conceptos_nuevos': 16,
                'solicitudes_investigacion': 2}})
print('listo sha:', h)
