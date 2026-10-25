"""Registra el cierre comprobado del ámbito chat, correspondencias y cruces."""
import copy
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    config = read(ROOT / 'ontologia/revision-ronda-3.json')
    semantic = read(ROOT / 'data/semantica/cobertura.json')
    sync = read(ROOT / 'reports/studio-portal-sync.json')
    native = read(HERE / 'control-studio-final.json')
    chat = read(HERE / 'instalacion-chat.json')
    rules = read(ROOT / 'ontologia/semantica.json')
    with zipfile.ZipFile(ROOT / config['respaldo']) as archive:
        previous = json.loads(archive.read('ontologia/semantica.json'))
    after = copy.deepcopy(rules)
    previous.pop('vinculos_documentales_revisados')
    after.pop('vinculos_documentales_revisados')
    if previous != after:
        raise ValueError('El núcleo semántico cambió fuera de los vínculos aprobados')
    if sync['verificado'] is not True or sync['shacl']['conforms'] is not True or sync['shacl'].get('skipped_constraints'):
        raise ValueError('Falta verificación completa de sincronización')
    if [native[k] for k in ('revisadas', 'fichas', 'comparaciones', 'evidencias')] != [865, 3, 72, 144]:
        raise ValueError('Los conteos vivos no coinciden')
    if sha(Path(chat['bundle_instalado'])) != chat['sha256_bundle_despues']:
        raise ValueError('El bundle instalado de chat cambió')
    paths = ['scripts/integrar_ronda_3.py', 'scripts/integrar_cruces_r3.py', 'scripts/guardar_rdf.py',
             'scripts/consolidar_semantica.py', 'scripts/integrar_cobertura.py', 'scripts/ampliar_portal.py',
             'scripts/sincronizar_studio_portal.py', 'tests/test_ronda_3_integrada.py',
             'tests/test_guardar_rdf.py', 'tests/test_ronda_2.py']
    hashes = {}
    for relative in paths:
        source = ROOT / relative
        target = HERE / 'codigo-instalado' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        hashes[relative] = sha(source)
    write(HERE / 'codigo-instalado/manifiesto.json', hashes)
    agent_dir = ROOT.parent / 'open-ontologies/studio/src-tauri/sidecars/agent'
    e2e = agent_dir.parent / 'evidencia/e2e_recuperacion.json'
    cases = read(e2e)['casos']
    if len(cases) != 6 or '"documental_revisada":865' not in cases[0]['resumen']:
        raise ValueError('Falta la prueba de recuperación contra el grafo final')
    report = {
        'estado': 'completada', 'fecha_utc': datetime.now(timezone.utc).isoformat(),
        'alcance': 'Chat, 29 correspondencias y evidencia de cruces; integración semántica del otro chat preservada.',
        'semantica': semantic['resumen'], 'correspondencias_nuevas': 29,
        'vinculos_previos_preservados': 836, 'resto_nucleo_semantico_intacto': True,
        'cruces': semantic['integracion_ronda_3']['cruces'],
        'studio': {'triples': sync['triples_totales_studio'], 'sincronizacion_verificada': True,
                   'shacl_conforme': True, 'infracciones': sync['shacl']['violation_count'],
                   'respaldo': sync['respaldo'], 'ediciones_ajenas_conservadas': True},
        'pruebas': {'centrales': 108, 'sidecar': 45, 'casos_recuperacion_http': 6,
                    'llamadas_modelo': 0, 'respuesta_modelo_desde_ui': 'no_evaluada'},
        'chat': {'bundle_sha256': chat['sha256_bundle_despues'], 'e2e_sha256': sha(e2e),
                 'resumenes_recuperacion': [c['resumen'] for c in cases]},
        'manifiesto_evidencia': config['manifiesto_sha256'], 'respaldo_central': config['respaldo'],
        'codigo_instalado_sha256': hashes,
        'ajustes_integracion': ['Indexar solo variables con IRI, conservando las siete filas sin nombre en el informe.',
                               'Guardar Turtle mediante temporal completo y reemplazo, tras errores OSError22 al truncar destinos existentes.',
                               'Conservar el conteo histórico de ronda 2 y comprobar su esperado_actual actualizado.',
                               'Oráculo de recuperación HTTP basado en conteos vivos, sin fijar 836/232 históricos.'],
        'limites': ['Solo 2020 cruzado en el caso nuevo de proyecciones.',
                   'Igualdad numérica no acredita identidad de medidas ni vigencia de catálogos.',
                   'F1/F3 recomputan agregados históricos; no son una nueva lectura de microdatos.',
                   'El triaje de 3916 pares no acredita comparabilidad exhaustiva.',
                   'La respuesta del modelo desde la interfaz sigue sin evaluar.']}
    write(ROOT / 'reports/integracion-ronda-3.json', report)
    application = read(HERE / 'aplicacion.json')
    application.update({'estado': 'completada', 'pendiente': [], 'studio_modificado': True,
                        'sincronizacion_verificada': True, 'pruebas_centrales': 108,
                        'codigo_instalado_sha256': hashes, 'ajustes_integracion': report['ajustes_integracion']})
    write(HERE / 'aplicacion.json', application)
    orchestration = read(ROOT / 'docs/orquestacion-ronda-3.json')
    orchestration['estado'] = 'completada_ambito_chat_correspondencias_cruces'
    orchestration['coordinacion']['relevo_recibido'] = True
    orchestration['coordinacion']['no_escritura_central_hasta_relevo'] = False
    orchestration['resultado'] = {'informe': 'reports/integracion-ronda-3.json', 'revisadas': 865,
                                'fichas': 3, 'comparaciones_2020': 72, 'studio_verificado': True}
    for entry in orchestration['sesiones']:
        if entry['agente'] == 2:
            entry['estado_revision'] = 'integradas_29;865_totales'
        if entry['agente'] == 5:
            entry['estado_revision'] = 'integradas_3_fichas;72_comparaciones;144_evidencias'
    write(ROOT / 'docs/orquestacion-ronda-3.json', orchestration)
    print(json.dumps({'estado': report['estado'], 'pruebas': report['pruebas'], 'studio': report['studio']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
