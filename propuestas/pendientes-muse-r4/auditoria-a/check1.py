import json, hashlib, unicodedata
from urllib.parse import unquote

def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()

def norm(s):
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())

insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}

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

for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    print('====', lote)
    for r in d['reglas']:
        rid = r['id']; conc = r.get('concepto'); rep = r.get('representacion')
        defs = r.get('definiciones', [])
        if len(defs) != 1:
            print(f' {rid} NDEFS={len(defs)}')
        for dd in defs:
            dic, idx, row = get_row(dd)
            rn = field(row, {'nombre variable','nombre de variable','variable','nombre campo','nombre del campo'})
            rd = field(row, {'descripcion','definicion'})
            if rn not in r.get('nombres', []) or rd not in r.get('descripciones', []):
                print(f' MISMATCH {rid} row=({rn!r},{str(rd)[:70]!r})')
            tipo = ''
            for k in row:
                if 'tipo de dato' in norm(k):
                    tipo = row[k]
            fmt = ''
            for k in row:
                if norm(k) == 'formato':
                    fmt = row[k]
            ej = ''
            for k in row:
                if 'ejemplo' in norm(k):
                    ej = row[k]
            if 'booleano' in norm(str(tipo)) and any(s in conc for s in ['conteo','cantidad','procedimiento','pruebas','atencion','tipos','tipo-pruebas']):
                print(f' FLAG-BOOL {rid} conc={conc} tipo={tipo!r} fmt={fmt!r} ej={ej!r}')
            if rep == 'hora' and 'fecha' in norm(str(tipo)):
                print(f' FLAG-HORA {rid} tipo={tipo!r} ej={ej!r}')
