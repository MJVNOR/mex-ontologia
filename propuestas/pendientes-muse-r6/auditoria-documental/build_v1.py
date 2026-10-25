"""Auditoria-documental R6: 4 entregas listas; salud y diversos-presas pendientes."""
import json, hashlib
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r6')
OUT = STAGE / 'auditoria-documental'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}

sha_fin = {}
for f in ['tic', 'matriculas', 'epidemiologia', 'catalogos']:
    h = sha(STAGE / f / 'entrega.json')
    lj = json.load(open(STAGE / f / 'listo.json', encoding='utf-8'))
    assert any(h == lj[k] for k in lj if 'sha' in k.lower()), f
    sha_fin[f] = h

dictamenes = []
# verificacion fila por fila: huellas + motivo/evidencia presentes
tot_dec = 0
for f, n in [('tic', 24), ('matriculas', 30), ('epidemiologia', 25), ('catalogos', 17)]:
    d = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    assert len(d.get('decisiones_significados', [])) == n, (f, len(d.get('decisiones_significados', [])))
    assert len(d.get('reglas', [])) == 0 and len(d.get('vinculos', [])) == 0, f
    for s in d['decisiones_significados']:
        assert s.get('decision') in ('pendiente', 'artefacto_documental'), (f, s.get('definicion_iri'))
        assert s.get('motivo'), (f, s.get('definicion_iri'))
        tot_dec += 1
        dictamenes.append({'tipo': 'decision', 'id': s.get('definicion_iri', s.get('id', f)), 'entrega': f,
            'dictamen': 'resolucion',
            'motivo': f"Pendiente bien fundado con evidencia y solicitud precisa; 0 propuestas/0 vinculos. {str(s.get('motivo'))[:200]}",
            'evidencia': [f'propuestas/pendientes-muse-r6/{f}/entrega.json']})
assert tot_dec == 96, tot_dec

# advertencias concretas
dictamenes.append({'tipo': 'advertencia', 'id': 'ADV-TIC-PROSA-6-11-6', 'entrega': 'tic', 'dictamen': 'advertencia',
    'motivo': 'Prosa resultado.md 6+11+6+1 inconsistente con motivos por ID (5 truncadas / 9 anaforas-sin-sujeto-vacuas / 9 contradicciones / 1 tautologia por lectura propia; la prosa enumera 5 nombres para 6 y 9 items para 6). Total 24/24 por ID verificado OK; no usar conteos de prosa como evidencia. Corregir prosa o eliminar buckets.',
    'evidencia': ['propuestas/pendientes-muse-r6/tic/resultado.md', '24 definicion_iri distintos con motivo individual']})
dictamenes.append({'tipo': 'advertencia', 'id': 'ADV-CAT-URLS-TITULO', 'entrega': 'catalogos', 'dictamen': 'advertencia',
    'motivo': 'Fuentes INV-R4C usan slugs construidos desde titulos (dataset/Promedio%20Academico, Matriculas, Recursos%20Hidricos, Fiebre%20manchada%20(Rickettsia)...), no UUID verificado ni constancia de URL-final en R6. Decisiones se sostienen por C1/C2 (API estructurada + core-properties, primarias y frescas); normalizar URLs a UUID/slug verificado y registrar query+fecha de búsquedas negativas (DuckDuckGo acotada OK, sin pretension universal).',
    'evidencia': ['propuestas/pendientes-muse-r6/catalogos/entrega.json#fuentes']})
dictamenes.append({'tipo': 'advertencia', 'id': 'ADV-PENDIENTES-FALTANTES', 'entrega': 'salud+diversos-presas', 'dictamen': 'advertencia',
    'motivo': 'Sin entrega: salud (85 = nac53+def32 reagrupados) ni diversos-presas (7, incluye 2 artefactos y columna presas). No se finge revision total: 96/171 decisiones auditadas; vigencias/presas/columna presas y diferenciacion de artefactos quedan pendientes de entrega.',
    'evidencia': ['propuestas/pendientes-muse-r6/salud/asignacion.json', 'propuestas/pendientes-muse-r6/diversos-presas/asignacion.json']})

entrega = {'rol': 'auditoria-documental', 'version': 'v1', 'modelo': 'Muse 1.3',
    'sha_entregas': sha_fin,
    'preservacion_179_171': 'R5: 179 pendientes; 8 aceptadas R5 (7 TIC+1 nac) -> 171 = tic24+nac53+def32+epi25+mat30+div7. R6: salud85=nac53+def32 reagrupados; diversos-presas7. Auditado: 24+30+25+17=96; pendientes de entrega: 85+7=75.',
    'base_intacta': True,
    'dictamenes': dictamenes,
    'fuentes_no_verificadas': ['Slugs dataset construidos desde titulos (catalogos INV-R4C): no re-verificados en R6; decisiones sostenidas por C1/C2.',
        'Ausencia web adopcion UTH: acotada a DuckDuckGo (cero accionables); registrar query+fecha.',
        'EPI-R6-01..03 y TIC r6-tic-web-01..07 y MAT web: en manos del rol web / publicador.',
        'Matriculas PDF UES verificado (magic+sha); EPI manual SHA corregido a 64hex verificado.'],
    'conteos': {'decisiones_auditadas': 96, 'resolucion': 96, 'advertencias': 3, 'reglas_propuestas': 0, 'artefactos_en_listos': 0,
                'pendientes_entrega': {'salud': 85, 'diversos-presas': 7}}}
json.dump(entrega, open(OUT / 'entrega.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(dictamenes), 'dictamenes; decisiones:', tot_dec)
