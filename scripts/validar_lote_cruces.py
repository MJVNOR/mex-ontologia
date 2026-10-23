"""Diagnóstico de todos los candidatos prioritarios y ejecución de estrategias explícitas."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import re
import tomllib

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef, XSD
from construir_catalogo import ROOT, PROV
from cruzar_registro_civil import entero
from inspeccionar_contenido import descargar, tablas
from integrar_contenido import clave, valor
from inventariar_portal import api

OUT = ROOT / 'data/portal/lote-cruces'


def guardar(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def huella(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalizar_clave(value):
    if value is None or not str(value).strip():
        return None
    # No eliminar acentos, signos ni ceros de códigos locales para hacerlos coincidir.
    return ' '.join(str(value).strip().split())


def diagnosticar_valores(rows, names):
    result = {}
    for name in names:
        values = [normalizar_clave(r.get(name)) for r in rows]
        nonnull = [v for v in values if v is not None]
        result[name] = {'filas_muestra': len(rows), 'nulos': len(values) - len(nonnull),
                        'distintos_muestra': len(set(nonnull)), 'repeticiones_muestra': len(nonnull) - len(set(nonnull)),
                        'valores_muestra_clave': sorted(set(nonnull))[:100]}
    return result


def comparar_muestras(pair, profiles, a, b):
    comparisons = []
    for assessment in pair['evaluacion_claves']:
        family = assessment['familia']
        sides = []
        for dataset, sample in [(pair['conjunto_a'], a), (pair['conjunto_b'], b)]:
            if not sample or not sample['ok']:
                sides.append((set(), []))
                continue
            columns = [c for c in profiles[dataset]['columnas_clave'] if c['familia'] == family and c['recurso_id'] == sample['recurso_id']]
            names = sorted({c['campo'] for c in columns} & set(sample['campos']))
            values = {v for name in names for v in sample['campos'][name]['valores_muestra_clave']}
            sides.append((values, names))
        va, vb = sides[0][0], sides[1][0]
        comparisons.append({'familia': family, 'campos_a': sides[0][1], 'campos_b': sides[1][1],
                            'valores_distintos_a': len(va), 'valores_distintos_b': len(vb), 'coincidencias_exactas_muestra': len(va & vb),
                            'ejemplos_coincidentes': sorted(va & vb)[:10],
                            'interpretacion': 'Coincidencia textual muestral, sin equivalencia ni cobertura demostradas' if va & vb else
                            'Sin coincidencias en estas muestras; no demuestra incompatibilidad del conjunto'})
    return comparisons


def lectura_educativa(resource, inspection, definitions, refresh=False):
    """Lee una tabla completa de indicadores públicos, sin promediar ni enlazar personas."""
    signature = hashlib.sha256(json.dumps([resource['id'], 'educacion_v1']).encode()).hexdigest()
    path = OUT / 'agregados' / (signature + '.json')
    if path.exists() and not refresh:
        return json.loads(path.read_text(encoding='utf-8'))
    result = {'recurso_id': resource['id'], 'conjunto_id': resource['conjunto_id'], 'nombre': resource['nombre'],
              'ok': False, 'consultado_en_utc': datetime.now(timezone.utc).isoformat(),
              'estrategia': {'medida': 'conteos_de_' + clave(resource['conjunto']), 'grano_origen': 'programa_sede_periodo_declarado'}}
    try:
        data, evidence = descargar(resource['url'])
        if not evidence['completo']:
            raise ValueError('Archivo incompleto')
        sheets = dict(tablas(data, resource['formato'], True, diccionario=True))
        matching = [t for t in inspection['tablas'] if any(f['id'] == 'Programa Educativo' for f in t['campos'])]
        if len(matching) != 1:
            raise ValueError('Hoja educativa ambigua')
        table = matching[0]
        rows = sheets[table['hoja']]
        if len(rows) >= 10001:
            raise ValueError('Tabla no leída completa')
        fields = {f['id']: f['posicion_original'] - 1 for f in table['campos']}
        program_index = fields.pop('Programa Educativo')
        d = definitions[resource['conjunto_id']]
        if clave(d.get('Programa Educativo', {}).get('descripcion', '')) != 'nombre del programa educativo':
            raise ValueError('Definición de programa no respaldada')
        for name in fields:
            description = clave(d.get(name, {}).get('descripcion', ''))
            if 'numero de estudiantes' not in description or clave(name) not in description:
                raise ValueError('Medida de sede sin definición explícita de número de estudiantes: ' + name)
        seen, values, raw_programs, controls = set(), [], {}, {}
        for row in rows[table['fila_encabezado']:]:
            if not any(str(v).strip() for v in row):
                continue
            raw = str(row[program_index]).strip() if len(row) > program_index else ''
            program = ' '.join(raw.split()).casefold()
            if not program:
                raise ValueError('Fila de medidas sin programa')
            if program in {'total', 'totales', 'total general'}:
                if controls:
                    raise ValueError('Más de una fila de totales')
                controls = {name: entero(row[i]) if len(row) > i and str(row[i]).strip() else None for name, i in fields.items()}
                continue
            if program in seen:
                raise ValueError('Nombre de programa duplicado al normalizar mayúsculas y espacios')
            seen.add(program)
            raw_programs[program] = raw
            for name, i in fields.items():
                value = entero(row[i]) if len(row) > i and str(row[i]).strip() else None
                if value is not None and value < 0:
                    raise ValueError('Medida negativa')
                values.append({'programa_clave_local': program, 'programa_declarado': raw, 'sede_declarada': name, 'valor': value})
        for name, control in controls.items():
            if control is not None and control != sum(v['valor'] for v in values if v['sede_declarada'] == name and v['valor'] is not None):
                raise ValueError('Fila total no concuerda con programas')
        period = re.findall(r'\b(?:19|20)\d{2}\b', resource['nombre'])
        if len(period) != 2:
            raise ValueError('Periodo declarado no inequívoco')
        result.update(ok=True, periodo_declarado='-'.join(period), evidencia=evidence, filas_programa=len(seen), valores=values,
                      valor_total=sum(v['valor'] for v in values if v['valor'] is not None), total_filas=len(seen),
                      alcance='Comparación exploratoria de indicadores publicados por programa y sede con periodo coincidente en metadatos. No cohorte ni tasa; no se valida externamente el periodo.')
    except Exception as error:
        result['error'] = f'{type(error).__name__}: {error}'
    guardar(path, result)
    return result


def unir_educacion(a, b):
    if not a['ok'] or not b['ok'] or a['periodo_declarado'] != b['periodo_declarado']:
        raise ValueError('Fuentes educativas sin validación o periodo declarado coincidente')
    aa = {(v['programa_clave_local'], v['sede_declarada']): v for v in a['valores']}
    bb = {(v['programa_clave_local'], v['sede_declarada']): v for v in b['valores']}
    if len(aa) != len(a['valores']) or len(bb) != len(b['valores']):
        raise ValueError('Grano educativo duplicado')
    return [{'programa_clave_local': k[0], 'sede_declarada': k[1],
             'programa_declarado_a': aa.get(k, {}).get('programa_declarado'), 'programa_declarado_b': bb.get(k, {}).get('programa_declarado'),
             'periodo_declarado': a['periodo_declarado'], 'valor_a': aa.get(k, {}).get('valor'), 'valor_b': bb.get(k, {}).get('valor'),
             'presente_en_ambas': k in aa and k in bb} for k in sorted(set(aa) | set(bb))]


def muestra(recurso, fields, inspection, refresh=False):
    signature = hashlib.sha256(json.dumps([recurso['id'], recurso.get('url'), sorted(fields)], ensure_ascii=False).encode()).hexdigest()
    path = OUT / 'muestras' / (signature + '.json')
    if path.exists() and not refresh:
        return json.loads(path.read_text(encoding='utf-8'))
    result = {'recurso_id': recurso['id'], 'nombre': recurso['nombre'], 'conjunto': recurso['conjunto'],
              'consultado_en_utc': datetime.now(timezone.utc).isoformat(), 'ok': False, 'limite': 100,
              'campos_solicitados': sorted(fields)}
    try:
        if recurso.get('datastore', {}).get('ok'):
            response = api('datastore_search', resource_id=recurso['id'], fields=','.join(fields), limit=100, sort='_id asc')
            if not response['ok']:
                raise ValueError(str(response.get('error', response)))
            result.update(fuente=response['url'], metodo='muestra_api', total_declarado=response['result'].get('total'))
            rows = response['result']['records']
        else:
            data, evidence = descargar(recurso['url'], parcial=recurso['formato'].upper() == 'CSV')
            sheets = dict(tablas(data, recurso['formato'].upper(), evidence['completo']))
            choices = [(sum(f['id'] in fields for f in t['campos']), t) for t in inspection.get('tablas', [])]
            if not choices:
                raise ValueError('No hay esquema de archivo recuperado')
            _, table = max(choices, key=lambda x: x[0])
            if not any(f['id'] in fields for f in table['campos']):
                raise ValueError('Las claves candidatas no aparecen en la hoja inspeccionada')
            sheet = sheets[table['hoja']]
            start = table['fila_encabezado']
            rows = [{f['id']: row[f['posicion_original'] - 1] if len(row) >= f['posicion_original'] else None
                     for f in table['campos'] if f['id'] in fields} for row in sheet[start:start + 100]
                    if any(str(v).strip() for v in row)]
            result.update(fuente=recurso['url'], metodo='muestra_archivo_acotado', hoja=table['hoja'],
                          limite=30 - start, evidencia_archivo=evidence)
        result.update(ok=True, campos=diagnosticar_valores(rows, fields), filas_muestra=len(rows),
                      alcance='Diagnóstico de muestra; no demuestra unicidad ni cobertura integral')
    except Exception as error:
        result['error'] = f'{type(error).__name__}: {error}'
    guardar(path, result)
    return result


def referencia_municipal(inventory, refresh=False):
    path = OUT / 'catalogo-municipal-portal.json'
    resource = next(r for r in inventory['recursos'] if r['nombre'] == 'Mapa' and r['formato'] == 'JSON')
    if path.exists() and not refresh:
        return json.loads(path.read_text(encoding='utf-8'))
    result = {'recurso_id': resource['id'], 'fuente': resource['url'], 'ok': False,
              'consultado_en_utc': datetime.now(timezone.utc).isoformat()}
    try:
        data, evidence = descargar(resource['url'])
        geo = json.loads(data)
        if geo.get('type') != 'FeatureCollection':
            raise ValueError('No es FeatureCollection')
        by_code = {}
        for feature in geo['features']:
            p = feature['properties']
            ent, mun = str(p['CVE_ENT']).zfill(2), str(p['CVE_MUN']).zfill(3)
            code = str(p['CVEGEO'])
            if ent != '26' or code != ent + mun or not 1 <= entero(mun) <= 72 or not p.get('NOMGEO'):
                raise ValueError('Clave geográfica inconsistente')
            value = {'cvegeo': code, 'cve_ent': ent, 'cve_mun': mun, 'nombre': p['NOMGEO']}
            if code in by_code and by_code[code] != value:
                raise ValueError('Conflicto de nombre para el mismo código')
            by_code[code] = value
        if set(int(v['cve_mun']) for v in by_code.values()) != set(range(1, 73)):
            raise ValueError('Referencia no cubre códigos municipales 1–72')
        result.update(ok=True, evidencia=evidence, municipios=sorted(by_code.values(), key=lambda x: x['cvegeo']),
                      alcance='Referencia geográfica publicada por el portal; no prueba que otros códigos locales usen este catálogo')
    except Exception as error:
        result['error'] = str(error)
    guardar(path, result)
    return result


def estrategia_registro(resource, definitions):
    title = resource['conjunto']
    if title not in {'Matrimonios', 'Divorcios', 'Nacimientos'} or not resource.get('datastore', {}).get('ok'):
        return None
    year = {'Matrimonios': 'año_matrimonio', 'Divorcios': 'año_registro', 'Nacimientos': 'año'}[title]
    d = definitions.get(resource['conjunto_id'], {})
    if clave(d.get('municipio', {}).get('descripcion', '')) != 'municipio de registro' or 'registro' not in clave(d.get(year, {}).get('descripcion', '')):
        return None
    schema = {f['id'] for f in resource['datastore']['campos']}
    required = {'_id', 'municipio', year} | ({'mes', 'total', 'hombres', 'mujeres'} if title == 'Nacimientos' else set())
    if not required <= schema:
        return None
    if title == 'Nacimientos' and clave(d.get('total', {}).get('descripcion', '')) != 'total de nacimientos':
        return None
    years = re.findall(r'\b(?:19|20)\d{2}\b', resource['nombre'] or '')
    if len(years) != 1:
        return None
    return {'anio': int(years[0]), 'campo_anio': year, 'campos': sorted(required),
            'medida': 'suma_total_nacimientos' if title == 'Nacimientos' else 'conteo_filas_' + clave(title),
            'grano_origen': 'municipio_mes' if title == 'Nacimientos' else 'fila_registro_publicado'}


def agregar_validado(resource, strategy, refresh=False, retry_errors=False):
    signature = hashlib.sha256(json.dumps([resource['id'], strategy], sort_keys=True).encode()).hexdigest()
    path = OUT / 'agregados' / (signature + '.json')
    if path.exists() and not refresh:
        cached = json.loads(path.read_text(encoding='utf-8'))
        if cached['ok'] or not retry_errors:
            return cached
    result = {'recurso_id': resource['id'], 'conjunto_id': resource['conjunto_id'], 'nombre': resource['nombre'],
              'consultado_en_utc': datetime.now(timezone.utc).isoformat(), 'estrategia': strategy, 'ok': False}
    try:
        counts, seen, groups, urls = Counter(), set(), set(), []
        offset, expected, digest = 0, None, hashlib.sha256()
        while True:
            response = api('datastore_search', resource_id=resource['id'], fields=','.join(strategy['campos']),
                           sort='_id asc', limit=5000, offset=offset)
            if not response['ok']:
                raise ValueError(str(response.get('error', response)))
            body = response['result']
            expected = body['total'] if expected is None else expected
            if body['total'] != expected or body.get('total_was_estimated'):
                raise ValueError('Total inestable o estimado')
            rows = body['records']
            if not rows and offset < expected:
                raise ValueError('Página incompleta')
            urls.append(response['url'])
            for row in rows:
                if row['_id'] in seen:
                    raise ValueError('ID de fila duplicado')
                seen.add(row['_id'])
                mun, year = entero(row['municipio']), entero(row[strategy['campo_anio']])
                if not 1 <= mun <= 72 or year != strategy['anio']:
                    raise ValueError('Municipio o año fuera de dominio')
                value = 1
                if strategy['grano_origen'] == 'municipio_mes':
                    month, value = entero(row['mes']), entero(row['total'])
                    if not 1 <= month <= 12 or value < 0:
                        raise ValueError('Mes o medida inválida')
                    if entero(row['hombres']) < 0 or entero(row['mujeres']) < 0 or entero(row['hombres']) + entero(row['mujeres']) != value:
                        raise ValueError(f"Total no coincide con hombres + mujeres: _id={row['_id']}, municipio={mun}, mes={month}, hombres={row['hombres']}, mujeres={row['mujeres']}, total={value}. Revisar fuente o definición antes de sumar.")
                    if (mun, month) in groups:
                        raise ValueError('Grano municipio/mes duplicado: sumar duplicaría agregados')
                    groups.add((mun, month))
                counts[(mun, year)] += value
                digest.update((json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n').encode())
            offset += len(rows)
            if offset >= expected:
                break
        final = api('datastore_search', resource_id=resource['id'], limit=0)
        if not final['ok'] or final['result']['total'] != expected or final['result'].get('total_was_estimated') or len(seen) != expected:
            raise ValueError('Total final no coincide')
        if expected == 0:
            raise ValueError('Recurso vacío')
        coverage = {str(mun): sorted(month for m, month in groups if m == mun) for mun, _ in counts} if groups else {}
        # Monthly aggregates cannot be presented as annual if any municipality lacks a month.
        if groups and any(len(months) != 12 for months in coverage.values()):
            missing = {mun: sorted(set(range(1, 13)) - set(months)) for mun, months in coverage.items() if len(months) != 12}
            raise ValueError('Faltan meses por municipio; ausencia no equivale a cero. Ejemplos: ' + json.dumps(dict(list(missing.items())[:5])))
        result.update(ok=True, total_filas=expected, valor_total=sum(counts.values()), consultas=urls,
                      sha256_campos_leidos=digest.hexdigest(), cobertura_meses=coverage,
                      agregados=[{'municipio_local': mun, 'anio_registro': year, 'valor': value} for (mun, year), value in sorted(counts.items())],
                      comprobaciones=['IDs únicos', 'total estable', 'año real verificado', 'dominio de clave', 'agregación previa al join'],
                      limite='API sin instantánea transaccional; conteo de registros publicados sin deduplicación de eventos')
    except Exception as error:
        result.update(ok=False, error=f'{type(error).__name__}: {error}')
    guardar(path, result)
    return result


def unir(a, b):
    if not a['ok'] or not b['ok']:
        raise ValueError('No unir resultados que fallaron validación')
    aa = {(r['municipio_local'], r['anio_registro']): r['valor'] for r in a['agregados']}
    bb = {(r['municipio_local'], r['anio_registro']): r['valor'] for r in b['agregados']}
    if len(aa) != len(a['agregados']) or len(bb) != len(b['agregados']):
        raise ValueError('Grano de salida no único')
    return [{'municipio_local': k[0], 'anio_registro': k[1], 'valor_a': aa.get(k), 'valor_b': bb.get(k),
             'presente_en_ambas': k in aa and k in bb} for k in sorted(set(aa) | set(bb))]


def rdf_lote(report, base):
    g, mex = Graph(), Namespace(base + 'vocab/')
    g.bind('mex', mex)
    for cls, label in [(mex.ValidacionLote, 'Validación de cruce por lote'), (mex.EjecucionCruceLote, 'Ejecución exploratoria de cruce'),
                       (mex.ResultadoCruceLote, 'Resultado agregado del lote'), (mex.ResultadoEducativoLote, 'Comparación de indicadores educativos'),
                       (mex.ReferenciaMunicipalPortal, 'Referencia municipal del portal')]:
        g.add((cls, RDF.type, OWL.Class)).add((cls, RDFS.label, Literal(label, lang='es')))
    objects = {'validacionLote': 'Validación del candidato por lote', 'ejecucionLote': 'Ejecución parcial por recursos',
               'resultadoLote': 'Resultado del cruce agregado'}
    data = {'decisionLote': 'Decisión del lote', 'motivoLote': 'Motivo de la decisión', 'anioLote': 'Año de registro comprobado',
            'codigoLocalLote': 'Código local municipal', 'valorALote': 'Valor de la medida A', 'valorBLote': 'Valor de la medida B',
            'medidaALote': 'Medida A y agregación', 'medidaBLote': 'Medida B y agregación', 'ambasLote': 'Clave presente en ambas fuentes',
            'cvegeoReferencia': 'CVEGEO en referencia del portal', 'nombreMunicipioReferencia': 'Nombre en referencia municipal',
            'programaLocalLote': 'Programa según clave textual local', 'sedeDeclaradaLote': 'Sede declarada',
            'periodoDeclaradoLote': 'Periodo declarado en metadatos', 'alcanceLote': 'Alcance de ejecución y límites'}
    for mapping, cls in [(objects, OWL.ObjectProperty), (data, OWL.DatatypeProperty)]:
        for key, label in mapping.items():
            g.add((mex[key], RDF.type, cls)).add((mex[key], RDFS.label, Literal(label, lang='es')))
    source = URIRef((OUT / 'validacion-lote.json').as_uri())
    for pair in report['pares']:
        node = URIRef(base + 'batch-validation/' + pair['id'])
        g.add((node, RDF.type, mex.ValidacionLote)).add((node, RDFS.label, Literal(pair['titulo_a'] + ' ↔ ' + pair['titulo_b'], lang='es')))
        g.add((URIRef(base + 'opportunity/' + pair['id']), mex.validacionLote, node))
        g.add((node, mex.decisionLote, Literal(pair['decision'])))
        g.add((node, PROV.wasDerivedFrom, source))
        for reason in pair['motivos']:
            g.add((node, mex.motivoLote, Literal(reason)))
        for execution in pair['ejecuciones']:
            enode = URIRef(base + 'batch-execution/' + execution['id'])
            g.add((enode, RDF.type, mex.EjecucionCruceLote)).add((enode, RDFS.label, Literal(pair['titulo_a'] + ' ↔ ' + pair['titulo_b'] + ' — ' + str(execution['anio']), lang='es')))
            g.add((node, mex.ejecucionLote, enode)).add((enode, PROV.wasDerivedFrom, source))
            if execution.get('anio') is not None:
                g.add((enode, mex.anioLote, Literal(execution['anio'])))
            if execution.get('periodo'):
                g.add((enode, mex.periodoDeclaradoLote, Literal(execution['periodo'])))
            g.add((enode, mex.alcanceLote, Literal(execution['alcance'])))
            g.add((enode, mex.medidaALote, Literal(execution['fuente_a']['estrategia']['medida'])))
            g.add((enode, mex.medidaBLote, Literal(execution['fuente_b']['estrategia']['medida'])))
            for side in ('fuente_a', 'fuente_b'):
                g.add((enode, PROV.wasDerivedFrom, URIRef(base + 'resource/' + execution[side]['recurso_id'])))
            for row in execution['filas']:
                if 'municipio_local' in row:
                    rnode = URIRef(str(enode) + '/municipio/' + str(row['municipio_local']))
                    g.add((rnode, RDF.type, mex.ResultadoCruceLote))
                    g.add((rnode, RDFS.label, Literal('Comparación ' + str(execution['anio']) + ' — código local ' + str(row['municipio_local']), lang='es')))
                    g.add((rnode, mex.codigoLocalLote, Literal(row['municipio_local'])))
                    g.add((rnode, mex.anioLote, Literal(row['anio_registro'])))
                else:
                    row_id = hashlib.sha256(json.dumps([row['programa_clave_local'], row['sede_declarada']], ensure_ascii=False).encode()).hexdigest()
                    rnode = URIRef(str(enode) + '/programa-sede/' + row_id)
                    g.add((rnode, RDF.type, mex.ResultadoEducativoLote))
                    g.add((rnode, RDFS.label, Literal((row['programa_declarado_a'] or row['programa_declarado_b']) + ' — ' + row['sede_declarada'], lang='es')))
                    g.add((rnode, mex.programaLocalLote, Literal(row['programa_clave_local'])))
                    g.add((rnode, mex.sedeDeclaradaLote, Literal(row['sede_declarada'])))
                    g.add((rnode, mex.periodoDeclaradoLote, Literal(row['periodo_declarado'])))
                g.add((enode, mex.resultadoLote, rnode)).add((rnode, mex.ambasLote, Literal(row['presente_en_ambas'])))
                for key, prop in [('valor_a', mex.valorALote), ('valor_b', mex.valorBLote)]:
                    if row[key] is not None:
                        g.add((rnode, prop, Literal(row[key])))
    catalog = report['referencia_municipal']
    if catalog['ok']:
        for row in catalog['municipios']:
            node = URIRef(base + 'municipal-reference/' + row['cvegeo'])
            g.add((node, RDF.type, mex.ReferenciaMunicipalPortal))
            g.add((node, RDFS.label, Literal(row['nombre'], lang='es')))
            g.add((node, mex.cvegeoReferencia, Literal(row['cvegeo'])))
            g.add((node, mex.nombreMunicipioReferencia, Literal(row['nombre'])))
            g.add((node, PROV.wasDerivedFrom, URIRef(catalog['fuente'])))
    return g


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Volver a consultar muestras y agregados')
    parser.add_argument('--retry-errors', action='store_true', help='Reintentar recursos con fallo integral')
    args = parser.parse_args()
    files = {'oportunidades': ROOT / 'data/portal/oportunidades-cruce.json', 'inventario': ROOT / 'data/portal/inventario.json',
             'inspeccion': ROOT / 'data/portal/contenido-inspeccion.json'}
    opportunity, inventory, inspection = [json.loads(files[key].read_text(encoding='utf-8')) for key in files]
    if opportunity['huellas_entrada']['inventario'] != huella(files['inventario']) or opportunity['huellas_entrada']['inspeccion'] != huella(files['inspeccion']):
        raise ValueError('Mapa de oportunidades desactualizado')
    pairs = [p for p in opportunity['pares'] if p['prioridad_revision'] == 'revisar_primero']
    resources = {r['id']: r for r in inventory['recursos']}
    inspections = {r['id']: r for r in inspection['recursos']}
    dataset_ids = {p[key] for p in pairs for key in ('conjunto_a', 'conjunto_b')}
    # Probe one representative resource per dataset; this is diagnostic coverage, not whole-dataset validation.
    selected, fields_for = {}, {}
    for dataset_id in sorted(dataset_ids):
        profile = opportunity['perfiles'][dataset_id]
        choices = [r for r in resources.values() if r['conjunto_id'] == dataset_id and r['clasificacion'] != 'diccionario' and inspections[r['id']]['ok']]
        choices = [r for r in choices if any(c['recurso_id'] == r['id'] and c['familia'] != 'periodo' for c in profile['columnas_clave'])]
        if not choices:
            continue
        resource = max(choices, key=lambda r: (r.get('datastore', {}).get('ok', False), max(re.findall(r'\b(?:19|20)\d{2}\b', r['nombre'] or '') or ['0000']), r['id']))
        cols = [c for c in profile['columnas_clave'] if c['recurso_id'] == resource['id'] and c['familia'] not in {'periodo'}]
        fields = sorted({c['campo'] for c in cols})[:10]
        if fields:
            selected[dataset_id], fields_for[dataset_id] = resource, fields
    samples = {}
    with ThreadPoolExecutor(3) as pool:
        jobs = {pool.submit(muestra, r, fields_for[d], inspections[r['id']], args.refresh): d for d, r in selected.items()}
        for job in as_completed(jobs):
            d = jobs[job]
            samples[d] = job.result()
            print('Muestra', len(samples), '/', len(jobs), samples[d]['conjunto'], 'ok' if samples[d]['ok'] else 'pendiente', flush=True)
    definitions = defaultdict(dict)
    for result in inspection['recursos']:
        r = resources[result['id']]
        if r['clasificacion'] == 'diccionario' and result['ok']:
            for row in result.get('definiciones', []):
                name = valor(row, {'nombre variable', 'nombre de variable', 'variable', 'nombre campo', 'nombre del campo'})
                if name:
                    item = {'descripcion': valor(row, {'descripcion', 'definicion'})}
                    if name in definitions[r['conjunto_id']]:
                        definitions[r['conjunto_id']][name] = {'descripcion': 'AMBIGUA'}
                    else:
                        definitions[r['conjunto_id']][name] = item
    strategies, aggregates = {}, {}
    for r in resources.values():
        strategy = estrategia_registro(r, definitions)
        if strategy and r['conjunto_id'] in dataset_ids:
            strategies[r['id']] = strategy
    # Fetch only resources that can participate in at least one prioritized strategy.
    eligible = set()
    pair_resources = {}
    for pair in pairs:
        aa = [r for r in resources.values() if r['conjunto_id'] == pair['conjunto_a'] and r['id'] in strategies]
        bb = [r for r in resources.values() if r['conjunto_id'] == pair['conjunto_b'] and r['id'] in strategies]
        matches = [(a, b) for a in aa for b in bb if strategies[a['id']]['anio'] == strategies[b['id']]['anio']]
        if matches:
            pair_resources[pair['id']] = matches
            eligible.update(r['id'] for match in matches for r in match)
    with ThreadPoolExecutor(3) as pool:
        jobs = {pool.submit(agregar_validado, resources[id_], strategies[id_], args.refresh, args.retry_errors): id_ for id_ in sorted(eligible)}
        for job in as_completed(jobs):
            id_ = jobs[job]
            aggregates[id_] = job.result()
            print('Agregado', len(aggregates), '/', len(jobs), resources[id_]['nombre'], 'ok' if aggregates[id_]['ok'] else aggregates[id_]['error'], flush=True)
    decisions, education_results = [], {}
    for pair in pairs:
        result = {key: pair[key] for key in ('id', 'titulo_a', 'titulo_b', 'conjunto_a', 'conjunto_b')}
        result.update(decision='requiere_revision', motivos=[], ejecuciones=[], pruebas_recursos=[])
        sa, sb = samples.get(pair['conjunto_a']), samples.get(pair['conjunto_b'])
        result['diagnostico_muestras'] = {'a': sa, 'b': sb}
        result['comparacion_muestras'] = comparar_muestras(pair, opportunity['perfiles'], sa, sb)
        if not sa or not sb or not sa['ok'] or not sb['ok']:
            result['motivos'].append('Muestra no disponible en uno o ambos recursos representativos; ver evidencia de acceso')
        for key in pair['evaluacion_claves']:
            if 'requiere_correspondencia_codigo_nombre' in key['pendientes']:
                result['motivos'].append('Se necesita catálogo de correspondencia código/nombre')
            if 'sentidos_distintos_requieren_pregunta_y_agregacion_explicitas' in key['pendientes']:
                result['motivos'].append('Se comparan poblaciones, ubicaciones o fechas con sentidos distintos')
        if any(f in pair['familias_compartidas'] for f in ('programa_educativo', 'producto_o_especie', 'clasificacion_delito')):
            result['motivos'].append('Homologar catálogo sectorial, medidas y grano antes de agregar')
        for a, b in pair_resources.get(pair['id'], []):
            ar, br = aggregates[a['id']], aggregates[b['id']]
            attempt = {'recurso_a': a['id'], 'recurso_b': b['id'], 'anio': strategies[a['id']]['anio'],
                       'ok_a': ar['ok'], 'ok_b': br['ok'], 'error_a': ar.get('error'), 'error_b': br.get('error')}
            result['pruebas_recursos'].append(attempt)
            if not ar['ok'] or not br['ok']:
                continue
            rows = unir(ar, br)
            execution = {'id': pair['id'] + '--' + a['id'] + '--' + b['id'], 'anio': strategies[a['id']]['anio'],
                         'fuente_a': ar, 'fuente_b': br, 'filas': rows,
                         'alcance': 'Exploratorio por código local de municipio de registro y año; no equivale a homologación oficial ni a cobertura de todos los recursos',
                         'unidades': 'Medidas independientes: conteo de filas publicadas o suma de total de nacimientos; no sumar ni dividir entre indicadores',
                         'limites': ['Sin correspondencia automática hacia CVEGEO', 'No deduplicación de eventos sin identificadores',
                                     'Ausencia de clave permanece null; no implica cero', 'No vincula personas ni cohortes', 'API sin instantánea transaccional']}
            result['ejecuciones'].append(execution)
        # Explicit bounded strategy: independent UES indicators; metadata period, not student/cohort linkage.
        education_counts = {'Titulados', 'Egresados', 'Población - Nuevo ingreso', 'Población - Reingreso'}
        if {pair['titulo_a'], pair['titulo_b']} <= education_counts and len(pair['publicador_comun']) == 1:
            aa = [r for r in resources.values() if r['conjunto_id'] == pair['conjunto_a'] and r['clasificacion'] != 'diccionario']
            bb = [r for r in resources.values() if r['conjunto_id'] == pair['conjunto_b'] and r['clasificacion'] != 'diccionario']
            for a in aa:
                for b in bb:
                    pa = re.findall(r'\b(?:19|20)\d{2}\b', a['nombre'])
                    pb = re.findall(r'\b(?:19|20)\d{2}\b', b['nombre'])
                    if len(pa) != 2 or pa != pb:
                        result['motivos'].append('Periodos declarados diferentes o ambiguos en recursos educativos; no se mezclan')
                        continue
                    ar = lectura_educativa(a, inspections[a['id']], definitions, args.refresh)
                    br = lectura_educativa(b, inspections[b['id']], definitions, args.refresh)
                    education_results[a['id']], education_results[b['id']] = ar, br
                    attempt = {'recurso_a': a['id'], 'recurso_b': b['id'], 'estrategia': 'programa_sede_periodo_declarado',
                               'ok_a': ar['ok'], 'ok_b': br['ok'], 'error_a': ar.get('error'), 'error_b': br.get('error')}
                    result['pruebas_recursos'].append(attempt)
                    if ar['ok'] and br['ok'] and ar['periodo_declarado'] == br['periodo_declarado']:
                        rows = unir_educacion(ar, br)
                        result['ejecuciones'].append({'id': pair['id'] + '--' + a['id'] + '--' + b['id'], 'anio': None,
                            'periodo': ar['periodo_declarado'], 'fuente_a': ar, 'fuente_b': br, 'filas': rows,
                            'alcance': 'Comparación exploratoria de conteos por programa y sede UES; periodo coincidente declarado en metadatos, sin validación externa. No tasa de titulación ni seguimiento de cohortes.',
                            'limites': ['Nombres solo normalizados por espacios y mayúsculas, sin homologación difusa',
                                        'Claves sin correspondencia conservan ausencia', 'Celdas vacías no son cero',
                                        'No unir personas ni inferir cohortes', 'Periodo declarado, no verificado con fechas de registros']})
        if result['ejecuciones']:
            result['decision'] = 'ejecucion_parcial_exploratoria'
            result['motivos'].append('Unión externa con grano único y medidas verificadas; respetar alcance y cobertura temporal declarados en cada ejecución')
        elif result['pruebas_recursos']:
            result['decision'] = 'fallo_validacion_integral'
            result['motivos'].append('Ninguna pareja de recursos de la estrategia superó todas las comprobaciones')
        else:
            result['motivos'].append('Sin estrategia automática de agregación validada para las medidas y el grano de estos recursos')
            if any('catálogo' in reason or 'sentidos distintos' in reason for reason in result['motivos']):
                result['decision'] = 'requiere_transformacion_o_catalogo'
        result['motivos'] = sorted(set(result['motivos']))
        result['pendientes_originales'] = pair['pendientes']
        decisions.append(result)
    report = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'huellas_entrada': {k: huella(p) for k, p in files.items()},
              'alcance': '98 pares prioritarios de la versión del mapa; muestras representativas y estrategias explícitas por recursos. No aprobación global de conjuntos.',
              'referencia_municipal': referencia_municipal(inventory, args.refresh),
              'resumen': {'pares_evaluados': len(decisions), 'decisiones': dict(Counter(p['decision'] for p in decisions)),
                          'muestras_recursos': len(samples), 'muestras_correctas': sum(s['ok'] for s in samples.values()),
                          'recursos_validacion_integral': len(aggregates) + len(education_results),
                          'recursos_integrales_correctos': sum(a['ok'] for a in aggregates.values()) + sum(a['ok'] for a in education_results.values()),
                          'recursos_api_integrales': len(aggregates), 'archivos_educativos_completos': len(education_results),
                          'ejecuciones_por_recursos_anio': sum(len(p['ejecuciones']) for p in decisions),
                          'resumenes': sum(len(e['filas']) for p in decisions for e in p['ejecuciones']),
                          'resumenes_con_valores_en_ambas': sum(row['valor_a'] is not None and row['valor_b'] is not None for p in decisions for e in p['ejecuciones'] for row in e['filas'])},
              'pares': decisions, 'agregados_recursos': list(aggregates.values()) + list(education_results.values())}
    guardar(OUT / 'validacion-lote.json', report)
    base = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']
    rdf_lote(report, base).serialize(OUT / 'lote.ttl', format='turtle', encoding='utf-8')
    lines = ['# Validación por lotes de oportunidades', '', report['alcance'], '', 'Fecha UTC: ' + report['generado_en_utc'], '',
             '| Resultado | Pares |', '| --- | ---: |']
    lines += [f'| {k} | {v} |' for k, v in report['resumen']['decisiones'].items()]
    lines += ['', '## Alcance comprobado', '', json.dumps(report['resumen'], ensure_ascii=False, indent=2), '',
              'Las muestras no demuestran compatibilidad completa. La ejecución parcial solo valida las estrategias y recursos listados; no aprueba todo el par ni sus otros años.', '',
              '## Resultado de cada par', '', '| Conjunto A | Conjunto B | Decisión | Ejecuciones | Motivos |', '| --- | --- | --- | ---: | --- |']
    lines += [f"| {p['titulo_a'].replace('|', '/')} | {p['titulo_b'].replace('|', '/')} | {p['decision']} | {len(p['ejecuciones'])} | {'; '.join(p['motivos'])} |" for p in decisions]
    lines += ['', '## Ejecuciones exploratorias', '', '| A | B | Año | Medida A | Total A | Medida B | Total B | Claves |', '| --- | --- | ---: | --- | ---: | --- | ---: | ---: |']
    lines += [f"| {p['titulo_a']} | {p['titulo_b']} | {e.get('periodo') or e['anio']} | {e['fuente_a']['estrategia']['medida']} | {e['fuente_a']['valor_total']} | {e['fuente_b']['estrategia']['medida']} | {e['fuente_b']['valor_total']} | {len(e['filas'])} |" for p in decisions for e in p['ejecuciones']]
    lines += ['', '## Límites y evidencia', '',
              '- Diagnóstico muestral: hasta 100 filas por API o hasta 30 filas de una hoja; no exhaustivo. Solo se guardan valores de claves/estratos y estadísticas, sin filas personales.',
              '- Estrategia integral disponible: municipio y año de registro del Registro Civil, con definiciones explícitas y publicador común del mapa. Nacimientos suma `total` y verifica hombres + mujeres, unicidad municipio/mes y 12 meses por municipio; no cuenta filas como nacimientos.',
              '- No se mezclan año de defunción con año de registro. Las otras estrategias esperan medidas, grano, catálogos o agregaciones revisadas.',
              '- Estrategia educativa: conteos UES de Titulados/Egresados y Nuevo ingreso/Reingreso, leídos completos y contrastados con diccionarios, por programa/sede y periodo coincidente declarado. No valida externamente el periodo; no produce tasas ni enlaza cohortes. Mantiene diferencias de acentuación como claves sin homologar.',
              '- Referencia municipal extraída de GeoJSON del portal. Su consistencia no prueba equivalencia con códigos locales del Registro Civil u otras fuentes. No se crearon esas equivalencias.',
              '- Ausencia permanece null y el join se hace después de agregar. No hay tasas, causalidad, cohortes ni identificación de personas.',
              '- Evidencia, fallos, URLs, huellas de campos y resultados: `data/portal/lote-cruces/validacion-lote.json`. Cachés fechadas en `muestras/` y `agregados/`. `--refresh` vuelve a consultar; no hay monitor programado.', '']
    (ROOT / 'reports/validacion-lote-cruces.md').write_text('\n'.join(lines), encoding='utf-8')
    exportar_educacion(report)
    print(json.dumps(report['resumen'], ensure_ascii=False, indent=2), flush=True)


def exportar_educacion(report):
    def cell(value):
        return str(value).replace('|', '/').replace('\n', ' ') if value is not None else 'Sin valor publicado'
    lines = ['# Comparaciones educativas del lote', '',
             'Comparaciones exploratorias de indicadores independientes de la Universidad Estatal de Sonora. Las claves usan nombres de programa y sede dentro de esta institución; solo se normalizan espacios y mayúsculas. El periodo procede de los metadatos, sin validación externa. No son tasas ni seguimientos de cohortes.', '',
             'Las celdas vacías y las claves sin correspondencia se conservan como ausencia. Un cero publicado sí aparece como 0. Los totales son sumas de valores conocidos; no rellenan ausencias.', '']
    for pair in report['pares']:
        for execution in pair['ejecuciones']:
            if not execution.get('periodo'):
                continue
            lines += ['## ' + pair['titulo_a'] + ' y ' + pair['titulo_b'], '', 'Periodo declarado: ' + execution['periodo'], '',
                      f"{len(execution['filas'])} claves de programa/sede; {sum(r['valor_a'] is not None and r['valor_b'] is not None for r in execution['filas'])} con valores numéricos en ambas fuentes.", '']
            for label, side in [(pair['titulo_a'], 'fuente_a'), (pair['titulo_b'], 'fuente_b')]:
                source = execution[side]
                lines += [f"- [{label}](https://datos.sonora.gob.mx/dataset/{source['conjunto_id']}/resource/{source['recurso_id']})"]
            lines += ['', '| Programa declarado A | Programa declarado B | Sede declarada | ' + pair['titulo_a'] + ' | ' + pair['titulo_b'] + ' |', '| --- | --- | --- | ---: | ---: |']
            lines += ['| ' + ' | '.join(cell(row[k]) for k in ('programa_declarado_a', 'programa_declarado_b', 'sede_declarada', 'valor_a', 'valor_b')) + ' |' for row in execution['filas']]
            lines += ['']
    (ROOT / 'reports/resultados-lote-educacion.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
