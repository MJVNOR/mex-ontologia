import json
sem = json.load(open('ontologia/semantica.json', encoding='utf-8'))
nucleo = set(sem['conceptos'].keys())
tot_new = 0
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    cn = d.get('conceptos_nuevos', {})
    tot_new += len(cn)
    bad = 0
    for k, v in cn.items():
        if not (isinstance(v, list) and len(v) == 3 and all(isinstance(x, (str, type(None))) for x in v)):
            print(f'BAD-FORMAT {lote} {k} {str(v)[:120]!r}')
            bad += 1
        if v[2] is not None and v[2] not in nucleo and v[2] not in cn:
            print(f'BAD-PARENT {lote} {k} padre={v[2]!r}')
            bad += 1
        if k in nucleo:
            print(f'DUP-NUCLEO {lote} {k}')
            bad += 1
    print(f'{lote}: conceptos_nuevos={len(cn)} problemas={bad}')
    # conceptos usados en reglas vs nuevos vs nucleo
    for r in d['reglas']:
        c = r.get('concepto')
        if c not in nucleo and c not in cn:
            print(f'  CONC-SIN-DEF {lote} {r["id"]} conc={c}')
print('total nuevos:', tot_new)
