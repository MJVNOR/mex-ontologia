import csv
p = 'propuestas/agente-1-catalogos/fuentes/5494daa1-09ca-4750-aeac-2558553700e1_33d0a99e-c721-496f-a05e-07646e9ae42a_Diccionario.bin'
with open(p, 'r', encoding='utf-8-sig', newline='') as f:
    rd = list(csv.reader(f))
print('total lineas inc hdr:', len(rd))
hdr = rd[0]
print('hdr[0:10]:', hdr[:10])
for i in (7, 8, 129, 130, 162, 163, 168, 169, 177, 178):
    # rd[0]=hdr, rd[1]=fila1 ... rd[177]=fila177
    if i < len(rd):
        print(f'--- linea csv {i} (fila datos {i}):')
        print('  nombrevar:', repr(rd[i][0]), '| desc:', repr(rd[i][4])[:100], '| identif:', repr(rd[i][5]), '| catref:', repr(rd[i][6]), '| detalle:', repr(rd[i][7]), '| ej:', repr(rd[i][9])[:60])
# ultimas 3 lineas completas
with open('propuestas/agente-1-catalogos/cola_fiebre.txt', 'w', encoding='utf-8') as f:
    for i in range(175, 179):
        f.write(f'linea {i}: ' + '|'.join(rd[i][:12]) + '\n')
print('ok')
