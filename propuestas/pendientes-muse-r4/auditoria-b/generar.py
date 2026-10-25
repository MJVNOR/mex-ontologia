"""Genera entrega.json / resultado.md / listo.json de auditoria-b (solo escribe en auditoria-b)."""
import hashlib, json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / 'propuestas/pendientes-muse-r4'
ME = STAGE / 'auditoria-b'
sys.path.insert(0, str(ROOT / 'scripts'))
from consolidar_semantica import columnas
from integrar_contenido import clave

def H(v):
    return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))

inv = load(ROOT / 'data/portal/inventario.json')
ins = load(ROOT / 'data/portal/contenido-inspeccion.json')
base_cov = load(STAGE / 'fuentes/data/semantica/cobertura.json')
base_sem = load(STAGE / 'fuentes/ontologia/semantica.json')
cols = {c['iri']: c for c in columnas(inv, ins, 'https://example.org/mex-ontologi/')}
vars_by_iri = {v['definicion_iri']: v for v in base_cov['variables'] if v.get('definicion_iri')}
raw_cache = {}
def raw_row(dic, n):
    if dic not in raw_cache:
        raw_cache[dic] = load(ROOT / f'data/portal/inspecciones/{dic}.json')['definiciones']
    return raw_cache[dic][n - 1]

merged_conc = dict(base_sem['conceptos'])
all_rules = {}
deliveries = {}
for l in [f'lote-{i}' for i in range(1, 7)] + ['ambiguedades']:
    d = load(STAGE / l / 'entrega.json')
    deliveries[l] = d
    for k, v in d.get('conceptos_nuevos', {}).items(): merged_conc[k] = v
    for r in d.get('reglas', []): all_rules[r['id']] = (l, r)
audit_a = load(STAGE / 'auditoria-a/entrega.json')
a_verdict = {r['id']: (r['dictamen'], str(r.get('motivo', ''))[:220]) for r in audit_a.get('dictamenes', [])}
supported = {v['definicion_iri'] for v in base_cov['variables']
             if v['estado'] == 'respaldada_por_definicion'}
supported.update(d for _, r in all_rules.values() for d in r['definiciones'])
prev_cols = {c['columna'] for c in base_sem['vinculos_documentales_revisados']}

dictamenes = []
rechazos = []
for l in [f'lote-{i}' for i in range(1, 7)] + ['ambiguedades']:
    d = deliveries[l]
    dec = {r['columna']: r for r in d.get('decisiones_columnas', [])}
    for v in d.get('vinculos', []):
        col_iri = v['columna']
        errs = []
        c = cols.get(col_iri)
        if c is None: errs.append('IRI fisica inexistente en inventario+inspeccion')
        else:
            if v.get('recurso') != c['recurso']: errs.append('recurso distinto del fisico')
            if v.get('campo') != c['campo']: errs.append('campo distinto del fisico')
            if v.get('huella_esquema') != c['huella_esquema']: errs.append('huella_esquema distinta')
        prop = dec.get(col_iri)
        if prop is None: errs.append('sin decision de columna')
        elif prop.get('decision') != 'proponer': errs.append('decision no proponer')
        pin = (prop or {}).get('definicion_iri') or v.get('definicion_iri')
        if not pin: errs.append('sin definicion_iri')
        vv = vars_by_iri.get(pin) if pin else None
        if pin and vv is None: errs.append('definicion_iri sin variable en cobertura: ' + str(pin))
        dep_rule = None
        if vv is not None:
            for a in ('diccionario', 'descripcion', 'huella_fila_diccionario'):
                if v.get(a) != vv[a]: errs.append(f'{a} distinto de la fila base')
            if c is not None and c['conjunto'] != vv['conjunto']: errs.append('conjunto fisico vs diccionario distinto')
            try:
                n = int(pin.split('%2F')[-1])
                if H(raw_row(vv['diccionario'], n)) != vv['huella_fila_diccionario']:
                    errs.append('huella base no reproduce fila RAW')
            except Exception as e: errs.append('raw: ' + repr(e))
            if v.get('concepto') != vv.get('concepto'):
                ok = [r for _, r in all_rules.values()
                      if pin in r.get('definiciones', []) and r.get('concepto') == v.get('concepto')
                      and r.get('nombres') == [vv['variable']] and r.get('descripciones') == [vv['descripcion']]]
                dep_rule = None
                dep_verdict = None
                for (_l, r) in all_rules.values():
                    if pin in r.get('definiciones', []) and r.get('concepto') == v.get('concepto'):
                        dep_rule = r['id']
                        dep_verdict = a_verdict.get(r['id'], ('SIN-DICTAMEN-A', ''))[0]
                if dep_rule and dep_verdict == 'aceptar':
                    pass  # respaldo semantico aceptado por auditoria-a vigente
                elif dep_rule and dep_verdict == 'condicionado':
                    errs.append('regla ' + dep_rule + ' condicionada por auditoria-a: '
                                + a_verdict[dep_rule][1])
                elif dep_rule:
                    errs.append('regla ' + dep_rule + ' sin aceptacion de auditoria-a '
                                '(veredicto: ' + str(dep_verdict) + ')')
                elif not ok:
                    errs.append('concepto sin respaldo ni regla nueva literal')
            if v.get('concepto') not in merged_conc: errs.append('concepto ausente en nucleo+propuestos')
            if not v.get('criterio'): errs.append('sin criterio')
            if col_iri in prev_cols: errs.append('solapa base 865')
        dep_txt = ''
        if dep_rule:
            dep_txt = (f" Soporte semantico regla {dep_rule}, veredicto auditoria-a vigente: {dep_verdict}."
                       + (" Dependencia explicita fiebre /1: sin aceptacion queda sin efecto; no se recurre a /177 ni /178."
                          if dep_rule == 'r4-lote-1-001' else ""))
        if errs:
            rechazos.append((l, col_iri, errs))
            dictamenes.append({'tipo': 'vinculos', 'id': col_iri, 'dictamen': 'rechazar',
                               'motivo': ' | '.join(errs),
                               'evidencia': [f'recurso {v.get("recurso")} campo {v.get("campo")}',
                                             f'definicion_iri {pin}']})
        else:
            ev = [f"data/portal/contenido-inspeccion.json recurso {v.get('recurso')} campo {v.get('campo')} "
                  f"huella_esquema={v.get('huella_esquema')}",
                  f"data/portal/inspecciones/{v.get('diccionario')}.json fila {pin.split('%2F')[-1] if pin else '?'} "
                  f"huella_fila={v.get('huella_fila_diccionario')} descripcion exacta verificada",
                  f"cobertura: conjunto {vv['conjunto']} concepto {v.get('concepto')} "
                  f"{'respaldado' if vv.get('estado')=='respaldada_por_definicion' else 'regla nueva literal '+ (dep_rule or '')}",
                  f"definicion {pin}"]
            dictamenes.append({'tipo': 'vinculos', 'id': col_iri, 'dictamen': 'aceptar',
                               'motivo': (f"Columna fisica + fila exacta + conjunto verificados; concepto "
                                          f"{v.get('concepto')} respaldado o con regla literal." + dep_txt),
                               'evidencia': ev})

sha_entregas = {l: sha(STAGE / l / 'entrega.json') for l in [f'lote-{i}' for i in range(1, 7)]}
sha_entregas['ambiguedades'] = load(STAGE / 'ambiguedades/listo.json').get('sha256_entrega') or \
    load(STAGE / 'ambiguedades/listo.json')['sha256']
code_files = ['codigo/scripts/consolidar_semantica.py', 'codigo/scripts/integrar_ronda_3.py',
              'codigo/scripts/integrar_ronda_4.py',
              'codigo/tests/test_cobertura_integrada.py', 'codigo/tests/test_ronda_3_integrada.py',
              'codigo/tests/test_ronda_4.py', 'codigo/tests/test_seleccion_documental.py',
              'comprobar.py', 'fijar_aceptaciones.py', 'instalar.py', 'verificar_studio.py']
sha_codigo = {f: sha(STAGE / 'integrador' / f) for f in code_files}

hallazgos = [
    {'archivo': 'reentregas finales lote-2/3/4/6 + ambiguedades/listo', 'bloquea': False,
     'detalle': 'Revalidadas entregas finales (lote-2 a46c804d, lote-3 c3aa6560, lote-4 81ca942e, lote-6 1d6653bc; '
                'lote-1/5/ambiguedades sin cambios) con marcadores SHA coincidentes. 3601 vinculos (673 decisiones '
                'lote-4 con 4 pendientes: Total_Egresos + P36/P39/P40 retirados por reglas 025/026/027 contradictorias), '
                '172 reglas. Dictamenes regenerados por IDs exactos vigentes; retirados eliminados.'},
    {'archivo': 'auditoria-a/entrega.json (172 aceptar, estado completo-reentregas-finales)', 'bloquea': False,
     'detalle': 'Dependencia semantica resuelta: r4-lote-1-001 aceptada (fiebre /1 sin condicion pendiente); '
                'tiempo-9/10/11 corregidas y aceptadas; 025/026/027 retiradas (sin exigir su inclusion); '
                'sha_entregas de A coinciden con entregas finales. Sin propuestas rechazadas vigentes.'},
    {'archivo': 'integrador/codigo/tests/*', 'bloquea': False,
     'detalle': '10/10 pruebas autocontenidas OK (test_ronda_4 6 + test_seleccion_documental 4) con path scripts; '
                'test_ronda_3_integrada/test_cobertura_integrada del codigo agregan ramas r4 aditivas sin rehashear '
                'historicos (865 y 29 fijos, conteos 865+adiciones). Sin ejecucion Studio.'},
    {'archivo': 'integrador/fijar_aceptaciones.py (SHA actual)', 'bloquea': False,
     'detalle': 'Whitelist de chat ampliada con ensayo-gemma4 y ensayo-gemini31 mas antes-cambio-modelo (14 nombres '
                'publicos). Exclusion total de secretos verificada: barrido de chat/ sin .env/claves/tokens/pem; los '
                '3 directorios whitelisteados solo contienen evaluacion.json y respuestas-saneadas.json. Nota: el '
                'ignore por nombre deja esos subdirectorios copiados vacios (su contenido no esta en la whitelist); '
                'conservador, no arrastra secretos ni rompe manifiesto. Guardas de bloqueo/cobertura exacta/cobertura '
                'de codigo sin cambios.'},
    {'archivo': 'integrador/instalar.py (SHA actual, sys.path codigo/scripts primero)', 'bloquea': False,
     'detalle': 'sys.path.insert(0, codigo/scripts) tras root/scripts deja [codigo, scripts]: construir resuelve al '
                'generador PREPARADO (PIN definition_pin verificado en fuente staged; ausente en live, que rechaza '
                'PIN). construir_catalogo solo existe en scripts/ (sin sombreado) y ROOT=Path(__file__).parents[1] '
                'absoluto: ROOT real preservado, verificado por importacion con el mismo orden (consolidar staged + '
                'ROOT==repo). Linea 79 duplica el insert (idempotente). instalar.py no ejecutado: nucleo y evidencia '
                'fijada intactos.'},
]
if rechazos:
    hallazgos.append({'archivo': 'vinculos no aceptados', 'bloquea': False,
                      'detalle': f'{len(rechazos)} vinculos sin aceptar (no se exige su inclusion; fijar solo instala aceptar): ' + str(rechazos[:10])})

entrega = {'auditor': 'auditoria-b', 'alcance': 'vinculos',
           'sha_entregas': sha_entregas, 'sha_codigo': sha_codigo,
           'dictamenes': dictamenes, 'hallazgos_codigo': hallazgos,
           'resumen': {'vinculos_auditados': len(dictamenes),
                       'aceptar': sum(1 for x in dictamenes if x['dictamen'] == 'aceptar'),
                       'condicionado': sum(1 for x in dictamenes if x['dictamen'] == 'condicionado'),
                       'rechazar': sum(1 for x in dictamenes if x['dictamen'] == 'rechazar'),
                       'dependencia_explicita_fiebre': 3},
           'observaciones_recalculadas': {
               'egresos-descripcion-urgencias': 'pendiente vigente (Total_Egresos candidata, variable fuera_del_nucleo)',
               'municipio-formato-ejemplo': 'significado resuelto (CVE_MUN documental_revisada municipio); pendiente solo composicion nnn vs 26048',
               'fecha-ejemplo-numerico': 'significado resuelto (Fecha documental_revisada fecha-precipitacion); pendiente solo codificacion DD/MM/AAAA vs 45658',
               'anio-nacimientos-2024': 'pendiente vigente (campo datastore sin vinculo; equivale a variable anio sin confirmar)',
               'anio-divorcios-2023': 'nota historica; alias anio_registro->anio-registro ya documental_revisada; sin peticion nueva'},
           'metodo': 'auditar.py en auditoria-b: IRI fisica, recurso/hoja/posicion, huella_esquema, diccionario mismo conjunto, '
                     'descripcion+huella_fila recomputada desde RAW, concepto en nucleo+propuestos o regla literal exacta, '
                     'ausencia de alias globales, no solape base 865, criterio presente; comprobar.py ejecutado una vez '
                     '(salida restaurada) y controles leidos sin edicion.'}
(ME / 'entrega.json').write_text(json.dumps(entrega, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('dictamenes', len(dictamenes), 'rechazos', len(rechazos))
print('sha entrega-b:', sha(ME / 'entrega.json'))
