import json, re
e = json.load(open('propuestas/investigacion-post-r6/tic/entrega.json', encoding='utf-8'))
pat = re.compile(r'manos del publicador|Solo el publicador|exclusiv', re.I)
cita = re.compile(r'Cita historica R5/R6 \(texto heredado, no afirmacion propia\): ".*?" Conclusion actual', re.S)
proPIO = re.compile(r'manos del publicador|Solo el publicador', re.I)
bad = []
for d in e['decisiones']:
    resto = cita.sub('', d['evidencia_faltante'])
    if proPIO.search(resto):
        bad.append((d['definicion_iri'], resto))
print('json fuera de cita:', bad)
m = open('propuestas/investigacion-post-r6/tic/entrega.md', encoding='utf-8').read()
m2 = cita.sub('', m)
print('md fuera de cita:', proPIO.findall(m2))
mot = [d['definicion_iri'] for d in e['decisiones'] if pat.search(d['motivo'])]
print('motivo con exclusividad:', mot)
