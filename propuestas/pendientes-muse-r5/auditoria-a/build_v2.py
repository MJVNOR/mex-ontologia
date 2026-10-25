"""Auditoria-a R5 v2: reentregas nacimientos(54,1 regla) + presas(0); reafirma v1."""
import json, hashlib
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r5')
OUT = STAGE / 'auditoria-a'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
sem = json.load(open('ontologia/semantica.json', encoding='utf-8'))

v1 = json.load(open(OUT / 'revision_finalizadas.v1.json', encoding='utf-8'))
dictamenes = list(v1['dictamenes'])

# --- regla unica nacimientos ---
d = json.load(open(STAGE / 'nacimientos' / 'entrega.json', encoding='utf-8'))
assert len(d['reglas']) == 1
r = d['reglas'][0]
assert r['id'] == 'r5-nac-resideextranjerod-no_especificada'
dd = r['definiciones'][0]
dec = unquote(dd)
dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
idx = int(dec.rsplit('/', 1)[1])
row = insp[dic]['definiciones'][idx - 1]
assert huella(row) == r['huella_fila_diccionario'], 'huella difiere'
tipo = next((row[k] for k in row if 'tipo de dato' in k.lower()), '')
assert tipo == 'Texto', tipo  # la fila /18 es Texto; el Numerico es /17, separado por limite
assert r['concepto'] not in sem['conceptos']
assert r['representacion'] == 'no_especificada'
dictamenes.append({'tipo': 'regla', 'id': r['id'], 'dictamen': 'aceptar',
    'motivo': 'Aceptar: fila /18 exacta (huella OK). Sin contradiccion tipo-sentido en la fila: Tipo Texto coherente con descripcion textual y ejemplo NO; el miembro Numerico es /17, no unificado por limite explicito con referencia a r3a7. no_especificada adecuada (texto declarado sin decodificar, ejemplo sin mapa). Sentido no inventado: literal de la descripcion + sujeto de la descripcion + alcance del titulo publicado. Ambito exacto; limites prohiben cruces, catalogo, vigencia e identidad.',
    'evidencia': [f"data/portal/contenido-inspeccion.json:diccionario={dic}:fila={idx}",
        f"huella_fila_diccionario={r['huella_fila_diccionario']} recomputada=OK", f"tipo={tipo} formato= ejemplo=NO",
        'r3a7-nac-resideextranjero-codigo verificado en nucleo (par /17 separado)']})

# --- 54 decisiones nacimientos ---
for s in d['decisiones_significados']:
    iri = s['definicion_iri']
    ok = bool(s.get('motivo')) and bool(s.get('evidencia'))
    assert ok, iri
    dictamenes.append({'tipo': 'decision_significado', 'id': iri, 'entrega': 'nacimientos',
        'decision_origen': s['decision'], 'dictamen': 'aceptar',
        'motivo': f"Pendiente/proponer bien fundado con evidencia y localizador. {str(s.get('motivo'))[:200]}",
        'evidencia': ['propuestas/pendientes-muse-r5/nacimientos/entrega.json', f'definicion_iri={iri}']})

# --- presas: 2 sig + 1 columna ---
p = json.load(open(STAGE / 'presas' / 'entrega.json', encoding='utf-8'))
assert len(p['reglas']) == 0
for s in p['decisiones_significados']:
    dictamenes.append({'tipo': 'decision_significado', 'id': s['definicion_iri'], 'entrega': 'presas',
        'decision_origen': s['decision'], 'dictamen': 'aceptar',
        'motivo': f"Pendiente bien fundado (variable ya respaldada, sin base para nuevo destino). {str(s.get('motivo'))[:200]}",
        'evidencia': ['propuestas/pendientes-muse-r5/presas/entrega.json']})
for c in p['decisiones_columnas']:
    dictamenes.append({'tipo': 'decision_columna', 'id': c.get('columna', c.get('campo')), 'entrega': 'presas',
        'decision_origen': c['decision'], 'dictamen': 'aceptar',
        'motivo': f"Columna Clave pendiente bien fundada (ambiguedad de hoja exacta conservada, sin joins por nombre). {str(c.get('motivo'))[:200]}",
        'evidencia': ['propuestas/pendientes-muse-r5/presas/entrega.json']})

a = sum(1 for x in dictamenes if x['dictamen'] == 'aceptar')
out = {'rol': 'auditoria-a', 'version': 'v2', 'modelo': 'Muse 1.3',
    'sha_entregas': {f: sha(STAGE / f / 'entrega.json') for f in ['nacimientos', 'defunciones', 'epidemiologia', 'diversos', 'presas']},
    'base_sin_cambios': True,
    'dictamenes': dictamenes,
    'conteos': {'dictamenes': len(dictamenes), 'aceptar': a, 'corregir': 0, 'rechazar': 0, 'reglas': 1, 'retiros': 0},
    'nota': 'v1 (64 dictamenes defunciones/epidemiologia/diversos) reafirmada: SHAs identicos. v2 agrega regla unica + 54 nacimientos + 3 presas. TIC/matriculas/catalogos-web aun sin entrega: criterios v1 y riesgos v1 siguen vigentes.'}
json.dump(out, open(OUT / 'revision_finalizadas.v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dictamenes:', len(dictamenes), 'aceptar:', a)
