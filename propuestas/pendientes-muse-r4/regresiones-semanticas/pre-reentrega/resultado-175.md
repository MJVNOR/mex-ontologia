# Regresiones semanticas r4

175 reglas (lote-1..6: 18+21+43+40+23+30) contra generador preparado `integrador/codigo/scripts`.
Combinada construida sin instalar sobre fuentes locales y codigo real.

## Cuentas verificadas

- A-alcance: 1050/1050 aprobados
- B-normalizacion: 382/382 aprobados
- C-preservacion: 7/7 aprobados
- D-esquema: 4/4 aprobados
- E-duplicadas: 6/6 aprobados
- F-estructura: 7/7 aprobados

Total: 1456/1456 aprobados, 0 fallidos.
Hallazgos bloqueantes: 0.

## Que verifica cada suite (conducta, no conteos)

- A-alcance: cada regla aplica a su fila exacta; mutando conjunto/diccionario/definicion/nombre/descripcion no alcanza otra fila.
- B-normalizacion: mayusculas/sin acentos conservan la regla; sentidos confundibles (mismo nombre/descripcion) discriminan.
- C-preservacion: 1212 significados y 865 vinculos intactos, 175 reglas y vinculos nuevos materializados, ninguna promocion ajena, 5 PIN resueltos.
- D-esquema: huella_esquema/huella_fila/descripcion/diccionario alterados abortan.
- E-duplicadas: columna duplicada, regla duplicada, pin sin columna, pin incompleto, nombre ambiguo sin pin y concepto ajeno se rechazan.
- F-estructura: una fila por regla, formato/linaje de conceptos, base intacta, calificadores, representacion y limites.

## Limites

- La propuesta combinada se construye sin instalar: no modifica ontologia/, data/ ni scripts/.
- Los 5 PIN ambiguos exigen el generador preparado (definicion_iri); el nucleo instalado los rechaza.
- Suite E/D sinteticas usan muestras minimas pero el mismo codigo (construir/interpretacion); D incluye 4 mutaciones sobre datos reales.
- No se valida contenido de filas ni valores: solo que la regla alcanza su fila y ninguna ajena.
- Normalizacion intencional (acentos/case) verificada como conservadora de regla; no como equivalencia entre filas.
