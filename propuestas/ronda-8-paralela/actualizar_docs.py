"""Actualiza vistas vigentes después del cierre R8; conserva informes anteriores."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/ronda-8-paralela/ejecucion-20261024'
r=json.loads((ROOT/'reports/ronda-8.json').read_text(encoding='utf-8'))
assert r['estado']=='cerrado_integrado_validado_y_sincronizado'
changes=[]
def update(rel,text):
    p=ROOT/rel;old=p.read_bytes();p.write_text(text,encoding='utf-8')
    changes.append({'ruta':rel,'sha256_antes':hashlib.sha256(old).hexdigest(),'sha256_despues':hashlib.sha256(p.read_bytes()).hexdigest()})
summary='R8 incorpora **28 correspondencias SINAC** con doble auditoría: **4506 correspondencias revisadas, 17 candidatas y cero ambiguas**. Conserva **1423 significados respaldados y 1106 conceptos**. La suite completa pasa **181 pruebas**; RDF y SHACL conformes, Studio sincronizado y verificado. [Informe y evidencia R8](reports/ronda-8.md).'
pending='Quedan **138 significados reales**, 16 vigencias y la referencia `des_mpo_res` con dos encabezados corruptos separados del conteo de significados. V13/V14 siguen con acceso no resuelto. Las 17 candidatas anteriores dependen del respaldo semántico faltante. [Condiciones para reabrir por caso](reports/ronda-8.json). Gemma quedó excluido y no se contactó a publicadores.'
p=ROOT/'README.md';text=p.read_text(encoding='utf-8')
start=text.index('## Estado vigente:');end=text.index('## Antecedentes de consolidación semántica',start)
section='## Estado vigente: ronda 8\n\n'+summary+'\n\n'+pending+'\n\nSe ejecutó el [plan paralelo R8](docs/plan-paralelo-ronda-8-sin-gemma.md) mediante el MCP nativo de OpenCode, con Muse 1.3. Obscura estuvo disponible; las brechas examinadas no aportaron nuevas pistas primarias concretas. No se repitieron búsquedas agotadas.\n\nAntecedentes fechados: [R7](reports/ronda-7.md), [R6](reports/ronda-6.md), [depuración](reports/pendientes-depurados.md) y [registro estructural R6](reports/cierre-brechas-post-r6.md). Sus cifras describen esos cierres históricos.\n\n'
update('README.md',text[:start]+section+text[end:])
p=ROOT/'PLAN.md';text=p.read_text(encoding='utf-8')
start=text.index('## Estado vigente y siguiente trabajo documental');end=text.index('## Antecedentes: consolidación semántica inicial',start)
section='## Estado vigente y siguiente trabajo documental\n\n'+summary+'\n\n'+pending+'\n\n## Ejecución paralela completada\n\nEl [plan R8](docs/plan-paralelo-ronda-8-sin-gemma.md) revisó 202 casos: 28 correspondencias integradas y 174 decisiones pendientes conservadas (138 significados, 17 correspondencias, 16 vigencias y tres registros de anomalía/encabezados). Se preservaron los manifiestos anteriores y los respaldos. [Recibo final](reports/ronda-8.json).\n\nPor instrucción del usuario, el chat «Identifica pendientes de la ontolog» revisará este cierre y actualizará su plan a partir de los resultados para continuar la ejecución. Las brechas externas requieren evidencia primaria nueva; los nombres de campos no acreditan significados, vigencias ni equivalencias de códigos.\n\n'
update('PLAN.md',text[:start]+section+text[end:])
p=ROOT/'docs/plan-paralelo-ronda-8-sin-gemma.md';text=p.read_text(encoding='utf-8')
title='# Plan y ejecución paralela R8 — sin Gemma\n'
assert text.startswith(title)
update('docs/plan-paralelo-ronda-8-sin-gemma.md',text.replace(title,title+'\nEstado: **ejecutado, validado y cerrado**. [Resultados R8](../reports/ronda-8.md). El reparto y la secuencia siguientes conservan el plan original.\n',1))
p=ROOT/'docs/nucleo-semantico.md';text=p.read_text(encoding='utf-8')
start=text.index('## Cobertura vigente R7');end=text.index('## Separar las entidades',start)
section='## Cobertura vigente R8\n\n1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas. Las 28 correspondencias nuevas de SINAC de R7 quedaron revisadas en R8. Quedan 138 significados reales sin respaldo y dos encabezados corruptos. Se conserva el requisito de significado respaldado para una correspondencia revisada. [Evidencia y límites R8](../reports/ronda-8.md).\n\n'
update('docs/nucleo-semantico.md',text[:start]+section+text[end:])
out=E/'documentacion-actualizada.json';assert not out.exists()
out.write_text(json.dumps({'cambios':changes,'recibo_r8_sha256':hashlib.sha256((ROOT/'reports/ronda-8.json').read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archivos_actualizados':len(changes)}))
