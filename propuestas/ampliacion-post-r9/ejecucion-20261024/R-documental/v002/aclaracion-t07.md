# R-documental v002 — Aclaracion de T-07 y revision de carriles

Fecha UTC: 2026-10-24T20:24:26+00:00. Preserva v001 byte a byte; no evalua entregas futuras.

## Que paso con T-07

T-07 aparecio en `false` en una corrida intermedia por un defecto del check, no de T: el titulo A3 se comparaba contra `Poblacion` (sin diacritico) y el mapa dice `Población`. ID, rango y score ya concordaban: A1 rango 2 score 3.0, A2 rango 4 score 3.0, A3 rango 1 score 5.0.

En el v001 sellado T-07 esta en `true` (A1=(2, 3.0) A2=(4, 3.0) A3=(1, 5.0)) y el resumen es 32/32 sin fallas. No corresponde hallazgo contra T: el hallazgo H-01 es otro asunto (huella del plan).

La misma corrida intermedia mostro T-11, T-15, A2-05 y A2-11 en false: T-11 quedo ligado a H-01; los otros tres eran literales del auditor (punto final, diacritico y nombres de eje). Solo cuentan los bytes sellados.

## Carriles

| Carril | ID | Rango | Score | Etiqueta staging | Estado |
| --- | --- | --- | --- | --- | --- |
| A1-911 | `19e5036d…` | 2 | 3.0 | A1-911 | NO_JOIN_APROBADO |
| A2-matrimonios-nacimientos | `1cf9c8e2…` | 4 | 3.0 | A2-matrimonios-nacimientos | NO_JOIN_APROBADO |
| A3-itama | `27a5c80c…` | 1 | 5.0 | A3-itama | NO_JOIN_APROBADO |

Solo 3 de 50 filas llevan etiqueta; las otras 47 quedan sin carril. T-07 verifica presencia/rango/score/titulos por ID; T-08b verifica la etiqueta exacta y la fidelidad de la fila; T-10 mantiene NO_JOIN_APROBADO. El carril no acredita comparabilidad ni autoriza join o rate.

## Regla corregida y limites

Para v002 de los autores: comparar por ID, rango y score; usar titulos normalizados solo como contraste; tomar literales UTF-8 de la fuente; mantener el mapeo de carriles por ID exacto. Una falla de check solo degrada el veredicto si no esta asociada a un hallazgo documentado.

No se aceptan bytes futuros: T/A2 v002 y A1/A3 v002 quedan pendientes de sello. W/v002 (6 normas 3.5.3) esta fuera de este encargo y no se reviso aqui; Q/v002 y S/v001 siguen en proceso. No se editan autores ni produccion.
