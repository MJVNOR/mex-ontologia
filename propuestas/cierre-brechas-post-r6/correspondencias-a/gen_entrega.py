import json, hashlib, datetime

BASE = 'propuestas/cierre-brechas-post-r6/correspondencias-a'
FECHA = '2026-10-24'

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

asig = json.load(open(f'{BASE}/asignacion.json', encoding='utf-8'))

# Verificacion estructural previa (nombre+posicion 1:1 en secuencia completa)
def full_align(rid, did):
    col = json.load(open(f'data/portal/inspecciones/{rid}.json', encoding='utf-8'))['tablas'][0]
    defs = json.load(open(f'data/portal/inspecciones/{did}.json', encoding='utf-8'))['definiciones']
    assert len(col['campos']) == len(defs), (rid, len(col['campos']), len(defs))
    exact = sum(1 for c in col['campos'] if c['id'] == defs[c['posicion_original'] - 1]['Nombre variable'])
    for c in col['campos']:
        assert c['id'].strip() == defs[c['posicion_original'] - 1]['Nombre variable'].strip(), c
    return len(col['campos']), col['hoja'], exact

N_SIN, HOJA_SIN, EX_SIN = full_align('46977217-9396-4f9c-bddb-6616e82530b4', '22202305-2d02-4c49-b216-cc98224357f0')
N_MAT, HOJA_MAT, EX_MAT = full_align('58f2d5a6-0432-48f1-8a35-a5efcce78bac', '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d')
N_DEN, HOJA_DEN, EX_DEN = full_align('5772b8ec-e272-4265-a757-f7ddd179fe04', '3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99')

GRP = {
    '46977217-9396-4f9c-bddb-6616e82530b4': dict(did='22202305-2d02-4c49-b216-cc98224357f0', ds='940de7d8-73ec-4a08-8d26-b7cc97ff17bd', pkg='evidencia/package_nacimientos_2026-10-24.json', nvar='106', per='2022-01-01 a 2022-09-26', n=N_SIN, hoja=HOJA_SIN, ex=EX_SIN),
    '58f2d5a6-0432-48f1-8a35-a5efcce78bac': dict(did='8c0e76ff-3a86-4b1d-beee-b04bebe7df8d', ds='e819466c-7282-46c5-84e9-65917dd8cc85', pkg='evidencia/package_matriculas_2026-10-24.json', nvar='70', per='2022-01-01 a 2022-06-01', n=N_MAT, hoja=HOJA_MAT, ex=EX_MAT),
    '5772b8ec-e272-4265-a757-f7ddd179fe04': dict(did='3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99', ds='c589afac-79f1-4aac-9ade-e949301bcca3', pkg='evidencia/package_denuncias_2026-10-24.json', nvar='9', per='2022-01-01 a 2022-03-31', n=N_DEN, hoja=HOJA_DEN, ex=EX_DEN),
}

INS = {}
for _did in ('22202305-2d02-4c49-b216-cc98224357f0', '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d', '3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99'):
    INS[_did] = json.load(open(f'data/portal/inspecciones/{_did}.json', encoding='utf-8'))['definiciones']

HUELLA = {
    '22202305-2d02-4c49-b216-cc98224357f0/83': '8acb1135cdd9dbc95750049533a5dacc41a05b4da37d6fe4ea9d19ea5b059a1d',
    '22202305-2d02-4c49-b216-cc98224357f0/102': '21c7fce4e834b211e513fcdc8b55a757dc5afc3da9e2b846db7aba776cfbfdf5',
    '22202305-2d02-4c49-b216-cc98224357f0/103': '305e3ccb01619f50cab0ded3a82e6211d21b4dcbebecd506e6911f6b489cf8f3',
    '22202305-2d02-4c49-b216-cc98224357f0/104': 'bda091e282317f0b810033ac9f31188dcecfe6208940a47fae73f4fb6ca85499',
    '22202305-2d02-4c49-b216-cc98224357f0/105': 'c77a7050ed8af0bf7ab37ca07a830539d720a02adb9c4722d417fcdcdabd4146',
    '3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99/2': '799f924f8f10e3831cebdb4fbbc233cb6965caae8902f799881277d12f24320d',
    '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d/14': '940c1f77837c39791ee0904bbe8123c69948da90bfc9965f38db9aacf6e680ec',
    '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d/20': 'ad458441825d75edce0abc7e0082d73b2e3fbc9ec36dbb1687451d73ff9d3eba',
    '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d/64': '6759b8b1157290027ece3602d7dff3c8609984dfbbf14c5408e656de0fe1b612',
    '8c0e76ff-3a86-4b1d-beee-b04bebe7df8d/66': 'e7e0a6b9c15be989bb0faca42c9b29e55a557cd16b0d417fbb4ba533330970d2',
}

HU = {}
for _k, _h in HUELLA.items():
    _did, _f = _k.rsplit('/', 1)
    _row = INS[_did][int(_f) - 1]
    HU[_k] = (_row['Nombre variable'], _h, _row['Descripci\u00f3n'])
    assert _row['Nombre variable'] == [c['campo'] for c in asig['casos'] if c['variable'].endswith('%2F' + _f) and c['recurso'] in GRP and GRP[c['recurso']]['did'] == _did][0], _k

decisiones = []
for caso in asig['casos']:
    col_iri = caso['columna']  # valor EXACTO campo clave_id
    rid = caso['recurso']
    g = GRP[rid]
    fila = col_iri.rsplit('%2F', 1)[1]
    key = f"{g['did']}/{fila}"
    var, huella, desc = HU[key]
    assert var == caso['campo'], (var, caso['campo'])
    ev_pkg = f"{BASE}/{g['pkg']}"
    ev_col = f"data/portal/inspecciones/{rid}.json"
    ev_def = f"data/portal/inspecciones/{g['did']}.json"
    decisiones.append({
        'id': col_iri,
        'estado': 'par_estructural_revisado_significado_pendiente',
        'original': caso,
        'motivo': ("Registro separado ESTRUCTURAL post-auditoria (dictamen requiere_correccion): par columna pos " + fila + " " + repr(var) + " <-> fila " + fila + " del diccionario " + g['did'] + " (huella " + huella + "), base: mismo conjunto CKAN " + g['ds'] + " (Diccionario pos 0 + datos pos 1, periodo " + g['per'] + ", numero_variables=" + g['nvar'] + ") + verificacion del ID (ver alineacion.json). Significado pendiente (descripcion " + repr(desc) + "); sin cambio de estatus semantico, sin concepto aprobado, sin joins/cruces, sin identidad de catalogos, sin vigencia del vinculo, sin promocion semantica. NO aplicable a vinculos_documentales_revisados (core exige respaldada_por_definicion)."),
        'evidencia_faltante': None,
        'evidencia': [
            {'ruta': ev_pkg, 'sha256': sha(ev_pkg), 'localizador': 'result.resources[0,1] (Diccionario pos 0 + datos pos 1) + result.numero_variables + resources[1].start_date/end_date', 'afirmacion_soportada': f"El publicador co-publica Diccionario y archivo de datos en el mismo conjunto, declara numero_variables={g['nvar']} y periodo {g['per']} del recurso de datos."},
            {'ruta': ev_col, 'sha256': sha(ev_col), 'localizador': f"tablas[0] hoja {g['hoja']!r}, campos[posicion_original={fila}]", 'afirmacion_soportada': f"Columna fisica pos {fila} de la hoja {g['hoja']!r} con nombre exacto {var!r}."},
            {'ruta': ev_def, 'sha256': sha(ev_def), 'localizador': f"definiciones[{int(fila) - 1}] (fila logica {fila}, variable {var!r})", 'afirmacion_soportada': f"Fila {fila} del diccionario con variable {var!r}, descripcion {desc!r}; mas coincidencia nominal+ordinal verificada en las {g['n']} posiciones (verificado por bytes: SINAC 106/106 y denuncias 9/9 exactas; matriculas 68/70 exactas + 2 con solo espacios del portal en filas ajenas a estos IDs)."},
        ],
        'propuesta': {'estado_propuesto': 'par_estructural_revisado_significado_pendiente', 'vinculo': f"columna {col_iri} documentada por fila {fila} del diccionario {g['did']} (huella {huella})", 'alcance': 'solo par estructural; concepto/significado y vigencia quedan pendientes y no se promueven', 'estado_semantico_actual': 'candidata_por_nombre', 'significado': 'pendiente', 'significado_pendiente': True, 'descripcion_fila': desc, 'huella_fila_diccionario': huella},
        'limites': ['Sin joins, cruces, homologaciones, equivalencias ni identidad de catalogos.', 'Sin nuevas vigencias: los periodos CKAN son metadato del recurso, no vigencia del vinculo.', 'Sin promocion semantica: el estatus de la correspondencia no cambia y no genera variable respaldada.', 'No fija edicion de manual, formato de valores, codebook ni fe de erratas.', 'La homonimia con manuales nacionales no se usa como respaldo; el par es estructural local (mismo conjunto + numero_variables + verificacion del ID).', 'NO aplicable a vinculos_documentales_revisados: el core exige respaldada_por_definicion.'],
    })

assert len(decisiones) == 10 and len({d['id'] for d in decisiones}) == 10

fuentes = []
seen = set()
for d in decisiones:
    for e in d['evidencia']:
        if e['ruta'] in seen:
            continue
        seen.add(e['ruta'])
        if e['ruta'].startswith(BASE):
            url = 'https://datos.sonora.gob.mx/api/3/action/package_show?id=' + GRP[[c['recurso'] for c in asig['casos'] if GRP[c['recurso']]['pkg'] in e['ruta']][0]]['ds']
            fuentes.append({'ruta': e['ruta'], 'sha256': e['sha256'], 'url': url, 'fecha_consulta': FECHA, 'localizador': e['localizador']})
        else:
            insp = json.load(open(e['ruta'], encoding='utf-8'))
            fuentes.append({'ruta': e['ruta'], 'sha256': e['sha256'], 'url': insp.get('fuente', ''), 'fecha_consulta': (insp.get('consultado_en_utc', '') or '')[:10], 'localizador': e['localizador']})

entrega = {
    'tarea': 'correspondencias-a',
    'tipo': 'correspondencias',
    'decisiones': decisiones,
    'fuentes': fuentes,
    'novedades_frente_a_investigacion_previa': ('package_show fresco 2026-10-24 de los 3 conjuntos con numero_variables declarado (106/70/9) + verificacion de alineacion nominal+ordinal 1:1 en secuencia completa (106/106 y 9/9 exactas; 68/70 exactas + 2 con solo espacios del portal en filas ajenas a estos IDs). R6/pendientes-depurados registraba recurso_de_datos como citado_sin_vinculo/no_acreditado; el conteo declarado por el publicador cierra ese hueco para el vinculo documental (no para el significado). Busquedas web nuevas (SINAC generico, UES matriculas) sin pista primaria adicional; portal CKAN como fuente primaria suficiente. Detalle fila por fila en alineacion.json (conteos reales verificados; matriculas con 2 diferencias solo-espacios fuera de los IDs). Auditoria (requiere_correccion) aplicada: registro separado estructural, sin concepto aprobado, sin promocion semantica; propuesta anterior en historial/ como rechazada.'),
    'busquedas_limitadas': ['websearch SINAC Sonora (resultados genericos nacionales, sin vinculo Sonora-local)', 'websearch UES matriculas titulacion (solo pagina del portal = misma fuente primaria)', 'CKAN package_show x3 via HTTPS 2026-10-24 (positivo; copias en evidencia/)', 'Navegador Obscura compartido no manejado por este agente (ver peticiones-web.json y web-obscura/disponibilidad.json)'],
    'auditoria': 'dictamen requiere_correccion aplicado: registro separado par_estructural_revisado_significado_pendiente; propuesta anterior propuesta_resolucion conservada solo en historial/ como rechazada, sin efecto.',
    'alineacion': None,
}

alineacion_pares = []
for _rid, _g in GRP.items():
    _col = json.load(open(f"data/portal/inspecciones/{_rid}.json", encoding='utf-8'))
    _dd = json.load(open(f"data/portal/inspecciones/{_g['did']}.json", encoding='utf-8'))
    _campos = _col['tablas'][0]['campos']
    _defs = _dd['definiciones']
    _filas = []
    _exact = 0
    _dif = []
    for _c in _campos:
        _v = _dd['definiciones'][_c['posicion_original'] - 1]['Nombre variable'] if _c['posicion_original'] <= len(_defs) else None
        _ok = (_c['id'] == _v)
        _exact += 1 if _ok else 0
        if not _ok:
            _dif.append({'posicion': _c['posicion_original'], 'campo_esquema': _c['id'], 'variable_diccionario': _v, 'coincide_normalizado': (_c['id'] or '').strip() == ((_v or '').strip())})
        _filas.append({'posicion': _c['posicion_original'], 'campo_esquema': _c['id'], 'variable_diccionario': _v, 'exacta': _ok})
    alineacion_pares.append({
        'recurso': _rid, 'hoja': _g['hoja'], 'diccionario': _g['did'], 'conjunto': _g['ds'],
        'conteo_columnas_esquema': len(_campos), 'conteo_filas_diccionario': len(_defs),
        'numero_variables_declarado': _g['nvar'], 'conteos_coinciden': (len(_campos) == len(_defs) == int(_g['nvar'])),
        'coincidencias_exactas': _exact, 'diferencias': _dif,
        'afirmacion_1_1': ('1:1 exacta' if not _dif else 'NO 1:1 exacta; ver diferencias (solo espacios del portal, fuera de los IDs asignados)' if all(d['coincide_normalizado'] for d in _dif) else 'MISMATCH REAL; no usar como 1:1'),
        'filas': _filas,
        'sha_fuentes_primarias': {'esquema': sha(f"data/portal/inspecciones/{_rid}.json"), 'diccionario': sha(f"data/portal/inspecciones/{_g['did']}.json"), 'package': sha(f"{BASE}/{_g['pkg']}")},
    })

al_out = json.dumps({'fecha_utc': FECHA, 'nota': 'Distribuciones y reportes derivados son CONTEXTO, no prueba directa del par; este artefacto solo contrasta esquema fisico vs fila de diccionario con SHA de fuentes primarias.', 'pares': alineacion_pares}, ensure_ascii=False, indent=1) + '\n'
open(f'{BASE}/alineacion.json', 'w', encoding='utf-8').write(al_out)
entrega['alineacion'] = {'ruta': f'{BASE}/alineacion.json', 'sha256': sha(f'{BASE}/alineacion.json')}

out = json.dumps(entrega, ensure_ascii=False, indent=1) + '\n'
open(f'{BASE}/entrega.json', 'w', encoding='utf-8').write(out)
json.load(open(f'{BASE}/entrega.json', encoding='utf-8'))
print('entrega.json OK', len(out), 'bytes; decisiones:', len(decisiones))
