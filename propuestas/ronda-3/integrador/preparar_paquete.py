"""Congela el paquete propio en staging; no escribe el núcleo ni el motor."""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE = HERE / 'paquete'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def copy(source, relative):
    target = PACKAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main():
    if PACKAGE.exists():
        raise ValueError('El paquete ya existe: no se sobrescribe evidencia congelada')
    for agent in (2, 5):
        receipt = json.loads((HERE / f'revision-agente-{agent}.json').read_text(encoding='utf-8'))
        name = 'agente-2-correspondencias' if agent == 2 else 'agente-5-cruces'
        source = HERE.parent / name / 'propuestas.json'
        if sha(source) != receipt['sha256_propuestas']:
            raise ValueError('Entrega aprobada modificada: ' + name)
    rules = json.loads((ROOT / 'ontologia/semantica.json').read_text(encoding='utf-8'))
    links = rules['vinculos_documentales_revisados']
    if len(links) != 836:
        raise ValueError('No se encuentra la base de 836 vínculos')
    coverage_base = ROOT / 'data/integracion-cobertura/base-semantica.json'
    if coverage_base.exists() and links != json.loads(coverage_base.read_text(encoding='utf-8'))['vinculos_documentales_revisados']:
        raise ValueError('La base no coincide con la fijada por el integrador semántico')
    PACKAGE.mkdir()
    write(PACKAGE / 'vinculos-anteriores.json', links)
    copy(HERE.parent / 'agente-2-correspondencias/entrada_integracion_29.json', 'correspondencias-29.json')
    copy(HERE.parent / 'agente-2-correspondencias/propuestas.json', 'entregas/agente-2-correspondencias/propuestas.json')
    for relative in ('propuestas.json', 'fichas/F1.json', 'fichas/F2.json', 'fichas/F3.json',
                     'fichas/claves-2020.json', 'matriz-cruces.json'):
        copy(HERE.parent / 'agente-5-cruces' / relative, 'entregas/agente-5-cruces/' + relative)
    for name in ('instalacion-chat.json', 'revision-agente-2.json', 'revision-agente-5.json',
                 'control-cruce-2020.json', 'control-cruces-staging.json'):
        copy(HERE / name, 'controles/' + name)
    for source, name in ((HERE / 'integrar_ronda_3.py', 'integrar_ronda_3.py'),
                         (HERE.parent / 'agente-5-cruces/staging/integrar_cruces_r3.py', 'integrar_cruces_r3.py'),
                         (HERE / 'ronda-3.ttl', 'ronda-3.ttl'),
                         (HERE.parent / 'agente-5-cruces/staging/cruces_r3.rq', 'cruces_r3.rq')):
        copy(source, 'codigo/' + name)
    inputs = ['data/portal/inventario.json', 'data/portal/contenido-inspeccion.json',
              'data/portal/lote-cruces/validacion-lote.json',
              'data/portal/oportunidades-cruce.json', 'data/portal/cruce-registro-civil.json']
    for digest in ('24301617b6a5d89cf99b34ed4d512324cedde52e0c625de9457238e3d8fa340c',
                   'e0e21aad3a84b4059efaf7525233ac05b08ced300f0f851fbadaab94057c027a'):
        relative = 'data/integracion/fuentes/' + digest + '.xlsx'
        if sha(ROOT / relative) != digest:
            raise ValueError('Original alterado: ' + relative)
        inputs.append(relative)
    manifest = {'ronda': 3, 'generado_en_utc': datetime.now(timezone.utc).isoformat(),
                'alcance': 'Chat instalado, 29 correspondencias y tres fichas de cruces; semántica integrada por otro chat.',
                'archivos': {p.relative_to(PACKAGE).as_posix(): sha(p) for p in sorted(PACKAGE.rglob('*')) if p.is_file()},
                'insumos': {relative: sha(ROOT / relative) for relative in inputs}}
    write(PACKAGE / 'manifiesto.json', manifest)
    print(json.dumps({'archivos': len(manifest['archivos']), 'insumos': len(inputs),
                      'manifiesto_sha256': sha(PACKAGE / 'manifiesto.json')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
