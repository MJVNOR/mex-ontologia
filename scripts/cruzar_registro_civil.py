"""Cruce agregado reproducible de matrimonios y divorcios registrados en 2022."""
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from inventariar_portal import ROOT, api, normalizar
from rdflib import Graph, URIRef, DCTERMS
import tomllib


def entero(value):
    if value is None or isinstance(value, bool):
        raise ValueError('Clave vacía o booleana')
    try:
        number = Decimal(str(value).strip())
        if not number.is_finite() or number != number.to_integral_value():
            raise ValueError('Clave no entera')
        return int(number)
    except InvalidOperation as error:
        raise ValueError('Clave no numérica') from error


def agregar(resource, year_field):
    counts, years, seen = Counter(), Counter(), set()
    offset, expected, urls = 0, None, []
    while True:
        response = api('datastore_search', resource_id=resource['id'], fields='_id,municipio,' + year_field,
                       sort='_id asc', limit=5000, offset=offset)
        if not response['ok']:
            raise RuntimeError(str(response))
        body = response['result']
        if expected is None:
            expected = body['total']
        if body['total'] != expected or body.get('total_was_estimated'):
            raise RuntimeError('Total inestable o estimado')
        rows = body['records']
        if not rows and offset < expected:
            raise RuntimeError('Paginación incompleta')
        urls.append(response['url'])
        for row in rows:
            if row['_id'] in seen:
                raise RuntimeError('Identificador duplicado entre páginas')
            seen.add(row['_id'])
            municipio, year = entero(row['municipio']), entero(row[year_field])
            # No convertir a INEGI ni asignar nombres: el diccionario no publica ese catálogo.
            if not 1 <= municipio <= 72:
                raise RuntimeError('Código municipal fuera del dominio esperado; revisar antes de cruzar')
            counts[(municipio, year)] += 1
            years[year] += 1
        offset += len(rows)
        if offset >= expected:
            break
    final = api('datastore_search', resource_id=resource['id'], limit=0)
    if not final['ok'] or final['result']['total'] != expected:
        raise RuntimeError('Fuente cambió al terminar')
    if set(years) != {2022} or len(seen) != expected or sum(counts.values()) != expected:
        raise RuntimeError('Cobertura temporal o conteo inconsistentes')
    return counts, {'recurso_id': resource['id'], 'conjunto_id': resource['conjunto_id'], 'nombre': resource['nombre'],
                    'campo_anio': year_field, 'total_registros': expected, 'municipios_observados': len(counts),
                    'consultas': urls, 'validacion_total_y_ids': True}


def main():
    inv = json.loads((ROOT / 'data/portal/inventario.json').read_text(encoding='utf-8'))
    sources, counts = [], []
    base = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']
    graph = Graph().parse(ROOT / 'data/catalogo/catalogo.ttl', format='turtle')
    publishers = []
    for title, year_field in [('Matrimonios', 'año_matrimonio'), ('Divorcios', 'año_registro')]:
        resource = next(r for r in inv['recursos'] if r['conjunto'] == title and r['nombre'] == title + ' 2022')
        publisher = set(graph.objects(URIRef(base + 'dataset/' + resource['conjunto_id']), DCTERMS.publisher))
        if len(publisher) != 1 or (publishers and publisher != publishers[0]):
            raise RuntimeError('Las fuentes no tienen una dependencia publicadora común verificada')
        publishers.append(publisher)
        dictionary = next(r for r in inv['recursos'] if r['conjunto_id'] == resource['conjunto_id'] and r['clasificacion'] == 'diccionario')
        evidence = json.loads((ROOT / 'data/portal/inspecciones' / (dictionary['id'] + '.json')).read_text(encoding='utf-8'))
        definitions = {row.get('Nombre variable'): row for row in evidence['definiciones']}
        if normalizar(definitions['municipio']['Descripción']).strip() != 'municipio de registro':
            raise RuntimeError('Definición municipal incompatible')
        if 'registro' not in normalizar(definitions[year_field]['Descripción']):
            raise RuntimeError('Año no definido como año de registro')
        counter, source = agregar(resource, year_field)
        source.update(diccionario_id=dictionary['id'], evidencia_clave=definitions['municipio'], evidencia_anio=definitions[year_field])
        source['publicador_iri'] = str(next(iter(publisher)))
        counts.append(counter)
        sources.append(source)
        print(title, source['total_registros'], 'registros; solo se conservan agregados', flush=True)
    keys = sorted(set(counts[0]) | set(counts[1]))
    rows = [{'codigo_municipio_fuente': key[0], 'anio_registro': key[1],
             'registros_matrimonios': counts[0].get(key), 'registros_divorcios': counts[1].get(key),
             'presente_en_ambas': key in counts[0] and key in counts[1]} for key in keys]
    report = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'fuentes': sources,
              'metodo': 'Conteos independientes por código municipal local y año de registro; unión externa de agregados',
              'alcance': 'Cruce exploratorio dentro del Registro Civil de Sonora. Coincidencia de códigos locales y definiciones; catálogo oficial de correspondencia no publicado en estos diccionarios.',
              'limites': ['No vincula personas ni matrimonios con sus divorcios.',
                          'No mide probabilidad de divorcio ni relación causal.',
                          'Código sin filas en una fuente se conserva como null; no se infiere cero.',
                          'Conteo de filas publicadas, sin deduplicación de eventos no identificables.',
                          'No se asignan nombres ni códigos INEGI sin catálogo de correspondencia.',
                          'Consultas paginadas y comprobación de totales; API no ofrece instantánea transaccional.'],
              'filas': rows}
    report['sha256_agregados'] = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    (ROOT / 'data/portal/cruce-registro-civil.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Primer cruce: Registro Civil, 2022', '', report['metodo'], '', report['alcance'], '',
             'Se consultaron exclusivamente `_id`, `municipio` y el año. Se descartaron las filas tras contarlas.', '',
             '| Fuente | Filas | Municipios observados |', '| --- | ---: | ---: |']
    lines += [f"| {s['nombre']} | {s['total_registros']} | {s['municipios_observados']} |" for s in sources]
    lines += ['', '| Código local | Año | Matrimonios | Divorcios |', '| --- | ---: | ---: | ---: |']
    lines += [f"| {r['codigo_municipio_fuente']:02} | 2022 | {r['registros_matrimonios'] if r['registros_matrimonios'] is not None else 'Sin filas observadas'} | {r['registros_divorcios'] if r['registros_divorcios'] is not None else 'Sin filas observadas'} |" for r in rows]
    lines += ['', '## Interpretación y límites', ''] + ['- ' + text for text in report['limites']]
    lines += ['', '## Fuentes consultadas', '']
    for source in sources:
        lines += [f"- [{source['nombre']}](https://datos.sonora.gob.mx/dataset/{source['conjunto_id']}/resource/{source['recurso_id']})", f"- [Diccionario](https://datos.sonora.gob.mx/dataset/{source['conjunto_id']}/resource/{source['diccionario_id']})"]
    (ROOT / 'reports/primer-cruce.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
