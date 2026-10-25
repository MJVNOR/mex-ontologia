import hashlib, json
from pathlib import Path
BASE = Path('propuestas/pendientes-muse-r6/catalogos/codigo')
files = ['scripts/integrar_ronda_5.py', 'scripts/integrar_ronda_6.py',
         'scripts/consolidar_semantica.py', 'tests/test_ronda_6.py']
shas = {f: hashlib.sha256((BASE / f).read_bytes()).hexdigest() for f in files}
for f, h in shas.items():
    print(f, h)

entrega = {
    'rol': 'auditoria-documental',
    'alcance': 'Solo staging catalogos/codigo (4 archivos). Central y manifiestos previos intactos.',
    'defecto_confirmado': 'integrar_ronda_5.validar_sobre_base delegaba a R6 ANTES de verificar exactitud/duplicados/aprobaciones R5: con config R6 presente, un payload R5 duplicado o sin aprobacion saltaba sus propios controles.',
    'correccion_staging': 'Reordenadas las validaciones historicas R5 (exactitud, duplicados, aprobaciones) antes de la delegacion a R6; delegacion intacta despues. Solo copia staging; central sin delegacion R6, intacto.',
    'consolidar_semantica': 'Diff staging-vs-central de 11 lineas: solo hook R6 (construir integra R6 si existe config). Sin cambios.',
    'tests': '12/12 OK offline (9 previos + 3 nuevos Ronda5ConConfigR6Test: duplicados, sin-aprobacion y delegacion-tras-chequeos con config R6 presente). Tests nuevos fallan contra codigo defectuoso (verificado).',
    'dictamen': 'aprobar-staging',
    'condicion': 'Root instala; la integracion del +1 pin requiere ademas el segundo auditor (dictamen-presas.json ya emitido por esta auditoria: aceptar pin /4). Sin reglas/conceptos nuevos; <=1 link exacto adenda (vinculo_propuesto).',
    'sha_archivos': shas,
}
json.dump(entrega, open('propuestas/pendientes-muse-r6/auditoria-documental/dictamen-codigo-r6.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

lj = json.load(open(BASE / 'listo-codigo.json', encoding='utf-8'))
lj['archivos_sha256'] = shas
lj['pruebas'] = {'test_ronda_6': '12/12 OK offline (9 previos + 3 Ronda5ConConfigR6Test con config R6 presente)',
                 'auditoria_r5_rechazada_con_configR6': 'OK (duplicados y sin-aprobacion fallan antes de delegar)'}
lj['revisiones'] = {'auditoria-documental': 'defecto R5-delegacion confirmado y corregido en staging; dictamen-codigo-r6.json'}
lj['central_modificado'] = False
lj['manifiestos_previos_modificados'] = 0
json.dump(lj, open(BASE / 'listo-codigo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dictamen + marker actualizados')
