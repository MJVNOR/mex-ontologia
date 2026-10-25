# Resultado tic — ronda 6

24 significados asignados. pendientes: 24. proponer: 0. artefacto_documental: 0. Reglas/conceptos nuevos: 0.

## Novedad r6 (única línea verificable)

- Relectura exacta 2026-10-23 de las 24 filas en `data/portal/inspecciones/*.json`: tipo/ejemplo/descripción byte-idénticos a r5 (mismas 24 huellas, `cobertura.json` unchanged sha `19237e41…`, 0 correspondencias en 4496, `inspecciones/*.json` con mismos sha que r5).
- La única línea pública razonable (páginas del portal) ya se agotó en r5: S09 negativo-portal + respuestas tic-web-01..07 (sin cuestionarios ni muestras públicas). R6 no re-visita páginas ni presenta esos negativos como hallazgos nuevos.

## Por qué todo queda pendiente

- 6 descripciones truncadas en celda fuente (P10/P16/P18/P21 Política Digital, P22 Desarrollo): colas `…permit…`, `…en ma...`, `…materia d...`, `…materia ...`, `…equipos...` verificadas; sin sentido literal completo.
- 11 anáforas sin referente declarado (P11→P10 truncada; P11/P15 Información General; P27/P29/P31/P33 Infraestructura `¿Cuáles?`/`¿Cuáles?4`; P7 Gobernanza y P7 Fortalezas): vecinas releídas (P26/P28/P30/P32, P8/P9/P14, P6, P10) confirman referente probable pero el diccionario no declara el vínculo; no se transfiere por proximidad.
- 6 contradicciones tipo-vs-descripción/ejemplo (P11 Presupuesto; P36/P39/P40 Desarrollo y Mejora; P8/P13 Mejora): se conservan como tales.
- 1 tautología (P10 Información General: `Actividades principales:` / `Actividades Principales`).

## Dependencia del publicador

Cada `pendientes[].requerido` en `entrega.json` nombra el documento exacto (cuestionario original completo o muestra de valores del recurso) que solo el publicador posee; `solicitudes-web.json` (r6-tic-web-01..07) lo registra sin pedir re-visitas. Sin ese documento no hay definición verificable: no se aprueba por nombre ni se infiere.

## Verificación

- 24/24 decisiones individuales con evidencia local + sha; `cobertura.json` sha coincide con `base.json`; núcleo y otras carpetas intactos.
- `listo.json` sha256 calculado desde bytes de `entrega.json`.
