"""Evalúa todos los pares del catálogo usando evidencia local, sin ejecutar joins masivos."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
import re
import tomllib
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, DCTERMS as DCT, URIRef, XSD
from construir_catalogo import ROOT, PROV
from integrar_contenido import clave, valor


def clasificar(nombre, descripcion='', tipo=''):
    """Detecta dimensiones; nunca convierte una medida o un texto libre en identificador."""
    name = re.sub(r'[^a-z0-9]+', ' ', clave(nombre)).strip()
    compact = name.replace(' ', '')
    desc = clave(descripcion)
    text = name + ' ' + desc
    family = None
    if ((compact.startswith('municipio') and not compact.startswith('municipios')) or compact.startswith(('cvemunici', 'nommunicipio', 'codigomunicipio', 'clavemunicipio')) or
            name in {'mun', 'muni', 'nom mun', 'cve mun', 'nom municipio'} or
            (name in {'clave', 'codigo'} and 'municipio' in desc and ('clave' in desc or 'codigo' in desc))):
        family = 'municipio'
    elif (compact.startswith('localidad') and not compact.startswith('localidades')) or name in {'loc', 'nom loc', 'cve loc'}:
        family = 'localidad'
    elif name in {'cvegeo', 'clave geoestadistica'}:
        family = 'clave_geoestadistica'
    elif name in {'clues', 'clave clues'}:
        family = 'unidad_salud_clues'
    elif name in {'programa educativo', 'carrera', 'clave carrera', 'programa de estudios'}:
        family = 'programa_educativo'
    elif compact in {'cct', 'clavecentrotrabajo', 'clavedelcentrodetrabajo'}:
        family = 'centro_trabajo'
    elif name in {'escuela', 'plantel', 'institucion educativa', 'nombre escuela', 'nombre del plantel'}:
        family = 'plantel_nombre'
    elif name in {'dependencia', 'institucion', 'organismo', 'unidad responsable', 'nombre dependencia'}:
        family = 'dependencia_nombre'
    elif name in {'region', 'cve region', 'colonia', 'distrito', 'ddr', 'cddr', 'nddr', 'jurisdiccion'}:
        family = 'division_territorial_declarada'
    elif name in {'especie', 'cvespe', 'cultivo', 'producto'}:
        family = 'producto_o_especie'
    elif name in {'delito', 'tipo de delito', 'subtipo de delito'}:
        family = 'clasificacion_delito'
    elif name in {'sexo', 'escolaridad', 'nivel', 'campo de formacion academica', 'modalidad'}:
        family = 'estrato_' + name.replace(' ', '_')
    elif name in {'cve ent', 'clave ent', 'nom ent', 'ent', 'entidad', 'estado', 'entidad federativa'}:
        family = 'entidad'
    elif re.match(r'^(ano|anio)( |$)', name) or compact in {'year', 'ejercicio', 'ejerciciofiscal'}:
        family = 'anio'
    elif name in {'mes', 'month'} or name.startswith('mes '):
        family = 'mes'
    elif name in {'fecha', 'periodo', 'ciclo', 'ciclo escolar', 'trimestre', 'semestre'} or name.startswith('fecha '):
        family = 'periodo'
    if family is None:
        return None
    scope = 'sin_especificar'
    for candidate, pattern in [('registro', r'registro|registrad'), ('residencia', r'resid|recid'),
                                ('nacimiento', r'nacimiento|nacio'), ('defuncion', r'defuncion|fallec'),
                                ('parto', r'parto'), ('ocurrencia', r'ocurr|delito'),
                                ('fiscal', r'fiscal'), ('escolar', r'escolar'), ('ubicacion', r'ubicacion')]:
        if re.search(pattern, text):
            scope = candidate
            break
    representation = ('codigo' if re.search(r'clave|codigo|cve', text) or name in {'mun', 'muni', 'loc', 'ent', 'cct'} else
                      'nombre' if re.search(r'\bnombre\b|\bnom\b', text) or family.endswith('_nombre') else 'sin_especificar')
    return {'familia': family, 'sentido': scope, 'representacion': representation,
            'tipo_declarado': tipo, 'apoyada_por_definicion': bool(desc and 'pendiente' not in desc)}


def perfiles(inventory, inspection, base, graph):
    resources = {r['id']: r for r in inventory['recursos']}
    profiles, definitions = {}, defaultdict(list)
    for r in resources.values():
        dataset = profiles.setdefault(r['conjunto_id'], {'id': r['conjunto_id'], 'titulo': r['conjunto'], 'columnas_clave': [],
                                                       'recursos_datos': [], 'anios_en_nombres': set(), 'publicadores': [], 'campos_observados': set()})
        if r['clasificacion'] != 'diccionario':
            dataset['recursos_datos'].append(r['id'])
            dataset['anios_en_nombres'].update(re.findall(r'\b(?:19|20)\d{2}\b', r.get('nombre') or ''))
    for result in inspection['recursos']:
        r = resources[result['id']]
        if not result['ok']:
            continue
        if r['clasificacion'] == 'diccionario':
            for i, row in enumerate(result.get('definiciones', []), 1):
                name = valor(row, {'nombre variable', 'nombre de variable', 'variable', 'nombre campo', 'nombre del campo'})
                if name:
                    definitions[(r['conjunto_id'], clave(name))].append({
                        'iri': base + 'definition/' + quote(r['id'] + '/' + str(i), safe=''),
                        'descripcion': valor(row, {'descripcion', 'definicion'}),
                        'tipo': valor(row, {'tipo de dato'}),
                        'unidad': valor(row, {'unidad de medida', 'unidades de medida'}),
                        'catalogo': valor(row, {'catalogo de referencia', 'catalago de referencia'})})
    for result in inspection['recursos']:
        r = resources[result['id']]
        if not result['ok'] or r['clasificacion'] == 'diccionario':
            continue
        fields = []
        if r.get('datastore', {}).get('ok'):
            fields += [(base + 'column/' + r['id'] + '/' + quote(f['id'], safe=''), f['id'], 'DataStore')
                       for f in r['datastore']['campos'] if not f['id'].startswith('_')]
        for table in result.get('tablas', []):
            fields += [(base + 'file-column/' + quote(r['id'] + '/' + table['hoja'] + '/' + str(f['posicion_original']), safe=''),
                        f['id'], 'encabezado_heuristico') for f in table['campos']]
        for iri, name, method in fields:
            profiles[r['conjunto_id']]['campos_observados'].add(clave(name))
            matches = definitions.get((r['conjunto_id'], clave(name)), [])
            definition = matches[0] if len(matches) == 1 else {}
            classification = clasificar(name, definition.get('descripcion', ''), definition.get('tipo', ''))
            if classification:
                profiles[r['conjunto_id']]['columnas_clave'].append({
                    'columna': iri, 'recurso_id': r['id'], 'campo': name, 'origen': method,
                    **classification, 'definicion': definition, 'definiciones_ambiguas': len(matches) > 1})
    for dataset in profiles.values():
        dataset['anios_en_nombres'] = sorted(dataset['anios_en_nombres'])
        dataset['publicadores'] = sorted(str(x) for x in graph.objects(URIRef(base + 'dataset/' + dataset['id']), DCT.publisher))
        dataset['familias'] = sorted({c['familia'] for c in dataset['columnas_clave']})
        dataset['campos_observados'] = sorted(dataset['campos_observados'])
    return profiles


TEMPORAL = {'anio', 'mes', 'periodo'}
WEAK = {'entidad', 'dependencia_nombre', 'plantel_nombre', 'division_territorial_declarada',
        'estrato_sexo', 'estrato_escolaridad', 'estrato_nivel', 'estrato_campo_de_formacion_academica', 'estrato_modalidad'}


def evaluar(a, b, executed):
    shared = sorted(set(a['familias']) & set(b['familias']))
    spatial = [f for f in shared if f not in TEMPORAL | WEAK]
    details, blockers = [], set()
    for family in shared:
        ca = [c for c in a['columnas_clave'] if c['familia'] == family]
        cb = [c for c in b['columnas_clave'] if c['familia'] == family]
        sa, sb = {c['sentido'] for c in ca} - {'sin_especificar'}, {c['sentido'] for c in cb} - {'sin_especificar'}
        ra, rb = {c['representacion'] for c in ca} - {'sin_especificar'}, {c['representacion'] for c in cb} - {'sin_especificar'}
        issues = []
        if sa and sb and not sa & sb:
            issues.append('sentidos_distintos_requieren_pregunta_y_agregacion_explicitas')
        if ra and rb and not ra & rb:
            issues.append('requiere_correspondencia_codigo_nombre')
        if 'sin_especificar' in {c['sentido'] for c in ca + cb}:
            issues.append('sentido_parcialmente_desconocido')
        if not all(c['apoyada_por_definicion'] for c in ca + cb):
            issues.append('faltan_definiciones_de_algunas_columnas')
        if any(c['origen'] == 'encabezado_heuristico' for c in ca + cb):
            issues.append('revisar_encabezados_heuristicos')
        if family in {'municipio', 'localidad', 'clave_geoestadistica', 'centro_trabajo'}:
            issues.append('verificar_catalogo_dominio_unicidad_y_contexto_de_clave')
        if family == 'localidad':
            issues.append('localidad_puede_requerir_entidad_y_municipio_como_clave_compuesta')
        if family == 'municipio':
            issues.append('municipio_puede_requerir_entidad_como_clave_compuesta')
        if family == 'programa_educativo':
            issues.append('programa_requiere_institucion_plan_y_homologacion_de_nombres')
        if family in {'producto_o_especie', 'clasificacion_delito'}:
            issues.append('homologar_taxonomia_y_nivel_de_clasificacion')
        if family == 'unidad_salud_clues':
            issues.append('comprobar_catalogo_clues_y_vigencia_de_unidades')
        if family in WEAK:
            issues.append('dimension_amplia_o_nombre_no_identifica_por_si_solo')
        details.append({'familia': family, 'columnas_a': [c['columna'] for c in ca], 'columnas_b': [c['columna'] for c in cb],
                        'sentidos_a': sorted(sa), 'sentidos_b': sorted(sb), 'representaciones_a': sorted(ra),
                        'representaciones_b': sorted(rb), 'pendientes': issues})
        blockers.update(issues)
    pair = frozenset((a['id'], b['id']))
    state = ('exploratorio_ejecutado' if pair == executed else 'candidata_por_validar' if spatial else
             'solo_dimensiones_amplias_o_tiempo' if shared else 'sin_clave_detectada')
    # No period overlap is claimed from filenames; their dates are only hints.
    hints = sorted(set(a['anios_en_nombres']) & set(b['anios_en_nombres']))
    if shared:
        blockers.update(['verificar_periodos_y_cobertura_real', 'definir_grano_y_agregacion_antes_del_join',
                         'comprobar_cardinalidad_y_evitar_multiplicacion_de_filas', 'validar_unidades_de_medidas_seleccionadas'])
    priority = ('cruce_existente' if state == 'exploratorio_ejecutado' else
                'revisar_primero' if spatial and hints and set(a['publicadores']) & set(b['publicadores']) else
                'revisar' if spatial else 'evidencia_insuficiente')
    return {'id': '--'.join(sorted((a['id'], b['id']))), 'conjunto_a': a['id'], 'titulo_a': a['titulo'],
            'conjunto_b': b['id'], 'titulo_b': b['titulo'], 'estado': state, 'prioridad_revision': priority,
            'familias_compartidas': shared, 'evaluacion_claves': details, 'pendientes': sorted(blockers),
            'anios_coincidentes_solo_en_nombres': hints,
            'publicador_comun': sorted(set(a['publicadores']) & set(b['publicadores'])),
            'nombres_campos_coincidentes_sin_garantia_semantica': sorted(set(a.get('campos_observados', [])) & set(b.get('campos_observados', []))),
            'alcance_ejecucion': 'Solo los dos recursos de 2022 del informe primer-cruce; no todos los recursos de estos conjuntos' if pair == executed else 'No ejecutado'}


def generar(profiles, cross):
    executed = frozenset(s['conjunto_id'] for s in cross['fuentes'])
    return [evaluar(a, b, executed) for a, b in combinations(sorted(profiles.values(), key=lambda x: x['id']), 2)]


def rdf_map(report, base):
    mex, graph = Namespace(base + 'vocab/'), Graph()
    graph.bind('mex', mex)
    evidence = (ROOT / 'data/portal/oportunidades-cruce.json').as_uri()
    for cls, label in [(mex.EvaluacionCruce, 'Oportunidad de cruce evaluada'), (mex.PerfilClaves, 'Perfil de claves del conjunto')]:
        graph.add((cls, RDF.type, OWL.Class)).add((cls, RDFS.label, Literal(label, lang='es')))
    objects = {'conjuntoA': 'Conjunto A', 'conjuntoB': 'Conjunto B', 'perfilClaves': 'Perfil de claves observado', 'columnaClave': 'Columna candidata a clave'}
    data = {'estadoOportunidad': 'Estado de oportunidad de cruce', 'prioridadRevision': 'Prioridad de revisión',
            'familiaClave': 'Familia de clave candidata', 'pendienteCruce': 'Verificación pendiente',
            'alcanceEjecucion': 'Alcance de ejecución del cruce', 'aniosNombreCoincidentes': 'Años coincidentes solo en nombres de recursos'}
    for mapping, cls in [(objects, OWL.ObjectProperty), (data, OWL.DatatypeProperty)]:
        for key, label in mapping.items():
            graph.add((mex[key], RDF.type, cls)).add((mex[key], RDFS.label, Literal(label, lang='es')))
    for p in report['perfiles'].values():
        node = URIRef(base + 'key-profile/' + p['id'])
        graph.add((node, RDF.type, mex.PerfilClaves)).add((node, RDFS.label, Literal('Claves — ' + p['titulo'], lang='es')))
        graph.add((URIRef(base + 'dataset/' + p['id']), mex.perfilClaves, node))
        graph.add((node, PROV.wasDerivedFrom, URIRef(evidence)))
        for column in p['columnas_clave']:
            graph.add((node, mex.columnaClave, URIRef(column['columna'])))
        for family in p['familias']:
            graph.add((node, mex.familiaClave, Literal(family)))
    for row in report['pares']:
        node = URIRef(base + 'opportunity/' + row['id'])
        graph.add((node, RDF.type, mex.EvaluacionCruce))
        graph.add((node, RDFS.label, Literal(row['titulo_a'] + ' ↔ ' + row['titulo_b'], lang='es')))
        graph.add((node, mex.conjuntoA, URIRef(base + 'dataset/' + row['conjunto_a'])))
        graph.add((node, mex.conjuntoB, URIRef(base + 'dataset/' + row['conjunto_b'])))
        graph.add((node, mex.estadoOportunidad, Literal(row['estado'])))
        graph.add((node, mex.prioridadRevision, Literal(row['prioridad_revision'])))
        graph.add((node, mex.alcanceEjecucion, Literal(row['alcance_ejecucion'])))
        graph.add((node, PROV.wasDerivedFrom, URIRef(evidence)))
        for family in row['familias_compartidas']:
            graph.add((node, mex.familiaClave, Literal(family)))
        for blocker in row['pendientes']:
            graph.add((node, mex.pendienteCruce, Literal(blocker)))
        if row['anios_coincidentes_solo_en_nombres']:
            graph.add((node, mex.aniosNombreCoincidentes, Literal(', '.join(row['anios_coincidentes_solo_en_nombres']))))
    return graph


def main():
    paths = {'inventario': ROOT / 'data/portal/inventario.json', 'inspeccion': ROOT / 'data/portal/contenido-inspeccion.json',
             'cruce': ROOT / 'data/portal/cruce-registro-civil.json', 'catalogo': ROOT / 'data/catalogo/catalogo.ttl'}
    inventory, inspection, cross = [json.loads(paths[key].read_text(encoding='utf-8')) for key in ('inventario', 'inspeccion', 'cruce')]
    if {r['id'] for r in inventory['recursos']} != {r['id'] for r in inspection['recursos']}:
        raise ValueError('Inventario e inspección no coinciden')
    base = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']
    graph = Graph().parse(paths['catalogo'], format='turtle')
    profiles = perfiles(inventory, inspection, base, graph)
    pairs = generar(profiles, cross)
    summary = dict(Counter(p['estado'] for p in pairs))
    report = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'version_reglas': 1,
              'huellas_entrada': {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()},
              'alcance': 'Todos los pares no ordenados de conjuntos del inventario. Dimensiones detectadas por reglas conservadoras sobre nombres y definiciones, no todos los cruces matemáticamente posibles.',
              'resumen': {'conjuntos': len(profiles), 'pares_evaluados': len(pairs), 'estados': summary,
                          'columnas_clave_candidatas': sum(len(p['columnas_clave']) for p in profiles.values()),
                          'conjuntos_sin_clave_detectada': sum(not p['columnas_clave'] for p in profiles.values())},
              'perfiles': profiles, 'pares': pairs}
    (ROOT / 'data/portal/oportunidades-cruce.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    rdf_map(report, base).serialize(ROOT / 'data/portal/oportunidades.ttl', format='turtle', encoding='utf-8')
    lines = ['# Mapa de oportunidades de cruce', '', report['alcance'], '', 'Fecha UTC: ' + report['generado_en_utc'], '',
             f"Se evaluaron {len(pairs):,} pares entre {len(profiles)} conjuntos. Cada par aparece una sola vez.", '',
             '| Estado | Pares |', '| --- | ---: |']
    lines += [f'| {state} | {total} |' for state, total in sorted(summary.items())]
    lines += ['', '## Cómo leer el resultado', '',
              '- Candidata por validar: comparte alguna clave territorial, de establecimiento, programa educativo o categoría sectorial. No está autorizada automáticamente como join correcto.',
              '- Solo dimensiones amplias o tiempo: compartir año, mes, entidad, estrato o un nombre institucional no basta para enlazar filas.',
              '- Sin clave detectada: las reglas no encontraron una clave común; no demuestra que un cruce sea imposible.',
              '- Exploratorio ejecutado: únicamente matrimonios y divorcios de 2022; sigue pendiente el catálogo oficial de códigos.',
              '- Prioridad de revisión no es una puntuación de compatibilidad: usa coincidencias de nombres de años y dependencia publicadora como pistas.',
              '- Se deben comprobar claves compuestas, unicidad, cardinalidad, población de referencia, grano, periodos y unidades antes de ejecutar cada cruce nuevo.',
              '- No se crean equivalencias de columnas, no se vinculan personas y no se multiplican microdatos. Los cruces de tres o más conjuntos requieren validar primero cada enlace y el grano del resultado.', '',
              '## Pares candidatos y cruce existente', '',
              'La evidencia completa, con cada columna, definición, sentido, recurso y diferencias detectadas, está en `data/portal/oportunidades-cruce.json`. Los demás pares también están conservados allí.', '',
              '| Conjunto A | Conjunto B | Familias de clave | Estado | Prioridad |', '| --- | --- | --- | --- | --- |']
    ordered = sorted(pairs, key=lambda p: ({'cruce_existente': 0, 'revisar_primero': 1, 'revisar': 2, 'evidencia_insuficiente': 3}[p['prioridad_revision']], p['titulo_a'], p['titulo_b']))
    for p in ordered:
        if p['estado'] in {'candidata_por_validar', 'exploratorio_ejecutado'}:
            a = f"[{p['titulo_a'].replace('|', '/')}](https://datos.sonora.gob.mx/dataset/{p['conjunto_a']})"
            b = f"[{p['titulo_b'].replace('|', '/')}](https://datos.sonora.gob.mx/dataset/{p['conjunto_b']})"
            lines.append(f"| {a} | {b} | {', '.join(p['familias_compartidas'])} | {p['estado']} | {p['prioridad_revision']} |")
    lines += ['', '## Conjuntos sin claves reconocidas', '']
    lines += ['- ' + p['titulo'] for p in profiles.values() if not p['columnas_clave']]
    lines += ['', '## Actualizar', '', 'Ejecutar `uv run python scripts/mapear_cruces.py` después de actualizar el inventario, las inspecciones y el cruce. Luego regenerar el grafo con `scripts/ampliar_portal.py --load` y sincronizar Studio con `scripts/sincronizar_studio_portal.py`.', '']
    (ROOT / 'reports/oportunidades-cruce.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(report['resumen'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
