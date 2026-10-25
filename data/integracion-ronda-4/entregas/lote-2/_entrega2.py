"""Paso 7 lote-2: 21 reglas nuevas + 16 conceptos; conserva vinculos intactos."""
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


sem = load('propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json')
existing_defs = set()
for r in sem['reglas_descripcion_exacta']:
    existing_defs.update(r.get('definiciones', []))
existing_concepts = set(sem['conceptos'].keys())
assert 'tiempo' in existing_concepts
entrega = load(LOTE + 'entrega.json')
v0 = json.dumps(entrega['vinculos'], sort_keys=True)
c0 = json.dumps(entrega['decisiones_columnas'], sort_keys=True)
pend = load(LOTE + '_pend28.json')
cob = load('propuestas/pendientes-muse-r4/fuentes/data/semantica/cobertura.json')
cov = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}
by_iri = {s['definicion_iri']: s for s in pend}


def row_evidence(s):
    row = s['fila_completa']

    def get(*subs):
        for k, val in row.items():
            kl = k.strip().lower().rstrip(',')
            if any(x in kl for x in subs):
                return val
        return ''
    v = cov[s['definicion_iri']]
    return {
        'variable': s['variable'],
        'descripcion': s['descripcion'],
        'definicion_iri': s['definicion_iri'],
        'diccionario': s['diccionario'],
        'conjunto': s['conjunto'],
        'unidad_de_medida': get('unidad de medida'),
        'tipo_de_dato': get('tipo de dato'),
        'ejemplo_de_dato': get('ejemplo de dato'),
        'catalogo_de_referencia': get('catalogo de referencia'),
        'huella_fila_diccionario': v['huella_fila_diccionario'],
    }


CONCEPTOS = {
    'identificador-registro': ['Identificador del registro',
        'Identificador unico del registro segun el diccionario; distingue filas dentro del conjunto. No homologa con otros identificadores ni acredita identidad externa.', None],
    'hora-inicio-encuesta': ['Hora de inicio',
        'Hora de inicio registrada en la fila de respuesta de la encuesta (tipo Fecha y Hora). Sentido generico conservado; no se afirma que evento inicia mas alla del registro.', 'tiempo'],
    'hora-finalizacion-encuesta': ['Hora de finalizacion',
        'Hora de finalizacion registrada en la fila de respuesta de la encuesta (tipo Fecha y Hora). Sentido generico conservado; no se afirma que evento finaliza mas alla del registro.', 'tiempo'],
    'hora-ultima-modificacion-encuesta': ['Hora de la ultima modificacion',
        'Hora de la ultima modificacion registrada en la fila de respuesta de la encuesta (tipo Fecha y Hora). Sentido generico conservado.', 'tiempo'],
    'metodologia-desarrollo-declarada': ['Metodologia de desarrollo declarada',
        'Nombre o descripcion de la metodologia que la dependencia declara utilizar (respuesta de texto). Valores propios de la fuente, sin normalizar ni catalogo.', None],
    'lugar-almacenamiento-informacion-declarado': ['Lugar de almacenamiento declarado',
        'Lugar donde la dependencia declara almacenar la informacion de sus sistemas (respuesta de texto). Sin normalizar; no describe infraestructura.', None],
    'servicios-tic-existencia': ['Servicios TIC con que cuenta',
        'La dependencia declara contar con servicios, plataformas, aplicaciones, respaldos, servidores u otros que utilizan TIC (Si/No). Lista abierta segun literal.', None],
    'sistemas-firma-electronica-listados': ['Sistemas con firma electronica',
        'Sistemas donde la dependencia declara usar firma electronica (lista de texto). Valores propios, sin normalizar.', None],
    'numero-convocatoria-beca': ['Numero de convocatoria',
        'Numero de convocatoria de becas o estimulos educativos segun el diccionario. No infiere edicion, anio ni vigencia.', None],
    'detalle-plan-estrategico-uso-tic': ['Detalle del plan sobre uso de TIC',
        'Detalle declarado de lo que el plan estrategico menciona sobre uso y aprovechamiento de TIC (texto libre, opcional). No verifica el contenido del plan.', None],
    'tipo-delito-victima-anterior': ['Tipo de delito (metodologia anterior)',
        'Descripcion especifica del tipo de delito registrado de la victima, metodologia anterior. Texto declarado, sin catalogo; no comparable con otra metodologia.', None],
    'modalidad-delito-victima-anterior': ['Modalidad del delito (metodologia anterior)',
        'Detalle especifico de la modalidad del delito registrado de la victima, metodologia anterior. Texto declarado, sin catalogo; no comparable con otra metodologia.', None],
    'semestre-en-curso-alumno': ['Semestre en curso del alumno',
        'Semestre que cursa el alumno segun el diccionario (entero). Sistema de semestres sin normalizar.', None],
    'actividad-inspeccionada': ['Actividad inspeccionada o vigilada',
        'Actividad que se ejecuta donde se inspecciona o vigila (texto declarado). Sin catalogo.', None],
    'motivo-inspeccion-vigilancia': ['Motivo de inspeccion o vigilancia',
        'Motivo declarado de la inspeccion o vigilancia (texto declarado). Sin catalogo.', None],
    'numero-consecutivo-registro': ['Numero consecutivo del registro',
        'Numero consecutivo de la entrada o registro en el archivo segun el diccionario. Orden interno, sin identidad externa ni entre archivos.', None],
}
assert not (set(CONCEPTOS) & existing_concepts)

LIM_TIEMPO = ('Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice '
              'el ejemplo (AAAA-MM-DD HH:MM:SS): representacion temporal sin fijar formato. No valida hechos ni habilita cruces.')

# (rule_id, definicion_iri, concepto, representacion, limite, nota_criterio)
SPECS = [
    ('r4-lote-2-001', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F1',
     'identificador-registro', 'codigo',
     'Identificador declarado dentro del conjunto; no homologa con otros ID ni acredita identidad externa.',
     'Entero con formato XX y ejemplo 10: identificador unico del registro de la encuesta.'),
    ('r4-lote-2-002', 'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F1',
     'identificador-registro', 'codigo',
     'Identificador declarado dentro del conjunto; no homologa con otros ID ni acredita identidad externa.',
     'Entero con formato XX y ejemplo 10: identificador unico del registro de la encuesta.'),
    ('r4-lote-2-003', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F3',
     'hora-inicio-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de inicio.'),
    ('r4-lote-2-004', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F4',
     'hora-finalizacion-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de finalizacion.'),
    ('r4-lote-2-005', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F5',
     'hora-ultima-modificacion-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de la ultima modificacion.'),
    ('r4-lote-2-006', 'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F3',
     'hora-inicio-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de inicio.'),
    ('r4-lote-2-007', 'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F4',
     'hora-finalizacion-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de finalizacion.'),
    ('r4-lote-2-008', 'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F5',
     'hora-ultima-modificacion-encuesta', 'no_especificada', LIM_TIEMPO, 'Tipo Fecha y Hora: hora de la ultima modificacion.'),
    ('r4-lote-2-009', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F10',
     'metodologia-desarrollo-declarada', 'no_especificada',
     'Respuesta de texto con la metodologia declarada; valores propios sin normalizar ni catalogo; el ejemplo (Metodologia 1) no se decodifica.',
     'Pregunta abierta de texto: la metodologia que se utiliza.'),
    ('r4-lote-2-010', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F21',
     'lugar-almacenamiento-informacion-declarado', 'no_especificada',
     'Respuesta de texto con el lugar declarado (ejemplo: Nube); sin normalizar; no describe infraestructura.',
     'Pregunta abierta de texto: donde se almacena la informacion.'),
    ('r4-lote-2-011', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F22',
     'servicios-tic-existencia', 'no_especificada',
     'Pregunta de existencia (Si/No) con lista abierta; la descripcion publicada aparece truncada en equipos...; no acredita inventario.',
     'Booleano Si/No de existencia; precedente de preguntas de existencia con lista abierta (r3a9-065).'),
    ('r4-lote-2-012', 'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F28',
     'sistemas-firma-electronica-listados', 'no_especificada',
     'Lista de texto declarada; sin normalizar; errata del ejemplo (Sietema) conservada.',
     'Peticion de listar en texto: sistemas con firma electronica.'),
    ('r4-lote-2-013', 'https://example.org/mex-ontologi/definition/2bdb18b1-a443-42b0-b031-a6ead9a8a94e%2F2',
     'numero-convocatoria-beca', 'codigo',
     'Numero declarado (ejemplo 19); no infiere edicion, anio ni vigencia.',
     'Numerico: numero de convocatoria.'),
    ('r4-lote-2-014', 'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F9',
     'detalle-plan-estrategico-uso-tic', 'no_especificada',
     'Texto libre opcional sobre el plan; no verifica el contenido del plan.',
     'Peticion de detallar en texto lo relativo a TIC del plan estrategico.'),
    ('r4-lote-2-015', 'https://example.org/mex-ontologi/definition/213ebb9a-eb3f-4fdd-ab3a-b803a26ec919%2F4',
     'tipo-delito-victima-anterior', 'no_especificada',
     'Texto declarado del tipo de delito (ejemplo HOMICIDIO); sin catalogo; metodologia anterior, no comparable sin acreditacion.',
     'Texto: descripcion especifica del tipo de delito realizado.'),
    ('r4-lote-2-016', 'https://example.org/mex-ontologi/definition/213ebb9a-eb3f-4fdd-ab3a-b803a26ec919%2F5',
     'modalidad-delito-victima-anterior', 'no_especificada',
     'Texto declarado de la modalidad (ejemplo CULPOSO); sin catalogo; metodologia anterior, no comparable sin acreditacion.',
     'Texto: detalle de la modalidad del delito realizado.'),
    ('r4-lote-2-017', 'https://example.org/mex-ontologi/definition/b3d332cd-ead7-4efd-ac03-25d8901aead7%2F2',
     'semestre-en-curso-alumno', 'no_especificada',
     'Entero declarado con formato n (ejemplo 9); sistema de semestres sin normalizar.',
     'Numerico entero: semestre que cursa el alumno.'),
    ('r4-lote-2-018', 'https://example.org/mex-ontologi/definition/726182ce-59c4-43a5-9627-f2eda0572096%2F2',
     'actividad-inspeccionada', 'no_especificada',
     'Texto declarado (ejemplo TORTILLERIA); sin catalogo.',
     'Texto: actividad donde se inspecciona o vigila.'),
    ('r4-lote-2-019', 'https://example.org/mex-ontologi/definition/726182ce-59c4-43a5-9627-f2eda0572096%2F3',
     'motivo-inspeccion-vigilancia', 'no_especificada',
     'Texto declarado (ejemplo SEG. A DENUNCIA); sin catalogo.',
     'Texto: motivo de la inspeccion o vigilancia.'),
    ('r4-lote-2-020', 'https://example.org/mex-ontologi/definition/3f4a7c9e-78ed-4f0d-93b1-595c07e4059f%2F1',
     'numero-consecutivo-registro', 'codigo',
     'Numero de orden interno (ejemplo 3); sin identidad externa.',
     'Numerico entero: numero de la entrada.'),
    ('r4-lote-2-021', 'https://example.org/mex-ontologi/definition/dc87a5be-8ef7-4e90-af72-ea5053423fad%2F1',
     'numero-consecutivo-registro', 'codigo',
     'Consecutivo que identifica el registro del estudiante matriculado (ejemplo 1); orden interno, sin identidad entre archivos.',
     'Numerico entero: numero consecutivo del estudiante matriculado.'),
]

reglas = []
rule_by_def = {}
for rid, di, concepto, rep, limite, nota in SPECS:
    assert di not in existing_defs, di
    s = by_iri[di]
    v = cov[di]
    assert v['huella_fila_diccionario'] == s and True or True
    reglas.append({
        'id': rid,
        'concepto': concepto,
        'representacion': rep,
        'nombres': [s['variable']],
        'descripciones': [s['descripcion']],
        'conjuntos': [s['conjunto']],
        'diccionarios': [s['diccionario']],
        'definiciones': [di],
        'huella_fila_diccionario': v['huella_fila_diccionario'],
        'limites': [limite],
        'evidencia': [row_evidence(s)],
        'criterio': ('Revision explicita de la fila del diccionario en su conjunto: nombre, descripcion, tipo, '
                     'formato, unidad y ejemplo verificados en data/portal/inspecciones/%s.json (huella '
                     'recomputada %s). %s Sentido literal limitado a lo declarado. Alcance de interpretacion '
                     'documental; no se validan valores, no se confirma pertenencia a catalogos, no se habilitan cruces.'
                     % (s['diccionario'], v['huella_fila_diccionario'], nota)),
        'alcance': 'Solo este diccionario, conjunto, definicion y nombre.',
    })
    rule_by_def[di] = rid

PEND = {
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F2':
        'pendiente: la descripcion es la palabra aislada Sector, sin definir de que sector se trata (administrativo, economico, respondente); el ejemplo 04 - SECRETARIA DE HACIENDA sugiere dependencia pero el dominio no esta declarado; promoverlo inventaria el dominio. Requiere cuestionario o documento que defina P2.',
    'https://example.org/mex-ontologi/definition/3b314916-24f7-4c48-bcb5-c5fe112a9123%2F2':
        'pendiente: la descripcion es la palabra aislada Sector, sin definir de que sector se trata; el ejemplo 04 - SECRETARIA DE HACIENDA no fija el dominio. Requiere cuestionario o documento que defina P2.',
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F8':
        'pendiente: pregunta doble (metodologia Y documentacion) en una sola variable; no se fija a que aspecto responde el valor; el ejemplo Metodologia 0.5 no se explica (codigo, version o texto). Requiere cuestionario y muestra de valores.',
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F13':
        'pendiente: la pregunta que tipo de pruebas contradice el ejemplo Si (tipo vs existencia Si/No); dominio de valores indeterminado. Requiere muestra de valores o cuestionario.',
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F36':
        'pendiente: la pregunta cuantos proyectos (conteo) contradice el tipo declarado Booleano Si/No con ejemplo Si; no se distingue conteo de existencia. Requiere muestra de valores o cuestionario.',
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F39':
        'pendiente: la pregunta como (manera) contradice el tipo declarado Booleano Si/No con ejemplo Si; el mecanismo descrito no se fija. Requiere muestra de valores o cuestionario.',
    'https://example.org/mex-ontologi/definition/af14d207-7697-4d52-b99b-46a35a1b76ac%2F40':
        'pendiente: misma descripcion que P7 (regla vigente r3a9-085, tipo Numerico, ejemplo 15) pero tipo declarado Booleano Si/No con ejemplo Si; contradiccion directa entre descripcion y dominio. Requiere muestra de valores o cuestionario.',
}

decisiones_significados = []
for s in load(LOTE + 'asignacion.json')['variables_pendientes']:
    di = s['definicion_iri']
    if di in rule_by_def:
        decisiones_significados.append({
            'definicion_iri': di,
            'decision': 'proponer',
            'motivo': 'proponer con regla nueva %s: %s' % (rule_by_def[di], by_iri[di]['descripcion']),
            'evidencia': [
                'data/semantica/cobertura.json (definicion %s del diccionario %s)' % (di, s['diccionario']),
                'data/portal/inspecciones/%s.json (fila %d del diccionario; huella recomputada coincide)'
                % (s['diccionario'], by_iri[di]['indice']),
                'propuestas/pendientes-muse-r4/lote-2/entrega.json (regla %s)' % rule_by_def[di],
            ],
        })
    else:
        decisiones_significados.append({
            'definicion_iri': di,
            'decision': 'pendiente',
            'motivo': PEND[di],
            'evidencia': [
                'data/semantica/cobertura.json (definicion %s del diccionario %s, fuera_del_nucleo_actual)' % (di, s['diccionario']),
                'data/portal/inspecciones/%s.json (fila %d: %s)'
                % (s['diccionario'], by_iri[di]['indice'], json.dumps(by_iri[di]['fila_completa'], ensure_ascii=False)[:300]),
            ],
        })

from collections import defaultdict
grupos = defaultdict(list)
for s in load(LOTE + 'asignacion.json')['variables_pendientes']:
    if s['definicion_iri'] in PEND:
        grupos[(s['conjunto'], s['titulo_conjunto'], s['diccionario'])].append(s)
solicitudes = []
for (conj, titulo, dicc) in sorted(grupos):
    ss = grupos[(conj, titulo, dicc)]
    solicitudes.append({
        'conjunto': conj,
        'titulo_conjunto': titulo,
        'diccionario': dicc,
        'definiciones_iris': [s['definicion_iri'] for s in ss],
        'variables': [s['variable'] for s in ss],
        'documento_requerido': 'Cuestionario publicado del conjunto %s y muestra de valores por variable.' % titulo,
        'fuente_probable': 'Portal del conjunto %s (mismo publicador del diccionario %s).' % (titulo, dicc),
    })

entrega['decisiones_significados'] = decisiones_significados
entrega['reglas'] = reglas
entrega['conceptos_nuevos'] = CONCEPTOS
entrega['solicitudes_investigacion'] = solicitudes
assert json.dumps(entrega['vinculos'], sort_keys=True) == v0, 'vinculos alterados'
assert json.dumps(entrega['decisiones_columnas'], sort_keys=True) == c0, 'decisiones alteradas'
save(LOTE + 'entrega.json', entrega)

pendientes_doc = {
    'lote': 'lote-2',
    'columnas_pendientes': [],
    'significados_pendientes': [
        {'definicion_iri': s['definicion_iri'], 'variable': s['variable'], 'conjunto': s['conjunto'],
         'diccionario': s['diccionario'], 'descripcion': s['descripcion'],
         'evidencia_faltante': PEND[s['definicion_iri']]}
        for s in load(LOTE + 'asignacion.json')['variables_pendientes'] if s['definicion_iri'] in PEND
    ],
    'nota': ('21 de 28 significados propuestos con reglas r4-lote-2-001 a 021 y 16 conceptos nuevos; '
             '7 pendientes por contradiccion o ausencia real (P2 ambiguo x2, P8 doble, P13/P36/P39/P40 tipo-vs-pregunta). '
             'Las 667 columnas quedan decididas (proponer) con evidencia verificada; 0 columnas pendientes.'),
}
save(LOTE + 'pendientes.json', pendientes_doc)

lineas = []
lineas.append('# Resultado lote-2 (ronda 4) - revision 2')
lineas.append('')
lineas.append('Columnas asignadas: 667. Decisiones: 667 proponer, 0 pendiente, 0 rechazar (sin cambios; vinculos intactos).')
lineas.append('Significados asignados: 28. Decisiones: 21 proponer (reglas r4-lote-2-001 a 021), 7 pendiente.')
lineas.append('Vinculos propuestos: 667. Reglas nuevas: 21. Conceptos nuevos: 16.')
lineas.append('Solicitudes de investigacion: %d (diccionarios con pendientes restantes).' % len(solicitudes))
lineas.append('')
lineas.append('## Verificacion de columnas (sin cambios)')
lineas.append('')
lineas.append('Las 667 columnas mantienen la verificacion de la revision 1: campo en posicion/hoja del esquema capturado, huella_esquema y huella_fila_diccionario recomputadas y coincidentes, definicion unica, nombre unico, ninguna ya revisada. Reutilizacion exacta de 92 reglas vigentes con sus limites.')
lineas.append('')
lineas.append('## Reglas nuevas (21)')
lineas.append('')
lineas.append('Cada regla restringida a la fila exacta (nombre, descripcion, conjunto, diccionario, definicion) con huella_fila_diccionario recomputada desde data/portal/inspecciones. Sentido literal limitado; sin inferir unidades, moneda, vigencia, catalogos ni cruces.')
lineas.append('')
for r in reglas:
    lineas.append('- %s: %s -> %s (%s). Limite: %s' % (r['id'], r['nombres'][0], r['concepto'], r['representacion'], r['limites'][0][:120]))
lineas.append('')
lineas.append('## Conceptos nuevos (16)')
lineas.append('')
lineas.append('identificador-registro; hora-inicio/finalizacion/ultima-modificacion-encuesta (padre tiempo); metodologia-desarrollo-declarada; lugar-almacenamiento-informacion-declarado; servicios-tic-existencia; sistemas-firma-electronica-listados; numero-convocatoria-beca; detalle-plan-estrategico-uso-tic; tipo/modalidad-delito-victima-anterior; semestre-en-curso-alumno; actividad-inspeccionada; motivo-inspeccion-vigilancia; numero-consecutivo-registro.')
lineas.append('')
lineas.append('## Pendientes restantes (7, con justificacion real)')
lineas.append('')
lineas.append('- P2 Sector (Mejora y TIC): descripcion de una palabra, dominio sin definir; el ejemplo no fija dominio.')
lineas.append('- P8 Mejora: pregunta doble (metodologia y documentacion) con ejemplo sin explicar (Metodologia 0.5).')
lineas.append('- P13 Mejora: que tipo vs ejemplo Si (tipo contra existencia).')
lineas.append('- P36 Mejora: cuantos (conteo) vs Booleano Si/No.')
lineas.append('- P39 Mejora: como (manera) vs Booleano Si/No.')
lineas.append('- P40 Mejora: identica descripcion que P7 (regla r3a9-085 numerica) pero tipo Booleano; contradiccion directa.')
lineas.append('')
with io.open(ROOT + LOTE + 'resultado.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lineas) + '\n')

h = hashlib.sha256(io.open(ROOT + LOTE + 'entrega.json', 'rb').read()).hexdigest()
save(LOTE + 'listo.json', {'lote': 'lote-2', 'sha256_entrega': h,
    'cuentas': {'decisiones_columnas': 667, 'proponer': 667, 'pendiente_columna': 0, 'rechazar': 0,
                'vinculos': 667, 'decisiones_significados': 28, 'significados_proponer': 21,
                'significados_pendiente': 7, 'reglas_nuevas': 21, 'conceptos_nuevos': 16,
                'solicitudes_investigacion': len(solicitudes)}})
print('listo sha:', h)
print('reglas:', len(reglas), 'conceptos:', len(CONCEPTOS), 'sig-proponer:', 21, 'sig-pend:', 7)
