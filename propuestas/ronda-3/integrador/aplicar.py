"""Aplica el paquete propio SOLO tras el relevo explícito del integrador semántico.

No regenera ni carga el motor. La validación y sincronización son pasos posteriores.
"""
import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = HERE / 'paquete'
MANIFEST_SHA = 'c926c28467a499ff72ed626da8014cc6c642c31f7760ca25cffa4ad1d6782dff'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replace_once(path, old, new):
    text = path.read_text(encoding='utf-8')
    if text.count(old) != 1:
        raise ValueError('Punto de integración cambió: ' + str(path))
    return text.replace(old, new, 1)


def main():
    release_path = ROOT / 'propuestas/cobertura-muse-20261023/integrador/coordinacion.json'
    release = read(release_path)
    if release.get('semantica_lista') is not True:
        raise ValueError('El integrador semántico no ha liberado el núcleo')
    if (ROOT / 'ontologia/revision-ronda-3.json').exists():
        raise ValueError('Ronda 3 ya instalada: no repetir aplicación')
    if sha(PACKAGE / 'manifiesto.json') != MANIFEST_SHA:
        raise ValueError('Manifiesto de staging modificado')
    manifest = read(PACKAGE / 'manifiesto.json')
    for relative, expected in manifest['archivos'].items():
        path = (PACKAGE / relative).resolve()
        if not path.is_relative_to(PACKAGE.resolve()) or sha(path) != expected:
            raise ValueError('Paquete alterado: ' + relative)
    for relative, expected in manifest['insumos'].items():
        if sha(ROOT / relative) != expected:
            raise ValueError('Insumo alterado: ' + relative)
    sem_path = ROOT / 'ontologia/semantica.json'
    if sha(sem_path) != release['semantica_sha256']:
        raise ValueError('El núcleo cambió después del relevo semántico')
    rules = read(sem_path)
    previous = read(PACKAGE / 'vinculos-anteriores.json')
    additions = read(PACKAGE / 'correspondencias-29.json')['entradas']
    if rules['vinculos_documentales_revisados'] != previous or len(previous) != 836:
        raise ValueError('Las 836 correspondencias anteriores cambiaron')
    before = copy.deepcopy(rules)
    rules['vinculos_documentales_revisados'] += additions
    current = read(ROOT / 'data/semantica/cobertura.json')
    states = current['resumen']['estados_correspondencias']
    if states['documental_revisada'] != 836:
        raise ValueError('Cobertura central no está en el relevo esperado')
    by_column = {m['columna']: m for m in current['correspondencias']}
    for addition in additions:
        row = by_column[addition['columna']]
        if row['estado'] != 'candidata_por_nombre' or row['concepto'] != addition['concepto']:
            raise ValueError('Correspondencia no elegible después de cobertura: ' + addition['columna'])
    changes = {}
    coverage_path = ROOT / 'scripts/integrar_cobertura.py'
    changes[coverage_path] = replace_once(coverage_path,
        "    for key in ('vinculos_documentales_revisados', 'observaciones_revision', 'condiciones'):\n        if rules[key] != previous[key]:\n            raise ValueError('La ampliación de cobertura alteró ' + key)\n",
        "    for key in ('observaciones_revision', 'condiciones'):\n        if rules[key] != previous[key]:\n            raise ValueError('La ampliación de cobertura alteró ' + key)\n"
        "    if (root / 'ontologia/revision-ronda-3.json').exists():\n        from integrar_ronda_3 import validar_extension_vinculos\n        validar_extension_vinculos(rules, previous['vinculos_documentales_revisados'], root)\n"
        "    elif rules['vinculos_documentales_revisados'] != previous['vinculos_documentales_revisados']:\n        raise ValueError('La ampliación de cobertura alteró vinculos_documentales_revisados')\n")
    generator = ROOT / 'scripts/consolidar_semantica.py'
    hook = "    report['huellas_entrada'] = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}"
    changes[generator] = replace_once(generator, hook,
        "    if (ROOT / 'ontologia/revision-ronda-3.json').exists():\n        from integrar_ronda_3 import construir as integrar_ronda_3\n"
        "        r3_data, r3_report, r3_sources = integrar_ronda_3(report, rules, base)\n        data += r3_data\n"
        "        report['integracion_ronda_3'] = r3_report\n        sources.update(r3_sources)\n" + hook)
    old_save = "    data.serialize(OUT / 'interpretaciones.ttl', format='turtle', encoding='utf-8')\n    model.serialize(OUT / 'nucleo.ttl', format='turtle', encoding='utf-8')"
    if changes[generator].count(old_save) != 1:
        raise ValueError('El guardado semántico cambió antes de integrar')
    changes[generator] = changes[generator].replace(old_save,
        "    from guardar_rdf import serializar_atomico\n    serializar_atomico(data, OUT / 'interpretaciones.ttl')\n    serializar_atomico(model, OUT / 'nucleo.ttl')", 1)
    expand = ROOT / 'scripts/ampliar_portal.py'
    hook = '    shapes.serialize(output / "shapes.ttl", format="turtle", encoding="utf-8")'
    changes[expand] = replace_once(expand, hook,
        "    if (ROOT / 'ontologia/revision-ronda-3.json').exists():\n"
        "        shapes.parse(data=(ROOT / 'shapes/ronda-3.ttl').read_text(encoding='utf-8').replace('{{BASE_IRI}}', config['base_iri']), format='turtle')\n" + hook)
    replacements = {
        'from construir_catalogo import ROOT, PROV, motor, url_http': 'from construir_catalogo import ROOT, PROV, motor, url_http\nfrom guardar_rdf import serializar_atomico',
        "        content.serialize(ROOT / 'data/portal/contenido.ttl', format='turtle', encoding='utf-8')": "        serializar_atomico(content, ROOT / 'data/portal/contenido.ttl')",
        '        graph.serialize(output / name, format="turtle", encoding="utf-8")': '        serializar_atomico(graph, output / name)',
        '    shapes.serialize(output / "shapes.ttl", format="turtle", encoding="utf-8")': '    serializar_atomico(shapes, output / "shapes.ttl")',
    }
    for old, new in replacements.items():
        if changes[expand].count(old) != 1:
            raise ValueError('El guardado del portal cambió antes de integrar')
        changes[expand] = changes[expand].replace(old, new, 1)
    agents_path = ROOT / 'ontologia/revision-agentes.json'
    agents = read(agents_path)
    agents['esperado_actual']['correspondencias_revisadas'] = 865
    r2_path = ROOT / 'ontologia/revision-ronda-2.json'
    r2 = read(r2_path)
    r2['esperado_actual']['revisadas'] = 865
    r2['esperado_actual']['candidatas'] = states['candidata_por_nombre'] - 29
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup = ROOT / 'data/backups' / ('antes-ronda-3-' + stamp + '.zip')
    backup.parent.mkdir(parents=True, exist_ok=True)
    targets = [sem_path, agents_path, r2_path, *changes,
               ROOT / 'ontologia/revision-cobertura.json', ROOT / 'data/semantica/cobertura.json', release_path]
    with zipfile.ZipFile(backup, 'x', zipfile.ZIP_DEFLATED) as archive:
        for path in targets:
            archive.write(path, path.relative_to(ROOT).as_posix())
    destination = ROOT / 'data/integracion-ronda-3'
    if destination.exists():
        raise ValueError('La carpeta de evidencia ya existe: no sobrescribir')
    shutil.copytree(PACKAGE, destination)
    for name in ('integrar_ronda_3.py', 'integrar_cruces_r3.py'):
        target = ROOT / 'scripts' / name
        if target.exists():
            raise ValueError('Módulo central ya existe: ' + name)
        shutil.copy2(destination / 'codigo' / name, target)
        if name == 'integrar_ronda_3.py':
            text = target.read_text(encoding='utf-8')
            old = "variables = {v['iri']: v for v in report['variables']}"
            if text.count(old) != 1:
                raise ValueError('Cambió el módulo de correspondencias fijado')
            target.write_text(text.replace(old, "variables = {v['iri']: v for v in report['variables'] if v.get('iri')}", 1), encoding='utf-8')
    shutil.copy2(HERE / 'guardar_rdf.py', ROOT / 'scripts/guardar_rdf.py')
    shutil.copy2(destination / 'codigo/ronda-3.ttl', ROOT / 'shapes/ronda-3.ttl')
    shutil.copy2(destination / 'codigo/cruces_r3.rq', ROOT / 'queries/portal/cruces_ronda_3.rq')
    write(ROOT / 'ontologia/revision-ronda-3.json', {
        'version': 1, 'evidencia': 'data/integracion-ronda-3', 'manifiesto_sha256': MANIFEST_SHA,
        'respaldo': backup.relative_to(ROOT).as_posix(), 'respaldo_sha256': sha(backup),
        'relevo': release_path.relative_to(ROOT).as_posix(), 'relevo_sha256': sha(release_path),
        'esperado': {'revisadas': 865, 'adiciones': 29, 'fichas': 3, 'comparaciones_2020': 72, 'evidencias_fuente': 144}})
    for path, text in changes.items():
        path.write_text(text, encoding='utf-8')
    write(sem_path, rules)
    write(agents_path, agents)
    write(r2_path, r2)
    before.pop('vinculos_documentales_revisados')
    after = copy.deepcopy(read(sem_path))
    after.pop('vinculos_documentales_revisados')
    if before != after:
        raise ValueError('Se modificó el núcleo semántico fuera de correspondencias')
    report = {'aplicada_en_utc': datetime.now(timezone.utc).isoformat(),
              'respaldo': backup.relative_to(ROOT).as_posix(), 'manifiesto_sha256': MANIFEST_SHA,
              'reglas_conceptos_preservados': True, 'vinculos_previos_preservados': 836,
              'vinculos_totales': 865, 'studio_modificado': False, 'pendiente': 'regenerar_validar_sincronizar'}
    report['ajustes_integracion'] = ['Omitir las siete filas sin nombre al indexar variables por IRI; no son destinos de correspondencias.',
                                    'Publicar Turtle por reemplazo de un temporal completo; evita truncar destinos con error de acceso y conserva el previo ante fallo.']
    write(HERE / 'aplicacion.json', report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
