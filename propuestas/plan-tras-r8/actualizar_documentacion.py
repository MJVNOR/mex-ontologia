"""Actualiza las portadas corrientes después del recibo R9 cerrado."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'propuestas/plan-tras-r8/ejecucion-20261024'
report=json.loads((ROOT/'reports/ronda-9.json').read_text(encoding='utf-8'))
assert report['estado']=='cerrado_integrado_validado_y_sincronizado'
n=report['pruebas']['pruebas']
current=f'''R9 ejecuta el plan devuelto tras la revisión independiente de R8: incorpora **dos declaraciones de unidad cualificadas** (milímetros y hectáreas) y una regla SHACL de exclusión entre significado documentado y candidato. Conserva **1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas**. La suite completa pasa **{n} pruebas**; RDF y SHACL conformes, Studio sincronizado y verificado. [Informe y evidencia R9](reports/ronda-9.md).

Quedan **138 significados reales**, 16 vigencias y `des_mpo_res`; dos encabezados corruptos siguen separados del conteo de significados. V13/V14 mantienen acceso no resuelto. Las 17 candidatas dependen del respaldo faltante. Los pilotos de intervalos temporales y jerarquía clínica dieron resultados negativos documentados. Gemma quedó excluido y no se contactó a publicadores.
'''
files={}
for name in ('README.md','PLAN.md'):
    p=ROOT/name;text=p.read_text(encoding='utf-8')
    if name=='README.md':
        start=text.index('## Estado vigente: ronda 8')
        end=text.index('## Antecedentes de consolidación semántica',start)
        replacement='## Estado vigente: ronda 9\n\n'+current+'\nSe completó el [plan posterior a R8](docs/plan-actualizado-tras-r8.md) con agentes paralelos mediante el MCP nativo de OpenCode y Muse 1.3. [Ejecución y decisiones](docs/plan-paralelo-ronda-9-sin-gemma.md). Obscura permitió verificar términos normativos; no se repitieron búsquedas agotadas sin pistas nuevas.\n\nAntecedentes fechados: [R8](reports/ronda-8.md), [R7](reports/ronda-7.md) y [R6](reports/ronda-6.md). Sus cifras describen esos cierres históricos.\n\n'
    else:
        start=text.index('R8 incorpora **28 correspondencias SINAC**')
        end=text.index('## Ejecución paralela completada',start)
        replacement=current+'\nSe ejecutó el [plan posterior a R8](docs/plan-actualizado-tras-r8.md); su [recibo de ejecución R9](docs/plan-paralelo-ronda-9-sin-gemma.md) distingue lo integrado de las brechas que requieren documentación primaria nueva.\n\n'
    p.write_text(text[:start]+replacement+text[end:],encoding='utf-8');files[name]=hashlib.sha256(p.read_bytes()).hexdigest()
p=ROOT/'docs/nucleo-semantico.md';text=p.read_text(encoding='utf-8')
start=text.index('## Cobertura vigente R8');end=text.index('## Separar las entidades',start)
text=text[:start]+'''## Cobertura vigente R9

1423 significados respaldados, 1106 conceptos, 4506 correspondencias revisadas, 17 candidatas y cero ambiguas. R8 revisó las 28 correspondencias SINAC; R9 conserva ese núcleo y añade dos declaraciones de unidad sobre definiciones concretas y la exclusión SHACL documentado/candidato. Una declaración de unidad no se atribuye globalmente a otros archivos o periodos. No se integraron intervalos ni jerarquías clínicas sin respaldo.

Quedan 138 significados reales sin respaldo y dos encabezados corruptos. Se conserva el requisito de significado respaldado para una correspondencia revisada. [Evidencia y límites R9](../reports/ronda-9.md). [Formato y lanzamientos](versionado-y-lanzamientos.md).

'''+text[end:]
p.write_text(text,encoding='utf-8');files[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
p=ROOT/'docs/plan-paralelo-ronda-9-sin-gemma.md'
p.write_text(f'''# Ejecución del plan posterior a R8 — R9

Estado: **ejecutado, integrado, validado y sincronizado**. El plan fue devuelto por el chat solicitado después de revisar el cierre R8.

| Frente paralelo | Resultado |
| --- | --- |
| C1 — 17 candidatas | Trazadas; cero promociones sin significado respaldado |
| C2 — oportunidades | 1191 pares priorizados y top50; mapa estructural original preservado, sin nuevos joins |
| C3 — cobertura | 5523 columnas reconciliadas; cinco observaciones conservadas |
| C4 — referencias | 19 casos, 104 evidencias, siete necesidades y preguntas documentales sin enviar |
| P1 — QUDT | Dos declaraciones cualificadas, con literales exactos y términos HTTP verificados; hm³ fuera del grafo nuevo |
| P2 — OWL-Time | Negativo: faltan bordes y referencia temporal suficientes |
| P3 — jerarquía clínica | Negativo: 101 conceptos sin jerarquía documental acreditada |
| P4 — SHACL y versiones | Exclusión probada sobre 1442 variables y cuatro fixtures; formato separado del lanzamiento |
| W — estándares | Fuentes primarias por Obscura; términos tentativos inválidos descartados |
| A/B — auditorías | Dictámenes independientes sobre el payload exacto y el integrador final |

El coordinador integró solo el material aceptado en una secuencia, preservando los manifiestos R1–R8. La suite pasó **{n} pruebas** antes y después de generar RDF. Portal y Studio superaron SHACL; la sincronización conservó sus distintos ámbitos y las ediciones ajenas.

Los 138 significados, 16 vigencias, `des_mpo_res`, las filas corruptas y las 17 candidatas conservan su evidencia faltante y condiciones de reapertura. No hubo contactos externos ni cambios de Gemma.

Expediente: `propuestas/plan-tras-r8/ejecucion-20261024/`. [Informe y recibos](../reports/ronda-9.md). [Plan recibido](plan-actualizado-tras-r8.md).
''',encoding='utf-8')
files[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(E/'documentacion-actualizada.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(files))
