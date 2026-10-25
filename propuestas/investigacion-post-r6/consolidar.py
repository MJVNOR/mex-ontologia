"""Coteja y reúne dictámenes documentales; no modifica el núcleo ni el grafo."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path('propuestas/investigacion-post-r6')

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    baseline = read(FOLDER / 'base.json')
    for path, fingerprint in baseline['fuentes_base'].items():
        require(sha(path) == fingerprint, f'Fuente base alterada: {path}')
    original = read('reports/pendientes-depurados.json')
    expected = {r['definicion_iri']: r for r in original['significados']}
    decisions, deliveries, checked, groups = [], {}, {}, []

    def check_references(value):
        if isinstance(value, dict):
            if isinstance(value.get('ruta'), str) and value.get('sha256'):
                path = Path(value['ruta'])
                require((ROOT / path).resolve().is_relative_to(ROOT), f'Ruta fuera del proyecto: {path}')
                require((ROOT / path).is_file(), f'Evidencia no encontrada: {path}')
                require(sha(path) == value['sha256'], f'SHA no coincide: {path}')
                checked[path.as_posix()] = value['sha256']
            for item in value.values():
                check_references(item)
        elif isinstance(value, list):
            for item in value:
                check_references(item)

    for group, count in original['por_grupo'].items():
        path = FOLDER / group / 'entrega.json'
        doc = read(path)
        require(doc['grupo_fuente'] == group, f'Grupo incorrecto: {path}')
        require((ROOT / FOLDER / group / 'listo.json').is_file(), f'Falta cierre: {group}')
        rows = doc['decisiones']
        ids = [r['definicion_iri'] for r in rows]
        target = {iri for iri, row in expected.items() if row['grupo_fuente'] == group}
        require(len(ids) == len(set(ids)) == count and set(ids) == target, f'Asignación incompleta: {group}')
        for row in rows:
            source = expected[row['definicion_iri']]
            for key in ('variable', 'descripcion_original', 'huella_fila_diccionario'):
                require(row[key] == source[key], f'Original alterado: {group}/{row["variable"]}/{key}')
            require(row['estado'] in ('sigue_pendiente', 'propuesta_respaldada'), 'Estado no permitido')
            require(row.get('evidencia') and row.get('motivo') and row.get('vinculo_fuente_local'), f'Falta motivación: {row["variable"]}')
            if row['estado'] == 'sigue_pendiente':
                require(row.get('evidencia_faltante'), f'Falta brecha: {row["variable"]}')
            else:
                require(row.get('significado_propuesto'), f'Falta propuesta: {row["variable"]}')
            decisions.append(dict(row, grupo_fuente=group))
        check_references(doc)
        marker = read(FOLDER / group / 'listo.json')
        check_references(marker)
        if isinstance(marker.get('archivos'), dict):
            for filename, fingerprint in marker['archivos'].items():
                require(sha(FOLDER / group / filename) == fingerprint, f'Marcador obsoleto: {group}/{filename}')
        for key, filename in (('sha256_entrega_json', 'entrega.json'), ('sha256_entrega_md', 'entrega.md')):
            if key in marker:
                require(sha(FOLDER / group / filename) == marker[key], f'Marcador obsoleto: {group}/{filename}')
        deliveries[group] = {'ruta': path.as_posix(), 'sha256': sha(path)}
        groups.append({'grupo': group, 'investigados': count, 'estados': dict(Counter(r['estado'] for r in rows)), 'informe': f'../{FOLDER.as_posix()}/{group}/entrega.md'})

    require(len(decisions) == len({r['definicion_iri'] for r in decisions}) == 169, 'Cobertura global distinta de 169')
    audits = {}
    for name in ('auditoria-salud', 'auditoria-otros', 'auditoria-educacion-tic', 'auditoria-clasif'):
        path = FOLDER / name / 'dictamen.json'
        doc = read(path)
        check_references(doc)
        if name != 'auditoria-clasif':
            require(doc.get('dictamen') == 'aceptar', f'Auditoría documental sin aceptación final: {name}')
        else:
            require(doc.get('dictamen', doc.get('veredicto')) == 'rechazar', 'Falta dictamen de la propuesta CLASIF rechazada')
        audits[name] = {'ruta': path.as_posix(), 'sha256': sha(path), 'dictamen': doc}
    states = dict(Counter(r['estado'] for r in decisions))
    report = {'generado_en_utc': datetime.now(timezone.utc).isoformat(), 'alcance': 'Investigación documental de los 169 pendientes reales tras R6; las propuestas no se integran sin aprobación independiente.', 'resumen': {'investigados': len(decisions), **states, 'promociones_integradas': 0}, 'grupos': groups, 'decisiones': decisions, 'entregas': deliveries, 'auditorias': audits, 'fuentes_cotejadas': checked, 'fuentes_base_preservadas': baseline['fuentes_base'], 'conteos_semanticos': original['conteos_semanticos_preservados'], 'grafo_modificado': False, 'contactos_externos': 0, 'chat': 'pospuesto por decisión del usuario'}
    lines = ['# Investigación documental posterior a R6', '', f'Se investigaron **169 significados** con seis agentes OpenCode en paralelo (`opencode-go/muse-spark-1.3-contributor`). Siguen pendientes {states.get("sigue_pendiente", 0)}; propuestas activas: {states.get("propuesta_respaldada", 0)}. No se integraron promociones.', '', '| Fuente | IDs examinados | Informe |', '| --- | ---: | --- |']
    lines += [f'| {r["grupo"]} | {r["investigados"]} | [Evidencia y dictámenes]({r["informe"]}) |' for r in groups]
    lines += ['', 'Cada dictamen conserva el texto original, la evidencia examinada, su vínculo con el recurso local y el obstáculo concreto para la promoción. Las búsquedas negativas se limitan a las fuentes consultadas; no prueban que la documentación no exista.', '', '## Revisión independiente', '']
    lines += [f'- [{name}](../{item["ruta"]})' for name, item in audits.items()]
    lines += ['', '## Resultados y límites', '', '- **Defunciones:** examen por ID de las 32 variables contra el manual SEED Modelo 2022, con pregunta y página. Se distinguen certificados generales y fetales; persisten obstáculos de correspondencia formal, códigos o ámbito por variable.', '- **Nacimientos:** contraste de las 53 variables con documentación SINAC y fuentes primarias preservadas; la documentación examinada no acredita la definición o edición aplicable a cada campo local.', '- **Matrículas:** revisión del archivo 2022-2, sus distribuciones y documentación UES adicional. Los valores observados y normas de otras ediciones no acreditan por sí solos el significado y representación de los 30 campos.', '- **Epidemiología y TIC:** se conservan fuentes e intentos nuevos de consulta, junto con el documento o vínculo concreto que aún falta por campo.', '- **CLASIF:** se confirmó que las 2129 filas del archivo local coinciden por clave y en sus 28 campos con el extracto Sonora del producto CONAPO 2020. Esa evidencia acredita procedencia; los diccionarios local y nacional siguen diciendo únicamente «Clasificación». Se rechazó la glosa «tipo de asentamiento» por falta de fuente explícita. Los 38 valores nacionales son observados, no un catálogo cerrado. No se promovió un concepto tautológico ni se autorizaron cruces.', '- **Vías limitadas:** se registran fallos HTTP y documentos que no pudieron examinarse. El RAR de cálculo CONAPO pudo extraerse con tar.exe de Windows y su programa se examinó como texto, sin ejecutarlo; no aportó una definición de CLASIF.', '', '## Estado preservado', '', 'Se mantienen 1392 significados respaldados, 1075 conceptos, 4475 correspondencias revisadas, 20 candidatas y cero ambiguas. Las 16 brechas de vigencia y la anomalía heredada `des_mpo_res` siguen en su matriz previa. Se conservan los dos encabezados corruptos fuera de esta vista de investigación.', '', f'Se cotejaron {len(checked)} referencias locales con SHA-256, los originales de los 169 registros y los 12 archivos base. No se contactó a publicadores ni se modificó Studio o el chat. El código preparado para una eventual R7 permanece en staging, marcado para no aplicar.', '', '[Detalle completo, decisiones y hashes](investigacion-post-r6.json).', '']
    (ROOT / 'reports/investigacion-post-r6.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'reports/investigacion-post-r6.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'resumen': report['resumen'], 'fuentes_cotejadas': len(checked)}, ensure_ascii=True))

if __name__ == '__main__':
    main()
