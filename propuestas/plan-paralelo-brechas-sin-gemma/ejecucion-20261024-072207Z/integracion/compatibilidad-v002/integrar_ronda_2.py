"""Integra la ronda 2 aprobada desde evidencia fijada; sin red ni modelos."""
from collections import Counter
import csv
import hashlib
import io
import json
import re
from urllib.parse import quote
import zipfile

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, SKOS
from construir_catalogo import ROOT, PROV
from integrar_entregas import leer_tabla

OUT = ROOT / 'data/integracion-ronda-2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validar_codigo(code, width):
    if not isinstance(code, str) or re.fullmatch('[0-9]{' + str(width) + '}', code) is None:
        raise ValueError('Código no textual o de ancho incorrecto: ' + repr(code))
    return code


def validar_estado_dictamen(variable, decision, aprobadas_posteriores):
    """True solo para una resolución posterior exacta; nunca promociona por sí misma."""
    definition = decision['definicion_iri']
    if (variable.get('definicion_iri') != definition or
            variable['huella_fila_diccionario'] != decision['huella_fila_diccionario']):
        raise ValueError('Evidencia de dictamen histórico cambió')
    if variable['estado'] == 'candidata_sin_definicion_suficiente':
        return False
    rule = aprobadas_posteriores.get(definition)
    if (rule and variable['estado'] == 'respaldada_por_definicion' and
            variable.get('regla') == rule['id'] and variable.get('concepto') == rule['concepto'] and
            rule['huella_fila_diccionario'] == decision['huella_fila_diccionario']):
        return True
    raise ValueError('Dictamen no corresponde a pendiente actual ni a resolución posterior aprobada')


def cargar_evidencia():
    config_path = ROOT / 'ontologia/revision-ronda-2.json'
    config = json.loads(config_path.read_text(encoding='utf-8'))
    path = ROOT / config['manifiesto']
    if sha(path) != config['sha256_manifiesto']:
        raise ValueError('Manifiesto de ronda 2 cambió')
    manifest = json.loads(path.read_text(encoding='utf-8'))
    sources = {'reglas_ronda_2': config_path, 'manifiesto_ronda_2': path}
    for relative, meta in manifest['archivos'].items():
        f = ROOT / relative
        if not f.resolve().is_relative_to(OUT.resolve()) or sha(f) != meta['sha256']:
            raise ValueError('Evidencia de ronda 2 cambió: ' + str(f))
        sources['ronda_2_' + relative] = f
    return config, manifest, sources


def construir(semantic, semantic_data, inventory, inspection, base):
    from consolidar_semantica import columnas
    config, manifest, sources = cargar_evidencia()

    def folder(agent):
        return OUT / 'entregas' / agent

    def read(agent, name='propuestas.json'):
        return json.loads((folder(agent) / name).read_text(encoding='utf-8'))

    g, model, mex = Graph(), Graph(), Namespace(base + 'vocab/')
    for graph in [g, model]:
        for prefix, ns in [('mex', mex), ('prov', PROV), ('skos', SKOS)]:
            graph.bind(prefix, ns)

    def node(kind, key):
        return URIRef(base + kind + '/' + quote(str(key), safe=''))

    def lit(subject, key, value):
        if value is not None:
            g.add((subject, mex[key], Literal(value)))

    def evidence(subject, path):
        g.add((subject, PROV.wasDerivedFrom, URIRef(path.as_uri())))

    classes = {'DictamenPendienteSemantico': 'Dictamen de pendiente semántico',
               'ContrasteLocalidadesCensales': 'Contraste IML 2020 con ITER 2020',
               'ComprobacionLocalidadCensal': 'Coincidencia observada IML e ITER',
               'RevisionVigenciaCatalogo': 'Revisión de vigencia de catálogo',
               'EvaluacionPipelineConsulta': 'Diagnóstico parcial del pipeline fuente de consulta',
               'ResultadoCasoEvaluacion': 'Resultado de caso de evaluación del pipeline fuente'}
    objects = {'objetoRevisado': 'Objeto de revisión', 'entradaLocalidadObservada': 'Entrada de localidad observada',
               'contrasteLocalidades': 'Contraste entre fuentes censales', 'referenciaDeclarada': 'Referencia declarada',
               'evaluacionConsulta': 'Evaluación de consulta a la que pertenece el caso'}
    literals = {'estadoDictamen': 'Estado de dictamen', 'tipoPendiente': 'Tipo de pendiente revisado',
                'preguntaPublicador': 'Pregunta preparada sin enviar al publicador',
                'evidenciaRevisionJson': 'Evidencia y alcance de revisión (JSON)',
                'estadoContraste': 'Estado de contraste entre dos fuentes',
                'fechaReferenciaCensal': 'Fecha de referencia declarada por ITER',
                'anioDeclaradoIML': 'Año declarado por IML', 'totalLocalidadesFuenteCensal': 'Localidades publicadas en ITER',
                'localidadesComprobadas': 'Localidades IML comprobadas contra ITER',
                'localidadesSoloFuenteCensal': 'Localidades publicadas solo en ITER',
                'sha256FuenteCensal': 'SHA-256 de la fuente censal', 'filaFuenteCensal': 'Fila del CSV censal',
                'claveCensalOriginal': 'Clave compuesta de componentes censales originales',
                'nombreCensalOriginal': 'Nombre censal original', 'nombreMunicipioCensalOriginal': 'Nombre municipal censal original',
                'poblacionCoincidente': 'Población coincidente en las dos fuentes examinadas',
                'estadoCoincidenciaCensal': 'Estado de coincidencia entre fuentes publicadas',
                'estadoVigenciaRevisada': 'Resultado de revisión de vigencia',
                'facetasVigenciaJson': 'Publicación, periodo, edición y aplicabilidad (JSON)',
                'fechaConsultaCkan': 'Fecha UTC de consulta de metadatos CKAN',
                'canalEvaluado': 'Canal evaluado', 'identidadBackend': 'Identidad con backend instalado',
                'estadoEvaluacionUI': 'Estado de evaluación de la interfaz', 'casosIntentados': 'Casos intentados',
                'respuestasModelo': 'Intentos con respuesta del modelo', 'aciertosEvaluacion': 'Aciertos observados',
                'fallosRecuperacion': 'Fallos observados de recuperación', 'intentosSinRespuesta': 'Intentos sin respuesta por HTTP o cuota',
                'estadoCasoEvaluacion': 'Estado observado del caso', 'preguntaEvaluacion': 'Pregunta de evaluación',
                'respuestaEsperada': 'Respuesta esperada en la instantánea evaluada',
                'respuestaObtenida': 'Respuesta obtenida del modelo', 'sha256GrafoAntesRonda2': 'SHA-256 del archivo de grafo previo a ronda 2'}
    for k, label in classes.items():
        model.add((mex[k], RDF.type, OWL.Class)).add((mex[k], RDFS.label, Literal(label, lang='es')))
    for fields, cls in [(objects, OWL.ObjectProperty), (literals, OWL.DatatypeProperty)]:
        for k, label in fields.items():
            model.add((mex[k], RDF.type, cls)).add((mex[k], RDFS.label, Literal(label, lang='es')))

    p1 = read('agente-1-correspondencias')
    variables = {v['definicion_iri']: v for v in semantic['variables']}
    cols = {c['iri']: c for c in columnas(inventory, inspection, base)}
    mappings = {m['columna']: m for m in semantic['correspondencias'] if m['estado'] == 'documental_revisada'}
    for p in p1['propuestas_revisadas']:
        c, v = cols[p['columna']], variables[p['definicion_iri']]
        if (mappings[p['columna']]['variable'] != p['variable_iri']
                or c['huella_esquema'] != p['huellas']['huella_esquema']
                or v['huella_fila_diccionario'] != p['huellas']['huella_fila_diccionario']
                or (c['recurso'], c['campo'], c['conjunto']) != (p['recurso'], p['campo'], p['conjunto'])):
            raise ValueError('Correspondencia de ronda 2 sin evidencia vigente')
        review = URIRef(mappings[p['columna']]['iri'])
        evidence(review, folder('agente-1-correspondencias') / 'propuestas.json')
        lit(review, 'evidenciaRevisionJson', json.dumps(p['evidencia_vinculo'], ensure_ascii=False))
    # The previously approved 162 records remain byte-for-byte equivalent JSON values.
    rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(ROOT / config['respaldo']) as archive:
        previous = json.loads(archive.read('ontologia/semantica.json'))
    if len(previous['vinculos_documentales_revisados']) != 162 or any(
            r not in rules['vinculos_documentales_revisados'] for r in previous['vinculos_documentales_revisados']):
        raise ValueError('Se alteró una revisión anterior a ronda 2')

    approved_later = {}
    if (ROOT / 'ontologia/revision-ronda-4.json').exists():
        from integrar_ronda_4 import validar
        _, _, _, r4, _ = validar(rules)
        approved_later = {definition: rule for rule in r4['reglas'] for definition in rule['definiciones']}
    p2 = read('agente-2-pendientes')
    questions = {q['id']: q for q in p2['preguntas_publicador']}
    for d in p2['decisiones']:
        review = node('pending-review-round-2', d['id'])
        g.add((review, RDF.type, mex.DictamenPendienteSemantico))
        g.add((review, RDFS.label, Literal(d['id'] + ' — ' + d['clasificacion'], lang='es')))
        lit(review, 'estadoDictamen', d['clasificacion']); lit(review, 'tipoPendiente', d['tipo'])
        lit(review, 'evidenciaRevisionJson', json.dumps(d, ensure_ascii=False))
        if d['tipo'] == 'significado':
            v = variables[d['definicion_iri']]
            if validar_estado_dictamen(v, d, approved_later):
                g.add((review, mex.limiteSemantico, Literal(
                    'Dictamen histórico de ronda 2: este significado fue respaldado después por una regla auditada de ronda 4. '
                    'La clasificación original se conserva como evidencia histórica; el estado vigente se consulta en la variable documentada.', lang='es')))
            target = URIRef(v['iri'])
        elif d['tipo'] == 'referencia_catalogo':
            target = URIRef(d['referencia_iri'])
        else:
            target = URIRef(d['columna_iri'])
            if cols[d['columna_iri']]['huella_esquema'] != d['huella_esquema']:
                raise ValueError('Esquema de pendiente revisado cambió')
        g.add((review, mex.objetoRevisado, target))
        evidence(review, folder('agente-2-pendientes') / 'propuestas.json')
        if d.get('pregunta_id'):
            lit(review, 'preguntaPublicador', questions[d['pregunta_id']]['texto'])
        g.add((review, mex.limiteSemantico, Literal('Dictamen documental; no promueve significado ni correspondencia. Preguntas preparadas, sin contactar al publicador.', lang='es')))

    p3 = read('agente-3-localidades-inegi', 'inegi-fuente.json')
    contrast = read('agente-3-localidades-inegi', 'contraste-localidades.json')
    zip_path = folder('agente-3-localidades-inegi') / 'fuentes' / p3['archivo_zip']
    if sha(zip_path) != p3['sha256_zip']:
        raise ValueError('Fuente ITER cambió')
    dataset = 'iter_26_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_26CSV20.csv'
    with zipfile.ZipFile(zip_path) as archive:
        csv_text = archive.read(dataset).decode('utf-8-sig')
    raw_rows = list(csv.DictReader(io.StringIO(csv_text)))
    if any(None in r or any(v is None for v in r.values()) for r in raw_rows):
        raise ValueError('CSV censal malformado')
    iter_rows, aggregates, specials = {}, 0, 0
    for rowno, row in enumerate(raw_rows, 2):
        ent = validar_codigo(row['ENTIDAD'], 2); mun = validar_codigo(row['MUN'], 3); loc = validar_codigo(row['LOC'], 4)
        if ent != '26':
            raise ValueError('Localidad fuera de Sonora')
        if mun == '000' or loc == '0000':
            aggregates += 1
            continue
        if loc in ['9998', '9999']:
            specials += 1
            continue
        code = ent + mun + loc
        if code in iter_rows:
            raise ValueError('Clave censal duplicada')
        iter_rows[code] = (rowno, row)
    iml_hash = contrast['fuente_iml']['sha256']
    iml_path = ROOT / 'data/integracion/fuentes' / (iml_hash + '.xlsx')
    table = leer_tabla(iml_path, 'IML_2020'); header = table[0]
    iml_rows = [(n, dict(zip(header, row))) for n, row in enumerate(table[1:], 2)]
    if (len(raw_rows), aggregates, specials, len(iter_rows), len(iml_rows)) != (7500, 75, 125, 7300, 1850):
        raise ValueError('Universos de contraste cambiaron')
    check_node = node('locality-census-comparison', iml_hash + '/' + p3['sha256_zip'])
    g.add((check_node, RDF.type, mex.ContrasteLocalidadesCensales))
    g.add((check_node, RDFS.label, Literal('Contraste completo de fuentes IML 2020 e ITER 2020: 1,850 coincidencias', lang='es')))
    for k, v in [('estadoContraste', 'contraste_completo_entre_dos_fuentes'), ('fechaReferenciaCensal', '2020-03-15'),
                 ('anioDeclaradoIML', '2020'), ('totalLocalidadesFuenteCensal', 7300), ('localidadesComprobadas', 1850),
                 ('localidadesSoloFuenteCensal', 5450), ('sha256FuenteCensal', p3['sha256_zip'])]:
        lit(check_node, k, v)
    limit = 'Coincidencia en estas fuentes publicadas; no catálogo cartográfico completo, identidad de universos ni idéntico corte IML. Sin asignación a otros recursos ni vigencia histórica general.'
    g.add((check_node, mex.limiteSemantico, Literal(limit, lang='es')))
    g.add((check_node, PROV.wasDerivedFrom, URIRef(p3['url_descarga'])))
    evidence(check_node, folder('agente-3-localidades-inegi') / 'contraste-localidades.json')
    observed_reference = node('observed-locality-reference', iml_hash + '/IML_2020')
    revised_status = Literal('cotejo_ITER_2020_disponible_sin_vigencia_general_acreditada')
    semantic_data.set((observed_reference, mex.estadoVigencia, revised_status))
    g.add((observed_reference, mex.estadoVigencia, revised_status))
    g.add((observed_reference, mex.contrasteLocalidades, check_node))
    seen = set()
    for iml_rowno, row in iml_rows:
        code = validar_codigo(row['CVE_LOC'], 9)
        if code in seen or code not in iter_rows:
            raise ValueError('Clave IML duplicada o ausente en ITER')
        seen.add(code)
        iter_rowno, original = iter_rows[code]
        if ((row['NOM_LOC'], row['NOM_MUN']) != (original['NOM_LOC'], original['NOM_MUN'])
                or int(row['POB_TOT']) != int(original['POBTOT'])):
            raise ValueError('Coincidencia censal dejó de coincidir: ' + code)
        review = node('locality-census-check', iml_hash + '/' + p3['sha256_zip'] + '/' + code)
        g.add((review, RDF.type, mex.ComprobacionLocalidadCensal))
        g.add((review, RDFS.label, Literal(code + ' — IML/ITER: clave, nombre y población coincidentes', lang='es')))
        g.add((review, mex.entradaLocalidadObservada, node('observed-locality', iml_hash + '/' + code)))
        g.add((review, mex.contrasteLocalidades, check_node))
        for k, v in [('claveCensalOriginal', code), ('nombreCensalOriginal', original['NOM_LOC']),
                     ('nombreMunicipioCensalOriginal', original['NOM_MUN']), ('filaFuenteCensal', iter_rowno),
                     ('filaOriginal', iml_rowno), ('poblacionCoincidente', int(row['POB_TOT'])),
                     ('fechaReferenciaCensal', '2020-03-15'),
                     ('estadoCoincidenciaCensal', 'clave_nombre_poblacion_coincidentes_en_fuentes')]:
            lit(review, k, v)
        g.add((review, PROV.wasDerivedFrom, URIRef(p3['url_descarga'])))
        g.add((review, PROV.wasDerivedFrom, URIRef('https://datos.sonora.gob.mx/dataset/b54f94ee-b5f1-404c-ab41-f19f6dcc8b4f/resource/8e684391-9137-4359-b654-f19602911421/download/indice-de-marginacion-localidades-2020.xlsx')))

    p4 = read('agente-4-vigencia', 'matriz-vigencia.json')
    for row in p4['referencias']:
        target = URIRef(row['referencia_iri'])
        if (target, mex.estadoReferenciaCatalogo, Literal('recurso_catalogo_identificado')) not in semantic_data:
            raise ValueError('Vigencia revisada de una referencia no identificada')
        if row['vigencia'] != 'no_acreditada':
            raise ValueError('Cambió el resultado de vigencia aprobado')
        review = node('catalog-validity-review-round-2', row['referencia_iri'].rsplit('/', 1)[-1])
        g.add((review, RDF.type, mex.RevisionVigenciaCatalogo))
        g.add((review, RDFS.label, Literal(row['titulo_conjunto'] + ' — vigencia no acreditada', lang='es')))
        g.add((review, mex.referenciaDeclarada, target))
        lit(review, 'estadoVigenciaRevisada', row['vigencia'])
        lit(review, 'fechaConsultaCkan', p4['fecha_consulta_ckan_utc'])
        lit(review, 'facetasVigenciaJson', json.dumps({k: row[k] for k in ['f1_ckan', 'f2_periodos_declarados', 'f3_edicion', 'f4_aplicabilidad']}, ensure_ascii=False))
        g.add((review, PROV.wasDerivedFrom, URIRef(row['f1_ckan']['paquete_url'])))
        evidence(review, folder('agente-4-vigencia') / 'matriz-vigencia.json')
        g.add((review, mex.limiteSemantico, Literal('No se localizó evidencia suficiente en el alcance documentado. La fecha CKAN no acredita edición ni aplicabilidad histórica. No_acreditada no significa inválida.', lang='es')))

    p5 = read('agente-5-evaluacion-chat', 'registro.json')
    scope = read('agente-5-evaluacion-chat', 'alcance.json')
    if len(p5) != 20 or len({x['id'] for x in p5}) != 20:
        raise ValueError('Evaluación sin 20 casos únicos')
    states = Counter(r['estado'] for r in p5)
    if states != Counter({'acierto': 2, 'fallo_recuperacion_contexto_parcial': 2, 'no_ejecutado_cuota_modelo': 16}):
        raise ValueError('Estados de evaluación diferentes de los aprobados')
    evaluation = node('query-pipeline-evaluation', config['sha256_manifiesto'])
    g.add((evaluation, RDF.type, mex.EvaluacionPipelineConsulta))
    g.add((evaluation, RDFS.label, Literal('Ronda 2: diagnóstico parcial del pipeline fuente, UI sin evaluar', lang='es')))
    for k, v in [('canalEvaluado', 'pipeline_fuente_GraphRAG_QA_Gemini_con_grafo_vivo'),
                 ('identidadBackend', 'no_demostrada_con_instalacion_Studio'), ('estadoEvaluacionUI', 'no_ejecutada'),
                 ('casosIntentados', 20), ('respuestasModelo', 4), ('aciertosEvaluacion', 2),
                 ('fallosRecuperacion', 2), ('intentosSinRespuesta', 16),
                 ('sha256GrafoAntesRonda2', config['sha256_grafo_previo'])]:
        lit(evaluation, k, v)
    lit(evaluation, 'evidenciaRevisionJson', json.dumps(scope, ensure_ascii=False))
    g.add((evaluation, mex.limiteSemantico, Literal('Diagnóstico histórico anterior a esta integración: 4 respuestas, 16 errores HTTP/cuota, sin evaluación UI ni identidad demostrada con el bundle instalado. No certifica el chat.', lang='es')))
    evidence(evaluation, folder('agente-5-evaluacion-chat') / 'registro.json')
    for case in p5:
        review = node('query-evaluation-case-round-2', config['sha256_manifiesto'] + '/' + case['id'])
        g.add((review, RDF.type, mex.ResultadoCasoEvaluacion)).add((review, mex.evaluacionConsulta, evaluation))
        g.add((review, RDFS.label, Literal(case['id'] + ' — ' + case['estado'], lang='es')))
        lit(review, 'estadoCasoEvaluacion', case['estado']); lit(review, 'preguntaEvaluacion', case['pregunta'])
        lit(review, 'respuestaEsperada', case['esperada'])
        if case.get('obtenida'):
            lit(review, 'respuestaObtenida', case['obtenida'])
        lit(review, 'evidenciaRevisionJson', json.dumps(case, ensure_ascii=False))
        evidence(review, folder('agente-5-evaluacion-chat') / 'respuestas_brutas' / (case['id'] + '.md'))

    summary = {'correspondencias_nuevas': len(p1['propuestas_revisadas']),
               'correspondencias_revisadas_totales': semantic['resumen']['estados_correspondencias']['documental_revisada'],
               'correspondencias_candidatas_restantes': semantic['resumen']['estados_correspondencias']['candidata_por_nombre'],
               'dictamenes_pendientes': len(p2['decisiones']), 'preguntas_no_enviadas': len(questions),
               'clasificaciones_dictamenes': dict(Counter(d['clasificacion'] for d in p2['decisiones'])),
               'coincidencias_iml_iter': len(seen), 'solo_iter': 5450, 'vigencias_no_acreditadas': len(p4['referencias']),
               'evaluacion_pipeline': {'intentos': 20, 'respuestas': 4, 'aciertos': 2, 'fallos_recuperacion': 2,
                                       'errores_http_cuota': 16, 'ui': 'no_ejecutada', 'identidad_backend': 'no_demostrada'},
               'respaldo': config['respaldo'], 'fuentes_fijadas': len(manifest['archivos'])}
    expected = dict(config.get('esperado_actual', config['esperado']))
    r6cfg = ROOT / 'ontologia/revision-ronda-6.json'
    if r6cfg.exists():
        # R6 añade como máximo su vínculo auditado; el esperado histórico queda intacto.
        r6exp = (json.loads(r6cfg.read_text(encoding='utf-8')).get('estados_correspondencias_esperados') or {})
        if 'documental_revisada' in r6exp:
            expected['revisadas'] = r6exp['documental_revisada']

    r7cfg = ROOT / 'ontologia/revision-ronda-7.json'
    if r7cfg.exists():
        # R7: revisadas y candidatas derivadas de baseline+accepted auditados
        # sobre anclas históricas intactas. Sin defaults ni observados.
        if not r6cfg.exists():
            raise ValueError('R7 exige su base R6 instalada')
        from integrar_ronda_7 import cargar as cargar_ronda_7
        r7config, r7folder, r7base, r7accepted, r7sources = cargar_ronda_7()
        sources.update({k: v for k, v in r7sources.items() if k not in sources})
        if (len(r7accepted['reglas']), len(r7accepted['vinculos']), len(r7accepted['conceptos'])) != (31, 3, 31):
            raise ValueError('R7 fuera del lote auditado 31/3/31')
        expected['revisadas'] = len(r7base['vinculos_documentales_revisados']) + len(r7accepted['vinculos'])
        if expected['revisadas'] != 4478:
            raise ValueError('R7 sin 4478 revisadas derivadas')
        expected['candidatas'] = config['esperado_actual']['candidatas'] - len(r7accepted['vinculos'])
        if expected['candidatas'] != 17:
            raise ValueError('R7 sin 17 candidatas derivadas')

    if (summary['correspondencias_revisadas_totales'], summary['correspondencias_candidatas_restantes'],
            len(seen), len(p2['decisiones']), len(p4['referencias'])) != (
            expected['revisadas'], expected['candidatas'], expected['comprobaciones_localidades'],
            expected['decisiones_pendientes'], expected['vigencias_no_acreditadas']):
        raise ValueError('Conteos inesperados de ronda 2')
    (OUT / 'ronda-2.ttl').write_text(g.serialize(format='turtle'), encoding='utf-8')
    (ROOT / 'reports/integracion-ronda-2.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Integración central — ronda 2 (antecedente histórico)', '',
             'Los conteos de las tablas describen el cierre original de ronda 2. La cobertura vigente se registra en reports/consolidacion-semantica.md y data/semantica/cobertura.json.', '',
             'Las cinco entregas se conservan como copias fijadas por SHA-256. Las carpetas originales no se modifican. La generación es sin red ni modelos.', '',
             '| Resultado | Cantidad |', '| --- | ---: |',
             '| Nuevas correspondencias documentales | 674 |', '| Correspondencias revisadas totales | 836 |',
             '| Correspondencias candidatas restantes | 118 |', '| Columnas ambiguas / vínculos | 3 / 6 |',
             '| Conceptos / variables respaldadas / significados candidatos | 103 / 232 / 23 |',
             '| Dictámenes de pendientes / preguntas sin enviar | 32 / 14 |',
             '| Coincidencias IML con ITER 2020: clave, nombre y población | 1850 |',
             '| Localidades publicadas solo en ITER | 5450 |', '| Revisiones de vigencia no acreditada | 16 |', '',
             '## Alcance por entrega', '',
             '- Agente 1: se conservan las 162 revisiones anteriores y se añaden 674. Las 21 diferencias por acento agudo se documentan por recurso. Año/ano permanece pendiente; no se crean alias globales ni conceptos nuevos. La revisión documental no valida valores ni vigencia.',
             '- Agente 2: 32 dictámenes calificados (23 requieren aclaración, 8 documentados con límite y un caso ya resuelto). Las 14 preguntas están preparadas, sin contactar al publicador. Los significados candidatos y las observaciones originales permanecen; los dictámenes no son promociones.',
             '- Agente 3: contraste completo de dos fuentes publicadas. Se separan 75 agregados y 125 especiales de 7300 localidades ITER; las 1850 claves IML tienen nombres y población idénticos, sin transformaciones. Se integra una comprobación por localidad, no identidad oficial ni asignación a otros conjuntos. ITER declara 2020-03-15; IML declara año 2020. El motivo de las 5450 exclusiones no queda acreditado y no se cotejó el Marco Geoestadístico.',
             '- Agente 4: 16 revisiones de aplicabilidad temporal no acreditada, con fechas CKAN, periodos declarados, edición y aplicabilidad separados. Se conserva la evidencia primaria CMPE 2016 sin atribuir adopción por periodo ni vigencia a UTH. No_acreditada no significa inválida.',
             '- Agente 5: diagnóstico histórico PARCIAL del pipeline fuente contra el grafo vivo previo a esta integración: 20 intentos, 4 respuestas (2 aciertos y 2 fallos de recuperación), 16 intentos con error HTTP/cuota. UI no evaluada; identidad con el backend instalado no demostrada. No se relanzaron modelos ni se corrigió el chat. Las expectativas y consultas guardadas conservan los conteos anteriores 162/792; son evidencia histórica, no los conteos actuales.', '',
             '## Reproducción y pendientes', '',
             'ontologia/revision-ronda-2.json fija data/integracion-ronda-2/manifiesto.json. scripts/ampliar_portal.py --load regenera y valida el grafo; scripts/sincronizar_studio_portal.py respalda y conserva las ediciones ajenas a la ampliación.', '',
             'Al cerrar esta ronda quedaron 23 significados candidatos, 118 correspondencias candidatas, 3 columnas ambiguas/6 vínculos, des_mpo_res sin resolver, vigencia histórica no acreditada y pruebas pendientes de UI/16 preguntas sin respuesta. Entonces 1308 definiciones estaban fuera del núcleo; las ampliaciones posteriores se documentan en la cobertura vigente. Esta ronda no ejecutó nuevos cruces ni creó owl:sameAs/skos:exactMatch.', '',
             'Respaldo central previo: ' + config['respaldo'], '']
    (ROOT / 'reports/integracion-ronda-2.md').write_text('\n'.join(lines), encoding='utf-8')
    return g, model, summary, sources
