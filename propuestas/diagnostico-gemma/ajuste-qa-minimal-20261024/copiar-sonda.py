from pathlib import Path
src = Path('propuestas/pendientes-muse-r6/probar-bundle-instalado.mjs').read_text(encoding='utf-8')
old = "const OUT=ROOT+'/propuestas/pendientes-muse-r6/prueba-bundle';"
new = "const OUT=ROOT+'/propuestas/diagnostico-gemma/ajuste-qa-minimal-20261024/sonda-instalada-c6';"
assert old in src, 'OUT no encontrado'
Path('propuestas/diagnostico-gemma/ajuste-qa-minimal-20261024/sonda-instalada-c6.mjs').write_text(
    src.replace(old, new), encoding='utf-8')
print('copia sonda OK (unico cambio: OUT)')
