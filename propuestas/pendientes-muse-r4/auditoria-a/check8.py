import json
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    pend = [x for x in d.get('decisiones_significados', []) if x.get('decision')=='pendiente']
    print(f"== {lote} pendientes_significados={len(pend)}")
    for p in pend[:4]:
        print(f"  {str(p.get('definicion_iri'))[-40:]} | {str(p.get('motivo'))[:220]!r}")
    print()
