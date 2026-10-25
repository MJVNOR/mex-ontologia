"""Fija insumos y reparte pendientes sin modificar el núcleo."""
import collections
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r4'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if (STAGE / 'fuentes/manifiesto.json').exists():
        raise RuntimeError('Base ya fijada; no reemplazar')
    pending = read(ROOT / 'reports/pendientes-semanticos.json')
    coverage = read(ROOT / 'data/semantica/cobertura.json')
    names = [f'lote-{i}' for i in range(1, 7)]
    lots = {n: {'columnas': [], 'variables_pendientes': []} for n in names}
    by_dataset = collections.defaultdict(lambda: {'columnas': [], 'variables_pendientes': []})
    for c in pending['columnas']:
        if c['estado'] == 'candidata_por_nombre':
            by_dataset[c['conjunto']]['columnas'].append(c)
    for v in pending['variables_pendientes']:
        by_dataset[v['conjunto']]['variables_pendientes'].append(v)
    for dataset, group in sorted(by_dataset.items(), key=lambda kv: -(len(kv[1]['columnas'])+4*len(kv[1]['variables_pendientes']))):
        target = min(names, key=lambda n: len(lots[n]['columnas'])+4*len(lots[n]['variables_pendientes']))
        for k in group:
            lots[target][k].extend(group[k])
    all_variables = {v['definicion_iri']: v for v in coverage['variables'] if v.get('definicion_iri')}
    snapshots = ['reports/pendientes-semanticos.json', 'data/semantica/cobertura.json',
                 'ontologia/semantica.json', 'ontologia/revision-agentes.json',
                 'ontologia/revision-cobertura.json', 'ontologia/revision-ronda-3.json',
                 'scripts/consolidar_semantica.py', 'scripts/integrar_ronda_3.py']
    manifest = {'insumos_centrales': {p: sha(ROOT / p) for p in snapshots}, 'lotes': {}}
    with ZipFile(STAGE / 'integrador/antes-r4.zip', 'x', ZIP_DEFLATED) as archive:
        for directory in ['ontologia', 'scripts', 'shapes', 'tests', 'queries']:
            for p in (ROOT / directory).rglob('*'):
                if p.is_file() and '__pycache__' not in p.parts:
                    archive.write(p, p.relative_to(ROOT))
    for p in snapshots:
        dest = STAGE / 'fuentes' / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((ROOT / p).read_bytes())
    for name, lot in lots.items():
        ids = {d for c in lot['columnas'] for d in c['definiciones_por_nombre']}
        ids.update(v['definicion_iri'] for v in lot['variables_pendientes'])
        lot['definiciones_contexto'] = [all_variables[d] for d in sorted(ids)]
        lot['resumen'] = {'columnas': len(lot['columnas']), 'significados': len(lot['variables_pendientes'])}
        write(STAGE / name / 'asignacion.json', lot)
        manifest['lotes'][name] = dict(lot['resumen'], sha256=sha(STAGE / name / 'asignacion.json'))
    write(STAGE / 'ambiguedades/asignacion.json', {
        'columnas': [c for c in pending['columnas'] if c['estado']=='ambigua_por_nombre'],
        'observaciones': pending['observaciones_revision']})
    for name in ['investigacion', 'catalogos', 'chat', 'auditoria-a', 'auditoria-b']:
        (STAGE / name).mkdir(parents=True, exist_ok=True)
    write(STAGE / 'fuentes/manifiesto.json', manifest)
    common = '''# Instrucciones de la ronda 4

Trabaja autónomamente hasta terminar tu encargo. Solo puedes escribir en TU carpeta asignada bajo propuestas/pendientes-muse-r4/. Lee asignacion.json si existe, fuentes/manifiesto.json, docs/nucleo-semantico.md y docs/correspondencias-y-cruces-ronda-3.md. No modificar núcleo, scripts centrales, reportes, otras entregas, configuraciones, credenciales ni Studio salvo el evaluador con autorización de pruebas de chat. No lanzar subagentes. No esperar/pollear a otros: termina lo comprobable y deja solicitudes concretas.

Base vigente: 865 correspondencias revisadas, 1212 significados respaldados, 940 conceptos. El informe cobertura-muse.md es histórico (836 correspondencias). Preservar la base actual. Las coincidencias de nombre solo son candidatos. No inferir unidades, escalas, moneda, identidad entre medidas, catálogos nacionales, vigencias, cohortes ni tasas. Conservar códigos, ceros, léxico y calificadores. Una revisión documental no valida datos ni habilita cruces.

## Especialistas lote-1 a lote-6
Revisar TODAS tus columnas y definiciones. Puedes usar scripts locales en TU carpeta para preparar y verificar; agrupa por conjunto/diccionario/recurso para examinar evidencia completa, sin aprobar solo por nombre ni por estar respaldada la definición. Consulta esquemas capturados en data/ y diccionarios, títulos, contexto, unicidad y huellas. Usa reglas previas como formato, no como aprobación automática de filas nuevas. Si falta evidencia, pendiente preciso. Los significados con descripción vacía requieren respaldo explícito vinculado a esa definición, no una interpretación del nombre.

Entrega entrega.json con:
- decisiones_columnas: una por columna asignada, campos columna, recurso, campo, decision (proponer|pendiente|rechazar), definicion_iri (si destino), motivo, evidencia (lista de rutas y localizadores verificables).
- vinculos: formato EXACTO de ontologia/semantica.json vinculos_documentales_revisados, uno por decision proponer. Incluye recurso,campo,columna,diccionario,concepto,descripcion,huella_esquema,huella_fila_diccionario,criterio. Verifica cada huella desde fuentes. Indica definición en decisiones_columnas. Un vínculo que dependa de significado nuevo se marca dependencia explícita.
- decisiones_significados: una por definición pendiente asignada, definicion_iri, decision (proponer|pendiente), motivo, evidencia.
- reglas: reglas propuestas con ID r4-lote-N-..., nombres/descripciones/conjuntos/diccionarios/definiciones restringidos a la fila exacta, huella_fila_diccionario, concepto, representacion, evidencia, limites, criterio. Nunca aprobar solo por clasificador o sugerencia. No cambiar reglas previas.
- conceptos_nuevos: objeto del mismo formato de tres elementos del núcleo (etiqueta, definición, padre); reutilizar conceptos respaldados cuando sea exacto, no aproximado.
- solicitudes_investigacion: dudas con IRIs, fuente probable y documento requerido.

Escribe pendientes.json (detalle de evidencia faltante) y resultado.md con cuentas verificadas. Al terminar, listo.json debe tener sha256 de entrega.json y los conteos. No editar tras listo hasta petición del integrador. Si no puedes completar, registra estado incompleto y conteos exactos; no generar decisiones fingiendo revisión.

## Otros roles
Entregan entrega.json con evidencias, decisiones y pendientes identificados; resultado.md y listo.json con sha256 de entrega.json. Solo el investigador controla Obscura; los demás leen fuentes locales y dejan solicitudes. No contactar publicadores. Fuente nacional no acredita aplicación local ni versión histórica. Auditores solo aprueban versiones SHA exactas: no aprobar conteos ni textos de agentes sin examinar respaldo.
'''
    (STAGE / 'INSTRUCCIONES.md').write_text(common, encoding='utf-8')
    write(STAGE / 'integrador/estado.json', {'estado': 'base_fijada', 'modelo':'opencode-go/muse-spark-1.3-contributor', 'sesiones_previstas':12, 'concurrencia_maxima':6, 'lotes':manifest['lotes']})
    print(json.dumps(manifest['lotes'], ensure_ascii=True))

if __name__ == '__main__':
    main()
