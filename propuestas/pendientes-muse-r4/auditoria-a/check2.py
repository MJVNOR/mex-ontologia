import json, unicodedata
from urllib.parse import unquote
def norm(s):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
sem = json.load(open('ontologia/semantica.json', encoding='utf-8'))
nucleo_conc = set(sem['conceptos'].keys())
def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    idx = int(dec.rsplit('/', 1)[1])
    return dic, idx, insp[dic]['definiciones'][idx-1]
def field(row, names):
    for k in row:
        if norm(k) in names:
            return row[k]
    return ''
# concepto -> reglas
from collections import defaultdict
conc2rules = defaultdict(list)
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        for dd in r.get('definiciones', []):
            dic, idx, row = get_row(dd)
            tipo = field(row, {'tipo de dato'})
            ej = field(row, {'ejemplo de dato'})
            fmt = field(row, {'formato'})
            conc2rules[r.get('concepto')].append((r['id'], lote, dic, idx, r.get('representacion'), tipo, fmt, ej, field(row, {'descripcion','definicion'})))
        # limites presencia
        lim = r.get('limites', r.get('limite', ''))
        if not lim:
            print(f"NOLIM {r['id']}")
for conc, lst in sorted(conc2rules.items()):
    dics = set(x[2] for x in lst)
    lotes = set(x[1] for x in lst)
    if len(lst) > 1:
        print(f"CONC-REUSE {conc} n={len(lst)} lotes={sorted(lotes)} dics={sorted(dics)}")
        for x in lst:
            print(f"   {x[0]} rep={x[4]} tipo={str(x[5])[:30]!r} desc={str(x[8])[:70]!r}")
# representacion checks
print("---- representacion vs tipo ----")
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        rep = r.get('representacion')
        for dd in r.get('definiciones', []):
            dic, idx, row = get_row(dd)
            tipo = field(row, {'tipo de dato'})
            fmt = field(row, {'formato'})
            ej = field(row, {'ejemplo de dato'})
            cat = field(row, {'catalogo de referencia'})
            # codigo sin formato ni catalogo?
            if rep == 'codigo' and not str(fmt).strip() and not str(cat).strip():
                # check ejemplo looks like code?
                print(f" COD-SIN-FMT {r['id']} tipo={tipo!r} fmt={fmt!r} ej={ej!r} conc={r.get('concepto')}")
            if rep == 'nombre' and 'codigo' in norm(str(tipo)):
                print(f" NOM-vs-COD {r['id']} tipo={tipo!r}")
print("---- nucleo reuse ----")
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    for r in d['reglas']:
        if r.get('concepto') in nucleo_conc:
            print(f" NUCLEO-REUSE {r['id']} conc={r.get('concepto')} rep={r.get('representacion')}")
