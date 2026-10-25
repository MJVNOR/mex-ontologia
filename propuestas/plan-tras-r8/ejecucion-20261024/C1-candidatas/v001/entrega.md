# C1 - Candidatas: auditoria derivada de las 17 (v001)

Estado: auditoria_derivada. Sin promociones. Sin cambios al nucleo, grafo ni Studio.

## Resumen
- Casos asignados/cubiertos: 17/17
- Columnas: 17 | Recursos: 5 | Conjuntos: 5 | Diccionarios: 5
- Recursos: 46977217-9396-4f9c-bddb-6616e82530b4, 5772b8ec-e272-4265-a757-f7ddd179fe04, 58f2d5a6-0432-48f1-8a35-a5efcce78bac, 6f39fc5d-e097-4954-8cd7-10e8f9dea541, ad6f77b8-569d-4826-8ce0-3c6efddcb098
- Promociones propuestas: 0 | Cambios nucleo/grafo: 0
- Consultas nuevas/modificadas: 0 (ver Impacto)

## Resultado global
17/17 trazadas a su par estructural (columna+definicion por nombre 1:1, mismo conjunto, revision null). 16 dependen de significado candidata_sin_definicion_suficiente (regla pista_nombre_o_clasificador_sin_promocion, representacion no_especificada); 1 (Total_Egresos) de significado fuera_del_nucleo_actual con contradiccion nombre/descripcion. Ninguna cumple Puerta 1 ni criterio de integracion (significado respaldado + evidencia fisica especifica). Se conservan como candidatas; no se promueve nada.

## Casos (id = columna; IRIs conservados)

| # | Campo | Recurso | Variable | Estado variable | Concepto pista | Cond. R8 |
|---|---|---|---|---|---|---|
| 1 | MUNICIPIOCERTIFICAD | 46977217-9396-4f9c-bddb-6616e82530b4 | MUNICIPIOCERTIFICAD | candidata_sin_definicion_suficiente | municipio | rol+catalogo+contexto |
| 2 | LOCALIDADCERTIFICAD | 46977217-9396-4f9c-bddb-6616e82530b4 | LOCALIDADCERTIFICAD | candidata_sin_definicion_suficiente | localidad | rol+catalogo+contexto |
| 3 | TRIMESTRE | 5772b8ec-e272-4265-a757-f7ddd179fe04 | TRIMESTRE | candidata_sin_definicion_suficiente | tiempo | periodo+unidad |
| 4 | Fecha inscripción en ciclo escolar  señalado | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha inscripción en ciclo escolar  señalado | candidata_sin_definicion_suficiente | tiempo | periodo |
| 5 | Municipio | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Municipio | candidata_sin_definicion_suficiente | municipio | rol+distincion |
| 6 | Fecha de alternativa de titulación de no exigibilidad | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de alternativa de titulación de no exigibilidad | candidata_sin_definicion_suficiente | tiempo | periodo |
| 7 | Fecha de alternativa de titulación de examen prof. | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de alternativa de titulación de examen prof. | candidata_sin_definicion_suficiente | tiempo | periodo |
| 8 | Fecha de titulación del título profesional | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de titulación del título profesional | candidata_sin_definicion_suficiente | tiempo | periodo |
| 9 | Fecha de impresión del título profesional | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de impresión del título profesional | candidata_sin_definicion_suficiente | tiempo | periodo |
| 10 | Fecha de la convalidación | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de la convalidación | candidata_sin_definicion_suficiente | tiempo | periodo |
| 11 | Fecha de la equivalencia | 58f2d5a6-0432-48f1-8a35-a5efcce78bac | Fecha de la equivalencia | candidata_sin_definicion_suficiente | tiempo | periodo |
| 12 | CLUES | 6f39fc5d-e097-4954-8cd7-10e8f9dea541 | CLUES | candidata_sin_definicion_suficiente | unidad-salud | catalogo |
| 13 | MUNICIPIOOCURRENCIA | 6f39fc5d-e097-4954-8cd7-10e8f9dea541 | MUNICIPIOOCURRENCIA | candidata_sin_definicion_suficiente | municipio | rol+catalogo+contexto |
| 14 | MUNICIPIOOCURRENCIAD | 6f39fc5d-e097-4954-8cd7-10e8f9dea541 | MUNICIPIOOCURRENCIAD | candidata_sin_definicion_suficiente | municipio | rol+catalogo+contexto |
| 15 | LOCALIDADOCURRENCIA | 6f39fc5d-e097-4954-8cd7-10e8f9dea541 | LOCALIDADOCURRENCIA | candidata_sin_definicion_suficiente | localidad | rol+catalogo+contexto |
| 16 | LOCALIDADOCURRENCIAD | 6f39fc5d-e097-4954-8cd7-10e8f9dea541 | LOCALIDADOCURRENCIAD | candidata_sin_definicion_suficiente | localidad | rol+catalogo+contexto |
| 17 | Total_Egresos | ad6f77b8-569d-4826-8ce0-3c6efddcb098 | Total_Egresos | fuera_del_nucleo_actual | None | unidad+grano+significado |

### 1. MUNICIPIOCERTIFICAD
- id (columna): https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F103
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/34e6ca285dacc378ab591dc75b24dc56dea4aea3fb7e09dc9eb081dd2c848d43 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F103 | huella fila: 305e3ccb01619f50cab0ded3a82e6211d21b4dcbebecd506e6911f6b489cf8f3
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; representacion no_especificada; concepto generico municipio sin rol (registro/certificacion no documentada). Falla condicion R8 rol y catalogo/contexto: sin funcion, poblacion, catalogo ni version.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 46977217-9396-4f9c-bddb-6616e82530b4 / columna https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F103 / definicion https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F103 (22202305-2d02-4c49-b216-cc98224357f0 fila variable MUNICIPIOCERTIFICAD, conjunto 940de7d8-73ec-4a08-8d26-b7cc97ff17bd). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/940de7d8-73ec-4a08-8d26-b7cc97ff17bd/resource/46977217-9396-4f9c-bddb-6616e82530b4/download/202209281437030-file.xlsx

### 2. LOCALIDADCERTIFICAD
- id (columna): https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F105
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/555c6a5549f72040c6993661dd04e4f915e47e6ccd1adf9f72216d1ea6e101df (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F105 | huella fila: c77a7050ed8af0bf7ab37ca07a830539d720a02adb9c4722d417fcdcdabd4146
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; representacion no_especificada; concepto generico localidad sin funcion ni contexto entidad/municipio. Falla condicion R8 rol, contexto y catalogo.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 46977217-9396-4f9c-bddb-6616e82530b4 / columna https://example.org/mex-ontologi/file-column/46977217-9396-4f9c-bddb-6616e82530b4%2FSINAC%202022%2026-09-22%2F105 / definicion https://example.org/mex-ontologi/definition/22202305-2d02-4c49-b216-cc98224357f0%2F105 (22202305-2d02-4c49-b216-cc98224357f0 fila variable LOCALIDADCERTIFICAD, conjunto 940de7d8-73ec-4a08-8d26-b7cc97ff17bd). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/940de7d8-73ec-4a08-8d26-b7cc97ff17bd/resource/46977217-9396-4f9c-bddb-6616e82530b4/download/202209281437030-file.xlsx

### 3. TRIMESTRE
- id (columna): https://example.org/mex-ontologi/file-column/5772b8ec-e272-4265-a757-f7ddd179fe04%2F2020%2F2
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/3697415e6c6eeb6e37209fee90ed97172e02683e43182ab4e0fe368a8486e740 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2 | huella fila: 799f924f8f10e3831cebdb4fbbc233cb6965caae8902f799881277d12f24320d
- descripcion/evidencia: Trimestre del estrato / Trimestre del estrato
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Trimestre del estrato: evento, cobertura, unidad y representacion no especificadas. Falla condicion R8 periodo y unidad; no se convierte titulo en intervalo.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 5772b8ec-e272-4265-a757-f7ddd179fe04 / columna https://example.org/mex-ontologi/file-column/5772b8ec-e272-4265-a757-f7ddd179fe04%2F2020%2F2 / definicion https://example.org/mex-ontologi/definition/3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99%2F2 (3f6942e3-a9c5-42c0-a38b-2c7aad2a6c99 fila variable TRIMESTRE, conjunto c589afac-79f1-4aac-9ade-e949301bcca3). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/c589afac-79f1-4aac-9ade-e949301bcca3/resource/5772b8ec-e272-4265-a757-f7ddd179fe04/download/conjunto-de-datos-denuncias-1er-trim-2022.xlsx

### 4. Fecha inscripción en ciclo escolar  señalado
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F14
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/8161a023cb3d7a9661132d20b6cbaae6c2884a6b5fa391875fad75d22e6444a7 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F14 | huella fila: 940c1f77837c39791ee0904bbe8123c69948da90bfc9965f38db9aacf6e680ec
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F14 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F14 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha inscripción en ciclo escolar  señalado, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 5. Municipio
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F20
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/83d163255621640274ea2dd6c5eac0ae23213ff74f0965c5af327e60ce9f2759 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F20 | huella fila: ad458441825d75edce0abc7e0082d73b2e3fbc9ec36dbb1687451d73ff9d3eba
- descripcion/evidencia: Municipio donde el alumno / Municipio donde el alumno
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion truncada Municipio donde el alumno; rol no resuelto (residencia vs escuela) y representacion no_especificada. Falla condicion R8 rol; distincion municipio-escuela vs municipio-residencia sin resolver.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F20 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F20 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Municipio, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 6. Fecha de alternativa de titulación de no exigibilidad
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F64
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/363e74572737332fa8262e020123c09df47e02139849195709f6b549d92b8f2f (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F64 | huella fila: 6759b8b1157290027ece3602d7dff3c8609984dfbbf14c5408e656de0fe1b612
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F64 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F64 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de alternativa de titulación de no exigibilidad, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 7. Fecha de alternativa de titulación de examen prof.
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F66
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/28c749dd4423e8bd5173a89fb13c87656a217e7721add9dd94515f14990130d8 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F66 | huella fila: e7e0a6b9c15be989bb0faca42c9b29e55a557cd16b0d417fbb4ba533330970d2
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F66 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F66 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de alternativa de titulación de examen prof., conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 8. Fecha de titulación del título profesional
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F67
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/15f7714d68849ed29af0b5df589e7a1dea9c5c367e1a82a8a6a1a5429e6d6067 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F67 | huella fila: de5cd0cf3209d047b3dbc8b3a76992f8a52c6e1f6d5b20ca452b762f6b10e993
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F67 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F67 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de titulación del título profesional, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 9. Fecha de impresión del título profesional
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F68
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/f11ea089cc117184c6cfef726469e0daa436db1ffd352ae9fdf14a6f7e59e9a7 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F68 | huella fila: 0475086a02e3cd9f2d50ded42b978d782edb3e1ea742601c0c0b40fec2e43d58
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F68 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F68 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de impresión del título profesional, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 10. Fecha de la convalidación
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F69
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/94677a6d587bb1e0562bb676b48d332e98b52e8d06e071794b26470f5934fab0 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F69 | huella fila: a0792669fb9fb33d8e517cc98ef71161b90ee12f10a620cfa84b647522a5c6c1
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F69 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F69 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de la convalidación, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 11. Fecha de la equivalencia
- id (columna): https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F70
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/062509cc9e36f5ba3121d2283e6e733794f3de8ba4f867ea9f2d944f8c2dc380 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F70 | huella fila: 1fe84a93ab498ab4d7dc47f0a54b4ad5278e0d9194e5cc00c06c3028927ff3b3
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar (o inscripcion sin bordes/calendario acreditados); evento, bordes, calendario y representacion no especificados. Falla condicion R8 periodo; un nombre de fecha no acredita intervalo ni formato.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 58f2d5a6-0432-48f1-8a35-a5efcce78bac / columna https://example.org/mex-ontologi/file-column/58f2d5a6-0432-48f1-8a35-a5efcce78bac%2FEstudiantes%202022-2%2F70 / definicion https://example.org/mex-ontologi/definition/8c0e76ff-3a86-4b1d-beee-b04bebe7df8d%2F70 (8c0e76ff-3a86-4b1d-beee-b04bebe7df8d fila variable Fecha de la equivalencia, conjunto e819466c-7282-46c5-84e9-65917dd8cc85). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, evento/bordes/calendario para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/e819466c-7282-46c5-84e9-65917dd8cc85/resource/58f2d5a6-0432-48f1-8a35-a5efcce78bac/download/202209271427270-file.xlsx

### 12. CLUES
- id (columna): https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F38
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/68f886f1a92ce9f61d496f491a455ea41a23c4cf5beb4aa256e6e209bcb4c407 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F38 | huella fila: 1b32ad8dbecd8c74b4f0bfd3497c88a32c8b2f8590a4a9f42f2b10717804423b
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; concepto unidad-salud exige evidencia adicional de pertenencia a catalogo CLUES (base-semantica). Falla condicion R8 catalogo.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 / columna https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F38 / definicion https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F38 (12f684e9-f4d5-4714-933d-aa153a812174 fila variable CLUES, conjunto cd3d6e34-3789-479e-9f2b-a717b8419f9c). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c/resource/6f39fc5d-e097-4954-8cd7-10e8f9dea541/download/202209281428110-file.xlsx

### 13. MUNICIPIOOCURRENCIA
- id (columna): https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F72
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/6aa4d39f3f4bbc60ea7c9fb33afdf57781f562039c628bd181b95f8b7f238d26 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F72 | huella fila: da9a0fcd2979fbcca215523a090a0332d76bfb531c9f92fecae3bd347819febf
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; rol de ocurrencia sugerido solo por nombre; representacion/catalogo no especificados; contexto entidad/municipio no acreditado. Falla condiciones R8 rol, catalogo y contexto.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 / columna https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F72 / definicion https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F72 (12f684e9-f4d5-4714-933d-aa153a812174 fila variable MUNICIPIOOCURRENCIA, conjunto cd3d6e34-3789-479e-9f2b-a717b8419f9c). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c/resource/6f39fc5d-e097-4954-8cd7-10e8f9dea541/download/202209281428110-file.xlsx

### 14. MUNICIPIOOCURRENCIAD
- id (columna): https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F73
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/58b9734fc3425f4bcf2326343b962482a4d4a338ddeda128dcdeecb31a2b1c51 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F73 | huella fila: 45f58439a5c544c88713e5f5ba62c1a0ddf40f9aa6181a506e30f6d50a6e1b85
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; rol de ocurrencia sugerido solo por nombre; representacion/catalogo no especificados; contexto entidad/municipio no acreditado. Falla condiciones R8 rol, catalogo y contexto.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 / columna https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F73 / definicion https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F73 (12f684e9-f4d5-4714-933d-aa153a812174 fila variable MUNICIPIOOCURRENCIAD, conjunto cd3d6e34-3789-479e-9f2b-a717b8419f9c). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c/resource/6f39fc5d-e097-4954-8cd7-10e8f9dea541/download/202209281428110-file.xlsx

### 15. LOCALIDADOCURRENCIA
- id (columna): https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F74
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/a1fbeef646e35e26905c938c32410793d204be75166107ed49ba569318474fb4 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F74 | huella fila: 0485c56408609aa3a1cab7e67e8e7b1f0b4ee7cd6607fbe8c97de194423cac9d
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; rol de ocurrencia sugerido solo por nombre; representacion/catalogo no especificados; contexto entidad/municipio no acreditado. Falla condiciones R8 rol, catalogo y contexto.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 / columna https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F74 / definicion https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F74 (12f684e9-f4d5-4714-933d-aa153a812174 fila variable LOCALIDADOCURRENCIA, conjunto cd3d6e34-3789-479e-9f2b-a717b8419f9c). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c/resource/6f39fc5d-e097-4954-8cd7-10e8f9dea541/download/202209281428110-file.xlsx

### 16. LOCALIDADOCURRENCIAD
- id (columna): https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F75
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/18f1ca2d834cc0f73d707783c2b54c32f439b3cbe9ec73807e3ebac2d92b5289 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F75 | huella fila: 6f76513d06bf1de37df4a91e3103ac0e3782913df200633ca0673e907e345bd4
- descripcion/evidencia: Pendiente de especificar / Pendiente de especificar
- representacion: no_especificada | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Descripcion Pendiente de especificar; rol de ocurrencia sugerido solo por nombre; representacion/catalogo no especificados; contexto entidad/municipio no acreditado. Falla condiciones R8 rol, catalogo y contexto.
- dependencia: Significado candidata_sin_definicion_suficiente, regla pista_nombre_o_clasificador_sin_promocion; bloquea Puerta 1 (promocion exige significado respaldado).
- alcance: Solo recurso 6f39fc5d-e097-4954-8cd7-10e8f9dea541 / columna https://example.org/mex-ontologi/file-column/6f39fc5d-e097-4954-8cd7-10e8f9dea541%2FSEED%2020%2009%2022%2F75 / definicion https://example.org/mex-ontologi/definition/12f684e9-f4d5-4714-933d-aa153a812174%2F75 (12f684e9-f4d5-4714-933d-aa153a812174 fila variable LOCALIDADOCURRENCIAD, conjunto cd3d6e34-3789-479e-9f2b-a717b8419f9c). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Diccionario/codebook/instrumento oficial vinculado a esta edicion local que acredite descripcion, representacion, rol/funcion y catalogo+contexto para esta variable/recurso, + evidencia fisica especifica. Sin pista primaria concreta no se repiten busquedas agotadas.
- esquema: https://datos.sonora.gob.mx/dataset/cd3d6e34-3789-479e-9f2b-a717b8419f9c/resource/6f39fc5d-e097-4954-8cd7-10e8f9dea541/download/202209281428110-file.xlsx

### 17. Total_Egresos
- id (columna): https://example.org/mex-ontologi/file-column/ad6f77b8-569d-4826-8ce0-3c6efddcb098%2FEgresos%20Hospitalarios%202018-2022%2F15
- correspondencia: https://example.org/mex-ontologi/semantic-mapping/e1e53ced78b1a6f64800fa02d6f35d8ee00429b87e9360609cc0e7560ed56bd0 (estado candidata_por_nombre, revision null)
- definicion: https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15 | huella fila: 98c73e56ff407766447b52e08850d0b8669f6979145b4c66fac1f1f83aec9f05
- descripcion/evidencia: Total de urgencias atendidas / Total de urgencias atendidas
- representacion:  | catalogo: (vacio)
- par estructural: nombre-exacto-1:1-mismo-conjunto; revision_explicita null
- motivo no promocion: Variable fuera_del_nucleo_actual, concepto null; nombre Total_Egresos contradice descripcion Total de urgencias atendidas; observacion egresos-descripcion-urgencias pendiente_aclaracion_o_revision. Falla condiciones R8 unidad y grano (poblacion y regla de agregacion no acreditadas).
- dependencia: Significado fuera_del_nucleo_actual; observacion semantica egresos-descripcion-urgencias pendiente_aclaracion_o_revision.
- alcance: Solo recurso ad6f77b8-569d-4826-8ce0-3c6efddcb098 / columna https://example.org/mex-ontologi/file-column/ad6f77b8-569d-4826-8ce0-3c6efddcb098%2FEgresos%20Hospitalarios%202018-2022%2F15 / definicion https://example.org/mex-ontologi/definition/f89137ba-d82e-44fe-80c7-cc355f09f9f5%2F15 (f89137ba-d82e-44fe-80c7-cc355f09f9f5 fila variable Total_Egresos, conjunto 8993c917-47d8-4304-8141-5f481fe04301). No autoriza otra edicion, adopcion global, joins, codigos, vigencias ni identidad de catalogos.
- reapertura: Aclaracion de la fuente que resuelva la contradiccion Total_Egresos vs Total de urgencias atendidas (poblacion, unidad, regla de agregacion) + evidencia fisica especifica de este recurso/columna/edicion. Sin eso, conservar fuera_del_nucleo_actual.
- esquema: https://datos.sonora.gob.mx/dataset/8993c917-47d8-4304-8141-5f481fe04301/resource/ad6f77b8-569d-4826-8ce0-3c6efddcb098/download/202209261836370-file.xlsx

## Impacto
- Columnas: 17 | Recursos: 5 | Consultas nuevas: 0 | Existentes modificadas: 0
- Ninguna consulta validada cambia: queries/portal/semantica_correspondencias.rq y semantica_significados.rq agregan por estado; las 17 siguen contando como candidata_por_nombre/candidata_sin_definicion hasta respaldo. Oportunidades-cruce no es join validado (solo_dimensiones_amplias/candidata_por_validar); no se autoriza cruce por nombre.

## Fuentes primarias y fijos R8
- propuestas/plan-tras-r8/ejecucion-20261024/C1-candidatas/asignacion.json - sha256 f59de03c081aed8efef2d8f87b700a282e15d163b1153924d47cbeaf97484db7 - Asignacion de los 17 casos; IRIs, huellas y estados de partida.
- propuestas/plan-tras-r8/ejecucion-20261024/base.json - sha256 b3ac1894567579899741655fb5f47c2dbc9dc3662f971bd1c2f9246733a7bf9a - Base R8 congelada: conteos 1563/4523/17 y hashes fijos.
- reports/ronda-8.json - sha256 5ac384bc4c253f5310ae69402c8d9249d2ee85082086c2dca85483f8b4b7eacb - Informe R8 cerrado_integrado_validado_y_sincronizado; 28 SINAC, limites, 202 casos.
- reports/pendientes-semanticos.json - sha256 a3f04d9c88d38f60d9ca9bf8fa8b155b27e6ed5f9a4ad11431933b7f87e16c69 - 17 columnas candidata_por_nombre con par 1:1 + fuente_esquema; 5 observaciones.
- data/semantica/cobertura.json - sha256 683f58b24d23b9c97b569ae19dd14ed43b722a08857519766c435e447e9c3638 - 17 correspondencias candidata_por_nombre revision null + 17 variables (16 candidata_sin_definicion + 1 fuera_del_nucleo).
- ontologia/semantica.json - sha256 dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd - Condiciones catalogo/rol/periodo/contexto/grano/unidad, distinciones y observacion egresos-descripcion-urgencias.
- docs/plan-actualizado-tras-r8.md - sha256 751411a04650c484e97161912aadb23d6800b08d24b39df43c5f92c0b8a6ea59 - Puerta 1 y criterios de integracion; C1 informe derivado sin edicion del nucleo.
- docs/plan-actualizado-tras-r8.json - sha256 418cda3ae229df4bebb90a43363ba96e64eec4f631034c975ac5dc18af0473c0 - Conteos fijos: 5523 columnas, 4506 revisadas, 17 candidatas, 833/154/13.
- docs/investigacion-opencode-obscura.md - sha256 23a30b6910bbb67f87784a2ac566e1a25d8865c9d336874f5442db6aa04a15e0 - Reglas web: Obscura solo con pista primaria concreta; resto local; sin contactos externos; Gemma excluido.
- propuestas/plan-tras-r8/ejecucion-20261024/base-semantica.json - sha256 dba467b63286171bb68f5b1400a1ed51bfb99d5663e5b34a36f31fb94953cebd - Glosario local: unidad-salud exige evidencia CLUES; municipio/localidad exigen rol.

## Limites
- Gemma excluido
- Sin contactos externos ni mensajes a publicadores
- Sin promocion por nombre (Puerta 1)
- Sin cambios en produccion/semantica/shapes centrales/manifiestos previos/grafo/Studio
- Sin repetir busquedas agotadas sin pista primaria concreta
- Sin inventar unidades, fechas, jerarquias, codigos, vigencias o equivalencias
- Escritura exclusiva en propuestas/plan-tras-r8/ejecucion-20261024/C1-candidatas/
- Un resultado negativo se limita a lo examinado; no demuestra inexistencia universal

## Condiciones de aceptacion
- Los 17 pares siguen como candidatas mientras el significado no este respaldado
- Cada caso conserva id=columna, IRI de correspondencia, definicion_iri y huella_fila_diccionario verificables contra base R8
- 833 sin definicion / 154 con definicion sin interpretacion / 13 sin diccionario permanecen visibles como estados distintos
- No se anaden unidades, intervalos, codigos, identidad de catalogos, equivalencias ni joins por nombre
- Auditor coteja conteos, IRIs, localizadores y hashes con base congelada; entrega congelada verificable por SHA-256 calculado por codigo
- Sin evidencia nueva, cada pendiente conserva su condicion exacta de reapertura

Propuestas/consultas/fixtures: no aplica. Peticiones web: no aplica (sin pista primaria concreta).
Verificacion: auditor coteja conteos, IRIs, huellas y hashes contra base congelada; congelada.json con SHA-256 por codigo.