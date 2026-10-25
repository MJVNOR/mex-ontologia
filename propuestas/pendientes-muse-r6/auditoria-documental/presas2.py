import json, hashlib, sys
sys.path.insert(0, 'scripts')
from consolidar_semantica import huella
insp = {r['id']: r for r in json.load(open('data/portal/contenido-inspeccion.json', encoding='utf-8'))['recursos']}
tabla = insp['4219d141-5084-4308-bda3-d44ca28a4f53']['tablas'][0]
h_esc = huella(tabla)
print('huella_esquema recomputada:', h_esc)
print('adenda declara            : 29af60e8a6e9e2026623388d9e06cddb2689bfd25de8db395ab97bf7e47eecfd')
print('MATCH' if h_esc == '29af60e8a6e9e2026623388d9e06cddb2689bfd25de8db395ab97bf7e47eecfd' else 'DIFIERE')
row = insp['bfb8788b-8ce3-475e-8bbd-dd1c5154c877']['definiciones'][3]
h_fila = huella(row)
print('huella_fila/4 recomputada :', h_fila)
print('adenda declara            : d120834445f43d0bb67d135c256e73c91984a2fad6ec8ddbc5639c023dd44153')
print('MATCH' if h_fila == 'd120834445f43d0bb67d135c256e73c91984a2fad6ec8ddbc5639c023dd44153' else 'DIFIERE')
# cobertura: 15 correspondencias del recurso
cob = json.load(open('data/semantica/cobertura.json', encoding='utf-8'))
corr = [c for c in cob['correspondencias'] if '4219d141' in json.dumps(c)]
print('correspondencias recurso 4219d141:', len(corr))
from collections import Counter
print(Counter(str(c.get('estado', c.get('tipo', '?'))) for c in corr))
for c in corr:
    print(' -', str(c.get('estado', c.get('tipo'))), str(c.get('definicion_iri', c.get('definicion', '')))[-14:], str(c.get('descripcion', c.get('concepto', '')))[:60])
