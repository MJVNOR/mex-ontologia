# Instrucciones de la ronda 4

Trabaja autónomamente hasta terminar tu encargo. Solo puedes escribir en TU carpeta asignada bajo propuestas/pendientes-muse-r4/. Lee asignacion.json si existe, fuentes/manifiesto.json, docs/nucleo-semantico.md y docs/correspondencias-y-cruces-ronda-3.md. No modificar núcleo, scripts centrales, reportes, otras entregas, configuraciones, credenciales ni Studio salvo el evaluador con autorización de pruebas de chat. No lanzar subagentes. No esperar/pollear a otros: termina lo comprobable y deja solicitudes concretas.

Base vigente: 865 correspondencias revisadas, 1212 significados respaldados, 940 conceptos. El informe cobertura-muse.md es histórico (836 correspondencias). Preservar la base actual. Las coincidencias de nombre solo son candidatos. No inferir unidades, escalas, moneda, identidad entre medidas, catálogos nacionales, vigencias, cohortes ni tasas. Conservar códigos, ceros, léxico y calificadores. Una revisión documental no valida datos ni habilita cruces.

## Especialistas lote-1 a lote-6
Revisar TODAS tus columnas y definiciones. Puedes usar scripts locales en TU carpeta para preparar y verificar; agrupa por conjunto/diccionario/recurso para examinar evidencia completa, sin aprobar solo por nombre ni por estar respaldada la definición. Consulta esquemas capturados en data/ y diccionarios, títulos, contexto, unicidad y huellas. Usa reglas previas como formato, no como aprobación automática de filas nuevas. Si falta evidencia, pendiente preciso. Los significados con descripción vacía requieren respaldo explícito vinculado a esa definición, no una interpretación del nombre.

Entrega entrega.json con:
- decisiones_columnas: una por columna asignada, campos columna, recurso, campo, decision (proponer|pendiente|rechazar), definicion_iri (si destino), motivo, evidencia (lista de rutas y localizadores verificables).
- vinculos: formato EXACTO de ontologia/semantica.json vinculos_documentales_revisados, uno por decision proponer. Incluye recurso,campo,columna,diccionario,concepto,descripcion,huella_esquema,huella_fila_diccionario,criterio. Verifica cada huella desde fuentes. Indica definición en decisiones_columnas. Un vínculo que dependa de significado nuevo se marca dependencia explícita.
- decisiones_significados: una por definición pendiente asignada, definicion_iri, decision (proponer|pendiente), motivo, evidencia.
- reglas: reglas propuestas con ID r4-lote-N-..., nombres/descripciones/conjuntos/diccionarios/definiciones restringidos a la fila exacta, huella_fila_diccionario, concepto, representacion, evidencia, limites, criterio. Nunca aprobar solo por clasificador o sugerencia. No cambiar reglas previas.
- conceptos_nuevos: objeto del mismo formato de tres elementos del núcleo (etiqueta, definición, padre); reutilizar conceptos respaldados cuando sea exacto, no aproximado.
- solicitudes_investigacion: dudas con IRIs, fuente probable y documento requerido.

Escribe pendientes.json (detalle de evidencia faltante) y resultado.md con cuentas verificadas. Al terminar, listo.json debe tener sha256 de entrega.json y los conteos. No editar tras listo hasta petición del integrador. Si no puedes completar, registra estado incompleto y conteos exactos; no generar decisiones fingiendo revisión.

## Otros roles
Entregan entrega.json con evidencias, decisiones y pendientes identificados; resultado.md y listo.json con sha256 de entrega.json. Solo el investigador controla Obscura; los demás leen fuentes locales y dejan solicitudes. No contactar publicadores. Fuente nacional no acredita aplicación local ni versión histórica. Auditores solo aprueban versiones SHA exactas: no aprobar conteos ni textos de agentes sin examinar respaldo.
