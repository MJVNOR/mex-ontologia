"""Incluye resoluciones R7 exactas en la comprobación de dictámenes históricos R2."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-paralelo-brechas-sin-gemma/ejecucion-20261024-072207Z'
out=E/'integracion/compatibilidad-v004'
assert not out.exists()
out.mkdir()
shutil.copy2(ROOT/'scripts/integrar_entregas.py',out/'integrar_entregas.py')
code=(ROOT/'scripts/integrar_ronda_2.py').read_text(encoding='utf-8')
needle="    p2 = read('agente-2-pendientes')"
assert code.count(needle)==1
code=code.replace(needle,"""    if (ROOT / 'ontologia/revision-ronda-7.json').exists():
        # validar(rules) arriba comprueba la cadena exacta R4→R5→R6→R7.
        # Cada resolución posterior conserva el gate de estado, regla,
        # concepto y huella de fila de validar_estado_dictamen.
        from integrar_ronda_7 import cargar as cargar_r7_dictamenes
        _, _, _, aceptadas_r7_dictamenes, fuentes_r7_dictamenes = cargar_r7_dictamenes()
        sources.update(fuentes_r7_dictamenes)
        approved_later.update({d: r for r in aceptadas_r7_dictamenes['reglas'] for d in r['definiciones']})
"""+needle)
code=code.replace('por una regla auditada de ronda 4. ','por una regla auditada posterior. ')
(out/'integrar_ronda_2.py').write_text(code,encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
seal={'version':'v004','alcance':'v003 sin cambios de conteos; resoluciones exactas R7 en dictámenes R2 y límite histórico fiel','archivos':[{'ruta':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(out.glob('*.py'))]}
(out/'congelada.json').write_text(json.dumps(seal,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(seal))
