"""Paso 2 lote-2: inspecciona reglas existentes reutilizadas."""
import io
import json

sem = json.load(io.open('C:/Users/marti/Documents/MEX-Ontologi/propuestas/pendientes-muse-r4/fuentes/ontologia/semantica.json', encoding='utf-8'))
rules = {r['id']: r for r in sem['reglas_descripcion_exacta']}
asig = json.load(io.open('C:/Users/marti/Documents/MEX-Ontologi/propuestas/pendientes-muse-r4/lote-2/asignacion.json', encoding='utf-8'))
ctx = {x['definicion_iri']: x for x in asig['definiciones_contexto']}
need = sorted({ctx[c['definiciones_por_nombre'][0]]['regla'] for c in asig['columnas']})
print('reglas distintas reutilizadas:', len(need))
for rid in need:
    r = rules.get(rid)
    if r is None:
        print('FALTA REGLA:', rid)
        continue
    print('=' * 80)
    print(json.dumps(r, ensure_ascii=False, indent=1)[:1800])
