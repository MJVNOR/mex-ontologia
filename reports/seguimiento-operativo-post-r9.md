# Seguimiento operativo posterior a R9

Estado: completado. Actualización documental; no abre una ronda semántica nueva.

## Avances

- [Cobertura operativa R9](cobertura-operativa-r9.md): estados, denominadores y criterios de reapertura de 26 frentes; incluye las 17 candidatas individualizadas y las cinco observaciones de esquema.
- Siete necesidades y siete preguntas preservadas como copia exacta del expediente, preparadas y **no enviadas**.
- Presas: la asociación `cat_estatal/Clave → /4` ya estaba integrada en R6. Los archivos cotejados no aportan evidencia primaria nueva; V05 sigue sin vigencia acreditada.

## Validación

- **213 pruebas Python OK**, incluidas nueve pruebas del nuevo generador.
- RDF y SHACL conformes: portal **322405 triples** y Studio **323014 triples**.
- La exportación viva de Studio coincide con el snapshot R9; no se aplicaron operaciones de actualización ni carga sobre Studio.
- Los 52 archivos fijados de estado y evidencia R9 conservan sus hashes. Manifiestos R1–R9 intactos.

## Pendientes

Se mantienen 138 significados, 16 vigencias (V13/V14 con acceso no resuelto), `des_mpo_res`, dos encabezados corruptos, 17 candidatas y cinco observaciones de esquema. Solo se reabren con evidencia concreta. No se promovieron candidatas ni ejecutaron joins por el ranking. Gemma quedó excluido y no se contactó a publicadores.

## Archivos

Nuevos: `scripts/generar_cobertura_operativa.py`, `tests/test_generar_cobertura_operativa.py`, `reports/cobertura-operativa-r9.json` y `.md`, este informe y su JSON. README y PLAN enlazan la vista operativa; sus copias previas están en el expediente. Entregas Presas, preguntas, auditoría, suite y recibos: `propuestas/cobertura-operativa-post-r9/ejecucion-20261024/`.

[Recibo con hashes, archivos y validación](seguimiento-operativo-post-r9.json).
