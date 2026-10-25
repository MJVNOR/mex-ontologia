"""Genera una vista documental depurada; no modifica fuentes, semántica ni RDF."""
from collections import Counter
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DELIVERIES = Path('propuestas/depuracion-post-r6')


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8-sig'))


def digest(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def row_fingerprint(row):
    raw = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def reference(path, pointer):
    return {'ruta': str(path).replace('\\', '/'), 'sha256': digest(path), 'json_pointer': pointer}


def source_checks(documents):
    """Coteja las referencias locales que declaran ruta y SHA-256 juntos."""
    checked = {}

    def visit(value):
        if isinstance(value, dict):
            sha = value.get('sha256')
            if sha:
                for key in ('ruta', 'archivo', 'fuente', 'localizador'):
                    path = value.get(key)
                    if isinstance(path, str) and (ROOT / path).is_file():
                        require(digest(path) == sha, f'Huella de fuente no coincide: {path}')
                        checked[path] = sha
                        break
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for document in documents:
        visit(document)
    return checked


def cell(value):
    return str(value).replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')


def main():
    orchestration = read(DELIVERIES / 'orquestacion.json')
    for path, sha in orchestration['base_fuentes'].items():
        require(digest(path) == sha, f'Cambió una fuente histórica o semántica: {path}')

    paths = {
        'encabezados': DELIVERIES / 'encabezados/exclusiones.json',
        'significados': DELIVERIES / 'significados/pendientes.json',
        'catalogos': DELIVERIES / 'catalogos/brechas.json',
    }
    inputs = {key: read(path) for key, path in paths.items()}
    exclusions = inputs['encabezados']['exclusiones']
    meanings = inputs['significados']['significados']
    gaps = inputs['catalogos']['brechas']
    historical_path = Path('reports/pendientes-ronda-5.json')
    historical = read(historical_path)['significados']
    indexed = {r['definicion_iri']: (i, r) for i, r in enumerate(historical)}
    require(len(indexed) == len(historical) == 171, 'Base histórica no tiene 171 IDs únicos')
    meaning_ids = [r['definicion_iri'] for r in meanings]
    excluded_ids = [r['definicion_iri'] for r in exclusions]
    require(len(set(meaning_ids)) == len(meanings) == 169, 'Se requieren 169 significados únicos')
    require(len(set(excluded_ids)) == len(exclusions) == 2, 'Se requieren dos exclusiones únicas')
    require(not set(meaning_ids) & set(excluded_ids), 'Significados y exclusiones se solapan')
    require(set(meaning_ids) | set(excluded_ids) == set(indexed), 'La partición no conserva los 171 registros')
    require({r['definicion_iri'] for r in inputs['significados']['lista_ids_2_excluidos']} == set(excluded_ids), 'Agentes discrepan en las dos exclusiones')

    audit_path = Path('propuestas/pendientes-muse-r6/auditoria-documental/entrega-final.json')
    audit = read(audit_path)
    audit_index = {}
    for i, decision in enumerate(audit['dictamenes']):
        if decision.get('tipo') == 'decision' and decision.get('id') in indexed:
            require(decision['id'] not in audit_index, f'Dictamen R6 duplicado: {decision["id"]}')
            audit_index[decision['id']] = i
    require(set(audit_index) == set(indexed), 'Falta dictamen R6 para parte de los 171 registros')

    dictionaries = {}
    verified_rows = []
    for record in meanings + exclusions:
        iri = record['definicion_iri']
        original_index, original = indexed[iri]
        require(record['variable'] == original['variable'], f'Nombre alterado: {iri}')
        require(record['descripcion_original'] == original['descripcion'], f'Descripción alterada: {iri}')
        require(record['huella_fila_diccionario'] == original['huella_fila_diccionario'], f'Huella declarada alterada: {iri}')
        dictionary = original['diccionario']
        path = Path('data/portal/inspecciones') / f'{dictionary}.json'
        if dictionary not in dictionaries:
            dictionaries[dictionary] = read(path)
        logical_row = int(iri.split('%2F')[-1])
        raw_row = dictionaries[dictionary]['definiciones'][logical_row - 1]
        require(row_fingerprint(raw_row) == original['huella_fila_diccionario'], f'Fila original no coincide: {iri}')
        result = dict(record)
        result['trazabilidad_verificada'] = {
            'lista_historica': reference(historical_path, f'/significados/{original_index}'),
            'diccionario': reference(path, f'/definiciones/{logical_row - 1}'),
            'fila_logica_1_based': logical_row,
            'dictamen_r6': reference(audit_path, f'/dictamenes/{audit_index[iri]}'),
            'nota': 'El índice del JSON pointer empieza en cero; la fila lógica empieza en uno.',
        }
        verified_rows.append(result)
    meaning_rows, excluded_rows = verified_rows[:len(meanings)], verified_rows[len(meanings):]

    required_ids = {f'V{i:02}' for i in range(1, 17)} | {'des_mpo_res'}
    require(len(gaps) == 17 and {r['id'] for r in gaps} == required_ids, 'Matriz de catálogos no conserva V01–V16 + des_mpo_res')
    for gap in gaps:
        require(gap.get('documento_requerido_exacto') and gap.get('criterio_aceptacion') and gap.get('campos_minimos'), f'Falta documento o criterio: {gap["id"]}')
    reference_gap = next(r for r in gaps if r['id'] == 'des_mpo_res')
    require(reference_gap['tipo'] == 'anomalia_referencia_heredada', 'des_mpo_res no es un catálogo acreditado')
    reference_gap = dict(reference_gap)
    reference_gap['definiciones_corruptas_relacionadas'] = excluded_ids
    reference_gap['nota_conteo'] = 'Este caso remite a las mismas dos exclusiones; no agrega significados ni acredita otro catálogo.'
    gaps = [reference_gap if r['id'] == 'des_mpo_res' else r for r in gaps]

    by_group = Counter(r['grupo_fuente'] for r in meanings)
    by_dataset = Counter(r['conjunto_titulo'] for r in meanings)
    declared = {r['grupo_fuente']: r['n'] for r in inputs['significados']['tabla_resumen_por_fuente']}
    require(dict(by_group) == declared and sum(by_group.values()) == 169, 'Los grupos no suman los mismos 169 IDs')
    checked_sources = source_checks(inputs.values())
    coverage = read('data/semantica/cobertura.json')
    variable_states = Counter(r['estado'] for r in coverage['variables'])
    mapping_states = Counter(r['estado'] for r in coverage['correspondencias'])
    semantics = read('ontologia/semantica.json')
    require(variable_states['respaldada_por_definicion'] == 1392, 'Cambió el total de significados respaldados')
    require(len(semantics['conceptos']) == 1075, 'Cambió el total de conceptos')
    require(mapping_states['documental_revisada'] == 4475 and mapping_states['candidata_por_nombre'] == 20, 'Cambió el estado de correspondencias R6')
    require(sum(mapping_states.values()) == 4495, 'Aparecieron correspondencias en otro estado')

    now = datetime.now(timezone.utc)
    report = {
        'generado_en_utc': now.isoformat(),
        'fecha_local_hermosillo': now.astimezone(timezone(timedelta(hours=-7))).date().isoformat(),
        'alcance': 'Vista de trabajo documental derivada de R6; conserva fuentes y denominadores históricos.',
        'resumen': {'registros_historicos': 171, 'significados_pendientes_reales': 169, 'encabezados_corruptos_excluidos_de_la_vista': 2, 'vigencias_catalogos': 16, 'anomalias_referencia_heredada': 1},
        'conteos_semanticos_preservados': {'significados_respaldados': 1392, 'conceptos': 1075, 'correspondencias_revisadas': 4475, 'candidatas': 20, 'ambiguas': 0},
        'por_grupo': dict(sorted(by_group.items())),
        'por_conjunto': dict(sorted(by_dataset.items())),
        'significados': meaning_rows,
        'encabezados_excluidos': excluded_rows,
        'brechas_catalogos': gaps,
        'nota_des_mpo_res': reference_gap['nota_conteo'],
        'fuentes_historicas_preservadas': orchestration['base_fuentes'],
        'entregas': {key: reference(path, '') for key, path in paths.items()},
        'fuentes_cotejadas': checked_sources,
        'validacion': {'particion_171_igual_169_mas_2': True, 'ids_duplicados': 0, 'huellas_de_filas_cotejadas': len(verified_rows), 'diccionarios_cotejados': len(dictionaries), 'fuentes_locales_con_sha_cotejado': len(checked_sources), 'contactos_externos': 0, 'grafo_modificado': False},
        'criterios': ['No se borran las dos filas del inventario original ni se cuentan como significados resueltos.', 'La vista de 169 pendientes no cambia el denominador histórico de cobertura.', 'Los documentos requeridos y sus campos son condiciones de aceptación futuras, no definiciones o vigencias acreditadas.', 'Las búsquedas negativas se limitan al inventario y evidencia revisados.', 'Examinar evidencia primaria preservada sigue siendo válido; una norma nacional sin vínculo local no basta por sí sola.'],
    }
    lines = [
        '# Pendientes documentales depurados tras R6', '',
        '**171 registros históricos = 169 significados pendientes reales + 2 encabezados corruptos.**', '',
        'Se excluyen los encabezados de la vista accionable y se conservan sus celdas, identificadores y procedencia. No se cuentan como significados resueltos ni se cambian los denominadores históricos.', '',
        'El estado semántico conserva 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y 0 ambiguas.', '',
        '## Significados pendientes por fuente', '', '| Grupo | Pendientes |', '| --- | ---: |',
    ]
    lines += [f'| {cell(group)} | {count} |' for group, count in sorted(by_group.items())]
    lines += ['', 'Los 169 registros están enumerados en [el detalle por fuente](../propuestas/depuracion-post-r6/significados/pendientes.md) y en [el JSON consolidado](pendientes-depurados.json). Cada registro conserva el texto original, la evidencia faltante y el criterio de aceptación; sus localizadores cotejados distinguen índice JSON desde cero de fila lógica desde uno.', '', '## Encabezados excluidos de la vista', '', '| Registro | Diccionario / fila lógica | Texto original |', '| --- | --- | --- |']
    lines += [f'| {cell(r["id_estable"])} | {cell(r["diccionario"])} / {r["trazabilidad_verificada"]["fila_logica_1_based"]} | {cell(r["variable"])} / {cell(r["descripcion_original"])} |' for r in excluded_rows]
    lines += ['', '[Celdas originales, motivos y huellas de las exclusiones](../propuestas/depuracion-post-r6/encabezados/exclusiones.md). Se requiere aclaración o fe de erratas para corregir el diccionario original.', '', '## Documentos faltantes de catálogos y referencia heredada', '', 'Se mantienen 16 brechas de vigencia (V01–V16) y un caso de anomalía de referencia (`des_mpo_res`). Este último remite a las mismas dos filas corruptas: no acredita la existencia de un catálogo ni agrega dos significados pendientes nuevos.', '', '| ID | Conjunto | Documento requerido |', '| --- | --- | --- |']
    lines += [f'| {cell(r["id"])} | {cell(r["conjunto"]["titulo"])} | {cell(r["documento_requerido_exacto"])} |' for r in gaps]
    lines += ['', '[Matriz completa con evidencia, campos mínimos y criterios de aceptación](../propuestas/depuracion-post-r6/catalogos/brechas.md). Los periodos citados delimitan lo que debe acreditarse; no son vigencias demostradas. La resolución de Presas en R6 acredita el vínculo de columna con la definición /4 y mantiene abierta su vigencia V05.', '', '## Validación y regeneración', '', f'- 171 identificadores únicos particionados sin pérdidas ni solapamiento; {len(verified_rows)} huellas de filas cotejadas en {len(dictionaries)} diccionarios.', f'- {len(checked_sources)} fuentes locales cotejadas por SHA-256 y fuentes históricas de [la orquestación](../propuestas/depuracion-post-r6/orquestacion.json) conservadas.', '- Cero definiciones o vigencias nuevas; cero contactos externos; sin cambios de grafo ni del chat.', '- La revisión por ID del manual SEED 2022 ya preservado puede continuar como investigación documental; no promueve automáticamente significados.', '', 'Regenerar únicamente esta vista:', '', '```powershell', 'uv run python scripts/depurar_pendientes.py', '```', '']
    out = ROOT / 'reports'
    (out / 'pendientes-depurados.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'pendientes-depurados.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'resumen': report['resumen'], 'validacion': report['validacion']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
