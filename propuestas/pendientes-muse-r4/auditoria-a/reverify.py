import json, hashlib, re
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r4')
def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
base = {d['id']: d for d in json.load(open(STAGE / 'auditoria-a' / 'entrega.json', encoding='utf-8'))['dictamenes']}

def ev_field(ev, prefix):
    for e in ev:
        if e.startswith(prefix):
            return e[len(prefix):]
    return ''

mismatch = 0
total = 0
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        total += 1
        b = base.get(r['id'])
        if b is None:
            print('ID-NUEVO (no estaba en revision previa):', r['id']); mismatch += 1
            continue
        if b['dictamen'] != 'aceptar':
            continue  # cambiadas: ya examinadas aparte
        # no cambiada segun previa: verificar identidad de campos clave
        old_conc = ev_field(b['evidencia'], 'concepto=').split(' representacion=')[0]
        old_rep = ev_field(b['evidencia'], 'concepto=').split('representacion=')[-1]
        old_h = ev_field(b['evidencia'], 'huella_fila_diccionario=').split(' recomputada=')[0]
        if r.get('concepto') != old_conc or r.get('representacion') != old_rep or r.get('huella_fila_diccionario') != old_h:
            print('CAMBIO-NO-DECLARADO:', r['id'], (old_conc, r.get('concepto')), (old_rep, r.get('representacion')))
            mismatch += 1
        dd = r['definiciones'][0]
        dec = unquote(dd)
        dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
        idx = int(dec.rsplit('/', 1)[1])
        if huella(insp[dic]['definiciones'][idx-1]) != r.get('huella_fila_diccionario'):
            print('HUELLA-DIFIERE:', r['id']); mismatch += 1
print('total reglas:', total, '| discrepancias en no-cambiadas:', mismatch)

# pendientes de las 3 retiradas
for lote in ['lote-4']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    for s in d['decisiones_significados']:
        iri = s.get('definicion_iri','')
        if iri.endswith('%2F36') or iri.endswith('%2F39') or iri.endswith('%2F40'):
            print(lote, iri[-12:], s.get('decision'), '|', str(s.get('motivo'))[:250])
    # conteos decisiones
    from collections import Counter
    print('decisiones:', Counter(x.get('decision') for x in d['decisiones_significados']))
for lote in ['lote-1','lote-2','lote-3','lote-5','lote-6']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    from collections import Counter
    print(lote, 'reglas:', len(d['reglas']), 'sig:', Counter(x.get('decision') for x in d['decisiones_significados']))
