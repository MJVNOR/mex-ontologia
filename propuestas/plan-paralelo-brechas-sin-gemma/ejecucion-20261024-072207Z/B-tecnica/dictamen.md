# Dictamen B-tecnica GLOBAL (2026-10-24)

Dictamen: **aceptar**. defectos: [] (0 abiertos).
Seleccion FINAL: `seleccion-v002.json` sha256
`ef174231023600715cfdfc477eebf2f3e06478744ec2a5c043c014f91a489f92`
(10 versiones + 3 paquetes web; `seleccion.json` anterior no modificada:
`02f51d22…8123254`).

## Cobertura 188 = 31 + 155 + 2

- Lote-1 (128, sin cambios, SHAs identicos en seleccion): S1 v002, S3,
  S4, S5, V1, V2 v001 — dictamen lote-1 intacto, no re-auditados.
- Lote-2 (59): S2 v002, 53 casos, 31 propuestas aprobadas con acotacion;
  V3 v002, 6 correcciones a novedad. SHAs identicos en seleccion.
- Resto (7, auditado, 0 errores): S6 v002, 5 brechas (3 con
  respuesta W sin_hallazgo, 0 propuestas); V4 v004 (seleccion-v002),
  2 acceso_no_resuelto con resultado negativo final W-v003 incorporado
  y sin pendiente futura (v003 auditada antes con identico
  estado/puerta; el delta v003→v004 solo anade la evidencia W-v003
  y actualiza motivo/reapertura/limites).
- Estados globales: 31 propuesta_para_auditar, 155 brecha_externa,
  2 acceso_no_resuelto. 0 afirmaciones fuera de las 31.

## Por ID propuesto

27 aceptar con texto integro + 4 con texto acotado (74, 76: sin el
parentesis DOF/CEN; 84: sin "duracion codificada como hora"; 99: sin
verificacion de instancia). Texto minimo aprobado por ID y limites en
`dictamen.json` (decisiones_propuestas, copiado exacto de lote-2).

## Notas

- Otros 9 roles + 3 paquetes identicos entre seleccion y seleccion-v002;
  128 de lote-1 y 59 de lote-2 intactos, no reexaminados.
- Rutas `.\`, U+FFFD y nominales ya observados en lotes; no bloqueantes.
- Las reglas R7 se materializan aparte: no se afirma instalacion.
  Revision concreta de aceptadas.json + codigo con SHA, pendiente.
- Sin Gemma, tests ni contactos en lo auditado. Sin editar otros
  dictamenes congelados.
