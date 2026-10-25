"""Actualiza las vistas vigentes después de emitir el recibo final R7."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
report=json.loads((ROOT/'reports/ronda-7.json').read_text(encoding='utf-8'))
assert report['estado']=='integrado_regenerado_validado_y_sincronizado'
summary='R7 incorpora 31 significados SINAC con evidencia fijada y auditoría independiente: **1423 significados respaldados, 1106 conceptos, 4478 correspondencias revisadas, 45 candidatas y cero ambiguas**. Las candidatas se dividen en 17 anteriores y 28 coincidencias automáticas nuevas. [Resultado y límites](reports/ronda-7.md).'
pending='Quedan **138 significados reales**, 16 vigencias de catálogos y la anomalía `des_mpo_res` con dos filas de encabezado corruptas. V13/V14 conservan acceso no resuelto. Cada caso mantiene fuentes, evidencia faltante y condición de reapertura en [el informe completo](reports/ronda-7.json). Gemma quedó excluido y no se contactó a publicadores.'
changes=[]
def update(rel,text):
    p=ROOT/rel
    old=p.read_bytes()
    p.write_text(text,encoding='utf-8')
    changes.append({'ruta':rel,'sha256_antes':hashlib.sha256(old).hexdigest(),'sha256_despues':hashlib.sha256(p.read_bytes()).hexdigest()})
p=ROOT/'README.md'
text=p.read_text(encoding='utf-8')
start=text.index('## Estado vigente:')
end=text.index('## Antecedentes de consolidación semántica',start)
section='## Estado vigente: ronda 7\n\n'+summary+'\n\n'+pending+'\n\nEl plan paralelo se ejecutó con agentes OpenCode Muse 1.3 y fuentes primarias investigadas mediante el MCP de Obscura. Los 20 pares estructurales de R6 se preservan como antecedente; tres se promovieron al respaldar sus significados. [Ejecución del plan](reports/ejecucion-plan-sin-gemma.md) · [Investigación con Obscura](docs/investigacion-opencode-obscura.md).\n\nAntecedentes fechados: [R6](reports/ronda-6.md), [depuración](reports/pendientes-depurados.md), [investigación anterior](reports/investigacion-post-r6.md) y [registro estructural R6](reports/cierre-brechas-post-r6.md). Sus cifras describen esos cierres históricos.\n\n'
update('README.md',text[:start]+section+text[end:])
p=ROOT/'PLAN.md'
text=p.read_text(encoding='utf-8')
start=text.index('## Estado vigente y siguiente trabajo documental')
end=text.index('## Antecedentes: consolidación semántica inicial',start)
section='## Estado vigente y siguiente trabajo documental\n\n'+summary+'\n\n'+pending+'\n\n## Ejecución paralela completada\n\nEl [plan sin Gemma](docs/plan-paralelo-brechas-sin-gemma.md) se ejecutó con diez frentes temáticos, investigación web por Obscura y revisiones independientes. Se integró únicamente lo auditado; se regeneró y validó el grafo y se sincronizó Studio con respaldo. Los manifiestos de rondas anteriores se conservaron. [Recibo final](reports/ejecucion-plan-sin-gemma.md).\n\nEl siguiente trabajo requiere evidencia primaria nueva para las brechas externas o revisión documental específica de las 28 candidatas surgidas al incorporar significados. Las coincidencias de nombre no autorizan cruces ni equivalencias de códigos.\n\n'
update('PLAN.md',text[:start]+section+text[end:])
p=ROOT/'docs/plan-paralelo-brechas-sin-gemma.md'
text=p.read_text(encoding='utf-8')
text=text.replace('Estado: plan de ejecución; esta planificación no lanza agentes ni cambia el núcleo.','Estado: **ejecutado y cerrado en R7**. [Resultados, evidencia, validación y brechas conservadas](../reports/ronda-7.md). El resto del documento conserva el plan y su punto de partida R6 como antecedente.')
update('docs/plan-paralelo-brechas-sin-gemma.md',text)
p=ROOT/'docs/nucleo-semantico.md'
text=p.read_text(encoding='utf-8')
intro='\n## Cobertura vigente R7\n\n1423 significados respaldados, 1106 conceptos, 4478 correspondencias revisadas, 45 candidatas (17 previas y 28 nuevas) y cero ambiguas. Quedan 138 significados reales sin respaldo y dos encabezados corruptos. Se conserva el requisito de significado respaldado para una correspondencia revisada. [Evidencia y límites R7](../reports/ronda-7.md).\n'
index=text.index('\n## Separar las entidades')
update('docs/nucleo-semantico.md',text[:index]+intro+text[index:])
out=ROOT/report['expediente']/'integracion/documentacion-actualizada.json'
assert not out.exists()
out.write_text(json.dumps({'cambios':changes,'recibo_r7_sha256':hashlib.sha256((ROOT/'reports/ronda-7.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(changes))
