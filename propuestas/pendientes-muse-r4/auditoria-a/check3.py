import json
for lote in ['lote-4','lote-2','lote-5','lote-3','lote-6','lote-1']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    print('====', lote)
    for r in d['reglas']:
        lim = r.get('limites', r.get('limite', ''))
        print(f" {r['id']} conc={r.get('concepto')} rep={r.get('representacion')}")
        print(f"   lim: {str(lim)[:400]}")
        print(f"   crit: {str(r.get('criterio'))[:200]}")
