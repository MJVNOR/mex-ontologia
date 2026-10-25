# Regresiones semanticas r4 (final)

172 reglas finales (lote-1..6: 18+21+43+37+23+30), 351 decisiones de significado, 3601 vinculos (3596+5 PIN).
Lote-4 retiro 3 contradicciones reales (r4-lote-4-025/026/027); correcciones de conceptos/representaciones/limites en 2/3/4/6 verificadas sobre archivos finales.
Informe anterior 1456/175 archivado en `pre-reentrega/` como instantanea valida; no es el resultado final.
Generador preparado `integrador/codigo/scripts`; combinada construida sin instalar, solo fuentes locales.

## Cuentas verificadas

- A-alcance: 1032/1032 aprobados
- B-normalizacion: 377/377 aprobados
- C-preservacion: 7/7 aprobados
- D-esquema: 4/4 aprobados
- E-duplicadas: 6/6 aprobados
- F-estructura: 7/7 aprobados
- G-retiradas: 7/7 aprobados

Total: 1440/1440 aprobados, 0 fallidos.
Hallazgos bloqueantes: 0.

## Que verifica cada suite (conducta, no conteos)

- A-alcance: cada regla aplica a su fila exacta; mutando conjunto/diccionario/definicion/nombre/descripcion no alcanza otra fila.
- B-normalizacion: mayusculas/sin acentos conservan la regla; sentidos confundibles (mismo nombre/descripcion) discriminan.
- C-preservacion: 1212 significados y 865 vinculos intactos, 175 reglas y vinculos nuevos materializados, ninguna promocion ajena, 5 PIN resueltos.
- D-esquema: huella_esquema/huella_fila/descripcion/diccionario alterados abortan.
- E-duplicadas: columna duplicada, regla duplicada, pin sin columna, pin incompleto, nombre ambiguo sin pin y concepto ajeno se rechazan.
- F-estructura: una fila por regla, formato/linaje de conceptos, base intacta, calificadores, representacion y limites.
- G-retiradas: IDs retirados ausentes, sus 3 definiciones no respaldadas, sus 3 columnas no revisadas (+1 columna control por observacion).

## Limites

- La propuesta combinada se construye sin instalar: no modifica ontologia/, data/, scripts/ ni integrador/.
- Los 5 PIN ambiguos exigen el generador preparado (definicion_iri); el nucleo instalado los rechaza.
- Suite E/D sinteticas usan muestras minimas pero el mismo codigo (construir/interpretacion); D incluye 4 mutaciones sobre datos reales.
- No se valida contenido de filas ni valores: solo que la regla alcanza su fila y ninguna ajena.
- Normalizacion intencional (acentos/case) verificada como conservadora de regla; no como equivalencia entre filas.
- Correcciones de conceptos/representaciones/limites en lotes 2/3/4/6 verificadas sobre archivos finales; sin copia previa de entregas no hay dif de contenido, solo conducta final.
- Retiradas r4-lote-4-025/026/027: sus definiciones no quedan respaldadas y sus 3 columnas no quedan revisadas (suite G + columna control).
