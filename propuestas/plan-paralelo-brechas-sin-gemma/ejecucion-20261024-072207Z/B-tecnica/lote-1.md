# Dictamen B-tecnica — lote-1 (2026-10-24)

Dictamen: **aceptar**. Alcance: 128 casos en 7 versiones congeladas
(S1-defunciones v002; S3, S4, S5, V1, V2, V3 v001).
No incluye S2/S6/V4 (60 casos, lote-2 pendiente); no se declara completo el lote total.

## Verificado por bytes

- Base: 341/341 archivos existen y su sha256 coincide con `base.json`.
- Asignaciones: 10/10 sha256 coinciden; los 128 IDs estan dentro de su asignacion.
- Congeladas: 7/7 marcadores y entregas coinciden en bytes con `lote-1.json`.
- Originales: 128/128 `original_sha256` coinciden con `comprobacion.json`.
- Evidencia: 128/128 decisiones con puerta, estado, motivo, evidencia
  (ruta relativa + sha256 recalculado de bytes + localizador +
  afirmacion soportada), evidencia_faltante, limites y condicion_reapertura.
- Congruencia: 32+30+25+24+5+6+6 = 128; conteos iguales en entrega.json,
  entrega.md y congelada; 0 promociones; fechas solo `2026-10-24` sin hora inventada.
- Regla de versiones: S1 corrige en v002 nueva con v001 preservada; resto v001 intactas.
- Nucleo: cobertura, semantica, studio-live, portal y manifiestos r5/r6 intactos;
  Gemma excluido; sin suites de pruebas; sin contactos externos.
- V3 (6 pista_nueva): cada ID trae URL y motivo de novedad; el cierre como
  brecha_externa esta justificado por ID, se acepta.

## Resultado

- defectos: ninguno.
- propuestas_aceptadas: ninguna (0 promociones en el lote).
- Observacion no bloqueante: `V1-uth-presas/v001/congelada.json` no trae objeto
  `conteos`; los conteos 5/5 constan en entrega.json y entrega.md. No requiere version nueva.

Dictamen global final pendiente hasta `seleccion.json` del coordinador y lote-2.
