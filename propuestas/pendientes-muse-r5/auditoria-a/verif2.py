import json
for f in ['defunciones', 'epidemiologia', 'diversos']:
    d = json.load(open(f'propuestas/pendientes-muse-r5/{f}/entrega.json', encoding='utf-8'))
    print('=' * 25, f)
    print(' FUENTES:', json.dumps(d.get('fuentes', []), ensure_ascii=False)[:2500])
    print()
    sq = d.get('solicitudes_investigacion', d.get('solicitudes_web', []))
    if isinstance(sq, list):
        print(' SOLICITUDES n=', len(sq))
        for s in sq[:4]:
            print('  -', json.dumps(s, ensure_ascii=False)[:350])
    elif isinstance(sq, str):
        print(' SOLICITUDES ref:', sq)
    print()
