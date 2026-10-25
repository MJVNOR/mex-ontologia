# Dictamen B-tecnica — lote-2 (2026-10-24)

Dictamen: **aceptar_parcial**. Alcance: S2-nacimientos v002 (53 casos:
31 propuestas A1–A5) y V3-coespo v002 (6 correcciones, 0 propuestas).
S6 y V4 quedan a adenda; no se declara completo el lote total ni el dictamen global.

## Verificado por bytes (no solo notas del autor)

- Congeladas: 4/4 marcadores y entregas coinciden con `lote-2.json`.
- Asignacion y originales: 53 S2 + 6 V3 dentro de su asignacion;
  originales coinciden con `comprobacion.json`.
- Evidencia: toda entrada con ruta+sha256+localizador; sha recalculado
  de bytes coincide (rutas con `.\` normalizadas, resuelven en Windows).
- Codebook nuevo: zip con 20 xlsx; contenido jamas examinado antes.
  A1 17/17: codigo local en catalogo + etiqueta D identica a la
  descripcion (verificado en bytes, incl. mapeo 1↔'01', 2↔'02').
  Descriptor: 31/31 IDnac + texto + catalogo coinciden.
  Geografia/CLUES fechada: 26=SONORA, 055 VIGENTE, 0001, SRSMP000314
  EN OPERACION. Recurso trae columnas hermanas ANOMALIACIE1/2.
  Zip sin columnas D ni DIAGNOSTICOS (20/20 listado).
- Congruencia: 31 propuestas + 22 brechas = 53; V3 6 brechas, 0 propuestas;
  fechas solo `2026-10-24`; JSON cargable; v001 de S2/V3 preservadas;
  lote-1 intacto. Nucleo/Gemma/tests/contactos: sin cambios ni uso.

## Por ID

Aceptar (27, texto integro de la entrega):
31, 32, 34, 37, 39, 43, 45, 57, 58, 59, 61, 63, 65, 67, 69, 71, 72,
77, 79, 83, 87, 89, 97, 100, 102, 104, 106
(A1 prueba formal completa; A2 significado minimo con tipo compatible;
A3 geo/CLUES con valor fechado verificado. Sin aprobar codigos,
vigencias ni equivalencias adicionales.)

Aceptar con texto acotado (4, texto exacto en `lote-2.json`):
- 74, 76 (A4): se corta ` (lineamientos DOF CEN en evidencia previa)`
  por carecer de ruta+sha en la entrega. Aprobado: variable + texto
  descriptor (incl. 0000=NINGUNA APARENTE) + ejemplo local + hermana
  ANOMALIACIE; equivalencia total del catalogo no verificada.
- 84 (A5): se corta ` (duracion codificada como hora)`. Aprobado:
  variable + descriptor + tipo Hora + ejemplo como instancia de formato;
  unidad no acreditada.
- 99 (A3): texto integro; ejemplo local vacio, sin verificacion de
  instancia; aprobado solo el significado de la variable.

Rechazos: ninguno. Brechas externas aceptadas: 22 S2 (D-derivadas sin
variable nacional + ANOMALIACIE sin contraparte) y 6 V3 (correccion de
novedad verificada, estado/condicion conservados).

Obs. no bloqueantes: rutas con `.\`; U+FFFD en afirmaciones (canonico
con acento en el descriptor); `ESTABLECIMIENTOS_SALUD` vs archivo
`ESTABLECIMIENTO_SALUD_202204` (nominal); package_show version=null.

Global final pendiente a `seleccion.json` + adenda S6/V4.
