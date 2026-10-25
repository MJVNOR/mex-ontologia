# -*- coding: utf-8 -*-
"""Vuelca la inspeccion de las 126 definiciones asignadas para lectura humana."""
import json

from pathlib import Path
BASE = Path(__file__).resolve().parent.parent
rows = json.load(open(BASE / 'fuente/inspeccion-126.json', encoding='utf-8'))
cur = None
for r in rows:
    key = (r['titulo'], r['dic'][:8])
    if key != cur:
        cur = key
        print('=' * 100)
        print(key[0], '| dic', key[1], '| notas:', (r['notas_conjunto'] or '')[:220].replace('\n', ' '))
        print('  grupos:', r['grupos'])
    n = r['iri'].split('%2F')[1]
    print('  [%s] var=%s | desc=%s | tipo=%s unidad=%s ej=%s cat=%s nulos=%s' % (
        n, r['var'], r['desc'], r['tipo'], r['unidad'], r['ejemplo'], r['catalogo'], r['nulos']))
