"""Expone cobertura y pendientes sin promover coincidencias a hechos semánticos."""
from collections import Counter, defaultdict
import json
from pathlib import Path

from construir_catalogo import ROOT
from integrar_contenido import clave


def auditar(report, inventory, cols):
    resources = {r['id']: r for r in inventory['recursos']}
    variables = defaultdict(list)
    dictionaries = defaultdict(set)
    mappings = defaultdict(list)
    for v in report['variables']:
        variables[(v['conjunto'], clave(v['variable']))].append(v)
        dictionaries[v['conjunto']].add(v['diccionario'])
    for m in report['correspondencias']:
        mappings[m['columna']].append(m)
    coverage = []
    for col in cols:
        links = mappings[col['iri']]
        definitions = variables[(col['conjunto'], clave(col['campo']))]
        states = {m['estado'] for m in links}
        if 'documental_revisada' in states:
            status = 'documental_revisada'
        elif 'ambigua_por_nombre' in states:
            status = 'ambigua_por_nombre'
        elif links:
            status = 'candidata_por_nombre'
        elif definitions:
            status = 'definicion_sin_interpretacion_compartida'
        elif dictionaries[col['conjunto']]:
            status = 'sin_definicion_coincidente'
        else:
            status = 'sin_diccionario_en_conjunto'
        coverage.append({'columna': col['iri'], 'recurso': col['recurso'], 'titulo_recurso': resources[col['recurso']]['nombre'],
                         'conjunto': col['conjunto'], 'campo': col['campo'], 'estado': status, 'fuente_esquema': col['fuente'],
                         'correspondencias': [m['iri'] for m in links],
                         'definiciones_por_nombre': [v['definicion_iri'] for v in definitions]})
    pending = []
    for v in report['variables']:
        if v['estado'] == 'respaldada_por_definicion':
            continue
        description = clave(v['descripcion'])
        reason = ('descripcion_vacia_o_pendiente' if not description or description == 'pendiente de especificar'
                  else 'pista_sin_interpretacion_revisada' if v['estado'] == 'candidata_sin_definicion_suficiente'
                  else 'dominio_o_medida_sin_regla_revisada')
        pending.append({k: v[k] for k in ['conjunto', 'titulo_conjunto', 'diccionario', 'variable', 'descripcion', 'estado', 'definicion_iri']} | {'motivo': reason})
    summary = {'columnas_examinadas': len(coverage), 'estados_columnas': dict(Counter(c['estado'] for c in coverage)),
               'variables_pendientes': len(pending), 'motivos_variables_pendientes': dict(Counter(v['motivo'] for v in pending)),
               'recursos_con_revision_explicita': len({c['recurso'] for c in coverage if c['estado'] == 'documental_revisada'}),
               'observaciones_documentales': len(report['observaciones_revision'])}
    result = {'generado_en_utc': report['generado_en_utc'], 'resumen': summary, 'columnas': coverage,
              'variables_pendientes': pending, 'observaciones_revision': report['observaciones_revision'],
              'huellas_entrada': report.get('huellas_entrada', {})}
    (ROOT / 'reports/pendientes-semanticos.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Cobertura y pendientes semánticos', '',
             'La unidad de cobertura es una columna física de recurso/hoja/API; no una fila de datos. Una interpretación documental no valida valores ni habilita un cruce por sí sola.', '',
             '| Estado de columna | Cantidad |', '| --- | ---: |']
    lines += [f'| {s} | {n} |' for s, n in summary['estados_columnas'].items()]
    lines += ['', 'Los estados son excluyentes por columna. Las correspondencias pueden sumar más porque una columna ambigua puede apuntar a más de una definición.', '',
              '## Revisiones explícitas por recurso', '', '| Recurso | Columnas revisadas |', '| --- | ---: |']
    reviewed = Counter(c['recurso'] for c in coverage if c['estado'] == 'documental_revisada')
    lines += [f"| {resources[rid]['nombre']} ({rid}) | {count} |" for rid, count in reviewed.items()]
    lines += ['', '## Observaciones que requieren revisión', '']
    lines += [f"- **{n['id']}**: {n['observacion']} Recurso: `{n['recurso']}`; campo: `{n['campo']}`." for n in report['observaciones_revision']]
    lines += ['', '## Definiciones aún sin interpretación compartida', '', '| Motivo | Cantidad |', '| --- | ---: |']
    lines += [f'| {s} | {n} |' for s, n in summary['motivos_variables_pendientes'].items()]
    lines += ['', 'El archivo JSON contiene todas las columnas y definiciones pendientes con sus identificadores de evidencia. No se completan textos vacíos, no se resuelven catálogos por parecido ni se propagan revisiones entre años.', '']
    (ROOT / 'reports/pendientes-semanticos.md').write_text('\n'.join(lines), encoding='utf-8')
    return summary


if __name__ == '__main__':
    import tomllib
    from consolidar_semantica import columnas
    report = json.loads((ROOT / 'data/semantica/cobertura.json').read_text(encoding='utf-8'))
    inventory = json.loads((ROOT / 'data/portal/inventario.json').read_text(encoding='utf-8'))
    inspection = json.loads((ROOT / 'data/portal/contenido-inspeccion.json').read_text(encoding='utf-8'))
    base = tomllib.loads((ROOT / 'config.toml').read_text(encoding='utf-8'))['catalogo']['base_iri']
    print(json.dumps(auditar(report, inventory, columnas(inventory, inspection, base)), ensure_ascii=False, indent=2))
