"""Auditoria-b independiente: verifica cada vinculo propuesto (lote-1..6 + ambiguedades) y codigo de integracion."""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT/'propuestas/pendientes-muse-r4'
sys.path.insert(0, str(ROOT/'scripts'))
from consolidar_semantica import columnas, huella
from integrar_contenido import clave

def H(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

inv = load(ROOT/'data/portal/inventario.json')
ins = load(ROOT/'data/portal/contenido-inspeccion.json')
base_cov = load(STAGE/'fuentes/data/semantica/cobertura.json')
base_sem = load(STAGE/'fuentes/ontologia/semantica.json')
cols = {c['iri']:c for c in columnas(inv,ins,'https://example.org/mex-ontologi/')}
vars_by_iri = {v['definicion_iri']:v for v in base_cov['variables'] if v.get('definicion_iri')}
# huellas recomputed from raw inspecciones for spot-check of every diccionario usado
raw_cache = {}
def raw_row(dic, n):
    if dic not in raw_cache:
        raw_cache[dic]=load(ROOT/f'data/portal/inspecciones/{dic}.json')['definiciones']
    return raw_cache[dic][n-1]
def defnum(iri): return iri.split('%2F')[-1]

# conceptos merged (base + all new)
merged_conc = dict(base_sem['conceptos'])
new_rules = {}
for l in [f'lote-{i}' for i in range(1,7)]:
    d = load(STAGE/l/'entrega.json')
    for k,v in d.get('conceptos_nuevos',{}).items(): merged_conc[k]=v
    for r in d.get('reglas',[]): new_rules[r['id']]=r
supported = {v['definicion_iri'] for v in base_cov['variables'] if v['estado']=='respaldada_por_definicion'}
supported.update(d for r in new_rules.values() for d in r['definiciones'])
# baseline columnas revisadas (865) para solape
prev_cols = {c['columna'] for c in base_sem['vinculos_documentales_revisados']}

out = {'checks':[], 'fails':[]}
# comprobar.py execution (read-only)
import subprocess
res = subprocess.run([sys.executable, str(STAGE/'integrador/comprobar.py'),
                      *[f'lote-{i}' for i in range(1,7)]], capture_output=True, text=True, cwd=str(ROOT))
out['comprobar_lotes'] = res.stdout[-2000:] + res.stderr[-500:]
try:
    ctl = load(STAGE/'integrador/control-entregas.json')
    out['control'] = ctl
except Exception as e:
    out['control_error']=repr(e)

# per-vinculo verification
dicts = []
for l in [f'lote-{i}' for i in range(1,7)]+['ambiguedades']:
    d = load(STAGE/l/'entrega.json')
    dec = {r['columna']:r for r in d.get('decisiones_columnas',[])}
    for v in d.get('vinculos',[]):
        col_iri = v['columna']
        errs = []
        c = cols.get(col_iri)
        if c is None: errs.append('IRI fisica inexistente')
        else:
            if v.get('recurso')!=c['recurso']: errs.append(f"recurso {v.get('recurso')}!={c['recurso']}")
            if v.get('campo')!=c['campo']: errs.append(f"campo {v.get('campo')}!={c['campo']}")
            if v.get('huella_esquema')!=c['huella_esquema']: errs.append('huella_esquema distinta de fisica')
        prop = dec.get(col_iri)
        pin = (prop or {}).get('definicion_iri') or v.get('definicion_iri')
        if prop is None: errs.append('sin decision de columna')
        elif prop.get('decision')!='proponer': errs.append('decision no proponer')
        if not pin: errs.append('sin definicion_iri ni en decision ni vinculo')
        vv = vars_by_iri.get(pin) if pin else None
        if pin and vv is None: errs.append('definicion_iri sin variable en cobertura base: '+str(pin))
        else:
            if v.get('diccionario')!=vv['diccionario']: errs.append('diccionario distinto')
            if v.get('descripcion')!=vv['descripcion']: errs.append(f"descripcion distinta: vinculo={v.get('descripcion')!r} base={vv['descripcion']!r}")
            if v.get('huella_fila_diccionario')!=vv['huella_fila_diccionario']: errs.append('huella_fila distinta de base')
            if c is not None and c['conjunto']!=vv['conjunto']: errs.append('conjunto fisico vs diccionario distinto')
            # recompute huella from raw
            try:
                n=int(defnum(pin))
                if H(raw_row(vv['diccionario'],n))!=vv['huella_fila_diccionario']: errs.append('huella base no reproduce raw')
            except Exception as e: errs.append('raw error '+repr(e))
            if v.get('concepto')!=vv.get('concepto'):
                # permitido solo si una regla nueva del mismo lote respalda pin con ese concepto
                ok_new = False
                for l2 in [f'lote-{i}' for i in range(1,7)]:
                    d2 = load(STAGE/l2/'entrega.json')
                    for r in d2.get('reglas',[]):
                        if pin in r.get('definiciones',[]) and r.get('concepto')==v.get('concepto'):
                            # verificar regla literal exacta
                            if (r.get('nombres')==[vv['variable']] and r.get('descripciones')==[vv['descripcion']]
                                and r.get('conjuntos')==[vv['conjunto']] and r.get('diccionarios')==[vv['diccionario']]
                                and r.get('huella_fila_diccionario')==vv['huella_fila_diccionario']
                                and len(r.get('definiciones',[]))==1):
                                ok_new = True
                            else:
                                errs.append('regla nueva no literal exacta: '+r['id'])
                if not ok_new: errs.append(f"concepto {v.get('concepto')}!={vv.get('concepto')} sin regla nueva que lo respalde")
            if v.get('concepto') not in merged_conc: errs.append('concepto ausente en nucleo+propuestos')
            # dependencia: si variable no respaldada en base, debe haber regla nueva que la respalde
            if pin not in {x['definicion_iri'] for x in base_cov['variables'] if x['estado']=='respaldada_por_definicion'}:
                if pin not in supported: errs.append('definicion sin respaldo ni regla nueva ni dependencia')
            if not v.get('criterio'): errs.append('sin criterio')
            if 'variable' in v and v.get('variable')!=v.get('campo') and not v.get('columna'):
                errs.append('alias global sin columna fisica')
            if col_iri in prev_cols: errs.append('solapa base 865')
        dicts.append((l, col_iri, pin, errs, v, prop, vv, c))

Path(__file__).parent.joinpath('detalle.json').write_text(json.dumps(
    [{'lote':l,'columna':c,'definicion_iri':p,'errores':e} for l,c,p,e,_,_,_,_ in dicts],
    ensure_ascii=False,indent=1),encoding='utf-8')
print('vinculos',len(dicts))
from collections import Counter
print(Counter(l for l,_,_,_,_,_,_,_ in dicts))
bad=[x for x in dicts if x[3]]
print('con errores:',len(bad))
for l,c,p,e,_,_,_,_ in bad[:40]:
    print(l,c[-40:],p[-12:] if p else None,e)
