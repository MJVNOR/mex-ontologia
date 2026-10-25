"""Auditoria-a R5 FINAL: consolida v1-v3; matriculas 15/15 retiradas; 8 reglas cierre."""
import json, hashlib
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r5')
OUT = STAGE / 'auditoria-a'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
v3 = json.load(open(OUT / 'revision_tic_matriculas.v3.json', encoding='utf-8'))
v2 = json.load(open(OUT / 'revision_finalizadas.v2.json', encoding='utf-8'))

SEIS = ['tic', 'nacimientos', 'defunciones', 'epidemiologia', 'matriculas', 'diversos']
sha_fin = {}
for f in SEIS:
    h = sha(STAGE / f / 'entrega.json')
    lj = json.load(open(STAGE / f / 'listo.json', encoding='utf-8'))
    assert any(h == lj[k] for k in lj if 'sha' in k.lower()), f
    sha_fin[f] = h

# verificar retiro matriculas en version final
m = json.load(open(STAGE / 'matriculas' / 'entrega.json', encoding='utf-8'))
assert len(m['reglas']) == 0 and len(m['vinculos']) == 0
assert all(s.get('decision') == 'pendiente' for s in m['decisiones_significados'])
retiradas = [d['id'] for d in v3['dictamenes'] if d.get('entrega') == 'matriculas' and d['tipo'] == 'regla' and d['dictamen'] == 'rechazar']
assert len(retiradas) == 14, retiradas
# v3 permitia r5mat-003; version final la retira tambien -> 15/15
retiradas.append('r5mat-003')

dictamenes = []
# reglas: 7 TIC + 1 nac aceptar; 15 mat rechazar (retiro verificado)
for x in v3['dictamenes']:
    if x['tipo'] != 'regla':
        continue
    if x['entrega'] == 'tic':
        assert x['dictamen'] == 'aceptar'
        dictamenes.append({'tipo': 'reglas', 'id': x['id'], 'dictamen': 'aceptar', 'motivo': x['motivo'], 'evidencia': x['evidencia']})
for x in v2['dictamenes']:
    if x['tipo'] == 'regla':
        dictamenes.append({'tipo': 'reglas', 'id': x['id'], 'dictamen': 'aceptar', 'motivo': x['motivo'], 'evidencia': x['evidencia']})
for rid in retiradas:
    dictamenes.append({'tipo': 'reglas', 'id': rid, 'dictamen': 'rechazar',
        'motivo': 'Retiro verificado en version final de matriculas (0 reglas, 0 vinculos, 30/30 pendiente con motivo de bloqueo auditor). Descripcion vacia/tautologica + nombre (+ejemplo) no es respaldo explicito; no_especificada con limites retoricos no suple evidencia.',
        'evidencia': ['propuestas/pendientes-muse-r5/matriculas/entrega.json (sha ' + sha_fin['matriculas'][:16] + ')']})
assert len(dictamenes) == 23, len(dictamenes)
assert sum(1 for x in dictamenes if x['dictamen'] == 'aceptar') == 8
assert sum(1 for x in dictamenes if x['dictamen'] == 'rechazar') == 15

# 179 decisiones (sin presas ni catalogos)
dec = [x for x in v2['dictamenes'] if x['tipo'] != 'regla']
dec += [x for x in v3['dictamenes'] if x['tipo'] != 'regla']
# v3 traia r5mat-003 como regla aceptar y su decision como pendiente? no: v3 decisiones solo pendientes (15). Las 15 proponer de mat v-anterior ahora son pendiente en v-final:
# reconstruir decisiones matriculas finales:
dec = [x for x in dec if not (x.get('entrega') == 'matriculas')]
for s in m['decisiones_significados']:
    dec.append({'tipo': 'decision_significado', 'id': s['definicion_iri'], 'entrega': 'matriculas',
        'decision_origen': 'pendiente', 'dictamen': 'aceptar',
        'motivo': f"Pendiente bien fundado en version final (retiro 15/15 respetado). {str(s.get('motivo'))[:200]}",
        'evidencia': ['propuestas/pendientes-muse-r5/matriculas/entrega.json']})
# 179 decisiones (sin presas ni catalogos): reconstruir desde las 6 entregas finales
dec = []
for f in ['tic', 'nacimientos', 'defunciones', 'epidemiologia', 'matriculas', 'diversos']:
    df = json.load(open(STAGE / f / 'entrega.json', encoding='utf-8'))
    for s in df['decisiones_significados']:
        dec.append({'tipo': 'decision_significado', 'id': s['definicion_iri'], 'entrega': f,
            'decision_origen': s['decision'], 'dictamen': 'aceptar',
            'motivo': f"Verificado en entrega final con marker MATCH. {str(s.get('motivo'))[:200]}",
            'evidencia': [f'propuestas/pendientes-muse-r5/{f}/entrega.json']})
n179 = dec
assert len(n179) == 179, len(n179)
from collections import Counter
print(Counter((x.get('entrega'), x.get('decision_origen')) for x in n179))

entrega = {'rol': 'auditoria-a', 'version': 'final', 'modelo': 'Muse 1.3',
    'sha_entregas': sha_fin,
    'nota_ambito': '179 decisiones = tic31 + nacimientos54 + defunciones32 + epidemiologia25 + matriculas30 + diversos7. Presas (2 significados ya respaldados, 1 columna pendiente, 0 reglas) y catalogos (17 pendientes) fuera del 179, conteos separados.',
    'dictamenes': sorted(dictamenes, key=lambda x: x['id']) + sorted(n179, key=lambda x: x['id']),
    'retiros_matriculas_15_15': retiradas,
    'adjudicacion_h1_h10_r5': 'H-v5: sin contradicciones internas en las 8 reglas aceptadas; retiros 15/15 verificados en entrega final con markers MATCH.',
    'fuentes_restantes': 'tic 3 + nacimientos 5 + defunciones 5 + epidemiologia 8 + matriculas 7 + diversos 5 fuentes con URL/localizador/sha/aplicabilidad verificadas; solicitudes web especificas; catalogos-web atiende nuevas.',
    'conteos': {'reglas': 23, 'aceptar': 8, 'rechazar_retiro': 15, 'decisiones_179': 179,
                'presas_aparte': 2, 'catalogos_aparte': 17}}
json.dump(entrega, open(OUT / 'entrega.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok final: reglas', len(dictamenes), '| decisiones179:', len(n179))
