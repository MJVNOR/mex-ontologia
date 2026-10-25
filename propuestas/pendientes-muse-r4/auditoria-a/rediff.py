import json, hashlib, unicodedata
from pathlib import Path
from urllib.parse import unquote

STAGE = Path('propuestas/pendientes-muse-r4')
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
def norm(s):
    import unicodedata
    return " ".join("".join(c for c in unicodedata.normalize("NFD", str(s).lower()) if unicodedata.category(c) != "Mn").strip(" ,;:\t\n").split())
def huella(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
def get_row(defiri):
    dec = unquote(defiri)
    dic = dec.split('/definition/', 1)[1].rsplit('/', 1)[0]
    return dic, int(dec.rsplit('/', 1)[1])

base = {d['id']: d for d in json.load(open(STAGE / 'auditoria-a' / 'entrega.json', encoding='utf-8'))['dictamenes']}
print('baseline dictamenes:', len(base))

for lote in ['lote-2', 'lote-3', 'lote-4', 'lote-6']:
    d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
    print(f'==== {lote} ({len(d["reglas"])} reglas)')
    for r in d['reglas']:
        rid = r['id']
        b = base.get(rid)
        if b is None:
            print(f'  NEW-ID {rid} conc={r.get("concepto")} rep={r.get("representacion")}')
        elif b['dictamen'] != 'aceptar':
            print(f'  WAS-{b["dictamen"]} {rid}')
        # check huella still OK
        dd = r['definiciones'][0]
        dic, idx = get_row(dd)
        row = insp[dic]['definiciones'][idx - 1]
        if huella(row) != r.get('huella_fila_diccionario'):
            print(f'  HUELLA-DIFIERE {rid}')
# retired check
for rid in ['r4-lote-4-025', 'r4-lote-4-026', 'r4-lote-4-027']:
    found = []
    for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
        d = json.load(open(STAGE / lote / 'entrega.json', encoding='utf-8'))
        if any(r['id'] == rid for r in d['reglas']):
            found.append(lote)
    print(rid, 'presente en:', found or 'NINGUNO (retirada)')
