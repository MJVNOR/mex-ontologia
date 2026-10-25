# Auditoría transversal de medidas — 175 reglas nuevas + 135 conceptos combinados

Revisión independiente de unidades, representaciones, tiempos/eventos, sujetos y calificadores. No se modifica ninguna entrega de lote.

## Cuentas verificadas

- Reglas revisadas: 175 (18+21+43+40+23+30).
- Conceptos nuevos revisados: 135 (18+16+37+23+14+27).
- Hallazgos: 10 (H1–H10). Bloqueantes: H1, H2, H3, H4, H5. Informativos/aptos: H6–H10.

## Dictámenes (corto)

- H1 [BLOQUEA] P36/P39/P40 lote-4 (+P13 pruebas): pregunta de conteo/procedimiento con tipo Booleano Si/No. El positivo overclaim ("denota el conteo") contradice su propio límite. Corregir y no usar como medida.
- H2 [BLOQUEA] r4-lote-4-002/003/004 sin calificador de metodología; colisionan con fuero-común / municipal-anterior / víctima-anterior. Calificar o desambiguar.
- H3 [BLOQUEA] r4-lote-3-tiempo-9/10/11 con representación `hora` recorta la fecha (tipo Fecha y Hora, ejemplo con fecha). Misma huella con doble representación (lote-3 `hora` vs lote-4 `no_especificada`). Unificar + aclarar contradicción de formato DD/MM/AAAA vs AAAA-MM-DD en todos los relojes P3/P4/P5.
- H4 [BLOQUEA cruce] Mismo concepto reutilizado en 3 encuestas TIC (y duplicados lote-2/5) autoriza comparación sin acreditar población/periodo/cuestionario. Apto intra-encuesta; bloqueado el cruce.
- H5 [BLOQUEA] Lote-3 P10/P16/P18 con representación `codigo` para preguntas Si/No o lista libre. Pasar a `no_especificada` o respaldar catálogo.
- H6 Observación: r4-lote-4-001, descripción defectuosa; el ejemplo no fija sentido normativo. Solicitar redacción al publicador.
- H7 Apto: pares código/nombre separados; sector con prefijo no decodificado; CIE como clave declarada sin versión. Mantener.
- H8 Apto: ningún padre agrega unidad/moneda/identidad (solo `tiempo` y `mes`; montos, conteos, CQ, edades con padre null y límites correctos).
- H9 Sin reglas nuevas de municipio/capacidad/generación: no hay falsa equivalencia nueva que dictaminar; no cruzar CVE_LOC con municipios ni AGEB.
- H10 Apto: sujetos calificados (madre/difunto/víctima/alumno/dependencia); identificadores solo locales.

## Focos pedidos

- P36/P39/P40 lote-4 = r4-lote-4-025/026/027: ver H1. 027 además duplica literal de r3a9-059.
- Metodologías delictivas: bien separadas salvo H2. Lote-2 marca "no comparable"; extender esa disciplina a lote-4.
