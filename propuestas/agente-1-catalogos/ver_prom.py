import json
d = json.load(open('propuestas/agente-1-catalogos/exactos.json', encoding='utf-8'))
print(sorted(d['diccionarios'].keys()))
print(d['diccionarios']['403912fd-5853-4e18-8256-f77206f855bd']['fila'])
