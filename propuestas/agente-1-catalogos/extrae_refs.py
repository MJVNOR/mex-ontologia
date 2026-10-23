import json, re
ttl = open('data/semantica/interpretaciones.ttl', encoding='utf-8').read()
chunks = ttl.split('<https://example.org/mex-ontologi/declared-code-reference/')
refs = []
for ch in chunks[1:]:
    iri = 'https://example.org/mex-ontologi/declared-code-reference/' + ch.split('>', 1)[0]
    block = ch.split('\n\n', 1)[0]
    if 'solo_referencia_declarada_sin_resolver' not in block:
        continue
    m_label = re.search(r'rdfs:label\s+"(.*?)"@es', block, re.DOTALL)
    m_nombre = re.search(r'mex:nombreCatalogoDeclarado\s+"(.*?)"\s*\.', block, re.DOTALL)
    # todas las derivaciones definition/... dentro del bloque (incluye segundas tras coma)
    derivs = re.findall(r'<(https://example\.org/mex-ontologi/definition/[^>]+)>', block)
    # dedup manteniendo orden
    seen, uniq = set(), []
    for d in derivs:
        if d not in seen:
            seen.add(d); uniq.append(d)
    refs.append({'referencia_iri': iri, 'id': iri.rsplit('/', 1)[-1],
                 'label': m_label.group(1) if m_label else '',
                 'derivaciones': uniq,
                 'nombre_catalogo': m_nombre.group(1) if m_nombre else ''})
cob = json.load(open('data/semantica/cobertura.json', encoding='utf-8'))
by_def = {v.get('definicion_iri'): v for v in cob.get('variables', []) if v.get('definicion_iri')}
out = []
for r in refs:
    out.append({**r, 'evidencias_variables': [
        {'definicion_iri': d, 'variable': by_def.get(d)} for d in r['derivaciones']]})
json.dump(out, open('propuestas/agente-1-catalogos/fase1_refs.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
for r in out:
    print(r['id'], '|', r['nombre_catalogo'][:80], '| derivs:', len(r['derivaciones']))
    for e in r['evidencias_variables']:
        v = e['variable']
        print('  ', e['definicion_iri'].split('%2F')[-1], '->',
              (v.get('variable') if v else None), '|', (v.get('descripcion') if v else None),
              '| huella:', (v.get('huella_fila_diccionario') if v else None))
