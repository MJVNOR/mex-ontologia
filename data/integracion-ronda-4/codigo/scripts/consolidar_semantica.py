"""Consolida conceptos, variables documentadas y correspondencias sin ejecutar cruces."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import tomllib
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS, URIRef, XSD, DCTERMS as DCT
from construir_catalogo import ROOT, PROV
from integrar_contenido import clave, valor
from mapear_cruces import clasificar

OUT = ROOT / 'data/semantica'
RULES = ROOT / 'ontologia/semantica.json'


def huella(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def validar_calificador(raw):
    """Conserva dimensiones y valores documentales sin normalizar códigos."""
    if not isinstance(raw, dict) or not raw:
        raise ValueError('Calificador documental debe ser un objeto no vacío')
    if any(not isinstance(k, str) or not k.strip() or
           not isinstance(v, str) or not v.strip() for k, v in raw.items()):
        raise ValueError('Dimensión y valor del calificador deben ser textos no vacíos')
    return dict(raw)


@lru_cache(maxsize=16384)
def _clave_literal(text):
    """Normaliza un literal; la caché depende del texto, no de reglas mutables."""
    return clave(text)


def interpretacion(name, description, dataset, rules, dictionary=None, definition=None):
    normalized_description, normalized_name = _clave_literal(str(description)), _clave_literal(str(name))
    matches = [r for r in rules['reglas_descripcion_exacta'] if normalized_description in {_clave_literal(str(d)) for d in r['descripciones']}
               and (not r.get('nombres') or normalized_name in {_clave_literal(str(n)) for n in r['nombres']})
               and (not r.get('conjuntos') or dataset in r['conjuntos'])
               and (not r.get('diccionarios') or dictionary in r['diccionarios'])
               and (not r.get('definiciones') or definition in r['definiciones'])]
    if len(matches) > 1:
        raise ValueError('Reglas semánticas en conflicto: ' + str([r['id'] for r in matches]))
    if matches:
        rule = matches[0]
        assignment = {'estado': 'respaldada_por_definicion', 'concepto': rule['concepto'],
                      'regla': rule['id'], 'representacion': rule['representacion']}
        if 'calificador' in rule:
            assignment['calificador'] = validar_calificador(rule['calificador'])
        limits = rule.get('limites', [])
        if isinstance(limits, str):
            limits = [limits]
        limits = [*limits, *([rule['limite']] if rule.get('limite') else [])]
        if limits:
            assignment['limites'] = list(dict.fromkeys(limits))
        if rule.get('fuente_revision'):
            assignment['fuente_revision'] = rule['fuente_revision']
        return assignment
    family = clasificar(name, description)
    suggestions = {'municipio': 'municipio', 'entidad': 'entidad', 'localidad': 'localidad', 'clave_geoestadistica': 'territorio',
                   'anio': 'anio', 'mes': 'tiempo', 'periodo': 'tiempo', 'programa_educativo': 'programa-educativo',
                   'dependencia_nombre': 'organizacion', 'plantel_nombre': 'organizacion', 'unidad_salud_clues': 'unidad-salud'}
    concept = suggestions.get(family['familia']) if family else None
    if concept:
        return {'estado': 'candidata_sin_definicion_suficiente', 'concepto': concept,
                'regla': 'pista_nombre_o_clasificador_sin_promocion', 'representacion': 'no_especificada'}
    return {'estado': 'fuera_del_nucleo_actual'}


def columnas(inventory, inspection, base):
    resources = {r['id']: r for r in inventory['recursos']}
    cols = []
    for result in inspection['recursos']:
        r = resources[result['id']]
        if r['clasificacion'] == 'diccionario' or not result['ok']:
            continue
        if r.get('datastore', {}).get('ok'):
            fields = [f for f in r['datastore']['campos'] if not f['id'].startswith('_')]
            schema_hash = huella([{'nombre': f['id'], 'tipo': f.get('type')} for f in fields])
            for field in fields:
                cols.append({'iri': base + 'column/' + r['id'] + '/' + quote(field['id'], safe=''),
                             'campo': field['id'], 'recurso': r['id'], 'conjunto': r['conjunto_id'],
                             'fuente': r['datastore']['url'], 'huella_esquema': schema_hash,
                             'nombre_unico': sum(clave(f['id']) == clave(field['id']) for f in fields) == 1})
        for table in result.get('tablas', []):
            for field in table['campos']:
                cols.append({'iri': base + 'file-column/' + quote(r['id'] + '/' + table['hoja'] + '/' + str(field['posicion_original']), safe=''),
                             'campo': field['id'], 'recurso': r['id'], 'conjunto': r['conjunto_id'],
                             'fuente': result.get('fuente') or r['url'], 'huella_esquema': huella(table),
                             'nombre_unico': sum(clave(f['id']) == clave(field['id']) for f in table['campos']) == 1})
    return cols


def construir(inventory, inspection, rules, reference, base):
    mex, g, model = Namespace(base + 'vocab/'), Graph(), Graph()
    for graph in (g, model):
        for prefix, ns in [('mex', mex), ('skos', SKOS), ('prov', PROV), ('dct', DCT)]:
            graph.bind(prefix, ns)
    def node(kind, id_):
        return URIRef(base + kind + '/' + quote(str(id_), safe=''))
    def concept(id_):
        return node('concept', id_)
    rules_uri = URIRef(RULES.as_uri())
    scheme = node('concept-scheme', 'nucleo-compartido')
    model.add((scheme, RDF.type, SKOS.ConceptScheme)).add((scheme, RDFS.label, Literal('Conceptos compartidos de MEX-Ontologi', lang='es')))
    model.add((scheme, SKOS.note, Literal(rules['alcance'], lang='es')))
    model.add((scheme, PROV.wasDerivedFrom, rules_uri))
    classes = {'ConceptoCompartido': 'Concepto compartido', 'VariableDocumentada': 'Variable documentada',
               'CorrespondenciaSemantica': 'Correspondencia semántica de columna', 'ReferenciaCatalogoDeclarada': 'Referencia a catálogo declarada',
               'SistemaIdentificadores': 'Sistema de identificadores observado', 'EntradaCatalogo': 'Entrada de catálogo de códigos',
               'MunicipioSegunFuente': 'Municipio según referencia del portal', 'CondicionConexion': 'Condición para conectar información',
               'CalificadorDocumental': 'Calificador documental de variable'}
    for key, label in classes.items():
        model.add((mex[key], RDF.type, OWL.Class)).add((mex[key], RDFS.label, Literal(label, lang='es')))
    model.add((mex.ConceptoCompartido, RDFS.subClassOf, SKOS.Concept))
    model.add((mex.EntradaCatalogo, RDFS.subClassOf, SKOS.Concept))
    objects = {'variableDocumentada': 'Variable documentada del conjunto', 'definicionOriginal': 'Definición original de la variable',
               'significadoDocumentado': 'Significado respaldado por definición documental', 'significadoCandidato': 'Significado candidato sin confirmar',
               'columnaOrigen': 'Columna de origen de la correspondencia', 'variableDestino': 'Variable documental de destino',
               'catalogoDeclarado': 'Referencia a catálogo declarada por la fuente', 'requiereCondicion': 'Condición necesaria para conectar',
               'requiereDistinguirDe': 'Sentido que debe distinguirse', 'usaSistemaIdentificadores': 'Sistema de identificadores observado en esta columna',
               'denotaMunicipioFuente': 'Municipio identificado por la entrada en esta referencia',
               'tieneCalificadorDocumentado': 'Calificador documental de la variable'}
    literals = {'estadoSemantico': 'Estado de interpretación semántica', 'reglaSemantica': 'Regla de interpretación documentada',
                'representacionDocumentada': 'Representación documental de la variable', 'tipoDatoOriginal': 'Tipo de dato declarado original',
                'unidadOriginal': 'Unidad original sin homologar', 'nombreVariableLocal': 'Nombre de variable local',
                'estadoCorrespondencia': 'Estado de correspondencia entre columna y variable', 'evidenciaTextual': 'Definición textual usada como evidencia',
                'nombreCatalogoDeclarado': 'Nombre de catálogo declarado', 'estadoReferenciaCatalogo': 'Estado de resolución del catálogo',
                'limiteSemantico': 'Límite de interpretación', 'patronCodigo': 'Patrón de código observado',
                'componenteEntidad': 'Componente entidad del código', 'componenteMunicipio': 'Componente municipio del código',
                'criterioRevision': 'Criterio de revisión documental de esta correspondencia',
                'dimensionCalificador': 'Dimensión del calificador documental', 'valorCalificador': 'Valor del calificador documental',
                'sha256Evidencia': 'Huella SHA-256 de la evidencia fijada',
                'huellaEsquemaRevisado': 'Huella del esquema revisado', 'huellaFilaDiccionario': 'Huella de la fila del diccionario revisada'}
    for mapping, cls in [(objects, OWL.ObjectProperty), (literals, OWL.DatatypeProperty)]:
        for key, label in mapping.items():
            model.add((mex[key], RDF.type, cls)).add((mex[key], RDFS.label, Literal(label, lang='es')))
    ontology = node('ontology', 'nucleo-semantico')
    model.add((ontology, RDF.type, OWL.Ontology)).add((ontology, RDFS.label, Literal('Núcleo semántico de MEX-Ontologi', lang='es')))
    model.add((ontology, PROV.wasDerivedFrom, rules_uri))
    for id_, (label, definition, broader) in rules['conceptos'].items():
        c = concept(id_)
        model.add((c, RDF.type, SKOS.Concept)).add((c, RDF.type, mex.ConceptoCompartido))
        model.add((c, SKOS.prefLabel, Literal(label, lang='es'))).add((c, RDFS.label, Literal(label, lang='es')))
        model.add((c, SKOS.definition, Literal(definition, lang='es'))).add((c, SKOS.inScheme, scheme))
        model.add((c, PROV.wasDerivedFrom, rules_uri))
        if broader:
            if broader not in rules['conceptos']:
                raise ValueError('Concepto más amplio inexistente: ' + broader)
            model.add((c, SKOS.broader, concept(broader)))
        else:
            model.add((scheme, SKOS.hasTopConcept, c))
        for condition in rules['condiciones']:
            model.add((c, mex.requiereCondicion, node('connection-condition', condition)))
    for id_, text in rules['condiciones'].items():
        condition = node('connection-condition', id_)
        model.add((condition, RDF.type, mex.CondicionConexion)).add((condition, RDFS.label, Literal('Comprobar ' + id_, lang='es')))
        model.add((condition, DCT.description, Literal(text, lang='es'))).add((condition, PROV.wasDerivedFrom, rules_uri))
    for a, b in [('municipio-registro', 'municipio-residencia'), ('municipio-registro', 'municipio-defuncion'),
                 ('anio-registro', 'anio-defuncion'), ('organizacion-publicadora', 'organizacion-capturadora'),
                 *rules.get('distinciones', [])]:
        if a not in rules['conceptos'] or b not in rules['conceptos']:
            raise ValueError('Distinción refiere un concepto inexistente')
        model.add((concept(a), mex.requiereDistinguirDe, concept(b)))
        model.add((concept(b), mex.requiereDistinguirDe, concept(a)))
    resources = {r['id']: r for r in inventory['recursos']}
    observations = rules.get('observaciones_revision', [])
    variable_notes = {(n['diccionario'], clave(n['variable'])) for n in observations if n.get('diccionario')}
    variables, lookup, declared_refs, all_names = [], defaultdict(list), set(), Counter()
    total_rows, no_name = 0, 0
    for result in inspection['recursos']:
        r = resources[result['id']]
        if r['clasificacion'] != 'diccionario' or not result['ok']:
            continue
        for index, row in enumerate(result.get('definiciones', []), 1):
            total_rows += 1
            name = valor(row, {'nombre variable', 'nombre de variable', 'variable', 'nombre campo', 'nombre del campo'})
            if not name:
                no_name += 1
                continue
            all_names[(r['conjunto_id'], clave(name))] += 1
            description = valor(row, {'descripcion', 'definicion'})
            assignment = interpretacion(name, description, r['conjunto_id'], rules,
                                       r['id'], str(node('definition', r['id'] + '/' + str(index))))
            catalog = valor(row, {'catalogo de referencia', 'catalago de referencia'})
            valid_catalog = clave(catalog) not in {'', 'n/a', 'na', 'no aplica', '-', 'ninguno'}
            record = {'conjunto': r['conjunto_id'], 'titulo_conjunto': r['conjunto'], 'diccionario': r['id'], 'variable': name,
                      'descripcion': description, **assignment, 'catalogo_declarado': catalog, 'huella_fila_diccionario': huella(row),
                      'definicion_iri': str(node('definition', r['id'] + '/' + str(index)))}
            if assignment['estado'] == 'fuera_del_nucleo_actual' and not valid_catalog and (r['id'], clave(name)) not in variable_notes:
                variables.append(record)
                continue
            definition = node('definition', r['id'] + '/' + str(index))
            variable = node('documented-variable', r['id'] + '/' + str(index))
            record.update(iri=str(variable), definicion_iri=str(definition))
            variables.append(record)
            lookup[(r['conjunto_id'], clave(name))].append(record)
            g.add((variable, RDF.type, mex.VariableDocumentada))
            g.add((variable, RDFS.label, Literal(name + ' — ' + r['conjunto'], lang='es')))
            g.add((variable, mex.nombreVariableLocal, Literal(name)))
            g.add((variable, mex.definicionOriginal, definition)).add((variable, PROV.wasDerivedFrom, definition))
            g.add((node('dataset', r['conjunto_id']), mex.variableDocumentada, variable))
            g.add((variable, mex.estadoSemantico, Literal(assignment['estado'])))
            if description:
                g.add((variable, DCT.description, Literal(description, lang='es')))
            for key, prop in [('tipo de dato', mex.tipoDatoOriginal), ('unidad de medida', mex.unidadOriginal)]:
                raw = valor(row, {key, 'unidades de medida'} if key == 'unidad de medida' else {key})
                if raw:
                    g.add((variable, prop, Literal(raw)))
            if assignment.get('concepto'):
                prop = mex.significadoDocumentado if assignment['estado'] == 'respaldada_por_definicion' else mex.significadoCandidato
                g.add((variable, prop, concept(assignment['concepto'])))
                g.add((variable, mex.reglaSemantica, Literal(assignment['regla'])))
                g.add((variable, mex.representacionDocumentada, Literal(assignment['representacion'])))
                g.add((variable, PROV.wasDerivedFrom, rules_uri))
            for dimension, value in assignment.get('calificador', {}).items():
                qualifier = node('documented-qualifier', r['id'] + '/' + str(index) + '/' + dimension)
                g.add((variable, mex.tieneCalificadorDocumentado, qualifier))
                g.add((qualifier, RDF.type, mex.CalificadorDocumental))
                g.add((qualifier, RDFS.label, Literal(dimension + ': ' + value, lang='es')))
                g.add((qualifier, mex.dimensionCalificador, Literal(dimension, datatype=XSD.string)))
                g.add((qualifier, mex.valorCalificador, Literal(value, datatype=XSD.string)))
                g.add((qualifier, PROV.wasDerivedFrom, definition))
                g.add((qualifier, PROV.wasDerivedFrom, rules_uri))
            for limit in assignment.get('limites', []):
                g.add((variable, mex.limiteSemantico, Literal(limit, lang='es')))
            if assignment.get('fuente_revision'):
                source = (ROOT / assignment['fuente_revision']).resolve()
                if not source.is_relative_to(ROOT.resolve()):
                    raise ValueError('Fuente de revisión fuera del proyecto')
                g.add((variable, PROV.wasDerivedFrom, URIRef(source.as_uri())))
            if valid_catalog:
                refid = hashlib.sha256((r['conjunto_id'] + '\n' + catalog).encode()).hexdigest()
                ref = node('declared-code-reference', refid)
                declared_refs.add(ref)
                g.add((variable, mex.catalogoDeclarado, ref))
                g.add((ref, RDF.type, mex.ReferenciaCatalogoDeclarada)).add((ref, RDFS.label, Literal(catalog + ' — ' + r['conjunto'], lang='es')))
                g.add((ref, mex.nombreCatalogoDeclarado, Literal(catalog)))
                g.add((ref, mex.estadoReferenciaCatalogo, Literal('solo_referencia_declarada_sin_resolver')))
                g.add((ref, PROV.wasDerivedFrom, definition))
    # All candidates remain qualified statements; no generic column→concept assertion is created.
    links, verified = [], set()
    revisions = rules.get('vinculos_documentales_revisados', [])
    manual = {(r['recurso'], r['campo'], r.get('columna')): r for r in revisions}
    if len(manual) != len(revisions):
        raise ValueError('Revisiones documentales duplicadas')
    cols = columnas(inventory, inspection, base)
    for col in cols:
        exact_key = (col['recurso'], col['campo'], col['iri'])
        fallback_key = (col['recurso'], col['campo'], None)
        revision_key = exact_key if exact_key in manual else fallback_key
        revision = manual.get(revision_key)
        # An alias is accepted only for an explicitly reviewed physical column.
        variable_name = revision.get('variable', col['campo']) if revision else col['campo']
        if revision and variable_name != col['campo'] and not revision.get('columna'):
            raise ValueError('Un alias revisado requiere la IRI de la columna física')
        matches = lookup.get((col['conjunto'], clave(variable_name)), [])
        definition_pin = revision.get('definicion_iri') if revision else None
        if definition_pin:
            if not revision.get('columna') or not all(revision.get(k) for k in ('huella_esquema', 'huella_fila_diccionario', 'descripcion', 'criterio')):
                raise ValueError('Selección de definición requiere columna física y evidencia completa')
            matches = [v for v in matches if v['definicion_iri'] == definition_pin]
        if not matches:
            continue
        if revision:
            name_ambiguous = (all_names[(col['conjunto'], clave(variable_name))] != 1 or not col['nombre_unico']) and not definition_pin
            if len(matches) != 1 or name_ambiguous or matches[0]['diccionario'] != revision['diccionario'] or matches[0].get('concepto') != revision['concepto'] or matches[0]['estado'] != 'respaldada_por_definicion':
                raise ValueError('Correspondencia revisada dejó de coincidir: ' + str(revision))
            for key, observed in [('huella_esquema', col['huella_esquema']),
                                  ('huella_fila_diccionario', matches[0]['huella_fila_diccionario']),
                                  ('descripcion', matches[0]['descripcion'])]:
                if key in revision and revision[key] != observed:
                    raise ValueError('Evidencia de revisión cambió: ' + key + ' en ' + col['iri'])
            verified.add(revision_key)
        for match in matches:
            status = ('documental_revisada' if revision else 'ambigua_por_nombre' if all_names[(col['conjunto'], clave(col['campo']))] != 1 or not col['nombre_unico'] else 'candidata_por_nombre')
            mid = hashlib.sha256((col['iri'] + '\n' + match['iri']).encode()).hexdigest()
            mapping = node('semantic-mapping', mid)
            g.add((mapping, RDF.type, mex.CorrespondenciaSemantica))
            g.add((mapping, RDFS.label, Literal(col['campo'] + ' — ' + resources[col['recurso']]['conjunto'], lang='es')))
            g.add((mapping, mex.columnaOrigen, URIRef(col['iri']))).add((mapping, mex.variableDestino, URIRef(match['iri'])))
            g.add((mapping, mex.estadoCorrespondencia, Literal(status)))
            if match['descripcion']:
                g.add((mapping, mex.evidenciaTextual, Literal(match['descripcion'], lang='es')))
            g.add((mapping, PROV.wasDerivedFrom, URIRef(match['definicion_iri'])))
            g.add((mapping, PROV.wasDerivedFrom, URIRef(col['fuente'])))
            if revision:
                g.add((mapping, PROV.wasDerivedFrom, rules_uri))
                g.add((mapping, mex.criterioRevision, Literal(revision.get('criterio', 'Revisión documental explícita de esta columna y su diccionario.'), lang='es')))
                g.add((mapping, mex.huellaEsquemaRevisado, Literal(col['huella_esquema'])))
                g.add((mapping, mex.huellaFilaDiccionario, Literal(match['huella_fila_diccionario'])))
                g.add((mapping, mex.limiteSemantico, Literal('Confirma la interpretación documental de esta columna; no valida filas, catálogos, unidades ni equivalencia con otras fuentes.', lang='es')))
                g.add((URIRef(col['iri']), mex.significadoDocumentado, concept(match['concepto'])))
            links.append({'iri': str(mapping), 'columna': col['iri'], 'campo': col['campo'], 'recurso': col['recurso'],
                          'variable': match['iri'], 'concepto': match.get('concepto'), 'estado': status,
                          'revision': revision, 'evidencia_textual': match['descripcion']})
    if verified != set(manual):
        raise ValueError('No se encontraron todas las columnas revisadas: ' + str(set(manual) - verified))
    for note in observations:
        targets = [URIRef(c['iri']) for c in cols if c['recurso'] == note['recurso'] and c['campo'] == note['campo']]
        if len(targets) != 1:
            raise ValueError('Observación sin columna única: ' + note['id'])
        if note.get('diccionario'):
            vs = [v for v in variables if v['diccionario'] == note['diccionario'] and clave(v['variable']) == clave(note['variable'])]
            if len(vs) != 1 or vs[0]['huella_fila_diccionario'] != note['huella_fila_diccionario']:
                raise ValueError('Evidencia de observación cambió: ' + note['id'])
            targets.append(URIRef(vs[0]['iri']))
        for target in targets:
            g.add((target, mex.limiteSemantico, Literal(note['observacion'], lang='es')))
            g.add((target, PROV.wasDerivedFrom, rules_uri))
    system_count = 0
    # Only this concrete field has a verified identifier-system binding from recovered reference data.
    if reference and reference.get('ok'):
        entries = reference['municipios']
        if len(entries) != 72 or {e['cvegeo'] for e in entries} != {'26' + str(i).zfill(3) for i in range(1, 73)}:
            raise ValueError('Referencia municipal inconsistente o duplicada')
        system = node('identifier-system', 'geojson-' + reference['recurso_id'])
        system_count += 1
        g.add((system, RDF.type, mex.SistemaIdentificadores)).add((system, RDF.type, SKOS.ConceptScheme))
        g.add((system, RDFS.label, Literal('CVEGEO municipal según GeoJSON del portal', lang='es')))
        g.add((system, mex.patronCodigo, Literal('26 + tres dígitos de municipio')))
        g.add((system, PROV.wasDerivedFrom, URIRef(reference['fuente'])))
        g.add((system, mex.limiteSemantico, Literal('Consistencia interna de esta referencia; no prueba que otros códigos locales usen el mismo sistema.', lang='es')))
        for row in entries:
            if row['cvegeo'] != row['cve_ent'] + row['cve_mun'] or row['cve_ent'] != '26' or not row['nombre'].strip():
                raise ValueError('Componentes de CVEGEO inconsistentes')
            entry = node('code-entry', reference['recurso_id'] + '/' + row['cvegeo'])
            territory = node('municipality-source', reference['recurso_id'] + '/' + row['cvegeo'])
            g.add((entry, RDF.type, mex.EntradaCatalogo)).add((entry, RDF.type, SKOS.Concept))
            g.add((entry, SKOS.inScheme, system)).add((entry, SKOS.notation, Literal(row['cvegeo'])))
            g.add((entry, RDFS.label, Literal(row['cvegeo'] + ' — ' + row['nombre'], lang='es')))
            g.add((entry, mex.componenteEntidad, Literal(row['cve_ent']))).add((entry, mex.componenteMunicipio, Literal(row['cve_mun'])))
            g.add((entry, mex.denotaMunicipioFuente, territory)).add((entry, PROV.wasDerivedFrom, URIRef(reference['fuente'])))
            g.add((territory, RDF.type, mex.MunicipioSegunFuente)).add((territory, RDFS.label, Literal(row['nombre'], lang='es')))
            g.add((territory, PROV.wasDerivedFrom, URIRef(reference['fuente'])))
        actual_columns = [c for c in cols if c['recurso'] == reference['recurso_id'] and c['campo'] == 'CVEGEO']
        if len(actual_columns) != 1:
            raise ValueError('Columna CVEGEO de la referencia no identificada de forma única')
        g.add((URIRef(actual_columns[0]['iri']), mex.usaSistemaIdentificadores, system))
        g.add((URIRef(actual_columns[0]['iri']), mex.significadoDocumentado, concept('municipio')))
    report = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'conceptos': rules['conceptos'],
              'resumen': {'definiciones_con_nombre_examinadas': len(variables), 'filas_sin_nombre': no_name,
                          'estados_variables': dict(Counter(v['estado'] for v in variables)),
                          'variables_materializadas': sum('iri' in v for v in variables),
                          'estados_correspondencias': dict(Counter(m['estado'] for m in links)), 'columnas_totales_examinadas': len(cols),
                          'columnas_con_correspondencia': len({m['columna'] for m in links}),
                          'conceptos_compartidos': len(rules['conceptos']), 'referencias_catalogo_sin_resolver': len(declared_refs),
                          'sistemas_identificadores_recuperados': system_count, 'condiciones_conexion': len(rules['condiciones'])},
              'variables': variables, 'correspondencias': links, 'observaciones_revision': observations}
    return g, model, report


def generar():
    sources = {'reglas': RULES, 'inventario': ROOT / 'data/portal/inventario.json',
               'inspeccion': ROOT / 'data/portal/contenido-inspeccion.json'}
    reference_path = ROOT / 'data/portal/lote-cruces/catalogo-municipal-portal.json'
    reference = None
    if reference_path.exists():
        sources['referencia_municipal'] = reference_path
        reference = json.loads(reference_path.read_text(encoding='utf-8'))
    rules, inventory, inspection = [json.loads(sources[key].read_text(encoding='utf-8')) for key in ('reglas', 'inventario', 'inspeccion')]
    if (ROOT / 'ontologia/revision-cobertura.json').exists():
        from integrar_cobertura import cargar_evidencia
        cargar_evidencia(rules)
    if {r['id'] for r in inventory['recursos']} != {r['id'] for r in inspection['recursos']}:
        raise ValueError('Inventario e inspección no coinciden')
    base = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']
    data, model, report = construir(inventory, inspection, rules, reference, base)
    territorial_rules = ROOT / 'ontologia/territorio.json'
    if territorial_rules.exists():
        from integrar_territorio import construir as construir_territorio, documentar as documentar_territorio
        sources['reglas_territoriales'] = territorial_rules
        sources['catalogos_territoriales'] = ROOT / 'data/territorio/catalogos.json'
        catalogs = json.loads(sources['catalogos_territoriales'].read_text(encoding='utf-8'))
        for key in ['inventario', 'inspeccion']:
            if catalogs['huellas_entrada'][key] != hashlib.sha256(sources[key].read_bytes()).hexdigest():
                raise ValueError('Inventario de catálogos territoriales desactualizado: ' + key)
        for ref in catalogs['referencias']:
            path = (ROOT / ref['archivo']).resolve()
            if not path.is_relative_to((ROOT / 'data/territorio/fuentes').resolve()):
                raise ValueError('Fuente territorial fuera de su carpeta')
            if hashlib.sha256(path.read_bytes()).hexdigest() != ref['archivo_sha256']:
                raise ValueError('Archivo de catálogo cambió: ' + ref['recurso'])
            sources['catalogo_' + ref['recurso']] = path
        territorial_data, territorial_model, territorial_report = construir_territorio(
            catalogs, json.loads(territorial_rules.read_text(encoding='utf-8')), inventory, report, reference, base)
        mex = Namespace(base + 'vocab/')
        for resolution in territorial_report['resoluciones']:
            declared = URIRef(resolution['referencia_declarada'])
            if (declared, RDF.type, mex.ReferenciaCatalogoDeclarada) not in data:
                raise ValueError('Referencia declarada inexistente al resolver catálogo')
            data.set((declared, mex.estadoReferenciaCatalogo, Literal('recurso_catalogo_identificado')))
        data += territorial_data
        model += territorial_model
        report['territorio'] = territorial_report
        report['resumen']['referencias_catalogo_sin_resolver'] = len(set(data.subjects(mex.estadoReferenciaCatalogo, Literal('solo_referencia_declarada_sin_resolver'))))
        report['resumen']['referencias_catalogo_con_recurso_identificado'] = len(territorial_report['resoluciones'])
        (ROOT / 'data/territorio/territorio.ttl').write_text(territorial_data.serialize(format='turtle'), encoding='utf-8')
        (ROOT / 'data/territorio/verificacion.json').write_text(json.dumps(territorial_report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        documentar_territorio(territorial_report)
    if (ROOT / 'ontologia/revision-agentes.json').exists():
        from integrar_entregas import construir as integrar_entregas
        reviewed_data, reviewed_model, reviewed_report, reviewed_sources = integrar_entregas(
            report, data, inventory, inspection, base)
        data += reviewed_data
        model += reviewed_model
        report['integracion_agentes'] = reviewed_report
        sources.update(reviewed_sources)
        mex = Namespace(base + 'vocab/')
        report['resumen']['referencias_catalogo_sin_resolver'] = len(set(data.subjects(
            mex.estadoReferenciaCatalogo, Literal('solo_referencia_declarada_sin_resolver'))))
        report['resumen']['referencias_catalogo_con_recurso_identificado'] = len(set(data.subjects(
            mex.estadoReferenciaCatalogo, Literal('recurso_catalogo_identificado'))))
    if (ROOT / 'ontologia/revision-ronda-2.json').exists():
        from integrar_ronda_2 import construir as integrar_ronda_2
        round_data, round_model, round_report, round_sources = integrar_ronda_2(
            report, data, inventory, inspection, base)
        data += round_data
        model += round_model
        report['integracion_ronda_2'] = round_report
        sources.update(round_sources)
    if (ROOT / 'ontologia/revision-cobertura.json').exists():
        from integrar_cobertura import construir as integrar_cobertura
        coverage_data, coverage_report, coverage_sources = integrar_cobertura(report, rules, base)
        data += coverage_data
        report['integracion_cobertura'] = coverage_report
        sources.update(coverage_sources)
    if (ROOT / 'ontologia/revision-ronda-3.json').exists():
        from integrar_ronda_3 import construir as integrar_ronda_3
        r3_data, r3_report, r3_sources = integrar_ronda_3(report, rules, base)
        data += r3_data
        report['integracion_ronda_3'] = r3_report
        sources.update(r3_sources)
    if (ROOT / 'ontologia/revision-ronda-4.json').exists():
        from integrar_ronda_4 import construir as integrar_ronda_4
        r4_data, r4_report, r4_sources = integrar_ronda_4(report, rules, base)
        data += r4_data
        report['integracion_ronda_4'] = r4_report
        sources.update(r4_sources)
    report['huellas_entrada'] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}
    from auditar_semantica import auditar
    report['auditoria_cobertura'] = auditar(report, inventory, columnas(inventory, inspection, base))
    OUT.mkdir(parents=True, exist_ok=True)
    from guardar_rdf import serializar_atomico
    serializar_atomico(data, OUT / 'interpretaciones.ttl')
    serializar_atomico(model, OUT / 'nucleo.ttl')
    (OUT / 'cobertura.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    documentar(report)
    return data, model, report


def documentar(report):
    s = report['resumen']
    lines = ['# Consolidación semántica del portal', '',
             'Este módulo describe significados documentales, referencias y condiciones de conexión. No ejecuta cruces, no agrega filas ni convierte coincidencias de nombres en equivalencias.', '',
             'Fecha UTC: ' + report['generado_en_utc'], '', '| Indicador | Resultado |', '| --- | ---: |']
    for key, value in s.items():
        if not isinstance(value, dict):
            lines.append(f'| {key} | {value} |')
    for title, key in [('Interpretación de variables', 'estados_variables'), ('Correspondencia columna–variable', 'estados_correspondencias')]:
        lines += ['', '## ' + title, '', '| Estado | Cantidad |', '| --- | ---: |']
        lines += [f'| {state} | {count} |' for state, count in s[key].items()]
    lines += ['', '## Conceptos compartidos', '', '| Concepto | Definición local |', '| --- | --- |']
    lines += [f'| {value[0]} | {value[1]} |' for value in report['conceptos'].values()]
    lines += ['', '## Variables con interpretación documental respaldada', '',
              'El significado se respalda en definiciones concretas; no valida valores ni unidades, no resuelve catálogos y no homologa identidades entre fuentes.', '',
              '| Conjunto | Variable | Significado | Representación | Evidencia literal |', '| --- | --- | --- | --- | --- |']
    for row in report['variables']:
        if row['estado'] == 'respaldada_por_definicion':
            values = [row['titulo_conjunto'], row['variable'], row['concepto'], row['representacion'], row['descripcion']]
            lines.append('| ' + ' | '.join(str(v).replace('|', '/').replace('\n', ' ') for v in values) + ' |')
    lines += ['', '## Límites y pendientes', '',
              '- Las reglas de descripción exacta están revisadas en `ontologia/semantica.json`; no hay promoción por expresión regular. Las pistas por nombres se mantienen candidatas.',
              '- Las variables fuera del núcleo compartido siguen en sus definiciones originales. No se ha completado la semántica de las 1,563 variables ni de todos los dominios.',
              '- Un concepto compartido expresa un aspecto común, no identidad de variables, valores, población, unidades o catálogos.',
              f"- {s['estados_correspondencias'].get('documental_revisada', 0)} correspondencias columna/variable tienen revisión documental explícita. Las demás coincidencias de nombre siguen candidatas o ambiguas.",
              '- La referencia CVEGEO sigue asociada únicamente a su columna original del GeoJSON. Los catálogos territoriales recuperados añaden correspondencias calificadas entre instantáneas; no homologan automáticamente columnas de datos ni acreditan vigencia histórica.',
              '- No se asignan fechas reales a partir del nombre de una columna. Año de registro y año de fallecimiento son conceptos distintos.',
              '- El publicador de un conjunto sigue siendo la organización CKAN publicada. Una variable de dependencia capturadora no identifica automáticamente al publicador.',
              '- El glosario local usa SKOS; la procedencia usa PROV-O. No se crean `owl:sameAs`, `skos:exactMatch` ni nuevas relaciones de linaje entre tableros y datos.', '',
              '## Reproducción', '',
              'Ejecutar `uv run python scripts/consolidar_semantica.py` para generar solo esta capa, sin red. `scripts/ampliar_portal.py --load` la incorpora y valida en el grafo completo. `scripts/sincronizar_studio_portal.py` actualiza Studio con respaldo.', '',
              'Evidencia detallada: `data/semantica/cobertura.json`. Vocabulario: `data/semantica/nucleo.ttl`. Interpretaciones: `data/semantica/interpretaciones.ttl`.', '',
              'Referencias: [SKOS](https://www.w3.org/TR/skos-reference/), [PROV-O](https://www.w3.org/TR/prov-o/).', '']
    (ROOT / 'reports/consolidacion-semantica.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    _, _, report = generar()
    print(json.dumps(report['resumen'], ensure_ascii=False, indent=2))
