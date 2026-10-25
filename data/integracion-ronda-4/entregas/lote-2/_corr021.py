"""Paso 9 lote-2: condicion auditoria-a sobre r4-lote-2-021 (concepto propio)."""
import hashlib
import io
import json
import sys

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'
LOTE = 'propuestas/pendientes-muse-r4/lote-2/'
sys.path.insert(0, ROOT + 'scripts')

EST = 'https://example.org/mex-ontologi/definition/dc87a5be-8ef7-4e90-af72-ea5053423fad%2F1'
NUEVO = 'numero-estudiante-matriculado'


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


def save(rel, obj):
    with io.open(ROOT + rel, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


entrega = load(LOTE + 'entrega.json')
snap_otras = json.dumps([r for r in entrega['reglas'] if r['id'] != 'r4-lote-2-021'], sort_keys=True)

# 1. concepto nuevo propio
assert NUEVO not in entrega['conceptos_nuevos']
entrega['conceptos_nuevos'][NUEVO] = [
    'Numero de estudiante matriculado',
    'Numero consecutivo que significa estudiante matriculado segun el diccionario de Matriculas (variable Estudiante); '
    'identifica el registro del estudiante en el archivo. Orden interno, sin identidad entre archivos ni con ordinales '
    'genericos de otras entradas.',
    None,
]

# 2. regla 021: solo cambia concepto/limite/criterio; ID y fuentes intactos
n = 0
for r in entrega['reglas']:
    if r['id'] == 'r4-lote-2-021':
        assert r['definiciones'] == [EST] and r['concepto'] == 'numero-consecutivo-registro'
        r['concepto'] = NUEVO
        r['limites'] = ['Consecutivo que significa estudiante matriculado (ejemplo 1); identifica el registro del '
                        'estudiante en Matriculas. Concepto propio, distinto del ordinal generico de entradas; '
                        'orden interno, sin identidad externa.']
        r['criterio'] = (r['criterio'].replace(
            'Sentido literal limitado a lo declarado.',
            'Sentido literal limitado a lo declarado como estudiante matriculado; concepto propio especifico, '
            'distinto del ordinal generico numero-consecutivo-registro (condicion de auditoria-a).'))
        n += 1
assert n == 1
assert json.dumps([r for r in entrega['reglas'] if r['id'] != 'r4-lote-2-021'], sort_keys=True) == snap_otras

# 3-4. vinculos y decisiones de las 14 columnas Estudiante (todas adicionales)
nv = nd = 0
for v in entrega['vinculos']:
    d = next(x for x in entrega['decisiones_columnas'] if x['columna'] == v['columna'])
    if d.get('definicion_iri') == EST:
        assert v['concepto'] == 'numero-consecutivo-registro' and v['diccionario'] == 'dc87a5be-8ef7-4e90-af72-ea5053423fad'
        v['concepto'] = NUEVO
        v['criterio'] = v['criterio'].replace(
            'Reutilizacion de regla propuesta r4-lote-2-021 y concepto numero-consecutivo-registro',
            'Reutilizacion de regla propuesta r4-lote-2-021 y concepto propio numero-estudiante-matriculado '
            '(distinto del ordinal generico; condicion de auditoria-a)')
        nv += 1
for d in entrega['decisiones_columnas']:
    if d.get('definicion_iri') == EST:
        assert 'regla propuesta r4-lote-2-021' in d['motivo']
        d['motivo'] = d['motivo'].replace(
            'dependencia explicita: regla propuesta r4-lote-2-021 (pendiente de auditoria)',
            'dependencia explicita: regla propuesta r4-lote-2-021 con concepto propio numero-estudiante-matriculado '
            '(distinto del ordinal generico; condicion de auditoria-a)')
        nd += 1
print('vinculos actualizados:', nv, 'decisiones actualizadas:', nd)
assert nv == 14 and nd == 14

# 5. decision de significado
for d in entrega['decisiones_significados']:
    if d['definicion_iri'] == EST:
        assert d['decision'] == 'proponer'
        d['motivo'] = ('proponer con regla nueva r4-lote-2-021 (concepto propio numero-estudiante-matriculado, '
                       'condicion de auditoria-a): Numero consecutivo, que significa estudiante matriculado')

save(LOTE + 'entrega.json', entrega)

p = load(LOTE + 'pendientes.json')
save(LOTE + 'pendientes.json', p)

rd = io.open(ROOT + LOTE + 'resultado.md', encoding='utf-8').read()
rd = rd.replace('Conceptos nuevos (16).', 'Conceptos nuevos (17).')
rd = rd.replace('numero-consecutivo-registro.',
                'numero-consecutivo-registro.\n\n## Correccion auditoria-a (r4-lote-2-021)\n\nConcepto propio '
                'numero-estudiante-matriculado, distinto del ordinal generico, aplicado a la regla r4-lote-2-021 '
                '(ID y fuentes intactos), a sus 14 vinculos (columnas Estudiante adicionales) y a sus decisiones/motivos. '
                'Las demas reglas no cambian.')
io.open(ROOT + LOTE + 'resultado.md', 'w', encoding='utf-8').write(rd)

h = hashlib.sha256(io.open(ROOT + LOTE + 'entrega.json', 'rb').read()).hexdigest()
save(LOTE + 'listo.json', {'lote': 'lote-2', 'sha256_entrega': h,
    'cuentas': {'decisiones_columnas': 708, 'proponer': 708, 'pendiente_columna': 0, 'rechazar': 0,
                'vinculos': 708, 'decisiones_significados': 28, 'significados_proponer': 21,
                'significados_pendiente': 7, 'reglas_nuevas': 21, 'conceptos_nuevos': 17,
                'solicitudes_investigacion': 2}})
print('listo sha:', h)

# verificacion base + entrega actual (sin semantica-propuesta antigua, sin escribir control)
sys.path.insert(0, ROOT + 'propuestas/pendientes-muse-r4/integrador')
import comprobar
r = comprobar.check('lote-2')
print('valido:', r['valido'], '| col:', r['columnas'], 'vinc:', r['vinculos'], 'reglas:', r['reglas'])
for e in r['errores'][:10]:
    print(' -', e[:200])
