"""Paso 1 lote-2: vuelca contexto de definiciones no-agricolas a JSON ascii-safe."""
import io, json

d = json.load(io.open('propuestas/pendientes-muse-r4/lote-2/asignacion.json', encoding='utf-8'))
ctx = {x['definicion_iri']: x for x in d['definiciones_contexto']}
seen = {}
for col in d['columnas']:
    di = col['definiciones_por_nombre'][0]
    x = ctx[di]
    if 'Agricultura' in x['titulo_conjunto']:
        continue
    if di not in seen:
        seen[di] = {
            'titulo_conjunto': x['titulo_conjunto'],
            'diccionario': x['diccionario'],
            'variable': x['variable'],
            'descripcion': x['descripcion'],
            'estado': x['estado'],
            'concepto': x.get('concepto'),
            'regla': x.get('regla'),
            'representacion': x.get('representacion'),
            'limites': x.get('limites'),
            'catalogo_declarado': x.get('catalogo_declarado'),
            'huella_fila_diccionario': x.get('huella_fila_diccionario'),
            'definicion_iri': x['definicion_iri'],
            'fuente_revision': x.get('fuente_revision'),
        }
out = sorted(seen.values(), key=lambda z: (z['titulo_conjunto'], z['variable']))
io.open('propuestas/pendientes-muse-r4/lote-2/_ctx_noagri.json', 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=1) + '\n')
print('defs no-agricolas distintas:', len(out))
