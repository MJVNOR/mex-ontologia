# Ronda 7 — ejecución paralela sin Gemma

## Resultado

- 31 significados SINAC incorporados con dos auditorías y evidencia fijada por SHA-256.
- 1423 significados respaldados, 1106 conceptos y 4478 correspondencias revisadas.
- 45 correspondencias candidatas: 17 anteriores y 28 nuevas coincidencias automáticas. Cero ambiguas.
- Studio sincronizado y verificado: 322662 triples. RDF y SHACL conformes.

## Brechas conservadas

| Frente | Significados sin respaldo |
| --- | ---: |
| Defunciones | 32 |
| Nacimientos | 22 |
| Matrículas | 30 |
| Epidemiología | 25 |
| TIC | 24 |
| Diversos | 5 |

Quedan 138 significados reales, 16 vigencias y la anomalía `des_mpo_res` con dos encabezados corruptos. V13/V14 permanecen como acceso no resuelto. El JSON conserva por caso las fuentes examinadas, evidencia faltante y condición para reabrir. Las consultas web específicas quedaron atendidas por las vías examinadas.

## Alcance

Los textos aprobados mantienen sus límites de recurso y edición. No acreditan vigencias, joins, identidades de catálogos ni códigos que la evidencia no documenta. Los 20 pares estructurales de R6 se conservan como antecedente; tres se promovieron.

La predicción inicial de 17 candidatas no contemplaba las 28 coincidencias que aparecen al materializar los nuevos significados. Se corrigieron los adaptadores de conteos de R1/R2 sin modificar manifiestos anteriores.

Gemma quedó excluido y no se contactó a publicadores. Se validaron datos, RDF y SHACL; no se ejecutó la suite Python en esta ronda.

[Casos, auditorías, evidencia, respaldos y recibo de Studio](ronda-7.json).
