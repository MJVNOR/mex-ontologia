"""R10: extensión de unidades declaradas y formas SHACL posteriores a R9.

Staging: no instala, no crea material real ni aprobaciones. El loader exige
dos dictámenes reales (a y b) con el SHA exacto de aceptadas.json y una
aprobación por cada unidad y cada forma. R1-R9 no se modifican y la base IRI
actual queda fuera de alcance.
"""
import hashlib
import json
import re
import tomllib
import unicodedata
import uuid
from pathlib import Path
from urllib.parse import urlsplit

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

from construir_catalogo import PROV, ROOT

EVIDENCIA = 'data/integracion-ronda-10'
BASE = 'https://example.org/mex-ontologi/'
BASE_IRI_ACTUAL = 'https://example.org/mex-ontologi/'
MEX = Namespace(BASE + 'vocab/')
QUDT = Namespace('http://qudt.org/schema/qudt/')
QUDT_UNIT = Namespace('http://qudt.org/vocab/unit/')
SH = Namespace('http://www.w3.org/ns/shacl#')
XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
PIN_REGLAS = 'dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd'
MAX_UNIDADES = 6
ARCHIVOS = {'datos': 'datos/unidades.ttl', 'shapes': 'shapes/adicionales.ttl'}
MODELO = 'modelo/unidades.ttl'
OBLIGATORIOS = frozenset({
    'aceptadas.json', 'base-semantica.json', 'cobertura-r9.json',
    'config-iri-base.toml', 'datos/unidades.ttl', 'shapes/adicionales.ttl',
    'auditorias/a.json', 'auditorias/b.json'})
CAMPOS_ACEPTADAS = frozenset({
    'format_version', 'release', 'release_base', 'unidades', 'formas',
    'archivos_instalables'})
CAMPOS_UNIDAD = frozenset({
    'id', 'diccionario', 'fila', 'conjunto', 'nombre', 'unidad_literal',
    'unidad_qudt', 'normativa_uri', 'normativa_sha256',
    'huella_fila_diccionario', 'fuente_url', 'sujeto', 'variable',
    'definicion_iri'})
CAMPOS_UNIDAD_OPCIONALES = frozenset({
    'etiqueta', 'comentario', 'evidencia_normativa'})
CAMPOS_FORMA = frozenset({'id'})
R9_DEFINICIONES = frozenset({
    BASE + 'definition/6713de4e-1e2b-447d-8000-f6ceaabd8473%2F6',
    BASE + 'definition/94215f51-9c89-414d-8c3d-92792e609a2a%2F14'})
R9_SUJETOS = frozenset({
    BASE + 'propuesta/p1-qudt/v003/declaracion-precipitacion-mm',
    BASE + 'propuesta/p1-qudt/v003/declaracion-superficie-ha'})
R9_PINES = frozenset({
    ('6713de4e-1e2b-447d-8000-f6ceaabd8473', 6),
    ('94215f51-9c89-414d-8c3d-92792e609a2a', 14)})
RESUMEN_R9 = {
    'definiciones_con_nombre_examinadas': 1563,
    'filas_sin_nombre': 7,
    'estados_variables': {
        'respaldada_por_definicion': 1423,
        'fuera_del_nucleo_actual': 124,
        'candidata_sin_definicion_suficiente': 16},
    'variables_materializadas': 1442,
    'estados_correspondencias': {
        'documental_revisada': 4506,
        'candidata_por_nombre': 17},
    'columnas_totales_examinadas': 5523,
    'columnas_con_correspondencia': 4523,
    'conceptos_compartidos': 1106,
    'referencias_catalogo_sin_resolver': 1,
    'sistemas_identificadores_recuperados': 1,
    'condiciones_conexion': 6,
    'referencias_catalogo_con_recurso_identificado': 16}
PREDICADOS_PROHIBIDOS = frozenset({
    MEX.datoscore, MEX.estadoPropuesta, MEX.motivoNegativo, MEX.negativo,
    MEX.factorConversion, MEX.factoresConversion, MEX.conversion,
    QUDT.conversionMultiplier, QUDT.conversionOffset, QUDT.hasQuantityKind,
    QUDT.quantityValue, QUDT.QuantityValue})
OBJETOS_PROHIBIDOS = frozenset({
    QUDT.QuantityValue, QUDT_UNIT.M3, QUDT_UNIT.M3_})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def canon(value):
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode('utf-8')).hexdigest()


def _sha_text(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _uuid_text(value):
    if not isinstance(value, str):
        return False
    try:
        return str(uuid.UUID(value)) == value
    except (ValueError, AttributeError):
        return False


def _url(value, http=False):
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        return False
    if any(c in value for c in '<>"{}|\\^`'):
        return False
    parsed = urlsplit(value)
    schemes = {'http'} if http else {'http', 'https'}
    return parsed.scheme in schemes and bool(parsed.netloc)


def _id(value):
    return isinstance(value, str) and re.fullmatch(
        r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}', value) is not None


def dentro(root, rel):
    """Resuelve una ruta relativa y la confina a root; rechaza escapes."""
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        raise ValueError('Ruta de evidencia no relativa: ' + repr(rel))
    if rel.startswith(('/', '\\')) or '\\' in rel:
        raise ValueError('Ruta de evidencia no POSIX: ' + rel)
    parts = Path(rel).parts
    if any(part in ('..', '') for part in parts) or ':' in parts[0]:
        raise ValueError('Ruta de evidencia con segmento no permitido: ' + rel)
    root = Path(root).resolve()
    path = (root / rel).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError('Evidencia fuera de carpeta: ' + rel)
    return path


def comprobar_resumen(summary):
    """Exige el snapshot R9 completo, no solo los cinco conteos citados."""
    if summary != RESUMEN_R9:
        raise ValueError(
            'Snapshot R9 alterado: se exige 1423/1106/4506/17/1442 y el resto exacto')


def _plano(text):
    return unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('ascii').lower().strip()


def _politica_literal(literal, qudt):
    """Puerta explícita para literales ambiguos; no normaliza el literal."""
    plano = _plano(literal)
    if plano in {'hm3', 'hectometro cubico', 'hectometros cubicos'}:
        raise ValueError('hm3 sin termino exacto verificado: no admisible')
    if plano in {'m3', 'metro cubico', 'metros cubicos'}:
        raise ValueError('M3 no admisible en R10: no se sustituye hm3')
    if plano in {'tonelada', 'toneladas'} and qudt != str(QUDT_UNIT.TON):
        raise ValueError('Toneladas ambiguas: solo tonelada metrica exacta (QUDT TON)')
    if qudt in {str(QUDT_UNIT.M3), str(QUDT_UNIT.M3_)}:
        raise ValueError('M3 prohibido en R10')


def _validar_unidad(unit, ids, sujetos, definiciones, pares):
    if not isinstance(unit, dict):
        raise ValueError('Unidad R10 debe ser objeto')
    keys = set(unit)
    if not CAMPOS_UNIDAD <= keys or not keys <= CAMPOS_UNIDAD | CAMPOS_UNIDAD_OPCIONALES:
        raise ValueError('Esquema de unidad R10 inexacto: ' + repr(sorted(keys)))
    uid = unit['id']
    if not _id(uid) or uid in ids:
        raise ValueError('Identificador de unidad R10 invalido o duplicado: ' + repr(uid))
    ids.add(uid)
    if not _uuid_text(unit['diccionario']) or not _uuid_text(unit['conjunto']):
        raise ValueError('UUID de fuente R10 invalido: ' + uid)
    if not isinstance(unit['fila'], int) or isinstance(unit['fila'], bool) or unit['fila'] < 1:
        raise ValueError('Fila R10 invalida: ' + uid)
    for key in ('nombre', 'unidad_literal'):
        if not isinstance(unit[key], str) or not unit[key]:
            raise ValueError('Texto R10 vacio: ' + key)
    for key in ('sujeto', 'variable', 'definicion_iri', 'fuente_url'):
        if not _url(unit[key]):
            raise ValueError('URL R10 invalida: ' + key)
    if not unit['sujeto'].startswith(BASE):
        raise ValueError('Sujeto R10 fuera de la base IRI actual')
    if not unit['variable'].startswith(BASE + 'documented-variable/'):
        raise ValueError('Variable R10 fuera del espacio documentado')
    if not unit['definicion_iri'].startswith(BASE + 'definition/'):
        raise ValueError('Definicion R10 fuera del espacio documentado')
    if not _url(unit['unidad_qudt'], http=True) or not unit['unidad_qudt'].startswith(str(QUDT_UNIT)):
        raise ValueError('Unidad QUDT R10 debe ser IRI http canonica de unit:')
    if unit['normativa_uri'] != unit['unidad_qudt']:
        raise ValueError('URI canonica normativa distinta de la unidad QUDT')
    if not _sha_text(unit['huella_fila_diccionario']) or not _sha_text(unit['normativa_sha256']):
        raise ValueError('SHA R10 invalido: ' + uid)
    if unit['fuente_url'] == unit['normativa_uri']:
        raise ValueError('Procedencia R10 sin URL local distinta de la normativa')
    for key in CAMPOS_UNIDAD_OPCIONALES:
        if key in unit and (not isinstance(unit[key], str) or not unit[key].strip()):
            raise ValueError('Anotacion R10 vacia: ' + key)
    if 'evidencia_normativa' in unit and unit['normativa_sha256'] not in unit['evidencia_normativa']:
        raise ValueError('Evidencia normativa R10 sin SHA fijado')
    _politica_literal(unit['unidad_literal'], unit['unidad_qudt'])
    if unit['sujeto'] in sujetos or unit['definicion_iri'] in definiciones:
        raise ValueError('Unidad R10 duplicada por sujeto o definicion: ' + uid)
    if (unit['diccionario'], unit['fila']) in pares:
        raise ValueError('Unidad R10 duplicada por diccionario/fila: ' + uid)
    sujetos.add(unit['sujeto'])
    definiciones.add(unit['definicion_iri'])
    pares.add((unit['diccionario'], unit['fila']))


def _validar_aceptadas(accepted):
    if not isinstance(accepted, dict) or set(accepted) != CAMPOS_ACEPTADAS:
        raise ValueError('Esquema de aceptadas R10 inexacto')
    if accepted['format_version'] != 1 or accepted['release'] != 'R10' or accepted['release_base'] != 'R9':
        raise ValueError('Formato/lanzamiento R10 incorrectos')
    unidades = accepted['unidades']
    formas = accepted['formas']
    if not isinstance(unidades, list) or len(unidades) > MAX_UNIDADES:
        raise ValueError('R10 admite 0..6 unidades')
    if not isinstance(formas, list):
        raise ValueError('Formas R10 deben ser lista')
    ids = set()
    sujetos, definiciones, pares = set(R9_SUJETOS), set(R9_DEFINICIONES), set(R9_PINES)
    for unit in unidades:
        _validar_unidad(unit, ids, sujetos, definiciones, pares)
    for forma in formas:
        if not isinstance(forma, dict) or set(forma) != CAMPOS_FORMA:
            raise ValueError('Esquema de forma R10 inexacto')
        fid = forma['id']
        if not _id(fid) or fid in ids:
            raise ValueError('Identificador de forma R10 invalido o duplicado: ' + repr(fid))
        ids.add(fid)
    archivos = accepted['archivos_instalables']
    if (not isinstance(archivos, dict) or not {'datos', 'shapes'} <= set(archivos)
            or not set(archivos) <= {'datos', 'shapes', 'modelo'}):
        raise ValueError('archivos_instalables R10 debe cubrir datos/shapes y modelo opcional')
    if any(not _sha_text(value) for value in archivos.values()):
        raise ValueError('SHA de archivo instalable R10 invalido')
    return ids


def _validar_archivos(folder, accepted, files):
    archivos = accepted['archivos_instalables']
    for kind, rel in ARCHIVOS.items():
        path = dentro(folder, rel)
        if not path.is_file() or sha(path) != archivos[kind]:
            raise ValueError('Archivo instalable R10 alterado: ' + rel)
        if files.get(rel) != archivos[kind]:
            raise ValueError('Manifiesto R10 no coincide con archivo instalable: ' + rel)
    if 'modelo' in archivos:
        path = dentro(folder, MODELO)
        if not path.is_file() or sha(path) != archivos['modelo']:
            raise ValueError('Modelo R10 alterado')
        if files.get(MODELO) != archivos['modelo']:
            raise ValueError('Manifiesto R10 no coincide con modelo')
    elif MODELO in files:
        raise ValueError('Modelo R10 en manifiesto sin declararse instalable')


def _auditorias(folder, accepted, ids):
    aceptadas = dentro(folder, 'aceptadas.json')
    for name in ('a', 'b'):
        audit = read(dentro(folder, f'auditorias/{name}.json'))
        if not isinstance(audit, dict):
            raise ValueError('Auditoria R10 debe ser objeto: ' + name)
        if audit.get('auditor') != name or audit.get('dictamen') != 'aceptar':
            raise ValueError('Dictamen R10 ausente o no aceptado: ' + name)
        if audit.get('aceptadas_sha256') != sha(aceptadas):
            raise ValueError('Auditoria R10 no cubre el SHA exacto de aceptadas: ' + name)
        rows = audit.get('dictamenes')
        if not isinstance(rows, list):
            raise ValueError('Dictamenes R10 deben ser lista: ' + name)
        seen = []
        for row in rows:
            if (not isinstance(row, dict) or row.get('dictamen') != 'aceptar'
                    or not isinstance(row.get('id'), str)):
                raise ValueError('Dictamen R10 invalido: ' + name)
            seen.append(row['id'])
        if len(seen) != len(set(seen)) or set(seen) != ids:
            raise ValueError('Aprobacion R10 incompleta por unidad/forma: ' + name)


def _datos(folder, accepted):
    graph = Graph().parse(dentro(folder, ARCHIVOS['datos']), format='turtle')
    units = accepted['unidades']
    expected = set()
    subjects = {URIRef(unit['sujeto']) for unit in units}
    actual = set(graph.subjects())
    if actual != subjects:
        raise ValueError('Sujetos R10 fuera de la whitelist: '
                         + repr(sorted(str(s) for s in actual ^ subjects)))
    for unit in units:
        subject = URIRef(unit['sujeto'])
        expected.add((subject, RDF.type, MEX.UnidadDeclarada))
        expected.add((subject, MEX.variableDocumentada, URIRef(unit['variable'])))
        expected.add((subject, MEX.definicionFuente, URIRef(unit['definicion_iri'])))
        expected.add((subject, MEX.conjuntoFuente, Literal(unit['conjunto'])))
        expected.add((subject, MEX.diccionarioFuente, Literal(unit['diccionario'])))
        expected.add((subject, MEX.unidadLiteral, Literal(unit['unidad_literal'])))
        expected.add((subject, MEX.unidadQudt, URIRef(unit['unidad_qudt'])))
        expected.add((subject, PROV.wasDerivedFrom, URIRef(unit['fuente_url'])))
        expected.add((subject, PROV.wasDerivedFrom, URIRef(unit['normativa_uri'])))
        for key, predicate in (('etiqueta', RDFS.label), ('comentario', RDFS.comment),
                               ('evidencia_normativa', MEX.evidenciaNormativa)):
            if key in unit:
                expected.add((subject, predicate, Literal(unit[key])))
    qudt_units = {URIRef(unit['unidad_qudt']) for unit in units}
    for subject, predicate, obj in graph:
        if not isinstance(subject, URIRef):
            raise ValueError('Sujeto R10 no IRI')
        if predicate in PREDICADOS_PROHIBIDOS:
            raise ValueError('Predicado R10 prohibido: ' + str(predicate))
        if isinstance(obj, URIRef) and obj in OBJETOS_PROHIBIDOS:
            raise ValueError('Objeto R10 prohibido: ' + str(obj))
        if predicate == MEX.unidadQudt and obj not in qudt_units:
            raise ValueError('Unidad QUDT R10 no declarada')
    extra = set(graph) - expected
    missing = expected - set(graph)
    if extra or missing:
        raise ValueError('Grafo R10 fuera de la whitelist estructural: extra='
                         + repr(sorted(map(str, extra))) + ' missing='
                         + repr(sorted(map(str, missing))))
    return graph


def _modelo(folder, accepted):
    if 'modelo' not in accepted['archivos_instalables']:
        return Graph()
    graph = Graph().parse(dentro(folder, MODELO), format='turtle')
    terms = {'UnidadDeclarada', 'variableDocumentada', 'definicionFuente',
             'conjuntoFuente', 'diccionarioFuente', 'unidadLiteral',
             'unidadQudt', 'evidenciaNormativa'}
    if set(graph.subjects()) != {MEX[term] for term in terms}:
        raise ValueError('Modelo R10 fuera del vocabulario minimo')
    for subject, predicate, obj in graph:
        if predicate not in {RDF.type, RDFS.label, RDFS.comment}:
            raise ValueError('Modelo R10 con inferencias adicionales')
        expected_type = RDFS.Class if subject == MEX.UnidadDeclarada else RDF.Property
        if predicate == RDF.type and obj != expected_type:
            raise ValueError('Tipo de vocabulario R10 no permitido')
        if predicate != RDF.type and not isinstance(obj, Literal):
            raise ValueError('Modelo R10 con anotacion no literal')
    for term in terms:
        expected_type = RDFS.Class if term == 'UnidadDeclarada' else RDF.Property
        if (MEX[term], RDF.type, expected_type) not in graph:
            raise ValueError('Tipo de vocabulario R10 ausente: ' + term)
    return graph


def _shapes(folder, accepted):
    graph = Graph().parse(dentro(folder, ARCHIVOS['shapes']), format='turtle')
    formas = accepted['formas']
    if not formas:
        if len(graph):
            raise ValueError('Formas R10 vacias pero shapes/adicionales.ttl no esta vacio')
        return graph
    if not len(graph):
        raise ValueError('Formas R10 declaradas sin shapes/adicionales.ttl')
    allowed = (str(SH), str(RDF), str(RDFS), str(XSD), str(MEX), str(PROV), BASE)
    for subject, predicate, obj in graph:
        if not isinstance(predicate, URIRef):
            raise ValueError('Shape R10 con predicado no IRI')
        if not any(str(predicate).startswith(prefix) for prefix in allowed):
            raise ValueError('Shape R10 con predicado fuera de SHACL/RDF/RDFS/XSD/mex: '
                             + str(predicate))
        if isinstance(obj, URIRef) and not any(str(obj).startswith(prefix) for prefix in allowed):
            raise ValueError('Shape R10 con objeto fuera de SHACL/RDF/RDFS/XSD/mex: '
                             + str(obj))
        if (isinstance(obj, Literal) and obj.datatype is not None
                and not str(obj.datatype).startswith(str(XSD))):
            raise ValueError('Shape R10 con literal de tipo ajeno: ' + str(obj.datatype))
    declared = {f['id'] for f in formas}
    actual = {str(s).rsplit('/', 1)[-1]
              for s in graph.subjects(RDF.type, SH.NodeShape)}
    if actual != declared:
        raise ValueError('IDs de formas R10 no coinciden con NodeShapes reales')
    node_shapes = bool(actual)
    property_shapes = any(True for _ in graph.subjects(RDF.type, SH.PropertyShape))
    if not node_shapes and not property_shapes:
        raise ValueError('Shapes R10 sin forma SHACL')
    return graph


def cargar(root=ROOT):
    root = Path(root)
    cp = root / 'ontologia/revision-ronda-10.json'
    config = read(cp)
    if (not isinstance(config, dict)
            or set(config) != {'format_version', 'release', 'evidencia', 'manifiesto_sha256'}):
        raise ValueError('Esquema de configuracion R10 inexacto')
    if config['format_version'] != 1 or config['release'] != 'R10' or config['evidencia'] != EVIDENCIA:
        raise ValueError('Configuracion R10 inexacta')
    if not _sha_text(config['manifiesto_sha256']):
        raise ValueError('SHA de manifiesto R10 invalido')
    folder = dentro(root, EVIDENCIA)
    mp = dentro(folder, 'manifiesto.json')
    if sha(mp) != config['manifiesto_sha256']:
        raise ValueError('Manifiesto R10 alterado')
    manifest = read(mp)
    if (not isinstance(manifest, dict)
            or set(manifest) != {'format_version', 'release', 'archivos'}):
        raise ValueError('Esquema de manifiesto R10 inexacto')
    if manifest['format_version'] != 1 or manifest['release'] != 'R10':
        raise ValueError('Manifiesto R10 de otro formato/lanzamiento')
    files = manifest['archivos']
    if not isinstance(files, dict) or not files:
        raise ValueError('Manifiesto R10 sin archivos')
    verified, resolved = {}, set()
    for rel, digest in files.items():
        if not _sha_text(digest):
            raise ValueError('SHA de manifiesto R10 invalido: ' + repr(rel))
        path = dentro(folder, rel)
        if path in resolved:
            raise ValueError('Ruta R10 duplicada en manifiesto: ' + rel)
        resolved.add(path)
        if not path.is_file() or sha(path) != digest:
            raise ValueError('Evidencia R10 alterada: ' + rel)
        verified[rel] = path
    live_config_bytes = (root / 'config.toml').read_bytes()
    live_config = tomllib.loads(live_config_bytes.decode('utf-8'))['catalogo']
    if live_config.get('base_iri') != BASE_IRI_ACTUAL:
        raise ValueError('baseIRI actual distinta de la fijada: migracion fuera de alcance')
    evidence_config = dentro(folder, 'config-iri-base.toml')
    if evidence_config.read_bytes() != live_config_bytes:
        raise ValueError('config-iri-base.toml no es copia byte a byte de config.toml')
    baseline_path = dentro(folder, 'base-semantica.json')
    if sha(baseline_path) != PIN_REGLAS:
        raise ValueError('Snapshot de reglas R9 no es el fijado dba467b6')
    baseline = read(baseline_path)
    if baseline != read(root / 'ontologia/semantica.json'):
        raise ValueError('Reglas vivas distintas del snapshot R9')
    cob9 = read(dentro(folder, 'cobertura-r9.json'))
    comprobar_resumen(cob9.get('resumen'))
    accepted = read(dentro(folder, 'aceptadas.json'))
    ids = _validar_aceptadas(accepted)
    required = set(OBLIGATORIOS)
    required |= {f'filas/{unit["id"]}.json' for unit in accepted['unidades']}
    required |= {f'normativa/{unit["id"]}.txt' for unit in accepted['unidades']}
    if 'modelo' in accepted['archivos_instalables']:
        required.add(MODELO)
    if set(files) != required:
        raise ValueError('Manifiesto R10 no coincide con archivos obligatorios: '
                         + repr(sorted(set(files) ^ required)))
    _validar_archivos(folder, accepted, files)
    _auditorias(folder, accepted, ids)
    _datos(folder, accepted)
    _modelo(folder, accepted)
    _shapes(folder, accepted)
    sources = {
        'revision_ronda_10': cp,
        'manifiesto_ronda_10': mp,
        'config_iri_base_r10': evidence_config,
        'base_semantica_r10': baseline_path,
        'cobertura_r9_r10': dentro(folder, 'cobertura-r9.json')}
    for rel, path in verified.items():
        sources['ronda_10_' + rel] = path
    return config, folder, baseline, accepted, cob9, sources


def _index(variables):
    index = {}
    for variable in variables:
        definition = variable.get('definicion_iri')
        if not definition:
            continue
        if definition in index:
            raise ValueError('Definicion duplicada en reporte R10: ' + definition)
        index[definition] = variable
    return index


def construir(report, rules, base, root=ROOT):
    config, folder, baseline, accepted, cob9, sources = cargar(root)
    if base != BASE_IRI_ACTUAL:
        raise ValueError('R10 exige la baseIRI actual sin migracion')
    if rules != baseline:
        raise ValueError('R10 exige las reglas R9 intactas')
    if report.get('resumen') != cob9.get('resumen'):
        raise ValueError('Reporte vivo distinto del snapshot R9')
    comprobar_resumen(report.get('resumen'))
    live = _index(report.get('variables', []))
    old = _index(cob9.get('variables', []))
    for unit in accepted['unidades']:
        definition = unit['definicion_iri']
        if definition not in live or definition not in old:
            raise ValueError('Unidad R10 sin definicion viva respaldada: ' + unit['id'])
        if live[definition] != old[definition]:
            raise ValueError('Variable R10 cambio de contexto en reporte vivo: ' + unit['id'])
        variable = old[definition]
        if variable.get('estado') != 'respaldada_por_definicion':
            raise ValueError('Unidad R10 sin significado respaldado: ' + unit['id'])
        for key, variable_key in (
                ('variable', 'iri'), ('definicion_iri', 'definicion_iri'),
                ('conjunto', 'conjunto'), ('diccionario', 'diccionario'),
                ('nombre', 'variable'),
                ('huella_fila_diccionario', 'huella_fila_diccionario')):
            if unit[key] != variable.get(variable_key):
                raise ValueError('Variable/fuente R10 inexacta: ' + unit['id'] + ' ' + key)
        row = read(dentro(folder, f'filas/{unit["id"]}.json'))
        if canon(row) != unit['huella_fila_diccionario']:
            raise ValueError('Fila R10 alterada: ' + unit['id'])
        if row.get('Unidad de medida') != unit['unidad_literal']:
            raise ValueError('Literal de unidad R10 no coincide con la fila: ' + unit['id'])
        if row.get('Nombre variable') != unit['nombre']:
            raise ValueError('Nombre de variable R10 no coincide con la fila: ' + unit['id'])
        norm = dentro(folder, f'normativa/{unit["id"]}.txt')
        if sha(norm) != unit['normativa_sha256']:
            raise ValueError('Normativa R10 alterada: ' + unit['id'])
        text = norm.read_text(encoding='utf-8')
        if '3.5.3' not in text:
            raise ValueError('Normativa R10 sin version QUDT 3.5.3: ' + unit['id'])
        if unit['normativa_uri'] not in text:
            raise ValueError('Normativa R10 sin URI canonica exacta: ' + unit['id'])
    graph = _datos(folder, accepted) + _modelo(folder, accepted)
    for unit in accepted['unidades']:
        for rel in (f'filas/{unit["id"]}.json', f'normativa/{unit["id"]}.txt'):
            path = dentro(folder, rel)
            entity = URIRef(path.as_uri())
            graph.add((entity, RDF.type, PROV.Entity))
            graph.add((entity, MEX.sha256Evidencia, Literal(sha(path))))
            graph.add((URIRef(unit['sujeto']), PROV.wasDerivedFrom, entity))
    receipt = {
        'format_version': 1,
        'release': 'R10',
        'release_base': 'R9',
        'base_iri': BASE_IRI_ACTUAL,
        'declaraciones_unidad': len(accepted['unidades']),
        'formas_shacl': len(accepted['formas']),
        'manifiesto_sha256': config['manifiesto_sha256'],
        'archivos_instalables': dict(accepted['archivos_instalables']),
        'base_semantica_sha256': sha(dentro(folder, 'base-semantica.json')),
        'cobertura_r9_sha256': sha(dentro(folder, 'cobertura-r9.json')),
        'config_sha256': sha(Path(root) / 'config.toml')}
    return graph, receipt, sources


def cargar_shapes(root=ROOT):
    _, folder, _, accepted, _, _ = cargar(root)
    return _shapes(folder, accepted)
