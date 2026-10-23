"""Modelo de estructuras de archivo, definiciones declaradas y cruces agregados."""
from collections import Counter, defaultdict
import hashlib
import json
from urllib.parse import quote

from rdflib import DCTERMS as DCT, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef, XSD
from construir_catalogo import ROOT, PROV
from inventariar_portal import normalizar


def clave(value):
    return ' '.join(normalizar(value).strip(' ,;:\t\n').split())


def valor(row, names):
    for key, value in row.items():
        if clave(key) in names and value is not None and str(value).strip():
            return str(value).strip()
    return ''


def integrar(inventory, inspection, cross, base):
    mex, g, model = Namespace(base + 'vocab/'), Graph(), Graph()
    for graph in (g, model):
        graph.bind('mex', mex)
        graph.bind('prov', PROV)
        graph.bind('dct', DCT)
    def node(kind, value):
        return URIRef(base + kind + '/' + quote(str(value), safe=''))
    def entity(subject, cls, label, source):
        g.add((subject, RDF.type, cls)).add((subject, RDFS.label, Literal(label, lang='es')))
        g.add((subject, PROV.wasDerivedFrom, URIRef(source)))
        return subject
    resources = {r['id']: r for r in inventory['recursos']}
    definitions, columns = defaultdict(list), []
    report = {'generado_en_utc': inspection['generado_en_utc'], 'inspeccionados': len(inspection['recursos']),
              'inspecciones_correctas': 0, 'diccionarios_leidos': 0, 'filas_diccionario': 0,
              'definiciones_con_nombre': 0, 'filas_sin_nombre_variable': 0, 'columnas_archivo': 0,
              'esquemas_archivo': 0, 'columnas_con_definicion_candidata': 0, 'fallos': [], 'roles_candidatos': Counter()}
    for result in inspection['recursos']:
        resource = resources[result['id']]
        subject = node('resource', resource['id'])
        checked = node('inspection', resource['id'])
        source = result.get('fuente') or ('https://datos.sonora.gob.mx/api/3/action/resource_show?id=' + resource['id'])
        entity(checked, mex.InspeccionContenido, 'Inspección — ' + resource['conjunto'] + ' — ' + str(resource['nombre']), source)
        g.add((subject, mex.inspeccionContenido, checked))
        g.add((checked, mex.resultadoInspeccion, Literal('observado' if result['ok'] else 'no_disponible')))
        g.add((checked, PROV.endedAtTime, Literal(result['consultado_en_utc'], datatype=XSD.dateTime)))
        g.add((checked, mex.metodoInspeccion, Literal(result.get('metodo', 'intento_archivo'))))
        if not result['ok']:
            g.add((checked, mex.detalleInspeccion, Literal(result.get('error', 'Error no especificado'))))
            report['fallos'].append({'id': resource['id'], 'conjunto': resource['conjunto'], 'recurso': resource['nombre'], 'error': result.get('error')})
            continue
        report['inspecciones_correctas'] += 1
        if 'definiciones' in result:
            report['diccionarios_leidos'] += 1
            for i, row in enumerate(result['definiciones'], 1):
                report['filas_diccionario'] += 1
                name = valor(row, {'nombre variable', 'nombre de variable', 'variable', 'nombre campo', 'nombre del campo'})
                if not name:
                    report['filas_sin_nombre_variable'] += 1
                    continue
                definition = node('definition', resource['id'] + '/' + str(i))
                entity(definition, mex.DefinicionVariable, name + ' — ' + resource['conjunto'], source)
                g.add((subject, mex.definicionVariable, definition))
                g.add((definition, mex.nombreVariableDeclarado, Literal(name)))
                cleaned = {k: v for k, v in row.items() if v is not None and str(v).strip() and k != 'hoja'}
                g.add((definition, mex.filaDiccionario, Literal(json.dumps(cleaned, ensure_ascii=False, sort_keys=True))))
                description = valor(row, {'descripcion', 'definicion'})
                unit = valor(row, {'unidad de medida', 'unidades de medida'})
                if description:
                    g.add((definition, DCT.description, Literal(description, lang='es')))
                if unit:
                    g.add((definition, mex.unidadDeclarada, Literal(unit)))
                definitions[(resource['conjunto_id'], clave(name))].append((definition, description))
                report['definiciones_con_nombre'] += 1
        # API schemas already exist in the preceding model; no file schema is invented for them.
        for table_index, table in enumerate(result.get('tablas', []), 1):
            schema = node('file-schema', resource['id'] + '/' + table['hoja'])
            entity(schema, mex.EsquemaObservado, 'Esquema archivo — ' + table['hoja'] + ' — ' + resource['conjunto'] + ' — ' + str(resource['nombre']), source)
            g.add((subject, mex.esquemaArchivo, schema))
            g.add((schema, mex.nombreHoja, Literal(table['hoja'])))
            g.add((schema, mex.metodoEncabezado, Literal(table['metodo_encabezado'])))
            g.add((schema, mex.filaEncabezado, Literal(table['fila_encabezado'])))
            report['esquemas_archivo'] += 1
            for field in table['campos']:
                # Position distinguishes repeated labels in a worksheet.
                col = node('file-column', resource['id'] + '/' + table['hoja'] + '/' + str(field['posicion_original']))
                entity(col, mex.ColumnaObservada, field['id'] + ' — ' + table['hoja'] + ' — ' + resource['conjunto'] + ' — ' + str(resource['nombre']), source)
                g.add((schema, mex.columna, col)).add((col, DCT.isPartOf, schema))
                g.add((col, mex.nombreCampo, Literal(field['id']))).add((col, mex.posicionCampo, Literal(field['posicion_original'])))
                g.add((col, mex.campoInterno, Literal(False)))
                if resource['clasificacion'] != 'diccionario':
                    columns.append((col, resource, field['id']))
                report['columnas_archivo'] += 1
    for resource in resources.values():
        if resource['clasificacion'] != 'diccionario' and resource.get('datastore', {}).get('ok'):
            for field in resource['datastore']['campos']:
                if not field['id'].startswith('_'):
                    columns.append((URIRef(base + 'column/' + resource['id'] + '/' + quote(field['id'], safe='')), resource, field['id']))
    candidates = []
    for column, resource, name in columns:
        matches = definitions.get((resource['conjunto_id'], clave(name)), [])
        if len(matches) == 1:
            definition, description = matches[0]
            g.add((column, mex.definicionCandidata, definition))
            report['columnas_con_definicion_candidata'] += 1
            text = clave(description)
            role = ('municipio_registro' if 'municipio de registro' in text else
                    'codigo_municipio' if 'clave' in text and 'municipio' in text else
                    'anio_registro' if 'ano' in text and 'registro' in text else
                    'municipio_declarado' if 'municipio' in text else None)
            if role:
                g.add((column, mex.rolCandidato, Literal(role)))
                candidates.append({'columna': str(column), 'conjunto': resource['conjunto'], 'recurso_id': resource['id'],
                                   'campo': name, 'rol_candidato': role, 'definicion': description,
                                   'evidencia': 'Nombre normalizado único dentro del conjunto y descripción del diccionario; requiere revisión de dominio para cruces nuevos'})
                report['roles_candidatos'][role] += 1
    crossnode = node('cross', 'registro-civil-2022')
    first_source = cross['fuentes'][0]['consultas'][0]
    entity(crossnode, mex.CruceAgregado, 'Cruce exploratorio: matrimonios y divorcios registrados en 2022', first_source)
    g.add((crossnode, DCT.description, Literal(cross['alcance'], lang='es')))
    g.add((crossnode, mex.metodoCruce, Literal(cross['metodo'])))
    for limitation in cross['limites']:
        g.add((crossnode, mex.limitacionCruce, Literal(limitation, lang='es')))
    for source in cross['fuentes']:
        g.add((crossnode, PROV.wasDerivedFrom, node('resource', source['recurso_id'])))
        g.add((crossnode, PROV.wasDerivedFrom, node('resource', source['diccionario_id'])))
    for row in cross['filas']:
        observation = node('aggregate', 'registro-civil-2022/' + str(row['codigo_municipio_fuente']))
        entity(observation, mex.ResumenMunicipalLocal, 'Registro Civil 2022 — código local ' + str(row['codigo_municipio_fuente']), first_source)
        g.add((crossnode, mex.resumenMunicipal, observation))
        g.add((observation, DCT.isPartOf, crossnode))
        g.add((observation, mex.codigoMunicipioFuente, Literal(row['codigo_municipio_fuente'])))
        g.add((observation, mex.anioRegistro, Literal(row['anio_registro'])))
        g.add((observation, mex.presenteEnAmbas, Literal(row['presente_en_ambas'])))
        for key, prop in [('registros_matrimonios', mex.conteoMatrimonios), ('registros_divorcios', mex.conteoDivorcios)]:
            if row[key] is not None:
                g.add((observation, prop, Literal(row[key])))
    for cls, label in [(mex.InspeccionContenido, 'Inspección de contenido'), (mex.DefinicionVariable, 'Definición declarada de variable'),
                       (mex.CruceAgregado, 'Cruce agregado'), (mex.ResumenMunicipalLocal, 'Resumen por código municipal local')]:
        model.add((cls, RDF.type, OWL.Class)).add((cls, RDFS.label, Literal(label, lang='es')))
    obj = {'inspeccionContenido': 'Inspección del recurso', 'esquemaArchivo': 'Esquema observado en archivo',
           'definicionVariable': 'Definición en diccionario', 'definicionCandidata': 'Definición candidata por nombre dentro del conjunto',
           'resumenMunicipal': 'Resumen municipal del cruce'}
    data = {'resultadoInspeccion': 'Resultado de inspección', 'metodoInspeccion': 'Método de inspección',
            'detalleInspeccion': 'Detalle de inspección', 'nombreHoja': 'Nombre de hoja', 'filaEncabezado': 'Fila del encabezado',
            'metodoEncabezado': 'Método de detección del encabezado', 'nombreVariableDeclarado': 'Nombre de variable declarado',
            'filaDiccionario': 'Contenido declarado en diccionario', 'unidadDeclarada': 'Unidad declarada sin normalizar',
            'rolCandidato': 'Rol candidato según diccionario', 'codigoMunicipioFuente': 'Código municipal local de la fuente',
            'anioRegistro': 'Año de registro', 'conteoMatrimonios': 'Filas de matrimonios publicados',
            'conteoDivorcios': 'Filas de divorcios publicados', 'presenteEnAmbas': 'Código observado en ambas fuentes',
            'metodoCruce': 'Método de cruce', 'limitacionCruce': 'Límite de interpretación del cruce'}
    for names, cls in [(obj, OWL.ObjectProperty), (data, OWL.DatatypeProperty)]:
        for name, label in names.items():
            model.add((mex[name], RDF.type, cls)).add((mex[name], RDFS.label, Literal(label, lang='es')))
    report['roles_candidatos'] = dict(report['roles_candidatos'])
    report['candidatos'] = candidates
    report['cruce'] = {'resumenes': len(cross['filas']), 'codigos_en_ambas': sum(r['presente_en_ambas'] for r in cross['filas']),
                       'fuentes': [{k: v for k, v in s.items() if k in ('recurso_id', 'nombre', 'total_registros')} for s in cross['fuentes']]}
    return g, model, report


def documentar(report):
    (ROOT / 'reports/contenido-cobertura.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Cobertura de estructuras y contenido', '', 'Fecha UTC: ' + report['generado_en_utc'], '',
             '| Indicador | Total |', '| --- | ---: |']
    for key in ['inspeccionados', 'inspecciones_correctas', 'diccionarios_leidos', 'filas_diccionario', 'definiciones_con_nombre',
                'filas_sin_nombre_variable', 'esquemas_archivo', 'columnas_archivo', 'columnas_con_definicion_candidata']:
        lines.append(f'| {key} | {report[key]} |')
    lines += ['', '## Recursos sin estructura disponible', '', '| Conjunto | Recurso | Causa |', '| --- | --- | --- |']
    lines += [f"| {r['conjunto']} | {r['recurso']} | {r['error']} |" for r in report['fallos']]
    lines += ['', '## Conexiones candidatas', '', 'Las coincidencias de nombre se limitan al mismo conjunto y requieren una única definición. No se crean equivalencias globales ni identidades de municipios.', '',
              '| Rol según diccionario | Columnas |', '| --- | ---: |']
    lines += [f'| {key} | {value} |' for key, value in report['roles_candidatos'].items()]
    lines += ['', '## Alcance y límites', '',
              '- Todos los recursos tienen un intento registrado, con fecha y fuente. Un fallo no se presenta como un esquema recuperado.',
              '- Los esquemas de archivo describen cada hoja, conservan posiciones y etiquetas repetidas. Los encabezados detectados son candidatos y requieren revisión; no equivalen a un contrato de datos validado.',
              '- Se leen hasta 30 filas para detectar encabezados. Las filas de datos no se guardan ni se incorporan al grafo. Excel usa copias acotadas en memoria o rangos HTTP; CSV de datos usa un prefijo acotado.',
              '- Los diccionarios sí se leen completos, hasta 10,000 filas y con límite de bytes. Se conservan los valores originales. Las filas sin nombre de variable quedan en la evidencia JSON, sin inventar definiciones.',
              '- La lectura completa del diccionario no valida la exactitud de sus definiciones ni resuelve sus referencias a catálogos externos.',
              '- El primer cruce consulta solo tres campos por fila en dos recursos. Se conservan agregados, comprobando totales, IDs únicos y año.',
              '- Las visualizaciones siguen inventariadas por URL; este proceso no demuestra de qué conjuntos se alimentan.',
              '- La cobertura del catálogo original está en reports/cobertura-portal.md; este documento describe la inspección posterior.', '',
              'Resultados del cruce: [primer-cruce.md](primer-cruce.md). Evidencia estructurada: `data/portal/contenido-inspeccion.json`, `data/portal/inspecciones/` y `data/portal/cruce-registro-civil.json`.', '']
    (ROOT / 'reports/contenido-cobertura.md').write_text('\n'.join(lines), encoding='utf-8')
