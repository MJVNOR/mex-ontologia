import json, hashlib, pathlib
D = pathlib.Path('propuestas/cierre-brechas-post-r6/vigencias-uth-presas')
ent = json.loads((D / 'entrega.json').read_text(encoding='utf-8'))
assert ent['tarea'] == 'vigencias-uth-presas' and ent['tipo'] == 'vigencias'
ids = [d['id'] for d in ent['decisiones']]
assert ids == ['V01', 'V02', 'V03', 'V04', 'V05'], ids
assert len(set(ids)) == 5
for d in ent['decisiones']:
    assert d['estado'] in ('propuesta_resolucion', 'sigue_pendiente'), d['id']
    assert d['id'] == d['original']['id'], d['id']
    for e in d['evidencia']:
        assert set(e) >= {'ruta', 'sha256', 'localizador', 'afirmacion_soportada'}, (d['id'], e)
        r = e['ruta']
        if not r.startswith('local:'):
            p = pathlib.Path(r)
            if not p.is_absolute():
                p = pathlib.Path('.') / r
            assert p.exists(), r
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            assert h == e['sha256'], (d['id'], r, h, e['sha256'])
archivos = ['peticiones-web.json', 'busquedas-limitadas.json', 'entrega.json', 'entrega.md', 'build_entrega.py']
for f in sorted((D / 'evidencia').glob('*')):
    archivos.append('evidencia/' + f.name)
cierre = {'archivos': [{'ruta': 'propuestas/cierre-brechas-post-r6/vigencias-uth-presas/' + a,
                        'sha256': hashlib.sha256((D / a).read_bytes()).hexdigest()} for a in archivos],
          'conteos': {'decisiones': 5, 'sigue_pendiente': sum(1 for d in ent['decisiones'] if d['estado'] == 'sigue_pendiente'),
                      'propuesta_resolucion': sum(1 for d in ent['decisiones'] if d['estado'] == 'propuesta_resolucion')}}
(D / 'cierrelisto.json').write_text(json.dumps(cierre, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print(json.dumps(cierre['conteos'], ensure_ascii=False))
print('cierrelisto.json', hashlib.sha256((D / 'cierrelisto.json').read_bytes()).hexdigest())
