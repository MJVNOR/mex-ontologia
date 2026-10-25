import json, hashlib
from urllib.parse import unquote
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def huella(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
for lote in ['tic', 'matriculas']:
    d = json.load(open(f'propuestas/pendientes-muse-r5/{lote}/entrega.json', encoding='utf-8'))
    print('=' * 25, lote)
    for r in d['reglas']:
        dd = r['definiciones'][0]
        dec = unquote(dd)
        dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
        idx = int(dec.rsplit('/', 1)[1])
        row = insp[dic]['definiciones'][idx - 1]
        ok = huella(row) == r.get('huella_fila_diccionario')
        print(f" {r['id']} dic={dic[:8]} idx={idx} huella={'OK' if ok else 'DIFIERE'} tipo={next((str(row[k]) for k in row if 'tipo de dato' in k.lower()),'?')}")
    print(' conceptos_nuevos:', json.dumps(d.get('conceptos_nuevos', {}), ensure_ascii=False)[:1000])
    from collections import Counter
    print(' sig:', Counter(s.get('decision') for s in d['decisiones_significados']), 'cols:', Counter(c.get('decision') for c in d.get('decisiones_columnas', [])), 'vinc:', len(d.get('vinculos', [])))
    for s in d['decisiones_significados']:
        if s.get('decision') == 'pendiente':
            print('  PEND', str(s.get('definicion_iri',''))[-14:], '|', str(s.get('motivo'))[:160])
