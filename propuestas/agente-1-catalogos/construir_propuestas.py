"""Construye propuestas.json (9 propuestas, no aplicadas) desde evidencia literal.
Literales (hojas, encabezados, nombres, entradas) desde archivos descargados.
Normalizaciones solo en campos *_norm. Sin cambios de clasificacion.
"""
import json, unicodedata, datetime

B = 'propuestas/agente-1-catalogos'
refs = json.load(open(f'{B}/fase1_refs.json', encoding='utf-8'))
man = json.load(open(f'{B}/manifiesto_descargas.json', encoding='utf-8'))
mues = json.load(open(f'{B}/muestras_datos.json', encoding='utf-8'))
cat = json.load(open(f'{B}/catalogos_contenido.json', encoding='utf-8'))
conj = {d['id']: d for d in json.load(open(f'{B}/conjuntos_objetivo.json', encoding='utf-8'))}
ex = json.load(open(f'{B}/exactos.json', encoding='utf-8'))
FECHA = man.get('fecha_consulta_utc')

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return ' '.join(s.lower().split())

def dl(cj, rc):
    for a in man['archivos']:
        if a['conjunto'] == cj and a['recurso'] == rc:
            return a
    raise KeyError(cj + rc)

def muestra(cj):
    for m in mues['muestras']:
        if m['conjunto'] == cj:
            return m
    return None

def ref_de(rid):
    for r in refs:
        if r['id'] == rid:
            return r
    raise KeyError(rid)

def cat_filas(cj, rc, hoja):
    for k, v in cat.items():
        if cj in k and rc in k:
            for h in v['hojas']:
                if h['hoja'] == hoja:
                    return h
    raise KeyError(cj + rc + hoja)

# Entradas educativas literales desde el archivo (Hoja1 del primer catalogo)
EDU = cat_filas('403912fd-5853-4e18-8256-f77206f855bd',
                '6d561451-ff08-45d6-b1af-285ff5f417b1', 'Hoja1')['filas']
EDU_HDR = cat_filas('403912fd-5853-4e18-8256-f77206f855bd',
                    '6d561451-ff08-45d6-b1af-285ff5f417b1', 'Hoja1')['encabezado']
EDU_SHA = '53bd5e971a033998ed8a72317b6ad1e69314d82463220d8cfd156dfad9034259'
EDU_NOTA_IGUALDAD = ('Los cuatro archivos catalogo.xlsx tienen SHA-256 idéntico 53bd5e97… '
    '(misma Hoja1, 10 entradas). La igualdad se registra aparte por huella; '
    'las cuatro referencias permanecen separadas por conjunto.')

P = []
def add(pid, rid, clas, conjunto, recurso_cat, hoja, campo_cat, campo_dic,
        corr_justificacion, usa_norm, evidencia_extra,
        justificacion, alcance, limitaciones, cambios,
        nombre_dic, desc_dic, ejemplo_dic, detalle_dic=None, identif_dic=None,
        var_dic=None, derivas=None, huellas=None):
    r = ref_de(rid)
    d = dl(conjunto, recurso_cat)
    m = muestra(conjunto)
    ds = conj[conjunto]
    norm_obj = ({'metodo': 'minusculas, NFD sin diacriticos, espacios colapsados; solo para comparar',
                 'campo_catalogo_norm': norm(campo_cat),
                 'campo_diccionario_norm': norm(campo_dic)}
                if usa_norm else
                {'metodo': 'ninguna; coincidencia literal de cadenas',
                 'campo_catalogo_norm': campo_cat, 'campo_diccionario_norm': campo_dic})
    P.append({
        'id_propuesta': pid,
        'referencia_original': {
            'iri': r['referencia_iri'], 'id': r['id'],
            'nombre_catalogo_grafo': r['nombre_catalogo'],
            'label_grafo': r['label'],
            'nota_codificacion_grafo': ('literales del grafo central con daño de codificación; '
                'los originales legibles están en nombre_catalogo_diccionario'),
            'nombre_catalogo_diccionario': nombre_dic,
            'variable_diccionario': var_dic, 'descripcion_diccionario': desc_dic,
            'detalle_relacion_diccionario': detalle_dic, 'identificadores_diccionario': identif_dic,
            'ejemplo_diccionario': ejemplo_dic,
            'definicion_iris': derivas, 'huellas_fila_diccionario': huellas},
        'organizacion_publicadora': ds['organization']['title'],
        'titulo_conjunto': ds['title'],
        'conjunto': conjunto, 'clasificacion': clas,
        'recurso': {'conjunto': conjunto, 'recurso': recurso_cat,
            'nombre_recurso': next(x['name'] for x in ds['resources'] if x['id'] == recurso_cat),
            'url': d['url'], 'hoja': hoja, 'campo_catalogo': campo_cat,
            'campo_diccionario': campo_dic,
            'correspondencia_campos_justificacion': corr_justificacion,
            'normalizacion': norm_obj},
        'evidencia': {'fuente_conjunto_url': f'https://datos.sonora.gob.mx/dataset/{conjunto}',
            'fuente_recurso_url': d['url'], 'http_status': d['http_status'],
            'content_type': d['content_type'], 'fecha_consulta_utc': d['fecha_descarga_utc'] or FECHA,
            'sha256': d['sha256'], 'bytes': d['bytes'], 'archivo_local': d['archivo_local'],
            **evidencia_extra,
            'muestra_datos': ({'recurso': m['recurso'], 'url': m['url'], 'hoja': m['hoja'],
                'encabezado_real': m['encabezado_real'], 'indice_columna': m['indice_columna'],
                'primeros_valores': (m['primeros_valores'] or [])[:25],
                'distribucion_muestra': m['distribucion_muestra_25'],
                'sha256_muestra': m['sha256'],
                'nota': ('Muestra (primeras filas). Apoya identificación; no demuestra unicidad, '
                         'cobertura ni ausencia de códigos contradictorios.')} if m else None)},
        'justificacion': justificacion, 'alcance': alcance,
        'limitaciones': limitaciones, 'cambios_sugeridos_integrador': cambios,
        'no_aplicado': True})

ED = ex['diccionarios']
E403 = ED['403912fd-5853-4e18-8256-f77206f855bd']['fila']
Ee5a = ED['e5aad52d-5760-481c-ba65-db0ba4a5315e']['fila']
Ee7a = ED['e7a3d62f-4ace-479c-aa52-1c9e384dc429']['fila']
E85e = ED['85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f']['fila']
H = ED['ee8f639f-5e89-46ae-93b9-934b05fc6233']['fila_clave']
F = ED['5494daa1-09ca-4750-aeac-2558553700e1']['filas']

def ev_ref(rid):
    r = ref_de(rid)
    evs = r['evidencias_variables']
    return ([e['definicion_iri'] for e in evs],
            [(e['variable'] or {}).get('huella_fila_diccionario') for e in evs])

der, hue = ev_ref('1eb8b1a583f52b32f256fb5643ffa7402dfb5ecf27d2df1d7114e71403a262a9')
add('P01', '1eb8b1a583f52b32f256fb5643ffa7402dfb5ecf27d2df1d7114e71403a262a9', 'recurso_identificado',
    '403912fd-5853-4e18-8256-f77206f855bd', '6d561451-ff08-45d6-b1af-285ff5f417b1', 'Hoja1',
    'Campo de Formación Académica', 'CAMPO DE FORMACIÓN ACADÉMICA',
    ('Correspondencia justificada no literal en mayúsculas/acentos: diccionario '
     '"CAMPO DE FORMACIÓN ACADÉMICA" ↔ catálogo "Campo de Formación Académica"; mismo rol '
     '(código de 2 dígitos) y ejemplo de dato 07 que coincide con el código 07 del catálogo.'),
    True,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 10, 'codigos_unicos': True,
     'encabezado_catalogo': EDU_HDR, 'entradas_completas': EDU,
     'sha_igualdad_4_conjuntos': EDU_SHA, 'nota_igualdad': EDU_NOTA_IGUALDAD},
    ('Diccionario del mismo conjunto declara el catálogo; recurso Catalogo del mismo conjunto '
     'contiene Hoja1 con el campo y 10 códigos (revisión completa); ejemplo 07 y muestra de datos '
     '2022-1 (04,06,07,09,10) caen dentro del catálogo.'),
    'Identifica el recurso publicado que corresponde a esta referencia, por conjunto. No afirma que todos los archivos de datos lo usen ni su vigencia histórica.',
    ['Vigencia histórica no comprobada (metadatos del recurso con fechas 1989-06-04 genéricas).',
     'Muestra de datos parcial (25 primeras filas de un archivo); cobertura total pendiente para el integrador.',
     'Archivo catalogo.xlsx idéntico en 4 conjuntos (misma huella); no se fusionan las referencias.'],
    {'accion': ('Agregar vínculo catalogoRecuperado a esta referencia con {recurso, hoja Hoja1, '
                'campo_catalogo, campo_diccionario, sha256, fecha_consulta} y cambiar estado a '
                'recurso_catalogo_identificado solo para este conjunto; conservar nombre original; '
                'no extender a otros conjuntos ni a columnas de datos.')},
    E403[6], E403[4], E403[8], None, None, E403[0], der, hue)

der, hue = ev_ref('4c28a0a21e5753bd01eb1cb39615ff939b13c949af50741af5c405bf575619f0')
add('P02', '4c28a0a21e5753bd01eb1cb39615ff939b13c949af50741af5c405bf575619f0', 'recurso_identificado',
    'e5aad52d-5760-481c-ba65-db0ba4a5315e', 'aaf0c6c1-76a7-40ac-b542-1319d1bb2a5a', 'Hoja1',
    'Campo de Formación Académica', 'Campo de Formación Académica',
    ('Correspondencia directa de campo (mismo nombre); el nombre del catálogo en el diccionario '
     'lleva dos puntos finales "…superior:" que se conservan como texto original sin fusionar.'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 10, 'codigos_unicos': True,
     'encabezado_catalogo': EDU_HDR, 'entradas_completas': EDU,
     'sha_igualdad_4_conjuntos': EDU_SHA, 'nota_igualdad': EDU_NOTA_IGUALDAD},
    ('Mismo caso que P01 en otro conjunto: catálogo declarado, recurso Catalogo propio, Hoja1 con '
     '10 códigos (revisión completa); ejemplo 7 y muestra de Matrículas ene-abr 2022 (07 dominante, 04) '
     'dentro del catálogo.'),
    'Identifica recurso por conjunto; no prueba uso en todos los archivos ni vigencia.',
    ['Vigencia no comprobada.', 'Muestra parcial (25 filas).', 'Catálogo idéntico en 4 conjuntos; referencias separadas.'],
    {'accion': ('Vincular recurso/hoja/campo a esta referencia (este conjunto), estado '
                'recurso_catalogo_identificado; conservar los dos puntos del nombre original; no propagar.')},
    Ee5a[6], Ee5a[4], Ee5a[8], None, None, Ee5a[0], der, hue)

der, hue = ev_ref('4c67f244bf4078ad48133d122b3d7df031a00b7a266145d111ff78622ebecfc4')
add('P03', '4c67f244bf4078ad48133d122b3d7df031a00b7a266145d111ff78622ebecfc4', 'recurso_identificado',
    'e7a3d62f-4ace-479c-aa52-1c9e384dc429', '0e69d911-6ed3-4268-841b-0c4989e7cb45', 'Hoja1',
    'Campo de Formación Académica', 'Campo de Formación Académica',
    ('Correspondencia directa de campo; nombre de catálogo sin dos puntos (se conserva tal cual, '
     'distinto de P02).'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 10, 'codigos_unicos': True,
     'encabezado_catalogo': EDU_HDR, 'entradas_completas': EDU,
     'sha_igualdad_4_conjuntos': EDU_SHA, 'nota_igualdad': EDU_NOTA_IGUALDAD},
    ('Recurso Catalogo propio del conjunto Titulados con Hoja1 de 10 códigos (revisión completa); '
     'ejemplo 7 y muestra de Titulados 2022 (04,06,07,10…) dentro del catálogo.'),
    'Identifica recurso por conjunto; no prueba uso total ni vigencia.',
    ['Vigencia no comprobada.', 'Muestra parcial.', 'Catálogo idéntico; referencias separadas.'],
    {'accion': ('Vincular recurso/hoja/campo a esta referencia (este conjunto), estado '
                'recurso_catalogo_identificado; conservar nombre original; no propagar.')},
    Ee7a[6], Ee7a[4], Ee7a[8], None, None, Ee7a[0], der, hue)

der, hue = ev_ref('7c2e51a0134a25e1c5636921b27ba896e4eb8978108c1b79d238b10548a021bb')
add('P04', '7c2e51a0134a25e1c5636921b27ba896e4eb8978108c1b79d238b10548a021bb', 'recurso_identificado',
    '85ee0e2b-ba05-4d9a-8177-cdbf0cb42f8f', 'af7a9aba-5a0e-4cf0-9b7d-5a3550e7907e', 'Hoja1',
    'Campo de Formación Académica', 'Campo de Formación Académica',
    ('Correspondencia directa de campo; la descripción del diccionario usa "formación académica" '
     'con espacio (variante ortográfica conservada).'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 10, 'codigos_unicos': True,
     'encabezado_catalogo': EDU_HDR, 'entradas_completas': EDU,
     'sha_igualdad_4_conjuntos': EDU_SHA, 'nota_igualdad': EDU_NOTA_IGUALDAD},
    ('Recurso Catalogo propio del conjunto Egresados con Hoja1 de 10 códigos (revisión completa); '
     'ejemplo 7 y muestra de Egresados 2022 (04,06,07,09,10) dentro del catálogo.'),
    'Identifica recurso por conjunto; no prueba uso total ni vigencia.',
    ['Vigencia no comprobada.', 'Muestra parcial.', 'Catálogo idéntico; referencias separadas.'],
    {'accion': ('Vincular recurso/hoja/campo a esta referencia (este conjunto), estado '
                'recurso_catalogo_identificado; conservar variante ortográfica original; no propagar.')},
    E85e[6], E85e[4], E85e[8], None, None, E85e[0], der, hue)

der, hue = ev_ref('3b45c474da5b2dc83e061ed7c26d470eaff0cd4935c626ac4cfa11e64a0e16e8')
HIDR = cat_filas('ee8f639f-5e89-46ae-93b9-934b05fc6233',
                 'f5060479-ee16-49b5-99d4-09aabef8042e', 'Catálogo_estatal')
add('P05', '3b45c474da5b2dc83e061ed7c26d470eaff0cd4935c626ac4cfa11e64a0e16e8', 'recurso_identificado',
    'ee8f639f-5e89-46ae-93b9-934b05fc6233', 'f5060479-ee16-49b5-99d4-09aabef8042e', 'Catálogo_estatal',
    'Clave', 'Clave',
    ('Correspondencia directa Clave↔Clave; el diccionario detalla "Identifica la clave de una presa '
     'junto a su descripción" y el ejemplo LCDSO coincide con el primer código del catálogo. '
     'No se usa el parecido del nombre del recurso ("Catalogo") sino hoja+campo+contenido.'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 10, 'codigos_unicos': True,
     'encabezado_catalogo': HIDR['encabezado'],
     'codigos': [r[0] for r in HIDR['filas']],
     'detalle_diccionario': H[7], 'ejemplo_diccionario': H[9],
     'otras_hojas_no_referenciadas': ['Municipios (72 entradas)', 'Regiones (10 entradas)']},
    ('Diccionario declara Catálogo_estatal para Clave (Clave de la presa ); recurso Catalogo del mismo '
     'conjunto contiene hoja Catálogo_estatal con columna Clave y 10 presas (revisión completa, códigos '
     'únicos); muestra de datos 1980-1989 usa esas claves.'),
    ('Identifica hoja y campo del recurso; no afirma que todos los archivos hídricos lo usen ni su '
     'vigencia por año (hay un recurso 1960-1969 sin URL).'),
    ['Vigencia histórica no comprobada; el catálogo incluye 1 presa de Chihuahua (AGZCH) y 9 de Sonora: no es un catálogo exclusivo de Sonora.',
     'Muestra de datos parcial (25 filas de 1980-1989); BICSO no aparece en la muestra.',
     'Hojas Municipios/Regiones del mismo archivo no forman parte de esta referencia.'],
    {'accion': ('Vincular referencia a {recurso f5060479, hoja Catálogo_estatal, campo Clave}, estado '
                'recurso_catalogo_identificado; conservar nombre original Catálogo_estatal; no vincular '
                'hojas Municipios/Regiones ni columnas de datos automáticamente.')},
    H[6], H[4], H[9], H[7], H[5], H[0], der, hue)

der, hue = ev_ref('9ff643fe3f91869a5a3aff089018f3913d8510551a6d50a7566123a44969b05f')
S = F['servic_atencion']
add('P06', '9ff643fe3f91869a5a3aff089018f3913d8510551a6d50a7566123a44969b05f', 'recurso_identificado',
    '5494daa1-09ca-4750-aeac-2558553700e1', '08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8', 'Catalogo Servicios',
    'servic_atencion', 'servic_atencion',
    ('Correspondencia directa servic_atencion↔servic_atencion respaldada por columnas Identificadores '
     'y Detalle del diccionario (ambas servic_atencion) y ejemplo "Urgencias médicas" que coincide '
     'con la entrada 1 del catálogo.'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 7, 'codigos_unicos': True,
     'encabezado_catalogo': ['servic_atencion', 'tipo de atencion'],
     'codigos': ['1', '2', '3', '4', '5', '6', '7'],
     'detalle_diccionario': S[7], 'ejemplo_diccionario': S[9]},
    ('Recurso Catalogo del mismo conjunto contiene hoja Catalogo Servicios con ese campo y 7 entradas '
     '(revisión completa); muestra Fiebre 2022 (n=50: 1,2,3,5,7 más 0 nulo) cae en catálogo salvo el 0 '
     'documentado como nulo.'),
    'Identifica hoja/campo; no prueba cobertura total ni vigencia.',
    ['Muestra parcial (n=50 de 2022); códigos 4 y 6 no aparecen en la muestra pero existen en el catálogo (revisión completa del catálogo sí hecha).',
     'Valor 0 en datos corresponde a nulo documentado, no a entrada del catálogo.'],
    {'accion': ('Vincular referencia a {recurso 08d3b1a7, hoja Catalogo Servicios, campo servic_atencion}, '
                'estado recurso_catalogo_identificado; conservar nombre original Catálogo servicios.')},
    S[6], S[4], S[9], S[7], S[5], S[0], der, hue)

der, hue = ev_ref('5b1ccbaafec13e5b4e83d513d5817f79d39b709d3a03efc206f2b265dc66fc75')
M = F['motiv_rech_ricket_sangre']
add('P07', '5b1ccbaafec13e5b4e83d513d5817f79d39b709d3a03efc206f2b265dc66fc75', 'recurso_identificado',
    '5494daa1-09ca-4750-aeac-2558553700e1', '08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8', 'Catalogo rechazo',
    'motiv_rech_ricket_sangre', 'motiv_rech_ricket_sangre',
    ('Correspondencia directa respaldada por Identificadores/Detalle (motiv_rech_ricket_sangre) y '
     'ejemplo 3 que coincide con la entrada 3 "Días de transito". Nombre del catálogo con espacio '
     'final conservado ("Motivos de rechazo ").'),
    False,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 20, 'codigos_unicos': True,
     'encabezado_catalogo': ['motiv_rech_ricket_sangre', 'Tipo de rechazo'],
     'codigos': [str(i) for i in range(1, 21)],
     'detalle_diccionario': M[7], 'ejemplo_diccionario': M[9]},
    ('Hoja Catalogo rechazo del mismo recurso con 20 entradas (revisión completa); muestra 2022 (n=50) '
     'mayormente 0/vacío (rechazo no aplica) sin contradecir el catálogo.'),
    'Identifica hoja/campo; la muestra casi no ejercita el catálogo (solo confirma formato de nulos); cobertura de uso pendiente.',
    ['Muestra n=50 con 45 ceros y 5 vacíos: apoyo débil de uso; la identificación se sostiene en diccionario+catálogo, no en la muestra.',
     'Vigencia no comprobada.'],
    {'accion': ('Vincular referencia a {recurso 08d3b1a7, hoja Catalogo rechazo, campo '
                'motiv_rech_ricket_sangre}, estado recurso_catalogo_identificado; conservar espacio final '
                'del nombre original.')},
    M[6], M[4], M[9], M[7], M[5], M[0], der, hue)

der, hue = ev_ref('c8e9eb88050d4c254c2f8e08bee2bac5095eea83f8e07aab0d2e9ce79aca9131')
E = F['ricket_especie_rtpcr']
add('P08', 'c8e9eb88050d4c254c2f8e08bee2bac5095eea83f8e07aab0d2e9ce79aca9131', 'recurso_identificado',
    '5494daa1-09ca-4750-aeac-2558553700e1', '08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8', 'Catalogo especie',
    'ricket_especie', 'ricket_especie_rtpcr',
    ('Correspondencia explícitamente justificada NO literal: la variable (ricket_especie_rtpcr) difiere '
     'de la columna del catálogo (ricket_especie), pero el diccionario la puentea en "Detalle de '
     'relación con catálogos" = ricket_especie e "Identificadores" = ricket_especie_rtpcr; ejemplo 1 '
     'coincide con la entrada 1 "R. Rickettsii". No se usa el parecido de nombres.'),
    True,
    {'hoja_fila_encabezado': 1, 'filas_datos_catalogo': 4, 'codigos_unicos': True,
     'encabezado_catalogo': ['ricket_especie', 'especie'],
     'codigos': ['1', '2', '3', '4'], 'detalle_diccionario': E[7],
     'identificadores_diccionario': E[5], 'ejemplo_diccionario': E[9]},
    ('Hoja Catalogo especie del mismo recurso con 4 entradas (revisión completa, únicas); muestra 2022 '
     '(n=50: 14 unos, resto 0/vacío) compatible.'),
    'Identifica hoja/campo mediante puente documental; la diferencia de nombres queda registrada y no se homologa.',
    ['Muestra parcial; la mayoría de filas son 0/vacío (nulo).', 'Vigencia no comprobada.',
     'No extender el puente ricket_especie a otras variables.'],
    {'accion': ('Vincular referencia a {recurso 08d3b1a7, hoja Catalogo especie, campo ricket_especie ↔ '
                'variable ricket_especie_rtpcr} con nota de correspondencia no literal y su justificación '
                '(detalle del diccionario); estado recurso_catalogo_identificado.')},
    E[6], E[4], E[9], E[7], E[5], E[0], der, hue)

der, hue = ev_ref('a2902c1feb2fa4b8349946c2ae418a11bf0f465032c5c62adaf33fb053373cf2')
add('P09', 'a2902c1feb2fa4b8349946c2ae418a11bf0f465032c5c62adaf33fb053373cf2', 'sin_resolver',
    '5494daa1-09ca-4750-aeac-2558553700e1', '08d3b1a7-dbc0-4f43-b1d2-3266cebb88f8', None, None,
    'ide_id / ide_col',
    ('Sin correspondencia: el único recurso Catalogo del conjunto tiene 3 hojas (Catalogo Servicios, '
     'Catalogo rechazo, Catalogo especie) y ninguna contiene columnas des_mpo_res, ide_id, ide_col, '
     'des_jur_res ni cve_loc_res (búsqueda de texto completo negativa en el libro). No se asigna a '
     'Vigilancia Epidemiológica: ambas evidencias (filas 177 y 178) pertenecen al diccionario 33d0a99e '
     'de Fiebre manchada.'),
    False,
    {'hojas_catalogo_revisadas': ['Catalogo Servicios', 'Catalogo rechazo', 'Catalogo especie'],
     'busqueda_texto_completo': ('des_mpo_res/ide_id/ide_col/des_jur_res/cve_loc_res sin ocurrencias '
                                 'en el libro'),
     'filas_origen_177': {'definicion_iri': der[0], 'huella': hue[0], 'linea_csv': 177,
        'nombrevar': 'ide_id', 'descripcion': 'ide_col', 'identificadores': 'des_jur_res',
        'catalogo_ref': 'des_mpo_res', 'detalle': 'cve_loc_res', 'ejemplo': 'ide_cp'},
     'filas_origen_178': {'definicion_iri': der[1], 'huella': hue[1], 'linea_csv': 178,
        'nombrevar': 'ide_id', 'descripcion': 'ide_col', 'identificadores': 'des_jur_res',
        'catalogo_ref': 'des_mpo_res', 'detalle': 'cve_loc_res', 'ejemplo': 'id_cp'},
     'nota_filas': ('Ambas filas se conservan como evidencias distintas de la misma referencia (difieren '
                    'en ejemplo ide_cp vs id_cp y en huella). Parecen fragmentos de encabezado '
                    'desalineados al final del CSV.'),
     'variable_homonima_no_origen': ('La variable des_mpo_res de la fila 7 (Municipio donde reside el caso, '
        'ejemplo Hermosillo) tiene Catálogo de referencia vacío; NO es el origen de esta referencia aunque '
        'comparta el nombre.')},
    ('No se encontró recurso publicado que corresponda: el catálogo del conjunto no contiene la hoja/campo '
     'y ningún otro recurso del conjunto es un catálogo. La columna de datos des_mpo_res (fila 7) usa '
     'texto libre municipal (muestra 2022: HERMOSILLO, PUERTO PEÑASCO, CAJEME…).'),
    ('Evidencia documental (celdas Catálogo de referencia = des_mpo_res en líneas 177/178) distinguida '
     'de la inferencia (sin candidato).'),
    ['No se puede descartar que exista un catálogo externo (p. ej. municipal) al que aluda el nombre, pero no hay publicación que lo respalde dentro del conjunto.',
     'Las filas 177/178 son degeneradas; requieren aclaración de la fuente antes de cualquier vínculo.',
     'No usar la coincidencia del nombre con la variable de la fila 7 como prueba.'],
    {'accion': ('Mantener estado solo_referencia_declarada_sin_resolver; conservar ambas derivaciones 177 '
                'y 178 con sus huellas; no crear vínculo catalogoRecuperado; pedir aclaración a la fuente '
                'sobre las líneas 177/178 y sobre si existe catálogo de municipios de residencia.')},
    'des_mpo_res', 'ide_id / ide_col (filas degeneradas 177-178)', None, None, None,
    'ide_id / ide_col', der, hue)

doc = {'generado_en_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'nota': ('Propuestas, no aplicadas al grafo. Nombres, hojas, encabezados, códigos y entradas '
          'conservados literalmente desde los archivos publicados; cualquier normalización va solo en '
          'campos normalizacion/*. Identificar el catálogo no afirma uso total en datos ni vigencia histórica.'),
 'total': len(P), 'propuestas': P}
with open(f'{B}/propuestas.json', 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
print('propuestas:', len(P))
