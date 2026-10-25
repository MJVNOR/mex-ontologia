import json
for f in ['defunciones', 'epidemiologia', 'diversos']:
    d = json.load(open(f'propuestas/pendientes-muse-r5/{f}/entrega.json', encoding='utf-8'))
    print('=' * 30, f)
    for s in d['decisiones_significados']:
        print(' -', str(s.get('definicion_iri', ''))[-52:])
        print('   dec:', s.get('decision'), '| motivo:', str(s.get('motivo'))[:320])
    print('  total:', len(d['decisiones_significados']))
    if f == 'diversos':
        print('  COLUMNAS:', json.dumps(d['decisiones_columnas'], ensure_ascii=False)[:2000])
        print('  PENDIENTES:', json.dumps(d['pendientes'], ensure_ascii=False)[:2000])
        print('  VERIF:', json.dumps(d.get('verificacion', {}), ensure_ascii=False)[:1500])
