# A-documental — dictamen lote-2 (2026-10-24)

Alcance: S2-nacimientos v002 (53 casos, 31 propuestas) + V3-coespo v002
(6 correcciones). S6 y V4 irán en adenda; no bloquean. Sin dictamen global.

## S2-nacimientos v002 — dictamen: parcial

31 propuestas evaluadas por ID/tier. 9 aceptar, 22 aceptar_con_texto_acotado,
0 rechazos totales. `propuestas_aceptadas`: 31 IDs (significado mínimo
acotado; ver textos exactos en `lote-2.json`).

- **A1 (17, 32–97): aceptar_con_texto_acotado.** Prueba formal verificada por A
  contra bytes: mnemónico exacto + IDnac + catálogo del descriptor, y par
  código=descripción confirmado uno por uno en los 10 xlsx (1='SI',
  1='PRIMER TRIMESTRE', 1='NINGUNA' vía '01', 2='NO', 2='NO REMUNERADO...',
  1='ÚNICO', 3='CESÁREA', 8='NO APLICA', 1='MÉDICO', 11='MÉDICO GINECO
  OBSTETRA', 7='MÉDICO GINECO-OBSTETRA', 0='NO ESPECIFICADO'), con etiqueta D
  local idéntica documentada en la misma entrega. Distinto de igualdad de
  valores sola y sin asumir identidad global de catálogos. Se acepta el
  significado + código(s) con ejemplo local; **no** "tabla determinada",
  **no** lista completa de códigos, **no** vigencia más allá del recurso
  2022-01-01 a 2022-09-26.
- **A2 (6: 31, 57, 58, 71, 72, 106): aceptar.** Significado mínimo del
  descriptor (99 = No Especificado consta en el descriptor) + tipo compatible.
- **A3 geo (100, 102, 104): aceptar.** 26=SONORA, 26/055 SLRC VIGENTE,
  26/055/0001 SLRC verificados en catálogos fechados contemporáneos;
  reservados del descriptor. **83: acotado** — CLUES registrada
  (SONORA/SLRC), pero "EN OPERACION" no aprobado: el estatus en el archivo
  es '1' sin catálogo de estatus citado. **99: acotado** — significado sin
  verificación de valor local (ejemplo vacío declarado).
- **A4 (74, 76): acotado.** Solo el significado del descriptor. Excluidos:
  '0000 = NINGUNA APARENTE' (corroborado solo por la hermana ANOMALIACIE,
  ella misma en brecha 73/75) y 'DIAGNOSTICOS = CIE-10' (ausente del zip;
  DOF CEN citado sin localizador en esta entrega).
- **A5 (84): acotado.** Solo el significado del descriptor; formato Hora
  como duración no especificado, sin lectura de duración aprobada.
- **22 brechas (*D + ANOMALIACIE1/2): conformes.** Sin variable nacional ni
  regla de decodificación publicada; sin contraparte en el instrumento.
  No se fuerzan promociones. Cero promociones de correspondencias.

Límites transversales: instrumento nacional (DGIS/SINAC), sin carta Sonora
exigida como único medio (ámbito probado por consistencia 26/SONORA +
identificador + edición); edición por título/rango sin acta separada
(declarado); zip con 20 xlsx verificados por bytes. Observaciones menores
(no defectos): ruta de evidencia del zip con barra invertida; "DEFUN 2022"
residual en límites S2 — para B/coordinador.

## V3-coespo v002 — dictamen: aceptar

Aplica lo pedido en lote-1: retira "nunca examinado"/"por primera vez",
formula acotada, puerta `sin_pista_nueva` + `analisis_adicional_de_
documento_conocido`, API como re-verificación. Estado y condición
conservados; v001 no editada (sha verificado). Se cierra el defecto.

## Propuestas aceptadas

31 IDs S2 (listados en `lote-2.json`): 9 tal cual + 22 con texto acotado.
V3 v002: 0 propuestas (6 brecha_externa). Sin dictamen global.
