import json
# pendientes vs reglas: any pendiente definicion that now has a regla?
for lote in ['lote-1','lote-2','lote-3','lote-4','lote-5','lote-6']:
    d = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/entrega.json', encoding='utf-8'))
    reglas_defs = set()
    for r in d['reglas']:
        for dd in r.get('definiciones', []):
            reglas_defs.add(dd)
    sig = d.get('decisiones_significados', [])
    pend_s = [x for x in sig if x.get('decision')=='pendiente']
    prop_s = [x for x in sig if x.get('decision')=='proponer']
    print(f"== {lote} sig_total={len(sig)} proponer={len(prop_s)} pendiente={len(pend_s)} reglas={len(d['reglas'])}")
    # check pendientes that have regla
    for p in pend_s:
        iri = p.get('definicion_iri')
        if iri in reglas_defs:
            print(f"  PEND-CON-REGLA !!! {iri} motivo={str(p.get('motivo'))[:150]!r}")
    # check proponer without regla
    for p in prop_s:
        iri = p.get('definicion_iri')
        if iri not in reglas_defs:
            # may reuse existing rule; check motivo mentions rule
            print(f"  PROP-SIN-REGLA-NUEVA {iri} motivo={str(p.get('motivo'))[:160]!r}")
    pj = json.load(open(f'propuestas/pendientes-muse-r4/{lote}/pendientes.json', encoding='utf-8'))
    print(f"  pendientes.json keys: {list(pj.keys()) if isinstance(pj,dict) else type(pj)}")
