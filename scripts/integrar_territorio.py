"""Referencias territoriales recuperadas y correspondencias calificadas entre instantáneas."""
from collections import Counter
import hashlib
import json
from urllib.parse import quote
import unicodedata

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS, URIRef, XSD, DCTERMS as DCT
from construir_catalogo import PROV, ROOT


def nombre_comparable(name):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD', name.casefold()) if not unicodedata.combining(c)).split())


def reparar_comparacion(name):
    """A reversible UTF-8/Latin-1 repair for comparison only; never overwrite a source label."""
    if not any(c in name for c in ['Ã', 'Â']):
        return name, False
    for encoding in ['latin1', 'cp1252']:
        try:
            repaired = name.encode(encoding).decode('utf-8')
            if repaired.encode('utf-8').decode(encoding) == name:
                return repaired, True
        except (UnicodeError, ValueError):
            pass
    return name, False


def comparar(entry, level, target):
    original = entry['codigo']
    code = '26' + original.zfill(3) if level == 'municipio_local' else original
    transformation = 'anteponer 26 y completar municipio a tres dígitos; solo esta referencia' if level == 'municipio_local' else 'sin transformación de código'
    if code not in target:
        special = nombre_comparable(entry['nombre']) in {'no especificado', 'otros municipios'}
        return {'estado': 'categoria_no_municipal' if special else 'sin_codigo_destino', 'codigo_destino': code,
                'transformacion': transformation, 'nombre_origen': entry['nombre'], 'nombre_destino_original': None}
    raw_name = target[code]['nombre']
    name, repaired = reparar_comparacion(raw_name)
    equal = nombre_comparable(entry['nombre']) == nombre_comparable(name)
    status = ('codigo_y_nombre_con_reparacion_codificacion' if repaired else 'codigo_y_nombre_normalizado') if equal else 'pendiente_nombre_distinto'
    if equal and entry['nombre'] == raw_name:
        status = 'codigo_y_nombre_exacto'
    return {'estado': status, 'codigo_destino': code, 'transformacion': transformation,
            'nombre_origen': entry['nombre'], 'nombre_destino_original': raw_name,
            'nombre_destino_para_comparar': name, 'reparacion_codificacion': repaired}


def aplicar_alias(ref, entry, assessment, reference, aliases):
    matches = [a for a in aliases if (a['archivo_sha256'], a['hoja'], a['codigo_origen']) ==
               (ref['archivo_sha256'], ref['hoja'], entry['codigo'])]
    if len(matches) > 1:
        raise ValueError('Alias territorial duplicado')
    if not matches:
        return assessment
    alias = matches[0]
    if (alias['nombre_origen'] != entry['nombre'] or alias['recurso_destino'] != reference['recurso_id']
            or alias['codigo_destino'] != assessment['codigo_destino']
            or alias['nombre_destino_original'] != assessment['nombre_destino_original']):
        raise ValueError('Evidencia de alias cambió; requiere revisión')
    return {**assessment, 'estado': 'codigo_y_alias_revisado', 'revision_alias': alias}


def construir(payload, rules, inventory, semantic, reference, base):
    mex, g, model = Namespace(base + 'vocab/'), Graph(), Graph()
    for graph in [g, model]:
        for prefix, ns in [('mex', mex), ('skos', SKOS), ('prov', PROV)]:
            graph.bind(prefix, ns)
    def node(kind, value):
        return URIRef(base + kind + '/' + quote(value, safe=''))
    def scheme(ref):
        return node('territorial-reference', ref['archivo_sha256'] + '/' + ref['hoja'])
    def entry_node(ref, code):
        return node('territorial-entry', ref['archivo_sha256'] + '/' + ref['hoja'] + '/' + code)
    for key, label in {'ReferenciaTerritorial': 'Referencia territorial recuperada',
                       'EntradaReferenciaTerritorial': 'Entrada de referencia territorial',
                       'CorrespondenciaTerritorial': 'Correspondencia territorial entre referencias',
                       'VinculoCatalogoTerritorial': 'Identificación documental de catálogo territorial'}.items():
        model.add((mex[key], RDF.type, OWL.Class)).add((mex[key], RDFS.label, Literal(label, lang='es')))
    for key in ['entradaTerritorialOrigen', 'entradaTerritorialDestino', 'referenciaTerritorial',
                'catalogoRecuperado', 'referenciaDeclarada', 'defineReferenciaTerritorial']:
        model.add((mex[key], RDF.type, OWL.ObjectProperty)).add((mex[key], RDFS.label, Literal(key, lang='es')))
    for key in ['estadoCorrespondenciaTerritorial', 'codigoOriginal', 'nombreOriginal', 'hojaOriginal',
                'celdaCodigo', 'celdaNombre', 'archivoSha256', 'transformacionCodigo', 'nombreComparado',
                'estadoVigencia', 'alcanceReferencia']:
        model.add((mex[key], RDF.type, OWL.DatatypeProperty)).add((mex[key], RDFS.label, Literal(key, lang='es')))
    resources = {r['id']: r for r in inventory['recursos']}
    targets = {e['cvegeo']: e for e in reference['municipios']}
    if len(targets) != 72 or set(targets) != {'26' + str(i).zfill(3) for i in range(1, 73)}:
        raise ValueError('Referencia GeoJSON incompleta o ambigua')
    groups, comparisons, resolved, used_aliases = {}, [], [], set()
    for ref in payload['referencias']:
        resource = resources.get(ref['recurso'])
        if not resource or resource['url'] != ref['fuente'] or resource['conjunto_id'] != ref['conjunto']:
            raise ValueError('Catálogo territorial no coincide con su publicación en el inventario')
        key = (ref['archivo_sha256'], ref['hoja'])
        if key in groups and groups[key]['entradas'] != ref['entradas']:
            raise ValueError('Mismo archivo/hoja con entradas distintas')
        first = key not in groups
        groups[key] = ref
        system = scheme(ref)
        source = URIRef(ref['fuente'])
        g.add((system, RDF.type, mex.ReferenciaTerritorial)).add((system, RDF.type, SKOS.ConceptScheme))
        g.add((system, RDFS.label, Literal(ref['hoja'] + ' — ' + ref['archivo_sha256'][:12], lang='es')))
        g.add((system, mex.hojaOriginal, Literal(ref['hoja']))).add((system, mex.archivoSha256, Literal(ref['archivo_sha256'])))
        g.add((system, mex.alcanceReferencia, Literal(ref['alcance']))).add((system, mex.estadoVigencia, Literal('no_documentada')))
        g.add((system, mex.limiteSemantico, Literal(rules['limite'], lang='es'))).add((system, PROV.wasDerivedFrom, source))
        physical = node('file-column', ref['recurso'] + '/' + ref['hoja'] + '/' + str(ref['posicion_codigo']))
        g.add((physical, mex.defineReferenciaTerritorial, system))
        codes = [row['codigo'] for row in ref['entradas']]
        if len(set(codes)) != len(codes):
            raise ValueError('Código repetido en catálogo')
        for row in ref['entradas']:
            entry = entry_node(ref, row['codigo'])
            g.add((entry, RDF.type, mex.EntradaReferenciaTerritorial)).add((entry, RDF.type, SKOS.Concept))
            g.add((entry, SKOS.inScheme, system)).add((entry, SKOS.notation, Literal(row['codigo'])))
            g.add((entry, mex.codigoOriginal, Literal(row['codigo']))).add((entry, mex.nombreOriginal, Literal(row['nombre'])))
            g.add((entry, RDFS.label, Literal(row['codigo'] + ' — ' + row['nombre'], lang='es')))
            g.add((entry, mex.celdaCodigo, Literal(row['celda_codigo']))).add((entry, mex.celdaNombre, Literal(row['celda_nombre'])))
            g.add((entry, PROV.wasDerivedFrom, source))
            if not first or not ref['nivel'].startswith('municipio'):
                continue
            assessment = comparar(row, ref['nivel'], targets)
            assessment = aplicar_alias(ref, row, assessment, reference, rules.get('aliases_revisados', []))
            if assessment.get('revision_alias'):
                used_aliases.add(assessment['revision_alias']['id'])
            mapping = node('territorial-mapping', ref['archivo_sha256'] + '/' + ref['hoja'] + '/' + row['codigo'])
            g.add((mapping, RDF.type, mex.CorrespondenciaTerritorial))
            g.add((mapping, RDFS.label, Literal(row['codigo'] + ' — ' + row['nombre'] + ' — ' + assessment['estado'], lang='es')))
            g.add((mapping, mex.entradaTerritorialOrigen, entry))
            g.add((mapping, mex.estadoCorrespondenciaTerritorial, Literal(assessment['estado'])))
            g.add((mapping, mex.transformacionCodigo, Literal(assessment['transformacion'], lang='es')))
            g.add((mapping, mex.limiteSemantico, Literal(rules['limite'], lang='es')))
            g.add((mapping, PROV.wasDerivedFrom, source)).add((mapping, PROV.wasDerivedFrom, URIRef(reference['fuente'])))
            if assessment.get('revision_alias'):
                alias = assessment['revision_alias']
                review = node('territorial-review', alias['id'])
                g.add((review, RDF.type, PROV.Entity))
                g.add((review, RDFS.label, Literal('Alias territorial revisado por el usuario: ' + alias['id'], lang='es')))
                g.add((review, mex.evidenciaTextual, Literal(alias['evidencia_usuario'], lang='es')))
                g.add((review, mex.criterioRevision, Literal(alias['criterio'], lang='es')))
                g.add((review, DCT.date, Literal(alias['fecha_revision'], datatype=XSD.date)))
                g.add((mapping, PROV.wasDerivedFrom, review))
            # Special categories never receive a municipal destination.
            if assessment['estado'].startswith('codigo_y_nombre') or assessment['estado'] == 'codigo_y_alias_revisado':
                destination = node('code-entry', reference['recurso_id'] + '/' + assessment['codigo_destino'])
                g.add((mapping, mex.entradaTerritorialDestino, destination))
            if assessment.get('nombre_destino_para_comparar'):
                g.add((mapping, mex.nombreComparado, Literal(assessment['nombre_destino_para_comparar'])))
            comparisons.append({'iri': str(mapping), 'referencia': str(system), 'codigo_origen': row['codigo'], **assessment})
    if used_aliases != {a['id'] for a in rules.get('aliases_revisados', [])}:
        raise ValueError('No se encontró la entrada de un alias revisado')
    for rule in rules['resoluciones']:
        refs = [r for r in payload['referencias'] if r['recurso'] == rule['recurso'] and r['hoja'] == rule['hoja']]
        variables = [v for v in semantic['variables'] if v['diccionario'] == rule['diccionario'] and v['variable'] == rule['variable']]
        if len(refs) != 1 or len(variables) != 1:
            raise ValueError('Resolución de catálogo no única')
        ref, variable = refs[0], variables[0]
        if ref['archivo_sha256'] != rule['archivo_sha256'] or variable['huella_fila_diccionario'] != rule['huella_fila_diccionario']:
            raise ValueError('Evidencia de catálogo cambió; requiere revisión')
        if ref['conjunto'] != variable['conjunto'] or not variable['catalogo_declarado']:
            raise ValueError('Catálogo fuera del conjunto o sin referencia declarada')
        if variable['variable'].casefold() != ref['campo_codigo'].casefold():
            raise ValueError('Campo de catálogo distinto a la variable declarada')
        refid = hashlib.sha256((variable['conjunto'] + '\n' + variable['catalogo_declarado']).encode()).hexdigest()
        declared = node('declared-code-reference', refid)
        system = scheme(ref)
        binding = node('territorial-binding', refid)
        g.add((binding, RDF.type, mex.VinculoCatalogoTerritorial))
        g.add((binding, RDFS.label, Literal(variable['variable'] + ' — catálogo territorial identificado', lang='es')))
        g.add((binding, mex.referenciaDeclarada, declared)).add((binding, mex.catalogoRecuperado, system))
        g.add((binding, mex.variableDestino, URIRef(variable['iri'])))
        g.add((binding, mex.criterioRevision, Literal(rule['criterio'], lang='es')))
        g.add((binding, PROV.wasDerivedFrom, URIRef(variable['definicion_iri'])))
        g.add((binding, PROV.wasDerivedFrom, URIRef(ref['fuente'])))
        g.add((declared, mex.catalogoRecuperado, system))
        resolved.append({'referencia_declarada': str(declared), 'catalogo': str(system), 'variable': variable['iri'], 'vinculo': str(binding),
                         'nombre_variable': variable['variable'], 'titulo_conjunto': ref['titulo_conjunto'],
                         'fuente': ref['fuente'], 'hoja': ref['hoja']})
    summary = {'archivos_leidos': len({r['recurso'] for r in payload['referencias']}), 'hojas_por_recurso': len(payload['referencias']),
               'referencias_distintas_por_archivo_hoja': len(groups), 'entradas_distintas': len(set(g.subjects(RDF.type, mex.EntradaReferenciaTerritorial))),
               'referencias_declaradas_con_recurso_identificado': len({r['referencia_declarada'] for r in resolved}),
               'estados_correspondencias': dict(Counter(c['estado'] for c in comparisons)),
               'catalogos_localidad_en_los_archivos_examinados': 0}
    return g, model, {'resumen': summary, 'resoluciones': resolved, 'correspondencias': comparisons}


def documentar(report):
    s = report['resumen']
    lines = ['# Catálogos territoriales y correspondencias', '',
             'Esta revisión identifica referencias publicadas y contrasta sus entradas con la instantánea del GeoJSON del portal. No valida todas las filas de los conjuntos ni habilita cruces sin comprobar periodo, papel territorial y grano.', '',
             '| Indicador | Resultado |', '| --- | ---: |']
    lines += [f'| {key} | {value} |' for key, value in s.items() if not isinstance(value, dict)]
    lines += ['', 'Los archivos con el mismo SHA-256 y la misma hoja comparten una referencia y sus entradas. Se conservan las URL de todas las publicaciones; no se confunden sus conjuntos ni publicadores.', '',
              '## Referencias declaradas con recurso identificado', '', '| Conjunto | Variable | Hoja | Fuente |', '| --- | --- | --- | --- |']
    lines += [f"| {r['titulo_conjunto']} | {r['nombre_variable']} | {r['hoja']} | [Catálogo publicado]({r['fuente']}) |" for r in report['resoluciones']]
    lines += ['', 'Identificar el recurso no demuestra que todos los códigos de sus archivos de datos pertenezcan al catálogo, ni confirma la versión aplicable a cada año. Esta capa territorial identifica ocho referencias. El resultado combinado con las entregas revisadas se registra en reports/integracion-agentes.md y data/semantica/cobertura.json.', '',
              '## Contraste municipal entre referencias', '', '| Estado | Entradas comparadas |', '| --- | ---: |']
    lines += [f'| {state} | {count} |' for state, count in s['estados_correspondencias'].items()]
    lines += ['', 'Estas cantidades cuentan pares de entradas por referencia distinta, no municipios únicos. Los estados de coincidencia de código/nombre o alias explícitamente revisado reciben un destino; las coincidencias siguen siendo afirmaciones calificadas, sin `owl:sameAs` ni `skos:exactMatch`.', '',
              'Los códigos locales se conservan tal como aparecen. Cuando se contrasta `MUNI`, la transformación `26 + municipio a tres dígitos` se registra en cada correspondencia; no se aplica a otros campos ni al Registro Civil.', '',
              '## Textos y casos pendientes', '',
              'Los nombres del GeoJSON se conservan con su codificación original. Para comparar, se registra una reparación reversible de UTF-8 interpretado como Latin-1 o Windows-1252, seguida de comparación sin diferencias de mayúsculas, tildes y espacios. Se mantienen ambas representaciones; no se sobrescribe la fuente.', '']
    for c in report['correspondencias']:
        if c.get('revision_alias'):
            alias = c['revision_alias']
            lines.append(f"- Alias revisado por el usuario el {alias['fecha_revision']}: {alias['nombre_origen']} / {alias['nombre_destino_original']}, códigos {alias['codigo_origen']} / {alias['codigo_destino']}. Se conservan los textos originales; la revisión se limita a estas entradas de Sonora.")
    for c in report['correspondencias']:
        if c['estado'] in {'pendiente_nombre_distinto', 'categoria_no_municipal', 'sin_codigo_destino'}:
            lines.append(f"- `{c['codigo_origen']}` — {c['nombre_origen']}: `{c['estado']}`. Nombre del destino consultado: {c.get('nombre_destino_original') or 'sin entrada'}. No se creó enlace a un municipio destino.")
    lines += ['', '## Localidades y alcance', '',
              'No se encontró una hoja de catálogo de localidades entre los archivos territoriales examinados. Los catálogos municipales de conjuntos llamados «marginación por localidad» siguen siendo catálogos de municipios; el título del conjunto no los convierte en referencias de localidad. No se asignan claves de localidad sin entidad, municipio y una referencia documental adecuada.', '',
              'Los códigos y nombres de las hojas de catálogos sí se enlazan con la referencia que definen mediante `mex:defineReferenciaTerritorial`. Las columnas de los archivos de datos conservan sus estados semánticos anteriores; esta revisión no acredita automáticamente su pertenencia al catálogo.', '',
              '## Evidencia y reproducción', '',
              '- `data/territorio/catalogos.json`: extracción completa de las hojas y selección de Sonora en las tablas municipales nacionales, con códigos originales, celdas, tipos y SHA-256.',
              '- `data/territorio/verificacion.json`: estados de cada correspondencia y recursos identificados.',
              '- `ontologia/territorio.json`: las ocho resoluciones documentales revisadas, fijadas a las huellas de archivo y de fila de diccionario.',
              '- `data/territorio/territorio.ttl`: capa RDF generada, integrada con el núcleo semántico.', '',
              'La generación normal no consulta la red. Para actualizar los catálogos, ejecutar `uv run python scripts/extraer_catalogos_territoriales.py --refresh`, revisar los cambios y actualizar las resoluciones solo si su evidencia sigue siendo válida. Luego ejecutar `scripts/ampliar_portal.py --load` y `scripts/sincronizar_studio_portal.py`.', '']
    (ROOT / 'reports/catalogos-territoriales.md').write_text('\n'.join(lines), encoding='utf-8')
