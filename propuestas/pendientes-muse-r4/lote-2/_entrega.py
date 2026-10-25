"""Paso 3 lote-2: construye entrega.json, pendientes.json, resultado.md, listo.json."""
import hashlib
import io
import json

ROOT = 'C:/Users/marti/Documents/MEX-Ontologi/'
LOTE = 'propuestas/pendientes-muse-r4/lote-2/'


def load(rel):
    with io.open(ROOT + rel, encoding='utf-8') as f:
        return json.load(f)


def save(rel, obj):
    with io.open(ROOT + rel, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


asig = load(LOTE + 'asignacion.json')
ver = {v['columna']: v for v in load(LOTE + '_verificacion.json')}
assert len(asig['columnas']) == 667 and len(ver) == 667

decisiones_columnas = []
vinculos = []
for col in asig['columnas']:
    v = ver[col['columna']]
    assert v.get('ok_esquema') and v.get('definicion_ok') and v.get('huella_coincide'), col['columna']
    ev = [
        'data/portal/inspecciones/%s.json (campo %s verificado en esquema; huella_esquema %s)'
        % (v['recurso'], v['campo'], v['huella_esquema']),
        'data/semantica/cobertura.json (definicion %s; huella_fila_diccionario %s recomputada desde inspeccion del diccionario %s)'
        % (col['definiciones_por_nombre'][0], v['huella_fila'], v['diccionario']),
        'ontologia/semantica.json (regla %s; concepto %s; reutilizacion exacta)' % (v['regla'], v['concepto']),
        'propuestas/pendientes-muse-r4/lote-2/asignacion.json (columna candidata_por_nombre)',
    ]
    motivo = ('proponer: campo verificado en esquema capturado del recurso y fila de diccionario '
              'del mismo conjunto con descripcion literal; reutilizacion exacta de regla %s y concepto %s; '
              'huellas recomputadas coinciden; sin inferir unidades, moneda, vigencia ni cruces.'
              % (v['regla'], v['concepto']))
    decisiones_columnas.append({
        'columna': col['columna'],
        'recurso': col['recurso'],
        'campo': col['campo'],
        'decision': 'proponer',
        'definicion_iri': col['definiciones_por_nombre'][0],
        'motivo': motivo,
        'evidencia': ev,
    })
    vinculos.append({
        'recurso': col['recurso'],
        'campo': col['campo'],
        'columna': col['columna'],
        'diccionario': v['diccionario'],
        'concepto': v['concepto'],
        'descripcion': v['descripcion'],
        'huella_esquema': v['huella_esquema'],
        'huella_fila_diccionario': v['huella_fila'],
        'criterio': ('Revision explicita del campo en el esquema de este recurso y su fila de diccionario '
                     'en el mismo conjunto: nombre, contexto, descripcion y representacion verificados, '
                     'huellas recomputadas desde fuentes locales. Reutilizacion exacta de regla %s y concepto %s '
                     'para la misma definicion. Alcance de interpretacion documental; no se validan valores, '
                     'no se confirma pertenencia a catalogos, no se habilitan cruces.' % (v['regla'], v['concepto'])),
    })

# 28 significados pendientes: fuera del nucleo, sin regla revisada
decisiones_significados = []
for s in asig['variables_pendientes']:
    decisiones_significados.append({
        'definicion_iri': s['definicion_iri'],
        'decision': 'pendiente',
        'motivo': ('fuera_del_nucleo_actual (%s): la descripcion %r no basta para fijar concepto compartido '
                   'sin regla revisada; no se aprueba por nombre ni por clasificador.'
                   % (s['motivo'], s['descripcion'])),
        'evidencia': [
            'data/semantica/cobertura.json (variable %s del diccionario %s, conjunto %s: estado fuera_del_nucleo_actual)'
            % (s['variable'], s['diccionario'], s['conjunto']),
            'propuestas/pendientes-muse-r4/lote-2/asignacion.json (variables_pendientes)',
        ],
    })

# solicitudes agrupadas por diccionario
from collections import defaultdict
grupos = defaultdict(list)
for s in asig['variables_pendientes']:
    grupos[(s['conjunto'], s['titulo_conjunto'], s['diccionario'])].append(s)
solicitudes = []
for (conj, titulo, dicc), ss in sorted(grupos.items()):
    solicitudes.append({
        'conjunto': conj,
        'titulo_conjunto': titulo,
        'diccionario': dicc,
        'definiciones_iris': [s['definicion_iri'] for s in ss],
        'variables': [s['variable'] for s in ss],
        'documento_requerido': ('Diccionario publicado del conjunto %s y muestra de valores por variable; '
                                'sin ello no se fija concepto ni regla.' % titulo),
        'fuente_probable': 'Portal del conjunto %s (mismo publicador del diccionario %s).' % (titulo, dicc),
    })

entrega = {
    'lote': 'lote-2',
    'decisiones_columnas': decisiones_columnas,
    'vinculos': vinculos,
    'decisiones_significados': decisiones_significados,
    'reglas': [],
    'conceptos_nuevos': {},
    'solicitudes_investigacion': solicitudes,
}
save(LOTE + 'entrega.json', entrega)

pendientes = {
    'lote': 'lote-2',
    'columnas_pendientes': [],
    'significados_pendientes': [
        {'definicion_iri': s['definicion_iri'], 'variable': s['variable'], 'conjunto': s['conjunto'],
         'diccionario': s['diccionario'], 'descripcion': s['descripcion'],
         'evidencia_faltante': 'Regla revisada y documento/muestra que respalde el significado; la descripcion actual no basta.'}
        for s in asig['variables_pendientes']
    ],
    'nota': ('Las 667 columnas asignadas quedan decididas (proponer) con evidencia verificada; '
             'no hay columnas pendientes. Reglas nuevas: 0. Conceptos nuevos: 0.'),
}
save(LOTE + 'pendientes.json', pendientes)

# resultado.md (ascii-safe: todo el contenido es ascii)
lineas = []
lineas.append('# Resultado lote-2 (ronda 4)')
lineas.append('')
lineas.append('Columnas asignadas: 667. Decisiones: 667 proponer, 0 pendiente, 0 rechazar.')
lineas.append('Significados asignados: 28. Decisiones: 0 proponer, 28 pendiente.')
lineas.append('Vinculos propuestos: 667. Reglas nuevas: 0. Conceptos nuevos: 0.')
lineas.append('Solicitudes de investigacion: %d (agrupadas por diccionario).' % len(solicitudes))
lineas.append('')
lineas.append('## Verificacion por columna (todas)')
lineas.append('')
lineas.append('Para cada una de las 667 columnas se verifico:')
lineas.append('')
lineas.append('- El campo existe con el mismo nombre en la posicion/hoja indicada del esquema capturado en data/portal/inspecciones/<recurso>.json; huella_esquema recomputada con la misma funcion huella() de scripts/consolidar_semantica.py.')
lineas.append('- La definicion candidata es unica (una sola definicion_por_nombre) y su variable coincide con el campo por normalizacion de clave; nombre unico en el esquema.')
lineas.append('- La huella_fila_diccionario de cobertura se recomputo desde la fila del diccionario en data/portal/inspecciones/<diccionario>.json y coincide en los 667 casos.')
lineas.append('- Ninguna columna estaba ya revisada en ontologia/semantica.json.')
lineas.append('')
lineas.append('No se aprobo por nombre ni por definicion respaldada: cada vinculo fija IRI fisica, huella de esquema y huella de fila propios. Se reutilizan exactamente 92 reglas vigentes (r3a3-*, r3a8-*, r3a9-*, r3a10-*) y sus conceptos, con sus limites (moneda no declarada, medida no declarada, metodologia anterior, sin vigencia ni cruces).')
lineas.append('')
lineas.append('## Grupos revisados')
lineas.append('')
from collections import Counter
c1 = Counter((v['recurso'], ) for v in ver.values())
lineas.append('- Agricultura Sonora (conjunto 3e17a7e8, diccionario 94215f51): 359 columnas en 25 recursos anuales (campos CIERREYAVAN, CDDR, NDDR, CMUN, NMUN, CVECUL/CVEVAR, CULTIVO/DESVAR, SUPSEM, SUPCOSE, SUPSINI, PRODTON, RENDMNTO, PMR, VALPROD, CVMES, NMES segun recurso).')
lineas.append('- Matriculas (conjunto e5aad52d, diccionario dc87a5be): 127 columnas en 14 recursos periodicos (Sede, Nivel, Modalidad, Campo de Formacion, Grado, Sexo, Estado de Nacimiento, Estado civil, Edad).')
lineas.append('- Programa anual de adquisiciones (conjunto 665d76b2, diccionario a2b6100b): 70 columnas en 5 recursos (cantidad, iva, enero-diciembre).')
lineas.append('- Beneficiarios de becas (diccionario 2bdb18b1): 30 columnas en 5 recursos (CicloEscolar, Programa, Nivel, Clave, Importe, Genero).')
lineas.append('- Estudiantes egresados (diccionario 598dbd86): 17 columnas en 5 recursos (Nivel, Campo de Formacion, Hombres/Mujeres Egresados).')
lineas.append('- Estudiantes de reingreso (diccionario fe8e7f84): 14 columnas Nivel en 14 recursos.')
lineas.append('- Poblacion ITAMA Externamiento (diccionario a7ee5717): 14 columnas en 3 recursos (SEXO, EDAD ACTUAL, DELITO en 5 hojas del recurso 71defd43: POBLACION EXTERNAMIENTO, TIEMPO LIBRE, DIVERSO PROCESO, SENTENCIAS, ORAL; SENTENCIA). Cada hoja tiene su propio esquema y huella; la IRI fisica distingue la hoja.')
lineas.append('- Victimas metodologia anterior (diccionario 213ebb9a, recurso 2014-2017): 13 columnas (INEGI, ENERO-DICIEMBRE).')
lineas.append('- Mejora Regulatoria (diccionario af14d207): 8 columnas (P6, P7, P9, P11, P12, P14, P15, P16).')
lineas.append('- Matriculas Ciclo 2021-2022 (diccionario b3d332cd): 8 columnas (Programa academico, Sexo, Promedios, Creditos, Residencias, Seguro, Discapacidad).')
lineas.append('- Planeacion TIC (diccionario 3b314916): 6 columnas (P6, P7, P8, P10, P11, P12).')
lineas.append('- Titulados 2020-2021 (diccionario 3f4a7c9e): 1 columna (Sexo).')
lineas.append('')
lineas.append('## Significados pendientes (28)')
lineas.append('')
lineas.append('Todos fuera_del_nucleo_actual por dominio_o_medida_sin_regla_revisada. Sin regla vigente que respalde el significado y con descripciones genericas o de encuesta (p. ej. ID, P2 Sector, horas, metodologias, Convocatoria, DELITO/MODALIDAD de victimas, Semestre que cursa, ACTIVIDAD/MOTIVO, No., Estudiante), quedan pendientes con evidencia faltante precisa en pendientes.json y solicitudes agrupadas por diccionario en entrega.json. No se crean reglas ni conceptos nuevos.')
lineas.append('')
with io.open(ROOT + LOTE + 'resultado.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lineas) + '\n')

h = hashlib.sha256(io.open(ROOT + LOTE + 'entrega.json', 'rb').read()).hexdigest()
save(LOTE + 'listo.json', {'lote': 'lote-2', 'sha256_entrega': h,
                           'cuentas': {'decisiones_columnas': 667, 'proponer': 667, 'pendiente_columna': 0,
                                       'rechazar': 0, 'vinculos': 667, 'decisiones_significados': 28,
                                       'significados_proponer': 0, 'significados_pendiente': 28,
                                       'reglas_nuevas': 0, 'conceptos_nuevos': 0,
                                       'solicitudes_investigacion': len(solicitudes)}})
print('listo sha:', h)
print('columnas:', len(decisiones_columnas), 'vinculos:', len(vinculos))
print('significados:', len(decisiones_significados), 'solicitudes:', len(solicitudes))
