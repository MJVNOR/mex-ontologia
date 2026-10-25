"""Auditoria-b ronda 5: verifica entregas cerradas, huellas fisicas y propuestas.
Solo escribe en propuestas/pendientes-muse-r5/auditoria-b/."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r5'
ME = STAGE / 'auditoria-b'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import huella
from integrar_contenido import clave

ME.mkdir(parents=True, exist_ok=True)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def H(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()

inv = load(ROOT / 'data/portal/inventario.json')
ins = load(ROOT / 'data/portal/contenido-inspeccion.json')
cob = load(ROOT / 'data/semantica/cobertura.json')
sem = load(ROOT / 'ontologia/semantica.json')
vars_by_iri = {v['definicion_iri']: v for v in cob['variables'] if v.get('definicion_iri')}

result = {'sha_entregas': {}, 'checks': [], 'dictamenes': []}

def check(name, ok, detail):
    result['checks'].append({'id': name, 'ok': bool(ok), 'detalle': detail})
    if not ok:
        raise ValueError('FALLO: ' + name + ' | ' + detail)

# 1. SHA entregas cerradas vs listo + control
for l in ['nacimientos', 'defunciones', 'epidemiologia', 'diversos', 'presas']:
    h = sha(STAGE / l / 'entrega.json')
    result['sha_entregas'][l] = h
    li = load(STAGE / l / 'listo.json')
    mk = li.get('sha256_entrega') or li.get('sha256') or li.get('sha256_entrega_json')
    check(l + '.listo', mk == h, f'listo={mk} file={h[:12]}')
ctl = load(STAGE / 'control.json')
for l in ['nacimientos', 'defunciones', 'diversos']:
    check(l + '.control', ctl['roles'][l]['sha256'] == result['sha_entregas'][l], 'control coincide')

# 2. Nacimientos columna 18: fisica + fila + regla + no-unificacion
d = load(STAGE / 'nacimientos/entrega.json')
COL = 'https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F18'
PIN = 'https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F18'
res = next(x for x in ins['recursos'] if x['id'] == '46977217-9396-4f9c-bddb-6616e82530b4')
tab = next(t for t in res['tablas'] if 'SINAC' in t['hoja'])
check('nac18.fisica', tab['campos'][17] == {'id': 'RESIDEEXTRANJEROD', 'posicion_original': 18}, str(tab['campos'][17]))
vinc = next(v for v in d['vinculos'] if v['columna'] == COL)
check('nac18.huella_esquema', vinc['huella_esquema'] == H(tab) == '9b46e1c0e32acd903780264f0ebbc538a835eb1bf92a70faa36ba7e839a1ec95', vinc['huella_esquema'])
raw = load(ROOT / 'data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json')
f18, f17 = raw['definiciones'][17], raw['definiciones'][16]
check('nac18.fila', (f18['Nombre variable'], f18['Tipo de dato']) == ('RESIDEEXTRANJEROD', 'Texto')
      and vinc['huella_fila_diccionario'] == H(f18) == '3c0156d2eaf5b3fbb00c421ae87e96fb5c7211b688f03739b9c73d269c5f68a1',
      repr({k: v for k, v in f18.items() if v})[:200])
check('nac18.tipo-contradiccion', (f17['Nombre variable'], f17['Tipo de dato']) == ('RESIDEEXTRANJERO', 'Numérico entero')
      and f17['Descripción'] != f18['Descripción'], 'Texto vs Numerico entero; descripciones distintas')
check('nac18.sin-alias', vinc['campo'] == f18['Nombre variable'] and 'variable' not in vinc, vinc['campo'])
vv = vars_by_iri[PIN]
check('nac18.conjunto-unico', vv['conjunto'] == '940de7d8-73ec-4a08-8d26-b7cc97ff17bd'
      and sum(1 for x in cob['variables'] if x.get('definicion_iri')
              and (x['conjunto'], clave(x['variable'])) == (vv['conjunto'], clave(vv['variable']))) == 1
      and vv['estado'] == 'fuera_del_nucleo_actual', vv['estado'])
rule = next(r for r in d['reglas'] if PIN in r['definiciones'])
check('nac18.regla-literal', rule['id'] == 'r5-nac-resideextranjerod-no_especificada'
      and rule['nombres'] == ['RESIDEEXTRANJEROD'] and rule['descripciones'] == [f18['Descripción']]
      and rule['conjuntos'] == [vv['conjunto']] and rule['diccionarios'] == ['22202305-2d02-4c49-b216-cc98224357f0']
      and len(rule['definiciones']) == 1 and rule['huella_fila_diccionario'] == H(f18)
      and rule['concepto'] in d['conceptos_nuevos'] and vinc['concepto'] == rule['concepto']
      and rule.get('calificador') and all(rule['calificador'].values()), rule['id'])
check('nac18.precedente-r3a7', 'r3a7-nac-resideextranjero-codigo' in
      [r['id'] for r in sem['reglas_descripcion_exacta']], 'separacion documentada')
dec = {c['columna']: c for c in d['decisiones_columnas']}[COL]
check('nac18.decision', dec['decision'] == 'proponer' and dec['definicion_iri'] == PIN, dec['decision'])
check('nac18.no-solape', COL not in {c['columna'] for c in sem['vinculos_documentales_revisados']}, 'nueva')

result['dictamenes'] += [
    {'tipo': 'reglas', 'id': rule['id'], 'dictamen': 'aceptar',
     'motivo': 'Fila /18 literal exacta (nombre, descripcion, Texto, ejemplo NO), huella RAW verificada, '
               'definicion unica, concepto nuevo limitado a lo documentado; no unifica con /17 por '
               'contradiccion de tipo (Texto vs Numerico entero) y descripciones distintas, con precedente r3a7.',
     'evidencia': ['data/portal/inspecciones/22202305-2d02-4c49-b216-cc98224357f0.json fila 18 huella 3c0156d2',
                   'r3a7-nac-resideextranjero-codigo vigente en ontologia/semantica.json',
                   'definicion https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F18']},
    {'tipo': 'vinculos', 'id': COL, 'dictamen': 'aceptar',
     'motivo': 'Columna fisica pos 18 hoja SINAC 2022 26-09-22 verificada + huella_esquema exacta; mismo conjunto; '
               'fila /18 exacta sin alias; concepto respaldado por regla literal nueva.',
     'evidencia': ['data/portal/contenido-inspeccion.json recurso 46977217 huella 9b46e1c0',
                   'huella_fila 3c0156d2 recomputada de RAW', 'definicion ' + PIN]},
]

# 3. Presas: huellas + fuente fisica + pendiente fundado
e = load(STAGE / 'presas/entrega.json')
rt = next(x for x in ins['recursos'] if x['id'] == '4219d141-5084-4308-bda3-d44ca28a4f53')
tp = next(t for t in rt['tablas'] if t['hoja'] == 'cat_estatal')
check('presas.fisica', tp['campos'][0] == {'id': 'Clave', 'posicion_original': 1}
      and sum(c['id'] == 'Clave' for c in tp['campos']) == 1
      and H(tp) == '29af60e8a6e9e2026623388d9e06cddb2689bfd25de8db395ab97bf7e47eecfd', 'pos1 Clave unica')
rp = load(ROOT / 'data/portal/inspecciones/bfb8788b-8ce3-475e-8bbd-dd1c5154c877.json')
check('presas.filas', H(rp['definiciones'][0]) == '87295257ea33a0a7d02963306433c01568b34189c09aa867351ac9f19faee0e4'
      and H(rp['definiciones'][3]) == 'd120834445f43d0bb67d135c256e73c91984a2fad6ec8ddbc5639c023dd44153'
      and rp['definiciones'][0].get('hoja') == 'Histórico_presas'
      and rp['definiciones'][3].get('hoja') == 'Catálogo_estatal', 'f1 vs f4')
for n, rl in [('1', 'r3a10-0363'), ('4', 'r3a10-0365')]:
    k = f'https://example.org/mex-ontologi/definition/bfb8788b-8ce3-475e-8bbd-dd1c5154c877%2F{n}'
    v = vars_by_iri[k]
    check(f'presas.def{n}', v['estado'] == 'respaldada_por_definicion' and v['regla'] == rl, v.get('regla'))
check('presas.pendiente', e['conteos']['pendiente'] == 1 and e['conteos']['proponer'] == 0
      and e['decisiones_columnas'][0]['decision'] == 'pendiente', 'no se fuerza por nombre')
result['dictamenes'].append(
    {'tipo': 'pendientes', 'id': 'https://example.org/mex-ontologi/file-column/4219d141-5084-4308-bda3-d44ca28a4f53%2Fcat_estatal%2F1',
     'dictamen': 'aceptar',
     'motivo': 'Se acepta mantener pendiente: dos filas Clave respaldadas con distinta hoja/descripcion; hoja fisica '
               'sin correspondencia exacta; dominio compartido no verificable (sin recurso Historico_presas ni datastore). '
               'Elegir /1 o /4 seria aprobar por nombre.',
     'evidencia': ['huella_esquema 29af60e8 re-verificada', 'huellas f1 87295257 / f4 d1208344 re-verificadas',
                   '2 correspondencias ambigua_por_nombre vigentes en cobertura']})

# 4. Cierres: epidemiologia key + presas control stale (corregir, procedural)
li_epi = load(STAGE / 'epidemiologia/listo.json')
if 'sha256_entrega' not in li_epi:
    result['dictamenes'].append(
        {'tipo': 'cierre', 'id': 'epidemiologia/listo.json', 'dictamen': 'corregir',
         'motivo': 'Contenido SHA coincide (5145bbe2) pero la clave es sha256_entrega_json en vez de sha256_entrega; '
                   'el verificador de control no la reconoce. Renombrar clave, sin tocar entrega.',
         'evidencia': ['listo.json key sha256_entrega_json', 'control.json error registrado']})

(ME / 'entrega.json').write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('checks:', len(result['checks']), 'dictamenes:', len(result['dictamenes']))
print('sha entrega-b:', sha(ME / 'entrega.json'))
