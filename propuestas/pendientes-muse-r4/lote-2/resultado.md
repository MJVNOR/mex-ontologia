# Resultado lote-2 (ronda 4) - revision 2

Columnas asignadas: 667 + 41 adicionales = 708. Decisiones: 708 proponer, 0 pendiente, 0 rechazar.
Significados asignados: 28. Decisiones: 21 proponer (reglas r4-lote-2-001 a 021), 7 pendiente.
Vinculos propuestos: 708 (667 intactos + 41 nuevos con dependencia explicita de su regla propuesta). Reglas nuevas: 21. Conceptos nuevos: 16.
Solicitudes de investigacion: 2 (diccionarios con pendientes restantes).

## Verificacion de columnas (sin cambios)

Las 667 columnas mantienen la verificacion de la revision 1: campo en posicion/hoja del esquema capturado, huella_esquema y huella_fila_diccionario recomputadas y coincidentes, definicion unica, nombre unico, ninguna ya revisada. Reutilizacion exacta de 92 reglas vigentes con sus limites.

## Reglas nuevas (21)

Cada regla restringida a la fila exacta (nombre, descripcion, conjunto, diccionario, definicion) con huella_fila_diccionario recomputada desde data/portal/inspecciones. Sentido literal limitado; sin inferir unidades, moneda, vigencia, catalogos ni cruces.

- r4-lote-2-001: ID -> identificador-registro (codigo). Limite: Identificador declarado dentro del conjunto; no homologa con otros ID ni acredita identidad externa.
- r4-lote-2-002: ID -> identificador-registro (codigo). Limite: Identificador declarado dentro del conjunto; no homologa con otros ID ni acredita identidad externa.
- r4-lote-2-003: P3 -> hora-inicio-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-004: P4 -> hora-finalizacion-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-005: P5 -> hora-ultima-modificacion-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-006: P3 -> hora-inicio-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-007: P4 -> hora-finalizacion-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-008: P5 -> hora-ultima-modificacion-encuesta (no_especificada). Limite: Metadato temporal de la fila de respuesta; el formato declarado (DD/MM/AAAA HH:MM) contradice el ejemplo (AAAA-MM-DD HH:
- r4-lote-2-009: P10 -> metodologia-desarrollo-declarada (no_especificada). Limite: Respuesta de texto con la metodologia declarada; valores propios sin normalizar ni catalogo; el ejemplo (Metodologia 1) 
- r4-lote-2-010: P21 -> lugar-almacenamiento-informacion-declarado (no_especificada). Limite: Respuesta de texto con el lugar declarado (ejemplo: Nube); sin normalizar; no describe infraestructura.
- r4-lote-2-011: P22 -> servicios-tic-existencia (no_especificada). Limite: Pregunta de existencia (Si/No) con lista abierta; la descripcion publicada aparece truncada en equipos...; no acredita i
- r4-lote-2-012: P28 -> sistemas-firma-electronica-listados (no_especificada). Limite: Lista de texto declarada; sin normalizar; errata del ejemplo (Sietema) conservada.
- r4-lote-2-013: Convocatoria -> numero-convocatoria-beca (codigo). Limite: Numero declarado (ejemplo 19); no infiere edicion, anio ni vigencia.
- r4-lote-2-014: P9 -> detalle-plan-estrategico-uso-tic (no_especificada). Limite: Texto libre opcional sobre el plan; no verifica el contenido del plan.
- r4-lote-2-015: DELITO -> tipo-delito-victima-anterior (no_especificada). Limite: Texto declarado del tipo de delito (ejemplo HOMICIDIO); sin catalogo; metodologia anterior, no comparable sin acreditaci
- r4-lote-2-016: MODALIDAD -> modalidad-delito-victima-anterior (no_especificada). Limite: Texto declarado de la modalidad (ejemplo CULPOSO); sin catalogo; metodologia anterior, no comparable sin acreditacion.
- r4-lote-2-017: Semestre que cursa -> semestre-en-curso-alumno (no_especificada). Limite: Entero declarado con formato n (ejemplo 9); sistema de semestres sin normalizar.
- r4-lote-2-018: ACTIVIDAD -> actividad-inspeccionada (no_especificada). Limite: Texto declarado (ejemplo TORTILLERIA); sin catalogo.
- r4-lote-2-019: MOTIVO -> motivo-inspeccion-vigilancia (no_especificada). Limite: Texto declarado (ejemplo SEG. A DENUNCIA); sin catalogo.
- r4-lote-2-020: No. -> numero-consecutivo-registro (codigo). Limite: Numero de orden interno (ejemplo 3); sin identidad externa.
- r4-lote-2-021: Estudiante -> numero-consecutivo-registro (codigo). Limite: Consecutivo que identifica el registro del estudiante matriculado (ejemplo 1); orden interno, sin identidad entre archiv

## Conceptos nuevos (16)

identificador-registro; hora-inicio/finalizacion/ultima-modificacion-encuesta (padre tiempo); metodologia-desarrollo-declarada; lugar-almacenamiento-informacion-declarado; servicios-tic-existencia; sistemas-firma-electronica-listados; numero-convocatoria-beca; detalle-plan-estrategico-uso-tic; tipo/modalidad-delito-victima-anterior; semestre-en-curso-alumno; actividad-inspeccionada; motivo-inspeccion-vigilancia; numero-consecutivo-registro.

## Correccion auditoria-a (r4-lote-2-021)

Concepto propio numero-estudiante-matriculado, distinto del ordinal generico, aplicado a la regla r4-lote-2-021 (ID y fuentes intactos), a sus 14 vinculos (columnas Estudiante adicionales) y a sus decisiones/motivos. Las demas reglas no cambian.

## Pendientes restantes (7, con justificacion real)

- P2 Sector (Mejora y TIC): descripcion de una palabra, dominio sin definir; el ejemplo no fija dominio.
- P8 Mejora: pregunta doble (metodologia y documentacion) con ejemplo sin explicar (Metodologia 0.5).
- P13 Mejora: que tipo vs ejemplo Si (tipo contra existencia).
- P36 Mejora: cuantos (conteo) vs Booleano Si/No.
- P39 Mejora: como (manera) vs Booleano Si/No.
- P40 Mejora: identica descripcion que P7 (regla r3a9-085 numerica) pero tipo Booleano; contradiccion directa.


## Columnas adicionales (41)

Todas proponer con dependencia explicita de su regla propuesta (pendiente de auditoria), interpretacion comprobada contra integrador/semantica-propuesta.json: Inspeccion y Vigilancia 2do Trim 2022 ACTIVIDAD x4 / MOTIVO x4 (4 hojas); Matriculas Estudiante x14; Planeacion TIC ID/P3/P4/P5/P9; Becas Convocatoria x5; Victimas DELITO/MODALIDAD; Mejora ID/P3/P4/P5/P10; Matriculas Semestre que cursa; Titulados No. Huellas de esquema y fila recomputadas en los 41 casos; nombres unicos; sin traslape con las 667 originales.
