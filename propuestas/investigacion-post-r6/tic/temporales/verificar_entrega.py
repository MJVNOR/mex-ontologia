import json, hashlib, pathlib
REPO = pathlib.Path(r'C:\Users\marti\Documents\MEX-Ontologi')
e = json.loads((REPO / 'propuestas/investigacion-post-r6/tic/entrega.json').read_bytes().decode('utf-8'))
assert e['grupo_fuente'] == 'tic'
assert len(e['decisiones']) == 24
req = ['definicion_iri', 'variable', 'descripcion_original', 'huella_fila_diccionario',
       'estado', 'significado_propuesto', 'evidencia', 'vinculo_fuente_local',
       'evidencia_faltante', 'motivo', 'limites']
for d in e['decisiones']:
    for k in req:
        assert k in d, (d.get('definicion_iri'), k)
    assert d['estado'] in ('propuesta_respaldada', 'sigue_pendiente'), d['estado']
    if d['estado'] == 'sigue_pendiente':
        assert d['significado_propuesto'] is None
        assert d['evidencia_faltante'] and d['motivo'] and d['limites']
    for ev in d['evidencia']:
        p = REPO / ev['ruta']
        assert p.is_file(), ev['ruta']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == ev['sha256'], ev['ruta']
        assert ev['localizador'] and ev['afirmacion_soportada']
for f in e['fuentes']:
    p = REPO / f['ruta']
    assert p.is_file(), f['ruta']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == f['sha256'], f['ruta']
    assert f['url'] and f['fecha_consulta'] and f['localizador']
# cruce con asignacion
pend = json.loads((REPO / 'propuestas/depuracion-post-r6/significados/pendientes.json').read_bytes().decode('utf-8'))
asig = {s['definicion_iri']: s for s in pend['significados'] if s.get('grupo_fuente') == 'tic'}
dec = {d['definicion_iri']: d for d in e['decisiones']}
assert set(asig) == set(dec), 'cobertura de IDs'
for iri, s in asig.items():
    d = dec[iri]
    assert d['variable'] == s['variable'] and d['descripcion_original'] == s['descripcion_original']
    assert d['huella_fila_diccionario'] == s['huella_fila_diccionario']
print('VERIFICACION OK: 24/24 decisiones, fuentes y evidencias con SHA valido, IDs exactos del grupo tic')
