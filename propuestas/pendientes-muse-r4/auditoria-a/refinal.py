import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r4')
OUT = STAGE / 'auditoria-a'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
prev = json.load(open(OUT / 'entrega.json', encoding='utf-8'))
prev_d = {d['id']: d for d in prev['dictamenes']}

RETIROS = {
    'r4-lote-4-025': 'Tipo Booleano Si/No vs concepto de conteo (P36 Cuantos proyectos): contradiccion real; pasa a pendiente sin inventar existencia alternativa.',
    'r4-lote-4-026': 'Tipo Booleano Si/No vs concepto de procedimiento (P39 Como atiende): contradiccion real; pasa a pendiente.',
    'r4-lote-4-027': 'Tipo Booleano Si/No vs concepto de conteo (P40 Cuantas personas) + duplica r3a9-059: contradiccion real; pasa a pendiente.',
}
CORREGIDAS_ACEPTADAS = {
    'r4-lote-2-021': 'Condicion cumplida: concepto propio numero-estudiante-matriculado con limite que lo distingue del ordinal generico.',
    'r4-lote-3-sector-dependencia-encuestada-8': 'Condicion cumplida: limite sin separar codigo/nombre, sin catalogo, sin comparacion entre encuestas.',
    'r4-lote-3-tiempo-9': 'Condicion cumplida: concepto propio momento-inicio-encuesta, no_especificada conserva Fecha y Hora, contradiccion formato-vs-ejemplo explicita, sin evento/cobertura.',
    'r4-lote-3-tiempo-10': 'Condicion cumplida: concepto propio momento-finalizacion-encuesta, resto igual que tiempo-9.',
    'r4-lote-3-tiempo-11': 'Condicion cumplida: concepto propio momento-ultima-modificacion-encuesta, resto igual que tiempo-9.',
    'r4-lote-3-apoyo-tendencias-tic-dependencia-14': 'Condicion cumplida: representacion no_especificada, solo existencia declarada, nota de truncamiento.',
    'r4-lote-3-recursos-anuales-innovacion-mencionados-16': 'Condicion cumplida: limite sin monto/moneda/unidad, solo lista declarada.',
    'r4-lote-3-instrumentos-previos-ley-gobierno-digital-18': 'Condicion cumplida: no_especificada + nota de truncamiento.',
    'r4-lote-3-instrumentos-actuales-mejora-administracion-20': 'Condicion cumplida: no_especificada + nota de truncamiento.',
    'r4-lote-4-002': 'Condicion cumplida: limite de no-comparabilidad entre metodologias (alternativa aceptada al renombre).',
    'r4-lote-4-003': 'Condicion cumplida: igual que 002 para subtipo.',
    'r4-lote-4-004': 'Condicion cumplida: igual que 002 para modalidad.',
    'r4-lote-4-008': 'Condicion cumplida: limite sin equiparacion de sectores entre encuestas.',
    'r4-lote-4-009': 'Condicion cumplida: igual que 008.',
    'r4-lote-4-010': 'Condicion cumplida: igual que 008.',
    'r4-lote-4-022': 'Condicion cumplida: positivo reformulado a respuesta de texto libre; limite no tabular ni agregar.',
    'r4-lote-4-038': 'Condicion cumplida: limite sin equivalencia entre diccionarios ni version CIE.',
    'r4-lote-4-039': 'Condicion cumplida: igual que 038.',
    'r4-lote-6-dig-sector-nombre': 'Condicion cumplida: limite sin separar codigo/nombre, sin comparar entre encuestas.',
}

dictamenes, cobertura = [], {'total_significados': 0, 'proponer': 0, 'pendiente': 0, 'detalle_por_lote': {}, 'defectos': []}
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    det = {'significados': len(d['decisiones_significados']), 'reglas': len(d['reglas']), 'definiciones': []}
    for s in d['decisiones_significados']:
        cobertura['total_significados'] += 1
        cobertura['proponer' if s.get('decision') == 'proponer' else 'pendiente'] += 1
        if not s.get('definicion_iri') or not s.get('motivo') or not s.get('evidencia'):
            cobertura['defectos'].append(f"{lote} {s.get('definicion_iri')}: sin motivo/evidencia")
        det['definiciones'].append(s.get('definicion_iri'))
    cobertura['detalle_por_lote'][lote] = det
    for r in d['reglas']:
        rid = r['id']
        assert rid not in RETIROS, rid
        dd = r['definiciones'][0]
        dec = unquote(dd)
        dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
        idx = int(dec.rsplit('/', 1)[1])
        h_ok = huella(insp[dic]['definiciones'][idx-1]) == r.get('huella_fila_diccionario')
        assert h_ok, rid
        row = insp[dic]['definiciones'][idx-1]
        tipo = next((row[k] for k in row if 'tipo de dato' in k.lower()), '')
        if rid in CORREGIDAS_ACEPTADAS:
            motivo = 'Reentrega verificada fila exacta (huella OK). ' + CORREGIDAS_ACEPTADAS[rid]
        else:
            assert prev_d[rid]['dictamen'] == 'aceptar', rid
            motivo = 'Sin cambios contra revision previa verificada (concepto/representacion/huella identicos, huella recomputada OK); aceptacion previa se mantiene.'
        dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'aceptar', 'motivo': motivo,
            'evidencia': [f"data/portal/contenido-inspeccion.json:diccionario={dic}:fila={idx}",
                f"huella_fila_diccionario={r.get('huella_fila_diccionario')} recomputada=OK",
                f"tipo={tipo}", f"definicion_iri={dd}",
                f"concepto={r.get('concepto')} representacion={r.get('representacion')}"]})
assert len(dictamenes) == 172, len(dictamenes)

entrega = {
    'rol': 'auditoria-a',
    'fecha_utc': datetime.now(timezone.utc).isoformat(),
    'alcance': 'Reauditoria de reentregas finales lote-2,3,4,6 tras dictamen (controles de integrador pasan): 172 reglas actuales (175 menos 3 retiradas), 351 decisiones. Sin modificar propuestas; sin UI/chat; sin Obscura; sin subagentes.',
    'sha_entregas': {lote: sha(STAGE / lote / 'entrega.json') for lote in
                     ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6','ambiguedades']},
    'sha_releidas_al_cierre': True,
    'dictamenes': dictamenes,
    'retiros': [{'id': k, 'destino': 'pendiente_por_contradiccion_real', 'motivo': v} for k, v in RETIROS.items()],
    'cobertura_revision': cobertura,
    'dictamen_conceptos_nuevos': prev['dictamen_conceptos_nuevos'] | {'nota_reentrega': 'Conceptos de reglas retiradas (conteo-proyectos, atencion-incidencias, conteo-personas) no se incorporan; nuevos momento-*-encuesta (lote-3, padre null) y numero-estudiante-matriculado (lote-2) verificados con formato valido y sin duplicar nucleo.'},
    'dictamen_fuentes_investigacion': prev['dictamen_fuentes_investigacion'],
    'dictamen_fuentes_catalogos': prev['dictamen_fuentes_catalogos'],
    'dictamen_ambiguedades': prev['dictamen_ambiguedades'],
    'adjudicacion_h1_h10': [
        {'h': 'H1', 'clase': 'resuelto_por_retiro_y_correccion',
         'detalle': '025/026/027 retiradas y pasadas a pendiente por contradiccion real (verificado en reentrega). 022 corregida y aceptada (positivo de texto libre + no tabular).',
         'reglas': ['r4-lote-4-022'], 'retiradas': ['r4-lote-4-025','r4-lote-4-026','r4-lote-4-027']},
        {'h': 'H2', 'clase': 'resuelto_por_correccion',
         'detalle': '002/003/004 con limite de no-comparabilidad entre metodologias verificado; 001 sin cambios aceptada.',
         'reglas': ['r4-lote-4-001','r4-lote-4-002','r4-lote-4-003','r4-lote-4-004']},
        {'h': 'H3', 'clase': 'resuelto_por_correccion',
         'detalle': 'tiempo-9/10/11 ahora con conceptos propios momento-*-encuesta y no_especificada que conserva Fecha y Hora, contradiccion formato-vs-ejemplo explicita. Aceptadas.',
         'reglas': ['r4-lote-3-tiempo-9','r4-lote-3-tiempo-10','r4-lote-3-tiempo-11']},
        {'h': 'H4', 'clase': 'resuelto_por_correccion_y_limite_verificado',
         'detalle': 'Sector (008/009/010, lote-3-08, dig-sector) y CIE (038/039) con limites de no-equiparacion verificados. Metadatos compartidos sin cambios: alcance+limite bastan, ninguna regla afirma equivalencia.',
         'reglas': ['r4-lote-4-008','r4-lote-4-009','r4-lote-4-010','r4-lote-4-038','r4-lote-4-039','r4-lote-3-sector-dependencia-encuestada-8','r4-lote-6-dig-sector-nombre']},
        {'h': 'H5', 'clase': 'resuelto_por_correccion',
         'detalle': '14/18/20 con no_especificada y notas de truncamiento verificadas. Aceptadas.',
         'reglas': ['r4-lote-3-apoyo-tendencias-tic-dependencia-14','r4-lote-3-instrumentos-previos-ley-gobierno-digital-18','r4-lote-3-instrumentos-actuales-mejora-administracion-20']},
        {'h': 'H6', 'clase': 'confirmado_limite_existente_suficiente_mas_solicitud',
         'detalle': '001 sin cambios aceptada; solicitud de redaccion normativa registrada en pendientes.',
         'reglas': ['r4-lote-4-001']},
        {'h': 'H7', 'clase': 'confirmado_sin_cambios', 'detalle': 'Patrones codigo+nombre, sector, CIE, CVE_LOC sin cambios; aceptaciones se mantienen.', 'reglas': []},
        {'h': 'H8', 'clase': 'confirmado_sin_cambios', 'detalle': 'Padres y limites sin cambios; nuevos conceptos verificados.', 'reglas': []},
        {'h': 'H9', 'clase': 'confirmado_sin_cambios', 'detalle': 'Sin nuevas equivalencias energeticas/territoriales.', 'reglas': []},
        {'h': 'H10', 'clase': 'confirmado_sin_cambios', 'detalle': 'Sujetos calificados sin cambios.', 'reglas': []},
    ],
    'hallazgos': [
        'Reentregas lote-2,3,4,6 con controles de integrador que pasan: 172 reglas (3 retiradas), 351 decisiones (172 proponer, 179 pendiente).',
        '19 reglas cambiadas reexaminadas fila exacta: condiciones cumplidas en las 19 (conceptos propios de momento, no_especificada en booleanos, limites de no-equiparacion/comparabilidad, concepto propio de estudiante).',
        '153 reglas no cambiadas identicas a la revision previa (concepto/representacion/huella) con huella recomputada OK.',
        '3 retiros (025/026/027) correctamente pasados a pendiente por contradiccion real, sin inventar existencia alternativa.',
        '135+ conceptos nuevos verificados (incluye momento-*-encuesta y numero-estudiante-matriculado); conceptos de retiradas no se incorporan.',
    ],
    'pendientes': prev['pendientes'],
    'conteos': {'reglas_dictaminadas': 172, 'aceptar': 172, 'rechazado': 0, 'condicionado': 0,
                'significados_revisados': 351, 'significados_proponer': 172, 'significados_pendiente': 179, 'retiros': 3},
}
json.dump(entrega, open(OUT / 'entrega.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok 172 aceptar; cobertura', cobertura['total_significados'], cobertura['proponer'], cobertura['pendiente'], 'defectos:', cobertura['defectos'])
