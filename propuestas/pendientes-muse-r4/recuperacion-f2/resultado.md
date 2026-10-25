# Resultado — recuperación F2 + presupuesto Gemma4 (propuesta aislada, v4)

Bloqueo corregido antes de entrega: el primer patch inyectaba texto F2 (solo-2020, grandes_grupos/indicadores, 1990-2040, dos fuentes) para F1/F3. Falsa afirmación: F1 es Matrimonios-Divorcios 2022 y F3 Titulados-Egresados 2020-2021 + Nuevo-Reingreso 2021-2022, ambas con 0 comparaciones en RDF. Ahora cada resumen de ficha deriva de su RDF real (conteos nativos, periodos/roles/medidas observados, ALCANCE por lo observado o ausencia declarada, ejemplo con su periodoCruzado); cero frases acreditativas hardcodeadas fuera de su ficha; el texto de ficha vale solo como hechos citados (la fuente investigada puede traer prompt injection). `test_fichas_f1_f3.mjs`: FICHAS OK (F1/F3 con lo suyo, F9 inexistente vacío, F2 derivado intacto con 72/144/2020/ambas fuentes).

Fallo F2 y 26001: alias resuelto por IRI exacto + detalle por `codigoTextual`+`periodoCruzado` (vecindad hop-1 nunca traía medidas por fuente).

Corrección 429 (dashboard usuario Gemma4 31B: RPM 1/30, TPM 13.08K/16K, RPD 1/14.4K): límite por minuto por llamadas sucesivas con 2s entre ellas; solo C2 (22499tok) supera 16K por sí solo; NO se afirma cuota diaria agotada (RPD 1/14.4K). Presupuesto minimizador (≤10000tok, margen 1.15, holgura 100tok) + harness con espaciado mínimo 65s y respeto RetryInfo (esperas >15min → pendiente_cuota).

Verificación (0 llamadas al modelo, solo SELECT): `test_regresion` REGRESION OK (C2 F2; C6 aditivo; C1/C3/C4/C5 byte-idénticos); `test_presupuesto` PRESUPUESTO OK (6/6 en 9851–9903tok, sin truncar, sin prohibidos); `harness_gemma` 6/6 bajo presupuesto, grafo 284810 intacto. Llamadas reales solo con `--con-modelo` + `ONTO_ALLOW_MODEL_CALLS=1` (humano; sintaxis verificada).

Aplicar: respaldar `graphrag.ts`, copiar `graphrag.f2.ts` encima (o `patch -p1`), pasar `{model}`, recompilar si aplica, reiniciar Studio. SHAs: original `b1099305…a440ef`, copia `030d539b…e45b93`, patch `c320c1ca…5b0e7a`. Sin UI, sin tocar repo/instalación/grafo.
